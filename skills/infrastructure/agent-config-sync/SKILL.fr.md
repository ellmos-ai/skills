---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-11-09
description: "Utiliser pour planifier et synchroniser les configurations de serveurs MCP, les compétences et les règles entre plusieurs agents IA (ex. 'synchroniser la configuration des agents', 'harmoniser les MCPs', 'dupliquer les compétences entre agents', /agent-config-sync). Identifie les paramètres locaux et laisse l'utilisateur choisir la source de vérité. Ne PAS utiliser pour synchroniser uniquement les MCPs (utiliser mcp-config-sync)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: fr
status: active
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Français** — Documentation officielle complète traduite en français pour la compétence `agent-config-sync`.



> **English** — Offizielle English-Version / Documento Oficial en English.


# Agent Config Sync (English)

The skill separates endpoint selection, resources and truth. Run:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

The user can select an explicit endpoint list, one provider across app classes,
one app class across providers, or all detected endpoints. Detection is
evidence, not authorization.

Truth can be one endpoint, one file, an ordered set of files such as multiple
`AGENTS.md` layers, or a skills directory. No filename or provider is the
implicit hub. Without a selected truth source, plans stay blocked.

Review `--status` and `--plan`; only use `--apply --yes` after approval.
MCP blocks and skill directories are implemented. Rule-file topologies remain
fail-closed until the user selects a merge/redirect adapter.