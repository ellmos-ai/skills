# Ergebnis: letter-hooker nutzerneutral

session: 01a0e03a-d5fc-79e3-b6d5-c8ce58cc5cbb | codex | 2026-09-27

## Neu

- Vier eigenständige Hooks unter `skills/infrastructure/letter-hooker/hooks/` für Dokument-Traversierung, Gardener-/Memory-Preflight, Lock-/Git-Hygiene sowie Pfad- und Quellenautorität.
- Portabler Loader unter `skills/infrastructure/letter-hooker/scripts/agy_kontext_and_workflow_loader.py`, dazu `config.example.json` und ein `.gitignore` für die lokale `config.json`.

## Geändert

- Alle acht Letter-Hooker-Anleitungen (`SKILL.md` und sieben Sprachfassungen): relative Hook-Links, Skill-lokaler Loader-Aufruf, konfigurierbare Stichwortliste und aufgelöste Python-Dependency.
- `skills/infrastructure/automation-self-care/SKILL.de.md`: Policy als optionale lokale Konfiguration beschrieben und die vier gebündelten Hooks verknüpft.

## Verifikation

- `python testing/privacy_gate.py` — Exit 0.
- `python -m pytest testing/ -q` — 150 bestanden.
- `python build_public_registry.py --check` — aktuell.
- `python build_skills_map.py --check` — aktuell.
- `python testing/skill_tester.py batch --type static --ci skills/infrastructure/letter-hooker/SKILL.md` — 1/1 bestanden.
- Konfigurations-Smoke-Test: Pfadüberschreibungen, Skill-Mapping-Erweiterung/-Überschreibung, Host-Slot-Umgebungsvariable und Auflösung aller Standard-Mappings geprüft.
- `git diff --cached --check` — sauber.

## Nebenbefund

Ein vorhandener Verweis in `automation-self-care/SKILL.de.md` auf `references/provider-profiles.md` zeigt auf eine nicht vorhandene Datei. Er war nicht Teil des Hook-Umbaus und blieb unverändert; alle neu gesetzten Hook-Links lösen sich auf.
