---
name: finanz-versicherung
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Estructura documentos financieros y de seguros proporcionados en un resumen y una lista neutrales.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [finance, insurance, documents, checklist]
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

<img src="banner.png" width="100%" alt="finanz-versicherung banner">

# Resumen financiero y de seguros

## Propósito

Ordenar contratos, plazos, documentos y preguntas sin asesoramiento ni recomendaciones de productos.

**Resultado:** Resumen factual, lista de plazos y preguntas para un profesional cualificado.

## Flujo de trabajo

1. Aclarar el objetivo, el contexto y el formato de salida deseado.
2. Usar solo la información proporcionada en la solicitud actual.
3. Crear un resultado estructurado y verificable.
4. Marcar las suposiciones y pedir confirmación antes de cambios externos.

## Ejemplo

**Entrada:** Crea una lista de renovación con estos datos contractuales anonimizados.

**Resultado:** Resumen factual, lista de plazos y preguntas para un profesional cualificado.

## Núcleo público y extensiones privadas

Este skill público contiene únicamente el método transferible. Los adaptadores específicos de aplicaciones, cuentas, rutas locales, bases de datos y ajustes personales deben permanecer en un perfil adicional privado o en un fork privado.

Sin un perfil privado, el skill utiliza solo la información proporcionada explícitamente en la solicitud actual.

## Límites y protección de datos

- Los datos no se guardan de forma predeterminada.
- No se abre ni modifica ninguna fuente, archivo o interfaz sin permiso explícito.
- El skill no sustituye el asesoramiento financiero, fiscal, jurídico o de seguros.

## Registro de cambios

### 2.0.0 (2026-07-30)

- Núcleo público neutral; se eliminaron integraciones privadas y perfiles personales.
