---
name: rotation-check
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-30
description: >
  轮换式流水线检查的基础骨架：每次运行从集合（项目、文件夹、仓库）中精确选择一个目标 —— 优先选择未检查时间最长的目标 ——，
  执行检查，并将结果记录在检查注册表（Registry）和历史日志中。当需要将周期性检查均匀分布到多个项目（"定期检查所有 X 的 Y"）、
  自动化程序必须避免重复检查、创建或使用检查注册表/CHECKS-LOG 结构，或者需要在流水线上公平分配定期质量轮次（源码检查、样式检查、健康检查、审计）时使用此技能。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [automation, check, rotation, registry, pipeline, log, audit, wartung]
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
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="rotation-check banner">
# 轮换检查 — 每次运行一个目标、公平覆盖、记忆机制

## 目的

当需要对包含众多项目的流水线进行定期审计（源码、样式、健康状况、安全性、翻译等）时，往往会面临分配难题：每次运行检查所有项目成本过高；如果没有记忆机制，每次运行又会随机重复检查相同的项目。轮换模式同时解决了这两个问题：**每次运行精确选择一个目标、优先选择"最久未检查"的目标、使用注册表作为记忆。** 这样，即使执行频率较低（每天/每周），也能在数周内可验证且无重复地覆盖整条流水线。

作为成熟的生产自动化体系中横跨多个项目流水线的核心骨架，该模式已得到充分验证。

## 组成要素

### 1. 每个流水线两个文件（一次性创建）

| 文件 | 内容 | 性质 |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | 每次检查对应一行精简记录：目标、日期、检查类型、结果、下一步计划 | 状态总览 —— 在每次选择目标前读取 |
| `CHECKS-LOG.txt` | 每次运行的简短历史条目，包含细节/凭证 | 日志 —— 仅追加 (append-only) |

两者均位于流水线根目录（而非单个项目内部），以便单次运行能够通过一次读取获取全局信息。注册表单行格式：

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. 选择规则

1. 读取注册表和日志（必须在选择目标**之前**执行 —— 否则会导致重复检查）。
2. 候选目标：针对**当前**检查类型从未检查过，或距离上次检查时间最长的目标。
3. 避让/跳过：如果目标最近刚被**密切相关**的检查触及（例如在源码检查之后立即进行引用检查没有任何价值），或者当前处于锁定/编辑状态（尊重锁机制）。
   **兄弟冷冻期 (Sibling Cooldown)：** 如果多个相关的检查覆盖同一组目标（例如针对同一流水线的开发、Bug 查找和 Review），请约定冷却时间（经验值：约 24 小时），在此期间不要再次选择已被兄弟检查处理过的目标 —— 避免冲突和相互矛盾的并行修改。
4. 仅在有充分理由时才破例优先处理（例如自上次检查以来进行了重大改动） —— 并在日志中说明理由。

### 3. 执行检查 — 带 Read-only 退出

将实际检查（可自由定义：源码检查、样式检查、安全审计等）应用于选定的**单个**目标。包含两种有效结果：

- **发现问题 (Finding)：** 在当前范围内修复可以解决的问题；将较大规模的工作作为后续任务记录在项目本地的 TODO/任务文件中（检查本身不必解决所有问题）。
- **无须处理 (Nothing to do)：** 简要记录并结束。空跑是一种合理结果，而非失败 —— 绝不要为了"必须找到问题"而擅自扩大检查范围。

### 4. 记录与文档

- 补充注册表记录行（精简），编写日志条目（细节/凭证）。
- **日志维护：** 如果注册表/日志变得过于冗长（经验值：数百行），将旧状态移动至 `_archiv/`，创建新文件，并在文件头指向上一个文件（路径 + 日期）。
- **路径偏移 (Path Drift)：** 如果预期路径指向不存在的位置（目标被移动/重命名），**切勿**重新创建 —— 通过流水线的主控状态文件/注册表进行修正，并将错误路径记录在失败日志中。

### 5. 节奏控制

将检查频率与被审计对象的变更速率挂钩：针对稳定代码库的轮换检查每周运行一次效果良好（每次运行一个目标 ≈ 针对 ~12 个目标每季度覆盖整条流水线）；快速变化的检查（例如针对活跃开发工作）每天运行。实践经验：最初设置的每小时检查几乎全部缩减为每天/每周 —— 覆盖率保持不变，而成本大幅下降。

## Prompt 模板（用于 Scheduler / 自动化）

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

## 红线预警 (Red Flags)

| 想法 | 事实 |
| --- | --- |
| "我随便挑一个感兴趣的项目吧" | 必须严格通过注册表选择 —— 否则会导致偏愛项目偏差和盲区。 |
| "检查完我再去读注册表" | 必须在检查前读取。注册表是选择标准，而不只是记录日志。 |
| "单次运行处理多个目标效率更高" | 单个目标能保持单次运行短小、幂等且可随时中断；处理量是通过轮换积累的。 |
| "这次运行没有发现问题，白跑了" | 一次经记录的空跑更新了系统的记忆 —— 这构成了该体系一半的价值。 |

## 相关技能

- `workflow-extract` — 从 Session / 外部自动化构建自动化流程；使用本骨架作为标准组件。
- `pipeline-optimizer` — 用于流水线的结构化重构（Rotation-Check 负责日常维护，Optimizer 负责全面改造）。

## 更新日志

### 1.1.0 (2026-07-03)
- 补充兄弟冷冻期作为选择规则（防止覆盖同一目标集合的相关检查之间发生碰撞；基于自动化资产全量分类的发现）。

### 1.0.0 (2026-07-03)
- 初始版本。从 Codex 自动化资产中抽象提取（轮换模式应用于 77 个自动化中的约 40 个：带 CHECKED-REGISTRY/CHECKS-LOG 的研究/软件/Roblox 检查）。
