---
name: pingpong
version: 1.0.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-08-04
description: >
  Betreibt eine zeitlich begrenzte, sitzungsgebundene Funkstelle über einen
  gemeinsam synchronisierten Ordner. ListenSync scannt systematisch nach
  Aufträgen und Neuigkeiten; WriteSync versendet Deltas und Receipts. Verwenden
  bei PingPong, Dosentelefon, ListenSync, WriteSync, Sync-Listener,
  Auftragswache, News-Scan oder Goal-/Loop-Überwachung.

# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: de
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

Betreibe zwei oder mehr Systeme als Funkstellen über einen gemeinsamen Sync-Ordner. Halte den fachlichen Vertrag providerneutral; nur der Fortsetzungsadapter unterscheidet sich.

## Modus bestimmen

- ListenSync: Genau ein systematischer Listener pro Host. Er scannt, übernimmt passende Aufträge und führt bei Antworten auch WriteSync aus.
- WriteSync: Jeder arbeitende Akteur darf eigene relevante Deltas, Aufträge, Neuigkeiten und Receipts senden. Dieser Modus startet keinen Listener.
- Fehlt der Modus, verwende ListenSync.

## Laufvertrag festlegen

1. Verwende standardmäßig 24h. Akzeptiere auch relative Dauern wie 15m, 2h, 3d oder einen absoluten ISO-8601-Endzeitpunkt.
2. Messe die lokale Startzeit und nenne expires_at mit Datum, Uhrzeit und Zeitzone.
3. Starte mit 15 Minuten. Nutze die Kadenz aus references/protocol.md, sofern der User keine feste Kadenz verlangt.
4. Definiere Zielerfüllung als: Endzeit erreicht, abschließender FileCommander-Scan belegt, alle bis dahin erkannten passenden Eingänge bearbeitet oder präzise blockiert dokumentiert, State aktualisiert und eigener Scheduler beendet.
5. Behaupte ohne FileCommander-Beleg weder Scan noch Zielerfüllung.

## Provider-Adapter verwenden

### Codex

Erstelle vor dem ersten Scan ausdrücklich ein persistiertes Goal mit dem vollständigen Laufvertrag und expires_at. Bearbeite pro Fortsetzung genau einen vollständigen Scanzyklus. Beende das Goal nicht nach einem leeren oder erfolgreichen Einzelzyklus. Warte danach real bis next_scan_at, beispielsweise mit:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

Führe am Ablaufzeitpunkt den Abschlusszyklus aus. Markiere das Goal nur bei erfülltem Erfolgskriterium als abgeschlossen.

### Claude Code

Starte den Auftrag als /loop <Kadenz> $pingpong. Wenn der Skill bereits aus einem geplanten Lauf kommt, lege keinen zweiten Loop an. Ersetze bei einer Kadenzänderung nur den eigenen Cron-Job. Lösche ihn nach dem Abschlusszyklus.

## Zyklus ausführen

Lies references/protocol.md vollständig und führe genau einen dort beschriebenen Scan-, Bearbeitungs- und State-Zyklus aus. Verwende für jeden Zugriff im Sync-Ordner ellmos FileCommander. Ein Shell-Listing, ein Scheduler-Eintrag oder ein Dateiname allein ist kein Scanbeleg.

Erfinde bei Leerlauf keine Arbeit. Melde knapp: Scanzeit, gelesene Freshness-Dateien, aktuelle Kadenz, empty_runs, next_scan_at und expires_at.

## WriteSync ausführen

Schreibe nur in den eigenen Systemslot oder einen ausdrücklich globalen Kanal. Nenne Absender, Empfänger, Zeit, Bezug, Handlung, Ergebnis, offene Punkte und gewünschte Kadenz. Merge statt Überschreiben; keine Credentials; Locks respektieren. Lies die kanonische Datei nach dem Schreiben mit FileCommander zurück.

## Changelog

### 1.0.0 (2026-08-04)

- Providerneutraler ListenSync-/WriteSync-Vertrag mit Codex-Goal- und Claude-Loop-Adaptern.
- FileCommander-Beleg, Freshness-Guard, adaptive Kadenz und absolute Ablaufbedingung ergänzt.
