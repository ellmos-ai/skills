---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: "決定の要点を1つ、または関連する決定のグループについて、極めて短く実質のある出力形式。背後の分析がすでに存在する場合(チャットで作成、`decide`、`decision-briefing`、チケットまたは文書から)に使用します。コンテキストは2〜3行、各選択肢の賛否は箇条書きで、paveman/caveman風に簡略化したスタイル、トーキングポイント、根拠のある推奨、そして完全な説明を読むための分析全文へのパス/リンクを記載します。「賛否と推奨付きで簡潔に」「決定事項のエグゼクティブサマリー」「<Thema>の簡単な背景」「決定Xを短くまとめて」、/decision-shot、または完全な導出ではなく本質だけが必要な人に結果を渡す場合にこのスキルを使用してください。多数の未決定事項を収集して文字ごとに問い合わせるためには使用しないでください(それはdecision-briefingの役割です)。決定をまだ分析する段階では使用しないでください(それはdecideの役割です)。decision-shotは完成した分析を前提とし、その提示のみを圧縮します。"
visibility: public
language: ja
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
translated_from_sha256: 26ff135e844d526543d9f5df212d36e408a427a71cc13a9e744a55abdb5ed991
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:12.134714+00:00"
---
<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> 分析はすでに終わっています。今必要なのは二度目の導出ではなく、要点と、完全版へ戻るための道筋です。

## 使用するタイミング

- 1つの決定(または密接に関連する決定のグループ、例えば同じテーマの複数の下位質問)がすでに検討済みである場合 — チャット内、チケット内、`decide`フレームワークによるもの、または`decision-briefing`のフェーズ2によるもの — で、それを今すぐ誰か(ユーザー、別のエージェント、引き継ぎ文書)が数秒で把握できるようにする必要がある場合。
- トリガーとなる語句: 「賛否と一緒に短く」「エグゼクティブサマリー」「簡単な背景」「それについてのトーキングポイント」「推奨付きで圧縮して」、`/decision-shot`。
- **使用しないこと**: ユーザーが順番に、またはバッチで文字ごとに回答することになっている未決定の複数の論点がある場合 — それは[decision-briefing](../decision-briefing/SKILL.md)の役割です。決定をこれから検討する場合 — それは[decide](../decide/SKILL.md)の役割です。decision-shotは既存の分析を提示するための純粋な表現方法です。

## 区別(要約)

| スキル | 役割 | 完了の時点 |
|---|---|---|
| `decide` | フレームワーク(賛否マトリクス、加重スコアリング、決定木など)を使って1つの決定を検討する | 分析がまだ残っている |
| `decision-briefing` | あるテーマの多数の未決定事項を集め、A/B/C/Dのバッチとして提示し、文字による回答を受け付ける | 複数の論点が未決定のまま |
| `decision-shot` | 1つの完成した分析(出所を問わず)を、完全版へのリンク付きのエグゼクティブ向け要約に圧縮する | 分析はすでにあり、提示だけが欠けている |
| `knappform` | セッション内のすべての回答に対する汎用の回答スタイル修飾子 | セッション全体に及び、テーマに依存しない |
| `paveman` | 既存の文章ファイル(ルール/メモリファイル)を決定論的に短くする | ファイルを短くする、チャット出力ではない |

`decision-shot`は上記4つのいずれとも競合しません。`decide`の後、または`decision-briefing`と並行して、本質を伝達する必要が生じたときに使う**形式**です。簡略化された文体は`knappform`/`paveman`に従います(完全な削除リストはそちらを参照)が、ここでは固定の5部構成の形式に一貫して適用されます。

## 形式(必須、5部構成)

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## ルール

- **利用者向けの文章には技術的な番号や略語を含めない(一人称の日常語)**: 人間に見える本文(タイトル、コンテキスト、選択肢、トーキングポイント、推奨)には、内部の略語、チケット番号(`T-...`)、D番号、相対ファイルパスを**含めないでください**。
  コンテキストは状況と予定の行動を一人称で説明します(「私は〜を提案します」)。
  技術的な参照(チケットID、正確なファイルパス)は、最後の行`**Vollanalyse:**`、または参照表にのみ記載します。
- **行数は上限であり目標ではない。** コンテキスト2〜3行、選択肢ごとに箇条書き2〜4個、トーキングポイント2〜3個、推奨は1文。これを超えるものは削除し、短くして残すことはしません。1つの選択肢が4つの箇条書きに収まらない場合、それはこのスキルに属さず、完全版の分析に属します。
- **`knappform`/`paveman`に倣った簡潔な文体**: 埋め草の語、決まり文句、回避表現は使わない。否定(`nicht`、`nie`、`kein`、`nur`、`außer`)はそのまま残す — 削除すると主張が逆転するため。
- **賛否は文ではなく箇条書き。** `+`/`-`を接頭辞とし、1行に1つの考えを書き、補足文は付けない。
- **トーキングポイントは分析的ではなくコミュニケーション用。** 「分析に何と書いてあるか」ではなく、「誰かに聞かれたら何と言うか」に答えるものです。賛否リストと重複している場合は、まだ十分に凝縮されていない兆候です。
- **推奨は1文で自ら根拠を示す。** 賛成リストの繰り返しや「上記参照」は不要 — その1文だけで、ブロックの残りがなくても成立する必要があります。
- **完全版分析へのリンク/パスは必須であり、任意ではない。** decision-shotは分析の代わりにはならず、分析を素早く見つけられるようにするものです。確かな出所がない場合(口頭でチャット内に生まれ、文書がないなど)は、欄を空白にせず、チャット/セッションの参照をできるだけ具体的に示します(例: 「このセッション、F4への回答」)。
- **関連する複数の決定**(グループ、例えば同じテーマの複数の下位質問): 決定ごとに1ブロックとし、`---`で区切ります。共通のコンテキストは、本当にすべてに当てはまる場合にのみ冒頭に一度書きます。

### 保存されたDecision-Shotのセッション由来

重要な新規の永続成果物として保存される決定ショットは、次で終わります:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

セッションIDは、まず明示的な実行時/CLIの指定から取得し、その後で信頼できるプロバイダー環境またはフックから取得します。両方がない場合は`unbekannt`と記載します。値を推測することは決してしないでください。サブエージェントは親セッションを使用します。通常のチャット、出典、ポリシー、`CLAUDE.md`、READMEおよび旧ファイルには、一律に刻印や後付けの刻印をしません。

## 例

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## 変更履歴

### 1.2.0 (2026-09-18)
- わかりやすい決定文の文体ルールを定着(T-20260913-883789445、利用者の指示 2026-09-13):
  - 表示テキスト(タイトル、コンテキスト、トーキングポイント)にチケット番号、D番号、内部パスを含めない。
  - コンテキストと推奨は一人称の日常語で、自然な表現で書く。
  - 技術的なチケットおよびパスの参照は、最後の完全版分析の行に厳密に限定する。

### 1.1.0 (2026-09-09)
- P-018: 重要な新規保存のDecision-Shotにセッションスタンプを追加。出典の優先順位を狭め、除外項目を設定。

### 1.0.0 (2026-08-24)
- 初版。
