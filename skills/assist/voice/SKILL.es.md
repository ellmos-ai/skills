---
name: voice
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Planifica grabación, transcripción y síntesis de voz con herramientas opcionales e intercambiables.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [voice, speech, stt, tts, provider-neutral]
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

<img src="banner.png" width="100%" alt="voice banner">

# Asistente de voz neutral

## Propósito

Definir un flujo de voz sin exigir un proveedor privado.

**Resultado:** Plan con formato de entrada, decisión de privacidad, opciones y alternativa.

## Flujo de trabajo

1. Aclarar el objetivo, el contexto y el formato de salida deseado.
2. Usar solo la información proporcionada en la solicitud actual.
3. Crear un resultado estructurado y verificable.
4. Marcar las suposiciones y pedir confirmación antes de cambios externos.

## Ejemplo

**Entrada:** Planifica un flujo local de transcripción para un archivo de audio.

**Resultado:** Plan con formato de entrada, decisión de privacidad, opciones y alternativa.

## Núcleo público y extensiones privadas

Este skill público contiene únicamente el método transferible. Los adaptadores específicos de aplicaciones, cuentas, rutas locales, bases de datos y ajustes personales deben permanecer en un perfil adicional privado o en un fork privado.

Sin un perfil privado, el skill utiliza solo la información proporcionada explícitamente en la solicitud actual.

## Límites y protección de datos

- Los datos no se guardan de forma predeterminada.
- No se abre ni modifica ninguna fuente, archivo o interfaz sin permiso explícito.
- Antes del procesamiento en la nube deben aclararse el consentimiento, la clasificación y la conservación.

## Registro de cambios

### 2.0.0 (2026-07-30)

- Núcleo público neutral; se eliminaron integraciones privadas y perfiles personales.
