# SKILL*.md-Frontmatter: ungueltiges YAML behoben

## Befund

`yaml.safe_load` auf jede `SKILL*.md`-Frontmatter angewendet: 279 von 1060 echten
Skill-Dateien parsten nicht (2 weitere Treffer, `skill-explorer/assets/skill-*-template.md`,
sind Vorlagen mit `{{platzhaltern}}`, keine echten Skills -- ausgenommen).

Zwei Fehlerbilder:
1. **267 Dateien** (DE/EN/ES/RU, vereinzelt ZH/JA): unquotierte einzeilige
   `description:`-Werte mit einem `": "` im Fliesstext (z. B. "... coding tools:
   CodeCommander MCP ...") -- YAML liest das als neue Mapping-Zeile ->
   "mapping values are not allowed here". FR-Dateien mit `[Sprache] ...`-Praefix
   fallen unter dasselbe Muster (`[` am Wertanfang wird als Flow-Sequence-Start
   gelesen).
2. **10 Dateien** (`condition` + `decision-avatar`, je 5 Sprachen): ein
   `description: >`-Faltblock, dessen Fortsetzungszeilen die 2-Space-Einrueckung
   verloren hatten -> "while scanning a simple key".

## Fix

Rein mechanisch, keine Wortaenderung:
- Fehlerbild 1: Wert extrahiert, per `json.dumps(wert, ensure_ascii=False)`
  requotiert.
- Fehlerbild 2: Fortsetzungszeilen zu einer logischen Zeile zusammengefuegt
  (wie YAMLs eigenes Falten es getan haette), dann ebenso requotiert.
- Jede Datei nach dem Fix mit `yaml.safe_load` re-validiert; 0 Dateien blieben
  ungueltig.
- `registry/components.json` + `registry/public-skill-files.json` neu gebaut
  (Byte-Aenderung der Quelldateien macht den Registry-Hash sonst stale).

11 deployte Skills (agents-bridge, brainstorm, decide, decision-briefing,
github-repo-care, rbx-dev, rbx-studio, roblox-live-verify, skill-explorer,
structured-thinking, think) sind Teil dieser 279 -- ihre Quelle ist mitrepariert;
Deploy nach `~/.claude/skills/` erfolgt separat ueber `skill_sync.py` aus dem
OneDrive-Mirror (siehe Ticket-Notiz unten).

## Verursacher (Teil 3)

Kein im Repo verbliebenes Script gefunden. Die Batch-Uebersetzung stammt aus
Commit `acfbb72` ("i18n(skills): complete 7-language multi-lingual expansion...",
2026-07-30) -- ein einmaliger Agenten-/Skript-Lauf, dessen Werkzeug selbst nie
committet wurde (kein zugehoeriges Script im Commit, keine Spur in
`tools/`/`scripts/`-Ordnern dieses Repos). `check_language_parity.py`
(bilingual-doc-sync) wurde geprueft: es liest nur, schreibt keine
`description:`-Felder -- kein Risiko einer Wiederholung durch dieses Script.
Da kein Verursacher-Script mehr existiert, das gepatcht werden koennte, ist das
neue CI-Gate (Teil 4) der einzige belastbare Schutz gegen Wiederholung,
unabhaengig davon, welches Werkzeug eine kuenftige Batch-Uebersetzung schreibt.

## CI-Gate (Teil 4)

`testing/frontmatter_yaml_gate.py` + `testing/test_frontmatter_yaml_gate.py`
(automatisch von `pytest` erfasst, `testpaths` in `pyproject.toml` deckt
`testing/` bereits ab -- kein Workflow-Eintrag noetig). Prueft jede echte
`SKILL*.md` (Vorlagen-Assets ausgeschlossen) mit `yaml.safe_load` und dass das
Ergebnis ein Mapping ist.

## Verifikation

- `python testing/frontmatter_yaml_gate.py`: vorher 279 Verstoesse, Exit 1;
  nachher "1060 SKILL*.md-Dateien geprueft", Exit 0.
- `python -m pytest -ra -q`: 433 passed (430 bestehende + 3 neue,
  minus false-positive-Ausschluss der Vorlagen).
- `ruff check .`: All checks passed.
- `python build_public_registry.py --check` / `build_skills_map.py --check`:
  aktuell.

## Zusaetzlich noetig: zwei vorbestehende, unabhaengige Bugs

Der lokale `skill-static-s-tests`-Pre-Commit-Hook (`testing/skill_tester.py batch
--type static --ci <geaenderte SKILL.md-Dateien>`) blockierte den Commit --
reproduziert auf dem unveraenderten `origin/master` mit derselben Dateiliste
(identisches Ergebnis, 27/116 bestanden), also NICHT durch die Requotierung
verursacht:

1. **`category`-Pruefung falsch fuer Uebersetzungs-Unterordner:** Fuer
   `skills/utilities/think/en/SKILL.md` verglich `frontmatter_gate_errors()`
   `category: utilities` gegen den Ordner `en/` statt gegen `utilities/` (eine
   Ebene zu flach, weil der Sprachordner nicht mitgezaehlt wurde). Betraf jede
   Uebersetzung jedes Skills mit `<lang>/SKILL.md`-Unterordner -- 89 der 116
   gemeldeten Falschbefunde. Fix in `testing/skill_tester.py`
   (`frontmatter_gate_errors`): wenn `inherits_visibility()` True ist (Sprach-
   Unterordner erkannt), eine Ordnerebene weiter nach oben vergleichen.
2. **3 echte Luecken:** `skills/utilities/lebende-verfassung/{en,es,ru}/SKILL.md`
   fehlte das Pflichtfeld `standalone` (die anderen Sprachvarianten haben es).
   Ergaenzt (`standalone: true`, wie in der deutschen Primaerfassung).

Beide Funde sind unabhaengig vom YAML-Requoting, aber noetig, um den Commit
ueberhaupt durch den vorhandenen Hook zu bekommen -- ohne sie waere jeder
Commit an einer Uebersetzungsdatei blockiert gewesen, nicht nur dieser.
Verifiziert: `python testing/skill_tester.py batch --type static --ci <die
116 geaenderten SKILL.md>` -> 116/116 bestanden, Exit 0 (vorher 27/116, Exit 1,
identisch auf master reproduziert).

## Nicht Teil dieser Aenderung

- Der OneDrive-Mirror (`.TOPICS/.AI/.SKILLS`) und der Deploy-Schritt
  (`skill_sync.py deploy <skill>`) werden separat behandelt -- dieses Repo ist
  laut `REPO.pointer.json` die Quelle der Wahrheit (`authority.git:
  local-checkout-plus-github`), der Mirror ist ein abgeleiteter Read-Surface.
