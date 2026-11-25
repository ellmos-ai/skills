# Änderungsverlauf

## 0.2.0 — 2026-11-25

- Optionale rückwärtskompatible Punkt-Felder `timeframe`, `owner` (`lukas`/`team`/`shared`) und `category` ergänzt (inkl. Validierung in `read()`).
- `add` um `--timeframe`, `--owner`, `--category` erweitert.
- Neuer nicht-destruktiver Subcommand `update <ID>` zum gezielten Aktualisieren von `--text`, `--weight`, `--timeframe`, `--owner`, `--category` unter Erhalt bestehender `plans` und `status`.
- Neuer Lese-Subcommand `summary` (`--format markdown|text|json`, `--timeframe`, `--exact`, `--include-ongoing`, `--owner`, `--category`, `--group-by timeframe|category|owner`, `--output PFAD`) mit Zeitraum-Overlap-Matching und atomarem Datei-Export.
- `agenda_hook.py` gibt gesetzte `timeframe`/`owner`/`category`-Felder kompakt mit aus.

## 0.1.1 — 2026-11-22

`add 'TEXT' [--weight N]`: einzelnen Punkt mit der nächsten freien ID ergänzen, ohne `set` (Agenda-ID, Aktivität, Deadline und bestehende Punkt-IDs bleiben erhalten).

## 0.1.0 — 2026-10-21

Erste neutrale Fassung mit privatem Zustand, Revisionsprüfung und Anbieteranbindung.
