---
name: mcp-config-sync
version: 2.0.1
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-11-22
description: "À utiliser lorsque des configurations de serveurs MCP doivent être comparées et synchronisées entre différents outils d'agents (Claude, Gemini, Codex, etc.) (ex. 'synchroniser les MCP', 'comparer la configuration MCP', 'transférer des serveurs MCP', /mcp-config-sync). Détecte les définitions de serveurs existantes et les aligne sous contrôle utilisateur sans hub maître fixe. Ne PAS utiliser si des compétences et règles doivent aussi être reflétées (utiliser agent-config-sync)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: fr
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **Français** — Version française officielle de la compétence `mcp-config-sync`.

# MCP Config Sync — Synchronisation des configurations MCP

Voici le point d'entrée centré sur MCP vers `agent-config-sync`. Il ne présuppose aucun
fournisseur, aucune application et aucun fichier maître.

## Déroulement

1. Demander quels points de terminaison concrets ou quels axes souhaite l'utilisateur : au sein d'un fournisseur
   à travers les classes d'applications, au sein d'une classe d'applications à travers les fournisseurs, une liste explicite,
   ou l'ensemble des fournisseurs et classes détectés.
2. Exécuter `agent-config-sync/scripts/sync.py --discover`, puis `--offer`.
3. Présenter les points de terminaison détectés séparément des candidats non vérifiés.
4. Laisser l'utilisateur choisir la source de vérité, les cibles, la direction et la politique de conflit.
5. Matérialiser `registry.json`, examiner `--plan`, et seulement ensuite utiliser
   `--apply --yes`.

La découverte et les propositions sont en lecture seule. Il n'existe ni hub implicite ni
« tout synchroniser » implicite. Les anciens scripts Claude Code↔Claude Desktop constituent un profil hérité,
pas le comportement générique par défaut.

## Exemple d'appel

```
agent-config-sync/scripts/sync.py --discover
agent-config-sync/scripts/sync.py --offer
agent-config-sync/scripts/sync.py --plan
agent-config-sync/scripts/sync.py --apply --yes
```

## Journal des modifications

- v2.0.1 (2026-11-22) : Mention linguistique corrigée.
- v2.0.0 (2026-07-27) : Synchronisation rendue neutre vis-à-vis des fournisseurs — plus de fichier hub/maître
  implicite, l'utilisateur choisit lui-même source, cibles, direction et politique de conflit.
- v1.0.1 (2026-06-13) : Compétence publiée (scripts de synchro + modèle passés en chemins génériques,
  références anonymisées, version EN).
