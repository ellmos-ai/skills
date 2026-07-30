---
name: orchestrator
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: Protocolo neutral en cuanto a proveedores para descomponer tareas complejas, encargar workers independientes y verificar de forma basada en evidencia sus resultados.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [orchestrierung, multi-agent, delegation, evidenz, checkpoint, workflow]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'local-agent-skills/orchestrator/', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="orchestrator banner">

> **Español** — Versión oficial en español de `orchestrator`.


# Orchestrator (Español)

## Descripción general y propósito

Utiliza este skill cuando una tarea conste de al menos dos paquetes de trabajo ampliamente independientes y la delegación aporte una ventaja real de tiempo, contexto o calidad. Para tareas pequeñas y estrechamente acopladas, trabaja directamente.

El skill describe un protocolo. El inicio, la interrupción y la reanudación concretos de los workers se realizan a través de las capacidades del runtime correspondiente.

## Límite de autoridad

La delegación no amplía los permisos. Cada worker recibe como máximo el alcance y los derechos de modificación que ya se aplican a la tarea principal. Las acciones externas, irreversibles o que requieran aprobación de otro modo permanecen sujetas a aprobación.

## Procedimiento

### 1. Evaluar la situación

1. Registrar el objetivo, los criterios de éxito y las exclusiones de la tarea principal.
2. Comprobar las reglas del proyecto, bloqueos, cambios en curso y presupuestos disponibles.
3. Antes del dispatch, guardar el estado actual de bloqueos, estado y diff de las áreas afectadas como baseline. Solo así se pueden distinguir posteriormente con fiabilidad los cambios externos existentes de los cambios del worker.
4. Paralelizar solo aquellos paquetes de trabajo que sean lo suficientemente independientes.
5. Separar las áreas de escritura superpuestas o procesarlas secuencialmente.

### 2. Escribir el contrato de encargo

Antes de cada dispatch, crear un contrato breve y verificable:

| Campo | Contenido obligatorio |
|---|---|
| Identificador | ID estable del paquete de trabajo |
| Objetivo | exactamente un resultado concreto |
| Entradas | archivos, datos o fuentes de contexto relevantes |
| Alcance positivo | lo que se permite leer o modificar |
| Alcance negativo | lo que permanece expresamente sin tocar |
| Criterio de éxito | condición observable para "hecho" |
| Evidencia | prueba esperada, como test, diff o referencia |
| Formato de respuesta | mensaje de finalización compacto y estructurado |

Un worker recibe únicamente el contexto necesario para este contrato.

### 3. Ejecutar y observar

- Mantener un fan-out pequeño y aumentarlo solo si existe un beneficio independiente.
- Seguir el progreso a través del estado del runtime o un checkpoint habitual del proyecto.
- En caso de conflictos, ampliación del alcance o falta de autoridad, detenerse y escalar.
- Un worker fallido no debe bloquear automáticamente paquetes de trabajo independientes.

### 4. Verificar resultados

Una notificación de finalización es inicialmente una afirmación. El orchestrator lo verifica por sí mismo:

1. ¿Existe el artefacto afirmado o el cambio mencionado?
2. ¿Pertenece al alcance acordado?
3. ¿Pasa actualmente el test o la prueba acordada?
4. ¿Se respetaron los cambios externos, bloqueos y alcances negativos?
5. ¿Se contradicen los resultados de diferentes workers?

Solo entonces se considera completado un paquete de trabajo.

### 5. Integrar y asegurar

- Resolver los conflictos de forma consciente; no concatenar resultados a ciegas.
- Volver a ejecutar los tests globales necesarios tras la integración.
- Identificar claramente los paquetes pendientes, fallidos y pospuestos.
- En ejecuciones prolongadas, guardar el objetivo, estado, evidencia y siguiente paso en un checkpoint recuperable.

## Prompt mínimo del Worker

```text
Auftrag: <Kennung und Ziel>
Eingaben: <Quellen>
Du darfst: <positiver Scope>
Du darfst nicht: <negativer Scope>
Fertig, wenn: <prüfbares Kriterium>
Belege mit: <Test, Diff oder Fundstelle>
Antworte als: <Rückgabeformat>
```

## Condiciones de parada

Detener solo el paquete de trabajo afectado si su alcance, autoridad o evidencia no están claros. Los paquetes independientes y seguros pueden continuar ejecutándose.

Detener toda la delegación si:

- las subtareas ya no son independientes,
- no se puede separar con seguridad un área de escritura compartida,
- las reglas, bloqueos o autoridad para todo el alcance restante no están claros,
- los costes previstos superan el beneficio reconocible,
- no se puede generar o verificar la evidencia requerida.

## Registro de cambios

### 1.1.0 (2026-07-28)
- Se eliminaron las vinculaciones de usuario, ruta, modelo y proveedor.
- Se detallaron el contrato de encargo, el límite de autoridad, la verificación de evidencias y los checkpoints como mecánica central portable.
- Se separó explícitamente la baseline para cambios externos, así como las paradas locales de paquete y globales.

### 1.0.0 (2026-06-17)
- Versión inicial local.