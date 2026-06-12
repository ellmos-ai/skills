---
name: mcp-config-sync
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-05-16
updated: 2026-06-13
description: >
  Synchronisiert MCP-Server zwischen den Agent-Apps Claude Code und Claude Desktop auf demselben Rechner. Aktiviert sich, wenn der User einen MCP-Server in beiden Apps verfuegbar machen will, einen MCP-Server hinzufuegt/aendert/entfernt, fragt "warum sieht Claude Desktop den Server nicht", "sync zwischen claude-code und claude-desktop", "MCP in beiden", "shared mcp", oder Plugins/Extensions zwischen beiden Apps koordinieren will. Auch beim Umzug auf ein neues System nutzen, sobald beide Apps installiert sind, damit beide denselben MCP-Stand haben. Skill enthaelt Sync-Skripte fuer Windows (PowerShell) und macOS (zsh+jq) sowie eine Master-Datei-Vorlage.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [mcp, claude-code, claude-desktop, sync, windows, macos]
language: de
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

Synchronisiert die drei Bereiche, in denen Claude Code und Claude Desktop sich Inhalte teilen koennen — MCP-Server, Skills-Status, Plugin/Extension-Paritaet.

## Ueberblick — was ist synchronisierbar?

| Bereich | Sync-Status | Mechanik |
|---|---|---|
| **MCP-Server** | automatisch | Master-Datei + Skript spiegelt in beide Configs |
| **User-Skills** | teilweise | Claude Code liest `~/.claude/skills/`, Claude Desktop nicht direkt — siehe `references/skills-sync-options.md` |
| **Plugins/Extensions** | nur Mapping | unterschiedliche Marketplaces — siehe `references/plugin-extension-parity.md` |

## Erstmaliger Setup

1. Master-Datei am Ziel-Pfad anlegen:
   - Windows: `%USERPROFILE%\.claude\_shared-mcp.json`
   - macOS: `~/.claude/_shared-mcp.json`

   Vorlage: `assets/_shared-mcp.template.json`. Pfade fuer das jeweilige System anpassen.

2. Sync-Skript am gleichen Ort ablegen:
   - Windows: `scripts/sync-tools.ps1` -> `%USERPROFILE%\.claude\sync-tools.ps1`
   - macOS: `scripts/sync-tools.sh` -> `~/.claude/sync-tools.sh` (`chmod +x` nicht vergessen)

3. macOS-Voraussetzung: `brew install jq`

## Routine-Sync (jedes Mal nach Aenderung der Master-Datei)

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\sync-tools.ps1"
```

**macOS:**
```zsh
~/.claude/sync-tools.sh
```

**Danach:**
- Claude Desktop **vollstaendig** beenden (Tray-Icon -> Quit, nicht nur Fenster schliessen) und neu starten
- In Claude Code wahlweise mit `claude --mcp-config ~/.claude/profiles/shared.json` starten

## Was passiert beim Sync?

Das Skript nimmt den `mcpServers`-Block aus der Master-Datei und schreibt ihn an zwei Stellen:

1. **Claude Code**: `~/.claude/profiles/shared.json` (Datei wird komplett ueberschrieben — andere Profile bleiben unberuehrt)
2. **Claude Desktop**: `<AppData>/Claude/claude_desktop_config.json` — der `mcpServers`-Block wird ersetzt, alle anderen Felder (`isUsingBuiltInNodeForMcp`, `preferences`, ...) bleiben erhalten. Vorher wird ein Backup mit Zeitstempel angelegt.

## Master-Datei-Schema

```json
{
  "_comment": "Optional, wird ignoriert.",
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

Zusaetzliche Top-Level-Felder werden vom Skript ignoriert. Fuer absolute Pfade, die plattformuebergreifend sind, im Master Slash-Pfade (`C:/Users/<user>/...`) verwenden — Windows akzeptiert beides, macOS nutzt eh Forward-Slashes.

## Wenn ein MCP-Server nur in einer App laufen soll

Nicht in die Master-Datei aufnehmen. Stattdessen:
- Claude Code only: in einem anderen Profile-File (`~/.claude/profiles/<name>.json`) eintragen, dann `claude --mcp-config ...`
- Claude Desktop only: per Hand in `claude_desktop_config.json` ergaenzen — der Sync-Lauf laesst andere Server in der Config unangetastet, weil er nur den `mcpServers`-Block ersetzt.

> **Beachten:** Wenn ein neuer Master-Sync laeuft, geht der nicht in der Master-Datei stehende Server in Claude Desktop verloren. Wenn Claude-Desktop-only-Server gepflegt werden sollen, **immer manuell in der Master-Datei eintragen** und das Skript zum einzigen Schreiber machen — sonst gehen sie beim naechsten Sync verloren.

## Aufbau dieses Skills

```
mcp-config-sync/
├── SKILL.md (diese Datei)
├── scripts/
│   ├── sync-tools.ps1    Windows-Sync (PowerShell)
│   └── sync-tools.sh     macOS-Sync (zsh+jq)
├── assets/
│   └── _shared-mcp.template.json  Master-Datei-Vorlage
└── references/
    ├── plugin-extension-parity.md  Mapping Claude-Code-Plugins ↔ Claude-Desktop-Extensions
    └── skills-sync-options.md      Optionen, User-Skills auch in Claude Desktop nutzbar zu machen
```

Bei den meisten Anfragen reicht die SKILL.md. Reference-Dateien nur dann lesen, wenn der User explizit nach Plugin-Mapping oder Skills-Sync-Optionen fragt.

## Anti-Pattern

- **Nicht** den `mcpServers`-Block in `claude_desktop_config.json` haendisch editieren, wenn die Master-Datei der wahre Quellort ist — der naechste Sync ueberschreibt das.
- **Nicht** versuchen, das Skill-Verzeichnis `~/.claude/skills/` per Junction in Claude Desktops session-internen Skill-Pfad zu binden — das ist fragil und wird durch Anthropic-Updates regelmaessig zerstoert. Stattdessen einen Index-/Bridge-Skill verwenden (siehe `references/skills-sync-options.md`, Option 1).
- **Nicht** Claude-Code-Plugins und Claude-Desktop-Extensions 1:1 abgleichen wollen — die Toolkits sind komplementaer, nicht spiegelbar.

---

## Changelog

### 1.0.1 (2026-06-13)
- Erstveroeffentlichung in der Skill-Bibliothek: hartkodierte User-Pfade in SKILL.md, Sync-Skript und Master-Vorlage durch `%USERPROFILE%`/`$HOME`-Platzhalter ersetzt

### 1.0.0 (2026-05-16)
- Initiale Fassung: Master-Datei + Sync-Skripte (Windows/macOS), Plugin-Paritaets- und Skills-Sync-Referenzen
