---
name: file-collect-sort-action
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "Detecta solicitudes del usuario con la forma \"saca de una carpeta siempre ciertos archivos y recógelos en un destino\" y configura para ello el módulo file-collect-sort-action (CLI fcsa): un agente impulsado por configuración que escanea carpetas, categoriza archivos mediante plantillas y aplica acciones escalonadas (move/copy/duplicate-check/delete/OCR/place-information). Usa esta skill con frases como \"saca de <Ordner> siempre <Dateiart> y recógelos en <Ziel>\", \"ordena la carpeta X automáticamente según ...\", \"recoge los archivos entrantes de ... en ...\", \"organiza esta carpeta según reglas\" o \"mueve automáticamente todos los <Dateiart> de <Ordner>\". Configura SIEMPRE primero un Dry-Run y activa el modo real solo tras el «go» explícito del usuario; el borrado permanece por defecto en modo _trash."
# Kompatibilitaet
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [dateien, sortierung, automatisierung, config-driven, ordner-ueberwachung, duplikate, ocr]
language: es
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: [fcsa]
  services: []
  protocols: []
  python: []
  modules: [file-collect-sort-action]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 844e8b0e6411e463278a6084440cd4915bf241f8ab5a036d1fa25913e18c681f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="file-collect-sort-action banner">

# File Collect Sort Action

> El usuario dejó este módulo deliberadamente en espera pasiva hasta que una tarea concreta lo requiera
> (Ticket T-20260818-916568570, el usuario, textualmente: *"algún día diré: saca de la carpeta siempre tales y tales archivos y recógelos allí -> entonces reconoces la skill de nuestro módulo y la configuras"*). Esta skill ES la detección que estaba esperando.

## Cuándo se activa esta skill

Los disparadores son frases del usuario que describen una **recolección recurrente según regla**, no un "mueve este archivo una vez":

- "Saca de `<Ordner>` siempre `<Dateiart>` y recógelos en `<Ziel>`"
- "Ordena la carpeta `<X>` automáticamente según `<Kriterium>`"
- "Recoge los archivos entrantes de `<Quelle>` en `<Ziel>`"
- "Organiza esta carpeta según reglas" / "mueve automáticamente todos los `<Dateiart>` de `<Ordner>`"
- Cualquier variante que nombre el **origen**, la **característica de identificación** (tipo de archivo, patrón de nombre o contenido) y el **destino**, e implique que debe ocurrir **de forma repetida** (no solo una vez ahora)

**No** es esta skill: mover un único archivo puntual (eso lo hace un agente directamente, sin capa de configuración) — `dokument-ingest` (responde a "¿con qué leo el *contenido*?", no a "¿adónde pertenece el *archivo*?") — ni la indexación incremental de texto sin mover archivos (`gardener`).

## Qué puede hacer el módulo (resumen)

`file-collect-sort-action` (nombre corto **f-csa**, CLI **`fcsa`**) es un agente de escaneo→categorización→acción impulsado por configuración, con tres archivos de configuración y una memoria de procesamiento:

| Archivo | Función |
|---|---|
| `config.json` | `scan_paths` (lista positiva), inclusión/exclusión de formatos, reglas de detección de duplicados, puertas de seguridad (`allow_hard_delete`) |
| `categories-definitions.json` | Plantillas de detección por categoría (nombre de archivo/extensión/contenido), checks/gates, `default_target`, `default_actions` + `default_stepping` |
| `action-rules.json` | Parámetros de acción por categoría (destinos de move/copy, modo de duplicados, modo de borrado, backend de OCR, orden de colocación) |
| `processing-csa.json` | Se escribe **en cada carpeta escaneada**: archivos conocidos, su categoría, acciones aplicadas, huella (fingerprint) de la configuración efectiva |

IDs de acción conocidas: `duplicate_check`, `move`, `copy`, `delete`, `ocr_extract`,
`place_information`. Semántica de secuencia: `default_stepping: true` = las acciones se ejecutan de izquierda a derecha tal como se listan, y un ID de acción listado dos veces se ejecuta **dos veces**; `false` = conjunto (los duplicados colapsan en una sola ejecución).

## Modelo de seguridad — SIEMPRE respetar al configurar

- **El Dry-Run es obligatorio antes de cada primera ejecución real**, por cada ruta de escaneo. `fcsa run` (sin `--dry-run`) rechaza la ejecución sin un Dry-Run registrado para exactamente esa ruta.
- **Un cambio de configuración vuelve a desarmar la confirmación** (huella sobre los tres archivos de configuración): tras cada ajuste de configuración, la siguiente ejecución real necesita de nuevo un Dry-Run reciente.
- **El borrado es fail-closed.** `delete` siempre mueve a `trash_dir`, salvo que *tanto* `action-rules.json` (`delete.hard_delete: true`) *como* `config.json` (`allow_hard_delete: true`) acepten explícitamente. **Además, para esta skill aplica:** nunca activar el borrado definitivo sin una autorización explícita y separada del usuario; el valor por defecto sigue siendo `_trash`.
- **`scan_paths` es una lista positiva explícita**: cualquier otra ruta lanza `PathNotAllowedError`, y las rutas con segmento `.PRIVAT` o `CREDENTIALS` se rechazan al cargarse.
- **El Dry-Run no deja efectos (byte a byte) en la carpeta escaneada**: `processing-csa.json` se escribe únicamente en una ejecución real, nunca en un Dry-Run.

## Flujo: desde la frase del disparador hasta la automatización configurada

1. **Estructurar la tarea.** Extraer de la frase del usuario el origen, la(s) característica(s) de identificación y el/los destino(s). Si hay ambigüedad, preguntar de forma específica (¿tipo de archivo? ¿incluir subcarpetas? ¿qué hacer ante una colisión de nombres en el destino: skip/overwrite/rename/quarantine?).
2. **Localizar el módulo.** Primero comprobar con `fcsa --help` si la CLI está disponible. Si falta, determinar la vía de módulo o paquete autorizada para el sistema actual; no inventar una ruta local, un nombre de paquete ni un checkout paralelo. Tras una instalación, volver a ejecutar `fcsa --help` antes de crear configuraciones.
3. **Crear la carpeta de configuración.** `fcsa init <config-dir>`: escribe `scan_paths` primero en una carpeta nueva `inbox/` **dentro** de la propia carpeta de configuración, nunca automáticamente en una carpeta real del usuario. Plantillas de ejemplo para ello: `fcsa/_examples/*.example.json` en el módulo.
4. **Ajustar la configuración a la tarea real.** Establecer `scan_paths` en la carpeta de origen indicada, registrar en `categories-definitions.json` la(s) plantilla(s) de detección para el tipo de archivo indicado (`default_target` = destino indicado), y configurar en `action-rules.json` las acciones adecuadas (normalmente `move`, opcionalmente `duplicate_check` antes). `state_dir`/`trash_dir` NO deben estar dentro de un `scan_path` (el módulo lo rechaza; de lo contrario se produce un bucle de autoalimentación).
5. **Presentar siempre primero el Dry-Run:** `fcsa run --config-dir <config-dir> --dry-run`. Mostrar el resultado al usuario (qué se movería adónde y qué se detectó como duplicado).
6. **Activar el modo real solo tras el «go» explícito del usuario.** Solo entonces `fcsa run --config-dir
   <config-dir>` (sin `--dry-run`). `fcsa status --config-dir <config-dir>` muestra después el estado.
7. **Ampliar paso a paso** (usuario: «y luego se va ampliando con el tiempo»): añadir más categorías o carpetas en lugar de empezar una nueva configuración. Los tres archivos de configuración se pueden mantener de forma aditiva. Cada ampliación necesita de nuevo un Dry-Run antes de la siguiente ejecución real, por la huella de configuración.

## Límites / puntos abiertos conocidos (estado del ticket T-20260818-916568570)

- El módulo está en la pasada 1, con estado "development". La pipeline principal, la CLI y las puertas de seguridad están terminadas y probadas (63/63 tests), pero **nunca se ha activado contra una carpeta real del usuario**. La primera activación real es deliberadamente este uso de la skill. La visibilidad del repositorio es "private": no publicar sin un ticket propio `repo-publish-check`.
- Se documentan dos interpretaciones de lagunas de especificación (`CHANGELOG.md`/`TODO.md` en el módulo): `default_stepping: false` colapsa una acción listada dos veces en **una** sola ejecución; `duplicate_check` con resultado `skip` aborta **toda** la cadena de acciones restante para el archivo (no solo move/copy). Si es necesario, aclarar con el usuario antes de que una configuración dependa de ello.
- OCR es un backend enchufable (`none`/`command`); no se incluye ningún motor OCR propio. Para una extracción OCR real, conectar `ellmos-filecommander` `fc_ocr` mediante el tipo de backend `command`.

## Origen

Módulo construido en el ticket T-20260818-916568570 (pasada 1, fcsa-worker), dejado en espera pasiva (PARKED/until-trigger) por deseo del usuario hasta que se produzca exactamente el disparador descrito arriba. Esta skill implementa exactamente esa nota de espera.

## Changelog

### 1.0.0 (2026-08-18)
- Versión inicial. Documentada la detección de disparadores para tareas de «recoger/ordenar archivos automáticamente», el flujo de configuración con Dry-Run obligatorio y la activación real solo tras el «go» del usuario.
