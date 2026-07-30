---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: Asistente de desarrollo (sucesor de ATI). Proporciona una visión general rápida del proyecto mediante un escaneo headless y redirige a las herramientas de código disponibles: CodeCommander MCP (análisis/refactorización/diagnóstico) y el módulo ellmos-code-tools. Enrutamiento puro de herramientas + escaneo, sin almacenamiento propio.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: es
status: active
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="dev banner">

> **Español** — Versión oficial en español de `dev`.


# Dev — Asistente de Desarrollo (ATI) (Español)

Obtiene primero una visión general y luego delega en las herramientas adecuadas.

## Descripción general y propósito

Sucesor del agente ATI/entwickler de BACH. Dos tareas principales:
1. **Escaneo de proyecto** (headless, stdlib): visión general rápida y eficiente en tokens sobre la estructura, los lenguajes y los indicadores de compilación de un proyecto, antes de ejecutar análisis costosos.
2. **Enrutamiento de herramientas:** delega en las herramientas de código existentes en lugar de duplicar su funcionalidad.

## Disparadores (Triggers)

| Entrada del usuario | Acción |
|---|---|
| "Obtén una visión general del proyecto X" | `dev_core.py scan <path>` |
| "¿Qué tipo de proyecto es este / qué stack usa?" | `dev_core.py scan <path>` |
| "Analiza este archivo / refactoriza" | → CodeCommander MCP |
| "Genera/revisa código Python" | → CodeCommander MCP / ellmos-code-tools |

## Panorama de herramientas (Objetivos de enrutamiento)

- **CodeCommander MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`, `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`, `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation`, etc.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): Herramientas de desarrollo CLI (Structural-Edit, pycutter context, Method-Analyzer).
- **FileCommander MCP**: Operaciones de archivos y directorios en árboles de gran tamaño.

## Punto de entrada CLI (dev_core.py)

```bash
python dev_core.py scan .              # current project
python dev_core.py scan /path/project  # structure + languages + markers
```

Detecta, por ejemplo: Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go, Java, Roblox (Rojo), Docker, repositorio Git.

## Almacenamiento (Store)

Sin almacenamiento. Puro escaneo + enrutamiento.

## Actitud

Recomendamos CodeCommander/ellmos-code-tools como herramientas de código, pero estamos abiertos a otras (p. ej., ruff/pylint/eslint) si el usuario las prefiere.

## Privacidad

- `dev_core.py` solo lee nombres de archivos/directorios (estructura), sin contenido, sin subida de datos.
- Se omiten: `.git`, `node_modules`, `.venv`, `__pycache__`, etc.

## Recursos relacionados

- `assist/AGENTS.md` — Enrutador general
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## Historial de cambios

### 0.1.0 (2026-06-22)
- Versión inicial. Sucesor de ATI/entwickler: escaneo de proyecto headless (stdlib) + enrutamiento a CodeCommander MCP / ellmos-code-tools. Neutral para el usuario, sin almacenamiento.