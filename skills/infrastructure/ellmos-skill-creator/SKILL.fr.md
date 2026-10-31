---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "Crée ou révise un skill POUR CET ÉCOSYSTÈME : délègue la boucle générique entretien/ébauche/évaluation au plugin officiel skill-creator (Anthropic, Apache-2.0), mais impose en plus les exigences ellmos que le plugin officiel ne connaît pas — frontmatter maison (9 champs), règles de catégorie/visibilité, détection neutre vis-à-vis du fournisseur, de l'utilisateur et d'ellmos mais sensible à ellmos via grounding-seed, config.json fourni (y compris le contrat d'apprentissage) + connections.json, conscience des fournisseurs/vendeurs (proposer des alternatives state-of-the-art, y compris les propres composants ellmos), une section d'auto-mise à jour ET un ensemble réutilisable de fichiers d'apprentissage/couverture (user-usecases.json, usecase-gaps.json, known-providers-and-abilities.json, gap-closing-analysis.json — inspirés de evals.json de skill-creator et de A2A/AgentSkill, sans standard parallèle). TOUJOURS utiliser lorsqu'un NOUVEAU skill doit naître pour ce système ou qu'un skill existant doit être mis en conformité ellmos — même pour « crée un skill », « fais-moi un skill pour X », « utilise skill-creator », « créer un nouveau skill », « rends ce skill conforme ellmos », « créer un contrat d'apprentissage/code de comportement pour un skill », « vérifier la couverture des usecases d'un skill ». Pour simplement TROUVER/ROUTER un skill, utiliser plutôt skill-finder, et pour l'audit du paysage, skill-explorer."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 1e6dace03eb8afc639fa08debace08a61441912a22399c11a49f7fe6e7dc3ecb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:09.407398+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## Origine et décision (fork vs. construction propre)

**Décision : construction propre, pas de fork.** Justification, pour qu'elle ne se perde pas :

- `skill-creator` (Anthropic, marketplace `claude-plugins-official`) est sous licence **Apache-2.0**
  (texte de LICENSE lu et vérifié dans le clone, 2026-08-24) — un fork serait juridiquement
  possible et constitue déjà, ailleurs dans le dépôt, le modèle établi (`skills/third-party/grilling`).
- Un fork aurait toutefois embarqué toute la machinerie d'évaluation/benchmark de l'original
  (`agents/{analyzer,comparator,grader}.md`, `eval-viewer/`, 7 scripts, SKILL.md de 485 lignes) —
  une capacité déjà présente et directement appelable (`Skill: skill-creator:skill-creator`).
  Selon la règle 4 de `.PLUGINS/CLAUDE.md` (« vérifier les capacités avant de reconstruire ») et le
  motif P10 (« deux interrupteurs que personne ne compare »), ce serait un doublon, pas une extension.
- La véritable lacune est **purement spécifique à ellmos** et fondamentalement inconnue de l'original :
  frontmatter maison (`templates/SKILL.md`), `docs/CONVENTIONS.md`, neutralité vis-à-vis du fournisseur/de l'utilisateur/d'ellmos
  avec sensibilité à ellmos, raccordement `grounding-seed`, conscience des fournisseurs, auto-mise à jour.
- Ce skill ne contient **aucun texte d'Anthropic** (formulation propre partout) — il ne déclenche donc
  pas non plus d'obligation d'attribution Apache-2.0 pour les modifications. Il **compose** l'original au lieu
  de le copier : c'est à la fois la voie juridiquement la plus propre et celle qui demande le moins de maintenance.

## Quand activer

- « crée un skill pour X », « construire un nouveau skill », « utilise skill-creator »
- « rends ce skill conforme ellmos », « mettre un skill au standard maison »
- Toujours lorsque la **cible** est un skill dans `.AI/.SKILLS/skills/…` (ou son clone canonique Plan-D) —
  pas pour les demandes générales hors écosystème (« fais-moi n'importe quel skill Claude sans lien ici »).

## Procédure

### Étape 1 — Déléguer entretien/ébauche/évaluation

Appeler le `Skill: skill-creator:skill-creator` officiel pour : clarification de l'intention,
ébauche de la structure SKILL.md, cas de test, boucle d'évaluation, optimisation de la description
(`scripts/improve_description.py`). **Ne pas réinventer** — cette partie est générique et déjà bien résolue dans l'original.

### Étape 2 — Mettre en place le squelette maison ellmos (obligatoire, additif au format original)

Compléter le SKILL.md produit par l'original avec les neuf champs maison de
`.SKILLS/templates/SKILL.md` (ou `AGENT.md`/`WORKFLOW.md`/`PROMPT.md` selon le type), lire au préalable
`.SKILLS/docs/CONVENTIONS.md` pour les dossiers de catégorie, la règle flat (<5 fichiers à plat),
la convention de version (SemVer : MAJOR/MINOR/PATCH) et les ensembles multilingues (Core : DE+EN obligatoire).
**`visibility` démarre toujours sur `private-only`** — la publication est une décision ultérieure, vérifiée
et prise par l'utilisateur (`.AI/VISIBILITY-POLICY.md`), jamais une valeur par défaut. Ces champs sont purement **additifs** au format
Anthropic (clés YAML supplémentaires à côté de `name`/`description`) — chaque skill ainsi produit reste entièrement
`anthropic_compatible: true`.

### Étape 3 — Faire respecter les principes : neutre vis-à-vis du fournisseur et de l'utilisateur, neutre pour ellmos mais sensible à ellmos

Texte complet et modèles de code : `references/ELLMOS-PRINCIPLES.md`. En bref : le skill produit doit être
**autonome** (il apporte tout ce dont il a besoin) et, **en même temps**, utiliser les composants ellmos
dès qu'ils sont là — il en décide lui-même à l'exécution, jamais de façon câblée en dur. C'est exactement le
motif que `grounding-seed` fournit déjà (README : « cultivated landscape, not wildflower » / « viable alone, more productive
together ») — **aucun second mécanisme de détection n'est inventé**, ce skill renvoie systématiquement les skills produits vers `grounding_seed.detect_ecosystem()`.

### Étape 4 — Fournir config.json + connections.json

`grounding-seed` est déjà importable comme paquet Python (vérifié le 2026-08-24 :
`import grounding_seed` se résout correctement dans l'arbre source `grounding-seed` cloné localement, clone Plan-D) — c'est le **point d'ancrage canonique**, il ne faut pas inventer de nouveau fichier. Pour chaque skill produit ayant des besoins externes (programmes, services, fournisseurs) :

- **`config.json`** — réglages propres au skill (modèle : `templates/skill-config.template.json`).
  `grounding_seed.store.LocalStore(root)` utilise par défaut ce nom de fichier pour son stockage des rôles — un skill produit peut donc soit utiliser
  son propre `config.json` comme backend `LocalStore`, soit le garder séparé s'il a aussi besoin de réglages purement comportementaux
  (dans ce cas, une seconde instance `LocalStore(root, filename="connections.json")`).
- **`connections.json`** — les points d'ancrage externes **effectivement résolus**
  (quel programme/service a été trouvé, depuis quand, avec quelle origine) — modèle : `templates/skill-connections.template.json`, schéma `ellmos.source-resolver.user-config.v1`
  (identique à `source-resolver` ; d'après le README de grounding-seed, ce choix est volontaire pour qu'une migration ultérieure vers le
  véritable `source-resolver` soit sans perte — voir `migration.py` là-bas).

Détails, CLI et exemple de code : section « Docking » de `references/ELLMOS-PRINCIPLES.md`.

### Étape 5 — Intégrer la conscience des fournisseurs/vendeurs

Texte complet : `references/VENDOR-AWARENESS.md`. En bref : le skill produit reçoit une section « Fournisseurs & alternatives » qui (a) nomme le(s) fournisseur(s) state-of-the-art du sujet
(p. ex. ElevenLabs pour le TTS), (b) au moins un fournisseur de remplacement, (c) liste **explicitement les composants propres à ellmos comme candidats de même rang**
lorsqu'ils couvrent le sujet (p. ex. `ellmos-voice-io` au lieu de/à côté d'ElevenLabs) — et **propose** l'installation ou la migration
lorsqu'une exigence de l'utilisateur s'y prête, au lieu de la supposer tacitement. Base pour « ce qui est présent sur le système » :
`grounding_seed.scan.scan_resources([...])` (vérifie `shutil.which`) plus `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` pour les candidats ellmos.

### Étape 6 — Mettre en place l'auto-mise à jour

Texte complet : `references/SELF-UPDATE.md`. En bref : chaque skill produit reçoit une section « Auto-mise à jour » qui (a) propose périodiquement une courte recherche web pour rester à l'état de l'art, (b) connaît les skills/workflows apparentés et signale les nouvelles alternatives qui pourraient mieux convenir, (c) tient à jour un petit JSON d'apprentissage (modèle : `templates/skill-connections.template.json`, champ `notizen`/`gelernt`) qui, si le composant mémoire ellmos (USMC/Gardener) est présent, peut être externalisé au lieu de grandir localement — là encore : détecter plutôt que câbler en dur (`grounding_seed.detect_ecosystem()`).

### Étape 6b — Mettre en place le contrat d'apprentissage et la couverture des usecases (motif réutilisable)

Texte complet : `references/LEARNING-CONTRACT-AND-COVERAGE.md`. En bref : non seulement ce skill lui-même, mais **chaque skill qu'il produit** reçoit un petit ensemble réutilisable de fichiers d'apprentissage/couverture — vérifié par rapport aux standards établis, sans standard parallèle :

- `evals/evals.json` — **réutiliser**, ne pas dupliquer : c'est déjà le standard skill-creator pour les cas de test rédigés par l'auteur.
- `user-usecases.json` — les cas d'usage effectivement formulés par l'utilisateur, de même forme que `evals.json` (modèle : `templates/user-usecases.template.json`).
- `usecase-gaps.json` — rapprochement : quels cas d'usage utilisateur ne sont pas testés/couverts (modèle : `templates/usecase-gaps.template.json`).
- `known-providers-and-abilities.json` — espace des candidats de fournisseurs connus par rôle, champs inspirés de A2A/`AgentSkill` (id/name/description/tags), non inventés (modèle : `templates/known-providers-and-abilities.template.json`).
- `gap-closing-analysis.json` — voies structurelles de fermeture pour chaque lacune (module ellmos, bundle ellmos, module tiers, reconstruction) — sans doublon avec `grading.json.eval_feedback` (modèle : `templates/gap-closing-analysis.template.json`).
- `config.json`, champ `lernvertrag` — code de comportement (choisir la meilleure option, **l'utilisateur est roi**, ne jamais installer de son propre chef, intervalle de mise à jour) — volontairement une extension de `config.json`, pas un septième fichier.

Schémas : `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — même convention maison que `skill-v1.schema.json`.
`grounding-seed` a été examiné pour cet ensemble de fichiers et volontairement **pas** étendu (justification dans `LEARNING-CONTRACT-AND-COVERAGE.md`) — seul `connections.json` reste sa part.

### Étape 7 — Enregistrer, tester, committer

- Choisir le dossier de catégorie selon `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md` ; en cas de doute, demander `skill-finder`
  ou `controlcenter_find_skill` pour savoir si une famille existe déjà.
- Lancer `testing/` (privacy_gate + tests de métadonnées) avant tout commit.
- **Ne pas éditer à la main** les fichiers de registre (`registry/components.json`, `SKILLS-MAP.md`, `llms.txt`) — ils sont générés (`build_public_registry.py`, `build_skills_map.py`,
  `catalog.py`). Si une session étrangère non committée tourne actuellement dans le clone canonique, NE PAS régénérer globalement (cela mélangerait
  modifications étrangères et propres dans un même fichier) — committer plutôt isolément le nouveau dossier de skill et laisser la régénération du registre
  au prochain passage propre (`skill-register-care`).
- `git commit -- skills/<kategorie>/<name>/` — uniquement les chemins propres et nouveaux.

## Compatibilité avec le format Anthropic

Tous les champs supplémentaires sont de simples extensions YAML à côté de `name`/`description` — un Claude Code standard hors de cet écosystème lit toujours uniquement
`name`/`description` et ignore le reste. `config.json`/`connections.json` sont des ressources groupées optionnelles (comme prévu dans
`docs/CONVENTIONS.md`), pas une dépendance obligatoire — un skill sans elles fonctionne à l'identique.

## Skills apparentés

- `skill-creator:skill-creator` — boucle générique entretien/évaluation (délégué, étape 1).
- `skill-finder` — routeur des skills propres existants (à vérifier AVANT de construire : cela existe-t-il déjà ?).
- `skill-explorer` — audit du paysage + recherche web de nouveaux skills/plugins (niveau méta : le *parc* de nos skills ; ce skill-ci rend au contraire chaque skill *produit* conscient des fournisseurs).
- `skill-family-care`, `skill-register-care` — maintenance après la construction.
- `grounding-seed` (module, `.AI/.MODULES/.CONTROL/grounding-seed`) — la logique réelle de raccordement/auto-approvisionnement, seulement référencée ici, non dupliquée.

## Journal des modifications

### 0.2.0 (2026-08-24)
- Complément (ticket T-20260824-218233618, extension du périmètre) : motif réutilisable d'apprentissage/couverture
  ajouté pour chaque skill produit — `user-usecases.json`,
  `usecase-gaps.json`, `known-providers-and-abilities.json`,
  `gap-closing-analysis.json` (nouveaux schémas maison dans `.SKILLS/schemas/`) plus le champ de contrat d'apprentissage dans
  `config.json`. `evals/evals.json` (skill-creator) volontairement réutilisé plutôt que dupliqué. `grounding-seed` examiné — aucune extension
  nécessaire (justification dans `references/LEARNING-CONTRACT-AND-COVERAGE.md`), donc pas de ticket de suivi. Les noms de champs des catalogues de fournisseurs sont calqués sur le protocole A2A (`AgentSkill`)
  au lieu d'un vocabulaire propre.

### 0.1.0 (2026-08-24)
- Première version. Décision de construction propre plutôt que fork prise et justifiée (ticket
  T-20260824-218233618). Délègue la création générique de skills à
  `skill-creator:skill-creator`, ajoute le squelette maison, les principes ellmos,
  le raccordement `grounding-seed` (config.json/connections.json), la conscience des fournisseurs et l'auto-mise à jour.
