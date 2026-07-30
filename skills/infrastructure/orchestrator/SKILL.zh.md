---
name: orchestrator
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: 用于分解复杂任务、委派独立 Worker 以及基于证据验收其结果的供应商中立协议。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [orchestrierung, multi-agent, delegation, evidenz, checkpoint, workflow]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'local-agent-skills/orchestrator/', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="orchestrator banner">

> **中文** — `orchestrator` 官方中文版本。


# Orchestrator (中文)

## 概述与目的

当某一任务包含至少两个基本独立的工作包，且委派确实在时间、上下文或质量上能带来实际优势时，请使用本 Skill。对于小型且紧密耦合的任务，请直接处理。

本 Skill 描述了一套协议。Worker 的具体启动、暂停和恢复操作均通过对应 Runtime 的能力来实现。

## 权限边界

委派不会扩大授权。每个 Worker 最多获得主任务已具有的范围和修改权限。外部的、不可逆的或需要额外批准的操作仍须遵守审批流程。

## 流程

### 1. 评估状况

1. 记录主任务的目标、成功标准和排除事项。
2. 检查项目规则、锁、正在进行的变更以及可用预算。
3. 在 Dispatch 之前，保存受影响区域当前的锁、状态和 Diff 状态作为 Baseline。只有这样，后续才能可靠地将既有的外部变更与 Worker 的变更区分开来。
4. 只对足够独立的工作包进行并行化处理。
5. 分离重叠的写入区域或采用顺序处理。

### 2. 编写任务契约

在每次 Dispatch 之前，创建一个简短且可验证的契约：

| 字段 | 必填内容 |
|---|---|
| 标识符 | 工作包的稳定 ID |
| 目标 | 恰好一个具体的结果 |
| 输入 | 相关的文件、数据或上下文来源 |
| 正向 Scope | 允许读取或修改的内容 |
| 负向 Scope | 明确禁止触碰的内容 |
| 成功标准 | 用于判定“完成”的可观察条件 |
| 证据 | 预期的证明，例如测试、Diff 或出处 |
| 返回格式 | 紧凑、结构化的完成消息 |

Worker 仅接收其履行该契约所需的上下文。

### 3. 执行与观察

- 保持 Fan-out 规模较小，仅在带来独立收益时扩增。
- 通过 Runtime 状态或标准的项目 Checkpoint 跟踪进度。
- 发生冲突、Scope 扩大或缺乏权限时，立即停止并向上升级。
- 失败的 Worker 不应自动阻塞其他独立的工作包。

### 4. 验收结果

完成通知首先只是一项声明。Orchestrator 需自行进行验证：

1. 所声称的产物或变更是否存在？
2. 它是否属于约定好的 Scope？
3. 约定好的测试或证明当前是否通过？
4. 是否遵守了外部变更、锁以及负向 Scope？
5. 不同 Worker 的结果之间是否存在矛盾？

只有在上述条件均满足后，工作包才算正式完成。

### 5. 集成与保存

- 有意识地解决冲突；切勿盲目拼接结果。
- 集成后重新执行必要的全局测试。
- 明确标注未完成、失败和推迟的工作包。
- 对于长时间运行的任务，将目标、状态、证据和下一步计划保存在可恢复的 Checkpoint 中。

## 最小 Worker Prompt

```text
Auftrag: <Kennung und Ziel>
Eingaben: <Quellen>
Du darfst: <positiver Scope>
Du darfst nicht: <negativer Scope>
Fertig, wenn: <prüfbares Kriterium>
Belege mit: <Test, Diff oder Fundstelle>
Antworte als: <Rückgabeformat>
```

## 停止条件

如果某个工作包的 Scope、权限或证据变得不明确，仅停止受影响的工作包。独立且安全的工作包可继续运行。

出现以下情况时，停止整个委派：

- 子任务不再具有独立性，
- 无法安全地分离共享的写入区域，
- 整个剩余 Scope 的规则、锁或权限不明确，
- 预期成本超出可识别的收益，
- 无法生成或验证所需的证据。

## 变更日志

### 1.1.0 (2026-07-28)
- 移除了用户、路径、模型和供应商绑定。
- 将任务契约、权限边界、证据验收和 Checkpoint 提炼为可移植的核心机制。
- 明确区分了外部变更 Baseline 以及包局部和全局停止机制。

### 1.0.0 (2026-06-17)
- 本地初始版本。