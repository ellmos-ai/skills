---
language: ru
---

> **Русский** — Официальная полная документация на русском языке для навыка `wayfinding-routing`.



> **English** — Offizielle English-Version / Documento Oficial en English.


# Wayfinding-Routing (Self-Orientation & Emergency Fallback Engine) (English)

The **Wayfinding-Routing** skill (also known as **`survival-routing`**, **`dead-reckoning`**, **`pathfinder-routing`**, and **`celestial-routing`**) serves as the definitive navigation and emergency recovery framework for LLM agents.

It equips agents with proactive wayfinding heuristics during normal execution and emergency protocols when encountering context drift, recurring execution errors, failing APIs, or dead ends.

---

## Обзор Синонимов и Стратегий

| Стратегия Синонима | Метафора и Основной Принцип | Применимый Сценарий |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (Primary) | **Wayfinding / Spatial Orientation:** Navigating without external GPS by reading signposts and environmental cues. | Основной цикл навигации для sidecars, `workflowhooker`, and `automation-self-care`. |
| **`survival-routing`** | **Emergency Fallback & Self-Preservation:** Circuit-breaking and graceful degradation when tools fail or loops form. | Аварийное восстановление при таймаутах команд, fail repeatedly, or hit permission walls. |
| **`dead-reckoning`** | **Nautical Dead Reckoning (Koppelnavigation):** Reconstructing exact state from step-by-step breadcrumbs without external status. | Отслеживание шагов выполнения в рабочих файлах or `TODO.md` to enable precise backtracking. |
| **`pathfinder-routing`** | **Scout / Pathfinder Trailblazing:** Preflight scanning and paving paths for multi-agent teams. | Предварительное сканирование деревьев каталогов, locks, and task dependencies. |
| **`celestial-routing`** | **Astronavigation:** Aligning with immutable North-Star anchor documents when local context is noisy. | Fallback to `CLAUDE.md`, `AGENTS.md`, `START.md` when prompt instructions conflict. |

---

## 5 основных протоколов аварийной ориентации & Orientation Protocols

### 1. `PROTOCOL-ANCHOR-RESET` (North-Star Fallback / Celestial Routing)
- ****Триггер (Trigger):**** Дрейф контекста, противоречивые указания, or loss of orientation in long multi-turn sessions.
- ****Эвристическое Правило:**** Прекратить генерацию текста. Очистить гипотезы. Re-read root anchor documents (`CLAUDE.md`, `AGENTS.md`, `START.md`). Reset goal state to the authoritative root directive before taking further action.

### 2. `PROTOCOL-STOP-EXPLAIN` (Rubber-Duck Reflection Loop)
- ****Триггер (Trigger):**** Команда или редактирование повторно сбоит with an identical error.
- ****Эвристическое Правило:**** **Lock command execution.** The agent MUST output a formal self-reflection before trying a 3rd attempt:
  1. *What exact error occurred in attempt 1 & 2?*
  2. *Why did the previous diagnostic hypothesis fail?*
  3. *What is the new alternative approach?*
  Execution is unlocked ONLY after writing this explicit justification.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Multi-Tiered Fallback Cascade)
- ****Триггер (Trigger):**** Основной инструмент или API недоступен or returns errors.
- ****Эвристическое Правило:**** Никогда не завершать работу аварийно и не циклиться. Step down through degradation tiers:
  - ****Уровень 1 (Оптимальный):**** Full Native API / MCP Tool
  - ****Уровень 2 (Резервный):**** Local Python CLI / Script
  - ****Уровень 3 (Только чтение):**** Direct file parsing (`view_file` / raw text)
  - ****Уровень 4 (Передача контроля):**** Present structured status report and open options to the user.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead-Reckoning & Sackgassen-Erkennung)
- ****Триггер (Trigger):**** Сложный процесс упирается в препятствие an unresolvable block at step N.
- ****Эвристическое Правило:**** Фиксировать хлебные крошки перед изменениями. If a path fails:
  1. Revert uncommitted changes (`git checkout` / restore state).
  2. Jump back to the last clean breadcrumb checkpoint.
  3. Mark the failed route as blocked in `TODO.md`.
  4. Attempt alternative path B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Notaus & Safe Exit)
- ****Триггер (Trigger):**** Достижение лимитов выполнения или бесконечный цикл, or critical system lock error.
- ****Эвристическое Правило:**** Выполнить последовательность аварийного останова:
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