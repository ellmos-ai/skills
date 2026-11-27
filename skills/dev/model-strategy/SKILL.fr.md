---
name: model-strategy
version: 3.2.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-27
description: "À utiliser pour choisir l'allocation optimale de modèles et d'effort de raisonnement lors d'exécutions multi-agents, de revues ou de tâches de sous-agents (ex. 'quel modèle pour cette tâche', 'définir la stratégie de modèles', 'choisir un modèle de révision', /model-strategy). Définit des affectations basées sur les rôles (penseur, exécutant, réviseur, escalade) et pilote l'effort de raisonnement de manière rentable. Ne PAS utiliser pour la comptabilité des budgets de tokens (utiliser infrastructure/budgetierung)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor, roles]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---


<img src="banner.png" width="100%" alt="model-strategy banner">

> **Français** — Version française officielle de la compétence `model-strategy`.

# Stratégie de changement de modèle (Model-Switching)

> Stratégie multi-modèles basée sur les rôles : configuration plutôt que catalogue textuel, rôles plutôt que tableau figé
> de scores, validation obligatoire des brouillons, changement de fournisseur pour des revues indépendantes.

---

## 0. Configuration

**Les modèles n'ont pas leur place dans ce texte.** Les modèles précis, les fournisseurs et les voies d'appel
disponibles à un instant donné évoluent plus vite qu'une compétence ne peut être maintenue — et diffèrent
selon chaque utilisateur. Cette compétence ne décrit donc que des **rôles et principes** ; le
catalogue effectif réside dans un fichier de configuration placé dans le dossier de la compétence.

### Ordre de chargement

1. **Fichier local** dans le dossier de la compétence : `models.local.json` ou `models.private.json` (ces deux
   motifs de nommage sont déjà déclarés comme privés dans le `.gitignore` de cette bibliothèque,
   `skills/**/*.local.*` et `skills/**/*.private.*` — ne jamais publier, ne jamais commiter).
   S'il existe, il constitue le catalogue faisant foi.
2. **Valeurs par défaut neutres** `models.defaults.json` (suivi par Git, neutre vis-à-vis des modèles) — définit
   la taxonomie des rôles, les dimensions de score, les niveaux de raisonnement, les garde-fous pour les brouillons
   et les règles de protection des mini-exécutants sans toucher aux surcharges locales.
3. **Fichier d'exemple** `models.example.json` dans le même dossier — modèle neutre à emplacements réservés,
   montrant le schéma du catalogue. Sert uniquement de modèle pour créer votre propre fichier local, et non
   de catalogue pour des exécutions réelles.
4. **Relevé en direct (live)**, lorsque les fichiers locaux ou standard sont absents ou incomplets : quels modèles
   le runtime actuel propose-t-il réellement (par ex. l'énumération `model` d'un outil natif de sous-agent,
   `codex debug models --bundled`, une liste de modèles propre à l'application) ? Un modèle deviné vaut
   toujours moins qu'un bref relevé effectif.

**En cas de contradiction, la mesure en direct prévaut.** Un fichier de configuration peut être obsolète (un
modèle a été arrêté, renommé ou remplacé) ; une mesure fraîche sur le runtime lui-même prime sur
toute source textuelle, y compris votre propre configuration locale. Mentionner brièvement la contradiction
et mettre ensuite à jour le fichier de configuration au lieu de l'ignorer silencieusement.

**`deprecated: true` signifie : ne jamais utiliser.** Une entrée marquée `deprecated` reste dans le
catalogue à des fins de reconnaissance/historique (afin qu'un agent puisse identifier une ancienne mention),
mais n'est plus jamais choisie pour une nouvelle tâche — pas même en solution de repli.

### Schéma (voir `models.example.json`)

Chaque entrée du catalogue comporte : `id`, `provider`, `invoke` (modèle d'appel, sans vrais chemins dans
l'exemple), `effort_levels`, `roles` (voir section 1), `strengths`, `weaknesses`, `guardrails`
(restrictions de fiabilité telles que « brouillon uniquement », « ne pas écrire soi-même dans le système de fichiers »,
« validation stricte » — voir section 3), `budget_hint` (renvoi vers la compétence `budgetierung`),
`verified` (disponibilité attestée dans votre propre runtime, voir section 5) et `deprecated`.

---

## 1. Des rôles plutôt qu'une hiérarchie figée de modèles

Le choix d'un modèle répond d'abord à **quel rôle** exige la tâche, puis seulement à quel
modèle concret remplit le mieux et au moindre coût ce rôle à ce moment-là. Les rôles sont plus stables que
les noms de modèles — un modèle peut être remplacé, le rôle demeure.

| Rôle | Question | Caractéristique typique |
|---|---|---|
| **Penseur/Décideur** | Architecture, stratégie, exigences ambiguës, arbitrage d'alternatives | plus coûteux, employé de manière ciblée plutôt qu'en continu |
| **Exécutant continu** | Réalisation courante sur de nombreuses étapes : implémentation, débogage, tâches standard | assez économique pour tourner en continu |
| **Générateur de brouillons** | Première version rapide (design, texte, code, structure, traduction) | rapide, mais soumis par principe à une validation obligatoire (section 3) |
| **Réviseur/Validation** | Vérifie les résultats d'autres modèles | efficacité maximale avec un fournisseur différent de celui du créateur (section 4) |
| **Escalade** | Sollicité uniquement pour l'unique étape la plus difficile | jamais pour toute l'exécution, toujours brièvement justifié |

Un modèle peut assumer plusieurs rôles (par ex. à la fois exécutant continu et réviseur
occasionnel). Quels modèles occupent actuellement quels rôles figure dans la configuration
(section 0), et non ici. Pour la plus petite classe d'exécutants (coût par mission, qualité
par type de tâche), voir la section 7.

### Orientation grossière de difficulté (sans tableau figé)

Un calcul de score sur des dimensions fixes (clarté, complexité, créativité, contexte,
criticité) peut servir d'**orientation approximative** pour distinguer entre exécutant continu et
penseur/escalade — ce n'est pas un mécanisme contraignant qui imposerait automatiquement un modèle :

```
SCORE = (10 - CLARTÉ) + COMPLEXITÉ + CRÉATIVITÉ + CONTEXTE + CRITICITÉ   (0-10 par dimension)
```

Score faible → un exécutant continu ou même un modèle local économique/sans tokens suffit.
Score élevé (exigences systématiquement contradictoires, démonstration mathématique, statistique
à conséquences lourdes) → penseur/escalade, généralement suivi d'une revue. Entre les deux se situe
le cas courant de l'exécutant continu. Le seuil concret à partir duquel on escalade dépend du
catalogue actuel (certains utilisateurs n'ont que deux affectations de rôles, d'autres six) et
n'a donc pas sa place dans un tableau figé au sein de ce texte.

---

## 2. L'effort de raisonnement comme axe indépendant

L'effort de raisonnement (par ex. `low`/`medium`/`high`/`xhigh`/`max`, ou un échelonnement plus fin/différent
selon le fournisseur) est un **axe indépendant du choix de modèle/rôle** : choisir d'abord un modèle
adapté sur le plan métier et disponible en direct pour le rôle, puis adapter sa profondeur de réflexion
à la difficulté.

- Niveaux bas pour la routine et les sous-tâches bien définies.
- Niveaux élevés pour la science, les preuves mathématiques et les décisions d'architecture majeures.
- N'activer un mode en largeur (sous-tâches parallèles clairement séparées plutôt que plus de profondeur
  sur un seul fil) que si le runtime actuel offre un mode dédié et si la règle habituelle de confirmation/coût
  pour les fan-outs importants ou difficiles à estimer est respectée.

**Aucun niveau d'effort n'étend les droits d'écriture, de coût, d'approbation ou de publication.**
Les délégations restent dans les limites de l'autorité existante (voir section 5). Si un niveau n'est
pas disponible dans le runtime actuel, il faut le signaler et se rabattre sur un niveau attesté comme disponible —
jamais déclarer silencieusement le comportement le moins cher comme un succès.

Les étapes isolées longues ou intensives en calcul doivent — indépendamment du niveau d'effort — s'exécuter
sur l'hôte de calcul prévu à cet effet, et non sur la machine interactive locale ; le seuil correspondant
est une règle d'environnement, pas une règle de stratégie de modèles.

---

## 3. Obligation de validation pour les modèles de brouillon

Les modèles au rôle de **Générateur de brouillons** fournissent par principe un brouillon, jamais une livraison
finale — quelle que soit la bonne impression initiale. Ce n'est pas une dévalorisation systématique d'un
modèle particulier, mais une propriété du rôle : les premières versions rapides sont précieuses parce
qu'elles sont rapides, et précisément pour cela plus sujettes aux erreurs.

Il en découle trois règles fixes, indépendamment du modèle concret :

1. **Chaque brouillon est vérifié avant adoption** — par un modèle exécutant continu ou réviseur,
   jamais par simple confiance dans la qualité apparente du brouillon.
2. **Un modèle de brouillon n'écrit de préférence pas lui-même dans le système cible** (système de fichiers cible,
   base de données de production, emplacement publié). Il renvoie le résultat ; un modèle validé
   l'applique. Ce garde-fou figure explicitement dans l'entrée correspondante du catalogue (`guardrails`),
   car son implémentation technique varie selon l'outil.
3. **Les domaines techniques exigeants** (par ex. LaTeX, textes juridiques ou chiffrés, code critique pour la sécurité)
   reçoivent une validation **plus stricte** qu'un texte général, même si le modèle de brouillon donne
   habituellement de bons résultats dans ce domaine.

---

## 4. Changement de fournisseur pour des revues indépendantes

Une revue est d'autant plus probante que le créateur et le vérificateur **n'utilisent pas le même fournisseur ni
le même modèle** — sinon ils risquent de partager les mêmes angles morts.

- **Modèles de revue :**

  | Modèle | Fonctionnement | Quand l'utiliser |
  |---|---|---|
  | **Session-Advisor** | L'utilisateur désigne un réviseur dans la session active, l'agent l'appelle de manière ciblée | Standard pour preuves/architecture |
  | **Orchestrateur comme réviseur** | Le modèle le plus fort/coordinateur relit la sortie d'un sous-agent exécutant | L'orchestrateur est de toute façon plus puissant que l'exécutant |
  | **Agent contradictoire / changement de fournisseur** | Le modèle A (fournisseur 1) travaille, le modèle B (fournisseur 2) vérifie de manière adversariale | Vérification indépendante, deux perspectives, fiabilité maximale |
  | **Recommandation plutôt qu'auto-exécution** | L'agent recommande explicitement : « traiter cette tâche avec le rôle Escalade + Revue » | La session actuelle est trop faible pour l'étape |

- **Quand recourir à une revue :** démonstrations mathématiques, décisions d'architecture à conséquences
  durables, méthodologie statistique/plan d'étude, bugs complexes après plusieurs cycles de débogage
  infructueux, tout brouillon issu de la section 3.
- **Quand aucune revue n'est nécessaire :** code de routine, contenu éditorial, mise en forme ; tâches bien
  définies et non critiques dans le cadre d'une procédure déjà éprouvée.
- **Les faiblesses documentées restent dans la configuration, pas ici** — par ex. « le modèle X ne convient pas
  aux revues mathématiques » doit figurer comme entrée `weaknesses` dans le catalogue, car cela évolue
  avec le modèle et non avec la compétence.

---

## 5. Les droits dépendent de la mission, pas du modèle

Il n'existe volontairement **aucune matrice de permissions par nom de modèle** (quel modèle a le droit de supprimer,
lequel peut exécuter des commandes système). Une telle matrice laisse croire que les droits sont une propriété
du modèle — ils sont une propriété de la **mission et de l'autorité accordée** :

- Ce qu'un agent a le droit de lire, écrire, supprimer ou exécuter résulte du bac à sable (sandbox) du
  runtime actuel, du périmètre de la mission et d'une éventuelle approbation de l'utilisateur — et non du fait
  qu'un modèle cher ou bon marché soit en train de répondre.
- Les garde-fous du catalogue (champ `guardrails`) sont des **indications de fiabilité**, et non une extension
  ou restriction de droits : « brouillon uniquement » indique quel degré de confiance accorder au résultat,
  non ce qui serait techniquement permis.
- Une délégation (à un sous-agent, à un agent externe, à un autre modèle) reste dans les limites de l'autorité
  de l'exécution délégante. Elle n'élargit rien.

### Escalade et désescalade (schémas, pas noms de modèles)

- **Vers le haut (le rôle passe à Penseur/Escalade) :** décision d'architecture requise,
  plusieurs systèmes doivent être intégrés, exigences contradictoires/floues, planification stratégique
  nécessaire, bug critique après plusieurs cycles infructueux.
- **Latérale (autre rôle, même niveau) :** recherche hors domaine, revue indépendante,
  outil spécialisé d'un autre fournisseur.
- **Vers le bas (désescalade) :** le concept est défini → l'exécutant continu prend en charge l'implémentation ;
  la tâche est triviale/répétitive → un modèle moins cher prend le relais ; tâche purement textuelle sans
  accès aux outils → un modèle local/sans tokens prend le relais, s'il est disponible dans l'inventaire et
  attesté (`verified: true` dans le catalogue).

### Règle de transparence en cas de changement de modèle

**Tout changement silencieux de modèle par rapport à la dotation configurée doit être signalé.** Si un runtime
choisit de sa propre initiative (quota, disponibilité, défaut interne) un autre modèle que celui défini dans
`models.local.json`/`models.private.json`, ce n'est pas une erreur, mais cela doit être mentionné de manière
transparente — jamais déclaré silencieusement comme le succès de la stratégie prévue. Cela vaut quels que
soient les deux modèles concernés ; les versions antérieures de cette compétence citaient ici une paire de
modèles précise comme précédent — la règle est désormais volontairement neutre afin de ne dépendre d'aucun
changement de modèle particulier.

---

## 6. Quotas, déroulement et découpage des rôles — renvois plutôt que double maintenance

Cette compétence répond à **quel rôle** et **avec quel soin (effort, revue)**. Deux questions voisines
ne sont volontairement pas traitées ici pour éviter toute maintenance en double :

- **« À quelle fréquence puis-je utiliser un modèle coûteux/rare ? »** → Compétence `budgetierung` : négociation
  de quotas par fenêtre temporelle, compte courant, pré-procédure en pièces de puzzle avant escalade.
  Le champ `budget_hint` du catalogue renvoie exactement ici.
- **« Comment découper la tâche, déléguer les lots de travail et réceptionner les résultats ? »** →
  Compétence `orchestrator` (protocole de découpage, commande, réception) ou compétence
  `choose-your-orchestrator` (lorsque la forme d'orchestration adaptée doit d'abord être négociée —
  contrat de session pour les emplacements de modèles, le parallélisme, la profondeur de spawn, les limites
  d'écriture, la réception et l'escalade).

---

## 7. Petits exécutants (classe Haiku) : qualité et coûts par mission

Mesure 2026-10 (Haiku 5.5, `claude-haiku-5-5` ; famille alors composée de Fable 5.1, Opus 5.5, Sonnet 5.5,
Haiku 5.5 ; environ 30 missions, comparées à Sonnet 5.5). Tarifs par million de tokens (état 2026-10-06) :
Haiku 5.5 0,10 $/0,50 $ (jusqu'à 100k en prompt), Sonnet 5.5 2 $/10 $, Opus 5.5 4 $/20 $ — par token ≈ 1/20 de
Sonnet, 1/40 d'Opus. Les tarifs et constats deviennent caducs avec les modèles : en cas d'écart, la mesure
fraîche fait foi (section 0).

**Piège d'efficacité : bon marché par token ≠ bon marché par mission.** Un sous-agent Haiku dans le harness
Claude Code consomme ~180–360k tokens par mission, même pour un fichier de 193 lignes. La charge de base
(~45–65k tokens par tour) provient du harness (listes de compétences/agents/MCP, hooks de démarrage), et non du
`CLAUDE.md` du projet (répétition après raccourcissement du fichier de règles : 186k → 182k). Contre-mesures :

- **Regrouper :** plusieurs sous-tâches par exécutant afin de ne payer la charge de base qu'une fois ; jamais
  un sous-agent par document.
- **Exécutant headless naïf** pour les tâches de masse à entrée fixe : `claude -p --model haiku
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' --disable-slash-commands --tools Read,Write`
  → mesuré à 0,018 $ par traduction de README (même profil de tokens : Sonnet ≈ 0,35 $, Opus ≈ 0,66 $).
  `--bare` (sans `CLAUDE.md` ni hooks) économise davantage, mais requiert une clé API. Pour de très gros
  volumes, préférer API/Batch au sous-agent.
- **Résultat sous forme de fichier plus message de 3–5 lignes**, peu d'appels d'outils.

**Qualité par type de tâche (mesurée) :**

| Type de tâche | Constat |
|---|---|
| Vérification de fidélité ancien → nouveau (essaim de contrôle) | très bon ; a trouvé 2 erreurs critiques manquées par l'auteur et le script de test ; ~6 % de faux positifs |
| Revue de code sur fichier unique | bon ; 8 vrais constats contre 6 pour le modèle de référence, 4 constats supplémentaires sur un second fichier ; chaque constat nécessite une contre-vérification |
| Traduction (par ex. README DE→EN) | bon (~9/10) ; parité complète ; les termes techniques fluctuent entre exécutions → glossaire ; libellés UI/emplacements réservés ont besoin de contexte |
| Alignement Doc ↔ Code | bon ; aucun faux positif sur les échantillons |
| Cartographie des doublons | exploitable ; ~85–90 % de rappel par rapport au modèle de référence, ~1 faux positif par section |
| Petit correctif clairement spécifié avec test | bon |
| Mécanique (tests en worktree, rebase, PR, état des lieux) | bon ; signale honnêtement instabilité et blocages, ne contourne aucun garde-fou |

**Recommandations :**

1. Traductions en masse (docs, README, chaînes i18n) : très adapté, avec fichier de glossaire, règle de parité 1:1 et sondage par un modèle plus fort ; regrouper plusieurs documents par exécutant ou utiliser l'exécutant headless naïf ou l'API Batch — jamais un sous-agent par document.
2. Essaims de contrôle (fidélité ancien→nouveau, Doc↔Code, avant/après, existence de liens/chemins) : le meilleur usage — second lecteur indépendant qui repère ce qui échappe à l'auteur.
3. Mettre à jour une base documentaire selon le schéma *petit modèle cartographie → exécutant continu rédige → petit modèle vérifie → penseur valide* ; ne jamais laisser le petit modèle réécrire seul des textes normatifs.
4. Pré-vérification de revue de code par fichier et petits correctifs clairement spécifiés avec test.
5. Mécanique : exécutions de tests, relectures (readbacks), analyse de journaux, états des lieux via `git grep`.
6. **Pas** pour les décisions d'architecture, de fusion (merge) et de sécurité, ni pour les fichiers de règles normatifs ou les grandes synthèses transversales.
7. Règles d'efficacité : regrouper les tâches par exécutant, résultat en fichier plus message de 3–5 lignes, peu d'appels d'outils ; ne jamais adopter de résultats sans vérification (la section 3 s'applique ici aussi).

**Règle d'emploi :** Le modèle est un outil de brouillon et de vérification (rôle *Générateur de brouillons* ou
second lecteur en essaim de contrôle, section 1) — ni instance d'acceptation, ni exécutant continu standard.
Le travail productif passe par l'exécutant continu de la configuration ; la petite classe uniquement sur
commande explicite de l'utilisateur. Les tâches de masse à entrée fixe passent de préférence par l'API
(Batch, ≈ 0,001 $ par README), et non comme sous-agent dans le harness.

---

## Journal des modifications

### 3.2.0 (2026-11-27)
- Externalisation des valeurs par défaut neutres de taxonomie, score, effort et garde-fous dans `models.defaults.json` (indépendamment de `models.local.json` / `models.example.json`).

### 3.1.1 (2026-11-22)
- Mention linguistique corrigée.

### 3.1.0 (2026-10-11) — Petits exécutants (classe Haiku) mesurés
- Nouvelle section 7 : Haiku 5.5 comme exécutant, mesure 2026-10 (qualité par type de tâche, tarifs, recommandations).
- Piège d'efficacité documenté : sous-agent ~180–360k tokens par mission (charge de base du harness ~45–65k par
  tour) ; contre-mesures : regroupement, exécutant headless naïf (0,018 $ par traduction de README), API/Batch pour
  les tâches de masse.
- Règle d'emploi : petite classe uniquement sur commande explicite, travail productif via l'exécutant continu.
- Liste du schéma en section 0 complétée par `verified` (champ déjà utilisé dans `models.example.json` et en section 5).

### 3.0.0 (2026-10-03) — Rupture : catalogue de modèles externalisé
- Catalogue de modèles retiré du texte de la compétence et déplacé vers `models.example.json` (suivi par Git, neutre)
  plus un fichier de configuration local non publié (`models.local.json` / `models.private.json`, déjà déclaré privé via `.gitignore`).
- Ordre de chargement documenté : fichier local → fichier d'exemple → relevé en direct ; en cas de contradiction,
  la mesure en direct l'emporte ; `deprecated: true` n'est jamais utilisé.
- Hiérarchie figée de niveaux 1 à 4 et tableau fixe score→modèle remplacés par cinq rôles
  (Penseur/Décideur, Exécutant continu, Générateur de brouillons, Réviseur/Validation, Escalade) ; le score
  ne reste qu'une orientation approximative.
- Obligation de validation des modèles de brouillon ajoutée en section dédiée (contrôle obligatoire, pas de droits
  d'écriture directe dans le système cible, validation plus stricte dans les domaines techniques exigeants).
- Changement de fournisseur pour des revues indépendantes érigé en principe au lieu de paires de modèles fixes.
- Matrice de permissions par nom de modèle supprimée — les droits dépendent de la mission/autorité, pas du modèle ;
  les garde-fous sont des indications de fiabilité, pas des clauses de droits.
- Voie d'appel concrète Companion-1.0.4, chaîne d'escalade fixe Ollama/Haiku et règle de précédent Fable/Opus-4.8
  retirées ou transformées en une règle neutre « tout changement silencieux de modèle doit être signalé ».
- Quotas renvoyés vers la compétence `budgetierung`, déroulement de délégation et découpage des rôles vers
  `orchestrator` et `choose-your-orchestrator` au lieu d'être maintenus en double.

### 2.2.0 (2026-09-02)
- Ajout de l'effort de raisonnement comme axe orthogonal au choix de modèle (`xhigh`, `max` ciblé,
  `ultracode` orienté largeur).
- Clarification du seuil de calcul local ainsi que des limites de runtime, coûts et autorité.

### 2.1.0 (2026-07-02)
- RÈGLE DE PRÉCÉDENT : un modèle précis en remplace un autre dans toutes les recommandations niveau 4 / réviseur /
  preuve (décision utilisateur ; neutralisée depuis la version 3.0.0).
- Ajout de l'avertissement de changement silencieux de modèle.

### 2.0.0 (2026-06-12)
- Délégation inter-agents : agents externes et un modèle local comme cibles de routage.
- Appariement de conseiller (Advisor) : 4 modèles (Session-Advisor, Orchestrateur comme réviseur,
  Agent contradictoire, Recommandation utilisateur).
- Matrice d'accessibilité : lancement par sous-agent vs utilisateur uniquement documenté.
- Escalade latérale vers des agents externes (recherche, revue).
- Seuils de score étendus.

### 1.0.0 (2026-03-15)
- Portage depuis BACH v3.8.0 (`ing-strategie` v2.0.0).

---

*Porté depuis BACH v3.8.0 | Basé sur les rôles depuis la v3.0.0*
