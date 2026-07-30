---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 使用 glob 通配符模式进行批量文件操作（删除、移动、复制、列出）。用于高效文件系统操作的 CLI 工具。零依赖。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/batch_file_ops.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `batch-file-ops` 官方中文版本。


# batch_file_ops - 批量文件操作 (中文)

用于使用 glob 模式高效批量处理文件的 CLI 工具。
支持：delete、move、copy、list。零依赖（仅限 Python 标准库）。

---

## 操作

| 操作 | 描述 |
|------|------|
| `delete` | 删除与模式匹配的文件 |
| `move` | 移动与模式匹配的文件 |
| `copy` | 复制与模式匹配的文件 |
| `list` | 列出与模式匹配的文件 |

## CLI 使用方法

```bash
python batch_file_ops.py <action> <source> [<target>] --pattern "<glob>" [--dry-run] [--recursive]
```

### 参数

| 参数 | 描述 |
|------|------|
| `action` | `delete`、`move`、`copy` 或 `list` |
| `source` | 源目录 |
| `target` | 目标目录（仅用于 `move` 和 `copy`） |
| `--pattern`, `-p` | Glob 通配符模式（例如 `*.py`、`TOOLS_*.py`） - 默认值：`*` |
| `--dry-run`, `-n` | 仅预览，不做更改 |
| `--recursive`, `-r` | 在子目录中递归搜索 |

---

## 示例与用法

```bash
# 列出目录中的所有 Python 文件 (中文)
python batch_file_ops.py list /path/to/directory --pattern "*.py"

# 删除所有 .tmp 文件 (先使用 dry-run 预览！) (中文)
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp"

# 移动文件 (中文)
python batch_file_ops.py move /source /target --pattern "*.txt"

# 复制文件（递归）(中文)
python batch_file_ops.py copy /source /target --pattern "*.md" --recursive

# 模式示例 (中文)
python batch_file_ops.py delete /path --pattern "TOOLS_*.py"
python batch_file_ops.py list /path --pattern "backup_202?-*"
```

---

## 注意事项

- **优先使用 Dry-run：** 在使用 `delete` 和 `move` 时，始终先使用 `--dry-run`
- **Glob 通配符模式：** 使用 Python 的 `pathlib.glob()` / `pathlib.rglob()`
- **兼容 Windows：** 自动 UTF-8 输出编码
- **仅限文件：** 跳过目录（仅处理文件）