---
name: dev-cycle
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-06-13
description: Ciclo de desarrollo de 8 fases: Solicitudes de funciones, estado actual, planificación funcional, frontend, planificación de backend, código de backend, pruebas, casos de uso. Marco iterativo para el desarrollo sistemático de software.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="dev-cycle banner">
> **Español** — Versión oficial en español de `dev-cycle`.

# Ciclo de Desarrollo (Dev Cycle) (Español)

> **Objetivo:** Proceso estructurado desde la solicitud de funciones hasta el sistema validado.
> Cada desarrollo pasa por estas 8 fases.

---

## Resumen y propósito

```
  +--------------------------------------------------------------+
  |                    CICLO DE DESARROLLO                       |
  +--------------------------------------------------------------+
  |                                                                |
  |  Fase 1   Solicitudes de funciones (Requisitos funcionales)    |
  |     |                                                          |
  |     v                                                          |
  |  Fase 2   Comprobar estado actual (¿Qué existe ya?)             |
  |     |                                                          |
  |     v                                                          |
  |  Fase 3   Planificación funcional                              |
  |            (Workflows, Agentes, Expertos, Habilidades, Servicios)|
  |     |                                                          |
  |     v                                                          |
  |  Fase 4   Implementar Frontend funcional                       |
  |            (Archivos de habilidades, markdown, perfiles agentes) |
  |     |                                                          |
  |     v                                                          |
  |  Fase 5   Planificar y alinear Backend                           |
  |            (Manejadores CLI, esquema DB, puntos finales API)   |
  |     |                                                          |
  |     v                                                          |
  |  Fase 6   Implementar tareas de Backend                        |
  |            (Código Python, herramientas, migraciones DB)       |
  |     |                                                          |
  |     v                                                          |
  |  Fase 7   Pruebas técnicas y correcciones de errores           |
  |            (Pruebas B/O/E, protocolo bugfix)                   |
  |     |                                                          |
  |     v                                                          |
  |  Fase 8   Prueba funcional y de funciones: CASOS DE USO        |
  |            (Validación de extremo a extremo desde perspectiva  |
  |             del usuario)                                       |
  |                                                                |
  +--------------------------------------------------------------+

  Principios fundamentales en todo el proceso:
  - Descripción funcional primero (antes del código)
  - CLI Primero (todo controlable vía terminal)
  - Clara separación de datos de usuario y datos del sistema
```

---

## Fase 1: Solicitudes de funciones (Requisitos funcionales)

**Qué:** Recopilar y formular requisitos funcionales.

**Entrada:**
- Deseos, ideas y problemas del usuario
- Sugerencias de socios (asistentes LLM)
- Información procedente de casos de uso (¡bucle de retroalimentación!)

**Salida:**
- Tareas en el sistema de tareas (por ejemplo, como problema/issue, ticket o lista TODO)
- Los requisitos describen QUÉ se desea, no CÓMO

**Reglas:**
- Formular siempre los requisitos funcionalmente ("El usuario puede hacer X")
- No técnicamente ("Implementar endpoint REST para X")
- Usar casos de uso como fuente de requisitos (Fase 8 -> Fase 1)

---

## Fase 2: Comprobar estado actual

**Qué:** Inventario de la funcionalidad existente.

**Lista de verificación:**
```
  [ ] Buscar herramientas/scripts existentes
  [ ] Revisar documentación/ayuda sobre el tema
  [ ] Comprobar habilidades/agentes/servicios existentes
  [ ] Comprobar esquema de DB (si corresponde)
  [ ] Revisar casos de uso: ¿se ha probado algo similar?
```

**Salida:**
- Documentación de lo que existe, lo que falta y lo que necesita extensión
- Evitar duplicaciones

---

## Fase 3: Planificación funcional

**Qué:** Planificar a nivel funcional: NO escribir código de inmediato.

**Niveles de planificación:**

| Nivel | Pregunta | Artefacto |
|-------|----------|-----------|
| Workflow | ¿CUÁNDO/CÓMO se realiza la coordinación? | workflows/*.md |
| Agente | ¿QUIÉN ejecuta? | agents/*.txt |
| Experto | ¿QUIÉN tiene el conocimiento del dominio? | experts/*/ |
| Habilidad (Skill) | ¿QUÉ se hace? | skills/*.md |
| Servicio | ¿CÓMO se hace técnicamente? | services/*/ |

**Reglas:**
- Pensar funcionalmente primero, luego técnicamente
- Los flujos de trabajo describen procesos, no detalles de implementación
- Cada agente necesita un perfil claro
- Los servicios deben funcionar sin datos de usuario

---

## Fase 4: Implementar Frontend funcional

**Qué:** Crear archivos de habilidades, markdown de flujo de trabajo, perfiles de agente.

El "frontend" aquí es la capa de descripción funcional:
- Archivos de flujo de trabajo (.md)
- Perfiles de agente (.txt)
- Conocimiento de expertos
- Descripciones de servicios
- Archivos de ayuda

**Salida:**
- Existen todas las descripciones funcionales
- Un socio LLM podría leer y entender el flujo de trabajo
- La capa funcional está totalmente documentada

---

## Fase 5: Planificar y alinear Backend

**Qué:** Alinear la arquitectura técnica con el frontend funcional.

**Áreas de planificación:**

| Área | Pregunta | Ubicación |
|------|----------|-----------|
| Manejadores CLI | ¿Qué comandos? | handlers/*.py |
| Esquema DB | ¿Qué tablas/columnas? | schema/*.sql |
| Endpoints API | ¿Qué endpoints de GUI? | server.py |
| Herramientas | ¿Qué scripts de Python? | tools/*.py |

**Salida:**
- Plan técnico alineado con el frontend funcional
- Diseño de esquema de DB
- Estructura de comandos CLI

---

## Fase 6: Implementar tareas de Backend

**Qué:** Escribir código Python, migraciones de base de datos, manejadores CLI.

**Lista de verificación (por tarea):**
```
  [ ] ¿Funciona sin datos de usuario (DB vacía)?
  [ ] ¿Comando CLI disponible?
  [ ] ¿La entrada puede venir de archivos/carpetas?
  [ ] ¿La salida va a una DB estructurada?
  [ ] ¿El escaneo/importación es repetible (idempotente)?
  [ ] ¿Sin rutas codificadas de forma rígida?
  [ ] ¿Herramienta registrada y documentada?
  [ ] ¿Archivo de ayuda creado?
```

---

## Fase 7: Pruebas técnicas y correcciones de errores

**Qué:** Garantizar la corrección técnica.

**Tipos de prueba (B/O/E):**

| Tipo | Perspectiva | Descripción |
|------|-------------|-------------|
| Pruebas B | Externa/Automatizada | Pruebas automatizadas, CI/CD |
| Pruebas O | Funcional (Entrada->Salida) | Verificación funcional manual |
| Pruebas E | Subjetiva/Experiencia | Evaluación de UX, ergonomía |

**Ante errores:**
- Aplicar el protocolo bugfix
- Observar la regla de los 20 minutos (cambiar de enfoque tras 20 min)
- Documentar lecciones aprendidas

---

## Fase 8: Prueba funcional y de funciones - CASOS DE USO

**Qué:** Validación de extremo a extremo desde la perspectiva del usuario.

**Los casos de uso sirven para AMBOS propósitos:**
1. **Indicadores de funciones** - ¿Qué se desea? ¿Qué debería ser posible?
2. **Escenarios de prueba** - ¿Funciona realmente de la A a la Z?

**Formato de caso de uso:**
```
  CASO_DE_USO_NNN: Título corto

  PRECONDICIÓN: ¿Qué debe estar listo?
  ENTRADA:      ¿Qué ingresa el usuario / qué datos?
  ESPERADO:     ¿Cuál debería ser el resultado?
  PRUEBAS:      ¿Qué componentes se prueban?
```

**Bucle de retroalimentación:**
- Casos de uso fallidos -> nuevas tareas en la Fase 1
- Casos de uso exitosos -> funciones validadas
- Nuevas ideas de casos de uso -> capturar como tareas

---

## Resumen: El ciclo

```
  Fase 8 (Casos de uso)
       |
       | Nuevos requisitos / errores
       v
  Fase 1 (Solicitudes funciones) -->  Fase 2 (Estado actual)
       ^                                    |
       |                                    v
  Fase 7 (Pruebas/Errores)       Fase 3 (Planificación funcional)
       ^                                    |
       |                                    v
  Fase 6 (Código Backend)        Fase 4 (Frontend funcional)
       ^                                    |
       |                                    v
       +──────────────────── Fase 5 (Planificación Backend)
```

El ciclo es un bucle: los casos de uso validan funciones y simultáneamente generan nuevos requisitos.

---

## Habilidades específicas por fase

| Fase | Habilidad especializada | Activador |
|------|-------------------------|-----------|
| Fases 1-3 | Project bootstrapper (si está disponible) | Crear un nuevo proyecto |
| Fase 2 | [project-onboarding](../project-onboarding/SKILL.es.md) | Asumir un proyecto existente |
| Fases 2-3 | [docs-analysis](../docs-analysis/SKILL.es.md) | Verificar documentos de requisitos contra código |
| Fases 5-6 | [pipeline-optimizer](../pipeline-optimizer/SKILL.es.md) | Renovar estructuras existentes |
| Fase 7 | [bugfix-protocol](../bugfix-protocol/SKILL.es.md) | Depuración sistemática en 6 fases |
| Fases 7-8 | [bugsweep](../bugsweep/SKILL.es.md) | Barrido de errores convergente antes de un lanzamiento |

Si su colección de habilidades tiene un índice de habilidades, búsquelo para obtener más habilidades específicas por fase.

---

## Historial de cambios

### 1.1.0 (2026-06-13)
- Nueva tabla de "Habilidades específicas por fase" con referencias a project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol y bugsweep.

### 1.0.0 (2026-03-12)
- Portado desde BACH (dev-zyklus v1.0.0).

---

*Creado: 2026-01-28 | Portado: 2026-03-12*