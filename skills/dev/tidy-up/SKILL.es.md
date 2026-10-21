---
name: tidy-up
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: "Ejecución única de solucionador de tareas, redactor y mantenedor sobre la carpeta del proyecto en la que la sesión ya estaba trabajando (incluidas las subcarpetas) — no es un barrido de todo el sistema. Resuelve los puntos triviales o autónomos abiertos del registro, actualiza la documentación al estado real medido (tanto en el proyecto COMO en la raíz de la canalización en la que se encuentra el proyecto) y retira los restos y archivos temporales según el principio de la papelera. Usa esta habilidad con /tidy-up, \"limpia el proyecto\", \"ordena esto antes de seguir\", al final de una sesión de trabajo en un proyecto, o como tarea autónoma pendiente dentro de /work-autonomous + /goal."
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [hygiene, maintenance, cleanup, documentation, tasksolver, writer, maintainer, autonomy, goal, work-autonomous, ticket-master]
language: es
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: [work-autonomous, bilingual-doc-sync]
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 27510ce60a4dd2defe9ee4686aeae6378ce8aea2f2376b98163d1d1340960233
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="tidy-up banner">

# Tidy Up — Ejecución de solucionador de tareas, redactor y mantenedor para la carpeta activa del proyecto

## Propósito

Al final de una sesión de trabajo en un proyecto suelen quedar pequeños pendientes: un punto TODO completado que nunca se marcó; un README que muestra el estado antiguo en lugar del estado medido; un puñado de archivos de prueba que ya nadie necesita. `tidy-up` es una **ejecución única y autolimitada** que pone al día exactamente eso para **una** carpeta de proyecto — aquella en la que la sesión ya estaba trabajando. No es un bucle permanente ni un barrido de todo el sistema.

La ejecución consta de tres roles que el propio modelo asume uno tras otro:

1. **SOLUCIONADOR DE TAREAS (TASKSOLVER)** — resolver o clasificar correctamente los puntos abiertos, triviales o autónomos, del registro del proyecto.
2. **REDACTOR (WRITER)** — actualizar la documentación al estado real medido, tanto en el proyecto COMO en la raíz de la canalización en la que se encuentra el proyecto.
3. **MANTENEDOR (MAINTAINER)** — higiene: recoger restos y archivos temporales (principio de la papelera), mantener el registro y el catálogo, y archivar los pendientes restantes en lugar de mencionarlos solo en el chat.

**Medido antes de construir esta habilidad:** en esta biblioteca (estado del 2026-08-19) **no existen** habilidades independientes ni roles con los nombres `tasksolver`/`writer`/`maintainer` — ni como nombre de habilidad ni como rol documentado en otra habilidad (búsqueda de texto completo sobre `skills/**/SKILL.md`, sin coincidencias salvo un nombre no relacionado, `privat-mail-writer`). Por ello, los tres roles se definen directamente más abajo como secciones, no se orquestan externamente. Si más adelante surgen habilidades independientes `tasksolver`/`writer`/`maintainer`, `tidy-up` las asumirá mediante referencia en lugar de seguir duplicando la lógica (verificación obligatoria en cada evolución de esta habilidad).

## Alcance — ¿qué cuenta como "la carpeta activa del proyecto"?

- La carpeta del proyecto en la que la sesión trabajó en este contexto, **incluidas todas las subcarpetas**. Sin saltos a proyectos vecinos, sin barrido de una canalización completa ni de `.TOPICS/` en su totalidad.
- **Una** excepción acotada: la actualización de documentación o registro puede tocar además el **nivel raíz de la canalización** en la que se encuentra el proyecto (p. ej., una línea de estado para este proyecto en una tabla de resumen de toda la canalización) — pero solo la línea o sección que afecta a este proyecto, no reordenar toda la raíz de la canalización.
- Si no está claro cuál es "la carpeta activa del proyecto" (p. ej., la sesión trabajó en varias carpetas), tomar la raíz común más cercana del proyecto (donde se encuentran README/TODO/CLAUDE.md del proyecto); en caso de duda, acotar más en lugar de ampliar.

## Rol 1 — SOLUCIONADOR DE TAREAS (TASKSOLVER)

Objetivo: llevar el registro del proyecto (`TODO.md`/`AUFGABEN.txt`/convención local equivalente) a un estado correcto y actual.

1. Localizar el registro del proyecto (la convención local tiene prioridad sobre crear un archivo nuevo — véase la regla "Las tareas pendientes se archivan, no se mencionan" en el reglamento global).
2. Evaluar cada punto abierto por separado:
   - **Ya completado** (p. ej., por la sesión que acaba de terminar) → marcar como completado / trasladar a `DONE.md` o a la convención local de completados.
   - **Trivial y resoluble de forma autónoma** (no requiere decisión, aprobación, datos, hardware ni sesión del usuario; véase la tabla de delimitación en `work-autonomous`) → resolverlo ahora y luego archivarlo como completado.
   - **No trivial o no autónomo** → NO tocarlo, pero dejarlo archivado correctamente (no dejarlo sin comentario si existe un lugar mejor — p. ej., un punto que hace tiempo merecía una categoría de ticket `USER/*`).
3. No inventar tareas nuevas — `tidy-up` resuelve los restos existentes, no genera una agenda nueva.

## Rol 2 — REDACTOR (WRITER)

Objetivo: que la documentación muestre el estado **medido**, no el recordado ni el deseado.

1. En el proyecto: comprobar README/CHANGELOG/líneas de estado frente a la situación real del código y de las carpetas (p. ej., los archivos mencionados aún existen, el número de versión indicado es correcto, la marca "en curso" no está completada desde hace tiempo).
2. En la raíz de la canalización: si existe allí un registro o una tabla de estado que liste este proyecto (p. ej., `.TOPICS/<Pipeline>/ROADMAP.md`, `STATUS.md`, una tabla de proyectos en el README de la canalización), actualizar la línea/sección de EXACTAMENTE este proyecto.
3. **Nunca reemplazar contenido curado, solo medir y actualizar.** Las tablas, changelogs o secciones cuidadosamente redactadas conservan forma y tono — solo se corrigen los hechos (cifras, estado, nombres de archivo, versiones). Si hay dudas sobre si una sección está curada, es preferible añadir una nota que sobrescribir una formulación existente.
4. No reescribir desde cero cuando basta con una actualización.
5. **Seguimiento de traducciones** (complemento del 2026-08-19, encargo directo del usuario): si al proyecto le falta una versión lingüística que la **política P-006** (`.SYNC/_policies/library/P-006_sprachstufen.md`) exige para su nivel, o si una versión existente está claramente desactualizada, el paso REDACTOR la pone al día. Resumen de P-006: el **conjunto básico (DE+EN) es obligatorio** para todo repositorio publicado u objeto catalogado (repositorio: `README.md` EN + `README_de.md`; habilidad: `SKILL.md` DE + `SKILL.en.md`); los conjuntos completo/mundial (ES/ZH/JA/RU o bien +FR/HI/AR/BN/PT) son el objetivo, pero se completan **poco a poco**, no en una sola campaña a través de `tidy-up`. **Herramienta: la habilidad existente `bilingual-doc-sync` se orquesta (se invoca), su lógica NO se duplica** — ya cubre exactamente "completar una versión faltante" + verificación de paridad de secciones + corrección de divergencias. `tidy-up` solo aporta el impulso (qué objeto, qué idioma obligatorio falta según P-006) para la carpeta activa del proyecto; la calidad de la traducción, la paridad estructural y la regla del idioma principal siguen siendo responsabilidad de `bilingual-doc-sync`. **Límites iguales a los de P-006:** traducir solo hasta el estado real medido, no inventar contenido, respetar las tildes y diacríticos reales, el enfriamiento del repositorio (<24 h desde el último commit) y los bloqueos activos — en tal caso dejar este punto sin traducir y archivarlo como pendiente (Rol 3) en lugar de forzarlo.

## Rol 3 — MANTENEDOR (MAINTAINER)

Objetivo: higiene sin que se pierda nada.

1. **Recoger restos/archivos temporales** (restos de scripts, `*.tmp`, copias duplicadas, salidas de depuración olvidadas) — principio de la papelera: trasladarlos a una carpeta local `_archive/` (crearla y registrarla en `.gitignore` si aún no existe), **nunca borrarlos directamente**. Si el origen o la finalidad de un hallazgo no está claro: averiguar activamente su finalidad (leer el archivo), no retirarlo sin leerlo — véase la convención "certificar a posteriori los cambios ajenos".
2. **Mantenimiento de registro/catálogo:** si el proyecto forma parte de un catálogo o registro más grande (registro de habilidades, manifiesto de módulos, resumen de la canalización), comprobar que la entrada de este proyecto siga siendo correcta — no reconstruir todo el registro, solo esta única entrada.
3. **Archivar los pendientes restantes en lugar de mencionarlos en el chat:** lo que quede al final de esta ejecución (puntos no resolubles de forma autónoma, defectos detectados pero no corregidos, elementos aplazados deliberadamente) se archiva según la regla "Las tareas pendientes se archivan, no se mencionan" — principalmente de forma local en el lugar del hallazgo (convención TODO.md/AUFGABEN.txt del proyecto), si no, de forma centralizada (`ticket-master`/`TASKPLAN`), siempre con contexto (qué es, por qué está abierto, siguiente paso).
4. **Respetar los bloqueos:** antes de cada cambio, comprobar si hay un `LOCK.txt`/`LOCK.<scope>.txt`/`LOCK.user.*` activo en la carpeta del proyecto. Un `LOCK.user.*` detiene a `tidy-up` por completo en el área afectada — sin sortearlo y sin una limpieza parcial del área bloqueada.
5. **Commit y push solo según la convención del repositorio del proyecto** — cuando existan superficies separadas de planificación y de desarrollo, realizar los cambios en el clon local autorizado del proyecto, no en una copia de planificación o de proyección.
   Los cambios propios se tratan según la convención global de "commit y push inmediatos", cuando el proyecto lo prevea.

## Autolimitación

`tidy-up` es **una ejecución, no un bucle**. Tras el Rol 3, la habilidad termina con un breve resumen (qué se resolvió, qué se actualizó, qué se limpió, qué quedó archivado como pendiente) y devuelve el control a la sesión que la invocó. Una nueva llamada a `/tidy-up` en el mismo proyecto poco después está permitida, pero no es automáticamente útil — véase el criterio de vencimiento más abajo.

## Relación con work-autonomous

Las ejecuciones de `tidy-up` **cuentan como tarea ejecutable de forma autónoma en el sentido del Nivel 1 de `work-autonomous`** (trabajo normal y visible — sin motivo para pasar a la costosa comprobación de agotamiento del Nivel 2 mientras haya una ejecución de `tidy-up` vencida). En la práctica: si `/work-autonomous` se usa junto con `/tidy-up` dentro de un `/goal`, el objetivo solo se considera completado cuando también se hayan resuelto los puntos vencidos de `tidy-up` — siempre que sean ejecutables de forma autónoma (véase la tabla de delimitación en `work-autonomous`; un punto de `tidy-up` que requiera una decisión del usuario no cuenta como autónomo, igual que cualquier otra tarea vinculada a `USER/*`).

**Criterio de vencimiento** (¿cuándo está "vencida" una ejecución de `tidy-up`?):

1. La sesión ya ha trabajado en este contexto sobre una carpeta de proyecto concreta (no: solo investigación o lectura sin cambios — entonces no hay nada que limpiar).
2. Desde la última ejecución registrada de `tidy-up` para ESTE proyecto ha transcurrido el enfriamiento (por defecto: 1 vez por cierre de sesión en este proyecto — no más de una ejecución **dentro** de la misma sesión sin cambios nuevos desde la última).
3. Ningún `LOCK.user.*` activo bloquea la carpeta del proyecto (véase el Rol 3, punto 4).

Registro de la última ejecución (análogo al patrón de guardia de `work-autonomous`, pero deliberadamente más sencillo — `tidy-up` no necesita una cadena de cuatro pasos, solo una marca de tiempo por proyecto):

```bash
usmc --agent <agent> note "tidy-up: project=<projekt-pfad-oder-slug> at=<ISO-Zeit> result=<done|nothing-to-do>" \
  --type context --priority 2 --tags "tidy-up-log,<projekt-slug>"
```

Antes de una nueva ejecución, leer el mismo día (`usmc --agent <agent> working --limit 20` filtrado por `tidy-up-log,<projekt-slug>`) para comprobar el criterio 2.

Un constructo `/goal` (si existe o se construye — el propio `work-autonomous` no invoca ningún `/goal`, véase su sección "Deliberadamente sin `/goal` integrado") lee este criterio de vencimiento del mismo modo que lee su propia señal de aborto de `work-autonomous`: si una ejecución de `tidy-up` está vencida Y es ejecutable de forma autónoma, el objetivo aún no ha terminado — independientemente de si la cadena de cuatro pasos propia de `work-autonomous` ya informa "agotado".

La entrada complementaria, mínimamente invasiva, en la propia habilidad `work-autonomous` (Nivel 1, nueva fuente "ejecuciones de tidy-up vencidas del proyecto activo") forma parte de esta ampliación — véase la entrada del changelog correspondiente.

## Habilidades relacionadas

- **`work-autonomous`** — véase arriba; `tidy-up` es una de las fuentes que procesa el Nivel 1 de `work-autonomous`, no un sustituto de su comprobación de agotamiento.
- **`bilingual-doc-sync`** — la orquesta el Rol 2 (REDACTOR) para el seguimiento de traducciones (véase allí), sin duplicarla. `tidy-up` decide solo QUÉ falta según P-006; `bilingual-doc-sync` decide CÓMO se traduce y sincroniza.
- **`bugsweep`** — búsqueda sistemática de errores con escalada por duplicación. Propósito distinto (encontrar fallos, no mantener registro/documentación/higiene) — si hay solapamiento (un hallazgo de la búsqueda de errores acaba en el registro), `tidy-up` solo asume el mantenimiento del registro, no la búsqueda de errores en sí.
- **`dev-cycle`** — marco de 8 fases para el desarrollo de nuevas funciones. `tidy-up` no es un marco de desarrollo, sino una ejecución de cierre/higiene tras trabajo ya realizado.
- **`folder-flattening`** — reestructura jerarquías de carpetas anidadas. `tidy-up` limpia archivos dentro de la estructura existente y no cambia la estructura en sí.

## Ejemplos

```
User: "/tidy-up"
(Session hat gerade am autorisierten lokalen Checkout von `beispiel-projekt` gearbeitet)

→ TASKSOLVER: TODO.md gelesen — 2 Punkte bereits durch die Sitzung erledigt (nach DONE.md
  verschoben), 1 trivialer Punkt ("README-Tippfehler in Zeile 12") autonom geloest, 1 Punkt
  braucht Nutzerentscheidung (unveraendert stehen gelassen).
→ WRITER: README-Versionsangabe war 1.2.0, tatsaechlich 1.3.0 (package.json) — korrigiert.
  Pipeline-Root-Statustabelle: Zeile fuer "beispiel-projekt" von "in Arbeit" auf "aktiv" gesetzt.
→ MAINTAINER: 3 Debug-Skripte im Projektroot gefunden, nach _archive/ verschoben (Zweck geprueft:
  einmalige Testskripte, nicht mehr referenziert). Skill-Registry-Eintrag geprueft: stimmt.
  1 offener Punkt (Nutzerentscheidung) in AUFGABEN.txt belassen, dort bereits korrekt einsortiert.
→ USMC-Log geschrieben: tidy-up: project=beispiel-projekt at=2026-08-19T14:30 result=done
→ Zusammenfassung an Nutzer: 3 geloest, 2 Doku-Stellen aktualisiert, 3 Dateien archiviert, 1 Punkt
  offen (Nutzerentscheidung noetig).
```

```
Kombiniert mit /goal + /work-autonomous:

/goal "Projekt X fertigstellen" mit /work-autonomous + /tidy-up als Bedingungen
→ work-autonomous Ebene 1 findet: ACTIONABLE-Ticket erledigt, dann kein weiteres Ticket mehr,
  ABER tidy-up-Faelligkeitskriterium erfuellt (Session hat an Projekt X gearbeitet, kein
  protokollierter Lauf seit Sitzungsbeginn, kein LOCK.user aktiv) → tidy-up-Durchlauf ausgefuehrt.
→ Erst NACHDEM tidy-up "done" meldet UND work-autonomous Ebene 2 "exhausted" meldet, gilt das
  Goal als abgeschlossen.
```


## Changelog

### 1.1.0 (2026-08-19)
- Complemento de un añadido en vivo a T-20260819-461890468 (usuario, literal: "bis zu einer uebersetzung nachzuziehen die noch nicht existiert soll auch zum skill gehoeren" — es decir, hasta completar una traducción que aún no existe, también debe pertenecer a la habilidad): el Rol 2 (REDACTOR) recibe un quinto punto, el seguimiento de traducciones según la **política P-006** (niveles lingüísticos: conjunto básico DE+EN obligatorio, completo/mundial poco a poco). La herramienta es la habilidad ya existente `bilingual-doc-sync` — se orquesta, no se duplica. Se añadieron la dependencia en el frontmatter y la entrada en "Habilidades relacionadas".

### 1.0.0 (2026-08-19)
- Versión inicial a partir del ticket T-20260819-461890468. Tres roles (solucionador de tareas/redactor/mantenedor) definidos como secciones de la habilidad, tras una búsqueda de texto completo en la biblioteca que confirmó que no existen habilidades independientes `tasksolver`/`writer`/`maintainer` (de lo contrario se habría orquestado en lugar de duplicar). Alcance limitado a la carpeta activa del proyecto + línea de estado en la raíz de la canalización. Integración con goal: las ejecuciones de `tidy-up` cuentan como fuente del Nivel 1 de `work-autonomous`, con un registro USMC de vencimiento propio y ligero (sin la guardia de cuatro pasos de `work-autonomous` — `tidy-up` es demasiado simple para ello). Se añadió la entrada complementaria, mínimamente invasiva, en `work-autonomous` 1.3.0 (véase su changelog).
