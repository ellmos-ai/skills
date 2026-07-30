---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: Punto de entrada neutral respecto al proveedor para descubrir, planificar y sincronizar la configuración de MCP entre proveedores seleccionados por el usuario y clases de aplicación. El usuario selecciona la fuente de verdad, los objetivos y el alcance; ningún proveedor actúa como centro implícito.

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

> **Español** — Versión oficial en español de `mcp-config-sync`.


# MCP Config Sync (Español)

Este es el punto de entrada enfocado en MCP para `agent-config-sync`. No asume
ningún proveedor, aplicación ni archivo maestro.

1. Preguntar qué puntos de extremo o ejes concretos desea el usuario: dentro de un proveedor
   a través de clases de aplicación, dentro de una clase de aplicación a través de proveedores, una lista explícita,
   o cada proveedor y clase detectados.
2. Ejecutar `agent-config-sync/scripts/sync.py --discover`, y luego `--offer`.
3. Presentar los puntos de extremo detectados por separado de los candidatos no verificados.
4. Permitir que el usuario elija la fuente de verdad, los objetivos, la dirección y la política de conflictos.
5. Materializar `registry.json`, revisar `--plan`, y solo entonces usar
   `--apply --yes`.

El descubrimiento y las ofertas son de solo lectura. No hay un centro implícito ni una
sincronización total implícita ("sync all"). Los antiguos scripts de Claude Code↔Claude Desktop son un perfil heredado,
no el valor predeterminado genérico.