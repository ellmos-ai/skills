---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: 基于 Rojo 的完整 Roblox 游戏开发元技能 — 了解并统一三个专业技能 `/rojo`（文件系统→Studio 同步、项目设置）、`/rbx-studio`（编辑器、MCP、资源、恶意软件扫描）和 `/game-design`（角色、工作流、GDD）的入口点。在任何 Roblox 游戏开发工作中使用此技能：规划/构建/设置 Roblox 游戏、创建新项目骨架、定义代码架构（Main + 管理器模块、_G.ClientState + HUD、GameEnums 中的 Remotes）、避免 Luau/Roblox 陷阱，或者当不确定哪个 Roblox 专业技能合适时 — 路由由此处开始。也可在“开发 Roblox 游戏”、“构建 Roblox 游戏”、“新建 Roblox 项目”、“Luau 项目结构”、“如何组织 Roblox 代码”、“Roblox 开发设置”时触发。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: zh
status: active
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="rbx-dev banner">

> **中文** — `rbx-dev` 官方中文版本。

> **注意：** 与 Roblox Corporation 无关；“Roblox”是其所有者的商标。“rbx”是通用的社区简称。

# Roblox-Dev — Roblox 游戏开发元技能（中文）

## 概述与目的

基于 Rojo 且支持版本控制工作流的 Roblox 游戏开发核心入口点。
本技能汇总了全局知识 — 项目结构、架构模式以及最主要的 Luau 陷阱 — 并将专业问题路由至三个子技能：

| 子技能 | 用途 |
| --- | --- |
| **`/rojo`** | 文件系统→Studio 同步、`default.project.json`、rokit/Wally/Lune、项目骨架、同步问题 |
| **`/rbx-studio`** | Studio 操作、场景 vs 代码模式、Studio MCP、资源流水线、**恶意软件扫描** |
| **`/game-design`** | 角色与子任务、开发链、游戏设计文档（KONZEPT.md）、多 Agent 协作 |

> 路由规则：如果是关于**同步/构建/设置** → `/rojo`。关于 **Studio 中的编辑器/资源/测试**
> → `/rbx-studio`。关于**概念/角色/流程** → `/game-design`。关于**代码架构、
> Luau 陷阱或整体流程** → 留在本技能。

## 技术栈一览

- **语言：** Luau（`.luau`，非 `.lua`）。代码使用英文，注释/文档使用中文，UI 文本使用目标语言。
- **同步：** 结合 rokit 的 Rojo（固定工具版本）。文件系统 = 唯一事实来源。
- **工具：** Rojo（同步/构建）、Lune（Studio 外部的测试/脚本）、Wally（包管理器）、
  可选 Knit（服务/控制器框架，新项目）、Selene（代码检查器/linter）。
- **控制：** Roblox-Studio-MCP 用于 AI 驱动的检查/测试/资源插入。

## 项目结构（标准）

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

骨架由 `/rojo` 通过 `scaffold_roblox_project.sh` 创建。

## 架构模式

**服务端 — Main + 管理器模块。** 每个项目仅有**一个** Script：`Main.server.luau`。它
集中创建 remotes 文件夹并通过 `require()` 加载所有功能模块：
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
所有其他服务端文件均为 `.luau`（ModuleScripts）。

**客户端 — 共享状态 + HUD。** GameClient 写入共享状态，HUD 在 Heartbeat 中读取它：
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — 在 GameEnums 中集中定义。** 在 `GameEnums.Remotes` 中统一定义 remote 名称；
服务端根据这些定义创建事件，客户端通过相同的名称查找事件。这样可以避免服务端与客户端之间的字符串不匹配。

## 游戏的整体开发流程

1. **概念** (`/game-design`)：KONZEPT.md — 类型、USP、3–4 个核心机制、变现策略。
2. **设置** (`/rojo`)：生成骨架，定义 `default.project.json` 映射。
3. **后端**：Config → GameEnums → *Defs → Main.server → *Manager。
4. **前端**：GameClient → HUD。
5. **灰盒玩法测试** (`/rbx-studio`)：玩法优先，使用 basic parts + 可选 AI 材质。
6. **资源升级** (`/rbx-studio`)：Creator Store 资源、**恶意软件扫描**、场景保存为 .rbxl。
7. **测试** (`/game-design`)：QA + 游戏评论 + 用户画像盲测，不断迭代。
8. **发布** (`/game-design` 商业角色)：商店页面、变现、长线运营（live ops）。

## Luau/Roblox 常见陷阱（简明列表）

最常见的陷阱 — 完整标注列表：
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md)。

- 当同一行后面还有代码时，`task.wait(x)` 后面需要加分号。
- `Model.Position` 不存在 → 使用 `model:GetPivot().Position`。
- 字典上的 `#table` 为 0 → 手动计数。
- `mouse.Hit` 可能为 nil → 使用前检查。
- DataStore 调用**务必**放在 `pcall` 中。
- `tick()` 已废弃 → 使用 `os.clock()`；`SetPrimaryPartCFrame` → 使用 `PivotTo`。
- 事件名称在 `GameEnums.Remotes` 中集中管理；所有 RemoteEvent 在 `Main.server.luau` 中创建。
- 禁止循环 `require`（否则会导致死锁）。
- 仅在 `.luau` ModuleScripts 上使用 `require()`，切勿在 Scripts/LocalScripts 上使用。

## 每次 Commit 前（检查清单）

- [ ] 多语句行中 `task.wait(...)` 后加了分号
- [ ] 未使用 `Model.Position`、`tick()`、`SetPrimaryPartCFrame`
- [ ] DataStore 放在了 `pcall` 中，`mouse.Hit` 检查了 nil
- [ ] 事件名称服务端↔客户端一致（通过 GameEnums）
- [ ] 所有 RemoteEvents 均在 `Main.server.luau` 中创建
- [ ] 无循环 require
- [ ] Marketplace 资源已扫描（`/rbx-studio` → 恶意软件扫描），已归档报告

## 知识来源

- **当前引擎/创作者文档：** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine`（引擎 API）和 `/roblox/creator-docs`
  （教程/指南）；备用 <https://create.roblox.com/docs>。
- **参考流水线**（若本系统包含）：`<your Roblox project pipeline>` —
  包括 `SKILL.md`、`GUIDE.md`、`LESSONS_LEARNED.md`、`ROJO_FAQ.md`、`ROBLOX_MCP_FAQ.md`、
  `AGENT_ROLES.md`、`_malware_reports/PATTERNS.md`、`_knowledge/`（本地 API 缓存）。

## 更改日志

### 1.0.0 (2026-06-17)
- 初始版本。覆盖 `/rojo`、`/rbx-studio`、`/game-design` 的元技能；项目结构、架构模式和 Luau 经验总结提炼自 `.ROBLOX` 流水线，对用户中立。