---
name: kognitive-umstrukturierung
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Kognitive Verhaltenstherapie: ABC-Modell, automatische Gedanken, Denkfehler erkennen und Gedankenprotokoll fuehren.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [kvt, cbt, kognitive-umstrukturierung, denkfehler, gedankenprotokoll, abc-modell]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/kognitive_umstrukturierung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Kognitive Umstrukturierung

> Verhaltenstherapeutische Kerntechnik: ABC-Schema, dysfunktionale Gedanken erkennen und veraendern

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Kognitive Umstrukturierung ist eine Kerntechnik der kognitiven Verhaltenstherapie (KVT).
Sie hilft dabei, automatische negative Gedanken zu erkennen, zu hinterfragen und durch
hilfreichere Alternativen zu ersetzen.

**Hinweis:** Dies ist Unterstuetzung, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. ABC-Modell (Ellis)

Das ABC-Modell erklaert wie Ereignisse, Gedanken und Gefuehle zusammenhaengen.

```
A (Activating Event)   ->  B (Beliefs / Gedanken)  ->  C (Consequences / Gefuehle/Verhalten)
Ausloser                   Bewertung / Ueberzeugung     Emotionale Folge
```

**Wichtig:** Nicht das Ereignis (A) erzeugt die Emotion (C), sondern die Bewertung (B)!

**Beispiel:**
```
A: Chef kritisiert einen Bericht im Meeting
B: "Ich bin inkompetent, alle denken das jetzt"
C: Scham, Rueckzug, Vermeidung zukuenftiger Beitraege
```

**Ziel:** B veraendern, um C zu beeinflussen.

---

## 2. Automatische Negative Gedanken (ANGs) erkennen

**Was sind ANGs?**
- Schnelle, automatische Bewertungen in stressigen Situationen
- Oft als Fakten wahrgenommen, obwohl sie Interpretationen sind
- Tendieren zu Uebertreibung, Verallgemeinerung, Katastrophisierung

**Typische Erkennungsmerkmale:**
- Absolutes Denken: "immer", "nie", "alle", "niemand"
- Katastrophisierung: "Das wird furchtbar enden"
- Gedankenlesen: "Er denkt bestimmt, dass..."
- Uebergeneralisierung: "Das klappt bei mir nie"

**Erkennungs-Fragen:**
- "Was ist dir durch den Kopf gegangen, als das passiert ist?"
- "Wenn du an die Situation denkst, welche Worte kommen?"
- "Was befuerchtest du koennte passieren?"

---

## 3. Kognitive Verzerrungen (Denkfehler)

| Denkfehler | Beschreibung | Beispiel |
|------------|--------------|---------|
| Alles-oder-nichts | Schwarz-Weiss-Denken | "Wenn ich nicht perfekt bin, bin ich ein Versager" |
| Uebergeneralisierung | Ein Fall = Allgemeines Muster | "Das geht bei mir immer schief" |
| Gedankenfilter | Nur Negatives wahrnehmen | Focussieren auf einzigen Kritikpunkt im Feedback |
| Gedankenlesen | Andere wissen was andere denken | "Er hasst mich sicher" |
| Katastrophisieren | Schlimmsten Fall annehmen | "Das wird eine Katastrophe werden" |
| Emotionale Begruendung | Gefuehl = Realitaet | "Ich fuehle mich dumm, also bin ich dumm" |
| Sollte/Muss-Denken | Starre Regeln | "Ich muesste das koennen" |
| Personalisierung | Alles auf sich beziehen | "Der schlechte Auftrag war meine Schuld" |

---

## 4. Gedanken hinterfragen (Sokratisches Fragen)

**Ziel:** Gedanken nicht direkt widerlegen, sondern Pruefung anregen.

**Fragen-Set:**

1. **Beweise pruefen:**
   - "Welche Beweise gibt es dafuer?"
   - "Welche Beweise sprechen dagegen?"

2. **Alternative Erklaerungen:**
   - "Gibt es andere Erklaerungen dafuer?"
   - "Wie wuerde jemand anderes diese Situation sehen?"

3. **Konsequenzen einschaetzen:**
   - "Was ist das Schlimmste, was passieren koennte? Wie wahrscheinlich ist das?"
   - "Was ist das Beste, was passieren koennte?"
   - "Was ist das Realistischste?"

4. **Nuetzlichkeit pruefen:**
   - "Hilft mir dieser Gedanke dabei, meine Ziele zu erreichen?"
   - "Was wuerde ich einem guten Freund sagen, der so denkt?"

---

## 5. Kognitive Umstrukturierung Schritt-fuer-Schritt

### Protokoll-Format (Gedankenprotokoll)

```
SITUATION
Was ist passiert? (Wann? Wo? Wer war dabei?)
[Freitext]

GEDANKE
Was bin ich dadurch durch den Kopf gegangen?
Automatischer Gedanke: [...]
Glaube ich daran? (0-100%): [...]%

EMOTION
Welche Emotionen hatte ich?
Emotion: [...]    Intensitaet (0-100%): [...]%

DENKFEHLER
Welche kognitiven Verzerrungen stecken darin?
[Liste aus Tabelle oben]

PRUEFEN
Beweise dafuer: [...]
Beweise dagegen: [...]
Alternative Sichtweise: [...]

ALTERNATIVER GEDANKE
Ausgewogener, realistischerer Gedanke:
[...]
Glaube ich daran? (0-100%): [...]%

ERGEBNIS
Emotion danach: [...]   Intensitaet: [...]%
Was nehme ich mit: [...]
```

---

## 6. Verhaltensaktivierung

**Zusatz zu kognitiver Arbeit:** Verhalten veraendern unterstuetzt Gedanken-Veraenderung.

**Prinzip:** Positive Aktivitaeten -> Bessere Stimmung -> Hilfreichere Gedanken

**Schritte:**
1. Liste angenehmer/bedeutungsvoller Aktivitaeten erstellen
2. Aktivitaeten planen (konkret: wann, wie, wo)
3. Umsetzung tracken
4. Stimmung vor/nach bewerten

**Beispiel-Aktivitaeten:**
- Spaziergang (Natur, frische Luft)
- Kontakt zu wichtigen Menschen
- Kreative Taetigkeiten
- Koerperliche Bewegung
- Dinge, die frueher Freude gemacht haben

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Kognitive Verzerrungen und das ABC-Modell erklaeren
- Sokratische Fragen stellen
- Gedankenprotokolle anleiten
- Psychoedukativ ueber KVT-Techniken informieren

**Ein KI-Assistent darf NICHT:**
- Professionelle kognitive Verhaltenstherapie ersetzen
- Diagnosen stellen oder Behandlungsempfehlungen geben
- Krisenintervention durchfuehren
- EMDR, Prolonged Exposure (PE) oder Narrative Exposure Therapy (NET) anwenden

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Quellenangaben

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: Beck (1979), Ellis (1962) — Keine professionelle Therapie*
