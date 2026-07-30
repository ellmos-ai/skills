---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: 用于 Python 应用程序的通用插件系统。支持自动发现、校验和容错。零依赖（仅使用 Python 标准库）。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="plugin-system banner">

> **中文** — `plugin-system` 官方中文版本。


# Plugin System (中文)

适用于 Python CLI 应用程序的具容错能力的插件系统。
故障插件绝不会导致应用程序的其他部分停止运行。

## 核心特性

- **自动发现（Auto-Discovery）：** 自动查找目录中的插件
- **校验（Validation）：** 检查每个插件类上的 `name`、`version` 和 `execute()`
- **容错性（Fault Tolerance）：** 有缺陷的插件将被记录到日志中但不会被加载
- **零依赖（Zero Dependencies）：** 仅使用 Python 标准库

## 文件列表

```
scripts/
  plugin_system.py       核心：PluginBase (ABC) + PluginManager
  cli_demo.py            带有 argparse 的演示 CLI
  test_plugin_system.py  16+ 个单元测试
examples/
  hello.py               Hello World 插件
  calculator.py          计算器插件
  systeminfo.py          系统信息插件
```

## 快速入门

### 1. 创建插件

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. 使用 PluginManager

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./my_plugins")
plugins = manager.discover_plugins()

# 列出所有插件
manager.list_plugins()

# 执行插件
success, result = manager.execute_plugin("MyPlugin", param="value")
if success:
    print(result)
```

### 3. 集成到您的应用程序中

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## 插件接口

每个插件必须满足：

| 要求 | 详细信息 |
|-------------|---------|
| 继承 `PluginBase` | `from plugin_system import PluginBase` |
| 设置 `name` | 类属性，非空 |
| 设置 `version` | 类属性，语义化版本 |
| 实现 `execute()` | 接受任意 `*args, **kwargs` |

## 容错机制

| 错误类型 | 行为 |
|-----------|----------|
| 插件中的 `SyntaxError` | 跳过该插件，继续加载其余插件 |
| 缺失必要属性 | 插件被标记为 `is_valid=False` |
| `execute()` 中的异常 | 返回 `(False, error_message)` |
| 目录中无插件 | 返回空列表，不会崩溃 |

## 变更日志

### 1.0.0 (2026-03-12)
- 从 MODULAR_AGENTS/plugins 迁移至技能库
- PluginBase ABC + PluginManager
- 3 个示例插件 (Hello, Calculator, SystemInfo)
- 16+ 个单元测试
- 带有 argparse 的 CLI 演示