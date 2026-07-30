---
name: system-onboarding
version: 1.2.0
type: skill
author: ellmos contributors
created: 2026-05-16
updated: 2026-07-29
description: >
  Protocolo de incorporación agnóstico del proveedor para una estación de trabajo nueva, reconstruida o de reemplazo.
  Establece los requisitos previos del sistema operativo, entornos de ejecución de agentes, superficies de reglas
  compartidas, habilidades portátiles, configuración verificada y evidencias posteriores a la instalación sin copiar
  credenciales, prompts privados o configuraciones específicas del host en un repositorio.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [onboarding, setup, agent-runtimes, windows, macos, verification, sync]
language: es
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "internal onboarding protocol (sanitized for portable publication)"
  origin_version: "1.2.0"
  last_sync_from_origin: "2026-07-29"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="system-onboarding banner">

> **Español** — Versión oficial en español de `system-onboarding`.

# Incorporación del sistema

Use este protocolo para configurar una estación de trabajo nueva o reconstruida para trabajo con agentes de prioridad local (local-first). Es una guía de secuenciación y verificación, no un instalador ni una fuente de credenciales. Consulte las instrucciones específicas de cada producto en la documentación actual del proveedor antes de modificar un sistema en vivo.

## Activación

Utilícelo para una estación de trabajo nueva, un sistema operativo reinstalado, un dispositivo de reemplazo o la recuperación controlada de un entorno de ejecución de agentes. Primero identifique el sistema operativo, el entorno de ejecución objetivo, el propietario, la superficie de reglas compartida y si la solicitud es una reconstrucción completa o una reparación acotada de componentes. No asuma que una configuración copiada de un host es segura o compatible en otro.

## Flujo de trabajo ordenado

1. Establezca las actualizaciones del sistema operativo, Git, control de código fuente autenticado, Python y la versión Node.js LTS compatible actual donde sea necesario.
2. Instale únicamente los entornos de ejecución de agentes solicitados a través de sus instaladores compatibles y complete sus flujos de inicio de sesión nativos sin colocar tokens en archivos del proyecto.
3. Cree directorios raíz de configuración local y cargue una superficie de reglas canónica seleccionada explícitamente. Combine plantillas; nunca sobrescriba a ciegas el estado local existente.
4. Instale habilidades portátiles y configuraciones de MCP o complementos solo a través de sus procedimientos de despliegue indicados. Trate el formato de configuración de cada proveedor como distinto.
5. Configure la sincronización compartida solo después de que el entorno de ejecución local funcione. Comparta contratos y recibos sanitizados, no credenciales, prompts completos o rutas locales de la máquina.
6. Recree un programador de tareas o automatización solo a través de su superficie nativa compatible. Conserve el estado anterior y mantenga el nuevo trabajo desactivado hasta que su propietario apruebe la activación.
7. Ejecute las comprobaciones posteriores a la instalación correspondientes y escriba un recibo local que distinga la instalación, la configuración, el registro del programador y el resultado exitoso.

Lea únicamente la referencia correspondiente para la plataforma objetivo:

- [Visión general](references/overview.md) para límites y ubicación de datos;
- [Lista de verificación de Windows](references/windows-checklist.md) para Windows;
- [Lista de verificación de macOS](references/mac-checklist.md) para macOS; y
- [Post-instalación](references/post-install.md) para verificación y recuperación.

## Límites

- Nunca publique credenciales, códigos de recuperación, prompts privados, identificadores de cuenta o registros sin procesar en un repositorio compartido o carpeta de sincronización.
- Mantenga los entornos virtuales, las cachés de dependencias y los artefactos de ejecución grandes fuera de las carpetas de proyectos sincronizadas en la nube.
- No convierta una configuración copiada en autoritativa. El host de destino debe descubrir y releer su propio estado compatible.
- No registre una programación simplemente porque exista un archivo de tarea. El registro nativo y las evidencias del resultado son requisitos independientes.
- Cuando se esté reparando un host existente, realice un inventario de su estado actual y sus bloqueos antes de cambiar cualquier configuración.

## Evidencia de finalización

Un recibo de incorporación completo registra el sistema operativo de destino, los entornos de ejecución seleccionados, sus versiones verificadas, las referencias de reglas canónicas cargadas, las habilidades o extensiones explícitas desplegadas, las capacidades no compatibles y cualquier decisión diferida del usuario. La salida exitosa de un comando por sí sola no es evidencia de que una aplicación haya cargado su nueva configuración o de que una tarea programada haya logrado el resultado previsto.

## Historial de cambios

### 1.2.0 (2026-07-29)

- Se portó la secuencia de incorporación reutilizable y las referencias de plataforma al catálogo público de habilidades tras eliminar rutas específicas del host, detalles de cuenta y material operativo privado.