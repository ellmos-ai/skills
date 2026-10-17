---
name: grilling
description: "Interroga al usuario sin descanso sobre un plan, una decisión o una idea. Úsalo cuando el usuario quiera poner a prueba su razonamiento o emplee cualquier frase desencadenante de \"grill\", como \"interrógame\", \"interrógame sobre este plan\" o \"destroza mi plan en modo grill\", incluidas las alemanas como \"grill mich\", \"grill mich zu diesem Plan\" o \"zerpflück meinen Plan im Grill-Modus\". Punto de entrada para el comando /grill-me; también puede invocarse directamente."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: es
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
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

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich"). The `category` and `language` fields and this
comment were added; all are local convention (recommended, not one of the
nine house fields), not upstream content, and `language: en` reflects that
the vendored body is unmodified English. The body (the design tree / frontier
/ rounds method) is unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458 alongside skills/third-
party/grill-me/ (the thin, explicit-only entry point that calls this skill).
-->
