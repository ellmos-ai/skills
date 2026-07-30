---
name: law-checker
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: Apunta al módulo independiente law-checker ("Departamento Legal"): evaluaciones jurídicas preliminares impulsadas por IA fundadas en fuentes para el derecho alemán con un registro de estatutos y un agente de encarnación de estatutos. Utilice esta habilidad cuando una situación, contrato, notificación oficial o pregunta legal bajo el derecho alemán deba ser verificada con citas exactas (artículo/sección, párrafo, frase) -- con un límite claro: orientación inicial asistida por IA, no un sustituto de un abogado.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/law-checker', 'origin_path': 'SKILL.md, config.json, agents/gesetzbuch.md, references/', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [legal, law, germany, wrapper, pointer-skill]
language: es
status: active
---

<img src="banner.png" width="100%" alt="law-checker banner">

> **Español** — Versión oficial en español de `law-checker`.

# law-checker (Departamento Legal) -- Pointer Skill

Esta habilidad es un **puntero ligero (wrapper)** hacia el repositorio del módulo público e independiente [`ellmos-ai/law-checker`](https://github.com/ellmos-ai/law-checker) (licencia MIT, público). La habilidad real reside allí; este repositorio solo se enlaza a ella y documenta la instalación para que el módulo sea descubrible a través del catálogo central de habilidades.

## Lo que hace el módulo

`law-checker` produce evaluaciones jurídicas preliminares basadas en fuentes para el derecho alemán:

- **Registro de leyes (`config.json`):** leyes activables; cada afirmación legal debe estar respaldada por textos legales oficiales recuperados localmente (artículo o sección, párrafo, frase donde sea necesario, cita corta, fuente, fecha de recuperación).
- **Agente de encarnación de estatutos (`agents/gesetzbuch.md`):** un agente genérico que responde "desde el interior de la ley" para cualquier ley registrada; se escala a cualquier estatuto añadido al registro.
- **Capa separada de jurisprudencia:** las decisiones judiciales solo se citan tras la verificación web (tribunal, fecha, número de expediente, ECLI cuando esté disponible).
- **Flujo de trabajo de riesgo y escalado:** formato de informe con una escala de nivel de riesgo, disciplina de plazos y una matriz de enrutamiento por especialidad de abogado.

## Límites (importante)

- **Solo orientación inicial asistida por IA, no sustituye el asesoramiento legal individual y no la realiza un abogado colegiado.**
- No es un despacho de abogados, ni un servicio legal alojado, ni un calendario de plazos.
- Si hay correo legal real involucrado (carta de advertencia, notificación oficial, demanda, plazo): asegure el documento original, tome nota del plazo y consulte a un abogado cualificado — no automatice el asunto.

## Instalación (genérica, sin rutas locales)

1. Clonar el módulo:
   ```bash
   git clone https://github.com/ellmos-ai/law-checker.git <clone-path>
   ```
2. Adoptar `<clone-path>/SKILL.md` en su propio entorno de habilidades (p. ej., `~/.claude/skills/law-checker/` o el equivalente para su entorno de ejecución de agentes).
3. Establecer la ruta del módulo en el `SKILL.md` adoptado y sus referencias a `<clone-path>` — NO envíe rutas locales reales ni nombres de host a un entorno de habilidades versionado.
4. Cargar el registro de leyes: `python <clone-path>/_tools/gesetze_fetch.py` (recupera los textos oficiales configurados; los textos en sí no están en el repositorio para evitar redistribuir capturas obsoletas de portales).
5. Para obtener detalles sobre la estructura, la licencia y la responsabilidad, consulte el README del repositorio del módulo.

## Origen de esta habilidad puntero

Este wrapper se añadió el 23-07-2026 como una entrada de demostración para el repositorio `ellmos-ai/skills`. No hay **duplicación de código** — el mantenimiento y el control de versiones permanecen exclusivamente en el repositorio del módulo `ellmos-ai/law-checker`.

## Registro de cambios

### 0.1.0 (2026-07-23)
- Habilidad puntero inicial para `ellmos-ai/law-checker`.