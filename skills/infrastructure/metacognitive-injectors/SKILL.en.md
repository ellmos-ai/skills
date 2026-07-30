---
name: metacognitive-injectors
version: 1.4.0
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-30
updated: 2026-07-30
description: >
  Metacognitive injectors and self-talk strategies (Self-Talk, Metacognitive Auditing, Evaluator Hooks, Pre-Flight Checklists, State Persistence & Personas).
  Integrates Active Information Search (Gardener & USMC System Memory), Rehearsal (Active Retrieval Practice), Baddeley's Working Memory (State + Hooks),
  Miyake Executive Functions and CBT/ACT therapeutic strategies.
standalone: true
anthropic_compatible: true
bach_compatible: true
category: infrastructure
tags: [metacognition, self-talk, metacognitive-injectors, evaluator-hook, quality-gate, multi-agent, auditing, pre-flight-checklist, working-memory, active-retrieval, rehearsal, gardener, usmc, state-persistence, hooks, survival-routing, persona-routing]
aliases: [self-talk, metacognitive-self-talk, metacognitive-auditing, evaluator-hook, preflight-checklist, inner-speech, active-retrieval, rehearsal]
language: en
status: active
---

<img src="banner.png" width="100%" alt="metacognitive-injectors banner">

# Metacognitive Injectors (Metacognitive-Injectors, Active Retrieval & Memory Search)

The skill **Metacognitive-Injectors** (also known as **`self-talk`**, **`metacognitive-auditing`**, **`evaluator-hook`**, **`preflight-checklist`**, **`inner-speech`**, **`active-retrieval`**, and **`rehearsal`**) establishes cognitive science and therapeutic self-monitoring strategies for AI agents.

---

## 1. Active Information Search & System Memory (Gardener & USMC)

### A. Active Information Search in System Memories
- Before making assumptions or jumping to conclusions, **actively search system memory**:
  1. **Gardener DB (`gardener.py` / `hb_garden_*`):** Queries observed learnings, user decisions, and path agreements (e.g. `Gardener().find("companion")`).
  2. **USMC SQLite DB (`usmc_memory.db`):** Queries stored facts, lessons, and session histories.
  3. **Central Rule Files (`CLAUDE.md`, `.SYNC`, `AGENTS.md`):** Reads established conventions and paths.

### B. Rehearsal: Active Retrieval & Reproduction (Retrieval Practice)
- **Subvocal Rehearsal Loop (Phonological Loop):**
  Do not merely read information passively; **actively retrieve it, reconstruct it in working memory, and match it against reality** before generating outputs.
  - *"Have I retrieved the exact path to the script from memory?"*
  - *"Does the command syntax match the examples stored in system memory?"*

---

## 2. Multi-Model Fallback Cascade & Codex Companion Interface

| Priority | Auditor / Advisor | Interface / Command | Function / Rule |
| :--- | :--- | :--- | :--- |
| **Primary (1)** | **Gemini Subagent** | `invoke_subagent` / `define_subagent` | Internal subagent for routine checks. |
| **Secondary (2)** | **Codex Companion (Native)** | `node "<USER_HOME>\.codex\.tmp\marketplaces\openai-codex\plugins\codex\scripts\codex-companion.mjs" task "..."` | Native Codex Companion for audits & **`/goal` sign-off**. |
| **Tertiary (3)** | **Codex CLI Direct** | `codex exec --skip-git-repo-check` | Direct Codex CLI call. |
| **Quaternary (4)** | **Claude CLI / Swarm** | `claude -p ...` / `hb_swarm_consensus` | Third opinion if Codex tokens are exhausted. |
