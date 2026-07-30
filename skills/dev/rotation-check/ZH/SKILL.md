---
language: zh
---

> **中文** — `rotation-check` 官方中文版本。

# Rotation-Check — 单次运行单个目标、公平覆盖与记忆机制

## 概述与目的

要定期检查包含多个项目的流水线（源码、样式、健康状况、安全性、翻译等），必然会面临分配难题：每次运行都检查所有项目成本过高；而如果没有记忆机制，每次运行又会随机重复检查相同的内容。轮询模式（Rotation pattern）完美解决了这两个问题：**每次运行仅选择一个目标，按“未检查时间最长”进行选择，并使用注册表（Registry）作为记忆载体。** 这样，即使执行频率较低（如每日或每周），数周内也能无遗漏且无重复劳动地覆盖整条流水线。

该模式已在多个项目流水线的成熟生产自动化体系中被验证为核心骨干。

## 核心组件

### 1. 每个流水线配置两个文件（一次性创建）

| 文件 | 内容 | 性质 |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | 每次检查仅占一行紧凑记录：目标、日期、检查类型、结果、下一步计划 | 状态总览 — 每次选择目标前必须先读取 |
| `CHECKS-LOG.txt` | 每次运行的简短历史记录，包含详细信息/凭据 | 日志 — 仅追加模式（append-only） |

这两个文件均存放在流水线根目录（而非单个项目中），以便运行任务可以通过一次读取获取全局状态。注册表单行格式：

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. 选择规则

1. 读取注册表和日志（必选步骤，必须在选择目标前执行 — 否则会导致重复检查）。
2. 候选目标：在此检查类型下，从未检查过或最长时间未检查的目标。
3. 避让/跳过：如果目标最近刚被**密切相关**的检查处理过（例如在源码检查后立即进行引用检查是没有意义的），或者目标当前处于锁定/正在编辑状态，则进行避让（尊重锁机制）。
   **兄弟冷却期（Sibling Cooldown）：** 当有多个相关检查在同一个目标集上运行（例如针对同一流水线的开发、Bug 查找和代码审查）时，约定一个缓冲期（经验值为 ~24 小时），在此期间不重复选择被兄弟检查处理过的目标 — 避免碰撞和冲突的并行修改。
4. 仅在有充分理由时才打破顺序优先处理（例如自上次检查以来进行了重大重构） — 并在日志中说明原因。

### 3. 执行检查 — 具备只读退出机制

针对选择的**唯一**目标应用实际检查（检查内容可自由定义：源码检查、代码风格检查、安全审计等）。存在两种合法输出：

- **发现问题（Finding）：** 修复属于当前范围的问题；较大的事项作为后续任务记入项目本地的 TODO/AUFGABEN 文件中（检查过程不必亲自解决所有问题）。
- **无须处理（Nothing to do）：** 简要记录并结束。空跑（无变更）也是一种有效结果，绝非失败 — 绝不能为了“查出点什么”而擅自扩大检查范围。

### 4. 记录与文档

- 追加/更新注册表行（紧凑），编写日志条目（详细信息/凭据）。
- **日志整理（Log Hygiene）：** 当注册表/日志过于庞杂时（经验值为数百行），将旧状态移至 `_archiv/`，新建一份干净的文件，并在文件头指明前任文件（路径 + 日期）。
- **路径漂移（Path Drift）：** 如果预期路径指向空处（目标被移动/重命名），切勿重新创建 — 须通过流水线的主状态文件/注册表进行修正，并将错误路径记录在失败日志中。

### 5. 节奏与频率

频率应与被检查对象的变更速率挂钩：对稳定资产的轮询检查每周运行一次即可（以 ~12 个目标为例，每次运行一个目标 ≈ 每季度覆盖整条流水线）；对于快速变更的检查（如活动开发项）则每日运行。实践经验：最初设为每小时一次的检查几乎全部缩减为每日/每周 — 覆盖率保持不变，而成本大幅下降。

## Prompt 模板（适用于调度器/自动化）

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## 常见误区（Red Flags）

| 错误想法 | 实际情况 |
| --- | --- |
| “我挑个感兴趣的项目检查就行” | 必须仅通过注册表选择 — 否则会出现偏爱特定项目和盲区问题。 |
| “检查完我再去读注册表” | 必须在检查前读取。注册表是选择标准，而不只是事后的记录日志。 |
| “一次运行多检查几个目标效率更高” | 每次仅检查一个目标能保持单次运行短小、幂等且随时可中断；整体覆盖量是通过持续轮询达到的。 |
| “这次运行什么都没做，白费了” | 简要记录一次空跑能更新系统的记忆状态 — 这本身就占了整个系统一半的价值。 |

## 相关 Skill

- `workflow-extract` — 从会话/外部自动化中提取并构建自动化流程；将本架构作为标准组件使用。
- `pipeline-optimizer` — 用于流水线的结构性重构（rotation-check 负责日常维护，optimizer 负责重构更新）。

## 变更日志

### 1.1.0 (2026-07-03)
- 增加了兄弟冷却期（Sibling Cooldown）选择规则（防止针对同一目标集的关联检查之间发生冲突；该规则提炼自自动化资产的全量分类实践）。

### 1.0.0 (2026-07-03)
- 初始版本。从 Codex 自动化资产中抽象提炼（在 77 个自动化中有 ~40 个采用了轮询模式：包含 CHECKED-REGISTRY/CHECKS-LOG 的研究/软件/Roblox 检查）。
