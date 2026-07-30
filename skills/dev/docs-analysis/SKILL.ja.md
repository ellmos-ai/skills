---
name: docs-analysis
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: ドキュメント要件分析：docs/ フォルダ内のコンセプトおよび要件ドキュメントを分析し、要件を現在のコードと照合して、統合された差分レポートを作成します。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [docs-analysis, requirements, code-review, diff-report, quality-assurance]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/docs-analyse.md', 'origin_version': '1.2.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `docs-analysis` の公式日本語版。


# ドキュメント要件分析 (日本語)

> すべてのコンセプトおよび要件ドキュメントを分析し、要件を現在のコードと照合して、統合された差分レポートを作成します。

---

## 概要と目的

`../docs/` フォルダ内のすべてのコンセプトおよび要件ドキュメントを分析し、それらの要件を現在のコードと照合して、統合された差分レポートを作成します。

---

## 命名規則

### プレフィックスとサフィックス
すべての分析対象ドキュメントには以下が付与されます：
- **プレフィックス：** `conN_` （N = 分析バージョン：1, 2, 3, ...）
- **サフィックス：** `_XX` （XX = 達成率：10 の倍数に四捨五入）

### アーカイブのしきい値
- **>= 75% 達成：** ドキュメントは `../docs/_archive/` に移動
- **< 75% 達成：** ドキュメントはプレフィックス/サフィックス付きで `../docs/` に保持
- **しきい値は設定可能**（デフォルト：75）

---

## プロセス

### フェーズ 1: ドキュメントの収集
- `../docs/`（ルート）内のすべての `*.md` および `*.txt` ファイルを一覧表示
- `README.txt` を除外

### フェーズ 2: 要件の抽出
各ドキュメントについて：
- コンテンツを読み込む
- 要件の特定（チェックリスト、表、MISSING/TODO マーカー）
- 分類：構造、コード、API、DB スキーマ、CLI、機能

### フェーズ 3: コード検証
各要件について：
- 検証方法の決定（Glob、Grep、Read）
- 検証を実行
- 状態を記録：FULFILLED, PARTIAL, MISSING

### フェーズ 4: 評価
- 達成済み要件と未達成要件をカウント
- 達成率（%）を計算
- 判定：アーカイブ（>= 75%）または保持（< 75%）

### フェーズ 5: 出力の生成
- `REQUIREMENTS_ANALYSIS.md` の作成（要約）
- `consense_diff.md` の作成（未達成要件のみ、優先度順）

### フェーズ 6: バージョニング
- 最大の `conN_` プレフィックスをスキャン
- 新しいバージョン = 最大 + 1

### フェーズ 7: リネームと移動
- ドキュメントに新しいプレフィックス/サフィックスを適用
- アーカイブまたは保持

---

## 出力

| ファイル | 説明 |
|----------|------|
| `conN_REQUIREMENTS_ANALYSIS.md` | 完全な分析（バージョン N） |
| `consense_diff_N.md` | 統合された未達成要件 |
| `_archive/conN_*_XX.*` | アーカイブ済み（>=75%）ドキュメント |

---

## 優先度分類

| 優先度 | 基準 |
|:------:|------|
| P1 | コア機能が欠落、システム利用不可 |
| P2 | 重要な機能が欠落、回避策あり |
| P3 | あると良い、UX の向上 |
| P4 | 軽微、ドキュメント、コード品質 |

---

## 変更履歴

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*