---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: 操作 Rojo — 用于在 VS Code / Claude Code 中取代 Studio 编辑器进行专业 Roblox 开发的文件系统到 Roblox Studio 同步工具。凡涉及 Rojo 时请使用本 skill：`rojo serve`/`rojo build`、编写或调试 `default.project.json`、rokit/rokit.toml 与工具版本（Rojo, Lune, Wally）、嵌套与扁平路径映射（ReplicatedStorage.Project.shared）、连接/端口/同步问题，或需要创建 Roblox 项目脚手架时。当触发词为“rojo 连接失败”、“脚本在 Studio 中位置不对”、“如何将 src/ 映射到 Studio”、“端口 34872 被占用”、“Rojo 中 ModuleScript 与 Script 的区别”时也可触发。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: zh
status: active
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `rojo` 官方中文版本。


# Rojo — 文件系统 → Roblox Studio 同步

## 概述与目的

Rojo 将常规的文件系统项目（`src/` 中的 `.luau` 文件，通过 Git 进行版本控制）
连接到 Roblox Studio。您可以在自己选择的编辑器（VS Code、Claude Code）中编写代码，Rojo
会将其实时同步到运行中的 Studio 实例中。这使得 Roblox 代码可以像常规项目一样进行版本控制、
diff 比对，并使用专业工具编辑 — 而不必局限于 Studio 内置的脚本编辑器。

在处理 Rojo 配置、`default.project.json` 映射、工具链（rokit/Wally/Lune）以及常见同步问题时，请使用本 skill。

## 心智模型

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**核心规则：** 文件系统是唯一真理来源。每次连接时，Rojo 都会用文件系统内容覆盖
映射的 Studio 区域。因此，**切勿**在 Studio 中直接编辑代码（下一次同步时会被覆盖丢失），
只能在编辑器中修改。`Workspace`（3D 场景、地形）**不受** Rojo 映射并予以保留 —
场景与代码的工作流请参阅 `/rbx-studio` skill。

## 文件扩展名 → Roblox 类型（Rojo 约定）

Rojo 根据文件扩展名推导实例类型。这是最常见的错误来源：

| 文件               | Roblox 类型   | 可否 `require()` | 作用                      |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **是**          | 逻辑模块、定义            |
| `Foo.server.luau`  | Script        | 否              | 服务端入口点              |
| `Foo.client.luau`  | LocalScript   | 否              | 客户端入口点              |
| `init.luau`        | 成为文件夹节点本身 | 是          | 使该文件夹成为 ModuleScript |

> 经验法则：**只有入口点**使用 `.server.luau`/`.client.luau`。通过 `require()`
> 加载的所有内容**必须**是 `.luau` ModuleScript。对 Script/LocalScript 调用
> `require()` 会抛出 "Attempted to call require with invalid argument(s)" 错误。

## CLI 命令

```bash
rojo serve default.project.json     # 启动实时同步服务器（默认端口 34872）
rojo serve                          # 自动使用 default.project.json
rojo build default.project.json -o game.rbxlx   # 单次构建 → Place 文件 (XML)
rojo build default.project.json -o game.rbxl    # 单次构建 → Place 文件 (二进制)
rojo plugin install                 # 安装 Rojo Studio 插件（仅需一次）
rojo --version                      # 检查已安装的版本
```

在 `rojo serve` 之后：在 Studio 中打开 Rojo 插件 → **Connect** (localhost:34872)。
`rojo build` 不需要运行中的 Studio — 非常适合 CI、冒烟测试和发布。

## `default.project.json` — 映射配置

该文件将文件系统路径映射到 Roblox 数据模型层级。键名：

- `name` — 项目名称（显示用）
- `$className` — 节点的 Roblox 类名（`DataModel`, `ServerScriptService`, `Folder` …）
- `$path` — 在该节点下同步的文件系统路径（相对于项目根目录）

开箱即用的标准模板位于 [`assets/default.project.json`](assets/default.project.json)。

### 扁平 vs. 嵌套 — 最重要的决策

您的代码必须与映射方式保持一致。两种变体：

**扁平（Flat）** — `src/server` 的内容直接放置在 `ServerScriptService` 下：
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ 代码引用示例：`ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`。

**嵌套（Nested）** — 内容放置在 `ServerScriptService.ProjectName` 下：
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ 代码引用示例：`ReplicatedStorage.ProjectName.shared.Config` 等。

两种方式均有效。请在项目范围内确定使用**一种**变体，并保持所有
`require`/`WaitForChild` 路径与其一致。不匹配时的症状：`WaitForChild(...)`
无限等待（infinite yield），因为期望的节点位于其他位置。

## 通过 rokit 管理工具链

[rokit](https://github.com/rojo-rbx/rokit) 是工具链管理器。项目（或父文件夹）中的
`rokit.toml` 用于锁定具体的工具版本 → 在所有机器上实现可复现的构建。
如果缺失，将提示 `Failed to find tool 'rojo' in any project manifest file`。

标准 `rokit.toml`（参见 [`assets/rokit.toml`](assets/rokit.toml)）：
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> 版本说明：7.4.4 是整个参考流水线中持续锁定的版本。较新的项目可以使用 7.6.x —
> 但请先通过 `rojo build` 针对项目进行验证，因为主版本之间项目格式可能会发生变化。

克隆/设置完成后：执行 `rokit install` 拉取所有固定的工具。

- **Lune** — Studio 之外的 Luau 运行器（单元测试、构建脚本、资源处理）。
- **Wally** — 包管理器：`wally install` → `Packages/` → 在 Studio 中位于
  `ReplicatedStorage.Packages` 下。依赖项列在 `wally.toml` 中（参见
  [`assets/wally.toml`](assets/wally.toml)），例如框架 `sleitnick/knit@1.7.0`。

## 创建新项目

脚本 [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) 可创建一个
完整的 Rojo 脚手架（包含 project.json, rokit.toml, wally.toml, 带有初始文件的
`src/{shared,server,client,gui}/` 以及 KONZEPT 存根）：

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # 扁平映射（默认）
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # 嵌套映射
```

之后执行：`cd MeinSpiel && rokit install && rojo serve`。

## 故障排除

| 症状 | 原因 | 解决方案 |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | 缺少 `rokit.toml` | 在项目或父文件夹中创建包含 Rojo 固定版本的 `rokit.toml`，并运行 `rokit install` |
| `require` 抛出 "invalid argument(s)" | 对 Script/LocalScript 调用了 `require()` | 只有 `.luau` ModuleScript 才能被 require；请检查文件扩展名 |
| 端口 34872 被占用 (`os error 10048`) | 旧的 Rojo 进程正在运行 | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F`，然后重新运行 `rojo serve` |
| 脚本在 Studio 中位置不对 | 使用了扁平映射而非嵌套映射（或反之） | 调整 `default.project.json` 以匹配代码路径（见上文） |
| `WaitForChild` 无限等待 | 期望节点不存在 / 创建前服务端报错 | **首先检查服务端控制台是否有报错**；检查映射与创建顺序 |
| 重命名文件后同步停止 | Rojo 未能立即检测到重命名 | 停止服务器（Ctrl+C）并重新启动，在 Studio 中重新连接（Disconnect→Reconnect） |
| 断开重新连接后在 Studio 中的修改丢失 | 直接在 Studio 中编辑而非在文件系统中编辑 | **只能**在编辑器中修改代码；Rojo 会覆盖已映射的区域 |

### Rojo 的已知限制

1. **不支持地形/Workspace 同步** — 在 Studio 中构建 3D 场景和地形，或通过代码动态生成。
2. **不支持 `.rbxl` 合并** — Place 文件为二进制格式，无法进行 git 合并。切勿将其作为主要源码。
3. **Play 运行模式下不支持实时同步** — 在运行期间所做的修改会在停止运行后丢弃。
4. **Git Bash 路径转换问题** — `/c/...` 可能会被转换为 `C:/...` 从而破坏 Rojo 路径；如有疑问，请使用相对路径或 Windows 原生路径。

## 代码检查（Selene）

Roblox Luau 项目通常使用 **Selene** 进行代码检查（根目录下使用 `selene.toml`，
设置 `std = "roblox"`）。如果项目使用 `_G` 作为共享客户端状态，可通过
`global_usage = "allow"` 允许全局变量。请在包含 Roblox API 定义文件（`roblox.yml`）的目录中运行 Selene。

## 拓展阅读

- 关联 Skill：`/rbx-studio`（Studio 操作、MCP、资源），`/game-design`
  （角色、工作流、GDD），元 Skill `/rbx-dev`（融合上述三者 + 架构模式）。
- 当前引擎/Rojo 文档：Context7 MCP（`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`）或
  <https://rojo.space/docs/>。
- 如果本系统存在，项目丰富的参考流水线位于
  `<your Roblox project pipeline>`（包含 `ROJO_FAQ.md`, `SKILL.md`）。

## 更新日志

### 1.0.0 (2026-06-17)
- 初始版本。从 `.ROBLOX` 流水线（ROJO_FAQ, ROJO_START, _template）提炼，以用户中立的提炼方式编写。