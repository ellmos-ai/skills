---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: ユーザーが選択したプロバイダーとアプリクラス間の MCP 設定を検出、計画、同期するためのプロバイダー中立のエントリーポイント。ユーザーが信頼できる情報源、ターゲット、スコープを選択し、暗黙のハブとなるプロバイダーは存在しません。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: ja
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **日本語** — `mcp-config-sync` の公式日本語版。


# MCP Config Sync (日本語)

これは `agent-config-sync` への MCP に特化したエントリーポイントです。特定の
プロバイダー、アプリ、またはマスターファイルを前提としません。

1. ユーザーが希望する具体的なエンドポイントまたは軸を確認します：単一プロバイダー内での
   アプリクラス間、単一アプリクラス内でのプロバイダー間、明示的なリスト、
   または検出されたすべてのプロバイダーとクラス。
2. `agent-config-sync/scripts/sync.py --discover` を実行し、次に `--offer` を実行します。
3. 検出されたエンドポイントを未検証の候補とは分けて提示します。
4. ユーザーに信頼できる情報源（真実のソース）、ターゲット、方向、および競合ポリシーを選択させます。
5. `registry.json` を具現化し、`--plan` を確認した上でのみ
   `--apply --yes` を使用します。

検出およびオファーは読み取り専用です。暗黙のハブや暗黙の
「すべて同期」は存在しません。以前の Claude Code↔Claude Desktop スクリプトはレガシープロファイルであり、
汎用的なデフォルトではありません。