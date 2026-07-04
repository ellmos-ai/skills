# Skill Conventions -- Frontmatter-Spezifikation

Jede SKILL.md in dieser Bibliothek folgt einem standardisierten YAML-Frontmatter.
Die Felder sind so gestaltet, dass jeder Skill seine Herkunft, Abhaengigkeiten und
Kompatibilitaet **in sich selbst** traegt. Externe Systeme koennen diese Felder
auslesen, um Skills zu katalogisieren, zu synchronisieren oder zu validieren.

---

## Pflichtfelder

```yaml
---
name: skill-name                    # Eindeutiger Identifier (kebab-case)
version: 1.0.0                      # Semantic Versioning (MAJOR.MINOR.PATCH)
type: skill                         # skill | agent | expert | service | protocol | tool | assist
author: Name                        # Ersteller (Person oder KI-Partner)
created: 2026-03-12                 # Erstelldatum (ISO 8601)
updated: 2026-03-12                 # Letzte Aenderung (ISO 8601)
description: >
  Kurze Beschreibung der Faehigkeit.
---
```

## Kompatibilitaets-Felder

Diese Felder definieren, ob ein Skill eigenstaendig funktioniert und mit welchen
Systemen er kompatibel ist.

```yaml
standalone: true                    # true = funktioniert ohne externes System
                                    # false = braucht BACH oder anderes System

anthropic_compatible: true          # Entspricht dem Anthropic Skills-Standard
                                    # (SKILL.md + optionale scripts/)

bach_compatible: true               # Kann in BACH geladen/genutzt werden
bach_origin: false                  # Stammt aus dem BACH-System
```

### Entscheidungsmatrix

| standalone | bach_origin | Bedeutung |
|-----------|-------------|-----------|
| `true` | `false` | Eigenstaendiger Skill, nie in BACH gewesen |
| `true` | `true` | Aus BACH exportiert, standalone-faehig gemacht |
| `false` | `true` | BACH-interner Skill (braucht BACH-Runtime) |
| `false` | `false` | Abhaengig von anderem System (nicht BACH) |

### Woran erkennt man BACH-Abhaengigkeit im Skill-Body?

Typische Indikatoren fuer BACH-gebundene Skills:
- `from bach_api import ...` in Scripts
- `bach <command>` Aufrufe in Anweisungen
- Referenzen auf `bach.db`, `hub/`, `core/`
- `orchestrates:` Feld mit BACH-Agenten/Experten

Ein `standalone: true` Skill darf KEINE dieser Abhaengigkeiten haben,
es sei denn sie sind als optional markiert (Fallback-Logik).

---

## Typ `assist` -- persoenliche Assistenz-Skills

`type: assist` kennzeichnet persoenliche Assistenz-Skills (Kalender, Medizin-Daten,
Tageszeitung, Transkription, Voice, ...), die typischerweise lokal-first arbeiten,
optional mehrere Backends via Presence-Check und/oder `assist/prefs.json` waehlen
und haeufig personenbezogene Daten beruehren. Eigenes Schema: `schemas/assist-v1.schema.json`
(analog `agent-v1`/`workflow-v1`/`prompt-v1`, `type: "assist"` const).

**Privacy-Sonderfall:** Die konkreten `assist`-Skills sind ueber `skills/assist/`
in `.gitignore` als privat/untracked markiert und werden von `registry-generate`
NICHT erfasst (Registry bleibt git-tracked-only, Privacy-Gate unveraendert).
Zur lokalen Qualitaetspruefung kann `versionctl validate --include-untracked`
auch diese Skills mitpruefen, ohne sie in die Registry aufzunehmen.

---

## Provenance-Felder (Herkunfts-Tracking)

```yaml
provenance:
  origin: "bach"                          # Quelle: bach | custom | community | anthropic
  origin_path: "system/agents/steuer/"    # Pfad im Quellsystem
  origin_version: "1.2.0"                # Version zum Zeitpunkt des Exports
  origin_repo: "github.com/ellmos-ai/bach"  # Optional: Git-Repo der Quelle
  last_sync_from_origin: "2026-03-12"    # Letzter Import von der Quelle hierher
  last_sync_to_origin: null              # Letzter Rueckfluss von hier zur Quelle
  local_changes_since_sync: false        # true wenn lokal geaendert seit letztem Sync
```

### Sync-Richtungen

```
BACH (Quelle)  ──export──>  .SKILLS (Bibliothek)  ──publish──>  GitHub
                <──import──                        <──pull────
```

- **Export (BACH -> .SKILLS):** `last_sync_from_origin` wird aktualisiert
- **Import (.SKILLS -> BACH):** `last_sync_to_origin` wird aktualisiert
- **Lokale Aenderung:** `local_changes_since_sync: true` + `updated` Datum

---

## Optionale Felder

```yaml
# Abhaengigkeiten (was braucht der Skill?)
dependencies:
  tools: []                     # Python-Tools / Scripts
  services: []                  # Externe Services / APIs
  protocols: []                 # Workflow-Protokolle
  python: []                    # pip-Pakete (z.B. ["requests", "beautifulsoup4"])

# Kategorisierung
category: productivity          # Themen-Kategorie (Ordnername)
tags: [automation, cli]         # Freitext-Tags fuer Suche
language: de                    # Sprache des Skills (de | en | multi)

# Fuer Agenten/Experten
orchestrates:
  experts: []                   # Untergeordnete Experten
  services: []                  # Genutzte Services

# Status
status: active                  # active | draft | deprecated | archived

# BACH-spezifisch (nur wenn bach_compatible: true)
bach_integration:
  handler: "steuer"             # Zugehoeriger BACH-Handler
  db_tables: ["steuer_*"]       # Genutzte DB-Tabellen
  hooks: ["after_task_done"]    # Genutzte Hook-Events
```

---

## Datei-Layout eines Skills

```
skills/<kategorie>/<skill-name>/
  SKILL.md                      # Pflicht: Definition + Frontmatter
  scripts/                      # Optional: ausfuehrbarer Code
    main.py                     #   Hauptscript
    utils.py                    #   Hilfsfunktionen
  references/                   # Optional: Referenzdokumente
    anleitung.md                #   Detaillierte Anleitung
  tests/                        # Optional: Tests
    test_main.py
```

### Flat-Regel (< 5 Dateien)

Wenn ein Skill weniger als 5 Dateien hat, liegen alle flat im Root:

```
skills/<kategorie>/<skill-name>/
  SKILL.md
  main.py
  config.json
```

---

## Versions-Konvention

- **MAJOR:** Inkompatible Aenderungen (Frontmatter-Felder umbenannt, API gebrochen)
- **MINOR:** Neue Funktionalitaet (neues Script, neue Sektion in SKILL.md)
- **PATCH:** Bugfixes, Tippfehler, kleine Verbesserungen

Bei Sync mit BACH: Die Version in `.SKILLS` kann von der BACH-Version abweichen.
Das `provenance.origin_version` Feld zeigt den BACH-Stand beim letzten Sync.

---

## Changelog im Skill

Jede SKILL.md sollte am Ende einen Changelog-Abschnitt haben:

```markdown
## Changelog

### 1.1.0 (2026-03-12)
- Neues Script fuer automatischen Export

### 1.0.0 (2026-03-01)
- Initialer Export aus BACH v3.8.0
```

---

## Mehrsprachigkeit

Skills können in mehreren Sprachen vorliegen. Unterstützte Sprachen:

| Code | Sprache | Ausbaustufe | Datei-Suffix |
|------|---------|-------------|--------------|
| `de` | Deutsch | 1 (Primär) | `SKILL.md` (kein Suffix) |
| `en` | Englisch | 1 | `SKILL.en.md` |
| `es` | Spanisch | 2 | `SKILL.es.md` |
| `zh` | Chinesisch | 2 | `SKILL.zh.md` |
| `ja` | Japanisch | 2 | `SKILL.ja.md` |
| `ru` | Russisch | 2 | `SKILL.ru.md` |

### Sprach-Feld

```yaml
language: de            # de, en, es, zh, ja, ru, multi
```

### Umsetzungsmodelle

| Modell | Struktur | Wann verwenden |
|--------|----------|----------------|
| **Einsprachig** | `SKILL.md` (eine Sprache) | Standard, einfachste Variante |
| **Parallel** | `SKILL.md` (DE) + `SKILL.{code}.md` | Wenn mehrere Sprachen gepflegt werden |
| **Multi** | `SKILL.md` mit `language: multi` + Sektionen | Kurze Skills, wo beides passt |

### Paralleles Modell (empfohlen)

```
skills/<kategorie>/<skill-name>/
  SKILL.md          # Primär-Version (Deutsch)
  SKILL.en.md       # Englische Version
  SKILL.es.md       # Spanische Version (optional, Ausbaustufe 2)
  SKILL.zh.md       # Chinesische Version (optional, Ausbaustufe 2)
  SKILL.ja.md       # Japanische Version (optional, Ausbaustufe 2)
  SKILL.ru.md       # Russische Version (optional, Ausbaustufe 2)
  scripts/          # Scripts bleiben sprachneutral (Code ist englisch)
```

**Regeln:**
- Frontmatter-Felder sind identisch (name, version, tags, provenance, etc.)
- Nur `language:` und `description:` unterscheiden sich
- Scripts/Code werden NICHT dupliziert -- Code ist sprachneutral (englisch)
- Docstrings in Scripts bleiben auf Englisch
- Die `SKILL.md` (ohne Suffix) ist immer die Primärsprache (Deutsch)
- Ausbaustufe 2 Dateien werden nur bei Bedarf erstellt (kein Vorab-Stub)

### BACH-DB als Quelle

BACH enthaelt ~1870 Skills (942 DE, 927 EN) in der `skills`-Tabelle.
Beim Export aus BACH koennen beide Sprachversionen uebernommen werden:

```bash
# BACH Skill-Export mit Sprachvarianten
python skill_export.py --skill <name> --format anthropic --language de
python skill_export.py --skill <name> --format anthropic --language en
```

### catalog.py Unterstuetzung

`catalog.py list` zeigt die Sprache jedes Skills an.
`catalog.py list --language en` filtert nach Sprache.
