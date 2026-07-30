---
name: decision-briefing
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: 每当有多个决策挂起或积压时使用——无论是在特定主题、项目、文档中，还是在整个会话期间：对它们进行盘点，提供带有 A/B/C/D 选项及明确推荐的编号简报，接受字母答复（包括批量答复），记录结果并写回源文档。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [entscheidung, briefing, batch, decision-session, priorisierung, workflow]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/decision-briefing/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `decision-briefing` 官方中文版本。


# Decision-Briefing — 处理单一主题上的多个决策

> 将一堆待办决策转化为带推荐意见的编号简报，用户可以通过单个字母快速回答——既可逐一回答，也可批量处理。

---

## 何时使用？

**只要有多个决策待处理**，无论属于何种主题，均应使用。典型场景：

- 某领域/主题中积压了许多待决事项
- 一份文档（计划、TODO 列表、概念方案）中包含多个未定要点
- 对话过程中积累了多个决策问题
- Agent 本身有多个问题需要询问用户——将其打包为简报，而非逐个发问
- 用户希望在稳固的基础上快速清理待决事项

**触发词：** 待办决策、决策会话、简报、梳理决策、逐一处理、让我们决定所有这些

**适用范围：** [decide](../decide/SKILL.en.md) 为单项决策提供框架。`decision-briefing` 负责协调梳理某一主题上的多个决策，并将 `decide` 应用于复杂的个案。

---

## 核心交互体验 (Core UX)

本 Skill 的核心在于简报格式。每个决策的呈现方式都旨在将用户的回答成本降低至单个字母：

- **编号：** `[E01]`、`[E02]`、… — 在整个会话中保持稳定的引用
- **简短问题** + 1–2 句背景上下文
- **字母选项** A/B/C/D（2–4 个选项，仅在必要时提供更多）
- **明确标注推荐** 并附带一句话理由（例如 `→ 推荐：A — 因为 …`）
- 可选：后果提示（做出该选择后将产生什么结果）

**用户回答格式：**

```
Single:    "E01: A"  or  "1A"
Batch:     "1A 2C 3B"  or  "E01: A, E02: C, E03: B"
Deepen:    "E02: more info"  or  "2?"
Defer:     "E03: later"
```

---

## 工作流与步骤

```
Topic + decisions at hand
     |
     v
Phase 1: CAPTURE & INVENTORY
     |
     v
Phase 2: PREPARE THE BRIEFING
     |
     v
Phase 3: DECISION SESSION
     |
     v
Phase 4: RECORD & WRITE BACK
```

### 阶段 1：捕获与盘点

来源：用户提及的内容、现有的文档或对话上下文。无需进行系统级的全量扫描——仅处理已有信息。

1. 列出所有待决策事项（每项占一行：简短标题）
2. 识别并合并**重复项**（同一问题被多次表述）
3. 标记**依赖关系**（“E04 依赖于 E01”）
4. 确定**顺序**：阻塞项优先（其他决策所依赖的事项），其次按紧急程度排序
5. 将列表展示给用户确认（“我收集全了吗？是否有遗漏？”）

### 阶段 2：准备简报

针对每个决策：

```
[E01] <Short question>
  Context: <1-2 sentences: Why is this up? What depends on it?>
  A) <Option>
  B) <Option>
  C) <Option>
  → Recommendation: <letter> — <one-sentence rationale>
  (optional) Consequence: <what follows from the choice / next action>
```

良好选项的设定规则：

- 各选项必须互斥并覆盖完整光谱
- 如有必要，可包含“保持现状”或“推迟”选项
- 推荐理由需透明客观——切忌暗中诱导
- 事实不清时：先澄清（或标记为开放性问题），切勿盲目推测

### 阶段 3：决策会话

1. 展示简报——每个消息包含一个决策，或作为批量一次性展示；当决策数量 >5 时，按 3–5 个一组分块展示
2. 接收字母答复并予以确认
3. 收到“更多信息”答复时：对该决策进行深入分析（使用下文的方法工具箱）
4. 对于复杂的单项决策（多标准、高风险）：升级至 [decide](../decide/SKILL.en.md) Skill（加权评分、情景分析）
5. 明确将推迟的决策记录为待决事项——绝不隐蔽丢弃

### 阶段 4：记录与写回

1. 创建**结果表格**：

```
| No.  | Decision            | Chosen | Status   |
|------|---------------------|--------|----------|
| E01  | <short title>       | A      | decided  |
| E02  | <short title>       | C      | decided  |
| E03  | <short title>       | —      | deferred |
```

2. 将已决策事项写回**源文档/TODO 文件**——写在未决问题所在的位置，例如：

```
DECISION: <question>
  → DECIDED 2026-06-13: Option A (<short form>)
  → Next action: <if the decision implies a follow-up action>
```

3. 保持**推迟事项在源文档或 TODO 列表中显式为未决状态**，以便在下次简报中重新出现

---

## 示例与应用

主题：协会网站重构——项目计划中的 3 个待决事项。

```
[E01] Which system for the new website?
  Context: Current site is hand-maintained HTML; 2 people will maintain content in the future.
  A) Static site generator (fast, secure, maintained via Git)
  B) Classic CMS with admin interface
  C) Hosted website builder
  → Recommendation: B — two non-technical editors need an interface, not Git.

[E02] How is it hosted?
  Context: Budget ~10 EUR/month, no dedicated admin in the club.
  A) Shared hosting with the current provider
  B) Small dedicated VPS
  C) Managed hosting matching the chosen system
  → Recommendation: C — least maintenance effort without an admin; consequence: depends on E01.

[E03] When does the new site go live?
  Context: Content is 60% migrated; club anniversary in 3 months.
  A) Immediately as a soft launch (rest follows)
  B) After complete content migration
  C) On the anniversary as the deadline
  → Recommendation: A — reversible and yields early feedback; final content follows.
```

用户以批量形式回答：**"1B 2C 3A"** → 生成结果表格，随后在项目计划中将这三个决策标记为 DECIDED。

---

## 方法工具箱（用于“更多信息”及深入分析）

| 方法 | 适用场景 | 概要 |
|--------|------|---------|
| **优缺点矩阵 (Pro/con matrix)** | 2–3 个选项，快速比较 | 并排评估所有选项 |
| **加权评分法 (Weighted scoring)** | 多项评价标准 | 对标准加权，按选项打分（尽可能定量） |
| **二阶思考 (Second-order thinking)** | 后果/风险不明 | 后果背后的后果是什么？ |
| **事前剖析 (Premortem)** | 高风险决策 | “失败了——为什么？” 提前查找薄弱环节 |
| **10/10/10 法** | 情绪/时间维度偏差 | 10分钟/10个月/10年后来看，这项决策会怎样？ |

---

## 工作原则

- **绝不强加决策：** 提供充分信息，透明地阐明推荐理由——决策权始终在用户手中
- **偏差识别：** 当思维误区显现时予以指出（如确认偏误、沉没成本）
- **关注可逆性：** 快速决定可逆决策；对不可逆/终极决策更加审慎深入
- **尊重时间紧迫度：** 快速决策需要更简易的方法——并非每个问题都需要加权评分分析

---

## 适用范围与协同效应

| 功能 | `decide` | `decision-briefing` |
|---|---|---|
| 使用框架结构化单项决策 | ✓ | — |
| 盘点某一主题上的多个决策 | — | ✓ |
| 带有 A/B/C 选项的编号简报 | — | ✓ |
| 批量回答 ("1A 2C 3B") | — | ✓ |
| 写回源文档 | — | ✓ |

**协同效应：** 对于会话中复杂的个案，`decision-briefing` 会应用 `decide` 中的框架（加权评分、情景分析）。对于此前更广泛的思考过程（分析 → 构思 → 决策），请参阅 [structured-thinking](../structured-thinking/SKILL.en.md)。

---

## 变更日志

### 1.0.0 (2026-06-13)
- 移植自 BACH 专家 Skill `decision-briefing` v1.0.0；有意移除了扫描器组件（scanner.py、sources.json、标记扫描）——捕获过程保持轻量化，完全基于已有上下文

---

*移植自 BACH | 无扫描器独立版本*

**另请参阅：** [decide](../decide/SKILL.en.md)（单项决策框架）| [structured-thinking](../structured-thinking/SKILL.en.md)（分析 → 构思 → 决策的元工作流）
