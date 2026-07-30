---
name: skill-finder
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  用于本地自有技能的主动查找器/路由工具（类似于 using-superpowers）。在开始任何非平庸任务时，
  务必首先使用此技能检查是否有合适的本地技能，并路由到正确的技能。当收到 "哪个技能合适"、"是否有对应的技能"、
  "查找技能" 或在处理本地技能比临时解决更好的任务前自动激活。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: zh
status: active

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-finder banner">
# 技能查找器 (Skill-Finder)

## 基本规则

在开始任何非平庸任务之前，首先检查是否有本地技能能够更好地解决该任务。哪怕只有轻微怀疑，也应加载相应的技能并**遵循其实时指南**（阅读文件，切勿凭记忆工作）。如果没有适用的技能，则正常继续。

## 技能族路由表

<!-- 基于 SKILL-MAP.md + inventory_skills.py 生成/更新。主题 -> 技能族 -> 技能。
     维护：子技能 skill-family-care 或重新运行 skill-explorer 审计。更新日期：2026-06-17 -->

| 主题 / 意图 | 技能族 | 技能 |
|-----------------|---------|----------|
| 深入思考 / 分析问题 | 思考工具 (Denkwerkzeuge) | `/structured-thinking` (引导 `/think` → `/brainstorm` → `/decide`) |
| 新创意 / 创造力 | 思考工具 (Denkwerkzeuge) | `/brainstorm` (对比 `/think` 分析, `/decide` 决策) |
| 决策栈 | 思考工具 (Denkwerkzeuge) | `/decision-briefing` |
| 构建或使用经授权的用户偏好模型 | 多智能体 (Multi-Agent) | `build-your-users-mind`（构建）· `decision-avatar`（使用） |
| Bug / 测试失败 | 编程与调试 (Coding & Debugging) | `/bugfix-protocol` (单个 Bug), `/bugsweep` (多个，发布前) |
| 新建/已有项目或流水线 | 项目/流水线 (Projekt/Pipeline) | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Roblox 游戏 | 游戏开发 (Game-Dev) | `/roblox-dev` (→ `/rojo`, `/roblox-studio`, `/game-design`) |
| 心理咨询 / 辅导 / 危机 | 心理咨询 (Therapie) | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| 演示文稿 / 幻灯片 | 办公 (Office) | `/academic-pptx` (内容) + `/pptx` (文件) |
| 多智能体协调 | 多智能体 (Multi-Agent) | `/swarm-operations`, `/model-strategy` |
| 求职 / 自我管理 | 个人 (Persönlich) | `/bewerbungsexperte`, `/selbstmanagement` |
| 技能对比/清理/查找 | 系统/元技能 (System/Meta) | `skill-explorer` (审计/探索), `code-skill-index` (列表) |
| 系统搭建 / MCP 同步 / 智能体对接 | 系统/元技能 (System/Meta) | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| 文件工具 | 实用工具 (Utilities) | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| 对话历史 → 保存为技能 | 系统/元技能 (System/Meta) | `skill-extractor` (`/skill-extract`) |
| 对话历史/外部自动化 → 自动化流程 | 系统/元技能 (System/Meta) | `workflow-extract` (`/automations-extract`) |
| 跨多项目的周期性检查 | 编程与调试 (Coding & Debugging) | `rotation-check` (注册表/日志骨架) |
| 问题卡壳、挖掘创意 | 思考工具 (Denkwerkzeuge) | `idea-mining` (对比 `/brainstorm` = 自由/宽泛) |
| 保持德语/英语文档版本同步 | 实用工具 (Utilities) | `bilingual-doc-sync` |
| 文本中的 AI 痕迹/对话残余、AI 披露说明 | 实用工具 (Utilities) | `llm-text-hygiene` |
| 任务中的条件/时间点/顺序 ("只有当...", "从 6 点起", "一旦 X 完成") | 流程 (Prozess) | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |

完整列表：技能 `code-skill-index`。

## 红线预警 (意味着 STOP 的辩解)

| 想法 | 事实 |
|---------|----------|
| "这只是一个简单的问题。" | 提问也是任务 —— 优先检查技能。 |
| "我了解这个概念。" | 了解概念 ≠ 使用技能。必须阅读实时文件。 |
| "用技能太大材小用了。" | 简单的问题会变复杂 —— 必须使用技能。 |
| "我自己先探索一下。" | 技能会告诉你如何探索。先检查技能。 |

## 维护说明

在技能族发生变更时更新路由表（使用子技能 `skill-family-care` 或运行 `skill-explorer` 中的 `inventory_skills.py`）。

## 更新日志

### 0.2.0 (2026-07-03)
- 为新技能添加路由行：skill-extractor、workflow-extract、rotation-check、idea-mining、bilingual-doc-sync (Codex 自动化提取)。

### 0.1.0 (2026-06-17)
- 初始版本。由审计模式 ([F]) 生成，作为 using-superpowers 的对应工具。路由表取自 2026-06-17 的审计（10 个用户技能族）。
