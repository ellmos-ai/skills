---
name: trampelpfadanalyse
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-06-21
updated: 2026-06-21
description: Análisis de errores para flujos de trabajo de pipelines y archivos de control: verifica si una convención o procedimiento es realmente visible y descubrible para un LLM. Comparación empírica baseline → intervención → retest utilizando subagentes ingenuos (copias en sandbox aisladas, caso de prueba idéntico, medición cuantitativa del éxito). Usa esta habilidad cuando los agentes ignoren repetidamente una regla/README/convención o naveguen de forma incorrecta, y desees medir si un cambio en la documentación realmente cambia el comportamiento. Se activa con "is the convention even seen", "why does no agent follow the rule", "make a doc signpost measurably effective", "desire-path analysis", "trampelpfadanalyse".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [workflow, error-analysis, llm-ux, doc-audit, baseline-retest, naive-subagent, empirical, pipeline, control-file]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/system/trampelpfadanalyse.md', 'origin_version': '2.0', 'origin_repo': 'github.com/ellmos-ai/swarm-ai', 'last_sync_from_origin': '2026-06-21', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="trampelpfadanalyse banner">

> **Español** — Versión oficial en español de `trampelpfadanalyse`.


# Análisis de rutas de deseo (Desire-Path Analysis) — Haciendo las convenciones empíricamente visibles para los LLM

Un método para descubrir errores en flujos de trabajo de pipelines y archivos de control que no provienen
de código roto, sino de que una **convención es invisible para un LLM**. En lugar de adivinar si un README
o una regla es "lo suficientemente clara", se mide empíricamente: subagentes ingenuos (naive) sin
conocimiento previo son liberados en el flujo de trabajo, su comportamiento se convierte en la
**línea base (baseline)**, un cambio de documentación orientado (un "señalizador" / signpost) es la
**intervención**, y subagentes ingenuos frescos proporcionan el **retest**. La diferencia (diff) con la
línea base es la medición del éxito.

El nombre proviene del *desire path* (en alemán: *Trampelpfad*, sendero de deseo): donde la gente realmente
camina en lugar de la ruta pavimentada es donde pertenece un camino. Por analogía, las rutas de los LLM
ingenuos muestran dónde realmente se necesitan la documentación y las protecciones (guardrails), no dónde
asumimos que están.

## Cuándo usar esta habilidad

- Los agentes ignoran repetidamente una regla/convención a pesar de que está documentada.
- Quieres saber si un procedimiento es **visible/descubrible** para un LLM antes de escribir más documentación
  ("¿hay alguien aquí hablando con la pared?").
- Después de una reestructuración (nuevos directorios, renombre de archivos): ¿pueden los agentes encontrar
  todavía los puntos de entrada?
- Hiciste un cambio en la documentación y quieres **probar** que funciona, no solo esperarlo.
- Prueba de incorporación (onboarding) antes de integrar nuevos agentes LLM en una pipeline.

No apto para: errores de código puros (→ depuración sistemática), o selección de patrones de coordinación de
swarm para una tarea de producción (→ ver `swarm-operations`). Esta habilidad utiliza un swarm de agentes
ingenuos exclusivamente como **instrumento de medición**.

## La idea central en una frase

Trata la documentación como UX: lo que cuenta no es lo que escribiste, sino lo que un usuario imparcial
(aquí: un agente ingenuo) hace realmente con ella — y tú mides eso, lo cambias y lo vuelves a medir.

---

## El proceso: 5 pasos

```
1. BASELINE       naive subagents → measure current behavior (quantitative)
2. PATH ANALYSIS  where exactly does it fail? which doc location misleads?
3. INTERVENTION   put up a "signpost" (README/convention made more prominent)
4. RETEST         FRESH naive subagents, identical test case
5. DIFF           retest vs. baseline → success measurement + honest assessment
```

### Paso 1 — Línea base (Baseline): medir el comportamiento actual de forma ingenua

Primero formula el problema como una **pregunta verificable**, por ejemplo: "¿Crea un agente un registro
en la ubicación exigida por la convención?" o "¿Encuentra un agente el punto de entrada de la pipeline?".

Luego libera subagentes ingenuos:

- **Ingenuo significa:** sin memoria del proyecto, sin habilidades, sin pistas previas — el agente solo
  conoce la ruta de entrada y la tarea. Esto mide la **descubribilidad pura a través de la documentación
  existente**, no el conocimiento previo del agente.
- **Copias de sandbox aisladas:** cada agente de prueba trabaja en su propia copia de la carpeta/flujo de
  trabajo afectado, por lo que las pruebas no se influyen entre sí y el estado real se mantiene intacto.
- **Mismo caso de prueba, múltiples repeticiones:** la variabilidad existe. Una prueba es una anécdota;
  n repeticiones (por ejemplo, 3 o más si es necesario) ofrecen una tasa.
- **Un modelo económico e "ingenuo"** es suficiente y realista — no debe adivinar hábilmente, sino mostrar
  adónde conduce la documentación a un agente promedio.

Prompt mínimo de prueba (ajustar marcadores de posición):

```
You are exploring <SYSTEM>. It is located at: <PATH>.
TASK: <specific task>.
RULES:
1. You only know the path above, nothing else.
2. Explore to complete the task. Max. <N> steps.
3. Report at the end: VISITED_DIRECTORIES, READ_FILES,
   TASK_COMPLETED (yes/no), MOST_HELPFUL_FILE.
```

**Registrar como métricas de línea base** (siempre cuantitativas, nunca "parece mejor"):

| Métrica | Significado |
|---|---|
| Tasa de éxito | con qué frecuencia se completó la tarea según la convención (ej. 0/3) |
| Comportamiento erróneo | con qué frecuencia se usó la ubicación/método incorrecto (ej. 3/3 registro colectivo en lugar de por entrada) |
| Rutas hacia la meta | cuántos pasos/desvíos para alcanzar la meta |
| Puntos ciegos | qué archivo/ubicación relevante nadie abre |

### Paso 2 — Análisis de rutas (Path analysis): ¿dónde falla realmente?

Evalúa los informes de prueba conjuntamente (un "mapa de calor" de ubicaciones visitadas es suficiente):

- ¿Qué archivo se lee **con frecuencia** (CALIENTE / HOT)? Si falta orientación allí, ese es el lugar más
  efectivo para una señal (signpost).
- ¿Qué ubicación relevante **nunca** se abre (FRÍA / COLD / punto ciego)? Es efectivamente invisible, sin
  importar cuán bueno sea su contenido.
- ¿Dónde entra el agente en un bucle o elude la convención (callejón sin salida, elusión)? Eso marca la
  laguna concreta en la documentación.

Tabla de hallazgos:

| Hallazgo | Significado | Acción (→ Paso 3) |
|---|---|---|
| CALIENTE + sin orientación | mucho tráfico, sin señalización | colocar la señalización justo allí |
| TIBIO + errores | los agentes llegan pero tropiezan | añadir ejemplo/aclaración |
| FRÍO | la ubicación nunca se encuentra | vincularla desde un archivo CALIENTE |
| Elusión | la convención es eludida | indicar la señal en el punto de elusión |

Resultado del Paso 2: **una hipótesis concreta y localizada** — "Los agentes leen X, pero X no menciona
la convención; por eso terminan en Y."

### Paso 3 — Intervención: colocar un señalizador (signpost)

Coloca **exactamente un** señalizador (una variable por pasada, de lo contrario la diferencia no es
interpretable). Señalizadores típicos:

- Colocar la convención **de forma destacada por donde la ruta CALIENTE ya pasa** (por ejemplo, una nota
  corta y explícita en la parte superior del README/archivo de control más leído).
- Una **tabla de navegación rápida** al inicio del archivo central de arquitectura/visión general que apunte
  a los antiguos puntos ciegos.
- Una **referencia cruzada/señalizador** desde un archivo CALIENTE hacia una ubicación FRÍA.
- Opcionalmente una **protección (guardrail)** (por ejemplo, una nota PreToolUse) para acciones peligrosas o
  que violen la convención.

Mantén la señalización corta y de vista imposible de omitir — los agentes ojean rápido, rara vez leen detenidamente.

### Paso 4 — Retest con subagentes ingenuos FRESCOS

Repite el Paso 1 **de forma idéntica** — misma tarea, mismo número de repeticiones, mismo modelo, misma
condición ingenua — pero en copias de sandbox **con** el nuevo señalizador. Importante:

- Agentes **frescos** sin memoria de la ejecución de la línea base (de lo contrario mides aprendizaje,
  no descubribilidad).
- **Solo el señalizador** difiere de la configuración de la línea base.

### Paso 5 — Diferencia (Diff) con la línea base + medición honesta del éxito

Pon el retest y la línea base directamente lado a lado:

| Métrica | Línea base | Tras el señalizador | Δ |
|---|---|---|---|
| Tasa de éxito | ej. 0/3 | ej. 3/3 | +3 |
| Comportamiento erróneo | ej. 3/3 | ej. 0/3 | −3 |
| Puntos ciegos | ej. 1 | ej. 0 | −1 |

Evaluación — y no maquillar los resultados:

- **Funciona** (el comportamiento erróneo se reduce mensurablemente): conservar el señalizador, documentarlo.
- **No funciona** (pequeño Δ): el señalizador estaba en el lugar equivocado o era demasiado sutil → volver al
  Paso 2/3, diferente señalizador, medir de nuevo.
- **Declarar límites abiertamente:** muestras pequeñas n son indicadores, no pruebas definitivas; un agente
  ingenuo modela un "usuario promedio sin información", no a cada usuario real; verificar explícitamente falsos
  positivos/negativos en la puntuación del éxito (¿qué contó exactamente como "completado"?).

---

## Mini caso de estudio (real, con números actuales)

Problema: Una pipeline de tickets exigía que las finalizaciones triviales tuvieran **un** registro dedicado por
ticket, pero los agentes ponían todo en **un registro colectivo**.

- **Paso 1 (línea base):** 3 subagentes ingenuos, misma tarea → **3/3 usaron el registro colectivo**
  (convención no seguida).
- **Paso 2 (análisis de rutas):** el README más leído no mencionaba la regla por ticket en un lugar visible →
  la ruta ingenua conducía al registro colectivo.
- **Paso 3 (intervención):** un señalizador corto y explícito sobre la convención de registro colocado de forma
  destacada en el README.
- **Paso 4 (retest):** 3 subagentes ingenuos frescos, tarea idéntica.
- **Paso 5 (diff):** **3/3 incorrectos → 0/3 incorrectos**, los tres crearon un registro por ticket correcto.
  (Documentado en el ticket T-20260621-44.)

Lección: La convención no estaba "redactada de forma muy débil" — era **invisible** en la ruta que realmente
se leía. El señalizador en el lugar correcto, verificado empíricamente, resolvió el problema.

---

## Fuente y métodos relacionados

Este método proviene del Análisis de Rutas de Deseo v2.0 (swarm como instrumento de medición empírico para
el comportamiento de LLM). Los resultados de referencia originales de una ejecución grande (100 pruebas ingenuas)
están documentados como evidencia de la fuente: el mayor punto ciego fue un directorio de ayuda que **0/100**
agentes visitaron (a pesar de muchos archivos de ayuda), y la tarea "crear una nueva skill" tuvo un éxito del
**0%** porque nadie encontró el directorio de plantillas — ambos problemas clásicos de visibilidad, no de contenido.

## Ver también

- `swarm-operations` (dev) — catálogo de **patrones de coordinación** de swarm para tareas de producción;
  incluye el análisis de rutas de deseo solo como sección conceptual. Esta habilidad es la variante de
  **proceso** aplicable con un bucle línea base → retest.
- `pipeline-optimizer` (dev) — renovación de pipeline en 6 pasos; su retest con subagentes frescos corresponde
  a los Pasos 4–5 aquí.
- `bugfix-protocol` / depuración sistemática — para errores de código reales en lugar de problemas de visibilidad.

## Historial de cambios

### 0.1.0 (2026-06-21)
- Port inicial desde Desire-Path Analysis v2.0 (fuente: swarm-ai/BACH).
- Enfocado en el proceso aplicable de 5 pasos (línea base → análisis de rutas → intervención → retest → diff);
  los patrones de coordinación de swarm fueron omitidos deliberadamente (permanecen en `swarm-operations`).
  Neutral con marcadores de posición; caso de estudio mini real.
