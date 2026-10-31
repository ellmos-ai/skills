---
name: sec-verify-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "セキュリティパッチが脆弱性を本当に塞いでいるかを独立して確認する（パッチ適用後の状態で source-to-sink の経路をたどり直し、ネガティブテストと回帰テストを行う）。回帰リスクと、自動マージが妥当かどうか（critical/high では既定で不可）を評価する。読み取り専用のレビューで、何も適用しない。トリガー：「パッチで穴は塞がったか」「パッチをレビューして」「修正を検証して」、status が fixed の所見。パッチの作成（sec-fix）や一般的なコードレビューには使わない。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, review, verification, regression]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-verify-fix - パッチは穴を塞いだか

「verify-fix」フェーズ。コントラクト：`sec-scan/references/contract.md`（ライフサイクル §2、ルール 7 は §6）。status が `fixed` で `fix.patchFile` がある所見が前提となる。

## まず独立性

レビュアーはパッチの作者**ではない**（ルール 7）：別のプロバイダー（Claude <-> Codex）が望ましい。それが無理なら、新しいコンテキストを持つ独立した最上位クラスのサブエージェントを使い、所見、パッチ、コードだけを渡す。作者の推論は渡さない。どうしても自分で確認するしかない場合は、結果にそう明記する。その場合 `verifiedBy` は空のままで、status は `fixed` のまま。

## 手順

1. **スクラッチコピーにパッチを適用する**（元のリポジトリには決して適用しない）。`sec-fix` と同様にロックを確認する（ルール 2）。パッチがきれいに適用できないなら、それ自体が結果である。
2. **経路をたどり直す：** `evidence` にある元の source-to-sink の経路を、パッチ適用後の状態で一行ずつ追う。sink はまだ到達可能か。パッチが覆っていない並行する経路（他の呼び出し元、入力のバリエーション、別のエンコーディング）はないか。
3. **ネガティブテスト：** 以前なら所見を引き起こしたはずの、最小限で兵器化されていない入力が、今は拒否または無害化されなければならない。スクラッチコピーのみ、自分のコードのみ（ルール 1）。テストを意味のある形で実行できない場合は「not tested」と報告する。
4. **回帰テスト：** パッチ前後のプロジェクトのテスト。正当な入力が引き続き動作すること。失敗したテストや実行されなかったテストを明記する。
5. **回帰リスクを評価する：** 影響を受ける実行時の経路と呼び出し元、変更された契約（シグネチャ、フォーマット、エラー時の挙動）、その箇所のテストカバレッジ、可逆性（コードのみのパッチ vs. データ移行／設定変更）。低／中／高の水準を、理由とともに示す。
6. **自動マージして良いか。** 可／不可を理由とともに示す。**critical/high では既定で不可。** 可とするのは、経路が塞がれ、ネガティブテストと回帰テストが緑で、リスクが低く、ロールバックが簡単な場合のみ。レビュアーが単独で決定することは決してない。リポジトリのマージルールが優先する。

## 結果

- **塞がっているか：** はい／部分的に／いいえ。開いたままの具体的な箇所を示す。「いいえ」「部分的に」の場合、status は `fixed` のままで、作業は `sec-fix` に戻る。その所見は破棄されない。
- **「はい」の場合：** `status: verified`、`fix.verifiedBy: "<provider>/<model>"`、そして `python scripts/secfind.py validate findings.json coverage.json`（スクリプトは `sec-scan` にある）。根拠、リスク水準、マージの推奨はユーザーへのレポートに書く。コントラクトにはそれらのフィールドがないので、作らない。
- 何も適用せず、コミットもプッシュもしない（ルール 3）。

## 変更履歴

### 0.1.0 (2026-10-31)
- 初版。
