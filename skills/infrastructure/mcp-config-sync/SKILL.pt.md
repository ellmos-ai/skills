---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: "Ponto de entrada neutro quanto ao provedor para descobrir, planejar e sincronizar a configuração MCP entre provedores e classes de aplicativos selecionados pelo usuário. O usuário seleciona a fonte da verdade, os destinos e o escopo; nenhum provedor é um hub implícito."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: pt
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: f28dce27691f8415486c17dfc3c7b37d7990885d89917c1d8986523de97609e7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **Português** — Versão oficial em português.


# MCP Config Sync (Português)

Este é o ponto de entrada focado em MCP para `agent-config-sync`. Ele não pressupõe
nenhum provedor, aplicativo ou arquivo mestre.

## Fluxo

1. Pergunte quais endpoints ou eixos concretos o usuário deseja: dentro de um provedor
   entre classes de aplicativos, dentro de uma classe de aplicativo entre provedores,
   uma lista explícita, ou todos os provedores e classes detectados.
2. Execute `agent-config-sync/scripts/sync.py --discover` e depois `--offer`.
3. Apresente os endpoints detectados separadamente dos candidatos não verificados.
4. Deixe o usuário escolher a fonte da verdade, os destinos, a direção e a política de conflitos.
5. Materialize `registry.json`, revise `--plan` e só então use
   `--apply --yes`.

A descoberta e as ofertas são somente leitura. Não existe hub implícito nem "sincronizar tudo"
implícito. Os antigos scripts Claude Code↔Claude Desktop são um perfil legado, não o padrão genérico.

## Exemplo de chamada

```
agent-config-sync/scripts/sync.py --discover
agent-config-sync/scripts/sync.py --offer
agent-config-sync/scripts/sync.py --plan
agent-config-sync/scripts/sync.py --apply --yes
```

## Registro de alterações

- v2.0.0 (2026-07-27): Sync tornado neutro quanto ao provedor -- sem arquivo hub/mestre implícito; o usuário escolhe a fonte, os destinos, a direção e a política de conflitos.
- v1.0.1 (2026-06-13): Skill publicada (scripts de sincronização e modelo convertidos para caminhos genéricos, referências anonimizadas, versão em inglês).
