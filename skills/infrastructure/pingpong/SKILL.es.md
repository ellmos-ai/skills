---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "Opera una estación de radio limitada en el tiempo y vinculada a la sesión mediante una carpeta sincronizada en común. ListenSync escanea de forma sistemática en busca de encargos y novedades; WriteSync envía deltas y acuses de recibo. Usar con PingPong, Dosentelefon (teléfono de latas), ListenSync, WriteSync, Sync-Listener (listener de sincronización), Auftragswache (vigilancia de encargos), News-Scan (escaneo de novedades) o supervisión de Goal/Loop."
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: es
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

Opera dos o más sistemas como estaciones de radio mediante una carpeta de sincronización compartida. Mantén el contrato funcional neutral respecto al proveedor; solo el adaptador de continuación cambia.

## Determinar el modo

- ListenSync: Exactamente un listener sistemático por host. Escanea, asume los encargos pertinentes y, cuando hay respuestas, también ejecuta WriteSync.
- WriteSync: Cada actor que trabaja puede enviar sus propios deltas, encargos, novedades y acuses de recibo relevantes. Este modo no inicia ningún listener.
- Si falta el modo, usa ListenSync.

## Aclarar la participación (STATE y CALL)

Antes del contrato de ejecución, la comprobación en dos pasos decide si realmente hay alguien a quien contactar. `scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` responde con exactamente tres valores: salida 0 `call-for-me` (activar y generar un agente), salida 1 `idle` (estoy activo yo mismo, desactivar), salida 3 `check-failed` (ilegible; nunca tratarlo como inactividad). La participación requiere STATE y CALL a la vez; quien convoca un call lo termina al cumplir su propósito; de lo contrario caduca. Reglas completas en references/protocol.md.

## Establecer el contrato de ejecución

1. Usa 24h por defecto. Acepta también duraciones relativas como 15m, 2h, 3d o una hora de finalización absoluta en ISO 8601.
2. Mide la hora local de inicio e indica expires_at con fecha, hora y zona horaria.
3. Empieza con 15 minutos. Usa la cadencia de references/protocol.md, salvo que el usuario exija una cadencia fija.
4. Define el cumplimiento del objetivo como: alcanzada la hora final, escaneo final verificado por FileCommander, todas las entradas pertinentes detectadas hasta entonces procesadas o bloqueos documentados con precisión, state actualizado y scheduler propio finalizado.
5. Sin prueba de FileCommander, no afirmes ni escaneo ni cumplimiento del objetivo.

## Usar adaptadores de proveedor

### Codex

Antes del primer escaneo, crea explícitamente un Goal persistido con el contrato de ejecución completo y expires_at. Procesa por continuación exactamente un ciclo de escaneo completo. No cierres el Goal tras un ciclo vacío o exitoso individual. Después espera de forma real hasta next_scan_at, por ejemplo con:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

Al llegar a la hora de caducidad, ejecuta el ciclo de cierre. Marca el Goal como completado solo cuando se cumpla el criterio de éxito.

### Claude Code

Inicia el encargo como /loop <Kadenz> $pingpong. Si la skill ya proviene de una ejecución programada, no crees un segundo loop. Al cambiar la cadencia, reemplaza solo tu propio cron job. Elimínalo tras el ciclo de cierre.

## Ejecutar el ciclo

Lee references/protocol.md completo y ejecuta exactamente un ciclo de escaneo, procesamiento y actualización de state descrito allí. Usa ellmos FileCommander para cada acceso a la carpeta de sincronización. Un listado de shell, una entrada del scheduler o un nombre de archivo por sí solo no constituyen prueba de escaneo.

Si no hay actividad, no inventes trabajo. Informa brevemente: hora del escaneo, archivos de freshness leídos, cadencia actual, empty_runs, next_scan_at y expires_at.

## Ejecutar WriteSync

Escribe solo en la ranura propia del sistema o en un canal global explícitamente indicado. Indica remitente, destinatario, hora, referencia, acción, resultado, puntos abiertos y cadencia deseada. Fusiona en lugar de sobrescribir; sin credenciales; respeta los locks. Tras escribir, vuelve a leer el archivo canónico con FileCommander.

## Registro de cambios

### 1.1.0 (2026-09-13)

- Añadida la marca de participación específica de host STATE (campo `pingpong` en `agents/registry/<slot>.state.json`) y los archivos CALL dirigidos `call-<von>-to-<an|all>.txt` con caducidad; `pingpong_runtime.py` conoce para ello `state`, `call` y la comprobación en dos pasos `check` con resultado de tres valores. Los nombres antiguos `pull-` siguen leyéndose de forma transitoria. Implementación de T-20260830-425388998 según decisión del usuario del 2026-09-11 (corte mínimo: solo STATE, CALL y caducidad).

### 1.0.1 (2026-09-09)

- Añadidos metadatos declarativos de rol según el contrato opcional de rol del módulo v2; ningún starter neutral declara nada. La identidad del protocolo existente y la ruta de discovery se mantienen.

### 1.0.0 (2026-08-04)

- Contrato de ListenSync/WriteSync neutral respecto al proveedor, con adaptadores de Goal de Codex y de loop de Claude.
- Añadidos prueba de FileCommander, guardia de freshness, cadencia adaptativa y condición de caducidad absoluta.
