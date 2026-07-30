---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: General Blender workflow skill for AI agents working with .blend, .fbx, .obj, .glb, glTF, materials, scene inspection, bpy automation, headless Blender batch runs, export/reimport validation, previews, and optional Blender MCP control. Use when a task asks to open, inspect, create, automate, convert, optimize, render, or verify Blender or 3D asset files in a user-agnostic way.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: en
status: active
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

> **English** — Official English version of `using-blender`.

# Using Blender

## Core Rule

Work with Blender in three modes, appropriate to the task:

1. **GUI Mode:** Open Blender visibly when the user wants to view, inspect, or manually edit an asset.
2. **Headless Mode:** Use `blender --background --python <script.py>` when export, re-import, batch processing, or deterministic validation is required.
3. **MCP Mode:** Only use when a running Blender add-on is intentionally connected and live scene control is necessary. Check security and licensing status beforehand.

## Standard Workflow

1. Clarify goal: view, create, convert, optimize, render, or verify.
2. Read existing files: Manifest, README, export formats, and existing validation results first.
3. Determine Blender path: `blender` on PATH, project-specific configuration, or user path. Do not write local private paths into publishable documentation.
4. For automation, use a small `bpy` script that makes inputs, outputs, and errors explicit.
5. After every export, execute at least one re-import or loading check before considering the result usable.
6. Document artifacts concisely: Source, export formats, tool version, verification status, and known limitations.

## Export and Validation Rules

- Prefer `.glb` for general web/preview use.
- Offer `.fbx` or `.obj/.mtl` additionally for game engines and DCC exchange if the target workflow requires it.
- Always check roundtrips: file exists, is non-empty, can be re-imported, and expected object/material names are present.
- For large assets, gather metrics: mesh count, materials, bounding box, file size, and optionally triangle count.
- For render checks, use a small preview resolution before starting expensive Cycles or Full HD renders.

## Security Rules

- `bpy` code is local Python code with filesystem access. Only execute self-written or audited scripts.
- Do not enable external Blender add-ons, asset downloaders, or telemetry servers without checking licenses and data privacy.
- For MCP servers with an arbitrary `execute_python` tool, limit scope, network, working directory, and timeout beforehand.
- For marketplace or external assets, verify the license separately. Technical loadability does not replace usage rights.

## MCP Options

For live control, read [references/blender-mcp-review.md](references/blender-mcp-review.md) when a Blender MCP server needs to be selected, installed, or evaluated.

## Changelog

### 1.0.0 (2026-06-20)
- Initial user-agnostic Blender skill with GUI, headless, and MCP routing.