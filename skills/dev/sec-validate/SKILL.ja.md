---
name: sec-validate
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "findings.json のすべての候補を反証しようと試みる。source-to-sink の経路をたどり、到達可能性と対策を確認し、重大度を較正し、安全な範囲でローカルに再現する。validatedBy（confirmed/refuted/uncertain）と、理由付きの status（validated または rejected）を設定する。「所見を検証して」「誤検知を除いて」「本当に悪用できるのか」「スキャン結果の独立した再確認」といった場面で使う。検証者は検出者とは別のプロバイダーであることが望ましい。新しい問題の発見は sec-scan、外部レポートの分類は sec-triage、レポートは sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, validation, false-positives, exploitability, review]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-validate

ellmos セキュリティファミリーのフェーズ 3。コントラクト：`sec-scan/references/contract.md`（ライフサイクル 2、重大度 3、ルール 6）。バリデーター：`sec-scan/scripts/secfind.py`。姿勢：**確認するのではなく、反証する。** 反証の試みが失敗したときに限り、候補は `validated` とみなされる。

## 入力と独立性

- 入力：スキャンの `findings.json` + `coverage.json`、`status: candidate` の候補（またはユーザーが指定した `id` の選択）。
- **独立した検証者（コントラクト 6.7）：** スキャンの `provider.name` とは別のプロバイダー（Claude <-> Codex）が望ましい。それが無理な場合は、最上位モデルクラスの独立したサブエージェントを使う。このサブエージェントは、事前に検出者の推論を**読まない**。そのことを結果に記録する。複数のプロバイダーやファンアウトを使う場合は、先にコストを見積もってユーザーに警告する（6.5）。コードがサードパーティのプロバイダーに送られる場合は、外部送信を明示する（6.6）。
- プリフライトは `sec-scan` の手順 2 と同じ（所有権、ロック確認、フェイルクローズド）。

## 候補ごとに

1. **改めて読む：** `location` にあるコードを自分で読む。検出者の `evidence` はヒントとしてのみ使う。
2. **経路をたどる：** source -> 変換 -> sink。各ステップに file:line を付ける。連鎖が途切れていれば、それが反証の根拠になる。
3. **到達可能性：** どのルート、呼び出し元、認証がそこにつながるか。デッドコード、テストコード、管理者専用の経路、内部の呼び出し元は、重大度を下げるか反証になる。
4. **対策を探す：** バリデーション、エスケープ、パラメータ化クエリ、フレームワークによる保護、設定、上流でのチェック、権限。他の場所（ミドルウェア、ラッパー）も見る。
5. **攻撃者の前提条件を明記する**（匿名、アカウント、ローカルアクセス、特定の設定）。
6. **安全な場合は再現する：** ローカルのコピーまたはテスト環境のみで、合成データとスタブサービスを使う。例：的を絞った単体テスト、または攻撃用の入力で関数を呼び出す。第三者のシステムや本番環境に対しては**決して**行わない。外向きのネットワークアクセス、実際のシークレット、破壊的な操作も不可。安全に再現できない場合は静的な論証で足り、評決 `uncertain` も認められる。
7. **コントラクト 3 に従って重大度を較正する**（到達可能性 × 影響）。`confidence` をリセットする。変更は `description` に「severity 旧 -> 新：理由」と記録する。
8. **評決を書く：**

| 評決 | `findings.json` での結果 |
|---|---|
| `confirmed` | `status: validated`、`validatedBy: {provider, model, verdict: confirmed}`。経路と再現内容は `description` に。`impact` と `recommendation` を追加する |
| `refuted` | `status: rejected`、`rejectedReason` に具体的な対策または連鎖の途切れ箇所を書く、`validatedBy.verdict: refuted` |
| `uncertain` | `status` は `candidate` のまま、`validatedBy.verdict: uncertain`、`description` に判断のために何が足りないかを書く |

`validatedBy.provider` / `.model` は検出者ではなく**検証者**を指す。検出者と同じプロバイダーの場合は「validated by the same provider」という検証者警告が出る。警告は表示されたままとし、抑制しない。

## 締めくくり

`python sec-scan/scripts/secfind.py validate findings.json coverage.json` を実行し、終了コードを示す。サマリー：評決ごとの件数、重大度の変更、未解決の `uncertain`。続いて `sec-triage`（検証済みの所見）と `sec-report` へ進む。`description` や再現の出力にシークレットの値を含めない（コントラクト 6.4）。パッチ適用もコミットも行わない。

## 変更履歴

### 0.1.0 (2026-10-31)

- 初版：反証手順、評決のマッピング、独立性。
