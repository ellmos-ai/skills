# Berichts-, Ausgabeoptionen & austauschbare `templates/` (`v0.4.1`)

Wenn ein Skill strukturierte Dokumente oder Berichte für Menschen und nachgelagerte Werkzeuge erzeugt (Prüfberichte, Protokolle, Kalenderblätter, Zusammenfassungen, Dossiers), trennt der Ocean-Standard Layout, Formatwahl und Zustellung sauber vom Fachcode — **nur dort, wo dies fachlich gebraucht wird**.

## 1. Pragmatische Bedarfsprüfung („Nur dort, wo sinnvoll“)

Beantworte bei jedem neuen oder überarbeiteten Skill zuerst nüchtern:

> **Rendert dieser Skill tatsächlich strukturierte Berichte, Protokolle, Kalenderblätter oder mehrformatige Dokumentexporte?**

- **Nein** (reiner Denk-, Beratungs-, Therapie-, Konventions- oder Router-/Umbrella-Skill, oder ein reines CLI-/Prüfwerkzeug mit JSON-/Konsolenausgabe):
  - **Kein `templates/`-Ordner und kein künstliches Berichts-Skript anlegen!** (`init <name> --minimal` oder `init <name> --no-templates`).
  - `audit-skill` wertet das Fehlen von `templates/` und `scripts/` bei solchen Skills **niemals** ab (`100/100 conformant`).
- **Ja** (der Skill erzeugt aufbereitete Berichte/Dokumente oder bettet bisher HTML/Markdown-Layouts direkt im Code ein):
  - Lege `templates/` an (`init <name> --with-reports`) und unterstütze die passenden Standardformate (`html`, `pdf`, `md`, `txt`, `json`).

## 2. Die fünf Standard-Ausgabeformate für Berichts-Skills

| Format | Zweck & Qualitätsanforderung |
|---|---|
| `html` | Eigenständiges UTF-8-HTML5-Dokument mit eingebettetem CSS und `@media print`-Regeln (A4/Letter-sauberer Umbruch, keine externen CDN-Fonts oder Skripte, konsequentes `html.escape`). |
| `pdf` | Druckfertiges Dokument. Darf optional einen isolierten Headless-Renderer mit eigenem temporärem `--user-data-dir` und fensterloser Ausführung nutzen (niemals laufende Browser-Prozesse oder Nutzerprofile anfassen!), **muss aber zwingend einen reinen Python-Stdlib-`%PDF-1.4`-Fallback besitzen**, damit `--format pdf` auf jedem System und in jeder CI ohne Browser deterministisch funktioniert. |
| `md` | Sauberes GitHub-Flavored Markdown für Dokumentation, Reviews und Artefakte. |
| `txt` | Barrierearmes, spalten- und konsolenfreundliches Klartextformat ohne HTML-/Markdown-Rauschen. |
| `json` | Vollständige, maschinenlesbare Strukturdaten (`ensure_ascii=False`, stabiles Schema) für Pipelines und Tests. |

## 3. Austauschbare `templates/` statt Inline-Markup im Code

Sobald ein Skill Berichte rendert, gehört das Darstellungs-Markup in Vorlagendateien unter `templates/` (Referenzvorlagen in diesem Skill unter `templates/output/`):

- `report.template.html` (oder sprechender Fachname wie `ergebnisprotokoll.html`)
- `report.template.md`
- `report.template.txt`

### Standard-Platzhalter

Die mitgelieferten Referenzvorlagen nutzen einfache, stdlib-freundliche Platzhalter ohne externe Template-Engine:

- `{{title}}` — Haupttitel des Berichts (in HTML automatisch via `html.escape` maskiert!)
- `{{subtitle}}` — Untertitel / Zeitraum / Kontext
- `{{generated_at}}` — ISO-8601-Zeitstempel der Erzeugung
- `{{summary}}` — Kurzfassung / Kennzahlenblock
- `{{body_html}}` / `{{body_md}}` / `{{body_txt}}` — formatgerechter Hauptinhalt
- `{{footer}}` — Herkunfts- und Versionszeile des erzeugenden Skills

### Anpassbarkeit ohne Codeänderung (`templates.custom_dir`)

Über den Konfigurationsblock `templates` lässt sich jederzeit ein eigenes Vorlagenverzeichnis einhängen, ohne den Skill-Code zu berühren:

```json
"templates": {
  "dir": "./templates",
  "custom_dir": null,
  "html": "report.template.html",
  "md": "report.template.md",
  "txt": "report.template.txt"
}
```

## 4. Konfigurierbare Zustellungswege (`delivery` — Safe-by-Default)

Falls Ergebnisse an Kanäle (Dateiablage, E-Mail, Chat, Ticket-Queue) übergeben werden können, steuert der Abschnitt `delivery` das Ziel — mit unverhandelbaren Sicherheits-Defaults:

```json
"delivery": {
  "enabled": false,
  "dry_run": true,
  "mode": "draft",
  "channel": null,
  "target": null
}
```

- **Entwurf / Dry-Run als Standard:** Ohne ausdrückliche Aktivierung erzeugt der Skill ausschließlich lokale Dateien bzw. Vorschauen (`dry_run: true`, `mode: "draft"`).
