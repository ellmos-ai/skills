# Portierungs-Checklisten

Checklisten fuer die Aufnahme von Skills in die Bibliothek aus verschiedenen Quellen.

---

## Checkliste A: BACH-Skill portieren

### Vorbereitung

- [ ] **Skill in BACH identifizieren** -- Pfad, Typ, Version, Abhaengigkeiten
- [ ] **BACH-DB pruefen** -- `SELECT * FROM skills WHERE name LIKE '%<name>%'`
      Gibt es DE- und EN-Versionen? Beide exportieren
- [ ] **Standalone-Eignung pruefen** -- Braucht der Skill BACH-Runtime?
      - `bach_api`-Imports? → Nicht standalone-faehig (oder optional machen)
      - `bach.db`-Zugriff? → Nicht standalone-faehig
      - Nur Markdown/Protokoll? → Standalone-faehig
      - Python-Tool ohne BACH-Imports? → Standalone-faehig
- [ ] **Abhaengigkeiten analysieren** -- BACH `skill_export.py` DependencyResolver nutzen
      oder manuell: AST-Imports in .py-Dateien pruefen
- [ ] **Kategorie festlegen** -- Existierende Kategorie oder neue anlegen

### Export / Kopie

- [ ] **BACH-Export nutzen (wenn moeglich)**:
      `python skill_export.py --skill <name> --format anthropic --output /c/Users/lukas/OneDrive/.SKILLS/skills/<kategorie>/`
- [ ] **Oder manuell kopieren** -- SKILL.md + Scripts + Referenzen

### Bereinigung (KRITISCH)

- [ ] **Frontmatter ersetzen** -- BACH-Header → .SKILLS-Standard (siehe CONVENTIONS.md)
      - `type:` anpassen (therapie-skill → skill, boss-agent → agent, etc.)
      - `standalone: true` setzen
      - `bach_origin: true` setzen
      - `bach_compatible:` setzen (true wenn rueckwaerts kompatibel)
      - `provenance:`-Block mit origin_path, origin_version, last_sync_from_origin
- [ ] **BACH-spezifische Felder entfernen:**
      - `parent_agent:` entfernen
      - `expert:` entfernen
      - `orchestrates:` entfernen (oder unter `bach_integration:` dokumentieren)
- [ ] **BACH-CLI-Befehle entfernen:**
      - `bach psycho session start` → entfernen
      - `bach task add` → entfernen
      - `bach skills create` → entfernen
      - `bach tools search` → entfernen
      - Ganze "Anwendung im BACH-Kontext"-Sektionen entfernen
- [ ] **BACH-Wiki-Referenzen entfernen:**
      - `Wiki: psychotherapie/...` → entfernen
      - `Wiki: methoden/...` → entfernen
      - Interne Skill-Referenzen auf Standalone-Pfade anpassen
- [ ] **BACH-Bezeichnungen ersetzen:**
      - "BACH darf" → "Ein KI-Assistent darf"
      - "BACH bietet" → "Dieser Skill bietet"
      - "Registriert als BACH Tool" → entfernen
- [ ] **Python-Code bereinigen:**
      - `from tools.<x> import` → `from <x> import` (relativer Import)
      - `from bach_api import` → entfernen oder als optional markieren
      - `from core.` / `from hub.` → entfernen
      - Hardcodierte Pfade (`C:\Users\lukas\...`) → relative Pfade
      - Emojis in print-Statements → ASCII-Alternative oder entfernen
- [ ] **Nutzerspezifisches entfernen:**
      - Benutzernamen, Pfade, IP-Adressen, API-Keys
      - Referenzen auf lokale Konfigurationen

### Zweisprachigkeit

- [ ] **DE-Version erstellen** -- Primaer-SKILL.md (Deutsch)
- [ ] **EN-Version pruefen** -- Existiert in BACH-DB (`language='en'`)?
      Falls ja: Als SKILL.en.md exportieren und bereinigen
      Falls nein: Optional spaeter uebersetzen lassen
- [ ] **language: de** (oder en, multi) im Frontmatter setzen

### Qualitaetssicherung

- [ ] **Grep-Pruefung** -- Keine verbotenen Muster:
      ```
      rg -i "bach psycho|bach task|bach skills|parent_agent:|expert:|from tools\.|from bach_api|from core\.|from hub\." SKILL.md scripts/
      rg "C:\\\\Users|/c/Users/lukas" SKILL.md scripts/
      ```
- [ ] **Python-Code testen** (wenn vorhanden):
      - `python -c "import <module>"` -- Importiert ohne Fehler?
      - Selbst-Tests (`python <script>.py`) laufen durch?
- [ ] **SKILL.md validieren** -- `python catalog.py info <skill-name>`
- [ ] **Changelog eintragen** -- `### 1.0.0 (YYYY-MM-DD) - Portiert aus BACH v<version>`

### Abschluss

- [ ] **catalog.py sync-status** -- Skill erscheint in der Liste
- [ ] **Git add + commit** -- Skill committen (gitignore fuer private Skills beachten)
- [ ] **Provenance dokumentiert** -- origin_path, origin_version gesetzt

---

## Checkliste B: Neuen Skill erstellen (kein BACH-Ursprung)

### Vorbereitung

- [ ] **Duplikat-Check** -- `python catalog.py list` -- Gibt es den Skill schon?
- [ ] **Kategorie waehlen** -- Existierende oder neue Kategorie
- [ ] **Skill-Typ festlegen** -- skill | agent | tool | protocol | service | expert
- [ ] **Abhaengigkeiten identifizieren** -- Python-Pakete, externe Services

### Erstellung

- [ ] **Ordner anlegen** -- `skills/<kategorie>/<skill-name>/`
- [ ] **SKILL.md erstellen** -- Vorlage: `skills/_templates/TEMPLATE_SKILL.md`
      Oder: `python catalog.py create <kategorie>/<skill-name> --type <typ>`
- [ ] **Frontmatter ausfuellen:**
      - `standalone: true`
      - `bach_origin: false`
      - `bach_compatible: false` (oder true wenn BACH-kompatibel gestaltet)
      - `provenance: origin: "custom"`
- [ ] **Scripts erstellen** (wenn noetig) -- Flat-Regel beachten (< 5 Dateien)
- [ ] **Kein nutzerspezifischer Content** -- Keine Pfade, Keys, Namen

### Qualitaetssicherung

- [ ] **Anthropic-kompatibel** -- SKILL.md + optionale scripts/ (kein proprietaeres Format)
- [ ] **Zero/minimale Dependencies** bevorzugen -- stdlib > pip-Paket > externer Service
- [ ] **Tests vorhanden** (fuer Tools mit Code)
- [ ] **Changelog** im SKILL.md

---

## Checkliste C: Externes Projekt als Skill aufnehmen

### Eignungspruefung

- [ ] **Ist es ein Skill?** Oder ein eigenstaendiges Projekt?
      - Skill: Abgeschlossene Faehigkeit, < 20 Dateien, klar abgegrenzt
      - Projekt: Eigenes Repo, eigene UI, eigene DB → Kein Skill, eigenes Repo behalten
- [ ] **Wrapper-Skill noetig?** → Nein -- User koennen Wrapper selbst erstellen
- [ ] **Lizenz kompatibel?** -- MIT, Apache 2.0, BSD → OK. GPL → Vorsicht

### Migration

- [ ] **Kern extrahieren** -- Nur die Skill-relevanten Dateien, nicht das ganze Projekt
- [ ] **Abhaengigkeiten minimieren** -- Braucht es wirklich alle pip-Pakete?
- [ ] **SKILL.md erstellen** -- Mit vollstaendigem Frontmatter
- [ ] **Provenance setzen:**
      ```yaml
      provenance:
        origin: "community"          # oder "custom"
        origin_path: "github.com/<user>/<repo>"
        origin_version: "<tag>"
      ```
- [ ] **Bereinigung** -- Keine projektspezifischen Konfigurationen
- [ ] **Tests** -- Funktioniert der Skill isoliert?

---

## Quick-Reference: Verbotene Muster in Standalone-Skills

| Muster | Problem | Loesung |
|--------|---------|---------|
| `from bach_api import` | BACH-Runtime noetig | Entfernen oder optional |
| `from tools.<x> import` | BACH-interner Pfad | `from <x> import` |
| `from core.` / `from hub.` | BACH-Architektur | Entfernen |
| `bach psycho session` | BACH-CLI | Sektion entfernen |
| `bach task add` | BACH-CLI | Sektion entfernen |
| `parent_agent:` | BACH-Frontmatter | Feld entfernen |
| `expert:` | BACH-Frontmatter | Feld entfernen |
| `C:\Users\lukas\` | Nutzerspezifisch | Relative Pfade |
| `bach.db` | BACH-Datenbank | Entfernen |
| `SQ046`, `SQ047` etc. | BACH-Sprintreferenzen | Entfernen |

---

## BACH skill_export.py nutzen

Fuer zukuenftige Portierungen kann der BACH-eigene Exporter genutzt werden:

```bash
cd /c/Users/lukas/OneDrive/.AI/BACH/system
PYTHONIOENCODING=utf-8 python tools/skill_export.py \
  --skill <skill-name> \
  --format anthropic \
  --output /c/Users/lukas/OneDrive/.SKILLS/skills/<kategorie>/
```

Der Exporter:
- Liest SKILL.md und extrahiert Dependencies
- Kopiert Scripts nach `scripts/`
- Kopiert Referenz-Workflows nach `references/`
- Erzeugt requirements.txt bei pip-Abhaengigkeiten
- Konvertiert Frontmatter ins Anthropic-Format

**Aber:** Der Exporter bereinigt NICHT von BACH-spezifischem Content.
Die manuelle Bereinigung (Checkliste A, Abschnitt "Bereinigung") ist weiterhin noetig.
