---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 新しいソフトウェアプロジェクトのオンボーディングに関する標準手順：機能分析、コード品質レビュー、オンボーディングチェックリスト、およびタスク作成。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `project-onboarding` の公式日本語版。


# 新しいソフトウェアプロジェクトの標準オンボーディング手順 (日本語)

**バージョン:** 1.0
**日付:** 2026-03-12

---

## 概要と目的

この手順は、新しく発見されたソフトウェアフォルダをタスク管理システムに追加する前に実行すべきステップを定義します。

```
+─────────────────────────────────────────────────────+
|             標準オンボーディング手順                |
+─────────────────────────────────────────────────────+
|  1. 機能分析の作成                                  |
|  2. コード品質レビュー（標準テスト）                |
|  3. TASKS.txt の作成                                |
|  4. タスク管理への追加                              |
+─────────────────────────────────────────────────────+
```

---

## フェーズ 1: 機能分析

**目的:** ツール、その機能、および開発ステータスを理解する。

**作成するファイル:** `Feature_Analysis_<ToolName>.md`

### テンプレート

```markdown
# 機能分析: <ToolName> (日本語)

## 概要
ツールが何を行うかを説明する簡潔な一文。

---

## ハイライト

| 機能 | 説明 |
|---------|-------------|
| **機能 1** | 説明 |
| **機能 2** | 説明 |

---

## 開発段階の評価

### 現在のステータス: **<Status> (<X>%)**

選択可能なステータス:
- プロトタイプ / Prototype (0-30%)
- アルファ / Alpha (30-60%)
- ベータ / Beta (60-85%)
- 本番準備完了 / Production Ready (85-95%)
- リリース / Release (95-100%)

| カテゴリ | 評価 (1-5) | 詳細 |
|----------|:------------:|---------|
| **機能性** | 3 | |
| **UI/UX** | 3 | |
| **安定性** | 3 | |
| **ドキュメント** | 3 | |

---

## 推奨される拡張機能

### 優先度: 高
1. ...

### 優先度: 中
2. ...

### 優先度: 低
3. ...

---

## 技術的詳細

フレームワーク:   <Framework>
ファイルサイズ:   Pythonコード計 <X> 行
メインファイル:   <main.py>

---
*分析作成日: <Date>*
```

---

## フェーズ 2: コード品質レビュー

**目的:** 技術的品質を確保し、既知の問題を特定する。

### 推奨されるチェック項目

| テスト | ツール | 説明 |
|------|------|-------------|
| **文字コード** | 文字コードチェッカー（例：`chardet`, `file`） | UTF-8であることを確認 |
| **メソッド分析** | リンター（例：`pylint`, `flake8`） | 肥大化したメソッドを検索 |
| **インデント** | フォーマッター（例：`black`, `autopep8`） | 一貫性をチェック |
| **インポート** | インポートチェッカー（例：`isort`, `pylint`） | 未使用のインポートを検索 |

### チェックポイント

- [ ] すべての .py ファイルは UTF-8 でエンコードされているか？
- [ ] 異常に大きいメソッド（100行超）はないか？
- [ ] インデントが一貫しているか（スペース vs タブ）？
- [ ] 未使用のインポートは削除されているか？
- [ ] Docstring が存在するか？

### 結果のドキュメント化

`TASKS.txt` の "QUALITY REVIEW" セクションに問題を記録します。

---

## フェーズ 3: TASKS.txt の作成

**目的:** 未完了のタスクを構造化された形式で記録する。

**作成するファイル:** プロジェクトフォルダ内の `TASKS.txt`

### テンプレート

```
TASKS - <ToolName> V<Version>
==============================
ステータス: <Status>
日付: <Date>

未完了タスク (OPEN TASKS):
[ ] <タスク 1> - 工数: <LOW|MEDIUM|HIGH>
[ ] <タスク 2> - 工数: <LOW|MEDIUM|HIGH>

---
完了済み (DONE - Archive):
- <完了したタスク> (<Version>, <Date>)
```

### ステータス値

| ステータス | 意味 |
|--------|---------|
| NEWLY DISCOVERED | 未分析（新しく発見された） |
| ANALYSIS NEEDED | 機能分析が進行中 |
| QUALITY REVIEW | コードテスト／レビューを実行中 |
| VALIDATED & READY | 検証完了、機能開発の準備完了 |
| MVP | 实装最小限の製品 (Minimum Viable Product) |
| BUILD ONLY | ビルド／コンパイルのみが必要 |
| BLOCKED | ブロック中（ユーザーテスト／決定待ち） |

---

## フェーズ 4: タスク管理の統合

フェーズ 1〜3 の完了後：

1. **タスクの移行:** TASKS.txt のエントリをタスク／チケットとして作成
2. **検証:** すべてのタスクが正しく分類されているか？
3. **分類:** プロジェクトを適切なカテゴリ（単一ツール、スイート、ライブラリなど）に割当

### 自動オンボーディングタスク

新規プロジェクトの場合、以下の標準タスクを作成します：

| タスク | 説明 | 工数 |
|------|-------------|--------|
| onb_1 | 機能分析の作成 | medium |
| onb_2 | コード品質レビュー | low |
| onb_3 | TASKS.txt の作成 | low |

タスクには依存関係があります：onb_2 は onb_1 に依存、onb_3 は onb_2 に依存。

---

## クイックチェックリスト

```
[ ] 1. Feature_Analysis_<Name>.md を作成した
[ ] 2. コード品質レビューを完了した（リンター、文字コード、インポート）
[ ] 3. ステータス付きの TASKS.txt を作成した
[ ] 4. タスクをタスク管理に追加した
```

---

## 例と適用

```bash
# 1. 機能分析
# -> Feature_Analysis_MyTool.md を作成（テンプレート参照）

# 2. コード品質
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # 文字コードのチェック

# 3. TASKS.txt
# -> ツールフォルダ内にステータス "QUALITY REVIEW" で作成

# 4. タスクの作成
# -> TASKS.txt のエントリをチケット/イシューとして登録
```

---

*作成日: 2026-01-10 | 移植日: 2026-03-12*