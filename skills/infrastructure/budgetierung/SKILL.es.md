---
name: budgetierung
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-10-03
updated: 2026-10-03
description: "Concepto de cuenta para el uso presupuestado de modelos caros o escasos (Advisor, Reviewer, modelos especialistas, workers de larga duración) en ejecuciones largas de agentes. Comienza con una negociación conjunta entre usuario y modelo sobre modelos disponibles, roles y cuotas por ventana de tiempo, lleva una cuenta de cada uso, exige un procedimiento previo de piezas de puzle antes de cualquier escalado y permite ajustes en mitad de la ejecución. Usar con «presupuesto», «cuota», «llevar la cuenta», «solo una vez por hora», «usar el revisor con moderación», «Fable/Codex/Sol/Astra/Luna/Advisor solo de forma limitada», «/budgetierung», y siempre que una ejecución de operador, de investigación o de automatización deba combinar varios modelos con costes distintos, incluso si el usuario no menciona la palabra presupuesto pero sí fija límites de uso para los modelos."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [budget, kontingent, modellwahl, eskalation, reviewer, advisor, operator, konto]
language: es
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: ae8346a5144eac699936053f5ca7e12be53014cde4b7826264e2f5fd1e986b0c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
# Presupuestación — negociar, llevar y ajustar cuotas de modelos

## Para qué

Las ejecuciones largas de agentes combinan hoy a menudo varios modelos con precios y disponibilidad muy distintos: un agente principal que piensa y decide, workers baratos de larga duración para la ejecución y unos pocos especialistas caros para revisiones, auditorías o avances. Sin un acuerdo previo se producen dos errores: los modelos caros se gastan en tareas rutinarias, o se dejan de usar por una precaución mal entendida. La cuenta hace que el uso sea **visible y negociable**: lo permitido se fija de antemano, cada uso se registra y el usuario puede reajustar en cualquier momento.

Los modelos, los precios y las cuotas cambian constantemente, porque aparecen modelos nuevos, cambian las suscripciones y los proyectos tienen distinta importancia. Por eso esta skill **no contiene cifras fijas**, sino un procedimiento para establecerlas juntos por cada uso y proyecto.

## Fase 1 — Negociación al inicio

Antes de delegar trabajo, aclarar el presupuesto con el usuario. Lo que ya haya indicado no se vuelve a preguntar; solo se cubren las lagunas y se pide confirmar el resultado una vez, brevemente.

1. **Relevar el inventario:** ¿Qué modelos y accesos son realmente invocables en este host? Comprobar en lugar de suponer: archivos de configuración, listas de modelos de las CLI, tipos de subagentes disponibles. Anotar los nombres de los modelos exactamente como se invocan.
2. **Proponer roles:** Cada modelo recibe un rol:
   - *Pensador/Decisor* (agente principal),
   - *Worker de larga duración* (ejecución, sin límite o con un presupuesto amplio),
   - *Revisor/Auditor* (revisión independiente, idealmente de un proveedor distinto al del autor),
   - *Escalado* (subproblemas de alta complejidad, intentos de avance),
   - *Advisor/Asesor* (corrección de rumbo del agente principal).
3. **Fijar cuotas:** Por recurso, un presupuesto y una ventana de tiempo, por ejemplo «2 solicitudes por hora» o «permanente, sin límite». Aclarar explícitamente:
   - **¿Caducidad o acumulación?** Las unidades no usadas suelen caducar; dejarlo por escrito.
   - **¿Fondos comunes o separados?** ¿Comparten dos modelos una unidad (p. ej., «Fable *o* Astra»)?
   - **¿Cuenta el Advisor?** Las llamadas al Advisor son caras y fáciles de olvidar; si tienen cuota propia, forman parte del fondo común o quedan fuera del presupuesto, debe constar en la cuenta.
   - **Nivel de esfuerzo:** En modelos con niveles de razonamiento, el nivel forma parte del presupuesto (xhigh ≠ low).
4. **Acordar el procedimiento previo** (Fase 3), salvo que el usuario quiera otra cosa.
5. **Abrir la cuenta** (Fase 2) e indicar al usuario la ruta.

Forma breve de la pregunta cuando faltan datos: una pregunta con propuesta en lugar de una lista abierta, por ejemplo «Propuesta: Sonnet como worker de larga duración, revisión con Codex 1×/hora, Advisor solo a petición; ¿te parece bien?».

## Fase 2 — La cuenta

Un archivo Markdown en el proyecto, por ejemplo `_operator/KONTINGENT.md`, o en la ubicación que prevean las convenciones del proyecto. Plantilla: [references/konto-vorlage.md](references/konto-vorlage.md).

La cuenta contiene:
- **Bloque de reglas:** las cuotas negociadas como tabla (Recurso | nombre exacto de la invocación/modelo | presupuesto por ventana | caducidad sí/no).
- **Registro de cambios de las reglas:** cada ajuste hecho por el usuario se añade con fecha, sin sobrescribir lo anterior. Así se puede seguir bajo qué regla estaba un registro anterior.
- **Tabla de registros:** una fila por cada uso de un recurso presupuestado, con número, hora real de inicio, **modelo realmente ejecutado**, finalidad, procedimiento previo recorrido, ruta del resultado y próxima ventana disponible más cercana.

Importante:
- **Registrar el modelo real, no el previsto.** Sin indicación explícita del modelo, las CLI recurren a su modelo por defecto. Por eso hay que fijar siempre el modelo de forma explícita y, en caso de duda, comprobarlo en la configuración o en la respuesta. Si después resulta que se ejecutó otro modelo, hay que **reclasificar** el registro y anotar el error.
- **Hora de inicio tomada de un comprobante** (archivo de marcas de tiempo, log), no estimada.
- **Usos fuera de presupuesto** (desencadenados por el usuario o expresamente exentos) también se registran, con la anotación «sin unidad registrada», para que el panorama quede completo.
- Los workers ilimitados de larga duración no necesitan registro individual. Basta una línea indicando que están en marcha y en qué.

## Fase 3 — Procedimiento previo antes de cualquier escalado

Las unidades caras están reservadas para las excepciones. Antes de registrar una:

1. **Definir la pieza de puzle:** ¿qué falta exactamente? ¿Qué propiedades debería tener la solución, la fuente o el resultado de la comprobación? Por escrito, unas pocas líneas.
2. **Buscar barato:** web, bases de datos especializadas, material del proyecto, con workers de larga duración.
3. **Herramientas de ideas:** por ejemplo `/idea-mining`, después `/skill-finder`, si existe una skill para la tarea.
4. **Solo entonces registrar**, y anotar en la cuenta qué pasos se han recorrido. Si un paso no encaja objetivamente (p. ej., la búsqueda de ideas cuando lo que se necesita es una *comprobación*), anotar el motivo en lugar de ejecutarlo para cumplir el trámite.

Una cuota que caduca **no es motivo** para consumirla. Por otro lado, la falsa austeridad también es un error: si para el siguiente paso hace falta una aprobación independiente (p. ej., un registro de reclamaciones con cambio de proveedor), ese es justamente el caso excepcional para el que existe el presupuesto.

## Fase 4 — Ajustes durante la ejecución

El usuario puede cambiar las reglas en cualquier momento: nuevos modelos, más o menos unidades, un Advisor que a partir de ahora cuente. En ese caso:
- incorporar la nueva regla al bloque de reglas con fecha y conservar la anterior,
- comprobar si los registros previos deben clasificarse de otro modo con la nueva regla, y anotarlo,
- comprobar si existe para el nuevo recurso una tarea abierta adecuada, y entonces usarlo. Si no existe, puede quedar sin usar hasta que surja la necesidad: una cuota es un marco, no un encargo. El usuario puede haber sobreestimado la necesidad, y ocupar recursos por ocupar también tiene un coste,
- confirmar al usuario en una frase lo que ahora está vigente.

Si el propio modelo propone un ajuste (p. ej., porque un recurso queda permanentemente sin usar o aparece un cuello de botella), lo formula como propuesta con justificación. La decisión la toma el usuario.

## Fase 5 — Cierre

Al final de una ejecución o bloque, en el informe al usuario, una línea sobre el consumo: qué unidades se usaron, para qué y con qué resultado, y qué caducó sin usarse. La cuenta permanece en el proyecto; una sesión posterior la lee primero.

## Ejemplo

El usuario dice: «Actúa como operador, usa workers Sonnet, usa Fable o Codex solo una vez por hora y lleva una cuenta.» Más tarde: «Sol puede revisar dos veces por hora, Luna de forma permanente, y el Advisor tiene una cuota extra.»

→ La Fase 1 confirma brevemente los roles; la Fase 2 abre la cuenta con la primera regla. Con el segundo mensaje, la Fase 4 completa el bloque de reglas y detecta que dos auditorías anteriores con «Codex», sin indicación de modelo, en realidad se ejecutaron con el modelo por defecto. Por eso los registros se reclasifican. Para Luna hay justo ahora una tarea de exploración abierta adecuada, así que se utiliza; sin una tarea así, quedaría sin usar.

## Skills relacionadas

- `operator` — modelo de roles Operador/Worker, en el que se integra esta cuenta.
- `model-strategy` — cuándo encaja objetivamente cada modelo; esta skill regula *cuánto* de cada uno.
- `idea-mining`, `skill-finder` — bloques del procedimiento previo.
- `advisor-skill` — asesoramiento selectivo; sus llamadas deben constar en la cuenta.
- `orchestrator` — paquetes de trabajo, perfiles (paralelismo), aceptación.
- `choose-your-orchestrator` — contrato de sesión, en cuyas ranuras de presupuesto se registra esta cuenta.

## Registro de cambios

### 1.0.0 (2026-10-03)
- Versión inicial: negociación, cuenta, procedimiento previo, ajustes durante la ejecución, cierre.
