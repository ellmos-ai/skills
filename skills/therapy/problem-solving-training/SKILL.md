---
name: problemloese-training
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Strukturiertes Problemloesen in 6 Schritten: Problem definieren, Ziele, Brainstorming, Bewertung, Umsetzung und Evaluation.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [problemloesung, entscheidung, strukturiert, sechs-schritte, coping]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/problemloese_training.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Problemloese-Training

> Strukturiertes Problemloesen in 6 Schritten nach D'Zurilla und Goldfried: Probleme systematisch angehen statt gruebelnd im Kreis drehen

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Das Problemloese-Training (Social Problem-Solving, SPS) ist eine evidenzbasierte
Intervention aus der kognitiven Verhaltenstherapie. Es hilft Menschen, Probleme
systematisch und loesungsorientiert anzugehen statt sich in Gruebeln, Vermeidung
oder impulsivem Handeln zu verlieren.

Evidenz: Meta-Analysen zeigen signifikante Effekte bei Depression (d=0.83),
Angststoerungen und Stressbelastung (Malouff et al. 2007, Bell & D'Zurilla 2009).

**Hinweis:** Dies ist Unterstuetzung, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Problemloese-Orientierung

Bevor die eigentlichen Schritte beginnen, ist die innere Haltung entscheidend.

### Foerderliche Haltung
- "Probleme gehoeren zum Leben — sie sind loesbar"
- "Ich kann Schritt fuer Schritt vorgehen"
- "Es gibt selten nur eine richtige Loesung"
- "Nicht-Handeln ist auch eine Entscheidung — meist keine gute"

### Hinderliche Haltung
- "Das hat alles keinen Sinn"
- "Ich kann das sowieso nicht"
- "Es gibt keine Loesung"
- Impulsives Handeln ohne Nachdenken
- Vermeidung und Aufschieben

**Erster Schritt:** Die eigene Problemloese-Haltung reflektieren.

---

## 2. Das 6-Schritte-Modell

### Schritt 1: Problem definieren

**Ziel:** Das Problem klar, konkret und bearbeitbar formulieren.

**Leitfragen:**
- Was genau ist das Problem? (Fakten, nicht Interpretationen)
- Wer ist beteiligt?
- Wann und wo tritt es auf?
- Warum ist es ein Problem fuer mich?

**Arbeitsblatt:**

```
PROBLEMDEFINITION

Situation: [Was passiert konkret?]
Beteiligte: [Wer ist beteiligt?]
Haeufigkeit: [Wie oft? Wann?]
Auswirkung: [Was macht es zum Problem?]

Konkrete Problemformulierung:
[...]
```

**Typische Fehler:**
- Problem zu vage ("Alles ist schlecht")
- Mehrere Probleme vermischen
- Loesung schon in die Formulierung packen

---

### Schritt 2: Ziele festlegen

**Ziel:** Was soll nach der Problemloesung anders sein?

**SMART-Kriterien:**
- Spezifisch: Was genau?
- Messbar: Woran erkenne ich den Erfolg?
- Attraktiv: Warum will ich das?
- Realistisch: Ist es machbar?
- Terminiert: Bis wann?

**Arbeitsblatt:**

```
ZIELSETZUNG

Mein Ziel: [...]
Woran erkenne ich, dass ich es erreicht habe? [...]
Bis wann? [...]
Realistisch (0-10)? [...]
Wichtig fuer mich (0-10)? [...]
```

---

### Schritt 3: Alternativen sammeln (Brainstorming)

**Ziel:** Moeglichst viele Loesungsideen generieren — ohne sofortige Bewertung.

**Brainstorming-Regeln:**
1. Quantitaet vor Qualitaet — je mehr Ideen, desto besser
2. Keine Bewertung waehrend des Sammelns
3. Kreativ und ungewoehnlich denken ist erlaubt
4. Kombinieren und Variieren bestehender Ideen

**Arbeitsblatt:**

```
BRAINSTORMING

Loesungsideen (mindestens 5-8):
1. [...]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
7. [...]
8. [...]
```

**Hilfsfragen:**
- "Was wuerde jemand tun, der dieses Problem nicht hat?"
- "Was habe ich frueher in aehnlichen Situationen gemacht?"
- "Was wuerde ich einem Freund raten?"
- "Was waere die mutigste Loesung?"
- "Was waere die einfachste Loesung?"

---

### Schritt 4: Alternativen bewerten

**Ziel:** Vor- und Nachteile jeder Alternative systematisch abwaegen.

**Bewertungskriterien:**
- Wirksamkeit: Loest es das Problem?
- Machbarkeit: Kann ich es umsetzen?
- Zeitaufwand: Wie lange dauert es?
- Auswirkungen: Auf mich? Auf andere?
- Risiken: Was koennte schiefgehen?

**Arbeitsblatt:**

```
BEWERTUNGSMATRIX

| Alternative | Wirksamkeit (0-10) | Machbarkeit (0-10) | Aufwand (0-10) | Risiko (0-10) | Gesamt |
|-------------|-------------------|--------------------|--------------|--------------||--------|
| 1. [...]    |                   |                    |              |              |        |
| 2. [...]    |                   |                    |              |              |        |
| 3. [...]    |                   |                    |              |              |        |

Bevorzugte Loesung: [...]
Begruendung: [...]
```

---

### Schritt 5: Umsetzen

**Ziel:** Die gewaehlte Loesung konkret planen und durchfuehren.

**Umsetzungsplan:**

```
AKTIONSPLAN

Gewaehlte Loesung: [...]

Konkrete Schritte:
1. [Was?] — [Wann?] — [Wo?]
2. [Was?] — [Wann?] — [Wo?]
3. [Was?] — [Wann?] — [Wo?]

Moegliche Hindernisse: [...]
Plan B: [...]
Unterstuetzung die ich brauche: [...]
Erster Schritt (heute/morgen): [...]
```

---

### Schritt 6: Evaluieren

**Ziel:** Ergebnis pruefen und bei Bedarf nachsteuern.

**Evaluationsfragen:**
- Wurde das Problem geloest? (Ganz / teilweise / gar nicht)
- Bin ich mit dem Ergebnis zufrieden? (0-10)
- Was hat gut funktioniert?
- Was wuerde ich naechstes Mal anders machen?
- Brauche ich einen neuen Versuch mit einer anderen Alternative?

**Arbeitsblatt:**

```
EVALUATION

Ergebnis: [Geloest / Teilweise / Nicht geloest]
Zufriedenheit (0-10): [...]
Was hat funktioniert: [...]
Was nicht: [...]
Naechster Schritt: [Abschluss / Neuer Versuch / Anderer Ansatz]
```

---

## 3. Haeufige Probleme beim Problemloesen

| Problem | Abhilfe |
|---------|---------|
| "Ich weiss nicht, wo anfangen" | Zurueck zu Schritt 1, Problem kleiner formulieren |
| "Keine Loesung ist gut genug" | Perfektionismus hinterfragen, "gut genug" akzeptieren |
| "Ich trau mich nicht" | Kleinsten moeglichen Schritt identifizieren |
| "Es klappt nicht" | Evaluation: Was genau klappt nicht? Neuer Versuch |
| Problem ist zu gross | In Teilprobleme zerlegen, eins nach dem anderen |
| Emotionen blockieren | Erst Emotionsregulation (Atemtechnik, PMR), dann Problemloesen |

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Durch die 6 Schritte fuehren und Arbeitsblatt-Struktur bereitstellen
- Brainstorming-Fragen stellen
- Bei der Bewertung von Alternativen unterstuetzen
- Fortschritt dokumentieren

**Ein KI-Assistent darf NICHT:**
- Loesungen vorgeben oder "die richtige Antwort" suggerieren
- Beziehungs- oder Lebensberatung im therapeutischen Sinne durchfuehren
- Bei schweren psychischen Belastungen alleinige Unterstuetzung sein
- Diagnosen stellen

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: D'Zurilla & Goldfried (1971), Nezu et al. (2013), Malouff et al. (2007) — Keine professionelle Therapie*
