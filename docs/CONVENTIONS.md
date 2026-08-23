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
visibility: public                  # public | public potential | private profile | private-only
---
```

### `visibility` -- wie weit darf der Skill nach aussen?

**Fail-closed:** Fehlt das Feld, gilt der Skill als **privat** (`DEFAULT_VISIBILITY` in
`build_public_registry.py`). Ein vergessenes Feld veroeffentlicht also nichts -- es haelt
zurueck. Deshalb ist das Feld Pflicht: Jeder Skill beantwortet die Frage selbst, statt sie
offenzulassen.

| Wert | Bedeutung | Im oeffentlichen Repo? |
|---|---|---|
| `public` | Nutzerneutral und freigegeben | ja, getrackt |
| `public potential` | Koennte spaeter veroeffentlicht werden, noch nicht entschieden | nein |
| `private profile` | Persoenliche Daten, Vorlagen, Vorgaben -- nie | nein |
| `private-only` | Zweck/Implementierung host- oder systemgebunden -- nie als solcher | nein |

**Die Deklaration muss zum Git-Zustand passen.** `visibility` steuert die Listung (Registry,
`SKILLS-MAP.md`, Pages); die `.gitignore` plus `FORBIDDEN_PUBLIC_SKILL_DIRECTORIES` in
`testing/privacy_gate.py` steuern, ob die Datei ueberhaupt im oeffentlichen Repo liegt.
Widersprechen sich beide, luegt eine Seite -- `privacy_gate.py` blockiert dann den Push:

* *privat deklariert, aber getrackt* -- oeffentlich lesbar, obwohl nirgends gelistet
  (die gefaehrliche Richtung: eine Veroeffentlichung, die keine Liste je zeigen wuerde)
* *`public`/undeklariert, aber ausgeschlossen* -- der Katalog verspricht etwas, das im
  oeffentlichen Repo nicht liegt

Statusbegriffe und die Paar-Tabelle "oeffentlicher Kern <-> privater Rest" fuehrt
`SKILLS-MAP-PRIVATE.md` (nicht im oeffentlichen Repo).

### `third_party` und `license` -- fremdes Material

Beide Felder sind **freiwillig** und wirken nur, wenn sie gesetzt sind. Wer sie
weglaesst, hat einen eigenen Skill unter der Repo-Lizenz (MIT) -- das ist der
Normalfall und braucht keine Erklaerung.

```yaml
third_party: true                   # nur bei fremdem Material
license: MIT                        # SPDX-Kennung; bei third_party Pflicht
upstream: https://github.com/…      # Quelle; bei third_party Pflicht
```

**`license` darf jeder Skill fuehren**, auch ein eigener -- etwa wenn er
bewusst unter einer anderen Lizenz stehen soll als das Repo. Ohne Feld gilt die
Repo-Lizenz. Wenn gesetzt, wird die **Form** geprueft (SPDX-Kennung), nicht die
Erlaubnis: `MIT`, `Apache-2.0`, `GPL-3.0-or-later`, auch `MIT OR Apache-2.0`.
Diese Formpruefung existiert, weil `provenance.origin` ohne sie auf sieben
Schreibweisen inklusive Freitext angewachsen ist.

**`third_party: true` hat dagegen Konsequenzen.** Der Skill muss dann in
`skills/third-party/` liegen, eine Lizenz aus der Allow-Liste fuehren, die
Upstream-`LICENSE`-Datei danebenlegen und auf seine Quelle zeigen.
`testing/privacy_gate.py` prueft das und blockiert Abweichungen -- in beide
Richtungen, denn Ordner und Flag muessen uebereinstimmen.

Im Areal gilt ein **eigener, kleinerer Pflichtfeld-Satz** (`name`,
`description`, `third_party`, `license`, `upstream`): Die neun Hausfelder sind
unsere Konvention, kein externer Standard -- kein fremder Skill fuehrt sie.
Details, Lizenz-Allow-Liste und der Umgang mit Treffern des Content-Scans:
`skills/third-party/README.md`.

Fremdmaterial, das wir nur **nutzen und gut finden**, gehoert nicht hierher,
sondern nach `skills/_reference/` (gitignored, lebt in der OneDrive-Bibliothek).
Etwas zu benutzen und etwas weiterzugeben sind verschiedene Fragen; nur die
zweite braucht eine Erlaubnis.

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

## Typ `assist` -- Assistenz-Skills

`type: assist` kennzeichnet methodische Assistenz-Skills, etwa für Kalender,
Notizen, Bestandsübersichten oder Sprachworkflows. Ein öffentlicher Assist-Skill
muss ohne ein bestimmtes Benutzerkonto, lokales Programm, persönliches Profil
oder private Datenbank nutzbar sein.

### Verbindliche Public/Private-Trennung

| Ebene | Ablage | Darf öffentlich sein? |
|---|---|---|
| Nutzerneutraler Kern | `skills/<kategorie>/<name>/SKILL*.md` und neutrale Assets | Ja |
| Generischer optionaler Adapter | Öffentlich nur bei dokumentierter, frei verfügbarer Schnittstelle | Nach Prüfung |
| App-/Host-spezifischer Adapter | Getrenntes privates Repository | Nein |
| Persönliches Profil oder Vorlage | Getrenntes privates Repository | Nein |
| Konten, lokale Pfade, Datenbanken und Echtdaten | Außerhalb dieses Repositories | Nein |

Öffentliche Kerne dürfen private Erweiterungen als Konzept erwähnen, aber keine
Namen persönlicher Profile, absoluten Benutzerpfade, Hostnamen, Kontodaten oder
private App-Verträge enthalten. Ohne privates Profil müssen sie ausschließlich
mit den im aktuellen Auftrag bereitgestellten Daten funktionieren.

Für `foerderplaner` gilt dieselbe Trennung: Der öffentliche Skill plant Unterricht
und Förderung. Allgemeine Berichtserstellung ist ein eigener öffentlicher Kern
(`report-forge`). Persönliche Förderbericht-Vorlagen und Profile bleiben privat.

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

## Mehrsprachigkeit [G 2026-07-30]

Skills können in mehreren Sprachen vorliegen. Die Sprachen sind in drei
aufeinander aufbauende Sets organisiert:

### Sprachsets

| Set | Sprachen | Abdeckung (Weltbevölkerung) | Status |
|-----|----------|----------------------------|--------|
| **Core Set** | DE, EN | ~20% | ✅ Pflicht für jeden Skill |
| **Full Set** | Core + ES, ZH, JA, RU | ~40–45% | ✅ Aktueller Standard |
| **World Set** | Full + FR, HI, AR, BN, PT | ~55–60% | 🟢 Ausbau beschlossen [U 2026-08-12] — Zielbild, schrittweise |

### Sprachkatalog

| Code | Sprache | Set | Datei-Suffix | Sprecher (gesamt) |
|------|---------|-----|--------------|-------------------|
| `de` | Deutsch | Core | `SKILL.md` (kein Suffix) | ~95 Mio. |
| `en` | Englisch | Core | `SKILL.en.md` | ~1.500 Mio. |
| `es` | Spanisch | Full | `SKILL.es.md` | ~555 Mio. |
| `zh` | Chinesisch | Full | `SKILL.zh.md` | ~1.150 Mio. |
| `ja` | Japanisch | Full | `SKILL.ja.md` | ~125 Mio. |
| `ru` | Russisch | Full | `SKILL.ru.md` | ~250 Mio. |
| `fr` | Französisch | World | `SKILL.fr.md` | ~310 Mio. |
| `hi` | Hindi | World | `SKILL.hi.md` | ~600 Mio. |
| `ar` | Arabisch | World | `SKILL.ar.md` | ~400 Mio. |
| `bn` | Bengali | World | `SKILL.bn.md` | ~270 Mio. |
| `pt` | Portugiesisch | World | `SKILL.pt.md` | ~260 Mio. |

**Aktueller Zielumfang:** Alle Skills werden auf **Full Set** gepflegt.
Der World-Ausbaubeschluss ist erteilt [U 2026-08-12]: World-Set-Sprachen werden
**nach und nach** vollständig übersetzt — bevorzugt als Leerlauf-Sprachzug
(ein Objekt × eine Sprache je Leerlauf). Die Sets gelten über Skills hinaus
als Sprachstufen für Repos, Module, Bundles und Stacks in `.AI` und
`.SOFTWARE` (systemweite Regel: P-006 „Sprachstufen" im Policy-Register).

### Sprach-Feld

```yaml
language: de            # de, en, es, zh, ja, ru, fr, hi, ar, bn, pt, multi
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
  SKILL.md          # Primär-Version (Deutsch, Core)
  SKILL.en.md       # Englische Version (Core)
  SKILL.es.md       # Spanische Version (Full)
  SKILL.zh.md       # Chinesische Version (Full)
  SKILL.ja.md       # Japanische Version (Full)
  SKILL.ru.md       # Russische Version (Full)
  SKILL.fr.md       # Französische Version (World, nur bei Ausbau)
  scripts/          # Scripts bleiben sprachneutral (Code ist englisch)
```

**Regeln:**
- Frontmatter-Felder sind identisch (name, version, tags, provenance, etc.)
- Nur `language:` und `description:` unterscheiden sich
- Scripts/Code werden NICHT dupliziert -- Code ist sprachneutral (englisch)
- Docstrings in Scripts bleiben auf Englisch
- Die `SKILL.md` (ohne Suffix) ist immer die Primärsprache (Deutsch)
- Core- und Full-Set-Dateien werden aktiv gepflegt
- World-Set-Dateien werden nur bei explizitem Ausbaubeschluss erstellt (Stubs erlaubt)

### BACH-DB als Quelle

BACH enthaelt ~1870 Skills (942 DE, 927 EN) in der `skills`-Tabelle.
Beim Export aus BACH koennen beide Sprachversionen uebernommen werden:

```bash
# BACH Skill-Export mit Sprachvarianten
python skill_export.py --skill <name> --format anthropic --language de
python skill_export.py --skill <name> --format anthropic --language en
```

### Öffentlicher Katalog

`python build_public_registry.py` erzeugt den reduzierten öffentlichen
Discovery-Index `registry/components.json`. Er enthält ausschließlich die für
Installation und Auffindbarkeit notwendigen Felder. Interne Bewertungen,
Ownership-, Privacy-, Branch- und Wartungsdaten gehören in die vollständige
Registry des getrennten No-Push-Repositories.

Die nicht-zirkuläre Quellenautorität dafür ist
`registry/public-skill-files.json`: In einem Git-Checkout wird sie aus den
getrackten öffentlichen Skill- und Sprachdateien erzeugt und mit `--check`
gegen Git geprüft. In gitlosen Archiven und angereicherten Plan-D-Projektionen
ist ausschließlich diese versionierte Dateiliste maßgeblich. Physisch daneben
liegende interne Zusatzskills werden weder veröffentlicht noch gelöscht;
fehlende, unsichere oder veraltete Manifest-Einträge führen zu einem
fail-closed Fehler.

`python build_skills_map.py` erzeugt daraus die öffentliche `SKILLS-MAP.md`.

---

## Banner (visuelle Identitaet)

Jeder Skill erhält schrittweise ein eigenes Banner (Rollout seit 2026-07-23,
beginnend mit den Featured-Skills aus dem README):

- **Datei:** `banner.png` direkt im Skill-Ordner (Ausnahme Kollektionen: ein Banner
  pro Kategorie-Ordner, z. B. `skills/therapy/banner.png`).
- **Format:** 1200x300 px, PNG, möglichst < 400 KB.
- **Design-Familie:** angelehnt an das Repo-Banner (`assets/banner_v2.svg`) --
  heller Off-White-Grund, Paint-Splatter-Akzente, kräftiger Farbverlauf im
  Skill-Namen, dezentes thematisches Motiv pro Skill.
- **Einbettung:** erste Zeile nach dem YAML-Frontmatter in allen direkt im
  Skill-Ordner liegenden `SKILL*.md`-Sprachfassungen:
  `<img src="banner.png" width="100%" alt="<skill-name> banner">`
  Wenn kein `banner.png` existiert, wird keine leere Referenz eingefügt.
- Banner sind rein dekorativ: keine inhaltstragenden Informationen, damit
  Runtimes, die nur Text lesen, nichts verlieren.
