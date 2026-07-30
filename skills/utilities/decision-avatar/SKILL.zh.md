---
name: decision-avatar
version: 1.0.0
type: protocol
author: Claude + Codex
created: 2026-07-28
updated: 2026-07-30
description: >
  当存在已明确授权的本地决策配置文件时：根据经过验证的反馈预测重复性决策，
校准置信度，并严格区分预测、决策和执行。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [entscheidung, avatar, theory-of-mind, feedback, konfidenz, provenance]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "private decision-avatar profile (not published)"
  origin_version: "1.2.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="decision-avatar banner">

# Decision Avatar

## 目的

本 Skill 并不复制特定人类个体。它提供了一套可验证的程序，以便在重复发生的决策类型中，根据真实、经授权的证据推导出概率性的偏好。

仅当存在本地决策配置文件且其使用在当前任务中被允许时才使用它。如果没有配置文件，本 Skill 不提供代行决策。

仅当任务、适用的 Agent 规则或配置文件元数据明确允许当前目的时，使用才被视为获得授权。仅凭配置文件可访问并不构成同意。

## 核心原则

1. **证据重于推测。** 直接表述和经确认的决策比推断出的模式具有更高的权重。
2. **预测非本人表述。** Agent 的输出绝不能作为新的原始证据流回配置文件中。
3. **决策不同于执行。** 一项建议可以是明确的，即使其执行需要额外的授权。
4. **默许并非反馈。** 未提出异议并不能确认一项预测。
5. **配置文件保持本地和私密。** 请勿将个人数据、密钥或敏感内容写入共享的 Skill 文件中。

## 可移植配置文件模型

文件名可自由配置；仅需要以下角色划分：

| 角色 | 内容 |
|---|---|
| 方法论 | 证据等级、数据保护与校准规则 |
| 已证实偏好 | 直接表述与经确认的决策 |
| 假设 | 附带置信度与来源的衍生规则 |
| 动作 | 根据预测采取的行动 |
| 反馈 | 本人的确认、修正或拒绝 |

与项目相关且最新的决策优先于通用偏好。

每条经处理的证据应至少包含：

```text
Quellen-ID:
Datum:
Entscheidungstyp und Gültigkeitsbereich:
Status: bestätigt/korrigiert/widerrufen
Gültig bis: <optional>
```

请勿使用已撤销、已过期或超出其适用范围的证据。当确认的证据发生冲突时，首先以更具体的为准，其次以更新的为准。如果冲突持续存在，请将置信度设置为“低”并升级处理。

## 决策循环

### 0. 检查本地优先规则

如果针对当前项目或具体决策类型存在经确认的规则，请使用该规则并记录其来源。

### 1. 寻找真实证据

仅使用根据本地方法论被允许的证据。任务列表、Agent 日志、先前的 Avatar 回复以及当前会话的论点均不属于本人的表述。

### 2. 生成预测

始终附带理由输出结果，并标注以下三个等级之一：

- **高 (high):** 多条直接、一致且相关的证据，
- **中 (medium):** 具有有限或间接证据的合理模式，
- **低 (low):** 新颖局势、矛盾证据或无可靠模式。

后果重大的决策不会自动归为“低”。置信度衡量的是偏好证据的充分程度，而非后续执行的影响范围。

### 3. 区分模式

| 模式 | 结果 | 侧面影响 (Side Effect) |
|---|---|---|
| 预测 (Predict) | 概率性立场 + 证据 + 置信度 | 无 |
| 决策 (Decide) | 具体选择 + 理由 + 置信度 | 无 |
| 执行 (Act) | 授权且安全的实施 + 动作日志 | 可能存在 |

在执行模式下，还须适用 Runtime 的授权与安全规则。置信度低或缺乏执行权限会导致升级处理，而不是静默执行。

### 4. 校准反馈

获得真实反馈后：

1. 将预测标记为已确认、已修正或已拒绝。
2. （可选）记录评分量表。
3. 记录方向性错误与拟合/裁剪错误之间的差异。
4. 调整假设与置信度。
5. 仅将真实反馈吸收进已证实的偏好中。

## 输出格式

```text
Entscheidungstyp:
Modus:
Wahrscheinliche Präferenz:
Konfidenz:
Zulässige Belege:
Gegenbelege oder Unsicherheit:
Ausführung autorisiert: ja/nein
Nächster Schritt:
```

在输出中仅列出脱敏后的来源 ID 和决策所需的证据摘要。请勿复现私密表述、绝对配置文件路径或敏感原始数据。

## 局限性

- 不对个人的内部心理状态进行诊断或断言。
- 不在其允许目的之外使用配置文件。
- 不自动将 Agent 的假设吸收为个人的认知知识。
- 如果需要新的授权，绝不单凭预测就自动执行。

## 变更日志

### 1.0.0 (2026-07-28)
- 将反馈预知、置信度校准和来源分离从个人 Avatar 配置中提取为独立、可移植的协议。
- 实现了授权、证据生命周期、冲突解决和脱敏输出的操作化。
