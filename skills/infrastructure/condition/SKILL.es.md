---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-28
description: Lenguaje de condiciones flexible para objetivos, prompts y tareas. Traduce condiciones, marcas de tiempo y dependencias de secuencia en gates verificables, de modo que un subpaso solo se ejecute tras una aprobación comprobada. Usar siempre con /condition, /if, /if-only, /when, /after, /and o /or, así como con expresiones como "solo cuando", "tan pronto como", "solo si", "después de", "esperar hasta", "después" o "no antes". Usar también cuando varios subobjetivos dependan entre sí o un objetivo contenga una aprobación posterior.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'condition/SKILL.md', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `condition`.


# condition — Lenguaje de condiciones para objetivos y prompts

## Idea principal

Las condiciones en texto libre se pasan por alto fácilmente. Por ello, traduce cada condición relevante en un gate nombrado y verificable:

> Generoso en la lectura, inflexible en la comprobación.

La entrada puede ser en lenguaje natural e incompleta. La traducción interna, sin embargo, debe registrar claramente:

1. qué condición debe cumplirse,
2. qué subpaso está bloqueado,
3. qué consulta de herramienta sirve como evidencia,
4. si el incumplimiento implica retraso o prohibición.

Bloquea únicamente el subpaso afectado. Continúa con el trabajo independiente.

## Elementos de lenguaje

| Expresión | Semántica | Ejemplo |
| --- | --- | --- |
| `/condition <Condición> -> <Paso>` | Gate canónico | `/condition Tests green -> Build release` |
| `/if <Condición> -> <Paso>` | Sinónimo de `/condition` | `/if Review complete -> Merge` |
| `/when <Condición> -> <Paso>` | Ejecutar tan pronto como se cumpla la condición | `/when Export finished -> Verify report` |
| `/if-only <Condición> -> <Paso>` | Solo si se cumple; de lo contrario no ejecutar | `/if-only Backup proven -> Delete legacy data` |
| `/after <Duración> -> <Paso>` | Desplazamiento de tiempo desde la creación | `/after 30 minutes -> Check status` |
| `/and` | Todas las condiciones vinculadas deben cumplirse | `/if Tests green /and Review present -> Merge` |
| `/or` | Al menos una condición es suficiente | `/if Approval present /or Emergency rule active -> Start` |

Utiliza condiciones numeradas como `/condition 1 ...` y `/condition 2 ...` cuando un prompt contenga varios gates. Si se mezclan `/and` y `/or`, no inventes una precedencia implícita de operadores: usa paréntesis o subcondiciones numeradas. Si el significado sigue siendo ambiguo, consulta antes de autorizar un paso de riesgo.

Trata `/if-only` como una prohibición. Si la condición no se puede comprobar, no ejecutes el paso. En caso de formulación poco clara y consecuencias irreversibles, elige la interpretación más estricta.

## Flujo de trabajo

### 1. Normalizar la condición

Traduce la entrada a una frase verificable. Convierte horas relativas al momento de la creación en una marca de tiempo absoluta con zona horaria.

| Entrada | Condición normalizada | Clase de evidencia |
| --- | --- | --- |
| `time 06:00` | La hora del sistema es al menos las 06:00 en la zona horaria acordada | Herramienta de reloj/tiempo |
| `after 2 hours` | La hora del sistema es al menos la hora de creación más dos horas | Herramienta de reloj/tiempo |
| `wenn Worker A fertig ist` | El artefacto de aceptación o estado de tarea de A muestra finalización | Herramienta de tareas/archivos |
| `wenn Tests grün sind` | La ejecución de prueba prescrita finaliza con éxito | Herramienta de procesos/pruebas |
| `nach dem Push` | El remoto de destino contiene el commit esperado | Herramienta de control de versiones |
| `wenn der User zustimmt` | Existe aprobación explícita en la conversación | Entrada del usuario |

Si no hay una vía de evidencia objetiva reconocible, indícalo abiertamente. Nunca formules un gate de manera que solo pueda cerrarse por suposición.

### 2. Registrar el estado del Gate

Si se dispone de un almacén persistente de gates, tareas o memoria, guarda al menos estos campos:

```text
id
condition
blocks
mode = wait | only
proof_method
status = open | met | dropped
created_at
evidence
```

Si no existe un almacén persistente, mantén el estado de forma visible en el objetivo actual, plan de tareas o documento de entrega. Solo afirma que un gate sobrevive a las sesiones si el almacenamiento utilizado es realmente persistente.

Un adaptador de runtime existente puede usar diferentes nombres de comando. Funcionalmente necesita: `open`, `list`, `meet` y `drop` u operaciones equivalentes.

### 3. Reordenar el trabajo

Un gate abierto no bloquea toda la tarea. Ejecuta todos los pasos independientes y vuelve a verificar el estado del gate antes del siguiente paso dependiente.

No realices sondeos (polling) activos en bucles cortos del agente. Para tiempos de espera más largos, utiliza un programador (scheduler), un trabajo en segundo plano o un evento que notifique una sola vez al ocurrir. Tras la señal de activación, vuelve a comprobar la condición real con la herramienta prevista.

### 4. Verificar estrictamente y cerrar

Ejecuta primero la consulta de la herramienta y luego cierra el gate con evidencia concreta. Las evidencias adecuadas incluyen, por ejemplo:

- Tiempo: marca de tiempo medida con zona horaria,
- Archivo: ruta, metadatos o hash del artefacto esperado,
- Pruebas: comando ejecutado, código de salida y resumen relevante,
- Repositorio: rama, ID de commit y comparación con el remoto,
- Proceso o tarea: ID estable y estado final medido,
- Aprobación: respuesta inequívoca del usuario en el contexto actual.

Una estimación, un estado esperado o la simple afirmación de otro worker no es suficiente si se dispone de una comprobación independiente.

Si un gate queda obsoleto por un cambio en la tarea, márcalo como `dropped` con la debida justificación. En el caso de `/or`, cierra o descarta también las alternativas que ya no se necesiten para que no queden gates zombi.

### 5. Escalar

Cuando se hayan completado todos los pasos independientes:

1. comprueba si el trabajo previo bloqueante se puede realizar activamente dentro de la tarea,
2. para condiciones de pura espera, utiliza un programador o trabajo en segundo plano adecuado,
3. en caso de decisiones del usuario o dependencias externas, entrega la tarea con un gate abierto y un estado intermedio claro.

No derives autorización adicional a partir de una condición. Un gate cumplido solo cambia el orden; no amplía el alcance autorizado de la tarea.

## Ejemplos y aplicación

### Objetivo con condición de tiempo

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

La verificación de datos puede realizarse antes. La publicación permanece bloqueada hasta que una consulta de tiempo actual compruebe que son al menos las 16:00.

### Prompt con múltiples condiciones

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Comprueba ambos gates por separado. Realiza el merge solo después.

### Prohibición en lugar de retraso

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Sin un backup verificado, no elimines nada y menciona la prohibición abierta en el informe final.

## Trampas habituales

- Repetir la condición solo en texto libre en lugar de mantenerla como un estado.
- Pausar un objetivo completo aunque solo un subpaso esté bloqueado.
- Guardar el tiempo relativo sin marca de tiempo de creación ni zona horaria.
- Sustituir la evidencia de la herramienta por suposiciones o autodeclaraciones.
- Tratar `/if-only` como una simple espera.
- Dejar abiertas las alternativas de gates no necesarias tras un `/or`.
- Incluir nombres de proveedores, modelos, usuarios o hosts en la mecánica general.
- Tratar una ruta de runtime local como un requisito para el propio lenguaje.

## Registro de cambios

### 1.1.0 (2026-07-28)

- Formulado de manera neutral respecto a proveedores, usuarios y sistemas para runtimes de skills compartidos.
- Se hizo explícito el uso en objetivos y prompts.
- Se describió el runtime como un adaptador intercambiable; se eliminaron rutas locales fijas y nombres de modelos.
- Se aclararon los enlaces ambiguos `/and`/`/or`, los estados persistentes y los límites de autorización.

### 1.0.0 (2026-07-25)

- Versión inicial con `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and` y `/or`.