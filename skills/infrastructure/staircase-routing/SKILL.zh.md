---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  独立的导航与路由策略，通过在目录层级结构中向上和向下搜索指示牌文档（CLAUDE.md、AGENTS.md、
  README.md、RULES.md）以及用户可配置的关键词（通过 staircase-config.json 或 config.json）。
  亦被称为 Up-and-Down Routing（上下路由）或 Walking Bass Routing（低音步进路由）。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
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
---

> **中文** — `staircase-routing` 官方中文版本。

# Staircase-Routing（上下路由 / Walking Bass 路由）

**Staircase-Routing** 技能（亦称为 *Up-and-Down Routing* 或 *Walking Bass Routing*）为 AI 智能体抽离并独立了目录文档巡检策略。

当智能体进入某个目录或处理某个文件时，会使用该策略定位权威上下文、规则及指示牌文档，然后再修改代码或采取具体行动。

---

## 1. 指示牌文档标准

默认情况下，Staircase-Routing 会查找以下标准指示牌文档：
- **全局与项目控制：** `CLAUDE.md`、`AGENTS.md`、`START.md`、`RULES.md`
- **项目概述与任务：** `README.md`、`TODO.md`、`NOTIZ.md`、`BEWEISNOTIZ.md`
- **用户自定义关键词：** 通过 `staircase-config.json` 或 `config.json` 进行配置。

---

## 2. 遍历算法

```
                           [ Root / Workspace Level ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Step 2: Read Root Signpost)
                           └───────────▲────────────┘
                                       │ (Staircase Up)
                           ┌───────────┴────────────┐
                           │ Subfolder / Target Dir │ ◄── (Step 1: Start at CWD)
                           └───────────┬────────────┘
                                       │ (Staircase Down)
                           ┌───────────▼────────────┐
                           │ Child / Module Dir     │ ◄── (Step 3: Discover Sub-Signposts)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### 步骤 1：当前工作目录（CWD）巡检
- 巡检目标文件所在的目录或当前活动的工作目录。
- 如果存在指示牌文档，立即进行读取。

### 步骤 2：向上遍历（Staircase Up）
- 如果在 CWD 中**未**找到任何指示牌文档，则向上移动至父目录（`..`）。
- 逐步向上重复此过程，直到到达根指示牌文档（`CLAUDE.md` 或 `AGENTS.md`）或工作区边界。
- 读取所有发现的根指示牌文档，以确立全局指令与项目规则。

### 步骤 3：向下巡检（Staircase Down）
- 从已确立的根目录开始，向下步进至与当前任务相关的子目录。
- 发现特定模块级的指示牌文档、领域规则或组件配置，并对其进行读取。

---

## 3. 用户可配置关键词（`staircase-config.json`）

智能体可以读取本地或全局的 `staircase-config.json` 来自定义目标指示牌：

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. 与 `letter-hooker` 及定时任务的集成

`staircase-routing` 作为核心预检引导程序（bootloader）嵌入在 **`letter-hooker`** 技能和 **`antigravity-kontext-and-workflow-loader-and-divider`** 定时任务中，以确保智能体在发起任何修改之前始终能够定位并遵循指示牌文档。