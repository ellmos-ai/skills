---
name: agents-bridge
version: 3.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-07-04
updated: 2026-08-22
description: プロバイダーおよびユーザーに依存しない、エージェント、CLI、IDE のブートルール用ブリッジ。既知的ブートストラップサーフェスを検出し、ユーザーに順序付けられた1つ以上の真実のソースの選択を求め、ルールを重複させることなく軽量ローダーをレンダリングします。

standalone: true
anthropic_compatible: true
category: infrastructure
tags: [multi-agent, bootstrap, rules, agents-md, provider-neutral]
language: ja
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
---

<img src="banner.png" width="100%" alt="agents-bridge banner">

> **日本語** — `agents-bridge` の公式日本語版。


# AGENTS-BRIDGE (日本語)

このスキルを使用して、エージェントまたは IDE を明示的に選択されたルールファイルに接続します。
どのプロバイダー、ファイル名、ホスト、クラウドディレクトリも暗黙的に正格（canonical）ではありません。

## ワークフローと手順

1. ソースパスおよびターゲットパスを制御するすべてのローカル指示を読み取ります。
2. `python scripts/bridge.py discover` を実行し、必要に応じて `--project` を渡します。
3. 順序付けられた真実のソース（truth sources）とターゲットをユーザーに選択させます。空の選択は書き込みを許可しません。
4. リダイレクトまたは順序付けられたローダーを優先します。ターゲットが参照をロードできない場合にのみ生成されたコピーを使用し、出所（provenance）とドリフトチェックを記録します。
5. 以下でプレビューします:

   ```text
   python scripts/bridge.py render --truth <path> --target-kind generic
   ```

6. プレビューを確認した後にのみ、ターゲットを作成または変更します。
7. ターゲットエージェントが実際に選択されたすべてのソースを読み取ったことを証明します。

`references/agent-conventions.md`、
`references/truth-topologies.md`、および
`references/inventory-contract.md` を参照してください。

`agent-config-sync` は、より広範な構成トポロジを管理します。
`agents-bridge` はブートおよびルールアクセスに限定されています。ランタイムパートナーブリッジおよびスケジューラは別個のコンポーネントです。
