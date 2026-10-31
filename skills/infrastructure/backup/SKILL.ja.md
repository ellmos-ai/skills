---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "mac-backupのフェイルクローズドコアを通じて、ファイルを明示的に計画、ミラー、検証、復元、またはアーカイブします。ユーザー自身のホスト間バックアップジョブに使用し、一般的なクラウド同期や付随的なファイルコピーには使用しないでください。"
visibility: public
language: ja
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# バックアップ

インストール済みの`mac-backup` CLIを唯一の転送実装として使用してください。生の`scp`、`rsync`、SSHFS、エクスプローラー操作、またはアドホックな削除でフローを再構築しないでください。

## リクエストのルーティング

- 通常の「バックアップ」リクエストは`mirror`を意味します。ソースは変更されません。
- `archive`はソースのクリーンアップを意味し、独立した破壊的な意図です。「backup」「copy」「free some space」（「バックアップ」「コピー」「空き容量を増やす」）から推測しないでください。
- `restore`は新しい宛先に書き込み、黙って上書きすることはありません。
- 検証済みのジョブJSONが存在しない場合は、ジョブ提案を準備し、`init-target`や転送の前に停止してください。

## 実行

1. ジョブを読み込み、`mac-backup plan <job> --json`を実行します。
2. 返されたソースクラス、ファイル数、バイト数、宛先ボリュームID、暗号化状態、ホストフィンガープリントが、リクエストおよび現在のデバイス証跡と一致することを確認します。
3. ミラーの場合は`mac-backup mirror <job> --json`を実行し、その後`mac-backup verify <job> --json`を実行します。
4. リストアの場合は新しい絶対パスの宛先を使用し、コマンドのマニフェスト結果で復元されたファイルを検証します。
5. アーカイブの場合は`--confirm-delete`を、ユーザーがソースの削除を明示的に要求し、検証済みの計画がまさにそのソースを指定している場合にのみ渡してください。ポリシーによるブロックは正しい結果です。`target_encryption_required`、`source_class_unknown_cleanup_blocked`、`onedrive_dehydrate_not_implemented`、ロック、ID不一致、または欠落したアンカーを決して回避しないでください。

`init-target`は特権的なセットアップであり、通常の実行ではありません。ボリュームIDと暗号化について独立して取得したOSの証跡が必要です。提案されたジョブからコピーした値は証跡になりません。

宛先の検証と実際のリストアテストの両方が合格するまでは、ミラーが完全なバックアップであると決して主張しないでください。秘密情報、実際のジョブファイル、ローカルアンカー、ユーザーのファイル名をチケット、Git、OneDriveに含めないでください。

## 変更履歴

### 1.0.0 (2026-08-24)
- `~/.claude/skills/backup/`デプロイマスターの中立化されたコピーを、分類されたライブラリに追加しました。同期のギャップの原因: スキルはデプロイされていたものの、`skills/<category>/`の下にソースエントリがなく、そのため`skill_sync.py status`はそれを `NUR-ZIEL`（宛先のみ）として報告し、`catalog.py`/`build_public_registry.py`（`skills/`のみをスキャン）はそれを一度も見ませんでした。そのため、デプロイのコピーをどのように編集しても、公開レジストリや`SKILLS-MAP.md`に到達できませんでした。
