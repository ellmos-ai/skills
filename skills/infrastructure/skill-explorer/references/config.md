# config.json — persistierte Entscheidungen

## Zweck

Damit Re-Runs sich an frühere Entscheidungen erinnern (welche Familien gebildet, welche Router
gesetzt, welche Subskills erzeugt, wo das Register liegt), pflegt `skill-explorer` eine
`config.json` in seinem eigenen Verzeichnis: `~/.claude/skills/skill-explorer/config.json`.

Die Datei wird **zur Laufzeit** angelegt/aktualisiert (nicht mitausgeliefert — Vorlage:
`assets/config.example.json`). Ein leeres/fehlendes config bedeutet „erster Lauf".

## Lebenszyklus

1. **Beim Start** `config.json` lesen (falls vorhanden). Bekannte Familien/Router als Vorbelegung
   nutzen, damit der Bericht zeigt, was bereits eingerichtet ist (z. B. „Familie X bereits verlinkt").
2. **Nach Phase 2** (Ausführung der bestätigten Nummern) die Datei aktualisieren:
   - `families[*].linked` / `.umbrella` setzen, wenn c2/c1 ausgeführt wurde,
   - `subskills_created[*].installed` setzen, wenn [F]/[P1]/[P2] ausgeführt wurde,
   - `decisions_log` um den Lauf ergänzen (`date`, `chosen`-Nummern),
   - `updated` / `last_audit` auf das aktuelle Datum.
3. **Idempotenz:** Vor dem Erzeugen eines Subskills/Umbrellas in der config prüfen, ob er schon
   `installed` ist → dann aktualisieren statt neu anlegen (keine Duplikate).

## Felder

| Feld | Bedeutung |
|------|-----------|
| `register.exists` / `.artifacts` | ob ein Register existiert und welche Artefakte es bilden |
| `families[name].members` | Skill-Verzeichnisse der Familie |
| `families[name].router` | Wegweiser-Text (für `inject_family_header.py`) |
| `families[name].linked` | ob c2 (Header-Router) gesetzt wurde |
| `families[name].umbrella` | Name des c1-Umbrella-Skills oder null |
| `subskills_created` | Status von `skill-finder` / `skill-family-care` / `skill-register-care` |
| `branches` | erzeugte Branches von Drittanbieter-Skills (Original, Datum, Grund, Status) |
| `decisions_log` | Historie der pro Lauf gewählten Nummern |

Wenn ein Branch angelegt wird, wird er unter `branches` vermerkt — damit erkennt ein Re-Run, dass
der Branch bereits existiert, und legt keinen zweiten an (Idempotenz).

> Das Datum wird vom ausführenden Modell gesetzt (aktuelles Datum), nicht geraten. Pfade nutzerneutral
> als `~/...` speichern.
