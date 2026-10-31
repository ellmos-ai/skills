---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: "ellmos エコシステムで新しいエージェントロールを構築・検証する：ネイティブ Claude Code サブエージェント（永続的なロール定義）と Companion-Worker（SendMessage で再利用されるインスタンス、チケット／タスクシリーズ用）。エージェントロールの構築中に蓄積された、これまで形式化されていなかった独自の知見（ati-agent、bueroassistent、versicherungs-agent など）を、再利用可能な Scaffold-plus-Verify の手順に体系化する。新しいロールを作成したい場合（「新しいエージェントロールを作る」「サブエージェントを作成する」「Companion-Worker を起動する」）や、既存のエージェントがハウス規約に沿っているか検証したい場合（「このエージェントは正しく設定されているか？」）にこのスキルを使用する。"
visibility: public
language: ja
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
translated_from_sha256: 55b76ad25a5d65f61987662e674bc9c74ea0f6a8586ad4748268bc9441711db5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="agent-role-scaffolder banner">

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agenten-Orchestrierung START -->
> **エージェント・オーケストレーション・ファミリー — ガイド:** モデルの選択／段階的配置 -> `model-strategy`；オーケストレーションパターンの選択 -> `choose-your-orchestrator`；スウォーム操作（5つの基本パターン＋2つのモード）-> `swarm-operations`；タスクの分解・委任・受け取り -> `orchestrator`；プロバイダー横断のメッセージング／プレゼンス／ロック -> `agents-bridge`；**新しいロールを構築または検証する -> 本スキル（agent-role-scaffolder）**。
<!-- FAMILY-ROUTER:Agenten-Orchestrierung END -->

## 目的

このエコシステムには、すでに成熟したオーケストレーション系スキルのファミリー（`model-strategy`、`swarm-operations`、`orchestrator`、`choose-your-orchestrator`、`agents-bridge`）がありますが、**「新しいロールを適切に作るにはどうするか」を扱うものはありません。** `agent-role-scaffolder` はこのギャップを埋めます。上記のスキルを複製するのではなく、段階的配置、オーケストレーションパターン、またはプロバイダー横断メッセージングが必要になった時点で、それらへ**ルーティング**します。

**由来:** チケット `T-20260825-935905816`（マーケットプレイス全体の精査）でのユーザー決定 M5：判定 (b) — 独自のエージェント構築知見は存在していたが、形式化されていなかった。公式の Claude Code プラグイン `agent-sdk-dev`（claude-plugins-official、Apache-2.0）を**構造上の手本**として使用した。これは、scaffolding 用コマンドファイル1つと、チェックリストおよび PASS／PASS-WITH-WARNINGS／FAIL の報告形式を備えた検証用サブエージェント2つという構成である。取り入れたのは**形式**（Scaffold 質問カタログ → 構築 → 構造化報告付きの検証チェックリスト）であり、文章やテーマではない。そのプラグインは生の Claude Agent SDK アプリ（Python/TypeScript）を構築するが、本スキルは **ellmos 独自のエージェントロール**（サブエージェント定義と Companion-Worker）を構築する。原典はインストールしていない。ローカルのマーケットプレイスキャッシュに読み取り専用で置かれており、参照のみを行った（`.PLUGINS/CLAUDE.md` ルール5：アイデアは自由に使うが、表現はそのまま使わない）。レジスター項目：`.AI/.PLUGINS/PLUGIN-REGISTER.md`、ステータス `zitiert`。

## 2つの構築経路 — どちらもここに属する

ellmos エコシステムでは、新しいロールは構造的に異なる2つの経路で作られ、混同してはなりません（手本プラグインの TS／Python の分離に相当するが、ここでは実際のシステム境界に沿っている）：

| | **ネイティブサブエージェント** | **Companion-Worker** |
|---|---|---|
| 生成されるもの | 永続的なロール定義（`~/.claude/agents/<name>.md`、`Agent` ツールで起動可能） | 特定の名前を持つ一時的インスタンス。`SendMessage` で再利用され、**1つ**のタスクシリーズ専用 |
| 寿命 | 永続、セッションをまたいで再利用可能 | チケット／テーマシリーズの期間中のみ。その後破棄 |
| 既存の例 | `ati-agent`、`bueroassistent`、`versicherungs-agent`、`gesundheitsassistent`、`persoenlicher-assistent`、`production`、`research-agent`、`reflection-agent`、`test-agent`、`entwickler-agent` | このセッションモデル自体（例：`skillcreator-bau`、`policyreg-decisions`、`workflowhooker-ausbau` — チケットシステム内の名前付きワーカー） |
| ライフサイクル層 | Claude Code 独自のエージェントレジストリ | **COMA**（`.MODULES/.ORCHESTRATION/coma`）— プロセス横断で起動される場合。ツール内のみの場合は不要 |
| ここでの構築手順 | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**経験則:** その能力が、固定のトリガー説明（例：「税務証憑が関わるときは常に」）を持つ、複数セッションにわたって再利用される独自の名前を必要とする → ネイティブサブエージェント。限られてはいるが内容的にまとまったタスクの連続で、コーディネーターが今まさに委任している（チケットの連鎖、テーマの切り替え） → Companion-Worker。

## 手順

1. **構築経路を選ぶ**（上の表）— 迷ったら推測せず、ユーザーに確認する。
2. **Scaffold の質問を順に進める**（対応する `references/*.md` を参照）— 手本プラグインに倣い、一度にすべてではなく順番に：目的／きっかけ、ツールの必要性（`Tools:`）、モデル選択（→ **ステップ3**）、調整の必要性（ボスエージェントが専門家を率いるか、単独ロールか）。
3. **モデル選択はここでは決めず、`model-strategy` に委ねる。** スコアベースの選択、エージェント間委任、アドバイザーのペアリング、エスカレーションのトリガーは、そちらですでに解決されている。ここでは参照のみ。既存の経験則として、サブエージェントはメインモデルを**一律には継承しない**（フィードバックメモ `feedback_subagenten_modellstaffelung` を参照）。
4. **オーケストレーションパターンを確認する**。新しいロールが他の複数のロールと協働する場合：`choose-your-orchestrator` がパターンを選び、`swarm-operations` が5つの基本パターン＋2つのモードを提供し、`orchestrator` が分解・委任・受け取りのプロトコルを提供する。
5. **チーム／メッセージングの規約を守る**（`references/
   model-staffing-and-messaging.md`）：エージェント間通信には `SendMessage`、チケット委任時はファイル名によるチケットクレーム、依頼時は「繰り返さず参照する」（中核ルールをプロンプトに書き直さず、タスク固有の内容のみを書く）。
6. **検証する** — 選んだ `references/*.md` ファイルの該当チェックリストを処理し、`PASS / PASS MIT WARNUNGEN / FAIL` 形式で報告を作成する（構造は下記）。
7. **必要に応じて登録する** — 永続的な新ロールは該当するレジスター（`~/.claude/agents/`、必要に応じてプラグインのバンドル）に入れる。Companion-Worker はレジスター項目不要で、明確な最初のタスク引き継ぎだけが必要。

## 検証報告形式（両方の構築経路に共通）

構造は手本プラグインから意図的に取り入れた（形式であり文言ではない）— 簡潔な4つのセクション：

- **ステータス:** PASS | PASS MIT WARNUNGEN（警告付き合格）| FAIL
- **重大な問題:** ロールを使えなくする要素（トリガー説明の欠落、`Tools:` が広すぎる／狭すぎる、`model-strategy` で根拠づけられていないモデル、既存ロールとの境界が未確認）
- **警告:** 最適ではないが機能する要素（段階的配置ではなくメインモデルを継承している、長期稼働の Companion-Worker にローテーション基準がない など）
- **合格した検査項目と推奨事項:** 問題のない点と次に行うべきこと

## 関連スキル

- `model-strategy` — モデル選択／段階的配置（手順3、ここでは参照のみ）。
- `swarm-operations` — 複数ロールの協働のためのスウォームパターン。
- `choose-your-orchestrator` — 適切なオーケストレーションパターンを選ぶ。
- `orchestrator` — 分解・委任・受け取りのプロトコル。
- `agents-bridge` — プロバイダー横断のメッセージング／プレゼンス／ロック。新ロールが Claude Code の外で Codex／Gemini／Kimi と通信する必要がある場合。
- `skill-explorer` — 新しいロールを構築する**前に**、その能力がすでに存在するかを確認する（重複の回避）。

## 変更履歴

### 1.0.0 (2026-08-25)
- 初版。ユーザー決定 M5（`T-20260825-935905816`）に基づき `ellmos-skill-creator` を通じて構築。Companion-Worker パターン（一次資料：`_control-center/_TICKETS/README.md`、セクション「指導原則（コンテキスト経済）」）、COMA ライフサイクル（一次資料：`.MODULES/.ORCHESTRATION/coma/README.md`）、および既存ロールで観察された「ボスエージェントが専門家を調整する」パターンを形式化。`model-strategy`／`swarm-operations`／`orchestrator`／`choose-your-orchestrator`／`agents-bridge` を複製せず、意図的にそこへルーティングする。手本 `agent-sdk-dev`（claude-plugins-official）はインストールせず、読み取りのみを行い、構造上の出典として引用した（`.PLUGINS/CLAUDE.md` ルール5）。
