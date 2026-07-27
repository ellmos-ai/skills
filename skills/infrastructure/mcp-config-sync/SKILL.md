---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: >
  Anbieterneutraler Einstieg zum Erkennen, Planen und Synchronisieren von
  MCP-Konfigurationen zwischen frei gewählten Agent-Anbietern und App-Klassen.
  Der User bestimmt Quelle, Ziele und Umfang. Der Skill inventarisiert bekannte
  Möglichkeiten auf dem aktuellen System und bietet Topologien an, ohne
  automatisch eine Truth-Quelle festzulegen.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: de
status: active
dependencies:
  tools: [python]
  services: []
  protocols: [agent-config-sync]
  python: []
provenance:
  origin: "custom"
  origin_path: "skills/infrastructure/mcp-config-sync/"
  origin_version: "2.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="mcp-config-sync banner">

# MCP Config Sync

Dieser Skill ist der MCP-spezifische Einstieg zu `agent-config-sync`. Er nimmt
keinen Anbieter, keine App und keine zentrale Datei als Standard an.

## Pflichtablauf

1. Frage in der Form: „Zwischen welchen Endpoints soll synchronisiert werden?“
   Zulässig sind konkrete Namen oder Auswahlachsen:
   - innerhalb eines Anbieters zwischen App-Klassen,
   - innerhalb einer App-Klasse zwischen Anbietern,
   - explizite Endpoint-Liste,
   - alle erkannten Anbieter und Klassen.
2. Führe im benachbarten Skill `agent-config-sync` aus:
   `python scripts/sync.py --discover`, danach `--offer`.
3. Zeige nur live belegte Endpoints als erkannt. Bekannte, aber nicht belegte
   Möglichkeiten bleiben als Kandidaten gekennzeichnet.
4. Lasse den User Truth-Quelle, Ziele, Richtung und Konfliktregel bestimmen.
5. Erzeuge `registry.json`, zeige `--plan`, und schreibe erst nach expliziter
   Freigabe mit `--apply --yes`.

## Auswahlbeispiele

- „MCP zwischen Claude Code und Claude Desktop.“
- „MCP zwischen allen installierten CLI-Anbietern.“
- „MCP von dieser JSON-Datei nach Codex und Cursor.“
- „Zeig erst alle Sync-Möglichkeiten auf diesem Rechner.“

Die alte Claude-Code↔Claude-Desktop-Automation liegt nur noch als
Migrationsreferenz unter `agent-config-sync/references/legacy-mcp-config-sync.md`.
Die Skripte in diesem Ordner sind nicht mehr der generische Standard und dürfen
nur für bewusst gewählte Legacy-Profile verwendet werden.

## Sicherheitsgrenzen

- Discovery und Angebote sind read-only.
- Kein impliziter Hub und kein implizites „alles“.
- Unverifizierte Pfade oder Formate werden nicht beschrieben.
- Vor jedem Write: Plan, Backup, Verifikation.
- App-/Marketplace-Erweiterungen werden als Mapping behandelt, nicht blind
  gespiegelt.

## Changelog

### 2.0.0 (2026-07-27)

- Anbieter- und app-klassenneutral.
- Systeminventar und Topologieangebote vor jeder Auswahl.
- Truth-Quelle wird ausschließlich vom User festgelegt.
- Claude-Paar wird zum optionalen Legacy-Profil.
