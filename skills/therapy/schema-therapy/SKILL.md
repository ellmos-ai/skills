---
name: schema-therapy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Schematherapie nach Jeffrey Young: Schemata, Modi, Inneres-Kind-Konzept und Bewaeltigungsstile — psychoedukativ vermittelt.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [schematherapie, schema-therapy, modi, inneres-kind, bewaeltigungsstile, persoenlichkeit]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/schematherapie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Schematherapie

> Grundlagen der Schematherapie nach Jeffrey Young: Schemata, Modi, Inneres-Kind-Konzept und Bewaeltigungsstile — psychoedukativ vermittelt

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Die Schematherapie wurde von Jeffrey E. Young ab den 1990er-Jahren als Erweiterung
der kognitiven Verhaltenstherapie entwickelt. Sie integriert Elemente aus KVT,
Bindungstheorie, Gestalttherapie und psychodynamischen Ansaetzen.

Evidenz: Die Schematherapie ist empirisch gut belegt, insbesondere fuer
Persoenlichkeitsstoerungen (Giesen-Bloo et al. 2006, Masley et al. 2012).
In Deutschland ist sie als Methode innerhalb der Verhaltenstherapie anerkannt.

**Hinweis:** Dies ist Psychoedukation, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Fruehe maladaptive Schemata

### Prinzip
Schemata sind tief verwurzelte emotionale und kognitive Muster, die in der Kindheit
durch unerfuellte Grundbeduerfnisse entstehen. Sie beeinflussen, wie wir die Welt,
uns selbst und andere wahrnehmen.

### Die fuenf Grundbeduerfnisse (nach Young)

| Grundbeduerfnis | Wenn unerfuellt, entstehen z.B. |
|----------------|-------------------------------|
| Sichere Bindung | Verlassenheit, Misstrauen |
| Autonomie & Kompetenz | Abhaengigkeit, Versagensangst |
| Realistische Grenzen | Anspruchshaltung, mangelnde Selbstkontrolle |
| Freier Ausdruck von Beduerfnissen | Unterwerfung, Aufopferung |
| Spontanitaet & Spiel | Uebertriebene Standards, Bestrafungsneigung |

### Die 18 Schemata — Ueberblick (5 Domaenen)

**Domaene 1: Abgetrenntheit und Ablehnung**
- Verlassenheit / Instabilitaet
- Misstrauen / Missbrauch
- Emotionale Entbehrung
- Unzulaenglichkeit / Scham
- Soziale Isolation

**Domaene 2: Beeintraechtigte Autonomie**
- Abhaengigkeit / Inkompetenz
- Verletzbarkeit
- Verstrickung / Unentwickeltes Selbst
- Versagen

**Domaene 3: Beeintraechtigte Grenzen**
- Anspruchshaltung / Grandiosiaet
- Unzureichende Selbstkontrolle

**Domaene 4: Fremdbestimmtheit**
- Unterwerfung
- Aufopferung
- Streben nach Anerkennung

**Domaene 5: Uebermaessige Wachsamkeit**
- Negativitaet / Pessimismus
- Emotionale Gehemmtheit
- Uebertriebene Standards
- Bestrafungsneigung

### Reflexionsfragen zur Schema-Erkennung
- "Welche Ueberzeugungen ueber dich selbst tauchen immer wieder auf?"
- "In welchen Situationen reagierst du besonders stark emotional?"
- "Erkennst du Muster, die sich in verschiedenen Beziehungen wiederholen?"
- "Welche Beduerfnisse kamen in deiner Kindheit moeglicherweise zu kurz?"

---

## 2. Das Modi-Modell

### Prinzip
Modi sind momentane emotionale Zustaende, die durch Schemata aktiviert werden.
Das Modi-Modell hilft, verschiedene "innere Anteile" zu verstehen und einzuordnen.

### Die vier Modi-Kategorien

**Kind-Modi:**
- *Verletztes Kind:* Fuehlt sich traurig, einsam, aengstlich, ueberwaeltigt
- *Aergerliches Kind:* Wuetend ueber unerfuellte Beduerfnisse
- *Impulsives Kind:* Handelt unueberlegt, will sofortige Befriedigung
- *Glueckliches Kind:* Fuehlt sich sicher, geliebt, spontan

**Maladaptive Eltern-Modi:**
- *Strafender Elternmodus:* Innere Stimme, die kritisiert, bestraft, abwertet
- *Fordernder Elternmodus:* Innere Stimme, die Perfektion und Leistung verlangt

**Maladaptive Bewaeltigungsmodi:**
- *Unterwerfung / Erduldung:* Gibt nach, passt sich uebertrieben an
- *Vermeidung:* Betaeubt Gefuehle, zieht sich zurueck, lenkt ab
- *Ueberkompensation:* Dominiert, kontrolliert, greift an

**Gesunder Erwachsener:**
- Kann Beduerfnisse wahrnehmen und angemessen erfuellen
- Setzt gesunde Grenzen
- Troestet und beruhigt das verletzte Kind
- Begrenzt uebertriebene Eltern-Modi

### Uebung: Modi im Alltag erkennen

```
Situation: ______________
Welchen Modus spuere ich gerade?
  [ ] Verletztes Kind — "Ich fuehle mich klein und hilflos"
  [ ] Aergerliches Kind — "Das ist unfair!"
  [ ] Strafender Elternmodus — "Du bist nicht gut genug"
  [ ] Fordernder Elternmodus — "Du musst mehr leisten"
  [ ] Vermeidung — "Ich will nicht darueber nachdenken"
  [ ] Ueberkompensation — "Ich zeig's denen"
  [ ] Gesunder Erwachsener — "Was brauche ich jetzt wirklich?"
```

---

## 3. Inneres-Kind-Arbeit (psychoedukativ)

### Prinzip
Die Innere-Kind-Arbeit in der Schematherapie zielt darauf ab, eine fuersorgliche
innere Haltung gegenueber den eigenen verletzten Anteilen zu entwickeln.

**ACHTUNG:** Tiefgehende Innere-Kind-Arbeit gehoert in professionelle therapeutische Begleitung.

### Reflexionsuebung: Brief an das innere Kind

```
Schreibe einen kurzen Brief an dein juengeres Ich:
1. Was haettest du damals gebraucht?
2. Was wuerdest du dem Kind heute sagen?
3. Welchen Trost wuerdest du anbieten?
```

### Reflexionsfragen
- "Wenn du an die Situation denkst — wie alt fuehlst du dich innerlich?"
- "Was haette ein fuersorglicher Erwachsener damals zu dir gesagt?"
- "Welche Beduerfnisse des Kindes in dir kommen gerade zu kurz?"

---

## 4. Bewaeltigungsstile verstehen

### Die drei Grundmuster

| Bewaeltigungsstil | Strategie | Beispiel |
|-------------------|-----------|----------|
| Erduldung | Schema akzeptieren, sich fuegen | "So bin ich eben, ich kann nichts aendern" |
| Vermeidung | Schema nicht fuehlen wollen | Ablenkung, Substanzkonsum, Ueberarbeitung |
| Ueberkompensation | Gegenteil des Schemas leben | Perfektionismus statt Versagensgefuehl |

### Reflexionsfragen
- "Wenn du unter Druck geraetst — neigst du eher dazu, dich zu fuegen, zu fliehen oder zu kaempfen?"
- "Welche deiner Gewohnheiten koennten Vermeidungsstrategien sein?"
- "Gibt es Bereiche, in denen du das Gegenteil von dem machst, was du eigentlich fuehlst?"

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Schemata und Modi als Konzepte erklaeren
- Reflexionsfragen stellen zur Selbsterkundung
- Bewaeltigungsstile als Psychoedukation vorstellen
- Innere-Kind-Reflexionsuebungen anleiten (einfache, schriftliche)

**Ein KI-Assistent darf NICHT:**
- Schemata diagnostizieren oder zuschreiben
- Stuhlarbeit oder erlebnisaktivierende Uebungen durchfuehren
- Reparenting (Nachbeelterung) anbieten
- Traumatische Kindheitserfahrungen bearbeiten
- Schema-Modi-Therapie ersetzen

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Quellenangaben

- Young, J. E., Klosko, J. S. & Weishaar, M. E. (2003). *Schema Therapy: A Practitioner's Guide.* Guilford Press.
- Giesen-Bloo, J. et al. (2006). Outpatient Psychotherapy for Borderline Personality Disorder. *Archives of General Psychiatry*, 63(6), 649-658.
- Roediger, E. (2011). *Praxis der Schematherapie.* Schattauer.

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: Young et al. (2003), Giesen-Bloo et al. (2006), Roediger (2011) — Keine professionelle Therapie*
