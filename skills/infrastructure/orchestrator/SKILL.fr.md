---
name: orchestrator
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: [Français] Compétence d'agent pour orchestrator: Providerneutrales Protokoll zum Zerlegen komplexer Aufgaben, zum Beauftragen unabhängiger Worker und zur evidenzbasierten Abnahme ihrer Ergebnisse.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [orchestrierung, multi-agent, delegation, evidenz, checkpoint, workflow]
language: fr
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'local-agent-skills/orchestrator/', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **Version Officielle en Français** — Documentation complète traduite en français pour la compétence `orchestrator`.



> **English Translation** — Official English version of `orchestrator`.


# Orchestrator

## Zweck

Nutze diesen Skill, wenn eine Aufgabe aus mindestens zwei weitgehend unabhängigen
Arbeitspaketen besteht und Delegation einen echten Zeit-, Kontext- oder
Qualitätsvorteil bringt. Für kleine, eng gekoppelte Aufgaben arbeite direkt.

Der Skill beschreibt ein Protokoll. Das konkrete Starten, Unterbrechen und
Wiederaufnehmen von Workern erfolgt über die Fähigkeiten der jeweiligen Runtime.

## Autoritätsgrenze

Delegation erweitert keine Berechtigung. Jeder Worker erhält höchstens den Scope
und die Änderungsrechte, die für die Hauptaufgabe bereits gelten. Externe,
irreversible oder anderweitig freigabepflichtige Aktionen bleiben
freigabepflichtig.

## Ablauf

### 1. Lage prüfen

1. Ziel, Erfolgskriterien und Ausschlüsse der Hauptaufgabe festhalten.
2. Projektregeln, Sperren, laufende Änderungen und verfügbare Budgets prüfen.
3. Vor dem Dispatch den aktuellen Lock-, Status- und Diff-Zustand der betroffenen
   Bereiche als Baseline sichern. Nur so lassen sich vorhandene fremde Änderungen
   später zuverlässig von Worker-Änderungen unterscheiden.
4. Nur Arbeitspakete parallelisieren, die unabhängig genug sind.
5. Überschneidende Schreibbereiche trennen oder sequentiell bearbeiten.

### 2. Auftragsvertrag schreiben

Vor jedem Dispatch einen kurzen, prüfbaren Vertrag erstellen:

| Feld | Pflichtinhalt |
|---|---|
| Kennung | stabile ID des Arbeitspakets |
| Ziel | genau ein konkretes Ergebnis |
| Eingaben | relevante Dateien, Daten oder Kontextquellen |
| Positiver Scope | was gelesen oder geändert werden darf |
| Negativer Scope | was ausdrücklich unberührt bleibt |
| Erfolgskriterium | beobachtbare Bedingung für „fertig“ |
| Evidenz | erwarteter Nachweis, etwa Test, Diff oder Fundstelle |
| Rückgabeformat | kompakte, strukturierte Abschlussmeldung |

Ein Worker bekommt nur den Kontext, den er für diesen Vertrag benötigt.

### 3. Ausführen und beobachten

- Fan-out klein halten und nur bei unabhängigem Nutzen vergrößern.
- Fortschritt über Runtime-Status oder einen projektüblichen Checkpoint verfolgen.
- Bei Konflikten, Scope-Ausweitung oder fehlender Autorität stoppen und eskalieren.
- Ein fehlgeschlagener Worker darf unabhängige Arbeitspakete nicht automatisch
  blockieren.

### 4. Ergebnisse abnehmen

Eine Fertigmeldung ist zunächst eine Behauptung. Der Orchestrator prüft selbst:

1. Existiert das behauptete Artefakt oder die genannte Änderung?
2. Gehört es zum vereinbarten Scope?
3. Besteht der vereinbarte Test oder Nachweis aktuell?
4. Wurden fremde Änderungen, Sperren und negative Scopes respektiert?
5. Widersprechen sich Ergebnisse verschiedener Worker?

Erst danach gilt ein Arbeitspaket als abgeschlossen.

### 5. Integrieren und sichern

- Konflikte bewusst auflösen; Ergebnisse nicht blind aneinanderhängen.
- Erforderliche Gesamttests nach der Integration erneut ausführen.
- Offene, fehlgeschlagene und zurückgestellte Pakete klar ausweisen.
- Bei längeren Läufen Ziel, Status, Evidenz und nächsten Schritt in einem
  wiederauffindbaren Checkpoint sichern.

## Minimaler Worker-Prompt

```text
Auftrag: <Kennung und Ziel>
Eingaben: <Quellen>
Du darfst: <positiver Scope>
Du darfst nicht: <negativer Scope>
Fertig, wenn: <prüfbares Kriterium>
Belege mit: <Test, Diff oder Fundstelle>
Antworte als: <Rückgabeformat>
```

## Stop-Bedingungen

Stoppe nur das betroffene Arbeitspaket, wenn sein Scope, seine Autorität oder
seine Evidenz unklar wird. Unabhängige, sichere Pakete dürfen weiterlaufen.

Stoppe die gesamte Delegation, wenn:

- die Teilaufgaben nicht mehr unabhängig sind,
- ein gemeinsamer Schreibbereich nicht sicher getrennt werden kann,
- Regeln, Sperren oder Autorität für den gesamten verbleibenden Scope unklar sind,
- die erwarteten Kosten den erkennbaren Nutzen übersteigen,
- die geforderte Evidenz nicht erzeugt oder geprüft werden kann.

## Journal des Modifications

### 1.1.0 (2026-07-28)
- Nutzer-, Pfad-, Modell- und Providerbindungen entfernt.
- Auftragsvertrag, Autoritätsgrenze, Evidenzabnahme und Checkpoints als
  portable Kernmechanik herausgearbeitet.
- Baseline für fremde Änderungen sowie paketlokale und globale Stopps
  ausdrücklich getrennt.

### 1.0.0 (2026-06-17)
- Lokale Ausgangsfassung.