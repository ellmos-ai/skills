---
name: therapie-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Habilidad meta/paraguas para la familia "Terapia / Asesoramiento". Conoce todas las habilidades terapéuticas
  (estabilización, visión general de métodos, técnicas de conversación + procedimientos especializados desregistrados) y encamina
  hacia la adecuada. Utilice esta habilidad cuando no esté claro qué habilidad terapéutica/de asesoramiento se adapta,
  se necesite una visión general de los métodos disponibles o deba clasificarse primero una situación de crisis o asesoramiento.
  Activar también con "qué método terapéutico se adapta", "estructurar asesoramiento", "crisis — qué hacer", "elegir enfoque terapéutico".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: therapy
tags: [therapie, beratung, umbrella, meta, routing]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: [counseling-basics, guideline-therapies-overview, stabilization-techniques, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/therapie-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="therapie-umbrella banner">

# Terapia / Asesoramiento — Umbrella

## Propósito

Punto de entrada para la familia "Terapia / Asesoramiento". Agrupa el enrutamiento general y remite al skill correspondiente para casos especializados. Tres skills de entrada activos forman el frente; detrás se encuentra una serie más larga de métodos especializados desregistrados accesibles a través de `code-skill-index` (catálogo `catalog-therapy.md`).

## Miembros y Enrutamiento

| Skill | Para qué | Cuándo usar este en lugar de los otros |
|-------|----------|----------------------------------------|
| `/stabilization-techniques` | Intervención en crisis, grounding, lugar seguro, PMR, pánico, Ventana de Tolerancia | **Primero** en estrés agudo/crisis — estabilización antes de la metodología |
| `/guideline-therapies-overview` | Visión general de terapias de guía: TCC, ACT, Terapia de Esquemas, Exposición, Sistémica, Psicodinámica | Cuando se deba elegir o explicar el **método** adecuado |
| `/counseling-basics` | Técnicas de conversación: escucha activa, reflejo, validación, MI/OARS, preguntas circulares | Cuando se trate del **CÓMO de la conversación**, no del método terapéutico |
| (skills especiales desregistrados) | Procedimientos individuales (genograma, detalles de exposición, psicología positiva, …) | Cuando se necesite a fondo un procedimiento individual concreto → vía `code-skill-index` |

> Regla de enrutamiento: crisis aguda → `/stabilization-techniques` · elegir/explicar método →
> `/guideline-therapies-overview` · técnica de conversación → `/counseling-basics` · procedimiento individual profundo →
> skill especializado desregistrado vía `code-skill-index`.

## Combinaciones Bien Acopladas

- `/stabilization-techniques` (primero, agudo) → `/guideline-therapies-overview` (después, a medio plazo):
  primero establecer la seguridad/Ventana de Tolerancia, luego elegir el procedimiento de guía adecuado.
- `/counseling-basics` acompaña a **ambos** — la actitud de asesoramiento (MI/OARS, validación) sostiene tanto
  la estabilización como el trabajo metodológico.

## Convenciones Comunes

- No sustituir el diagnóstico médico/clínico; trabajar de forma psicoeducativa y orientada a recursos.
- Ventana de Tolerancia como eje guía: en hiperhiperactivación estabilizar primero, no confrontar.
- Leer los archivos en vivo de los skills individuales antes de la aplicación — este umbrella no reproduce contenidos.

## Changelog

### 0.1.0 (2026-06-17)
- Versión inicial. Generada por el modo de auditoría (1c1) para la familia Terapia / Asesoramiento.
