---
name: dev
version: 0.1.1
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-11-22
description: "Utiliser pour obtenir un aperçu rapide d'un projet logiciel via analyse headless et orienter vers les bons outils de développement (ex. 'scanner le projet', 'état du projet', 'lancer CodeCommander', /dev). Analyse la structure et route vers CodeCommander MCP et ellmos-code-tools sans stockage propre. NE PAS utiliser pour des pipelines de développement automatisés avancés (utiliser dev/dev-soft-agent)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: fr
status: active
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="dev banner">

> **Français** — Version française officielle de la compétence `dev`.

# Dev — Assistant développeur (ATI)

Fournit d'abord une vue d'ensemble, puis transmet aux bons outils.

## Objectif

Successeur de l'agent ATI/entwickler de BACH. Deux missions :
1. **Analyse du projet** (headless, stdlib) : vue d'ensemble rapide et économe en
   tokens de la structure, des langages et des marqueurs de build d'un projet —
   avant de lancer une analyse coûteuse.
2. **Routage d'outils :** oriente vers les outils de développement existants au
   lieu de les dupliquer.

## Déclencheurs

| Entrée utilisateur | Action |
|---|---|
| « Donne-moi une vue d'ensemble du projet X » | `dev_core.py scan <pfad>` |
| « Quel est ce projet / quelle stack ? » | `dev_core.py scan <pfad>` |
| « Analyse ce fichier / refactorise » | → CodeCommander-MCP |
| « Génère/vérifie du code Python » | → CodeCommander-MCP / ellmos-code-tools |

## Paysage d'outils (cibles de routage)

- **CodeCommander-MCP** (`.AI/.MCP/ellmos-codecommander-mcp`) : `cc_analyze_code`,
  `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`,
  `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation`, etc.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`) : outils CLI de
  développement (Structural-Edit, contexte pycutter, Method-Analyzer).
- **FileCommander-MCP** : opérations sur fichiers et répertoires sur de grandes arborescences.

## Point d'entrée CLI (`dev_core.py`)

```bash
python dev_core.py scan .              # projet actuel
python dev_core.py scan /chemin/projet # structure + langages + marqueurs
```

Détecte entre autres : Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go,
Java, Roblox (Rojo), Docker, dépôt Git.

## Stockage

Aucun stockage. Analyse et routage uniquement.

## Posture

Nous recommandons CodeCommander/ellmos-code-tools comme outils de développement, mais
restons ouverts à d'autres (p. ex. ruff/pylint/eslint) si l'utilisateur le préfère.

## Confidentialité

- `dev_core.py` ne lit que les noms de fichiers et de répertoires (structure), aucun contenu, aucun envoi.
- Sont ignorés notamment : `.git`, `node_modules`, `.venv`, `__pycache__`.

## Ressources associées

- `assist/AGENTS.md` — Routeur principal
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## Journal des modifications

### 0.1.1 (2026-11-22)
- Avis de langue corrigé

### 0.1.0 (2026-06-22)
- Version initiale. Successeur d'ATI/entwickler : analyse de projet headless (stdlib) +
  routage vers CodeCommander-MCP / ellmos-code-tools. Neutre envers l'utilisateur, sans stockage.