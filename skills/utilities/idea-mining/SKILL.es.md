---
language: es
description: Extraer ideas, filtrar contra el historial y explorar una hasta completarla. Un flujo de trabajo de 5 fases (A-E) para la resolución de problemas complejos.
---

> **Español** — Versión oficial en español de `idea-mining`.

<img src="banner.png" width="100%" alt="idea-mining banner">

# Idea-Mining — Extraer ideas, filtrar, ejecutar una

## Descripción general y propósito

Ante problemas complejos, la generación de ideas raras veces falla por falta de ocurrencias, sino por tres razones: las ideas no se **registran**, no se comprueban contra **lo que ya se ha intentado** (volviendo a caer en los mismos callejones sin salida) y ninguna se **persigue de forma consistente hasta el final**. Este flujo de trabajo separa estrictamente las tres fases: primero, extraer de forma divergente (sin evaluación); luego, filtrar (contra la documentación del proyecto); y, finalmente, explorar SUBSTANCIALMENTE UNA idea.

Origen: destilado de una sesión de automatización de investigación productiva sobre problemas matemáticos abiertos; funciona de igual manera para bloqueos de arquitectura, diseño y conceptos.

## Fase A — Llenar el depósito de ideas (divergente, sin evaluación)

Escribir todos los hallazgos en un archivo `IDEENSPEICHER.md` en la carpeta del proyecto (palabras clave + 2–3 frases, anotar fuente/disparador). Recorrer las ocho técnicas secuencialmente —se dirigen a diferentes espacios asociativos, por lo que en problemas verdaderamente bloqueados no se debe omitir ninguna (para bloqueos menores o tiempo limitado, basta con un subconjunto justificado, pero al menos una técnica blanda de la 3–5 más la investigación):

1. **Reconocimiento:** ¿Me resulta familiar? ¿He visto esta estructura antes en otro contexto?
2. **Disciplina distante:** ¿Existe un problema o fórmula similar en una disciplina lejana (Física↔Economía, Biología↔Informática, …)? ¿Dónde reside exactamente la conexión?
3. **Alegoría cotidiana:** Contar el problema en una alegoría inspirada en la naturaleza (olas, arena, corriente, crecimiento…). Efectivo: hacer que un **subagente imparcial** invente la alegoría y ver a dónde conduce —la propia visión ya está deformada por el problema.
4. **Incomodidad / Rana→Príncipe:** ¿Qué me molesta del estado actual, qué me parece feo? ¿Qué tendría que cambiar para que de repente me parezca hermoso? El malestar estético a menudo señala una representación mal elegida.
5. **Reencuadre de cuento de hadas:** Contar el problema como un cuento de hadas: ¿Quién es el héroe, quiénes los villanos, qué peligros acechan, qué podría ayudar al héroe? La asignación de roles fuerza una estructura causal que permanece invisible en el formalismo.
6. **Investigación:** Buscar en la web, bases de datos especializadas, servidores de preprints, foros (Reddit/ResearchGate/GitHub) nuevas publicaciones, scripts y enfoques. Cargar fuentes relevantes en una carpeta `_sources/` y leer en busca de innovaciones —mantener una postura crítica con los preprints.
7. **Proyectos hermanos:** Revisar proyectos personales/internos relacionados en busca de ideas de solución retrotransferibles (subproblemas resueltos allí, herramientas construidas allí).
8. **Revisión transversal del inventario:** Revisar todo el inventario de proyectos propios (pipeline) en busca de enfoques que puedan encajar en ESTE problema.

## Fase B — Filtro (contra lo ya intentado)

Cotejar el depósito de ideas con la documentación del proyecto: notas de prueba, registros de decisiones, TODO/DONE, depósitos de ideas anteriores. **Se elimina aquello que esté documentado como ya intentado y finalizado** —no lo que simplemente "suene poco probable" (la evaluación por atractivo llega solo en la Fase C). Guardar las ideas supervivientes en `IDEENSPEICHER_FILTERED.md`.

Es requisito previo contar con una documentación de experimentos bien mantenida —si no existe, el primer paso es crearla (de lo contrario, cada ejecución futura producirá duplicación de esfuerzos).

## Fase C — Elegir y ejecutar

1. Explorar brevemente de una a tres ideas del filtrado (un párrafo cada una: ¿cuál sería el primer paso concreto, cuál la señal de éxito?).
2. Elegir **una** —la que tenga la mayor atracción. La atracción es aquí un criterio legítimo: en problemas difíciles, solo una idea que *desees* seguir te llevará adelante.
3. Llevar la elección hasta el final o al menos hacerla avanzar sustancialmente —no saltar a la siguiente idea ante el primer obstáculo (eso sería un comportamiento de Fase A durante la Fase C).

## Fase D — Documentar

- Registrar los hallazgos en la documentación del proyecto (nota de prueba, registro de decisiones, ADR) —**incluidos los fallos**, ya que constituyen el filtro para la siguiente ejecución.
- Devolver las ideas de seguimiento abiertas a `IDEENSPEICHER.md` o TODO.
- Informe breve: extraídas (cantidad) | filtradas (supervivientes) | exploradas | resultado | siguiente paso.

## Fase E — Siembra (transferencia externa opcional)

La Técnica 7 trae ideas DESDE proyectos hermanos —la Fase E invierte la dirección: Si la exploración ha dado un resultado transferible (método, herramienta, patrón de solución), revisar brevemente el inventario de proyectos propios: ¿A quién ayudaría esto?

- **Sembrar de forma selectiva, no dispersar:** Como máximo ~3 proyectos receptores provistos directamente de una entrada TODO concreta (qué adoptar, dónde se encuentra, por qué encaja); anotar otros candidatos solo como una lista priorizada en el proyecto propio.
- Razón del límite: La dispersión amplia crea tareas difusas en muchos proyectos que nadie asume —tres semillas precisas superan a diez difusas.

## Como ejecución periódica

El flujo de trabajo es muy adecuado como automatización recurrente para un proyecto fijo (ronda de innovación). Para ello, combinarlo con la estructura de rotación (skill `rotation-check`): el registro evita que las mismas ideas sean "redescubiertas" múltiples veces —el depósito de ideas y la documentación de experimentos actúan aquí como memoria.

## Ejemplo y aplicación

```text
Problema: Una prueba de convergencia lleva semanas atascada en una estimación.

A) Extracción → IDEENSPEICHER.md: p. ej., (2) ¿estructura similar en la teoría
   de colas?; (3) Alegoría de subagente "la arena cae a través de tamices cada vez más finos" →
   idea: estimar paso a paso en lugar de globalmente; (6) Preprint de 2026 con nuevo
   lema, descargado en _sources/; (7) El proyecto vecino tiene un script de comprobación
   numérica que se puede retrotransferir.
B) Filtro contra BEWEISNOTIZ.md: "reforzar estimación global" se intentó 2 veces
   y se descartó de forma documentada → eliminado. 3 ideas sobreviven → IDEENSPEICHER_FILTERED.md.
C) Elección principal: la idea del tamiz (mayor atracción) — llevada a cabo hasta un resultado parcial.
D) BEWEISNOTIZ.md actualizado (incluido el fallo de la idea 2), informe breve.
```

## Banderas rojas (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "Las técnicas 3–5 son un juego" | Las técnicas blandas aportan las ideas que la investigación no puede proporcionar —abordan diferentes espacios asociativos. |
| "Evalúo mientras recopilo" | La evaluación en la Fase A destruye el rendimiento divergente. Guardar primero, filtrar después. |
| "El filtro tarda demasiado, ya me acuerdo" | La memoria suaviza los intentos fallidos —solo la documentación cuenta. |
| "La idea se atasca, tomo la siguiente" | En la Fase C se sigue adelante; volver a la Fase A solo con un motivo documentado. |

## Skills relacionadas

- `brainstorm` — métodos creativos amplios (SCAMPER, Six Hats) sin pipeline de filtro/exploración.
- `think` / `decide` — análisis y decisión de selección, utilizables dentro de la Fase C.
- `rotation-check` — estructura para despliegue periódico.
- `swarm-operations` — subagentes imparciales para la técnica 3 y exploración paralela.

## Registro de cambios

### 1.1.0 (2026-07-03)
- Fase E "Siembra": transferencia externa opcional de resultados transferibles a
  proyectos hermanos (máx. ~3 receptores directos) —integrada en lugar de un skill
  cross-project-transfer independiente (decisión de deduplicación).

### 1.0.0 (2026-07-03)
- Versión inicial. Abstraído de la automatización Codex "ultra-deep-idea-search-single-project"
  (depósito de ideas → filtro → elección principal → exploración) y generalizado para ser neutro al usuario.