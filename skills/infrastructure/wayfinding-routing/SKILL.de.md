---
name: wayfinding-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  Universeller Skill für LLM-Navigation, Orientierung und
  Ausfallsicherheit. Stellt aktives Wayfinding, Selbstorientierung und
  Wiederherstellungsheuristiken bereit, wenn Agenten mit Kontextdrift,
  fehlschlagenden Werkzeugen, Schleifen oder Sackgassen konfrontiert sind.
  Enthält die synonymen Strategien survival-routing, dead-reckoning,
  pathfinder-routing und celestial-routing.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, self-orientation, resilience, recovery, heuristics]
language: de
status: active
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
---

<img src="banner.png" width="100%" alt="wayfinding-routing banner">

# Wayfinding-Routing (Selbstorientierungs- und Notfall-Fallback-Engine)

Der Skill **Wayfinding-Routing**, auch bekannt als **`survival-routing`**,
**`dead-reckoning`**, **`pathfinder-routing`** und **`celestial-routing`**,
dient LLM-Agenten als verbindlicher Rahmen für Navigation und
Notfallwiederherstellung.

Er stattet Agenten mit proaktiven Wayfinding-Heuristiken für die normale
Ausführung und mit Notfallprotokollen für Kontextdrift, wiederkehrende
Ausführungsfehler, ausfallende APIs oder Sackgassen aus.

---

## Übersicht der Synonyme und Strategien

| Synonyme Strategie | Metapher und Kernprinzip | Anwendungsfall |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (primär) | **Wayfinding / räumliche Orientierung:** Navigation ohne externes GPS durch Wegweiser und Umgebungshinweise. | Primärer Navigationsregelkreis für Sidecars, `workflowhooker` und `automation-self-care`. |
| **`survival-routing`** | **Notfall-Fallback und Selbsterhalt:** Circuit-Breaking und kontrollierte Degradation, wenn Werkzeuge ausfallen oder Schleifen entstehen. | Notfallwiederherstellung bei Timeouts, wiederholten Fehlern oder Berechtigungsgrenzen. |
| **`dead-reckoning`** | **Nautische Koppelnavigation:** Exakten Zustand aus schrittweisen Brotkrumen ohne externe Statusquelle rekonstruieren. | Ausführungsschritte in Scratch-Dateien oder `TODO.md` verfolgen, um präzise zurückzugehen. |
| **`pathfinder-routing`** | **Pfadfinder und Vorauskommando:** Wege für Multi-Agenten-Teams vorab prüfen und vorbereiten. | Preflight-Prüfung von Verzeichnisbäumen, Sperren und Aufgabenabhängigkeiten. |
| **`celestial-routing`** | **Astronavigation:** An unveränderlichen Nordstern-Ankerdokumenten ausrichten, wenn lokaler Kontext verrauscht ist. | Rückfall auf `CLAUDE.md`, `AGENTS.md` und `START.md`, wenn Prompt-Anweisungen widersprüchlich sind. |

---

## Die fünf zentralen Notfall- und Orientierungsprotokolle

### 1. `PROTOCOL-ANCHOR-RESET` (Nordstern-Fallback / Celestial Routing)

- **Auslöser:** Kontextdrift, widersprüchliche Nutzeranweisungen oder
  Orientierungsverlust in langen Sitzungen mit vielen Turns.
- **Heuristische Regel:** Freie Texterzeugung anhalten. Flüchtige Annahmen
  verwerfen. Root-Ankerdokumente (`CLAUDE.md`, `AGENTS.md`, `START.md`) erneut
  lesen. Den Zielzustand vor weiteren Aktionen auf die maßgebliche
  Root-Anweisung zurücksetzen.

### 2. `PROTOCOL-STOP-EXPLAIN` (Rubber-Duck-Reflexionsschleife)

- **Auslöser:** Ein Terminalbefehl, eine Dateiänderung oder eine API-Anfrage
  schlägt zweimal mit demselben Fehler fehl.
- **Heuristische Regel:** **Befehlsausführung sperren.** Vor dem dritten Versuch
  muss der Agent eine formale Selbstreflexion ausgeben:
  1. *Welcher genaue Fehler trat in Versuch 1 und 2 auf?*
  2. *Warum scheiterte die vorherige Diagnosehypothese?*
  3. *Welcher neue alternative Ansatz wird gewählt?*
  Die Ausführung wird erst nach dieser ausdrücklichen Begründung entsperrt.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (mehrstufige Fallback-Kaskade)

- **Auslöser:** Primäres Werkzeug, MCP-Server oder externe API ist nicht
  verfügbar oder liefert Fehler.
- **Heuristische Regel:** Niemals abrupt scheitern oder blind schleifen.
  Stufenweise degradieren:
  - **Stufe 1 (optimal):** vollständige native API oder MCP-Werkzeug
  - **Stufe 2 (Ersatzwerkzeug):** lokale Python-CLI oder Skript
  - **Stufe 3 (Nur-Lese-Zustand):** direkte Dateiauswertung
    (`view_file` oder Rohtext)
  - **Stufe 4 (Übergabe):** strukturierten Statusbericht und offene Optionen
    für den Nutzer darstellen.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead Reckoning und Sackgassenerkennung)

- **Auslöser:** Ein komplexer mehrstufiger Refactoring- oder Workflow-Pfad
  stößt in Schritt N auf eine unauflösbare Blockade.
- **Heuristische Regel:** Vor zerstörerischen Änderungen Brotkrumen
  aufzeichnen. Scheitert ein Pfad:
  1. Nicht eingecheckte Änderungen zurücknehmen und Zustand wiederherstellen.
  2. Zum letzten sauberen Brotkrumen-Checkpoint zurückspringen.
  3. Die fehlgeschlagene Route in `TODO.md` als blockiert markieren.
  4. Alternativen Pfad B versuchen.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Notaus und sicherer Ausstieg)

- **Auslöser:** Ausführungslimit erreicht, Endlosschleife erkannt oder
  kritischer Systemsperrfehler.
- **Heuristische Regel:** Notabschaltung ausführen:
  1. Alle selbst erworbenen Datei- und Git-Sperren freigeben
     (`python -m workflowhooker check`).
  2. Aktuellen Teilzustand in `.SYNC/SURVIVAL_STATE.json` oder
     `AUTOMATIONS-MEMORY.md` speichern.
  3. Vorfall in `ANTIGRAVITY-LOG.txt` protokollieren.
  4. Mit einer umsetzbaren Zusammenfassung für Nutzer oder Orchestrator sauber
     beenden.

---

## Integration mit `automation-self-care` und `workflowhooker`

`wayfinding-routing` liefert die zugrunde liegende Navigationslogik für:

- **`automation-self-care`**: Prüft Sidecar-Prompts anhand der fünf Protokolle
  auf Selbstheilungsfähigkeit.
- **`workflowhooker`**: Liefert Standardheuristiken für schrittweise
  Sperrprüfung und Brotkrumenprotokollierung.
- **`staircase-routing`**: Nutzt `PROTOCOL-ANCHOR-RESET` für vertikale
  Verzeichnisnavigation.
