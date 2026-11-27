---
name: kalender
version: 0.3.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-11-27
description: "Use when scheduling, querying, mirroring, or reporting appointments across separate calendar silos, importing TerminPilot/ICS files, or generating printable HTML/PDF/MD/TXT/ICS calendar sheets (e.g. 'add appointment', 'medical appointments in 2027 as PDF', /kalender). Do NOT use for software project milestones (use dev/dev-cycle)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, multi-calendar, reports, pdf, html, terminpilot, google-calendar, routinika]
language: en
status: stable
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Standalone multi-silo calendar with Flag-3 backend selection, lossless v0.1 migration, RFC 5545 import/export, and stdlib report generator (HTML/PDF/MD/TXT/ICS).\n'}
---

<img src="banner.png" width="100%" alt="kalender banner">

> **English** — Official English version of `kalender`.

## Overview & Purpose

Capture, mirror, query, and render appointments across **isolated calendar silos**
as print-ready **calendar sheets or structured reports (`HTML`, `PDF`, `MD`, `TXT`, `ICS`)**
with zero external Python dependencies. The core (`kalender_core.py`) uses a local
SQLite database (`store.db`) by default and migrates existing `v0.1` stores
losslessly on open.

**Flag 3 — Backend selection (`assist/prefs.json` → `kalender_backend`):**

| `kalender_backend` in `prefs.json` | Behavior |
|---|---|
| `local` (default) | Local multi-silo SQLite store (`store.db`) |
| `google` | Google Calendar MCP (LLM path only, not in core) |
| `routinika` | Routinika calendar via `module-installer` |
| `uptoday` | UpToday calendar via `module-installer` |
| not set | LLM asks the user interactively for the preferred backend |

---

## Preconfigured Calendar Silos

Opening a store automatically seeds eight standard calendar profiles via
`INSERT OR IGNORE` (custom profiles can be added anytime via `calendar add`):

| Silo ID | Label | Category (`category`) | Color |
|---|---|---|---|
| `user` | User Calendar *(default, delete-protected)* | `personal` | `#2563eb` |
| `tickets` | Ticket Calendar | `tasks` | `#7c3aed` |
| `finanzen` | Finance / Payment Deadlines | `finance` | `#059669` |
| `gesundheit` | Medical & Health Appointments | `health` | `#dc2626` |
| `geburtstage_privat` | Birthdays (private) | `birthdays` | `#db2777` |
| `geburtstage_beruflich` | Birthdays (professional) | `birthdays` | `#d97706` |
| `terminpilot` | TerminPilot / Scheduling Polls | `coordination` | `#0891b2` |
| `routinen` | Routines | `routines` | `#4b5563` |

---

## Triggers

| Phrase | Action |
|---|---|
| "Add dental checkup to health calendar" | `add ... --calendar gesundheit` |
| "What is on today / this week across all calendars?" | `today` / `week` (`--calendar all`) |
| "Export all medical appointments for 2027 as PDF" | `report --view year --year 2027 --calendar gesundheit --format pdf --out ...` |
| "Render a printable calendar sheet for December 2026" | `report --view month --month 2026-12 --format html` (or `--format pdf`) |
| "Import the TerminPilot ICS file" | `import-ics poll.ics --calendar terminpilot` |
| "Mirror this appointment into my main calendar" | `mirror <id> --to user` / `sync-mirrors` |

---

## CLI Entry Point

```bash
# Manage calendar profiles / silos
python kalender_core.py calendar list [--json]
python kalender_core.py calendar add club --name "Club Events" --category community --color "#0ea5e9"
python kalender_core.py calendar delete club

# Create an appointment (default silo: user)
python kalender_core.py add "Annual Checkup" --date 2027-03-15 --time 09:30 --duration 45 --calendar gesundheit --location "Clinic"

# Range & list queries (--calendar all is default; single ID or comma list supported)
python kalender_core.py today [--calendar all|user,gesundheit] [--json]
python kalender_core.py day --date 2027-03-15 [--calendar gesundheit] [--json]
python kalender_core.py week [--from 2027-03-15] [--calendar all]
python kalender_core.py month [--month 2027-03] [--calendar user,finanzen]
python kalender_core.py year --year 2027 [--calendar gesundheit] [--category health]
python kalender_core.py range --from 2027-01-01 --to 2027-06-30 [--search "Tax"]
python kalender_core.py list [--calendar all] [--category finance] [--search "Tax"] [--limit 50]

# Cross-silo operations: mirror, sync-mirrors, transfer, clone
python kalender_core.py mirror <event_id> --to user
python kalender_core.py sync-mirrors [--json]
python kalender_core.py transfer <event_id> --to finanzen
python kalender_core.py clone <event_id> --to routinen

# TerminPilot / RFC 5545 ICS import & export
python kalender_core.py import-ics terminpilot_export.ics [--calendar terminpilot] [--json]
python kalender_core.py export [--calendar gesundheit] [--from 2027-01-01] [--to 2027-12-31] [--out medical_2027.ics]

# Graphical calendar sheet & report generator (report / alias: render)
python kalender_core.py report --view month --month 2026-12 --format html --out december_2026.html
python kalender_core.py report --view month --month 2026-12 --format pdf --out december_2026.pdf
python kalender_core.py render --view year --year 2027 --calendar gesundheit --format pdf --title "Medical Appointments 2027" --out medical_2027.pdf
python kalender_core.py report --view week --from 2026-12-07 --format md --out week.md
python kalender_core.py report --view range --from 2027-01-01 --to 2027-03-31 --format txt
```

---

## Store & Schema (`v0.2.0`, backward-compatible with `v0.1`)

| Property | Value |
|---|---|
| Type | SQLite (`local` backend, 100% Python stdlib) |
| Default path | `skills/assist/kalender/store.db` |
| Override | `--store <path>` or environment variable `KALENDER_STORE` |
| Tables | `calendars`, `events` |

```sql
CREATE TABLE IF NOT EXISTS calendars (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT,
    color       TEXT,
    description TEXT,
    is_default  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id                 TEXT PRIMARY KEY,
    title              TEXT NOT NULL,
    date               TEXT NOT NULL,               -- YYYY-MM-DD
    time               TEXT,                        -- HH:MM (optional)
    duration_min       INTEGER,
    location           TEXT,
    description        TEXT,
    recurrence         TEXT,                        -- ICS RRULE (optional)
    ics_uid            TEXT UNIQUE,
    created_at         TEXT NOT NULL,
    updated_at         TEXT NOT NULL,
    calendar_id        TEXT NOT NULL DEFAULT 'user',
    category           TEXT,
    source_calendar_id TEXT,
    source_event_id    TEXT,
    link_mode          TEXT,                        -- NULL | 'mirror' | 'transfer' | 'clone'
    external_id        TEXT,
    end_time           TEXT,                        -- HH:MM (optional)
    status             TEXT NOT NULL DEFAULT 'planned'
);
```

---

## Design & Privacy

- **Zero Dependencies:** Every feature — including print-ready HTML calendar grids, the `%PDF-1.4` vector/report writer (WinAnsi encoding), and RFC 5545 import/export — runs exclusively on the Python standard library with zero network or browser dependencies.
- **Silo Isolation & Unified View:** Dedicated silos keep tickets, finances, birthdays, and health appointments cleanly separated while `--calendar all` merges them on demand.
- **Privacy:** Local appointments remain inside `store.db`; never commit `store.db` to Git.

---

## Related Resources

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`) — optional LLM-driven backend
- Skill `assist/haushalt-manager` — Routinika integration pattern
- `tools/module-installer/module_installer.py` — module integration helper

---

## Configuration & Templates (`kalender-config.json`, `templates/`)

Default silos, calendar/date defaults, first weekday, supported report formats, and template paths are externalized in [kalender-config.json](kalender-config.json) with self-healing fallback (`.corrupt.<ts>.bak` via `check-config --repair`). HTML, Markdown, and plain-text outputs load replaceable templates under `templates/` (`month-sheet.template.html`, `week-sheet.template.html`, `agenda-report.template.html`, `agenda-report.template.md`, `agenda-report.template.txt`, optionally overridden via `templates.custom_dir`).

```bash
python kalender_core.py check-config [--repair] [--json]
```

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.3.0 | 2026-11-27 | Externalized defaults, silos, and formatting options into `kalender-config.json` with self-healing (`check-config --repair`, `.corrupt.<ts>.bak`) and replaceable templates under `templates/*.template.{html,md,txt}` |
| 0.2.0 | 2026-11-27 | Multi-calendar silos (`calendars` + lossless `events` migration), cross-silo operations (`mirror`, `sync-mirrors`, `transfer`, `clone`), idempotent TerminPilot/ICS import (`import-ics`), extended range queries (`day`, `year`, `range`, `--json`), and graphical calendar sheet / report generator (`html`, `pdf`, `md`, `txt`, `ics`) |
| 0.1.1 | 2026-11-22 | Corrected language hint |
| 0.1.0 | 2026-06-22 | Initial creation — Flag-3 logic, local backend, ICS export |
