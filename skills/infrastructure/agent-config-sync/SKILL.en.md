---
name: agent-config-sync
version: 0.2.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-06-20
updated: 2026-06-20
description: >
  Synchronizes MCP servers AND skills across ALL known agent apps and CLIs
  (Claude Code, Claude Desktop, Codex CLI, Antigravity/Gemini, Kimi Code, Cursor, Cline,
  Windsurf, GitHub Copilot, ...) on one or more systems. Activates when an MCP server or
  skill should be available in multiple agent tools, the user asks "sync mcp/skills across
  all agents", "why doesn't tool X have the server/skill", "distribute MCP/skills
  everywhere", "config-sync between agents", or a new agent tool needs to be brought up
  to the shared state. Reads a registry (which tools sync how), a config (provider standard
  specs: where + which format) and a run cache (resolved real paths), applies sync rules
  (pull vs. distribute) and verifies. Includes a learning mechanism: unknown/stale config
  locations are looked up via system search, WebSearch and Context7 and updated in the
  config. Supersedes the older mcp-config-sync skill (limited to Claude Code <-> Claude
  Desktop) by wrapping it as a special case. Claude MCP profiles are managed via the
  ellmos-controlcenter-mcp backend (resolve_profile / switch_profile), not by custom logic.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [mcp, skills, sync, multi-agent, claude-code, claude-desktop, codex, gemini, antigravity, kimi, cursor, cline, windsurf, copilot, config, registry, windows, macos, controlcenter]
language: en
status: active

aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]

dependencies:
  tools: [python]
  services: [ellmos-controlcenter-mcp]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "skills/infrastructure/agent-config-sync/"
  origin_version: "0.2.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Agent Config Sync

A **cross-agent sync protocol** for MCP servers **and** skills across all known agent apps
and CLIs. Instead of maintaining a separate script for each app pair, this skill describes
*declaratively* **which** tools live on a system, **what** they should share (MCP / skills /
both) and **how** (pull, push, bidirectional/distribute). A generic flow reads this
declaration and executes the sync.

**Claude MCP profile backend:** For `claude-code` and `claude-desktop`,
**`ellmos-controlcenter-mcp`** is used as the backend (MCP tools `resolve_profile` /
`switch_profile`). `sync.py` contains no Claude-profile logic of its own; the agent
calls the ControlCenter MCP tools at runtime. Directly readable JSON profile files
(e.g. `shared.json`) are still read directly.

**Supersedes `mcp-config-sync`:** The older skill `mcp-config-sync` is wrapped as the
`claude-pair` registry relation (pull, scope mcp) inside this skill. Once `agent-config-sync`
is deployed in production, `mcp-config-sync` should be set to `status: deprecated`.

## Relationship to existing skills (no duplication)

| Skill | Responsibility | Relationship |
|---|---|---|
| **agent-config-sync** (this) | Sync of **MCP servers + skills** across **all** agent tools, rule-based | Axis 1 (inter-agent) + inter-IDE distribution |
| `mcp-config-sync` | MCP only, Claude Code <-> Claude Desktop only, 1 script | **Special case**, wrapped here (see `references/legacy-mcp-config-sync.md`); kept as legacy for now |
| `agents-bridge` | Routes foreign agents to the single rule source `CLAUDE.md` via redirect file | **Rule** sync (knowledge/workflows), NOT tool config. Complementary. |
| `system-onboarding` | First-time setup of a new system (install order) | Provides the config-location tables this skill builds on |

**What this skill is NOT:** no rule/CLAUDE.md sync (that is `agents-bridge`), no system
first-setup (that is `system-onboarding`), no plugin/extension marketplace comparison
(those toolkits are complementary, see `mcp-config-sync/references/plugin-extension-parity.md`).

## The three data layers

The skill deliberately separates **what-should-happen** from **what-do-providers-look-like**
from **where-does-it-really-live**:

```
  REGISTRY  (local/private)       which tools sync how? (relations, mode, scope)
      |  reads
      v
  CONFIG    (publishable)         provider standard specs: per tool where + format
      |  resolves paths into
      v
  CACHE     (local/private)       resolved real directories/files (run cache)
```

| File | Content | Privacy |
|---|---|---|
| `REGISTRY.md` + `registry.example.json` | which tools, sync pairs/groups, mode, scope | Template publishable; **real `registry.json` local/gitignored** |
| `CONFIG.md` + `config.json` | per provider: config location (placeholder `<HOME>`), format, merge key, quirks, source date | publishable (neutral) |
| `CACHE.md` + `cache.json` | resolved real paths on THIS system | **local/gitignored** |

## Protocol

### 0. Lock + caution
- If an active `LOCK*.txt` exists in the target area: do not write (respect the LOCK system).
- Default is **read-only**: `--status`/`--plan` change nothing. `--apply` only with
  `--yes` and after reviewing the plan.

### 1. Read registry
- Load `registry.json` (fallback: `registry.example.json`).
- Returns: installed tools on this `host`, sync relations (pairs/groups),
  per relation: mode (`pull` | `push` | `bidirectional`) and scope (`mcp` | `skills` | `both`).

### 2. Read config (provider specs)
- Load `config.json`: per provider config location (with `<HOME>` placeholder), format
  (`json` | `toml` | `dir`), `mcp_key` (e.g. `mcpServers`), `skills_dir`, quirks.

### 3. Resolve cache
- Expand placeholders (`<HOME>`, `<APPDATA>`, ...) against the real system -> `cache.json`.
- Check whether the file/directory exists. **Missing -> learning mechanism (step 6).**

### 4. Build plan (pull vs. distribute)
- Per relation: read the **source state** and compare with the **target state**.
- **pull**: a designated master/hub is read, targets get its state.
- **push/distribute**: one source tool distributes to multiple targets.
- **bidirectional**: union; on conflict (same key, different value) -> escalate, do not guess.
- For **mcp**: only replace the `mcp_key` block, preserve all other config fields;
  format conversion JSON<->TOML where needed (Codex = TOML).
- For **skills**: directory comparison (`skills_dir`); respect app-specific quirks
  (e.g. Claude Desktop does not read `~/.claude/skills/` directly -> Bridge-Skill,
  see `mcp-config-sync/references/skills-sync-options.md`).
- Output: human-readable **plan** (which file, which keys, add/update/remove).

### 5. Apply + verify (only `--apply --yes`)
- Before each write: **timestamped backup**.
- Write (format-preserving, target block only).
- **Verification:** re-read target, compare expected/actual; output diff.
- Note: apps may need restarting (Claude Desktop: quit completely from tray), for changes to take effect.

### 6. Learning mechanism (config self-healing)
Triggered when a config location is missing, a provider is unknown, or a format does not match:

1. **Config location stale/not found** -> **system search** for known filenames:
   - MCP server search: ellmos-FileCommander (`fc_search_files`/`fc_search`) or `Glob`
     over home/AppData roots for `*config*.json`, `config.toml`,
     `claude_desktop_config.json`, `settings.json`, `mcp.json`.
   - Write the found real path to `cache.json`; if it permanently differs from the config
     standard, update `config.json` (with source note).
2. **Unknown provider** (tool not in `config.json`) -> **WebSearch** for
   "<tool> MCP config file location" / "<tool> custom rules file", verify result,
   add a new provider entry to `config.json` (with `sources` field + date).
3. **Format/schema uncertainty** -> look up current spec via **WebSearch** AND
   **Context7** (`resolve-library-id` -> `query-docs`, e.g. "Model Context Protocol",
   "claude code mcp config", "codex config.toml"); correct `config.json`.

> Every automatic config change documents itself: set `sources` + `updated` fields
> on the affected provider entry.

## Usage

```bash
# Status: resolve paths, check presence, update cache.json (read-only for agent configs)
PYTHONIOENCODING=utf-8 python scripts/sync.py --status

# Plan: what would a sync do? (read-only, no writes)
PYTHONIOENCODING=utf-8 python scripts/sync.py --plan

# Apply: block-replace per relation, backup + verification (confirmation required)
PYTHONIOENCODING=utf-8 python scripts/sync.py --apply --yes

# Run tests (fixtures only -- no real config writes)
PYTHONIOENCODING=utf-8 python -m pytest skills/infrastructure/agent-config-sync/tests/ -v
```

### ControlCenter backend (Claude providers)

For `claude-code` and `claude-desktop` targets, no direct config write is made.
Instead, use the **`ellmos-controlcenter-mcp`** server:

```
resolve_profile()   -- read the active profile and server content
switch_profile()    -- switch profile / regenerate MCP config file
```

The `--plan` output explicitly shows which ControlCenter action is needed.

## Privacy / conventions

- **Publishable (neutral):** `SKILL.md`, `SKILL.en.md`, `CONFIG.md`, `config.json`,
  `REGISTRY.md`, `registry.example.json`, `CACHE.md`, `cache.example.json`, `scripts/`,
  `tests/`. Placeholders only (`<HOME>`, `~`, `<HOST>`, `<USER>`),
  NO real personal paths/hostnames.
- **Local/private (gitignored):** `registry.json`, `cache.json` (the instances filled
  with real paths for THIS system). Patterns added to `.SKILLS/.gitignore`.
- **Source = `skills/...`.** Do NOT deploy to `~/.claude/skills/` without user decision
  via `skill_sync.py`.

## Skill structure

```
agent-config-sync/
├── SKILL.md                  (this file -- protocol, DE, primary)
├── SKILL.en.md               (this file -- English version)
├── REGISTRY.md               docs: which tools sync how
├── registry.example.json     template (publishable)
├── registry.json             real instance for this system (LOCAL, gitignored)
├── CONFIG.md                 docs: provider standard specs
├── config.json               per provider: location + format + quirks (publishable)
├── CACHE.md                  docs: run cache of resolved paths
├── cache.example.json        template (publishable)
├── cache.json                resolved real paths (LOCAL, gitignored)
├── scripts/
│   └── sync.py               functional implementation (--status/--plan/--apply)
├── tests/
│   └── test_sync.py          pytest tests (fixtures only, no real config writes)
└── references/
    └── legacy-mcp-config-sync.md   how the old MCP skill is absorbed here
```

## Changelog

### 0.2.0 (2026-06-20)
- `--apply` implemented: format-preserving JSON block-replace, TOML section-replace
  (Codex), backup + verification per step, skills directory sync.
- Test suite (`tests/test_sync.py`, 15 tests, fixtures only -- no real config writes).
- ControlCenter backend wiring: Claude provider writes delegate to
  `ellmos-controlcenter-mcp` (resolve_profile/switch_profile); no custom profile logic.
- Test isolation via `--root` flag and `AGENT_CONFIG_SYNC_TEST_ROOT` env guard.
- User-neutral: placeholders in SKILL.md/CONFIG/templates; `registry.json`/`cache.json` gitignored.
- Versioning conformance: `last_sync_from_origin: null` (original custom skill),
  `status: active`, added to `registry/components.json`.
- Supersede relation to `mcp-config-sync` modelled in `references/legacy-mcp-config-sync.md`
  and SKILL.md header.
- i18n: SKILL.md (DE, primary) + SKILL.en.md (EN, complete).

### 0.1.0 (2026-06-20)
- Initial scaffold: protocol SKILL.md, Registry/Config/Cache model (template + docs),
  learning mechanism (system search/WebSearch/Context7), `scripts/sync.py` stub
  (`--status`/`--plan`). Wraps `mcp-config-sync` as a special case.
