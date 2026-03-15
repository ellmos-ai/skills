---
name: genogram-work
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Genogramm-Arbeit: Familien-Beziehungsmuster erkennen und reflektieren. Mehrgenerationen-Perspektive, Genogramm-Symbole, Muster-Erkennung und Ressourcen in der Familiengeschichte.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [genogramm, systemische-therapie, familientherapie, mehrgenerationen, beziehungsmuster]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/genogramm_arbeit.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Genogramm-Arbeit

> Familien-Beziehungsmuster erkennen und reflektieren: Mehrgenerationen-Perspektive, Genogramm-Symbole, Muster-Erkennung und Ressourcen in der Familiengeschichte

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Das Genogramm ist ein Werkzeug aus der systemischen Therapie und Familientherapie.
Es wurde massgeblich von Murray Bowen (Mehrgenerationen-Ansatz) und Monica McGoldrick
(Genogramm-Standardisierung) gepraegt. Es stellt Familienbeziehungen ueber mehrere
Generationen grafisch dar und macht Muster, Rollen und Dynamiken sichtbar.

Evidenz: Genogrammarbeit ist Bestandteil aller systemischen Therapieausbildungen und
in der klinischen Praxis als diagnostisches und reflexives Werkzeug etabliert
(McGoldrick, Gerson & Petry 2020, von Schlippe & Schweitzer 2012).

**Hinweis:** Dies ist ein Reflexionswerkzeug, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Was ist ein Genogramm?

### Definition
Ein Genogramm ist eine erweiterte grafische Darstellung des Stammbaums, die neben
der biologischen Abstammung auch Beziehungsqualitaeten, emotionale Muster, Konflikte,
Krankheiten und wichtige Lebensereignisse erfasst — typischerweise ueber drei Generationen.

### Unterschied zum Stammbaum

| Stammbaum | Genogramm |
|-----------|-----------|
| Wer ist mit wem verwandt? | Wie stehen die Personen zueinander? |
| Biologische Abstammung | Emotionale Beziehungsqualitaet |
| Statische Fakten | Dynamische Muster |
| Historisch orientiert | Muster-orientiert |

---

## 2. Genogramm-Symbole (Standard nach McGoldrick)

### Personen

```
Maennlich:    [ ]     (Quadrat)
Weiblich:     ( )     (Kreis)
Divers:       < >     (Raute)
Verstorben:   [X]     (Symbol mit X)
Indexperson:  [=]     (doppelte Umrandung)
```

### Beziehungen

```
Ehe/Partnerschaft:     ———————      (durchgezogene Linie)
Trennung:              ——/——        (Linie mit einem Strich)
Scheidung:             ——//——       (Linie mit zwei Strichen)
Enge Beziehung:        ═══════      (Doppellinie)
Verstrickte Beziehung: ≡≡≡≡≡≡≡      (Dreifachlinie)
Konflikt:              /\/\/\/\     (Zickzack-Linie)
Distanz:               · · · · ·   (gepunktete Linie)
Abbruch:               ——||——      (Linie mit Doppelstrich)
```

---

## 3. Wie erstelle ich ein Genogramm?

### Schritt-fuer-Schritt-Anleitung

**Schritt 1: Daten sammeln**
Fuer jede Person (mindestens 3 Generationen):
- Name, Geburtsjahr, ggf. Sterbejahr
- Beruf, Wohnort
- Besondere Lebensereignisse (Migration, Krankheit, Verluste)
- Beziehungsstatus

**Schritt 2: Grundstruktur zeichnen**
- Grosseltern oben, Kinder unten
- Partner nebeneinander
- Kinder von links nach rechts (aelteste zuerst)

**Schritt 3: Beziehungsqualitaeten eintragen**
- Welche Beziehungen sind eng, welche distanziert?
- Wo gibt es Konflikte?
- Wo gibt es Verstrickungen oder Abbrueche?

**Schritt 4: Muster markieren**
- Wiederkehrende Themen farblich markieren
- Z.B.: Sucht (rot), psychische Erkrankung (blau), Trennung (orange)

---

## 4. Muster erkennen — Mehrgenerationen-Perspektive

### Typische Mehrgenerationen-Muster

**Wiederholungsmuster:**
- Scheidungen ueber mehrere Generationen
- Suchtverhalten (Alkohol, Arbeit, ...)
- Fruehe Elternschaft
- Berufswahl / Rollenverteilung

**Beziehungsmuster:**
- Verstrickung (zu enge Beziehung, keine Grenzen)
- Cut-off (Kontaktabbruch, Ausschluss)
- Triangulierung (Kind wird in Elternkonflikt hineingezogen)
- Parentifizierung (Kind uebernimmt Elternrolle)

**Rollen und Auftraege:**
- "Der Starke" / "Die Kuemmerin"
- "Das schwarze Schaf"
- "Der Friedensstifter"
- Unausgesprochene Familienauftraege ("Du sollst es besser haben")

### Reflexionsfragen zu Mustern
- "Welche Themen tauchen in deiner Familie ueber Generationen auf?"
- "Welche Rolle hast du in deiner Familie uebernommen?"
- "Gibt es Familienregeln, die nie ausgesprochen wurden?"
- "Wem in der Familie aehnelst du am meisten — und in welcher Hinsicht?"
- "Welche Beziehungsmuster deiner Eltern erkennst du bei dir wieder?"

---

## 5. Ressourcen im Genogramm

### Nicht nur Probleme — auch Staerken

Das Genogramm zeigt nicht nur Belastungen, sondern auch Ressourcen:
- Wer hat schwierige Zeiten gemeistert?
- Welche Staerken gibt es in der Familie?
- Wer war ein positives Vorbild?
- Welche Werte wurden weitergegeben, die hilfreich sind?

### Reflexionsfragen zu Ressourcen
- "Wer in deiner Familie bewundert dich? Wofuer?"
- "Von wem hast du eine Staerke geerbt oder gelernt?"
- "Welches Familienmitglied hat eine Krise besonders gut gemeistert?"
- "Welche positiven Familientraditionen moechtest du weiterfuehren?"
- "Was hat deine Familie zusammengehalten?"

---

## 6. Uebungen

### Uebung 1: Mein Genogramm
Zeichne dein eigenes Genogramm (3 Generationen).
Verwende die Symbole aus Abschnitt 2.
Notiere zu jeder Person 2-3 Stichworte.

### Uebung 2: Beziehungsqualitaeten
Trage in dein Genogramm die Beziehungsqualitaeten ein:
- Wo sind die engsten Beziehungen?
- Wo gibt es Konflikte?
- Wo gibt es Distanz oder Kontaktabbruch?

### Uebung 3: Muster-Suche
Schau dir dein fertiges Genogramm an und beantworte:
1. Welche Themen wiederholen sich?
2. Welche Rollen erkennst du?
3. Welche Muster moechtest du weiterfuehren — und welche nicht?

### Uebung 4: Ressourcen-Genogramm
Markiere in deinem Genogramm alle positiven Ressourcen:
Staerken, Talente, gemeisterte Krisen, positive Werte.

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Genogramm-Konzepte und Symbole erklaeren
- Bei der Erstellung eines einfachen Genogramms unterstuetzen
- Reflexionsfragen zu Familienmustern stellen
- Auf Ressourcen in der Familiengeschichte hinweisen

**Ein KI-Assistent darf NICHT:**
- Familiendiagnosen stellen
- Familiengeheimnisse oder Traumata bearbeiten
- Familienaufstellungen durchfuehren
- Schuldzuweisungen an Familienmitglieder foerdern
- Familientherapeutische Interventionen vornehmen

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Quellenangaben

- McGoldrick, M., Gerson, R. & Petry, S. (2020). *Genograms: Assessment and Treatment.* Norton.
- Bowen, M. (1978). *Family Therapy in Clinical Practice.* Jason Aronson.
- von Schlippe, A. & Schweitzer, J. (2012). *Lehrbuch der systemischen Therapie und Beratung.* Vandenhoeck & Ruprecht.

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: McGoldrick et al. (2020), Bowen (1978), von Schlippe & Schweitzer (2012) — Keine professionelle Therapie*
