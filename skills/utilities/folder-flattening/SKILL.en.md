---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Restructure nested folder hierarchies into flat, machine-readable layouts.
  Bash-based with intelligent merge logic.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: utilities
tags: [folder, flattening, filesystem, bash, reorganization, cleanup]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ordner-flattening.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Workflow: Folder Flattening

Goal: Convert nested folder structures into a flat, machine-readable structure.
Advantage: No more clicking through directories — search via database (Verzeichnis.db) instead.
Duplicates are allowed when thematically meaningful.

---

## Phase Overview

| Phase | What Happens | Script Section |
|-------|-------------|----------------|
| 1 | Flatten: Pull all subfolders to one level | `phase_flatten` |
| 2 | Shorten: Truncate long path names to last segment, merge on conflicts | `phase_shorten` |
| 3 | Clean up: Resolve multiple underscores (`___`), remove trailing `_` | `phase_cleanup_underscores` |
| 4 | Group: Number folders, CD folders, short names into collection folders | `phase_group_problematic` |
| 5 | Triplet analysis: Sliding groups of 3, shortest name as merge target | `phase_tripel_merge` |
| 6 | Media format merge: Consolidate folders by file type (template) | `phase_media_merge` |
| 7 | Clean up: Delete empty folders | `phase_cleanup_empty` |

---

## Important Rules

### Triplet Analysis Matching
- **Substring**: `Education` in `EducationalBrochures` -> merge into `Education`
- **Plural/Umlaut**: `Room` = `Rooms`, `Part` = `Parts`, `Book` = `Books`
- **First word**: `Autism ADHD` matches `Autism Career` (same beginning)

### Minimum Length
- Single-word name without spaces: **at least 8 characters** (prevents `Hand`, `House`, `Form`)
- With spaces (e.g., `ICF Catalog`): **from 3 characters OK**
- This keeps `ICF`, `ASD Women` etc. permitted

### Restart After Merge
After each merge, the folder list is reloaded and restarted at the merge target.
This way, e.g., `Autism` collects all extensions before moving on.

---

## Media Format Merge (Template System)

Phase 6 uses a template array `MEDIA_TYPES`. Each entry defines:
- Target folder (with `_` prefix)
- File extensions belonging to this type

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Images|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Extensible:
    # "_Spreadsheets|xlsx|xls|csv|ods"
    # "_Presentations|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

Only folders containing **exclusively** files of one type are moved.
Folders with subfolders are skipped.

### Adding a New Media Type

Simply add a new line to the `MEDIA_TYPES` array:
```bash
"_TargetFolder|ext1|ext2|ext3"
```

---

## Execution

```bash
# Complete run:
cd /path/to/target/directory
bash ordner_flattening_komplett.sh

# Or individual phases:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## Experience Values (Session 2026-01-26)

- Start: 206 folders + 252 loose files, ~5600 nested subfolders
- After flatten: ~2200 folders on one level
- After shorten + clean up: ~2005 folders
- After grouping (numbers, CDs): ~2005 -> collection folders created
- After triplet v1: ~1561 folders
- After triplet v2 (8-character rule): further reduction
- Media format phase: Audio/video/image folders consolidated
