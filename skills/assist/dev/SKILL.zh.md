---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: 开发者助手（ATI 的继任者）。通过无头扫描提供快速的项目概览，并路由到可用的编程工具：CodeCommander MCP（分析/重构/诊断）和 ellmos-code-tools 模块。纯工具路由 + 扫描，无自定义存储。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: zh
status: active
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `dev` 官方中文版本。


# Dev — 开发者助手 (ATI) (中文)

首先获取概览，然后交由合适的工具处理。

## 概览与目的

BACH 的 ATI/entwickler 代理的继任者。包含两大任务：
1. **项目扫描**（无头模式，仅依赖 stdlib）：在进行高成本分析之前，快速且节省 Token 地获取项目的结构、语言和构建标记概览。
2. **工具路由**：分发至现有的编程工具，避免重复建设。

## 触发条件 (Triggers)

| 用户输入 | 操作 |
|---|---|
| "获取项目 X 的概览" | `dev_core.py scan <path>` |
| "这是什么类型的项目 / 使用什么技术栈？" | `dev_core.py scan <path>` |
| "分析此文件 / 重构" | → CodeCommander MCP |
| "生成/检查 Python 代码" | → CodeCommander MCP / ellmos-code-tools |

## 工具生态（路由目标）

- **CodeCommander MCP** (`.AI/.MCP/ellmos-codecommander-mcp`)：`cc_analyze_code`、`cc_analyze_methods`、`cc_extract_classes`、`cc_diagnose_imports`、`cc_runtime_import_diagnose`、`cc_generate_python_code`、`cc_check_indentation` 等。
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`)：CLI 开发者工具（Structural-Edit、pycutter context、Method-Analyzer）。
- **FileCommander MCP**：跨大型文件树的文件/目录操作。

## CLI 入口点 (dev_core.py)

```bash
python dev_core.py scan .              # current project
python dev_core.py scan /path/project  # structure + languages + markers
```

检测项示例：Python (pyproject/requirements/setup)、Node/TypeScript、Rust、Go、Java、Roblox (Rojo)、Docker、Git 仓库。

## 存储 (Store)

无存储。纯扫描 + 路由。

## 态度

我们推荐 CodeCommander/ellmos-code-tools 作为编程工具，但如果用户更偏好其他工具（如 ruff/pylint/eslint），我们也保持开放态度。

## 隐私

- `dev_core.py` 仅读取文件/目录名称（结构），不读取内容，不上传数据。
- 跳过项：`.git`、`node_modules`、`.venv`、`__pycache__` 等。

## 相关资源

- `assist/AGENTS.md` — 统一路由器
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## 更新日志

### 0.1.0 (2026-06-22)
- 初始版本。ATI/entwickler 的继任者：无头项目扫描 (stdlib) + 路由至 CodeCommander MCP / ellmos-code-tools。对用户中立，无存储。