---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: Apunta al módulo independiente steuer-assistent: una hoja de trabajo de recibos local y offline-first para los gastos relacionados con los ingresos de empleados en Alemania (Werbungskosten): registrar, sumar al céntimo y exportación privada en ZIP. Utilice este skill cuando los recibos de Werbungskosten deban prepararse de forma estructurada, con un límite claro: no es asesoramiento fiscal, no comprueba la deducibilidad y no crea ni envía declaraciones de impuestos (eso se realiza a través de ELSTER o software autorizado).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: es
status: active
---

<img src="banner.png" width="100%" alt="steuer-assistent banner">

> **Español** — Versión oficial en español de `steuer-assistent`.


# steuer-assistent -- Pointer Skill (Español)

Este skill es un **indicador ligero (wrapper)** hacia el repositorio del módulo público e independiente
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
(licencia MIT, público). El skill real reside allí; este repositorio solo
enlaza a él y documenta su instalación.

Nota: `steuer-assistent` está enfocado en la legislación fiscal alemana (gastos
de empleados relacionados con sus ingresos, "Werbungskosten"); su CLI y
documentación están diseñados en alemán.

## Qué hace el módulo

`steuer-assistent` es un módulo de Python pequeño y offline-first para
recibos autocategorizados de gastos de empleados relacionados con sus ingresos
en Alemania (Werbungskosten):

- Registrar recibos (categoría, importe, fecha, nota opcional).
- Sumar los gastos registrados al céntimo, por año.
- Exportar una hoja de trabajo privada e informal en un archivo ZIP (CSV + resumen + un
  aviso informal, sin los archivos de los recibos en sí).
- Almacenamiento local (por defecto `%USERPROFILE%\.steuer-assistent\steuer.db`), sin
  acceso a la red, sin carga en la nube y sin acceso a otras bases de datos.

## Límites (importante)

- **No es asesoramiento fiscal.** El módulo no evalúa la deducibilidad de
  partidas individuales y no crea ni envía declaraciones de impuestos.
- La presentación electrónica oficial se realiza exclusivamente a través de ELSTER o
  software autorizado, no a través de este módulo.
- Alcance: una hoja de trabajo privada para gastos de empleados relacionados con sus
  ingresos; no incluye el seguimiento de gastos comerciales ni de trabajo autónomo.

## Instalación (genérica, sin rutas locales)

1. Clonar el módulo:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <clone-path>
   ```
2. Instalar y verificar:
   ```bash
   cd <clone-path>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. Adoptar `<clone-path>/SKILL.md` en su propio entorno de skills (p. ej.,
   `~/.claude/skills/steuer-assistent/`). NO incluya rutas locales ni nombres de
   host reales en un entorno de skills con control de versiones.
4. Ajustar la ruta del almacenamiento si es necesario mediante `STEUER_ASSISTENT_DB=<path>` o
   `--store <path>`; el valor predeterminado es el directorio personal del usuario.
5. Para comandos CLI, privacidad y límites, consulte el README del repositorio del módulo.

## Origen de este pointer skill

Este wrapper se añadió el 23-07-2026 como una entrada de demostración para el
repositorio `ellmos-ai/skills`. **No hay duplicación de código**: el mantenimiento
y el control de versiones se realizan exclusivamente en el repositorio del módulo `ellmos-ai/steuer-assistent`.

## Historial de cambios

### 0.1.0 (2026-07-23)
- Pointer skill inicial para `ellmos-ai/steuer-assistent`.
