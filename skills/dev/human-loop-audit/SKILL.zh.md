---
name: human-loop-audit
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "交互式拉链式审计流程，适用于一系列应用/被测对象：用户实时测试并在聊天中给出简短反馈，智能体在此过程中已经启动下一个对象，并同时评估上一个对象的反馈（结构化记录，立即将修复任务委派给工作进程）——而不是顺序等待。当出现\"human-loop-audit\"、\"lass uns die Apps im Reißverschluss durchtesten\"、\"ich teste, du wertest aus und reparierst\"，或需要与用户共同测试一系列GUI/产品且发现问题应立即转化为修复时，使用此技能。完成时输出每个对象的结构化发现列表（正常/缺陷/期望），以及已启动修复任务的列表。"
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [audit, usertest, human-in-the-loop, gui-test, reissverschluss, delegation, feedback]
language: zh
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: b65128841e358d7ba0f7a3892feea4ef776f3b6e3021109bb89010a6243e82d5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:09.984391+00:00"
---
<img src="banner.png" width="100%" alt="human-loop-audit banner">

# Human-Loop-Audit

> **不要与`reissverschluss-merge`混淆：** 名称共享"拉链"意象，但`reissverschluss-merge`是一个**Git合并流程**（分段合并两个代码分支）。这里的`human-loop-audit`与Git无关——它是一个**与用户共同进行的测试/审计流程**。两个技能都只把拉链作为相同的基本思想使用（两股线齿对齐地交错合并，而不是逐股依次进行）。

## 目的与角色分工

用户的时间是**串行瓶颈**：只有他能真正实时操作应用，并在几秒内判断它的使用感受是否正确。其他一切——打开对象、结构化记录反馈、启动修复——都由智能体承担，并且是在用户**已经**在测试下一个对象的**同时**进行，而不是之后。智能体同时扮演驾驶舱操作员和评估者的角色。

**核心在于重叠，而不是顺序本身：** 纯粹顺序的"打开应用→等待→评估→打开下一个应用"会浪费用户测试期间的等待时间。Human-Loop-Audit正是利用了这段窗口。

## 流程

1. 用户发出**"start"** → 智能体打开**第一个**被测对象。只需启动进程（例如`Start-Process <exe>`，或该对象对应的启动命令）——**无需接管桌面**，用户自行操作。简短确认其已打开。
2. **用户测试并在聊天中写下反馈**——简短的要点即可，不要改写任何会改变含义的内容。
3. **反馈一经到达，两件事并行而非依次进行：**
   - 智能体**立即打开下一个被测对象**，使用户无需等待即可继续测试。
   - **同时**，智能体评估已收到的反馈：按对象结构化记录发现（**正常** / **缺陷** / **期望**，附简短描述），并且对于缺陷或明确的期望，**立即将修复任务委派给一个工作进程**（不要攒到"之后"再委派——修复应当在用户继续测试的同时进行）。
4. **重复**，直到所有对象测试完毕（对每个后续对象回到第2/3步）。
5. **收尾：** 向用户呈现发现列表（每个对象的正常/缺陷/期望）以及已启动修复的列表（工作进程/任务/状态）。

## 发现结构（每个被测对象）

| 对象 | 状态 | 发现 | 修复委派给 |
|---|---|---|---|
| `<App/Objekt-Name>` | 正常 / 缺陷 / 期望 | 简短要点，保留用户原话 | 若已委派，填写工作进程名称/会话 |

一个对象可以有多行（多个发现）。不会悄悄合并任何内容——收尾时应从该表读取，而不是凭记忆。

## 与相关技能的区别

- **`reissverschluss-merge`**（见上方说明）——纯粹的Git合并流程，尽管名称意象相同，但没有实质交集。
- 存在相关但范围更窄的、带有固定附加阶段（资源审查、提交表单、ID回写）且**顺序**实施（"修复项的实施单独进行"）的波次/商店提交测试周期，它们是项目本地流程。`human-loop-audit`则刻意作为**通用**流程，适用于**任意**应用/GUI系列，并且修复**立即且并行**地委派，而不是作为之后单独的一步。
- **`bugsweep` / `bugfix-protocol`**——实际的修复工作，`human-loop-audit`会将其委派出去；该技能本身不做修复。

## 常见陷阱

- **不要等待评估完成后才打开下一个对象**——纯粹顺序的"先等待、再评估、然后打开下一个"会白白浪费正是本技能所依赖的重叠。
- **立即结构化记录反馈**，不要留在聊天记录中积累——否则会话中断时将会丢失。
- **若某对象已知不稳定，不要盲目启动**——在用户实时面对之前，先检查其能否正常启动。
- **立即委派，而不是在结束时集中委派**——否则修复要等到用户测试完毕才开始，本流程的时间优势就会丧失。

## 触发示例

- "human-loop-audit"
- "Lass uns die Apps im Reißverschluss durchtesten."
- "Ich teste, du wertest aus und reparierst."
- "start"（在事先宣布了Human-Loop-Audit之后，作为第1步的启动信号）

## 变更日志

### 1.0.0 (2026-08-18)
- 初始版本。流程源自用户于2026-08-18的定义：拉链式审计，并行评估 + 立即委派修复，与`reissverschluss-merge`（Git合并，名称意象相同，无关联）以及较窄的项目本地波次测试周期（顺序实施而非并行）加以区分。
