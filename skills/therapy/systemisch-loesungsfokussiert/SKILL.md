---
name: systemisch-loesungsfokussiert
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: >
  Systemische und loesungsfokussierte Methoden: Wunderfrage, Skalierung, Ausnahmen-Exploration,
  zirkulaere Fragen, hypothetische Fragen, Verschlimmerungsfragen, Coping-Fragen.
  Zusammengefuehrt aus solution-focused-therapy und systemic-questioning.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [sfbt, systemisch, loesungsfokussiert, wunderfrage, skalierung, zirkulaer, fragetechniken, de-shazer]
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
    - "therapy/solution-focused-therapy (v1.0.0, BACH skills/therapie/loesungsfokussierte_therapie.md)"
    - "therapy/systemic-questioning (v1.0.0, BACH skills/therapie/systemische_fragetechniken.md)"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-05-19"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Systemische & Loesungsfokussierte Methoden

> Wunderfrage, Skalierung, Ausnahmen, zirkulaere Fragen, hypothetische Fragen — ein integrierter Skill

Siehe: [ETHICS.md](../ETHICS.md)

---

## Grundlage

### Loesungsfokussierte Kurztherapie (SFBT)

Entwickelt von Steve de Shazer und Insoo Kim Berg am Brief Family Therapy Center (Milwaukee).
Kernidee: Statt Probleme zu analysieren, direkt an Loesungen arbeiten.
"Problem talk creates problems, solution talk creates solutions" (de Shazer).

**Die drei Grundregeln:**
1. **"If it ain't broke, don't fix it"** — Was funktioniert, nicht veraendern
2. **"If it works, do more of it"** — Was klappt, verstaerken
3. **"If it doesn't work, do something different"** — Was nicht hilft, aendern

### Systemische Perspektive

Probleme entstehen nicht in Personen, sondern in Beziehungen und Mustern zwischen Personen.
Fragen zielen darauf ab, Perspektiven zu erweitern, Muster sichtbar zu machen und neue Moeglichkeiten zu eroeffnen.

**Hinweis:** Dies ist Psychoedukation, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Die Wunderfrage

### Grundform

```
"Stell dir vor, heute Nacht passiert ein Wunder, waehrend du schlaefst.
Das Problem, das dich beschaeftigt, ist geloest.
Du weisst es aber nicht, weil du geschlafen hast.

Woran wuerdest du morgen frueh als Erstes merken, dass das Wunder passiert ist?"
```

### Vertiefende Nachfragen

**Sinnesebene:**
- "Was genau wuerdest du morgen frueh anders machen?"
- "Wie wuerdest du aufstehen? Was wuerdest du als Erstes tun?"
- "Was wuerdest du fuehlen, wenn du die Augen oeffnest?"

**Beziehungsebene:**
- "Woran wuerde dein Partner / deine Partnerin das Wunder bemerken?"
- "Was wuerde er/sie anders an dir sehen?"
- "Wer in deinem Umfeld wuerde es als Erstes bemerken?"

**Bruchteile des Wunders:**
- "Welcher Teil dieses Wunders passiert vielleicht schon ein kleines bisschen?"
- "Auf einer Skala von 0 bis 10 — wie weit bist du schon in Richtung Wunder?"

### Verkuerzte Varianten

- "Wenn das Problem morgen weg waere — was waere anders?"
- "Wie saehe dein idealer Alltag aus?"
- "Wenn alles so waere, wie du es dir wuenschst — was wuerdest du tun?"

---

## 2. Skalierungstechniken

### Grundstruktur

"Auf einer Skala von 0 bis 10, wobei 0 [Pol A] und 10 [Pol B] ist — wo stehst du gerade?"

### Varianten

| Typ | Beispielfrage |
|-----|---------------|
| **Zustandsskalierung** | "Wie belastet fuehlst du dich gerade?" |
| **Bewaeltigungsskalierung** | "Wie gut schaffst du es, trotz des Problems deinen Alltag zu bewaeltigen?" |
| **Zuversichtsskalierung** | "Wie zuversichtlich bist du, dass du Fortschritte machen kannst?" |
| **Fortschrittsskalierung** | "Wo standest du vor einer Woche / einem Monat?" |
| **Beziehungsskalierung** | "Wo auf der Skala wuerde dein Partner eure Beziehung einschaetzen?" |

### Der "Ein-Punkt-hoeher"-Trick

Immer nur nach dem naechsten Punkt fragen — nie nach dem Endziel.

```
"Was waere bei einer 6 anders als bei der jetzigen 5?"
"Was koenntest du MORGEN tun, das in Richtung 6 geht?"
```

### Follow-up-Fragen (essentiell!)

- "Was hat dazu gefuehrt, dass du nicht bei 0 bist?" (Ressourcenaktivierung)
- "Was muesste passieren, damit du einen Punkt hoeher kommst?" (Kleinschrittige Loesungsorientierung)
- "Woran wuerdest du merken, dass du bei [Zielwert] bist?" (Konkretisierung)

---

## 3. Ausnahmen-Exploration

### Prinzip

Ausnahmen sind Momente, in denen das Problem nicht oder weniger auftritt.
Sie enthalten bereits funktionierende Loesungsansaetze.

### Systematische Suche

**Phase 1 — Finden:**
- "Wann war es in letzter Zeit einmal etwas besser — auch nur minimal?"
- "Gibt es Tage, an denen das Problem weniger stark auftritt?"

**Phase 2 — Detailliert beschreiben:**
- "Beschreibe diesen Moment so genau wie moeglich"
- "Was war an diesem Tag anders?"

**Phase 3 — Eigenen Beitrag erkennen:**
- "Was hast DU dazu beigetragen, dass es besser war?"
- "Welche Entscheidung hast du getroffen?"

**Phase 4 — Verstaerken:**
- "Wie koenntest du das bewusst wiederholen?"
- "Was waere ein erster kleiner Schritt in diese Richtung?"

### Typen von Ausnahmen

| Typ | Beschreibung | Nachfrage |
|-----|-------------|-----------|
| Absichtlich | Klient hat bewusst etwas anders gemacht | "Mach mehr davon!" |
| Zufaellig | Etwas war anders, ohne bewusstes Zutun | "Was war anders an den Umstaenden?" |
| Extern | Andere haben etwas getan | "Was koenntest du tun, um das wahrscheinlicher zu machen?" |

---

## 4. Zirkulaere Fragen

### Prinzip

Perspektivwechsel anregen — die Person wird eingeladen, sich in die Position anderer zu versetzen und Beziehungsmuster zu erkennen.

### Grundstruktur

"Was glaubst du, wie [Person X] das sieht/empfindet/beurteilt?"

### Varianten

**Beziehungsfragen:**
- "Was glaubst du, was dein Partner denkt, wenn du dich zurueckziehst?"
- "Wie wuerde deine beste Freundin eure Beziehung beschreiben?"
- "Wenn ich deinen Bruder fragen wuerde, was das groesste Problem in der Familie ist — was wuerde er sagen?"

**Unterschiedsfragen:**
- "Wer in der Familie leidet am meisten unter der Situation?"
- "Wer bemerkt die Veraenderung zuerst?"

**Uebereinstimmungsfragen:**
- "Wuerde dein Partner dem zustimmen?"
- "Wer in deinem Umfeld sieht das aehnlich wie du?"

**Klassifikationsfragen:**
- "Wenn du deine Familienmitglieder danach ordnen wuerdest, wer am besten mit Konflikten umgeht — wie saehe die Reihenfolge aus?"

---

## 5. Hypothetische Fragen

Neue Denkraeume eroeffnen, starre Ueberzeugungen aufloeckern, Handlungsoptionen durchspielen.

- "Angenommen, du wuerdest es einfach mal ausprobieren — was koennte im besten Fall passieren?"
- "Was wuerde passieren, wenn du das Gegenteil von dem taetst, was du normalerweise tust?"
- "Wenn du einen Ratschlag an jemanden geben wuerdest, der in der gleichen Situation ist — was wuerdest du sagen?"
- "Wenn Angst keine Rolle spielen wuerde — was wuerdest du tun?"
- "Wenn du in 5 Jahren auf heute zurueckblickst — was wuerdest du dir raten?"

---

## 6. Verschlimmerungsfragen (Paradoxe Intervention)

Kontrollueberzeugung staerken: Wer beschreiben kann, wie er das Problem verschlimmern koennte, hat Einfluss — und kann es auch verbessern.

- "Was koenntest du tun, damit es garantiert schlimmer wird?"
- "Wie koenntest du dafuer sorgen, dass der Streit eskaliert?"
- "Was muesste passieren, damit alles komplett schiefgeht?"

**Wichtig:** NICHT geeignet bei akuter Krise, Suizidalitaet oder schwerer Depression.

---

## 7. Coping-Fragen & Ressourcen-Kommentare

- "Wie schaffst du es trotzdem, jeden Tag aufzustehen?"
- "Was haelt dich aufrecht?"
- "Es beeindruckt mich, dass du trotz der Schwierigkeiten hier bist."

---

## Kontextsensitive Auswahl

| Situation | Empfohlene Technik | Begruendung |
|---|---|---|
| Person steckt im Problem fest | Wunderfrage | Loest aus der Problemtrance |
| Fortschritt nicht sichtbar | Skalierungsfragen | Macht kleine Schritte messbar |
| Beziehungskonflikte | Zirkulaere Fragen | Ermoeglicht Perspektivwechsel |
| "Es ist IMMER so" | Ausnahme-Fragen | Durchbricht Generalisierung |
| Angst vor Veraenderung | Hypothetische Fragen | Risikofreies Probedenken |
| Hilflosigkeit / Kontrollverlust | Verschlimmerungsfragen | Zeigt eigenen Einfluss |
| Unklare Ziele | Wunderfrage + Skalierung | Klaert Richtung und Ausgangspunkt |

---

## Kombinationsmuster

### Skalierung + Ausnahme + Kleiner Schritt

1. "Auf einer Skala von 0-10, wo stehst du gerade?" → z.B. "4"
2. "Was hat dazu gefuehrt, dass du nicht bei 0 bist?" (Ressourcen!)
3. "Gab es Momente, wo du bei 5 oder hoeher warst?" (Ausnahmen!)
4. "Was war da anders?" (Muster erkennen!)
5. "Was waere der kleinste Schritt, um von 4 auf 5 zu kommen?" (Handlung!)

### Wunderfrage + Zirkulaer + Skalierung

1. Wunderfrage stellen (Zielbild erzeugen)
2. "Wer wuerde es zuerst merken?" (Zirkulaer — Beziehungskontext)
3. "Wie weit bist du schon auf dem Weg zum Wunder?" (Skalierung — Fortschritt)

### Zirkulaer + Hypothetisch

1. "Was glaubst du, wie dein Chef die Situation sieht?"
2. "Angenommen, er wuerde genau das sagen — was koenntest du dann tun?"

---

## Reflexionsfragen zur Selbstanwendung

- "Was funktioniert in meinem Leben gut — und wie mache ich das?"
- "Was ist eine kleine Ausnahme, auf die ich aufbauen koennte?"
- "Wenn das Problem morgen weg waere — was wuerde ich als Erstes tun?"
- "Was habe ich frueher schon einmal geschafft, obwohl es schwer war?"

---

## Dos and Don'ts

### Dos
- **Offen fragen** — keine Suggestivfragen
- **Neugierig bleiben** — die Antwort ist wertvoller als die Frage
- **Pausen lassen** — gute Fragen brauchen Zeit
- **An Antworten anknuepfen** — Follow-up ist wichtiger als die naechste Technik
- **Wertschaetzend formulieren** — "Was ist dir gelungen?" statt "Was hast du falsch gemacht?"

### Don'ts
- **Nicht verhoerartig fragen** — max. 2-3 Fragen am Stueck, dann reflektieren
- **Nicht bei akuter Krise** — erst stabilisieren, dann explorieren
- **Nicht als Manipulation** — Fragen muessen authentisch neugierig sein
- **Verschlimmerungsfragen nicht bei Suizidalitaet** — niemals

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- SFBT- und systemische Konzepte erklaeren und einordnen
- Wunderfrage, Ausnahmen-Exploration und Skalierung anleiten
- Zirkulaere und hypothetische Fragen stellen
- Reflexionsfragen stellen und auf Ressourcen hinweisen

**Ein KI-Assistent darf NICHT:**
- Therapie durchfuehren oder ersetzen
- Persistierende Probleme verharmlosen ("Denk einfach positiv")
- Akute Krisen mit Loesungsorientierung uebergehen
- Beziehungsberatung geben, die professionelle Therapie ersetzt
- Verschlimmerungsfragen bei fragilen Zustaenden einsetzen

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Quellenangaben

- de Shazer, S. (1985). *Keys to Solution in Brief Therapy.* Norton.
- de Shazer, S. (1988). *Clues: Investigating Solutions in Brief Therapy.* Norton.
- Berg, I. K. & Miller, S. D. (1992). *Working with the Problem Drinker.* Norton.
- Berg, I. K. & Dolan, Y. (2001). *Tales of Solutions.* Norton.
- Selvini Palazzoli, M. et al. (1981). *Hypothetisieren — Zirkularitaet — Neutralitaet.*
- Schlippe, A. von & Schweitzer, J. (2012). *Lehrbuch der systemischen Therapie und Beratung.*
- Gingerich, W. J. & Peterson, L. T. (2013). Effectiveness of Solution-Focused Brief Therapy. *Research on Social Work Practice*, 23(3), 266-283.
- Kim, J. S. et al. (2019). Solution-Focused Brief Therapy: A Meta-Analysis. *Journal of Marital and Family Therapy*, 45(2), 271-286.

---

## Changelog

### 1.0.0 (2026-05-19)
- Zusammengefuehrt aus `solution-focused-therapy` (v1.0.0) und `systemic-questioning` (v1.0.0)
- Alle einzigartigen Inhalte beider Quellen integriert

---

*Merged aus BACH v3.8.0 Exports | Standalone-Version*
*Keine professionelle Therapie — Psychoedukation und Reflexion*
