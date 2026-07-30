---
name: wayfinding-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  通用 LLM 导航、定向与紧急恢复能力 Skill。
  在 Agent 面临上下文漂移、工具失效、循环死锁或到达死胡同（死局）时，
  提供主动路径规划、自我定向与恢复启发式规则。包含同义词策略：
  survival-routing、dead-reckoning、pathfinder-routing 以及 celestial-routing。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, self-orientation, resilience, recovery, heuristics]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
---

> **中文** — `wayfinding-routing` 官方中文版本。

# Wayfinding-Routing（自我定向与紧急回退引擎）

The **Wayfinding-Routing** skill（也称为 **`survival-routing`**、**`dead-reckoning`**、**`pathfinder-routing`** 和 **`celestial-routing`**）是 LLM Agent 的权威导航与紧急恢复框架。

它为 Agent 提供正常执行期间的主动路径查找（Wayfinding）启发式规则，以及在遭遇上下文漂移、重复执行错误、API 故障或死胡同时的紧急处理协议。

---

## 同义词与策略概述

| 同义词策略 | 隐喻与核心原则 | 应用场景 |
| :--- | :--- | :--- |
| **`wayfinding-routing`**（主要） | **路径查找 / 空间定向：** 无需外部 GPS，通过阅读路标和环境线索进行导航。 | sidecar、`workflowhooker` 和 `automation-self-care` 的主要导航循环。 |
| **`survival-routing`** | **紧急降级与自我保护：** 当工具故障或形成死循环时进行熔断与优雅降级。 | 当命令超时、连续失败或触发权限限制时的紧急恢复。 |
| **`dead-reckoning`** | **航海推算导航 (Koppelnavigation)：** 在没有外部状态的情况下，从逐步面包屑（痕迹）重建精确状态。 | 在临时文件或 `TODO.md` 中记录执行步骤，以便实现精确的回溯。 |
| **`pathfinder-routing`** | **侦察 / 探路开拓：** 为多 Agent 团队进行预检扫描与铺平道路。 | 对目录树、锁和任务依赖项进行预检扫描。 |
| **`celestial-routing`** | **天文导航：** 当局部上下文充满噪音时，对齐不可变的北极星锚点文档。 | 当 Prompt 指令发生冲突时，回退至 `CLAUDE.md`、`AGENTS.md`、`START.md`。 |

---

## 5 大核心紧急与定向协议

### 1. `PROTOCOL-ANCHOR-RESET`（北极星回退 / 天文导航）
- **触发条件：** 上下文漂移、用户指令冲突，或在长多轮会话中失去定向。
- **启发式规则：** 停止自由文本生成。清除临时假设。重新阅读根锚点文档（`CLAUDE.md`、`AGENTS.md`、`START.md`）。在采取进一步行动之前，将目标状态重置为具有权威性的根指令。

### 2. `PROTOCOL-STOP-EXPLAIN`（小黄鸭反思循环）
- **触发条件：** 终端命令、文件编辑或 API 请求连续两次出现相同的错误失败。
- **启发式规则：** **锁定命令执行。** Agent 在尝试第 3 次之前，必须输出正式的自我反思：
  1. *第 1 次和第 2 次尝试中究竟发生了什么错误？*
  2. *为什么之前的诊断假设失败了？*
  3. *新的替代方案是什么？*
  仅在写出此明确的理由说明后，方可解除执行锁定。

### 3. `PROTOCOL-GRACEFUL-DEGRADATION`（多级降级级联）
- **触发条件：** 主要工具、MCP 服务器或外部 API 不可用或返回错误。
- **启发式规则：** 切勿突然失败或盲目死循环。按降级层级逐级下探：
  - **Tier 1（最佳）：** 完整原生 API / MCP 工具
  - **Tier 2（备用工具）：** 本地 Python CLI / 脚本
  - **Tier 3（只读状态）：** 直接文件解析（`view_file` / 原始文本）
  - **Tier 4（交接）：** 向用户展示结构化的状态报告并提供可选方案。

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK`（推算导航与死胡同识别）
- **触发条件：** 复杂的重构或工作流路径在第 N 步遇到了无法解决的阻碍。
- **启发式规则：** 在进行破坏性更改之前记录面包屑痕迹。如果某条路径失败：
  1. 还原未提交的更改（`git checkout` / 恢复状态）。
  2. 跳回上一个干净的面包屑检查点。
  3. 在 `TODO.md` 中将失败的路线标记为已阻塞。
  4. 尝试替代路线 B。

### 5. `PROTOCOL-CIRCUIT-BREAKER`（紧急停止与安全退出）
- **触发条件：** 达到执行限制、检测到无限循环，或发生严重系统锁错误。
- **启发式规则：** 执行紧急关机序列：
  1. 释放所有已获取的文件锁和 Git 锁（`python -m workflowhooker check`）。
  2. 将当前的阶段性状态保存至 `.SYNC/SURVIVAL_STATE.json` 或 `AUTOMATIONS-MEMORY.md`。
  3. 将事件记录在 `ANTIGRAVITY-LOG.txt` 中。
  4. 为用户或协调器（orchestrator）提供包含可操作摘要的干净退出。

---

## 与 `automation-self-care` 及 `workflowhooker` 的集成

`wayfinding-routing` 为以下模块提供底层导航逻辑：
- **`automation-self-care`**：对照 5 大协议评估 sidecar prompts，确保具备自愈能力。
- **`workflowhooker`**：为逐步检查锁状态和记录面包屑痕迹提供标准启发式规则。
- **`staircase-routing`**：利用 `PROTOCOL-ANCHOR-RESET` 进行垂直目录导航。