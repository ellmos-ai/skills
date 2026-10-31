---
name: sec-report
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "スクリプト render_report.py により、findings.json と coverage.json からセキュリティレポート report.md（重大度別にグループ化、ギャップを示すカバレッジの節、却下された所見は別掲、飾らないサマリー）と findings.sarif（SARIF 2.1.0）を作成する。「セキュリティレポートを書いて」「スキャン結果をまとめて」「SARIF をエクスポートして」「code scanning 用のレポート」といった場面で使う。データが不正なら中止し、部分的なスキャンは部分的として報告する。新しい所見は sec-scan / sec-diff-scan、検証は sec-validate、分類は sec-triage。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, report, sarif, coverage, findings]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-report

ellmos セキュリティファミリーの最終フェーズ。コントラクト：`sec-scan/references/contract.md`（ファイル 1、重大度 3、カバレッジ 5、ルール 6）。スクリプトは、隣接するフォルダー `sec-scan/scripts` から `seclib` をインポートする（リポジトリでは `skills/dev/`、フラットなデプロイでは `~/.claude/skills/`。2 つのフォルダーは並べて置く必要がある）。標準ライブラリのみ。

## 使い方

```
python scripts/render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]
```

インタープリターは明示的に呼び出す。`OUTDIR` はスキャンディレクトリ。先に `sec-scan` の手順 2 と同様にロックを確認する（フェイルクローズド）。結果：`OUTDIR/report.md` と `OUTDIR/findings.sarif`。終了コード：0 = 書き込み済み、1 = 入力が読めないか不正（**何も書き込まれない**）、2 = 使い方の誤り。終了コードと出力を示す。レポートの既定の言語はドイツ語で、英語にするには `--lang en` を使う。

## 動作

- **最初に検証する**（`seclib.validate_findings`）。エラーを列挙し、壊れたデータからはレポートを作らない。先に原因（`sec-scan`、`sec-validate`）を直してから、再度レンダリングする。
- **report.md：** ヘッダー（対象、ref、スキャナー）· サマリー · 警告 · 重大度別（critical から info まで）の所見（位置、確信度、ステータス、検証者、証拠、説明、影響、推奨対応、チケットを含む）· **却下された所見は理由とともに別掲** · カバレッジ（スキャン済みは深さ付き、未スキャンは理由付き、制限）。
- **誠実さ（コントラクト 5、6.9）：** `complete: false` は最上部に「PARTIAL SCAN」として表示される。所見がなく、かつカバレッジが不完全な場合は「NOT a clean result」と書かれる。「カバレッジが完全で所見なし」の場合に限り、クリーンな結果のように読める。警告（例：検出者と検証者が同じプロバイダー）はレポートに表示される。
- **findings.sarif：** `seclib.to_sarif` による SARIF 2.1.0。却下された所見は `suppressions` としてログに残る。code scanning のアップロードにそのまま使える。アップロードは外部への公開にあたるため、ユーザーの指示が必要。

## 引き渡す前に

レポートを読み返す：シークレットの値がないこと（バリデーターが捉えるのは一般的なパターンのみ。コントラクト 6.4）、位置のみであること。チケットシステムやチャットのレポートにも値を入れない。公開リポジトリの脆弱性は、公開 issue ではなく非公開の報告窓口（SECURITY.md）を通す。

## テスト

スキルのフォルダーで `python -m pytest tests -q -p no:cacheprovider` を実行する（レポート、SARIF、部分的なスキャン、バッククォートを含む証拠、出力なしの異常系を対象）。

## 変更履歴

### 0.1.0 (2026-10-31)

- `render_report.py` を備えた初版：検証済みデータから report.md と findings.sarif を生成。
