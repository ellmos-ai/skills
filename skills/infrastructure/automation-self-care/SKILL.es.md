---
name: automation-self-care
version: 1.0.1
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-30
description: >
  Construye y opera un conjunto central de autocuidado neutral respecto al
  proveedor para tareas de LLM programadas y automatizaciones de aplicaciones de
  escritorio. Úsalo cuando un agente deba descubrir su programador nativo,
  instalar verificaciones recurrentes de higiene, calidad de prompt, frecuencia,
  carga, recursos, entre sistemas, permisos y tiempo de ejecución, o mejorar
  continuamente una flota de automatización existente con protección contra
  eliminación, lectura posterior y reversión. Se activa con autocuidado de
  automatización, cuidado de tareas del programador, mantenimiento de
  automatización de aplicaciones de escritorio, auditoría de flotas de
  automatización, programaciones con autocuración, solicitudes para recrear la
  familia de tareas de mantenimiento al estilo ANTIGRAVITY,
  core-set-textautomations, basic-text-automations, textbased-automation-core,
  textbased-automation-drivers o textbased-desktopapp-automations.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system]
language: es
status: active
aliases: [core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
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
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="automation-self-care banner">

> **Español** — Versión oficial en español de `automation-self-care`.

# Automation Self-Care

Crea una flota de mantenimiento nativa y específica del proveedor a partir de un bucle de control neutral respecto al proveedor. Preserva la intención original de la familia de tareas ANTIGRAVITY al tiempo que requiere evidencia, cambios reversibles y lectura posterior nativa.

## Límites no negociables

- Trata el descubrimiento, la planificación, la aprobación, la mutación y la lectura posterior como fases independientes.
- Utiliza la API de automatización, comando o interfaz de usuario admitida por la aplicación de destino. Nunca asumas que editar un archivo de almacenamiento modifica el estado activo de la aplicación.
- Lee las reglas locales, los bloqueos, los registros de eliminación/supresión y las programaciones existentes antes de proponer una tarea.
- No inventes soporte para el programador. Si no se puede probar la creación, actualización o lectura posterior, elabora un plan de instalación manual y detente antes de la mutación.
- Realiza como máximo un cambio de ajuste independientemente comprobable por ejecución de cuidado.
- Protege las tareas de cuidado para que no se desactiven a sí mismas ni reduzcan su propia cadencia por debajo del límite de recuperación configurado.
- Conserva el prompt, la programación, el modelo, los permisos y el estado habilitado anteriores para que cada mutación pueda revertirse.
- Contabiliza el éxito únicamente tras obtener evidencia del resultado, no simplemente al iniciar el programador o recibir un código de salida 0.
- Nunca copies secretos, prompts privados ni datos personales en un registro compartido.

## Flujo de trabajo

### 1. Descubrir la superficie de automatización nativa

Inventaria el actor actual, el proveedor, la clase de aplicación, la superficie del programador, las operaciones admitidas, los archivos de estado, el historial de ejecución, la telemetría de uso y el método de lectura posterior. Registra las capacidades utilizando el contrato de perfil en [provider-adapter-contract.md](references/provider-adapter-contract.md).

Distingue entre programaciones nativas de aplicaciones de escritorio, ejecución CLI/headless, programador de SO o iniciador de servicios, servicio de programador general, motor de flujo de trabajo y automatización no admitida o solo por UI. No equipares la existencia de un archivo de configuración con una ruta de mutación admitida.

### 2. Inventariar la flota

Para cada tarea, captura un identificador local estable, propósito, huella digital del prompt, programación, estado habilitado, modelo, permisos, rutas de destino, último evento del programador, último resultado exitoso y propietario actual. Mantén el contenido del prompt de forma local.

Verifica la superficie activa autoritativa dos veces antes de la mutación cuando la aplicación pueda reescribir el estado desde la memoria.

### 3. Diseñar el conjunto central (core set)

Lee [core-set.md](references/core-set.md). Selecciona una de las siguientes opciones:

- `compact`: cinco tareas de cuidado que combinan la frecuencia con la distribución de carga; o
- `full`: nueve tareas enfocadas correspondientes a la familia de mantenimiento original.

Genera un plan neutral respecto al proveedor:

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
```

El generador nunca instala tareas. Revisa cada capacidad marcada como `blocked` y elige horarios locales sin colisiones antes de aplicar el plan.

### 4. Preparar la instalación

Instala a través del adaptador de proveedor nativo:

1. Comienza con la higiene en modo de solo lectura.
2. Añade protección de recursos.
3. Añade ajuste de calidad del prompt con opción de reversión.
4. Añade ajuste de frecuencia y carga solo después de tener suficiente evidencia de ejecución.
5. Añade la coordinación entre sistemas al final.

Crea tareas nuevas o importadas desactivadas a menos que el usuario haya aprobado explícitamente la instalación activa. Para una prueba piloto no supervisada, requiere primero un registro de eliminación, una instantánea del estado previo, un recibo de ejecución y una ruta de reversión.

### 5. Ejecutar el bucle de cuidado

Cada tarea de cuidado sigue esta secuencia:

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

Utiliza el catálogo de hipótesis y las reglas de evidencia en [core-set.md](references/core-set.md). Una causa desconocida significa observar, restringir permisos o pausar de forma segura; nunca adivines una reparación.

### 6. Coordinar entre actores

Mantén el estado de la aplicación local como autoritativo. Comparte únicamente los contratos de tareas, la cobertura, el estado, los recibos y las huellas digitales sanitizadas. Se permiten revisiones redundantes de solo lectura; las mutaciones de un solo escritor requieren una reclamación o un bloqueo nativo equivalente.

### 7. Sistemas sin enlaces de eventos nativos (Extensión Letter-Hooker)

Trata la limitación de tokens o suscripciones como un estado de capacidad, no como un actor defectuoso. Devuelve la cobertura delegada después de que el actor original produzca un recibo exitoso.

## Resultados requeridos

Para cada configuración o ejecución de cuidado, informa:

- superficie nativa descubierta y capacidades no admitidas;
- topología seleccionada y tareas creadas, propuestas u omitidas;
- mutación exacta y lectura posterior antes/después;
- evidencia del resultado o ventana de observación abierta;
- ubicación de reversión y condición de retorno;
- actualización de cobertura compartida, si existe un registro de coordinación.

## Ejemplo

Usuario: "Configura programaciones automantenidas en esta aplicación de escritorio."

Descubre si la aplicación puede listar, crear, actualizar y verificar tareas programadas. Genera el plan compacto, presenta las capacidades no admitidas y luego instala únicamente las tareas aprobadas a través de la superficie nativa. Una carpeta que contenga un prompt de tarea sin un registro en el programador activo no constituye una configuración completada.

## Registro de cambios

### 1.0.1 (2026-07-30)

- Se añadieron alias de automatización de texto neutrales respecto al proveedor y automatización de aplicaciones de escritorio.

### 1.0.0 (2026-07-28)

- Se consolidó la familia de mantenimiento original de ANTIGRAVITY, el bucle de control F1-F6 y adaptaciones posteriores específicas de proveedores en una habilidad de conjunto central neutral.