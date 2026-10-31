---
name: protection-shield
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "許可された緊急防御と定期的なサーバーログ・構成確認を、証拠と復旧手順に結び付ける。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [defense, incident-response, server, logs, monitoring]
language: ja
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [tech-detect, security-tech-stack-check], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# protection-shield

所有または明示的に許可されたシステム・ネットワーク・サーバーのみを対象とする。変更前に資産、所有者、権限、ロック、影響、復旧を確認する。警報だけで本番変更は許可されない。反撃、他者資産へのアクセス、無許可のサービス走査はしない。

緊急時は UTC 時刻、限定したログ、構成ハッシュを保存し、秘密を伏せ、症状と確認済み侵害を区別する。既存の手順、決定、資産別の非公開動作設定を読む。具体的な許可がある場合だけ既存ツールで指定サービス、ファイアウォール規則、承認済みの認証情報更新、または security-tech-stack-check のパッチを扱う。対象と復旧方法を結び、結果、動作、ログ効果、副作用、復旧を別々に確認する。

定期確認は非公開設定で資産、許可済みログ/API、期間、フィルター、保存期間、tech-detect 記録、予定、連絡先を指定する。既存スケジューラーに接続し、新しい常駐プロセスは作らない。各回で指定範囲のみ読み、重複を除き security-tech-stack-check で最新勧告を確認する。範囲と読取失敗を報告し、実際の予定実行と結果の記録があるまで稼働中としない。

同一サーバーの定期点検では、slot と hostname を変えずに前回と今回の tech-detect 記録を compare する。axis=same-host-time、chronology、双方の収集時刻、範囲と未知版を確認する。名前の変更で検査を回避せず、出典不足は HOLD とする。
