---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: "Anbieterneutraler Planer zur Synchronisierung von MCP-Konfiguration, Skills und Regeldateien über Agenten-Anbieter und App-Klassen hinweg. Er erkennt belegte lokale Optionen und lässt den Benutzer Wahrheitsquelle, Ziele, Richtung und Konflikte auswählen."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: de
status: active
visibility: public
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 53ba3789a0734868d5d243eab03ffe02b5daee779a5ccf68036937081049010c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T13:01:55.003932+00:00"
---
<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


# Agent Config Sync (Deutsch)

Der Skill trennt Endpunktauswahl, Ressourcen und Wahrheitsquelle. Ausführen:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

Der Benutzer kann eine explizite Endpunktliste auswählen, einen Anbieter über App-Klassen hinweg, eine App-Klasse über Anbieter hinweg oder alle erkannten Endpunkte. Die Erkennung ist ein Nachweis, keine Autorisierung.

Die Wahrheitsquelle kann ein Endpunkt, eine Datei, eine geordnete Menge von Dateien wie mehrere `AGENTS.md`-Ebenen oder ein Skills-Verzeichnis sein. Kein Dateiname oder Anbieter fungiert implizit als Zentrum. Ohne ausgewählte Wahrheitsquelle bleiben Pläne blockiert.

Überprüfe `--status` und `--plan`; verwende `--apply --yes` erst nach Genehmigung.
MCP-Blöcke und Skill-Verzeichnisse sind implementiert. Regeldatei-Topologien bleiben fail-closed, bis der Benutzer einen Merge-/Redirect-Adapter auswählt.
