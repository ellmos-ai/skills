---
name: decision-briefing
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: トピック、プロジェクト、ドキュメント、またはセッションを通じて複数の決定事項が保留中または蓄積している場合にいつでも使用：インベントリを作成し、A/B/C/Dの選択肢と推奨事項を明示した番号付きブリーフィングを提示し、文字回答（バッチ処理を含む）を受け付け、結果を記録して元のドキュメントに書き戻します。

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


# Decision-Briefing — 1つのトピックに関する多数の意思決定の処理 (日本語)

> 蓄積した保留中の意思決定を推奨事項付きの番号付きブリーフィングに変換し、ユーザーが単一文字（個別またはバッチ）で超高速に回答できるようにします。

---

## 使用タイミング

**トピックに関わらず、複数の決定事項が保留中になり次第いつでも**使用します。典型的な状況：

- 1つの領域/トピックに多数の未決定事項が蓄積している
- ドキュメント（計画、TODOリスト、コンセプト）に複数の未決定項目が含まれている
- 会話中に複数の決定に関する質問が蓄積した
- Agent自身がユーザーに対して複数の質問を持っている — 1つずつ聞く代わりにブリーフィングとしてまとめる
- ユーザーが未決定項目を迅速かつ確固たる根拠に基づいてクリアしたい

**トリガーワード:** open decisions, decision session, briefing, work through, go through, let's decide all of this

**適用範囲:** [decide](../decide/SKILL.en.md) は1つの質問に対するフレームワークを提供します。`decision-briefing` は1つのトピックに関する多数の意思決定の処理を調整し、複雑な個別ケースに `decide` を適用します。

---

## コアUX (Core UX)

このスキルの核心はブリーフィングフォーマットです。各決定事項は、回答が文字1つで済むように提示されます：

- **ナンバリング:** `[E01]`, `[E02]`, … — セッションを通じて安定した参照
- **簡潔な質問** + 1〜2文の文脈
- **文字による選択肢** A/B/C/D（2〜4個の選択肢、必要な場合のみそれ以上）
- **明示された推奨事項** と1文の理由付け（例：`→ 推奨: A — なぜなら…`）
- 任意：結果の注意事項（選択から生じること）

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

### フェーズ 1: 収集とインベントリ作成

ソース：ユーザーが指定したもの、手元にあるドキュメント、または会話コンテキスト。システム全体のスキャンは行わず、すでに存在するもののみを対象とします。

1. 保留中のすべての決定事項をリスト化（1行に1つ：短縮タイトル）
2. **重複**を検出して統合（同じ質問の複数表現）
3. **依存関係**をマーク（「E04はE01に依存」）
4. **順序**を設定：ブロッカーを最優先（他が依存する決定）、次に緊急度順
5. リストをユーザーに示して確認（「すべて拾えていますか？漏れはありませんか？」）

### フェーズ 2: ブリーフィングの準備

決定事項ごと：

```
[E01] <Short question>
  Context: <1-2 sentences: Why is this up? What depends on it?>
  A) <Option>
  B) <Option>
  C) <Option>
  → Recommendation: <letter> — <one-sentence rationale>
  (optional) Consequence: <what follows from the choice / next action>
```

優れた選択肢のルール：

- 選択肢は相互に排他的であり、全体をカバーしていること
- 有用であれば「現状維持」または「保留」の選択肢を含める
- 推奨事項は透明性を持って根拠付けられる — 密かに誘導しない
- 事実が不明確な場合：まず明確化する（またはオープンクエスチョンとしてフラグを立てる）、推測しない

### フェーズ 3: 意思決定セッション

1. ブリーフィングを提示 — メッセージごとに1つの決定、またはバッチとして一度にすべて。5つを超える決定がある場合は3〜5個のブロックに分ける
2. 文字による回答を受け付け、確認を返す
3. 「詳細情報」の回答に対して：決定を深掘りする（以下のメソッドツールボックスを参照）
4. 複雑な個別ケース（多数の基準、高い利害）：[decide](../decide/SKILL.en.md) スキルへエスカレーション（加重スコアリング、シナリオ分析）
5. 保留された決定は明示的にオープンとして繰り越す — 黙ってドロップしない

### フェーズ 4: 記録と書き戻し

1. **結果テーブル**を作成：

```
| No.  | Decision            | Chosen | Status   |
|------|---------------------|--------|----------|
| E01  | <short title>       | A      | decided  |
| E02  | <short title>       | C      | decided  |
| E03  | <short title>       | —      | deferred |
```

2. 決定された項目を**元のドキュメント/TODOファイル**に書き戻す — オープンクエスチョンの場所、例：

```
DECISION: <question>
  → DECIDED 2026-06-13: Option A (<short form>)
  → Next action: <if the decision implies a follow-up action>
```

3. **保留項目を明示的にオープンとして維持**（元ドキュメントまたはTODOリスト内）し、次のブリーフィングで再提示されるようにする

---

## 例と応用

トピック：クラブWebサイトのリニューアル — プロジェクト計画からの3つの保留中の決定。

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

ユーザーがバッチで回答：**"1B 2C 3A"** → 結果テーブル、その後3つの決定事項がプロジェクト計画内で DECIDED とマークされます。

---

## メソッドツールボックス（「詳細情報」と深掘り用）

| メソッド | タイミング | 概要 |
|--------|------|---------|
| **メリット・デメリット行列** | 2〜3個の選択肢、迅速な比較 | すべての選択肢を並べて評価 |
| **加重スコアリング** | 複数の評価基準 | 基準の重み付け、選択肢ごとの点数（可能な限り定量化） |
| **二次思考 (Second-order thinking)** | 不明確な利害 | 帰結の帰結は何か？ |
| **プレモーテム (Premortem)** | リスクのある決定 | 「失敗した — なぜか？」 事前に弱点を特定 |
| **10/10/10 メソッド** | 感情的/時間的歪み | 10分後 / 10ヶ月後 / 10年後に決定はどう見えるか？ |

---

## 作業原則

- **決して決定を押し付けない:** 情報を提示し、推奨の根拠を透明に説明する — 決定するのはユーザー
- **バイアス検出:** 思考のエラーが見えたら指摘する（確証バイアス、サンクコスト）
- **可逆性に留意:** 可逆的な決定は迅速に下し、不可逆なものはより慎重に扱う
- **時間的プレッシャーを尊重:** 迅速な決定にはよりシンプルな手法が必要 — すべての質問が加重スコアリング分析を必要とするわけではない

---

## 適用範囲とシナジー

| 機能 | `decide` | `decision-briefing` |
|---|---|---|
| フレームワークによる単一決定の構造化 | ✓ | — |
| 1つのトピックに関する多数の決定のインベントリ作成 | — | ✓ |
| A/B/C選択肢付き番号付きブリーフィング | — | ✓ |
| バッチ回答 ("1A 2C 3B") | — | ✓ |
| 元のドキュメントへの書き戻し | — | ✓ |

**シナジー:** セッション内の複雑な個別ケースに対して、`decision-briefing` は `decide` のフレームワーク（加重スコアリング、シナリオ分析）を適用します。その前のより広範な思考プロセス（分析 → アイデア出し → 決定）については、[structured-thinking](../structured-thinking/SKILL.en.md) を参照してください。

---

## 変更履歴

### 1.0.0 (2026-06-13)
- BACH エキスパート `decision-briefing` v1.0.0 より移植。スキャナーコンポーネント (scanner.py, sources.json, マーカーのสキャン) は意図的に削除 — 収集は軽量で、手元のコンテキストに基づきます

---

*BACHより移植 | スキャナーなしのスタンドアロン版*

**参照:** [decide](../decide/SKILL.en.md) (単一決定用のフレームワーク) | [structured-thinking](../structured-thinking/SKILL.en.md) (メタワークフローとしての 分析 → アイデア出し → 決定)