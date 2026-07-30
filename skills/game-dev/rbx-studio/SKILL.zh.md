---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: 使用 Roblox Studio 进行游戏开发 —— 用于构建、测试和发布 3D 场景的官方可视化编辑器。使用此 Skill 了解：Studio 基础知识（Explorer、Workspace、运行测试、将 Place 保存为 .rbxl）、与 Rojo 的协同工作（Connect、场景模式与代码模式）、通过 Roblox-Studio-MCP 进行 AI 控制（execute_luau、insert_from_creator_store、generate_material、screen_capture、Play/Stop、读取 Console）、完整的 Asset 流水线工作流（Creator Store → 清理 → 套件构建 → 场景搭建 → .rbxl → Rojo 赋予活力），以及最重要针对 Marketplace Asset 的强制恶意软件扫描。还可在包含以下词汇时触发："在 Store 中嵌入资产"、"Studio MCP 不工作"、"studios: []"、"生成材质"、"保存场景"、"这个 Roblox 资产安全吗"、"Play 之后脚本消失"。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: zh
status: active
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `rbx-studio` 官方中文版本。

> **Note:** Not affiliated with Roblox Corporation; "Roblox" is a trademark of its owners. "rbx" is the common community shorthand.

# Roblox Studio — 编辑器、测试、资产与 MCP

## 概述与目的

Roblox Studio 是官方编辑器：用于构建 3D 场景、在 Play 模式下测试游戏、
从 Creator Store 插入资产，以及发布 Place。在 Rojo 工作流中，
Studio 拥有**场景**（Workspace、Terrain、放置的模型）和**测试** ——
而**代码**通过 Rojo 来自文件系统（参见 Skill `/rojo`）。

本 Skill 涵盖：Studio 基础知识、场景与代码工作的清晰分离、
通过 Roblox-Studio-MCP 进行 AI 控制，以及包含对每个 Marketplace 资产进行
**强制恶意软件扫描**的资产工作流。

## 基础知识

- **Explorer** — 所有 Instance 的树状结构（Workspace、ServerScriptService、ReplicatedStorage 等）。
  在 Rojo 激活状态下，映射区域会从文件系统实时填充。
- **Play-Test（运行测试）** — 绿色 Play 按钮（或 F5）可启动本地服务器+客户端会话。
  每次启动后，**检查 Output 控制台是否有错误** —— 这是最重要的调试习惯。
- **保存 Place** — File → Save As → `.rbxl`（二进制）或 `.rbxlx`（XML，可进行 diff 比较）。
  保存的 Place 包含**场景**。代码存在于文件系统中，而不是 Place 中。

## 关键工作流：场景模式 vs. 代码模式

连接（Connect）时，Rojo 会用文件系统内容覆盖所有已映射的脚本区域。
`Workspace`（3D 场景）**未**被映射并保持原样。由此得出了
日常工作中最重要的一条规则 —— 切勿混淆这两种模式：

**模式 A — 编辑场景（Rojo 关闭）：**
1. 停止 Rojo 服务器（`taskkill //F //IM rojo.exe` 或 Ctrl+C）。
2. 在 Studio 中打开 Place，放置资产，构建世界并进行布置。
3. File → Save → `.rbxl` 现在保存了新的场景。

**模式 B — 测试代码（Rojo 开启）：**
1. 在 Studio 中打开同一个 Place。
2. 启动 `rojo serve` → 在 Studio 的 Rojo 插件中点击 Connect。
3. 按下 Play 并测试。Rojo 会同步脚本；Workspace 来自 `.rbxl`。
4. 在 Rojo 运行期间，**不要**保存（否则 Rojo 的状态会冻结写入 `.rbxl` 中）。

通过这种方式，场景工作（Studio）和代码工作（编辑器 + Rojo）可以并行且无冲突地运行 —— 
美术人员构建场景，开发者编写代码。

## Roblox-Studio-MCP — AI 控制 Studio

Roblox-Studio-MCP 允许 Claude/Gemini/Codex 直接控制正在**运行**的 Studio
实例：执行代码、检查属性、Play/Stop、读取控制台、插入资产。它**不能**
替代 Rojo —— 而是对 Rojo 的补充：Rojo 用于持久的代码修改，MCP 用于检查、
测试、资产插入和材质生成。

```
编辑器 + Rojo  ──(持久代码同步)──►  Studio (运行中)  ◄──(检查/测试/插入)──  MCP ◄── AI
```

### 可用的 MCP 工具（典型）

| 工具 | 用途 |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | 列出已打开的实例 / 选择当前激活的实例 |
| `search_game_tree` / `inspect_instance` | 搜索层级结构 / 读取属性 |
| `execute_luau` | 直接在 Studio 中执行 Luau 代码 |
| `script_read` / `script_grep` / `script_search` | 分析脚本 |
| `multi_edit` | 批量修改多个实例/脚本 |
| `start_stop_play` | 控制 Play/Stop |
| `get_console_output` | 读取 Output 日志 |
| `screen_capture` | 截取场景屏幕截图 |
| `insert_from_creator_store` | 从 Creator Store 插入资产 |
| `generate_material` | 生成 AI 材质/纹理 (MaterialVariant) |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | 模拟输入 |

### 配置设置（用户无关）

MCP 作为随 Studio 一起分发的服务器运行，通常通过一个轻量级 JSON 过滤包装器进行连接
（用于过滤掉某些客户端无法解析的非 JSON banner）：

- MCP 批处理文件 (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- 可选包装器: `<your roblox-mcp wrapper>`
  （如果本系统存在；由 Claude/Codex/Gemini 共享）
- 客户端配置: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

配置示例 (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

### 常见的 MCP 问题

| 症状 | 含义 / 解决办法 |
| --- | --- |
| `studios: []` 或 `Not connected to WS host` | 并不意味着立即“损坏”：发送 `initialize` → 等待 2–3 秒 → `list_roblox_studios`；否则重启 Studio |
| `Error: connection closed: initialized request` | Studio 根本没有打开 —— 启动 Studio，加载 Place，重试 |
| 通过 MCP 编写的脚本在 Play/Stop 后消失 | 通过 MCP 对代码进行的修改不是持久性的 —— 对于持久代码更改请使用 **Rojo** |
| 插件 VM 中通过 `require()` 获取的值错误 | 插件 VM 有自己的 require 缓存 —— 如需验证，直接读取 `.Source` 或在 Play 后检查服务器日志 |

## 资产流水线（Creator Store → 游戏）

先进行 Greybox（灰盒测试玩法），后续再添加资产（发布前）。经过验证的顺序：

```
搜索商店      → 例如 "medieval" → 加载多个候选对象
筛选剔除      → 移除风格不符/劣质资产，保留 5–8 个合适的资产
清理资产      → 移除所有脚本（防恶意软件！），仅保留几何体/网格 (Meshes)
构建套件/集合 → 基于基础资产衍生变体（统一材质与比例）
构建场景 (Studio) → 将资产组装为场景（村庄、竞技场、公园）
保存为 .RBXL  → 场景作为“舞台”
ROJO 赋予活力 → 通过 Rojo 添加脚本/玩法/HUD；Workspace 保持不变
```

**变体技术（“模块化套件”）：** 获取一个良好的基础资产，并基于它衍生出整套
物件（房屋 → 塔楼、粮仓、铁匠铺、废墟）。它们共享材质、颜色和
比例 —— 以最小的精力实现一致的外观，这也是专业工作室的通用做法。

**资产来源（优先级）：** Creator Store（免费、庞大，**必须进行恶意软件检查**） →
AI 材质（`generate_material`） → 自制网格（Blender → .fbx） → 购买的资产包。

## 强制要求：Marketplace 资产的恶意软件扫描

Creator Store 资产可能包含混淆的恶意脚本（后门、远程代码、
Bot 网络钩子）。在使用前扫描**每一个**导入的资产并移除所有脚本 ——
仅保留几何体/网格 (Meshes)。

- 模式参考：[`references/malware-patterns.md`](references/malware-patterns.md) — 8 个
  已知混淆模式（反向属性 Payload、伪造系统脚本、远程
  `require()`、`loadstring`、`string.char`、`getfenv/setfenv`、隐藏 Values、延迟执行）。
- 扫描器：[`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — 在 Studio 中通过
  `execute_luau`（或 Command Bar）运行它；它会对照所有模式检查 Instance 并报告发现。

**警示信号（需立即注意）：** 纯装饰模型中包含大型脚本 · 属性中的反向字符串 ·
`require(<number>)` · `loadstring` · 不需要网络功能的资产中包含 `HttpService`。
如有疑问：直接删除该脚本。记录发现结果（例如参考流水线中的 `_malware_reports/YYYY-MM-DD_*.md`）。

## 重要的 Luau/Studio 踩坑指南（节选）

在 Studio 中最常遇到的陷阱 —— 完整的列表由 Skill `/rbx-dev` 维护：

- `Model.Position` 不存在 → `model:GetPivot().Position`。
- `tick()` 已弃用 → `os.clock()` / `workspace:GetServerTimeNow()`。
- `SetPrimaryPartCFrame()` 已弃用 → `model:PivotTo(cf)`。
- DataStore 调用**务必**包裹在 `pcall` 中。
- Baseplate + 程序生成的地板在同一高度 → Z-fighting（闪烁）：移除 Baseplate
  或将地板提升 +0.1 studs。
- 注意 Part 预算（每个程序生成的房间建议约 50–80 个 Part）。

## 进一步阅读

- 姐妹 Skill：`/rojo`（同步、项目配置）、`/game-design`（角色、工作流、GDD）、
  元 Skill `/rbx-dev`（架构模式 + 所有 Luau 经验）。
- 引擎/开发者文档：Context7 MCP（`/websites/create_roblox_reference_engine`、
  `/roblox/creator-docs`）或 <https://create.roblox.com/docs>。
- 参考流水线（如果存在）：`<your Roblox project pipeline>`
  （`ROBLOX_MCP_FAQ.md`、`ASSET_PIPELINE.md`、`_malware_reports/PATTERNS.md`）。

## 变更日志

### 1.0.0 (2026-06-17)
- 初始版本。提炼自 `.ROBLOX` 流水线（ROBLOX_MCP_FAQ、ASSET_PIPELINE、
  PATTERNS、LESSONS_LEARNED），以用户无关的方式编写。