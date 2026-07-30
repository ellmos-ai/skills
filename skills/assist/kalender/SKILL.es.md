---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Habilidad de calendario con selección de backend adaptable al usuario (Flag 3). Por defecto: almacenamiento SQLite local. Opcional: Google Calendar MCP, Routinika o UpToday como backend — controlado mediante assist/prefs.json. Sin preferencia, el LLM consulta al usuario de forma interactiva.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: es
status: stable
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
---

> **Español** — Versión oficial en español de `kalender`.


## Descripción general y propósito

Capturar, consultar y gestionar citas, con un backend seleccionable. El núcleo
(`kalender_core.py`) siempre utiliza el **almacenamiento SQLite local** por defecto.
El LLM selecciona un backend alternativo de `assist/prefs.json` si es necesario.

**Flag 3 — Selección de backend:**

| `kalender_backend` en prefs.json | Comportamiento |
|---|---|
| `local` (predeterminado) | Almacenamiento SQLite en la carpeta de esta habilidad |
| `google` | Google Calendar MCP (solo ruta LLM, no en core.py) |
| `routinika` | Calendario Routinika mediante module-installer (no impl. v0.1) |
| `uptoday` | Calendario UpToday mediante module-installer (no impl. v0.1) |
| no establecido | El LLM consulta al usuario de forma interactiva sobre el backend preferido |

> `kalender_core.py` implementa exclusivamente el backend `local`.
> Google Calendar MCP y otros backends son gestionados por el LLM y están
> documentados en SKILL.md, no en el núcleo.

---

## Desencadenadores

| Frase | Acción |
|---|---|
| "Añadir una cita" | Capturar una nueva cita |
| "¿Qué hay para hoy?" | Consultar las citas de hoy |
| "¿Qué hay esta semana?" | Vista general de 7 días |
| "Cita [título] el [fecha]" | Crear cita con fecha |
| "Todas las citas de [mes]" | Vista general mensual |
| "Eliminar cita [ID]" | Eliminar cita |
| "Exportar cita" | Exportación ICS de todas las citas o de citas individuales |

---

## Flujo de trabajo y procedimiento

1. **Comprobar backend**: leer `assist/prefs.json` → `kalender_backend`.
2. **Sin preferencia**: el LLM pregunta al usuario: ¿calendario local, Google Calendar u otro?
3. **Backend local**: core.py — crear/consultar/eliminar cita en el almacenamiento SQLite.
4. **Backend Google**: el LLM llama a Google Calendar MCP directamente (core.py no interviene).
5. **Salida**: Lista de citas legible o confirmación.

---

## Punto de entrada CLI

```bash
# Create appointment (Deutsch)
python kalender_core.py add "Dentist" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Dr. X practice"]

# Today's appointments (Deutsch)
python kalender_core.py today

# Weekly overview (Deutsch)
python kalender_core.py week [--from 2026-06-22]

# Monthly overview (Deutsch)
python kalender_core.py month [--month 2026-07]

# All appointments (optionally with search term) (Deutsch)
python kalender_core.py list [--search "Dentist"] [--limit 50]

# Delete appointment (Deutsch)
python kalender_core.py delete <id>

# ICS export (Deutsch)
python kalender_core.py export [--id <id>] [--out calendar.ics]

# Backend check (Deutsch)
python kalender_core.py check-backend

# Alternative store (e.g. for tests) (Deutsch)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## Almacenamiento

| Propiedad | Valor |
|---|---|
| Tipo | SQLite (backend local) |
| Ruta (predeterminada) | `skills/assist/kalender/store.db` |
| Sobrescribir | `--store <path>` o variable de entorno `KALENDER_STORE` |
| Tablas | `events` |

### Esquema

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (short: 8 hex)
    title        TEXT NOT NULL,         -- appointment name
    date         TEXT NOT NULL,         -- ISO date YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- duration in minutes (optional)
    location     TEXT,                  -- location (optional)
    description  TEXT,                  -- note/description
    recurrence   TEXT,                  -- ICS RRULE (optional, e.g. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID for import/export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## Filosofía de diseño

- El núcleo implementa únicamente el backend `local`: ligero, sin dependencias externas.
- La exportación ICS genera un subconjunto válido de RFC 5545 (VCALENDAR + VEVENT), importable en todas las aplicaciones de calendario habituales.
- La importación ICS (análisis sintáctico) aún no está implementada en v0.1 (planificada para v0.2).
- Las reglas de recurrencia (`recurrence`/RRULE) se almacenan pero no se evalúan (la evaluación está planificada para v0.2).

---

## Privacidad

- Las citas locales permanecen en `store.db`: sin acceso a la red en el núcleo.
- Al utilizar el backend de Google Calendar, Google Calendar MCP procesa los datos; se aplica la política de privacidad de Google.
- No confirmar `store.db` en Git (recomendado: `.gitignore`).

---

## Recursos relacionados

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`): backend alternativo, impulsado por LLM
- Skill `assist/haushalt-manager`: integración de Routinika (patrón de verificación de presencia)
- `tools/module-installer/module_installer.py`: para la futura integración del backend de Routinika/UpToday

---

## Registro de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-06-22 | Creación inicial: lógica Flag-3, backend local, exportación ICS |