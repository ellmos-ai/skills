---
name: grilling
description: "Stelle dem Nutzer zu einem Plan, einer Entscheidung oder Idee unnachgiebig Fragen. Verwenden, wenn der Nutzer seine Überlegungen auf die Probe stellen möchte oder einen beliebigen „grill“-Auslösesatz verwendet, einschließlich deutscher Formulierungen wie \"grill mich\", \"grill mich zu diesem Plan\" oder \"zerpflück meinen Plan im Grill-Modus\". Einstiegspunkt für den Befehl /grill-me; kann auch direkt aufgerufen werden."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: de
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

Befrage den Nutzer unnachgiebig, bis ihr ein gemeinsames Verständnis erreicht. Behandle dies als **Entscheidungsbaum**: Jede Entscheidung verzweigt sich in die Entscheidungen, die an ihr hängen.

Arbeite den Baum in **Runden** ab. Die **Front** ist jede Entscheidung, deren Voraussetzungen bereits geklärt sind: die Fragen, die du _jetzt_ stellen kannst, ohne Antworten zu erraten, die du noch nicht gehört hast. Stelle die gesamte Front in einer Runde: Nummeriere jede Frage und nenne deine empfohlene Antwort. Warte dann auf die Antworten des Nutzers, bevor die nächste Runde beginnt.

Formatiere eine Runde so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Jede Antwort des Nutzers verändert den Baum: Geklärte Entscheidungen schieben die Front nach außen und entsperren Fragen, die von ihnen abhingen. Berechne die Front neu und stelle die nächste Runde. Eine Frage, deren Antwort von einer anderen, in dieser Runde noch offenen Frage abhängt, gehört in eine _spätere_ Runde, nicht in diese.

Das Ermitteln von _Fakten_ ist deine Aufgabe, nie die des Nutzers. Wenn eine Frage der Front einen Fakt aus der Umgebung benötigt (Dateisystem, Werkzeuge usw.), beauftrage einen Sub-Agenten, ihn zu finden; frage den Nutzer nicht nach etwas, das du selbst nachschlagen kannst. Blockiere nicht deswegen: Eine laufende Erkundung ist eine ungeklärte Voraussetzung, daher warten nur die nachgelagerten Fragen auf den Bericht des Sub-Agenten; stelle den Rest der Front jetzt. Die _Entscheidungen_ liegen beim Nutzer: Lege sie ihm vor und warte auf seine Antwort.

Die Sitzung ist beendet, wenn die Front leer ist: Jeder Zweig des Entscheidungsbaums ist besucht, und nichts wird stillschweigend vorausgesetzt. Handle nicht danach, bevor der Nutzer bestätigt, dass ihr ein gemeinsames Verständnis erreicht habt.

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
