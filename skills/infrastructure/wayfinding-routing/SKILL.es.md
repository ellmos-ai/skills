---
name: wayfinding-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: Habilidad universal de navegación, orientación y resiliencia de emergencia para agentes LLM. Proporciona heurísticas activas de navegación, autoorientación y recuperación cuando los agentes enfrentan desviación de contexto, herramientas fallidas, bucles o caminos sin salida.
standalone: true
anthropic_compatible: true
bach_compatible: true
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, autoorientacion, resiliencia, recuperacion, heuristicas]
language: es
status: active
---

> **Español** — Documentación oficial completa traducida al español para la habilidad `wayfinding-routing`.

# Navegación y Orientación (Wayfinding-Routing)

La habilidad **Wayfinding-Routing** (también conocida como **`survival-routing`**, **`dead-reckoning`**, **`pathfinder-routing`** y **`celestial-routing`**) sirve como el marco definitivo de navegación y recuperación de emergencia para agentes LLM.

Equipa a los agentes con heurísticas proactivas de orientación durante la ejecución normal y con protocolos de emergencia cuando se enfrentan a desviaciones de contexto, errores de ejecución recurrentes, fallos de API o caminos sin salida.

---

## Resumen de Sinónimos y Estrategias

| Estrategia de Sinónimo | Metáfora y Principio Fundamental | Caso de Uso Aplicado |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (Principal) | **Orientación Espacial:** Navegar sin GPS externo leyendo señales y pistas ambientales. | Bucle principal de navegación para sidecars, `workflowhooker` y `automation-self-care`. |
| **`survival-routing`** | **Navegación de Supervivencia:** Interrupción de circuito y degradación gradual cuando fallan las herramientas. | Recuperación de emergencia cuando los comandos expiran, fallan repetidamente o chocan con permisos. |
| **`dead-reckoning`** | **Navegación por Estima (Koppelnavigation):** Reconstruir el estado exacto paso a paso a partir de migas de pan. | Seguimiento de pasos de ejecución en archivos temporales o `TODO.md` para permitir un retroceso preciso. |
| **`pathfinder-routing`** | **Explorador / Pionero:** Inspección previa y apertura de caminos para equipos multi-agente. | Inspección previa de árboles de directorios, bloqueos y dependencias de tareas. |
| **`celestial-routing`** | **Navegación Astronómica:** Alineación con documentos ancla inmutables cuando el contexto local tiene ruido. | Recuperación con respaldo en `CLAUDE.md`, `AGENTS.md`, `START.md` cuando las instrucciones del prompt chocan. |

---

## Los 5 Protocolos Principales de Emergencia y Orientación

### 1. `PROTOCOL-ANCHOR-RESET` (Reinicio de Ancla / Navegación Astronómica)
- **Disparador (Trigger):** Desviación de contexto, instrucciones contradictorias del usuario o pérdida de orientación en sesiones largas.
- **Regla Heurística:** Detener la generación de texto libre. Limpiar suposiciones transitorias. Releer los documentos ancla raíz (`CLAUDE.md`, `AGENTS.md`, `START.md`). Restablecer el estado del objetivo a la directiva raíz autorizada antes de tomar cualquier otra medida.

### 2. `PROTOCOL-STOP-EXPLAIN` (Bucle de Reflexión y Explicación)
- **Disparador (Trigger):** Un comando de terminal, edición de archivo o solicitud de API falla dos veces con un error idéntico.
- **Regla Heurística:** **Bloquear la ejecución de comandos.** El agente DEBE emitir una reflexión escrita formal antes de intentar un tercer intento:
  1. *¿Qué error exacto ocurrió en los intentos 1 y 2?*
  2. *¿Por qué falló la hipótesis de diagnóstico anterior?*
  3. *¿Cuál es el nuevo enfoque alternativo?*
  La ejecución se desbloquea ÚNICAMENTE después de escribir esta justificación explícita.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Cascada de Degradación Gradual)
- **Disparador (Trigger):** La herramienta principal, el servidor MCP o la API externa no está disponible o devuelve errores.
- **Regla Heurística:** Nunca fallar abruptamente ni entrar en bucles a ciegas. Degradar por niveles:
  - **Nivel 1 (Óptimo):** API nativa completa / Herramienta MCP
  - **Nivel 2 (Herramienta de Reserva):** CLI local en Python / Script
  - **Nivel 3 (Estado de Solo Lectura):** Análisis directo de archivos (`view_file` / texto plano)
  - **Nivel 4 (Transferencia):** Presentar un informe de estado estructurado y opciones abiertas al usuario.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Retroceso por Migas de Pan)
- **Disparador (Trigger):** Un flujo de trabajo complejo o una refactorización encuentra un bloqueo insuperable en el paso N.
- **Regla Heurística:** Registrar migas de pan antes de realizar cambios destructivos. Si una ruta falla:
  1. Revertir los cambios no confirmados (`git checkout` / restaurar estado).
  2. Saltar al último punto de control limpio de migas de pan.
  3. Marcar la ruta fallida como bloqueada en `TODO.md`.
  4. Intentar la ruta alternativa B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Interruptor de Circuito y Salida Segura)
- **Disparador (Trigger):** Se alcanzan los límites de ejecución, se detecta un bucle infinito o se produce un error crítico del sistema.
- **Regla Heurística:** Ejecutar la secuencia de apagado de emergencia:
  1. Liberar todos los bloqueos de archivos y git adquiridos (`python -m workflowhooker check`).
  2. Guardar el estado parcial actual en `.SYNC/SURVIVAL_STATE.json` o `AUTOMATIONS-MEMORY.md`.
  3. Registrar el incidente en `ANTIGRAVITY-LOG.txt`.
  4. Salir de forma segura con un resumen ejecutable para el usuario o el orquestador.