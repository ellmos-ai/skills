---
name: structured-thinking
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: >
  Meta-Skill: Strukturiertes Denken als 3-Phasen-Workflow. Vereint Analyse (think),
  Ideenfindung (brainstorm) und Entscheidungsfindung (decide) in einem durchgaengigen Prozess.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [denken, analyse, kreativitaet, entscheidung, workflow, meta-skill]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  merged_from:
    - "utilities/think (v1.0.0)"
    - "utilities/brainstorm (v1.0.0)"
    - "utilities/decide (v1.0.0)"
  local_changes_since_sync: false
---

# Structured Thinking — Analysieren, Ideenfinden, Entscheiden

> Meta-Workflow fuer strukturiertes Denken: Von der Problemanalyse ueber kreative Loesungen bis zur fundierten Entscheidung

---

## Workflow-Ueberblick

```
Problem/Frage
     |
     v
Phase 1: ANALYSIEREN (think)
  Divide & Conquer, Root Cause, Constraint Relaxation
     |
     v
Phase 2: IDEENFINDEN (brainstorm)
  SCAMPER, Six Hats, Reverse Brainstorming, Rapid Ideation
     |
     v
Phase 3: ENTSCHEIDEN (decide)
  Pro/Con, Weighted Scoring, Scenario Analysis, Eisenhower
     |
     v
Ergebnis + Begruendung
```

---

## Phase 1: Analysieren

Ziel: Problem verstehen, Ursachen identifizieren, Struktur erkennen.

### Ansaetze

| Methode | Wann | Ablauf |
|---------|------|--------|
| **Divide & Conquer** | Komplexes Problem | Problem → Teilprobleme → Einzeln loesen → Kombinieren |
| **Root Cause (5x Warum)** | Symptom sichtbar, Ursache unklar | Symptom → Warum? → Warum? → ... → Ursache → Loesung |
| **Constraint Relaxation** | Problem erscheint unloesbar | Constraints lockern → Loesen → Constraints wieder anziehen |
| **Analogie-Suche** | Neuartiges Problem | Aehnliches bekanntes Problem finden → Loesung adaptieren |

### Analyse-Frameworks

| Framework | Anwendung |
|-----------|-----------|
| **SWOT** | Staerken / Schwaechen / Chancen / Risiken |
| **Pareto** | 80/20 — Was bringt den groessten Hebel? |
| **Fishbone** | Systematische Ursachenanalyse (Ishikawa) |

### Heuristiken bei Unsicherheit

1. Was ist das Worst-Case-Szenario?
2. Ist es reversibel?
3. Was kostet Nicht-Handeln?

### Heuristiken bei Komplexitaet

1. Was ist der einfachste erste Schritt?
2. Was wuerde ein Experte tun?
3. Was waere die 80%-Loesung?

---

## Phase 2: Ideenfinden

Ziel: Moeglichst viele Loesungsansaetze generieren. Quantitaet vor Qualitaet. KEINE Kritik waehrend dieser Phase.

### Methoden

**SCAMPER** — Bestehende Loesungen systematisch verbessern:
- **S**ubstitute: Was ersetzen? | **C**ombine: Was kombinieren? | **A**dapt: Was anpassen?
- **M**odify: Was veraendern? | **P**ut to other use: Wofuer sonst? | **E**liminate: Was weglassen?
- **R**everse: Was umkehren?

**Six Thinking Hats** (de Bono) — 6 Perspektiven nacheinander:
1. Blau: Prozess-Kontrolle ("Was ist die Frage?")
2. Weiss: Fakten ("Was wissen wir?")
3. Rot: Emotion ("Was fuehlt sich richtig an?")
4. Schwarz: Kritik ("Was koennte schiefgehen?")
5. Gelb: Optimismus ("Was sind die Chancen?")
6. Gruen: Kreativitaet ("Welche neuen Ideen gibt es?")

**Reverse Brainstorming** — Problem umkehren:
1. "Wie machen wir es SCHLIMMER?"
2. Schlechte Ideen sammeln
3. Umkehren = Gute Ideen

**Rapid Ideation** — 50+ Ideen in 20 Min:
- Runde 1 (5 Min): Offene Ideation
- Runde 2 (5 Min): Variationen
- Runde 3 (5 Min): Kombinationen
- Runde 4 (5 Min): Extreme Ideen

### Nach der Ideation

1. Clustering: Aehnliche Ideen gruppieren
2. Feasibility/Impact Matrix: Machbarkeit vs. Wirkung bewerten
3. Top 5-10 Auswahl fuer Phase 3

---

## Phase 3: Entscheiden

Ziel: Beste Option auswaehlen mit transparenter Begruendung.

### Framework-Auswahl

| Situation | Framework |
|-----------|-----------|
| 2 Optionen, schnelle Entscheidung | **Pro/Con Matrix** |
| 3+ Optionen, mehrere Kriterien | **Weighted Scoring** |
| Sequenzielle Wenn-Dann-Entscheidung | **Decision Tree** |
| Hohe Unsicherheit | **Scenario Analysis** |
| Aufgaben priorisieren | **Eisenhower Matrix** |

### Weighted Scoring (Kernmethode)

1. Kriterien sammeln (3-7, spezifisch und messbar)
2. Gewichte festlegen (Summe = 100%, wichtigstes >= 25%)
3. Optionen bewerten (1-10 Skala)
4. Scores berechnen (Bewertung x Gewicht)
5. Vergleichen und empfehlen

### Scenario Analysis

```
Best Case (X%):      Ergebnis → Erwartungswert
Realistic Case (X%): Ergebnis → Erwartungswert
Worst Case (X%):     Ergebnis → Erwartungswert
Gesamt-Erwartungswert: [Summe]
```

### Eisenhower Matrix

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

### Quality Checklist vor finaler Empfehlung

- [ ] Alle relevanten Kriterien identifiziert?
- [ ] User-Werte beruecksichtigt?
- [ ] Langfristige Auswirkungen bedacht?
- [ ] Risiken identifiziert und bewertet?
- [ ] Bias-Check durchgefuehrt?
- [ ] Reversibilitaet geprueft?

---

## Kontextsensitive Auswahl

| Situation | Empfohlene Phase(n) |
|-----------|---------------------|
| "Ich habe ein Problem" | Phase 1 (Analyse) → ggf. Phase 2+3 |
| "Ich brauche Ideen" | Phase 2 (Ideenfindung) |
| "Ich muss mich entscheiden" | Phase 3 (Entscheidung) |
| "Ich bin festgefahren" | Phase 2 (Reverse Brainstorming) |
| "Was soll ich priorisieren?" | Phase 3 (Eisenhower) |
| "Komplexes Problem verstehen" | Phase 1 (Divide & Conquer + SWOT) |

---

## Changelog

### 1.0.0 (2026-05-19)
- Erstellt als Meta-Skill aus think, brainstorm und decide

---

*Meta-Skill | Detailreferenz: [think](../think/SKILL.md), [brainstorm](../brainstorm/SKILL.md), [decide](../decide/SKILL.md)*
