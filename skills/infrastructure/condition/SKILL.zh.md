---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-30
description: >
  用于目标、提示词和任务的灵活条件语言。将条件、时间戳和顺序依赖关系翻译为可验证的关卡（gate），
以便仅在经过证实批准后才执行子步骤。当出现 /condition, /if, /if-only, /when, /after, /and 或 /or
以及“只有当”、“一旦”、“仅当”、“在……之后”、“等待直到”、“之后”或“之前不行”等表述时，始终使用此 Skill。
当多个子目标互相依赖或某个 Goal 包含后续批准步骤时也可以使用。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "condition/SKILL.md"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="condition banner">

# condition — 目标与提示词的条件语言

## 核心理念

连续的文本条件很容易被忽视。因此，将每个相关条件翻译为一个具名的、可验证的关卡（Gate）：

> 解读时宽容，验证时严苛。

输入可以是自然语言且不完整的。然而，内部翻译必须明确记录：

1. 必须满足哪个条件，
2. 哪个子步骤被阻塞，
3. 哪个工具查询作为证据，
4. 未满足是意味着延迟还是禁止。

仅锁定受影响的子步骤。继续执行独立的工作。

## 语言构建块

| 表达式 | 语义 | 示例 |
| --- | --- | --- |
| `/condition <条件> -> <步骤>` | 标准关卡 | `/condition 测试通过 -> 构建发布` |
| `/if <条件> -> <步骤>` | `/condition` 的同义词 | `/if 审查完成 -> 合并` |
| `/when <条件> -> <步骤>` | 条件一旦发生立即执行 | `/when 导出完成 -> 检查报告` |
| `/if-only <条件> -> <步骤>` | 仅在满足时执行；否则完全不执行 | `/if-only 备份已验证 -> 删除旧数据` |
| `/after <时长> -> <步骤>` | 自设置时间起的时间偏移 | `/after 30 minutes -> 检查状态` |
| `/and` | 所有关联的条件必须全部成立 | `/if 测试通过 /and 审查完成 -> 合并` |
| `/or` | 至少满足一个条件即可 | `/if 已获批准 /or 应急规则生效 -> 启动` |

当提示词包含多个关卡时，使用带编号的条件，如 `/condition 1 ...` 和 `/condition 2 ...`。当混合使用 `/and` 和 `/or` 时，不要发明隐式的运算符优先级：使用括号或带编号的子条件。如果含义仍有歧义，请在释放风险步骤前询问澄清。

将 `/if-only` 视为禁止指令。如果无法证实条件，请勿执行该步骤。在表述模糊且后果不可逆的情况下，选择更严格的解读。

## 流程

### 1. 规范化条件

将输入翻译为一个可验证的句子。设置相对时间时，将其转换为带时区的绝对时间戳。

| 输入 | 规范化条件 | 证明工具类别 |
| --- | --- | --- |
| `time 06:00` | 系统时间在约定时区内至少为 06:00 | 时钟/时间工具 |
| `after 2 hours` | 系统时间至少为设置时间加上两小时 | 时钟/时间工具 |
| `wenn Worker A fertig ist` | Worker A 的交付物或任务状态显示已完成 | 任务/文件工具 |
| `wenn Tests grün sind` | 指定的测试运行成功结束 | 进程/测试工具 |
| `nach dem Push` | 目标 Remote 包含预期的 Commit | 版本控制工具 |
| `wenn der User zustimmt` | 对话中存在明确的用户同意 | 用户输入 |

如果没有可识别的客观证明方式，请公开说明。绝不要将关卡表述为仅凭推测即可关闭。

### 2. 记录关卡状态

如果有持久化的 Gate、Task 或 Memory 存储可用，至少保存以下字段：

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

如果不存在持久化存储，请在当前 Goal、Task 计划或交接文档中保持状态可见。仅当所用存储确实持久时，才声称 Gate 可以跨 Session 存活。

现有的 Runtime 适配器可以使用不同的命令名称。在功能上，它需要：`open`, `list`, `meet` 和 `drop` 或等效操作。

### 3. 重新排列工作

未关闭的 Gate 不会阻塞整个任务。执行所有独立的步骤，并在下一个受控步骤之前重新检查 Gate 状态。

不要在短 Agent 循环中主动轮询。对于较长的等待时间，请使用 Scheduler、后台作业或在触发时进行一次性通知的事件。在唤醒信号后，仍须使用指定的工具重新验证实际条件。

### 4. 严格验证并关闭

首先执行工具查询，然后用具体证据关闭 Gate。适当的证明包括：

- 时间：带时区的测得时间戳，
- 文件：预期交付物的路径、元数据或 Hash，
- 测试：已执行命令、Exit Code 及相关摘要，
- 仓库：Branch、Commit ID 及 Remote 对比，
- 进程或任务：稳定的 ID 及测得的最终状态，
- 同意：当前上下文中的明确用户回复。

当应有独立证明可用时，估计、预期状态或另一个 Worker 的口头断言是不够的。

如果 Gate 因任务变更而作废，请说明理由并标记为 `dropped`。对于 `/or`，同时关闭或丢弃不再需要的替代方案，以免留有僵尸关卡。

### 5. 升级处理

当所有独立步骤都已完成时：

1. 检查阻塞的前置工作是否可以在任务内部主动完成，
2. 对于纯等待条件，使用合适的 Scheduler 或后台作业，
3. 对于用户决策或外部依赖，以带有未关闭关卡和清晰中间状态的形式交接。

不要从条件中衍生出额外的权限。满足的关卡仅改变顺序；它不会扩大经授权的许可范围。

## 示例

### 带时间条件的 Goal

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

数据检查可以事先进行。发布一直保持锁定，直到当前时间查询证实至少已到 16:00。

### 包含多个条件的 Prompt

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

分别验证两个 Gate。之后才允许合并。

### 禁止而非延迟

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

在没有已验证备份的情况下，不删除任何内容，并在最终报告中列出未满足的禁止条件。

## 常见陷阱

- 仅在连续文本中重复条件，而不是将其作为状态来维护。
- 仅因一个子步骤受阻就暂停整个 Goal。
- 保存相对时间时未提供设置时间点和时区。
- 用假设或自我评估代替工具证明。
- 将 `/if-only` 当作普通的等待处理。
- 使用 `/or` 后留有不再需要的替代 Gate。
- 将提供商、模型、用户或主机名硬编码到通用机制中。
- 将本地 Runtime 路径视为语言本身的先决条件。

## 变更日志

### 1.1.0 (2026-07-28)

- 针对共享 Skill Runtime 进行了中立化表述（不依赖特定提供商、用户和系统）。
- 明确了在 Goal 和 Prompt 中的用法。
- 将 Runtime 描述为可替换的适配器；删除了固定本地路径和模型名称。
- 澄清了模糊的 `/and`/`/or` 链接、持久状态及授权边界。

### 1.0.0 (2026-07-25)

- 包含 `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and` 和 `/or` 的初始版本。
