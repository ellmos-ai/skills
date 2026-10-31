---
name: sec-triage
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "既存の所見（スキャナーのレポート、SARIF、GitHub code scanning、Dependabot、チケット）を ellmos セキュリティファミリーの findings.json 形式に変換し、id で重複を除き、リポジトリのセキュリティポリシー（SECURITY.md）に照らして重大度と優先度を設定し、チケットを紐付ける。静的な評価のみ。「このスキャン結果を分類して」「Dependabot のアラートに優先順位を付けて」「code scanning の所見を取り込んで」「セキュリティ所見のバックログを整理して」といった場面で使う。新しい脆弱性の発見は sec-scan、反証や再現は sec-validate、レポートは sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, triage, sarif, dependabot, code-scanning, prioritisation]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-triage

ellmos セキュリティファミリーのフェーズ 4。コントラクト：`sec-scan/references/contract.md`（ファイル 1、ライフサイクル 2、重大度 3、id 4、ルール 6）。バリデーター：`sec-scan/scripts/secfind.py`。**静的な証拠のみ：** 新たな発見（`sec-scan`）も、実行時の検証（`sec-validate`）も行わない。

## 入力

既存の所見：SARIF ファイルまたはスキャナーのレポート、GitHub code scanning と Dependabot（`gh` またはウェブ UI からエクスポートする。外部送信に注意）、チケット、監査リスト。`findings.json` が既にあればそれを継続し、なければ作成する（スキャンディレクトリはコントラクト 1 に従う）。プリフライトは `sec-scan` の手順 2 と同じ（所有権、ロック確認、フェイルクローズド）。

## 手順

1. **マッピング：** 元の所見 1 件につき 1 エントリー。`rule` はドット区切りの小文字に正規化する（`py.sql-injection`。元のルール識別子と出典は `description` に入れる）。`cwe` は出典のタグから、`location` はアラートから、`severity` は当初は出典が示すとおりに、`status: candidate` とする。
2. **証拠を確保する：** アラートのコード抜粋を使う。なければ、示されたファイルの該当箇所を読んで引用する。証拠が得られない場合（ファイルがない、行がずれた、コードのないアラート）は、でっち上げの証拠でその所見を取り込んでは**ならない**。取り込まなかったものとして、理由とともに `coverage.limits` に列挙する。シークレットの値はマスクする（コントラクト 4）。依存関係のアラートの場合：`rule` は例えば `dep.vulnerable-dependency`、`location` = manifest/lockfile の行、`evidence` = その行。アドバイザリ id と影響を受けるバージョンは `description` に書く。
3. **重複排除：** `python sec-scan/scripts/secfind.py id RULE PATH -` で `id` を作る。同じ `id`（複数の出典にまたがるものも含む）は 1 件の所見に統合し、出典を `description` に列挙する。重大度が異なる場合は高い方を採用して注記する。
4. **ポリシーを読む：** `SECURITY.md`（重大度の定義、期限、サポート対象バージョン、報告窓口）と、プロジェクト上の決定事項。なければコントラクト 3 を適用し、結果にその旨を記す。
5. **重大度と優先度を設定する：** 重大度をポリシーと照らし、理由を付けて調整する。優先度は重大度、露出、期限から導き、`priority` に設定する（`P0`-`P4`、P0 が最も緊急。ポリシーの区分をここに対応付ける）。理由は `description` に書く。
6. **ステータス：** バリデーターの定めにより、`triaged` には `validatedBy.verdict == confirmed` が必要。検証済み（`validated`）の所見は `triaged` になる。取り込んだだけで未検証の所見は、重大度・優先度を設定した上で `candidate` のままとし、`sec-validate` に回す。除外するのは、ポリシーが明示的に対象とする場合（例：サポート対象外のバージョン）に限る。`rejected` とし `rejectedReason` を付ける。
7. **チケット：** ユーザーまたはポリシーが求める場合のみ。`ticket_writer.py`（id を手で選ばない）、または GitHub の issue／ドラフトのアドバイザリを使う。公開リポジトリの脆弱性は、公開 issue ではなく**非公開**のアドバイザリのドラフトとする。参照は `ticket` に記録する。チケットにシークレットの値を入れない（コントラクト 6.4）。
8. **カバレッジ：** 純粋な取り込みは何もスキャンしない。`scanned: []`、`notScanned` に「import without own scan, repo not read」のエントリー（したがって `complete: false`）、`limits` に出典、取り込みの状態、取り込まなかった所見を書く。`provider.name` = 出典（例：`github-code-scanning`）、`model` = `n/a`、`engine` = 出典のツール。
9. **確認：** `python sec-scan/scripts/secfind.py validate findings.json coverage.json` を実行し、終了コードを示す。その後、候補は `sec-validate`、レポートは `sec-report` へ。

## 変更履歴

### 0.1.0 (2026-10-31)

- 初版：取り込み、id による重複排除、ポリシーに基づくトリアージ。
