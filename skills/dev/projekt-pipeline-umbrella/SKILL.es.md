---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Meta/Umbrella skill para la familia "Creación y reestructuración de proyectos/pipelines". Conoce todos los skills
  para crear, incorporar, reestructurar y analizar proyectos y pipelines, y redirige al más adecuado.
  Utilice este skill cuando no esté claro si algo debe crearse desde cero (greenfield) o reestructurarse (existente),
  o si se trata de un solo proyecto o de todo un pipeline. También activar en "crear nuevo proyecto/pipeline",
  "reestructurar existente", "incorporar proyecto", "renovar estructura de carpetas", "qué bootstrapper encaja".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">

# Creación y Reestructuración de Proyectos/Pipelines — Umbrella

## Propósito

Punto de entrada para la familia "Creación y reestructuración de proyectos/pipelines". Sus miembros se organizan a lo largo de dos ejes: **Greenfield vs. Existente** y **Nivel de Proyecto vs. Nivel de Pipeline**. Este Umbrella evita la confusión frecuente entre "bootstrap" vs. "optimize" vs. "onboard".

## Miembros y Enrutamiento

| Skill | Para qué sirve | Cuándo usar este en lugar de los otros |
|-------|-------|-------------------------------|
| `/project-bootstrapper` | Crear un NUEVO proyecto **en** un pipeline existente | Greenfield, Nivel de Proyecto |
| `/pipeline-bootstrapper` | Crear un pipeline de nivel superior COMPLETAMENTE NUEVO | Greenfield, Nivel de Pipeline (raro) |
| `/project-onboarding` | Incorporar/registrar un proyecto existente | Existente, Nivel de Proyecto |
| `/pipeline-optimizer` | Renovar estructura/pipeline existente (procedimiento de 6 pasos) | Existente, Reestructuración |
| `/docs-analysis` | Comprobar docs de requisitos/concepto frente al código actual | Existente, Análisis (sin reestructuración) |
| `/dev-cycle` | Marco de desarrollo de 8 fases para la construcción real | Transversal: el CÓMO del desarrollo |

> Regla de enrutamiento: **nuevo + proyecto** → `/project-bootstrapper` · **nuevo + pipeline** → `/pipeline-bootstrapper` · **incorporar existente** → `/project-onboarding` · **reestructurar existente** → `/pipeline-optimizer` · **solo comprobar** → `/docs-analysis` · **construir** → `/dev-cycle`.

## Combinaciones bien acopladas

- `/project-onboarding` (primero: registrar existente) → `/pipeline-optimizer` (después: reestructurar objetivamente) — entender primero, renovar después (cubre el principio de 6 pasos "leer primero, escribir después").
- `/docs-analysis` (encontrar brechas) → `/dev-cycle` (cerrar brechas).
- `/project-bootstrapper` (estructura) → `/dev-cycle` (desarrollar contenido).

## Convenciones comunes

- Leer siempre primero las convenciones existentes del pipeline (Registry, Templates, CLAUDE.md); no crear estándares paralelos.
- Los skills Greenfield crean, los skills Existente renuevan: no mezclarlos.
- Leer los archivos en vivo de los skills individuales antes de aplicarlos.

## Historial de cambios

### 0.1.0 (2026-06-17)
- Versión inicial. Generada por el modo de auditoría (3c1) para la familia de proyectos/pipelines.
