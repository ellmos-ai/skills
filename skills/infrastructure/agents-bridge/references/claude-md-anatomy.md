# Anatomie der globalen CLAUDE.md

> Reference-Datei zum Skill `agents-bridge`. Welche Sektionen hat die globale `~/CLAUDE.md` und wofuer sind sie da?

## Zwei Ebenen

1. **`~/CLAUDE.md`** — globale Regeln, die auf jedem Rechner gelten (Sprache, Encoding, OS-Stolperfallen, User-Profil)
2. **`~/OneDrive/CLAUDE.md`** — Projekt- und Ordnerstruktur (Wo liegt was in OneDrive)
3. **`<projekt>/CLAUDE.md`** — projektspezifisch (siehe Template unter `~/OneDrive/.TOPICS/.AI/_templates/project-docs/CLAUDE.md`)

## Standard-Sektionen in der globalen CLAUDE.md

| Sektion | Zweck |
|---|---|
| Sprache | Deutsch als Default, Umlaut-Konvention |
| Faktentreue | Keine erfundenen Zeitangaben, keine falschen Verifizierbarkeitsclaims |
| Das KI-Team | Claude / Gemini / GPT als drei Musketiere |
| User | Name, Standort, GitHub |
| System: Windows 11 + Git Bash | Encoding-Falle, NUL, &&, sqlite3 CLI fehlt |
| OneDrive | File-Locking, .venv-Verbot, grosse Binaer-Dateien |
| GitHub / Git | .gitignore-Regeln, Credential-Verbot |
| GUI-Entwicklung | PySide6 statt PyQt6 |
| Arbeitsweise | 4-Augen-Prinzip fuer Hooks |
| Bearbeitungskonventionen | README-Vollstaendig-Lesen-Regel |
| Globale Tools | Liste der Standard-Tools |
| Nachrichten an Claude | Inbox fuer Cross-Agent-Messages |

## Aenderungs-Protokoll

Aenderungen werden mit Kuerzel markiert: `[C YYYY-MM-DD Thema]`, wobei:
- `[C]` = Claude
- `[G]` = Gemini
- `[P]` = GPT
- `[U]` = User

Beispiel: `## Faktentreue [C 2026-04-21]`.

## Wann die globale CLAUDE.md anpassen?

- **Neue Plattform-Stolperfalle** (z.B. macOS-spezifischer Encoding-Issue): unter "System" oder neue Sektion
- **Neue dauerhafte Konvention** (z.B. neue Naming-Regel fuer Repos): unter "Arbeitsweise"
- **Persoenliche Daten geaendert** (Standort, GitHub): unter "User"
- **Neue Beziehung zwischen Agenten**: unter "Das KI-Team"

## Wann NICHT anpassen?

- Projekt-spezifische Regeln gehoeren in `<projekt>/CLAUDE.md`
- Temporaere Notizen gehoeren in `~/.claude/memory/IMPORTED_LESSONS.md` oder `LESSONS_NEW.md`
- IDE/Tool-spezifische Konventionen gehoeren in die jeweilige Bootstrap-Datei der IDE

## Multi-Agent-Setup

Der "Multi-Agent"-Block in der globalen CLAUDE.md ist nur skizziert. Detail-Ausgestaltung pro Projekt:
- Project-Template hat einen ausfuehrlichen `agents:`-Block (`~/OneDrive/.TOPICS/.AI/_templates/project-docs/CLAUDE.md`)
- Im konkreten Projekt: nur ausfuellen, wenn das Projekt mehrere AI-Agents orchestriert (Boss + Experten oder parallele Rollen)
