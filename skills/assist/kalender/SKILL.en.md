---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: >
  Calendar skill with user-adaptive backend selection (Flag 3). Default: local
  SQLite store. Optional: Google Calendar MCP, Routinika or UpToday as
  backend — controlled via assist/prefs.json. Without preference the LLM
  asks the user interactively.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags:
  - kalender
  - termine
  - events
  - ics
  - google-calendar
  - routinika
language: en
status: stable

dependencies:
  tools: []
  services:
    - name: Google Calendar MCP
      optional: true
      purpose: "Backend option when kalender_backend=google in prefs.json"
  protocols:
    - name: ICS / iCalendar
      optional: true
      purpose: "Import/export of appointments (RFC 5545 subset)"
  python: []

provenance:
  origin: eigenentwurf
  origin_path: ""
  origin_version: ""
  origin_repo: ""
  origin_license: MIT
  last_sync_from_origin: ""
  notes: >
    Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/).
    Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend).
    ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.
---

## Purpose

Capture, query and manage appointments — with a selectable backend. The core
(`kalender_core.py`) always uses the **local SQLite store** as the default.
The LLM selects an alternative backend from `assist/prefs.json` if needed.

**Flag 3 — Backend selection:**

| `kalender_backend` in prefs.json | Behaviour |
|---|---|
| `local` (default) | SQLite store in this skill folder |
| `google` | Google Calendar MCP (LLM path only, not in core.py) |
| `routinika` | Routinika calendar via module-installer (not impl. v0.1) |
| `uptoday` | UpToday calendar via module-installer (not impl. v0.1) |
| not set | LLM asks the user interactively for preferred backend |

> `kalender_core.py` implements the `local` backend exclusively.
> Google Calendar MCP and further backends are LLM-driven and are
> documented in SKILL.md, not in the core.

---

## Triggers

| Phrase | Action |
|---|---|
| "Add an appointment" | Capture a new appointment |
| "What is on today?" | Query today's appointments |
| "What is on this week?" | 7-day overview |
| "Appointment [title] on [date]" | Create appointment with date |
| "All appointments in [month]" | Monthly overview |
| "Delete appointment [ID]" | Remove appointment |
| "Export appointment" | ICS export of all/individual appointments |

---

## Workflow

1. **Check backend**: read `assist/prefs.json` → `kalender_backend`.
2. **Without preference**: LLM asks user: local calendar, Google Calendar or other?
3. **Local backend**: core.py — create/query/delete appointment in SQLite store.
4. **Google backend**: LLM calls Google Calendar MCP directly (core.py not involved).
5. **Output**: Readable appointment list or confirmation.

---

## CLI Entry Point

```bash
# Create appointment
python kalender_core.py add "Dentist" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Dr. X practice"]

# Today's appointments
python kalender_core.py today

# Weekly overview
python kalender_core.py week [--from 2026-06-22]

# Monthly overview
python kalender_core.py month [--month 2026-07]

# All appointments (optionally with search term)
python kalender_core.py list [--search "Dentist"] [--limit 50]

# Delete appointment
python kalender_core.py delete <id>

# ICS export
python kalender_core.py export [--id <id>] [--out calendar.ics]

# Backend check
python kalender_core.py check-backend

# Alternative store (e.g. for tests)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## Store

| Property | Value |
|---|---|
| Type | SQLite (local backend) |
| Path (default) | `skills/assist/kalender/store.db` |
| Override | `--store <path>` or env `KALENDER_STORE` |
| Tables | `events` |

### Schema

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

## Attitude

- The core implements only the `local` backend — lightweight, no external dependencies.
- ICS export generates a valid RFC 5545 subset (VCALENDAR + VEVENT), importable into all common calendar apps.
- ICS import (parsing) is not yet implemented in v0.1 — planned for v0.2.
- Recurrence rules (`recurrence`/RRULE) are stored but not evaluated — evaluation is v0.2.

---

## Privacy

- Local appointments stay in `store.db` — no network access in the core.
- When using the Google Calendar backend, Google Calendar MCP processes the data — Google's privacy policy applies.
- Do not commit `store.db` to Git (recommended: `.gitignore`).

---

## Related Resources

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`) — alternative backend, LLM-driven
- Skill `assist/haushalt-manager` — Routinika integration (presence check pattern)
- `tools/module-installer/module_installer.py` — for future Routinika/UpToday backend integration

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-06-22 | Initial creation — Flag-3 logic, local backend, ICS export |
