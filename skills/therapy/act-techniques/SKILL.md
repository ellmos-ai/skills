---
name: act-techniken
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Acceptance & Commitment Therapy (ACT) nach Steven Hayes: Hexaflex-Modell mit den sechs Kernprozessen psychischer Flexibilitaet.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [act, akzeptanz, defusion, werte, psychische-flexibilitaet, hayes]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/act_techniken.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# ACT-Techniken -- Acceptance & Commitment Therapy

## Grundlage

Die Acceptance & Commitment Therapy (ACT, gesprochen als Wort "act") wurde von **Steven C. Hayes** entwickelt und gehoert zur dritten Welle der Verhaltenstherapie. ACT zielt nicht auf Symptomreduktion, sondern auf **psychische Flexibilitaet** -- die Faehigkeit, im gegenwaertigen Moment offen und bewusst zu handeln, geleitet von persoenlichen Werten.

Kernaussage: **Nicht der Schmerz ist das Problem, sondern der Kampf gegen den Schmerz.**

---

## Das Hexaflex-Modell

Das Hexaflex ist das zentrale Modell der ACT. Sechs Kernprozesse bilden zusammen psychische Flexibilitaet. Jeder Prozess ist das Gegenstueck zu einem pathologischen Prozess (psychische Inflexibilitaet).

```
                    Gegenwaertigkeit
                         /    \
                        /      \
              Akzeptanz          Selbst-als-Kontext
                |    \          /    |
                |  PSYCHISCHE  |
                | FLEXIBILITAET|
                |  /          \     |
              Defusion          Werte
                        \      /
                         \    /
                    Engagiertes Handeln
```

### Flexibilitaet vs. Inflexibilitaet

| Kernprozess (flexibel) | Gegenpol (inflexibel) |
|---|---|
| Akzeptanz | Erlebnisvermeidung |
| Kognitive Defusion | Kognitive Fusion |
| Gegenwaertigkeit | Vergangenheits-/Zukunftsfokus |
| Selbst-als-Kontext | Konzeptualisiertes Selbst |
| Werte | Mangelnde Werteklaerung |
| Engagiertes Handeln | Untaetigkeit/Impulsivitaet |

---

## Die sechs Kernprozesse

### 1. Akzeptanz

**Definition:** Bereitschaft, innere Erlebnisse (Gefuehle, Gedanken, Koerperempfindungen) zuzulassen, ohne sie zu veraendern, zu vermeiden oder zu kontrollieren.

**Wichtig:** Akzeptanz ist NICHT Resignation. Es ist eine aktive, bewusste Entscheidung, dem Erleben Raum zu geben.

#### Techniken

- **Bereitschaftsskala (0-10):** "Wie bereit bist du gerade, dieses Gefuehl einfach da sein zu lassen?"
- **Expansion:** Das Gefuehl im Koerper lokalisieren, ihm Form/Farbe/Textur geben, es "atmen lassen"
- **Kampf-Schalter-Metapher:** Es gibt einen Schalter in uns -- nicht fuer Schmerz, sondern fuer den Kampf gegen Schmerz. Akzeptanz bedeutet, den Kampf-Schalter umzulegen.

#### Metapher: Treibsand

> Wenn du in Treibsand geraten bist, ist der natuerliche Instinkt zu kaempfen, sich zu wehren, zu strampeln. Aber genau das zieht dich tiefer hinein. Das einzig Hilfreiche: Sich flach hinlegen, die Oberflaeche vergroessern, den Kontakt mit dem Treibsand akzeptieren. Nicht weil Treibsand toll ist -- sondern weil der Kampf dagegen das eigentliche Problem ist.

---

### 2. Kognitive Defusion

**Definition:** Sich von Gedanken loesen -- sie als das sehen, was sie sind: mentale Ereignisse, nicht die Realitaet selbst. Statt "Ich bin wertlos" -> "Ich habe den Gedanken, dass ich wertlos bin."

#### Techniken

- **"Ich habe den Gedanken, dass..."** -- Gedanken sprachlich distanzieren
- **"Danke, Verstand!"** -- Den Verstand als ueberaktiven Berater anerkennen, ohne ihm zu gehorchen
- **Gedanken singen:** Den belastenden Gedanken auf die Melodie von "Happy Birthday" singen (verringert die Glaubwuerdigkeit)
- **Gedanken auf Blaetter:** Sich einen Bach vorstellen. Jeden Gedanken auf ein Blatt legen und vorbeitreiben lassen
- **Passagier-Benennung:** Dem inneren Kritiker einen Namen geben ("Ah, da ist wieder der Perfektionist-Peter")
- **Wiederholungsuebung:** Ein belastendes Wort 30 Sekunden schnell wiederholen -- es verliert seine emotionale Ladung

#### Metapher: Der ungebetene Gast

> Stell dir vor, du gibst eine Party und ein ungebetener Gast kommt. Du hast drei Moeglichkeiten: (1) Du wirfst ihn raus -- aber er kommt immer wieder und macht Laerm. (2) Du laesst ihn rein und verbringst den ganzen Abend damit, ihn zu ueberwachen -- dann verpasst du deine eigene Party. (3) Du laesst ihn rein, nimmst zur Kenntnis dass er da ist, und feierst weiter deine Party. Option 3 ist Defusion.

---

### 3. Gegenwaertigkeit (Kontakt mit dem gegenwaertigen Moment)

**Definition:** Bewusste, nicht-wertende Aufmerksamkeit auf das Hier und Jetzt. Weder in der Vergangenheit gruebelnd noch in der Zukunft sorgend.

#### Techniken

- **5-4-3-2-1 Uebung:** 5 Dinge sehen, 4 hoeren, 3 fuehlen, 2 riechen, 1 schmecken
- **Atemachtsamkeit:** 3 bewusste Atemzuege -- nur beobachten, nicht steuern
- **Sensorisches Ankern:** Einen Gegenstand mit voller Aufmerksamkeit erforschen (Textur, Gewicht, Temperatur)
- **Check-in-Fragen:** "Was passiert gerade in meinem Koerper? Was fuer Gedanken sind da? Was fuer Gefuehle?"

---

### 4. Selbst-als-Kontext (Beobachtendes Selbst)

**Definition:** Unterscheidung zwischen dem Selbst als Inhalt ("Ich BIN aengstlich") und dem Selbst als Kontext ("Ich BEMERKE Angst"). Das beobachtende Selbst ist der Raum, in dem alle Erlebnisse stattfinden -- aber es ist nicht diese Erlebnisse.

#### Techniken

- **Himmels-Metapher:** "Du bist der Himmel, nicht das Wetter. Wolken, Stuerme, Sonnenschein -- alles zieht vorbei. Aber der Himmel ist immer da."
- **Schachbrett-Metapher:** "Du bist nicht die weissen oder schwarzen Figuren. Du bist das Brett, auf dem das Spiel stattfindet."
- **Beobachter-Uebung:** Augen schliessen. Gedanken beobachten. Gefuehle beobachten. Koerperempfindungen beobachten. Dann: "Wer ist es, der all das beobachtet?"
- **Perspektiv-Uebungen:** "Wenn dein 80-jaehriges Selbst auf diese Situation zurueckblicken wuerde -- was wuerde es sagen?"

---

### 5. Werte

**Definition:** Frei gewaehlte Richtungen des Lebens. Werte sind keine Ziele (die man erreichen kann), sondern Kompassrichtungen (denen man folgt). Man "erreicht" niemals den Wert "liebevoller Partner sein" -- man lebt ihn, Moment fuer Moment.

#### Werteklaerung -- Lebensbereiche

| Lebensbereich | Leitfrage |
|---|---|
| Beziehungen | Was fuer ein Partner/Freund/Familienmitglied moechte ich sein? |
| Arbeit/Beruf | Was macht Arbeit fuer mich bedeutsam? |
| Persoenliches Wachstum | In welche Richtung moechte ich mich entwickeln? |
| Gesundheit | Wie moechte ich mit meinem Koerper umgehen? |
| Freizeit/Erholung | Was naehrt mich wirklich? |
| Spiritualitaet | Was gibt meinem Leben tieferen Sinn? |
| Gemeinschaft | Was moechte ich zur Welt beitragen? |

#### Techniken

- **Grabstein-Uebung:** "Was soll auf deinem Grabstein stehen? Nicht was du erreicht hast, sondern wofuer du gestanden hast."
- **Kompass-Uebung:** Fuer jeden Lebensbereich eine Richtung bestimmen und auf einer Skala von 1-10 bewerten: "Wie wichtig ist mir das?" und "Wie sehr lebe ich das gerade?"
- **Suesse-Stelle-des-Schmerzes:** "Hinter jedem Schmerz steckt ein Wert. Wer nicht liebt, kann nicht verletzt werden. Dass es wehtut, zeigt, dass dir etwas wichtig ist."

---

### 6. Engagiertes Handeln

**Definition:** Konkrete Handlungen, die mit den eigenen Werten uebereinstimmen. Nicht perfekt, nicht "wenn ich bereit bin", sondern JETZT, mit allen Schwierigkeiten.

#### Techniken

- **SMART-Werte-Ziele:** Spezifisch, Messbar, Attraktiv, Realistisch, Terminiert -- aber immer an einen Wert gekoppelt
- **Kleinster moeglicher Schritt:** "Was ist der kleinste Schritt, den du HEUTE in Richtung dieses Wertes gehen koenntest?"
- **Bereitschafts-Check:** "Bist du bereit, [unangenehmes Gefuehl] mitzunehmen, wenn es auftaucht, waehrend du diesen Schritt gehst?"
- **Hindernisse einplanen:** "Welche inneren Barrieren koennten auftauchen? Wie willst du mit ihnen umgehen?" (nicht: "Wie beseitigst du sie?")

#### Metapher: Passagiere im Bus

> Du bist der Busfahrer deines Lebens. Im Bus sitzen Passagiere -- das sind deine Gedanken, Gefuehle, Erinnerungen, Koerperempfindungen. Manche sind laut, bedrohlich, haesslich. Sie schreien: "Fahr rechts! Fahr links! Halt an!" Du hast drei Moeglichkeiten:
>
> 1. **Anhalten und kaempfen:** Du hoerst auf zu fahren und versuchst, die Passagiere rauszuwerfen. Aber du kommst nicht voran.
> 2. **Verhandeln:** Du faehrst dahin, wo die Passagiere wollen. Aber es ist nicht DEINE Richtung.
> 3. **Weiterfahren:** Du laesst die Passagiere schreien, nimmst sie mit -- und faehrst trotzdem in DEINE Richtung. Die Passagiere duerfen da sein. Aber SIE bestimmen nicht die Route.
>
> Engagiertes Handeln bedeutet: Den Bus in Richtung deiner Werte zu fahren, egal welche Passagiere mitfahren.

---

## Anwendungsbereiche

ACT ist evidenzbasiert wirksam bei:

- **Depression und Angststoerungen**
- **Chronische Schmerzen**
- **Suchterkrankungen**
- **Essstoerungen**
- **Burnout und Stress am Arbeitsplatz**
- **Trauma und PTBS** (ergaenzend)
- **Psychotische Stoerungen** (ergaenzend)

---

## Wann welchen Prozess ansprechen?

| Situation des Nutzers | Primaerer ACT-Prozess |
|---|---|
| Vermeidet bestimmte Gefuehle/Situationen | Akzeptanz |
| Ist in Gruebeln/Sorgen gefangen | Defusion |
| Lebt im Autopilot, dissoziiert | Gegenwaertigkeit |
| Definiert sich ueber Probleme ("Ich BIN...") | Selbst-als-Kontext |
| Fuehlt sich orientierungslos, sinnlos | Werte |
| Weiss was wichtig ist, handelt aber nicht | Engagiertes Handeln |

---

## Ethische Leitlinien

Ein KI-Assistent darf ACT-Techniken psychoedukativ erklaeren und Uebungen anleiten.

Ein KI-Assistent darf NICHT:
- Diagnosen stellen
- Eine therapeutische Beziehung simulieren
- Bei akuter Suizidalitaet allein handeln -- Verweis an professionelle Hilfe
- ACT als Ersatz fuer Psychotherapie darstellen

Siehe: [ETHICS.md](../ETHICS.md)

---

## Quellenangaben

- Hayes, S. C., Strosahl, K. D., & Wilson, K. G. (2012). *Acceptance and Commitment Therapy: The Process and Practice of Mindful Change.* 2nd Edition.
- Harris, R. (2009). *ACT Made Simple.*
- Hayes, S. C. (2005). *Get Out of Your Mind and Into Your Life.*

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
