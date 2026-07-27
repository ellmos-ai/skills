---
name: agents-bridge
version: 2.0.0
type: skill
author: ellmos-ai contributors
created: 2026-05-16
updated: 2026-07-27
description: >
  Anbieter- und nutzerneutrale Brücke zwischen Agenten, CLIs und IDEs. Entdeckt
  vorhandene Bootstrap-Konventionen, lässt den Nutzer eine oder mehrere
  Wahrheitsquellen und ihre Reihenfolge festlegen und erzeugt daraus kleine
  Loader- oder Redirect-Dateien ohne Regelkopien. Verwenden, wenn AGENTS.md,
  CLAUDE.md, GEMINI.md, Copilot-, Cursor-, Aider- oder andere Agent-Regeln
  verbunden werden sollen.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [multi-agent, bootstrap, rules, agents-md, provider-neutral]
language: de
status: active

dependencies:
  tools: [python]
  services: []
  protocols: [agent-config-sync]
  python: []

provenance:
  origin: "custom"
  origin_path: "skills/infrastructure/agents-bridge/"
  origin_version: "1.1.0"
  last_sync_from_origin: "2026-07-27"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# AGENTS-BRIDGE

Dieser Skill verbindet die Boot-Dateien verschiedener Agenten, ohne einen
bestimmten Anbieter, Dateinamen, Rechner oder Cloud-Ordner zur Wahrheit zu
erklären.

## Grundsatz

Die Nutzerin oder der Nutzer bestimmt:

1. welche Datei oder geordnete Dateimenge die Wahrheit bildet,
2. welches Zielsystem diese Regeln laden soll,
3. ob ein Redirect, ein geordneter Loader oder eine bewusst gepflegte Kopie
   gebraucht wird,
4. ob und wann geschrieben werden darf.

`CLAUDE.md`, `AGENTS.md`, `GEMINI.md` oder andere Regeldateien sind gleichwertige
Kandidaten. Ein bestehendes persönliches Profil darf eine konkrete Auswahl
enthalten; diese Auswahl gehört nicht in den portablen Skill.

```text
explizit gewählte Wahrheitsquellen
       │
       ├── Redirect, wenn das Ziel Verweise versteht
       ├── geordneter Loader, wenn mehrere Dateien gelesen werden müssen
       └── generierte Kopie nur mit Drift- und Herkunftskennzeichnung
                     │
        Agent / CLI / IDE / App-Klasse
```

## Pflichtablauf

1. **Lokale Regeln zuerst lesen.** Vor Änderungen die für Quell- und Zielpfad
   geltenden `AGENTS.md`, `CLAUDE.md` oder vergleichbaren Anweisungen prüfen.
2. **Möglichkeiten entdecken.**

   ```powershell
   python scripts/bridge.py discover
   python scripts/bridge.py discover --project C:\Pfad\zum\Projekt
   ```

   Das Ergebnis ist ein Inventar bekannter Boot-Flächen, keine Entscheidung.
3. **Wahrheit erfragen oder aus einem ausdrücklich gewählten Profil lesen.**
   Leere Auswahl bedeutet keine Autorisierung. Mehrere Dateien sind erlaubt und
   werden in angegebener Reihenfolge behandelt.
4. **Topologie anbieten.** Bevorzuge Redirect oder Loader. Eine Kopie ist nur
   sinnvoll, wenn das Ziel keine Verweise laden kann; dann müssen Herkunft,
   Generierungszeitpunkt und Driftprüfung dokumentiert werden.
5. **Loader vorschauen.**

   ```powershell
   python scripts/bridge.py render `
     --truth C:\rules\AGENTS.md `
     --truth C:\rules\team.md `
     --target-kind codex
   ```

   `render` schreibt nicht; die Ausgabe wird erst nach Prüfung am explizit
   gewählten Ziel angelegt.
6. **Lesetest durchführen.** Das Zielsystem muss nachweisbar eine kleine,
   ungefährliche Regel aus jeder Quelle wiedergeben können.
7. **Inventar und Bericht aktualisieren.** Nur das vom Nutzer bestimmte
   Inventar verwenden. Es gibt keinen impliziten `.SYNC`-, OneDrive- oder
   ControlCenter-Pfad.

## Auswahl der Topologie

| Situation | Empfehlung |
|---|---|
| Eine Wahrheit, Ziel kann Dateien referenzieren | kleiner Redirect |
| Mehrere geordnete Wahrheitsdateien | Loader mit nummerierter Lesereihenfolge |
| Ziel unterstützt nur eingebetteten Text | generierte Kopie mit Provenienz und Driftprüfung |
| Regeln sollen in beide Richtungen bearbeitet werden | zuerst Konflikt- und Ownership-Modell festlegen |
| Noch keine Wahrheit ausgewählt | nur Discovery und Angebot, keine Mutation |

Siehe `references/truth-topologies.md`.

## Verhältnis zu anderen Komponenten

- `agent-config-sync` entdeckt und plant Sync-Topologien für MCPs, Skills und
  Regeldateien. Es kann das hier beschriebene Wahrheitsprofil referenzieren.
- `mcp-config-sync` ist der MCP-spezifische Einstieg zu `agent-config-sync`.
- `agents-bridge` erzeugt nur den Boot-/Regelzugang eines Zielagenten.
- Ein gleichnamiges Laufzeitmodul wie `ellmos-agent-bridge` kann Heartbeats oder
  Partnernachrichten transportieren; es ist nicht automatisch die
  Regel-Wahrheit und nicht Bestandteil dieses Skills.

## Sicherheits- und Driftregeln

- Keine unbekannte vorhandene Boot-Datei überschreiben.
- Vor jeder Mutation Quelle, Ziel, Richtung und Strategie ausgeben.
- Keine Secrets, Tokens oder vollständige Anbieter-Konfigurationen in Loader
  aufnehmen.
- Absolute persönliche Pfade nur in lokalen Profilen speichern.
- Symlinks nur verwenden, wenn Plattform, Berechtigungen und Zieltool sie
  nachweisbar unterstützen.
- Bei mehreren editierbaren Quellen nie still eine Priorität erfinden.

## Mitgelieferte Dateien

```text
agents-bridge/
├── SKILL.md
├── SKILL.en.md
├── scripts/
│   └── bridge.py
├── tests/
│   └── test_bridge.py
├── references/
│   ├── agent-conventions.md
│   ├── truth-topologies.md
│   └── inventory-contract.md
└── assets/
    ├── AGENTS.md.template
    └── bridge-profile.example.json
```
