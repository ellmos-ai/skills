---
name: structured-thinking
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: Meta-skill: Pensamiento estructurado como un flujo de trabajo de 3 fases. Combina análisis (think), ideación (brainstorm) y toma de decisiones (decide) en un proceso continuo.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [denken, analyse, kreativitaet, entscheidung, workflow, meta-skill]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'merged_from': ['utilities/think (v1.0.0)', 'utilities/brainstorm (v1.0.0)', 'utilities/decide (v1.0.0)'], 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `structured-thinking`.


# Structured Thinking — Analizar, Idear, Decidir

> Metaflujo de trabajo para el pensamiento estructurado: desde el análisis del problema hasta soluciones creativas y una decisión bien fundamentada

---

## Flujo de trabajo y procedimiento

```
Problem/Question
     |
     v
Phase 1: ANALYZE (think)
  Divide & Conquer, Root Cause, Constraint Relaxation
     |
     v
Phase 2: IDEATE (brainstorm)
  SCAMPER, Six Hats, Reverse Brainstorming, Rapid Ideation
     |
     v
Phase 3: DECIDE (decide)
  Pro/Con, Weighted Scoring, Scenario Analysis, Eisenhower
     |
     v
Result + Rationale
```

---

## Fase 1: Analizar

Objetivo: Comprender el problema, identificar las causas y reconocer la estructura.

### Enfoques

| Método | Cuándo | Procedimiento |
|--------|--------|---------------|
| **Divide & Conquer** | Problema complejo | Problema → subproblemas → resolver individualmente → combinar |
| **Root Cause (5x Why)** | Síntoma visible, causa no clara | Síntoma → ¿Por qué? → ¿Por qué? → ... → causa → solución |
| **Constraint Relaxation** | El problema parece no tener solución | Flexibilizar restricciones → resolver → volver a aplicar restricciones |
| **Analogy Search** | Problema nuevo | Buscar un problema conocido similar → adaptar su solución |

### Marcos de análisis

| Marco | Aplicación |
|-------|------------|
| **SWOT (FODA)** | Fortalezas / Oportunidades / Debilidades / Amenazas |
| **Pareto** | 80/20 — ¿Qué genera el mayor impacto? |
| **Fishbone** | Análisis sistemático de causas (Ishikawa) |

### Heurísticas bajo incertidumbre

1. ¿Cuál es el peor escenario posible?
2. ¿Es reversible?
3. ¿Cuál es el costo de no actuar?

### Heurísticas bajo complejidad

1. ¿Cuál es el primer paso más simple?
2. ¿Qué haría un experto?
3. ¿Cuál sería la solución al 80%?

---

## Fase 2: Idear

Objetivo: Generar tantas propuestas de solución como sea posible. Cantidad sobre calidad. SIN críticas durante esta fase.

### Métodos

**SCAMPER** — Mejorar sistemáticamente las soluciones existentes:
- **S**ustituir: ¿Qué sustituir? | **C**ombinar: ¿Qué combinar? | **A**daptar: ¿Qué adaptar?
- **M**odificar: ¿Qué modificar? | **P**oner en otros usos: ¿Para qué más podría servir? | **E**liminar: ¿Qué descartar?
- **R**eorganizar/Invertir: ¿Qué invertir?

**Seis Sombreros para Pensar** (de Bono) — 6 perspectivas en secuencia:
1. Azul: Control del proceso ("¿Cuál es la pregunta?")
2. Blanco: Hechos ("¿Qué sabemos?")
3. Rojo: Emoción ("¿Qué nos dicta la intuición?")
4. Negro: Crítica ("¿Qué podría salir mal?")
5. Amarillo: Optimismo ("¿Cuáles son las oportunidades?")
6. Verde: Creatividad ("¿Qué nuevas ideas existen?")

**Brainstorming Inverso** — Invertir el problema:
1. "¿Cómo empeoramos el problema?"
2. Recopilar malas ideas
3. Invertir = buenas ideas

**Ideación Rápida** — Más de 50 ideas en 20 minutos:
- Ronda 1 (5 min): Ideación abierta
- Ronda 2 (5 min): Variaciones
- Ronda 3 (5 min): Combinaciones
- Ronda 4 (5 min): Ideas extremas

### Después de la ideación

1. Agrupación (Clustering): Agrupar ideas similares
2. Matriz Viabilidad/Impacto: Evaluar viabilidad vs. impacto
3. Seleccionar las 5-10 mejores para la Fase 3

---

## Fase 3: Decidir

Objetivo: Seleccionar la mejor opción con una justificación transparente.

### Selección del marco de trabajo

| Situación | Marco de trabajo |
|-----------|------------------|
| 2 opciones, decisión rápida | **Matriz Pros/Contras** |
| 3+ opciones, múltiples criterios | **Puntuación Ponderada** |
| Decisión secuencial de tipo si-entonces | **Árbol de Decisión** |
| Alta incertidumbre | **Análisis de Escenarios** |
| Priorización de tareas | **Matriz de Eisenhower** |

### Puntuación Ponderada (método principal)

1. Recopilar criterios (3-7, específicos y medibles)
2. Definir ponderaciones (suma = 100%, los más importantes >= 25%)
3. Calificar opciones (escala 1-10)
4. Calcular puntuaciones (calificación x ponderación)
5. Comparar y recomendar

### Análisis de Escenarios

```
Best Case (X%):      Outcome → expected value
Realistic Case (X%): Outcome → expected value
Worst Case (X%):     Outcome → expected value
Total expected value: [sum]
```

### Matriz de Eisenhower

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

### Lista de verificación de calidad antes de la recomendación final

- [ ] ¿Se han identificado todos los criterios relevantes?
- [ ] ¿Se han tenido en cuenta los valores del usuario?
- [ ] ¿Se consideran los efectos a largo plazo?
- [ ] ¿Se han identificado y evaluado los riesgos?
- [ ] ¿Se ha realizado la verificación de sesgos?
- [ ] ¿Se ha verificado la reversibilidad?

---

## Selección según el contexto

| Situación | Fase(s) recomendada(s) |
|-----------|------------------------|
| "Tengo un problema" | Fase 1 (análisis) → posiblemente Fase 2+3 |
| "Necesito ideas" | Fase 2 (ideación) |
| "Tengo que decidir" | Fase 3 (decisión) |
| "Estoy bloqueado" | Fase 2 (brainstorming inverso) |
| "¿Qué debo priorizar?" | Fase 3 (Eisenhower) |
| "Comprender un problema complejo" | Fase 1 (Divide & Conquer + SWOT) |

---

## Historial de cambios

### 1.0.0 (2026-05-19)
- Creado como meta-skill a partir de think, brainstorm y decide

---

*Meta-skill | Referencia detallada: [think](../think/SKILL.md), [brainstorm](../brainstorm/SKILL.md), [decide](../decide/SKILL.md)*