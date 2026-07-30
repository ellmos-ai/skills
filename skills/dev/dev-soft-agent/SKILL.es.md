---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Canalización automatizada de desarrollo de software. Escanea proyectos, prioriza tareas, analiza código u orquesta bucles de desarrollo. Cero dependencias (solo biblioteca estándar de Python).
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="dev-soft-agent banner">
> **Español** — Versión oficial en español de `dev-soft-agent`.

# Dev Soft Agent (Español)

Canalización automatizada de desarrollo de software. Extraída del agente ATI de BACH,
se ejecuta de forma completamente independiente utilizando únicamente la biblioteca estándar de Python.

## Componentes

```
scripts/
  config.py              Configuración (carpetas de escaneo, prefijos de nombres, pesos)
  project_manager.py     Escaneo de proyectos + clasificación por convención de nombres
  task_engine.py          Analizador de TASKS.txt + escáner de código (TODO/FIXME)
  code_analyzer.py       Análisis estático (LOC, importaciones, clases, funciones)
  dev_loop.py            Orquestador (DevLoop)
  policies/
    naming.py            Validación de snake_case / PascalCase / SCREAMING_SNAKE
    encoding.py          Cumplimiento de UTF-8 + detección de BOM
    paths.py             Detección de rutas codificadas de forma rígida (hardcoded)
  prompt_templates/
    task_prompt.txt      Prompt de LLM para procesamiento de tareas
    review_prompt.txt    Prompt de LLM para revisión de código
    analysis_prompt.txt  Prompt de LLM para análisis de proyecto
```

## Uso como biblioteca de Python

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# Escanear proyectos (Español)
projects = loop.scan_projects()

# Seleccionar proyecto (selección aleatoria ponderada por convención de nombres) (Español)
project = loop.select_project()

# Analizar código (Español)
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# Cargar y priorizar tareas (Español)
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# Sesión de desarrollo completa (Español)
result = loop.run_session()
loop.save_session()
```

## Uso como CLI

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## Convención de nombres (Clasificación de proyectos)

Los proyectos se clasifican según el nombre de su carpeta:

| Prefijo | Etiqueta | Peso | Significado |
|---------|----------|------|-------------|
| `RDY` | Ready (Listo) | 1.0 | Máxima prioridad |
| `RDY_FAST` | Fast Ready | 0.5 | Rápido de completar |
| `FAST` | Fast | 0.33 | Tarea pequeña |
| `DEV` | Development | 0.17 | En desarrollo |
| `REL` | Released | 0.0 | Finalizado, no requiere trabajo |
| `ARC` | Archived | 0.0 | Archivado |

El peso determina la probabilidad en la selección aleatoria.

## Formato de TASKS.txt

```markdown
# TASKS - NombreDelProyecto (Español)
# A fecha de: 2026-03-12 (Español)

## OPEN
- [ ] [BUG] Descripción del error
- [ ] [FEATURE] Nueva función

## IN PROGRESS
- [-] [REFACTOR] Reestructuración de código

## DONE
- [x] [BUG] Error corregido -- DONE 2026-03-01
```

## Políticas (Policies)

Políticas de calidad que se pueden verificar automáticamente contra el código:

- **NamingPolicy:** snake_case para módulos/funciones, PascalCase para clases
- **EncodingPolicy:** Forzar UTF-8, detectar BOM, señalar CRLF
- **PathPolicy:** Detectar e informar rutas absolutas codificadas de forma rígida

## Historial de cambios

### 0.1.0 (2026-03-12)
- Migración desde MODULAR_AGENTS/devSoftAgent a la biblioteca de habilidades.
- Escáner de proyectos, motor de tareas, analizador de código, DevLoop.
- 3 políticas (nombres, codificación, rutas).
- 3 plantillas de prompt (tarea, revisión, análisis).