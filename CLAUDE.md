# Skills Library -- Projekt-Anweisungen

## Projekt

Standalone-Skillbibliothek mit portierbaren KI-Skills im Anthropic-kompatiblen Format.
Repo: github.com/lukisch/skills (geplant)

## Regeln

1. **Frontmatter ist Pflicht** -- Jede SKILL.md braucht vollstaendigen YAML-Header (siehe docs/CONVENTIONS.md)
2. **Standalone-Deklaration** -- Jeder Skill muss `standalone: true/false` deklarieren
3. **Provenance pflegen** -- Bei Import/Export immer `provenance`-Felder aktualisieren
4. **Keine BACH-Runtime in standalone Skills** -- `standalone: true` Skills duerfen keine `bach_api` Imports oder `bach` CLI-Aufrufe enthalten
5. **Deutsch** -- Skill-Inhalte primaer auf Deutsch, technische Identifier auf Englisch
6. **Flat-Regel** -- Unter 5 Dateien: alles flat im Skill-Ordner, ab 5: Unterordner erlaubt

## Konventionen

- Skill-Namen: kebab-case (`steuer-assistent`, nicht `SteuerAssistent`)
- Versionen: Semantic Versioning (1.0.0)
- Kategorien = Ordnernamen unter `skills/`
- Details: `docs/CONVENTIONS.md`
