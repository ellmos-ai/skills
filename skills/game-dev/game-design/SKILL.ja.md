---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: ゲーム開発のプロセスとしての進め方 — ロール、サブタスク、ワークフロー、およびロールの説明（特にRobloxを対象としていますが、それに限定されません）。具体的なコードではなくゲーム開発の「組織構造」に関する場合にこのskillを使用します：どのようなロールが存在するか（Creative Director、Engineer、Artist、Polish/Audio、Business、QA-Tester、Game Critic）？誰がどのサブタスクを担当するか？開発チェーン（コンセプト → バックエンド → フロントエンド → ブラッシュアップ → テスト）はどのようになっているか？Game Design Document / KONZEPT.md の書き方は？複数の（AI）エージェントでゲームをどのように分担するか？「新しいゲームの計画」、「Game Design Document の作成」、「ゲームに必要なロール」、「ゲームの開発ワークフロー」、「誰がテストするか」、「ゲームアイデアの構造化」、「Robloxのジャンル/マネタイズ」などのキーワードでもトリガーします。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/game-design/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="game-design banner">

> **日本語** — `game-design` の公式日本語版。


# Game Design — Roles, Subtasks & Workflows

## 概要と目的

ゲーム開発は、単一の人物または1つのAIエージェントが複数の役割を兼任する場合であっても、明確に分離された専門分野からなるチームワークです。このskillは**組織モデル**を提供します：どのようなロールが存在し、どのサブタスクがそれに属し、どのような順序で相互作用し、どのようにゲームをコンセプト（GDD）としてまとめるか。*技術的な*方法については、`/rojo`（同期）、`/rbx-studio`（エディタ/アセット）、およびメタskill `/rbx-dev`（アーキテクチャ）を参照してください。

新しいゲームの計画、作業の分担（複数のAIエージェントに跨る場合を含む）、および Game Design Document の執筆/レビュー時にこのskillを使用します。

## ロール（開発5つ + テスト2つ）

実績のあるコンパクトなロール分配。すべてのサブタスクを含む完全な説明：[`references/roles-and-workflows.md`](references/roles-and-workflows.md)。

| ロール | 焦点 | 核心サブタスク |
| --- | --- | --- |
| **Creative Director** | 何を（WHAT）、なぜ（WHY）、誰のために（for WHOM） | GDD/KONZEPT、メカニクスの設計と調整、優先順位付け/スプリント、ストーリー、UXフロー |
| **Engineer** | どのように（HOW・技術的） | サーバー/クライアント/共有コード、ゲームループ、ネットワーク/remotes、DevOps（Rojo、ビルド）、バグ修正 |
| **Artist** | 世界がどのように見えるか | 世界/レベルデザイン、ライティングと雰囲気、パーティクル、アセット調達（マルウェアチェック含む） |
| **Polish / Audio** | どのように感じられ、聞こえるか | SFX/音楽/環境音、アニメーション、UI/UX微調整、ジュース感（画面揺れ、ヒットストップ）、フィードバック |
| **Business** | 外部向け | ストアページ、アイコン/サムネイル、マネタイズ（gamepass/プロダクト/パス）、アナリティクス、コミュニティ |
| **QA-Tester** | 技術的に正しいか | コードのバグスキャン、プレイテスト + コンソール確認、再現可能なレポート、回帰テスト、パフォーマンス |
| **Game Critic** | 面白いか | プレイヤー目線での第一印象・長期的印象、誠実な評価（面白さ、わかりやすさ、公平性）、提案 |

**基本ルール:** 開発とテストは**分離された**ロールです — 理想的には別々の人またはエージェントが担当します。コードを書いた本人はそれを客観的にテストできません。Game Critic は厳しい評価を行っても構いません。

## ワークフローと手順

作業はロールからロールへとチェーンのように流れます。最も重要なパターン：

**標準フィーチャーチェーン:**
```
Creative Director (plans feature) → Engineer (backend) → Artist (frontend/assets)
→ Polish/Audio (sound + fine-tuning) → QA-Tester (technical test)
→ Game Critic (player perspective) → Creative Director (feedback → next iteration)
```

**クイックフィックスチェーン:** QA-Tester (bug) → Engineer (fix) → QA-Tester (verifies)。

**アセットチェーン:** Artist (store search) → Artist (malware scan) → Artist (integrate) → QA (visual)。

**ポリッシュチェーン:** Game Critic (weakness) → Polish/Audio → Artist → Game Critic (re-check)。

**ヒューマンインザループ:** [agent chain] → human tester → Creative Director (feedback) → [chain]。

各イテレーションでは短い変更履歴を残す必要があります。終了条件：時間予算到達 **または** 品質目標の達成。

### ペルソナベースのテスト（Persona-based testing）

ゲームは非常に多様なプレイヤーが対応できて初めて生き残ります。そのため、自分自身の視点からだけでなく、年齢、経験、プラットフォーム（PC/モバイル/タブレット/コンソール）、集中力持持続時間、言語、アクセシビリティによって変化させた複数の**ペルソナ**（エージェントによるシミュレーションも可）からテストします。例：ボタンを押したいだけのタブレット上の9才のカジュアルな子供、メタ要素を探すPC上の12才のコアプレイヤー、大きなボタンを必要とする60才以上の初心者。
ペルソナテストは**ブラインド**（テスト担当者はデザイン意図を知らない状態）で実施する必要があります。

## Game Design Document (KONZEPT.md)

すべてのゲームを簡潔な GDD にまとめます — テンプレート: [`assets/KONZEPT_template.md`](assets/KONZEPT_template.md)。最小構造：

- **ビジョン** — 1〜2文: ゲームとは何か？
- **ジャンル / 参考** — 分類 + 参考タイトル。
- **コアメカニクス** — **最大 3〜4 つ**（集中が品質を生みます）。
- **ゲームプレイプーループ** — プレイヤーの毎分のループ体験。
- **ゲームモード / 形式** — 該当する場合。
- **マネタイズ** — gamepass、デベロッパープロダクト、バトルパス、ショップ。
- **技術** — スタック（Rojo/フレームワーク）、大まかなアーキテクチャ。
- **次のステップ** — 実装チェックリスト。
- **既知のバグ / 未解決の問題**。

## マルチエージェントによる分工

複数の AI エージェント（または人間+AI）でゲームを分担できます — 2つのモード：

- **Swarm（スウォーム）** — 同じタスク、異なる領域（例: 3つのエージェントがそれぞれ1つのシステムをバランス調整する）。
- **Team（チーム）** — 異なるロール、相互に調整（Engineer + Artist + Polish が1つの機能に対して並行して作業し、Creative Director が調整する）。

実践で証明されたルール: 開発とテストを**絶対に**同じエージェントに割り当てないこと、ロールごとにプロンプトを固定すること（システムプロンプト = ロール説明）、各チェーンのイテレーションは変更履歴 + テストレポートで終了すること、人間が最終的な品質ゲートであり続けること。

## Roblox固有の市場文脈（オリエンテーション）

Robloxのコンセプトワークの基礎となるプラットフォーム知識（保証ではなく、あくまで目安）:

- **収益性の高いジャンル:** Simulator, RPG, Tycoon, Horror, Obby — スケーリングと労力が大きく異なります。
- **ニッチ（高リスク、低競争）:** リアル戦略/RTS-lite、高品質なスポーツゲーム、cozy/生活シミュレーション、協力パズル/脱出、オートバトラー。
- **マネタイズの黄金律:** (1) LiveOps は必須（2〜4週間ごとのアップデート）、(2) マネタイズはゲームプレイを*支援*すべきでありブロックすべきではない、(3) ソーシャルデザイン（トレード、協力）はインフラである、(4) モバイルファースト（50%以上がスマホでプレイ）、(5) コンテンツクリエイターへの適性（YouTube/TikTok）はマーケティングである。

> 最新かつ信頼性の高い市場数値については、推測するのではなく調査を行ってください — 上記のポイントは安定したヒューリスティックであり、リアルタイムデータではありません。

## 参考文献

- 関連スキル: `/rojo`, `/rbx-studio`; メタスキル `/rbx-dev`（アーキテクチャパターン、プロジェクト構造、Luauの知見）。
- リファレンスパイプライン（利用可能な場合）: `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`, `IDEAS.md`, 市場分析)。

## 変更履歴

### 1.0.0 (2026-06-17)
- 初版。.ROBLOX/AGENT_ROLES.md および GUIDE.md から抽出された汎用的なロール/ワークフローフレームワーク。ユーザーニュートラル（プロジェクト固有のポートフォリオなし）。