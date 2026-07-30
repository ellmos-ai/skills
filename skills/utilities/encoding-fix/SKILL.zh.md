---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 用于修复双重/三重编码 UTF-8 的 Mojibake（乱码）修复工具。纠正 Windows cp1252/Latin-1 的误解析。零依赖。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/encoding_fix.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `encoding-fix` 官方中文版本。


# Encoding Fix (中文)

修复由于 Windows cp1252/Latin-1 误解析导致的 Mojibake（双重/三重编码的 UTF-8 乱码）。零外部依赖——仅基于 Python 标准库。

## 典型问题

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## 使用方法

### 作为 Python 库使用
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### 子进程输出处理
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### 命令行界面 (CLI)
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## 功能特性

- **幂等性:** 编码正确的文本不会被更改
- **多达 3 轮修复:** 甚至能修复三重编码的乱码字符串
- **子进程解码器:** 针对进程输出提供 UTF-8/cp1252 回退机制
- **零依赖:** 仅使用 Python 标准库

## 更新日志

### 1.0.0 (2026-03-12)
- 从 BACH system/tools/encoding_fix.py 移植