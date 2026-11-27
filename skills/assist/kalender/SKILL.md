---
name: kalender
version: 0.2.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-11-27
description: "Verwenden, wenn Termine, getrennte Kalender-Silos, TerminPilot-/ICS-Importe oder grafische Kalenderblätter und Berichte (HTML/PDF/MD/TXT/ICS) verwaltet, gespiegelt oder abgefragt werden sollen (z. B. 'Termin eintragen', 'Arzttermine 2027 als PDF', /kalender). NICHT verwenden für reine Projekt-Meilenstein-Planung (dafür dev/dev-cycle)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, multi-calendar, reports, pdf, html, terminpilot, google-calendar, routinika]
language: de
status: stable
visibility: public
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Eigenständiger Multi-Silo-Kalender mit Flag-3-Logik, verlustfreier v0.1-Migration, RFC-5545-Import/Export und Stdlib-Berichtsgenerator (HTML/PDF/MD/TXT/ICS).\n'}
---

<img src="banner.png" width="100%" alt="kalender banner">

## Zweck

Termine über **getrennte Kalender-Silos** erfassen, spiegeln, abfragen und als
druckreifes **Kalenderblatt oder Terminbericht (`HTML`, `PDF`, `MD`, `TXT`, `ICS`)**
ausgeben — ohne externe Python-Abhängigkeiten. Der Core (`kalender_core.py`)
arbeitet standardmäßig mit dem lokalen SQLite-Store (`store.db`) und migriert
bestehende `v0.1`-Datenbanken beim Öffnen verlustfrei.

**Flag 3 — Backend-Wahl (`assist/prefs.json` → `kalender_backend`):**

| `kalender_backend` in `prefs.json` | Verhalten |
|---|---|
| `local` (Standard/Default) | Lokaler Multi-Silo-SQLite-Store (`store.db`) |
| `google` | Google-Calendar-MCP (LLM-gesteuert, nicht im Core) |
| `routinika` | Routinika-Kalender via `module-installer` |
| `uptoday` | UpToday-Kalender via `module-installer` |
| nicht gesetzt | LLM fragt interaktiv nach bevorzugtem Backend |

---

## Vorkonfigurierte Kalender-Silos

Beim ersten Öffnen eines Stores werden acht Standard-Profile automatisch per
`INSERT OR IGNORE` angelegt (weitere eigene Profile jederzeit per `calendar add`):

| Silo-ID | Bezeichnung | Kategorie (`category`) | Farbe |
|---|---|---|---|
| `user` | Nutzerkalender *(Default, löschgeschützt)* | `personal` | `#2563eb` |
| `tickets` | Ticket-Kalender | `tasks` | `#7c3aed` |
| `finanzen` | Finanzkalender / Zahlungstermine | `finance` | `#059669` |
| `gesundheit` | Arzttermine & Gesundheit | `health` | `#dc2626` |
| `geburtstage_privat` | Geburtstage (privat) | `birthdays` | `#db2777` |
| `geburtstage_beruflich` | Geburtstage (beruflich) | `birthdays` | `#d97706` |
| `terminpilot` | TerminPilot / Terminabstimmung | `coordination` | `#0891b2` |
| `routinen` | Routinen | `routines` | `#4b5563` |

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Trag Zahnarzttermin im Gesundheitskalender ein" | `add ... --calendar gesundheit` |
| „Was steht heute / diese Woche insgesamt an?" | `today` / `week` (`--calendar all`) |
| „Zeig mir alle Arzttermine für 2027 als PDF" | `report --view year --year 2027 --calendar gesundheit --format pdf --out ...` |
| „Erstelle ein druckbares Kalenderblatt für Dezember 2026" | `report --view month --month 2026-12 --format html` (oder `--format pdf`) |
| „Importiere die TerminPilot-Datei in den Kalender" | `import-ics abstimmung.ics --calendar terminpilot` |
| „Spiegle den Termin in den Nutzerkalender" | `mirror <id> --to user` / `sync-mirrors` |

---

## CLI-Einstieg

```bash
# Kalender-Silos verwalten
python kalender_core.py calendar list [--json]
python kalender_core.py calendar add vereinsarbeit --name "Vereinskalender" --category community --color "#0ea5e9"
python kalender_core.py calendar delete vereinsarbeit

# Termin anlegen (Default-Silo: user)
python kalender_core.py add "Vorsorgeuntersuchung" --date 2027-03-15 --time 09:30 --duration 45 --calendar gesundheit --location "Praxis"

# Zeitraum- & Listenabfragen (--calendar all ist Standard; Einzel- oder Kommaliste möglich)
python kalender_core.py today [--calendar all|user,gesundheit] [--json]
python kalender_core.py day --date 2027-03-15 [--calendar gesundheit] [--json]
python kalender_core.py week [--from 2027-03-15] [--calendar all]
python kalender_core.py month [--month 2027-03] [--calendar user,finanzen]
python kalender_core.py year --year 2027 [--calendar gesundheit] [--category health]
python kalender_core.py range --from 2027-01-01 --to 2027-06-30 [--search "Steuer"]
python kalender_core.py list [--calendar all] [--category finance] [--search "Steuer"] [--limit 50]

# Silo-Operationen: Spiegeln, Synchronisieren, Verschieben, Klonen
python kalender_core.py mirror <event_id> --to user
python kalender_core.py sync-mirrors [--json]
python kalender_core.py transfer <event_id> --to finanzen
python kalender_core.py clone <event_id> --to routinen

# TerminPilot- / RFC-5545-ICS-Import & -Export
python kalender_core.py import-ics terminpilot_export.ics [--calendar terminpilot] [--json]
python kalender_core.py export [--calendar gesundheit] [--from 2027-01-01] [--to 2027-12-31] [--out arzt_2027.ics]

# Grafisches Kalenderblatt & Berichtsgenerator (report / Alias: render)
python kalender_core.py report --view month --month 2026-12 --format html --out dezember_2026.html
python kalender_core.py report --view month --month 2026-12 --format pdf --out dezember_2026.pdf
python kalender_core.py render --view year --year 2027 --calendar gesundheit --format pdf --title "Arzttermine 2027" --out arzt_2027.pdf
python kalender_core.py report --view week --from 2026-12-07 --format md --out woche.md
python kalender_core.py report --view range --from 2027-01-01 --to 2027-03-31 --format txt
```

---

## Store & Schema (`v0.2.0`, abwärtskompatibel zu `v0.1`)

| Eigenschaft | Wert |
|---|---|
| Typ | SQLite (`local`-Backend, 100 % Stdlib) |
| Pfad (Standard) | `skills/assist/kalender/store.db` |
| Override | `--store <pfad>` oder Umgebungsvariable `KALENDER_STORE` |
| Tabellen | `calendars`, `events` |

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

## Haltung & Datenschutz

- **Zero Dependencies:** Alle Funktionen einschließlich HTML-Monatsblatt, `%PDF-1.4`-Vektor-/Berichtsgenerator (WinAnsi-Umlaute) und RFC-5545-Import/Export laufen rein mit der Python-Standardbibliothek — ohne Browser-Start und ohne Netzwerkzugriff.
- **Silo-Isolation & Überblick:** Getrennte Fachkalender verhindern Vermischung (z. B. Tickets vs. Geburtstage vs. Finanzen), während `--calendar all` jederzeit die zusammengeführte Gesamtansicht liefert.
- **Datenschutz:** `store.db` bleibt lokal auf dem Gerät und gehört nicht in öffentliche Git-Repositories.

---

## Verwandte Ressourcen

- Google-Calendar-MCP (`mcp__claude_ai_Google_Calendar__*`) — optionales LLM-Backend
- Skill `assist/haushalt-manager` — Routinika-Integration
- `tools/module-installer/module_installer.py` — Modul-Anbindung

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.2.0 | 2026-11-27 | Multi-Kalender-Silos (`calendars` + additive `events`-Migration), Silo-Operationen (`mirror`, `sync-mirrors`, `transfer`, `clone`), idempotenter TerminPilot-/ICS-Import (`import-ics`), erweiterte Zeitraumabfragen (`day`, `year`, `range`, `--json`) sowie Berichts- & Kalenderblatt-Generator (`html`, `pdf`, `md`, `txt`, `ics`) |
| 0.1.1 | 2026-11-22 | Sprachhinweis korrigiert |
| 0.1.0 | 2026-06-22 | Erstanlage — Flag-3-Logik, local-Backend, ICS-Export |
