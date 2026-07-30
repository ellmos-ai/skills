---
name: trampelpfadanalyse
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-06-21
updated: 2026-06-21
description: 针对 Pipeline 与控制文件工作流的错误分析：检测约定或流程对于 LLM 是否真正可见与易于发现。使用朴素子 Agent 进行实证 Baseline → 干预 → Retest 对比（隔离的 Sandbox 副本、完全相同的测试用例、定量成功率测量）。当 Agent 反复忽略规则/README/约定或导航错误，且希望测量文档修改是否能切实改变行为时使用此 Skill。触发词包括："is the convention even seen"、"why does no agent follow the rule"、"make a doc signpost measurably effective"、"desire-path analysis"、"trampelpfadanalyse"。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [workflow, error-analysis, llm-ux, doc-audit, baseline-retest, naive-subagent, empirical, pipeline, control-file]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/system/trampelpfadanalyse.md', 'origin_version': '2.0', 'origin_repo': 'github.com/ellmos-ai/swarm-ai', 'last_sync_from_origin': '2026-06-21', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `trampelpfadanalyse` 官方中文版本。


# 欲望路径分析 (Desire-Path Analysis) — 让约定对 LLM 具备实证可见性

一种用于揭示 Pipeline 和控制文件工作流中并非源自代码 Bug、而是源于**约定对 LLM 不可见**的错误的分析方法。无需猜测 README 或规则是否“足够清晰”，而是通过实证方式进行测量：让毫无先验知识的朴素（naive）子 Agent 在工作流中运行，其行为构成**基线（Baseline）**；针对性的文档修改（“路标” / signpost）作为**干预措施（Intervention）**；全新的朴素子 Agent 进行**重测（Retest）**。与 Baseline 的 Diff 即为成功测量指标。

该名称源自*欲望路径*（德语：*Trampelpfad*，即人们因日常踩踏而自然形成的羊肠小道）：人们实际行走的地方才是应该铺设道路的地方。同理，朴素 LLM 的行走路径展示了究竟在哪里才真正需要文档/防护栏（Guardrails），而非我们主观假设的位置。

## 何时使用此 Skill

- 尽管已有文档说明，Agent 仍反复忽略某条规则/约定。
- 希望在撰写更多文档前了解某项流程对 LLM 是否**可见/易发现**（“这里有人是在对着墙说话吗？”）。
- 在重构之后（如新建目录、重命名文件）：Agent 是否仍能找到入口点？
- 进行了文档修改，并希望**证明**其有效——而非仅凭希望。
- 在将新 LLM Partner 集成到 Pipeline 之前的入职测试（Onboarding test）。

不适用于：纯代码 Bug（→ 参考 `bugfix-protocol` / 系统化调试），或为生产任务选择 Swarm 协调模式（→ 参考 `swarm-operations`）。本 Skill 仅将朴素 Agent 组成的 Swarm 用作**测量工具**。

## 一句话核心思想

将文档视为 UX：重要的不是你写了什么，而是无偏见的用户（此处指朴素 Agent）实际上用它做了什么——你需要对此进行测量、修改并再次测量。

---

## 流程：5 个步骤

```
1. BASELINE       naive subagents → measure current behavior (quantitative)
2. PATH ANALYSIS  where exactly does it fail? which doc location misleads?
3. INTERVENTION   put up a "signpost" (README/convention made more prominent)
4. RETEST         FRESH naive subagents, identical test case
5. DIFF           retest vs. baseline → success measurement + honest assessment
```

### 步骤 1 — Baseline：以朴素方式测量当前行为

首先将问题表述为一个**可测试的问题**，例如：“Agent 是否在约定指定的路径下创建了日志？”或“Agent 是否找到了 Pipeline 的入口点？”。

然后让朴素子 Agent 运行：

- **朴素（Naive）意味着：** 无项目记忆、无 Skill、无先验提示——Agent 仅知道入口路径和任务。这测量的是**基于现有文档的纯粹可发现性**，而非 Agent 的先验知识。
- **隔离的 Sandbox 副本：** 每个探测 Agent 在受影响文件夹/工作流的独立副本中工作，避免相互影响，且保持真实状态不受破坏。
- **相同测试用例，多次重复：** 存在随机变异性。单次探测只是偶然现象；n 次重复（如 3 次，必要时更多）才能得出统计率。
- **采用性价比高、较“朴素”的模型**即可且更符合实际——它不应进行聪明盲猜，而应展示文档会将普通 Agent 引导至何处。

最小探测 Prompt（请替换占位符）：

```
You are exploring <SYSTEM>. It is located at: <PATH>.
TASK: <specific task>.
RULES:
1. You only know the path above, nothing else.
2. Explore to complete the task. Max. <N> steps.
3. Report at the end: VISITED_DIRECTORIES, READ_FILES,
   TASK_COMPLETED (yes/no), MOST_HELPFUL_FILE.
```

**记录为 Baseline 指标**（必须是定量的，绝不能凭“感觉更好”）：

| 指标 | 含义 |
|---|---|
| 成功率 | 按照约定完成任务的频率（如 0/3） |
| 错误行为 | 使用错误位置/方法的频率（如 3/3 均使用了汇总日志而非单条日志） |
| 达标路径 | 达到目标所需的步骤数/迂回次数 |
| 盲区 | 没有任何 Agent 打开的相关文件/位置 |

### 步骤 2 — 路径分析（Path Analysis）：究竟在哪里失败？

共同评估探测报告（绘制一份访问位置的“热力图”即可）：

- 哪个文件被**频繁**阅读（热点 / HOT）？如果那里缺少指引，那就是设置路标最有效的位置。
- 哪个相关位置**从未**被打开（冷点 / COLD / 盲区）？无论其内容多好，实际上它是不可见的。
- Agent 在哪里产生循环或绕过了约定（死胡同、规避行为）？这标志着具体的文档缺口。

发现结果表：

| 发现 | 含义 | 行动（→ 步骤 3） |
|---|---|---|
| HOT + 无指引 | 高流量，无路标 | 直接在此处设置路标 |
| WARM + 发生错误 | Agent 到达但遭遇困难 | 添加示例/澄清说明 |
| COLD | 位置从未被找到 | 从 HOT 文件中建立链接指向它 |
| 规避行为 | 约定被绕过 | 在规避发生点添加提示 |

步骤 2 的产出：**一个具体的、局部化的假设**——“Agent 阅读了 X，但 X 未提及该约定；因此他们最终走到了 Y。”

### 步骤 3 — 干预（Intervention）：设立路标 (Signpost)

**仅设立一个**路标（每次测试仅改变一个变量，否则 Diff 无法解释）。典型的路标形式：

- 将约定**显著放置在 HOT 路径必经之处**（例如在阅读量最大的 README/控制文件顶部放置一段简明、明确的提示）。
- 在中央架构/概览文件的开头提供**快速导航表**，指向以前的盲区。
- 从 HOT 文件向 COLD 位置添加**指引/交叉引用 (Cross-reference)**。
- 可选：针对危险或违反约定的行为设置**防护栏 (Guardrail)**（例如 PreToolUse 提示）。

保持路标简短且醒目——Agent 习惯快速浏览，很少长篇大论地阅读。

### 步骤 4 — 使用全新的朴素子 Agent 进行 Retest

**完全相同地**重复步骤 1——相同的任务、相同的重复次数、相同的模型、相同的朴素条件——但在**带有**新路标的 Sandbox 副本上运行。重要注意：

- 使用**全新**的 Agent，不能带有 Baseline 运行的记忆（否则测量的是学习能力而非可发现性）。
- 与 Baseline 配置相比，**仅存在路标差异**。

### 步骤 5 — 与 Baseline 进行 Diff 对比 + 客观的成功测量

将 Retest 和 Baseline 直接并排对比：

| 指标 | Baseline | 设立路标后 | Δ |
|---|---|---|---|
| 成功率 | 例：0/3 | 例：3/3 | +3 |
| 错误行为 | 例：3/3 | 例：0/3 | −3 |
| 盲区 | 例：1 | 例：0 | −1 |

评估——切勿美化结果：

- **有效**（错误行为显著减少）：保留该路标并记录文档。
- **无效**（Δ 变化微弱）：路标位置摆放错误或不够明显 → 返回步骤 2/3，更换路标并重新测量。
- **坦诚说明局限性：** 较小的 n 样本仅作为参考而非严密证明；朴素 Agent 模拟的是“平均无知状态”，而非每一位真实用户；在成功评分中显式检查误报/漏报（究竟什么才被算作“完成”？）。

---

## 迷你案例研究（真实数据）

问题：某个 Ticket Pipeline 约定轻量级完成项各自需拥有**一个**专属的 Ticket 日志——但 Agent 却将所有内容都写入了**一个汇总日志**中。

- **步骤 1 (Baseline)：** 3 个朴素子 Agent，相同任务 → **3/3 使用了汇总日志**（未遵循约定）。
- **步骤 2 (路径分析)：** 阅读量最大的 README 在可见位置未提及单 Ticket 日志规则 → 朴素路径直接引导到了汇总日志。
- **步骤 3 (干预)：** 在 README 的显眼位置放置了一段关于日志约定的简短、明确的“路标”。
- **步骤 4 (Retest)：** 3 个全新的朴素子 Agent，相同任务。
- **步骤 5 (Diff)：** **3/3 错误 → 0/3 错误**，三个 Agent 均创建了正确的单 Ticket 日志。（记录于 Ticket T-20260621-44 中。）

教训：约定并非“措辞过于软弱”——而是在实际被阅读的路径上**不可见**。在正确的位置设立路标，并通过实证验证，解决了问题。

---

## 来源与相关方法

本方法源自欲望路径分析 v2.0（Desire-Path Analysis v2.0，将 Swarm 作为 LLM 行为的实证测量工具）。大规模运行（100 个朴素 probe）的原始参考结果作为源证据已被记录：最大的盲区是一个帮助目录，**0/100** 的 Agent 访问了该目录（尽管包含许多帮助文件）；而“创建新 Skill”任务的成功率为 **0%**，因为没有人找到模板目录——这两者都是典型的可见性问题，而非内容问题。

## 参见

- `swarm-operations` (dev) — 生产任务的 Swarm **协调模式**目录；它仅将欲望路径分析作为概念章节。本 Skill 是包含 Baseline→Retest 循环的可操作**流程**变体。
- `pipeline-optimizer` (dev) — 6 步 Pipeline 改造流程；其使用全新子 Agent 的重测对应于此处步骤 4–5。
- `bugfix-protocol` / 系统化调试 — 用于解决真实代码 Bug 而非可见性问题。

## 修改日志

### 0.1.0 (2026-06-21)
- 首次从 Desire-Path Analysis v2.0 移植（来源：swarm-ai/BACH）。
- 专注于可操作的 5 步流程（Baseline → 路径分析 → 干预 → Retest → Diff）；故意省略 Swarm 协调模式（保留在 `swarm-operations` 中）。包含占位符的用户中立说明；真实迷你案例研究。
