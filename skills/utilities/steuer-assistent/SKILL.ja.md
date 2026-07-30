---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: スタンドアロンモジュール steuer-assistent を指します：ドイツの従業員の所得関連経費（Werbungskosten）のためのローカルかつオフラインファーストの領収書ワークシート —— 記録、セント単位の集計、プライベートZIPエクスポート。Werbungskosten の領収書を構造化された方法で準備する必要がある場合にこの skill を使用してください —— 明確な境界線付き：税務相談ではなく、控除対象の確認も行わず、確定申告書の作成や提出も行いません（それらは ELSTER または認定ソフトウェア経由で行われます）。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: ja
status: active
---

<img src="banner.png" width="100%" alt="steuer-assistent banner">

> **日本語** — `steuer-assistent` の公式日本語版。


# steuer-assistent -- Pointer Skill (日本語)

この skill は、独立したパブリックモジュールリポジトリ
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
（MITライセンス、公開）への**軽量なポインター（wrapper）**です。実際の skill はそこに存在し、このリポジトリはそこへのリンクとインストール手順の文書化のみを行っています。

注: `steuer-assistent` はドイツの税法（従業員の所得関連経費、「Werbungskosten」）を対象としており、その CLI およびドキュメントは設計上ドイツ語となっています。

## モジュールの機能

`steuer-assistent` は、ドイツの従業員の所得関連経費（Werbungskosten）の自己分類された領収書のための小型でオフラインファーストな Python モジュールです：

- 領収書の記録（カテゴリ、金額、日付、オプションのメモ）。
- 記録された経費を年ごとにセント単位まで集計。
- プライベートで非公式な ZIP ワークシートのエクスポート（CSV + 要約 + 非公式の注記、領収書ファイル自体は含みません）。
- ローカルストレージ（デフォルトは `%USERPROFILE%\.steuer-assistent\steuer.db`）、ネットワークアクセスなし、クラウドアップロードなし、他のデータベースへのアクセスなし。

## 境界（重要）

- **税務相談ではありません。** モジュールは個別項目の控除可能性を評価せず、確定申告書の作成や提出も行いません。
- 公式な電子提出は、本モジュール経由ではなく、ELSTER または認定ソフトウェアを通じてのみ行われます。
- 範囲：従業員の所得関連経費のためのプライベートワークシート。事業/自営業の経費追跡は含まれません。

## インストール（汎用、ローカルパスなし）

1. モジュールのクローン:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <clone-path>
   ```
2. インストールと検証:
   ```bash
   cd <clone-path>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. `<clone-path>/SKILL.md` をご自身の skill 環境（例: `~/.claude/skills/steuer-assistent/`）に導入します。バージョン管理された skill 環境に実際のローカルパスやホスト名をコミットしないでください。
4. 必要に応じて `STEUER_ASSISTENT_DB=<path>` または `--store <path>` でストレージパスを調整します。デフォルトはユーザーのホームディレクトリです。
5. CLI コマンド、プライバシー、および境界については、モジュールリポジトリの README を参照してください。

## この pointer skill の起源

この wrapper は 2026-07-23 に `ellmos-ai/skills` リポジトリの展示エントリとして追加されました。**コードの重複はありません** —— メンテナンスとバージョン管理は `ellmos-ai/steuer-assistent` モジュールリポジトリでのみ行われます。

## 変更履歴

### 0.1.0 (2026-07-23)
- `ellmos-ai/steuer-assistent` の初期 pointer skill。