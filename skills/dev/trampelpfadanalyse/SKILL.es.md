---
name: trampelpfadanalyse
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-06-21
updated: 2026-06-21
description: Análisis de errores para flujos de trabajo de pipelines y archivos de control - comprobar si una convención o procedimiento es realmente visible y descubrible para un LLM. Línea base empírica → intervención → prueba de reevaluación comparativa utilizando subagentes ingenuos (copias aisladas en sandbox, caso de prueba idéntico, medición cuantitativa del éxito). Utilice esta habilidad cuando los agentes ignoren repetidamente una regla/README/convención o naveguen incorrectamente, y desee medir si un cambio en la documentación realmente altera el comportamiento. Se activa con 'is the convention even seen', 'why does no agent follow the rule', 'make a doc signpost measurably effective', 'desire-path analysis', 'trampelpfadanalyse'.

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

> **Español** — Versión oficial en español de `trampelpfadanalyse`.


# Análisis de Senderos Deseados (Desire-Path Analysis) — Hacer visibles empíricamente las convenciones para los LLM (Español)

Un método para descubrir errores en flujos de trabajo de pipelines y archivos de control que no proceden de un código defectuoso, sino de que **una convención resulta invisible para un LLM**. En lugar de adivinar si un README o una regla es "suficientemente clara", se mide empíricamente: se liberan subagentes ingenuos (sin contexto ni memoria previa) sobre el flujo de trabajo; su comportamiento se convierte en la **línea base (baseline)**; un cambio enfocado en la documentación (un "señalizador" o señal) es la **intervención**, y nuevos subagentes ingenuos proporcionan la **reevaluación (retest)**. La diferencia (diff) con respecto a la línea base constituye la medición del éxito.

El nombre proviene del concepto de *sendero deseado* (en alemán: *Trampelpfad*): el lugar por donde la gente camina realmente en vez de seguir la ruta pavimentada es donde debe estar el camino. Por analogía, las rutas de los LLM ingenuos muestran dónde se necesitan realmente la documentación o las barreras de protección, no dónde asumimos que deben estar.

## Cuándo utilizar esta habilidad

- Los agentes ignoran repetidamente una regla/convención a pesar de estar documentada.
- Deseas saber si un procedimiento es **visible/descubrible** para un LLM antes de escribir más documentación ("¿hay alguien aquí hablando solo?").
- Tras una reestructuración (nuevos directorios, renombrados): ¿pueden los agentes seguir encontrando los puntos de entrada?
- Realizaste un cambio en la documentación y deseas **demostrar** que funciona, no solo esperarlo.
- Prueba de integración antes de incorporar nuevos socios LLM a una pipeline.

No aplica para: errores puros de código (→ depuración sistemática), ni para la selección de patrones de coordinación de enjambres para tareas de producción (→ véase `swarm-operations`). Esta habilidad utiliza un enjambre de agentes ingenuos exclusivamente como **instrumento de medición**.

## La idea central en una frase

Trata la documentación como experiencia de usuario (UX): lo que cuenta no es lo que escribiste, sino lo que un usuario sin sesgos (aquí: un agente ingenuo) hace realmente con ello, y eso se mide, se modifica y se vuelve a medir.

---

## El proceso: 5 pasos

```
1. LÍNEA BASE       Subagentes ingenuos → medir comportamiento actual (cuantitativo)
2. ANÁLISIS RUTA    ¿Dónde falla exactamente? ¿Qué ubicación de doc induce a error?
3. INTERVENCIÓN     Colocar un "señalizador" (README/convención más visible)
4. REEVALUACIÓN     NUEVOS subagentes ingenuos, caso de prueba idéntico
5. DIFERENCIA       Reevaluación vs. Línea base → medición de éxito + evaluación honesta
```

### Paso 1 — Línea base: medir el comportamiento actual de forma ingenua

Primero formula el problema como una **pregunta verificable**, por ejemplo: "¿Crea el agente un registro en la ubicación exigida por la convención?" o "¿Encuentra el agente el punto de entrada de la pipeline?".

A continuación, libera a los subagentes ingenuos:

- **Ingenuo significa:** sin memoria del proyecto, sin habilidades, sin pistas previas; el agente solo conoce la ruta de entrada y la tarea. Esto mide la **descubribilidad pura a través de la documentación existente**, no el conocimiento previo del agente.
- **Copias en sandbox aisladas:** cada agente de prueba trabaja en su propia copia de la carpeta/flujo de trabajo afectado, de modo que las pruebas no se influyen entre sí y el estado real permanece intacto.
- **Mismo caso de prueba, múltiples repeticiones:** la variabilidad es real. Una prueba es una anécdota; n repeticiones (por ejemplo, 3 o más si es necesario) ofrecen una tasa.
- **Un modelo económico y "ingenuo"** es suficiente y realista: no debe adivinar de forma astuta, sino mostrar hacia dónde conduce la documentación a un agente promedio.

Prompt mínimo para la prueba (ajustar marcadores de posición):

```
Estás explorando <SISTEMA>. Está ubicado en: <RUTA>.
TAREA: <tarea específica>.
REGLAS:
1. Solo conoces la ruta anterior, nada más.
2. Explora para completar la tarea. Máx. <N> pasos.
3. Informa al final: DIRECTORIOS_VISITADOS, ARCHIVOS_LEÍDOS,
   TAREA_COMPLETADA (sí/no), ARCHIVO_MÁS_ÚTIL.
```

**Registrar como métricas de línea base** (siempre cuantitativas, nunca "parece mejor"):

| Métrica | Significado |
|---|---|
| Tasa de éxito | cuántas veces se completó la tarea según la convención (p. ej., 0/3) |
| Comportamiento erróneo | cuántas veces se usó una ubicación/método incorrecto (p. ej., 3/3 registro colectivo en lugar de individual) |
| Pasos hasta el objetivo | cuántos pasos/desvíos se tomaron para alcanzar el objetivo |
| Puntos ciegos | qué archivo/ubicación relevante no abrió nadie |

### Paso 2 — Análisis de ruta: ¿dónde falla realmente?

Evalúa conjuntamente los informes de prueba (basta con un "mapa de calor" de las ubicaciones visitadas):

- ¿Qué archivo se lee **con frecuencia** (HOT)? Si allí falta orientación, ese es el lugar más efectivo para colocar un señalizador.
- ¿Qué ubicación relevante **nunca** se abre (COLD / punto ciego)? Es efectivamente invisible, sin importar lo bueno que sea su contenido.
- ¿Dónde entra en bucle un agente o esquiva la convención (callejón sin salida, elusión)? Eso marca la laguna concreta de documentación.

Tabla de hallazgos:

| Hallazgo | Significado | Acción (→ Paso 3) |
|---|---|---|
| HOT + sin orientación | alto tráfico, sin señalización | colocar el señalizador justo allí |
| WARM + errores | los agentes llegan, se tropiezan | añadir ejemplo/aclaración |
| COLD | la ubicación nunca se encuentra | enlazar desde un archivo HOT |
| Elusión | la convención se pasa por alto | añadir indicación en el punto de elusión |

Resultado del Paso 2: **una hipótesis concreta y localizada** — "Los agentes leen X, pero X no menciona la convención; por eso terminan en Y."

### Paso 3 — Intervención: colocar un señalizador

Coloca **exactamente un** señalizador (una variable por ciclo; de lo contrario, la diferencia no será interpretable). Señalizadores típicos:

- Colocar la convención **de forma destacada por donde la ruta HOT ya pasa** (p. ej., una indicación corta y explícita en la parte superior del README/archivo de control más leído).
- Una **tabla de navegación rápida** al inicio del archivo central de arquitectura/visión general que apunte a los antiguos puntos ciegos.
- Una **referencia cruzada/señalizador** desde un archivo HOT hacia una ubicación COLD.
- Opcionalmente, una **barrera de protección (guardrail)** (p. ej., una indicación PreToolUse) para acciones peligrosas o que violen las convenciones.

Mantén el señalizador corto e imposible de pasar por alto: los agentes hojean por encima, raras veces leen con detenimiento.

### Paso 4 — Reevaluación con NUEVOS subagentes ingenuos

Repite el Paso 1 **de forma idéntica**: misma tarea, mismo número de repeticiones, mismo modelo, misma condición de ingenuidad, pero en copias de sandbox **con** el nuevo señalizador. Importante:

- Agentes **nuevos** sin memoria de la ejecución de línea base (de lo contrario, medirás el aprendizaje, no la descubribilidad).
- **Solo el señalizador** difiere con respecto a la configuración de la línea base.

### Paso 5 — Diferencia con respecto a la línea base + medición honesta del éxito

Coloca la reevaluación y la línea base frente a frente:

| Métrica | Línea base | Tras señalizador | Δ |
|---|---|---|---|
| Tasa de éxito | p. ej., 0/3 | p. ej., 3/3 | +3 |
| Comportamiento erróneo | p. ej., 3/3 | p. ej., 0/3 | −3 |
| Puntos ciegos | p. ej., 1 | p. ej., 0 | −1 |

Evaluación (sin adornar los resultados):

- **Funciona** (el comportamiento erróneo se reduce mensurablemente): mantener el señalizador y documentarlo.
- **No funciona** (poca Δ): el señalizador estaba en el lugar equivocado o era demasiado sutil → volver al Paso 2/3, probar un señalizador diferente y medir de nuevo.
- **Declarar abiertamente las limitaciones:** muestras pequeñas (n) son indicadores, no pruebas absolutas; un agente ingenuo modela a un "usuario promedio no informado", no a todos los usuarios reales; verificar explícitamente falsos positivos/negativos en la puntuación de éxito (¿qué contó exactamente como "completado"?).

---

## Mini caso de estudio (real, con cifras reales)

Problema: Una pipeline de tickets exigía que las finalizaciones triviales tuvieran cada una **un** registro dedicado por ticket, pero los agentes colocaban todo en **un único registro colectivo**.

- **Paso 1 (línea base):** 3 subagentes ingenuos, misma tarea → **3/3 utilizaron el registro colectivo** (convención no seguida).
- **Paso 2 (análisis de ruta):** el README más leído no mencionaba la regla del registro por ticket en un lugar visible → el camino ingenuo conducía al registro colectivo.
- **Paso 3 (intervención):** se colocó un "señalizador" corto y explícito sobre la convención de registro en un lugar destacado del README.
- **Paso 4 (reevaluación):** 3 subagentes ingenuos nuevos, tarea idéntica.
- **Paso 5 (diferencia):** **3/3 erróneos → 0/3 erróneos**, los tres crearon un registro correcto por ticket. (Documentado en el ticket T-20260621-44.)

Lección: La convención no estaba "redactada de forma débil", sino que era **invisible** en la ruta que realmente se leía. El señalizador en el lugar adecuado, verificado empíricamente, resolvió el problema.

---

## Fuente y métodos relacionados

Este método procede del Análisis de Senderos Deseados v2.0 (el enjambre como instrumento de medición empírico para el comportamiento de LLM). Los resultados de referencia originales de una prueba masiva (100 pruebas ingenuas) están documentados como evidencia de origen: el mayor punto ciego fue un directorio de ayuda que el **0/100** de los agentes visitó (a pesar de contener muchos archivos de ayuda), y la tarea "crear una nueva habilidad" tuvo un éxito del **0%** porque nadie encontró el directorio de plantillas; ambos fueron problemas clásicos de visibilidad y no de contenido.

## Véase también

- `swarm-operations` (dev) — catálogo de **patrones de coordinación** de enjambres para tareas de producción; incluye el análisis de senderos deseados solo como sección conceptual. Esta habilidad es la variante de **proceso** aplicable con un ciclo línea base→reevaluación.
- `pipeline-optimizer` (dev) — renovación de pipelines en 6 pasos; su reevaluación con subagentes nuevos se corresponde con los Pasos 4–5 de esta habilidad.
- `bugfix-protocol` / depuración sistemática — para errores reales de código en lugar de problemas de visibilidad.

## Registro de cambios

### 0.1.0 (2026-06-21)
- Adaptación inicial desde Desire-Path Analysis v2.0 (fuente: swarm-ai/BACH).
- Centrado en el proceso aplicable de 5 pasos (línea base → análisis de ruta → intervención → reevaluación → diferencia); los patrones de coordinación de enjambres se omiten deliberadamente (permanecen en `swarm-operations`). Neutral para el usuario con marcadores de posición; caso de estudio mini real.