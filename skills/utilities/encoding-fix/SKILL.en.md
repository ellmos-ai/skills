---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-09
description: "Use when text files suffer from character encoding corruption or mojibake (e.g. 'fix broken encoding', 'repair umlauts/mojibake', 'double-encoded UTF-8', /encoding-fix). Repairs cp1252, Latin-1, and multi-encoded UTF-8 text files without external dependencies. Do NOT use for clean format conversions without corrupted bytes."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/encoding_fix.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---



<img src="banner.png" width="100%" alt="encoding-fix banner">

> **English** — Offizielle English-Version / Documento Oficial en English.


# Encoding Fix (English)

Repairs mojibake (double/triple encoded UTF-8) caused by Windows cp1252/Latin-1
misinterpretation. Zero dependencies — Python stdlib only.

## Typical Problem

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## Usage

### As Library
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### Subprocess Output
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## Features

- **Idempotent:** Correctly encoded text is not modified
- **Up to 3 rounds:** Repairs even triple-encoded strings
- **Subprocess decoder:** UTF-8/cp1252 fallback for process output
- **Zero dependencies:** Python stdlib only

## Changelog

### 1.0.0 (2026-03-12)
- Ported from BACH system/tools/encoding_fix.py