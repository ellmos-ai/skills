---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 查找并删除在 Git Bash 中使用 /dev/null 创建的 Windows 保留 NUL 文件。支持无界面（Headless）或 GUI 模式。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/nulcleaner.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `nulcleaner` 官方中文版本。

# nulcleaner - Windows NUL File Cleanup (中文)

## 问题描述

在 Windows 的 Git Bash 中使用 `/dev/null` 时（例如 `> /dev/null`），输出不会重定向至空无之处，反而会在当前目录中生成一个名为 **`nul` 的实际文件**。Windows 将“NUL”保留为设备名称，这意味着无法通过常规方式删除这些文件。

该工具通过扩展 UNC 路径（`\\?\`）查找并删除此类 NUL 文件。

---

## 模式

| 模式 | 描述 |
|------|-------------|
| `scan` | 递归扫描目录中的 NUL 文件 |
| `delete` | 查找并删除 NUL 文件 |
| `gui` | 带文件选择功能的图形界面 |

---

## CLI 用法

```bash
# 仅扫描（显示找到的 NUL 文件） (中文)
python nulcleaner.py scan /path/to/directory

# 扫描并删除 (中文)
python nulcleaner.py delete /path/to/directory

# 启动 GUI 模式 (中文)
python nulcleaner.py gui
```

---

## 无界面 API (用于集成)

该工具还提供了用于无界面操作的 Python API：

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/path/to/directory", verbose=True)
print(f"Found: {result['found']}, Deleted: {result['deleted']}")
```

**返回值：** `{'found': int, 'deleted': int, 'errors': list}`

---

## 技术细节

- 使用扩展 UNC 路径（`\\?\`）删除 Windows 保留的文件名
- 使用 `os.walk()` 进行递归扫描
- 基于 tkinter 的 GUI（无外部依赖）
- 仅在 Windows 系统上有效（即出现该问题的地方）

---

## 预防措施

最好完全避免在 Git Bash 中使用 `/dev/null`。替代方案：
- 直接忽略输出
- 使用 `2>&1` 进行 stderr 重定向
- 在 Shell 脚本中注意 Windows 兼容性
