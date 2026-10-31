---
name: ellmos-security
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "プロバイダー中立の ellmos セキュリティスキルファミリー（sec-*）の入口兼ルーター。脅威モデルからスキャン、検証、トリアージ、修正、確認、追跡、レポートまでの各フェーズを整理し、適切なスキルを案内する。トリガー：「セキュリティレビュー」「このリポジトリの脆弱性を確認して」「どのセキュリティスキルを使うべきか」「PR をセキュリティチェックして」「サードパーティのプラグインを確認して」「SECURITY.md」「開示」。自分では検査を行わない。作業は sec-* の各スキルと、ここではリンクするだけの隣接スキルが担う。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, router, umbrella, vulnerability, appsec]
language: ja
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# ellmos-security - セキュリティファミリーの入口

このファミリーは、自分のコードの脆弱性を調べ、すべての所見を、疑いの段階から、追跡され検証された修正に至るまで運ぶ。すべてのスキルは 1 つのコントラクト（ファイル形式、ライフサイクル、重大度、ルール）を共有する：`sec-scan/references/contract.md`。Claude、Codex、Gemini、Kimi で動作し、特定ベンダーのスキャナーには依存しない。そうしたスキャナーはアダプターとしてのみ接続される（下表）。

## フェーズ

| フェーズ | スキル | いつ |
|---|---|---|
| モデル | `sec-threat-model` | 最初のスキャンの前：資産、信頼境界、エントリーポイント |
| スキャン | `sec-scan` | リポジトリ全体、または特定のパス |
| スキャン（変更） | `sec-diff-scan` | プルリクエスト、コミット範囲、diff |
| 検証 | `sec-validate` | 各 `candidate` を独立して確認または反証する |
| トリアージ | `sec-triage` | ポリシーに照らした重大度と優先度 |
| 修正 | `sec-fix` | 依頼があったときのみ、ファイルとしてのパッチ |
| 確認 | `sec-verify-fix` | パッチは穴を塞いだか、回帰リスク |
| 追跡 | `sec-track` | チケット、issue、またはアドバイザリのドラフト |
| レポート | `sec-report` | `report.md` と `findings.sarif` |

横断的なもの：`sec-policy`（SECURITY.md）、`sec-hardening`（構造的な対策）、`sec-writeup`（開示レポート）、`sec-supplychain`（インストール前のサードパーティコード）。

## 何をしたいか

- リポジトリを調べる -> `sec-scan`（新しいプロジェクトなら先に `sec-threat-model`）
- PR や diff を調べる -> `sec-diff-scan`
- 既存の所見を追う -> `sec-validate` -> `sec-triage` -> `sec-fix` -> `sec-verify-fix` -> `sec-track`
- 結果をレポートにする -> `sec-report`
- リポジトリのルールを定める、またはレビューする -> `sec-policy`
- 繰り返し現れる所見の種類を根本から解決する -> `sec-hardening`
- 欠陥を報告または開示する -> `sec-writeup`
- サードパーティのスキル、プラグイン、MCP サーバー、フックをインストールする -> `sec-supplychain`

## 隣接するスキル（別途保守、ファミリーの一部）

- `security-tech-stack-check` + `tech-detect`：計測した技術スタックに対する依存関係と CVE。
- `protection-shield`：自分のシステムでの緊急の防御と、定期的なログ／スタックのチェック。
- `repo-publish-check`：リポジトリを公開する前の公開ゲート。
- お使いのシステムに存在する場合：ご自身のセキュリティ案内と、個人のアカウント／データ（コードではない）向けのスキル。これらはこの公開ファミリーには含まれない。

## プロバイダーアダプター（コントラクト §7）

| プロバイダー | ネイティブのスキャンツール | 接続方法 | コストに関する注記 |
|---|---|---|---|
| Claude | `/claude-security` プラグイン | それでスキャンし、出力フォルダーを `findings.json`/`coverage.json` にマッピングする | マルチエージェントのプラグインスキャン：先に見積もって警告する（ルール 5）。外部送信に注意（ルール 6） |
| Codex | `codex-security` プラグイン | 同上。そのスキャン出力から | 同上 |
| Gemini、Kimi | なし | `sec-scan` の独自手順 | 実行中のセッションのトークン。`deep` スキャンは先に見積もる |

アダプターが検証を省くことは決してない。マッピングされた所見は `candidate` から始まる。正確なマッピング手順：`sec-scan` のアダプターの節。

## クイックスタート

**リポジトリ全体：** `sec-threat-model`（短く）-> `sec-scan` -> `python scripts/secfind.py validate findings.json coverage.json`（スクリプトは `sec-scan` にある）-> 別のプロバイダーで `sec-validate` -> `sec-triage` -> `sec-report`。

**プルリクエスト：** diff に対して `sec-diff-scan` -> PR 内の所見は直接作者へ。確認されたものは `sec-validate`、その後は上と同じ。`coverage.json` でカバレッジを確認する：diff しか見ていないことは「コードが安全」という意味ではない。

**確認済みの所見 1 件をチケットにする：** `sec-triage`（`SECURITY.md` に照らした重大度）-> 依頼があれば `sec-fix` -> 別のレビュアーによる `sec-verify-fix` -> `sec-track`（プレビュー、確認、`finding.ticket` への書き戻し）。

## 共通ルール（要約。正式にはコントラクト §6）

自分のコードのみ · 書き込む前に必ずロック · コミットではなくパッチ · 出力にシークレットの値を含めない · 大規模な実行の前にコストと外部送信の警告 · 独立した検証 · `coverage.json` のない結果は結果ではない。

## 変更履歴

### 0.1.0 (2026-10-31)
- ルーターの初版。
