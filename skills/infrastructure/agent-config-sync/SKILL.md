---
name: agent-config-sync
version: 0.2.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-06-20
updated: 2026-06-20
description: >
  Synchronisiert MCP-Server UND Skills uebergreifend ueber ALLE bekannten Agent-Apps und CLIs
  (Claude Code, Claude Desktop, Codex CLI, Antigravity/Gemini, Kimi Code, Cursor, Cline,
  Windsurf, GitHub Copilot, ...) auf einem oder mehreren Systemen. Aktiviert sich, wenn ein
  MCP-Server oder Skill in mehreren Agent-Tools verfuegbar gemacht werden soll, der User fragt
  "sync mcp/skills ueber alle agents", "warum hat Tool X den Server/Skill nicht", "MCP/Skills
  ueberall verteilen", "config-sync zwischen agents", oder ein neues Agent-Tool an den
  gemeinsamen Stand angeschlossen werden soll. Liest eine Registry (welche Tools syncen wie),
  eine Config (Anbieter-Standardspezifikationen: wo + welches Format) und einen Lauf-Cache
  (aufgeloeste reale Pfade), wendet Sync-Regeln an (pull vs. verteilen) und verifiziert.
  Enthaelt einen Lernmechanismus: unbekannte/veraltete Config-Orte werden per Systemsuche,
  WebSearch und Context7 nachgeschlagen und in der Config aktualisiert. Loest den aelteren,
  auf Claude Code <-> Claude Desktop beschraenkten Skill mcp-config-sync ab (umschliesst ihn
  als Spezialfall). Claude-MCP-Profile werden via ellmos-controlcenter-mcp-Backend verwaltet
  (resolve_profile / switch_profile), nicht durch eigene Logik.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [mcp, skills, sync, multi-agent, claude-code, claude-desktop, codex, gemini, antigravity, kimi, cursor, cline, windsurf, copilot, config, registry, windows, macos, controlcenter]
language: de
status: active

aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]

dependencies:
  tools: [python]
  services: [ellmos-controlcenter-mcp]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "skills/infrastructure/agent-config-sync/"
  origin_version: "0.2.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Agent Config Sync

Ein **uebergreifendes Sync-Protokoll** fuer MCP-Server **und** Skills ueber alle bekannten
Agent-Apps und CLIs. Statt fuer jedes App-Paar ein eigenes Skript zu pflegen, beschreibt
dieser Skill *deklarativ*, **welche** Tools auf einem System leben, **was** sie teilen sollen
(MCP / Skills / beides) und **wie** (pull, push, bidirektional/verteilen). Ein generischer
Ablauf liest diese Deklaration und fuehrt den Sync aus.

**Claude-MCP-Profile-Backend:** Fuer `claude-code` und `claude-desktop` wird
**`ellmos-controlcenter-mcp`** als Backend genutzt (MCP-Tool `resolve_profile`/`switch_profile`).
`sync.py` enthaelt keine eigene Claude-Profil-Logik; der Agent ruft die ControlCenter-MCP-Tools
zur Laufzeit auf. Direkt lesbare JSON-Profildateien (z.B. `shared.json`) werden weiterhin
direkt gelesen.

**Loest `mcp-config-sync` ab:** Der aeltere Skill `mcp-config-sync` ist als
Registry-Beziehung `claude-pair` (pull, scope mcp) in diesem Skill umschlossen.
Sobald `agent-config-sync` produktiv eingesetzt wird, sollte `mcp-config-sync` auf
`status: deprecated` gesetzt werden.

## Verhaeltnis zu bestehenden Skills (keine Duplikation)

| Skill | Zustaendigkeit | Verhaeltnis |
|---|---|---|
| **agent-config-sync** (dieser) | Sync von **MCP-Servern + Skills** ueber **alle** Agent-Tools, regelbasiert | Achse 1 (Inter-Agent) + Inter-IDE-Verteilung |
| `mcp-config-sync` | nur MCP, nur Claude Code <-> Claude Desktop, 1 Skript | **Spezialfall**, der hier umschlossen wird (siehe `references/legacy-mcp-config-sync.md`); bleibt vorerst als Legacy bestehen |
| `agents-bridge` | leitet fremde Agents per Redirect-Datei auf die EINE Regel-Quelle `CLAUDE.md` | **Regel**-Sync (Wissen/Workflows), NICHT Tool-Config. Komplementaer. |
| `system-onboarding` | Erstaufsetzen eines neuen Systems (Reihenfolge der Installation) | liefert die Config-Ort-Tabellen, auf denen dieser Skill aufbaut |

**Was dieser Skill NICHT ist:** kein Regel-/CLAUDE.md-Sync (das macht `agents-bridge`), kein
System-Erstsetup (das macht `system-onboarding`), kein Plugin-/Extension-Marktplatz-Abgleich
(die Toolkits sind komplementaer, siehe `mcp-config-sync/references/plugin-extension-parity.md`).

## Die drei Datenebenen

Der Skill trennt bewusst **Was-soll-passieren** von **Wie-sehen-die-Anbieter-aus** von
**Wo-liegt-es-real**:

```
  REGISTRY  (lokal/privat)        was syncen welche Tools wie? (Beziehungen, Modus, Scope)
      |  liest
      v
  CONFIG    (publizierbar)        Anbieter-Standardspezifikationen: pro Tool wo + Format
      |  loest Pfade auf nach
      v
  CACHE     (lokal/privat)        aufgeloeste reale Verzeichnisse/Dateien (Lauf-Cache)
```

| Datei | Inhalt | Privacy |
|---|---|---|
| `REGISTRY.md` + `registry.example.json` | welche Tools vorhanden, Sync-Paare/-Gruppen, Modus, Scope | Template publizierbar; **reale `registry.json` lokal/gitignored** |
| `CONFIG.md` + `config.json` | je Anbieter: Config-Ort (Platzhalter `<HOME>`), Format, Merge-Key, Eigenheiten, Quellen-Stand | publizierbar (neutral) |
| `CACHE.md` + `cache.json` | aufgeloeste reale Pfade auf DIESEM System | **lokal/gitignored** |

## Ablauf (Protokoll)

### 0. Lock + Vorsicht
- Bei aktiver `LOCK*.txt` im Zielbereich: nichts schreiben (LOCK-System beachten).
- Default ist **read-only**: `--status`/`--plan` veraendern nichts. `--apply` nur mit
  `--yes` und nach Anzeige des Plans.

### 1. Registry lesen
- `registry.json` (Fallback: `registry.example.json`) laden.
- Liefert: vorhandene Tools auf diesem `host`, die Sync-Beziehungen (Paare/Gruppen),
  je Beziehung Modus (`pull` | `push` | `bidirectional`) und Scope (`mcp` | `skills` | `both`).

### 2. Config lesen (Anbieter-Specs)
- `config.json` laden: je Anbieter Config-Ort (mit `<HOME>`-Platzhalter), Format
  (`json` | `toml` | `dir`), `mcp_key` (z.B. `mcpServers`), `skills_dir`, Eigenheiten.

### 3. Cache aufloesen
- Platzhalter (`<HOME>`, `<APPDATA>`, ...) gegen das reale System aufloesen → `cache.json`.
- Pruefen, ob die Datei/der Ordner existiert. **Fehlt sie → Lernmechanismus (Schritt 6).**

### 4. Plan bilden (pull vs. verteilen)
- Pro Beziehung den **Quellzustand** lesen und mit dem **Zielzustand** vergleichen.
- **pull**: ein designierter Master/Hub wird gelesen, Ziele bekommen dessen Stand.
- **push/verteilen**: ein Quell-Tool verteilt an mehrere Ziele.
- **bidirectional**: Vereinigung; bei Konflikt (gleicher Key, anderer Wert) → eskalieren,
  nicht raten.
- Fuer **mcp**: nur den `mcp_key`-Block ersetzen, restliche Config-Felder erhalten;
  Format-Konvertierung JSON↔TOML, wo noetig (Codex = TOML).
- Fuer **skills**: Verzeichnis-Abgleich (`skills_dir`); App-spezifische Eigenheiten
  beachten (z.B. Claude Desktop liest `~/.claude/skills/` NICHT direkt → Bridge-Skill,
  siehe `mcp-config-sync/references/skills-sync-options.md`).
- Ausgabe: menschenlesbarer **Plan** (welche Datei, welche Keys, add/update/remove).

### 5. Anwenden + Verifizieren (nur `--apply --yes`)
- Vor jedem Schreiben **Backup mit Zeitstempel**.
- Schreiben (Format-erhaltend, nur Ziel-Block).
- **Verifikation:** Ziel erneut lesen, Soll/Ist vergleichen; Diff ausgeben.
- Hinweis: Apps ggf. neu starten (Claude Desktop komplett beenden), damit Aenderungen greifen.

### 6. Lernmechanismus (Selbstheilung der Config)
Wird ausgeloest, wenn ein Config-Ort fehlt, ein Anbieter unbekannt ist oder ein Format
nicht passt:

1. **Config-Ort veraltet/nicht gefunden** → **Systemsuche** nach den bekannten Dateinamen:
   - MCP-Server-Suche: ellmos-FileCommander (`fc_search_files`/`fc_search`) oder `Glob`
     ueber die Home-/AppData-Wurzeln nach `*config*.json`, `config.toml`,
     `claude_desktop_config.json`, `settings.json`, `mcp.json`.
   - Gefundenen realen Pfad in `cache.json` eintragen; wenn er dauerhaft vom Config-Standard
     abweicht, `config.json` (mit Stand-Hinweis) aktualisieren.
2. **Unbekannter Anbieter** (Tool, das in `config.json` fehlt) → **WebSearch** nach
   "<tool> MCP config file location" / "<tool> custom rules file", Ergebnis verifizieren,
   neuen Anbieter-Eintrag in `config.json` anlegen (mit `sources`-Feld + Datum).
3. **Format-/Schema-Unsicherheit** → aktuelle Spezifikation per **WebSearch** UND
   **Context7** (`resolve-library-id` → `query-docs`, z.B. "Model Context Protocol",
   "claude code mcp config", "codex config.toml") nachschlagen; `config.json` korrigieren.

> Jede automatische Config-Aenderung dokumentiert sich selbst: Feld `sources` + `updated`
> im betroffenen Anbieter-Eintrag setzen.

## Aufruf

```bash
# Status: Pfade aufloesen, Existenz pruefen, cache.json aktualisieren (read-only fuer Agent-Configs)
PYTHONIOENCODING=utf-8 python scripts/sync.py --status

# Plan: was wuerde ein Sync tun? (read-only, kein Schreiben)
PYTHONIOENCODING=utf-8 python scripts/sync.py --plan

# Anwenden: block-replace pro Relation, Backup + Verifikation (bestaetigung erforderlich)
PYTHONIOENCODING=utf-8 python scripts/sync.py --apply --yes

# Tests ausfuehren (nutzen nur Fixtures -- keine echten Configs)
PYTHONIOENCODING=utf-8 python -m pytest skills/infrastructure/agent-config-sync/tests/ -v
```

### ControlCenter-Backend (Claude-Provider)

Fuer `claude-code`- und `claude-desktop`-Targets wird kein direkter Config-Write gemacht.
Stattdessen den **`ellmos-controlcenter-mcp`**-Server nutzen:

```
resolve_profile()   -- aktives Profil und Serverinhalt lesen
switch_profile()    -- Profil wechseln / MCP-Config-Datei neu erzeugen
```

Der `--plan`-Output zeigt explizit, welche ControlCenter-Aktion noetig ist.

## Privacy / Konventionen

- **Publizierbar (neutral):** `SKILL.md`, `CONFIG.md`, `config.json`, `REGISTRY.md`,
  `registry.example.json`, `CACHE.md`, `cache.example.json`, `scripts/`. Nur Platzhalter
  (`<HOME>`, `~`, `<HOST>`, `<USER>`), KEINE echten Personen-Pfade/Hostnames.
- **Lokal/privat (gitignored):** `registry.json`, `cache.json` (die mit echten Pfaden
  gefuellten Instanzen fuer DIESES System). Muster in der `.SKILLS/.gitignore` ergaenzt.
- **Quelle = `skills/...`.** NICHT nach `~/.claude/skills/` deployen — das entscheidet der
  User spaeter via `skill_sync.py`. Nicht committen/pushen ohne Freigabe.

## Aufbau dieses Skills

```
agent-config-sync/
├── SKILL.md                  (diese Datei — das Protokoll, DE)
├── SKILL.en.md               (englische Version)
├── REGISTRY.md               Doku: was syncen welche Tools wie
├── registry.example.json     Template (publizierbar)
├── registry.json             reale Instanz fuer dieses System (LOKAL, gitignored)
├── CONFIG.md                 Doku: Anbieter-Standardspezifikationen
├── config.json               je Anbieter: Ort + Format + Eigenheiten (publizierbar)
├── CACHE.md                  Doku: Lauf-Cache aufgeloester Pfade
├── cache.example.json        Template (publizierbar)
├── cache.json                aufgeloeste reale Pfade (LOKAL, gitignored)
├── scripts/
│   └── sync.py               Funktionale Implementierung (--status/--plan/--apply)
├── tests/
│   └── test_sync.py          Pytest-Tests (nur Fixtures, keine echten Config-Writes)
└── references/
    └── legacy-mcp-config-sync.md   wie der alte MCP-Skill hier aufgeht
```

## Changelog

### 0.2.0 (2026-06-20)
- `--apply` implementiert: format-erhaltendes JSON-block-replace, TOML-Abschnitt-replace
  (Codex), Backup + Verifikation je Schritt, Skills-Verzeichnis-Abgleich.
- Test-Suite (`tests/test_sync.py`, 15 Tests, nur Fixtures -- keine echten Config-Writes).
- ControlCenter-Backend-Anbindung: Claude-Provider-Writes delegieren an
  `ellmos-controlcenter-mcp` (resolve_profile/switch_profile); keine eigene Profil-Logik.
- Test-Isolation via `--root`-Flag und `AGENT_CONFIG_SYNC_TEST_ROOT`-Env-Guard.
- Nutzerneutral: Platzhalter in SKILL.md/CONFIG/Templates; `registry.json`/`cache.json` gitignored.
- Versionierungs-Konformitaet: `last_sync_from_origin: null` (originaerer custom-Skill),
  `status: active`, in `registry/components.json` aufgenommen.
- Supersede-Relation zu `mcp-config-sync` in `references/legacy-mcp-config-sync.md` und
  SKILL.md-Kopftext modelliert.
- i18n: SKILL.md (DE, primaer) + SKILL.en.md (EN, vollstaendig).

### 0.1.0 (2026-06-20)
- Initiales Scaffold: Protokoll-SKILL.md, Registry/Config/Cache-Modell (Template + Doku),
  Lernmechanismus (Systemsuche/WebSearch/Context7), `scripts/sync.py`-Stub
  (`--status`/`--plan`). Umschliesst `mcp-config-sync` als Spezialfall.
