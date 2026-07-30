---
name: skill-finder
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Buscador/enrutador activo para las habilidades locales propias (análogo a using-superpowers). Utilizar SIEMPRE
  al inicio de una tarea no trivial para verificar si encaja una habilidad del usuario y enrutar a la correcta.
  Se activa ante solicitudes de "¿qué habilidad encaja?", "¿hay una habilidad para esto?", "encontrar habilidad",
  o en general antes de tareas que una habilidad local resuelva mejor que el trabajo ad-hoc.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-finder banner">
# Buscador de Habilidades (Skill-Finder)

## La Regla

Antes de iniciar cualquier tarea no trivial, verifica primero si una habilidad local la resuelve mejor. Ante la menor sospecha, carga la habilidad correspondiente y **sigue sus instrucciones en vivo** (leer el archivo, no trabajar de memoria). Si ninguna habilidad aplica, procede normalmente.

## Enrutamiento por Familias

<!-- Generado/actualizado a partir de SKILL-MAP.md + inventory_skills.py. Tema -> Familia -> Habilidad.
     Mantenimiento: Sub-habilidad skill-family-care o nueva ejecución de auditoría skill-explorer. Estado: 2026-06-17 -->

| Tema / Intención | Familia | Habilidad(es) |
|-----------------|---------|----------|
| Reflexionar / analizar un problema | Herramientas de pensamiento | `/structured-thinking` (guía `/think` → `/brainstorm` → `/decide`) |
| Nuevas ideas / creatividad | Herramientas de pensamiento | `/brainstorm` (vs `/think` análisis, `/decide` selección) |
| Pila de decisiones | Herramientas de pensamiento | `/decision-briefing` |
| Crear o usar un modelo autorizado de preferencias del usuario | Multi-Agente | `build-your-users-mind` (creación) · `decision-avatar` (uso) |
| Error / fallo de prueba | Código y depuración | `/bugfix-protocol` (1 bug), `/bugsweep` (muchos, antes del lanzamiento) |
| Proyecto o pipeline nuevo/existente | Proyecto/Pipeline | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Juego de Roblox | Desarrollo de juegos | `/roblox-dev` (→ `/rojo`, `/roblox-studio`, `/game-design`) |
| Terapia / asesoramiento / crisis | Terapia | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| Presentación / diapositivas | Oficina | `/academic-pptx` (contenido) + `/pptx` (archivo) |
| Coordinación multi-agente | Multi-Agente | `/swarm-operations`, `/model-strategy` |
| Solicitud de empleo / autogestión | Personal | `/bewerbungsexperte`, `/selbstmanagement` |
| Comparar/limpiar/buscar habilidades | Sistema/Meta | `skill-explorer` (auditoría/exploración), `code-skill-index` (lista) |
| Configurar sistema / sincronizar MCP / conectar agentes | Sistema/Meta | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| Herramientas de archivos | Utilidades | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| Historial de chat → conservar como habilidad | Sistema/Meta | `skill-extractor` (`/skill-extract`) |
| Historial de chat/automatización externa → automatización | Sistema/Meta | `workflow-extract` (`/automations-extract`) |
| Revisión recurrente en muchos proyectos | Código y depuración | `rotation-check` (estructura registro/log) |
| Problema estancado, extraer ideas | Herramientas de pensamiento | `idea-mining` (vs `/brainstorm` = libre/amplio) |
| Mantener sincronizadas versiones DE/EN | Utilidades | `bilingual-doc-sync` |
| Riquezas de IA/restos de chat en texto, divulgación de IA | Utilidades | `llm-text-hygiene` |
| Condición/momento/orden en el encargo ("solo cuando", "a partir de 6 am", "tan pronto como X esté listo") | Proceso | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |

Lista completa: Habilidad `code-skill-index`.

## Señales de alerta (Racionalizaciones que significan ALTO)

| Pensamiento | Realidad |
|---------|----------|
| "Es solo una pregunta rápida." | Las preguntas son tareas — verificar habilidades primero. |
| "Conozco el concepto." | Conocer el concepto ≠ usar la habilidad. Leer archivo en vivo. |
| "La habilidad es excesiva." | Lo simple se vuelve complejo — utilízala. |
| "Exploraré por mi cuenta primero." | Las habilidades indican CÓMO explorar. Verificar primero. |

## Mantenimiento

Actualizar la tabla de enrutamiento ante un cambio de familia (sub-habilidad `skill-family-care` o nueva ejecución de `inventory_skills.py` desde `skill-explorer`).

## Registro de cambios

### 0.2.0 (2026-07-03)
- Líneas de enrutamiento añadidas para nuevas habilidades: skill-extractor, workflow-extract, rotation-check, idea-mining, bilingual-doc-sync (extracción de automatizaciones de Codex).

### 0.1.0 (2026-06-17)
- Versión inicial. Creada por el modo de auditoría ([F]) como análogo a using-superpowers. Tabla de enrutamiento de la auditoría del 2026-06-17 (10 familias del usuario).
