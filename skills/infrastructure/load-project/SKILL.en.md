---
name: load-project
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: Zu Beginn einer konkreten Projektaufgabe oder bei unklarem Kontext: Ziel auflösen, geltende Regelhierarchie laden, verbindliche Referenzen verfolgen und vor der eigentlichen Arbeit einen evidenzbasierten Lagebericht erstellen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [projekt, boot, kontext, regeln, locks, orientierung, onboarding]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'local-agent-skills/load-project/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **English Translation** — Official English version of `load-project`.


# Load Project

## Zweck

Nutze diesen Skill zu Beginn einer konkreten Projektaufgabe oder wenn der
Arbeitskontext unklar geworden ist. Ziel ist kein vollständiger Repository-Audit,
sondern der kleinste belastbare Kontext, mit dem sicher weitergearbeitet werden
kann.

## Konfiguration

Der Skill benötigt keine festen Verzeichnisnamen. Lokale Installationen können
optional folgende Werte in ihren allgemeinen Agentenregeln oder einer
projektlokalen Konfiguration festlegen:

- bekannte Workspace-Wurzeln,
- bevorzugte Dateiwerkzeuge,
- Namen zusätzlicher Boot- oder Registry-Dateien,
- Lock-Prüfer,
- projektspezifische Rollen und Prioritäten.

Fehlt eine solche Konfiguration, arbeitet der Skill ausschließlich mit dem
angegebenen Ziel und den dort auffindbaren Projektregeln.

## Ablauf

### 1. Ziel auflösen

1. Expliziten Pfad, Projektnamen oder aktuelle Arbeitsmappe als Startpunkt nehmen.
2. Den tatsächlichen Projekt- oder Repository-Root bestimmen.
3. Mehrdeutige Treffer anhand von Aufgabe, Root-Dokumenten und Repository-Grenzen
   eingrenzen; bei materiell unterschiedlichen Zielen nicht raten.

### 2. Regelhierarchie laden

Vom allgemeinen zum spezifischen Kontext lesen:

1. globale Agenten- und Sicherheitsregeln,
2. Workspace- oder Pipeline-Regeln,
3. Projekt- und Repository-Regeln,
4. aufgabenbezogene Anweisungen.

Spezifischere Regeln gelten innerhalb ihres Scopes; höherrangige Sicherheits- und
Autorisierungsgrenzen bleiben bestehen.

### 3. Root-Dokumente nach Rollen lesen

Dateinamen sind Hinweise, keine feste Norm. Suche gezielt nach Dokumenten mit
diesen Rollen:

| Rolle | Typischer Inhalt |
|---|---|
| Einstieg | Zweck, Navigation, Startanweisung |
| Regeln | Arbeitsweise, Sprache, Sicherheit, Konventionen |
| Architektur | Komponenten, Datenfluss, Grenzen |
| Status | aktueller Stand, offene Probleme, letzte Prüfung |
| Aufgaben | priorisierte nächste Arbeit |
| Register | kanonische Projekte, Checks oder Veröffentlichungen |
| Nachweis | Tests, Prüfprotokolle, Beweisnotizen |
| Übergabe | laufende Arbeit, fremde Änderungen, nächster Schritt |

Nur die für die konkrete Aufgabe relevanten Rollen laden.

### 4. Verbindliche Referenzen verfolgen

Wenn eine gelesene Regel weitere Dateien ausdrücklich als Pflichtlektüre nennt,
diese gezielt nachladen. Referenzketten beenden, sobald sie für die Aufgabe keinen
zusätzlichen verbindlichen Kontext mehr liefern.

### 5. Zustand und Sperren prüfen

- Locks anhand der lokalen Policy auf Owner, Scope, Zeitstempel und
  Gültigkeitskriterium prüfen; ohne definierte Stale-Regel einen Lock nie
  eigenmächtig für veraltet erklären,
- Versionskontrollstatus und fremde Änderungen,
- laufende Prozesse oder Checkpoints, sofern relevant,
- Aktualität von Registern, Tests und Statusangaben.

Den Ausgangszustand der betroffenen Bereiche vor Änderungen als Status-/Diff-
Baseline sichern. Lassen sich vorhandene Änderungen nicht sicher zuordnen, gelten
sie vorsorglich als fremd und bleiben unberührt.

Momentaufnahmen als solche behandeln und vor riskanten Aktionen erneut prüfen.

### 6. Lagebericht erstellen

Vor der Umsetzung knapp festhalten:

```text
Ziel:
Projekt-Root:
Geltende Regeln:
Evidenzquellen:
Snapshot-Zeitpunkt:
Relevanter Ist-Zustand:
Locks oder fremde Änderungen:
Erfolgskriterium:
Nächster sicherer Schritt:
```

Quellen nur so genau nennen, wie es zur Überprüfbarkeit nötig ist. Secrets,
personenbezogene Daten und vertrauliche Inhalte redigieren und nicht in den
Lagebericht kopieren.

Wenn die Aufgabe damit eindeutig und autorisiert ist, direkt weiterarbeiten.

## Grenzen

- Keine breite, unbeschränkte Dateisuche als Standard.
- Keine fehlenden Regeln oder Register neu erfinden.
- Keine alte Statusmeldung als aktuellen Nachweis behandeln.
- Keine fremden Änderungen überschreiben.
- Kein Projekt-Onboarding durchführen, wenn nur Kontext für eine konkrete Aufgabe
  geladen werden soll.

## Changelog

### 1.1.0 (2026-07-28)
- Feste Nutzer-, Workspace-, Tool- und Providerbindungen entfernt.
- Rollenbasierte Dokumenterkennung und optionale lokale Konfiguration eingeführt.
- Lock-Gültigkeit, Dirty-Tree-Provenienz, Snapshot-Nachweise und redigierte
  Lageberichte operationalisiert.

### 1.0.0 (2026-06-17)
- Lokale Ausgangsfassung.
