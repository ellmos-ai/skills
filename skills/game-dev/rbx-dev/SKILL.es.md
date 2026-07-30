---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Meta-habilidad para el desarrollo completo de juegos de Roblox con Rojo — el punto de entrada que conoce y unifica las tres habilidades especializadas `/rojo` (sincronización sistema de archivos→Studio, configuración del proyecto), `/rbx-studio` (editor, MCP, assets, escaneo de malware) y `/game-design` (roles, flujos de trabajo, GDD). Use esta habilidad para CUALQUIER proyecto de desarrollo de juegos en Roblox: planificar/construir/configurar un juego de Roblox, crear la estructura de un nuevo proyecto, definir la arquitectura del código (Main + módulos manager, _G.ClientState + HUD, remotes en GameEnums), evitar trampas de Luau/Roblox, o cuando no esté claro cuál de las habilidades especializadas de Roblox encaja — el enrutamiento se realiza desde aquí. También se activa con "desarrollar juego Roblox", "construir juego Roblox", "nuevo proyecto Roblox", "estructura de proyecto Luau", "cómo organizo código Roblox", "configuración dev Roblox".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: es
status: active
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="rbx-dev banner">

> **Español** — Versión oficial en español de `rbx-dev`.

> **Nota:** Sin afiliación con Roblox Corporation; "Roblox" es una marca registrada de sus propietarios. "rbx" es la abreviatura común de la comunidad.

# Roblox-Dev — Meta-Habilidad para el Desarrollo de Juegos en Roblox (Español)

## Descripción y Propósito

El punto de entrada central para el desarrollo de juegos en Roblox con un flujo de trabajo basado en Rojo y control de versiones.
Esta habilidad reúne el conocimiento general — estructura de proyectos, patrones de arquitectura y las
trampas de Luau más importantes — y redirige las preguntas especializadas a las tres sub-habilidades:

| Sub-habilidad | Para qué sirve |
| --- | --- |
| **`/rojo`** | Sincronización sistema de archivos→Studio, `default.project.json`, rokit/Wally/Lune, esqueleto del proyecto, problemas de sincronización |
| **`/rbx-studio`** | Operación de Studio, modo escena vs código, Studio MCP, pipeline de assets, **escaneo de malware** |
| **`/game-design`** | Roles y subtareas, cadenas de desarrollo, Documento de Diseño del Juego (KONZEPT.md), multi-agente |

> Regla de enrutamiento: Si se trata de **sincronización/construcción/configuración** → `/rojo`. Sobre **editor/assets/pruebas en Studio**
> → `/rbx-studio`. Sobre **concepto/roles/proceso** → `/game-design`. Sobre **arquitectura de código,
> trampas de Luau o el flujo general** → permanezca aquí.

## Vista Rápida del Stack

- **Lenguaje:** Luau (`.luau`, no `.lua`). Código en inglés, comentarios/documentación en español, textos de interfaz en el idioma de destino.
- **Sincronización:** Rojo mediante rokit (versiones fijadas de herramientas). Sistema de archivos = fuente de verdad.
- **Herramientas:** Rojo (sync/build), Lune (pruebas/scripts fuera de Studio), Wally (paquetes),
  opcionalmente Knit (framework de servicios/controladores, proyectos nuevos), Selene (linter).
- **Control:** Roblox-Studio-MCP para inspección guiada por IA, pruebas e inserción de assets.

## Estructura del Proyecto (Estándar)

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

Un esqueleto es creado por `/rojo` mediante `scaffold_roblox_project.sh`.

## Patrones de Arquitectura

**Servidor — Main + módulos manager.** Solo **un** Script por proyecto: `Main.server.luau`. Crea
de forma centralizada la carpeta de remotes y carga todos los módulos de funcionalidades mediante `require()`:
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
Todos los demás archivos del servidor son `.luau` (ModuleScripts).

**Cliente — estado compartido + HUD.** El GameClient escribe un estado compartido, el HUD lo lee
en el Heartbeat:
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — centralizados en GameEnums.** Defina los nombres remotos una vez en `GameEnums.Remotes`;
el servidor crea los eventos a partir de ellos y el cliente los busca con los mismos nombres. De esa manera no hay
desajustes de cadenas de texto entre el servidor y el cliente.

## Flujo General de un Juego

1. **Concepto** (`/game-design`): KONZEPT.md — género, propuesta de valor (USP), 3–4 mecánicas principales, monetización.
2. **Configuración** (`/rojo`): crear el esqueleto, definir el mapeo en `default.project.json`.
3. **Backend**: Config → GameEnums → *Defs → Main.server → *Manager.
4. **Frontend**: GameClient → HUD.
5. **Prueba en greybox** (`/rbx-studio`): jugabilidad primero, partes + opcionalmente materiales IA.
6. **Mejora de assets** (`/rbx-studio`): assets de la Creator Store, **escaneo de malware**, escena como .rbxl.
7. **Prueba** (`/game-design`): QA + crítica de juegos + pruebas a ciegas con personas, iterar.
8. **Lanzamiento** (`/game-design` rol de negocio): página de tienda, monetización, live ops.

## Trampas de Luau/Roblox (Lista Corta)

Las trampas más comunes — lista completa y anotada:
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md).

- Punto y coma después de `task.wait(x)` cuando sigue más código en la misma línea.
- `Model.Position` no existe → `model:GetPivot().Position`.
- `#table` en diccionarios = 0 → contar manualmente.
- `mouse.Hit` puede ser nil → verificar antes de usar.
- Llamadas a DataStore **siempre** en `pcall`.
- `tick()` obsoleto → `os.clock()`; `SetPrimaryPartCFrame` → `PivotTo`.
- Nombres de eventos centralizados en `GameEnums.Remotes`; crear todos los remotes en `Main.server.luau`.
- Sin `require` circulares (de lo contrario, punto muerto/deadlock).
- `require()` solo en ModuleScripts `.luau`, nunca en Scripts/LocalScripts.

## Antes de Cada Commit (Lista de Verificación)

- [ ] Puntos y comas después de `task.wait(...)` en líneas con múltiples sentencias
- [ ] sin `Model.Position`, sin `tick()`, sin `SetPrimaryPartCFrame`
- [ ] DataStore en `pcall`, `mouse.Hit` verificado para nil
- [ ] nombres de eventos coinciden servidor↔cliente (vía GameEnums)
- [ ] todos los RemoteEvents creados en `Main.server.luau`
- [ ] sin require circulares
- [ ] assets del marketplace escaneados (`/rbx-studio` → escaneo de malware), informes registrados

## Fuentes de Conocimiento

- **Documentación actual del motor/creador:** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine` (API del motor) y `/roblox/creator-docs`
  (tutoriales/guías); fallback <https://create.roblox.com/docs>.
- **Pipeline de referencia** (si está presente en este sistema): `<your Roblox project pipeline>` —
  incluyendo `SKILL.md`, `GUIDE.md`, `LESSONS_LEARNED.md`, `ROJO_FAQ.md`, `ROBLOX_MCP_FAQ.md`,
  `AGENT_ROLES.md`, `_malware_reports/PATTERNS.md`, `_knowledge/` (caché local de la API).

## Historial de Cambios

### 1.0.0 (2026-06-17)
- Versión inicial. Meta-habilidad sobre `/rojo`, `/rbx-studio`, `/game-design`; estructura de proyecto,
  patrones de arquitectura y lecciones de Luau extraídas del pipeline `.ROBLOX`, neutral para el usuario.