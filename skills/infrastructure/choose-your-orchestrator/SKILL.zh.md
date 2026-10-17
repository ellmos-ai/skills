---
name: choose-your-orchestrator
version: 1.1.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-10-03
description: "在复杂的多智能体工作之前，与用户共同选择合适且有边界的编排方式，并生成紧凑的会话契约。当用户使用 /choose-your-orchestrator，或在 Orchestrator、蜂群、模型路由或用户偏好模型的组合不确定时，以及在需要明确规定模型槽位、并行度、派生深度、写入边界、验收和升级的智能体程序之前，使用此技能。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: zh
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar, budgetierung]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 0b3feaa40d5c9d5310977fbc0e9c92572c1504e201baad19e7b73c7b64e4e846
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="choose-your-orchestrator banner">

# Choose Your Orchestrator

## 目的

在复杂的多智能体工作之前，澄清约束条件，推荐最小的有效组合（由现有技能构成），并输出一份具有约束力的会话编排契约。通过当前运行时的技能机制加载所选技能，并遵循其实时指引。不要将它们的流程复制到本技能中。

委派永远不会扩大权限。外部或不可逆操作，如发布、发送、删除、付款或生产环境变更，除非当前任务明确授权，否则仍由用户把关。

## 构件

| 构件 | 在契约中的职责 | 非其职责 |
|---|---|---|
| `orchestrator` | 工作包、范围、证据与验收 | 发明模型选择或蜂群模式 |
| `swarm-operations` | 蜂群模式、成本门控与可选的 Matruschka 分层 | 人为地并行化单个任务 |
| `model-strategy` | 基于实时可用性的能力与模型相关路由 | 规定固定的模型版本或权限 |
| `clutch` | 可选的外部路由建议 | 对派发或范围的唯一决定权 |
| `decision-avatar` | 在可逆不确定性下可选的已授权偏好信号 | 替代用户批准或扩大权限 |
| `budgetierung` | 针对昂贵模型/审查者/顾问、账户及升级前预检，按时间窗口协商的配额 | 按专业领域选择模型（这由 `model-strategy` 负责）或擅自设定配额 |

仅当 `clutch` 确实可用时才使用 `clutch route "<kurze Aufgabenbeschreibung>" --json`。将 JSON 响应视为建议，并对照可用的运行时槽位、预算、项目规则和用户边界进行核对。若 `clutch` 不可用或其输出无法解析，则使用 `model-strategy` 以及运行时的实时能力。不要在契约中硬编码当前的模型名称或版本。

## 推荐对话

### 1. 梳理任务

确定目标、任务类型、成功标准、负面范围、当前权限、现有锁，以及独立的工作包。首先从下方的表格中选择最小的合适路由建议。

### 2. 提出契约

展示一份简洁的草案，包括：

1. 构件与角色，
2. 模型/预算槽位（对于数小时的运行或紧张/昂贵的模型，通过 `budgetierung` 协商并作为账户管理），
3. 最大并行度与派生深度，
4. 写入边界与锁，
5. 验收与证据，
6. 升级与用户询问，
7. 权限边界。

推荐具体数值，并用一句话说明最重要的权衡。仅询问会实质改变结果的决定。将未决问题合并为至多三个清晰分隔的组；每组都先给出推荐选项。若所有维度均已明确设定，则不要重复询问。

### 3. 确认或精简

在任何实质性的预算、写入或权限问题悬而未决时，不要启动多智能体派发。若仅是并行性的收益不明确，则精简为单次执行。在没有实质性用户决定缺失的情况下，经明确授权的任务可以采用安全默认值启动。

### 4. 输出契约

在聊天中输出已确认的契约。若 `usmc` 命令可用，先检查其帮助信息，并通过其中记录的 Note/Write 命令另外写入一份隐私中立的会话笔记。不要编造子命令，也不要保存原始提示、机密或私人内容。若没有可用的 USMC 写入途径，则以聊天中的契约为准。

## 路由表

| 任务类型 | 建议 | 默认切分 |
|---|---|---|
| 审计 / 扫描 | `orchestrator` + `swarm-operations`；能力类别不同时使用 `model-strategy` | 独立区域，小型 `parallel-chunks` 或 `specialist` 组，集中合并 |
| 构建程序 | `orchestrator` + `model-strategy`；仅对真正独立的分支使用蜂群 | 负责人规划并验收，工作者在互不重叠的区域内构建 |
| 单项构建 | 单次执行；路由可选 `model-strategy` 或 `clutch` | 无蜂群或层级开销 |
| 工单运营 | 工单系统保持主导；`orchestrator` 补充工作契约与证据 | 不替代既有的路由/评分机制，尊重工单生命周期 |

## 安全默认值

除非用户、运行时或项目规则有更严格的规定，否则使用以下数值：

- 最多两个活跃工作者；先启动一个，并证明第二个的收益，
- Matruschka 关闭，最大派生深度 `0`，
- 未经明确批准，工作者不得拥有子智能体，
- 每个仓库或每个明确划定的区域只有一个写入者，
- 每次写入前都要有互不重叠的文件声明及项目惯用的锁，
- 负责人/编排者亲自检查产出物、差异与测试，
- 完成报告只有在证据验收后才算有效，
- 不可逆或外部操作仍由用户把关，
- 不确定性集中汇报，而非拆分为多次零散打断。

只有当用户明确确认 Matruschka，且契约为每一层说明模型/能力类别、活跃槽位上限、允许的子任务以及最大深度时，才启用它。以活跃而非仅存在的智能体进行计数。即便如此，每个区域仍只保留一个写入者。

## 契约格式

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze; Budget/Konto: <budgetierung-Konto, Pfad>>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## 示例

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## 停止条件

当范围重叠、锁不明确、运行时未提供推荐槽位、预算未确认，或验收无法被独立证实时，停止或精简编排。不要替用户猜测新的产品、隐私或权限决定，而应向用户询问。

## 变更日志

### 1.1.0 (2026-10-03)
- 新增 `budgetierung` 作为协商模型配额/账户的构件（构件表、契约对话中的模型/预算槽位、契约格式中的工作者槽位行）。

### 1.0.0 (2026-08-20)
- 引入推荐对话、路由表与紧凑的会话契约。
- 为并行性、Matruschka、写入边界、证据及外部操作设定安全默认值。
- 描述了 `clutch` 与已授权偏好模型的可选集成，且不绑定固定模型或扩大权限。
