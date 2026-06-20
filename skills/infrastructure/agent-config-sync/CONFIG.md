# CONFIG — Anbieter-Standardspezifikationen

> Publizierbar/neutral. Nur Platzhalter, keine echten Personen-Pfade.
> Maschinenlesbares Gegenstueck: `config.json`. Wird vom Lernmechanismus aktualisiert
> (Feld `sources` + `updated` je Anbieter).

Diese Datei beschreibt **je Agent-Anbieter**, wo dessen MCP- und/oder Skill-Konfiguration
liegt und in welchem Format. Pfade nutzen `<HOME>` (= `~` bzw. `%USERPROFILE%`),
`<APPDATA>` (Windows `%APPDATA%`), `<APPSUPPORT>` (macOS `~/Library/Application Support`).

## Felder je Anbieter (`config.json`)

| Feld | Bedeutung |
|---|---|
| `display_name` | Menschlicher Name |
| `kind` | `app` (GUI) \| `cli` \| `ide` |
| `mcp.path` | Datei/Ordner der MCP-Konfiguration (Platzhalter) |
| `mcp.format` | `json` \| `toml` \| `none` |
| `mcp.key` | JSON/TOML-Schluessel des MCP-Server-Blocks (z.B. `mcpServers`) |
| `mcp.merge` | `block-replace` (nur den Block ersetzen, Rest erhalten) \| `file` |
| `skills.path` | Ordner/Datei fuer Skills (oder `null` wenn nicht unterstuetzt) |
| `skills.kind` | `dir` \| `redirect` \| `none` |
| `notes` | Eigenheiten / Fallstricke |
| `sources` | Quellen-Hinweise (URL/Doku/Stand) fuer den Lernmechanismus |
| `updated` | letztes Verifikationsdatum dieses Eintrags |

## Anbieter (Stand 2026-06-20)

| Anbieter | MCP-Ort (Platzhalter) | Format | MCP-Key | Skills | Eigenheit |
|---|---|---|---|---|---|
| **Claude Code** | `<HOME>/.claude/profiles/<name>.json` (via `--mcp-config`) bzw. `<HOME>/.claude.json` | json | `mcpServers` | `<HOME>/.claude/skills/` (dir) | profilbasiert; Sammel-Deploy via `skill_sync.py` |
| **Claude Desktop** | Win `<APPDATA>/Claude/claude_desktop_config.json`, Mac `<APPSUPPORT>/Claude/claude_desktop_config.json` | json | `mcpServers` | session-intern, **kein direkter Zugriff** → Bridge-Skill | komplett beenden+neustarten noetig |
| **Codex CLI (GPT)** | `<HOME>/.codex/config.toml` | toml | `mcp_servers` | `<HOME>/.codex/` (+ `GPT.md`) | TOML, nicht JSON; Stop-Parsing bei `--%` beachten |
| **Antigravity / Gemini (agy)** | `<HOME>/.gemini/` (config + `GEMINI.md`) | json/dir | (zu verifizieren) | `<HOME>/.gemini/config/plugins/.../skills/` | MCP-Schema per Lernmechanismus verifizieren |
| **Kimi Code** | `<HOME>/.kimi-code/` | json | (zu verifizieren) | (zu verifizieren) | Logs in `<HOME>/.kimi-code/` |
| **Cursor** | `<HOME>/.cursor/mcp.json` bzw. `<projekt>/.cursor/mcp.json` | json | `mcpServers` | `<projekt>/.cursor/rules/*.mdc` (redirect) | projekt- vs. global-scope |
| **Cline (VS Code)** | VS-Code-globalStorage `cline_mcp_settings.json` | json | `mcpServers` | `.clinerules` (redirect) | Pfad per Lernmechanismus aufloesen |
| **Windsurf** | `<HOME>/.codeium/windsurf/mcp_config.json` | json | `mcpServers` | `.windsurfrules` (redirect) | zu verifizieren |
| **GitHub Copilot** | `.vscode/mcp.json` bzw. Settings | json | `servers` | `.github/copilot-instructions.md` (redirect) | abweichender Key `servers` |

> **Wichtig:** Eintraege mit "(zu verifizieren)" sind **nicht** als gesicherte Tatsachen zu
> behandeln. Vor einem echten Sync gegen sie den **Lernmechanismus** laufen lassen
> (WebSearch + Context7 + Systemsuche) und `config.json` aktualisieren. Die hier gefuehrten
> Pfade sind Standard-Annahmen, kein Beweis fuer das konkrete System (dafuer: `cache.json`).

## Format-Eigenheiten

- **JSON ↔ TOML:** Codex nutzt `config.toml` mit Tabelle `[mcp_servers.<name>]`; beim
  Verteilen aus einer JSON-Quelle muss umgewandelt werden (Key-Mapping `mcpServers` →
  `mcp_servers`).
- **block-replace:** Fuer `claude_desktop_config.json` und aehnliche Multi-Feld-Configs nur
  den MCP-Block ersetzen, niemals die ganze Datei (sonst gehen `preferences` etc. verloren).
- **redirect-skills:** IDE-„Regeln"-Dateien sind keine Skill-Verzeichnisse; fuer sie ist
  `agents-bridge` zustaendig, nicht dieser Skill. Hier nur als Hinweis gefuehrt.
