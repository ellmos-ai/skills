---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Meta-skill for complete Roblox game development with Rojo — the entry point that knows and unifies the three
  specialist skills `/rojo` (filesystem→Studio sync, project setup), `/rbx-studio` (editor, MCP, assets,
  malware scan) and `/game-design` (roles, workflows, GDD). Use this skill for
  ANY Roblox game-dev undertaking: planning/building/setting up a Roblox game, scaffolding a new project,
  defining code architecture (Main + manager modules, _G.ClientState + HUD, remotes in GameEnums),
  avoiding Luau/Roblox pitfalls, or when it is unclear which of the Roblox specialist skills fits —
  routing happens from here. Also trigger on "develop Roblox game", "build Roblox game",
  "new Roblox project", "Luau project structure", "how do I organize Roblox code", "Roblox dev setup".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: en
status: active

dependencies:
  tools: [rojo, rokit]
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/rbx-dev/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

> **Note:** Not affiliated with Roblox Corporation; "Roblox" is a trademark of its owners. "rbx" is the common community shorthand.



# Roblox-Dev — Meta-Skill for Roblox Game Development

## Purpose

The central entry point for Roblox game dev with a Rojo-based, version-controllable workflow.
This skill bundles the overarching knowledge — project structure, architecture patterns and the
most important Luau pitfalls — and routes specialist questions to the three sub-skills:

| Sub-skill | What for |
| --- | --- |
| **`/rojo`** | Filesystem→Studio sync, `default.project.json`, rokit/Wally/Lune, project skeleton, sync problems |
| **`/rbx-studio`** | Studio operation, scene-vs-code mode, Studio MCP, asset pipeline, **malware scan** |
| **`/game-design`** | Roles & subtasks, development chains, Game Design Document (KONZEPT.md), multi-agent |

> Routing rule: If it's about **sync/build/setup** → `/rojo`. About **editor/assets/testing in Studio**
> → `/rbx-studio`. About **concept/roles/process** → `/game-design`. About **code architecture,
> Luau pitfalls or the overall flow** → stay here.

## Stack at a Glance

- **Language:** Luau (`.luau`, not `.lua`). Code in English, comments/docs in German, UI texts in German.
- **Sync:** Rojo via rokit (pinned tool versions). Filesystem = source of truth.
- **Tools:** Rojo (sync/build), Lune (tests/scripts outside Studio), Wally (packages),
  optionally Knit (service/controller framework, new projects), Selene (linter).
- **Control:** Roblox-Studio-MCP for AI-driven inspection/tests/asset insertion.

## Project Structure (Standard)

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

A skeleton is created by `/rojo` via `scaffold_roblox_project.sh`.

## Architecture Patterns

**Server — Main + manager modules.** Only **one** Script per project: `Main.server.luau`. It
centrally creates the remotes folder and loads all feature modules via `require()`:
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
All other server files are `.luau` (ModuleScripts).

**Client — shared state + HUD.** The GameClient writes a shared state, the HUD reads
it in the Heartbeat:
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — centralized in GameEnums.** Define remote names once in `GameEnums.Remotes`;
the server creates the events from them, the client looks them up via the same names. That way there are no
string mismatches between server and client.

## Overall Flow of a Game

1. **Concept** (`/game-design`): KONZEPT.md — genre, USP, 3–4 core mechanics, monetization.
2. **Setup** (`/rojo`): scaffold the skeleton, define the `default.project.json` mapping.
3. **Backend**: Config → GameEnums → *Defs → Main.server → *Manager.
4. **Frontend**: GameClient → HUD.
5. **Greybox playtest** (`/rbx-studio`): gameplay first, parts + optionally AI materials.
6. **Asset upgrade** (`/rbx-studio`): Creator Store assets, **malware scan**, scene as .rbxl.
7. **Test** (`/game-design`): QA + game critic + persona blind tests, iterate.
8. **Release** (`/game-design` business role): store page, monetization, live ops.

## Luau/Roblox Pitfalls (Short List)

The most common pitfalls — full, annotated list:
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md).

- Semicolon after `task.wait(x)` when more code follows on the same line.
- `Model.Position` does not exist → `model:GetPivot().Position`.
- `#table` on dictionaries = 0 → count manually.
- `mouse.Hit` can be nil → check before use.
- DataStore calls **always** in `pcall`.
- `tick()` deprecated → `os.clock()`; `SetPrimaryPartCFrame` → `PivotTo`.
- Event names centralized in `GameEnums.Remotes`; create all remotes in `Main.server.luau`.
- No circular `require`s (otherwise deadlock).
- `require()` only on `.luau` ModuleScripts, never on Scripts/LocalScripts.

## Before Every Commit (Checklist)

- [ ] Semicolons after `task.wait(...)` in multi-statement lines
- [ ] no `Model.Position`, no `tick()`, no `SetPrimaryPartCFrame`
- [ ] DataStore in `pcall`, `mouse.Hit` checked for nil
- [ ] event names match server↔client (via GameEnums)
- [ ] all RemoteEvents created in `Main.server.luau`
- [ ] no circular requires
- [ ] marketplace assets scanned (`/rbx-studio` → malware scan), reports filed

## Knowledge Sources

- **Current engine/creator docs:** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine` (engine API) and `/roblox/creator-docs`
  (tutorials/guides); fallback <https://create.roblox.com/docs>.
- **Reference pipeline** (if present on this system): `<your Roblox project pipeline>` —
  including `SKILL.md`, `GUIDE.md`, `LESSONS_LEARNED.md`, `ROJO_FAQ.md`, `ROBLOX_MCP_FAQ.md`,
  `AGENT_ROLES.md`, `_malware_reports/PATTERNS.md`, `_knowledge/` (local API cache).

## Changelog

### 1.0.0 (2026-06-17)
- Initial version. Meta-skill over `/rojo`, `/rbx-studio`, `/game-design`; project structure,
  architecture patterns and Luau lessons distilled from the `.ROBLOX` pipeline, user-neutral.
