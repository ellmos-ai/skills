---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-11-09
description: "当在多个智能体提供方之间跨工具中立地规划和同步 MCP 服务端配置、技能库及规则指令文件时使用（例如 '同步智能体配置'、'跨工具对齐 MCP'、'跨智能体镜像技能'、/agent-config-sync）。探查本地配置选项并由用户决策唯一事实来源与冲突解决策略。切勿用于单纯的独立 MCP 配置同步（使用 mcp-config-sync）。"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: zh
status: active
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **中文** — `agent-config-sync` 官方中文版本。


# Agent Config Sync (中文)

该 Skill 将端点选择、资源与事实源解耦。运行方式如下：

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

用户可以选择明确的端点列表、跨应用类的单一提供商、跨提供商的单一应用类，或者所有检测到的端点。检测仅代表存在依据，并不代表获得授权。

事实源（Truth）可以是单个端点、单个文件、有序文件集合（例如多个 `AGENTS.md` 层级）或技能目录（skills directory）。任何文件名或提供商都不是隐式的核心枢纽（hub）。在未选择事实源的情况下，计划将保持阻塞状态。

请检查 `--status` 和 `--plan`；仅在获得批准后使用 `--apply --yes`。目前已实现 MCP 块与技能目录的支持。规则文件拓扑结构将保持故障封闭（fail-closed）状态，直到用户选择合并/重定向适配器。