---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: >
  Anbieterneutraler Sync-Planer für MCP-Konfigurationen, Skills und Regeldateien
  über Agent-Anbieter und App-Klassen. Er inventarisiert live erkennbare
  Möglichkeiten, bietet Auswahlachsen an und lässt den User Quelle der Wahrheit,
  Ziele, Richtung und Konfliktstrategie bestimmen. Truth kann eine Endpoint-
  Konfiguration, eine Datei oder eine geordnete Menge mehrerer Dateien sein.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: de
status: active
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies:
  tools: [python]
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "skills/infrastructure/agent-config-sync/"
  origin_version: "0.3.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="agent-config-sync banner">

# Agent Config Sync

Der Skill trennt drei Entscheidungen:

1. **Endpoints:** Welche installierten Agenten, CLIs, IDEs oder Desktop-Apps?
2. **Ressourcen:** MCP, Skills, Regeln oder eine explizite Teilmenge?
3. **Truth:** Welche Quelle(n), Richtung und Konfliktregel?

Keine dieser Entscheidungen wird aus dem Anbieter des aufrufenden Agenten
abgeleitet.

## Ablauf

### 1. System inventarisieren

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

`--discover` prüft bekannte CLI-Kommandos und konfigurierte Oberflächen.
„Bekannt“ bedeutet nur im Katalog geführt; „erkannt“ benötigt lokale Evidenz.
`--offer` bildet daraus:

- Anbieterachse: ein Anbieter über mehrere App-Klassen,
- App-Klassenachse: eine Klasse über mehrere Anbieter,
- Gesamtachse: alle erkannten Endpoints.

### 2. User-Auswahl erfassen

Der User darf konkrete Namen oder eine Achse nennen. Danach explizit festhalten:

- Mitglieder/Ziele,
- Ressourcen (`mcp`, `skills`, `rules`),
- Modus (`push`, `pull`, `bidirectional`),
- Truth-Quelle(n),
- Konfliktstrategie.

Ohne gewählte Truth-Quelle bleibt der Plan blockiert.

### 3. Truth modellieren

Eine Truth kann sein:

- ein Endpoint, etwa eine existierende MCP-Konfiguration,
- eine frei gewählte Datei,
- mehrere geordnete Dateien, etwa globale `AGENTS.md` plus Projektregeln,
- ein Verzeichnis für Skills.

Mehrere Regeldateien brauchen eine explizite Strategie:
`ordered-overlay`, `generated-loader`, `copy` oder `redirect`. Konflikte werden
nicht geraten. `CLAUDE.md`, `AGENTS.md`, `GPT.md` oder andere Namen sind
gleichberechtigte mögliche Quellen; keine davon ist global voreingestellt.

### 4. Plan, Apply, Verifikation

```bash
python scripts/sync.py --status
python scripts/sync.py --plan
python scripts/sync.py --apply --yes
```

`--apply` unterstützt derzeit MCP-Block-Transfers und Skill-Verzeichnisse.
Regeldatei-Topologien werden geplant, aber nur über einen vom User gewählten
Adapter umgesetzt; dadurch wird keine mehrteilige Truth versehentlich
plattkopiert.

## Registry

Die publizierte `registry.example.json` enthält keine aktive Relation und keinen
Hub. Eine lokale, gitignorierte `registry.json` hält nur die User-Entscheidung.
Selektoren dürfen Provider und App-Klassen kombinieren:

```json
{
  "name": "selected-cli-sync",
  "selection": {
    "providers": ["openai", "anthropic"],
    "app_classes": ["cli"]
  },
  "mode": "push",
  "source": "codex-cli",
  "scope": "mcp"
}
```

Siehe `REGISTRY.md` für Datei-Truth und Mehrfachquellen.

## Abgrenzung

- `mcp-config-sync` ist der MCP-spezifische Einstieg in diesen Skill.
- `agents-bridge` erzeugt Bootstrap-/Redirect-Regeln für fremde Agenten.
- `ellmos-agent-bridge` routet und koordiniert Partner zur Laufzeit.
- ControlCenter kann ein Adapter sein, ist aber keine notwendige zentrale Truth.

## Sicherheit

- Discovery, Offer und Plan sind read-only für Agent-Konfigurationen.
- `--apply` braucht `--yes`, Backups und Re-Read-Verifikation.
- Unverifizierte Formate und Pfade bleiben gesperrt.
- Lokale Registry/Cache-Dateien bleiben privat und gitignored.

## Changelog

### 0.3.0 (2026-07-27)

- Anbieter- und App-Klassenachsen sowie lokale Discovery/Offers.
- Kein voreingestellter Claude-Hub.
- Frei wählbare einzelne oder mehrere Truth-Dateien.
- Regeldateien als eigener Scope; Apply bleibt bis zur Adapterwahl fail-closed.
