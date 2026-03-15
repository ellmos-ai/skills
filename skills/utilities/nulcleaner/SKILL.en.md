---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Finds and deletes Windows-reserved NUL files created by
  using /dev/null in Git Bash. Headless or with GUI.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/tools/nulcleaner.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# nulcleaner - Windows NUL File Cleanup

## The Problem

When `/dev/null` is used in commands under Git Bash on Windows (e.g., `> /dev/null`),
instead of redirecting to nowhere, an actual **file named `nul`** is created in the current
directory. Windows reserves "NUL" as a device name, which means these files cannot be
deleted normally.

This tool finds and deletes such NUL files via the extended UNC path (`\\?\`).

---

## Modes

| Mode | Description |
|------|-------------|
| `scan` | Recursively scan directory for NUL files |
| `delete` | Find and delete NUL files |
| `gui` | Graphical interface with file selection |

---

## CLI Usage

```bash
# Scan only (shows found NUL files)
python nulcleaner.py scan /path/to/directory

# Scan and delete
python nulcleaner.py delete /path/to/directory

# Start GUI mode
python nulcleaner.py gui
```

---

## Headless API (for Integration)

The tool also provides a Python API for headless operation:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/path/to/directory", verbose=True)
print(f"Found: {result['found']}, Deleted: {result['deleted']}")
```

**Return value:** `{'found': int, 'deleted': int, 'errors': list}`

---

## Technical Details

- Uses the extended UNC path (`\\?\`) to delete Windows-reserved filenames
- Recursive scan with `os.walk()`
- GUI with tkinter (no external dependencies)
- Only works on Windows (where the problem occurs)

---

## Prevention

Best to avoid `/dev/null` in Git Bash altogether. Instead:
- Simply omit the output
- Use `2>&1` for stderr redirection
- Pay attention to Windows compatibility in shell scripts
