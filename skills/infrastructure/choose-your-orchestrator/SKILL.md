---
name: choose-your-orchestrator
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-08-20
description: >
  Wählt vor komplexer Multi-Agent-Arbeit gemeinsam mit dem Nutzer eine passende,
  begrenzte Orchestrierung und erzeugt einen kompakten Session-Vertrag. Nutze den
  Skill bei /choose-your-orchestrator, bei unsicherer Kombination aus Orchestrator,
  Schwarm, Modellrouting oder Nutzerpräferenzmodell sowie vor Agentenprogrammen,
  die Modellslots, Parallelität, Spawn-Tiefe, Schreibgrenzen, Abnahme und
  Eskalation ausdrücklich festlegen müssen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Choose Your Orchestrator

## Zweck

Kläre vor komplexer Multi-Agent-Arbeit die Randbedingungen, empfehle die kleinste
wirksame Kombination vorhandener Skills und gib einen verbindlichen
Session-Orchestrierungsvertrag aus. Lade die ausgewählten Skills über den
Skill-Mechanismus der aktuellen Runtime und folge ihren Live-Anleitungen. Kopiere
ihre Verfahren nicht in diesen Skill.

Delegation erweitert niemals die Autorität. Externe oder irreversible Aktionen wie
Veröffentlichen, Senden, Löschen, Bezahlen oder produktive Änderungen bleiben beim
Nutzer gegatet, sofern der aktuelle Auftrag sie nicht ausdrücklich autorisiert.

## Bausteine

| Baustein | Aufgabe im Vertrag | Nicht seine Aufgabe |
|---|---|---|
| `orchestrator` | Arbeitspakete, Scopes, Evidenz und Abnahme | Modellwahl oder Schwarmmuster erfinden |
| `swarm-operations` | Schwarmmuster, Kosten-Gate und optionale Matruschka-Staffelung | Einzelaufgaben künstlich parallelisieren |
| `model-strategy` | Fähigkeits- und modellbezogene Route anhand der Live-Verfügbarkeit | feste Modellversionen oder Berechtigungen vorgeben |
| `clutch` | optionaler externer Routingvorschlag | alleinige Autorität für Dispatch oder Scope |
| `decision-avatar` | optionales autorisiertes Präferenzsignal bei reversiblen Unsicherheiten | Nutzerfreigaben ersetzen oder Autorität erweitern |

Nutze `clutch route "<kurze Aufgabenbeschreibung>" --json` nur, wenn `clutch`
tatsächlich verfügbar ist. Behandle die JSON-Antwort als Vorschlag und gleiche sie
gegen verfügbare Runtime-Slots, Budget, Projektregeln und Nutzergrenzen ab. Ist
`clutch` nicht verfügbar oder seine Ausgabe unlesbar, nutze `model-strategy` und
die Live-Fähigkeiten der Runtime. Hardcode keine aktuellen Modellnamen oder
-versionen in den Vertrag.

## Empfehlungsdialog

### 1. Aufgabe einordnen

Ermittle Ziel, Aufgabentyp, Erfolgskriterien, negative Scopes, aktuelle
Berechtigungen, vorhandene Locks und unabhängige Arbeitspakete. Wähle zunächst den
kleinsten passenden Routenvorschlag aus der Tabelle unten.

### 2. Vertrag vorschlagen

Zeige einen kompakten Entwurf mit:

1. Bausteinen und Rollen,
2. Modell-/Budgetslots,
3. maximaler Parallelität und Spawn-Tiefe,
4. Schreibgrenzen und Locks,
5. Abnahme und Evidenz,
6. Eskalation und Nutzerfragen,
7. Autoritätsgrenze.

Empfehle konkrete Werte und nenne in einem Satz den wichtigsten Trade-off. Frage
nur nach Entscheidungen, die das Ergebnis materiell ändern. Bündele offene Fragen
in höchstens drei klar getrennte Gruppen; stelle die empfohlene Option jeweils
zuerst. Sind alle Dimensionen bereits ausdrücklich festgelegt, frage nicht erneut.

### 3. Bestätigen oder reduzieren

Beginne keinen Multi-Agent-Dispatch, solange eine materielle Budget-, Schreib- oder
Autoritätsfrage offen ist. Ist nur der Nutzen von Parallelität unklar, reduziere auf
Einzelfahrt. Ein explizit autorisierter Auftrag darf mit den sicheren Defaults
starten, wenn keine materielle Nutzerentscheidung fehlt.

### 4. Vertrag ausgeben

Gib den bestätigten Vertrag im Chat aus. Ist ein `usmc`-Befehl verfügbar, prüfe
zuerst dessen Hilfe und schreibe zusätzlich über einen dort dokumentierten
Note-/Write-Befehl eine privacy-neutrale Session-Notiz. Erfinde keinen Subcommand
und speichere keine Rohprompts, Secrets oder privaten Inhalte. Ohne verfügbaren
USMC-Schreibweg ist der Chatvertrag autoritativ.

## Routingtabelle

| Aufgabentyp | Empfehlung | Default-Zuschnitt |
|---|---|---|
| Audit / Sweep | `orchestrator` + `swarm-operations`; `model-strategy` bei unterschiedlichen Fähigkeitsklassen | unabhängige Bereiche, kleine `parallel-chunks`- oder `specialist`-Gruppe, zentraler Merge |
| Bauprogramm | `orchestrator` + `model-strategy`; Schwarm nur für wirklich unabhängige Stränge | Chef plant und nimmt ab, Worker bauen in disjunkten Bereichen |
| Einzelbau | Einzelfahrt; optional `model-strategy` oder `clutch` für die Route | kein Schwarm- oder Hierarchie-Overhead |
| Ticket-Betrieb | Ticket-System bleibt führend; `orchestrator` ergänzt Arbeitsverträge und Evidenz | vorhandenes Router-/Score-Regime nicht ersetzen, Ticket-Lifecycle respektieren |

## Sichere Defaults

Verwende diese Werte, sofern Nutzer, Runtime oder Projektregeln nichts Strengeres
vorgeben:

- maximal zwei aktive Worker; starte zunächst einen und belege den Nutzen des zweiten,
- Matruschka aus, maximale Spawn-Tiefe `0`,
- keine Worker-eigenen Subagenten ohne explizite Freigabe,
- ein Schreiber pro Repository oder klar abgegrenztem Bereich,
- disjunkte Datei-Claims und projektübliche Locks vor jedem Write,
- Chef/Orchestrator prüft Artefakte, Diffs und Tests selbst,
- Fertigmeldungen gelten erst nach Evidenzabnahme,
- irreversible oder externe Aktionen bleiben nutzergegatet,
- Unsicherheit wird gebündelt statt als viele Einzelunterbrechungen gemeldet.

Aktiviere Matruschka nur, wenn der Nutzer sie ausdrücklich bestätigt und der Vertrag
pro Ebene Modell-/Fähigkeitsklasse, aktive Slotgrenze, erlaubte Unteraufgaben und
maximale Tiefe nennt. Zähle aktive, nicht lediglich vorhandene Agenten. Auch dann
bleibt genau ein Schreiber pro Bereich bestehen.

## Vertragsformat

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## Beispiel

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## Stop-Bedingungen

Stoppe oder reduziere die Orchestrierung, wenn Scopes überlappen, Locks unklar sind,
die Runtime den empfohlenen Slot nicht anbietet, das Budget nicht bestätigt ist oder
die Abnahme nicht unabhängig belegt werden kann. Frage den Nutzer statt eine neue
Produkt-, Datenschutz- oder Autoritätsentscheidung zu erraten.

## Changelog

### 1.0.0 (2026-08-20)
- Empfehlungsdialog, Routentabelle und kompakter Session-Vertrag eingeführt.
- Sichere Defaults für Parallelität, Matruschka, Schreibgrenzen, Evidenz und
  externe Aktionen festgelegt.
- Optionale Integration von `clutch` und einem autorisierten Präferenzmodell ohne feste Modellbindung oder
  Autoritätserweiterung beschrieben.
