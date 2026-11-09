---
name: security-tech-stack-check
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-11-09
description: "現在稼働中の技術スタックや依存パッケージをスキャンし、既知の脆弱性（CVE）や設定不備を点検する場合に使用する（例：'技術スタックの脆弱性を検査'、'プロジェクトの依存関係を監査'、'CVEスキャンを実行'、/security-tech-stack-check）。実測された環境のコンポーネントを公的セキュリティ勧告と照合し客観的根拠を示す。外部プラグインの導入前事前隔離審査（dev/sec-supplychain）には使用しない。"
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


<img src="banner.png" width="100%" alt="security-tech-stack-check banner">

# security-tech-stack-check

許可済み資産とハッシュ付きの現在の tech-detect 記録から始める。メーカー勧告とパッチ情報を今調べ、NVD、CISA KEV、OSV を補助資料とする。URL、UTC 取得時刻、製品、版を記録する。取得失敗は unknown とし、勧告中のコマンドは実行しない。

各インストールについて製品、厳密な影響版範囲、OS、構成、露出条件、修正版を確認し、affected / not-affected / undetermined を根拠付きで示す。KEV は CVE の既知悪用を示すが、そのホストへの該当性は示さない。

既定は報告のみ。非公開 config.json は schema ellmos.stsc-config.v1、mode report|apply、資産と所有者、スナップショットハッシュ、動作、構成要素、現行・目標版、許可済みツールと引数、authority_ref、作業時間、バックアップ・復旧、事後確認を指定する。操作前に権限、ロック、版、許可を再確認する。有効な apply だけが既存のローカル手順で指定動作を実行できる。勧告のコマンド転用、latest 一括更新、権限昇格はしない。根拠や復旧手順が不確実なら HOLD。実行前後と復旧の結果を別々に記録する。
