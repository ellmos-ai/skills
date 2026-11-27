# Änderungsverlauf

## 0.3.0 — 2026-11-27

- Externe Konfiguration `agenda-config.json` (Horizonte, Gewichtsgrenzen, Anzeige-/Hook-Limits, Selbstheilung mit `.corrupt.<ts>.bak`) an `scripts/agenda.py` und `scripts/agenda_hook.py` angebunden.
- Austauschbare Ausgabe-Vorlagen `templates/agenda-overview.template.md` und `templates/agenda-board.template.html` ergänzt, `summary --format html` aktiviert und `tests/test_agenda.py` erweitert.

## 0.2.0 — 2026-11-25

- Optionale rückwärtskompatible Punkt-Felder `timeframe`, `owner` (`user`/`self`/`team`/`shared` oder kleingeschriebener Owner-Slug) und `category` ergänzt (inkl. Validierung in `read()`).
- `add` um `--timeframe`, `--owner`, `--category` erweitert.
- Neuer nicht-destruktiver Subcommand `update <ID>` zum gezielten Aktualisieren und reversiblen Zurücksetzen (`""`/`none`/`-`) von `--timeframe`, `--owner`, `--category` sowie Aktualisieren von `--text` und `--weight` unter Erhalt bestehender `plans` und `status`.
- Neuer Lese-Subcommand `summary` (`--format markdown|text|json`, `--timeframe`, `--exact`, `--include-ongoing`, `--owner`, `--category`, `--group-by timeframe|category|owner`, `--output PFAD`) mit Zeitraum-Overlap-Matching und atomarem Datei-Export.
- `agenda_hook.py` gibt gesetzte `timeframe`/`owner`/`category`-Felder kompakt mit aus.

## 0.1.1 — 2026-11-22

`add 'TEXT' [--weight N]`: einzelnen Punkt mit der nächsten freien ID ergänzen, ohne `set` (Agenda-ID, Aktivität, Deadline und bestehende Punkt-IDs bleiben erhalten).

## 0.1.0 — 2026-10-21

Erste neutrale Fassung mit privatem Zustand, Revisionsprüfung und Anbieteranbindung.
