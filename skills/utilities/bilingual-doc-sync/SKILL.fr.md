---
name: bilingual-doc-sync
version: 1.5.1
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-10-15
description: "Synchroniser des versions linguistiques parallèles d'un document (article DE/EN, README + README_de, SKILL.md + SKILL.en.md, textes de site web) : compléter la version manquante, vérifier le parallélisme des sections, corriger les divergences — avec une règle claire de langue directrice et un rétrotransfert contrôlé lorsque la version secondaire résout mieux un point. Utilisez cette compétence pour « DE et EN sont-ils synchrones ? », « reprends la version anglaise/allemande », « la traduction est obsolète », pour les articles/README/compétences bilingues, ou comme contrôle périodique sur un ensemble de documents. Inclut également l'audit d'expansion : évaluer si un projet/document mérite D'AUTRES langues (aptitude i18n selon le public cible, préparation technique, sans traduction de masse aveugle)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [übersetzung, zweisprachig, synchronisation, paper, readme, i18n, dokumentation]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [markdown-it-py]

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cc96429f6f5663a7890b76c0958f3c19c1856fccbd65cd0505a75f831260d65d
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T11:59:14.018622+00:00"
---
<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">
# Bilingual-Doc-Sync — maintenir synchrones les versions linguistiques parallèles

## Objectif

Les documents tenus dans deux langues divergent insidieusement : la version activement modifiée
s'étoffe, l'autre devient obsolète — jusqu'à ce que « traduction » ne soit plus qu'un nom. Cette
compétence transforme la vérification de synchronisation en un processus défini, avec une décision
préalable déterminante : **quelle version fait référence ?** Sans règle de langue directrice, chaque
divergence devient une décision au cas par cas et la comparaison n'est pas reproductible.

## Déroulement

### 0. Détecter le contenu monolingue (AVANT toute comparaison)

Une divergence n'est pas toujours « obsolète » — parfois il s'agit d'un **contenu nouveau et réel qui
n'existe jusqu'ici que dans une seule version** (contribution externe/PR dans une langue non directrice,
modification arrivée d'abord dans la version secondaire, ou perte de contenu due à une réécriture de
l'historique, etc.). La procédure initiale ne connaissait que « saisir en EN ou DE, puis livrer à tous » —
aucun cas où un élément n'existe que dans une version. Cas documenté : `ellmos-ai/skills` PR #1 a ajouté un
lien de découverte en chinois uniquement dans README.md ; une réécriture ultérieure de l'historique l'a
supprimé, car aucune étape ne vérifiait l'existence d'un contenu absent de toutes les autres versions
(T-20260926-967984806).

- **Vérifier, ne pas présumer :** avant la comparaison proprement dite (étape 3), tirer un diff par rapport
  au dernier état synchronisé connu (ou directement par rapport aux autres versions) et rechercher de manière
  ciblée un contenu nouveau dans UNE version et sans correspondant dans AUCUNE autre — pas seulement les
  sections manquantes de la langue directrice.
- **Outil :** `scripts/check_language_parity.py <datei1> <datei2> [...]` extrait les liens Markdown ET HTML (`[text](url)`, `<a href="url">`, `<img src="url">`)
  de toutes les versions fournies (les liens restent inchangés après traduction et constituent donc un
  indicateur robuste et indépendant de la langue) et signale chaque lien absent de TOUTES les versions
  avec le code de sortie 1. Code 0 signifie : aucun écart de sous-ensemble de liens n'a été trouvé —
  ce n'est pas une preuve de parité complète, mais un test de fumée ciblé de l'étape 0 avant la
  comparaison manuelle. Les liens à l'intérieur d'un bloc `<!-- lang-only: <code> -->` ne sont vérifiés que par
  rapport aux fichiers dont le code de langue figure dans le marquage (reconnu via le nom de fichier, p. ex.
  `README_zh.md` → `zh`, `README.md` → `en`) — ils ne comptent PAS là comme « absents des
  autres versions ». De plus, le script filtre par défaut les URL de badges `shields.io` dont le texte
  d'étiquette est encodé (la légende traduite se trouve souvent directement dans l'URL — pas une
  perte réelle de contenu, mais une variance de traduction attendue ; `--include-badges` désactive ce filtre).
  Les fichiers non lisibles en UTF-8 et les arguments manquants se terminent par le code de sortie 2 et
  un message d'erreur, et non par une trace d'exécution (traceback).
- **Décision en cas de découverte :** un contenu monolingue n'est JAMAIS supprimé silencieusement. Trois
  issues, sans suppression discrète :
  (a) **traduire et reporter dans TOUTES les versions** — le cas normal pour un contenu d'intérêt général ;
  (b) **restreindre volontairement à une ou plusieurs langue(s)** (« lang-only ») — lorsque le contenu ne
  concerne que ce public (cas documenté T-20260926-967984806 : un lien de découverte en chinois n'est pas
  pertinent pour les lecteurs DE/ES/JA/RU ; une traduction dans les six versions aurait elle-même été
  fausse — correction de l'utilisateur après la première version de cette étape). Marquage : **`<!-- lang-only: <code>[,<code>...] --> … <!-- /lang-only -->`**
  (commentaire HTML, invisible dans les moteurs de rendu Markdown ; pour plusieurs langues cibles, séparées
  par des virgules, p. ex. `zh,ja`). Aucune norme sectorielle établie n'est connue pour ce cas étroit (P-009
  vérifié) — les commentaires HTML sont le choix le plus portable et le plus discret pour Markdown.
  Le contenu marqué n'est **ni traduit ni signalé comme manquant** lors de la comparaison ;
  (c) **escalader comme conflit** lorsqu'il est incertain que le contenu soit encore voulu (p. ex. s'il semble
  contradictoire avec la version de référence) — demander à l'utilisateur ou à la chaîne de décision.
  Dans les trois cas : ne jamais retirer discrètement le contenu de la version où il figure, simplement parce
  que les autres ne l'ont pas.

### 1. Établir l'état des lieux

- Toutes les versions linguistiques (toutes) sont-elles présentes ? Si l'une manque complètement → **compléter**
  (traduction intégrale de la version directrice, et non réécriture libre).
- Vérifier la convention de nommage (p. ex. `DOKUMENT.md` + `DOKUMENT.en.md` ou suffixes `_de`/`_en`) et aligner
  les écarts — la facilité à retrouver les fichiers fait la moitié de la synchronisation.

### 2. Clarifier la langue directrice (avant toute comparaison)

- La langue directrice est la version dans laquelle on travaille sur le fond (souvent EN pour les articles,
  souvent la langue maternelle pour une documentation locale). Elle prévaut en cas de contradiction.
- **Exception de rétrotransfert :** si la version secondaire résout manifestement mieux un point (formulation
  plus claire, erreur corrigée), ce passage est REPRIS dans la version directrice — on rétrotransfère d'abord,
  puis on synchronise normalement. Vérifier l'exactitude technique avant d'adopter une formulation « plus
  élégante ».

### 3. Vérifier le parallélisme

Structure d'abord, puis contenu :

1. **Comparaison de la structure :** Sections et titres des deux versions côte à côte —
   les sections manquantes, supplémentaires ou réordonnées constituent les principales divergences.
2. **Échantillonnage par section** de la structure concordante : les affirmations, chiffres,
   renvois et exemples sont-ils identiques ? Particulièrement sujets à divergence : journaux de modifications,
   tableaux, valeurs numériques, bibliographies/répertoires de liens, sections modifiées en dernier.
3. **Vérifier les invariants non traduisibles** : les blocs de code, identifiants, formules et chemins
   doivent être IDENTIQUES dans les deux versions (le code n'est jamais traduit).

### 4. Corriger

- Résoudre les divergences dans le sens de la langue directrice (ou après rétrotransfert).
- Respecter la typographie de la langue cible (en allemand, de vrais Umlaute ä ö ü ß,
  pas de substitution ae/oe/ue ; conventions des guillemets).
- Mettre à jour les métadonnées : numéros de version, champs de date, entrées du journal de modifications dans les DEUX
  versions (le journal lui-même est le point de divergence le plus fréquent).

### 5. Documenter

Consigner le résultat (ce qui était divergent, ce qui a été repris, ce qui a été rétrotransféré).
Comme exécution périodique sur un fonds : la combiner avec l'échafaudage de rotation
(`rotation-check`) — un document (ou une paire de documents) par exécution, le registre faisant office de mémoire.

## Extension : audit d'expansion (faudrait-il PLUS de langues ?)

Outre la synchronisation des versions existantes, l'entretien linguistique implique de se demander si un
document/projet mérite D'AUTRES langues :

1. **Évaluer l'adéquation** au lieu de traduire aveuglément : public cible, utilisabilité internationale,
   présence en boutique/sur le web, mobilité du contenu. Tout document interne n'a pas besoin d'anglais ;
   toute application n'a pas besoin de cinq langues.
2. **Vérifier la préparation technique :** la cible est-elle préparée aux fichiers de langue ou aux versions parallèles
   (structure i18n, convention de nommage) ? Sinon, C'EST la première tâche, et non la traduction.
3. **Documenter la constatation, ne pas traduire en masse immédiatement :** consigner les tâches de traduction concrètes
   dans le fichier TODO local au projet ; « aucune autre langue n'est pertinente » est un résultat valable à consigner.
4. **Assurance qualité des versions dérivées :** vérifier par sondage les traductions auto-générées par rapport à la version directrice (section 3)
   avant de les considérer comme « disponibles ».

## Exemple

```text
Auftrag: „Prüf, ob das Paper in DE und EN synchron ist."

1. Bestand: paper_en.tex (führend) + paper_de.tex vorhanden.
2. Gliederung: DE fehlt der neue Abschnitt 4.2 (letzte EN-Revision); DE hat einen
   besseren Beweis-Absatz in 3.1.
3. Rücktransfer: 3.1-Formulierung fachlich geprüft → in EN übernommen.
4. Nachziehen: 4.2 nach DE übersetzt; Zahlen in Tabelle 2 abgeglichen (DE hatte
   veraltete Werte); Literaturverzeichnis identisch gemacht.
5. Registry-Eintrag: „paper-X | 2026-07-03 | de-en-sync | 3 Divergenzen behoben,
   1 Rücktransfer | nächster Check nach nächster EN-Revision".
```

## Signaux d'alerte

| Pensée | Réalité |
| --- | --- |
| « Je retraduis simplement les différences » | Clarifier d'abord la langue directrice et la question du rétrotransfert — sinon la meilleure solution sera écrasée. |
| « La structure correspond, donc c'est synchrone » | Les chiffres, journaux de modifications et renvois divergent en premier — un échantillonnage approfondi est obligatoire. |
| « Je traduis aussi les commentaires de code » | Les blocs de code et identifiants restent identiques dans les deux versions (en anglais). |
| « Je synchronise tous les documents d'un coup » | Une paire par exécution (échafaudage de rotation) garde la comparaison vérifiable. |

## Traductions en série autorisées

Pour une commande explicite portant sur un fonds linguistique complet, `scripts/worldset.py`
accompagne le processus avec l'API Claude Message Batches. L'unité de travail est source × langue × SHA-256. Le script ne nécessite que Python
3.10 ou plus récent ainsi que `pip install -r scripts/requirements.txt`. La liste des langues est reprise explicitement de la
convention de projet en vigueur ; les codes intégrés sont DE, EN, ES, ZH, JA,
RU, FR, HI, AR, BN et PT.

```bash
python scripts/worldset.py scan --root /path/to/checkout --kind skills --out /private/run/plan.json
python scripts/worldset.py submit --projection /private/run/plan.json --receipt /private/run/batch.json --limit 20
python scripts/worldset.py collect --receipt /private/run/batch.json --out /private/run/results
```

`--kind readme` planifie à la place les versions linguistiques du README. README.md est par défaut en anglais ; une autre langue directrice doit être
déclarée explicitement avec
`<!-- source-language: de -->`. Vérifier au préalable le fonds
pour les noms de fichiers alternatifs déjà établis.

`retry-plan --receipt ... --results ... --out ...` crée, à partir des échecs de porte terminés,
exactement une tentative de correction. Les erreurs répétées restent en attente de vérification. Par langue, `submit --glossary <json>` peut
utiliser un objet terminologique ; ses entrées sont transmises à l'expert linguistique concerné.

La clé API provient de `ANTHROPIC_API_KEY` ou `--key-file` ; sa valeur
n'est écrite ni dans les accusés de réception ni dans les traductions. Utiliser uniquement le solde existant expressément autorisé, ne jamais recharger
automatiquement. Le script interrompt le travail cloud en cas de solde insuffisant. Un adaptateur de modèle local
nécessite sa propre autorisation et un contrôle des ressources.

La projection est un instantané d'entrée, non une seconde file de tâches. L'identifiant de lot du fournisseur est le descripteur d'exécution ; les lots en cours sont interrogés,
non soumis à nouveau. Un accusé de réception sans identifiant de lot après une erreur de transport
doit être rapproché de la liste des lots du fournisseur. Ne pas répéter les soumissions aveuglément. Les modèles et glossaires sont des données non fiables.

Les sorties se trouvent exclusivement dans `raw/` et, après réussite des contrôles de structure et de langue, dans `candidates/`. Même les candidats réussis nécessitent un
échantillonnage linguistique indépendant ; les contrôles mécaniques ne prouvent pas la qualité de la traduction. Les versions linguistiques existantes sans hash source sont conservées,
car elles peuvent contenir des compléments autonomes. `--include-stale` ne planifie
que la retraduction des traductions obsolètes préalablement marquées par hash. Avant la reprise, revérifier le hash source,
l'état cible et les verrous ; exécuter ensuite les contrôles habituels du dépôt, de confidentialité,
de commit et de déploiement. L'exécution en arrière-plan passe uniquement par le planificateur déjà compétent, selon son contrat de réservation et de ressources.

### Contrôle linguistique séparé de l'API

Lors de l'analyse, la langue source déclarée s'applique, sinon l'allemand par défaut pour
les skills propres. Pour les sources étrangères en anglais, indiquer explicitement
\`--source-language en\` ; \`--kind skills-flat\` prend en charge une bibliothèque de skills plate.
\`--source-languages\` charge, pour les fonds mixtes, une correspondance JSON vérifiée
entre chemin source relatif et code de langue. La source originale est conservée ;
les versions allemandes manquantes sont alors créées sous \`SKILL.de.md\`.
Les anciens dossiers de langue existants comme \`EN/SKILL.md\` ou \`fr/SKILL.md\` comptent comme
versions conservées et ne sont pas complétés par des fichiers concurrents.

`scripts/worldset_review.py` prépare les candidats réussis en vue d'une vérification linguistique indépendante. Le traducteur reste Haiku ; le modèle de vérification est indiqué séparément. Utiliser d'abord un échantillon contrôlé à partir d'exemples déjà vérifiés, puis fixer l'étendue de vérification supplémentaire en fonction du taux d'erreur.

```bash
python scripts/worldset_review.py prepare --translation-receipt batch.json --results-dir staging --out review-plan.json
python scripts/worldset_review.py submit --projection review-plan.json --receipt review-batch.json --model claude-sonnet-5-5
python scripts/worldset_review.py collect --receipt review-batch.json --out review-results
```

La vérification lit intégralement chaque source et chaque version sélectionnées. Sa décision est liée au hachage de la source, au hachage du candidat, aux chemins, à la langue et au modèle de vérification effectivement observé. Les erreurs de sens et les déclencheurs locaux manquants bloquent l'acceptation, même avec une note globale élevée. En raison du taux d'erreur du pilote, le vérificateur automatique exige au moins 4,5 sur 5 points.
Chaque constat nommé nécessite en outre une vérification explicite par un opérateur : \`operator_reviewed: true\`, \`operator\` et \`operator_notes\` dans l'enregistrement de revue lié au hachage. Même les modifications de sens jugées mineures ne doivent pas passer automatiquement. Les réponses de vérification erronées ou tronquées restent en suspens. Les `reviews-<batch-id>.json` produits sont les entrées de `worldset.py apply` ; la vérification linguistique n'écrit aucune cible. Un jugement automatique ne remplace pas la validation finale propre au projet.

`retry-plan` permet une passe de correction. Pour `max_tokens`, sa limite de sortie est augmentée de façon ciblée à au moins 64 000 ; une fois la limite de 128 000 déjà atteinte, un découpage est nécessaire. L'autorisation des coûts d'API et l'interdiction de recharge automatique du crédit restent en vigueur. Les données brutes et les contrats de protection figés des lots terminés sont conservés. Les nouvelles règles d'analyse ne doivent pas remplacer après coup les associations de marqueurs antérieures. Avec des URL nues sans séparateur vers le texte suivant, la frontière peut être ambiguë ; ces cas restent en attente de vérification de format. Des liens Markdown explicites ou des séparateurs évitent cette ambiguïté.

## Corrections sémantiques ciblées

`scripts/worldset_repair.py` traite des candidats complets qui réussissent les vérifications mécaniques, mais dont la vérification linguistique ou la vérification par un opérateur a relevé des erreurs concrètes. L'entrée contient le lot d'origine et son ID, la source complète et la version candidate, leurs hachages, le modèle de traduction effectivement observé, l'enregistrement de revue indépendant complet et les `repair_feedback` concrets. Pour des ensembles source séparés, préparer chaque ensemble avec sa propre `--repository-root`.

```bash
python scripts/worldset_repair.py --repository-root repo prepare --cases repair-cases.json --out repair-plan.json
python scripts/worldset_repair.py --repository-root repo submit --projection repair-plan.json --receipt repair-batch.json
python scripts/worldset_repair.py --repository-root repo collect --receipt repair-batch.json --out repair-staging
```

L'ordre de réparation lie la source, le candidat, la revue complète et les retours à un nouvel ID. Avant l'appel d'API, la source actuelle et la cible encore manquante doivent correspondre. Le lot natif reste l'unique poignée d'exécution ; un reçu réservé après une soumission incertaine ne doit pas être soumis à nouveau. La clé d'API reste sur l'hôte d'exécution. Avec des hôtes différents, utiliser comme racine d'entrée une copie de la source stockée séparément et vérifiée par hachage ; elle ne remplace pas la nouvelle vérification de la source réelle lors de l'application.

Haiku fournit au maximum 16 remplacements uniques et non chevauchants. Le code, les liens, la langue et la provenance restent protégés ; seul l'horodatage du frontmatter est adapté par le collecteur. Après la dernière modification, toutes les vérifications mécaniques complètes sont à nouveau exécutées. Les versions cibles existantes et les candidats README sans frontmatter YAML sont exclus de cette voie de réparation ; cette limite est vérifiée avant la soumission.

Le résultat reste `review_required`. Ensuite, effectuer avec `worldset_review.py` une nouvelle vérification linguistique complète et indépendante, et résoudre en plus tous les constats. La revue précédente ne constitue pas une validation du candidat réparé. Ce n'est qu'après cela que s'applique le contrat d'application existant, avec un nouveau scan de verrous, une vérification du hachage de la source et une création atomique.

## Skills associés

- `rotation-check` — structure pour l'exécution périodique sur un ensemble de documents.
- `workflow-extract` — si cette vérification doit être installée comme automatisation permanente.

## Journal des modifications

### 1.5.1 (2026-10-15)
- Traiter les métadonnées de réflexion standard à côté du texte de réparation JSON ; rejeter les blocs d'outils, les types de réponse inconnus et les réponses sans texte JSON.
- Régression sécurisée avec des réponses réelles du fournisseur enregistrées et sélection de module non ambiguë dans le processus de test.

### 1.5.0 (2026-10-15)
- Ajout de corrections sémantiques limitées avec liaison complète à la source, au candidat, à la revue et aux retours, reçus natifs et nouvelle vérification linguistique indépendante ; les vérifications explicites restent actives même sous Python optimisé.

### 1.4.0 (2026-10-15)
- Prise en compte, lors de l'analyse, des langues source déclarées ou explicites, des bibliothèques plates et des anciens dossiers de langue existants, y compris les versions cibles allemandes de sources anglaises.

### 1.3.1 (2026-10-15)
- Ajout d'une vérification linguistique API séparée et liée au hachage ; protection des portées de code à l'aide de l'analyseur CommonMark, contrôle de l'association URL et paragraphes, et passes de correction limitées après épuisement de la limite de sortie.

### 1.3.0 (2026-10-15)
- Ajout de traductions en série autorisées avec projections d'entrée immuables, poignées de lot natives, zones de code et de liens protégées, provenance par hachage de source et candidats de vérification séparés.

### 1.2.2 (2026-09-26)
- `scripts/check_language_parity.py` : règle de préfixe pour les codes lang-only — un code de base (p. ex. `zh`) couvre désormais aussi ses variantes régionales (`zh-cn`, `zh-tw`) ; l'inverse ne s'applique pas.
- La vérification fail-closed d'un code lang-only compare désormais à TOUS les fichiers README du répertoire, et non plus seulement au sous-ensemble transmis — un appel avec seulement deux versions sur six ne déclenche donc plus de fausse alerte. Un code valide sans fichier dans CET appel produit désormais seulement un avertissement (pas de sortie 1) ; un code réellement inconnu (faute de frappe comme `cn` au lieu de `zh`) reste en sortie 1.

### 1.2.1 (2026-09-26)
- `scripts/check_language_parity.py` : une version « lang-only » qui ne correspond à aucune des versions linguistiques fournies (par ex. la faute de frappe `cn` au lieu de `zh`) est désormais signalée comme constat en mode fail-closed, au lieu d'exempter silencieusement le lien.
- Les noms de fichiers avec code de région sont désormais reconnus comme langue : `README_zh-CN.md` et `README_zh_CN.md` renvoient tous deux à `zh-cn`.

### 1.2.0 (2026-09-26)
- Ajout de l'étape 0 « Détecter le contenu monolingue » (T-20260926-967984806) : une divergence peut être un contenu nouveau, pas encore propagé, plutôt qu'un contenu obsolète ; trois issues possibles (traduire et propager partout / marquer comme lang-only / escalader comme conflit), jamais de suppression silencieuse. Nouveau marqueur `<!-- lang-only: <code> -->` pour un contenu volontairement restreint à un public cible.
- Ajout de `scripts/check_language_parity.py` et `scripts/test_check_language_parity.py` :
  détecte les liens qui n'apparaissent que dans un sous-ensemble des versions linguistiques (liens Markdown et HTML), respecte le marquage lang-only, filtre le bruit des badges shields.io, et intercepte les fichiers non UTF-8 avec la sortie 2 au lieu d'une trace d'exécution (Traceback).

### 1.1.0 (2026-07-03)
- Ajout de l'audit d'expansion (évaluation de l'aptitude à l'i18n, préparation technique, assurance qualité pour les versions reprises) — intégré plutôt que sous forme de skill i18n-coverage-audit distinct (décision de déduplication).

### 1.0.0 (2026-07-03)
- Version initiale. Extraite de l'automatisation Codex « research-paper-de-en-synchronisationscheck », généralisée à toutes les versions linguistiques tenues en parallèle (articles, README, skills, textes de site web).
