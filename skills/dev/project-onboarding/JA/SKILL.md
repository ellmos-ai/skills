---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 新しいソフトウェアプロジェクトのオンボーディング標準手順：機能分析、コード品質レビュー、オンボーディングチェックリスト、タスク作成。

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


# 新規ソフトウェアプロジェクトの標準オンボーディング手順 (日本語)

**バージョン:** 1.0
**日付:** 2026-03-12

---

## 概要と目的

本手順は、新しく発見されたソフトウェアフォルダをタスク管理システムに追加する前に実行する手順を定義します。

```
+─────────────────────────────────────────────────────+
|           STANDARD ONBOARDING PROCEDURE              |
+─────────────────────────────────────────────────────+
|  1. Create feature analysis                          |
|  2. Code quality review (standard tests)             |
|  3. Create TASKS.txt                                 |
|  4. Add to task management                           |
+─────────────────────────────────────────────────────+
```

---

## フェーズ 1: 機能分析

**目的:** ツール、その機能、および開発状況を理解する。

**作成ファイル:** `Feature_Analysis_<ToolName>.md`

### テンプレート

```markdown
# Feature Analysis: <ToolName> (Deutsch)

## Brief Description
A short sentence describing what the tool does.

---

## Highlights

| Feature | Description |
|---------|-------------|
| **Feature 1** | Description |
| **Feature 2** | Description |

---

## Development Stage Assessment

### Current Status: **<Status> (<X>%)**

Possible statuses:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Category | Rating (1-5) | Details |
|----------|:------------:|---------|
| **Functionality** | 3 | |
| **UI/UX** | 3 | |
| **Stability** | 3 | |
| **Documentation** | 3 | |

---

## Recommended Extensions

### Priority: High
1. ...

### Priority: Medium
2. ...

### Priority: Low
3. ...

---

## Technical Details

Framework:      <Framework>
File size:      <X> lines of Python
Main file:      <main.py>

---

*Analysis created: <Date>*
```

---

## フェーズ 2: コード品質レビュー

**目的:** 技術的品質を確保し、既知の問題を特定する。

### 推奨されるチェック項目

| テスト | ツール | 説明 |
|--------|--------|------|
| **エンコーディング** | エンコーディングチェッカー（例: `chardet`, `file`） | UTF-8 を確保 |
| **メソッド分析** | リンター（例: `pylint`, `flake8`） | 巨大なメソッドを検出 |
| **インデント** | フォーマッター（例: `black`, `autopep8`） | 一貫性をチェック |
| **インポート** | インポートチェッカー（例: `isort`, `pylint`） | 未使用のインポートを検出 |

### チェックポイント

- [ ] すべての .py ファイルが UTF-8 でエンコードされているか？
- [ ] 異常に大きなメソッド（>100行）がないか？
- [ ] インデントの一貫性があるか（スペース vs タブ）？
- [ ] 未使用のインポートが削除されているか？
- [ ] Docstring が存在するか？

### 結果の記録

問題点を TASKS.txt の "QUALITY REVIEW" に記録する。

---

## フェーズ 3: TASKS.txt の作成

**目的:** 未完了タスクを構造化された形式で記録する。

**作成ファイル:** プロジェクトフォルダ内の `TASKS.txt`

### テンプレート

```
TASKS - <ToolName> V<Version>
==============================
Status: <Status>
Date: <Date>

OPEN TASKS:
[ ] <Task 1> - Effort: <LOW|MEDIUM|HIGH>
[ ] <Task 2> - Effort: <LOW|MEDIUM|HIGH>

---
DONE (Archive):
- <Completed task> (<Version>, <Date>)
```

### ステータス値

| ステータス | 意味 |
|------------|------|
| NEWLY DISCOVERED | 未分析 |
| ANALYSIS NEEDED | 機能分析の進行中 |
| QUALITY REVIEW | コードテストを実行中 |
| VALIDATED & READY | 機能開発の準備完了 |
| MVP | 実用最小限の製品 |
| BUILD ONLY | ビルドのみ必要 |
| BLOCKED | ユーザーテスト/決定待ち |

---

## フェーズ 4: タスク管理の統合

フェーズ 1〜3 を完了した後：

1. **タスクの転送:** TASKS.txt のエントリをタスク/Issueとして作成する
2. **検証:** すべてのタスクが正しく分類されているか？
3. **分類:** プロジェクトを適切なカテゴリ（単一ツール、スイート、ライブラリなど）に割り当てる

### 自動オンボーディングタスク

新しいプロジェクトでは、以下の標準タスクを作成します：

| タスク | 説明 | 工数 |
|--------|------|------|
| onb_1 | 機能分析を作成 | 中 |
| onb_2 | コード品質レビュー | 低 |
| onb_3 | TASKS.txt を作成 | 低 |

タスクには依存関係があります: onb_2 は onb_1 に依存、onb_3 は onb_2 に依存します。

---

## クイックチェックリスト

```
[ ] 1. Feature_Analysis_<Name>.md created
[ ] 2. Code quality review completed (linter, encoding, imports)
[ ] 3. TASKS.txt created with status
[ ] 4. Tasks added to task management
```

---

## 例と適用方法

```bash
# 1. Feature analysis (Deutsch)
# -> Create Feature_Analysis_MyTool.md (see template) (Deutsch)

# 2. Code quality (Deutsch)
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Check encoding

# 3. TASKS.txt (Deutsch)
# -> Create in tool folder with status "QUALITY REVIEW" (Deutsch)

# 4. Create tasks (Deutsch)
# -> Capture TASKS.txt entries as issues/tickets (Deutsch)
```

---

*作成日: 2026-01-10 | 移植日: 2026-03-12*
