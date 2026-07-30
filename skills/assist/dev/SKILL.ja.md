---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: 開発者アシスタント（ATI の後継）。ヘッドレススキャンによりプロジェクトの概要を迅速に取得し、利用可能なコーディングツール（CodeCommander MCP（分析/リファクタリング/診断）および ellmos-code-tools モジュール）へルーティングします。独自のストアを持たず、純粋なツールルーティングとスキャンを実行します。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: ja
status: active
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `dev` の公式日本語版。


# Dev — 開発者アシスタント (ATI) (日本語)

最初に概要を取得し、最適なツールへ引き継ぎます。

## 概要と目的

BACH の ATI/entwickler エージェントの後継。2つのタスクを実行します：
1. **プロジェクトスキャン**（ヘッドレス、標準ライブラリのみ）：高コストな分析を実行する前に、プロジェクトの構造、言語、ビルドマーカーの概要を高速かつトークン効率良く取得します。
2. **ツールルーティング：** 機能を重複させることなく、既存のコーディングツールに委任します。

## トリガー (Triggers)

| ユーザー入力 | アクション |
|---|---|
| 「プロジェクト X の概要を取得して」 | `dev_core.py scan <path>` |
| 「これはどんなプロジェクト？ / 技術スタックは？」 | `dev_core.py scan <path>` |
| 「このファイルを分析/リファクタリングして」 | → CodeCommander MCP |
| 「Python コードを生成/チェックして」 | → CodeCommander MCP / ellmos-code-tools |

## ツールランドスケープ（ルーティング対象）

- **CodeCommander MCP** (`.AI/.MCP/ellmos-codecommander-mcp`)：`cc_analyze_code`、`cc_analyze_methods`、`cc_extract_classes`、`cc_diagnose_imports`、`cc_runtime_import_diagnose`、`cc_generate_python_code`、`cc_check_indentation` など。
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`)：CLI 開発ツール（Structural-Edit、pycutter context、Method-Analyzer）。
- **FileCommander MCP**：大規模ツリーでのファイル/ディレクトリ操作。

## CLI エントリーポイント (dev_core.py)

```bash
python dev_core.py scan .              # current project
python dev_core.py scan /path/project  # structure + languages + markers
```

検出例：Python (pyproject/requirements/setup)、Node/TypeScript、Rust、Go、Java、Roblox (Rojo)、Docker、Git リポジトリ。

## ストア (Store)

ストアなし。純粋なスキャン + ルーティング。

## スタンス

コーディングツールとして CodeCommander/ellmos-code-tools を推奨しますが、ユーザーが他のツール（例: ruff/pylint/eslint）を希望する場合は柔軟に対応します。

## プライバシー

- `dev_core.py` はファイル/ディレクトリ名（構造）のみを読み取り、コンテンツの読み取りやアップロードは行いません。
- スキップ対象：`.git`、`node_modules`、`.venv`、`__pycache__` など。

## 関連リソース

- `assist/AGENTS.md` — 統括ルーター
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## 変更履歴

### 0.1.0 (2026-06-22)
- 初版。ATI/entwickler の後継：ヘッドレスプロジェクトスキャン（標準ライブラリ） + CodeCommander MCP / ellmos-code-tools へのルーティング。ユーザー中立、ストアなし。