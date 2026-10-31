---
name: security-tech-stack-check
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "実測した構成要素を最新の一次セキュリティ情報と照合し、設定済みで権限のある修正だけを実施する。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, advisories, vulnerabilities, patching, tech-stack]
language: ja
status: active
visibility: public
dependencies: {'tools': ['web'], 'services': [], 'protocols': [tech-detect], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# security-tech-stack-check

許可済み資産とハッシュ付きの現在の tech-detect 記録から始める。メーカー勧告とパッチ情報を今調べ、NVD、CISA KEV、OSV を補助資料とする。URL、UTC 取得時刻、製品、版を記録する。取得失敗は unknown とし、勧告中のコマンドは実行しない。

各インストールについて製品、厳密な影響版範囲、OS、構成、露出条件、修正版を確認し、affected / not-affected / undetermined を根拠付きで示す。KEV は CVE の既知悪用を示すが、そのホストへの該当性は示さない。

既定は報告のみ。非公開 config.json は schema ellmos.stsc-config.v1、mode report|apply、資産と所有者、スナップショットハッシュ、動作、構成要素、現行・目標版、許可済みツールと引数、authority_ref、作業時間、バックアップ・復旧、事後確認を指定する。操作前に権限、ロック、版、許可を再確認する。有効な apply だけが既存のローカル手順で指定動作を実行できる。勧告のコマンド転用、latest 一括更新、権限昇格はしない。根拠や復旧手順が不確実なら HOLD。実行前後と復旧の結果を別々に記録する。
