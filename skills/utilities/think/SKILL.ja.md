---
name: think
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-06
description: "コード以外の問題を、決めたり変更したりする前にまず理解する必要があるときに使います。業務の流れ、組織、製品、戦略、指標、事業レベルのシステムの挙動など、原因が複数考えられる問題、部分に分解したい込み入った状況、SWOT や 80/20 の視点が必要な場面: 'なぜ ... が繰り返し起きるのか'、'根本原因を探して'、'なぜを5回'、'サブ問題に分けて'、'どこから手を付ければいい'、'簡単に SWOT して'、'実際には何が起きているのか'、/think。分割統治、根本原因分析、制約の緩和、類推探索、SWOT、パレート、特性要因図を使い、見つかった原因または構造と最初に確認すべき点で締めくくります。次の用途には使わないでください: ソフトウェアの欠陥（エラーメッセージ、失敗するビルド・テスト・デプロイ、リグレッション: bugfix-protocol）、多数のアイデア出し（brainstorm）、与えられた選択肢からの選択（decide）、プロジェクト履歴と照合したアイデア発掘（idea-mining）、分析・発想・決定を通した一連の流れ（structured-thinking）。"

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="think banner">

> **日本語** — `think` の公式日本語版。


# Think — 問題解決と分析

> 複雑な問題のための構造化思考プロセス

---

## 問題解決のアプローチ

### 1. Divide & Conquer（分割統治）

```
Problem -> Sub-problems -> Solve individually -> Combine
```

### 2. Root Cause Analysis（根本原因分析）

```
Symptom -> Why? -> Why? -> Why? -> Root cause -> Solution
```

### 3. Constraint Relaxation（制約緩和）

```
Unsolvable problem -> Relax constraints -> Solve -> Re-apply constraints
```

### 4. Analogy Search（類似検索）

```
New problem -> Similar known problem -> Adapt solution
```

---

## 分析手法

| 手法 | 適用 |
|------|------|
| **SWOT** | 強み / 弱み / 機会 / 脅威 |
| **Pro/Con (メリット/デメリット)** | 意思決定 |
| **Pareto** | 80/20 優先順位付け |
| **Fishbone** | 根本原因分析（石川図） |

---

## 意思決定ヒューリスティクス

### 不確実性下

```
1. 最悪のシナリオは何か？
2. それは不可逆か？
3. 行動しないことのコストは何か？
```

### 複雑性下

```
1. 最もシンプルな第一歩は何か？
2. 専門家ならどうするか？
3. 80%の解決策とは何か？
```

---

## 変更履歴

### 1.1.0 (2026-11-06)
- 説明文を明確なトリガーと境界づけで書き直し（docs/CONVENTIONS.md の規則）: 使用場面、典型的なユーザーの言い回し、スラッシュコマンドを先頭に置き、隣接スキルを「使わない場合」の節で明示。

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*