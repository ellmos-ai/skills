---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 二重/三重エンコードされた UTF-8 の文字化け修理。Windows cp1252/Latin-1 の誤解釈を修正。依存関係ゼロ。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/encoding_fix.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="encoding-fix banner">

> **日本語** — `encoding-fix` の公式日本語版。


# Encoding Fix (日本語)

Windows cp1252/Latin-1 の誤解釈によって発生する文字化け（二重/三重エンコードされた UTF-8）を修復します。依存関係ゼロ — Python 標準ライブラリのみ使用。

## 典型的な問題

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## 使い方

### ライブラリとして使用
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### サブプロセス出力
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## 特徴

- **冪等性：** 正しくエンコードされたテキストは変更されません
- **最大 3 ラウンド：** 三重にエンコードされた文字列さえも修復
- **サブプロセスデコーダー：** プロセス出力用の UTF-8/cp1252 フォールバック
- **依存関係ゼロ：** Python 標準ライブラリのみ使用

## 変更履歴

### 1.0.0 (2026-03-12)
- BACH system/tools/encoding_fix.py から移植
