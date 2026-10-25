---
name: tech-detect
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Registra versiones y hardware con pruebas en instantáneas privadas y compara equipos sin confundir ausencia de observación con desinstalación."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [inventory, hardware, software, python, versions, host-comparison]
language: es
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# Tech Detect

Úsalo solo en un equipo propio o autorizado. Lee primero el inventario y sus reglas por equipo. En una estructura como `.SYNC/_inventory`, el JSON `systems/<slot-propio>.json` es la entrada; este skill no lo actualiza ni modifica otros equipos.

1. Comprueba permisos, bloqueos, identificador del equipo y una salida privada. Ejecuta `python -X utf8 scripts/techshot.py capture --seed <inventario>/systems/<slot-propio>.json --slot <slot-propio> --output <privado>/techshot-<UTC>.json`.
2. El ayudante local lee el sistema y, según la plataforma, el registro de desinstalación de Windows, `dpkg-query` o Homebrew. Ninguna fuente cubre necesariamente todas las aplicaciones. No uses `Win32_Product`: [Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-software-installations?view=powershell-7.6) documenta comprobaciones y posibles reparaciones MSI.
3. Conserva por separado el intérprete Python efectivo, cada candidato observado en PATH y las instalaciones o entornos virtuales indicados con `--python-path`. Solo el intérprete actual tiene versión exacta por defecto. `--probe-python <ruta-fiable>` ejecuta explícitamente `-I -S --version`; sin esa prueba, la versión queda desconocida.
4. Cada instalación conserva identidad, versión, fuente y calidad `observed`, `reported`, `uncertain` o `unknown`. Los datos de hardware del inventario son declarados, no medidos en vivo. Registra errores y cobertura.
5. Compara dos archivos privados con `python -X utf8 scripts/techshot.py compare --left <a.json> --right <b.json> --output <comparación.json>`. Diferencia versiones distintas de paquetes no observados; no observar un paquete no demuestra que falte. Une alias solo con pruebas del fabricante.
6. Vincula capturas periódicas al programador existente solo tras autorización y comprueba su ejecución real por separado. Un commit no instala tareas programadas.

Contratos: `ellmos.techshot.v1` y `ellmos.techshot-comparison.v1`. Las instantáneas son observaciones junto al inventario existente, pueden contener rutas privadas y no prueban por sí solas seguridad ni vulnerabilidad. Entrega a `security-tech-stack-check` solo componentes y hashes necesarios.

## Cambios

### 1.0.0 (2026-10-25)

- Captura local y comparación entre equipos con calidad de evidencia explícita.

Observaciones de hardware: sistema operativo, arquitectura, CPU, RAM y capacidad del sistema de archivos se miden por separado del inventario declarado, con fuente o unknown. GPU queda unknown sin un colector portátil. Linux admite dpkg-query o rpm. La comparación marca campos de hardware diferentes o desconocidos; unknown no significa igual. No recoger números de serie, MAC ni PATH completo.

Comparación: distintos slot producen axis=cross-host aunque coincida hostname; el mismo slot y hostname con distintas horas capturadas produce axis=same-host-time. Se preservan el orden chronology, los hashes de entrada, horas, identidad, seed y cobertura. Una versión conocida igual con otra instalación desconocida sigue visible como version-uncertain. Rechazar procedencia obligatoria ausente; los archivos históricos completos siguen admitidos. La fecha de comparación no es una medición nueva.
