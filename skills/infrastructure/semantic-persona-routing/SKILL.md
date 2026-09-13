---
name: semantic-persona-routing
version: 1.1.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-09-03
description: >
  Erstellt und verwendet einen anbieterneutralen semantischen Routing-Graphen
  aus Personas, koordinierenden Rollen, Experten und aktiven Skill-Endpunkten.
  Verwenden, wenn ein LLM eine Anfrage von einer Leitrolle über einen Experten
  zu einem Skill routen, aus einem vorhandenen Agentensystem einen portablen
  Persona-Router extrahieren, eine semantische Domänenkarte mit einer
  lexikalischen Skill-Registry kombinieren oder fehlende Verbindungen zwischen
  Rolle und Skill sichtbar machen soll, statt still auf einen Ersatz
  zurückzufallen. Auslöser sind unter anderem semantisches Persona-Routing,
  Persona-Umbrella, Rollen-Router, Boss-Agent-Experten-Skill-Routing,
  Agentenrollen-Export oder die Wiederverwendung von Personas über mehrere
  LLM-Anbieter hinweg.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [persona, persona-authoring, semantic-routing, agents, experts, skills, umbrella, provider-neutral]
language: de
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="semantic-persona-routing banner">

# Semantisches Persona-Routing

Route zuerst nach Fähigkeit und wende Persönlichkeit danach an. Erstelle eine
portable Karte, die semantische Rollenwahl, deterministische Endpunktsuche und
anbieterspezifisches Laden voneinander trennt.

## Routing-Modell

```text
Anfrage
  -> semantische Domäne oder koordinierende Rolle
  -> Expertenfähigkeit
  -> ausdrücklich angegebener oder live aufgelöster Skill-Endpunkt
  -> optionales Persona-Overlay
  -> Anbieteradapter lädt und führt aus
```

Eine Persona steuert Kommunikationsstil, Prioritäten und Interaktionsmuster. Sie
verleiht keine Werkzeuge, Berechtigungen oder fachlichen Fähigkeiten. Eine Rolle
koordiniert, ein Experte grenzt die Domäne ein, und ein Skill ist der
ausführbare Endpunkt.

## Routing-Karte erstellen

Nutze ausdrückliche Metadaten als maßgebliche Quelle und lexikalische Ähnlichkeit
nur zur Kandidatensuche:

```bash
python scripts/build_routing_map.py \
  --roles-dir path/to/roles \
  --personas-dir path/to/personas \
  --skills-dir path/to/skills \
  --out routing-map.json
```

Der Builder versteht verbreitete `SKILL.md`-Felder wie `type`,
`orchestrates.experts`, `parent_agents`, `skills`, Beschreibungen und Herkunft.
Er erzeugt eine Laufzeitkarte, ohne dass das Quellsystem installiert sein muss.
Lies [routing-map-schema.md](references/routing-map-schema.md), bevor du das
Format erweiterst.

Jede exportierte Skill-ID ist eindeutig. Deklarieren mehrere Quelldateien dieselbe
stabile ID, wählt der Builder deterministisch den lexikografisch ersten relativen
Quellpfad und vermerkt ein `duplicate-skill-id`-Issue; er gibt nie zwei
Skill-Einträge mit derselben ID aus. Deklarierte Experten- und Persona-Skill-Verweise
werden nur dann auf eine bereinigte ID normalisiert, wenn diese ID in der
exportierten Registry existiert. Fehlerhafte, unbekannte und normalisierte Verweise
bleiben in `issues` sichtbar; unbekannte oder ungültige Verweise werden nie zu
Endpunkten oder Persona-Kompatibilitätslinks.

Stufe `candidate_skills` nicht automatisch hoch. Bestätige sie zuerst über
einen aktiven Skill-Resolver oder Quellmetadaten.

## Personas anlegen und ablegen

Der Kern erzeugt Karten, er erfindet keine Personas. Wer eigene Personas nutzen
will, legt sie **neben dem Skill** ab und baut die Karte neu:

```text
semantic-persona-routing/
  personas/<persona-id>.md          # eine Datei je Persona
  roles/<rolle>/SKILL.md            # koordinierende Rollen und Experten
  routing-map.json                  # erzeugte Karte
  config.json                       # host-lokal, nie veröffentlicht
```

Rollen liest der Builder ausschließlich aus `SKILL.md`-Dateien; Personas aus
jeder Markdown-Datei mit Frontmatter. Kopiere
[templates/persona.template.md](templates/persona.template.md) nach
`personas/<persona-id>.md` und fülle den Vertrag aus:

| Feld | Bedeutung |
|---|---|
| `name`, `type: persona` | stabile Persona-ID und Typ |
| `persona.display_name`, `short_name`, `gender`, `role`, `default_prompt` | Anzeige, Kurzname, Anrede, Rolle in einem Satz, Aufrufsatz des Anbieters |
| `parent_agents` | koordinierende Rollen, denen die Persona zugeordnet ist |
| `skills` | **Skill-Namen, nie Pfade** — nur diese werden zu Endpunkten aufgelöst |
| `optional_skills` | host-gebundene Skills; fehlen sie, bleiben sie eine sichtbare `GAP` |

Eine Persona darf Werkzeuge, Berechtigungen und Sicherheits-, Sperr- oder
Nutzerentscheidungen weder verleihen noch überschreiben; sie ist ein Overlay
über Rolle und Skills.

**Pfade:** Der Skill nennt keine Hostpfade. `config.example.json` zeigt das
Muster (`ellmos.skill-config.v1`, `einstellungen.paths` mit Platzhaltern wie
`<HOME>/<ONEDRIVE>/<TOPICS>`); die host-lokale Kopie heißt `config.json`,
wird beim Deploy bewahrt und nie ins Repository übernommen.

**Katalog bereinigen:** Eine Skill-Bibliothek mit Archiven oder Referenzkopien
erzeugt viele `duplicate-skill-id`-Issues. `--skills-layout catalog` nimmt nur
`<kategorie>/<name>/SKILL.md` und überspringt Ordner mit `_`-Präfix
(`_archive`, `_reference`, `_templates`):

```bash
python scripts/build_routing_map.py \
  --roles-dir roles --personas-dir personas \
  --skills-dir path/to/skills --skills-layout catalog \
  --out routing-map.json
```

## Eine Anfrage routen

### 0. Vorhandene Personas anbieten

Liegen Personas neben dem Skill (`personas/`), liste sie beim Aufruf mit
Anzeigename, Rolle und Skills auf und route zur passenden; nennt die Anfrage
keine Persona, wähle sie erst in Schritt 4. Das Format des Routing-Belegs bleibt
unverändert.

### 1. Koordinierende Rolle semantisch wählen

Vergleiche die Anfrage mit Rollennamen, Beschreibungen und Anwendungsfällen.
Bevorzuge die engste Rolle, die die gesamte Anfrage koordinieren kann. Halte bei
geringer Sicherheit mehrere Kandidaten sichtbar; frage den Nutzer nur, wenn die
Wahl das Ergebnis wesentlich verändert.

### 2. Experten innerhalb der Rolle wählen

Nutze nur Experten, die mit der gewählten koordinierenden Rolle verbunden sind,
sofern die Anfrage nicht eindeutig mehrere Rollen umfasst. Eine direkte
Expertenanfrage darf die koordinierende Rolle bei der Ausführung überspringen,
behält deren Verbindung aber in der Routenerklärung bei.

### 3. Ausführbare Endpunkte auflösen

Löse in dieser Reihenfolge auf:

1. `endpoint_skills` aus ausdrücklichen Quellmetadaten oder exakter Herkunft;
2. einen aktuellen externen Skill-Resolver oder lokalen Skill-Finder;
3. verifizierte `candidate_skills`;
4. eine sichtbare `GAP`, wenn kein Endpunkt existiert.

Route niemals zu einem Expertennamen, als wäre er ein installierter Skill. Ein
fehlender Endpunkt ist eine Portierungslücke und keine Erlaubnis, einen Endpunkt
zu erfinden.

Lies [endpoint-resolution.md](references/endpoint-resolution.md), wenn du eine
aktive Registry, einen lexikalischen Finder oder einen anbieterspezifischen
Skill-Loader anschließt.

### 4. Persona-Overlay anwenden

Wähle eine Persona, die der ausgewählten Rolle oder dem Experten zugeordnet ist.
Wenn mehrere Personas passen, bevorzuge eine, deren erklärte Grenzen und Stil
zur Aufgabe passen. Wende keine Persona an, wenn keine ausdrücklich verbunden
ist.

Persona-Anweisungen dürfen Sicherheitsregeln, Sperren, Nutzerentscheidungen,
berufliche Grenzen oder Werkzeugberechtigungen nicht überschreiben.

### 5. Laden und ausführen

Nutze den nativen Skill- oder Agentenlademechanismus des Anbieters. Lade vor der
Ausführung die ausgewählten aktiven Skill-Anweisungen. Halte den Router schlank;
die Ausführung gehört zum Worker oder zum aktuellen Agenten mit den geladenen
Skills.

## Routing-Beleg

Gib Folgendes zurück oder zeichne es auf:

```text
ROLE: <koordinierende Rolle oder direct>
EXPERT: <Experte oder n/a>
SKILLS: <verifizierte aktive Endpunkte>
PERSONA: <Overlay oder none>
RESOLUTION: explicit | provenance | live-resolver | verified-candidate | GAP
CONFIDENCE: high | medium | low
WHY: <ein kurzer Grund>
GAPS: <fehlende Endpunkte oder Warnungen vor veralteten Karten>
```

Erstelle die Karte neu, wenn sich Quellrollen oder Skill-Bestand ändern. Ein
aktiver Resolver darf eine veraltete Karte hinsichtlich der
Endpunktverfügbarkeit überstimmen, aber die semantische Rollentaxonomie nicht
stillschweigend umschreiben.

## Beispiel

Anfrage: „Ordne meine Belege und bereite die Übersicht für das Steuerjahr vor.“

Der Router wählt eine Büro-Koordination, danach den Steuerexperten, löst den
installierten Steuer-Skill auf und wendet schließlich eine ausdrücklich
verknüpfte, sorgfältige Steuer-Persona an. Existiert der Steuerexperte, aber
kein portabler Steuer-Skill, meldet er `GAP` und fährt nur über einen
ausdrücklich konfigurierten Ersatzweg fort.

## Änderungsprotokoll

### 1.1.0 (2026-09-03)

- Personas anlegen und ablegen: Ablagekonvention neben dem Skill, Frontmatter-
  Vertrag, neutrale Vorlage `templates/persona.template.md`, Pfad-Konvention mit
  `config.example.json`, Aufruf-Verhalten (vorhandene Personas anbieten) und
  `--skills-layout catalog` gegen doppelte Skill-IDs aus Archiv- und Referenzkopien.

### 1.0.0 (2026-07-28)

- Die anbieterneutrale Rollen-, Experten- und Skill-Kette aus einem bewährten
  Domänen-Router extrahiert und portable Kartenerstellung mit sichtbaren
  Endpunktlücken ergänzt.
