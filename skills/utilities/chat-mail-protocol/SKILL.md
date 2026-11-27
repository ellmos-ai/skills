---
name: chat-mail-protocol
version: 0.1.0
type: skill
author: Ocean Contributors
created: 2026-11-27
updated: 2026-11-27
description: "Verwenden, wenn aus Chatverläufen (WhatsApp, Discord, Slack, Telegram, Teams) oder E-Mail-Threads strukturierte Zusammenfassungen, Ergebnisprotokolle oder Aufgabenlisten entstehen sollen (z. B. 'Chat protokollieren', 'Mailverlauf zusammenfassen', /chat-mail-protocol, /protokoll). Nutzt eine selbstheilende Kanal-/Chat-Profil-Kaskade (default-config.json -> <kanal>.json -> <kanal>.<chat>.json), austauschbare Vorlagen und 5 Formate (html/pdf/md/txt/json) samt sicherem Dry-Run-Zustellplan. NICHT verwenden für das Neuformulieren einzelner E-Mails (privat-mail-writer) oder Multi-Quellen-Dossiers (dossier-briefing)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: utilities
tags: [protocol, meeting-notes, chat, email, whatsapp, slack, discord, action-items, ocean-standard]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: ["grounding-seed (optional, empfohlen)"]
  skills: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# chat-mail-protocol — Protokolle & Aufgabenlisten aus Chat- und Mailverläufen

Erzeugt aus unstrukturierten **Chat-Exporten** (WhatsApp, Slack, Discord, Telegram, Teams, JSON-Exporte, Plaintext) sowie mehrteiligen **E-Mail-Threads** quellengebundene **Zusammenfassungen**, **Ergebnisprotokolle**, **chronologische Protokolle** und **Aufgabenlisten** — vollständig nach dem `ocean-skill-creator` (`v0.4.0`)-Standard mit 100 % Python-Standardbibliothek.

## Wann aktivieren

- „erstelle ein Ergebnisprotokoll aus diesem WhatsApp-/Slack-/Discord-Chat“, `/chat-mail-protocol`, `/protokoll`
- „fasse diesen Mail-Thread zusammen und zieh alle offenen Aufgaben mit Verantwortlichen heraus“
- „erzeuge eine druckfertige PDF-/HTML-Protokollfassung und eine kurze Antwort für den Chat“
- **Abgrenzung:** Nicht für das Verfassen neuer persönlicher Anschreiben (`privat-mail-writer`), nicht für reine Audio-Spracherkennung (`transkription`) und nicht für aktenübergreifende Recherche-Dossiers (`dossier-briefing`).

## Kernregeln (Faktentreue & Sicherheit)

1. **Quellenanker statt Halluzination:** Jeder Beschluss (`D-xx`), jede Aufgabe (`A-xx`), jede offene Frage (`Q-xx`) und jeder Blocker (`B-xx`) referenziert die konkrete Quellnachricht (`#source_index`, Sprecher, Originalzitat).
2. **Niemals Fristen oder Zuständigkeiten erfinden:** Eine Frist (`due`) wird ausschließlich übernommen, wenn sie im Nachrichtentext explizit steht; andernfalls bleibt `due: null` (`—`). Unklare Zuständigkeiten werden ehrlich als `offen` ausgewiesen.
3. **Safe-by-Default bei Verteilung & Antwort (`dry_run: true`):** `protocol_core.py` versendet niemals eigenmächtig Nachrichten oder E-Mails nach außen. Auch `reply_in_chat: true` erzeugt zunächst einen geprüften Antwort-Entwurf im Zustellplan (`sent_externally: false`).

## Hierarchische Konfigurations-Kaskade & Selbstheilung

Alle Darstellungs-, Format- und Zustelloptionen liegen außerhalb des Codes in JSON-Profilen und werden von allgemein nach spezifisch zusammengeführt:

```text
1. default-config.json                (versioniertes, nutzerneutrales Fallback im Skill)
2. <config_dir>/config.json           (lokaler Basis-Override)
3. <config_dir>/<kanal>.json          (z. B. whatsapp.json, slack.json, discord.json, email.json)
4. <config_dir>/<kanal>.<chat>.json   (z. B. whatsapp.projekt-alpha.json — überschreibt whatsapp.json gezielt!)
5. CLI-Flags                          (--doc-types, --formats, --template, --anonymize)
```

- **Mitgelieferte Beispiel-Profile (`profiles/`):**
  [slack.example.json](profiles/slack.example.json), [whatsapp.example.json](profiles/whatsapp.example.json), [whatsapp.projekt-alpha.example.json](profiles/whatsapp.projekt-alpha.example.json), [discord.example.json](profiles/discord.example.json), [email.example.json](profiles/email.example.json).
- **Selbstheilung (`self_healing`):** Fehlt ein Kanal- oder Chat-Profil, greift automatisch die nächsthöhere Ebene bis hin zu [default-config.json](default-config.json). Ist eine lokale JSON-Datei beschädigt oder falsch typisiert, stürzt der Lauf nicht ab, sondern fällt kontrolliert zurück; mit `--repair-config` wird die defekte Datei verlustfrei als `<datei>.corrupt.<YYYYMMDDTHHMMSSZ>.bak` gesichert und atomar wiederhergestellt.

## Berichte, 5 Ausgabeformate & austauschbare `templates/`

Über [protocol_core.py](scripts/protocol_core.py) stehen fünf Ausgabeformate und austauschbare Vorlagen bereit:

- **Vorlagen unter `templates/` (oder per `templates.custom_dir` überschreibbar):**
  - [ergebnisprotokoll.html](templates/ergebnisprotokoll.html) — druckfertiges `@media print` A4-HTML mit Kopfbereich, Kurzfassung, Beschluss-Karten, Aufgabentabelle und offenen Punkten (vollständig `html.escape`-gesichert).
  - [ergebnisprotokoll.md](templates/ergebnisprotokoll.md) — strukturiertes Markdown-Ergebnisprotokoll.
  - [ergebnisprotokoll.txt](templates/ergebnisprotokoll.txt) — barrierearme Klartextfassung.
  - [kompakt-chat.txt](templates/kompakt-chat.txt) — kompakte Chat-Rückmeldung für `reply_in_chat`.
  - [aufgabenliste.md](templates/aufgabenliste.md) — fokussierte Aufgaben- und Zuständigkeitsübersicht.
- **Ausgabeformate (`--formats`):** `html`, `pdf` (reiner Python-Stdlib-`%PDF-1.4`-Generator mit `WinAnsiEncoding` für echte deutsche Umlaute `ä ö ü Ä Ö Ü ß`, automatischem Seitenumbruch und exakten `xref`-Offsets ohne Browserzwang), `md`, `txt`, `json`.

## CLI-Schnellstart

```bash
# Verlauf auswerten, Kanal automatisch erkennen und MD/HTML/PDF schreiben
python skills/utilities/chat-mail-protocol/scripts/protocol_core.py process \
  --input chat_export.txt \
  --chat projekt-alpha \
  --out-dir ./protokolle \
  --json

# Effektive Profil-Kaskade prüfen (inkl. optionaler Selbstheilung korrupter lokaler JSONs)
python skills/utilities/chat-mail-protocol/scripts/protocol_core.py show-config \
  --channel whatsapp --chat projekt-alpha --config-dir ./meine-profile --repair-config --json

# Verfügbare eingebaute und benutzerdefinierte Vorlagen anzeigen
python skills/utilities/chat-mail-protocol/scripts/protocol_core.py list-templates --json
```

## Anbieter & Alternativen

- **Eigenständiger Stdlib-Kern:** `scripts/protocol_core.py` arbeitet 100 % lokal und offline ohne Drittanbieter-Pakete.
- **Optionale Ökosystem-Kopplung:** Über `delivery.handoff_tasks_to` (`"ticket-master"` oder `"kalender"`) bereitet der Zustellplan strukturierte Aufgaben-Übergabedaten vor; externe Konnektoren werden bei Bedarf über [connections.json](connections.json) (`grounding-seed`) aufgelöst und niemals eigenmächtig installiert.

## Selbstaktualisierung

- Prüfe regelmäßig `lernvertrag.letzter_update_check` in `default-config.json` / `config.json`, ob neue Exportformate gängiger Messenger hinzugekommen sind, und gleiche Nachbarskills über `skill-finder` ab.
- Speichere bestätigte Erkenntnisse datiert in `connections.json` (`gelernt`).

## Verwandte Skills

- `ocean-skill-creator` — Architektur-, Config-Self-Healing- und Template-Standard dieses Skills.
- `privat-mail-writer` — Ausformulieren einzelner ausgehender E-Mails und Briefe.
- `dossier-briefing` — Quellenübergreifende Entscheidungs- und Hintergrunddossiers.
- `transkription` — Vorstufe für Sprachnachrichten oder Meeting-Audioaufnahmen vor der Protokollierung.
- `kalender` — Übernahme terminierter Folgeaufgaben oder Besprechungstermine.

## Changelog

### 0.1.0 (2026-11-27)
- Erstveröffentlichung nach `ocean-skill-creator` (`v0.4.0`)-Standard mit 4-stufiger Kanal-/Chat-Profil-Kaskade (`default-config.json` -> `config.json` -> `<kanal>.json` -> `<kanal>.<chat>.json`), Self-Healing-Backup, Multi-Messenger-/E-Mail-Parser, quellengebundener Beschluss-/Aufgabenextraktion, 5 Ausgabeformaten (`html`, `pdf` mit `WinAnsiEncoding`, `md`, `txt`, `json`), 5 Vorlagen und Dry-Run-Zustellplaner.
