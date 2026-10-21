---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: "Anbieterneutraler Einstiegspunkt zum Entdecken, Planen und Synchronisieren von MCP-Konfigurationen zwischen vom Nutzer ausgewählten Anbietern und App-Klassen. Der Nutzer wählt Wahrheitsquelle, Ziele und Umfang; kein Anbieter ist ein impliziter Hub."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: de
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: f28dce27691f8415486c17dfc3c7b37d7990885d89917c1d8986523de97609e7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T13:01:55.290867+00:00"
---
<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


# MCP Config Sync (Deutsch)

Dies ist der MCP-fokussierte Einstiegspunkt zu `agent-config-sync`. Er setzt
keinen Anbieter, keine App und keine Hauptdatei voraus.

## Ablauf

1. Frage, welche konkreten Endpunkte oder Achsen der Nutzer möchte: innerhalb
   eines Anbieters über App-Klassen hinweg, innerhalb einer App-Klasse über
   Anbieter hinweg, eine explizite Liste oder jeden erkannten Anbieter und jede
   erkannte Klasse.
2. Führe `agent-config-sync/scripts/sync.py --discover` aus, dann `--offer`.
3. Präsentiere erkannte Endpunkte getrennt von nicht verifizierten Kandidaten.
4. Lass den Nutzer Wahrheitsquelle, Ziele, Richtung und Konfliktpolitik wählen.
5. Materialisiere `registry.json`, prüfe `--plan` und verwende
   erst danach `--apply --yes`.

Erkennung und Angebote sind rein lesend. Es gibt keinen impliziten Hub und
kein implizites „alles synchronisieren“. Die früheren Claude Code↔Claude
Desktop-Skripte sind ein Legacy-Profil, nicht der generische Standard.

## Beispielaufruf

```
agent-config-sync/scripts/sync.py --discover
agent-config-sync/scripts/sync.py --offer
agent-config-sync/scripts/sync.py --plan
agent-config-sync/scripts/sync.py --apply --yes
```

## Änderungsprotokoll

- v2.0.0 (2026-07-27): Sync provider-neutral gemacht -- keine implizite
  Hub-/Master-Datei mehr, Nutzer waehlt Quelle, Ziele, Richtung und
  Konfliktpolitik selbst.
- v1.0.1 (2026-06-13): Skill veroeffentlicht (Sync-Scripts + Vorlage auf
  generische Pfade umgestellt, Referenzen anonymisiert, EN-Version).
