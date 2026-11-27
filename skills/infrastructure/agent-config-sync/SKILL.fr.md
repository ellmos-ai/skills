---
name: agent-config-sync
version: 0.3.1
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-11-22
description: "À utiliser lorsque les configurations de serveurs MCP, compétences et fichiers de règles doivent être synchronisés de manière neutre vis-à-vis des fournisseurs sur plusieurs frameworks d'agents (ex. 'synchroniser la config agents', 'aligner les MCP', 'refléter les compétences', /agent-config-sync). Détecte les configurations locales et laisse l'utilisateur choisir direction, cibles et résolution de conflits. Ne PAS utiliser pour un simple alignement de serveurs MCP sans compétences/règles (utiliser mcp-config-sync)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: fr
status: active
visibility: public
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Français** — Version française officielle de la compétence `agent-config-sync`.

# Agent Config Sync — Synchronisation des configurations d'agents

Cette compétence sépare la sélection des points de terminaison, les ressources et la source de vérité. Exécutez :

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

L'utilisateur peut sélectionner une liste explicite de points de terminaison, un fournisseur à travers toutes les classes
d'applications, une classe d'applications à travers tous les fournisseurs, ou l'ensemble des points détectés. La détection
constitue une preuve d'existence, non une autorisation.

La source de vérité peut être un point de terminaison, un fichier unique, un ensemble ordonné de fichiers tel que plusieurs
couches `AGENTS.md`, ou un répertoire de compétences. Aucun nom de fichier ni fournisseur n'est un hub implicite.
Sans source de vérité sélectionnée, les plans restent bloqués.

Examinez `--status` et `--plan` ; n'utilisez `--apply --yes` qu'après approbation explicite.
Les blocs MCP et les répertoires de compétences sont implémentés. Les topologies de fichiers de règles restent
verrouillées en mode fail-closed tant que l'utilisateur n'a pas choisi un adaptateur de fusion ou de redirection.

## Journal des modifications

### 0.3.1 (2026-11-22)
- Mention linguistique corrigée.
