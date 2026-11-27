---
name: ocean-skill-creator
version: 0.4.0
type: skill
author: Ocean Contributors
created: 2026-08-24
updated: 2026-11-27
description: "Verwenden, wenn ein neuer Skill entstehen oder ein bestehender auf Ocean-Standards nachgerüstet werden soll (z. B. 'erstelle einen Skill', 'neuen Skill anlegen', 'Skill auf Ocean-Standard heben', /ocean-skill-creator, Übergangs-Alias /ellmos-skill-creator). Delegiert den Entwurf an skill-creator und erzwingt Ocean-Standards (abwärtskompatibel zu ellmos): 9-Felder-Frontmatter, default-config.json mit Profil-Kaskade und Selbstheilung, Berichts-/Template-Ausgabe (html/pdf/md/txt/json), grounding-seed, Vendor-Bewusstsein, Lernvertrag sowie Scaffold-/Audit-CLI. NICHT verwenden für Skill-Suche (skill-finder) oder Bestands-Audits (skill-explorer)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [skill-authoring, ocean, config-cascade, self-healing, templates, grounding-seed, vendor-awareness]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: ["grounding-seed (optional, empfohlen)"]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="ocean-skill-creator banner">

# ocean-skill-creator — Ocean-Skill-Baukasten

> **Nachfolge-Hinweis (`v0.4.0`):** `ocean-skill-creator` ist der kanonische Nachfolger von `ellmos-skill-creator`. Bestehende `ellmos.*`-Schemas, `grounding-seed`-Andockpunkte und der Übergangs-Auslöser `/ellmos-skill-creator` bleiben vollständig abwärtskompatibel.

## Herkunft und Entscheidung (Fork vs. Eigenbau)

**Entscheidung: Eigenbau, kein Fork.** Begründung, damit sie dauerhaft nachvollziehbar bleibt:

- `skill-creator` (Anthropic, Marketplace `claude-plugins-official`) ist **Apache-2.0** lizenziert — ein Fork wäre rechtlich sauber möglich, hätte aber die gesamte generische Eval-/Benchmark-Maschinerie (`agents/`, `eval-viewer/`, 7 Skripte) unnötig dupliziert, obwohl sie direkt über `Skill: skill-creator:skill-creator` aufrufbar ist.
- Die eigentliche Aufgabe dieses Skills liegt in den **Ocean-Standards (abwärtskompatibel zu ellmos-Komponenten)**, die dem generischen Upstream unbekannt sind:
  9-Felder-Haus-Frontmatter, zweisprachige Kernparität (DE+EN), Anti-Hardcoding über ausgelagerte Einstellungen (`default-config.json` + 5-stufige Profil-Kaskade), selbstheilender Konfigurations-Loader mit `.corrupt.<ts>.bak`-Sicherung, standardisierte Berichts- und Template-Architektur (`html`/`pdf`/`md`/`txt`/`json` + `templates/`), `grounding-seed`-Andockung (`connections.json`), Anbieter-Bewusstsein sowie Lern- und Usecase-Abdeckung.
- Dieser Skill enthält **keinen Fremdtext** und **komponiert** das Original statt es zu kopieren. Zusätzlich bringt er mit [ocean_skill_scaffold.py](scripts/ocean_skill_scaffold.py) ein reines Python-Stdlib-Werkzeug für deterministisches Scaffolding, Selbstheilungs-Validierung und Bestands-Audits mit.

## Wann aktivieren

- „erstelle einen Skill für X“, „neuen Skill anlegen“, „skill-creator nutzen“, `/ocean-skill-creator` (oder Übergangs-Alias `/ellmos-skill-creator`)
- „mach diesen Skill Ocean-konform“, „bestehenden Skill auf Haus-Standard / Config-Kaskade / Berichts-Templates nachrüsten“
- „prüfe diesen Skill auf Hardcodierungen oder fehlende `default-config.json`“ (`audit-skill`)
- Immer dann, wenn der Zielort ein Skill unseres Ocean-/ellmos-Skill-Katalogs ist — nicht für lose Einmal-Prompts ohne Ökosystem-Bezug.

## Vorgehen

### Schritt 1 — Interview, Entwurf und Eval delegieren

Rufe bei Bedarf den offiziellen `Skill: skill-creator:skill-creator` auf für: Intent-Klärung, Grundstruktur des Ablaufs, Testfälle (`evals/evals.json`), Eval-Schleife und Auslöser-Schärfung. **Nicht neu erfinden**, was dort generisch gelöst ist — `ocean-skill-creator` legt das Ocean-Qualitäts- und Architektur-Fundament darüber.

### Schritt 1b — Beschreibung = Auslöser (Pflicht, nicht optional)

Die `description` entscheidet allein darüber, ob ein Skill jemals ausgewählt wird; der Markdown-Rumpf ist für den Router unsichtbar. Vor jedem Abschluss prüfen:

- **Das WANN steht ganz vorn** („Verwenden, wenn …“ / „Use when …“), danach was der Skill leistet. Der Auslöser inklusive 2–3 typischer Beispielphrasen muss zwingend innerhalb der **ersten 250 Zeichen** stehen, weil Laufzeitumgebungen lange Einträge in der Skill-Liste abschneiden.
- **Typische Nutzerformulierungen** in einfachen Anführungszeichen plus Slash-Befehl (`/mein-skill`).
- **Klare Abgrenzung** zu Nachbarskills („NICHT verwenden für … (dafür nachbar-skill)“).
- **YAML-Wert in doppelten Anführungszeichen**, maximal 1024 Zeichen, konsistent in allen Sprachfassungen.
- `python testing/skill_frontmatter_gate.py` meldet den Skill weder unter „ohne erkennbaren Auslöser“ noch unter „Auslöser erst nach den ersten 250 Zeichen“.

### Schritt 2 — Ocean-Haus-Scaffold aufsetzen (Pflicht, additiv zum Anthropic-Format)

Erzeuge das Grundgerüst bevorzugt direkt über das mitgelieferte Stdlib-Werkzeug:

```bash
python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py scaffold <name> --category <kategorie> --out skills/<kategorie> --with-reports --with-profiles --json
```

Prüfpunkte für das Frontmatter und die Dateistruktur (`docs/CONVENTIONS.md`):

- Alle **neun Haus-Pflichtfelder** (`name`, `version`, `type`, `author`, `created`, `updated`, `description`, `standalone`, `visibility`) plus `category`, `language`, `status`, `tags`, `dependencies` und `provenance`.
- **`visibility` startet bei jedem neuen Skill zwingend auf `private-only`** — eine Veröffentlichung (`public`) erfolgt erst nach ausdrücklicher Prüfung und Nutzerfreigabe.
- **Zweisprachiger Kern (Core P-006):** `SKILL.md` (Deutsch, Leitfassung) und `SKILL.en.md` (Englisch, strukturell paritätisch mit identischem `name:`).
- Alle Zusatzfelder sind rein additiv neben `name`/`description` (`anthropic_compatible: true`).

### Schritt 3 — Ocean-Prinzipien durchsetzen: anbieterneutral, nutzerneutral, Ocean-/ellmos-sensitiv

Volltext und Codemuster: [OCEAN-PRINCIPLES.md](references/OCEAN-PRINCIPLES.md). Kurzfassung:

- **Eigenständig lauffähig (`standalone`):** Der Skill bringt seine Standardkonfiguration (`default-config.json`), Vorlagen (`templates/`) und Stdlib-Fallbacks selbst mit.
- **Ökosystem-sensitiv zur Laufzeit:** Sind Ocean- oder abwärtskompatible ellmos-Komponenten vorhanden (`grounding_seed.detect_ecosystem()`, `source-resolver`), erkennt und nutzt der Skill sie dynamisch über `try/except ImportError` — niemals hart verdrahtet und ohne zweiten Erkennungsstandard.
- **Strikt nutzerneutral im Repo:** Keine persönlichen Namen, Hostnamen, lokalen Entwicklungspfade oder privaten IP-Adressen in versionierten Dateien (`author: Ocean Contributors` oder neutrale Projektbezeichnung).

### Schritt 4 — Ausgelagerte JSON-Einstellungen, Profil-Kaskade & Selbstheilung (Pflicht bei konfigurierbarem Verhalten)

Volltext, Merge-Regeln und Selbstheilungs-Protokoll: [CONFIG-AND-SELF-HEALING.md](references/CONFIG-AND-SELF-HEALING.md).

1. **Anti-Hardcoding-Gebot:** Pfade, Ausgabeformate, Schwellenwerte, Zeitfenster, Sprachen, Darstellungsstile und Zielkanäle gehören **niemals** als feste Konstanten in Skriptcode oder Fließtext, sondern in JSON-Einstellungsdateien.
2. **Verbindliche 5-stufige Konfigurations-Kaskade (aufsteigende Priorität):**
   `default-config.json` (versioniertes, nutzerneutrales Fallback im Skill) -> `config.json` (lokaler/privater Override) -> `<kanal>.json` (z. B. `profiles/mail.json`) -> `<kanal>.<chat>.json` (z. B. `profiles/mail.team-weekly.json`) -> **CLI-Override** (`--set schluessel=wert` bzw. explizite Flags).
   - Vorlagen: [default-config.template.json](templates/default-config.template.json), [skill-config.template.json](templates/skill-config.template.json) und [channel-profile.template.json](templates/channel-profile.template.json).
3. **Selbstheilender Konfigurations-Loader (`load_effective_config`):**
   - Fehlt `config.json` oder ein Kanalprofil, arbeitet der Skill nahtlos mit `default-config.json` weiter.
   - Ist eine lokale Override-Datei syntaktisch beschädigt (`JSONDecodeError`), kein JSON-Objekt oder weist einen falschen Abschnittstyp auf, stürzt der Skill nicht unkontrolliert ab, sondern fällt kontrolliert auf `default-config.json` zurück und protokolliert eine strukturierte Warnung.
   - Im Reparaturmodus (`--repair` / `repair=True`) sichert der Loader die defekte Datei zuerst verlustfrei als `<datei>.corrupt.<UTC-Zeitstempel>.bak`, ergänzt fehlende neue Schlüssel additiv aus `default-config.json` (ohne valide Nutzwerte zu überschreiben) und schreibt das geheilte JSON atomar (`tmp` im Zielordner + `os.replace`).
4. **Trennung von `connections.json`:** Aufgelöste externe Programme/Dienste liegen weiterhin getrennt in `connections.json` ([skill-connections.template.json](templates/skill-connections.template.json), Schema `ellmos.source-resolver.user-config.v1` für `grounding-seed`).

### Schritt 4b — Berichts-, Ausgabeoptionen & austauschbare `templates/` als fester Bestandteil

Volltext und Formatvertrag: [OUTPUT-AND-TEMPLATES.md](references/OUTPUT-AND-TEMPLATES.md).

**Pflicht-Check bei jeder Skill-Erstellung und jedem Retrofit:** Erzeugt der Skill Berichte, Prüfprotokolle, Zusammenfassungen, Übersichten, Kalender-/Statusblätter oder Exporte? Falls **ja**, sind folgende Bausteine verbindlich mitzuliefern:

- **Austauschbarer `templates/`-Ordner:** Strikte Trennung von Fachdaten und Layout über [report.template.html](templates/output/report.template.html) (eigenständiges UTF-8-HTML mit `@media print`), [report.template.md](templates/output/report.template.md) und [report.template.txt](templates/output/report.template.txt). Eigene Vorlagenverzeichnisse lassen sich über `templates.custom_dir` in der Config einhängen, ohne Skill-Code zu ändern.
- **Fünf Standard-Ausgabeformate (`html`, `pdf`, `md`, `txt`, `json`):**
  - `html` -> druckfertige Einzeldatei ohne externe CDN-Abhängigkeiten.
  - `pdf` -> optionaler isolierter Headless-Renderpfad (niemals laufende Nutzer-Browser oder Benutzerprofile anfassen!) **plus zwingender 100-%-Stdlib-`%PDF-1.4`-Fallback**, damit `--format pdf` auf jedem CI- und Server-System ohne Browser deterministisch funktioniert.
  - `md`, `txt` und `json` -> für Weiterverarbeitung in Chat, Konsole und Pipelines.
- **Sichere Zustellungs-Defaults (`delivery`):** Verteilungswege (Dateiablage, Mail, Messenger, Ticket) werden über `default-config.json` / `<kanal>.json` konfiguriert und stehen im Default **immer** auf `enabled: false`, `dry_run: true`, `mode: "draft"` (Entwurf statt Direktversand).

### Schritt 5 — Anbieter- & Vendor-Bewusstsein einbauen

Volltext: [VENDOR-AWARENESS.md](references/VENDOR-AWARENESS.md). Kurzfassung: Skills mit externem Werkzeug- oder Dienstbedarf erhalten den Abschnitt „Anbieter & Alternativen“ mit (a) aktuellem State-of-the-Art-Anbieter, (b) mindestens einer lokalen/kostenfreien Alternative und (c) vorhandenen Ocean-/ellmos-Komponenten als gleichrangigem Kandidaten (`grounding_seed.scan.scan_resources([...])`). Installationen werden begründet vorgeschlagen, niemals eigenmächtig ausgeführt.

### Schritt 6 — Selbstaktualisierung anlegen

Volltext: [SELF-UPDATE.md](references/SELF-UPDATE.md). Kurzfassung: Jeder produzierte Skill führt einen Abschnitt „Selbstaktualisierung“ mit Stichtagsprüfung (`letzter_update_check`), Verweis auf Nachbarskills (`skill-finder`) und strukturierter Ablage neuer Erkenntnisse (`connections.json` -> `gelernt` bzw. optionale Übergabe an vorhandene Memory-Komponenten per `try/except`).

### Schritt 6b — Lernvertrag + Usecase-Abdeckung mitliefern

Volltext: [LEARNING-CONTRACT-AND-COVERAGE.md](references/LEARNING-CONTRACT-AND-COVERAGE.md). Wiederverwendbarer Dateisatz ohne Parallelstandard:

- `evals/evals.json` — vom Autor entworfene Testfälle (`skill-creator`-Standard).
- `user-usecases.json` — reale Anwendungsfälle aus dem Betrieb ([user-usecases.template.json](templates/user-usecases.template.json)).
- `usecase-gaps.json` — offene Abdeckungslücken ([usecase-gaps.template.json](templates/usecase-gaps.template.json)).
- `known-providers-and-abilities.json` — Anbieterkatalog je Rolle nach A2A-`AgentSkill`-Feldern ([known-providers-and-abilities.template.json](templates/known-providers-and-abilities.template.json)).
- `gap-closing-analysis.json` — strukturelle Schließungswege ([gap-closing-analysis.template.json](templates/gap-closing-analysis.template.json)).
- `default-config.json` / `config.json` Feld `lernvertrag` — Verhaltenscodex (`user_ist_koenig: true`, `waehle_beste_option: true`, `installiert_nie_selbststaendig: true`).

### Schritt 7 — Prüfen (`validate-config` & `audit-skill`), registrieren und committen

1. **Konfiguration und Skill-Qualität automatisiert prüfen:**
   ```bash
   python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py validate-config --default skills/<kat>/<name>/default-config.json --config skills/<kat>/<name>/config.json --json
   python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py audit-skill skills/<kat>/<name> --json
   ```
2. **Repo-Gates ausführen:** `skill_frontmatter_gate.py`, `language_gate.py`, `privacy_gate.py`, `changed_skill_gate.py` sowie Skill-Unit-Tests (`pytest`) und `ruff check`.
3. **Katalog-Dateien generieren statt handeditieren:** Bei öffentlichen Skills in einer sauberen Arbeitskopie `python build_public_registry.py` und `python build_skills_map.py` ausführen (danach mit `--check` gegenprüfen).

## Kompatibilität zum Anthropic-Format und zu ellmos-Beständen

Alle Haus-Felder im YAML-Frontmatter sind reine Erweiterungen neben `name` und `description`; jede Standard-Claude-Code-Umgebung liest sie verlustfrei. Ebenso akzeptiert der Loader sowohl das neue Schema `ocean.skill-config.v2` als auch bestehende `ellmos.skill-config.v1`-Dateien.

## Verwandte Skills

- `skill-creator:skill-creator` — generischer Interview-, Entwurfs- und Eval-Loop (Schritt 1).
- `skill-finder` — prüft vor jedem Neubau, ob bereits ein passender lokaler Skill existiert.
- `skill-explorer` — katalogweiter Landschafts-Audit über alle Skills.
- `skill-family-care`, `skill-register-care` — Familien-Routing und Registerpflege nach dem Anlegen.
- `dual-use-software-design` — Architekturstandard für Anwendungen, die zugleich für Menschen und LLMs bedienbar sind.

## Changelog

### 0.4.0 (2026-11-27)
- Umbenennung von `ellmos-skill-creator` zu `ocean-skill-creator` (inkl. Übergangs-Alias `/ellmos-skill-creator` und voller Rückwärtskompatibilität zu `ellmos.*`-Schemas und `grounding-seed`).
- Schritt 4 erweitert: Anti-Hardcoding-Standard mit `default-config.json`, 5-stufiger Merge-Kaskade (`default-config.json` -> `config.json` -> `<kanal>.json` -> `<kanal>.<chat>.json` -> CLI) und selbstheilendem Config-Loader (`.corrupt.<ts>.bak`-Backup, additive Migration, atomares Schreiben); dokumentiert in `references/CONFIG-AND-SELF-HEALING.md`.
- Schritt 4b neu: Verbindliche Berichts-/Ausgabearchitektur (`html`, `pdf` inkl. Stdlib-`%PDF-1.4`-Fallback, `md`, `txt`, `json`), austauschbare `templates/` (`report.template.html/md/txt`) und sichere Dry-Run-Zustellungs-Defaults; dokumentiert in `references/OUTPUT-AND-TEMPLATES.md`.
- Neues Stdlib-CLI- und Bibliotheksskript `scripts/ocean_skill_scaffold.py` (`scaffold`, `validate-config`, `audit-skill`) samt `tests/test_ocean_skill_scaffold.py`.

### 0.3.1 (2026-11-15)
- Schritt 1b: Der Auslöser steht in den ersten 250 Zeichen der `description` (Skill-Liste kappt Einträge und lässt bei Überlauf ganze Beschreibungen weg); Gate-Hinweis „Auslöser erst nach den ersten 250 Zeichen“.

### 0.3.0 (2026-11-06)
- Schritt 1b: Beschreibung = Auslöser ist Pflicht (WANN zuerst, Formulierungen, Abgrenzung, Gate-Hinweis, Eval an echtem Fall).

### 0.2.0 (2026-08-24)
- Wiederverwendbares Lern- und Usecase-Abdeckungs-Muster ergänzt (`user-usecases.json`, `usecase-gaps.json`, `known-providers-and-abilities.json`, `gap-closing-analysis.json` sowie `lernvertrag` in der Skill-Konfiguration).

### 0.1.0 (2026-08-24)
- Erstfassung unter dem Namen `ellmos-skill-creator` als komponierender Aufsatz über `skill-creator:skill-creator` mit Haus-Scaffold, `grounding-seed`-Andockung, Vendor-Awareness und Selbstaktualisierung.
