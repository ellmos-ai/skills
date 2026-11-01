---
name: sec-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "明示的な依頼があった場合にのみ、確認済みの所見（status が validated または triaged）に対する最小限のセキュリティパッチを作成する。作業は元のリポジトリではなく、スクラッチコピーまたは worktree で行い、patches/<id>.diff として出力する。適用、コミット、プッシュは行わない。トリガー：「この所見を修正して」「SEC-... のパッチ」「この脆弱性を塞いで」。通常のバグ修正（bugfix-protocol を使う）、パッチの評価（sec-verify-fix）、問題の発見（sec-scan）には使わない。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, fix, remediation]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-fix banner">

# sec-fix - 最小限のセキュリティパッチ

ellmos セキュリティファミリーの「fix」フェーズ。コントラクト：`sec-scan/references/contract.md`（ディレクトリ §1、ライフサイクル §2、ルール §6）。ここでは適用方法のみを記す。

## いつ使うか（と、いつ使わないか）

- **明示的な依頼があったときのみ。** スキャンや検証が自動的に修正を引き起こすことはない。
- **status が `validated` または `triaged` の所見のみ。** `candidate` はまず `sec-validate` を通す。`rejected` はそのまま。
- 通常の、セキュリティ以外のバグ：`bugfix-protocol`。既存のパッチが良いかどうか：`sec-verify-fix`。複数の所見の背後にある構造的な原因：`sec-hardening`。

## 手順

1. **所見とその周辺を読む：** `findings.json`（所見、`evidence`、`recommendation`）、影響を受けるファイル、その箇所の呼び出し元。ある 1 つの呼び出し箇所の症状ではなく、原因を直す。複数の呼び出し元が同じ安全でない関数を使っている場合は、共通の箇所にパッチを当てる。
2. **ロックを確認する（コントラクト §6 ルール 2）：** `lock_scan.py --check-dir <repo> --json`。終了コード 0 = 空き、1 = ロック中、それ以外 = 不明 = 停止。`lock_scan.py` がないホストでは、代わりにリポジトリとその親フォルダーで `LOCK*.txt` を探す（なし = 空き、それ以外は停止）。`LOCK.user.*` には決して触れない。
3. **作業用コピー：** 元のリポジトリの外にあるフォルダーに、スクラッチコピーまたは `git worktree` を作る。元のリポジトリには何も書き込まない。
4. **ベースラインを測る：** パッチを当てる前にプロジェクトのテストを 1 回実行し、結果（緑／赤、件数）を記録する。テストがなければ、その旨を述べる。でっち上げない。
5. **最小限にパッチする：** source-to-sink の経路を塞ぐ最小の変更（バリデーション、パラメータ化、許可リスト、適切な場所でのエスケープ）。リファクタリングもスタイル修正も行わず、必要がなければ新しい依存関係も追加しない。プロジェクトにテストがある場合、その所見に対する回帰テストをパッチに含める。
6. **もう一度測る：** テストを再実行する。失敗したテストや実行されなかったテストを含め、前後の結果を正直に報告する。
7. **パッチを保存する：** 作業用コピーの `git diff` を、スキャンディレクトリの `patches/<id>.diff` に保存する。対象の状態に対して `git apply --check` で確認する（何も変更しない）。
8. **所見を更新する：** `status: fixed`、`fix.patchFile: patches/<id>.diff`。続けて `python scripts/secfind.py validate findings.json coverage.json` を実行する（スクリプトは `sec-scan` にある）。

## 制限

- **適用、コミット、プッシュは行わない（ルール 3）。** それにはユーザーの直接の指示が必要。
- **シークレットに関する所見：** 古い値は必然的に diff の `-` 行に現れる。パッチはスキャンディレクトリ内にローカルで保管し、チケット、チャット、レポートには決して載せない。まずプロバイダー側でシークレットをローテーションする（ルール 4）。未解決：マスクした diff が実用的に適用できるかどうか。でっち上げない。
- パッチの作者はそれをレビューしない：別のレビュアーによる `sec-verify-fix`（ルール 7）。
- 多数の所見を一度に修正する場合はコスト警告を出す（ルール 5）。順番に処理する。

## 変更履歴

### 0.1.0 (2026-10-31)
- 初版。
