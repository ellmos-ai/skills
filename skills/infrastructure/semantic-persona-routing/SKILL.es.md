---
name: semantic-persona-routing
version: 1.1.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-09-03
description: >
  Construye y utiliza un gráfico de enrutamiento semántico neutral respecto al proveedor a partir de personas,
  roles de coordinación, expertos y puntos de enlace de habilidades (skills) en vivo. Utilícelo cuando un LLM deba
  enrutar una solicitud a través del rol superior (boss-role) hacia un experto y luego a una habilidad, extraer un
  enrutador de personas portable desde un sistema de agentes existente, combinar un mapa de dominio semántico
  con un registro léxico de habilidades, o exponer puertos faltantes entre roles y habilidades en lugar de
  recurrir silenciosamente a alternativas. Se activa con enrutamiento semántico de personas, paraguas de personas (persona umbrella),
  enrutador de roles, enrutamiento de habilidades por agente principal/experto, exportación de roles de agente o
  solicitudes para hacer que las personas sean reutilizables entre proveedores de LLM.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [persona, persona-authoring, semantic-routing, agents, experts, skills, umbrella, provider-neutral]
language: es
status: active
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

<img src="banner.png" width="100%" alt="semantic-persona-routing banner">

> **Español** — Versión oficial en español de `semantic-persona-routing`.

# Enrutamiento Semántico de Personas (Semantic Persona Routing)

Enrute primero por capacidad y aplique la personalidad en segundo lugar. Construya un mapa portable que mantenga separados la elección semántica de roles, la búsqueda determinista de puntos de enlace (endpoints) y la carga específica del proveedor.

## Modelo de enrutamiento

```text
request
  -> semantic domain/coordinator role
  -> expert capability
  -> explicit or live-resolved skill endpoint
  -> optional persona overlay
  -> provider adapter loads and executes
```

Una persona controla el estilo de comunicación, las prioridades y los patrones de interacción. No otorga herramientas, permisos ni capacidad técnica en la materia. Un rol coordina; un experto delimita el dominio; una habilidad (skill) es el punto de enlace ejecutable.

## Construir el mapa de enrutamiento

Utilice los metadatos explícitos como autoridad y la similitud léxica únicamente como candidata:

```bash
python scripts/build_routing_map.py \
  --roles-dir path/to/roles \
  --personas-dir path/to/personas \
  --skills-dir path/to/skills \
  --out routing-map.json
```

El generador comprende campos comunes de `SKILL.md` como `type`, `orchestrates.experts`, `parent_agents`, `skills`, descripciones y procedencia (provenance). Produce un mapa en tiempo de ejecución sin requerir que el sistema de origen esté instalado. Lea [routing-map-schema.md](references/routing-map-schema.md) antes de extender el formato.

No promueva automáticamente los `candidate_skills`. Confíermelos primero frente a un resolvedor de habilidades en vivo o metadatos de origen.

## Crear y guardar personas

El núcleo construye mapas; nunca inventa personas. Para usar las tuyas,
guárdalas **junto al skill** y reconstruye el mapa: `personas/<persona-id>.md`
(un archivo por persona), `roles/<rol>/SKILL.md` (roles coordinadores y
expertos), `routing-map.json` (mapa generado) y `config.json` (local al host,
nunca publicado). El constructor lee roles solo de archivos `SKILL.md` y
personas de cualquier Markdown con frontmatter. Copia
[templates/persona.template.md](templates/persona.template.md) y completa el
contrato: `name` y `type: persona`; `persona.display_name`, `short_name`,
`gender`, `role`, `default_prompt`; `parent_agents` (roles coordinadores);
`skills` (**nombres de skills, nunca rutas**; solo estos se resuelven a
endpoints); `optional_skills` (skills ligados al host; si faltan, quedan como
`GAP` visible). Una persona nunca otorga herramientas ni permisos y nunca
anula reglas de seguridad, bloqueos o decisiones del usuario.

**Rutas:** el skill no nombra rutas del host. `config.example.json` muestra el
patrón (`ellmos.skill-config.v1`, `einstellungen.paths` con marcadores como
`<HOME>/<ONEDRIVE>/<TOPICS>`); la copia local es `config.json`, se conserva
al desplegar y nunca se versiona.

**Catálogo limpio:** `--skills-layout catalog` acepta solo
`<categoría>/<nombre>/SKILL.md` y omite directorios con prefijo `_`
(`_archive`, `_reference`, `_templates`), evitando issues
`duplicate-skill-id` por copias archivadas o de referencia.

## Enrutar una solicitud

### 0. Ofrecer las personas existentes

Si hay personas junto al skill (`personas/`), enuméralas al invocar con nombre,
rol y skills y enruta a la adecuada; si la solicitud no nombra ninguna, elígela
en el paso 4. El formato del comprobante de ruta no cambia.

### 1. Seleccionar semánticamente el rol coordinador

Compare la solicitud con los nombres de los roles, sus descripciones y casos de uso. Prefiera el rol más específico que pueda coordinar toda la solicitud. Mantenga visibles múltiples candidatos cuando la confianza sea baja; consulte al usuario solo cuando la elección cambie sustancialmente el resultado.

### 2. Seleccionar un experto dentro del rol

Utilice únicamente expertos conectados al coordinador seleccionado, a menos que la solicitud abarque claramente varios roles. Una solicitud directa a un experto puede omitir al coordinador para la ejecución, pero conserve el enlace con el coordinador en la explicación de la ruta.

### 3. Resolver los puntos de enlace ejecutables

Resuelva en este orden:

1. `endpoint_skills` provenientes de metadatos de origen explícitos o procedencia exacta;
2. un resolvedor de habilidades externo actual o un buscador local de habilidades;
3. `candidate_skills` verificados;
4. `GAP` visible cuando no exista ningún punto de enlace.

Nunca enrute hacia el nombre de un experto como si fuera una habilidad instalada. La falta de un punto de enlace representa una brecha de adaptación (porting gap), no una autorización para fabricar uno.

Lea [endpoint-resolution.md](references/endpoint-resolution.md) al conectar un registro en vivo, un buscador léxico o un cargador de habilidades específico del proveedor.

### 4. Aplicar la superposición de persona (persona overlay)

Elija una persona vinculada al rol o experto seleccionado. Si varias personas encajan, prefiera aquella cuyos límites declarados y estilo coincidan con la tarea. No aplique ninguna persona cuando ninguna esté explícitamente conectada.

Las instrucciones de la persona no pueden anular reglas de seguridad, bloqueos, decisiones del usuario, límites profesionales o permisos de herramientas.

### 5. Cargar y ejecutar

Utilice el mecanismo nativo de carga de habilidades/agentes del proveedor. Cargue las instrucciones de la habilidad en vivo seleccionada antes de la ejecución. Mantenga el enrutador ligero; la ejecución corresponde al trabajador (worker) o agente actual con las habilidades resueltas cargadas.

## Comprobante de ruta (Route receipt)

Devuelva o registre:

```text
ROLE: <coordinator or direct>
EXPERT: <expert or n/a>
SKILLS: <verified live endpoints>
PERSONA: <overlay or none>
RESOLUTION: explicit | provenance | live-resolver | verified-candidate | GAP
CONFIDENCE: high | medium | low
WHY: <one short reason>
GAPS: <missing endpoints or stale-map warnings>
```

Reconstruya el mapa cuando cambien los roles de origen o el inventario de habilidades. Un resolvedor en vivo puede sustituir a un mapa desactualizado en cuanto a la disponibilidad del punto de enlace, pero no debe reescribir silenciosamente la taxonomía semántica de roles.

## Ejemplo

Solicitud: "Organiza mis recibos y prepara el resumen del año fiscal."

El enrutador selecciona un coordinador de oficina, luego al experto fiscal, resuelve la habilidad fiscal instalada y finalmente aplica una persona fiscal meticulosa vinculada explícitamente. Si el experto fiscal existe pero no hay ninguna habilidad fiscal portable instalada, informe `GAP` y continúe únicamente mediante una alternativa (fallback) configurada explícitamente.

## Historial de cambios (Changelog)

### 1.1.0 (2026-09-03)

- Crear y guardar personas: convención de almacenamiento junto al skill,
  contrato de frontmatter, plantilla neutral `templates/persona.template.md`,
  convención de rutas con `config.example.json`, comportamiento de invocación y
  `--skills-layout catalog` contra ids de skill duplicados.

### 1.0.0 (2026-07-28)

- Se extrajo la cadena neutral respecto al proveedor rol/experto/habilidad a partir de un patrón probado de enrutador de dominio y se añadió la generación de mapas portables con brechas visibles de puntos de enlace.