---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: Habilidad general de flujo de trabajo de Blender para agentes de IA que trabajan con archivos .blend, .fbx, .obj, .glb, glTF, materiales, inspección de escenas, automatización de bpy, ejecuciones en lote de Blender en modo headless, validación de exportación/reimportación, vistas previas y control opcional de Blender MCP. Utilizar cuando una tarea solicite abrir, inspeccionar, crear, automatizar, convertir, optimizar, renderizar o verificar Blender o archivos de activos 3D de forma agnóstica al usuario.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: es
status: active
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `using-blender`.

# Uso de Blender

## Regla principal

Trabaja con Blender en tres modos, según la tarea:

1. **Modo GUI:** Abrir Blender de forma visible cuando el usuario desee ver, evaluar o editar manualmente un activo.
2. **Modo Headless:** Utilizar `blender --background --python <script.py>` cuando se requiera exportación, reimportación, procesamiento por lotes o verificación determinista.
3. **Modo MCP:** Utilizar solo cuando un complemento de Blender en ejecución esté conectado intencionadamente y se necesite control de la escena en vivo. Comprobar previamente el estado de seguridad y licencias.

## Flujo de trabajo estándar

1. Aclarar el objetivo: ver, crear, convertir, optimizar, renderizar o verificar.
2. Leer archivos existentes primero: Manifiesto, README, formatos de exportación y resultados de prueba existentes.
3. Determinar la ruta de Blender: `blender` en PATH, configuración específica del proyecto o ruta del usuario. No escribir rutas privadas locales en documentación publicable.
4. Para la automatización, utilizar un script corto de `bpy` que haga explícitas las entradas, salidas y errores.
5. Después de cada exportación, ejecutar al menos una verificación de reimportación o carga antes de considerar el resultado como utilizable.
6. Documentar los artefactos de forma concisa: Fuente, formatos de exportación, versión de herramientas, estado de verificación y limitaciones conocidas.

## Reglas de exportación y verificación

- Preferir `.glb` para uso general en web/vista previa.
- Ofrecer adicionalmente `.fbx` o `.obj/.mtl` para motores de juegos e intercambio DCC si el flujo de trabajo de destino lo requiere.
- Para roundtrips siempre verificar: el archivo existe, no está vacío, se puede reimportar y los nombres de objetos/materiales esperados están presentes.
- Para activos grandes, recopilar métricas: recuento de mallas, materiales, caja delimitadora (bounding box), tamaño de archivo y opcionalmente recuento de triángulos.
- Para verificaciones de renderizado, utilizar una resolución de vista previa pequeña antes de iniciar renderizados costosos de Cycles o Full HD.

## Reglas de seguridad

- El código `bpy` es código Python local con acceso al sistema de archivos. Ejecutar únicamente scripts propios o auditados.
- No activar complementos de Blender externos, descargadores de activos ni servidores de telemetría sin verificar licencias y privacidad de datos.
- Para servidores MCP con herramientas arbitrarias `execute_python`, limitar previamente el alcance, la red, el directorio de trabajo y el tiempo de espera.
- Para activos del mercado o externos, verificar la licencia por separado. La capacidad técnica de carga no reemplaza los derechos de uso.

## Opciones de MCP

Para control en vivo, lee [references/blender-mcp-review.md](references/blender-mcp-review.md) si se debe seleccionar, instalar o evaluar un servidor Blender MCP.

## Registro de cambios

### 1.0.0 (2026-06-20)
- Skill inicial de Blender agnóstico al usuario con enrutamiento GUI, headless y MCP.