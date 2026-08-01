---
name: foerderplaner
version: 2.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Planifica enseñanza, actividades y apoyo individual sin generador de informes ni plantillas personales.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: education
tags: [education, support, lesson-planning, differentiation]
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

<img src="banner.png" width="100%" alt="foerderplaner banner">

# Planificador de enseñanza y apoyo

## Propósito

Convertir la situación inicial y el objetivo en pasos concretos y revisables.

**Resultado:** Objetivos, medidas, diferenciación, criterios de observación y fechas de revisión.

## Flujo de trabajo

1. Aclarar el objetivo, el contexto y el formato de salida deseado.
2. Usar solo la información proporcionada en la solicitud actual.
3. Crear un resultado estructurado y verificable.
4. Marcar las suposiciones y pedir confirmación antes de cambios externos.

## Ejemplo

**Entrada:** Planifica cuatro semanas de apoyo a la comprensión lectora para un grupo anonimizado.

**Resultado:** Objetivos, medidas, diferenciación, criterios de observación y fechas de revisión.

## Núcleo público y extensiones privadas

Este skill público contiene únicamente el método transferible. Los adaptadores específicos de aplicaciones, cuentas, rutas locales, bases de datos y ajustes personales deben permanecer en un perfil adicional privado o en un fork privado.

Sin un perfil privado, el skill utiliza solo la información proporcionada explícitamente en la solicitud actual.

## Límites y protección de datos

- Los datos no se guardan de forma predeterminada.
- No se abre ni modifica ninguna fuente, archivo o interfaz sin permiso explícito.
- El skill no crea informes de apoyo, certificados ni evaluaciones oficiales. Los informes generales pueden realizarse aparte con `report-forge`; las plantillas personales siguen siendo privadas.

## Registro de cambios

### 2.0.0 (2026-07-30)

- Núcleo público neutral; se eliminaron integraciones privadas y perfiles personales.
