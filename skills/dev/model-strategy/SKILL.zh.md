---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: 多模型编排与模型切换策略。基于评分的模型选择、跨 Agent 委托（Gemini、Codex、Ollama）、顾问（Advisor）配对、升级触发条件、权限矩阵和成本效率优化。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `model-strategy` 官方中文版本。


# 模型切换策略 (Model-Switching Strategy) (中文)

> 多模型编排：基于评分的模型选择、跨 Agent 委托、顾问配对、升级触发条件与成本效率优化。

---

## 1. 模型目录

### Claude（可通过 Agent 工具启动子 Agent）

```
Level 4 (评审员):   Opus 4.8  — 顾问、数学审查            [仅限用户：/model, /advisor]
Level 3 (策略师):   Opus 4.6  — 架构、概念                [子 Agent：model:"opus"]
Level 3 (创意师):   Fable 5   — 创意文本、故事            [子 Agent：model:"fable"]
Level 2 (主力军):   Sonnet 4.6— 代码实现、调试            [子 Agent：model:"sonnet"]
Level 1 (极速版):   Haiku 4.5 — 模板代码、格式化          [子 Agent：model:"haiku"]
```

### 外部 Agent（Companion 脚本 / SSH）

```
Level 2-3: Gemini 3.5 pro  — 调研、学术数据库            [agy-companion CLI]
Level 2:   Gemini 3.5 flash— 快速调研                    [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — 代码审查、代码生成          [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — 简单代码任务                [codex-companion CLI]
```

### 本地模型（零 Token 消耗，24/7 全天候）

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku 到 Sonnet 级别 [<ollama-host>:11434]
           调用方式：SSH + curl http://<ollama-host>:11434/v1/chat/completions
           或者：通过 Agent 系统控制 API 进行委托（若可用）
```

### 可达性矩阵

| 模型 | LLM 可直接启动 | 调用路径 | 约束条件 |
|------|----------------|----------|----------|
| Sonnet 4.6 | 是 | `Agent(model:"sonnet")` | — |
| Opus 4.6 | 是 | `Agent(model:"opus")` | — |
| Haiku 4.5 | 是 | `Agent(model:"haiku")` | — |
| Fable 5 | 是 | `Agent(model:"fable")` | — |
| Opus 4.8 | 仅作为 Advisor | 会话中的 `advisor()` | 用户必须手动设置 `/advisor` |
| Gemini 3.5 | 是 (Bash) | `companion-for-agy "prompt"` | 仅限 Windows，stdout 替代方案 |
| Codex 5.5/4.5 | 是 (Bash) | `node codex-companion.mjs task "prompt"` | 需要鉴权 |
| Ollama | 是 (SSH/curl) | SSH + curl 到 Ollama 主机 API | 必须激活 VPN/Tailscale |
| Opus 4.8 作为主模型 | 否 | 用户操作：`/model opus 4.8` | 仅限用户操作 |
| Fable 5 作为主模型 | 否 | 用户操作：`/model fable` | 仅限用户操作 |

---

## 2. 得分计算 (Score Computation)

```
维度 (0-10):
  CLARITY     : 任务是否明确无歧义？
  COMPLEXITY  : 涉及多少个组件？
  CREATIVITY  : 是否需要全新的解决方案？
  CONTEXT     : 需要多少背景知识？
  CRITICALITY : 对完美度的要求有多高？

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### 评分阈值

| 得分 (Score) | 模型 | 适用示例 |
|--------------|------|----------|
| 0-8 | Ollama (本地主机) | Prompt 生成、摘要提取、简单文本 |
| 9-12 | Haiku | __init__.py、格式化、模板代码 |
| 13-22 | Sonnet | 功能实现、Bug 修复、标准代码 |
| 13-22 | Gemini 3.5 | 调研、文献检索、学术数据库 |
| 13-22 | Codex 5.5 | 代码生成（Luau, Node.js）、计算脚本 |
| 23-28 | Sonnet + 顾问审查 | 带有质量检查的复杂代码 |
| 23-35 | Fable 5 | 创意文本、营销文案、故事创作 |
| 29-40 | Opus 4.6 | 架构设计、策略规划、论文撰写 |
| 35-50 | Opus 4.6 + 顾问 | 数学证明、架构决策、统计分析 |
| 40-50 | Opus 4.8 (建议用户使用) | 数学证明推导、最高严谨度需求 |

---

## 3. 跨 Agent 委托 (Cross-Agent Delegation)

### 哪个外部 Agent 适合做什么？

| 任务类型 | 最佳 Agent | 原因 |
|----------|------------|------|
| 学术文献检索 | Gemini 3.5 pro | 原生 OpenAlex/arXiv/PubMed skill 校验 |
| 代码审查（第二意见） | Codex 5.5 | 独立的第三方视角 |
| 简单文本生成 | Ollama (本地主机) | 零 Token 成本，24/7 可用 |
| 创意文本、营销文案 | Fable 5 | 最强的创意写作输出 |
| 数学证明推导 | Opus 4.8 (顾问) | 最高深度的分析能力 |

### 排除项（已记录的弱点）

- **Gemini：** 绝不用于数学审查/证明工作（在 2026-06-07 的证明审查中记录过推导方向错误）
- **Codex 4.5：** 仅在 5.5 不可用时作为备选；否则一律使用 5.5

### 调用路径示例

> 请将占位符 `<host>`、`<ollama-host>`、`<tailscale-ip>`、`<user>` 和 `~/.ssh/<key>` 替换为实际的基础设施配置。

**Gemini（通过 companion-for-agy）：**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex（通过 codex-companion）：**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**远程主机上的 Ollama（通过 SSH）：**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**委托给带工具的 Agent 系统（示例）：**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. 顾问配对 (Advisor Pairing)

### 机制

`advisor()` 是一个 **会话级别工具** — 顾问模型由用户通过 `/advisor` 设置，而非程序自动设置。这产生了以下几种配对模式：

| 模式 | 工作方式 | 何时使用 |
|------|----------|----------|
| **会话顾问 (Session advisor)** | 用户设置 `/advisor opus 4.8`，Agent 调用 `advisor()` | 数学证明/架构设计的标准模式 |
| **编排者兼审查员 (Orchestrator-as-reviewer)** | Opus 主模型审查 Sonnet 子 Agent 的输出 | 编排者能力强于执行者 |
| **对抗 Agent (Counter-agent)** | Agent A 执行任务，Agent B 进行对抗性检查 | 独立验证，提供双重视角 |
| **用户建议 (User recommendation)** | Agent 建议："请使用 opus 4.8 + advisor 执行此任务" | 当当前会话模型能力不足时 |

### 何时建议使用顾问？

- 数学证明推导工作（Score ≥ 35）
- 具有长期影响的架构决策
- 统计学方法论 / 实验设计
- 经过 2+ 轮调试仍未解决的复杂 Bug

### 何时不使用顾问？

- 日常代码、内容整理、格式化（Score < 23）
- 简单的功能实现
- 定义明确且非关键的任务

---

## 5. 升级触发条件 (Escalation Triggers)

### Ollama -> Haiku
- 需要读取/访问文件
- 需要分析代码结构

### Haiku -> Sonnet
- 受影响文件超过 2 个
- 需要在多个方案间做出决策
- 发生意外错误
- 收到删除文件操作请求

### Sonnet -> Opus
- 需要作出架构决策
- 需要整合 3 个以上的系统
- 需求存在矛盾或不明确
- 需要战略规划

### Sonnet -> Gemini（横向升级）
- 需要进行科学学术调研
- 参考文献真实性验证

### Sonnet -> Codex（横向升级）
- 需要第二意见的代码审查
- 顾问节点过载（备选审查员）

### Opus -> Opus + 顾问
- 需要数学证明审查
- 关键架构决策
- 统计学方法论评估

### 降级条件 (De-escalation)
- 概念已定义明确 -> 由 Sonnet 接管具体代码实现
- 任务属重复性/机械性工作 -> 由 Haiku 接管
- 纯文本处理，无需工具访问 -> 由 Ollama 接管

---

## 6. 权限矩阵 (Permission Matrix)

| 操作 | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|------|--------|-------|--------|------|--------|-------|
| 读取文件 | - | 是 | 是 | 是 | 是* | 是* |
| 写入文件 | - | 是 | 是 | 是 | 是* | 是* |
| 删除文件 | - | - | 是** | 是 | - | - |
| 系统命令 | - | - | 是** | 是 | 是* | 是* |
| 架构决策 | - | - | - | 是 | - | - |
| 网络调研 | - | - | 是 | 是 | 是 | - |
| 调用 advisor() | - | - | 是 | 是 | - | - |

*通过 Companion 脚本在其沙箱模式下运行
**需经用户确认

---

## 7. 成本效率 (Cost Efficiency)

### 通过路由节省 Token

| 任务类型 | 未使用路由 | 使用路由 | 节省比例 |
|----------|------------|----------|----------|
| 机械琐事 | Opus Token | Ollama（免费） | 100% |
| 模板代码 | Opus Token | Haiku Token | ~80% |
| 标准代码 | Opus Token | Sonnet Token | ~50% |
| 学术调研 | Claude Token | Gemini Token | ~70%（独立预算） |
| 代码审查 | advisor() Token | Codex Token | ~60%（独立预算） |

---

## 8. 黄金法则

> "Opus 思考，Sonnet 构建，Haiku 执行，Ollama 节省。Gemini 调研，Codex 审查，Fable 创作。"

---

## 变更日志

### 2.0.0 (2026-06-12)
- 跨 Agent 委托：引入 Gemini、Codex、Ollama (本地主机) 作为路由目标
- 顾问配对：4 种模式（会话顾问、编排者兼审查员、对抗 Agent、用户建议）
- 可达性矩阵：明确记录了 LLM 可启动与仅限用户启动的区别
- 新增 Ollama（Qwen 3.5:35b-a3b，Haiku 到 Sonnet 级别）作为 Level 1-2
- 横向升级：Sonnet -> Gemini（调研），Sonnet -> Codex（审查）
- 记录排除事项（Gemini 不用于数学推导）
- 将评分阈值扩展到所有模型

### 1.0.0 (2026-03-15)
- 移植自 BACH v3.8.0 (ing-strategie v2.0.0)

---

*移植自 BACH v3.8.0 | 结合跨 Agent + 顾问扩展至 v2.0.0*