---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: Planificador neutral con respecto al proveedor para sincronizar la configuración de MCP, skills y archivos de reglas en distintos proveedores de agentes y clases de aplicaciones. Descubre opciones locales evidenciadas y permite al usuario elegir la fuente de verdad, los objetivos, la dirección y la resolución de conflictos.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: es
status: active
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Español** — Versión oficial en español de `agent-config-sync`.


# Agent Config Sync (Español)

El skill separa la selección de puntos de extremo (endpoints), recursos y la fuente de verdad. Ejecute:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

El usuario puede seleccionar una lista explícita de puntos de extremo, un proveedor a través de diferentes clases de aplicaciones, una clase de aplicación a través de distintos proveedores, o todos los puntos de extremo detectados. La detección constituye una evidencia, no una autorización.

La fuente de verdad (truth) puede ser un punto de extremo, un archivo, un conjunto ordenado de archivos como múltiples capas de `AGENTS.md`, o un directorio de skills. Ningún nombre de archivo ni proveedor actúa como hub implícito. Sin una fuente de verdad seleccionada, los planes permanecen bloqueados.

Revise `--status` y `--plan`; utilice `--apply --yes` únicamente tras su aprobación. Se han implementado los bloques MCP y los directorios de skills. Las topologías de archivos de reglas permanecen cerradas ante fallos (fail-closed) hasta que el usuario seleccione un adaptador de fusión o redirección.