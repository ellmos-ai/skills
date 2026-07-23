---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: >
  Developer assistant (ATI successor). Provides a quick project overview
  via headless scan and routes to the available coding tools:
  CodeCommander MCP (analysis/refactor/diagnose) and the ellmos-code-tools
  module. Pure tool routing + scan, no own store.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: en
status: active

dependencies:
  tools: [dev_core.py]
  services: []
  protocols: []
  python: [pathlib]
  external: [codecommander-mcp, ellmos-code-tools]

provenance:
  origin: "bach"
  origin_path: "system/agents/ati/ + system/agents/entwickler/"
  origin_version: "n/a"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Dev — Developer Assistant (ATI)

Gets an overview first, then hands off to the right tools.

## Purpose

Successor to BACH's ATI/entwickler agent. Two tasks:
1. **Project scan** (headless, stdlib): fast, token-efficient overview of
   structure, languages and build markers of a project — before expensive analysis runs.
2. **Tool routing:** delegates to existing coding tools instead of duplicating them.

## Triggers

| User input | Action |
|---|---|
| "Get an overview of project X" | `dev_core.py scan <path>` |
| "What kind of project is this / which stack?" | `dev_core.py scan <path>` |
| "Analyse this file / refactor" | → CodeCommander MCP |
| "Generate/check Python code" | → CodeCommander MCP / ellmos-code-tools |

## Tool Landscape (Routing Targets)

- **CodeCommander MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`,
  `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`,
  `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation` etc.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): CLI dev tools (Structural-Edit,
  pycutter context, Method-Analyzer).
- **FileCommander MCP**: File/directory operations over large trees.

## CLI Entry Point (dev_core.py)

```bash
python dev_core.py scan .              # current project
python dev_core.py scan /path/project  # structure + languages + markers
```

Detects e.g.: Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go,
Java, Roblox (Rojo), Docker, Git repo.

## Store

No store. Pure scan + routing.

## Attitude

We recommend CodeCommander/ellmos-code-tools as coding tools, but are open
to others (e.g. ruff/pylint/eslint) if the user prefers them.

## Privacy

- `dev_core.py` only reads file/directory names (structure), no content, no upload.
- Skipped: `.git`, `node_modules`, `.venv`, `__pycache__` etc.

## Related Resources

- `assist/AGENTS.md` — Umbrella router
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## Changelog

### 0.1.0 (2026-06-22)
- Initial version. ATI/entwickler successor: headless project scan (stdlib) +
  routing to CodeCommander MCP / ellmos-code-tools. User-neutral, no store.
