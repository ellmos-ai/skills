# Plugin / Extension — Paritaet zwischen Claude Code und Claude Desktop

> Stand: 2026-04-30. Reference-Datei zum Skill `mcp-config-sync`.

## Drei getrennte Erweiterungssysteme

Claude Code und Claude Desktop nutzen **unterschiedliche** Erweiterungssysteme:

| Bereich | Claude Code | Claude Desktop | Sync-Moeglichkeit |
|---|---|---|---|
| User-Skills | `~/.claude/skills/` | session-internem Pfad, kein User-Zugriff | nicht direkt — siehe `skills-sync-options.md` |
| Plugins | `enabledPlugins` in `settings.json` plus Marketplace | "Claude Extensions" als eigenes Format | **paritaere Mapping-Tabelle**, manuelle Doppel-Installation |
| MCP-Server | `~/.claude/profiles/*.json` (mit `--mcp-config`) | `mcpServers` in `claude_desktop_config.json` | **automatisch** via `sync-tools.ps1` / `.sh` |

## Funktionale Paritaet

| Funktionsbereich | Claude Code Plugin | Claude Desktop Extension | Status |
|---|---|---|---|
| Aktuelle Lib-Doku | `context7@claude-plugins-official` | `context7` | beidseitig vorhanden |
| Filesystem-Zugriff | (built-in via Bash/Edit) | `ant.dir.ant.anthropic.filesystem` | nur Desktop |
| Desktop-Steuerung | (built-in via computer-use) | `ant.dir.gh.wonderwhy-er.desktopcommandermcp` | nur Desktop |
| GitHub | `github@claude-plugins-official` | (manuell via MCP-Server) | nur Code |
| Frontend-Design | `frontend-design@claude-plugins-official` | — | nur Code |
| Code-Review | `code-review@claude-plugins-official` | — | nur Code |
| Vercel-Deploy | `vercel@claude-plugins-official` | — | nur Code |
| Skill-Erstellung | `skill-creator@claude-plugins-official` | — | nur Code |
| CLAUDE.md-Pflege | `claude-md-management@claude-plugins-official` | — | nur Code |
| Codex-Integration | `codex@openai-codex` | — | nur Code |
| Plugin-Entwicklung | `plugin-dev@claude-plugins-official` | — | nur Code |
| Hooks | `hookify@claude-plugins-official` | — | nur Code |
| Datenbanken | `supabase@claude-plugins-official` | `ant.dir.gh.jerichosequitin.metabase` | jeweils eigen |
| Security | — | `ant.dir.gh.socketdev.socket-mcp` | nur Desktop |
| PDF | (Anthropic-Skill `pdf`) | `ant.dir.gh.silverstein.pdf-filler-simple` + `pdf-viewer` (MCP) | jeweils eigen |
| HTML-Generator | — | `website-generator` | nur Desktop |
| Public Health | — | `ant.dir.gh.cicatriiz.pophive` | nur Desktop |
| Big-Data-Markets | `bigdata-com@claude-plugins-official` | — | nur Code |
| Loop-Workflows | `ralph-loop@claude-plugins-official` | — | nur Code |
| Superpowers | `superpowers@claude-plugins-official` | — | nur Code |
| Feature-Dev | `feature-dev@claude-plugins-official` | — | nur Code |
| Code-Simplifier | `code-simplifier@claude-plugins-official` | — | nur Code |

**Kernbeobachtung:** Die beiden Toolkits sind komplementaer, nicht ueberlappend. Claude Code ist auf Code-/Build-Workflows zentriert, Claude Desktop auf Office-/System-Workflows.

## Empfehlung

- **Nicht** versuchen, beide Listen identisch zu halten — sie sind mit Absicht unterschiedlich.
- `context7` ist der einzige sinnvolle Doppel-Eintrag und ist beidseitig vorhanden.
- Wenn ein neues Plugin in Claude Code installiert wird, das eine eigene MCP-Server-Komponente mitbringt: pruefen, ob es als Extension auch fuer Claude Desktop verfuegbar ist — falls ja, beide installieren.
