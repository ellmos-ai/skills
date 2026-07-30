---
name: skill-extractor
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: Extrae un skill reutilizable de un historial de chat (sesión actual o archivos de transcripción) — o mejora un skill existente muy similar en lugar de crear un duplicado. Utiliza este skill al solicitar "haz un skill de esto", "deberíamos registrar esto como un skill", "extrae skills de estos historiales de chat antiguos", "haz que esta forma de trabajar sea reutilizable", o al usar `/skill-extract`. También cubre ejecuciones masivas sobre muchas transcripciones antiguas (con reducción de datos mediante subagentes). Para AUTOMATIZACIONES recurrentes (Cron/Schedule/Loop), utiliza en su lugar el skill hermano workflow-extract.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, extraction, transcript, chatverlauf, meta, dedup, neutralisierung, workflow]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `skill-extractor`.


<img src="banner.png" width="100%" alt="skill-extractor banner">

# Skill-Extractor — Obtención de skills a partir de historiales de chat (Español)

## Descripción general y propósito

Las formas de trabajar valiosas surgen en las sesiones: un problema se resolvió con esfuerzo, el usuario realizó varias correcciones y al final queda un procedimiento funcional — y la próxima vez el agente vuelve a empezar desde cero. Este skill destila lo que vale la pena conservar de un historial de chat y lo convierte en un skill según las convenciones de la biblioteca de skills local. Principio fundamental: **Ampliar antes de crear de nuevo** — si existe un skill muy similar, se mejora en lugar de crear un duplicado.

Diferenciación: El resultado aquí es un **skill ejecutable** (capacidad/procedimiento que un agente carga según sea necesario). Si el historial debe convertirse en una **automatización autónoma** (prompt recurrente, cron, programación), se debe utilizar el skill hermano `workflow-extract`.

## Procedimiento

### 1. Determinar la fuente

Tres formas de entrada:

| Fuente | Acceso |
| --- | --- |
| **Sesión actual** | Usar el contexto de la conversación directamente — no se necesitan archivos |
| **Transcripciones individuales** | Leer archivos; ubicaciones y análisis sintáctico: `transcript-quellen.md` |
| **Masivo (muchos historiales antiguos)** | Primero reducción de datos mediante subagentes, luego extracción: sección "Modo masivo" |

### 2. Identificar lo que vale la pena extraer

No todas las sesiones contienen un skill. Busca estas señales — indican dónde se encuentra el conocimiento adquirido con esfuerzo que se necesitará de nuevo:

- **Repetición:** El mismo flujo ocurrió ≥2 veces (en esta sesión o a lo largo de varias sesiones).
- **Bucles de corrección:** El usuario reajustó el agente varias veces hasta que fue correcto — la versión final es el destilado, las correcciones son las justificaciones ("por qué así").
- **Marcadores explícitos:** "recuerda esto", "siempre lo hacemos así", "la próxima vez hazlo directamente así".
- **Cadenas de herramientas:** Una secuencia no obvia de herramientas/comandos que funcionó (incluidas las vías sin salida que deben evitarse).
- **Reglas de decisión:** Criterios mediante los cuales se eligió entre alternativas.

Registra para cada candidato: Desencadenador (cuándo se necesita), Procedimiento (pasos), Justificaciones (por qué así y no de otra forma), Dificultades (qué salió mal), Formato de resultado.

### 3. Filtro de duplicados (Dedup-Gate): Ampliar antes de crear de nuevo

Antes de escribir cualquier cosa, examina el entorno existente:

1. Buscar palabras clave del candidato en los directorios de skills (carpeta de despliegue del agente, p. ej., `~/.claude/skills/`, y — si existe — la biblioteca de skills curada como fuente de verdad; así como skills de plugins registrados).
2. **Leer** detenidamente los 2 o 3 skills más cercanos, no solo comparar nombres.
3. Decidir:

| Hallazgo | Acción |
| --- | --- |
| El candidato ya está cubierto en lo esencial | **Ampliar:** incorporar los elementos faltantes en el skill existente (nueva sección, nueva técnica, nueva dificultad), incrementar la versión MINOR, añadir entrada en el registro de cambios |
| Traslape parcial, pero núcleo diferente | **Nuevo skill** con referencia cruzada ("Skills relacionados") a los vecinos — no duplicar contenido, sino referenciarlo |
| Nada comparable | **Nuevo skill** |

Regla general: Si más de la mitad del candidato está incluida en un skill existente, se amplía. Un catálogo de skills lleno de gemelos casi idénticos es peor que un skill bien mantenido.

### 4. Neutralizar

El material bruto está lleno de detalles específicos de la sesión. Antes de escribir, abstraer según las reglas de `neutralisierung.md`: separar la mecánica (generalmente aplicable) de la configuración (específica del usuario/sistema), reemplazar rutas/hosts/nombres concretos por marcadores de posición o un bloque de configuración claramente marcado. Objetivo: El skill funciona para otros usuarios, otros sistemas u otros proyectos.

### 5. Escribir el skill

- **Formato:** Respetar las convenciones de la biblioteca destino (frontmatter, esquema de nombres, idioma, registro de cambios). En esta biblioteca: `docs/CONVENTIONS.md` (encabezado YAML completo, nombre en kebab-case, alemán como idioma primario, versionado semántico).
- **Formular la descripción de forma descriptiva y persuasiva:** La descripción es el mecanismo de activación. Escribe tanto QUÉ hace el skill como CUÁNDO debe activarse (formulaciones típicas de usuarios) — los skills suelen activarse con menor frecuencia de la deseada.
- **El porqué antes del qué:** Incorporar al skill las justificaciones de los bucles de corrección. Un skill que solo enumera pasos se aplicará incorrectamente en el primer caso especial; uno que explica por qué se puede adaptar.
- **Documentar dificultades:** Las vías sin salida de la sesión son muy valiosas — inclúyelas como una sección de "Banderas rojas" o "Dificultades".
- **Mantenerlo ligero:** Menos de ~300 líneas; externalizar el material detallado en archivos de referencia a los que apunte `SKILL.md`.

### 6. Wrapper de comando (opcional)

Si el skill se va a invocar directamente de forma regular, crea un comando de barra inclinada (en Claude Code: un archivo Markdown corto en `~/.claude/commands/<name>.md` que apunte al skill y pase los argumentos). Convención: Comando = punto de entrada ligero, el contenido reside en el skill.

### 7. Registrar y probar

- Guardar en la biblioteca (categoría correcta) y desplegar en el entorno (aquí: `python skill_sync.py deploy <name>` — la instalación inicial requiere el nombre explícito).
- Prueba de activación: Formular 2 o 3 prompts realistas que deberían activar el skill y verificar si la descripción surte efecto.
- Para un bucle de evaluación completo (casos de prueba, comparación con línea base, optimización de descripción), usa `skill-creator` si está instalado — este skill es el extractor, no el laboratorio de pruebas.
- Mantenimiento de índice/enrutamiento: Actualizar los skills de búsqueda/índice de skills si existen (aquí: `code-skill-index`, tabla de enrutamiento de `skill-finder`).

## Modo masivo: muchos historiales de chat antiguos

Las transcripciones son grandes (a menudo >100k tokens); nunca cargues todas en bruto en un solo contexto.
Map-Reduce mediante subagentes (patrón: skill `swarm-operations`, enjambre de tareas):

1. **Inventario:** Listar archivos de transcripción (ubicaciones: `transcript-quellen.md`), agrupar por proyecto/período. Para colecciones muy grandes, reducir primero con colectores/extractores existentes (p. ej., conjuntos de datos de oyentes de prompts/estudios que solo contienen prompts de usuario) — los prompts de usuario + correcciones contienen la mayor parte de la señal.
2. **Map:** Un subagent por paquete con una tarea delimitada: "Lee estas transcripciones, informa sobre candidatos a skill como una lista compacta (desencadenador, procedimiento, justificaciones, dificultades, sesión de origen)" — devolver solo los destilados, nunca texto bruto.
3. **Reduce:** Fusionar listas de candidatos, agrupar, consolidar duplicados. La frecuencia cuenta: Un patrón que aparece en 5 sesiones es un candidato más fuerte que un truco puntual.
4. **Filtro + Construcción:** Ejecutar los pasos 3–7 del flujo normal para los principales candidatos. Presentar al usuario una lista numerada de candidatos para su selección antes de la creación masiva — de lo contrario, la extracción masiva genera basura de skills.

## Ejemplo y aplicación

```text
User: „Wir haben jetzt dreimal PDF-Rechnungen nach demselben Schema geparst —
mach daraus einen Skill."

1. Quelle: aktuelle Session. Signal: Wiederholung (3×) + Korrektur („Beträge immer
   als Dezimalzahl mit Punkt, nicht Komma").
2. Dedup-Gate: Suche findet `pdf`-Skill (generisch, Erzeugung/Extraktion) — Kern
   überlappt nicht (hier: Rechnungs-Schema + Validierungsregeln) → neuer Skill
   `invoice-parsing` mit Querverweis auf `pdf`.
3. Neutralisieren: konkreter Ablageordner und Firmenname → Konfigurationsblock.
4. Skill schreiben: Schema-Tabelle, die Komma/Punkt-Korrektur als Fallstrick,
   Changelog 1.0.0. Trigger-Test mit „lies diese Rechnung ein".
```

## Banderas rojas

| Pensamiento | Realidad |
| --- | --- |
| "Crearé rápidamente un nuevo skill" | Primero el filtro de duplicados — ampliar antes de crear de nuevo. |
| "Dejaré las rutas, ya que es para este sistema" | La neutralización es obligatoria; los detalles concretos pertenecen a un bloque de configuración. |
| "El historial es largo, resumiré de memoria" | Buscar específicamente señales (correcciones, marcadores) — la memoria suaviza precisamente los puntos que hacen valioso al skill. |
| "Cada sesión genera un skill" | Sin señales de repetición/corrección/marcador: no hay skill. |

## Skills relacionados

- `workflow-extract` — misma extracción, pero el objetivo es una automatización autónoma.
- `skill-explorer` — auditoría/limpieza del entorno de skills (utiliza el filtro de duplicados a gran escala).
- `skill-creator` (plugin) — bucle de evaluación y optimización de descripciones para skills terminados.
- `swarm-operations` — patrón de enjambre para el modo masivo.

## Registro de cambios

### 1.0.0 (2026-07-03)
- Versión inicial. Creada a partir del encargo de abstraer sistemáticamente las automatizaciones de Codex e historiales de chat en skills.