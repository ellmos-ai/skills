---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  “项目/Pipeline 建设与改造”技能家族的 Meta/Umbrella Skill。了解所有用于创建、接管、
  改造和分析项目与 Pipeline 的 Skill，并引导至最合适的技能。当不确定某项工作是全新创建（Greenfield）
  还是改造（存量），或者涉及单个项目还是整个 Pipeline 时，请使用此 Skill。在触发“创建新项目/Pipeline”、
  “改造现有项目”、“接管项目”、“翻新目录结构”、“选择合适的 Bootstrapper”时也可使用。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: zh
status: active

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">

# 项目/Pipeline 建设与改造 — Umbrella

## 目的

“项目/Pipeline 建设与改造”技能家族的统一入口。家族成员沿两个维度排列：**Greenfield (全新) vs. 存量** 以及 **项目层级 vs. Pipeline 层级**。此 Umbrella 可防止常见的“bootstrap” vs. “optimize” vs. “onboard”概念混淆。

## 成员与路由 (Routing)

| Skill | 用途 | 何时使用此 Skill 而非其他 |
|-------|-------|-------------------------------|
| `/project-bootstrapper` | 在现有 Pipeline **中**创建新项目 | Greenfield，项目层级 |
| `/pipeline-bootstrapper` | 创建全新的顶层 Pipeline | Greenfield，Pipeline 层级（较少使用） |
| `/project-onboarding` | 接管/录入现有项目 | 存量，项目层级 |
| `/pipeline-optimizer` | 翻新现有 Pipeline/结构（6 步流程） | 存量，改造 |
| `/docs-analysis` | 对照当前代码检查需求/概念文档 | 存量，分析（不进行改造） |
| `/dev-cycle` | 实际构建过程的 8 阶段开发框架 | 横向：开发的具体方式 (HOW) |

> 路由规则：**全新 + 项目** → `/project-bootstrapper` · **全新 + Pipeline** → `/pipeline-bootstrapper` · **接管存量** → `/project-onboarding` · **改造存量** → `/pipeline-optimizer` · **仅检查** → `/docs-analysis` · **构建实现** → `/dev-cycle`。

## 推荐的搭配组合

- `/project-onboarding`（首先：录入存量）→ `/pipeline-optimizer`（随后：针对性改造）— 先理解，后翻新（遵循 6 步原则“先读后写”）。
- `/docs-analysis`（查找缺口）→ `/dev-cycle`（补齐缺口）。
- `/project-bootstrapper`（搭建骨架）→ `/dev-cycle`（开发具体内容）。

## 通用规范

- 务必首先阅读现有的 Pipeline 规范（Registry、Templates、CLAUDE.md）— 切勿创建平行的多套标准。
- Greenfield 类 Skill 用于创建，存量类 Skill 用于翻新 — 切勿混淆。
- 在应用前阅读具体 Skill 的最新在线文件。

## 更新日志 (Changelog)

### 0.1.0 (2026-06-17)
- 初始版本。由审计模式 (3c1) 为项目/Pipeline 技能家族生成。
