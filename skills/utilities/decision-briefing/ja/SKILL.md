---
name: decision-briefing
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: トピック、プロジェクト、ドキュメント、またはセッションを通じて複数の意志決定が保留または蓄積された場合に常に使用します。それらを棚卸しし、A/B/C/Dの選択肢と推奨事項を明記した番号付きブリーフィングを提示し、文字回答（バッチ処理を含む）を受け付け、結果を記録して元のドキュメントに書き戻します。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [entscheidung, briefing, batch, decision-session, priorisierung, workflow]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/decision-briefing/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `decision-briefing` の公式日本語版。


# Decision-Briefing — 1つのトピックに関する多数の意思決定の処理

> 積み上がった保留中の意志決定を、推奨事項付きの番号付きブリーフィングに変換し、ユーザーが単一の文字で迅速に回答できるようにします（1つずつ、またはまとめてバッチ処理）。

---

## いつ使用するか？

**トピックを問わず、複数の意思決定が保留中になった場合は常に**使用します。典型的な状況：

- 特定の領域/トピックで多くの保留中の意思決定が蓄積したとき
- ドキュメント（計画、TODOリスト、コンセプトなど）に未決定の項目が複数含まれているとき
- 会話の中で複数の意思決定を要する質問が蓄積したとき
- エージェント自身がユーザーに対して複数の質問を持っているとき — 1つずつ聞くのではなくブリーフィングとしてまとめて提示
- ユーザーが未決定事項を迅速かつ確実な根拠に基づいて解消したいとき

**トリガーワード:** 意思決定セッション、ブリーフィング、保留中の決定、順次処理、まとめて決定、一括決定

**スコープ:** [decide](../decide/SKILL.en.md) は「1つ」の質問に対するフレームワークを提供します。`decision-briefing` は1つのトピックに関する「多数」の意思決定の処理を調整し、複雑な個別ケースに対して `decide` を適用します。

---

## コアUX

このスキルの中核はブリーフィングフォーマットです。各意思決定は、回答に1文字の入力しかかからないように提示されます：

- **ナンバリング:** `[E01]`, `[E02]`, … — セッションを通じて一貫した参照ID
- **簡潔な質問** + 1〜2文のコンテキスト
- **文字による選択肢** A/B/C/D（2〜4個の選択肢、必要な場合のみ増やす）
- **明記された推奨事項** と1文の根拠（例: `→ Recommendation: A — because …`）
- オプション: 帰結についての注記（その選択から何が生じるか）

**ユーザー回答フォーマット:**

```
Single:    "E01: A"  or  "1A"
Batch:     "1A 2C 3B"  or  "E01: A, E02: C, E03: B"
Deepen:    "E02: more info"  or  "2?"
Defer:     "E03: later"
```

---

## ワークフローと手順

```
Topic + decisions at hand
     |
     v
Phase 1: CAPTURE & INVENTORY
     |
     v
Phase 2: PREPARE THE BRIEFING
     |
     v
Phase 3: DECISION SESSION
     |
     v
Phase 4: RECORD & WRITE BACK
```

### フェーズ 1: 収集と棚卸し

情報源：ユーザーが提示したもの、手元にあるドキュメント、または会話の文脈。システム全体のスキャンは行わず、既に存在する情報のみを対象とします。

1. すべての保留中の意思決定を一覧化（1行につき1項目：短いタイトル）
2. **重複** の検出と統合（同じ質問が複数回表現されている場合）
3. **依存関係** のマーク（「E04 は E01 に依存」）
4. **順序** の設定：ブロッカー（他の決定が依存しているもの）を優先し、次に対処の緊急度順
5. ユーザーに確認のためにリストを提示（「すべて網羅されていますか？不足はありませんか？」）

### フェーズ 2: ブリーフィングの準備

意思決定ごとに：

```
[E01] <Short question>
  Context: <1-2 sentences: Why is this up? What depends on it?>
  A) <Option>
  B) <Option>
  C) <Option>
  → Recommendation: <letter> — <one-sentence rationale>
  (optional) Consequence: <what follows from the choice / next action>
```

優れた選択肢を設定するためのルール：

- 選択肢は相互に排他的であり、選択肢の全範囲をカバーすること
- 有用であれば「現状維持」または「保留」の選択肢を含める
- 推奨事項は透明性を持って理由付けされ、誘導的であってはならない
- 事実関係が不透明な場合：推測せず、まず確認する（または未解決の質問としてフラグを立てる）

### フェーズ 3: 意思決定セッション

1. ブリーフィングを提示 — メッセージごとに1つの決定事項、またはバッチとして一度に提示。5を超える場合は3〜5個のブロックに分ける
2. 文字による回答を受け入れ、確認を返す
3. 「詳細情報」の回答に対して：意思決定を深掘りする（以下のメソッドツールボックスを参照）
4. 複雑な個別ケース（多基準、高リスク）の場合：[decide](../decide/SKILL.en.md) スキル（重み付けスコアリング、シナリオ分析）へエスカレーションする
5. 保留された決定事項は明示的に未解決として繰り越し、黙ってドロップしない

### フェーズ 4: 記録と書き戻し

1. **結果テーブル** を作成：

```
| No.  | Decision            | Chosen | Status   |
|------|---------------------|--------|----------|
| E01  | <short title>       | A      | decided  |
| E02  | <short title>       | C      | decided  |
| E03  | <short title>       | —      | deferred |
```

2. 決定した項目を **元ドキュメント/TODOファイル** の未決定の質問があった場所に書き戻す（例）：

```
DECISION: <question>
  → DECIDED 2026-06-13: Option A (<short form>)
  → Next action: <if the decision implies a follow-up action>
```

3. 次回のブリーフィングで再提示されるよう、**保留項目を元ドキュメントまたはTODOリストで明示的に保留状態として保持** する

---

## 例と応用

トピック：クラブのウェブサイトリニューアル — プロジェクト計画からの3つの保留中の決定。

```
[E01] Which system for the new website?
  Context: Current site is hand-maintained HTML; 2 people will maintain content in the future.
  A) Static site generator (fast, secure, maintained via Git)
  B) Classic CMS with admin interface
  C) Hosted website builder
  → Recommendation: B — two non-technical editors need an interface, not Git.

[E02] How is it hosted?
  Context: Budget ~10 EUR/month, no dedicated admin in the club.
  A) Shared hosting with the current provider
  B) Small dedicated VPS
  C) Managed hosting matching the chosen system
  → Recommendation: C — least maintenance effort without an admin; consequence: depends on E01.

[E03] When does the new site go live?
  Context: Content is 60% migrated; club anniversary in 3 months.
  A) Immediately as a soft launch (rest follows)
  B) After complete content migration
  C) On the anniversary as the deadline
  → Recommendation: A — reversible and yields early feedback; final content follows.
```

ユーザーがバッチで回答：**"1B 2C 3A"** → 結果テーブルの生成後、プロジェクト計画内で3つの意思決定が DECIDED とマークされます。

---

## メソッドツールボックス（「詳細情報」および深掘り用）

| メソッド | 適用場面 | 概要 |
|--------|------|---------|
| **長所・短所マトリクス (Pro/con matrix)** | 2〜3の選択肢、迅速な比較 | すべての選択肢を並べて評価 |
| **重み付けスコアリング (Weighted scoring)** | 複数の評価基準 | 基準を重み付けし、選択肢ごとに採点（可能な限り定量化） |
| **二次的思考 (Second-order thinking)** | 不確実な影響/リスク | 帰結の帰結（その後の影響）は何か？ |
| **プレモーテム (Premortem)** | リスクを伴う意思決定 | 「失敗した — なぜか？」事前に弱点を特定する |
| **10/10/10 メソッド** | 感情的/時間軸の歪み | 10分後 / 10ヶ月後 / 10年後にその決定はどう見えるか？ |

---

## 作業原則

- **意思決定を絶対に押し付けない:** 情報を十分に提供し、推奨理由を透明に説明する — 決定権はユーザーにある
- **バイアス検出:** 思考上の誤りがみられる場合は指摘する（確証バイアス、サンクコスト効果など）
- **不可逆性を考慮する:** 撤回可能な決定は迅速に下し、不可逆・最終的な決定はより慎重に扱う
- **時間的プレッシャーを尊重する:** 迅速な意思決定にはよりシンプルな手法を用いる — すべての質問が重み付けスコアリングを必要とするわけではない

---

## 適用範囲とシナジー

| 機能 | `decide` | `decision-briefing` |
|---|---|---|
| フレームワークを用いて単一の意思決定を構造化する | ✓ | — |
| 1つのトピックに関する多数の意思決定を棚卸しする | — | ✓ |
| A/B/C の選択肢付きの番号付きブリーフィング | — | ✓ |
| バッチ回答 ("1A 2C 3B") | — | ✓ |
| 元ドキュメントへの書き戻し | — | ✓ |

**シナジー:** セッション内の複雑な個別ケースについて、`decision-briefing` は `decide` のフレームワーク（重み付けスコアリング、シナリオ分析）を適用します。その前のより広範な思考プロセス（分析 → アイデア出し → 決定）については、[structured-thinking](../structured-thinking/SKILL.en.md) を参照してください。

---

## 変更履歴

### 1.0.0 (2026-06-13)
- BACH エキスパート `decision-briefing` v1.0.0 から移植。スキャナーコンポーネント（scanner.py, sources.json, マーカーのスキャン）は意図的に削除 — 収集は既存の文脈に基づく軽量な仕様に

---

*BACH より移植 | スキャナーなしのスタンドアロン版*

**関連項目:** [decide](../decide/SKILL.en.md)（単一の意思決定用フレームワーク）| [structured-thinking](../structured-thinking/SKILL.en.md)（メタワークフローとしての 分析 → アイデア出し → 決定）
