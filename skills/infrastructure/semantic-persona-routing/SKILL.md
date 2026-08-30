---
name: semantic-persona-routing
version: 1.0.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-28
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
tags: [persona, semantic-routing, agents, experts, skills, umbrella, provider-neutral]
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

Stufe `candidate_skills` nicht automatisch hoch. Bestätige sie zuerst über
einen aktiven Skill-Resolver oder Quellmetadaten.

## Eine Anfrage routen

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

### 1.0.0 (2026-07-28)

- Die anbieterneutrale Rollen-, Experten- und Skill-Kette aus einem bewährten
  Domänen-Router extrahiert und portable Kartenerstellung mit sichtbaren
  Endpunktlücken ergänzt.
