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
