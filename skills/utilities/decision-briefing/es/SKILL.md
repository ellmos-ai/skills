---
name: decision-briefing
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: Utilícelo siempre que haya varias decisiones pendientes o acumuladas, ya sea dentro de un tema, proyecto, documento o a lo largo de una sesión: inventaríelas, presente un briefing numerado con opciones A/B/C/D y una recomendación destacada, acepte respuestas por letra (incluidos envíos en lote), registre los resultados y escríbalos de nuevo en los documentos de origen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [entscheidung, briefing, batch, decision-session, priorisierung, workflow]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/decision-briefing/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="decision-briefing banner">

> **Español** — Versión oficial en español de `decision-briefing`.


# Decision-Briefing — Trabajar en múltiples decisiones sobre un tema

> Un cúmulo de decisiones pendientes se convierte en un briefing numerado con recomendaciones que el usuario puede responder a la velocidad de la luz mediante letras individuales: una por una o en lote.

---

## ¿Cuándo usar?

**Siempre que haya varias decisiones pendientes**, independientemente del tema. Situaciones típicas:

- Se han acumulado muchas decisiones pendientes en un área o tema
- Un documento (plan, lista de tareas, concepto) contiene varios puntos sin decidir
- Se han acumulado varias preguntas de decisión durante una conversación
- El propio agente tiene varias preguntas para el usuario: agrúpelas en un briefing en lugar de preguntarlas una por una
- El usuario desea resolver elementos pendientes de forma rápida y con una base sólida

**Palabras clave de activación:** decisiones abiertas, sesión de decisión, briefing, procesar, revisar, decidamos todo esto

**Alcance:** [decide](../decide/SKILL.en.md) proporciona marcos de trabajo para UNA pregunta. `decision-briefing` coordina el procesamiento de MUCHAS decisiones sobre un tema y aplica `decide` a casos individuales complejos.

---

## UX principal

El núcleo de esta habilidad es el formato de briefing. Cada decisión se presenta de forma que responder cueste solo una letra:

- **Numeración:** `[E01]`, `[E02]`, … — referencias estables durante toda la sesión
- **Pregunta corta** + 1–2 frases de contexto
- **Opciones mediante letras** A/B/C/D (2–4 opciones, más solo si es necesario)
- **Recomendación destacada** con una justificación de una frase (p. ej., `→ Recomendación: A — porque …`)
- Opcional: nota de consecuencia (lo que se deriva de la elección)

**Formatos de respuesta del usuario:**

```
Single:    "E01: A"  or  "1A"
Batch:     "1A 2C 3B"  or  "E01: A, E02: C, E03: B"
Deepen:    "E02: more info"  or  "2?"
Defer:     "E03: later"
```

---

## Flujo de trabajo y procedimiento

```
Topic + decisions at hand
     |
     v
Phase 1: CAPTURE & INVENTORY
     |
     v
Phase 2: PREPARE THE BRIEFING
     |
     v
Phase 3: DECISION SESSION
     |
     v
Phase 4: RECORD & WRITE BACK
```

### Fase 1: Captura e inventario

Fuentes: lo que el usuario mencione, un documento a mano o el contexto de la conversación. Sin escaneo a nivel de todo el sistema: solo lo que ya está disponible.

1. Listar todas las decisiones abiertas (una línea cada una: título corto)
2. Detectar y fusionar **duplicados** (misma pregunta planteada varias veces)
3. Marcar **dependencias** ("E04 depende de E01")
4. Establecer el **orden**: primero los bloqueadores (decisiones de las que dependen otras), luego por urgencia
5. Mostrar la lista al usuario para su confirmación ("¿Están todas? ¿Falta algo?")

### Fase 2: Preparar el briefing

Por decisión:

```
[E01] <Short question>
  Context: <1-2 sentences: Why is this up? What depends on it?>
  A) <Option>
  B) <Option>
  C) <Option>
  → Recommendation: <letter> — <one-sentence rationale>
  (optional) Consequence: <what follows from the choice / next action>
```

Reglas para buenas opciones:

- Las opciones deben ser mutuamente excluyentes y cubrir todo el espectro
- Si es útil, incluya una opción de "mantener el estado actual" o "posponer"
- La recomendación se justifica de forma transparente, nunca de manera encubierta o sugestionable
- Cuando los hechos no estén claros: aclare primero (o marque como pregunta abierta), no adivine

### Fase 3: Sesión de decisión

1. Presentar el briefing: una decisión por mensaje o todas a la vez en lote; con más de 5 decisiones, use bloques de 3–5
2. Aceptar respuestas por letra y confirmarlas
3. Ante una respuesta de "más información": profundizar en la decisión (caja de herramientas metodológicas a continuación)
4. Para casos individuales complejos (múltiples criterios, alto riesgo): escalar a la habilidad [decide](../decide/SKILL.en.md) (puntuación ponderada, análisis de escenarios)
5. Trasladar explícitamente las decisiones pospuestas como abiertas; nunca las omita en silencio

### Fase 4: Registrar y reescribir

1. Crear una **tabla de resultados**:

```
| No.  | Decision            | Chosen | Status   |
|------|---------------------|--------|----------|
| E01  | <short title>       | A      | decided  |
| E02  | <short title>       | C      | decided  |
| E03  | <short title>       | —      | deferred |
```

2. Reescribir los elementos decididos en los **documentos de origen/archivos TODO**, en la ubicación de la pregunta abierta, p. ej.:

```
DECISION: <question>
  → DECIDED 2026-06-13: Option A (<short form>)
  → Next action: <if the decision implies a follow-up action>
```

3. Mantener los **elementos pospuestos explícitamente abiertos** (en el documento de origen o en la lista TODO) para que reaparezcan en el próximo briefing

---

## Ejemplo y aplicación

Tema: rediseño del sitio web de un club: 3 decisiones abiertas del plan del proyecto.

```
[E01] Which system for the new website?
  Context: Current site is hand-maintained HTML; 2 people will maintain content in the future.
  A) Static site generator (fast, secure, maintained via Git)
  B) Classic CMS with admin interface
  C) Hosted website builder
  → Recommendation: B — two non-technical editors need an interface, not Git.

[E02] How is it hosted?
  Context: Budget ~10 EUR/month, no dedicated admin in the club.
  A) Shared hosting with the current provider
  B) Small dedicated VPS
  C) Managed hosting matching the chosen system
  → Recommendation: C — least maintenance effort without an admin; consequence: depends on E01.

[E03] When does the new site go live?
  Context: Content is 60% migrated; club anniversary in 3 months.
  A) Immediately as a soft launch (rest follows)
  B) After complete content migration
  C) On the anniversary as the deadline
  → Recommendation: A — reversible and yields early feedback; final content follows.
```

El usuario responde en lote: **"1B 2C 3A"** → tabla de resultados, luego las tres decisiones se marcan como DECIDED en el plan del proyecto.

---

## Caja de herramientas metodológicas (para "más información" y profundización)

| Método | Cuándo | Resumen |
|--------|------|---------|
| **Matriz de pros y contras** | 2–3 opciones, comparación rápida | Evaluar todas las opciones lado a lado |
| **Puntuación ponderada** | Múltiples criterios | Criterios ponderados, puntos por opción (cuantitativo donde sea posible) |
| **Pensamiento de segundo orden** | Riesgos / impacto incierto | ¿Cuáles son las consecuencias de las consecuencias? |
| **Premortem** | Decisión de alto riesgo | "Ha fallado — ¿por qué?" Identificar puntos débiles de antemano |
| **Método 10/10/10** | Distorsión emocional/temporal | ¿Cómo se ve la decisión en 10 minutos / 10 meses / 10 años? |

---

## Principios de trabajo

- **Nunca forzar decisiones:** proporcione información, justifique la recomendación con transparencia; el usuario decide
- **Detección de sesgos:** señale los errores de pensamiento cuando sean visibles (sesgo de confirmación, costo hundido)
- **Tener en cuenta la reversibilidad:** decida las opciones reversibles rápidamente; trate las definitivas con más detenimiento
- **Respetar la presión de tiempo:** las decisiones rápidas requieren métodos más simples; no todas las preguntas merecen un análisis de puntuación ponderada

---

## Alcance y sinergias

| Función | `decide` | `decision-briefing` |
|---|---|---|
| Estructurar una sola decisión con un marco de trabajo | ✓ | — |
| Inventariar muchas decisiones sobre un tema | — | ✓ |
| Briefing numerado con opciones A/B/C | — | ✓ |
| Respuestas en lote ("1A 2C 3B") | — | ✓ |
| Reescribir en documentos de origen | — | ✓ |

**Sinergia:** Para casos individuales complejos dentro de una sesión, `decision-briefing` aplica los marcos de trabajo de `decide` (puntuación ponderada, análisis de escenarios). Para el proceso de pensamiento más amplio anterior (analizar → idear → decidir), consulte [structured-thinking](../structured-thinking/SKILL.en.md).

---

## Registro de cambios

### 1.0.0 (2026-06-13)
- Adaptado del experto de BACH `decision-briefing` v1.0.0; el componente de escáner (scanner.py, sources.json, escaneos de marcadores) se eliminó deliberadamente: la captura es ligera, basada en el contexto disponible

---

*Adaptado de BACH | Versión independiente sin escáner*

**Vea también:** [decide](../decide/SKILL.en.md) (marcos de trabajo para una sola decisión) | [structured-thinking](../structured-thinking/SKILL.en.md) (analizar → idear → decidir como meta-flujo de trabajo)
