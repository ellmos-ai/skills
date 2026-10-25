---
name: cloud-communication-protocols
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-25
language: es
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [ping-pong, agent-beam, listeners, cross-machine, sync-yard, coordination]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: "Skill paraguas para protocolos de comunicación entre agentes basados en la nube, en distintas máquinas (Ping-Pong, agent-beam, Listener y protocolos futuros). Úselo cuando el trabajo se coordine entre máquinas mediante una carpeta de sincronización compartida o un Message-Yard."

translated_from_sha256: 9f6c20f17b3f62f11b709c05cde26d3c28b48495a60ffaa26cf96a17af27a8ce
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.755928+00:00"
---
<img src="banner.png" width="100%" alt="cloud-communication-protocols banner">

# cloud-communication-protocols

Familia de protocolos que permite a dos o más agentes en máquinas distintas
coordinarse a través de una carpeta compartida sincronizada en la nube (el
"Yard") en lugar de un canal directo. Este skill es el **paraguas**: reúne
los protocolos, indica cuál está probado y bloquea los que aún son concepto.

## Cuándo usar

- El trabajo se extiende a dos o más máquinas (verificación, configuraciones
  espejo, pilotos) y no existe un canal directo de agente a agente.
- Se necesita un vocabulario común para encargos, respuestas, cadencia y
  escalado entre estas máquinas.

## Protocolos de esta familia

### 1. Ping-Pong (probado, protocolo base)

Dos o más workers con escaneos programados desfasados salvan la latencia de
sincronización de la nube: cada lado escanea el Yard en busca de encargos
dirigidos a él, ejecuta, deja la respuesta y puede emitir encargos de
seguimiento para el otro lado.

Reglas clave: escribir solo en el propio slot, evidencia para cada acción,
idempotencia, ningún secreto en el Yard (solo claves públicas, huellas o
rutas), deltas de error cooperativos, verificación mediante readback sobre
el log.

**Cadencia: frecuencia de sondeo adaptativa.** El control de cadencia no
forma parte de las reglas de carga útil del protocolo base, pero toda
implementación lo necesita: un intervalo de sondeo fijo o inunda un Yard
vacío o pierde trabajo nuevo. Aplican dos mecanismos, y ambos deben tratarse
explícitamente, no de forma implícita:

- **A — Autoajustable (predeterminado, sin entrada del operador; el patrón
  `cooldown`/backoff).** Al encontrar un encargo nuevo → saltar
  directamente al intervalo más rápido (p. ej., 15 min). Ejecución vacía →
  enfriar por una escalera: 4 ejecuciones vacías consecutivas → 30 min, 2
  más → 1 h, después duplicar cada serie vacía adicional (2 h, 4 h, 8 h)
  hasta un techo rígido (24 h, nunca más). Persistir el contador de
  ejecuciones vacías y el intervalo actual en un pequeño archivo de estado
  en el worker (no en la memoria de la conversación), para que sobreviva a
  reinicios; un cambio de cadencia implica eliminar el job programado
  anterior y crear uno nuevo con el nuevo intervalo, conservando el
  contador. Esquema de referencia completo, esquema del archivo de estado y
  otros tipos de bucle (ráfaga, asistencia de despertar): skill
  complementario **`cron-tuner`**.
- **B — Override instruido por el par.** Cada lado puede fijar
  explícitamente la cadencia del otro en el texto del encargo —
  `CADENCE: match 15m` para sincronizar con una ventana más estrecha, o
  `CADENCE: pause 1h → 2h after 3
  empty` para ralentizar a un lado que tiene trabajo profundo
  planificable. Quien cambie la cadencia de un par confirma el nuevo
  intervalo en el siguiente delta (el readback también aplica a los relojes).

Ambos mecanismos solo cambian el tiempo de reacción, nunca las reglas del
protocolo base (disciplina de slot, evidencia, ningún secreto). Un canal
mutuo `WAKE: <Grund>` permite escaneos fuera de ciclo como pista, nunca
como autoridad; borrar después de leer.

Especificación completa y evidencia de referencia:
`dev-bricks/system-gap-master` → `docs/communications-protocols-skill.md`.

### 2. agent-beam (concepto, bloqueado)

Para trabajo urgente: un paquete de prompt + script de arranque se deposita
en el slot de destino, y un watcher en la máquina de destino lo usa para
lanzar una ejecución local del agente — el agente "aterriza" con el encargo
y el arranque y empieza de inmediato.

Bloqueado: requiere un contrato de confianza de arranque firmado, un paso de
cuarentena/revisión y aprobación explícita del operador antes de cada
activación.

### 3. Listener / Ear-to-Ear-Listening (concepto, bloqueado)

Los watchers observan disparadores en el Yard (llegadas de archivos,
archivos de bandera, cambios en el registro) y lanzan agentes en la otra
máquina. "Ear-to-Ear": el listener de un host observa la bandeja de entrada
del otro host.

Bloqueado: primero se necesitan reglas de debouncing, listas blancas de
disparadores por slot y un contrato de seguridad.

## Invariantes comunes (todos los protocolos)

- El Yard es transporte, nunca espacio de trabajo y nunca almacén de
  secretos.
- Cada acción deja una evidencia verificable; "hecho" sin artefacto no es
  hecho.
- El manejo de errores es cooperativo: deltas de error con hipótesis y
  contraprueba; las segundas opiniones son bienvenidas.
- La ausencia de un socio se gestiona con la regla de vacante de la
  plataforma (p. ej., 48 h), no mediante escalado.

## Añadir nuevos protocolos

Los nuevos protocolos se unen a esta familia como subsecciones de
`communications-protocols-skill.md` (primero como concepto, con su propio contrato de
seguridad y evidencia antes de "probado"). Enumerarlos aquí con una línea
cada uno: nombre, estado (concepto/piloto/probado), propósito.
