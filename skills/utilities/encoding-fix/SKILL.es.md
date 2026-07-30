---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Reparación de mojibake para UTF-8 con doble/triple codificación. Corrige malas interpretaciones de Windows cp1252/Latin-1. Sin dependencias.

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

Repara el mojibake (UTF-8 con doble o triple codificación) causado por una mala interpretación de Windows cp1252/Latin-1. Sin dependencias externas — solo la biblioteca estándar de Python.

## Problema Típico

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## Uso

### Como Biblioteca
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### Salida de Subprocesos
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### Línea de Comandos (CLI)
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## Características

- **Idempotente:** El texto codificado correctamente no se modifica
- **Hasta 3 rondas:** Repara incluso cadenas con triple codificación
- **Decodificador de subprocesos:** Mecanismo de reserva UTF-8/cp1252 para la salida de procesos
- **Sin dependencias:** Solo la biblioteca estándar de Python

## Registro de Cambios

### 1.0.0 (2026-03-12)
- Portado desde BACH system/tools/encoding_fix.py