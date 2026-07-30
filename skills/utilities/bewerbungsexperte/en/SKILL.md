---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: Specialist for the entire job application process. Analyzes job postings, optimizes profiles (LinkedIn/CV), and generates tailored cover letters. Generates ASCII CVs from a SQLite database and folder structure. cv_generator.py is ported standalone -- no BACH runtime required.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: en
status: active
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **English** — Official English version of `bewerbungsexperte`.


<img src="banner.png" width="100%" alt="bewerbungsexperte banner">
# BEWERBUNGSEXPERTE v1.1 (English)

> Your strategic partner for the next career step.

## ACTIVATION

```bash
# Example CV without database access (English)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# Generate CV from SQLite database (English)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# Save CV to file (English)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# With folder scan (English)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## SERVICE CATALOG

### 1. CV Generation (`cv_generator.py`)
- **Personal Data:** Read from `assistant_user_profile` table (key/value)
- **Work Experience:** Scan employer folder (certificates, contracts)
- **Education:** Scan degrees/qualifications folder
- **Continuing Education:** Scan certificates folder
- **References:** From `contacts` table (category='beruflich')
- **Dry-Run:** Without database -- sample data for testing

### 2. Job Diagnosis
- **Keyword Matching:** Alignment of CV with job requirements (ATS-Safe)
- **Company Check:** Research on corporate culture and benefits

### 3. Application Documents Service
- **CV Tuning:** Structuring and highlighting experience
- **Cover Letter:** Creation of customized, compelling letters
- **Portfolio:** Advice on work samples and references

## DATABASE TABLES (optional)

`cv_generator.py` reads from these tables if present:

- `assistant_user_profile` (key TEXT, value TEXT) — Personal data
  - Fields: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — References

Missing tables are ignored (empty sections in CV).

## FOLDER STRUCTURE (for --career-path etc.)

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```

## CLI OPTIONS

```
--db <pfad>           Path to SQLite database (required without --dry-run)
--output, -o          Output file (otherwise stdout)
--career-path         Path to employer folder
--education-path      Path to degrees/education folder
--certs-path          Path to certificates/trainings folder
--dry-run             Sample CV without database access
```

## WORKFLOW: CV GENERATION

1. **Preparation**
   - Provide SQLite DB (BACH DB or your own)
   - Create folder structure with documents (optional)

2. **Test without DB**
   - `python cv_generator.py --dry-run` -- checks if tool works

3. **Generation**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - Review output and adjust if necessary

4. **Export**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## DEPENDENCIES

Python Stdlib only: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
No pip install required, no BACH runtime import.

## CHANGELOG

### 1.1.0 (2026-06-22)
- Ported standalone from BACH v1.0.0
- `--db <pfad>` instead of hardcoded origin DB path
- Added `--dry-run` mode
- Removed `--scan-folders` (required BACH user_data_folders table)
- Neutralized footer text
- Verified BACH runtime independence

### 1.0.0 (2026-01-25, BACH internal)
- Initial version in BACH system/agents/_experts/bewerbungsexperte/

---
Status: ACTIVE
Domain: Career Consulting
