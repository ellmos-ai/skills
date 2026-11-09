---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-11-09
description: "当在多个 AI 智能体工具之间发现、规划并同步模型上下文协议（MCP）服务端配置时使用（例如 '同步 MCP 服务端'、'核对 MCP 配置'、'迁移 MCP 服务'、/mcp-config-sync）。探查已安装的 MCP 实例并以中立方式对齐配置，无强制中心节点。切勿用于同时同步全量技能与规则体系（使用 agent-config-sync）。"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: zh
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **中文** — `mcp-config-sync` 官方中文版本。


# MCP Config Sync (中文)

这是 `agent-config-sync` 中专注于 MCP 的入口点。它不预设任何
提供商、应用或主文件。

1. 询问用户需要哪些具体端点或维度：单个提供商内部
   跨应用类、单个应用类内部跨提供商、显式列表，
   或者所有检测到的提供商和类。
2. 运行 `agent-config-sync/scripts/sync.py --discover`，然后运行 `--offer`。
3. 将检测到的端点与未验证的候选项分开展示。
4. 让用户选择事实来源、目标、方向和冲突策略。
5. 实例化 `registry.json`，审查 `--plan`，只有在此之后才使用
   `--apply --yes`。

发现和提供都是只读的。没有隐式中心，也没有隐式的
“全量同步”。以往的 Claude Code↔Claude Desktop 脚本是遗留配置，
而不是通用默认选项。