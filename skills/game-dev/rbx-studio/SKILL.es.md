---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Manejo de Roblox Studio para el desarrollo de videojuegos: el editor visual en el que se construye, prueba y publica la escena 3D. Usa esta habilidad para: conceptos básicos de Studio (Explorer, Workspace, pruebas de juego, guardar el lugar como .rbxl), la interacción con Rojo (Connect, modo escena vs. código), control de Studio por IA a través de Roblox-Studio-MCP (execute_luau, insert_from_creator_store, generate_material, screen_capture, Play/Stop, lectura de consola), el flujo completo del pipeline de assets (Creator Store → limpieza → kit → escena → .rbxl → Rojo le da vida), y sobre todo el escaneo OBLIGATORIO de malware para assets del marketplace. También activar con "insertar un asset de la tienda", "Studio MCP no funciona", "studios: []", "generar material", "guardar escena", "¿es seguro este asset de Roblox?", "los scripts desaparecen después de ejecutar Play".
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: es
status: active
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `rbx-studio`.

> **Note:** Not affiliated with Roblox Corporation; "Roblox" is a trademark of its owners. "rbx" is the common community shorthand.

# Roblox Studio — Editor, Pruebas, Assets, MCP

## Visión general y propósito

Roblox Studio es el editor oficial: construye la escena 3D, prueba el juego en modo de ejecución,
inserta assets desde Creator Store y publica el lugar (place). En un flujo de trabajo con Rojo,
Studio posee la **escena** (Workspace, Terrain, modelos colocados) y las **pruebas**;
el **código** proviene de Rojo a través del sistema de archivos (consulta la habilidad `/rojo`).

Esta habilidad cubre: conceptos básicos de Studio, la separación clara entre el trabajo de escena y de código,
el control por IA a través de Roblox-Studio-MCP y el flujo de trabajo de assets, incluyendo el
**escaneo obligatorio de malware** para cada asset del marketplace.

## Conceptos básicos

- **Explorer** — árbol de todas las instancias (Workspace, ServerScriptService, ReplicatedStorage, …).
  Con Rojo activo, las áreas mapeadas se pueblan en vivo desde el sistema de archivos.
- **Play-Test** — el botón verde Play (o F5) inicia una sesión local de servidor+cliente.
  Después de cada inicio, **revisa la consola Output en busca de errores**: el reflejo de depuración más importante.
- **Guardar place** — File → Save As → `.rbxl` (binario) o `.rbxlx` (XML, diffable).
  El place guardado contiene la **escena**. El código reside en el sistema de archivos, no en el place.

## El flujo de trabajo crítico: modo escena vs. modo código

Al conectar, Rojo sobrescribe todas las áreas de script mapeadas con el contenido del sistema de archivos.
El `Workspace` (escena 3D) **no** está mapeado y se mantiene intacto. De esto se deriva la
regla más importante del trabajo diario: nunca mezclar ambos modos:

**Modo A — editar la escena (Rojo DESACTIVADO):**
1. Detener el servidor de Rojo (`taskkill //F //IM rojo.exe` o Ctrl+C).
2. Abrir el place en Studio, colocar assets, construir el mundo, organizar.
3. File → Save → el archivo `.rbxl` contiene ahora la nueva escena.

**Modo B — probar el código (Rojo ACTIVADO):**
1. Abrir el mismo place en Studio.
2. Iniciar `rojo serve` → en el plugin de Rojo en Studio → Connect.
3. Presionar Play y probar. Rojo sincroniza los scripts; el Workspace proviene del `.rbxl`.
4. Mientras Rojo esté ejecutándose, **no** guardes (de lo contrario, el estado de Rojo se congelará en el `.rbxl`).

De esta manera, el trabajo de escena (Studio) y el trabajo de código (editor + Rojo) pueden ejecutarse en paralelo y
sin conflictos: los artistas construyen escenas, los desarrolladores escriben código.

## Roblox-Studio-MCP — La IA controla Studio

El Roblox-Studio-MCP permite a Claude/Gemini/Codex controlar directamente una instancia **en ejecución** de Studio:
ejecutar código, inspeccionar, Play/Stop, leer la consola e insertar assets. **No** reemplaza a Rojo,
sino que lo complementa: Rojo para cambios de código persistentes, MCP para inspección,
pruebas, inserción de assets y generación de materiales.

```
Editor + Rojo  ──(sincronización de código persistente)──►  Studio (en ejecución)  ◄──(inspección/prueba/inserción)──  MCP ◄── IA
```

### Herramientas MCP disponibles (típicas)

| Herramienta | Propósito |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | listar instancias abiertas / seleccionar la activa |
| `search_game_tree` / `inspect_instance` | buscar en la jerarquía / leer propiedades |
| `execute_luau` | ejecutar código Luau directamente en Studio |
| `script_read` / `script_grep` / `script_search` | analizar scripts |
| `multi_edit` | cambiar múltiples instancias/scripts en lote |
| `start_stop_play` | controlar Play/Stop |
| `get_console_output` | leer el registro Output |
| `screen_capture` | captura de pantalla de la escena |
| `insert_from_creator_store` | insertar un asset desde Creator Store |
| `generate_material` | generar un material/textura por IA (MaterialVariant) |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | simular entrada de usuario |

### Configuración (neutral respecto al usuario)

El MCP se ejecuta como un servidor distribuido con Studio, a menudo conectado mediante un envoltorio ligero de filtro JSON
(que filtra banners no-JSON que algunos clientes de otro modo no pueden interpretar):

- MCP batch (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- wrapper opcional: `<your roblox-mcp wrapper>`
  (si está presente en este sistema; compartido por Claude/Codex/Gemini)
- Configuración de clientes: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

Ejemplo de entrada (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

### Problemas comunes de MCP

| Síntoma | Significado / solución |
| --- | --- |
| `studios: []` o `Not connected to WS host` | no significa inmediatamente "roto": envía `initialize` → espera 2–3 s → `list_roblox_studios`; de lo contrario, reinicia Studio |
| `Error: connection closed: initialized request` | Studio no está abierto en absoluto: inicia Studio, carga el place e intenta de nuevo |
| scripts escritos vía MCP desaparecen tras Play/Stop | las ediciones de código vía MCP no son persistentes: para cambios de código duraderos usa **Rojo** |
| valor vía `require()` en la VM del plugin es incorrecto | la VM del plugin tiene su propia caché de require; para verificar, lee `.Source` directamente o revisa el registro del servidor tras Play |

## Pipeline de assets (Creator Store → juego)

Greybox primero (gameplay), assets después (antes del lanzamiento). La secuencia comprobada:

```
BUSCAR EN LA TIENDA → ej. "medieval" → cargar varios candidatos
DESCARTAR           → eliminar los que no coincidan con el estilo / feos, conservar 5–8 adecuados
LIMPIAR             → eliminar TODOS los scripts (!malware!), conservar solo geometría/meshes
CREAR KIT / SET     → derivar variantes de los assets base (mismos materiales/proporciones)
CONSTRUIR ESCENA (Studio) → ensamblar assets en la escenografía (pueblo, arena, parque)
GUARDAR COMO .RBXL  → la escenografía es el "escenario"
ROJO LE DA VIDA     → los scripts/gameplay/HUD se añaden mediante Rojo; Workspace permanece intacto
```

**Técnica de variantes ("kit modular"):** Toma un buen asset base y deriva todo un
conjunto a partir de él (casa → torre, granero, herrería, ruina). Todos comparten materiales, colores y
proporciones → una apariencia coherente con un esfuerzo mínimo, tal como lo hacen los estudios profesionales.

**Fuentes de assets (prioridad):** Creator Store (gratuito, enorme, **verificación de malware obligatoria**) →
materiales por IA (`generate_material`) → tus propias meshes (Blender → .fbx) → paquetes de assets comprados.

## OBLIGATORIO: escaneo de malware para assets del marketplace

Los assets de Creator Store pueden contener scripts maliciosos ofuscados (puertas traseras, código remoto,
ganchos a redes de bots). Escanea **cada** asset importado antes de usarlo y elimina todos los scripts:
conserva solo la geometría/meshes.

- Referencia de patrones: [`references/malware-patterns.md`](references/malware-patterns.md) — los 8
  patrones de ofuscación conocidos (carga útil en atributos invertidos, script falso del sistema,
  `require()` remoto, `loadstring`, `string.char`, `getfenv/setfenv`, Values ocultos, ejecución diferida).
- Escáner: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — ejecútalo en Studio vía
  `execute_luau` (o en la Command Bar); verifica una instancia frente a todos los patrones e informa de los hallazgos.

**Señales de alerta inmediatas:** un script grande en un modelo puramente decorativo · cadenas invertidas en
atributos · `require(<number>)` · `loadstring` · `HttpService` en un asset que no requiere red.
En caso de duda: elimina el script. Documenta los hallazgos (ej. `_malware_reports/YYYY-MM-DD_*.md`
en el pipeline de referencia).

## Trampas importantes de Luau/Studio (extracto)

Las más comunes que causan problemas en Studio — la lista completa se mantiene en la habilidad `/rbx-dev`:

- `Model.Position` no existe → `model:GetPivot().Position`.
- `tick()` está obsoleto → `os.clock()` / `workspace:GetServerTimeNow()`.
- `SetPrimaryPartCFrame()` obsoleto → `model:PivotTo(cf)`.
- Llamadas a DataStore **siempre** dentro de `pcall`.
- Baseplate + suelo procedural a la misma altura → Z-fighting (parpadeo): elimina la Baseplate
  o eleva el suelo +0.1 studs.
- Mantén bajo control el presupuesto de partes (~50–80 partes por habitación generada proceduralmente).

## Lecturas adicionales

- Habilidades hermanas: `/rojo` (sincronización, configuración de proyecto), `/game-design` (roles, flujos de trabajo, GDD),
  meta habilidad `/rbx-dev` (patrones de arquitectura + todas las lecciones de Luau).
- Documentación del motor/creador: Context7 MCP (`/websites/create_roblox_reference_engine`,
  `/roblox/creator-docs`) o <https://create.roblox.com/docs>.
- Pipeline de referencia (si existe): `<your Roblox project pipeline>`
  (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`).

## Historial de cambios

### 1.0.0 (2026-06-17)
- Versión inicial. Distilada a partir del pipeline `.ROBLOX` (ROBLOX_MCP_FAQ, ASSET_PIPELINE,
  PATTERNS, LESSONS_LEARNED), escrita de forma neutral respecto al usuario.