---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Procedimiento estándar para la incorporación de nuevos proyectos de software: análisis de funciones, revisión de calidad de código, lista de verificación e integración de tareas.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `project-onboarding`.


# Procedimiento estándar de incorporación para nuevos proyectos de software (Español)

**Versión:** 1.0
**Fecha:** 2026-03-12

---

## Descripción general y propósito

Este procedimiento define qué pasos realizar en las carpetas de software recién descubiertas antes de agregarlas a un sistema de gestión de tareas.

```
+─────────────────────────────────────────────────────+
|           STANDARD ONBOARDING PROCEDURE              |
+─────────────────────────────────────────────────────+
|  1. Create feature analysis                          |
|  2. Code quality review (standard tests)             |
|  3. Create TASKS.txt                                 |
|  4. Add to task management                           |
+─────────────────────────────────────────────────────+
```

---

## Fase 1: Análisis de funciones

**Propósito:** Comprender la herramienta, sus funciones y el estado de desarrollo.

**Crear archivo:** `Feature_Analysis_<ToolName>.md`

### Plantilla

```markdown
# Feature Analysis: <ToolName> (Deutsch)

## Brief Description
A short sentence describing what the tool does.

---

## Highlights

| Feature | Description |
|---------|-------------|
| **Feature 1** | Description |
| **Feature 2** | Description |

---

## Development Stage Assessment

### Current Status: **<Status> (<X>%)**

Possible statuses:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Category | Rating (1-5) | Details |
|----------|:------------:|---------|
| **Functionality** | 3 | |
| **UI/UX** | 3 | |
| **Stability** | 3 | |
| **Documentation** | 3 | |

---

## Recommended Extensions

### Priority: High
1. ...

### Priority: Medium
2. ...

### Priority: Low
3. ...

---

## Technical Details

Framework:      <Framework>
File size:      <X> lines of Python
Main file:      <main.py>

---

*Analysis created: <Date>*
```

---

## Fase 2: Revisión de calidad de código

**Propósito:** Garantizar la calidad técnica e identificar problemas conocidos.

### Comprobaciones recomendadas

| Prueba | Herramienta | Descripción |
|--------|-------------|-------------|
| **Codificación** | Comprobador de codificación (p. ej., `chardet`, `file`) | Garantizar UTF-8 |
| **Análisis de métodos** | Linter (p. ej., `pylint`, `flake8`) | Encontrar métodos grandes |
| **Sangría** | Formateador (p. ej., `black`, `autopep8`) | Comprobar coherencia |
| **Importaciones** | Comprobador de importaciones (p. ej., `isort`, `pylint`) | Encontrar importaciones no utilizadas |

### Puntos de verificación

- [ ] ¿Todos los archivos .py están codificados en UTF-8?
- [ ] ¿Sin métodos inusualmente grandes (>100 líneas)?
- [ ] ¿Sangría coherente (espacios vs tabulaciones)?
- [ ] ¿Se eliminaron las importaciones no utilizadas?
- [ ] ¿Docstrings presentes?

### Documentar resultados

Registrar problemas en TASKS.txt en "QUALITY REVIEW".

---

## Fase 3: Crear TASKS.txt

**Propósito:** Capturar tareas pendientes en un formato estructurado.

**Crear archivo:** `TASKS.txt` en la carpeta del proyecto

### Plantilla

```
TASKS - <ToolName> V<Version>
==============================
Status: <Status>
Date: <Date>

OPEN TASKS:
[ ] <Task 1> - Effort: <LOW|MEDIUM|HIGH>
[ ] <Task 2> - Effort: <LOW|MEDIUM|HIGH>

---
DONE (Archive):
- <Completed task> (<Version>, <Date>)
```

### Valores de estado

| Estado | Significado |
|--------|-------------|
| NEWLY DISCOVERED | Aún no analizado |
| ANALYSIS NEEDED | Análisis de funciones en progreso |
| QUALITY REVIEW | Pruebas de código en ejecución |
| VALIDATED & READY | Listo para funciones |
| MVP | Producto Mínimo Viable |
| BUILD ONLY | Solo se requiere compilación |
| BLOCKED | Esperando prueba/decisión del usuario |

---

## Fase 4: Integración en la gestión de tareas

Después de completar las fases 1-3:

1. **Transferir tareas:** Crear entradas de TASKS.txt como tareas/problemas
2. **Verificar:** ¿Todas las tareas están correctamente categorizadas?
3. **Categorizar:** Asignar el proyecto a la categoría adecuada (herramienta individual, suite, biblioteca, etc.)

### Tareas automáticas de incorporación

Para nuevos proyectos, crear las siguientes tareas estándar:

| Tarea | Descripción | Esfuerzo |
|-------|-------------|----------|
| onb_1 | Crear análisis de funciones | medio |
| onb_2 | Revisión de calidad de código | bajo |
| onb_3 | Crear TASKS.txt | bajo |

Las tareas tienen dependencias: onb_2 depende de onb_1, onb_3 depende de onb_2.

---

## Lista de verificación rápida

```
[ ] 1. Feature_Analysis_<Name>.md created
[ ] 2. Code quality review completed (linter, encoding, imports)
[ ] 3. TASKS.txt created with status
[ ] 4. Tasks added to task management
```

---

## Ejemplo y uso

```bash
# 1. Feature analysis (Deutsch)
# -> Create Feature_Analysis_MyTool.md (see template) (Deutsch)

# 2. Code quality (Deutsch)
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Check encoding

# 3. TASKS.txt (Deutsch)
# -> Create in tool folder with status "QUALITY REVIEW" (Deutsch)

# 4. Create tasks (Deutsch)
# -> Capture TASKS.txt entries as issues/tickets (Deutsch)
```

---

*Creado: 2026-01-10 | Adaptado: 2026-03-12*
