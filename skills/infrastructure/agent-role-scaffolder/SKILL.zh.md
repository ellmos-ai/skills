---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: "在 ellmos 生态系统中搭建并验证新的智能体角色：原生 Claude Code 子智能体（持久的角色定义）以及 Companion-Worker（通过 SendMessage 复用、服务于一系列工单/任务的实例）。将此前在构建智能体角色（ati-agent、bueroassistent、versicherungs-agent 等）过程中积累但未经正式化的经验，整理为可复用的“脚手架加验证”流程。当需要创建新角色（“构建新的智能体角色”“创建子智能体”“启动 Companion-Worker”），或需要根据内部约定检查现有角色（“这个智能体配置是否正确？”）时，请使用此技能。"
visibility: public
language: zh
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
translated_from_sha256: 55b76ad25a5d65f61987662e674bc9c74ea0f6a8586ad4748268bc9441711db5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.238775+00:00"
---
<img src="banner.png" width="100%" alt="agent-role-scaffolder banner">

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agenten-Orchestrierung START -->
> **智能体编排系列 — 导航：** 选择/分级模型 -> `model-strategy`；选择编排模式 -> `choose-your-orchestrator`；群体操作（5 种基本模式 + 2 种模式）-> `swarm-operations`；任务拆分/委派/验收 -> `orchestrator`；跨提供商消息/在线状态/锁 -> `agents-bridge`；**构建或检查新角色 -> 本技能（agent-role-scaffolder）**。
<!-- FAMILY-ROUTER:Agenten-Orchestrierung END -->

## 目的

该生态系统已经拥有一套成熟的编排技能系列（`model-strategy`、`swarm-operations`、`orchestrator`、`choose-your-orchestrator`、`agents-bridge`），但**其中没有一个回答“如何正确地创建新角色”这一问题。** 本技能 `agent-role-scaffolder` 填补了这一空白。它不复制上述技能，而是在涉及分级、编排模式或跨提供商消息时**路由至它们**。

**来源：** 用户在工单 `T-20260825-935905816`（市场全面梳理）中做出的决策 M5：结论 (b) — 已有自身的智能体构建经验，但尚未正式化。官方 Claude Code 插件 `agent-sdk-dev`（claude-plugins-official，Apache-2.0）作为**结构性范本**：一个 scaffolding 命令文件，加上两个专题验证子智能体，附带检查清单和 PASS/PASS-WITH-WARNINGS/FAIL 报告格式。借鉴的是**形式**（脚手架问题目录 → 搭建 → 带结构化报告的验证清单），而非文本，也非对象——该插件构建的是原始 Claude Agent SDK 应用（Python/TypeScript），本技能构建的是 ellmos 自有的智能体角色（子智能体定义与 Companion-Worker）。原插件未安装，仅在本地市场缓存中以只读方式阅读（`.PLUGINS/CLAUDE.md` 规则 5：思路可自由借鉴，措辞不可照搬）。登记条目：`.AI/.PLUGINS/PLUGIN-REGISTER.md`，状态 `zitiert`。

## 两种构建路径 — 均属于本技能范围

在 ellmos 生态系统中，新角色通过两条结构上截然不同的路径产生，二者不可混淆（类似于范本插件中 TS/Python 的区分，但此处依据的是实际的系统边界）：

| | **原生子智能体** | **Companion-Worker** |
|---|---|---|
| 产出物 | 持久的角色定义（`~/.claude/agents/<name>.md`，可通过 `Agent` 工具启动） | 为**一个**任务系列临时命名、通过 `SendMessage` 复用的实例 |
| 生命周期 | 持久，可跨会话复用 | 在一个工单/主题系列的期间存在，之后丢弃 |
| 现有示例 | `ati-agent`、`bueroassistent`、`versicherungs-agent`、`gesundheitsassistent`、`persoenlicher-assistent`、`production`、`research-agent`、`reflection-agent`、`test-agent`、`entwickler-agent` | 本会话模型本身（例如 `skillcreator-bau`、`policyreg-decisions`、`workflowhooker-ausbau` — 工单系统中命名的 Worker） |
| 生命周期管理层 | Claude Code 自带的智能体注册表 | **COMA**（`.MODULES/.ORCHESTRATION/coma`）— 若以跨进程方式启动，而非仅限工具内部 |
| 此处的构建指南 | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**经验法则：** 若该能力需要一个在多个会话中可复用、具有固定触发描述的持久名称（例如“每当涉及税务凭证时”）→ 原生子智能体。若它是一系列有限但内容相关的任务，由协调者当前委派（工单链、主题切换）→ Companion-Worker。

## 流程

1. **选择构建路径**（见上表）— 有疑问时询问用户，而不是猜测。
2. **逐一过完脚手架问题**（见对应的 `references/*.md`）— 与范本插件一样依次进行，而非一次全部提出：目的/触发条件、工具需求（`Tools:`）、模型选择（→ **第 3 步**）、协调需求（带专家的 Boss 智能体还是单一角色？）。
3. **此处不决定模型 — 委派给 `model-strategy`。** 基于评分的选择、跨智能体委派、顾问配对、升级触发器在该处已解决；此处仅作引用。存量中的经验法则：子智能体**不会一律**继承主模型（参见反馈记忆 `feedback_subagenten_modellstaffelung`）。
4. **检查编排模式**，若新角色需要与多个其他角色协作——`choose-your-orchestrator` 选择模式，`swarm-operations` 提供 5 种基本模式 + 2 种模式，`orchestrator` 提供拆分/委派/验收协议。
5. **遵守团队/消息约定**（`references/
   model-staffing-and-messaging.md`）：跨智能体通信使用 `SendMessage`；工单委派时通过文件名认领工单；委派时“引用而不重复”（不要在提示词中重述核心规则，只写任务专属内容）。
6. **验证** — 在所选 `references/*.md` 文件中完成相应检查清单，按 `PASS / PASS MIT WARNUNGEN / FAIL` 格式生成报告（结构见下文）。
7. **必要时登记** — 持久的新角色应纳入相应注册表（`~/.claude/agents/`，如有需要可打包进插件）；Companion-Worker 不需要注册表条目，只需清晰的首次任务交接。

## 验证报告格式（两条构建路径通用）

结构有意借鉴自范本插件（借鉴形式，不借鉴措辞）——四个简明章节：

- **状态：** PASS | PASS 带警告 | FAIL
- **关键问题：** 导致角色不可用的问题（缺少触发描述、`Tools:` 过宽/过窄、模型未通过 `model-strategy` 论证、未检查与现有角色的边界）
- **警告：** 次优但可运行（例如继承主模型而非分级、长期运行的 Companion-Worker 缺少轮换标准）
- **已通过的检查与建议：** 哪些符合要求，接下来该做什么

## 相关技能

- `model-strategy` — 模型选择/分级（第 3 步，此处仅引用）。
- `swarm-operations` — 多角色协作的群体模式。
- `choose-your-orchestrator` — 选择合适的编排模式。
- `orchestrator` — 拆分/委派/验收协议。
- `agents-bridge` — 跨提供商消息/在线状态/锁，若新角色需要在 Claude Code 之外与 Codex/Gemini/Kimi 通信。
- `skill-explorer` — 在构建新角色之前检查某能力是否已存在（避免重复）。

## 变更日志

### 1.0.0 (2026-08-25)
- 初版。依据用户决策 M5（`T-20260825-935905816`）经 `ellmos-skill-creator` 构建。将 Companion-Worker 模式（主要来源：`_control-center/_TICKETS/README.md`，“指导原则（上下文经济）”一节）、COMA 生命周期（主要来源：`.MODULES/.ORCHESTRATION/coma/README.md`）以及现有角色中观察到的“Boss 智能体协调专家”模式正式化。有意路由至 `model-strategy`/`swarm-operations`/`orchestrator`/`choose-your-orchestrator`/`agents-bridge`，而非重复其内容。范本 `agent-sdk-dev`（claude-plugins-official）未安装，仅阅读并以结构方式引用（`.PLUGINS/CLAUDE.md` 规则 5）。
