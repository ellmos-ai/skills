---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "Crea o revisa una skill PARA ESTE ECOSISTEMA: delega el bucle genérico de entrevista, borrador y evaluación en el plugin oficial skill-creator (Anthropic, Apache-2.0), pero además aplica los requisitos de ellmos que el plugin oficial no conoce: frontmatter propio de la casa (9 campos), reglas de categoría y visibilidad, detección neutral respecto al proveedor, al usuario y a ellmos, pero sensible a ellmos mediante grounding-seed, config.json incluido (incluido el contrato de aprendizaje) más connections.json, conciencia de proveedores y fabricantes (proponer alternativas del estado del arte, incluidos los propios componentes de ellmos), una sección de autoactualización Y un conjunto reutilizable de archivos de aprendizaje y cobertura (user-usecases.json, usecase-gaps.json, known-providers-and-abilities.json, gap-closing-analysis.json, inspirados en evals.json de skill-creator y en A2A/AgentSkill, sin ser un estándar paralelo). Úsala SIEMPRE que vaya a nacer una NUEVA skill para este sistema o que una existente deba adaptarse a la conformidad con ellmos, incluso con peticiones como \"crea una skill\", \"hazme una skill para X\", \"usa skill-creator\", \"crear una nueva skill\", \"haz esta skill conforme a ellmos\", \"crear contrato de aprendizaje/códice de comportamiento para una skill\", \"comprobar la cobertura de casos de uso de una skill\". Para simplemente ENCONTRAR/ENRUTAR skills usa en su lugar skill-finder, y para la auditoría del panorama, skill-explorer."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: es
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 1e6dace03eb8afc639fa08debace08a61441912a22399c11a49f7fe6e7dc3ecb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.966939+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## Origen y decisión (fork frente a desarrollo propio)

**Decisión: desarrollo propio, no fork.** Justificación, para que no se pierda:

- `skill-creator` (Anthropic, marketplace `claude-plugins-official`) tiene licencia **Apache-2.0**
  (texto de LICENSE leído y verificado en el clon, 2026-08-24); un fork sería legalmente posible
  y en el repositorio ya es el patrón establecido en otros puntos (`skills/third-party/grilling`).
- Un fork, sin embargo, arrastraría toda la maquinaria de evaluación y benchmark del original
  (`agents/{analyzer,comparator,grader}.md`, `eval-viewer/`, 7 scripts, SKILL.md de 485 líneas), una capacidad que ya
  existe y se puede invocar directamente (`Skill: skill-creator:skill-creator`). Según la regla 4 de `.PLUGINS/CLAUDE.md`
  ("comprobar las capacidades antes de reconstruirlas") y el patrón P10 ("dos interruptores que nadie
  compara"), eso sería un duplicado, no una extensión.
- La brecha real es **puramente específica de ellmos** y el original la desconoce por completo:
  frontmatter de la casa (`templates/SKILL.md`), `docs/CONVENTIONS.md`, neutralidad respecto al proveedor y
  al usuario con sensibilidad a ellmos, integración con `grounding-seed`, conciencia de proveedores
  y autoactualización.
- Esta skill **no contiene texto de Anthropic** (formulación propia en todo el documento), por lo que
  tampoco activa la obligación de atribución de Apache-2.0 para modificaciones. **Compone** el original
  en lugar de copiarlo: es a la vez la vía legalmente más limpia y la de menor mantenimiento.

## Cuándo activar

- "crea una skill para X", "construir una nueva skill", "usa skill-creator"
- "haz esta skill conforme a ellmos", "adaptar una skill al estándar de la casa"
- Siempre que el **destino** sea una skill en `.AI/.SKILLS/skills/…` (o su clon canónico del Plan D), no en
  peticiones generales ajenas al ecosistema ("crea cualquier skill de Claude sin relación con esto").

## Procedimiento

### Paso 1 — Delegar entrevista, borrador y evaluación

Invoca el `Skill: skill-creator:skill-creator` oficial para: aclaración de la intención, borrador de la estructura de
SKILL.md, casos de prueba, bucle de evaluación y optimización de la descripción (`scripts/improve_description.py`).
**No lo reinventes**: esta parte es genérica y el original ya la resuelve bien.

### Paso 2 — Montar el scaffold de la casa ellmos (obligatorio, aditivo al formato original)

Completa el SKILL.md generado por el original con los nueve campos de la casa de `.SKILLS/templates/SKILL.md`
(o `AGENT.md`/`WORKFLOW.md`/`PROMPT.md` según el tipo), lee antes `.SKILLS/docs/CONVENTIONS.md` para
las carpetas por categoría, la regla plana (<5 archivos en plano), la convención de versiones (SemVer:
MAJOR/MINOR/PATCH) y los conjuntos multilingües (núcleo: DE+EN obligatorio). **`visibility` siempre
empieza en `private-only`**: publicar es una decisión posterior y verificada del usuario (`.AI/VISIBILITY-POLICY.md`),
nunca el valor por defecto. Estos campos son puramente **aditivos** al formato de Anthropic (claves YAML
adicionales junto a `name`/`description`): cada skill así generada sigue siendo totalmente
`anthropic_compatible: true`.

### Paso 3 — Aplicar los principios: neutral respecto al proveedor, al usuario y a ellmos, pero sensible a ellmos

Texto completo y patrones de código: `references/ELLMOS-PRINCIPLES.md`. Resumen: la skill generada debe ser **funcional por sí
sola** (trae todo lo que necesita) y, **al mismo tiempo**, usar los componentes de ellmos en cuanto estén
disponibles; lo decide ella misma en tiempo de ejecución, nunca mediante cableado fijo. Es exactamente el patrón
que ya ofrece `grounding-seed` (README: "cultivated landscape, not wildflower" / "viable alone, more productive
together"): **no se inventa un segundo mecanismo de detección**; esta skill remite de forma coherente las skills
producidas a `grounding_seed.detect_ecosystem()`.

### Paso 4 — Incluir config.json y connections.json

`grounding-seed` ya es importable como paquete de Python (verificado el 2026-08-24: `import grounding_seed` se resuelve
correctamente en el árbol de fuentes del clon local de `grounding-seed`, clon del Plan D); es el **punto de
acoplamiento canónico**, no hay que inventar un archivo nuevo. Para cada skill producida con necesidades externas
(programas, servicios, proveedores):

- **`config.json`**: ajustes propios de la skill (plantilla: `templates/skill-config.template.json`). `grounding_seed.store.LocalStore(root)` usa este
  nombre de archivo por defecto para su almacenamiento de roles; una skill producida puede, por tanto, usar su
  propio `config.json` como backend de `LocalStore`, o mantenerlo separado si además de roles necesita
  ajustes de comportamiento puros (en ese caso, una segunda instancia de `LocalStore(root, filename="connections.json")`).
- **`connections.json`**: los puntos de acoplamiento externos **efectivamente resueltos** (qué programa o servicio
  se encontró, desde cuándo y con qué procedencia), plantilla: `templates/skill-connections.template.json`, esquema `ellmos.source-resolver.user-config.v1`
  (idéntico a `source-resolver`; según el README de grounding-seed, se eligió a propósito para que una migración
  posterior al `source-resolver` real no pierda datos, véase `migration.py` allí).

Detalles, CLI y ejemplo de código: sección "Docking" de `references/ELLMOS-PRINCIPLES.md`.

### Paso 5 — Incorporar la conciencia de proveedores y fabricantes

Texto completo: `references/VENDOR-AWARENESS.md`. Resumen: la skill producida recibe una sección "Proveedores y alternativas" que
(a) nombra el/los proveedor(es) del estado del arte del tema (por ejemplo, ElevenLabs para TTS), (b) al menos un
proveedor alternativo, (c) enumera **los componentes propios de ellmos como candidatos de igual rango** cuando
cubren el tema (por ejemplo, `ellmos-voice-io` en lugar de o junto a ElevenLabs), y, si la petición del usuario
lo encaja, **propone** la instalación o el cambio en lugar de darlos por supuestos en silencio. La base para saber
"qué hay en el sistema" es `grounding_seed.scan.scan_resources([...])` (que comprueba `shutil.which`), más `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` para los
candidatos de ellmos.

### Paso 6 — Configurar la autoactualización

Texto completo: `references/SELF-UPDATE.md`. Resumen: cada skill producida recibe una sección "Autoactualización" que
(a) propone periódicamente una breve búsqueda en la web para mantenerse al día con el estado del arte,
(b) conoce las skills y flujos relacionados y nombra nuevas alternativas que podrían encajar mejor, y
(c) mantiene un pequeño JSON de aprendizaje (plantilla: `templates/skill-connections.template.json`, campo `notizen`/`gelernt`) que,
si existe el componente de memoria de ellmos (USMC/Gardener), puede externalizarse en lugar de crecer localmente.
También aquí: detectar en lugar de cablear (`grounding_seed.detect_ecosystem()`).

### Paso 6b — Crear el contrato de aprendizaje y la cobertura de casos de uso (patrón reutilizable)

Texto completo: `references/LEARNING-CONTRACT-AND-COVERAGE.md`. Resumen: no solo esta skill, sino **cada skill que ella produce**
recibe un pequeño conjunto reutilizable de archivos de aprendizaje y cobertura, verificado frente a estándares
establecidos, sin estándar paralelo:

- `evals/evals.json`: **reutilizar**, no duplicar; ya es el estándar de skill-creator para casos de prueba
  diseñados por el autor.
- `user-usecases.json`: casos de uso que el usuario realmente ha planteado, con la misma forma que
  `evals.json` (plantilla: `templates/user-usecases.template.json`).
- `usecase-gaps.json`: contraste: qué casos de uso del usuario están sin probar o sin cubrir
  (plantilla: `templates/usecase-gaps.template.json`).
- `known-providers-and-abilities.json`: espacio de candidatos de proveedores conocidos por rol, con campos alineados con
  A2A/`AgentSkill` (id/name/description/tags), no inventados (plantilla: `templates/known-providers-and-abilities.template.json`).
- `gap-closing-analysis.json`: vías estructurales de cierre por cada brecha (módulo de ellmos, paquete de ellmos,
  módulo externo, desarrollo nuevo); no duplica `grading.json.eval_feedback` (plantilla: `templates/gap-closing-analysis.template.json`).
- Campo `config.json` de `lernvertrag`: códice de comportamiento (elegir la mejor opción, **el usuario
  es el rey**, nunca instalar por cuenta propia, intervalo de actualización); se decidió de forma deliberada como
  extensión de `config.json` y no como un séptimo archivo.

Esquemas: `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json`; sigue la misma convención de la casa que `skill-v1.schema.json`.
`grounding-seed` se revisó para este conjunto de archivos y se decidió **no** ampliarlo (motivo en
`LEARNING-CONTRACT-AND-COVERAGE.md`); solo `connections.json` forma parte de él.

### Paso 7 — Registrar, probar, confirmar

- Elige la carpeta de categoría según `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md`; si tienes dudas, pregunta por
  `skill-finder` o `controlcenter_find_skill` para saber si ya existe una familia.
- Ejecuta `testing/` (privacy_gate + pruebas de metadatos) antes de confirmar los cambios.
- **No edites a mano** los archivos de registro (`registry/components.json`, `SKILLS-MAP.md`, `llms.txt`): se generan
  (`build_public_registry.py`, `build_skills_map.py`, `catalog.py`). Si en el clon canónico hay en curso una sesión ajena
  sin confirmar, NO regeneres globalmente (mezclaría cambios ajenos y propios en un mismo archivo); confirma en
  aislamiento la nueva carpeta de la skill y deja la regeneración del registro para la siguiente ejecución limpia
  (`skill-register-care`).
- `git commit -- skills/<kategorie>/<name>/`: solo las rutas propias y nuevas.

## Compatibilidad con el formato de Anthropic

Todos los campos adicionales son extensiones YAML puras junto a `name`/`description`: un Claude Code
estándar fuera de este ecosistema seguirá leyendo solo `name`/`description` e ignorará el resto.
`config.json`/`connections.json` son recursos opcionales incluidos (como se prevé en `docs/CONVENTIONS.md`), no una
dependencia obligatoria: una skill sin ellos funciona igual.

## Skills relacionadas

- `skill-creator:skill-creator`: bucle genérico de entrevista y evaluación (en el que se delega, paso 1).
- `skill-finder`: enrutador de skills propias existentes (comprobar ANTES de construir: ¿ya existe?).
- `skill-explorer`: auditoría del panorama y búsqueda web de nuevas skills/plugins (nivel meta: el *conjunto*
  de nuestras skills; esta skill, en cambio, hace que cada skill *producida* sea consciente del proveedor).
- `skill-family-care`, `skill-register-care`: mantenimiento tras la creación.
- `grounding-seed` (módulo, `.AI/.MODULES/.CONTROL/grounding-seed`): la lógica real de acoplamiento y autoabastecimiento, aquí solo
  referenciada, no duplicada.

## Registro de cambios

### 0.2.0 (2026-08-24)
- Complemento (ticket T-20260824-218233618, ampliación de alcance): añadido el patrón reutilizable de
  aprendizaje y cobertura para cada skill producida: `user-usecases.json`, `usecase-gaps.json`, `known-providers-and-abilities.json`,
  `gap-closing-analysis.json` (nuevos esquemas de la casa en `.SKILLS/schemas/`) más el campo de contrato de aprendizaje en
  `config.json`. `evals/evals.json` (skill-creator) se reutiliza a propósito en lugar de duplicarlo. `grounding-seed`
  revisado: no requiere ampliación (motivo en `references/LEARNING-CONTRACT-AND-COVERAGE.md`), por lo que no hay ticket de seguimiento. Los nombres
  de campo de los catálogos de proveedores se alinean con el protocolo A2A (`AgentSkill`) en lugar de usar
  vocabulario propio.

### 0.1.0 (2026-08-24)
- Versión inicial. Decisión de desarrollo propio frente a fork tomada y justificada (ticket
  T-20260824-218233618). Delega la creación genérica de skills en `skill-creator:skill-creator` y añade el scaffold de la casa,
  los principios de ellmos, la integración `grounding-seed` (config.json/connections.json), la conciencia de
  proveedores y la autoactualización.
