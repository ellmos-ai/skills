---
name: build-your-users-mind
version: 1.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Enlaza con el módulo público y neutral respecto al proveedor
  build-your-users-mind: un método consciente de la privacidad para crear un
  modelo empírico de preferencias basado en la teoría de la mente de un
  usuario autorizado a partir de sus propios registros de interacción.
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [theory-of-mind, user-model, decision-avatar, feedback, privacy, pointer-skill]
language: es
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "external"
  origin_path: "SKILL.md, templates/, scripts/, schemas/, TAXONOMY.md"
  origin_version: "1.0.0"
  origin_repo: "https://github.com/ellmos-ai/build-your-users-mind"
  last_sync_from_origin: "2026-07-30"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="build-your-users-mind banner">

# build-your-users-mind — referencia pública y neutral

Este skill es una referencia ligera al módulo público
[`ellmos-ai/build-your-users-mind`](https://github.com/ellmos-ai/build-your-users-mind).
El módulo contiene el método completo, plantillas, esquemas, scripts, pruebas y
documentación de adaptadores de origen. Este catálogo no duplica ese código.

## Qué hace el módulo

Con la autorización explícita del operador, el módulo ayuda a un agente a:

1. extraer intervenciones auténticas del usuario de sus propios registros;
2. redactar material sensible antes de guardarlo;
3. reducir y clasificar evidencias sobre preferencias y decisiones recurrentes;
4. crear un modelo local de preferencias con confianza y procedencia;
5. enlazar una referencia breve con el entorno del agente; y
6. calibrar predicciones con comentarios reales posteriores.

El módulo público sirve para cualquier usuario y entorno compatible. No contiene
el modelo de una persona concreta.

## Límite de seguridad y privacidad

- Se requiere autorización antes de leer registros de interacción.
- Perfiles, registros sin procesar, corpus de evidencias y rutas locales siguen
  siendo privados.
- Las predicciones son hipótesis inciertas, no lectura de mente, diagnóstico ni
  declaraciones del usuario.
- Una predicción de preferencias nunca amplía la autoridad del agente.
- Las acciones externas, irreversibles, críticas para la seguridad, legales,
  médicas, laborales, financieras o de impacto similar requieren confirmación
  explícita.
- Las predicciones del agente nunca deben convertirse en evidencia primaria
  sobre el usuario.

## Instalación

```bash
git clone https://github.com/ellmos-ai/build-your-users-mind.git <clone-path>
```

Sigue las instrucciones actuales de `README.md`, `SKILL.md`,
`SOURCE-ADAPTERS.md` y de privacidad del módulo. Mantén el perfil generado
fuera de repositorios públicos. El repositorio del módulo es la autoridad para
implementación y versiones.

## Núcleo público y perfiles privados

`build-your-users-mind` es el nombre público y neutral del módulo.
`decision-avatar` es el protocolo público de ejecución del catálogo. El avatar
de una persona identificada, sus evidencias, comandos locales y valores
específicos son extensiones privadas y no deben publicarse con un nombre
personal.

## Historial de cambios

### 1.0.0 (2026-07-30)

- Añadida la referencia neutral al módulo público independiente.
- Sustituido el perfil personal previamente publicado por un límite estricto
  entre núcleo público y perfil privado.
