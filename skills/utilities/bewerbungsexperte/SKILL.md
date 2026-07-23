---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: >
  Spezialist fuer den gesamten Bewerbungsprozess. Analysiert Stellenanzeigen,
  optimiert Profile (LinkedIn/CV) und generiert massgeschneiderte Anschreiben.
  Generiert ASCII-Lebenslaeufe aus einer SQLite-Datenbank und Ordnerstruktur.
  cv_generator.py ist standalone portiert -- keine BACH-Runtime noetig.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: de
status: active

dependencies:
  tools: [cv_generator.py]
  services: []
  protocols: []
  python: [sqlite3, pathlib, argparse, re]

provenance:
  origin: "bach"
  origin_path: "system/agents/_experts/bewerbungsexperte/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: true
---
# BEWERBUNGSEXPERTE v1.1

> Dein strategischer Partner fuer den naechsten Karriereschritt.

## AKTIVIERUNG

```bash
# Beispiel-CV ohne Datenbankzugriff
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# CV aus SQLite-Datenbank generieren
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# CV in Datei speichern
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# Mit Ordner-Scan
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## LEISTUNGSKATALOG

### 1. CV-Generierung (`cv_generator.py`)
- **Persoenliche Daten:** Aus `assistant_user_profile`-Tabelle lesen (key/value)
- **Berufserfahrung:** Arbeitgeber-Ordner scannen (Zeugnisse, Vertraege)
- **Ausbildung:** Abschluesse-Ordner scannen
- **Fortbildungen:** Zertifikate-Ordner scannen
- **Referenzen:** Aus `contacts`-Tabelle (category='beruflich')
- **Dry-Run:** Ohne Datenbank -- Beispieldaten fuer Tests

### 2. Stellendiagnose
- **Keyword-Matching:** Abgleich von CV mit Job-Requirements (ATS-Safe)
- **Unternehmens-Check:** Recherche zu Firmenkultur und Benefits

### 3. Unterlagen-Service
- **CV-Tuning:** Strukturierung und Pointierung von Erfahrungen
- **Anschreiben:** Erstellung von individuellen, ueberzeugenden Briefen
- **Portfolio:** Beratung zu Arbeitsproben und Referenzen

## DATENBANK-TABELLEN (optional)

`cv_generator.py` liest aus diesen Tabellen, wenn vorhanden:

- `assistant_user_profile` (key TEXT, value TEXT) — Persoenliche Daten
  - Felder: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — Referenzen

Fehlende Tabellen werden ignoriert (leere Sektionen im CV).

## ORDNERSTRUKTUR (fuer --career-path etc.)

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

## CLI-OPTIONEN

```
--db <pfad>           Pfad zur SQLite-Datenbank (Pflicht ohne --dry-run)
--output, -o          Ausgabedatei (ansonsten stdout)
--career-path         Pfad zum Arbeitgeber-Ordner
--education-path      Pfad zum Abschluesse-Ordner
--certs-path          Pfad zum Fortbildungen-Ordner
--dry-run             Beispiel-CV ohne Datenbankzugriff
```

## WORKFLOW: CV-GENERIERUNG

1. **Vorbereitung**
   - SQLite-DB bereitstellen (BACH-DB oder eigene)
   - Ordnerstruktur mit Dokumenten anlegen (optional)

2. **Test ohne DB**
   - `python cv_generator.py --dry-run` -- prueft ob Tool funktioniert

3. **Generierung**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - Ausgabe pruefen und ggf. anpassen

4. **Export**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## ABHÄNGIGKEITEN

Nur Python-Stdlib: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
Kein pip-Install noetig, kein BACH-Runtime-Import.

## ÄNDERUNGSLOG

### 1.1.0 (2026-06-22)
- Standalone portiert aus BACH v1.0.0
- `--db <pfad>` statt hardcodiertem Origin-DB-Pfad
- `--dry-run`-Modus hinzugefuegt
- `--scan-folders` entfernt (erforderte BACH user_data_folders-Tabelle)
- Footer-Text neutralisiert
- BACH-Runtime-Unabhaengigkeit verifiziert

### 1.0.0 (2026-01-25, BACH-intern)
- Initiale Version in BACH system/agents/_experts/bewerbungsexperte/

---
Status: AKTIV
Domain: Karriereberatung
