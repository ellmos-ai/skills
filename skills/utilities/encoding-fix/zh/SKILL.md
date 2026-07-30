---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 修复双重/三重编码 UTF-8 的乱码（Mojibake）。修复 Windows cp1252/Latin-1 误解析问题。零依赖。
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

修复由于 Windows cp1252/Latin-1 误解析导致的乱码（双重/三重 UTF-8 编码）。零依赖 — 仅使用 Python 标准库。

## 典型问题

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## 使用方法

### 作为库使用
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### 子进程输出
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## 特性

- **幂等性：** 正确编码的文本不会被修改
- **最多 3 轮修复：** 甚至能修复三重编码的字符串
- **子进程解码器：** 针对进程输出提供 UTF-8/cp1252 回退解码
- **零依赖：** 仅依赖 Python 标准库

## 更新日志

### 1.0.0 (2026-03-12)
- 从 BACH system/tools/encoding_fix.py 移植
