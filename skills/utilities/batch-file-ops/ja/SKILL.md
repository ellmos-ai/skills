---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: globパターンを使用したバッチファイル操作（削除、移動、コピー、一覧表示）。効率的なファイルシステム操作のためのCLIツール。依存関係なし。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/batch_file_ops.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `batch-file-ops` の公式日本語版。


# batch_file_ops - バッチファイル操作 (日本語)

globパターンを使用してファイルに対して効率的なバッチ操作を実行するCLIツール。
対応アクション: delete、move、copy、list。依存関係なし（Python標準ライブラリのみ）。

---

## アクション

| アクション | 説明 |
|------------|------|
| `delete` | パターンに一致するファイルを削除 |
| `move` | パターンに一致するファイルを移動 |
| `copy` | パターンに一致するファイルをコピー |
| `list` | パターンに一致するファイルを一覧表示 |

## CLI の使用方法

```bash
python batch_file_ops.py <action> <source> [<target>] --pattern "<glob>" [--dry-run] [--recursive]
```

### 引数

| 引数 | 説明 |
|------|------|
| `action` | `delete`、`move`、`copy`、または `list` |
| `source` | ソースディレクトリ |
| `target` | ターゲットディレクトリ（`move` および `copy` のみ） |
| `--pattern`, `-p` | Glob パターン（例: `*.py`、`TOOLS_*.py`） - デフォルト: `*` |
| `--dry-run`, `-n` | プレビューのみ、変更は実行しない |
| `--recursive`, `-r` | サブディレクトリ内を再帰的に検索 |

---

## 例と使用方法

```bash
# ディレクトリ内のすべてのPythonファイルを一覧表示
python batch_file_ops.py list /path/to/directory --pattern "*.py"

# すべての .tmp ファイルを削除（最初に dry-run で確認！）
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp"

# ファイルを移動
python batch_file_ops.py move /source /target --pattern "*.txt"

# ファイルをコピー（再帰的）
python batch_file_ops.py copy /source /target --pattern "*.md" --recursive

# パターンの例
python batch_file_ops.py delete /path --pattern "TOOLS_*.py"
python batch_file_ops.py list /path --pattern "backup_202?-*"
```

---

## 注意事項

- **最初に Dry-run を実行:** `delete` および `move` では、必ず最初に `--dry-run` を使用してください
- **Glob パターン:** Python の `pathlib.glob()` / `pathlib.rglob()` を使用
- **Windows 対応:** 自動 UTF-8 出力エンコーディング
- **ファイルのみ:** ディレクトリはスキップされます（ファイルのみが処理されます）
