---
name: decision-briefing
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: Usar cada vez que haya varias decisiones pendientes o acumuladas —ya sea dentro de un tema, proyecto, documento o a lo largo de una sesión: hacer un inventario, presentar un briefing numerado con opciones A/B/C/D y una recomendación marcada, aceptar respuestas por letras (incluidos lotes), registrar los resultados y escribirlos de nuevo en los documentos de origen.

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

> **Español** — Versión oficial en español de `decision-briefing`.


# Decision-Briefing — Trabajar en Varias Decisiones sobre un Tema (Español)

> Un cúmulo de decisiones pendientes se convierte en un briefing numerado con recomendaciones que el usuario puede responder a la velocidad de la luz con letras individuales, una por una o en lote.

---

## ¿Cuándo Usar?

**Siempre, tan pronto como haya varias decisiones pendientes**, independientemente del tema. Situaciones típicas:

- Se han acumulado muchas decisiones pendientes en un área/tema
- Un documento (plan, lista de tareas, concepto) contiene varios puntos indecisos
- Se han acumulado varias preguntas de decisión durante una conversación
- El propio agente tiene varias preguntas para el usuario: agruparlas como un briefing en lugar de preguntar una por una
- El usuario desea despejar elementos pendientes rápidamente y sobre una base sólida

**Palabras clave (Trigger words):** open decisions, decision session, briefing, work through, go through, let's decide all of this

**Alcance:** [decide](../decide/SKILL.en.md) proporciona marcos para UNA pregunta. `decision-briefing` coordina el trabajo a través de MUCHAS decisiones sobre un tema y aplica `decide` a casos individuales complejos.

---

## Experiencia de Usuario Principal (Core UX)

El núcleo de esta habilidad es el formato de briefing. Cada decisión se presenta de forma que responder cueste solo una letra:

- **Numeración:** `[E01]`, `[E02]`, … — referencias estables durante toda la sesión
- **Pregunta corta** + 1–2 frases de contexto
- **Opciones como letras** A/B/C/D (2–4 opciones, más solo si es necesario)
- **Recomendación marcada** con una justificación de una frase (ej. `→ Recomendación: A — porque …`)
- Opcional: nota de consecuencia (lo que se deriva de la elección)

**Formatos de respuesta del usuario:**

```
Single:    "E01: A"  or  "1A"
Batch:     "1A 2C 3B"  or  "E01: A, E02: C, E03: B"
Deepen:    "E02: more info"  or  "2?"
Defer:     "E03: later"
```

---

## Flujo de Trabajo y Procedimiento

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

### Fase 1: Captura e Inventario

Fuentes: lo que el usuario mencione, un documento a mano o el contexto de la conversación. Sin escaneo de todo el sistema: solo lo que ya está allí.

1. Listar todas las decisiones pendientes (una línea cada una: título corto)
2. Detectar y fusionar **duplicados** (misma pregunta planteada varias veces)
3. Marcar **dependencias** ("E04 depende de E01")
4. Establecer el **orden**: bloqueadores primero (decisiones de las que dependen otras), luego por urgencia
5. Mostrar la lista al usuario para su confirmación ("¿Están todas? ¿Falta algo?")

### Fase 2: Preparar el Briefing

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

- Las opciones deben ser mutuamente excluyentes y cubrir el espectro
- Si es útil, incluir una opción de "mantener statu quo" o "posponer"
- La recomendación se justifica de forma transparente — nunca de manera encubierta o sugestiva
- Cuando los hechos no estén claros: aclarar primero (o marcar como pregunta abierta), no adivinar

### Fase 3: Sesión de Decisión

1. Presentar el briefing — una decisión por mensaje o todas a la vez como un lote; con >5 decisiones, usar bloques de 3–5
2. Aceptar respuestas por letras y confirmarlas
3. Ante una respuesta de "más información": profundizar en la decisión (caja de herramientas de métodos a continuación)
4. Para casos individuales complejos (muchos criterios, gran impacto): escalar a la habilidad [decide](../decide/SKILL.en.md) (puntuación ponderada, análisis de escenarios)
5. Trasladar las decisiones pospuestas explícitamente como abiertas — nunca descartarlas en silencio

### Fase 4: Registro y Escritura de Vuelta

1. Crear una **tabla de resultados**:

```
| No.  | Decision            | Chosen | Status   |
|------|---------------------|--------|----------|
| E01  | <short title>       | A      | decided  |
| E02  | <short title>       | C      | decided  |
| E03  | <short title>       | —      | deferred |
```

2. Escribir los elementos decididos de nuevo en los **documentos de origen/archivos TODO** — en la ubicación de la pregunta abierta, ej.:

```
DECISION: <question>
  → DECIDED 2026-06-13: Option A (<short form>)
  → Next action: <if the decision implies a follow-up action>
```

3. Mantener los **elementos pospuestos explícitamente abiertos** (en el documento de origen o en la lista de tareas) para que reaparezcan en el siguiente briefing

---

## Ejemplo y Aplicación

Tema: rediseño del sitio web de un club — 3 decisiones pendientes del plan de proyecto.

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

El usuario responde en lote: **"1B 2C 3A"** → tabla de resultados, luego las tres decisiones se marcan como DECIDED en el plan de proyecto.

---

## Caja de Herramientas de Métodos (para "más información" y profundización)

| Método | Cuándo usar | Resumen |
|--------|------|---------|
| **Matriz pros/contras** | 2–3 opciones, comparación rápida | Evaluar todas las opciones lado a lado |
| **Puntuación ponderada** | Múltiples criterios | Criterios ponderados, puntos por opción (cuantitativo donde sea posible) |
| **Pensamiento de segundo orden** | Impacto/enfoque incierto | ¿Cuáles son las consecuencias de las consecuencias? |
| **Premortem** | Decisión arriesgada | "Ha fallado — ¿por qué?" Encontrar puntos débiles por adelantado |
| **Método 10/10/10** | Distorsión emocional/temporal | ¿Cómo se ve la decisión en 10 minutos / 10 meses / 10 años? |

---

## Principios de Trabajo

- **Nunca forzar decisiones:** proporcionar información, justificar la recomendación con transparencia — el usuario decide
- **Detección de sesgos:** nombrar errores de pensamiento cuando se vuelvan visibles (sesgo de confirmación, costo hundido)
- **Tener en cuenta la reversibilidad:** decidir decisiones reversibles rápidamente, tratar las definitivas con más detenimiento
- **Respetar la presión del tiempo:** las decisiones rápidas necesitan métodos más simples — no todas las preguntas merecen un análisis de puntuación ponderada

---

## Alcance y Sinergias

| Función | `decide` | `decision-briefing` |
|---|---|---|
| Estructurar una sola decisión con un marco de trabajo | ✓ | — |
| Inventariar muchas decisiones sobre un tema | — | ✓ |
| Briefing numerado con opciones A/B/C | — | ✓ |
| Respuestas en lote ("1A 2C 3B") | — | ✓ |
| Escribir de nuevo en documentos de origen | — | ✓ |

**Sinergia:** Para casos individuales complejos dentro de una sesión, `decision-briefing` aplica los marcos de trabajo de `decide` (puntuación ponderada, análisis de escenarios). Para el proceso de pensamiento más amplio anterior a esto (analizar → idear → decidir), consulte [structured-thinking](../structured-thinking/SKILL.en.md).

---

## Registro de Cambios

### 1.0.0 (2026-06-13)
- Portado desde el experto de BACH `decision-briefing` v1.0.0; el componente de escaneo (scanner.py, sources.json, escaneos de marcadores) fue eliminado deliberadamente — la captura es ligera, basada en el contexto a mano

---

*Portado desde BACH | Versión independiente sin escáner*

**Ver también:** [decide](../decide/SKILL.en.md) (marcos de trabajo para una sola decisión) | [structured-thinking](../structured-thinking/SKILL.en.md) (analizar → idear → decidir como metaworkflow)