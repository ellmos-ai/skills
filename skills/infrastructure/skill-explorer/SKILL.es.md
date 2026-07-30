---
name: skill-explorer
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Gestiona tu propio entorno de habilidades: analiza y compara las habilidades existentes (modo Auditoría), investiga en la web nuevas habilidades/plugins (modo Explorar), y al mismo tiempo es el instalador que genera subhabilidades ligeras (Skill-Finder, paraguas familiar, habilidades de mantenimiento) en lugar de cargar un monolito. Utiliza esta habilidad para "comparar/auditar habilidades", "qué habilidades están duplicadas", "crear familias de habilidades", "limpiar/consolidar habilidades", "mantener el registro de habilidades", "buscar habilidades/plugins sobre el tema X", "instalar nuevas habilidades", "explorar el mercado de habilidades" o para `/skill-explorer`. Entrega un subinforme por familia y una lista de decisiones numerada globalmente; instala/desinstala únicamente tras una comprobación de seguridad y aprobación explícita.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: es
status: active
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `skill-explorer`.


# Skill-Explorer — Gestionar el entorno de habilidades (Auditoría · Explorar · Instalador) (Español)

## Visión general y propósito

A medida que crece el inventario de habilidades, surgen duplicados, recursos sin usar y situaciones confusas de "qué habilidad usar en lugar de cuál", además de que constantemente aparecen nuevas habilidades/plugins. `skill-explorer` combina tres funciones en una sola herramienta:

| Rol | Qué hace | Detalle |
| --- | --- | --- |
| **Modo Auditoría** (hacia dentro) | analizar todas las habilidades, agruparlas en familias, recopilar capacidades/dependencias/recursos, generar un subinforme + recomendaciones numeradas por familia | `references/audit-mode.md` |
| **Modo Explorar** (hacia fuera) | investigar en la web (web/GitHub/Reddit, bilingüe) sobre nuevas habilidades/plugins de un tema, comparar e instalar de forma controlada | `references/explore-mode.md` |
| **Instalador** | *generar* subhabilidades ligeras en lugar de un monolito — Skill-Finder, paraguas familiar, habilidades de mantenimiento | a continuación + `references/family-care.md` |

Invocación: `/skill-explorer` (Auditoría por defecto) o "… buscar sobre el tema X" (Explorar). Ambos modos comparten una taxonomía (`references/clustering.md`), un formato de informe (`references/report-format.md`) y el esquema de numeración, de modo que el usuario puede responder con una sola lista numerada.

## Principio del instalador y persistencia

En lugar de crecer de forma monolítica, `skill-explorer` *genera* subhabilidades ligeras y cargables individualmente bajo demanda, de modo que nunca haya que cargar una sola habilidad excesivamente larga:

- **Skill-Finder** ([F]) — un buscador/enrutador activo análogo a un conserje tipo "using-superpowers" que lee el registro antes de cada tarea y enruta hacia la familia correspondiente (`references/skill-finder.md`, plantilla `assets/skill-finder-template.md`).
- **Paraguas familiar** (c1) — una metahabilidad que conoce a toda una familia (`assets/family-umbrella-template.md`).
- **Habilidades de mantenimiento** ([P1] familias, [P2] registro) — mantienen actualizados las familias/registro (`references/family-care.md`).

Las decisiones se persisten en `~/.claude/skills/skill-explorer/config.json` (`references/config.md`, plantilla `assets/config.example.json`): se leen al iniciar (familias/enrutadores/subhabilidades generadas conocidas) y se actualizan tras la ejecución, de modo que una reejecución nunca cree nada por duplicado.

## Mecanismo de rama (Personalización de habilidades de terceros)

Una habilidad de solo lectura (plugin, de terceros importada) se puede personalizar sin modificar la original: el directorio original se copia por completo (**rama**); después solo se edita la copia. La rama contiene cuatro campos obligatorios: una referencia a la original, la fecha de la rama, el autor y la razón. Una vez que la rama reemplaza a la original, esta última se elimina del registro en tiempo de ejecución (`SKILL.md` → `CONTENT.md`) o el enrutador familiar se apunta a la rama, evitando así que dos habilidades casi idénticas colisionen. Las ramas de terceros se mantienen **privadas** — no van a la biblioteca pública `.AI/.SKILLS`. Detalles: `references/skill-branching.md`.

## Flujo de trabajo y procedimiento

1. **Elegir modo:** analizar/limpiar el inventario → Modo Auditoría. Buscar/instalar desde fuera → Modo Explorar. (Explorar puede apoyarse en una auditoría previa/`config.json`.)
2. **Modo Auditoría** (`references/audit-mode.md`): inventario (script) → clústeres familiares → subinformes → **una lista de decisiones numerada globalmente** (a/b/c1/c2/c3, más R/F/P1/P2).
3. **Modo Explorar** (`references/explore-mode.md`): investigación bilingüe multifuente → 3 categorías por candidato → simulación de impacto → recomendaciones numeradas de instalación/eliminación.
4. **Ejecutar** solo tras la confirmación numérica del usuario; registrar la creación/cambios de habilidades y actualizar `config.json`.

## Reglas Inquebrantables

- **Inspección ≠ mutación:** agrupar todo, pero editar únicamente las habilidades **propiedad del usuario**; las habilidades de plugins/terceros son de solo lectura (nunca modificar el encabezado ni eliminar). Para personalizar una habilidad de terceros, cree una **rama** (copia fork) en su lugar — la original permanece intacta y todos los cambios se realizan exclusivamente en la copia (→ `references/skill-branching.md`).
- **Ampliar el registro, no duplicar:** si ya existe un registro de habilidades (índice + mapa de familias + habilidad índice), amplíelo en lugar de crear un cuarto elemento.
- **Seguridad principalmente manual:** antes de cada instalación, el modelo lee la propia habilidad y juzga; `scripts/scan_skill_security.py` es solo un triaje de apoyo con límites conocidos. Nunca instalar de forma automática.
- **Registro por origen:** creadas por el usuario → Biblioteca; de terceros → ruta externa, **no** Biblioteca.

## Orquestación (neutral respecto al modelo)

Los subinformes de familia o las fuentes/idiomas son rutas de trabajo independientes. Si la plataforma ofrece subagentes más económicos que el propio orquestador, asigne un subagente por familia/fuente y, como orquestador, solo consolide/verifique (enjambre especialista). De lo contrario, hágalo usted mismo secuencialmente.

## Recursos

- **Modos:** `references/audit-mode.md`, `references/explore-mode.md`
- **Compartidos:** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Auditoría:** `references/family-care.md`, `references/skill-finder.md`
- **Explorar:** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Rama:** `references/skill-branching.md`
- **Scripts:** `scripts/inventory_skills.py` (inventario), `scripts/inject_family_header.py` (enrutador de encabezado), `scripts/scan_skill_security.py` (triaje de seguridad)
- **Plantillas:** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`, `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Registro de cambios

### 1.1.0 (2026-06-17)
- Se añadió el mecanismo de rama: las habilidades de terceros/solo lectura se pueden personalizar a través de una copia fork (rama) — con una referencia al original, fecha, autor y razón; el original permanece intacto. La regla inquebrantable "Inspección ≠ mutación" se amplió con la alternativa de rama. Nueva sección `## Mecanismo de rama`. Nuevos archivos: `references/skill-branching.md`, `assets/branch-header.example.md`.

### 1.0.0 (2026-06-17)
- Versión inicial. Une la auditoría de inventario (agrupación por familias, decisiones numeradas) y la investigación web (instalación controlada con triaje de seguridad) en un solo instalador que genera subhabilidades ligeras.