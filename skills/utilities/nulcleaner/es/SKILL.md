---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Busca y elimina archivos NUL reservados de Windows creados al usar /dev/null en Git Bash. Sin interfaz (headless) o con interfaz gráfica (GUI).
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/nulcleaner.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `nulcleaner`.

# nulcleaner - Windows NUL File Cleanup (Español)

## El problema

Cuando se utiliza `/dev/null` en comandos bajo Git Bash en Windows (p. ej., `> /dev/null`), en lugar de redirigir a ninguna parte, se crea un **archivo real llamado `nul`** en el directorio actual. Windows reserva "NUL" como nombre de dispositivo, lo que significa que estos archivos no se pueden eliminar de forma normal.

Esta herramienta busca y elimina dichos archivos NUL mediante la ruta UNC extendida (`\\?\`).

---

## Modos

| Modo | Descripción |
|------|-------------|
| `scan` | Escanear recursivamente el directorio en busca de archivos NUL |
| `delete` | Buscar y eliminar archivos NUL |
| `gui` | Interfaz gráfica con selección de archivos |

---

## Uso de la CLI

```bash
# Solo escanear (muestra los archivos NUL encontrados) (Español)
python nulcleaner.py scan /path/to/directory

# Escanear y eliminar (Español)
python nulcleaner.py delete /path/to/directory

# Iniciar modo GUI (Español)
python nulcleaner.py gui
```

---

## API Headless (para integración)

La herramienta también proporciona una API de Python para su funcionamiento sin interfaz gráfica:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/path/to/directory", verbose=True)
print(f"Found: {result['found']}, Deleted: {result['deleted']}")
```

**Valor devuelto:** `{'found': int, 'deleted': int, 'errors': list}`

---

## Detalles técnicos

- Utiliza la ruta UNC extendida (`\\?\`) para eliminar nombres de archivos reservados de Windows
- Escaneo recursivo con `os.walk()`
- GUI con tkinter (sin dependencias externas)
- Solo funciona en Windows (donde ocurre el problema)

---

## Prevención

Es mejor evitar por completo el uso de `/dev/null` en Git Bash. En su lugar:
- Simplemente omita la salida
- Utilice `2>&1` para la redirección de stderr
- Preste atención a la compatibilidad con Windows en los scripts de shell
