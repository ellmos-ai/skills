---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Batch file operations (delete, move, copy, list) with glob patterns.
  CLI tool for efficient filesystem operations. Zero dependencies.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: en
status: active

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

# batch_file_ops - Batch File Operations

CLI tool for efficient batch operations on files using glob patterns.
Supports: delete, move, copy, list. Zero dependencies (Python stdlib only).

---

## Actions

| Action | Description |
|--------|-------------|
| `delete` | Delete files matching a pattern |
| `move` | Move files matching a pattern |
| `copy` | Copy files matching a pattern |
| `list` | List files matching a pattern |

## CLI Usage

```bash
python batch_file_ops.py <action> <source> [<target>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `action` | `delete`, `move`, `copy`, or `list` |
| `source` | Source directory |
| `target` | Target directory (only for `move` and `copy`) |
| `--pattern`, `-p` | Glob pattern (e.g., `*.py`, `TOOLS_*.py`) - Default: `*` |
| `--dry-run`, `-n` | Preview only, no changes |
| `--recursive`, `-r` | Search recursively in subdirectories |

---

## Examples

```bash
# List all Python files in a directory
python batch_file_ops.py list /path/to/directory --pattern "*.py"

# Delete all .tmp files (dry-run first!)
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp"

# Move files
python batch_file_ops.py move /source /target --pattern "*.txt"

# Copy files (recursive)
python batch_file_ops.py copy /source /target --pattern "*.md" --recursive

# Pattern examples
python batch_file_ops.py delete /path --pattern "TOOLS_*.py"
python batch_file_ops.py list /path --pattern "backup_202?-*"
```

---

## Notes

- **Dry-run first:** Always use `--dry-run` first with `delete` and `move`
- **Glob patterns:** Uses Python `pathlib.glob()` / `pathlib.rglob()`
- **Windows-compatible:** Automatic UTF-8 output encoding
- **Files only:** Directories are skipped (only files are processed)
