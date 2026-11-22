---
name: priorities
version: 0.1.0
type: skill
author: ellmos-ai
created: 2026-10-21
updated: 2026-10-21
description: "Use when setting session priorities with /prios or weighting existing session goals."
visibility: public potential
language: en
---

# Session priorities

Weight work within the current goals without reducing their scope or completion criteria. Use the provider namespace and a trusted runtime session ID. If unavailable, keep priorities in the conversation only. Never substitute a global or invented ID.

Read `scripts/priorities.py show --provider PROVIDER --session-id ID`, then `set '100::Focus one; 70::Focus two'` with the same identity and `--if-revision REVISION`. Use `clear` to remove weights. Each entry has a weight from 1 to 100. Semicolon or newline separates entries; plain entries retain descending order. Read again on a revision conflict.

Use an absolute script path and separate process arguments; never execute user text. Store private data outside source control. Default storage is `~/.local/state/agent-priorities`; `--root` overrides it. `/agenda prios` changes shared agenda weights through `agenda-setting`; `/prios` changes this session only. Native Codex invocation is `$priorities`; slash aliases depend on provider support.

The agenda, linked plans and policy registers supply planning context; project instructions, current user direction and higher-level rules retain their authority. Choose the next eligible goal step using these weights. Keep all remaining goal criteria. For actual planning, route to an existing planning skill. See [integration](references/integration.md).
