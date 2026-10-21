---
name: reissverschluss-merge
version: 1.0.0
type: skill
language: es
visibility: public
author: Claude (extrahiert aus einer Live-Merge-Session, Multi-Repo-PR-Abarbeitung)
created: 2026-08-07
provenance:
  origin: live-session-extraction
  extracted: 2026-08-07
  method: skill-extractor
updated: 2026-08-07
description: "Procedimiento de cremallera (en inglés: zipper merge) para fusiones con muchos conflictos: cuando dos ramas divergentes o un PR y su rama de destino CONTIENEN AMBOS cambios valiosos que parecen incompatibles, no se elige una parte de forma general, sino que se compara sección por sección, se adopta mediante una tabla de decisión (Tomar/Motivo) la versión mejor en cada caso, se confirma por secciones y solo al final se hace push. Último nivel de escalada: reconstruir en lugar de fusionar — solo adoptar la intención/funcionalidad de la rama y reconstruirla sobre el estado actual. Úsese ante: \"conflicto de fusión\", \"ramas divergentes\", \"main vs. master\", \"PR con conflictos\", \"zipper merge\", \"cremallera\", \"ambas partes tienen razón\", \"el PR es demasiado antiguo para fusionar\"."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
aliases:
  - zipper-merge
  - zipper-verfahren
  - reissverschluss
tags: [git, merge, konflikt, pull-request, branch, rebase, dev-workflow]
translated_from_sha256: 6a31c500a8da2c6d19255bf7601125cf9f2fed39f9387fa0c8e45b11260468ee
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.744053+00:00"
---
<img src="banner.png" width="100%" alt="reissverschluss-merge banner">

# Fusión en cremallera (zipper merge)

## Cuándo usar este procedimiento

Dos ramas del mismo repositorio están **fuertemente divergidas** y **ambas aportan valor** —
típicamente: `main` frente a `master` tras un mantenimiento paralelo, un PR antiguo frente a una
rama de destino que ha avanzado, dos estados de agentes o equipos con correcciones propias.
Una fusión normal eliminaría una parte ("ours"/"theirs") o generaría un caos de conflictos
imposible de desenredar. El procedimiento de cremallera resuelve esto haciendo que los dientes
de ambos lados **encajen sección por sección**: en cada sección gana la versión demostrablemente
mejor, o una mezcla justificada.

**No es necesario** en conflictos triviales (una parte claramente obsoleta,
pocos fragmentos): en ese caso, fusionar normalmente. El procedimiento compensa a partir del punto en el que
hay que sopesar seriamente varios archivos o secciones.

## Fase 0 — Panorama y elección de la base

1. **Revisar ambos lados por completo** (no solo los marcadores de conflicto):
   `git log --oneline A..B` y `B..A`, `git diff A...B --stat`, y después leer los archivos divergentes de ambas versiones.
2. **Elegir la base según la realidad, no según la fecha.** La base será la rama que
   coincida con la **realidad publicada**: estado del registro (npm/PyPI/…), versión desplegada,
   CI en verde, etiquetas de release. Una rama con fecha más reciente pero sin correspondencia
   con el mundo exterior es material, no base.
3. **Comprobar la coherencia de ambos lados** — a menudo AMBOS son incoherentes en sí mismos
   (p. ej., la base tiene la versión X sin el changelog correspondiente, mientras que la otra parte mantiene
   el changelog pero se queda atrás en la versión). Estos hallazgos pertenecen a la tabla, no debajo de la alfombra.

## Fase 1 — Tabla de decisión (el núcleo)

Para cada sección divergente (archivo, bloque, campo — tan fina como sea necesario) una
fila:

| Sección | Tomar | Motivo |
|---|---|---|
| `package.json` → version | Base | coincide con el registro |
| Bloque `overrides` | Otra parte | contiene actualizaciones de seguridad que faltan en la base |
| ↳ dentro la entrada `X` | **mezclar** | adoptar la entrada de la otra parte, pero elevarla a la versión más reciente de la base |
| Changelog `[Unreleased]` | **mezclar** | unificar ambos bloques, eliminar duplicados |

Reglas:

- **Hechos, no suposiciones.** Cada celda "Motivo" se apoya en algo verificable:
  consulta al registro, ejecución de pruebas, base de datos de advisories, instalación de prueba aislada
  del archivo controvertido. Quien adivina, fusiona suposiciones.
- **"Mezclar" es un veredicto legítimo** — la cremallera puede dejar que los dientes de ambos lados
  encajen dentro de una misma sección.
- **Descartar es un veredicto legítimo** — lo que no se sostiene en ningún lado
  (una insignia muerta, una funcionalidad a medio implantar) se elimina. El estado intermedio
  ("funcionalidad a medias") es la peor variante: completamente dentro o completamente fuera.
- La tabla terminada es el **documento de contrato** de la implementación — en un cambio de sesión
  o una entrega, basta para continuar de forma mecánica.

## Fase 2 — Implementación: confirmar por secciones, hacer push al final

1. Iniciar en la base una fusión real: `git merge <gegenseite>`
   (deliberadamente SIN `-X ours/theirs` — los conflictos deben quedar visibles a propósito).
2. Resolver los conflictos **sección por sección** exactamente según la tabla.
3. **Un commit por sección lógica** (o, con un único commit de fusión:
   un paso de resolución documentado por sección en el mensaje del commit).
   Cada mensaje de commit nombra el veredicto de la tabla ("overrides: otra parte +
   vitest elevado al estado de la base"). Así cada diente de la cremallera
   sigue siendo individualmente trazable y revertible.
4. **Pruebas tras la implementación** (suite, build, instalabilidad) — primero en verde,
   luego seguir.
5. **Hacer push solo al final** — el historial local puede reestructurarse durante el procedimiento;
   el remoto solo ve el resultado terminado.
6. **Cerrar la divergencia sin borrar:** llevar la rama perdedora al resultado mediante fast-forward
   (`git checkout <gegenseite> &&
   git merge --ff-only <basis>`). Ambos nombres apuntan después al mismo estado; no se pierde ningún historial.

## Ruta de escalada — reconstruir en lugar de fusionar (último nivel)

Si la cremallera ya no funciona, **no se fusiona, se reconstruye**: se destila la **intención/funcionalidad**
de la rama/PR (QUÉ quería conseguir — no CÓMO) y se implementa de nuevo sobre el estado actual.
La rama/PR antigua se cierra con referencia a la reconstrucción.

Desencadenantes de la escalada (basta uno):

- La otra parte está **demostrablemente defectuosa** (p. ej., nunca fue instalable,
  el build falla) — entonces nunca hubo un estado funcional que fusionar.
- Masa de conflictos ≫ sustancia: el cambio es pequeño, pero está diluido en cientos
  de líneas desplazadas (oleadas de renombrado/formateo intermedias).
- El historial está envenenado (p. ej., el mismo número de versión asignado en ambos lados
  a **contenidos distintos** — una fusión heredaría la mentira).
- El PR es tan antiguo que su contexto (APIs, estructura) ya no existe.

Procedimiento: fijar la intención en 2–5 frases (a partir de la descripción del PR, los commits,
la sustancia del diff) → reimplementar sobre el estado actual → pruebas → documentar en el
PR/rama antigua QUÉ se tomó y QUÉ no se tomó a propósito, y luego cerrar. Nombrar la autoría
de la idea en el texto del commit/PR.

## Trampas (de la sesión original, pagadas caro)

- **El bloque de changelog duplicado** `[Unreleased]` es el punto caliente más frecuente en ramas
  mantenidas en paralelo — unificar siempre, nunca descartar uno en silencio.
- **Ambos lados asignan el mismo número de versión a contenidos distintos:**
  antes de fusionar, aclarar qué número conoce el registro; el otro lado
  recibe una corrección en el changelog unificado.
- **Una fusión es una oportunidad de auditoría:** al leer por secciones, saltan a la vista
  cosas que ninguna rama veía (advisories abiertos, enlaces muertos, pins inconsistentes). Llévate los hallazgos,
  pero como commits propios — no los mezcles con las decisiones de la cremallera.
- **Adoptar "porque es más nuevo":** la fecha no es argumento. Cada adopción necesita
  un motivo verificable.
- **Reflejo del force-push:** el procedimiento funciona sin force-push (fusión +
  fast-forward). Si parece necesario un force, normalmente la elección de la base es errónea.

## Señales de alarma

| Pensamiento | Realidad |
|---|---|
| "Simplemente tomo el lado más nuevo" | Fecha ≠ calidad. Construir la tabla. |
| "Resuelvo los conflictos de una vez" | Un commit colectivo hace irrevisable cada decisión individual. |
| "Hago push entre medias" | Las crémalleras a medio terminar en el remoto confunden a cualquier lector. Push solo al final. |
| "Fusionar siempre sale de algún modo" | Con una contraparte defectuosa o un historial envenenado, reconstruir es más honesto y más rápido. |
| "La tabla es excesiva" | Sin tabla, tras el tercer archivo se olvida por qué la sección 1 se decidió así. |

## Skills relacionadas

- `bugfix-protocol` — si la fusión descubre un defecto real, continuar allí.
- `skill-extractor` — origen de este skill (destilado de una sesión en vivo).
- `human-loop-audit` — comparte solo la imagen de la cremallera, pero no tiene nada que ver con las fusiones de Git
  (procedimiento interactivo de pruebas de aplicaciones/GUI con el usuario).

## Changelog

### 1.0.0 (2026-08-07)
- Versión inicial. Extraída de una sesión de fusión en vivo del 2026-08-06
  (unificación main/master de varios repositorios con tabla de decisión, hallazgo de una
  contraparte nunca instalable, cierre mediante fast-forward; caso de escalada
  "adoptar la intención, reconstruir").
