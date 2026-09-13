---
name: structured-thinking
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: メタスキル：3つのフェーズからなるワークフローとしての構造化思考。分析（think）、発想（brainstorm）、意思決定（decide）を1つの連続したプロセスに統合します。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [denken, analyse, kreativitaet, entscheidung, workflow, meta-skill]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'merged_from': ['utilities/think (v1.0.0)', 'utilities/brainstorm (v1.0.0)', 'utilities/decide (v1.0.0)'], 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="structured-thinking banner">

> **日本語** — `structured-thinking` の公式日本語版。


# Structured Thinking — 分析、発想、意思決定

> 構造化思考のためのメタワークフロー：問題分析から創造的な解決策、根拠ある意思決定まで

---

## ワークフローと手順

```
Problem/Question
     |
     v
Phase 1: ANALYZE (think)
  Divide & Conquer, Root Cause, Constraint Relaxation
     |
     v
Phase 2: IDEATE (brainstorm)
  SCAMPER, Six Hats, Reverse Brainstorming, Rapid Ideation
     |
     v
Phase 3: DECIDE (decide)
  Pro/Con, Weighted Scoring, Scenario Analysis, Eisenhower
     |
     v
Result + Rationale
```

---

## フェーズ 1: 分析 (Analyze)

目標：問題を理解し、原因を特定し、構造を把握する。

### アプローチ

| 手法 | 適用時 | 手順 |
|------|--------|------|
| **Divide & Conquer** | 複雑な問題 | 問題 → サブ問題 → 個別に解決 → 統合 |
| **Root Cause (5x Why)** | 症状は明確、原因が不明 | 症状 → なぜ？ → なぜ？ → ... → 原因 → 解決策 |
| **Constraint Relaxation** | 問題が解決不可能に見える | 制約を緩和 → 解決 → 制約を再適用 |
| **Analogy Search** | 新しい問題 | 似た既存の既知の問題を探す → その解決策を適応 |

### 分析フレームワーク

| フレームワーク | 適用 |
|----------------|------|
| **SWOT** | 強み / 弱み / 機会 / 脅威 |
| **Pareto** | 80/20 — 最大のレバレッジをもたらすものは何か？ |
| **Fishbone** | 体系的な原因分析（石川図） |

### 不確実性下のヒューリスティクス

1. 最悪のシナリオは何か？
2. それは不可逆か？
3. 行動しないことのコストは何か？

### 複雑性下のヒューリスティクス

1. 最もシンプルな第一歩は何か？
2. 専門家ならどうするか？
3. 80%の解決策とは何か？

---

## フェーズ 2: 発想 (Ideate)

目標：できるだけ多くの解決アプローチを生成する。質より量。このフェーズでは批判厳禁。

### 手法

**SCAMPER** —— 既存の解決策を体系的に改善する：
- **S**ubstitute（代用）：何を置き換えるか？ | **C**ombine（結合）：何を組み合わせるか？ | **A**dapt（適応）：何を適応させるか？
- **M**odify（修正）：何を修正するか？ | **P**ut to other use（転用）：他に何に使えるか？ | **E**liminate（削減）：何を削るか？
- **R**everse（逆転）：何を逆転させるか？

**6つの思考帽子**（de Bono）—— 6つの視点を順番に適用：
1. 青：プロセス管理（「問いは何か？」）
2. 白：事実（「何が分かっているか？」）
3. 赤：感情（「直感はどう感じるか？」）
4. 黒：批判（「何が失敗し得るか？」）
5. 黄：楽観（「どんな機会があるか？」）
6. 緑：創造性（「どんな新しいアイデアがあるか？」）

**逆ブレインストーミング** —— 問題を逆転させる：
1. 「どうすれば状況を悪化させられるか？」
2. 悪いアイデアを集める
3. 逆転＝良いアイデア

**ラピッド・アイディエーション** —— 20分で50以上のアイデア：
- ラウンド1（5分）：オープンな発想
- ラウンド2（5分）：バリエーション
- ラウンド3（5分）：組み合わせ
- ラウンド4（5分）：極端なアイデア

### 発想の後

1. クラスタリング：似たアイデアをグループ化
2. 実現可能性/インパクトマトリクス：実現可能性とインパクトを評価
3. フェーズ3のために上位5〜10個を選択

---

## フェーズ 3: 意思決定 (Decide)

目標：透明性のある根拠を持って最適な選択肢を選定する。

### フレームワークの選択

| 状況 | フレームワーク |
|------|----------------|
| 2つの選択肢、迅速な決定 | **メリット/デメリットマトリクス (Pro/Con Matrix)** |
| 3つ以上の選択肢、複数の基準 | **重み付きスコアリング (Weighted Scoring)** |
| 順序立った If-Then 決定 | **意思決定ツリー (Decision Tree)** |
| 高い不確実性 | **シナリオ分析 (Scenario Analysis)** |
| タスクの優先順位付け | **アイゼンハワーマトリクス (Eisenhower Matrix)** |

### 重み付きスコアリング（コア手法）

1. 基準の収集（3〜7個、具体的かつ測定可能）
2. 重みの設定（合計＝100%、最も重要なものは>=25%）
3. 選択肢の評価（1〜10段階）
4. スコアの計算（評価 x 重み）
5. 比較と推奨

### シナリオ分析

```
Best Case (X%):      Outcome → expected value
Realistic Case (X%): Outcome → expected value
Worst Case (X%):     Outcome → expected value
Total expected value: [sum]
```

### アイゼンハワーマトリクス

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

### 最終推奨前の品質チェックリスト

- [ ] 関連するすべての基準が特定されているか？
- [ ] ユーザーの価値観が考慮されているか？
- [ ] 長期的な影響が考慮されているか？
- [ ] リスクが特定され評価されているか？
- [ ] バイアスチェックが実施されているか？
- [ ] 可逆性が確認されているか？

---

## 文脈に応じた選択

| 状況 | 推奨フェーズ |
|------|--------------|
| 「問題がある」 | フェーズ1（分析）→ 場合によりフェーズ2+3 |
| 「アイデアが必要」 | フェーズ2（発想） |
| 「決断しなければならない」 | フェーズ3（意思決定） |
| 「行き詰まっている」 | フェーズ2（逆ブレインストーミング） |
| 「何を優先すべきか？」 | フェーズ3（アイゼンハワー） |
| 「複雑な問題を理解する」 | フェーズ1（Divide & Conquer + SWOT） |

---

## 変更履歴

### 1.0.0 (2026-05-19)
- think, brainstorm, decide からメタスキルとして作成

---

*Meta-skill | 詳細参照：[think](../think/SKILL.md), [brainstorm](../brainstorm/SKILL.md), [decide](../decide/SKILL.md)*
