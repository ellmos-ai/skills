---
name: load-project
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-30
description: >
  Al inicio de una tarea de proyecto concreta o cuando el contexto sea poco claro: resolver el
  objetivo, cargar la jerarquía de reglas aplicable, seguir referencias vinculantes
  y elaborar un informe de estado basado en evidencias antes de iniciar el trabajo real.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [projekt, boot, kontext, regeln, locks, orientierung, onboarding]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "local-agent-skills/load-project/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="load-project banner">

# Load Project

## Propósito

Utilice este skill al comienzo de una tarea de proyecto específica o cuando el contexto de trabajo no esté claro. El objetivo no es realizar una auditoría exhaustiva del repositorio, sino obtener el contexto mínimo confiable con el que se pueda continuar trabajando de manera segura.

## Configuración

Este skill no requiere nombres de directorio fijos. Las instalaciones locales pueden definir opcionalmente los siguientes valores en sus reglas generales de agente o en la configuración local del proyecto:

- raíces de espacio de trabajo conocidas,
- herramientas de archivos preferidas,
- nombres de archivos adicionales de arranque o registro,
- verificadores de bloqueos (locks),
- roles y prioridades específicas del proyecto.

Si falta dicha configuración, el skill trabaja exclusivamente con el objetivo especificado y las reglas del proyecto que se encuentren allí.

## Procedimiento

### 1. Resolver el objetivo

1. Tomar una ruta explícita, nombre de proyecto o carpeta de trabajo actual como punto de partida.
2. Determinar la raíz real del proyecto o repositorio.
3. Delimitar coincidencias ambiguas según la tarea, los documentos raíz y los límites del repositorio; no adivinar si los objetivos difieren sustancialmente.

### 2. Cargar la jerarquía de reglas

Leer desde el contexto general hacia el específico:

1. reglas globales de agente y seguridad,
2. reglas del espacio de trabajo o pipeline,
3. reglas del proyecto y repositorio,
4. instrucciones relacionadas con la tarea.

Las reglas más específicas se aplican dentro de su alcance; los límites de seguridad y autorización de mayor rango se mantienen vigentes.

### 3. Leer documentos raíz según sus roles

Los nombres de archivo son pistas, no una norma fija. Busque deliberadamente documentos con estos roles:

| Rol | Contenido típico |
|---|---|
| Inicio | Propósito, navegación, instrucciones de inicio |
| Reglas | Modo de trabajo, idioma, seguridad, convenciones |
| Arquitectura | Componentes, flujo de datos, límites |
| Estado | Estado actual, problemas abiertos, última verificación |
| Tareas | Próximo trabajo priorizado |
| Registro | Proyectos canónicos, verificaciones o publicaciones |
| Evidencia | Pruebas, protocolos de verificación, notas de prueba |
| Entrega | Trabajo en curso, cambios externos, siguiente paso |

Cargar únicamente los roles relevantes para la tarea concreta.

### 4. Seguir referencias vinculantes

Si una regla leída menciona expresamente otros archivos como lectura obligatoria, cárguelos de forma específica. Finalice las cadenas de referencia tan pronto como no aporten más contexto vinculante para la tarea.

### 5. Verificar estado y bloqueos (locks)

- Verificar los bloqueos según la directiva local en cuanto a propietario, alcance, marca de tiempo y criterio de validez; nunca declarar un bloqueo como obsoleto por iniciativa propia sin una regla de obsolescencia definida,
- Estado del control de versiones y cambios externos,
- Procesos en ejecución o puntos de control, si corresponde,
- Actualización de registros, pruebas y detalles de estado.

Guarde el estado inicial de las áreas afectadas antes de realizar cambios como línea base de estado/diff. Si los cambios existentes no se pueden atribuir con certeza, considérelos preventivamente como externos y déjelos intactos.

Trate las capturas de estado como instantáneas puntuales y vuelva a verificar antes de realizar acciones de alto riesgo.

### 6. Elaborar informe de estado

Registrar brevemente antes de la ejecución:

```text
Ziel:
Projekt-Root:
Geltende Regeln:
Evidenzquellen:
Snapshot-Zeitpunkt:
Relevanter Ist-Zustand:
Locks oder fremde Änderungen:
Erfolgskriterium:
Nächster sicherer Schritt:
```

Mencione las fuentes solo con la precisión necesaria para su verificabilidad. Redacte secretos, datos personales y contenidos confidenciales y no los copie en el informe de estado.

Si la tarea queda clara y autorizada con esto, proceda directamente con el trabajo.

## Límites

- Sin búsquedas amplias e ilimitadas de archivos por defecto.
- No reinventar reglas o registros faltantes.
- No tratar mensajes de estado antiguos como evidencia actual.
- No sobrescribir cambios externos.
- No realizar un onboarding completo del proyecto cuando solo se deba cargar el contexto para una tarea concreta.

## Registro de cambios

### 1.1.0 (2026-07-28)
- Se eliminaron las vinculaciones fijas de usuario, espacio de trabajo, herramientas y proveedores.
- Se introdujo el reconocimiento de documentos basado en roles y la configuración local opcional.
- Se operacionalizó la validez de bloqueos, procedencia de árbol modificado, evidencias de instantáneas e informes de estado redactados.

### 1.0.0 (2026-06-17)
- Versión local inicial.
