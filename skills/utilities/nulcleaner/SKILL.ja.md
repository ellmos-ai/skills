---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Git Bash で /dev/null を使用した際に作成される Windows 予約済み NUL ファイルを検索および削除します。ヘッドレスまたは GUI で動作します。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/nulcleaner.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `nulcleaner` の公式日本語版。

# nulcleaner - Windows NUL File Cleanup (日本語)

## 問題点

Windows 上の Git Bash で `/dev/null` をコマンドに使用した場合（例：`> /dev/null`）、出力が破棄されず、現在のディレクトリに **`nul` という名前の実際のファイル** が作成されます。Windows では "NUL" がデバイス名として予約されているため、これらのファイルは通常の方法では削除できません。

本ツールは拡張 UNC パス（`\\?\`）を利用して、このような NUL ファイルを検索および削除します。

---

## モード

| モード | 説明 |
|------|-------------|
| `scan` | ディレクトリ内の NUL ファイルを再帰的にスキャン |
| `delete` | NUL ファイルを検索して削除 |
| `gui` | ファイル選択機能付きのグラフィカルインターフェース |

---

## CLI の使い方

```bash
# スキャンのみ（発見された NUL ファイルを表示） (日本語)
python nulcleaner.py scan /path/to/directory

# スキャンして削除 (日本語)
python nulcleaner.py delete /path/to/directory

# GUI モードを起動 (日本語)
python nulcleaner.py gui
```

---

## ヘッドレス API（統合用）

本ツールはヘッドレス運用向けの Python API も提供しています：

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/path/to/directory", verbose=True)
print(f"Found: {result['found']}, Deleted: {result['deleted']}")
```

**返り値:** `{'found': int, 'deleted': int, 'errors': list}`

---

## 技術的詳細

- 拡張 UNC パス（`\\?\`）を使用して Windows 予約済みファイル名を削除
- `os.walk()` による再帰的スキャン
- tkinter による GUI（外部依存関係なし）
- Windows 上でのみ動作（問題が発生する環境）

---

## 予防策

Git Bash での `/dev/null` の使用は避けるのがベストです。代わりに以下を検討してください：
- 単に出力を省略する
- stderr のリダイレクトには `2>&1` を使用する
- シェルスクリプトにおける Windows 互換性に注意する