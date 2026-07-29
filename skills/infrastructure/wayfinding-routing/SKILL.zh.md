---
language: zh
---

> **中文** — 针对该技能的官方完整中文文档: `wayfinding-routing`.



> **English** — Offizielle English-Version / Documento Oficial en English.


# Wayfinding-Routing (Self-Orientation & Emergency Fallback Engine) (English)

The **Wayfinding-Routing** skill (also known as **`survival-routing`**, **`dead-reckoning`**, **`pathfinder-routing`**, and **`celestial-routing`**) serves as the definitive navigation and emergency recovery framework for LLM agents.

It equips agents with proactive wayfinding heuristics during normal execution and emergency protocols when encountering context drift, recurring execution errors, failing APIs, or dead ends.

---

## 同义词与策略概述

| 同义策略 | 比喻与核心原则 | 应用场景 |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (Primary) | **Wayfinding / Spatial Orientation:** Navigating without external GPS by reading signposts and environmental cues. | Sidecars 的主导航循环, `workflowhooker`, and `automation-self-care`. |
| **`survival-routing`** | **Emergency Fallback & Self-Preservation:** Circuit-breaking and graceful degradation when tools fail or loops form. | 命令超时时的应急恢复, fail repeatedly, or hit permission walls. |
| **`dead-reckoning`** | **Nautical Dead Reckoning (Koppelnavigation):** Reconstructing exact state from step-by-step breadcrumbs without external status. | 在临时文件中跟踪执行步骤 or `TODO.md` to enable precise backtracking. |
| **`pathfinder-routing`** | **Scout / Pathfinder Trailblazing:** Preflight scanning and paving paths for multi-agent teams. | 目录树的事前扫描检查, locks, and task dependencies. |
| **`celestial-routing`** | **Astronavigation:** Aligning with immutable North-Star anchor documents when local context is noisy. | Fallback to `CLAUDE.md`, `AGENTS.md`, `START.md` when prompt instructions conflict. |

---

## 5大核心应急与方向重置协议 & Orientation Protocols

### 1. `PROTOCOL-ANCHOR-RESET` (North-Star Fallback / Celestial Routing)
- ****触发条件 (Trigger):**** 上下文漂移、用户指令冲突, or loss of orientation in long multi-turn sessions.
- ****启发式规则:**** 停止自由文本生成。清除临时假设. Re-read root anchor documents (`CLAUDE.md`, `AGENTS.md`, `START.md`). Reset goal state to the authoritative root directive before taking further action.

### 2. `PROTOCOL-STOP-EXPLAIN` (Rubber-Duck Reflection Loop)
- ****触发条件 (Trigger):**** 终端命令或文件编辑连续两次失败 with an identical error.
- ****启发式规则:**** **Lock command execution.** The agent MUST output a formal self-reflection before trying a 3rd attempt:
  1. *What exact error occurred in attempt 1 & 2?*
  2. *Why did the previous diagnostic hypothesis fail?*
  3. *What is the new alternative approach?*
  Execution is unlocked ONLY after writing this explicit justification.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Multi-Tiered Fallback Cascade)
- ****触发条件 (Trigger):**** 主工具或外部 API 不可用 or returns errors.
- ****启发式规则:**** 绝不突然崩溃或盲目进入死循环. Step down through degradation tiers:
  - ****第 1 层 (最佳):**** Full Native API / MCP Tool
  - ****第 2 层 (备用工具):**** Local Python CLI / Script
  - ****第 3 层 (只读状态):**** Direct file parsing (`view_file` / raw text)
  - ****第 4 层 (移交):**** Present structured status report and open options to the user.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead-Reckoning & Sackgassen-Erkennung)
- ****触发条件 (Trigger):**** 复杂的多步骤重构遇到无法解决的阻碍 an unresolvable block at step N.
- ****启发式规则:**** 在执行破坏性修改前记录面包屑痕迹. If a path fails:
  1. Revert uncommitted changes (`git checkout` / restore state).
  2. Jump back to the last clean breadcrumb checkpoint.
  3. Mark the failed route as blocked in `TODO.md`.
  4. Attempt alternative path B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Notaus & Safe Exit)
- ****触发条件 (Trigger):**** 达到执行极限或检测到无限循环, or critical system lock error.
- ****启发式规则:**** 执行紧急关机序列:
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