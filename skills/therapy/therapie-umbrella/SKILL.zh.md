---
name: therapie-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  “心理治疗 / 咨询”系列的元/框架 Skill（Umbrella Skill）。了解所有治疗相关 Skill
  （情绪稳定、方法概述、面谈技巧 + 未注册的专项疗法），并引导至最合适的 Skill。当不确定适用哪种治疗/咨询 Skill、
  需要了解可用方法概述、或需要对咨询/危机状况进行初始评估时使用此 Skill。也可通过“哪种治疗方法适用”、
  “如何结构化咨询”、“危机——该怎么办”、“选择治疗方案”等提示词触发。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: therapy
tags: [therapie, beratung, umbrella, meta, routing]
language: zh
status: active

dependencies:
  tools: []
  services: []
  protocols: [counseling-basics, guideline-therapies-overview, stabilization-techniques, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/therapie-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="therapie-umbrella banner">

# 心理治疗 / 咨询 — 框架 Skill (Umbrella)

## 目的

“心理治疗 / 咨询”系列的入口点。整合整体分流逻辑，并在特定情况下引导至最合适的 Skill。三个活跃的入口 Skill 构成前台；其后是一长串可通过 `code-skill-index`（目录 `catalog-therapy.md`）调用的未注册专项疗法。

## 成员与分流

| Skill | 用途 | 什么时候使用此 Skill 而非其他 |
|-------|------|-------------------------------|
| `/stabilization-techniques` | 危机干预、接地（Grounding）、安全岛、PMR、惊恐、容忍度窗口（Window of Tolerance） | **首先**在急性应激/危机中使用 — 稳定优先于方法论 |
| `/guideline-therapies-overview` | 标准指南疗法概述：CBT、ACT、图式疗法、暴露疗法、系统治疗、精神动力学 | 当需要选择或解释合适的**疗法**时 |
| `/counseling-basics` | 面谈技巧：倾听、镜像反馈、情绪确认、MI/OARS、循环提问 | 当关注点在于**对话的方式**而非特定治疗方法时 |
| (未注册的专项 Skill) | 单项疗法（家谱图、暴露疗法细节、积极心理学等） | 当需要深度应用某一具体的单项疗法时 → 通过 `code-skill-index` |

> 分流规则：急性危机 → `/stabilization-techniques` · 选择/解释方法 →
> `/guideline-therapies-overview` · 会谈技巧 → `/counseling-basics` · 深度单项疗法 →
> 通过 `code-skill-index` 访问未注册专项 Skill。

## 良好配合的组合

- `/stabilization-techniques`（首先，急性期）→ `/guideline-therapies-overview`（随后，中期）：
  先建立安全感/容忍度窗口，再选择合适的标准指南疗法。
- `/counseling-basics` 贯穿**两者** — 咨询态度（MI/OARS、情绪确认）为稳定干预和方法实践提供全程支持。

## 共同规范

- 不替代临床诊断；以心理教育和资源导向的方式开展工作。
- 以容忍度窗口（Window of Tolerance）为核心原则：过度过度唤起时先稳定情绪，切勿直接对抗。
- 使用前阅读各单独 Skill 的实时文件 — 本框架 Skill 不重复包含具体内容。

## 更新日志 (Changelog)

### 0.1.0 (2026-06-17)
- 初始版本。由审计模式 (1c1) 为心理治疗 / 咨询系列生成。
