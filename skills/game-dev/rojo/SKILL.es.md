---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Uso de Rojo: la herramienta de sincronización del sistema de archivos a Roblox Studio para el desarrollo profesional de Roblox en VS Code / Claude Code en lugar del editor de Studio. Usa esta skill siempre que Rojo esté involucrado: `rojo serve`/`rojo build`, escribir o depurar `default.project.json`, versiones de herramientas y rokit/rokit.toml (Rojo, Lune, Wally), mapeo de rutas anidado frente a plano (ReplicatedStorage.Project.shared), problemas de conexión/puerto/sincronización o cuando sea necesario crear la estructura básica de un proyecto de Roblox. También activa con "rojo connect no funciona", "los scripts terminan en el lugar equivocado en Studio", "cómo mapear src/ a Studio", "puerto 34872 en uso", "ModuleScript vs Script en Rojo".
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: es
status: active
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `rojo`.


# Rojo — Sincronización del Sistema de Archivos → Roblox Studio

## Visión general y propósito

Rojo conecta un proyecto normal del sistema de archivos (archivos `.luau` en `src/`, con control de versiones en Git)
con Roblox Studio. Escribes código en el editor de tu elección (VS Code, Claude Code) y Rojo
lo sincroniza en vivo en una instancia de Studio en ejecución. Esto hace que el código de Roblox sea versionable,
diferenciable (diffable) y editable con herramientas reales, en lugar de residir en el editor de scripts integrado de Studio.

Usa esta skill para todo lo relacionado con la configuración de Rojo, el mapeo de `default.project.json`, la
cadena de herramientas (rokit/Wally/Lune) y los problemas típicos de sincronización.

## Modelo mental

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**Regla principal:** El sistema de archivos es la fuente de verdad. En cada conexión, Rojo sobrescribe
las áreas mapeadas de Studio con el contenido del sistema de archivos. Por lo tanto, **nunca** edites código
en Studio (se perderá en la siguiente sincronización), solo en el editor. El `Workspace`
(escena 3D, terreno) **no** está mapeado por Rojo y se conserva; consulta la skill
`/rbx-studio` para el flujo de trabajo de escena vs. código.

## Extensiones de archivo → Tipo de Roblox (Convención de Rojo)

Rojo deriva el tipo de instancia a partir de la extensión. Esta es la fuente más común de errores:

| Archivo            | Tipo de Roblox | ¿Se puede requerir (`require()`)? | Rol                       |
| ------------------ | ------------- | --------------------------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **sí**                            | Módulo de lógica, definiciones |
| `Foo.server.luau`  | Script        | no                                | Punto de entrada del servidor |
| `Foo.client.luau`  | LocalScript   | no                                | Punto de entrada del cliente |
| `init.luau`        | se convierte en el propio nodo de carpeta | sí            | hace que la carpeta sea un ModuleScript |

> Regla general: **Solo los puntos de entrada** son `.server.luau`/`.client.luau`. Todo lo cargado mediante
> `require()` **debe** ser un ModuleScript `.luau`. Llamar a `require()` en un
> Script/LocalScript arroja "Attempted to call require with invalid argument(s)".

## Comandos de CLI

```bash
rojo serve default.project.json     # Iniciar servidor de sincronización en vivo (puerto predeterminado 34872)
rojo serve                          # usa default.project.json automáticamente
rojo build default.project.json -o game.rbxlx   # compilación única → archivo Place (XML)
rojo build default.project.json -o game.rbxl    # compilación única → archivo Place (binario)
rojo plugin install                 # instalar plugin de Rojo para Studio (una sola vez)
rojo --version                      # verificar la versión instalada
```

Después de `rojo serve`: en Studio, abre el plugin de Rojo → **Connect** (localhost:34872).
`rojo build` no requiere que Studio esté en ejecución: ideal para CI, pruebas de humo y lanzamientos.

## `default.project.json` — El mapeo

Este archivo mapea rutas del sistema de archivos a la jerarquía del modelo de datos de Roblox. Claves:

- `name` — nombre del proyecto (visualización)
- `$className` — clase de Roblox del nodo (`DataModel`, `ServerScriptService`, `Folder`, …)
- `$path` — ruta del sistema de archivos que se sincroniza bajo este nodo (relativa a la raíz del proyecto)

Una plantilla estándar lista para usar se encuentra en [`assets/default.project.json`](assets/default.project.json).

### Plano vs. Anidado — La decisión más importante

Tu código debe coincidir con el mapeo. Dos variantes:

**Plano (Flat)** — el contenido de `src/server` termina directamente en `ServerScriptService`:
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ El código hace referencia, por ejemplo, a `ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`.

**Anidado (Nested)** — el contenido termina en `ServerScriptService.ProjectName`:
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ El código hace referencia a `ReplicatedStorage.ProjectName.shared.Config`, etc.

Ambos son válidos. Decide una **única** variante para todo el proyecto y mantén cada
ruta de `require`/`WaitForChild` coherente con ella. Síntoma de desajuste: `WaitForChild(...)`
se cuelga indefinidamente (infinite yield), porque el nodo esperado se encuentra en otro lugar.

## Cadena de herramientas mediante rokit

[rokit](https://github.com/rojo-rbx/rokit) es el gestor de la cadena de herramientas. Un archivo `rokit.toml` en el
proyecto (o carpeta superior) fija las versiones exactas de las herramientas → compilaciones reproducibles en todas
las máquinas. Si falta, obtendrás `Failed to find tool 'rojo' in any project manifest file`.

Configuración estándar de `rokit.toml` (ver [`assets/rokit.toml`](assets/rokit.toml)):
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> Nota sobre la versión: 7.4.4 es la versión fijada sistemáticamente en toda la canalización de referencia.
> Los proyectos más recientes pueden usar 7.6.x, pero prueba primero con `rojo build` en el proyecto,
> ya que el formato del proyecto puede cambiar entre versiones principales.

Después de clonar/configurar: `rokit install` descarga todas las herramientas fijadas.

- **Lune** — ejecutor de Luau fuera de Studio (pruebas unitarias, scripts de compilación, procesamiento de assets).
- **Wally** — gestor de paquetes: `wally install` → `Packages/` → en Studio bajo
  `ReplicatedStorage.Packages`. Las dependencias se enumeran en `wally.toml` (ver
  [`assets/wally.toml`](assets/wally.toml)), p. ej., el framework `sleitnick/knit@1.7.0`.

## Creación de un nuevo proyecto

El script [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) crea una
estructura completa de Rojo (project.json, rokit.toml, wally.toml, `src/{shared,server,client,gui}/`
con archivos iniciales y borrador de KONZEPT):

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # mapeo plano (predeterminado)
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # mapeo anidado
```

Después de eso: `cd MeinSpiel && rokit install && rojo serve`.

## Solución de problemas

| Síntoma | Causa | Solución |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | no hay `rokit.toml` | crea `rokit.toml` con la versión fijada de Rojo en la carpeta del proyecto o carpeta padre y ejecuta `rokit install` |
| `require` lanza "invalid argument(s)" | `require()` en un Script/LocalScript | solo los ModuleScripts `.luau` se pueden requerir; comprueba la extensión |
| Puerto 34872 en uso (`os error 10048`) | un proceso de Rojo anterior está ejecutándose | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F`, luego ejecuta `rojo serve` de nuevo |
| Los scripts terminan en el lugar equivocado en Studio | mapeo plano en lugar de anidado (o viceversa) | ajusta `default.project.json` a las rutas de código (ver arriba) |
| `WaitForChild` se cuelga indefinidamente | el nodo esperado no existe / error en el servidor antes de crearse | **revisa primero la consola del servidor en busca de errores**; verifica el mapeo y el orden de creación |
| La sincronización se detiene tras renombrar un archivo | Rojo no detecta el cambio de nombre de inmediato | detén el servidor (Ctrl+C) y reinícialo; en Studio selecciona Disconnect → Reconnect |
| El cambio en Studio desaparece tras reconectar | edición en Studio en lugar de en el sistema de archivos | modifica el código **únicamente** en el editor; Rojo sobrescribe las áreas mapeadas |

### Limitaciones conocidas de Rojo

1. **Sin sincronización de terreno/Workspace** — construye la escena 3D y el terreno en Studio o genéralos mediante código.
2. **Sin fusión (merge) de `.rbxl`** — los archivos de lugar son binarios y no se pueden fusionar con git. Nunca los utilices como fuente primaria.
3. **Sin sincronización en vivo en modo Play** — los cambios realizados durante la reproducción se descartan al detener.
4. **Traducción de rutas en Git Bash** — `/c/...` se puede traducir a `C:/...` y romper las rutas de Rojo; en caso de duda, usa rutas relativas o rutas nativas de Windows.

## Linter (Selene)

Los proyectos de Roblox Luau se suelen analizar con **Selene** (`selene.toml` en la raíz,
`std = "roblox"`). Permite globales como `_G` mediante `global_usage = "allow"` si el proyecto
los utiliza para el estado compartido del cliente. Ejecuta Selene desde el directorio que contiene la definición
de la API de Roblox (`roblox.yml`).

## Lecturas adicionales

- Skills hermanas: `/rbx-studio` (operación de Studio, MCP, assets), `/game-design`
  (roles, flujos de trabajo, GDD), meta-skill `/rbx-dev` (combina las tres + patrones de arquitectura).
- Documentación actual del motor/Rojo: MCP Context7 (`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) o
  <https://rojo.space/docs/>.
- Si está presente en este sistema, una canalización de referencia de proyectos se encuentra en
  `<tu canalización de proyectos de Roblox>` (incl. `ROJO_FAQ.md`, `SKILL.md`).

## Historial de cambios

### 1.0.0 (2026-06-17)
- Versión inicial. Extraída de la canalización `.ROBLOX` (ROJO_FAQ, ROJO_START, _template),
  redactada de forma neutral para el usuario.