---
name: grill-me
description: "Ein gnadenloses Interview zur Schärfung eines Plans oder Entwurfs. Verwenden, wenn der Nutzer sagt \"nimm mich in die Mangel\", \"grill mich\", \"grill mich zu diesem Plan\" oder ausdrücklich /grill-me aufruft. Wird NICHT ausgelöst bei allgemeinen Formulierungen wie \"prüf das\", \"zeig Schwachstellen auf\", \"Stresstest\", \"Advocatus Diaboli\" oder \"kritisiere\" -- zur Überprüfung eines bereits geschriebenen Artefakts (Code, PR, Paper) stattdessen code-review, 3agenten-review, 7phasen-review oder caveman-review verwenden; grill-me befragt einen noch offenen Plan oder eine Idee, bevor sie gebaut wird."
disable-model-invocation: true
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: de
translated_from_sha256: 6074974f754dbd47e47fe7abbf10df62f7177cddba8d2fe20e6c581d9935d2b1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="grill-me banner">

Rufe das Skill-Werkzeug mit "grilling" auf.

<!--
Vendored from mattpocock/skills (skills/productivity/grill-me/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich") and an explicit non-trigger/abgrenzung note
against this library's existing artifact-review skills (code-review,
3agenten-review, 7phasen-review, caveman-review). The `category` and
`language` fields and this comment were added; all are local convention
(recommended, not one of the nine house fields), not upstream content, and
`language: en` reflects that the vendored body is unmodified English.
The body (the single instruction line) and `disable-model-invocation: true`
are unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458: the user asked whether a
"grill me" skill exists; none did locally, and this upstream implementation
(design-tree / frontier / rounds interrogation, see skills/third-party/grilling/)
is the well-known, MIT-licensed original that the term "grill me" refers to
in the current Claude Code skill ecosystem -- adopted rather than
independently re-implemented.
-->
