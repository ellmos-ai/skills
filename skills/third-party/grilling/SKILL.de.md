---
name: grilling
description: "Stelle dem Nutzer zu einem Plan, einer Entscheidung oder einer Idee unnachgiebig Fragen. Verwende diesen Skill, wenn der Nutzer seine Überlegungen auf die Probe stellen möchte, „grill me“ oder „grill-me“ sagt (der frühere Befehl /grill-me wurde durch /grilling ersetzt) oder einen anderen Auslösesatz mit „grill“ verwendet, darunter „grill mich“, „grill mich zu diesem Plan“ und „zerpflück meinen Plan im Grill-Modus“. Verwende ihn auch, wenn eine Planungssitzung endet und der Nutzer fragt, ob noch etwas offen ist."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: de
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
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

## Lokale Ergänzungen

Diese Regeln erweitern die ursprüngliche Methode, ändern sie aber nicht.

1. **Beginne mit dem, was bereits festgehalten ist.** Lies vor der ersten Runde den Plan und die Stelle, an der das Projekt Entscheidungen dokumentiert. Sammle alle Punkte, die noch offen, vorgeschlagen oder unbestätigt sind. Frage bereits entschiedene Punkte nicht erneut ab; verweise stattdessen darauf.
2. **Halte jede Antwort vor der nächsten Runde fest.** Trage jede Antwort im Entscheidungsprotokoll des Projekts als entschieden ein, mit Datum und Quelle. Eine Antwort, die nur im Chat steht, geht beim nächsten Zurücksetzen des Kontexts verloren.
3. **Pausiere bei Unterbrechungen, statt neu zu beginnen.** Wenn der Nutzer zuerst um etwas anderes bittet, erledige es und setze danach mit den übrigen offenen Punkten fort. Bereits geklärte Fragen bleiben geklärt.
4. **Begründe jede Empfehlung mit einem Grund.** Nenne die empfohlene Antwort und die einzelne Tatsache oder Regel, auf der sie beruht. Eine Empfehlung ist erst dann eine Entscheidung, wenn der Nutzer sie bestätigt.
5. **Zeige die ermittelten Fakten.** Wenn eine Frage auf einer nachgeschlagenen Tatsache beruht, nenne den Befund und seine Fundstelle, damit der Nutzer anhand der Belege entscheidet.
6. **Frage in der Sprache des Nutzers.** Formuliere Fragen und Empfehlungen in seiner Sprache; Bezeichner bleiben unverändert.
7. **Schließe mit einem Entscheidungsprotokoll.** Wenn die Frontier leer ist, liste auf, was entschieden wurde und was bewusst offen blieb, und bitte um Bestätigung des gemeinsamen Verständnisses.

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
