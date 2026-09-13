---
name: solution-focused-therapy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Grundlagen der lösungsfokussierten Kurztherapie nach Steve de Shazer und Insoo Kim Berg: Wunderfrage, Ausnahmen-Exploration, Skalierung, Ressourcenaktivierung.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [sfbt, lösungsfokussiert, wunderfrage, skalierung, kurztherapie, ressourcen]
language: de
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/loesungsfokussierte_therapie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="solution-focused-therapy banner">

# Lösungsfokussierte Therapie

> Grundlagen der lösungsfokussierten Kurztherapie nach Steve de Shazer und Insoo Kim Berg: Wunderfrage, Ausnahmen-Exploration, Skalierung, Ressourcenaktivierung

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Die lösungsfokussierte Kurztherapie (Solution-Focused Brief Therapy, SFBT) wurde
von Steve de Shazer und Insoo Kim Berg am Brief Family Therapy Center in Milwaukee
entwickelt. Sie gehört zu den am besten erforschten Kurztherapieverfahren.

Kernidee: Statt Probleme zu analysieren, wird direkt an Lösungen gearbeitet.
"Problem talk creates problems, solution talk creates solutions" (de Shazer).

Evidenz: Meta-Analysen belegen Wirksamkeit bei Depression, Angst, Verhaltensproblemen,
Substanzmissbrauch und Paarkonflikten (Gingerich & Peterson 2013, Kim et al. 2019).

**Hinweis:** Dies ist Psychoedukation, kein Ersatz für professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Grundhaltungen der SFBT

### Die drei Grundregeln (de Shazer)

1. **"If it ain't broke, don't fix it"** — Was funktioniert, nicht verändern
2. **"If it works, do more of it"** — Was klappt, verstärken
3. **"If it doesn't work, do something different"** — Was nicht hilft, ändern

### Menschenbild
- Jeder Mensch hat Ressourcen und Kompetenzen
- Der Klient ist Experte für sein eigenes Leben
- Kleine Veränderungen lösen größere aus (Schmetterlingseffekt)
- Die Lösung muss nichts mit dem Problem zu tun haben

---

## 2. Die Wunderfrage — Vertiefte Anwendung

### Grundform

```
"Stell dir vor, heute Nacht passiert ein Wunder, während du schläfst.
Das Problem, das dich beschäftigt, ist gelöst.
Du weißt es aber nicht, weil du geschlafen hast.

Woran würdest du morgen früh als Erstes merken, dass das Wunder passiert ist?"
```

### Vertiefende Nachfragen

**Sinnesebene konkretisieren:**
- "Was genau würdest du morgen früh anders machen?"
- "Wie würdest du aufstehen? Was würdest du als Erstes tun?"
- "Was würdest du fühlen, wenn du die Augen öffnest?"

**Beziehungsebene:**
- "Woran würde dein Partner / deine Partnerin das Wunder bemerken?"
- "Was würde er/sie anders an dir sehen?"
- "Wer in deinem Umfeld würde es als Erstes bemerken?"

**Bruchteile des Wunders finden:**
- "Welcher Teil dieses Wunders passiert vielleicht schon ein kleines bisschen?"
- "Auf einer Skala von 0 bis 10 — wie weit bist du schon in Richtung Wunder?"

---

## 3. Ausnahmen-Exploration

### Prinzip
Ausnahmen sind Momente, in denen das Problem nicht oder weniger auftritt.
Sie enthalten bereits funktionierende Lösungsansätze.

### Systematische Ausnahmen-Suche

**Phase 1: Ausnahmen finden**
- "Wann war es in letzter Zeit einmal etwas besser — auch nur minimal?"
- "Gibt es Tage, an denen das Problem weniger stark auftritt?"

**Phase 2: Ausnahmen detailliert beschreiben**
- "Beschreibe diesen Moment so genau wie möglich"
- "Was war an diesem Tag anders?"

**Phase 3: Eigenen Beitrag erkennen**
- "Was hast DU dazu beigetragen, dass es besser war?"
- "Welche Entscheidung hast du getroffen?"

**Phase 4: Ausnahmen verstärken**
- "Wie könntest du das bewusst wiederholen?"
- "Was wäre ein erster kleiner Schritt in diese Richtung?"

### Typen von Ausnahmen

| Typ | Beschreibung | Nachfrage |
|-----|-------------|-----------|
| Absichtliche Ausnahme | Klient hat bewusst etwas anders gemacht | "Mach mehr davon!" |
| Zufällige Ausnahme | Etwas war anders, ohne bewusstes Zutun | "Was war anders an den Umständen?" |
| Externe Ausnahme | Andere haben etwas getan | "Was könntest du tun, um das wahrscheinlicher zu machen?" |

---

## 4. Skalierungstechniken

### Basis-Skalierung
"Auf einer Skala von 0 bis 10, wobei 0 das Schlimmste und 10 das Bestmögliche ist..."

### Erweiterte Skalierungsformen

**Bewältigungsskalierung:**
- "Wie gut schaffst du es gerade, trotz des Problems deinen Alltag zu bewältigen?"

**Zuversichtsskalierung:**
- "Wie zuversichtlich bist du, dass du Fortschritte machen kannst?"

**Fortschrittsskalierung:**
- "Wo standest du vor einer Woche / einem Monat?"
- "Was hat zum Anstieg beigetragen?"

### Der "Ein-Punkt-höher"-Trick
Immer nur nach dem nächsten Punkt fragen — nie nach dem Endziel.

```
"Was wäre bei einer 6 anders als bei der jetzigen 5?"
"Was könntest du MORGEN tun, das in Richtung 6 geht?"
```

---

## 5. Weitere SFBT-Techniken

### Coping-Fragen
- "Wie schaffst du es trotzdem, jeden Tag aufzustehen?"
- "Was hält dich aufrecht?"

### Beziehungsfragen
- "Wenn ich deine Partnerin fragen würde, was würde sie sagen?"
- "Wer in deinem Umfeld würde die Veränderung als Erstes bemerken?"

### Komplimente / Ressourcen-Kommentare
- "Es beeindruckt mich, dass du trotz der Schwierigkeiten hier bist."

---

## 6. Reflexionsfragen zur Selbstanwendung

- "Was funktioniert in meinem Leben gut — und wie mache ich das?"
- "Was ist eine kleine Ausnahme, auf die ich aufbauen könnte?"
- "Wenn das Problem morgen weg wäre — was würde ich als Erstes tun?"
- "Was habe ich früher schon einmal geschafft, obwohl es schwer war?"

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- SFBT-Konzepte erklären und einordnen
- Wunderfrage, Ausnahmen-Exploration und Skalierung anleiten
- Reflexionsfragen stellen
- Auf Ressourcen und Stärken hinweisen

**Ein KI-Assistent darf NICHT:**
- Lösungsfokussierte Therapie durchführen
- Persistierende Probleme verharmlosen ("Denk einfach positiv")
- Akute Krisen mit Lösungsorientierung übergehen
- Versprechen, dass SFBT-Techniken Probleme lösen

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Quellenangaben

- de Shazer, S. (1988). *Clues: Investigating Solutions in Brief Therapy.* Norton.
- Berg, I. K. & Miller, S. D. (1992). *Working with the Problem Drinker.* Norton.
- Gingerich, W. J. & Peterson, L. T. (2013). Effectiveness of Solution-Focused Brief Therapy. *Research on Social Work Practice*, 23(3), 266-283.
- Kim, J. S. et al. (2019). Solution-Focused Brief Therapy: A Meta-Analysis. *Journal of Marital and Family Therapy*, 45(2), 271-286.

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: de Shazer (1988), Berg & Miller (1992), Gingerich & Peterson (2013), Kim et al. (2019) — Keine professionelle Therapie*
