---
name: skill-extractor
version: 1.3.2
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-11-22
description: "Utilisez cette compétence pour /skill-extract ou pour extraire d'un historique de chat (session courante ou fichiers de transcription) une compétence réutilisable — ou améliorer une compétence très proche au lieu de créer un doublon. Couvre aussi les lots sur de vieilles transcriptions ; pour des automatisations récurrentes, utilisez workflow-extract."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, extraction, transcript, chatverlauf, meta, dedup, neutralisierung, workflow]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="skill-extractor banner">

> **Français** — Version française officielle de la compétence `skill-extractor`.

# Skill-Extractor — Extraire des compétences depuis les historiques de discussion

## Vue d'ensemble et finalité

De précieuses méthodes de travail naissent au fil des sessions : un problème a été résolu laborieusement, l'utilisateur a corrigé plusieurs fois, au bout du compte un processus fonctionnel émerge — et la fois suivante, l'agent repart de zéro. Cette compétence distille d'un historique de conversation ce qui mérite d'être conservé et en fait une compétence conforme aux conventions de la bibliothèque locale de compétences. Principe directeur : **étendre avant de créer à neuf** — s'il existe déjà une compétence très similaire, on l'améliore au lieu de générer un doublon.

Délimitation : le résultat ici est une **compétence appelable** (capacité/procédure qu'un agent charge au besoin). Si l'historique doit devenir une **automatisation autonome** (prompt récurrent, cron, planification), utilisez la compétence sœur `workflow-extract`.

## Déroulement

### 1. Déterminer la source

Trois formes d'entrée :

| Source | Accès |
| --- | --- |
| **Session courante** | Utiliser directement le contexte de conversation — aucun fichier requis |
| **Transcriptions individuelles** | Lire les fichiers ; emplacements et analyse : `transcript-quellen.md` |
| **Lot / Bulk (nombreux anciens historiques)** | D'abord réduction des données via des sous-agents, puis extraction : section « Mode Bulk » |

Pour le format JSONL de Claude Code, utiliser d'abord `scripts/segment_stations.py`. Le script forme des stations déterministes entre points de rapport sans copier de texte de chat ni de paramètres d'outils dans la sortie. Les marqueurs, options et format de sortie figurent dans `transcript-quellen.md`.

### 2. Repérer ce qui mérite d'être extrait

Toutes les sessions ne contiennent pas une compétence. Cherchez ces signaux — ils révèlent où se cache un savoir chèrement acquis et réutilisable :

- **Répétition :** Le même processus s'est produit ≥ 2 fois (dans cette session ou sur plusieurs sessions).
- **Boucles de correction :** L'utilisateur a réajusté l'agent plusieurs fois jusqu'à ce que ce soit bon — la version finale est le distillat, les corrections sont les justifications (« pourquoi ainsi »).
- **Marqueurs explicites :** « retiens ça », « on fait toujours comme ça », « la prochaine fois fais directement ainsi ».
- **Chaînes d'outils :** Une séquence non évidente d'outils/commandes qui a fonctionné (y compris les impasses à éviter).
- **Règles de décision :** Critères selon lesquels un choix a été fait entre des alternatives.

Consigner par candidat : déclencheur (quand en a-t-on besoin), déroulement (étapes), justifications (pourquoi ainsi et pas autrement), pièges (ce qui a échoué), format du résultat.

**Pour les transcriptions JSONL, ne pas mener la recherche à la main.** `scripts/score_stations.py` prend les stations de l'étape 1 et fournit, au lieu d'occurrences dans le texte brut, une **liste notée de candidats** :

```bash
python scripts/score_stations.py <transcription.jsonl> [autres.jsonl ...] --candidates-only
```

L'évaluation repose sur une seule observation : **la suite (l'enchaînement) est l'étiquette.** Une station est jugée d'après ce que dit l'humain ensuite — s'il confirme, la procédure était solide ; s'il corrige, une règle manquait ; s'il change de direction, l'approche était mauvaise. Ainsi, les signaux listés plus haut deviennent comptabilisables et non plus seulement remarqués :

| Signal de la liste ci-dessus | Équivalent machine |
| --- | --- |
| Boucles de correction | Type d'enchaînement `KO`, pondéré avec plafond |
| Répétition | Même signature de chaîne d'outils dans ≥ 2 sessions |
| Chaînes d'outils | Longueur de chaîne ≥ 3 étapes |
| Impasses | Type d'enchaînement `RA` — pénalité, reste précieux à lire comme piège |
| Pièges | `is_error` suivi d'une correction (erreur sans correction non comptée) |

Une **séquence de stations** est l'unité, pas la station isolée — une compétence correspond à une section menée à terme, pas à un simple point de rapport.

**Les limites de l'automatisme doivent être lues avec esprit critique.** Le type d'enchaînement provient d'un préfiltre déterministe par listes de mots ; ce qui n'est pas univoque reste `unknown` plutôt que d'être deviné. Les demandes de précision claires sont reconnues comme `NT` : avec point d'interrogation, avec quelques débuts de question clairs comme « peux-tu … » ou « devons-nous … » et pour des ajouts comme « encore quelque chose sur … ». Les messages d'état vagues sans question, correction ni ordre reconnaissable restent volontairement `unknown`. Si `classified_ratio` descend sous 0,5, la sortie signale elle-même que le classement n'est pas fiable — reclassifier alors manuellement les enchaînements des meilleurs candidats avant de récolter. Un score est une recommandation de lecture, pas une décision de sélection : l'étape 3 reste obligatoire.

**Tout enchaînement n'est pas un prompt.** Les tours vides et enveloppes machine (notification de tâche, message de coéquipier, commande slash nue) ne portent pas de type de prompt et sont classés `empty` ou `non_prompt` — ils ne figurent **pas** au dénominateur de `classified_ratio`. Sur trois transcriptions réelles, cela représentait 127 enchaînements sur 246 ; les compter comme des échecs de classification faisait chuter l'indicateur de 0,64 à 0,45 et aurait lancé un modèle sur des entrées où il n'y a rien à reconnaître.

**Niveau modèle optionnel — et pourquoi il est rarement nécessaire.** `--classifier-cmd "<commande>"` transmet les `unknown` restants à une commande externe (liste JSON en entrée sur `stdin`, liste JSON d'étiquettes de même longueur en sortie sur `stdout` ; tout ce qui sort des sept types reste `unknown`). C'est délibérément une **commande plutôt qu'un adaptateur fournisseur** : cette bibliothèque est neutre vis-à-vis de l'utilisateur et n'embarque aucun point de terminaison de modèle. `follow_up_source` et le bloc `classification` indiquent quelles étiquettes proviennent du modèle.

> **Confidentialité :** C'est la seule étape où du texte de prompt quitte le processus. Le préfiltre ne lit le texte que localement et ne sort que des étiquettes ; une commande de classification peut le transmettre librement. C'est pourquoi cette étape est **désactivée** par défaut.
>
> **Mesuré avant d'activer** (60 enchaînements ouverts, 57 étiquetés à la main, Gemini 3.7 Flash) : **70,2 % de réussite** — et dans **0 %** des cas le modèle a honnêtement répondu « je ne sais pas ». Il devine toujours. Les erreurs ne sont pas uniformément réparties : 12 sur 17 ont atterri sur `NM`, dont 3 sur 4 `KO` mal classés. Or c'est précisément `KO` qui attribue les points dans le score — un modèle qui range les corrections dans `NM` fausse exactement le classement pour lequel on l'avait sollicité. Pour `--min-score`, cet état n'est **pas** exploitable.

Qui veut améliorer le taux dispose d'un levier moins coûteux dans le préfiltre : les prompts d'ordre (`ticket:`, `erstelle`, `starte`, …) ont capté dans le même échantillon **14 `SP` sur 25 avec 100 % de précision**, alors que le modèle en trouvait 15 tout en corrompant 17 autres étiquettes.

### 3. Garde-fou de déduplication : étendre avant de créer à neuf

Avant d'écrire quoi que ce soit, examiner l'écosystème existant :

1. Rechercher les mots-clés du candidat dans les répertoires de compétences (dossier de déploiement de l'agent, par ex. `~/.claude/skills/`, et — s'il existe — la bibliothèque de compétences organisée comme source de vérité ; de même pour les compétences de plugins enregistrées).
2. **Lire réellement** les 2 à 3 compétences les plus proches, ne pas se limiter aux noms.
3. Décider :

| Constat | Action |
| --- | --- |
| Le candidat est déjà couvert sur le fond | **Étendre :** intégrer les éléments manquants dans la compétence existante (nouvelle section, nouvelle technique, nouveau piège), incrémenter la version MINOR, entrée dans le changelog |
| Chevauchement partiel, mais cœur différent | **Nouvelle compétence** avec renvoi (« Compétences apparentées ») vers les voisines — ne pas dupliquer le contenu, mais référencer |
| Rien de comparable | **Nouvelle compétence** |

Règle empirique : si plus de la moitié du candidat figure déjà dans une compétence existante, on étend. Un parc de compétences plein de quasi-jumeaux vaut moins qu'une seule compétence bien entretenue.

### 4. Neutraliser

La matière brute est truffée de détails propres à la session. Avant rédaction, abstraire selon les règles de `neutralisierung.md` : séparer la mécanique (universelle) de la configuration (spécifique à l'utilisateur ou au système), remplacer les chemins/hôtes/noms concrets par des marqueurs ou un bloc de configuration clairement balisé. Objectif : la compétence fonctionne pour d'autres utilisateurs, d'autres systèmes, d'autres projets.

### 5. Rédiger la compétence

- **Format :** Respecter les conventions de la bibliothèque cible (frontmatter, schéma de nommage, langue, changelog). Dans cette bibliothèque : `docs/CONVENTIONS.md` (en-tête YAML complet, nom en kebab-case, allemand primaire, Semantic Versioning).
- **Formuler `description` de manière « incitative » (pushy) :** La description est le mécanisme déclencheur. Y inscrire aussi bien CE QUE fait la compétence que QUAND elle doit s'appliquer (formulations typiques des utilisateurs) — les compétences ont plutôt tendance à se déclencher trop rarement que trop souvent.
- **Le pourquoi avant le quoi :** Reprendre dans la compétence les justifications issues des boucles de correction. Une compétence qui se contente de lister des étapes est mal appliquée au premier cas particulier ; une compétence qui explique le pourquoi reste transposable.
- **Documenter les pièges :** Les impasses de la session valent de l'or — les intégrer dans une section « Signaux d'alerte » ou « Pièges ».
- **Rester concis :** Sous ~300 lignes ; déporter le matériel détaillé dans des fichiers de référence pointés par `SKILL.md`.

### 6. Wrapper de commande (optionnel)

Si la compétence doit être appelée régulièrement de façon directe, créer une commande slash (dans Claude Code : court fichier Markdown dans `~/.claude/commands/<nom>.md` qui pointe vers la compétence et transmet les arguments). Convention : commande = point d'entrée mince, le contenu vit dans la compétence.

### 7. Enregistrer et tester

- Déposer dans la bibliothèque (bonne catégorie) et déployer (ici : `python skill_sync.py deploy <nom>` — l'installation initiale requiert le nom explicite).
- Test de déclenchement : formuler 2 à 3 prompts réalistes devant déclencher la compétence et vérifier si la description accroche.
- Pour une boucle d'évaluation complète (cas de test, comparaison de base, optimisation de description), utiliser `skill-creator` s'il est installé — la présente compétence est l'extracteur, pas le banc d'essai.
- Maintenance de l'index et du routage : mettre à jour les compétences d'index/recherche de compétences s'il en existe (ici : `code-skill-index`, table de routage `skill-finder`).

## Mode Bulk : nombreux anciens historiques de chat

Les transcriptions sont volumineuses (souvent > 100k tokens) ; ne jamais tout charger brut dans un seul contexte. Map-Reduce via des sous-agents (modèle : compétence `swarm-operations`, essaim de tâches) :

1. **Inventaire :** Lister les fichiers de transcription (emplacements : `transcript-quellen.md`), regrouper par projet/période. Pour les très grands volumes, réduire d'abord avec les collecteurs/extracteurs existants (par ex. jeux de données Prompt-Listener/étude ne contenant que les prompts utilisateur) — les prompts utilisateur + corrections portent l'essentiel du signal.
2. **Map :** Un sous-agent par lot avec une consigne étroite : « Lis ces transcriptions, signale les candidats de compétences sous forme de liste compacte (déclencheur, déroulement, justifications, pièges, session preuve) » — ne renvoyer que les distillats, jamais le texte brut.
3. **Reduce :** Fusionner les listes de candidats, regrouper par thèmes, fusionner les doublons. La fréquence compte : un motif qui apparaît dans 5 sessions est un candidat plus fort qu'une astuce isolée.
4. **Gate + Construction :** Parcourir les étapes 3 à 7 du flux normal pour les meilleurs candidats. Soumettre à l'utilisateur une liste numérotée de candidats avant la construction en masse — sinon l'extraction en masse produit des déchets de compétences.

## Exemple et application

```text
Utilisateur : « Nous avons maintenant analysé trois fois des factures PDF selon le même schéma —
fais-en une compétence. »

1. Source : session courante. Signal : répétition (3×) + correction (« Toujours écrire
   les montants comme nombre décimal avec point, jamais avec virgule »).
2. Garde-fou de déduplication : la recherche trouve la compétence `pdf` (générique, génération/extraction) —
   le cœur ne se recouvre pas (ici : schéma de facture + règles de validation) → nouvelle compétence
   `invoice-parsing` avec renvoi vers `pdf`.
3. Neutraliser : dossier de dépôt concret et nom d'entreprise → bloc de configuration.
4. Écrire la compétence : tableau de schéma, correction virgule/point comme piège,
   Changelog 1.0.0. Test de déclenchement avec « lis cette facture ».
```

## Signaux d'alerte (Red Flags)

| Pensée | Réalité |
| --- | --- |
| « Je crée vite une nouvelle compétence » | Garde-fou de déduplication d'abord — étendre avant de créer à neuf. |
| « Je laisse les chemins en dur, c'est pour ce système » | La neutralisation est obligatoire ; le concret va dans un bloc de configuration. |
| « L'historique est long, je résume de mémoire » | Rechercher explicitement les signaux (corrections, marqueurs) — la mémoire lisse précisément les passages qui donnent sa valeur à la compétence. |
| « Chaque session donne une compétence » | Sans signal de répétition/correction/marqueur : pas de compétence. |

## Compétences apparentées

- `workflow-extract` — même extraction, mais la cible est une automatisation autonome.
- `skill-explorer` — audit/nettoyage du paysage de compétences (utilise le garde-fou de déduplication à grande échelle).
- `skill-creator` (Plugin) — boucle d'évaluation et optimisation de description pour compétences finalisées.
- `swarm-operations` — schéma d'essaim pour le mode Bulk.

## Journal des modifications

### 1.3.2 (2026-11-22)
- Indication de langue corrigée

### 1.3.1 (2026-09-14)
- **Préfiltre NT conservateur pour les enchaînements humains ouverts :** Des ajouts comme « encore quelque chose sur … » ainsi que des questions claires par point d'interrogation ou amorce interrogative nette sont reconnus comme `NT`. Les marqueurs spécifiques déjà actifs gardent la priorité.
- **Pas de fausse précision sur les messages d'état :** Les phrases sans question, correction ni ordre reconnaissable restent `unknown` ; la couverture supplémentaire n'invente aucun type de prompt.

### 1.3.0 (2026-09-13)
- **Les enchaînements qui ne sont pas des prompts ne comptent plus comme des échecs de classification.** `prompt_kind()` sépare `empty` (tour vide), `non_prompt` (enveloppe machine, commande slash nue) et `human` ; seuls ces derniers figurent au dénominateur de `classified_ratio`. Sur trois transcriptions réelles, 127 des 246 enchaînements n'étaient pas des énoncés — les comptabiliser avait abaissé l'indicateur de 0,64 à 0,45 et déclenché l'avertissement « classement non fiable » alors que le préfiltre n'avait aucun défaut. Effet secondaire : les textes machine n'étaient plus faussement classés `BE`/`KO` via leurs marqueurs lexicaux.
- **Prompt d'ordre (`SP`) dans le préfiltre.** S3 avait mesuré qu'un prompt de démarrage n'est pas identifiable linguistiquement — cela vaut pour le démarrage de SESSION, pas pour l'ORDRE (`ticket:`, `erstelle`, `starte`, …). Sur 57 enchaînements étiquetés à la main : 14 sur 25 `SP` avec 100 % de précision. Vérifié **en dernier** afin que « crée X, mais pas comme ça » reste une correction.
- **Niveau modèle optionnel `--classifier-cmd`** derrière le préfiltre : une commande (JSON en entrée, JSON en sortie), pas d'adaptateur fournisseur — la bibliothèque reste neutre vis-à-vis de l'utilisateur. Un seul appel par lot pour tous les enchaînements ouverts ; différence de longueur, JSON invalide ou code d'erreur ne provoquent jamais de décalage d'étiquettes. `follow_up_source` et le bloc `classification` indiquent l'origine de chaque étiquette.
- **Mesure sur le niveau modèle qui plaide contre son usage généralisé** (60 enchaînements ouverts, Gemini 3.7 Flash) : 70,2 % de réussite, 0 % de « unknown » honnête, et 12 erreurs sur 17 atterrissent sur `NM` — dont 3 des 4 `KO` déplacés, soit exactement la classe qui porte le score. Insuffisant pour calibrer `--min-score` ; le niveau reste opt-in et est signalé comme transition de confidentialité.
- Taux sur ces trois mêmes transcriptions : **0,451 → 0,644**, sans appel de modèle.

### 1.2.0 (2026-09-12)
- Ajout de l'évaluation de valeur de récolte des séquences de stations (`scripts/score_stations.py`) : signaux durs par station, classification d'enchaînement selon les sept types de `promptarchaeologie`, score et liste de candidats. L'étape 2 « Repérer ce qui mérite d'être extrait » reçoit ainsi une liste notée au lieu d'une recherche de signaux dans le texte brut. La sortie reste sans contenu ; `classified_ratio` indique jusqu'où l'automatisation est fiable au lieu de simuler un classement (Ticket T-20260831-971906399, S3/S4 ; décision utilisateur D-20260906-012).
- `station-skill-mask-v1.schema.json` : `$schema`/`$id` restaurés — les deux clés avaient été victimes d'une expansion de variable shell lors de la création (`""` comme clé).

### 1.1.0 (2026-08-31)
- Ajout d'un segmenteur de stations déterministe et sobre en données pour JSONL Claude Code.

### 1.0.0 (2026-07-03)
- Version initiale. Issue du mandat visant à abstraire systématiquement les automatisations Codex et les historiques de discussion en compétences.
