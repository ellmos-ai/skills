# Agent- und IDE-Konventionen

Diese Tabelle ist eine Discovery-Hilfe, keine Festlegung der Wahrheit. Produkte
ändern ihre Boot-Mechanik; vor dem Schreiben muss die lokal installierte Version
oder die aktuelle Herstellerdokumentation geprüft werden.

| Familie | Häufige Boot-Fläche | Typischer Geltungsbereich |
|---|---|---|
| Codex-kompatible Agenten | `AGENTS.md` | Benutzer, Verzeichnis oder Projekt |
| Claude-Code-kompatible Agenten | `CLAUDE.md` | Benutzer, Verzeichnis oder Projekt |
| Gemini-kompatible Agenten | `GEMINI.md` | Benutzer oder Projekt |
| GitHub Copilot | `.github/copilot-instructions.md` | Repository |
| Cursor | `.cursor/rules/*.mdc` | Repository und Globs |
| Aider | `CONVENTIONS.md` plus Konfiguration | Projekt oder expliziter Aufruf |
| Cline | `.clinerules` oder produktabhängige Rules | Projekt |
| Windsurf | `.windsurfrules` oder produktabhängige Rules | Projekt |
| JetBrains-AI-Familie | IDE-Einstellungen oder Projektdatei | Benutzer oder Projekt |

## Discovery-Regeln

1. Vorhandene Dateien und Verzeichnisse nur inventarisieren.
2. Aus einem Dateinamen nicht schließen, dass er kanonisch ist.
3. Eine vom Tool automatisch geladene Datei kann selbst ein Loader sein.
4. Globale, System-, Workspace- und Projektregeln als getrennte Ebenen
   ausweisen.
5. Bei konkurrierenden Dateien die tatsächliche Lade- und Prioritätsreihenfolge
   testen.

## Verifikation

Der Lesetest soll eine harmlose, eindeutige Markerregel verwenden. Ein Agent
muss den Marker und seine Herkunft benennen können. Danach den Marker wieder
entfernen. Ein bloß vorhandener Dateipfad beweist keine aktive Übernahme.
