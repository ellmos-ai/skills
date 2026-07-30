---
name: pipeline-optimizer
version: 1.2.0
type: protocol
author: Lukas Geiger (method) + Claude (write-up)
created: 2026-05-16
updated: 2026-06-13
aliases: [project-folder-optimizer, pipeline-renovator, project-renovator]
description: Procedimiento estructurado de 6 pasos para mejorar, renovar o reconstruir pipelines existentes, carpetas de proyectos individuales, estructuras de documentación o stacks de software. Direccionable como "pipeline optimizer" (para pipelines temáticos completos, p. ej. de software, investigación o desarrollo de videojuegos) o "project-folder optimizer" (para carpetas de proyectos individuales dentro de un pipeline, p. ej. una herramienta de software o proyecto de artículo académico). Se activa ante tareas como "mejorar pipeline X", "optimizar el stack", "reconstruir Y", "renovación", "refactorización de pipeline", "limpiar carpeta de proyecto", "mejorar estructura de carpetas", "unificar convenciones", "consolidación de documentación", "integrar en sistema existente" o cualquier intervención sustancial en estructuras establecidas. Proporciona análisis del estado actual, aclaración del propósito, boceto del estado ideal, plan de brechas, identificación empírica de puntos de dolor y reevaluación con subagentes limpios. Previene estándares paralelos, duplicación y rupturas en el pipeline.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [pipeline, renovation, refactoring, stack, workflow, lessons-learned]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/pipeline-optimizer/', 'origin_version': '1.1.1', 'last_sync_from_origin': '2026-05-16', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `pipeline-optimizer`.


# Pipeline Optimizer / Project-Folder Optimizer (Español)

**Renovación en 6 pasos sin incompatibilidades** — aplicable a dos escalas:

| Nombre de activador | Alcance | Ejemplo |
|---|---|---|
| **Pipeline optimizer** | Pipelines completos, stacks, estructuras de documentación | Sus pipelines temáticos, p. ej. `software/`, `research/`, `games/`, un sistema de agentes |
| **Project-folder optimizer** | Carpetas de proyecto individuales dentro de un pipeline | Una herramienta de software, un proyecto de artículo, un proyecto de juego |

Un **pipeline** aquí significa una estructura de nivel superior orientada a temas en la que conviven múltiples proyectos bajo convenciones compartidas (p. ej. un pipeline de software con reglas de publicación, un pipeline de investigación con un procedimiento de publicación).

Ambos utilizan el mismo flujo de trabajo de 6 pasos — la única diferencia es el **alcance** (a nivel de pipeline completo vs. proyecto único) y, en consecuencia, la profundidad de la inspección del estado actual en el paso A.

## Cuándo se aplica esta habilidad

Esta habilidad se aplica tan pronto como se le solicita mejorar, reconstruir o extender una estructura **existente** — no para construcciones desde cero (greenfield). Activadores concretos:

**Nivel de pipeline** (alcance: pipeline completo):
- "Hacer mejor el pipeline X"
- "Optimizar el stack"
- "Renovar el pipeline de software"
- "Consolidación de documentación en el pipeline de investigación"
- Intervención sustancial en un pipeline temático, `_tools/` central o componentes del sistema

**Nivel de carpeta de proyecto** (alcance: carpeta de proyecto único):
- "Limpiar / optimizar carpeta de proyecto X"
- "Mejorar la estructura de carpetas en Y"
- "Refactorizar una sola herramienta"
- "Unificar la configuración de un proyecto de artículo"
- "Alinear una carpeta de proyecto de juego con el estándar del pipeline"

**Transversal:**
- "Reconstruir X / integrarlo en Y existente"
- "Refactorización", "consolidación"
- "Unificar convenciones"
- "Integrar en un sistema existente"

## La metáfora de la edificación existente

Renovar una casa requiere primero saber **de qué está hecha** (piedra, madera, plástico), **para qué sirve** (refugio de montaña, forja de software) y **dónde ya cumple funciones**. La misma disciplina se aplica a los pipelines.

---

## Procedimiento — 6 pasos (NO omitir, NO reordenar)

### Paso A — Inspeccionar la edificación existente

**Pregunta:** ¿De qué está hecha la casa?

**Alcance de pipeline** (todos los documentos raíz + herramientas + plantillas):
- [ ] **Leer todos los documentos raíz completamente** (no solo fragmentos o puntos de inserción)
- [ ] Revisar carpetas de plantillas (`_templates/`, `_TEMPLATES/`) y carpetas de herramientas (`_tools/`)
- [ ] Archivos de políticas: p. ej. GITHUB-POLICY.md, RELEASE-MANAGEMENT.md, QUALITY_RULES.md, NAMING-SYSTEM.md, procedimientos de publicación, …
- [ ] Capturas de estado: p. ej. PROJECT_STATUS.md, resúmenes de estado, releases.json, archivos de registro
- [ ] Listas de verificación: p. ej. listas de verificación de lanzamientos, listas de verificación de compilación/PDF
- [ ] Flujos de trabajo: AGENTS.md, GUIDE.md, SKILL.md
- [ ] Archivos de lecciones aprendidas: LESSONS_LEARNED.md, MEMORY.md, archivos de estado de bucles

**Alcance de carpeta de proyecto** (sustancia del proyecto único + convenciones relevantes del pipeline):
- [ ] **Leer todos los archivos markdown y de control en la carpeta del proyecto** (README, CHANGELOG, TASKS/TODO, DONE, CONCEPT, plan de acción, notas de prueba, …)
- [ ] **Inspeccionar la estructura del código:** src/, tests/, configuración de compilación (pyproject.toml, requirements.txt, manifiestos del proyecto, archivos de cadena de herramientas, …)
- [ ] **Tener en cuenta las convenciones del pipeline primario** (p. ej. para un proyecto de software: política de GitHub, sistema de nombres, gestión de lanzamientos, plantillas)
- [ ] **Escanear herramientas/scripts existentes en el proyecto** (`_tools/`, `_scripts/`, build_*.bat, scripts START)
- [ ] **Archivos de configuración:** `.gitignore`, LICENSE, NOTICE, SECURITY.md, CODE_OF_CONDUCT.md

**Antipatrón:** Usar `grep -l "<keyword>"` para buscar puntos de inserción e insertar allí sin conocer el contexto del archivo.

**Resultado:** Nota de inventario con todas las convenciones, herramientas y plantillas relevantes dentro del alcance elegido.

### Paso B — Identificar el propósito

**Pregunta:** ¿Para qué existe la casa?

Explicitar el propósito en 1-2 frases.

**Ejemplos de pipelines:**

| Pipeline | Propósito |
|---|---|
| Pipeline de software | Desarrollar, probar y lanzar aplicaciones de escritorio + herramientas web en tiendas/GitHub |
| Pipeline de investigación | Escribir artículos científicos, revisarlos entre pares, publicarlos en repositorios/servidores de preprints |
| Pipeline de juegos | Desarrollar juegos y publicarlos en la plataforma de destino |
| Sistema de agentes | Sistema LLM para orquestación multi-agente |

**Ejemplos de carpetas de proyecto:**

| Carpeta de proyecto | Propósito |
|---|---|
| `software/PlannerApp` | Aplicación de planificación de escritorio, comercial, repositorio privado |
| `research/CosmologyModel` | Serie de artículos sobre modelos + cálculos numéricos |
| `games/SortingChaos` | Juego de clasificación, etapa alfa, progresión de niveles |

El propósito **dirige cada intervención** — las medidas que no sirvan al propósito se descartan.

### Paso C — Esbozar el estado ideal

**Pregunta:** ¿Cómo sería una casa perfecta para este propósito?

- Esbozarlo desde su propia perspectiva (breve, máx. 10 puntos)
- Incorporar una comparación de mejores prácticas (p. ej. stack Vercel para SaaS, stack python científico para investigación)
- No descender a la optimización de detalles — un esquema de nivel superior es suficiente

**Resultado:** 5-10 puntos de "estado ideal por pipeline"

### Paso D — Análisis de brechas + plan

**Cuatro preguntas por pipeline:**

1. **¿Qué tiene ya la casa?** — Incluso si se resuelve de manera diferente al ideal pero es **funcionalmente equivalente**.
   *Ejemplo:* El ideal dice "pip-licenses para licencias de terceros". La realidad: un script generador personalizado lo envuelve → funcionalmente equivalente, no se requiere intervención.

2. **¿Qué impide la función?** — Estructuras existentes que causan rupturas o esfuerzo extra en la actualidad.

3. **¿Qué no es funcional?** — Código muerto, convenciones desactualizadas, herramientas sin uso.

4. **¿Qué mejoraría mensurablemente las funciones?** — Intervenciones concretas con beneficio esperado.

→ A partir de esto, un **plan concreto**:
- ¿Qué se **construye de nuevo**?
- ¿Qué se **extiende**?
- ¿Qué se **demuele**?
- ¿Qué permanece **sin cambios** (¡importante especificar!)?

**Resultado:** Tabla de plan con columnas *Intervención* / *Existente* / *Medida* / *Justificación*

### Paso E — Trabajar empíricamente

No planificar únicamente de arriba a abajo — recopilar puntos de dolor:

- [ ] **Errores conocidos**: rastreador de problemas (issue tracker), archivos TASKS/TODO/DONE
- [ ] **Historial de errores**: archivos de lecciones aprendidas, registros de corrección de errores, registros de comprobaciones
- [ ] **Rupturas de automatización**: "¿Qué tengo que hacer siempre manualmente?"
- [ ] **Entrevista de usuario**: preguntar específicamente — puntos de dolor, deseos, soluciones temporales
- [ ] **Prueba propia**: recorrer el pipeline (crear un nuevo proyecto, ejecutar una compilación, simular un lanzamiento) — ¿dónde se rompe?

Los puntos de dolor encontrados empíricamente **priorizan el plan** del paso D.

### Paso F — Reevaluaciones tras la implementación

- [ ] Encargar a **subagentes limpios** (sin la carga del contexto de renovación) que recorran el flujo de trabajo modificado
- [ ] **Valores mensurables antes/después**: tiempo de configuración, tasa de error, número de pasos manuales, tiempo de compilación
- [ ] **Comprobación anti-regresión**: ¿siguen funcionando los flujos de trabajo existentes tras el cambio?
- [ ] Si **no hay una mejora mensurable** o hay una regresión: **revertir** la renovación o reajustar

## Antipatrones (prohibidos)

| Antipatrón | Daño | Antídoto |
|---|---|---|
| Buscar puntos de inserción en lugar de leer documentos | Estándares paralelos | Paso A completo |
| Transferir "mejores prácticas de X" 1:1 | Incompatibilidad | Paso D compara funcionalmente |
| Crear un nuevo archivo sin verificar convenciones | Duplicación (p. ej. NOTICE.md ↔ THIRD_PARTY_LICENSES.txt) | Paso A + paso D |
| Planificar de arriba a abajo sin datos empíricos | La solución no aborda el punto de dolor | Paso E antes de finalizar el plan |
| No probar los propios cambios | Regresión no detectada | Paso F con un agente limpio |
| "Aclarar más tarde" con estado incierto | El usuario descubre el conflicto después | En caso de duda, revisar el paso D nuevamente con el usuario |

## Estudio de caso — El incidente NOTICE.md

**Tarea:** Implementar mejoras de pipeline en varios pipelines temáticos (software, investigación, juegos).

**Error:** Se omitió el paso A — solo se buscaron puntos de inserción en lugar de leer los archivos de políticas completos.

**Consecuencia:** Se introdujo `NOTICE.md` como un "nuevo archivo de licencia" en 7 archivos, aunque `THIRD_PARTY_LICENSES.txt` + un generador de licencias personalizado (envoltorio alrededor de `pip-licenses`) ya estaban establecidos — documentado en la política de GitHub del pipeline (archivos obligatorios + lista de verificación de licencias). Todos los proyectos de software ya tenían archivos THIRD_PARTY.

**Detección:** Solo después de que el usuario preguntó ("Estoy seguro de que ya teníamos gestión de derechos").

**Corrección:** Se eliminó NOTICE.md de la plantilla del proyecto, se ajustaron 6 archivos adicionales y se hizo referencia al generador de licencias existente en lugar de `pip-licenses`.

**Lección:** Si el paso A se hubiera ejecutado por completo, el conflicto se habría detectado antes de escribir.

## Reglas generales

1. **Para "mejorar el pipeline", primero lea tanto tiempo como escriba.**
2. **Ningún estándar nuevo sin prueba de que no existe uno previo.**
3. **Utilice herramientas/envoltorios existentes en lugar de crear otros paralelos.**
4. **"Más de lo mismo" suele ser peor que "extender lo que existe".**
5. **Revertir en caso de conflicto** siempre es mejor que mantener dos estándares paralelos.

## Lista de verificación de finalización

Antes de reportar una renovación de pipeline como "completada":

- [ ] Paso A: ¿se leyeron todos los documentos raíz relevantes?
- [ ] Paso B: ¿se declaró el propósito del pipeline en 1-2 frases?
- [ ] Paso C: ¿se esbozó el estado ideal (5-10 puntos)?
- [ ] Paso D: ¿análisis de brechas con tabla (qué se mantiene / qué se extiende / qué es nuevo / qué se elimina)?
- [ ] Paso E: ¿se verificaron los datos empíricos (errores, lecciones, prueba propia, entrevista de usuario)?
- [ ] ¿Plan acordado con el usuario?
- [ ] Paso F: probado con un subagente limpio — ¿mejora mensurable?
- [ ] ¿No se introdujeron estándares paralelos?
- [ ] En caso de conflictos: ¿se revirtió o se justificó honestamente?

## Estructura óptima de carpeta de proyecto (para el optimizador de carpeta de proyecto)

Cuando la habilidad se aplica a **una sola carpeta de proyecto**, la siguiente recomendación combinada sirve como referencia ideal (paso C):

### Estándar Anthropic (Claude Code)

| Archivo/carpeta | Función |
|---|---|
| `CLAUDE.md` (raíz) | Cargado automáticamente por Claude Code, instrucciones específicas del proyecto |
| `.claude/settings.json` | Permisos, variables de entorno, selección de modelo (registrado/commit) |
| `.claude/settings.local.json` | Anulaciones locales (NO registrar en commit, añadir a `.gitignore`) |
| `.claude/commands/*.md` | Comandos slash personalizados |
| `.claude/agents/*.md` | Subagentes personalizados |
| `.claude/skills/<name>/SKILL.md` | Habilidades del proyecto |

### Su propia plantilla de documentación de proyecto (recomendado)

Si mantiene su propia plantilla de documentación de proyectos (p. ej. en `<your-workspace>/_templates/project-docs/`), **tres perfiles de implementación** resultan rentables. Ejemplo de división: **MINIMAL** proporciona el conjunto central de sesión con 7 archivos raíz (`AGENTS.md`, `CLAUDE.md`, `README.md`, `START.md`, `STATE.md`, `TODO.md`, `DONE.md`) más `_tools/`. **STANDARD** añade `CHANGELOG.md`, `DECISIONS.md` y `PATTERNS.md`. **FULL** se amplía a 14 archivos raíz y añade además `ARCHITECTURE.md`, `WORKFLOWS.md`, `TOOLS.md`, `GLOSSARY.md`, así como `workflows/` y `.github/`.

→ **Utilice dicha plantilla como base para nuevos proyectos** (copiar en lugar de crear manualmente).

### Adiciones específicas según el pipeline (ejemplos)

Según el pipeline, se añaden archivos obligatorios adicionales — patrones típicos:

- **Proyecto de software:** LICENSE, CODE_OF_CONDUCT.md, SECURITY.md, CONTRIBUTING.md, THIRD_PARTY_LICENSES.txt (generado), pyproject.toml/requirements.txt, entrada en el registro central de lanzamientos del pipeline. → Si está disponible: utilice la plantilla cookiecutter del pipeline.
- **Proyecto de investigación:** documento de concepto, plan de acción, plan de publicación, carpetas de archivo/fuentes/resultados/datos (`_archive/`, `_sources/`, `_results/`, `_data/`), `paper/` para LaTeX. Para proyectos de demostración: un archivo de notas de demostración con la cadena de demostración y su estado.
- **Proyecto de juegos:** manifiesto del proyecto y archivos de cadena de herramientas del motor (p. ej. para Roblox/Rojo: default.project.json, rokit.toml, wally.toml, selene.toml), documento de diseño de juego, `src/{server,client,shared}/` según la convención del motor.

### Referencia detallada completa

→ Ver **`references/optimal-project-structure.md`** en esta carpeta de habilidad (alemán). Contiene:
- Ejemplo de `settings.json` (esquema Anthropic)
- Entradas obligatorias en `.gitignore`
- Antipatrones (lo que NO pertenece a las carpetas de proyectos)
- Flujos de trabajo recomendados según el tipo de pipeline (software/investigación/juego)
- Convención de encabezado YAML para archivos de documentación
- Boceto de autochequeo

## Habilidades relacionadas (¿cuándo usar en lugar de esta?)

| Habilidad | Cuándo usar |
|---|---|
| **`project-onboarding`** | Incorporar un repositorio externo existente a su propio sistema |
| Project bootstrapper (si está disponible) | Crear un NUEVO proyecto en un pipeline existente (greenfield, sin reconstrucción) |
| Pipeline bootstrapper (si está disponible) | Crear un pipeline COMPLETAMENTE NUEVO (caso raro) |
| System onboarding (si está disponible) | Configurar un equipo nuevo |

El **pipeline optimizer** es responsable de la **renovación**, no de la nueva construcción ni de la incorporación. Si su colección de habilidades tiene un índice de habilidades, búsquelo para encontrar habilidades de arranque coincidentes.

## Referencias cruzadas

- Referencia de detalles: `references/optimal-project-structure.md` (en esta carpeta de habilidad)
- Documentación Anthropic Claude Code: `https://docs.claude.com/en/docs/claude-code`
- Si están disponibles: reglas globales de usuario (p. ej. una sección de "renovaciones" en su `~/CLAUDE.md`) y descripciones de stacks específicas por pipeline

## Elección de alcance: pipeline vs. carpeta de proyecto

Si no está claro qué alcance se pretende, **aclarar antes del paso A**:

| Pista | Alcance |
|---|---|
| "Mejorar todo el pipeline de software" | Pipeline |
| "Limpiar la carpeta de la herramienta X" | Carpeta de proyecto |
| "Sincronizar el registro central de lanzamientos" | Pipeline (activo central) |
| "Refactorizar AssetBuilder en el juego Y" | Carpeta de proyecto |
| "Introducir una convención de comprobación en todo el pipeline" | Pipeline |
| "Crear un archivo de comprobación en el proyecto Z" | Carpeta de proyecto |

En el **alcance de carpeta de proyecto**, verifique también brevemente las convenciones del pipeline primario (paso A extendido) para que la intervención siga siendo compatible con el pipeline.

---

## Historial de cambios

### 1.2.0 (2026-06-13)
- Primera publicación en la biblioteca de habilidades: rutas personales, nombres concretos de pipelines/proyectos y referencias a habilidades privadas reemplazadas por ejemplos genéricos; el procedimiento en sí (6 pasos, antipatrones, estudio de caso, listas de verificación) sin cambios

### 1.1.1 (2026-06-01) y anteriores
- Versiones internas (directorio de habilidades privado, antes de la publicación)
