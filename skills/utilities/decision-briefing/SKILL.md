---
name: decision-briefing
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: >
  Viele offene Entscheidungen eines Themas strukturiert abarbeiten: Inventarisieren,
  als nummeriertes Briefing mit Optionen A/B/C/D und markierter Empfehlung vorlegen,
  Buchstaben-Antworten (auch im Batch) entgegennehmen, Ergebnisse protokollieren
  und in die Quelldokumente zurueckschreiben.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: utilities
tags: [entscheidung, briefing, batch, decision-session, priorisierung, workflow]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/agents/_experts/decision-briefing/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-06-13"
  last_sync_to_origin: null
  local_changes_since_sync: true
  # Hinweis: Die Scanner-Komponente des BACH-Originals (scanner.py, sources.json,
  # systemweite Marker-Scans) wurde fuer die Standalone-Version bewusst entfernt.
  # Erfassung erfolgt leichtgewichtig aus dem vorliegenden Kontext.
---

# Decision-Briefing — Viele Entscheidungen eines Themas strukturiert abarbeiten

> Aus einem Berg offener Entscheidungen wird ein nummeriertes Briefing mit Empfehlungen, das der User blitzschnell per Buchstaben beantworten kann — einzeln oder im Batch.

---

## Wann nutzen?

- In EINEM Bereich/Thema haben sich viele offene Entscheidungen angesammelt
- Ein Dokument (Plan, TODO-Liste, Konzept) enthält mehrere unentschiedene Punkte
- Im Gespräch sind nacheinander mehrere Entscheidungsfragen aufgelaufen
- Der User will offene Punkte schnell und fundiert "wegarbeiten"

**Trigger-Wörter:** offene Entscheidungen, Entscheidungs-Session, Briefing, abarbeiten, durchgehen, entscheiden wir das mal alles

**Abgrenzung:** [decide](../decide/SKILL.md) liefert Frameworks für EINE Frage. `decision-briefing` koordiniert die Abarbeitung VIELER Entscheidungen eines Themas — und setzt `decide` bei komplexen Einzelfällen ein.

---

## Kern-UX

Das Herzstück ist das Briefing-Format. Jede Entscheidung wird so vorgelegt, dass die Antwort nur einen Buchstaben kostet:

- **Nummerierung:** `[E01]`, `[E02]`, … — stabile Referenz über die ganze Session
- **Kurze Frage** + 1–2 Sätze Kontext
- **Optionen als Buchstaben** A/B/C/D (2–4 Optionen, mehr nur wenn nötig)
- **Markierte Empfehlung** mit 1-Satz-Begründung (z.B. `→ Empfehlung: A — weil …`)
- Optional: Konsequenz-Hinweis (was folgt aus der Wahl)

**Antwortformate des Users:**

```
Einzeln:   "E01: A"  oder  "1A"
Batch:     "1A 2C 3B"  oder  "E01: A, E02: C, E03: B"
Vertiefen: "E02: mehr Info"  oder  "2?"
Vertagen:  "E03: später"
```

---

## Workflow (4 Phasen)

```
Thema + vorliegende Entscheidungen
     |
     v
Phase 1: ERFASSEN & INVENTARISIEREN
     |
     v
Phase 2: BRIEFING AUFBEREITEN
     |
     v
Phase 3: DECISION-SESSION
     |
     v
Phase 4: PROTOKOLL & RUECKSCHREIBEN
```

### Phase 1: Erfassen & Inventarisieren

Quellen: Was der User nennt, ein vorliegendes Dokument oder der Gesprächskontext. Kein systemweiter Scan — nur das, was vorliegt.

1. Alle offenen Entscheidungen als Liste aufstellen (je 1 Zeile: Kurztitel)
2. **Duplikate** erkennen und zusammenführen (gleiche Frage, mehrfach formuliert)
3. **Abhängigkeiten** markieren ("E04 hängt von E01 ab")
4. **Reihenfolge** festlegen: Blocker zuerst (Entscheidungen, von denen andere abhängen), dann nach Dringlichkeit
5. Liste dem User kurz zur Bestätigung zeigen ("Habe ich alle? Fehlt etwas?")

### Phase 2: Briefing aufbereiten

Pro Entscheidung:

```
[E01] <Kurze Frage>
  Kontext: <1-2 Saetze: Warum steht das an? Was haengt dran?>
  A) <Option>
  B) <Option>
  C) <Option>
  → Empfehlung: <Buchstabe> — <1-Satz-Begruendung>
  (optional) Konsequenz: <Was folgt aus der Wahl / naechste Aktion>
```

Regeln für gute Optionen:

- Optionen müssen sich gegenseitig ausschließen und das Spektrum abdecken
- Bei Bedarf eine Option "Status quo behalten" oder "vertagen" mit aufnehmen
- Die Empfehlung ist transparent begründet — nie versteckt suggestiv
- Bei unklarer Faktenlage: erst klären (oder als offene Frage kennzeichnen), nicht raten

### Phase 3: Decision-Session

1. Briefing vorlegen — einzeln (eine Entscheidung pro Nachricht) oder als Batch (alle auf einmal); bei >5 Entscheidungen in Blöcken von 3–5
2. Buchstaben-Antworten entgegennehmen und quittieren
3. Bei "mehr Info"-Antwort: Entscheidung vertiefen (Methoden-Werkzeugkasten unten)
4. Bei komplexen Einzelfällen (viele Kriterien, hohe Tragweite): an den [decide](../decide/SKILL.md)-Skill eskalieren (Weighted Scoring, Scenario Analysis)
5. Vertagte Entscheidungen explizit als offen weiterführen — nicht stillschweigend fallen lassen

### Phase 4: Protokoll & Rückschreiben

1. **Ergebnis-Tabelle** erstellen:

```
| Nr.  | Entscheidung        | Gewaehlt | Status   |
|------|---------------------|----------|----------|
| E01  | <Kurztitel>         | A        | getroffen|
| E02  | <Kurztitel>         | C        | getroffen|
| E03  | <Kurztitel>         | —        | vertagt  |
```

2. Getroffene Entscheidungen in die **Quelldokumente/TODO-Dateien eintragen** — am Fundort der offenen Frage, z.B.:

```
ENTSCHEIDUNG: <Frage>
  → GETROFFEN 2026-06-13: Option A (<Kurzfassung>)
  → Naechste Aktion: <falls die Entscheidung eine Folgeaktion impliziert>
```

3. **Vertagtes explizit als offen führen** (im Quelldokument oder in der TODO-Liste), damit es beim nächsten Briefing wieder auftaucht

---

## Beispiel-Briefing (fiktiv)

Thema: Relaunch einer Vereinswebsite — 3 offene Entscheidungen aus dem Projektplan.

```
[E01] Welches System fuer die neue Website?
  Kontext: Aktuelle Seite ist handgepflegtes HTML; 2 Personen sollen kuenftig Inhalte pflegen.
  A) Static-Site-Generator (schnell, sicher, Pflege via Git)
  B) Klassisches CMS mit Admin-Oberflaeche
  C) Website-Baukasten (gehostet)
  → Empfehlung: B — zwei nicht-technische Redakteure brauchen eine Oberflaeche, kein Git.

[E02] Wie wird gehostet?
  Kontext: Budget ~10 EUR/Monat, kein eigener Admin im Verein.
  A) Shared Hosting beim bestehenden Anbieter
  B) Eigener kleiner VPS
  C) Managed Hosting passend zum gewaehlten System
  → Empfehlung: C — am wenigsten Wartungsaufwand ohne Admin; Konsequenz: haengt von E01 ab.

[E03] Wann geht die neue Seite live?
  Kontext: Inhalte sind zu 60% migriert; Vereinsjubilaeum in 3 Monaten.
  A) Sofort als Soft-Launch (Rest nachziehen)
  B) Nach vollstaendiger Inhaltsmigration
  C) Zum Jubilaeum als Stichtag
  → Empfehlung: A — umkehrbar und liefert frueh Feedback; finale Inhalte folgen.
```

User antwortet im Batch: **"1B 2C 3A"** → Ergebnis-Tabelle, dann werden die drei Entscheidungen im Projektplan als GETROFFEN eingetragen.

---

## Methoden-Werkzeugkasten (für "mehr Info" und Vertiefung)

| Methode | Wann | Kurzbeschreibung |
|---------|------|------------------|
| **Pro/Contra-Matrix** | 2–3 Optionen, schneller Vergleich | Alle Optionen nebeneinander bewerten |
| **Nutzwertanalyse** | Mehrere Kriterien | Gewichtete Kriterien, Punkte pro Option (quantitativ wenn möglich) |
| **Second-Order Thinking** | Tragweite unklar | Was sind die Folgen der Folgen? |
| **Prämortem** | Riskante Entscheidung | "Es ist schiefgegangen — warum?" Schwachstellen vorab finden |
| **10/10/10-Methode** | Emotionale/zeitliche Verzerrung | Wie wirkt die Entscheidung in 10 Minuten / 10 Monaten / 10 Jahren? |

---

## Arbeitsprinzipien

- **Keine Entscheidungen aufdrängen:** Informationen liefern, Empfehlung transparent begründen — der User entscheidet
- **Bias-Erkennung:** Denkfehler ansprechen, wenn sie sichtbar werden (Confirmation Bias, Sunk Cost)
- **Reversibilität beachten:** Umkehrbare Entscheidungen schnell entscheiden, finale gründlicher behandeln
- **Zeitdruck berücksichtigen:** Schnelle Entscheidungen brauchen einfachere Methoden — nicht jede Frage verdient eine Nutzwertanalyse

---

## Abgrenzung und Synergien

| Funktion | `decide` | `decision-briefing` |
|---|---|---|
| Einzelne Entscheidung mit Framework strukturieren | ✓ | — |
| Viele Entscheidungen eines Themas inventarisieren | — | ✓ |
| Nummeriertes Briefing mit A/B/C-Optionen | — | ✓ |
| Batch-Antworten ("1A 2C 3B") | — | ✓ |
| Rückschreiben in Quelldokumente | — | ✓ |

**Synergie:** Bei komplexen Einzelfällen innerhalb einer Session wendet `decision-briefing` die Frameworks aus `decide` an (Weighted Scoring, Scenario Analysis). Für den größeren Denkprozess davor (Analyse → Ideen → Entscheidung) siehe [structured-thinking](../structured-thinking/SKILL.md).

---

## Changelog

### 1.0.0 (2026-06-13)
- Portiert aus dem BACH-Experten `decision-briefing` v1.0.0; Scanner-Komponente (scanner.py, sources.json, Marker-Scans) bewusst entfernt — Erfassung erfolgt leichtgewichtig aus dem vorliegenden Kontext

---

*Portiert aus BACH | Standalone-Version ohne Scanner*

**Siehe auch:** [decide](../decide/SKILL.md) (Frameworks für eine einzelne Entscheidung) | [structured-thinking](../structured-thinking/SKILL.md) (Analyse → Ideen → Entscheidung als Meta-Workflow)
