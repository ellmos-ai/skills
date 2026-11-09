---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-11-09
description: "複数のAIエージェント間でMCPサーバー設定、スキル、ルールファイルをベンダー中立に同期・調整する場合に使用する（例：'エージェント設定を同期'、'ツール間でMCP設定を調整'、'エージェント間でスキルをミラーリング'、/agent-config-sync）。ローカル設定を検出してマスターデータや同期方向をユーザーが選択できるようにする。MCP設定単体の同期（mcp-config-sync）には使用しない。"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: ja
status: active
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **日本語** — `agent-config-sync` の公式日本語版。


# Agent Config Sync (日本語)

このスキルは、エンドポイントの選択、リソース、および信頼できる情報源（Truth）を分離します。実行方法：

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

ユーザーは、明示的なエンドポイントリスト、アプリクラスを跨ぐ単一のプロバイダー、プロバイダーを跨ぐ単一のアプリクラス、または検出されたすべてのエンドポイントを選択できます。検出は証拠（evidence）であり、権限付与（authorization）ではありません。

信頼できる情報源（Truth）は、1つのエンドポイント、1つのファイル、複数の `AGENTS.md` レイヤーのような順序付けられたファイル群、またはスキルディレクトリ（skills directory）を指定できます。特定のファイル名やプロバイダーが暗黙的なハブになることはありません。選択された情報源がない場合、計画（plan）はブロックされたままになります。

`--status` と `--plan` を確認し、承認後にのみ `--apply --yes` を使用してください。MCPブロックおよびスキルディレクトリが実装されています。ルールファイルのトポロジは、ユーザーがマージ/リダイレクトアダプターを選択するまでフェイルクローズ（fail-closed）状態を維持します。