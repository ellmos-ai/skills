---
name: batch-file-ops
version: 1.0.1
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-22
description: "Utilisez cette compétence lorsque des opérations par lots sur le système de fichiers telles que supprimer, déplacer, copier ou lister via des motifs glob doivent être exécutées (par ex. 'déplacer tous les fichiers *.log', 'renommer/supprimer en lot', /batch-file-ops). Sans dépendance externe ; ne PAS utiliser pour des modifications sémantiques de texte."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: fr
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/batch_file_ops.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="batch-file-ops banner">

> **Français** — Version française officielle de la compétence `batch-file-ops`.

# batch_file_ops — Opérations par lots sur fichiers

Outil CLI pour exécuter efficacement des opérations par lots sur des fichiers à l'aide de motifs glob. Prend en charge : `delete`, `move`, `copy`, `list`. Zéro dépendance (uniquement la bibliothèque standard Python).

---

## Actions

| Action | Description |
|--------|-------------|
| `delete` | Supprimer les fichiers correspondant au motif |
| `move` | Déplacer les fichiers correspondant au motif |
| `copy` | Copier les fichiers correspondant au motif |
| `list` | Lister les fichiers correspondant au motif |

## Utilisation CLI

```bash
python batch_file_ops.py <action> <source> [<cible>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `action` | `delete`, `move`, `copy` ou `list` |
| `source` | Dossier source |
| `cible` | Dossier cible (uniquement pour `move` et `copy`) |
| `--pattern`, `-p` | Motif glob (par ex. `*.py`, `TOOLS_*.py`) - par défaut : `*` |
| `--dry-run`, `-n` | Afficher uniquement, ne rien modifier |
| `--recursive`, `-r` | Rechercher récursivement dans les sous-dossiers |

---

## Exemples

```bash
# Lister tous les fichiers Python dans un dossier
python batch_file_ops.py list /chemin/vers/dossier --pattern "*.py"

# Supprimer tous les fichiers .tmp (d'abord simulation à blanc !)
python batch_file_ops.py delete /chemin/vers/dossier --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /chemin/vers/dossier --pattern "*.tmp"

# Déplacer des fichiers
python batch_file_ops.py move /source /cible --pattern "*.txt"

# Copier des fichiers (récursif)
python batch_file_ops.py copy /source /cible --pattern "*.md" --recursive

# Exemples de motifs
python batch_file_ops.py delete /chemin --pattern "TOOLS_*.py"
python batch_file_ops.py list /chemin --pattern "backup_202?-*"
```

---

## Remarques

- **Simulation à blanc d'abord :** Pour `delete` et `move`, toujours utiliser `--dry-run` en premier
- **Motifs glob :** Utilise `pathlib.glob()` / `pathlib.rglob()` de Python
- **Compatible Windows :** Encodage de sortie UTF-8 automatique
- **Fichiers uniquement :** Les dossiers sont ignorés (seuls les fichiers sont traités)

## Journal des modifications

### 1.0.1 (2026-11-22)
- Indication de langue corrigée
