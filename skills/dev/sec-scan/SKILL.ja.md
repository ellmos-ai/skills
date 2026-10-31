---
name: sec-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "自分が所有するリポジトリに対して、プロバイダー中立のセキュリティスキャンを行う。脅威モデル、信頼境界ごとの分割、パッケージ単位の的を絞ったレビュー（インジェクション、認証・認可、シークレット、暗号、デシリアライズ、パス、SSRF、設定、脆弱な依存関係の利用）を行い、根拠付きの候補を findings.json に、正直なカバレッジを coverage.json に記録する。モードは standard と deep。「セキュリティスキャン」「このリポジトリの脆弱性を調べて」「セキュリティレビュー」「フルスキャン」「スキャナーの結果を ellmos 形式に取り込む」といった場面で使う。/claude-security と codex-security のアダプターを含む。変更・PR のみの場合は sec-diff-scan、候補の反証は sec-validate、外部レポートの取り込みは sec-triage、レポート作成は sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, vulnerabilities, sast, source-to-sink, cwe]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-scan

ellmos セキュリティファミリーの中核。共通コントラクト（フェーズ、ファイル、ライフサイクル、重大度、ルール、アダプター）は `references/contract.md` に、スキーマは `schemas/` に、バリデーターは `scripts/secfind.py` + `scripts/seclib.py`（標準ライブラリのみ）にある。このスキルはコントラクトを参照するだけで、内容は繰り返さない。隣接スキル：`sec-threat-model`、`sec-diff-scan`、`sec-validate`、`sec-triage`、`sec-report`。

## モード

- **standard：** 1 回のパス、1 つのモデル、1 つのセッション。
- **deep：** 互いに独立した複数のパス（パッケージの順序、分割、モデルを変える）を行い、`id` でマージする。コスト警告を出し、ユーザーの確認を得てからのみ実行する（コントラクト 6.5）。

## 手順

1. **対象とスコープ：** リポジトリ、ref（コミット SHA または `working-tree`）、除外パス。`scanId` を割り当てる。スキャンディレクトリの名前は `sec-scan-<scanId>/`（コントラクト 1）で、**リポジトリの外**にあるベースフォルダーの下に置き、プリフライトの後でのみ作成する。
2. **プリフライト：**
   - 自分のコード、または許可されたコードか。そうでなければ中止する（コントラクト 6.1）。
   - リポジトリと、スキャンディレクトリのベースフォルダーについてロックを確認する：`python <lock_scan.py> --check-dir '<path>' --json`。終了コードはすぐに控える。0 = 空き、1 = ロック中、それ以外（クラッシュ、読み取れない出力）= 不明 = 停止（コントラクト 6.2）。インタープリターは明示的に呼び出し、スクリプトを「開く」ことは決してしない。このホストに `lock_scan.py` が存在しない場合（ellmos のロックシステムがない場合）は、代わりにリポジトリとその親フォルダーで `LOCK*.txt` を探す：なし = 空き（レポートに注記する）、1 件以上 = 停止。
   - **外部送信を明示する：** コードがプロバイダー（ホスト型レビュー層、サードパーティのモデル）に送られるか。プライベートリポジトリはローカルセッションの中に留める（コントラクト 6.6）。**コストを明示し**、`deep` では確認を待つ（6.5）。
3. **脅威モデル：** `threatmodel.md` は存在し、最新か。そうでなければ `sec-threat-model` を実行する。
4. **パッケージの構成：** モデルの信頼境界とエントリーポイントに従ってリポジトリを分割し、パッケージごとにファイルと調査上の問いを定める。非常に大きなパッケージは、表面的に読むのではなく分割する。
5. **各パッケージをレビューする**（source-to-sink：source -> 変換 -> sink。経路上の対策も読む）：
   インジェクション（SQL、シェル、テンプレート、LDAP/NoSQL）、認証・認可とテナント分離、コード内のシークレット、暗号（アルゴリズム、乱数、鍵の扱い）、安全でないデシリアライズ、パス・ファイルアクセス（トラバーサル、アップロード、シンボリックリンク）、SSRF とオープンリダイレクト、安全でない設定（デバッグ、CORS、デフォルト値、権限）、既知の脆弱な依存関係の利用（コード内のパターン。アドバイザリの照合は `security-tech-stack-check`）。経路が裏付けない所見は記録しない。根拠のない疑いは `findings` ではなく `coverage.limits` に書く。
6. **候補を記録する：** `rule` はドット区切りの小文字（`py.sql-injection`）、該当する場合は `cwe`、`severity` と `confidence` はコントラクト 3 に従い、`status: candidate`、`location`、`evidence` は引用したコード／トレース。**シークレットの値はマスクする**（コントラクト 4）。`id` は必ず `python scripts/secfind.py id RULE PATH -`（スニペットは stdin）で生成し、手で付けない。
7. **カバレッジを正直に保つ：** `scanned` は深さ `read` / `skimmed` / `pattern-only` 付き、`notScanned` は理由付き（生成物、ベンダリング、大きすぎる、バイナリ、到達不能）、`limits` には手法上の限界を書く。`complete: true` にできるのは `notScanned` が空のときだけ（コントラクト 5）。`unknown` は「安全」ではない。
8. **検証：** `python scripts/secfind.py validate findings.json coverage.json` を実行し、終了コード（0/1）と出力を示す。エラーがあれば直して再実行する。
9. **まとめ：** 重大度ごとの候補数、カバレッジの状態、次のステップ（`sec-validate`、続いて `sec-triage`、`sec-report`）。部分的なスキャンは部分的として報告する（コントラクト 6.9）。

## deep

分割方法を変えた少なくとも 2 回のパスを行い、それぞれが独自の候補リストを持つ。`id` でマージする：同じ `id` は統合し（証拠を追加。重大度が異なる場合は高い方を採用し、差異を `description` に明記）、新しい `id` は追加する。カバレッジ = 読んだパスの和集合。`provider.model` には関与したすべてのモデルを列挙する。

## アダプター

既存のプロバイダー製スキャナーがスキャン部分を引き受けることができる（コントラクト 7）：**Claude** `/claude-security`、**Codex** `codex-security`。Gemini と Kimi には存在しないため、上記の手順に従う。

1. プリフライト（手順 2）の後にスキャナーを実行し、その出力ファイルを読んで `findings.json` / `coverage.json` にフィールド単位でマッピングする。スキャナーのファイルやフィールドはここでは前提にしない。マッピングは実際の出力を読みながら作り、`coverage.limits` に記録する。
2. **すべての所見は `candidate` から始まる。** スキャナーが確認済みとして報告していても同じ。アダプターが検証を省くことは決してない。
3. スキャン後に `provider.name` / `provider.model` を設定し、`provider.engine` = スキャナー名とする。
4. カバレッジはスキャンレポートから取る。得られない場合は `complete: false` とし、スキャナーのカバレッジが不明であることを `notScanned` または `limits` に記す。
5. 他の実行の所見と一致するよう、`secfind.py id` で `id` を作り直す。その後、手順 8 へ。

## 制限

パッチ適用、コミット、ネットワークスキャンは行わない（コントラクト 6.1、6.3）。実行時のエクスプロイトは行わない。再現は `sec-validate` の役割。

## 変更履歴

### 0.1.0 (2026-10-31)

- 初版：standard/deep モード、プリフライト、パッケージ、アダプター。
