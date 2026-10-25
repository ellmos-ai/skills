---
name: grilling
description: "Interroga al usuario sin descanso sobre un plan, una decisión o una idea. Activa esta skill cuando quiera poner a prueba su razonamiento, diga «grill me» o «grill-me» (el antiguo comando /grill-me fue sustituido por /grilling), o use cualquier otra expresión desencadenante con «grill», incluidas las expresiones en español «interrógame», «interrógame sobre este plan» y «destroza mi plan en modo grill», además de las alemanas «grill mich», «grill mich zu diesem Plan» y «zerpflück meinen Plan im Grill-Modus». Úsala también cuando termine una sesión de planificación y el usuario pregunte si queda algo abierto."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: es
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

Entrevista al usuario sin descanso hasta llegar a una comprensión compartida. Representa esto como un **árbol de diseño**: cada decisión se ramifica en las decisiones que dependen de ella.

Recorre el árbol por **rondas**. La **frontera** está formada por todas las decisiones cuyos prerrequisitos ya están resueltos: las preguntas que puedes formular _ahora_ sin suponer respuestas que aún no has escuchado. Plantea toda la frontera en una sola ronda: numera cada pregunta y ofrece tu respuesta recomendada. Después espera las respuestas del usuario antes de la siguiente ronda.

Formatea una ronda de esta manera:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Cada ronda, las respuestas del usuario remodelan el árbol: las decisiones resueltas empujan la frontera hacia afuera y desbloquean las preguntas que dependían de ellas. Recalcula la frontera y plantea la siguiente ronda. Una pregunta cuya respuesta depende de otra pregunta todavía abierta en esta ronda pertenece a una ronda _posterior_, no a esta.

Encontrar _hechos_ es tu tarea, nunca la del usuario. Cuando una pregunta de la frontera necesite un hecho del entorno (sistema de archivos, herramientas, etc.), encarga a un subagente que lo localice; no le pidas al usuario nada que puedas consultar tú mismo. No te bloquees por ello: una exploración en curso es un prerrequisito no resuelto, así que solo las preguntas posteriores a ella esperan el informe del subagente; plantea el resto de la frontera ahora. Las _decisiones_ son del usuario: presentáselas y espera.

La sesión termina cuando la frontera está vacía: cada rama del árbol de diseño ha sido visitada y no queda nada asumido en silencio. No actúes hasta que el usuario confirme que se ha alcanzado una comprensión compartida.

## Adiciones locales

Estas reglas amplían el método original, pero no lo modifican.

1. **Parte de lo que ya está escrito.** Antes de la primera ronda, lee el plan y el lugar donde el proyecto registra sus decisiones. Reúne todos los puntos que sigan abiertos, propuestos o sin confirmar. No vuelvas a preguntar lo que ya se decidió; cita el registro.
2. **Anota cada respuesta antes de la siguiente ronda.** Registra cada respuesta en el registro de decisiones del proyecto como decidida, con fecha y fuente. Una respuesta que solo esté en el chat se pierde al reiniciarse el contexto.
3. **Haz una pausa, no empieces de nuevo, si hay una interrupción.** Si el usuario pide otra cosa primero, hazla y luego retoma los puntos abiertos que queden. Lo que ya se resolvió sigue resuelto.
4. **Justifica cada recomendación con un motivo.** Da la respuesta que recomiendas y el único hecho o regla en que se apoya. Una recomendación no es una decisión hasta que el usuario la confirme.
5. **Muestra los hechos que comprobaste.** Si una pregunta depende de un dato que consultaste en el entorno, explica qué encontraste y dónde, para que el usuario decida con base en la evidencia.
6. **Pregunta en el idioma del usuario.** Formula las preguntas y recomendaciones en su idioma; los identificadores se mantienen sin cambios.
7. **Cierra con un registro.** Cuando la frontera esté vacía, enumera lo decidido y lo que se dejó abierto deliberadamente, y pide confirmar que se alcanzó una comprensión compartida.

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" /
  "grill-me" phrases, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the phrase triggers moved into
this description. The native /grill-me command no longer exists; /grilling
replaces it. The description only adds semantic matching and registers no
alias command. Rules 1-7 come from a planning session of the same day.
-->
