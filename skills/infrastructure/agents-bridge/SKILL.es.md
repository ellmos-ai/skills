---
name: agents-bridge
version: 3.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-07-04
updated: 2026-08-22
description: Puente neutral de proveedor y usuario para reglas de inicio de agentes, CLI e IDE. Descubre superficies de bootstrap conocidas, requiere que el usuario seleccione una o más fuentes de verdad ordenadas y genera cargadores pequeños sin duplicar reglas.

standalone: true
anthropic_compatible: true
category: infrastructure
tags: [multi-agent, bootstrap, rules, agents-md, provider-neutral]
language: es
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
---

<img src="banner.png" width="100%" alt="agents-bridge banner">

> **Español** — Versión oficial en español de `agents-bridge`.


# AGENTS-BRIDGE (Español)

Utilice esta skill para conectar un agente o IDE a archivos de reglas seleccionados explícitamente.
Ningún proveedor, nombre de archivo, host o directorio en la nube es implícitamente canónico.

## Flujo de trabajo y procedimiento

1. Lea todas las instrucciones locales que rigen los caminos de origen y destino.
2. Ejecute `python scripts/bridge.py discover` y opcionalmente pase `--project`.
3. Solicite al usuario que seleccione las fuentes de verdad ordenadas y el destino. Una selección vacía no autoriza ninguna escritura.
4. Prefiera una redirección o un cargador ordenado. Use una copia generada solo cuando el destino no pueda cargar referencias, y registre la procedencia más las comprobaciones de desviación (drift checks).
5. Vista previa con:

   ```text
   python scripts/bridge.py render --truth <path> --target-kind generic
   ```

6. Cree o modifique el destino solo después de revisar la vista previa.
7. Demuestre que el agente de destino realmente leyó cada fuente seleccionada.

Consulte `references/agent-conventions.md`,
`references/truth-topologies.md` y
`references/inventory-contract.md`.

`agent-config-sync` gestiona topologías de configuración más amplias.
`agents-bridge` se limita al acceso a reglas e inicio. Los puentes de socios en tiempo de ejecución y los programadores son componentes independientes.
