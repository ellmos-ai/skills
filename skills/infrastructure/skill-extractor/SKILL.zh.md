---
name: skill-extractor
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: 从对话历史（当前会话或转录文件）中提取可复用的技能 — 或者改进非常相似的现有技能，而不是创建重复项。在出现“将其做成技能”、“我们应该将其记录为技能”、“从这些/旧对话历史中提取技能”、“使这种工作方式可复用”或使用 `/skill-extract` 时使用此技能。还涵盖针对许多旧转录的大批量运行（通过子 Agent 进行数据缩减）。对于重复发生的自动化任务（Cron/Schedule/Loop），请改用姐妹技能 workflow-extract。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, extraction, transcript, chatverlauf, meta, dedup, neutralisierung, workflow]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

> **中文** — `skill-extractor` 官方中文版本。


<img src="banner.png" width="100%" alt="skill-extractor banner">

# Skill-Extractor — 从对话历史中提取 Skill（中文）

## 概述与目的

宝贵的工作方式往往诞生于会话中：一个问题经过艰苦努力得以解决，用户进行了多次纠正，最终形成了一套有效的流程 — 但下一次 Agent 又得从零开始。本 Skill 旨在从对话历史中提炼出值得保存的内容，并根据本地 Skill 库的规范将其制作成 Skill。核心原则：**先扩展后新建** — 如果存在非常相似的 Skill，则对其进行改进，而不是创建重复项。

界定：此处的输出是一个**可调用的 Skill**（Agent 根据需要加载的技能/流程）。如果希望将对话历史转化为**自主运行的自动化**（循环 Prompt、Cron、Schedule），请使用姐妹 Skill `workflow-extract`。

## 流程

### 1. 确定来源

三种输入形式：

| 来源 | 获取方式 |
| --- | --- |
| **当前会话** | 直接使用对话上下文 — 无需文件 |
| **单个转录文件** | 读取文件；位置与解析参见 `transcript-quellen.md` |
| **批量（多个旧对话）** | 先通过子 Agent 进行数据缩减，再进行提取：参见“批量模式”章节 |

### 2. 寻找值得提取的内容

并非每个会话都包含 Skill。寻找以下信号 — 它们表明其中蕴含着付出高昂代价才获取且会再次需要的知识：

- **重复性：** 同一流程出现了 ≥2 次（在本次会话或跨多个会话中）。
- **纠正循环：** 用户对 Agent 进行了多次微调，直到结果正确 — 最终版本是提炼出的精华，而纠正是理由依据（“为什么要这样做”）。
- **显式标记：** “记住这一点”、“我们总是这样做”、“下次直接这样做”。
- **工具链：** 一套行之有效的非显而易见的工具/命令序列（包括需要避免的死胡同）。
- **决策规则：** 在不同备选项之间做出选择的标准。

记录每个候选对象：触发条件（何时需要）、流程（步骤）、理由依据（为何这样处理而非其他方式）、陷阱（出了什么问题）、输出形式。

### 3. 去重关卡（Dedup Gate）：先扩展后新建

在编写任何内容之前，先检查现有环境：

1. 将候选关键字与 Skill 目录（Agent 的部署文件夹，例如 `~/.claude/skills/`，以及 — 如果存在 — 作为单一事实来源的精选 Skill 库；包含已注册的插件 Skill）进行检索匹配。
2. 真正**阅读** 2–3 个最接近的 Skill，而不仅仅是比较名称。
3. 做出决定：

| 检查结果 | 操作 |
| --- | --- |
| 候选内容核心已被覆盖 | **扩展：** 将缺失的元素融入现有 Skill（新章节、新技术、新陷阱），提升 MINOR 版本号，添加变更日志条目 |
| 部分重叠，但核心不同 | **新 Skill：** 添加互相引用（“相关 Skill”）指向相邻 Skill — 切勿重复内容，而是进行引用 |
| 无类似内容 | **新 Skill** |

经验法则：如果候选对象超过一半的内容已存在于某个 Skill 中，则进行扩展。满是近似双胞胎的 Skill 库不如一个精心维护的 Skill。

### 4. 抽象中立化（Neutralize）

原始材料充满了会话特定的细节。在编写之前，按照 `neutralisierung.md` 中的规则进行抽象：将机制（通用）与配置（用户/系统特定）分离，用占位符或明确标记的配置块替换具体的路径/主机/名称。目标：使 Skill 适用于其他用户、其他系统和其他项目。

### 5. 编写 Skill

- **格式：** 遵循目标库的规范（Frontmatter、命名方案、语言、变更日志）。在本库中：`docs/CONVENTIONS.md`（完整的 YAML 头部、kebab-case 命名、德语优先、语义化版本控制）。
- **写出具有强触发力的 Description：** description 是触发机制。既要写明 Skill 做了什么，也要写明何时触发（典型的用户表述） — Skill 往往更容易触发太少而非太多。
- **原因重于步骤：** 将纠正循环中的理由依据融入 Skill 中。仅列出步骤的 Skill 在遇到第一个特例时会被误用；而解释了原因的 Skill 则具备迁移适用性。
- **记录陷阱：** 会话中的死胡同极为宝贵 — 应将其作为“红旗（Red Flags）”或“陷阱”章节纳入。
- **保持精简：** 控制在约 300 行以内；将详细材料拆分至 `SKILL.md` 所引用的参考文件中。

### 6. 命令封装器（可选）

如果 Skill 需要定期被直接调用，请创建一个斜杠命令（对于 Claude Code：在 `~/.claude/commands/<name>.md` 中创建一个简短的 Markdown 文件，指向该 Skill 并传递参数）。规范：Command = 轻量级入口，具体内容存放在 Skill 中。

### 7. 注册与测试

- 保存至库中（正确的分类）并部署至运行环境（此处：`python skill_sync.py deploy <name>` — 首次安装需要明确指定名称）。
- 触发测试：构思 2–3 个应触发该 Skill 的真实 Prompt，检查 description 是否生效。
- 对于完整的评估循环（测试用例、基线对比、描述优化），如果已安装则使用 `skill-creator` — 本 Skill 是提取器，而非测试实验室。
- 索引/路由维护：更新 Skill 查找器/索引 Skill（如果存在，此处为：`code-skill-index`、`skill-finder` 路由表）。

## 批量模式：许多旧对话历史

转录文本通常很大（往往 >100k Token）；切勿将其全部原始文本直接加载到单个上下文中。
通过子 Agent 进行 Map-Reduce（模式：`swarm-operations` Skill，任务蜂群）：

1. **盘点：** 列出转录文件（位置参见 `transcript-quellen.md`），按项目/时间段打包。对于非常庞大的数据集，首先使用现有的收集器/提取器进行缩减（例如仅包含用户 Prompt 的 Prompt 监听器/研究数据集） — 用户 Prompt + 纠正包含最多的信号。
2. **Map：** 每个包分配一个任务明确的子 Agent：“阅读这些转录，将 Skill 候选对象以紧凑列表形式汇报（触发条件、流程、理由依据、陷阱、出处会话）” — 仅返回提炼出的内容，切勿返回原始文本。
3. **Reduce：** 合并候选列表，进行聚类，合并重复项。频次很重要：在 5 个会话中出现的模式比一次性的技巧更具候选价值。
4. **关卡 + 构建：** 对顶级候选对象执行正常流程的步骤 3–7。在批量构建之前，向用户提供一份带编号的候选列表供选择 — 否则批量提取会产生 Skill 垃圾。

## 示例与应用

```text
User: „Wir haben jetzt dreimal PDF-Rechnungen nach demselben Schema geparst —
mach daraus einen Skill."

1. Quelle: aktuelle Session. Signal: Wiederholung (3×) + Korrektur („Beträge immer
   als Dezimalzahl mit Punkt, nicht Komma").
2. Dedup-Gate: Suche findet `pdf`-Skill (generisch, Erzeugung/Extraktion) — Kern
   überlappt nicht (hier: Rechnungs-Schema + Validierungsregeln) → neuer Skill
   `invoice-parsing` mit Querverweis auf `pdf`.
3. Neutralisieren: konkreter Ablageordner und Firmenname → Konfigurationsblock.
4. Skill schreiben: Schema-Tabelle, die Komma/Punkt-Korrektur als Fallstrick,
   Changelog 1.0.0. Trigger-Test mit „lies diese Rechnung ein".
```

## 红旗

| 想法 | 现实 |
| --- | --- |
| “我来快速新建一个 Skill” | 先通过去重关卡 — 先扩展后新建。 |
| “我保留这些路径，反正就是给这个系统用的” | 必须进行中立化抽象；具体细节属于配置块。 |
| “历史记录太长了，我凭记忆总结一下” | 专门查找信号（纠正、标记） — 记忆往往会抹平那些使 Skill 产生价值的关键细节。 |
| “每个会话都能产生一个 Skill” | 没有重复/纠正/标记信号：就不能生成 Skill。 |

## 相关 Skill

- `workflow-extract` — 同样的提取过程，但目标是自主运行的自动化。
- `skill-explorer` — 针对 Skill 环境的审计/清理（在大范围内使用去重关卡）。
- `skill-creator`（插件） — 针对已完成 Skill 的评估循环和描述优化。
- `swarm-operations` — 用于批量模式的蜂群模式。

## 变更日志

### 1.0.0 (2026-07-03)
- 初始版本。源于将 Codex 自动化和对话历史系统地抽象为 Skill 的任务。