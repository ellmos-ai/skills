# Textproduction › storys — Narrative Texte

> Teilskill von `textproduction`. Router: `../SKILL.md`.
>
> Formate: Skript/Drehbuch, Kurzgeschichte, RPG-Abenteuer + Character Sheet,
> Weltenbau. Bildgenerierung fuer Visualisierungen optional (Cloud-Dienste).

---

## Trigger

| Nutzerwunsch | Muster |
|---|---|
| „Schreib ein Drehbuch / Skript" | Muster 1 |
| „Kurzgeschichte ueber [THEMA]" | Muster 2 |
| „RPG-Abenteuer erstellen", „Character Sheet" | Muster 3 |
| „Weltenbau fuer [SETTING]" | Muster 4 |
| „Bild generieren fuer [CHARAKTER/ORT]" | Muster 5 (optional, Cloud) |

---

## 1. Skript / Drehbuch

### Struktur

Ein Drehbuch hat feste Konventionen (Szenen-Heading, Aktion, Dialog, Charakter-Zeile).

```
Prompt-Muster:
"Schreibe ein Drehbuch-Excerpt im Branchenformat (Screenwriting-Konvention).

 Genre: [Drama / Komoedie / Thriller / Sci-Fi / ...]
 Szene: [Beschreibung der Situation]
 Charaktere: [Name + 1 Satz Charakter-Beschreibung]
 Ziel der Szene: [Konflikt, Wendung, Exposition]
 Laenge: ca. [X] Seiten (1 Seite ≈ 1 Minute Laufzeit)"

Beispiel-Output-Format:
INT. CAFÉ - TAG

ANNA (28, Biologin, erschoepft) starrt auf ihren Laptop.
Ein Anruf. Sie ignoriert ihn. Zweiter Anruf.

                    ANNA
          Das kann warten.

Sie legt das Handy um. Dritter Anruf. Sie seufzt.
```

### Revisions-Prompts

- "Schaerfe den Dialog in Szene 2 — Anna soll direkter und weniger zoeglich wirken."
- "Fuege eine Wendung am Ende der Szene ein."
- "Schreibe die Szene aus der Perspektive von Markus um."

---

## 2. Kurzgeschichte

```
Prompt-Muster:
"Schreibe eine Kurzgeschichte.

 Genre: [Literarisch / Krimi / Fantasy / Sci-Fi / Horror / ...]
 Hauptfigur: [Name, Alter, praegend Merkmal]
 Setting: [Ort, Zeitraum, Atmosphaere]
 Konflikt: [was treibt die Geschichte an?]
 Erzaehlperspektive: [Ich-Erzaehler / Auktorial / Nah 3. Person]
 Tonalitaet: [dunkel / humorvoll / melancholisch / spannungsgeladen]
 Laenge: ca. [X] Woerter
 Ende: [offen / abgeschlossen / Wendung]"
```

---

## 3. RPG-Abenteuer

### Session-Abenteuer

```
Prompt-Muster:
"Erstelle ein RPG-Abenteuer fuer [SYSTEM: D&D 5e / Pathfinder / generisch].

 Spielercharaktere: [Anzahl + Level]
 Setting: [Welt/Region, Epoche]
 Hauptplot: [1-2 Saetze: Was ist das zentrale Ziel/Problem?]

 Struktur:
 - Einstiegs-Hook (wie kommen die Spieler ins Abenteuer?)
 - Akt 1 — Erkundung: [Location, NPCs, erste Hinweise]
 - Akt 2 — Eskalation: [Wendung, Konflikt, optionaler Dungeon/Encounter]
 - Akt 3 — Finale: [Boss/Enthuellung, moegliche Enden]

 Zusaetzlich: 3 Encounter-Tabellen (Random-Events, Schatz, NPCs)"
```

### Character Sheet (Hintergrundgeschichte)

```
Prompt-Muster:
"Schreibe eine Hintergrundgeschichte fuer einen RPG-Charakter.

 Name: [NAME]
 Rasse/Klasse: [z.B. Halbling-Schurke]
 Motivation: [Was will der Charakter? Warum abenteuernd?]
 Dunkles Geheimnis: [optional]
 Pragende Erfahrung: [Schluesselmoment der Kindheit/Jugend]
 Aktuelles Ziel: [kurzfristig]
 Langfristiger Wunsch: [der tiefste Antrieb]
 Ton: [ernst / tragisch / komödiantisch]"
```

---

## 4. Weltenbau

```
Prompt-Muster:
"Entwickle ein Weltenbau-Dokument fuer [NAME DER WELT/SETTING].

 Abschnitte:
 1. Geographie & Klima (2-3 Saetze je Region)
 2. Geschichte (3 praegende Epochen, je 1 Absatz)
 3. Voelker & Kulturen (3-5 Voelker mit Kurzprofil)
 4. Magie / Technologie (Regeln, Grenzen, Risiken)
 5. Wichtige Orte (5 Orte mit Namen + 2-3 Saetzen)
 6. Aktuelle politische Lage (Konflikte, Allianzen)"
```

---

## 5. Bildgenerierung zur Visualisierung (optional) ☁️

Charaktere, Orte, Szenen visualisieren:

### Midjourney ☁️ (midjourney.com)

```
/imagine [SUBJEKT], [STIL], [DETAILTIEFE], [BELEUCHTUNG], [PERSPEKTIVE]

Beispiele:
/imagine a weathered elven cartographer in a cluttered map room,
         detailed oil painting, warm candlelight, close-up portrait --ar 2:3

/imagine ancient forest temple overgrown with vines, fantasy concept art,
         dramatic lighting, wide establishing shot --ar 16:9 --style raw
```

### Ideogram ☁️ (ideogram.ai) — Staerke: Text im Bild

```
Prompt + Negative Prompt + Style waehlen
Fuer Karten, Plakate, Titelbilder mit Text besonders geeignet
```

---

## Qualitaetscheck

- **Konsistenz:** Charakternamen, Ortsnamen, Zeitangaben im Text einheitlich?
- **Tempo:** Szene zu langsam/zu schnell? Ggf. kuerzen oder ausbauen.
- **Originalitaet:** Klischees identifizieren und gezielt brechen oder bewusst einsetzen.
- **Lesbarkeit:** Dialoge laut vorlesen — klingt es natuerlich?
