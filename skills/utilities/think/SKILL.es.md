---
name: think
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-06
description: "Usar cuando un problema ajeno al código debe entenderse antes de decidir o cambiar algo: proceso, organización, producto, estrategia, métrica o comportamiento de un sistema a nivel de negocio con varias causas posibles, un nudo que hay que dividir en partes o una situación que necesita un enfoque FODA (SWOT) o 80/20: '¿por qué sigue pasando ...?', 'encuentra la causa raíz', 'cinco porqués', 'divide esto en subproblemas', '¿por dónde empiezo?', 'un FODA rápido', '¿qué está pasando realmente?', /think. Aplica Divide y Vencerás, análisis de causa raíz, búsqueda de analogías, FODA, Pareto e Ishikawa, y termina con la causa o estructura hallada y lo primero que hay que comprobar. NO usar para defectos de software (mensajes de error, builds, pruebas o despliegues fallidos, regresiones: bugfix-protocol), generar muchas ideas (brainstorm), elegir entre opciones dadas (decide), explorar ideas frente al historial del proyecto (idea-mining) ni la cadena completa análisis-ideas-decisión (structured-thinking)."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="think banner">

> **Español** — Versión oficial en español de `think`.


# Think — Resolución de problemas y análisis

> Procesos de pensamiento estructurado para problemas complejos

---

## Enfoques de resolución de problemas

### 1. Divide & Conquer (Divide y vencerás)

```
Problem -> Sub-problems -> Solve individually -> Combine
```

### 2. Root Cause Analysis (Análisis de causa raíz)

```
Symptom -> Why? -> Why? -> Why? -> Root cause -> Solution
```

### 3. Constraint Relaxation (Flexibilización de restricciones)

```
Unsolvable problem -> Relax constraints -> Solve -> Re-apply constraints
```

### 4. Analogy Search (Búsqueda de analogías)

```
New problem -> Similar known problem -> Adapt solution
```

---

## Métodos de análisis

| Método | Aplicación |
|--------|------------|
| **SWOT (FODA)** | Fortalezas / Oportunidades / Debilidades / Amenazas |
| **Pros/Contras** | Toma de decisiones |
| **Pareto** | Priorización 80/20 |
| **Fishbone** | Análisis de causa raíz (Ishikawa) |

---

## Heurísticas de decisión

### Bajo incertidumbre

```
1. ¿Cuál es el peor escenario posible?
2. ¿Es reversible?
3. ¿Cuál es el costo de no actuar?
```

### Bajo complejidad

```
1. ¿Cuál es el primer paso más simple?
2. ¿Qué haría un experto?
3. ¿Cuál sería la solución al 80%?
```

---

## Historial de cambios

### 1.1.0 (2026-11-06)
- Descripción reescrita con un desencadenante claro y delimitación (regla de docs/CONVENTIONS.md): situación de uso, frases típicas del usuario y el comando slash al principio, y los skills vecinos en una cláusula NO usar.

### 1.0.0 (2026-03-15)
- Adaptado de BACH v3.8.0

---

*Adaptado de BACH v3.8.0 | Versión independiente*