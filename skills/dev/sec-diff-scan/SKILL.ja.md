---
name: sec-diff-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "リポジトリ全体ではなく変更を対象にしたセキュリティスキャン。PR、コミット、ブランチの差分、またはワーキングツリーのパッチが対象。変更された行を呼び出し元・呼び出し先とあわせてレビューし、既知パターンの回帰を探して、候補を findings.json に、diff とコンテキストのファイルを列挙した coverage.json とともに書き出す。「この PR のセキュリティレビュー」「この diff に脆弱性がないか確認」「マージ前に見てほしい」「この変更で穴が開いていないか」といった場面で使う。リポジトリ全体のスキャンは sec-scan、候補の反証は sec-validate、レポートは sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, diff, pull-request, regression, review]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-diff-scan banner">

# sec-diff-scan

`sec-scan` と同様だが、スコープは**変更**である。コントラクト、ファイル形式、ルール：`sec-scan/references/contract.md`。スキーマとバリデーターは `sec-scan/schemas/` と `sec-scan/scripts/` にある。プリフライト（所有権、ロック確認、外部送信、コスト）、候補の作成（`secfind.py id` による `id`、シークレットのマスク）、検証は `sec-scan` > 手順 と同じ。ここでは相違点のみを挙げる。

## スコープの確定

次のいずれかの出典を使い、必ず正確な比較基準点を添える：

- PR：その PR の base と head のコミット（ローカルでは `git diff <base>...<head>`、または `gh` で PR を取得する。外部送信に注意）。
- コミットまたはブランチ：`git diff <base>...<branch>`。
- ワーキングツリー：`git diff` と `git diff --staged`、加えて未追跡ファイル。

`findings.json` > `target.ref` = head コミット（または `working-tree`）、`target.scope` = diff のファイル。diff が空なら中止し、その旨を伝える。

## 手順（sec-scan の手順 3-5 の代わり）

1. **diff を読む。** ハンクだけでなく、変更された各ファイルを該当する関数の文脈で読む。
2. **コンテキストを取り込む：** 変更された関数の呼び出し元（誰が入力を渡すか）、呼び出し先（データはどこへ流れるか）、前提を記している設定やテスト。`threatmodel.md` があれば使う。なければ、触れられた信頼境界だけを簡潔に自分で特定する（完全なモデルは不要。それは `sec-threat-model` の役割）。
3. **変更に対するレビューの問い：**
   - 新しいエントリーポイントや新しい sink（シェル、SQL、ファイルシステム、デシリアライズ、HTTP クライアント）はないか。
   - チェックが削除・弱体化・迂回されていないか（認証デコレーター、バリデーション、エスケープ、権限チェック）。
   - 既知パターンの回帰：以前の所見やリポジトリ内の他の箇所と同じ種類のバグか（既存の `findings.json` があれば、その `rule` の値を参照する）。
   - manifest/lockfile での新しい依存関係やバージョン変更。変更に含まれるシークレットやトークン。設定のさらなる緩和（CORS、デバッグ、権限）。
4. **経路が変更箇所または触れられた箇所に実際に到達する場合にのみ、所見を報告する。** 変更とは無関係に、コンテキスト内に以前から存在する欠陥は、コントラクト 3 に従った実際の重大度で記録し、`description` に「既存であり、この変更で持ち込まれたものではない」と注記する（`info` に格下げしない）。未検証の場合は `coverage.limits` にのみ記す。それらは diff の対象ではない。

## カバレッジ

`coverage.json`：`scanned` = diff のファイル（深さは通常 `read`）**および**追加で読んだコンテキストファイル、`notScanned` = 読まなかった diff のファイル（バイナリ、生成物、大きすぎる）に理由を添える。`limits` には「変更のみ、リポジトリの残りはスキャンしていない」と書く。`complete` はコントラクト 5 に従う。diff スキャンで何も出なかったことは、リポジトリについて何も保証しない。

## スコープの制限

リポジトリ全体のスキャン（`sec-scan`）、実行時の確認（`sec-validate`）、修正は行わない。出力：`findings.json`、`coverage.json`、`secfind.py validate` の終了コード。

## 変更履歴

### 0.1.0 (2026-10-31)

- 初版：変更スコープ、コンテキストの取り込み、回帰の問い。
