# Berichts-, Ausgabeoptionen & austauschbare `templates/` (`v0.4.0`)

Viele Skills erzeugen strukturierte Ergebnisse für Menschen und nachgelagerte Werkzeuge: Prüfberichte, Übersichten, Zusammenfassungen, Kalenderblätter, Dossiers oder Datenexporte. Damit Layout, Formatwahl und Versandwege nicht in jedem Skill ad hoc im Code verstreut werden, gilt im `ocean-skill-creator` ein einheitlicher Ausgabe- und Template-Standard.

## 1. Pflicht-Entscheidung bei Entwurf & Retrofit

Beantworte bei jedem neuen oder überarbeiteten Skill explizit:

> **Erzeugt der Skill Berichte, Zusammenfassungen, Übersichten, Protokolle oder Exporte?**

- **Nein** (reiner interner Router, kleiner zustandsfreier Konverter): `default-config.json` genügt ohne Berichts-Templates.
- **Ja:** Der Skill erhält standardmäßig einen `templates/`-Ordner sowie die fünf Standard-Ausgabeformate (`html`, `pdf`, `md`, `txt`, `json`) (`scaffold ... --with-reports`).

## 2. Die fünf Standard-Ausgabeformate

| Format | Zweck & Qualitätsanforderung |
|---|---|
| `html` | Eigenständiges UTF-8-HTML5-Dokument mit eingebettetem CSS und `@media print`-Regeln (A4/Letter-sauberer Umbruch, keine externen CDN-Fonts oder Skripte). |
| `pdf` | Druckfertiges Dokument. Darf optional einen isolierten Headless-Renderer mit eigenem temporärem `--user-data-dir` und fensterloser Ausführung nutzen (niemals laufende Browser-Prozesse oder Nutzerprofile anfassen!), **muss aber zwingend einen reinen Python-Stdlib-`%PDF-1.4`-Fallback besitzen**, damit `--format pdf` auf jedem System und in jeder CI ohne Browser deterministisch funktioniert. |
| `md` | Sauberes GitHub-Flavored Markdown für Dokumentation, Reviews und Artefakte. |
| `txt` | Barrierearmes, spalten- und konsolenfreundliches Klartextformat ohne HTML-/Markdown-Rauschen. |
| `json` | Vollständige, maschinenlesbare Strukturdaten (`ensure_ascii=False`, stabiles Schema) für Pipelines und Tests. |

## 3. Austauschbare `templates/` statt Inline-Strings

Darstellungs-Markup gehört in Dateien unter `templates/` (Vorlagen in diesem Skill unter `templates/output/`):

- `report.template.html`
- `report.template.md`
- `report.template.txt`

### Standard-Platzhalter

Die mitgelieferten Vorlagen verwenden einfache, stdlib-freundliche Platzhalter ohne externe Template-Engine:

- `{{title}}` — Haupttitel des Berichts (in HTML automatisch via `html.escape` maskiert!)
- `{{subtitle}}` — Untertitel / Zeitraum / Kontext
- `{{generated_at}}` — ISO-8601-Zeitstempel der Erzeugung
- `{{summary}}` — Kurzfassung / Kennzahlenblock
- `{{body_html}}` / `{{body_md}}` / `{{body_txt}}` — formatgerechter Hauptinhalt
- `{{footer}}` — Herkunfts- und Versionszeile des erzeugenden Skills

### Anpassbarkeit ohne Codeänderung (`templates.custom_dir`)

In `default-config.json` definiert der Abschnitt `templates`:

```json
"templates": {
  "dir": "./templates",
  "custom_dir": null,
  "html": "report.template.html",
  "md": "report.template.md",
  "txt": "report.template.txt"
}
```

Setzt ein Nutzer oder ein Kanalprofil (`profiles/<kanal>.json`) `templates.custom_dir` auf ein eigenes Verzeichnis, lädt der Skill vorrangig die dort liegende Vorlage und fällt bei fehlender Einzeldatei automatisch auf `./templates/` zurück.

## 4. Konfigurierbare Zustellungswege (`delivery` — Safe-by-Default)

Falls Ergebnisse an Kanäle (Dateiablage, E-Mail, Chat, Ticket-Queue) übergeben werden können, steuert der Abschnitt `delivery` in der Konfigurations-Kaskade das Ziel — mit unverhandelbaren Sicherheits-Defaults in `default-config.json`:

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
- **Kanalprofile nutzen:** Kanalspezifische Formate (z. B. `pdf` für `mail.json`, kompaktes `md` oder `txt` für `chat.json`) werden über die Profil-Kaskade gesteuert statt im Code verzweigt.
