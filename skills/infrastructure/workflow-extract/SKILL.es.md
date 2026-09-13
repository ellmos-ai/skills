---
name: workflow-extract
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-30
description: >
  Construye una automatización de flujo de trabajo ejecutable y neutral para el usuario a partir de una transcripción de chat
  o de prompts de automatización existentes (ej. de otro sistema de agentes): un prompt recurrente
  o skill de automatización para Cron/Schedule/Loop. Alias: automations-extractor. Úsalo cuando se solicite:
  "haz una automatización de esto", "esto debe ejecutarse regularmente/por la noche", "extrae flujos de trabajo de estas
  transcripciones/automatizaciones", "construye una automatización a partir de esta sesión", o en `/workflow-extract`.
  Complementa sistemáticamente los bloques de construcción de automatización faltantes (selección por rotación,
  registro de verificación, idempotencia, higiene de logs, puerta de aprobación, traspaso de escalación, disciplina de reporte).
  También incluye el modo Auditoría de Flota (Fleet Audit): examinar flotas de automatización existentes en busca de fallos silenciosos,
  redundancia, desviación y vacíos. Si se necesita un skill ejecutable a petición, usa el skill hermano skill-extractor.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [automation, workflow, extraction, cron, schedule, loop, transcript, meta, rotation]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="workflow-extract banner">
# Workflow-Extract — Construir automatizaciones a partir de transcripciones de chat y automatizaciones externas (Español)

## Propósito

Algunos procesos no pertenecen a un skill ejecutable a petición que se carga manualmente, sino a una **automatización desatendida que se ejecuta sola**: verificaciones nocturnas, auditorías rotativas de proyectos, ejecuciones periódicas de mantenimiento. Este skill extrae dichos flujos de trabajo de dos tipos de fuentes: transcripciones de chat (un proceso desarrollado de forma interactiva que en el futuro debe ejecutarse sin supervisión) y prompts de automatización existentes de otros sistemas (ej. automatizaciones de Codex, tareas programadas, flujos de n8n), convirtiéndolos en prompts o skills de automatización neutros y robustos.

La diferencia con un flujo de trabajo interactivo: Una automatización **no tiene a nadie que la corrija**. Todo lo que el usuario interceptó en una sesión interactiva debe ser capturado por la propia automatización. Es precisamente por eso que existen los bloques de construcción en `automation-bausteine.md`.

## Proceso

### 1. Aclarar Fuente y Forma de Destino

| Fuente | Caso Típico |
| --- | --- |
| Sesión actual / Transcripción | Proceso desarrollado de forma interactiva, debe continuar ejecutándose periódicamente |
| Automatización externa (archivo de prompt, tarea cron, flujo n8n) | Portabilidad/abstracción a otro sistema o a la biblioteca |

Formas de destino (una o varias):

- **Prompt de Automatización:** texto de prompt independiente y neutral, utilizable en cualquier programador (automatizaciones Codex, Claude `/schedule`/cron, tareas programadas, n8n).
- **Skill de Flujo de Trabajo (Workflow Skill):** skill en la biblioteca que describe el proceso, que el prompt de automatización simplemente llama o parametriza (preferido cuando el mismo proceso se aplica a varios sistemas — fuente única de verdad).
- **Comando:** comando slash fino para la activación manual del mismo proceso.

### 2. Extraer el Núcleo del Flujo de Trabajo

Extraer de la fuente:

- **Tarea principal:** ¿Qué se verifica/mantiene/genera? (una oración)
- **Lógica de selección:** ¿A qué se aplica la tarea? ¿un objetivo fijo o rotación sobre un conjunto (un proyecto por ejecución)?
- **Prerrequisitos:** ¿Qué debe leerse/verificarse antes de trabajar (documentos raíz, registros, bloqueos)?
- **Deberes de documentación:** ¿Dónde se escriben los resultados, logs y tareas de seguimiento?
- **Rutas de salida:** ¿Cuándo finaliza la ejecución en modo solo lectura ("nada que hacer" es un resultado válido)?

En el caso de transcripciones de chat, evaluar además los bucles de corrección (ver `../skill-extractor/transcript-quellen.md`): Cada corrección del usuario es un candidato para una salvaguarda que la automatización necesitará por sí misma en el futuro.

### 3. Neutralizar

Sigue las reglas de `../skill-extractor/neutralisierung.md`: Separa la mecánica de la configuración, mueve rutas/hosts/nombres de proyectos a un bloque de configuración. Los prompts de automatización requieren urgentemente este bloque de configuración porque se copian literalmente en los programadores: los valores concretos pertenecen a UN solo lugar en el encabezado del prompt.

### 4. Complementar con Bloques de Construcción de Automatización

Contrasta el núcleo extraído con la lista de verificación en `automation-bausteine.md` y complementa los bloques faltantes: en particular, selección de rotación con registro de verificación, idempotencia, higiene de logs, respeto de bloqueos, salida en modo solo lectura e informe de finalización. Un flujo de trabajo sin estos bloques funciona durante la fase de prueba pero degenera en operación continua (verificaciones duplicadas, logs crecientes, colisiones con agentes paralelos).

### 5. Establecer Cadencia y Presupuesto

- **Vincular la frecuencia a la tasa de cambio:** Una verificación no necesita ejecutarse con más frecuencia de la que cambia su objeto. Experiencia de flotas de automatización consolidadas: Muchas verificaciones inicialmente horarias se redujeron a diarias/semanales; con la selección por rotación, incluso una cadencia baja cubre todo el pipeline.
- **Ventana nocturna para tareas pesadas**, las verificaciones cortas en modo solo lectura pueden ejecutarse con mayor frecuencia.
- **Conciencia de costos:** Cada ejecución consume tokens/cómputo; una ejecución que en su mayoría termina en modo solo lectura debe determinarlo tempranamente (leer el registro ANTES de realizar un análisis costoso).

### 6. Probar y Desplegar

1. **Ejecución de prueba (Dry Run):** Ejecuta el prompt finalizado una vez de forma interactiva (actuando como el programador) y verifica: ¿Finaliza limpiamente? ¿Escribe correctamente en el registro/log? ¿Permanece en el alcance?
2. **Prueba de caso límite:** Simula una ejecución donde no hay nada que hacer: debe finalizar en modo solo lectura con una breve entrada en el log, sin "inventar trabajo".
3. **Desplegar:** Registrar en el programador de destino; para formato de skill, almacenar en la biblioteca y desplegar.
4. **Supervisar ruta de fallos:** Revisa el log/registro tras las primeras 2-3 ejecuciones reales; las automatizaciones fallan con mayor frecuencia debido a desviaciones en las rutas (el objetivo cambió de lugar) y archivos de log crecientes.

## Modo Auditoría de Flota (Fleet Audit): Auditar una flota de automatización en ejecución

Para "revisa mis automatizaciones": no extraer, sino ayudar a operar la flota EXISTENTE. Verificar sistemáticamente mediante la fuente de automatización del sistema de destino (archivos de prompt/configuración, programaciones, logs de ejecución):

1. **Detección de fallos silenciosos / ejecuciones sin efecto (No-Op):** ¿La automatización se ejecuta pero no logra nada? (Leer logs/memorias de las últimas ejecuciones: ¿solo ejecuciones inactivas, errores, rutas muertas?)
2. **Redundancia + Retorno:** ¿Se superponen las automatizaciones en alcance? ¿El beneficio (resultado, problemas resueltos) justifica el consumo (tokens, ejecuciones)?
3. **Desviación (Drift):** ¿Las rutas de prompts, convenciones y programaciones aún coinciden con la realidad? (Objetivos movidos, políticas cambiadas, cadencia demasiado alta para la tasa de cambio).
4. **Reconciliación de catálogo:** ¿Falta alguna automatización que debería existir (vacíos en la cuadrícula de patrones)? Las sugerencias deben estar sujetas a aprobación (Bloque 12), nunca activarse solas.
5. **Informe de hallazgos:** una línea por automatización (conservar | ajustar | pausar | fusionar | eliminar) + justificación; realizar cambios solo tras la aprobación.

## Modo Masivo (Bulk): Revisar repositorios de automatización o muchas transcripciones

Para "revisa todas las automatizaciones del Sistema X en busca de flujos de trabajo abstraíbles" o "extrae candidatos a automatización de transcripciones de chat antiguas":

1. **Reducción de datos como en skill-extractor** (Map-Reduce mediante subagentes, patrón `swarm-operations`): Un subagente por paquete que informa por fuente: Tarea principal | Patrón (ej. verificación de rotación, verificación de estado, minería de ideas) | Elementos únicos | ¿Abstraíble y neutral? | ¿Cubierto por un skill existente?
2. **Patrón antes que piezas individuales:** Cuando muchas fuentes comparten la misma estructura (ej. 40 verificaciones de rotación), la ESTRUCTURA se convierte en un skill y los casos individuales en parametrizaciones, no en 40 skills individuales.
3. **Deduplicación contra el entorno de skills/comandos existente**, luego presentar la lista numerada de candidatos al usuario antes de la construcción masiva.

## Ejemplo

```text
Usuario: "Hoy probamos la verificación de citas de un documento; a partir de ahora esto debería ejecutarse semanalmente en todos los documentos."

1. Forma de destino: Prompt de automatización para el programador + referencia a rotation-check.
2. Núcleo: Verificar citas de documentos contra fuentes originales (web/base de datos), aplicar correcciones, escribir tarea de seguimiento "volver a cargar" en TODO.md si se modifica.
3. Neutralizar: Raíz del pipeline, rutas de registro/log → bloque de configuración.
4. Complementar bloques: Selección por rotación (un documento por ejecución), leer registro ANTES de la selección, salida en modo solo lectura ("todas las fuentes ok"), higiene de logs, informe de finalización.
5. Cadencia: Semanal es suficiente (los documentos cambian lentamente); ejecución de prueba + prueba inactiva, luego al programador.
```

## Banderas Rojas (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "El proceso se ejecutó en la sesión, así que se ejecutará como automatización" | Sin usuario faltan todas las salvaguardas correctivas; la lista de verificación de bloques es obligatoria. |
| "Cada hora no hace daño" | Sí hace daño: tokens, crecimiento de logs, riesgo de colisión. Vincula la cadencia a la tasa de cambio. |
| "Construiré una automatización separada para cada variante" | Estructura compartida como skill, variantes como parámetros. |
| "No se encontró nada — supongo que buscaré otro trabajo" | Salida en modo solo lectura con entrada en el log es el resultado correcto de una ejecución inactiva. |

## Skills Relacionados

- `skill-extractor`: misma extracción, el objetivo es un skill ejecutable a petición; comparte neutralización y fuentes de transcripción.
- `rotation-check`: estructura estándar para verificaciones rotativas de pipeline (tipo de automatización más frecuente); referenciar como bloque de construcción en lugar de reinventar.
- `swarm-operations`: patrón de enjambre para revisión masiva.

## Registro de Cambios (Changelog)

### 1.1.0 (2026-07-03)
- Modo Auditoría de Flota (verificación de la flota de automatización en ejecución: fallos silenciosos, redundancia, desviación, vacíos), integrado en lugar de un skill separado.
- Tres nuevos bloques de construcción en automation-bausteine.md: Puerta de aprobación mediante archivos centinela (12), Escalación escalonada con artefacto de traspaso (13), Disciplina de reporte para monitores (14).

### 1.0.0 (2026-07-03)
- Versión inicial. Creada a partir de la abstracción del inventario de automatizaciones de Codex (77 automatizaciones, patrón dominante de verificación por rotación) en bloques de construcción neutrales para el usuario.
