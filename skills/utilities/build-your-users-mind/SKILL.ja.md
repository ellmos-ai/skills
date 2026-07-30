---
name: build-your-users-mind
version: 1.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  公開され、プロバイダーに依存しない build-your-users-mind
  モジュールへのポインターです。明示的に許可されたユーザー自身の対話ログから、
  プライバシーに配慮した実証的な Theory-of-Mind
  選好モデルを構築するための手順を提供します。
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [theory-of-mind, user-model, decision-avatar, feedback, privacy, pointer-skill]
language: ja
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "external"
  origin_path: "SKILL.md, templates/, scripts/, schemas/, TAXONOMY.md"
  origin_version: "1.0.0"
  origin_repo: "https://github.com/ellmos-ai/build-your-users-mind"
  last_sync_from_origin: "2026-07-30"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="build-your-users-mind banner">

# build-your-users-mind — 公開・プロバイダー中立ポインター

このスキルは、公開モジュール
[`ellmos-ai/build-your-users-mind`](https://github.com/ellmos-ai/build-your-users-mind)
への軽量なポインターです。完全な手順、テンプレート、スキーマ、スクリプト、
テスト、ソースアダプターの文書はモジュール側にあります。このカタログでは
コードを複製しません。

## モジュールの機能

運用者の明示的な許可がある場合、エージェントは次を実行できます。

1. 運用者自身の対話ログから、ユーザーが実際に入力したターンだけを抽出する。
2. 永続化の前に機密情報を編集・除去する。
3. 繰り返し現れる選好や意思決定の証拠を縮約し、分類する。
4. 信頼度と出典を持つローカル選好モデルを作成する。
5. 選択したエージェント環境に短い参照を接続する。
6. 後から得られた実際のフィードバックで予測を較正する。

公開モジュールは、任意のユーザーと対応するエージェント環境向けの手順です。
特定の人物のモデルは含みません。

## 安全性とプライバシーの境界

- 対話ログを読む前に運用者の許可が必要です。
- 個人プロファイル、生ログ、証拠コーパス、ローカルパスは非公開にします。
- 予測は不確実な仮説であり、読心、診断、ユーザー本人の発言ではありません。
- 選好予測によってエージェントの権限を拡大してはいけません。
- 外部への作用、不可逆、安全上重要、法務、医療、雇用、金融など重大な行為には
  明示的な確認が必要です。
- エージェントが生成した予測をユーザーに関する一次証拠にしてはいけません。

## インストール

```bash
git clone https://github.com/ellmos-ai/build-your-users-mind.git <clone-path>
```

モジュールの最新の `README.md`、`SKILL.md`、`SOURCE-ADAPTERS.md` と
プライバシー手順に従ってください。生成したユーザープロファイルは公開
リポジトリの外に保管します。実装とバージョンの正本はモジュール
リポジトリです。

## 公開コアと非公開プロファイル

`build-your-users-mind` は公開されたユーザー中立のモジュール名です。
`decision-avatar` はこのカタログの公開ランタイムプロトコルです。特定人物の
アバター、証拠ファイル、ローカルコマンド、個別既定値は非公開の拡張であり、
個人名のスキルとして公開してはいけません。

## 変更履歴

### 1.0.0 (2026-07-30)

- 独立した公開モジュールへの中立的なポインターを追加。
- 公開されていた個人プロファイルを、公開コアと非公開プロファイルの厳格な
  境界に置き換え。
