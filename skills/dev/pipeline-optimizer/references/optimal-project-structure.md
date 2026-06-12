# Optimale Projektordner-Struktur

> Referenz-Dokument für den Pipeline-Optimizer / Projekt-Ordner-Optimizer.
> Beschreibt die empfohlene Projektordner-Struktur für Claude Code + Multi-Agent-Setups.
> Pfade wie `<workspace>` oder `<pipeline>` sind Platzhalter — durch die eigene Struktur ersetzen.

---

## 1. Anthropic-Standard (Claude Code)

Anthropic Claude Code lädt **automatisch** beim Session-Start:

| Datei/Ordner | Funktion | Pflicht? |
|---|---|:---:|
| `CLAUDE.md` (Root) | Projekt-spezifische Anweisungen für Claude | **Ja** (für Anthropic-Kompatibilität) |
| `.claude/settings.json` | Projekt-Settings: Permissions, Env-Vars, Hooks | empfohlen |
| `.claude/settings.local.json` | Lokale Overrides (NICHT committen, in `.gitignore`) | optional |
| `.claude/commands/*.md` | Custom Slash-Commands | optional |
| `.claude/agents/*.md` | Custom Subagents | optional |
| `.claude/skills/<name>/SKILL.md` | Projekt-spezifische Skills | optional |
| `.claude/hooks/` | Hook-Skripte | optional |

### Standard-Inhalt `.claude/settings.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(uv run pytest:*)",
      "Read(./**)",
      "Edit(./**)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ]
  },
  "env": {
    "PYTHONIOENCODING": "utf-8"
  }
}
```

### Standard-Inhalt `.claude/settings.local.json` (NICHT committen!)

```json
{
  "permissions": {
    "allow": [
      "Bash(echo $MY_SECRET:*)"
    ]
  },
  "env": {
    "MY_API_KEY": "loaded-from-password-manager"
  }
}
```

### `.gitignore`-Einträge (Pflicht)

```gitignore
.claude/settings.local.json
.claude/.cache/
.claude/state/
```

---

## 2. Eigenes Projekt-Doku-Template

Empfehlung: ein eigenes, Anthropic-kompatibles Template pflegen, z.B. unter:

```
<workspace>/_templates/project-docs/
```

### Template-Struktur

```
project-docs/
├── CLAUDE.md          # Auto-loaded für Claude Code — Projekt-Anweisungen
├── AGENTS.md          # Redirect für Codex/Cursor/Aider/Cline auf CLAUDE.md
├── README.md          # Projekt-Übersicht (für Menschen + GitHub)
├── ARCHITECTURE.md    # Technische Architektur
├── DECISIONS.md       # ADRs (Architecture Decision Records)
├── PATTERNS.md        # Anti-Patterns + bewährte Patterns
├── GLOSSARY.md        # Projektspezifische Begriffe
├── CHANGELOG.md       # Versionshistorie (Keep-a-Changelog Format)
├── TODO.md            # Aktive Aufgaben
├── DONE.md            # Abgeschlossene Aufgaben (aus TODO.md archiviert)
├── STATE.md           # Aktueller Stand der letzten Session
├── START.md           # Imperative Bootstrap-Sequenz für Sessions
├── TOOLS.md           # Welches Tool macht was
├── TEMPLATE.md        # Skelett für neue Markdown-Dateien
├── .github/           # GitHub-spezifische Konfiguration
├── _tools/            # Projekt-eigene Hilfsskripte
└── workflows/         # Workflow-Dokumentationen
```

### YAML-Header für Markdown-Dateien (Konvention)

Alle größeren MD-Dateien haben einen YAML-Frontmatter-Header für maschinelle Lesbarkeit:

```yaml
---
name: [project-name]
type: project-docs
profile: [MINIMAL|STANDARD|FULL]
version: 0.1.0
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
last_verified: [YYYY-MM-DD]
author: [author]
anthropic_compatible: true
description: |
  Project-specific instructions for AI coding agents in [project-name].
---
```

Ein kleines Lint-Script (z.B. `_tools/doc-lint`) kann den Header validieren.

### Drei Profile

Die Konvention unterscheidet **drei Detail-Stufen** je nach Projektgröße:

| Profile | Anwendung | Pflicht-Dateien |
|---|---|---|
| **MINIMAL** | Kleine Projekte, Proof-of-Concepts | AGENTS.md, CLAUDE.md, README.md, START.md, STATE.md, TODO.md, DONE.md |
| **STANDARD** | Normale Projekte (90% Fall) | + CHANGELOG.md, DECISIONS.md, PATTERNS.md |
| **FULL** | Komplexe Suiten, mehrere Mitwirkende | + ARCHITECTURE.md, WORKFLOWS.md, TOOLS.md, GLOSSARY.md, `.github/`, `workflows/` |

---

## 3. Pipeline-spezifische Ergänzungen (Beispiele)

### Software-Pipeline-Projekte (zusätzlich zu Anthropic + Doku-Template)

| Datei | Funktion | Quelle |
|---|---|---|
| `LICENSE` | Lizenz (MIT/Apache/GPL/Proprietary) | aus Pipeline-Templates |
| `CODE_OF_CONDUCT.md` | Verhaltenskodex | aus Pipeline-Templates |
| `SECURITY.md` | Vulnerability Reporting | aus Pipeline-Templates |
| `CONTRIBUTING.md` | Beitragsrichtlinie | aus Pipeline-Templates |
| `THIRD_PARTY_LICENSES.txt` | Dritt-Lizenzen | generiert (z.B. Wrapper um `pip-licenses`) |
| `pyproject.toml` oder `requirements.txt` | Python-Deps | Cookiecutter-Template |
| Eintrag in zentraler Release-Registry | Pipeline-Übersicht | z.B. `releases.json` der Pipeline |
| `RELEASES.md` | Release-Übersicht pro Projekt | aus Pipeline-Templates |

**Empfehlung:** Bei neuen Software-Projekten ein **Cookiecutter-Template nutzen** statt manuell aufbauen:
```bash
cd <pipeline>/software/<themenordner>
python -m cookiecutter <pipeline>/software/_templates/cookiecutter-python-project
```

### Forschungs-Pipeline-Projekte

| Datei | Funktion |
|---|---|
| `KONZEPT.md` | Projektkonzept |
| `AKTIONSPLAN.md` | Operativer Plan inkl. Status-Log |
| `PUBLIKATIONSPLAN.md` | Publikationsstrategie |
| `TODO.md` / `DONE.md` | Aufgaben |
| Beweisnotiz (z.B. `BEWEISNOTIZ.md`) | (bei Beweis-Projekten) Beweiskette + Status |
| `_archive/` | Alte Versionen |
| `_sources/` | Originalquellen (PDFs, Datasets) |
| `_results/` | Berechnungsergebnisse |
| `_data/` | Inputdaten |
| `paper/` | LaTeX-Hauptdateien (z.B. `*_v[N]_en.tex`) |

**`NOTICE.md`** im Projektordner ist OK, wenn externe Instrumente/Datasets mit Lizenz-Tabelle dokumentiert werden müssen.

### Game-Pipeline-Projekte (Beispiel: Roblox/Rojo)

| Datei | Funktion |
|---|---|
| `default.project.json` | Rojo-Konfiguration (Pflicht) |
| `rokit.toml` | Tool-Versionen (Rojo, Lune, Wally) |
| `wally.toml` | Package-Deps |
| `selene.toml` | Linter-Konfiguration |
| `KONZEPT.md` | Game Design Document |
| `TODO.md` | Aufgaben + bekannte Bugs |
| `src/server/Main.server.luau` | **Einziger** Server-Entry |
| `src/client/GameClient.client.luau` | Client-Entry |
| `src/shared/Config.luau` + `GameEnums.luau` | Zentrale Konstanten |

---

## 4. Multi-Agent-Kompatibilität

Damit nicht-Claude-Agenten (Codex, Cursor, Aider, Cline, Antigravity) dieselben Regeln lesen können:

### `AGENTS.md` als Redirect

```markdown
# AGENTS.md

> Diese Datei richtet sich an nicht-Claude-Agents (Codex, Cursor, Cline, Aider,
> Windsurf, Copilot, JetBrains AI).
>
> **Die kanonische Quelle für Projekt-Anweisungen ist [`CLAUDE.md`](./CLAUDE.md)**
> in diesem Projekt — bitte dort lesen.
>
> Zusätzlich gelten:
> - Globale User-Regeln: `~/CLAUDE.md` (oder Tool-spezifischer Mirror)
```

So gibt es **eine** Quelle der Wahrheit pro Projekt; alle anderen Agent-Konfigurationsdateien verweisen nur darauf.

---

## 5. Anti-Patterns (was NICHT in den Projektordner)

| Datei/Muster | Warum nicht | Wohin stattdessen |
|---|---|---|
| `.env` / `*.key` / `credentials.json` | Secrets | `.gitignore` + Passwort-Manager |
| `__pycache__/` / `.pytest_cache/` | Build-Artefakte | `.gitignore` |
| `.venv/` / `venv/` | Virtuelle Umgebungen | `.gitignore`, lokal generieren |
| Interne LLM-Aufgabendateien (in Release-Projekten) | Interne Kommunikation | nur im Dev-Stadium, vor Release entfernen |
| `Plan.txt` (in Release-Projekten) | Interne Planung | `.gitignore` |
| `_private/` | Private Inhalte | `.gitignore` |
| Große Binärdateien (`*.exe`, `*.msi`) | Repo-Bloat | GitHub Releases |
| `*.db` mit Nutzerdaten | Datenschutz (DSGVO) | `.gitignore`, Backup separat |

---

## 6. Empfohlener Workflow: Neuen Projektordner anlegen

### Software-Projekt

```bash
# 1. Aus Cookiecutter-Template generieren
cd <pipeline>/software/<themenordner>
python -m cookiecutter <pipeline>/software/_templates/cookiecutter-python-project

# 2. _templates/project-docs/ als Ergänzung kopieren
cp -r <workspace>/_templates/project-docs/{STATE.md,START.md,PATTERNS.md,GLOSSARY.md} ./

# 3. .claude/settings.json anlegen (siehe Abschnitt 1)
mkdir .claude
# ... settings.json schreiben

# 4. uv setup
uv venv
uv pip install -e .[dev]
uv run pytest  # smoke test

# 5. Registry-Eintrag (falls die Pipeline eine zentrale Registry führt)
```

### Forschungs-Projekt

```bash
# 1. Projektordner anlegen
cd <pipeline>/research/<themen-lab>
mkdir DRAFT__NeuesProjekt
cd DRAFT__NeuesProjekt

# 2. Pflichtdateien aus den Templates kopieren
cp <pipeline>/research/_templates/KONZEPT.md ./
cp <pipeline>/research/_templates/AKTIONSPLAN.md ./
cp <workspace>/_templates/project-docs/{TODO.md,DONE.md,CLAUDE.md,STATE.md} ./

# 3. Unterordner anlegen
mkdir paper _archive _sources _results _data

# 4. Status-Übersicht der Pipeline aktualisieren
```

### Game-Projekt (Beispiel Roblox)

```bash
# 1. Pipeline-Template kopieren
cd <pipeline>/games
cp -r _template NeuesGame
cd NeuesGame

# 2. Projekt-Doku aus _templates/project-docs/ ergänzen
cp <workspace>/_templates/project-docs/{CLAUDE.md,STATE.md,PATTERNS.md} ./

# 3. Toolchain-Setup
rokit install
wally install
```

---

## 7. Was ein „perfekter" Projektordner enthält (Quintessenz)

Für 90% aller Fälle (STANDARD-Profile) liefert dieser Skill folgendes als Empfehlung:

```
projektname/
├── CLAUDE.md              # Anthropic + LLM-Anweisungen
├── AGENTS.md              # Redirect für nicht-Claude-Agents
├── README.md              # Übersicht
├── STATE.md               # Aktueller Stand
├── TODO.md                # Aktive Aufgaben
├── DONE.md                # Erledigte Aufgaben
├── CHANGELOG.md           # Versionshistorie
├── ARCHITECTURE.md        # Technische Struktur
├── LICENSE                # Lizenz
├── .claude/
│   ├── settings.json      # Projekt-Settings (committed)
│   └── settings.local.json # Lokale Overrides (nicht committed)
├── START.md               # Session-Bootstrap
├── PATTERNS.md            # Do/Don't-Muster
├── DECISIONS.md           # ADR-/Warum-Achse
├── .gitignore             # mit .claude/settings.local.json + _private/
└── src/, tests/, docs/    # je nach Stack
```

**Plus pipeline-spezifische Pflichtdateien** (siehe Abschnitt 3).

---

## 8. Auto-Check-Befehl

Der Pipeline-Optimizer kann automatisch prüfen, ob ein Projektordner dem Standard entspricht:

```python
# Pseudocode für den Auto-Check
required_files = {
    "MINIMAL": ["AGENTS.md", "CLAUDE.md", "README.md", "START.md", "STATE.md", "TODO.md", "DONE.md"],
    "STANDARD": ["AGENTS.md", "CLAUDE.md", "README.md", "START.md", "STATE.md",
                 "TODO.md", "DONE.md", "CHANGELOG.md", "DECISIONS.md", "PATTERNS.md"],
    "FULL": ["AGENTS.md", "CLAUDE.md", "README.md", "START.md", "STATE.md", "TODO.md",
             "DONE.md", "CHANGELOG.md", "DECISIONS.md", "PATTERNS.md",
             "ARCHITECTURE.md", "WORKFLOWS.md", "TOOLS.md", "GLOSSARY.md"]
}
# Pro Pipeline zusätzliche Anforderungen aus Abschnitt 3
```

Mögliche Erweiterung: ein kleines Hilfsskript `pipeline-check.py`, das automatisch Lücken meldet (gehört in `_tools/` der jeweiligen Pipeline).
