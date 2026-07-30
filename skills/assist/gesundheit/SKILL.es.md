---
name: gesundheit
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Organiza información de salud facilitada voluntariamente y prepara preguntas para profesionales.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [health, organization, questions, safety]
language: es
status: stable
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
---

<img src="banner.png" width="100%" alt="gesundheit banner">

# Organizador de información de salud

## Propósito

Resumir síntomas, evolución, medicación y preguntas de forma objetiva.

**Resultado:** Cronología, observaciones estructuradas, señales de alerta y preguntas médicas.

## Flujo de trabajo

1. Aclarar el objetivo, el contexto y el formato de salida deseado.
2. Usar solo la información proporcionada en la solicitud actual.
3. Crear un resultado estructurado y verificable.
4. Marcar las suposiciones y pedir confirmación antes de cambios externos.

## Ejemplo

**Entrada:** Convierte estas notas de síntomas en una cronología breve para la consulta.

**Resultado:** Cronología, observaciones estructuradas, señales de alerta y preguntas médicas.

## Núcleo público y extensiones privadas

Este skill público contiene únicamente el método transferible. Los adaptadores específicos de aplicaciones, cuentas, rutas locales, bases de datos y ajustes personales deben permanecer en un perfil adicional privado o en un fork privado.

Sin un perfil privado, el skill utiliza solo la información proporcionada explícitamente en la solicitud actual.

## Límites y protección de datos

- Los datos no se guardan de forma predeterminada.
- No se abre ni modifica ninguna fuente, archivo o interfaz sin permiso explícito.
- El skill no diagnostica ni sustituye la atención médica. En peligro agudo se requieren servicios de emergencia locales.

## Registro de cambios

### 2.0.0 (2026-07-30)

- Núcleo público neutral; se eliminaron integraciones privadas y perfiles personales.
