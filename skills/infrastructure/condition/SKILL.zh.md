---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-28
description: 用于目标、提示词和任务的灵活条件语言。将条件、时间戳和顺序依赖关系转换为可验证的 Gate，以确保只有在获得证实批准后才执行子步骤。凡涉及 /condition、/if、/if-only、/when、/after、/and 或 /or，以及“只有当”、“一旦”、“仅当”、“之后”、“等到”、“然后”或“之前不行”等表达时，始终使用此技能。当多个子目标互相依赖或某个目标包含后续批准时，也应使用。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'condition/SKILL.md', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="condition banner">

> **中文** — `condition` 官方中文版本。


# condition — 目标与提示词的条件语言

## 核心理念

自然文本中的条件容易被遗漏。因此，需将每个相关条件转换为具名的、可验证的 Gate：

> 读取时宽容，验证时严谨。

输入可以是自然语言且不完整的。但内部转换必须明确记录：

1. 必须满足哪个条件，
2. 哪个子步骤被阻塞，
3. 哪个工具查询作为凭证，
4. 未满足条件意味着延迟还是禁止。

仅锁定受影响的子步骤，继续进行独立的任务。

## 语言构建块

| 表达式 | 语义 | 示例 |
| --- | --- | --- |
| `/condition <条件> -> <步骤>` | 规范 Gate | `/condition Tests green -> Build release` |
| `/if <条件> -> <步骤>` | `/condition` 的同义词 | `/if Review complete -> Merge` |
| `/when <条件> -> <步骤>` | 条件满足时立即执行 | `/when Export finished -> Verify report` |
| `/if-only <条件> -> <步骤>` | 仅在满足时执行；否则完全不执行 | `/if-only Backup proven -> Delete legacy data` |
| `/after <时长> -> <步骤>` | 从设置时间起的延迟时间 | `/after 30 minutes -> Check status` |
| `/and` | 所有关联条件必须全部成立 | `/if Tests green /and Review present -> Merge` |
| `/or` | 至少一个条件成立即可 | `/if Approval present /or Emergency rule active -> Start` |

当一个 Prompt 包含多个 Gate 时，使用编号条件，如 `/condition 1 ...` 和 `/condition 2 ...`。当混合使用 `/and` 与 `/or` 时，切勿自行捏造隐式的运算符优先级：应使用括号或编号子条件。如果含义仍然模糊，在释放风险步骤之前必须先询问确认。

将 `/if-only` 视为禁止指令。如果无法证实该条件，切勿执行该步骤。若表述不够清晰且可能带来不可逆后果，请选择更严格的解读。

## 执行流程

### 1. 规范化条件

将输入翻译为可验证的句子。将设置时的相对时间转换为带有时区的绝对时间戳。

| 输入 | 规范化条件 | 凭证类别 |
| --- | --- | --- |
| `time 06:00` | 系统时间在约定时区内至少达到 06:00 | 时钟/时间工具 |
| `after 2 hours` | 系统时间至少达到设置时间加上两小时 | 时钟/时间工具 |
| `wenn Worker A fertig ist` | A 的验收产物或任务状态显示已完成 | 任务/文件工具 |
| `wenn Tests grün sind` | 规定的测试运行成功结束 | 进程/测试工具 |
| `nach dem Push` | 目标 Remote 包含预期的 Commit | 版本控制工具 |
| `wenn der User zustimmt` | 会话中存在明确的用户同意 | 用户输入 |

如果没有可识别的客观凭证途径，应明确说明。切勿将 Gate 表述为只能通过猜测来关闭的形式。

### 2. 记录 Gate 状态

如果存在持久化的 Gate、Task 或 Memory 存储，至少在其中保存以下字段：

```text
id
condition
blocks
mode = wait | only
proof_method
status = open | met | dropped
created_at
evidence
```

如果没有持久化存储，需在当前 Goal、Task 计划或交接文档中清晰地维护状态。只有在所用存储确实具备持久性时，才能断言 Gate 能跨 Session 留存。

已有的 Runtime 适配器可以使用不同的命令名称。在功能上，它需要：`open`、`list`、`meet` 和 `drop` 或同等的操作。

### 3. 重排工作顺序

一个开启状态的 Gate 不会阻塞整个任务。执行所有独立的步骤，并在执行下一个依赖步骤前重新检查 Gate 状态。

切勿在短周期的 Agent 循环中进行主动轮询（polling）。对于较长的等待时间，应使用调度器（Scheduler）、后台任务或在发生时进行一次性通知的事件。收到唤醒信号后，仍需使用预定的工具重新证实实际条件。

### 4. 严格验证与关闭

首先执行工具查询，然后使用具体凭证关闭 Gate。合适的凭证包括例如：

- 时间：带有时区的新测时间戳，
- 文件：预期产物的路径、元数据或哈希值，
- 测试：已执行的命令、退出代码（Exit Code）及相关摘要，
- 仓库：分支（Branch）、Commit ID 及 Remote 比对，
- 进程或任务：稳定的 ID 及新测最终状态，
- 同意：当前上下文中的明确用户回复。

当可以获得独立凭证时，估计、预期状态或仅凭其他 Worker 的口头声称都是不够的。

如果 Gate 因任务变更而失效，应附带理由将其标记为 `dropped`。对于 `/or`，也应关闭或废弃不再需要的备选方案，以免残留 Zombie Gate。

### 5. 升级处理

当所有独立步骤均已完成时：

1. 检查阻塞的前置工作是否可以在任务内部主动完成，
2. 对于纯等待条件，使用合适的调度器或后台任务，
3. 对于用户决策或外部依赖，带着开启的 Gate 和清晰的中间状态进行交接。

切勿从条件中衍生出额外的授权。满足的 Gate 仅改变顺序；它不会扩大任务获得授权的范围。

## 示例与应用

### 带有时间条件的目标

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

数据检查可以提前进行。在当前时间查询证实至少达到 16:00 之前，发布操作保持锁定。

### 包含多个条件的提示词

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

分别验证两个 Gate。之后才进行 Merge。

### 禁止而非延迟

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

在没有经证实妥善的备份之前，切勿删除任何内容，并在最终报告中注明该开启的禁止项。

## 常见误区

- 仅在连续文本中重复条件，而不是将其作为状态进行跟踪。
- 尽管仅阻塞了一个子步骤，却暂停了整个 Goal。
- 在保存相对时间时未记录设置时间戳和时区。
- 用假设或自我陈述替代工具凭证。
- 将 `/if-only` 误当做单纯的等待处理。
- 在使用 `/or` 后保留不再需要的备用 Gate 为开启状态。
- 将供应商、模型、用户或主机名称硬编码到通用机制中。
- 将本地 Runtime 路径视为语言本身的先决条件。

## 变更日志

### 1.1.0 (2026-07-28)

- 针对共享技能 Runtime，采用供应商、用户和系统中立的语言表述。
- 明确了在 Goal 和 Prompt 中的用法。
- 将 Runtime 描述为可替换的适配器；删除了固定本地路径和模型名称。
- 澄清了模糊的 `/and`/`/or` 关联、持久化状态和授权边界。

### 1.0.0 (2026-07-25)

- 包含 `/condition`、`/if`、`/if-only`、`/when`、`/after`、`/and` 和 `/or` 的初始版本。