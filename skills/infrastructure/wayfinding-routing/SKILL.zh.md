---
name: wayfinding-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: [中文] 针对该技能的完整中文文档: wayfinding-routing: Universal LLM navigation, orientation, and emergency resilience skill. Provides active wayfinding, self-orientation, and recovery heuristics when agents face context drift, failing tools, loops, or dead ends. Includes synonym strategies: survival-routing, dead-reckoning, pathfinder-routing, and celestial-routing.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, self-orientation, resilience, recovery, heuristics]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': None, 'origin_version': None, 'origin_repo': 'github.com/ellmos-ai/skills'}
---

> **中文** — [中文] 针对该技能的完整中文文档: `wayfinding-routing`.



# Wayfinding-Routing (Self-Orientation & Emergency Fallback Engine)

The **Wayfinding-Routing** skill (also known as **`survival-routing`**, **`dead-reckoning`**, **`pathfinder-routing`**, and **`celestial-routing`**) serves as the definitive navigation and emergency recovery framework for LLM agents.

It equips agents with proactive wayfinding heuristics during normal execution and emergency protocols when encountering context drift, recurring execution errors, failing APIs, or dead ends.

---

## Synonym & Strategy Overview

| Synonym Strategy | Metaphor & Core Principle | Applied Use Case |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (Primary) | **Wayfinding / Spatial Orientation:** Navigating without external GPS by reading signposts and environmental cues. | Primary navigation loop for sidecars, `workflowhooker`, and `automation-self-care`. |
| **`survival-routing`** | **Emergency Fallback & Self-Preservation:** Circuit-breaking and graceful degradation when tools fail or loops form. | Emergency recovery when commands time out, fail repeatedly, or hit permission walls. |
| **`dead-reckoning`** | **Nautical Dead Reckoning (Koppelnavigation):** Reconstructing exact state from step-by-step breadcrumbs without external status. | Tracking execution steps in scratch files or `TODO.md` to enable precise backtracking. |
| **`pathfinder-routing`** | **Scout / Pathfinder Trailblazing:** Preflight scanning and paving paths for multi-agent teams. | Preflight inspection of directory trees, locks, and task dependencies. |
| **`celestial-routing`** | **Astronavigation:** Aligning with immutable North-Star anchor documents when local context is noisy. | Fallback to `CLAUDE.md`, `AGENTS.md`, `START.md` when prompt instructions conflict. |

---

## 5大核心应急与方向重置协议

### 1. `PROTOCOL-ANCHOR-RESET` (North-Star Fallback / Celestial Routing)
- **Trigger:** Context drift, conflicting user instructions, or loss of orientation in long multi-turn sessions.
- **Heuristic Rule:** Stop free text generation. Clear transient assumptions. Re-read root anchor documents (`CLAUDE.md`, `AGENTS.md`, `START.md`). Reset goal state to the authoritative root directive before taking further action.

### 2. `PROTOCOL-STOP-EXPLAIN` (Rubber-Duck Reflection Loop)
- **Trigger:** A terminal command, file edit, or API request fails twice with an identical error.
- **Heuristic Rule:** **Lock command execution.** The agent MUST output a formal self-reflection before trying a 3rd attempt:
  1. *What exact error occurred in attempt 1 & 2?*
  2. *Why did the previous diagnostic hypothesis fail?*
  3. *What is the new alternative approach?*
  Execution is unlocked ONLY after writing this explicit justification.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Multi-Tiered Fallback Cascade)
- **Trigger:** Primary tool, MCP server, or external API is unavailable or returns errors.
- **Heuristic Rule:** Never fail abruptly or loop blindly. Step down through degradation tiers:
  - **Tier 1 (Optimal):** Full Native API / MCP Tool
  - **Tier 2 (Fallback Tool):** Local Python CLI / Script
  - **Tier 3 (Read-Only State):** Direct file parsing (`view_file` / raw text)
  - **Tier 4 (Handoff):** Present structured status report and open options to the user.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead-Reckoning & Sackgassen-Erkennung)
- **Trigger:** A complex multi-step refactoring or workflow path hits an unresolvable block at step N.
- **Heuristic Rule:** Record breadcrumbs before making destructive changes. If a path fails:
  1. Revert uncommitted changes (`git checkout` / restore state).
  2. Jump back to the last clean breadcrumb checkpoint.
  3. Mark the failed route as blocked in `TODO.md`.
  4. Attempt alternative path B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Notaus & Safe Exit)
- **Trigger:** Execution limits reached, infinite loop detected, or critical system lock error.
- **Heuristic Rule:** Execute emergency shutdown sequence:
  1. Release all acquired file and git locks (`python -m workflowhooker check`).
  2. Save current partial state to `.SYNC/SURVIVAL_STATE.json` or `AUTOMATIONS-MEMORY.md`.
  3. Log incident in `ANTIGRAVITY-LOG.txt`.
  4. Exit cleanly with actionable summary for the user or orchestrator.

---

## Integration with `automation-self-care` & `workflowhooker`

`wayfinding-routing` provides the underlying navigation logic for:
- **`automation-self-care`**: Evaluates sidecar prompts against the 5 protocols to ensure self-healing capabilities.
- **`workflowhooker`**: Provides standard heuristics for step-by-step lock checking and breadcrumb recording.
- **`staircase-routing`**: Leverages `PROTOCOL-ANCHOR-RESET` for vertical directory navigation.