---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Operating Rojo — the filesystem-to-Roblox-Studio sync tool for professional
  Roblox development in VS Code / Claude Code instead of the Studio editor. Use this skill
  whenever Rojo is involved: `rojo serve`/`rojo build`, writing or debugging
  `default.project.json`, rokit/rokit.toml and tool versions (Rojo, Lune, Wally), nested
  vs. flat path mapping (ReplicatedStorage.Project.shared), connect/port/sync problems,
  or when a Roblox project skeleton needs to be created. Also trigger on "rojo connect
  not working", "scripts end up in the wrong place in Studio", "how do I map src/ to Studio", "port 34872
  in use", "ModuleScript vs Script in Rojo".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: en
status: active

dependencies:
  tools: [rojo, rokit]
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/rojo/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Rojo — Filesystem → Roblox Studio Sync

## Purpose

Rojo connects a normal filesystem project (`.luau` files in `src/`, versioned with Git)
to Roblox Studio. You write code in the editor of your choice (VS Code, Claude Code), and Rojo
syncs it live into a running Studio instance. This makes Roblox code versionable,
diffable and editable with real tools — instead of living in the built-in Studio script editor.

Use this skill for everything around Rojo setup, the `default.project.json` mapping, the
toolchain (rokit/Wally/Lune) and typical sync problems.

## Mental Model

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**Core rule:** The filesystem is the source of truth. On every connect, Rojo overwrites
the mapped Studio areas with the filesystem content. Therefore, **never** edit code
in Studio (it is lost on the next sync), only in the editor. The `Workspace`
(3D scene, terrain) is **not** mapped by Rojo and is preserved — see skill
`/rbx-studio` for the scene-vs-code workflow.

## File Extensions → Roblox Type (Rojo Convention)

Rojo derives the instance type from the extension. This is the most common source of errors:

| File               | Roblox Type   | `require()`-able | Role                      |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **yes**         | Logic module, definitions |
| `Foo.server.luau`  | Script        | no              | Server entry point        |
| `Foo.client.luau`  | LocalScript   | no              | Client entry point        |
| `init.luau`        | becomes the folder node itself | yes | makes the folder a ModuleScript |

> Rule of thumb: **Only entry points** are `.server.luau`/`.client.luau`. Everything loaded via
> `require()` **must** be a `.luau` ModuleScript. Calling `require()` on a
> Script/LocalScript throws "Attempted to call require with invalid argument(s)".

## CLI Commands

```bash
rojo serve default.project.json     # Live-Sync-Server starten (Standard-Port 34872)
rojo serve                          # nutzt default.project.json automatisch
rojo build default.project.json -o game.rbxlx   # einmaliger Build → Place-Datei (XML)
rojo build default.project.json -o game.rbxl    # Build → Place-Datei (binär)
rojo plugin install                 # Rojo-Studio-Plugin installieren (einmalig)
rojo --version                      # installierte Version prüfen
```

After `rojo serve`: in Studio, open the Rojo plugin → **Connect** (localhost:34872).
`rojo build` does not need a running Studio — ideal for CI, smoke tests and releases.

## `default.project.json` — the Mapping

This file maps filesystem paths onto the Roblox data model hierarchy. Keys:

- `name` — project name (display)
- `$className` — Roblox class of the node (`DataModel`, `ServerScriptService`, `Folder`, …)
- `$path` — filesystem path that is synced under this node (relative to the project root)

A ready-to-use standard template is located at [`assets/default.project.json`](assets/default.project.json).

### Flat vs. Nested — the most important decision

Your code must match the mapping. Two variants:

**Flat** — the content of `src/server` ends up directly in `ServerScriptService`:
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ Code references e.g. `ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`.

**Nested** — the content ends up in `ServerScriptService.ProjectName`:
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ Code references `ReplicatedStorage.ProjectName.shared.Config` etc.

Both are valid. Decide project-wide on **one** variant and keep every
`require`/`WaitForChild` path consistent with it. Symptom on mismatch: `WaitForChild(...)`
hangs indefinitely (infinite yield), because the expected node is located elsewhere.

## Toolchain via rokit

[rokit](https://github.com/rojo-rbx/rokit) is the toolchain manager. A `rokit.toml` in the
project (or parent folder) pins exact tool versions → reproducible builds on all
machines. If it is missing, you get `Failed to find tool 'rojo' in any project manifest file`.

Standard `rokit.toml` (see [`assets/rokit.toml`](assets/rokit.toml)):
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> Version note: 7.4.4 is the version pinned consistently throughout the reference pipeline.
> Newer projects can go to 7.6.x — but check first with `rojo build` against the project,
> since the project format can change between major versions.

After cloning/setup: `rokit install` pulls all pinned tools.

- **Lune** — Luau runner outside Studio (unit tests, build scripts, asset processing).
- **Wally** — package manager: `wally install` → `Packages/` → in Studio under
  `ReplicatedStorage.Packages`. Dependencies are listed in `wally.toml` (see
  [`assets/wally.toml`](assets/wally.toml)), e.g. the framework `sleitnick/knit@1.7.0`.

## Creating a New Project

The script [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) creates a
complete Rojo skeleton (project.json, rokit.toml, wally.toml, `src/{shared,server,client,gui}/`
with starter files, KONZEPT stub):

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # flaches Mapping (Default)
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # verschachteltes Mapping
```

After that: `cd MeinSpiel && rokit install && rojo serve`.

## Troubleshooting

| Symptom | Cause | Solution |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | no `rokit.toml` | create `rokit.toml` with a Rojo pin in the project/parent folder, `rokit install` |
| `require` throws "invalid argument(s)" | `require()` on a Script/LocalScript | only `.luau` ModuleScripts are require-able; check the extension |
| Port 34872 in use (`os error 10048`) | old Rojo process is running | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F`, then `rojo serve` again |
| Scripts end up in the wrong place in Studio | flat instead of nested mapping (or vice versa) | adjust `default.project.json` to the code paths (see above) |
| `WaitForChild` hangs indefinitely | expected node does not exist / server error before creation | **check the server console for errors first**; check mapping + creation order |
| Sync stops after file rename | Rojo does not detect the rename immediately | stop the server (Ctrl+C) + restart it, in Studio Disconnect→Reconnect |
| Change in Studio gone after reconnect | Studio edit instead of filesystem edit | change code **only** in the editor; Rojo overwrites mapped areas |

### Known Rojo Limitations

1. **No terrain/Workspace sync** — build the 3D scene & terrain in Studio or generate it via code.
2. **No `.rbxl` merge** — place files are binary, not git-mergeable. Never use as the primary source.
3. **No live sync in Play mode** — changes during Play are discarded on Stop.
4. **Git Bash path translation** — `/c/...` can be translated to `C:/...` and break Rojo paths; when in doubt, use relative paths or native Windows paths.

## Linting (Selene)

Roblox Luau projects are usually linted with **Selene** (`selene.toml` in the root,
`std = "roblox"`). Allow globals like `_G` via `global_usage = "allow"` if the project
uses them for shared client state. Run Selene from the directory containing the Roblox API definition
(`roblox.yml`).

## Further Reading

- Sister skills: `/rbx-studio` (Studio operation, MCP, assets), `/game-design`
  (roles, workflows, GDD), meta-skill `/rbx-dev` (combines all three + architecture patterns).
- Current engine/Rojo docs: Context7 MCP (`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) or
  <https://rojo.space/docs/>.
- If present on this system, a project-rich reference pipeline is located at
  `<your Roblox project pipeline>` (incl. `ROJO_FAQ.md`, `SKILL.md`).

## Changelog

### 1.0.0 (2026-06-17)
- Initial version. Distilled from the `.ROBLOX` pipeline (ROJO_FAQ, ROJO_START, _template),
  written in a user-neutral way.
