# Legacy: wie `mcp-config-sync` in `agent-config-sync` aufgeht

> Reference-Datei zum Skill `agent-config-sync`. Stand: 2026-06-20.

## Was der alte Skill ist

`mcp-config-sync` (v1.0.1) synchronisiert **nur MCP-Server**, **nur** zwischen **Claude Code
und Claude Desktop**, auf **einem** Rechner, ueber ein dediziertes Skript pro OS
(`sync-tools.ps1` / `sync-tools.sh`) plus eine Master-Datei (`_shared-mcp.json`).

## Abbildung auf das neue Modell

Der Legacy-Fall ist exakt **eine Registry-Beziehung** im neuen Skill:

```json
{
  "name": "claude-pair",
  "members": ["claude-code", "claude-desktop"],
  "mode": "pull",
  "source": "claude-code",
  "scope": "mcp"
}
```

- Die alte **Master-Datei** entspricht der **Quelle** (`source`) der Beziehung.
- Das alte **OS-Skript** entspricht der **block-replace**-Schreiblogik in
  `config.json` (`claude-desktop.mcp.merge = "block-replace"`), inkl. Zeitstempel-Backup.
- Die Reference-Dateien des Altskills bleiben gueltig und werden hier weiterverwendet:
  - `mcp-config-sync/references/skills-sync-options.md` (Claude Desktop liest
    `~/.claude/skills/` nicht direkt → Bridge-Skill)
  - `mcp-config-sync/references/plugin-extension-parity.md` (Plugins/Extensions sind
    komplementaer, NICHT Aufgabe dieses Skills)

## Migrationsempfehlung

- **Vorerst koexistieren lassen.** `mcp-config-sync` bleibt als funktionierender Legacy-Pfad
  fuer den Claude-Code↔Desktop-MCP-Fall bestehen, bis `agent-config-sync` ein getestetes
  `--apply` hat.
- **Nach `--apply`-Reife:** `mcp-config-sync` als `deprecated` markieren (Frontmatter
  `status: deprecated`) und in seiner SKILL.md auf `agent-config-sync` verweisen. Die
  bewaehrten OS-Skripte koennen als interne Schreib-Backends uebernommen werden.
- **Nicht** die Dateien des Altskills jetzt veraendern — dieser Skill referenziert sie nur.
