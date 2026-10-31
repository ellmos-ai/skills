---
name: folder-organization
version: 1.1.0
type: protocol
author: Lukas Geiger + OpenAI Codex
created: 2026-08-24
updated: 2026-08-24
description: "Ranger et organiser sémantiquement les dossiers et les dépôts de fichiers : repérer les règles locales et la taxonomie existante, affecter les fichiers selon leur contenu, conserver les ensembles qui vont ensemble, archiver les séries nettes de prédécesseurs/successeurs et les journaux, séparer les contenus mixtes valides et dépassés par Cut-and-Clue, et placer les candidats à la suppression dans une corbeille de contrôle réversible. Utilisez cette compétence pour « ranger le dossier », « classer les fichiers de façon pertinente », « archiver les anciennes versions », « nettoyer les fichiers journaux », « séparer les contenus obsolètes et valides », ou lorsque le rangement fait apparaître des fichiers de secrets ou des secrets dans un stockage cloud. Elle fonctionne de manière neutre vis-à-vis des fournisseurs et des utilisateurs, à elle seule ; les modules ou services de fichiers compatibles détectés ne sont utilisés que comme accélérateurs facultatifs. Pour des règles de regroupement récurrentes déjà entièrement définies, utilisez plutôt une automatisation de fichiers basée sur des règles ; pour la refonte de l'architecture complète d'un projet, utilisez un optimiseur de pipeline/projet."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: utilities
tags: [ordner, dateien, sortierung, archivierung, versionen, logs, geheimnisse, cloud, cut-and-clue, cleanup, standalone]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: ffe1a25ac259cfb78124036afbaf7b8b99b9e6c1dcb181f7d6d8f3d34da1ab2c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="folder-organization banner">

# Organisation des dossiers

## Objectif et périmètre

Produisez un rangement traçable, dans lequel chaque modification est justifiée par des règles
locales, le contenu, les relations entre fichiers ou une décision explicite de l'utilisateur. Cette
compétence est un protocole de rangement sémantique, et non un second programme de déplacement de
fichiers ni une dépendance obligatoire à un fournisseur.

Un inventaire ou un contrôle reste en lecture seule. Une demande explicite telle que « range ce
dossier » autorise des déplacements sûrs et réversibles à l'intérieur du périmètre indiqué, tant
qu'aucune ambiguïté non résolue ne subsiste. L'écrasement, la suppression définitive, le
déplacement hors du périmètre, la réécriture du contenu ou l'activation d'une automatisation
permanente exigent une autorisation distincte.

## Noyau autonome et amorces facultatives

Commencez toujours par le noyau autonome. Il ne nécessite que la lecture, l'écriture, le hachage et
les opérations ordinaires sur les fichiers. Pour un inventaire reproductible, le script
[`scripts/folder_organization.py`](scripts/folder_organization.py) est disponible ; les valeurs par défaut sûres et les
dérogations figurent dans [`config.json`](config.json). Le script n'écrit par défaut
que sur stdout. `--out` ne peut créer qu'un nouveau fichier en dehors de la racine
analysée ; les cibles existantes ne sont jamais écrasées. Ses découvertes de journaux et de versions
sont des indices de faible confiance, et non une autorisation d'archivage.

La version bibliothèque possède un frontmatter de catalogue étendu. Si un système cible n'accepte
que le frontmatter de base portable (`name`, `description`),
[`scripts/export_portable.py`](scripts/export_portable.py) produit une copie autonome dans un nouveau dossier cible.
Le déroulement fonctionnel et toutes les pièces locales de remplacement y restent entièrement
conservés.

Recherchez ensuite des capacités, et non des noms de marques. Une intégration existante peut
améliorer le noyau, mais elle ne modifie ni le sens ni les autorisations :

| Capacité requise | Remplacement autonome | Amorce/adaptateur facultatif détecté |
|---|---|---|
| Inventaire, empreintes, plan | script Python fourni ou recherche native de fichiers | planification/reçus FolderHome |
| Contenu documentaire/OCR | lecteur local existant ; sinon `unreadable/review` | doc-services ou extracteur équivalent |
| Opérations sûres face au cloud/verrous | opération native avec contrôle d'état frais | FileCommander ou adaptateur propre au fournisseur |
| Règles stables et récurrentes | configuration fournie sous forme de proposition | file-collect-sort-action ou automatisation équivalente |
| Réindexation des indices | marqueurs CLUE repérables dans le texte | Gardener ou autre indexeur local |

Les composants Ellmos sont donc des **amorces de fondement** : si leurs capacités sont disponibles
et autorisées pour la tâche, utilisez leurs contrôles plus stricts. Si elles manquent, exécutez le
même déroulement fonctionnel de manière heuristique, avec les pièces de remplacement de cette
compétence. Aucune transmission externe n'est justifiée uniquement parce qu'un lecteur local
manque.

## Démarche

### 1. Définir la racine, les règles et le mode

- Choisissez la plus petite racine commune de rangement ; ne parcourez pas un répertoire utilisateur
  ou cloud entier par commodité.
- Lisez les fichiers de contrôle dans la racine et au-dessus, par exemple `AGENTS.md`,
  `CLAUDE.md`, `README.md`, `START.md`, les règles de nommage, les
  registres, les manifestes et les verrous.
- Notez le mode : rangement sémantique unique, entretien des archives, entretien des journaux,
  Cut-and-Clue ou préparation d'une règle récurrente.
- Les dossiers cibles existants et leur usage réel priment sur une taxonomie idéale inventée.

### 2. Politique des secrets avant tout accès au contenu

Avant d'ouvrir ou de hacher un fichier, vérifiez son nom par rapport à `secret_policy.protected_name_patterns` et aux
exclusions de `config.json`. Les fichiers protégés comme `.env`, les clés
privées ou les fichiers d'identifiants ne sont saisis que par chemin et métadonnées ; leur contenu ne
doit jamais atteindre le contexte du modèle, le rapport ou le journal. `--hash-all` ne lève
pas cette limite. Si un signal de secret est repéré par hasard dans un fichier normalement lisible,
arrêtez l'affichage du contenu et signalez uniquement l'identifiant du signal.

Si la découverte se situe vraisemblablement dans une racine cloud ou de synchronisation, la
`cloud_action` configurée s'applique. La valeur par défaut est `localize-after-approval` : confirmer une
cible locale située hors de toutes les racines de synchronisation et des permissions restrictives,
effectuer un essai à blanc et obtenir une autorisation, copier le fichier de façon opaque puis le
vérifier par empreinte en interne, remplacer seulement ensuite la source cloud de manière
restaurable, et laisser un pointeur non secret. Sans `local_secret_root` défini, ou en présence de
références d'exécution menacées ou à risque, bloquez l'opération.

La transaction complète, les modes de pointeur (`control-file`, `sidecar`,
`placeholder`), la table locale des pointeurs, les indications de rotation et le blocage strict
sont décrits dans [`references/secrets-policy.md`](references/secrets-policy.md). Les fichiers suspects de contenir des
secrets sont retirés du rangement normal, de l'archivage, de Cut-and-Clue et de la corbeille jusqu'à
la décision de politique.

### 3. Recenser le stock et les relations

Relevez le chemin, la taille, la date de modification, le type et, lorsque cela reste proportionné,
le SHA-256. Pour les documents ambigus, lisez le contenu ou les métadonnées. Les fichiers binaires
illisibles restent explicitement non élucidés ; le nom et l'extension seuls ne justifient aucune
action irréversible.

Traitez les fichiers liés comme des ensembles : versions linguistiques, source/export,
Markdown/PDF, document/ressources, données/script/résultat, pièce jointe/fichier principal, ainsi que
prédécesseur/successeur. Avant tout déplacement, vérifiez les liens, manifestes, inclusions,
références de code et registres.

Pour la matrice détaillée des preuves et de la confiance dans les stocks difficiles, lisez
[`references/heuristics.md`](references/heuristics.md).

### 4. Planifier la structure cible et chaque décision individuelle

Déduisez la structure cible de la finalité, des règles existantes et des regroupements réels. La
racine sert d'aiguillage, non de stockage durable. Ne créez pas de dossiers génériques tels que
`_Sonstiges` lorsque le contenu d'une découverte reste indéterminé ; utilisez plutôt
`review/` ou une liste de décisions.

Chaque modification prévue comprend au minimum :

| Champ | Contenu |
|---|---|
| Source | chemin relatif exact et, facultativement, empreinte |
| Cible/action | `keep`, `move`, `rename`, `archive`, `trash-review`, `cut-and-clue`, `review` |
| Justification | règle, contenu, relation ou indice de version |
| Confiance | élevée, moyenne ou faible |
| Effet secondaire | liens, ensembles, registres ou automatisations concernés |

- **Élevée :** règle locale explicite, correspondance nette avec un manifeste ou succession
  clairement établie.
- **Moyenne :** forte adéquation de contenu ou regroupement existant, mais sans règle explicite.
- **Faible :** seulement le nom, l'extension, la date de modification ou une similitude incertaine.
  Ne pas déplacer automatiquement.

Avant toute mutation, fournissez un essai à blanc complet. Les collisions, liens symboliques,
verrous cloud, fichiers illisibles et cibles situées hors de la racine bloquent l'action concernée.

### 5. Archiver les versions et les journaux

Archivez un ancien fichier comme prédécesseur seulement si la série est établie par plusieurs
signaux : identifiant de version ou de date, indication de version interne, fort recouvrement de
contenu, finalité concordante et successeur valide clairement identifié. La date de modification
seule ne suffit pas. Les états de preuve référencés et les publications validées sont conservés.

Pour les journaux, distinguez le journal d'exécution actif, le journal d'audit/de preuve et
l'historique à rotation. Ne déplacez pas les journaux actifs ou encore en cours d'écriture. Archivez les
anciens journaux clos selon la convention locale, sinon par exemple sous `_archive/logs/<jahr>/`, avec
empreinte et lieu d'origine. La compression est une décision distincte ; archiver ne signifie pas
supprimer.

### 6. Appliquer Cut-and-Clue

Lorsqu'un fichier contient à la fois des contenus valides et dépassés, un déplacement aveugle est
aussi faux qu'une conservation intégrale. Il faut alors **découper** les contenus valides dans un ou
plusieurs nouveaux fichiers canoniques et laisser, dans l'ancien matériau et, si nécessaire, à
l'endroit même du problème, un **indice** lisible par machine indiquant le statut, la raison et le
successeur. Ce n'est qu'après contrôle d'exhaustivité que l'original est archivé.

Les marqueurs, les règles relatives à `[sic]`, aux fichiers binaires et à la protection
contre la perte d'historique figurent dans [`references/cut-and-clue.md`](references/cut-and-clue.md).
`[sic]` signale une erreur citée volontairement ; pour un contenu dépassé, utilisez
`OUTDATED` ou `SUPERSEDED`.

### 7. Corbeille de contrôle au lieu de la suppression

Déplacez les candidats à la suppression situés dans la racine vers un dossier d'exécution tel que
`_trash_review/<run-id>/`. Conservez la structure relative et écrivez `MANIFEST.md` ou
`RESTORE.json` avec la source, le nouveau chemin, l'empreinte, le motif et l'horodatage. Rien ne
doit être supprimé automatiquement à partir de là. L'utilisateur peut ainsi contrôler l'ensemble de
l'exécution, puis supprimer ou restaurer lui-même.

Si une zone d'entrée surveillée existe, placez la corbeille et les archives hors de son périmètre de
analyse afin d'éviter toute réinjection.

### 8. Exécuter et démontrer

- Juste avant chaque action, revérifiez la source, l'empreinte, la cible et l'absence de la cible.
- N'écrasez jamais ; en cas de collision, bloquez ou utilisez un nouveau nom explicitement prévu.
- Après l'exécution, relisez le stock cible, comparez les empreintes, recherchez les anciens noms de
  chemin dans les références et mettez à jour les registres concernés.
- Supprimez uniquement les dossiers vides créés par le processus lui-même. Pour chaque mutation,
  conservez un chemin de retour ou un manifeste.
- Si un indexeur local est disponible, réindexez les marqueurs CLUE ; sans indexeur, ils restent
  efficaces comme texte ordinaire et visible.

## Exemples brefs

- `bericht_v1.md` et `bericht_v2.md` : d'abord les marquer comme série de versions
  possible. Seuls la version interne, le contenu et les références peuvent décider si
  `v1` peut réellement être archivé.
- `konzept.md` contient des règles valides et des sections dépassées : reprenez intégralement
  la substance valide dans un nouveau fichier canonique, conservez l'original à l'identique et créez
  les indices ou le fichier annexe avec le successeur.
- `.env` dans une racine de synchronisation : ne l'ouvrez pas et ne le recopiez pas dans
  le rapport. Produisez un plan de politique ; sans `local_secret_root` confirmé, sans autorisation et
  sans bascule d'exécution sûre, ne modifiez aucun fichier.

## Apprentissage et automatisation

Recueillez les corrections de l'utilisateur comme candidates à des règles, sans jamais les intégrer
silencieusement. Ce n'est que lorsqu'un motif est confirmé de manière répétée, sans conflit et
clairement délimité, qu'il faut proposer une automatisation récurrente. Chaque automatisation nouvelle
ou modifiée requiert de nouveau un essai à blanc et une autorisation.

## Rapport final

Outre le stock, les actions, les archives, la corbeille, les successeurs Cut-and-Clue et les
décisions ouvertes, indiquez tous les candidats secrets uniquement par chemin ou identifiant de
signal, leur statut de politique, les transferts cloud bloqués ou autorisés, le mode de pointeur et
le résultat de relecture. Ne reproduisez jamais de valeurs, de chemins de secrets locaux ni de lignes
de contexte sensibles.

Mentionnez le stock initial, les actions exécutées et bloquées, les chemins des archives et de la
corbeille, les successeurs Cut-and-Clue, les références mises à jour, le résultat des empreintes et de
la relecture, les décisions ouvertes et les règles récurrentes proposées. Une planification n'est pas
un rangement exécuté.

## Compétences associées

- Automatisation de fichiers basée sur des règles : pour des schémas source-motif-cible déjà connus
  et récurrents.
- Optimiseur de pipeline/projet : pour la refonte structurelle d'un projet ou d'une pile complète.
- Nettoyage/maintenance : pour la clôture de session, l'entretien des registres et les fichiers
  temporaires de projet.
- Mise à plat des dossiers : uniquement si la transformation demandée est explicitement l'aplatissement.

## Journal des modifications

### 1.1.0 (2026-08-24)

- Ajout d'une politique configurable des secrets : non-ouverture des noms de fichiers protégés,
  détection aléatoire expurgée et externalisation cloud transactionnelle avec table de correspondance
  locale et pointeur non secret.

### 1.0.0 (2026-08-24)
- Première version neutre vis-à-vis des fournisseurs et des utilisateurs, avec script autonome,
  principe d'amorces facultatives, tri sémantique, archivage des versions et journaux, Cut-and-Clue et
  corbeille de contrôle.
