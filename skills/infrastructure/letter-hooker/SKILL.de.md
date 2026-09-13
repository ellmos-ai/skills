---
name: letter-hooker
version: 1.1.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-08-20
description: >
  Erweitert automation-self-care um Letter Hooks, Preflight-Bootloader,
  Regeln zum Durchlaufen von Dokumenten, den 3-Zeilen-Prompt-Header-Standard ([TITEL], ZWECK, AUFGABE)
  und selbstheilende Prompt-Kontextanreicherung für KI-Agenten und CLIs ohne native,
  ereignisgesteuerte JSON-Lifecycle-Hooks (TGAS - Text-Based Governance Automations Seed).
  Löst aus bei tgas, textbased-governance-automations-seed, textbasierte-governance-automationen-seed,
  textbased-governance-automations, letter-hooker, letter-hooks, prompt-enrichment, bootloader,
  prompt-structure-policy oder context-loader.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance, prompt-structure, textbased-governance, tgas]
language: de
status: active
aliases: [textbased-governance-automations-seed, tgas, textbasierte-governance-automationen-seed, textbased-governance-automations, textbased-governance-automatisations-seed, prompt-letter-hooks, prompt-bootloader, agy-workflow-loader, textbased-prompt-governance]
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
---

<img src="banner.png" width="100%" alt="letter-hooker banner">

# Letter-Hooker (Preflight- und Governance-Engine auf Prompt-Ebene)

Der Skill **Letter-Hooker** erweitert `automation-self-care` für KI-Agenten-Frameworks wie **Antigravity / Gemini CLI**, die keine nativen, ereignisgesteuerten JSON-Lifecycle-Hook-Loader besitzen (beispielsweise `~/.claude/settings.json` oder `~/.codex/hooks.json`).

Anstelle passiver Hooks bei jedem Tastendruck betreibt `letter-hooker` über geplante Aufgaben (`antigravity-kontext-and-workflow-loader-and-divider`) und Wartungsskripte (`agy_kontext_and_workflow_loader.py`) einen **aktiven Preflight-Bootloader auf Prompt-Ebene, eine 3-Zeilen-Header-Injektion und einen Letter-Hook-Einfügeregelkreis**.

---

## Kernfähigkeiten & Architektur

### 1. Verbindliche 3-Zeilen-Prompt-Header-Injektion
Um eine fehlerfreie Titelgenerierung in der Antigravity Conversation History zu garantieren und generische Titelfusionen zu vermeiden, wird jeder Task-Prompt strukturiert:
```text
[TITEL_DER_AUTOMATION_IN_GROSSBUCHSTABEN]
ZWECK: <Prägnante 1-2 Zeilen Zusammenfassung des Ziels>
AUFGABE: <Konkrete Arbeitsanweisungen, Kriterien, Schwellenwerte>
```

### 2. Preflight-Bootloader und Regeln zum Durchlaufen von Dokumenten
- **Suche nach oben und unten**: Weist Agenten verbindlich an, im aktuellen Arbeitsverzeichnis `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md` und `README.md` zu prüfen. Fehlen sie, wird nach oben gesucht, bis sie gefunden werden; danach folgt die Prüfung nach unten.
- **Memory- und Gardener-Preflight**: Vor zerstörerischen oder komplexen Änderungen ist eine Preflight-Abfrage bei `gardener` und `memoryhooker` verpflichtend.

### 3. Letter-Hook-Katalog und Referenzlinks
Modulare `.md`-Anweisungsdateien liegen unter `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`. Sie werden am Ende jedes Prompts angefügt:
```text
--- GOVERNANCE, WORKFLOW & HOOKS ---
1. POLICY: file:///<USER_HOME>/.gemini/AUTOMATION_POLICY.md
2. PREFLIGHT & MEMORY: file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md
3. PATHS & AUTHORITY: file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md
4. WORKFLOW HYGIENE & LOCKS: file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md
5. AUTOMATIONS-MEMORY: Registriere wichtige Aktionen und Verifikationsergebnisse in 'AUTOMATIONS-MEMORY.md' & 'ANTIGRAVITY-LOG.txt'.
```

### 4. Stündliche Stichwortliste und selbstheilende Prompt-Anreicherung
- Pflegt stündlich die [STICHWORTLISTE.json](file:///<USER_HOME>/OneDrive/.SYNC/STICHWORTLISTE.json) (71 aktive Aufgaben).
- Analysiert Ausführungsprotokolle (`AUTOMATIONS-MEMORY.md`) auf Fehlermuster (fehlender Kontext, fehlende Workflow-Anleitung, ungültige Pfade) und passt Aufgaben-Prompts dynamisch an.

### 5. 4-Stufen-Modellallokations-Unterstützung
- Bindet Tier 1 (3.6 Flash), Tier 2 (3.7 Flash), Tier 3 (3.1 Pro) und Tier 4 (Codex/Claude) anhand von Aufgabenprofil und Stichwort-Taxonomie ein.

---

## Wichtige Letter Hooks

- **`HOOK-POLICY-01`**: [AUTOMATION_POLICY.md](file:///<USER_HOME>/.gemini/AUTOMATION_POLICY.md)
- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md)

---

## Workflow-Integration

```bash
# Letter-Hooker-Wartungsengine ausführen
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **Sidecars prüfen**: Alle Prompttexte aus `sidecar.json` unter `~/.gemini/config/sidecars/` (oder `.gemini/antigravity/sidecar_data/`) lesen.
2. **Stichwortliste aktualisieren**: Domänenbegriffe extrahieren und in `.SYNC/STICHWORTLISTE.json` speichern.
3. **Prompts formatieren**: 3-Zeilen-Header-Standard (`[TITEL]`, `ZWECK:`, `AUFGABE:`) sicherstellen.
4. **Letter Hooks einfügen**: Bootloader-Regeln und `file://`-Referenzlinks an Prompts anhängen.
5. **Ergebnisse protokollieren**: Aktualisierungen in `ANTIGRAVITY-LOG.txt` und `ANTIGRAVITY-REGISTRY.md` festhalten.

---

## Änderungsprotokoll

### 1.1.0 (2026-08-20)
- **Prompt-Struktur-Standard**: Aufnahme des 3-Zeilen-Prompt-Headers zur Vermeidung von UI-Titelverzerrungen.
- **4-Stufen-Modell-Unterstützung**: Ergänzung von Modell-Tiering-Leitplanken (Gemini 3.7 Flash, 3.6 Flash, 3.1 Pro).
- **Konsolidierte Governance-Verlinkung**: Direkte Anbindung von `AUTOMATION_POLICY.md` als primärer Governance-Hook.
- **Neuer Primär-Alias**: `textbased-governance-automations`.

### 1.0.0 (2026-07-29)
- Erstveröffentlichung der Preflight-Bootloader- und Letter-Hook-Engine für Antigravity.
