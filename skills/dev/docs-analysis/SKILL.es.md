---
name: docs-analysis
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Análisis de requisitos de documentos: analiza los documentos de concepto y requisitos en la carpeta docs/, verifica los requisitos con el código actual y crea un informe de diferencias consolidado.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [docs-analysis, requirements, code-review, diff-report, quality-assurance]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/docs-analyse.md', 'origin_version': '1.2.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `docs-analysis`.


# Análisis de Requisitos de Documentos (Español)

> Analiza todos los documentos de concepto y requisitos, verifica sus requisitos con el código actual y crea un informe de diferencias consolidado.

---

## Resumen y Propósito

Analiza todos los documentos de concepto y requisitos en la carpeta `../docs/`, verifica sus requisitos con el código actual y crea un informe de diferencias consolidado.

---

## Convención de Nombres

### Prefijo y Sufijo
Todos los documentos analizados reciben:
- **Prefijo:** `conN_` donde N = versión de análisis (1, 2, 3, ...)
- **Sufijo:** `_XX` donde XX = porcentaje de cumplimiento (redondeado al 10 más cercano)

### Umbral de Archivado
- **>= 75% cumplido:** El documento se mueve a `../docs/_archive/`
- **< 75% cumplido:** El documento permanece en `../docs/` con prefijo/sufijo
- **Umbral configurable** (por defecto: 75)

---

## Proceso

### Fase 1: Recopilar documentos
- Listar todos los archivos `*.md` y `*.txt` en `../docs/` (raíz)
- Filtrar `README.txt`

### Fase 2: Extraer requisitos
Para cada documento:
- Leer contenido
- Identificar requisitos (listas de verificación, tablas, marcadores MISSING/TODO)
- Categorizar: Estructura, Código, API, Esquema BD, CLI, Funcionalidad

### Fase 3: Verificación de código
Para cada requisito:
- Determinar método de verificación (Glob, Grep, Read)
- Ejecutar verificación
- Marcar como: FULFILLED, PARTIAL, MISSING

### Fase 4: Evaluación
- Contar requisitos cumplidos vs. pendientes
- Calcular porcentaje de cumplimiento (%)
- Decidir: archivar (>= 75%) o conservar (< 75%)

### Fase 5: Generar salida
- Crear `REQUIREMENTS_ANALYSIS.md` (resumen)
- Crear `consense_diff.md` (solo requisitos pendientes, por prioridad)

### Fase 6: Versionado
- Escanear prefijo `conN_` más alto
- Nueva versión = más alto + 1

### Fase 7: Renombrar y mover
- Aplicar nuevo prefijo/sufijo a los documentos
- Archivar o conservar

---

## Salida

| Archivo | Descripción |
|---------|-------------|
| `conN_REQUIREMENTS_ANALYSIS.md` | Análisis completo (versión N) |
| `consense_diff_N.md` | Requisitos abiertos consolidados |
| `_archive/conN_*_XX.*` | Documentos archivados (>=75%) |

---

## Clasificación de Prioridad

| Prioridad | Criterio |
|:---------:|----------|
| P1 | Funcionalidad principal faltante, sistema no utilizable |
| P2 | Funcionalidad importante faltante, solución alternativa posible |
| P3 | Deseable, mejora la UX |
| P4 | Cosmético, documentación, calidad de código |

---

## Historial de Cambios

### 1.0.0 (2026-03-15)
- Adaptado desde BACH v3.8.0

---

*Adaptado desde BACH v3.8.0 | Versión independiente*