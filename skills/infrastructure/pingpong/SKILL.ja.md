---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "時間的に制限され、セッションに紐づいた無線局を、共同で同期されたフォルダ経由で運用します。ListenSync は依頼や新着情報を体系的にスキャンし、WriteSync は差分と受領確認を送信します。PingPong、Dosentelefon（缶電話）、ListenSync、WriteSync、Sync-Listener（同期リスナー）、Auftragswache（依頼監視）、News-Scan（ニューススキャン）、または Goal-/Loop-Überwachung（Goal/Loop 監視）を扱う場合に使用します。"
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: ja
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

共通の Sync フォルダを介して、2 台以上のシステムを無線局として運用します。プロトコル上の契約はプロバイダーに依存しないように保ち、異なるのは継続用アダプターのみです。

## モードの決定

- ListenSync: ホストごとに、体系的なリスナーをちょうど 1 つ置きます。スキャンを行い、該当する依頼を引き受け、応答がある場合は WriteSync も実行します。
- WriteSync: 作業を行う各アクターは、自身の関連する差分、依頼、新着情報、受領確認を送信してよいです。このモードではリスナーを起動しません。
- モードが指定されていない場合は、ListenSync を使用します。

## 参加の確認（STATE と CALL）

実行契約の前に、2 段階のチェックで、そもそも誰かに連絡が取れるかどうかを判断します。`scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` は、ちょうど 3 つの値で応答します。Exit 0 `call-for-me`（有効化し、エージェントを起動する）、Exit 1 `idle`（自分自身が有効であるため、無効化する）、Exit 3 `check-failed`（読み取り不能、決してアイドル状態として扱わない）。参加には STATE と CALL の両方が必要です。Call を招集した者は、目的を達成した時点でそれを終了させ、そうでなければ失効させます。完全な規則は references/protocol.md にあります。

## 実行契約の設定

1. 既定では 24h を使用します。15m、2h、3d のような相対的な期間や、ISO-8601 の絶対終了時刻も受け付けます。
2. ローカルの開始時刻を測定し、expires_at を日付、時刻、タイムゾーンとともに示します。
3. 15 分から開始します。ユーザーが固定の周期を求めない限り、references/protocol.md の周期を使用します。
4. 目標達成は次のように定義します。終了時刻に到達し、最終的な FileCommander スキャンで裏付けが取れ、それまでに検出された該当する入力がすべて処理されているか、または正確にブロックとして文書化され、State が更新され、自前のスケジューラーが終了していることです。
5. FileCommander による裏付けがない限り、スキャンや目標達成を主張しません。

## プロバイダーアダプターの使用

### Codex

最初のスキャンの前に、完全な実行契約と expires_at を含む永続化された Goal を明示的に作成します。継続ごとに、ちょうど 1 回の完全なスキャンサイクルを処理します。空または成功した単一サイクルの後に Goal を終了させてはいけません。その後、実際に next_scan_at まで待機します。例えば次のようにします。

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

失効時刻に最終サイクルを実行します。達成基準を満たした場合にのみ、Goal を完了としてマークします。

### Claude Code

タスクは /loop <Kadenz> $pingpong として開始します。スキルがすでにスケジュールされた実行から来ている場合は、2 つ目のループを作成しないでください。周期を変更する場合は、自身の Cron ジョブのみを置き換えます。最終サイクルの後にそれを削除します。

## サイクルの実行

references/protocol.md を最後まで読み、そこに記載された、スキャン、処理、State 更新の 1 サイクルをちょうど実行します。Sync フォルダへのアクセスには、毎回 ellmos FileCommander を使用します。シェルの一覧、スケジューラーのエントリ、またはファイル名だけでは、スキャンの裏付けにはなりません。

アイドル時には作業をでっち上げないでください。簡潔に報告します。スキャン時刻、読み取った Freshness ファイル、現在の周期、empty_runs、next_scan_at、expires_at。

## WriteSync の実行

自身のシステムスロット、または明示的にグローバルなチャネルにのみ書き込みます。送信者、受信者、時刻、参照、行動、結果、未解決の論点、希望する周期を明記します。上書きではなくマージします。認証情報は含めません。ロックを尊重します。書き込み後は、FileCommander で正規のファイルを読み戻します。

## 変更履歴

### 1.1.0 (2026-09-13)

- ホスト単位の参加マーク STATE（`agents/registry/<slot>.state.json` 内のフィールド `pingpong`）と、失効つきのアドレス指定された CALL ファイル `call-<von>-to-<an|all>.txt` を追加しました。これに伴い `pingpong_runtime.py` は `state`、`call`、および三値の結果を持つ 2 段階チェック `check` を認識します。旧 `pull-` の名前は経過措置として引き続き読み取られます。T-20260830-425388998 の実装は、2026-09-11 のユーザー判断に基づきます（最小の範囲：STATE、CALL、失効のみ）。

### 1.0.1 (2026-09-09)

- オプションのモジュール v2 ロール契約に従う宣言的なロールメタデータを追加しました。中立なスターターは何も宣言していません。既存のプロトコル同一性と検出パスは維持されます。

### 1.0.0 (2026-08-04)

- Codex の Goal アダプターと Claude のループアダプターを備えた、プロバイダーに依存しない ListenSync/WriteSync 契約。
- FileCommander による裏付け、Freshness ガード、適応的な周期、絶対的な失効条件を追加しました。
