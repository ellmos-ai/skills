---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-30
description: >
  Lenguaje flexible de condiciones para objetivos, prompts y tareas. Traduce condiciones,
marcas de tiempo y dependencias de secuencia en puertas verificables, de modo que una subetapa solo se
ejecute tras una aprobación comprobada. Usar siempre con /condition, /if, /if-only,
/when, /after, /and o /or, así como con expresiones como "solo cuando", "tan pronto como",
"solo si", "después de", "esperar hasta", "después" o "antes no". Usar también cuando varios subobjetivos
dependen entre sí o un objetivo contiene una aprobación posterior.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
language: es
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "condition/SKILL.md"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---
# condition — Lenguaje de condiciones para objetivos y prompts

## Idea principal

Las condiciones en texto corrido se pasan por alto fácilmente. Por lo tanto, traduzca cada condición relevante a una puerta (gate) nombrada y verificable:

> Generoso al leer, inflexible al demostrar.

La entrada puede ser en lenguaje natural e incompleta. La traducción interna, sin embargo, debe registrar inequívocamente:

1. qué condición debe cumplirse,
2. qué subetapa está bloqueada,
3. qué consulta de herramienta sirve como prueba,
4. si el incumplimiento significa retraso o prohibición.

Bloquee solo la subetapa afectada. Continúe con el trabajo independiente.

## Bloques de construcción del lenguaje

| Expresión | Semántica | Ejemplo |
| --- | --- | --- |
| `/condition <Condición> -> <Paso>` | Puerta canónica | `/condition Tests en verde -> Construir release` |
| `/if <Condición> -> <Paso>` | Sinónimo de `/condition` | `/if Review completado -> mergear` |
| `/when <Condición> -> <Paso>` | Ejecutar tan pronto como se cumpla la condición | `/when Exportación lista -> Revisar informe` |
| `/if-only <Condición> -> <Paso>` | Solo si se cumple; de lo contrario no ejecutar | `/if-only Backup comprobado -> Eliminar datos antiguos` |
| `/after <Duración> -> <Paso>` | Desplazamiento de tiempo desde el momento de inicio | `/after 30 minutes -> Comprobar estado` |
| `/and` | Todas las condiciones vinculadas deben aplicarse | `/if Tests en verde /and Review listo -> mergear` |
| `/or` | Al menos una condición es suficiente | `/if Aprobación lista /or Regla de emergencia activa -> iniciar` |

Utilice condiciones numeradas como `/condition 1 ...` y `/condition 2 ...` cuando un prompt contenga múltiples puertas. Al mezclar `/and` y `/or`, no invente una precedencia de operadores implícita: utilice paréntesis o subcondiciones numeradas. Si el significado sigue siendo ambiguo, pida aclaraciones antes de liberar un paso de riesgo.

Trate `/if-only` como una prohibición. Si la condición no se puede probar, no ejecute el paso. En caso de formulación poco clara y consecuencias irreversibles, elija la interpretación más estricta.

## Flujo de trabajo

### 1. Normalizar condición

Traduzca la entrada a una oración verificable. Al establecer horas relativas, conviértalas a una marca de tiempo absoluta con zona horaria.

| Entrada | Condición normalizada | Clase de prueba |
| --- | --- | --- |
| `time 06:00` | La hora del sistema es al menos las 06:00 en la zona horaria acordada | Herramienta de reloj/tiempo |
| `after 2 hours` | La hora del sistema es al menos el momento de inicio más dos horas | Herramienta de reloj/tiempo |
| `wenn Worker A fertig ist` | El artefacto de entrega o estado de tarea de A muestra finalización | Herramienta de tarea/archivo |
| `wenn Tests grün sind` | La ejecución de prueba prescrita finaliza con éxito | Herramienta de proceso/prueba |
| `nach dem Push` | El remoto de destino contiene el commit previsto | Herramienta de control de versiones |
| `wenn der User zustimmt` | Existe consentimiento explícito en la conversación | Entrada de usuario |

Si no se reconoce un método de prueba objetivo, expréselo abiertamente. Nunca formule una puerta de modo que solo pueda cerrarse por suposición.

### 2. Registrar estado de la puerta

Si hay un almacén de puertas, tareas o memoria persistente disponible, guarde al menos estos campos:

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

Si no existe un almacén persistente, mantenga el estado visiblemente en el objetivo actual, plan de tareas o documento de entrega. Solo afirme que una puerta sobrevive a las sesiones si el almacenamiento utilizado es realmente permanente.

Un adaptador de tiempo de ejecución existente puede usar nombres de comando diferentes. Funcionalmente necesita: `open`, `list`, `meet` y `drop` u operaciones equivalentes.

### 3. Reordenar el trabajo

Una puerta abierta no bloquea todo el pedido. Ejecute todos los pasos independientes y vuelva a verificar el estado de la puerta antes del siguiente paso dependiente.

No realice sondeos activos en bucles de agentes cortos. Para tiempos de espera más largos, utilice un programador, trabajo en segundo plano o evento que notifique una vez tras su ocurrencia. Tras la señal de activación, vuelva a verificar la condición real con la herramienta designada.

### 4. Verificar estrictamente y cerrar

Primero ejecute la consulta de la herramienta, luego cierre la puerta con evidencia concreta. Las pruebas adecuadas incluyen:

- Tiempo: marca de tiempo medida con zona horaria,
- Archivo: ruta, metadatos o hash del artefacto esperado,
- Pruebas: comando ejecutado, código de salida y resumen relevante,
- Repositorio: rama, ID de commit y comparación remota,
- Proceso o Tarea: ID estable y estado final medido,
- Consentimiento: respuesta inequívoca del usuario en el contexto actual.

Una estimación, un estado esperado o la mera afirmación de otro trabajador no es suficiente si se dispone de una prueba independiente.

Si una puerta se vuelve obsoleta debido a cambios en el pedido, márquela como `dropped` con justificación. Para `/or`, cierre o descarte también las alternativas que ya no se necesiten para no dejar puertas zombi.

### 5. Escalar

Cuando se completen todos los pasos independientes:

1. compruebe si el trabajo previo de bloqueo se puede realizar activamente dentro de la tarea,
2. para condiciones de espera puras, utilice un programador o trabajo en segundo plano adecuado,
3. para decisiones de usuario o dependencias externas, entregue con una puerta abierta y un estado intermedio claro.

No derive autorización adicional de una condición. Una puerta cumplida solo cambia la secuencia; no amplía el alcance autorizado.

## Ejemplos

### Objetivo con condición de tiempo

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

La comprobación de datos puede realizarse antes. La publicación permanece bloqueada hasta que una consulta de tiempo actual demuestre al menos las 16:00.

### Prompt con múltiples condiciones

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Comprobar ambas puertas por separado. Solo fusionar después.

### Prohibición en lugar de retraso

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Sin un backup comprobado, no eliminar nada y citar la prohibición abierta en el informe final.

## Trampas comunes

- Repetir la condición solo en texto corrido en lugar de mantenerla como estado.
- Pausar un objetivo completo aunque solo una subetapa esté bloqueada.
- Guardar tiempo relativo sin hora de inicio ni zona horaria.
- Reemplazar la prueba de herramienta con suposiciones o autoevaluación.
- Tratar `/if-only` como una simple espera.
- Dejar abiertas puertas alternativas no utilizadas después de `/or`.
- Codificar nombres de proveedores, modelos, usuarios o hosts en la mecánica general.
- Tratar una ruta de runtime local como un requisito para el lenguaje en sí.

## Registro de cambios

### 1.1.0 (2026-07-28)

- Formulado de forma neutral respecto a proveedores, usuarios y sistemas para runtimes de skills compartidos.
- Se hizo explícito el uso en objetivos y prompts.
- Se describió el runtime como un adaptador intercambiable; se eliminaron rutas locales fijas y nombres de modelos.
- Se aclararon vínculos ambiguos de `/and`/`/or`, estados persistentes y límites de autorización.

### 1.0.0 (2026-07-25)

- Versión inicial con `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and` y `/or`.
