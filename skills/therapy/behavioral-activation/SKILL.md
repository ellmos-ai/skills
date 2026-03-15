---
name: verhaltensaktivierung
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Verhaltensaktivierung bei Depression: Teufelskreis durchbrechen, Aktivitaetsprotokoll, Wochenplanung und werte-basierte Aktivitaeten.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [verhaltensaktivierung, depression, aktivitaet, wochenplan, werte, behavioral-activation]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/verhaltensaktivierung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Verhaltensaktivierung

> Aktivitaetenplanung, Stimmungs-Aktivitaets-Tagebuch und werte-basierte Aktivitaetenauswahl: Dem Teufelskreis aus Inaktivitaet und Niedergeschlagenheit entgegenwirken

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Verhaltensaktivierung (Behavioral Activation, BA) ist eine evidenzbasierte Intervention
aus der Verhaltenstherapie zur Behandlung von Depression. Sie basiert auf der Erkenntnis,
dass Depression zu Rueckzug und Inaktivitaet fuehrt, was die Stimmung weiter verschlechtert
(Teufelskreis). Durch gezielten Aufbau positiver Aktivitaeten wird dieser Kreislauf
durchbrochen.

Evidenz: Verhaltensaktivierung ist als eigenstaendige Therapieform wirksam und der
kognitiven Therapie ebenbuertig (Dimidjian et al. 2006, Richards et al. 2016 COBRA-Studie).
Bei leichter bis mittelschwerer Depression als Erstintervention empfohlen (NICE Guidelines).

**Hinweis:** Dies ist Unterstuetzung, kein Ersatz fuer professionelle Therapie.
Bei schwerer Depression oder Suizidgedanken IMMER professionelle Hilfe empfehlen.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Das Depressions-Modell der Verhaltensaktivierung

### Der Teufelskreis

```
Ausloesende Situation (Verlust, Stress, Veraenderung)
        |
        v
Niedergeschlagenheit, Energielosigkeit
        |
        v
Rueckzug, Vermeidung, Inaktivitaet
        |
        v
Weniger positive Erfahrungen, Isolation
        |
        v
Noch tiefere Niedergeschlagenheit
        |
        v
Noch mehr Rueckzug ... (Spirale)
```

### Das Gegenprinzip

```
Gezielte Aktivitaet (auch bei geringer Motivation)
        |
        v
Positive Erfahrung / Erfolgserlebnis / Kontakt
        |
        v
Leichte Stimmungsverbesserung
        |
        v
Etwas mehr Energie und Motivation
        |
        v
Weitere Aktivitaet ... (Aufwaertsspirale)
```

**Kernprinzip:** Nicht warten, bis die Motivation kommt — Handeln erzeugt Motivation.
"Act first, feel second." (Nicht: "Erst fuehlen, dann handeln.")

---

## 2. Stimmungs-Aktivitaets-Tagebuch

### Ziel
Zusammenhaenge zwischen Aktivitaeten und Stimmung sichtbar machen.
Erkennen, welche Aktivitaeten die Stimmung verbessern und welche verschlechtern.

### Tagebuch-Format

```
STIMMUNGS-AKTIVITAETS-TAGEBUCH

Datum: [...]

| Uhrzeit | Aktivitaet | Stimmung (0-10) | Freude (0-10) | Wichtigkeit (0-10) |
|---------|-----------|-----------------|---------------|---------------------|
| 07:00   | Aufgestanden, gefruestueckt | 3 | 2 | 5 |
| 08:00   | Arbeit: E-Mails | 4 | 1 | 6 |
| 10:00   | Spaziergang | 6 | 5 | 4 |
| 12:00   | Mittagessen mit Kollegin | 7 | 6 | 7 |
| 14:00   | Arbeit: Projekt | 5 | 3 | 7 |
| 18:00   | Fernsehen (allein) | 3 | 2 | 1 |
| 20:00   | Telefonat mit Freund | 6 | 5 | 8 |

Tagesdurchschnitt Stimmung: [...]
Beste Aktivitaet heute: [...]
Erkenntnis: [...]
```

### Auswertung nach einer Woche

**Leitfragen:**
- Welche Aktivitaeten heben die Stimmung regelmaessig?
- Welche Aktivitaeten druecken die Stimmung?
- Gibt es Zeiten, die besonders schwierig sind?
- Wie viel Zeit verbringe ich mit angenehmen vs. unangenehmen Aktivitaeten?
- Welche Aktivitaeten habe ich vermieden?

---

## 3. Aktivitaetenplanung

### Schritt 1: Aktivitaetenliste erstellen

Drei Kategorien von Aktivitaeten sammeln:

**A) Angenehme Aktivitaeten (Freude, Genuss)**
- Natur: Spaziergang, Park, Wald
- Sozial: Freunde treffen, telefonieren, gemeinsam kochen
- Kreativ: Musik, Malen, Schreiben, Basteln
- Koerperlich: Sport, Yoga, Tanzen, Schwimmen
- Genuss: Lieblingsgericht kochen, Buch lesen, Musik hoeren
- Entspannung: Bad nehmen, Meditation, Atemuebung

**B) Notwendige Aktivitaeten (Struktur, Selbstfuersorge)**
- Haushalt: Aufraeumen, Kochen, Einkaufen
- Koerperpflege: Duschen, Anziehen, Zaehneputzen
- Administration: Rechnungen, Termine, Papierkram
- Gesundheit: Arzttermine, Medikamente, Ernaehrung

**C) Werte-basierte Aktivitaeten (Sinn, Bedeutung)**
- Siehe Abschnitt 4 unten

### Schritt 2: Wochenplan erstellen

```
WOCHENPLAN

| Tag | Morgens | Mittags | Nachmittags | Abends |
|-----|---------|---------|-------------|--------|
| Mo  | [...]   | [...]   | [...]       | [...]  |
| Di  | [...]   | [...]   | [...]       | [...]  |
| Mi  | [...]   | [...]   | [...]       | [...]  |
| Do  | [...]   | [...]   | [...]       | [...]  |
| Fr  | [...]   | [...]   | [...]       | [...]  |
| Sa  | [...]   | [...]   | [...]       | [...]  |
| So  | [...]   | [...]   | [...]       | [...]  |
```

### Planungsregeln
1. **Klein anfangen:** Nicht den ganzen Tag durchplanen, sondern 1-2 Aktivitaeten pro Tag
2. **Mischung:** Angenehm + Notwendig + Werte-basiert
3. **Konkret:** "Dienstag 15:00 Spaziergang im Park" statt "Mehr bewegen"
4. **Realistisch:** Machbar auch bei wenig Energie
5. **Flexibel:** Plan ist Orientierung, kein Zwang
6. **Abgestuft:** Bei sehr geringer Energie: Mini-Schritte (5 Minuten reichen)

### Umgang mit Hindernissen

| Hindernis | Strategie |
|-----------|-----------|
| "Ich habe keine Energie" | Aktivitaet auf 5 Minuten reduzieren |
| "Ich habe keine Lust" | Erinnerung: Motivation kommt durch Handeln |
| "Es bringt sowieso nichts" | Experiment: Ausprobieren und Stimmung danach messen |
| "Ich schaffe es nicht allein" | Jemanden einbinden (Verabredung = Verbindlichkeit) |
| "Ich habe keine Zeit" | Kleine Aktivitaeten einbauen (Treppen steigen, 5 Min Pause draussen) |

---

## 4. Werte-basierte Aktivitaetenauswahl

### Prinzip
Aktivitaeten, die mit persoenlichen Werten uebereinstimmen, erzeugen nachhaltiges
Wohlbefinden — im Gegensatz zu reinem Vergnuegen, das schnell verfliegt.

### Lebensbereiche und Werte

```
WERTE-KOMPASS

Beziehungen:     Was fuer ein Partner/Freund/Familienmitglied moechte ich sein?
Arbeit/Bildung:  Was ist mir bei meiner Arbeit wichtig?
Freizeit:        Wie moechte ich meine freie Zeit verbringen?
Gesundheit:      Wie moechte ich mit meinem Koerper umgehen?
Gemeinschaft:    Welchen Beitrag moechte ich leisten?
Persoenliches:   Welcher Mensch moechte ich sein?
```

### Werte-Aktivitaeten-Mapping

**Beispiel:**

| Wert | Aktivitaet | Haeufigkeit |
|------|-----------|-------------|
| Verbundenheit | Freund anrufen | 2x pro Woche |
| Gesundheit | 20 Min spazieren | Taeglich |
| Kreativitaet | Gitarre spielen | 1x pro Woche |
| Hilfsbereitschaft | Nachbarin beim Einkauf helfen | 1x pro Woche |
| Lernen | 15 Min Fachbuch lesen | 3x pro Woche |

### Werte vs. Ziele
- **Wert:** Eine Richtung, in die man gehen moechte (z.B. "liebevoller Partner sein")
- **Ziel:** Ein erreichbarer Endpunkt (z.B. "Hochzeitstag planen")
- Werte koennen nie "abgehakt" werden — sie geben dauerhaft Orientierung

---

## 5. Fortschritt messen

### Wochen-Review

```
WOCHEN-REVIEW

Woche: [Datum]
Geplante Aktivitaeten: [Anzahl]
Umgesetzte Aktivitaeten: [Anzahl]
Durchschnittliche Stimmung: [0-10]

Was lief gut: [...]
Was war schwierig: [...]
Erkenntnis der Woche: [...]
Plan fuer naechste Woche: [...]
```

### Langzeit-Tracking
- Stimmungsverlauf ueber Wochen beobachten
- Zusammenhang zwischen Aktivitaetsgrad und Stimmung erkennen
- Erfolge sichtbar machen (auch kleine)

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Durch das Tagebuch und die Aktivitaetenplanung fuehren
- Aktivitaetenvorschlaege machen (nie verordnen)
- Stimmungs-Daten dokumentieren und Muster zurueckmelden
- Werte-Reflexion begleiten
- Kleine Fortschritte wuerdigen

**Ein KI-Assistent darf NICHT:**
- Bei schwerer Depression alleinige Unterstuetzung sein
- Medikamentenbezogene Empfehlungen geben
- Suizidalitaet einschaetzen
- Diagnosen stellen
- Garantieren, dass Verhaltensaktivierung ausreicht

**Wichtig:** Bei schwerer Depression (anhaltende Antriebslosigkeit, Suizidgedanken,
Unfaehigkeit den Alltag zu bewaeltigen) ist professionelle Hilfe unabdingbar.
Verhaltensaktivierung ist Ergaenzung, nicht Ersatz.

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: Martell et al. (2010), Dimidjian et al. (2006), Richards et al. (2016) — Keine professionelle Therapie*
