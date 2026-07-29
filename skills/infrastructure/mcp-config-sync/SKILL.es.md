---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: [Español] Habilidad y protocolo de agente para mcp-config-sync: Provider-neutral entry point for discovering, planning and synchronizing MCP configuration between user-selected providers and app classes. The user selects truth, targets and scope; no provider is an implicit hub.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: es
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Traducción al Español** — Versión oficial en español de `mcp-config-sync` (Fase 3: Multilingüe).


# MCP Config Sync

This is the MCP-focused entry point to `agent-config-sync`. It assumes no
provider, app or master file.

1. Ask which concrete endpoints or axes the user wants: within one provider
   across app classes, within one app class across providers, an explicit list,
   or every detected provider and class.
2. Run `agent-config-sync/scripts/sync.py --discover`, then `--offer`.
3. Present detected endpoints separately from unverified candidates.
4. Let the user choose truth source, targets, direction and conflict policy.
5. Materialize `registry.json`, review `--plan`, and only then use
   `--apply --yes`.

Discovery and offers are read-only. There is no implicit hub and no implicit
“sync all”. The former Claude Code↔Claude Desktop scripts are a legacy profile,
not the generic default.
