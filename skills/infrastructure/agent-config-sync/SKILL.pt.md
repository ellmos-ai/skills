---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: "Planejador neutro quanto ao provedor para sincronizar a configuração MCP, as skills e os arquivos de regras entre provedores de agentes e classes de aplicativos. Ele descobre opções locais com evidências e permite que o usuário escolha a fonte de verdade, os destinos, a direção e os conflitos."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: pt
status: active
visibility: public
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 53ba3789a0734868d5d243eab03ffe02b5daee779a5ccf68036937081049010c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Português** — Versão Oficial em Português / Documento Oficial em Português.

# Agent Config Sync (Português)

A skill separa a seleção de endpoints, os recursos e a fonte de verdade. Execute:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```


O usuário pode selecionar uma lista explícita de endpoints, um provedor em várias classes de aplicativos, uma classe de aplicativo em vários provedores ou todos os endpoints detectados. A detecção é evidência, não autorização.

A fonte de verdade pode ser um único endpoint, um único arquivo, um conjunto ordenado de arquivos, como múltiplas camadas `AGENTS.md`, ou um diretório de skills. Nenhum nome de arquivo ou provedor funciona como centro implícito. Sem uma fonte de verdade selecionada, os planos permanecem bloqueados.

Revise `--status` e `--plan`; use `--apply --yes` somente após a aprovação.
Os blocos MCP e os diretórios de skills estão implementados. As topologias de arquivos de regras permanecem bloqueadas por padrão (fail-closed) até que o usuário selecione um adaptador de mesclagem/redirecionamento.
