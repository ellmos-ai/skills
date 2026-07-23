---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: >
  Local, private capture of medical data: diagnoses, symptom histories
  and examination plans. No BACH origin — custom design with its own
  SQLite store. Strictly local, no cloud transfer.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags:
  - medizin
  - diagnose
  - symptome
  - gesundheit
  - privat
  - lokal
language: en
status: stable

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: eigenentwurf
  origin_path: ""
  origin_version: ""
  origin_repo: ""
  origin_license: MIT
  last_sync_from_origin: ""
  notes: >
    Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes
    Implementierungs-Vorbild im Ökosystem gefunden.
---

## Purpose

Securely and locally capture personal medical data: diagnoses (ICD-10 code
optional), symptom histories with date series and examination plans. All
data stays exclusively local in `medizin-daten/store.db`.

The skill does not replace medical consultation and makes no medical
statements — it is a structured notebook for personal health data.

---

## Triggers

| Phrase | Action |
|---|---|
| "Record a diagnosis" | Create new diagnosis |
| "Add diagnosis [name]" | Create named diagnosis |
| "Symptom history" | Record today's symptoms |
| "Record symptom [name]" | Log a single symptom |
| "Examination plan" | Show upcoming appointments/examinations |
| "Add appointment" | Enter examination appointment |
| "Show my diagnoses" | Output diagnosis list |

---

## Workflow

1. **Detect mode**: diagnosis / symptom / examination plan
2. **Structure input**: date, name, notes, optional ICD-10 code
3. **Save**: into `store.db` (local, no network access)
4. **Output**: readable summary for LLM context

---

## CLI Entry Point

```bash
# Create diagnosis
python medizin_daten_core.py add-diagnosis "Hypertension" [--icd I10] [--note "note"]

# List diagnoses
python medizin_daten_core.py diagnoses

# Record symptom
python medizin_daten_core.py add-symptom "Headache" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptom history for a name
python medizin_daten_core.py symptom-history "Headache" [--limit 30]

# Plan examination
python medizin_daten_core.py add-exam "Blood count" [--date 2026-07-01] [--note "fasting"]

# Upcoming examinations
python medizin_daten_core.py exams [--upcoming]

# Alternative store (e.g. for tests)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## Store

| Property | Value |
|---|---|
| Type | SQLite |
| Path (default) | `skills/assist/medizin-daten/store.db` |
| Override | `--store <path>` or env `MEDIZIN_STORE` |
| Tables | `diagnoses`, `symptoms`, `examination_plans` |

### Schema

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (short: 8 hex)
    name        TEXT NOT NULL,        -- name (e.g. "Hypertension")
    icd_code    TEXT,                 -- ICD-10 code optional (e.g. "I10")
    onset_date  TEXT,                 -- onset (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- free-text note
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    name         TEXT NOT NULL,       -- name (e.g. "Headache")
    severity     INTEGER,             -- 1–10 scale (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 timestamp
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    exam_name    TEXT NOT NULL,       -- examination name
    planned_date TEXT,                -- planned date (ISO-8601)
    done_date    TEXT,                -- completed on (NULL = pending)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## Attitude

- No medical recommendations, no diagnosis by the skill.
- ICD-10 codes are stored as free text — no validation against an external database.
- Severity scale 1–10 is user-subjective.
- Missing values (date, severity) are always allowed — the notebook principle applies.

---

## Privacy (Privacy Gate)

> **WARNING: Medical data is particularly sensitive.**

- `store.db` contains highly sensitive health data — **never commit to Git**.
- **No network access** — all operations run entirely locally.
- **No sharing** with external services, no sync with cloud backends.
- Backup recommendation: encrypted local backup (e.g. `age`/`gpg`).
- The skill checks at startup whether `store.db` is outside the local file system
  and issues a warning if the path is in a sync folder (OneDrive etc.).
- `~/.gitignore_global` or local `.gitignore` should exclude `store.db`.

---

## Related Resources

- Skill `assist/gesundheit` — general health assistance (not medical data)
- MediPlaner (`tools/module-installer` → `mediplaner`) — medication management (separate programme)

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-06-22 | Initial creation — custom design, privacy gate, 3-table schema |
