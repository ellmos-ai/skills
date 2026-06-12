# Skills Library -- Projekt-Anweisungen

## Projekt

Standalone-Skillbibliothek mit portierbaren KI-Skills im Anthropic-kompatiblen Format.
Repo: github.com/ellmos-ai/skills

## Regeln

1. **Frontmatter ist Pflicht** -- Jede SKILL.md braucht vollstaendigen YAML-Header (siehe docs/CONVENTIONS.md)
2. **Standalone-Deklaration** -- Jeder Skill muss `standalone: true/false` deklarieren
3. **Provenance pflegen** -- Bei Import/Export immer `provenance`-Felder aktualisieren
4. **Keine BACH-Runtime in standalone Skills** -- `standalone: true` Skills duerfen keine `bach_api` Imports oder `bach` CLI-Aufrufe enthalten
5. **Zweisprachig** -- Primaersprache Deutsch (`SKILL.md`), optionale EN-Version als `SKILL.en.md`. Code/Scripts immer englisch. Details: `docs/CONVENTIONS.md`
6. **Flat-Regel** -- Unter 5 Dateien: alles flat im Skill-Ordner, ab 5: Unterordner erlaubt
7. **Portierungs-Checkliste** -- Bei BACH-Exports immer `docs/PORTING_CHECKLIST.md` befolgen
8. **BACH-Export nutzen** -- `skill_export.py --format anthropic` als Ausgangsbasis, dann manuell bereinigen
9. **Qualitaetstests** -- Neue Skills mit `python testing/skill_tester.py test <skill>` pruefen. Batch: `python catalog.py quality --run`

## Konventionen

- Skill-Namen: kebab-case (`steuer-assistent`, nicht `SteuerAssistent`)
- Versionen: Semantic Versioning (1.0.0)
- Kategorien = Ordnernamen unter `skills/`
- Details: `docs/CONVENTIONS.md`

## Quelle der Wahrheit & Deployment

- **`skills/` in diesem Repo ist die Quelle der Wahrheit** fuer alle Skills: kategorisiert, mit Frontmatter, Provenance und Tests.
- **`~/.claude/skills/` ist nur Deployment-Ziel** (flache Skill-Ordner fuer die Claude-Code-Runtime). Dort NICHT direkt editieren -- Aenderungen immer hier machen und anschliessend deployen.
- **Sync-Tool:** `python skill_sync.py status` (Drift-Report), `python skill_sync.py deploy [skill ...]` (Quelle → Ziel, `--dry-run` zum Testen), `python skill_sync.py diff <skill>` (Unified-Diff). Sammel-Deploy (`deploy` ohne Argumente) aktualisiert nur Skills, die im Ziel schon existieren — Erstinstallation eines Skills nur mit explizitem Namen (das Deployment ist eine kuratierte Auswahl).
- **Deregistrierung:** Im Deployment kann `SKILL.md` bewusst zu `CONTENT.md` umbenannt sein (Skill wird von der Runtime nicht geladen, bleibt aber per Read-Tool nutzbar — Routing über Einstiegs-Skills). Das Sync-Tool erkennt und erhält das beim Deploy.
- **Hold-Liste:** `~/.claude/skills/.sync-hold` markiert Skills, deren Deployment-Version bewusst lokal abweicht (lokale Forks, z.B. Therapy-Einstiegs-Skills mit Routing-Tabellen). Sie werden beim Sammel-Deploy übersprungen; explizites Deploy braucht `--force`.
- Nur-Ziel-Skills (existieren nicht in der Quelle) werden NIE gelöscht, nur gemeldet.
- Privacy-Regel: Persoenliche Konkretwerte (Pfade, Hostnames, IPs, Key-Namen) gehoeren NICHT in veroeffentlichte Skills -- generische Platzhalter (`<host>`, `~/.ssh/<key>`) verwenden oder den Skill per `.gitignore` privat halten.
