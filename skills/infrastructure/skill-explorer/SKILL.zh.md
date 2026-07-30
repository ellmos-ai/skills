---
name: skill-explorer
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: 管理你自己的 Skill 全景：调查并对比现有 Skill（审计模式），在网络上检索新的 Skill/插件（探索模式），同时作为安装程序生成轻量级的子 Skill（Skill-Finder、家族伞、维护 Skill），避免加载单体文件。适用于“对比/审计 Skill”、“哪些 Skill 重复了”、“构建 Skill 家族”、“清理/巩固 Skill”、“维护 Skill 注册表”、“查找主题 X 的 Skill/插件”、“安装新 Skill”、“浏览 Skill 市场”或使用 `/skill-explorer`。按家族提供子报告和全局编号的决策列表；仅在安全检查和明确批准后进行安装/卸载。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: zh
status: active
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `skill-explorer` 官方中文版本。


# Skill-Explorer — 管理 Skill 全景（审计 · 探索 · 安装程序） (中文)

## 概述与目的

随着 Skill 清单的增加，会出现重复项、未使用的资源以及不明确“用哪个 Skill 替代哪个”的情况 — 并且网络上也不断涌现新的 Skill/插件。`skill-explorer` 将三种角色集成到一个工具中：

| 角色 | 作用 | 详情 |
| --- | --- | --- |
| **审计模式**（对内） | 调查所有 Skill，按家族进行聚类，收集功能/依赖项/资源，每个家族生成一份子报告及带编号的建议 | `references/audit-mode.md` |
| **探索模式**（对外） | 在网络上（Web/GitHub/Reddit，双语）检索关于特定主题的新 Skill/插件，进行对比并带门槛地安装 | `references/explore-mode.md` |
| **安装程序** | *生成*轻量级子 Skill 而不是单体 — Skill-Finder、家族伞、维护 Skill | 下文 + `references/family-care.md` |

调用方式：`/skill-explorer`（默认审计模式）或“……查找关于主题 X”（探索模式）。两种模式共享分类法（`references/clustering.md`）、报告格式（`references/report-format.md`）和编号方案，因此用户只需用一份统一编号的列表进行回复。

## 安装程序原理与持久化

`skill-explorer` 本身并不像单体那样膨胀，而是根据需要*生成*轻量、可单独加载的子 Skill，因此永远不必加载过长的单个 Skill：

- **Skill-Finder** ([F]) — 一个活跃的查找器/路由器，类似于“using-superpowers”看门人，在每次任务前读取注册表并路由到对应的家族（`references/skill-finder.md`，模板 `assets/skill-finder-template.md`）。
- **家族伞** (c1) — 了解整个家族的元 Skill（`assets/family-umbrella-template.md`）。
- **维护 Skill**（[P1] 家族，[P2] 注册表） — 保持家族/注册表最新状态（`references/family-care.md`）。

决策被持久化存储在 `~/.claude/skills/skill-explorer/config.json` 中（`references/config.md`，模板 `assets/config.example.json`）：启动时读取（已知的家族/路由器/已生成的子 Skill），执行后更新 — 这样再次运行绝不会重复创建任何内容。

## 分支机制（自定义第三方 Skill）

可以在不修改原件的情况下对只读 Skill（插件、导入的第三方 Skill）进行自定义：完整复制原始目录（**分支**）；之后仅对副本进行编辑。分支包含四个必填字段：指向原件的引用、创建分支的日期、作者和原因。一旦分支取代了原件，原件将从运行时取消注册（`SKILL.md` → `CONTENT.md`），或者将家族路由器指向该分支，从而避免两个几乎相同的 Skill 发生冲突。第三方分支保持**私有** — 它们不会进入公共的 `.AI/.SKILLS` 库。细节见：`references/skill-branching.md`。

## 工作流与步骤

1. **选择模式：** 调查/清理库存 → 审计模式。从外部搜索/安装 → 探索模式。（探索模式可以基于先前的审计/`config.json`。）
2. **审计模式**（`references/audit-mode.md`）：盘点（脚本）→ 家族聚类 → 子报告 → **一份全局编号的决策列表**（a/b/c1/c2/c3，加上 R/F/P1/P2）。
3. **探索模式**（`references/explore-mode.md`）：双语多源检索 → 每个候选者 3 个分类 → 影响模拟 → 带编号的安装/卸载建议。
4. **仅在**用户给予数字确认后执行；注册 Skill 的创建/更改并更新 `config.json`。

## 铁律

- **调查 ≠ 变更：** 聚类所有内容，但仅编辑**用户拥有**的 Skill；插件/第三方 Skill 是只读的（绝不修改标头/删除）。要自定义第三方 Skill，请改为创建**分支**（fork 副本） — 原件保持不变，所有修改仅在副本上进行（→ `references/skill-branching.md`）。
- **扩展注册表，而不是重复创建：** 如果已存在 Skill 注册表（索引 + 家族映射 + 索引 Skill），请扩展它，而不是创建第四个。
- **安全检查主要靠人工审查：** 在每次安装前，模型会读取 Skill 本身并作出评估；`scripts/scan_skill_security.py` 仅作为具有已知局限性的辅助分诊。绝不自动安装。
- **按来源注册：** 用户创建 → Library；第三方 → 外部路径，**而非** Library。

## 编排（模型无关）

家族子报告或数据源/语言是独立的工作路径。如果平台提供比编排器本身更廉价的子 Agent，可以为每个家族/数据源分配一个子 Agent，而编排器只负责整合/验证（专家蜂群）。否则由您自己顺序执行。

## 资源

- **模式：** `references/audit-mode.md`, `references/explore-mode.md`
- **共享：** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **审计：** `references/family-care.md`, `references/skill-finder.md`
- **探索：** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **分支：** `references/skill-branching.md`
- **脚本：** `scripts/inventory_skills.py`（盘点）, `scripts/inject_family_header.py`（标头路由器）, `scripts/scan_skill_security.py`（安全分诊）
- **模板：** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`, `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## 变更日志

### 1.1.0 (2026-06-17)
- 新增分支机制：第三方/只读 Skill 可以通过 fork 副本（分支）进行自定义 — 包含指向原件的引用、日期、作者和原因；原件保持不变。铁律“调查 ≠ 变更”补充了分支这一替代方案。新章节 `## 分支机制`。新文件：`references/skill-branching.md`, `assets/branch-header.example.md`。

### 1.0.0 (2026-06-17)
- 初始版本。在一个能够生成轻量级子 Skill 的安装程序中，集成了库存审计（家族聚类、带编号决策）和网络检索（带有安全分诊的控门安装）。