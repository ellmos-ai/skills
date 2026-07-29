---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: [日本語] エージェントスキル: letter-hooker: Extends automation-self-care with Letter Hooks, Preflight Bootloaders, Document Traversal Rules, and Self-Healing Prompt Context Enrichment for AI agents and CLIs that lack native, event-driven JSON lifecycle hooks (such as Antigravity / Gemini CLI). Use when an agent needs to inject preflight rules, search memory/gardener before work begins, enforce directory document reading strategies (CLAUDE.md / AGENTS.md), or dynamically route sidecar tasks to skills and security protocols.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['agy_kontext_and_workflow_loader.py']}
provenance: {'origin': 'fork of automation-self-care', 'origin_path': 'skills/infrastructure/automation-self-care', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills'}
---

> **公式日本語版** — スキルに関する完全な日本語ドキュメント: `letter-hooker`.



# Letter-Hooker (Prompt-Level Preflight & Governance Engine)

The **Letter-Hooker** skill extends `automation-self-care` for AI agent frameworks (like **Antigravity / Gemini CLI**) that do not possess native, event-driven JSON lifecycle hook loaders (e.g. `~/.claude/settings.json` or `~/.codex/hooks.json`).

Instead of relying on passive, per-keypress hooks, `letter-hooker` operates an **active, prompt-level preflight bootloader and letter-hook injection loop** via scheduled tasks and maintainer scripts (`agy_kontext_and_workflow_loader.py`).

---

## 主な機能

1. **Preflight Bootloaders & Document Traversal Rules**:
   - **Upward & Downward Search**: Enforces strict instructions for agents to inspect `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md`, and `README.md` at the current working directory level. If missing, traverse upwards until found; then inspect downwards.
   - **Memory & Gardener Preflight**: Mandatory preflight query to `gardener` and `memoryhooker` before executing destructive or complex modifications.

2. **Letter Hooks Catalog & Reference Links**:
   - Modular `.md` instruction files stored under `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`.
   - Injects explicit `file://` links directly into `sidecar.json` prompt text so agents read exact security and workflow protocols upon invocation.

3. **Daily Keyword List & Self-Healing Prompt Enrichment**:
   - Maintains a daily `STICHWORTLISTE.json` from active/standby tasks.
   - Analyzes execution logs (`AUTOMATIONS-MEMORY.md`) for failure patterns (missing context, missing workflow guidance, invalid paths) and dynamically patches task prompts.

4. **Skill & Persona Routing**:
   - Inspects task keywords and maps them to appropriate `.SKILLS` (e.g. `infrastructure/condition`, `semantic-persona-routing`, `orchestrator`, `think`, `decide`).

---

## 主要レターフック

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md)

---

## ワークフロー Integration

```bash
# Execute the Letter-Hooker Maintenance Engine
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **Scan Sidecars**: Read all `sidecar.json` prompt texts in `~/.gemini/config/sidecars/`.
2. **Update Keyword List**: Extract domain terms and save to `.SYNC/STICHWORTLISTE.json`.
3. **Inject Letter Hooks**: Append bootloader rules and `file://` reference links to prompts.
4. **Log Results**: Record updates in `ANTIGRAVITY-LOG.txt` and `ANTIGRAVITY-REGISTRY.md`.