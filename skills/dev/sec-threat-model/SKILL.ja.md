---
name: sec-threat-model
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "実際のソースコードに基づき、自分が所有するリポジトリの脅威モデル（資産、信頼境界、エントリーポイント、データフロー、攻撃者の目的、優先順位付きの調査上の問い）を作成または更新し、threatmodel.md として出力する。「脅威モデル」「攻撃対象領域」「このリポジトリでまず何をレビューすべきか」といった場面、セキュリティスキャンの前、アーキテクチャ変更の後に使う。単独でも、sec-scan のフェーズ 1 としても動作する。脆弱性そのものは見つけず（sec-scan / sec-diff-scan を使う）、依存関係のアドバイザリも確認しない（security-tech-stack-check を使う）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, threat-model, attack-surface, trust-boundaries, review]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-threat-model

ellmos セキュリティファミリー（`sec-threat-model`、`sec-scan`、`sec-diff-scan`、`sec-validate`、`sec-triage`、`sec-report`）のフェーズ 1。共通コントラクト：`sec-scan/references/contract.md`（第 1 節 スキャンディレクトリ、第 6 節 ルール）。ここでは繰り返さない。

## ルール

- 自分のコード、または明示的に許可されたコードのみ（コントラクト 6.1）。第三者のシステムへのネットワークアクセスやポートスキャンは行わない。
- モデルは README の主張ではなく、**実際に読んだソースコード**から作る。そこで主張されているだけのもの、裏付けられないものは `open` として入れ、事実としては扱わない。
- 書き込むのはスキャンディレクトリ（`<tmp>/ellmos-security/<repo>/<scanId>/`）のみで、ソースツリーには決して書かない。書き込む前に、`sec-scan` > プリフライト の記述どおりロックを確認する。

## 手順

1. **スコープを明確にする：** リポジトリ、ref（コミット SHA または `working-tree`）、除外パス。既存の `threatmodel.md` を読む。あれば更新モードに切り替え、変更点だけを引き継いで状態と ref を記す。
2. **構造を読む：** manifest、ビルド・デプロイ用ファイル、設定、ディレクトリツリー。言語とフレームワークはコードから導く。
3. **エントリーポイントを見つける：** HTTP ルート、CLI 引数、キュー／webhook のコンシューマー、ファイル・フォーマットのパーサー、IPC／ソケット、スケジュールされたジョブ、環境変数、プラグイン／スクリプトの読み込み箇所。それぞれについて file:line と呼び出し側の母集団（匿名、認証済み、内部）を記す。
4. **資産を挙げる：** シークレットとトークン、個人データ、ユーザーのファイル、データベース、計算資源、実行権限、評判／サプライチェーン。コード内の場所を示し、値は決して書かない。
5. **信頼境界を引く：** データが信頼度の低い側から高い側へ移る箇所（ネットワーク -> プロセス、ユーザー -> 管理者、テナント -> テナント、プロセス -> OS／シェル／DB、サードパーティのパッケージ -> 自分のコード）。強制手段（認証・認可、バリデーション、サンドボックス）がコードのどこにあるか、または欠けていること。
6. **データフローを描く：** 最も重要な資産とエントリーポイントについて、source -> 変換 -> sink を（テキストまたは Mermaid で、短く）示す。Sink：シェル、SQL、ファイルシステム、デシリアライズ、テンプレート、HTTP クライアント、ログ。
7. **攻撃者の目的を導く：** 境界ごとに、攻撃者が何を望むか（コード実行、データ流出、権限昇格、改ざん、停止）。STRIDE は思考の補助にとどめ、必須の枠組みにはしない。
8. **調査上の問いに優先順位を付ける：** 具体的で確認可能な問い（「ルート X の `user_id` は、検査されないまま `db.py` のクエリに届くか」）を、影響度と到達可能性の積の順に並べる。`sec-scan` がこれらを調査パッケージに変える。

## 出力：`threatmodel.md`

節は次の順序：**状態**（リポジトリ、ref、日付、読んだパス）· **資産** · **信頼境界** · **エントリーポイント**（表：パス、種別、呼び出し元、認証）· **データフロー** · **攻撃者の目的** · **調査上の問い**（番号付き、優先順位順）· **未解決**（前提、未読の領域、ドキュメントとコードの食い違い）。シークレットの値やエクスプロイトの手順は含めない。

## スコープの制限

脆弱性は見つけず、重大度も割り当てない。`open` の項目が多いモデルのほうが、滑らかに見えるモデルより誠実である。

## 変更履歴

### 0.1.0 (2026-10-31)

- セキュリティファミリーのフェーズ 1 としての初版。
