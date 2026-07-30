---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: 面向 AI 代理的通用 Blender 工作流技能，适用于处理 .blend、.fbx、.obj、.glb、glTF、材质、场景检查、bpy 自动化、无头 Blender 批量运行、导出/重新导入验证、预览以及可选的 Blender MCP 控制。当任务要求以用户无关的方式打开、检查、创建、自动化、转换、优化、渲染或验证 Blender 或 3D 资产文件时使用。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: zh
status: active
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

> **中文** — `using-blender` 官方中文版本。

# 使用 Blender

## 核心规则

根据任务需求，按以下三种模式使用 Blender：

1. **GUI 模式：** 当用户希望查看、评估或手动编辑资产时，以可见方式打开 Blender。
2. **无头（Headless）模式：** 当需要导出、重新导入、批量处理或确定性检查时，使用 `blender --background --python <script.py>`。
3. **MCP 模式：** 仅在故意连接了正在运行的 Blender 插件且需要实时场景控制时使用。使用前需先检查安全与许可状况。

## 标准流程

1. 明确目标：查看、创建、转换、优化、渲染或验证。
2. 首先读取现有文件：清单（Manifest）、README、导出格式以及现有的检查结果。
3. 确定 Blender 路径：PATH 中的 `blender`、项目特定配置或用户路径。切勿将本地私有路径写入可公开发布的文档中。
4. 对于自动化操作，使用小型 `bpy` 脚本，明确定义输入、输出和错误处理。
5. 每次导出后，在将结果视为可用之前，至少执行一次重新导入或加载检查。
6. 简明扼要地记录产物：来源、导出格式、工具版本、检查状态及已知限制。

## 导出与验证规则

- 对于通用 Web/预览用途，优先选用 `.glb`。
- 如果目标工作流需要，为游戏引擎和 DCC 交换额外提供 `.fbx` 或 `.obj/.mtl`。
- 对于往返（Roundtrip）测试务必检查：文件存在、非空、可重新导入，且存在预期的对象/材质名称。
- 对于大型资产，收集度量指标：网格数量、材质、包围盒（Bounding Box）、文件大小以及可选的三角形数量。
- 对于渲染检查，在启动高昂的 Cycles 或 Full HD 渲染之前，先使用较低的预览分辨率。

## 安全规则

- `bpy` 代码是具有文件系统访问权限的本地 Python 代码。仅执行自行编写或经过审计的脚本。
- 在未进行许可和数据隐私检查的情况下，切勿启用第三方 Blender 插件、资产下载器或远程测量（telemetry）服务器。
- 对于包含任意 `execute_python` 工具的 MCP 服务器，需事先限制其作用域、网络、工作目录和超时时间。
- 对于市场或外部资产，需单独核实其许可协议。技术上的可加载性并不等同于使用授权。

## MCP 选项

如需进行实时控制，且需要选择、安装或评估 Blender MCP 服务器时，请阅读 [references/blender-mcp-review.md](references/blender-mcp-review.md)。

## 变更日志

### 1.0.0 (2026-06-20)
- 初始的用户无关 Blender 技能，具备 GUI、无头及 MCP 路由支持。