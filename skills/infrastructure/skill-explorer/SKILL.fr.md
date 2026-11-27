---
name: skill-explorer
version: 1.1.3
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-11-27
description: "À utiliser pour « comparer/auditer les compétences », « quelles compétences sont en double », « former des familles de compétences », « nettoyer/consolider les compétences », « entretenir le registre des compétences », « trouver des compétences/plugins pour le sujet X », « installer de nouvelles compétences », « parcourir le marketplace » ou pour `/skill-explorer`. Gère votre paysage de compétences : recense et compare l'existant (mode Audit), recherche de nouvelles compétences/plugins sur le web (mode Explore) et génère des sous-compétences légères (Skill-Finder, parapluies de famille, compétences de maintenance) au lieu d'un monolithe."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: fr
status: active
visibility: public
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="skill-explorer banner">

> **Français** — Version française officielle de la compétence `skill-explorer`.

# Skill-Explorer — Gérer le paysage de compétences (Audit · Explore · Installateur)

## Objectif

À mesure que le stock de compétences grandit apparaissent des doublons, des ressources inutilisées et des situations
floues du type « quelle compétence plutôt que laquelle » — tandis que de nouveaux skills/plugins sortent sans cesse.
`skill-explorer` réunit trois rôles dans un seul outil :

| Rôle | Ce qu'il fait | Détail |
| --- | --- | --- |
| **Mode Audit** (vers l'intérieur) | examiner toutes les compétences, regrouper par familles, recenser capacités/dépendances/ressources, sous-rapport par famille + recommandations numérotées | `references/audit-mode.md` |
| **Mode Explore** (vers l'extérieur) | rechercher bilingue sur le web (Web/GitHub/Reddit) de nouveaux skills/plugins sur un sujet, comparer, installer sous contrôle | `references/explore-mode.md` |
| **Installateur** | *générer* des sous-compétences légères plutôt qu'un monolithe — Skill-Finder, parapluie de famille, compétences de maintenance | ci-dessous + `references/family-care.md` |

Appel : `/skill-explorer` (Audit par défaut) ou « trouver des … pour le sujet X » (Explore). Les deux modes partagent
taxonomie (`references/clustering.md`), format de rapport (`references/report-format.md`) et schéma de
numérotation afin que l'utilisateur puisse répondre par une unique liste de numéros.

## Principe d'installateur et persistance

Plutôt que de croître lui-même de manière monolithique, `skill-explorer` *génère* au besoin des sous-compétences
légères et chargeables individuellement — ainsi, aucune compétence unique démesurée n'a besoin d'être chargée :

- **Skill-Finder** ([F]) — routeur/rechercheur actif analogue à un portier « using-superpowers », qui lit
  le registre avant chaque tâche et oriente vers la bonne famille (`references/skill-finder.md`,
  modèle `assets/skill-finder-template.md`).
- **Parapluie de famille** (c1) — méta-compétence qui connaît toute une famille (`assets/family-umbrella-template.md`).
- **Compétences de maintenance** ([P1] Familles, [P2] Registre) — maintiennent familles et registre à jour (`references/family-care.md`).

Les décisions sont persistées dans `~/.claude/skills/skill-explorer/config.json`
(`references/config.md`, modèle `assets/config.example.json`) : lire au démarrage (familles connues,
routeurs, sous-compétences générées), mettre à jour après exécution — ainsi une réexécution ne crée rien en double.

## Mécanisme de branche (adapter des tiers)

Une compétence en lecture seule (plugin, tiers importé) peut être adaptée sans modifier l'original :
le répertoire d'origine est entièrement copié (**Branche**) ; ensuite seule la copie est éditée.
La branche porte quatre mentions obligatoires : référence à l'original, date de branchement,
auteur de la modification et motif. Dès que la branche remplace l'original, celui-ci est désenregistré pour
le runtime (`SKILL.md` → `CONTENT.md`) ou le routeur de famille pointe vers la branche afin que deux compétences
quasi identiques n'entrent pas en collision. Les branches tierces restent **privées** — elles ne rejoignent
pas la bibliothèque publique `.AI/.SKILLS`. Détails : `references/skill-branching.md`.

## Déroulement

1. **Choisir le mode :** examiner/nettoyer l'existant → Mode Audit. Chercher/installer depuis l'extérieur →
   Mode Explore. (Explore peut s'appuyer sur un audit/`config.json` précédent.)
2. **Mode Audit** (`references/audit-mode.md`) : inventaire (script) → regroupement par familles → sous-rapports →
   **une liste de décisions numérotée globalement** (a/b/c1/c2/c3, plus R/F/P1/P2).
3. **Mode Explore** (`references/explore-mode.md`) : recherche bilingue multi-sources → 3 catégories par
   candidat → simulation d'impact → recommandations d'installation/suppression numérotées.
4. **Exécuter** uniquement après confirmation par numéros de l'utilisateur ; enregistrer la création/modification
   et mettre à jour `config.json`.

## Règles d'airain

- **Survey ≠ Mutation :** tout regrouper, mais n'éditer que les compétences **appartenant à l'utilisateur** ;
  les compétences de plugins/tiers sont en lecture seule (jamais d'en-tête ni de suppression). Pour adapter
  une compétence tierce, créer plutôt une **Branche** (copie fork) — l'original reste intact, l'adaptation
  s'effectue exclusivement sur la copie (→ `references/skill-branching.md`).
- **Étendre le registre, ne pas le dupliquer :** s'il existe déjà un registre de compétences (Index + carte
  des familles + compétence d'index), l'étendre plutôt que d'en créer un quatrième.
- **Sécurité d'abord manuelle :** avant toute installation, le modèle lit lui-même la compétence et juge ;
  `scripts/scan_skill_security.py` n'est qu'un triage d'appoint aux limites connues. Jamais d'installation automatique.
- **Enregistrement selon l'origine :** rédigé par l'utilisateur → bibliothèque ; tiers → chemin externe, **pas** la bibliothèque.

## Orchestration (neutre vis-à-vis des modèles)

Les sous-rapports par famille ou les sources/langues constituent des pistes de travail indépendantes. Si la
plateforme propose des sous-agents moins coûteux que l'orchestrateur lui-même, confier chaque famille/source
à un sous-agent et n'utiliser l'orchestrateur que pour consolider/vérifier (essaim de spécialistes). Sinon, traiter séquentiellement soi-même.

## Ressources

- **Modes :** `references/audit-mode.md`, `references/explore-mode.md`
- **Partagé :** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Audit :** `references/family-care.md`, `references/skill-finder.md`
- **Explore :** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Branche :** `references/skill-branching.md`
- **Scripts :** `scripts/inventory_skills.py` (inventaire), `scripts/inject_family_header.py` (routeur d'en-tête),
  `scripts/scan_skill_security.py` (triage sécurité)
- **Modèles :** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`,
  `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Journal des modifications

### 1.1.2 (2026-11-22)
- Mention linguistique corrigée.

### 1.1.1 (2026-08-24)
- L'assistant d'inventaire accepte désormais aussi les anciens mappings `dependencies` sérialisés sur une ligne
  et traite les valeurs corrompues de façon tolérante au lieu d'interrompre tout l'audit. Son message de
  clôture est également compatible avec les consoles Windows.

### 1.1.0 (2026-06-17)
- Ajout du mécanisme de branche : les compétences tierces / en lecture seule peuvent être adaptées via une copie
  fork (branche) — avec référence à l'original, date, éditeur et motif ; l'original reste intact. Règle d'airain
  « Survey ≠ Mutation » étendue avec l'issue par branche. Nouvelle section `## Mécanisme de branche`.
  Ajouts : `references/skill-branching.md`, `assets/branch-header.example.md`.

### 1.0.0 (2026-06-17)
- Version initiale. Réunit l'audit d'inventaire (clustering par familles, décisions numérotées) et la
  recherche web (installation contrôlée avec triage sécurité) dans un installateur générant des sous-compétences légères.
