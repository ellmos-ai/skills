---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  Estrategia aislada de navegación y enrutamiento que busca hacia arriba y hacia abajo
  a través de las jerarquías de directorios documentos indicativos (CLAUDE.md, AGENTS.md,
  README.md, RULES.md) y palabras clave configurables por el usuario (a través de staircase-config.json
  o config.json). También conocida como Up-and-Down Routing o Walking Bass Routing.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
language: es
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
---

> **Español** — Versión oficial en español de `staircase-routing`.

# Staircase-Routing (Enrutamiento Up-and-Down / Walking Bass)

La habilidad **Staircase-Routing** (también conocida como *Up-and-Down Routing* o *Walking Bass Routing*) aísla la estrategia de inspección de documentos de directorio para agentes de IA.

Cuando un agente entra a un directorio o trabaja en un archivo, utiliza esta estrategia para localizar el contexto autoritativo, las reglas y los documentos indicativos antes de modificar el código o realizar acciones.

---

## 1. Estándares de Documentos Indicativos

Por defecto, Staircase-Routing busca documentos indicativos estándar:
- **Controles Globales y del Proyecto:** `CLAUDE.md`, `AGENTS.md`, `START.md`, `RULES.md`
- **Visión General e Inspección de Tareas del Proyecto:** `README.md`, `TODO.md`, `NOTIZ.md`, `BEWEISNOTIZ.md`
- **Palabras Clave Personalizables por el Usuario:** Configuradas mediante `staircase-config.json` o `config.json`.

---

## 2. Algoritmo de Recorrido

```
                           [ Root / Workspace Level ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Step 2: Read Root Signpost)
                           └───────────▲────────────┘
                                       │ (Staircase Up)
                           ┌───────────┴────────────┐
                           │ Subfolder / Target Dir │ ◄── (Step 1: Start at CWD)
                           └───────────┬────────────┘
                                       │ (Staircase Down)
                           ┌───────────▼────────────┐
                           │ Child / Module Dir     │ ◄── (Step 3: Discover Sub-Signposts)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### Paso 1: Inspección del Directorio de Trabajo Actual (CWD)
- Inspeccionar el directorio del archivo objetivo o el directorio de trabajo activo.
- Si existen documentos indicativos, leerlos inmediatamente.

### Paso 2: Recorrido Ascendente (Staircase Up)
- Si **no** se encuentra ningún documento indicativo en el CWD, subir al directorio padre (`..`).
- Repetir paso a paso hacia arriba hasta alcanzar un documento indicativo de la raíz (`CLAUDE.md` o `AGENTS.md`) o el límite del espacio de trabajo.
- Leer todos los documentos indicativos de la raíz descubiertos para establecer las directivas globales y las reglas del proyecto.

### Paso 3: Inspección Descendente (Staircase Down)
- Desde el directorio raíz establecido, descender a los directorios hijos relevantes para la tarea.
- Descubrir documentos indicativos especializados a nivel de módulo, reglas de dominio o configuraciones de componentes. Leerlos.

---

## 3. Palabras Clave Configurables por el Usuario (`staircase-config.json`)

Los agentes pueden leer un archivo `staircase-config.json` local o global para personalizar los documentos indicativos objetivo:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. Integración con `letter-hooker` y Tareas Programadas

`staircase-routing` está integrado como un cargador de arranque (bootloader) de verificación previa fundamental en la habilidad **`letter-hooker`** y en la tarea programada **`antigravity-kontext-and-workflow-loader-and-divider`**, garantizando que los agentes siempre localicen y obedezcan los documentos indicativos antes de iniciar ediciones.