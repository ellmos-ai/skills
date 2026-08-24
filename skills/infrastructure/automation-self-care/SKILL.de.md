---
name: automation-self-care
version: 1.1.0
type: skill
author: Lukas Geiger + OpenAI + Google Gemini
created: 2026-07-28
updated: 2026-08-20
description: >
  Erstellt und betreibt ein anbieterneutrales textbasiertes Governance- und Selbstpflege-Kernset
  für geplante LLM-Aufgaben und Desktop-App-Automationen (TGAS - Text-Based Governance Automations Seed).
  Erzwingt den strukturierten 3-Zeilen-Prompt-Standard ([TITEL], ZWECK, AUFGABE), 4-Stufen-Modellallokation
  (inklusive Gemini 3.7 Flash), aktive Tokenverbrauchssteuerung mit dynamischer Drosselung,
  Berechtigungs- und Sperrleitplanken sowie Fail-Closed-Sicherheit. Löst aus bei tgas,
  textbased-governance-automations-seed, textbasierte-governance-automationen-seed,
  textbased-governance-automations, textbasierte-governance-automationen, Automations-Selbstpflege,
  Scheduler-Pflege, Prompt-Struktur-Standard oder ANTIGRAVITY-Governance-Aufgabenfamilie.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, governance, token-governance, prompt-structure, tiering, tgas]
language: de
status: active
aliases: [textbased-governance-automations-seed, tgas, textbasierte-governance-automationen-seed, textbased-governance-automations, textbasierte-governance-automationen, textbased-governance-automatisations-seed, core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
dependencies:
  tools: []
  services: []
  protocols: []
  python: [token_tracker.py, token_analytics_engine.py]
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="automation-self-care banner">

# Automations-Selbstpflege & Textbasierte Governance-Engine

Erstelle und betreibe eine native, anbieterneutrale **Textbasierte Governance- und Selbstpflege-Flotte** für geplante Agenten-Automatisierungen und Hintergrund-Worker. Bewahre die vollständige Architektur und Absicht der ANTIGRAVITY-Wartungsfamilie durch evidenzbasierte Optimierung, reversible Änderungen, aktive Token-Governance, 4-Stufen-Modellallokation und nativen Readback.

---

## Nicht verhandelbare Grenzen & Governance-Leitplanken

1. **Strukturierter 3-Zeilen-Prompt-Header-Standard**:
   Jeder automatisierte Task-Prompt MUSS zwingend mit dem standardisierten 3-Zeilen-Kopf beginnen, um korrekte UI-Titelgenerierung in der Conversation History und sofortige Scope-Klarheit zu garantieren:
   ```text
   [TITEL_DER_AUTOMATION_IN_GROSSBUCHSTABEN]
   ZWECK: <Prägnante 1-2 Zeilen Zusammenfassung des Ziels>
   AUFGABE: <Konkrete Arbeitsanweisungen, Kriterien, Schwellenwerte>
   
   --- GOVERNANCE, WORKFLOW & HOOKS ---
   1. POLICY: file:///<USER_HOME>/.gemini/AUTOMATION_POLICY.md
   2. PREFLIGHT & MEMORY: file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md
   3. PATHS & AUTHORITY: file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md
   4. WORKFLOW HYGIENE & LOCKS: file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md
   5. LOGGING: Registriere Ergebnisse in 'AUTOMATIONS-MEMORY.md' & 'ANTIGRAVITY-LOG.txt'.
   ```
2. **Vier-Stufen-Modellallokation (Budget & Leistungsstufen)**:
   - **Tier 1 (High-Speed & Routine-Hygiene):** `Gemini 3.6 Flash (High)` (Wächter-Tasks, Token-Tracker, Verzeichnis-Sync, Umlaute, MCP-Pflege).
   - **Tier 2 (Advanced Logic & Code Dev):** `Gemini 3.7 Flash (High)` (Software-Entwicklung, GitHubBot Discoverability/Marketing, Roblox Lua, LaTeX-Design, Prompt-Verbesserung).
   - **Tier 3 (Deep Science & Kritische Reviews):** `Gemini 3.1 Pro (High)` / Claude (Mathematische Modellanalysen, Friedensforschung, Fachsprachen-Checks).
   - **Tier 4 (Schwere Multi-File-Refactorings):** `Codex (GPT-5.4)` / Claude Code (Große Architektur-Umbauten).
3. **Aktive Token-Governance & Drosselungsregeln**:
   - **Immunitäts-Regel:** Aufgaben mit `ANTIGRAVITY` oder Kern-Governance-Rollen im Namen dürfen NIEMALS deaktiviert werden.
   - **Guthaben > 50%:** Normalbetrieb; automatische Wiederherstellung aller zuvor gedrosselten Tasks und Originalmodelle (`RESTORED_ALL_SETTINGS`).
   - **Guthaben < 20%:** Pausiere Aufgaben mit `LOW`-Priorität (`LOW_CREDIT_THROTTLING_ACTIVE`).
   - **Guthaben < 10%:** Kritische Drosselung; belasse ausschließlich `HIGH`-Priorität aktiv und schalte Modelle auf Flash um (`CRITICAL_THROTTLING_ACTIVE`).
4. **Wächter-Immunität & Probe-Aktivierungs-Protokoll**:
   - Deaktiviere Wächter- oder Standby-Tasks niemals blind, nur weil ein Einzellauf keine Arbeit vorfand.
   - Teste zuvor deaktivierte Aufgaben mit hoher Nutzerpriorität **schrittweise einzeln** (Probe-Aktivierung) und entscheide erst im Folgelauf anhand der Erfolgsnachweise über die dauerhafte Aktivierung.
5. **Berechtigungs- & Sperrleitplanken (Fail-Closed)**:
   - Respektiere aktive Repository-Sperren (z. B. `LOCK.user.buildweek-no-push.txt` für BACH und BYUM).
   - Führe niemals unautorisierte Produktions-Uploads oder destruktive Massenänderungen durch.
   - Bei unklaren Berechtigungen gilt sofortiges **Fail-Closed** (read-only Abbruch).

---

## Multi-Provider-Unterstützung & Adapter-Zuordnung

TGAS ist vollständig **anbieterneutral** und bildet alle Desktop-KI-Agenten-Frameworks ab:

| Anbieter / Framework | Native Scheduler-Oberfläche | Speicherort & Konfiguration | Primäre Modelle |
| :--- | :--- | :--- | :--- |
| **Google Antigravity / Gemini CLI** | `sidecar_data/<task>/sidecar.json` | JSON args-Array + Letter Hooks | `Gemini 3.6 Flash`, `3.7 Flash`, `3.1 Pro` |
| **OpenAI Codex Desktop / Codex App** | `~/.codex/automations/` | `scheduled_tasks.toml` & `config.json` | `gpt-5.4`, `gpt-5-codex`, `gpt-5.1-mini` |
| **Anthropic Claude Desktop / Cowork** | `claude-desktop` Sessions / Task Scheduler | `applied-tasks.json` & `settings.json` | `claude-3-7-sonnet`, `claude-3-5-haiku` |
| **ChatGPT / Headless CLI** | OS Cron / Windows Aufgabenplanung | YAML- / JSON-Deskriptoren | Provider-APIs / Open-Compute |

Detaillierte Implementierungsschemata und Fähigkeiten-Profile sind dokumentiert in:
- [provider-profiles.md](references/provider-profiles.md) (Konkrete Provider-Adapter und Ausführungsmechanik)
- [provider-adapter-contract.md](references/provider-adapter-contract.md) (Capability-Profile JSON-Schema und Mutations-Verträge)
- [core-set.md](references/core-set.md) (Detaillierte Topologie- und Evidenzregeln)

---

## Vollständige 10-Task Governance-Topologie

| # | Task-Bezeichner | Standard-Takt | Modell-Tier | Kern-Governance-Verantwortung |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `antigravity-maintainer` | `35 1,13 * * *` | Tier 1 (3.6 Flash) | Verzeichnishygienie, SQLite-Vakuumierung, Bereinigung verwaister Dateien. |
| 2 | `antigravity-token-watcher` | `18 * * * *` | Tier 1 (3.6 Flash) | Live-Telemetrie, SQLite-Sync, 7d/30d Burn-Vorhersagen, dynamische Drosselung. |
| 3 | `antigravity-permissioner` | `37 19 * * *` | Tier 1 (3.6 Flash) | Workspace-Grenzen, Lock-Durchsetzung, Pfad-Autorisierung. |
| 4 | `antigravity-sheduler-state-controller` | `26 5,17 * * *` | Tier 1 (3.6 Flash) | Statuskontrolle, Probe-Aktivierungen, Erkennung defekter Tasks. |
| 5 | `antigravity-sheduled-task-sentiziser` | `27 2,14 * * *` | Tier 1 (3.6 Flash) | Arbeitslast-basierte Cron-Taktregulierung (Frequenz anheben/senken). |
| 6 | `antigravity-task-sheduler-burden-divisor` | `40 20 * * *` | Tier 1 (3.6 Flash) | Lastverteilung, Entzerrung von Lastspitzen, Kollisionsvermeidung. |
| 7 | `antigravity-sheduler-text-improver` | `30 6 * * *` | Tier 2 (3.7 Flash) | Prompt-Qualitätsaudits, Behebung irreführender Guidance (3-Zeilen-Kopf). |
| 8 | `antigravity-task-sync` | `50 10,22 * * *` | Tier 1 (3.6 Flash) | Bidirektionale Spiegelung zwischen aktiven Sidecars und Referenzkatalog. |
| 9 | `antigravity-file-bond-corrector` | `57 23 * * *` | Tier 1 (3.6 Flash) | Pfadbindungen, Namenskonventionen (`NAMING-SYSTEM.md`), Reparatur defekter Links. |
| 10 | `antigravity-kontext-and-workflow-loader-and-divider` | `2 * * * *` | Tier 1 (3.6 Flash) | Stichwortindex-Pflege (`STICHWORTLISTE.json`), Kontext- & Letter-Hook-Ladung. |

---

## Pflegeschleifen-Ablauf

```text
Prüfung des vorigen Laufs
  -> Evidenz des Arbeitsergebnisses erheben
  -> Token- & Guthabenstatus prüfen (token_tracker.py)
  -> Locks & Permissions prüfen (Fail-Closed)
  -> Höchstens EINE reversible Änderung anwenden (Prompt / Takt / Modell)
  -> Nativen Readback & Verifikation durchführen
  -> Quittung in AUTOMATIONS-MEMORY.md & ANTIGRAVITY-LOG.txt registrieren
```

---

## Änderungsprotokoll

### 1.1.0 (2026-08-20)
- **Prompt-Struktur-Standard**: Verbindlicher 3-Zeilen-Prompt-Kopf (`[TITEL]`, `ZWECK:`, `AUFGABE:`) zur Vermeidung von UI-Titelverzerrungen.
- **4-Stufen-Modellallokation**: Offizielle Aufnahme von `Gemini 3.7 Flash (High)` für Tier-2-Entwicklungsaufgaben.
- **Token-Governance-Integration**: Kodifizierung der 3-Stufen-Drosselungslogik (`>50%`, `<20%`, `<10%`) und der `ANTIGRAVITY`-Immunitätsregel.
- **10-Task Governance-Topologie**: Vollständige Dokumentation der 10 spezialisierten Wartungsaufgaben.
- **Neuer Primär-Alias**: `textbased-governance-automations` / `textbasierte-governance-automationen`.

### 1.0.1 (2026-07-30)
- Ergänzung anbieterneutraler Alias-Begriffe für Text- und Desktop-App-Automationen.

### 1.0.0 (2026-07-28)
- Konsolidierung der ursprünglichen ANTIGRAVITY-Aufgabenfamilie und des F1-F6-Regelkreises.
