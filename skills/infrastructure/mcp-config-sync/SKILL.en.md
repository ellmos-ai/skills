---
name: mcp-config-sync
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-05-16
updated: 2026-06-13
description: >
  Synchronizes MCP servers between the agent apps Claude Code and Claude Desktop on the same machine. Triggers when the user wants to make an MCP server available in both apps, adds/changes/removes an MCP server, asks "why doesn't Claude Desktop see the server", "sync between claude-code and claude-desktop", "MCP in both", "shared mcp", or wants to coordinate plugins/extensions between both apps. Also use when migrating to a new system, as soon as both apps are installed, so that both share the same MCP state. The skill includes sync scripts for Windows (PowerShell) and macOS (zsh+jq) plus a master-file template.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [mcp, claude-code, claude-desktop, sync, windows, macos]
language: en
status: active

dependencies:
  tools: [powershell, jq]
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/mcp-config-sync/"
  origin_version: "1.0.0"
  last_sync_from_origin: "2026-05-16"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# MCP Config Sync

Synchronizes the three areas in which Claude Code and Claude Desktop can share content — MCP servers, skills status, plugin/extension parity.

## Overview — what can be synced?

| Area | Sync status | Mechanics |
|---|---|---|
| **MCP servers** | automatic | master file + script mirrors into both configs |
| **User skills** | partial | Claude Code reads `~/.claude/skills/`, Claude Desktop does not directly — see `references/skills-sync-options.md` |
| **Plugins/extensions** | mapping only | different marketplaces — see `references/plugin-extension-parity.md` |

## First-time setup

1. Create the master file at the target path:
   - Windows: `%USERPROFILE%\.claude\_shared-mcp.json`
   - macOS: `~/.claude/_shared-mcp.json`

   Template: `assets/_shared-mcp.template.json`. Adjust the paths for the respective system.

2. Place the sync script in the same location:
   - Windows: `scripts/sync-tools.ps1` -> `%USERPROFILE%\.claude\sync-tools.ps1`
   - macOS: `scripts/sync-tools.sh` -> `~/.claude/sync-tools.sh` (do not forget `chmod +x`)

3. macOS prerequisite: `brew install jq`

## Routine sync (every time after changing the master file)

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\sync-tools.ps1"
```

**macOS:**
```zsh
~/.claude/sync-tools.sh
```

**Afterwards:**
- Quit Claude Desktop **completely** (tray icon -> Quit, not just closing the window) and restart it
- In Claude Code, optionally start with `claude --mcp-config ~/.claude/profiles/shared.json`

## What happens during a sync?

The script takes the `mcpServers` block from the master file and writes it to two places:

1. **Claude Code**: `~/.claude/profiles/shared.json` (the file is completely overwritten — other profiles remain untouched)
2. **Claude Desktop**: `<AppData>/Claude/claude_desktop_config.json` — the `mcpServers` block is replaced, all other fields (`isUsingBuiltInNodeForMcp`, `preferences`, ...) are preserved. A timestamped backup is created first.

## Master-file schema

```json
{
  "_comment": "Optional, ignored.",
  "_stand": "YYYY-MM-DD",
  "mcpServers": {
    "<server-name>": {
      "command": "node | npx | absolute path",
      "args": ["..."],
      "env": { "OPTIONAL_VAR": "value" }
    }
  }
}
```

Additional top-level fields are ignored by the script. For absolute paths that are cross-platform, use slash paths in the master (`C:/Users/<user>/...`) — Windows accepts both, macOS uses forward slashes anyway.

## When an MCP server should run in only one app

Do not add it to the master file. Instead:
- Claude Code only: add it to another profile file (`~/.claude/profiles/<name>.json`), then `claude --mcp-config ...`
- Claude Desktop only: add it manually to `claude_desktop_config.json` — note the warning below.

> **Caution:** When a new master sync runs, any server not listed in the master file is lost in Claude Desktop. If Claude-Desktop-only servers are to be maintained, **always enter them manually in the master file** and make the script the only writer — otherwise they will be lost on the next sync.

## Layout of this skill

```
mcp-config-sync/
├── SKILL.md (German primary version)
├── SKILL.en.md (this file)
├── scripts/
│   ├── sync-tools.ps1    Windows sync (PowerShell)
│   └── sync-tools.sh     macOS sync (zsh+jq)
├── assets/
│   └── _shared-mcp.template.json  master-file template
└── references/
    ├── plugin-extension-parity.md  mapping Claude Code plugins ↔ Claude Desktop extensions
    └── skills-sync-options.md      options to make user skills usable in Claude Desktop too
```

For most requests, the SKILL.md is sufficient. Only read the reference files when the user explicitly asks about plugin mapping or skills-sync options.

## Anti-patterns

- Do **not** hand-edit the `mcpServers` block in `claude_desktop_config.json` when the master file is the source of truth — the next sync will overwrite it.
- Do **not** try to bind the skill directory `~/.claude/skills/` via junction into Claude Desktop's session-internal skill path — this is fragile and regularly destroyed by Anthropic updates. Use an index/bridge skill instead (see `references/skills-sync-options.md`, option 1).
- Do **not** try to mirror Claude Code plugins and Claude Desktop extensions 1:1 — the toolkits are complementary, not mirrorable.

---

## Changelog

### 1.0.1 (2026-06-13)
- First publication in the skill library: hardcoded user paths in SKILL.md, sync script, and master template replaced with `%USERPROFILE%`/`$HOME` placeholders

### 1.0.0 (2026-05-16)
- Initial version: master file + sync scripts (Windows/macOS), plugin-parity and skills-sync references
