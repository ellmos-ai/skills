---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Reparación de mojibake para UTF-8 con codificación doble/triple. Corrige malinterpretaciones de Windows cp1252/Latin-1. Cero dependencias.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/encoding_fix.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `encoding-fix`.


# Encoding Fix (Español)

Repara mojibake (UTF-8 con codificación doble/triple) causado por la mala interpretación de Windows cp1252/Latin-1. Cero dependencias — solo la librería estándar de Python.

## Problema típico

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## Uso

### Como librería
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### Salida de subproceso
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## Características

- **Idempotente:** El texto correctamente codificado no se modifica
- **Hasta 3 rondas:** Repara incluso cadenas con triple codificación
- **Decodificador de subprocesos:** Alternativa UTF-8/cp1252 para la salida de procesos
- **Cero dependencias:** Solo la librería estándar de Python

## Historial de cambios

### 1.0.0 (2026-03-12)
- Portado desde BACH system/tools/encoding_fix.py
