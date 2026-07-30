---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Operaciones de archivos en lote (eliminar, mover, copiar, listar) con patrones glob. Herramienta de CLI para operaciones eficientes del sistema de archivos. Sin dependencias.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/batch_file_ops.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="batch-file-ops banner">

> **Español** — Versión oficial en español de `batch-file-ops`.


# batch_file_ops - Operaciones de archivos en lote (Español)

Herramienta CLI para operaciones eficientes en lote sobre archivos usando patrones glob.
Soporta: delete, move, copy, list. Sin dependencias (solo la biblioteca estándar de Python).

---

## Acciones

| Acción | Descripción |
|--------|-------------|
| `delete` | Eliminar archivos que coincidan con un patrón |
| `move` | Mover archivos que coincidan con un patrón |
| `copy` | Copiar archivos que coincidan con un patrón |
| `list` | Listar archivos que coincidan con un patrón |

## Uso de CLI

```bash
python batch_file_ops.py <action> <source> [<target>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Argumentos

| Argumento | Descripción |
|-----------|-------------|
| `action` | `delete`, `move`, `copy` o `list` |
| `source` | Directorio de origen |
| `target` | Directorio de destino (solo para `move` y `copy`) |
| `--pattern`, `-p` | Patrón glob (p. ej., `*.py`, `TOOLS_*.py`) - Por defecto: `*` |
| `--dry-run`, `-n` | Solo vista previa, sin cambios |
| `--recursive`, `-r` | Buscar de forma recursiva en subdirectorios |

---

## Ejemplo y aplicación

```bash
# Listar todos los archivos Python en un directorio (Español)
python batch_file_ops.py list /path/to/directory --pattern "*.py"

# Eliminar todos los archivos .tmp (¡primero ejecutar con dry-run!) (Español)
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp"

# Mover archivos (Español)
python batch_file_ops.py move /source /target --pattern "*.txt"

# Copiar archivos (recursivo) (Español)
python batch_file_ops.py copy /source /target --pattern "*.md" --recursive

# Ejemplos de patrones (Español)
python batch_file_ops.py delete /path --pattern "TOOLS_*.py"
python batch_file_ops.py list /path --pattern "backup_202?-*"
```

---

## Notas

- **Dry-run primero:** Use siempre `--dry-run` primero con `delete` y `move`
- **Patrones glob:** Utiliza `pathlib.glob()` / `pathlib.rglob()` de Python
- **Compatible con Windows:** Codificación de salida UTF-8 automática
- **Solo archivos:** Se omiten los directorios (solo se procesan archivos)