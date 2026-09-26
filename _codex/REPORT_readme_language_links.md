# README-Skilllinks nach Sprache

## Änderungen

- Skill-Links in den fünf nichtdeutschen README-Dateien zeigen jetzt auf die vorhandene passende Sprachdatei; falls diese fehlt, auf `SKILL.md` als deutsche Primärfassung. `README_de.md` behält diese Primärfassung.
- Die Rückfallregel steht in `docs/CONVENTIONS.md`. Das neue `testing/readme_language_link_gate.py` prüft alle Skill-Linkziele und ihre Sprache; der pytest-Wrapper wird über `testpaths = ["testing", "skills"]` automatisch entdeckt.
- Die sechs veralteten `trampelpfadanalyse`-Zeilen wurden entfernt: Commit `fea3bd5` weist den Skill als private-only aus und entfernt seine Dateien aus dem öffentlichen Repo.
- `README_EN.md` blieb unverändert. Es wurden keine Übersetzungsdateien erzeugt.

## Gate-Evidenz

- Vor den Linkkorrekturen: `python testing/readme_language_link_gate.py` meldete **172 Verstöße**, Exit 1. Beispiel: `README.md:220` erwartete `SKILL.en.md`, fand `SKILL.md`.
- Nach den Korrekturen: **238 Skill-Links in 6 READMEs geprüft**, Gate bestanden, Exit 0.

## Paritätsbefunde

- `README_de.md` hat dieselben 48 Featured-Skill-Einträge, dieselbe Reihenfolge und dieselben Icons wie `README.md`.
- `README_es.md`, `README_ja.md`, `README_ru.md` und `README_zh.md` lassen jeweils dieselben 20 Featured-Skills aus: `cognitive-restructuring`, `motivational-interviewing`, `lebende-verfassung`, `work-autonomous`, `piggyback-hosting`, `software-in-worten`, `metacognitive-injectors`, `paveman`, `wayfinding-routing`, `condition`, `letter-hooker`, `pingpong`, `choose-your-orchestrator`, `reissverschluss-merge`, `migrate-rename`, `projekt-pipeline-umbrella`, `tidy-up`, `human-loop-audit`, `folder-organization`, `iterative-bundle-selection`. Keine zusätzlichen Skills; die gemeinsame Reihenfolge stimmt jeweils mit Englisch überein.
- Icons: Englisch und Deutsch stimmen überein. Spanisch fehlen die Icons für `agents-bridge`, `automation-self-care`, `semantic-persona-routing` und `build-your-users-mind`. Japanisch, Russisch und Chinesisch haben keine Icons bei ihren 28 Featured-Zeilen.
- Die fünf Education-Skills stehen in allen sechs Dateien vollständig und in gleicher Reihenfolge.
- Die gemessenen Paritätsunterschiede wurden nicht korrigiert; Inhalts- und Übersetzungspflege bleibt außerhalb dieses Tickets.

## Verifikation

- `python -m pytest -ra -v`: **430 passed, 186 subtests passed**.
- `ruff check .`: **All checks passed**.
