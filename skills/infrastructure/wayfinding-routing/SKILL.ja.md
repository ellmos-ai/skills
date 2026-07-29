---
language: ja
---

> **日本語** — スキルに関する完全な公式日本語ドキュメント: `wayfinding-routing`.



> **English** — Offizielle English-Version / Documento Oficial en English.


# Wayfinding-Routing (Self-Orientation & Emergency Fallback Engine) (English)

The **Wayfinding-Routing** skill (also known as **`survival-routing`**, **`dead-reckoning`**, **`pathfinder-routing`**, and **`celestial-routing`**) serves as the definitive navigation and emergency recovery framework for LLM agents.

It equips agents with proactive wayfinding heuristics during normal execution and emergency protocols when encountering context drift, recurring execution errors, failing APIs, or dead ends.

---

## シノニムと戦略の概要

| シノニム戦略 | 比喩と核心原則 | 適用ユースケース |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (Primary) | **Wayfinding / Spatial Orientation:** Navigating without external GPS by reading signposts and environmental cues. | サイドカーの主要ナビゲーションループ, `workflowhooker`, and `automation-self-care`. |
| **`survival-routing`** | **Emergency Fallback & Self-Preservation:** Circuit-breaking and graceful degradation when tools fail or loops form. | コマンドタイムアウト時の緊急回復, fail repeatedly, or hit permission walls. |
| **`dead-reckoning`** | **Nautical Dead Reckoning (Koppelnavigation):** Reconstructing exact state from step-by-step breadcrumbs without external status. | 作業ファイルでの実行ステップ追跡 or `TODO.md` to enable precise backtracking. |
| **`pathfinder-routing`** | **Scout / Pathfinder Trailblazing:** Preflight scanning and paving paths for multi-agent teams. | ディレクトリツリーの事前検査, locks, and task dependencies. |
| **`celestial-routing`** | **Astronavigation:** Aligning with immutable North-Star anchor documents when local context is noisy. | Fallback to `CLAUDE.md`, `AGENTS.md`, `START.md` when prompt instructions conflict. |

---

## 5つの緊急・方向性判定プロトコル & Orientation Protocols

### 1. `PROTOCOL-ANCHOR-RESET` (North-Star Fallback / Celestial Routing)
- ****トリガー (Trigger):**** コンテキストの逸脱、衝突するユーザー指示, or loss of orientation in long multi-turn sessions.
- ****ヒューリスティックルール:**** 自由テキスト生成を停止。一時的仮定をクリア. Re-read root anchor documents (`CLAUDE.md`, `AGENTS.md`, `START.md`). Reset goal state to the authoritative root directive before taking further action.

### 2. `PROTOCOL-STOP-EXPLAIN` (Rubber-Duck Reflection Loop)
- ****トリガー (Trigger):**** ターミナルコマンドまたは編集が2回失敗 with an identical error.
- ****ヒューリスティックルール:**** **Lock command execution.** The agent MUST output a formal self-reflection before trying a 3rd attempt:
  1. *What exact error occurred in attempt 1 & 2?*
  2. *Why did the previous diagnostic hypothesis fail?*
  3. *What is the new alternative approach?*
  Execution is unlocked ONLY after writing this explicit justification.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Multi-Tiered Fallback Cascade)
- ****トリガー (Trigger):**** 主要ツールまたはAPIが利用不能 or returns errors.
- ****ヒューリスティックルール:**** 突然失敗したり盲目的ループに入らない. Step down through degradation tiers:
  - ****レベル 1 (最適):**** Full Native API / MCP Tool
  - ****レベル 2 (フォールバック):**** Local Python CLI / Script
  - ****レベル 3 (読み取り専用):**** Direct file parsing (`view_file` / raw text)
  - ****レベル 4 (引き継ぎ):**** Present structured status report and open options to the user.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead-Reckoning & Sackgassen-Erkennung)
- ****トリガー (Trigger):**** 複雑なリファクタリングが行き止まりに遭遇 an unresolvable block at step N.
- ****ヒューリスティックルール:**** 破壊的変更の前にパンくずを記録. If a path fails:
  1. Revert uncommitted changes (`git checkout` / restore state).
  2. Jump back to the last clean breadcrumb checkpoint.
  3. Mark the failed route as blocked in `TODO.md`.
  4. Attempt alternative path B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Notaus & Safe Exit)
- ****トリガー (Trigger):**** 実行制限到達または無限ループ検出, or critical system lock error.
- ****ヒューリスティックルール:**** 緊急シャットダウンシーケンスを実行:
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