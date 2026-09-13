---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  Erweitert automation-self-care um Letter Hooks, Preflight-Bootloader,
  Dokument-Traversierungsregeln und selbstheilende Prompt-Kontext-
  Anreicherung für KI-Agenten und CLIs ohne native, ereignisgetriebene
  JSON-Lifecycle-Hooks (wie Antigravity / Gemini CLI). Nutzen, wenn ein
  Agent Preflight-Regeln injizieren, vor Arbeitsbeginn Memory/Gardener
  durchsuchen, Verzeichnis-Dokument-Lesestrategien erzwingen
  (CLAUDE.md / AGENTS.md) oder Sidecar-Tasks dynamisch an Skills und
  Sicherheitsprotokolle routen soll.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: de
status: active
visibility: public
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

# Letter-Hooker (Prompt-Level Preflight & Governance Engine)

Der **Letter-Hooker**-Skill erweitert `automation-self-care` für KI-Agenten-Frameworks (wie **Antigravity / Gemini CLI**), die keine nativen, ereignisgetriebenen JSON-Lifecycle-Hook-Loader besitzen (z. B. `~/.claude/settings.json` oder `~/.codex/hooks.json`).

Statt sich auf passive Per-Keypress-Hooks zu verlassen, betreibt `letter-hooker` einen **aktiven Prompt-Level-Preflight-Bootloader und Letter-Hook-Injection-Loop** über geplante Tasks und Maintainer-Skripte (`agy_kontext_and_workflow_loader.py`).

---

## Kernfähigkeiten

1. **Preflight-Bootloader & Dokument-Traversierungsregeln**:
   - **Aufwärts- & Abwärtssuche**: Erzwingt strikte Anweisungen für Agenten, `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md` und `README.md` auf der aktuellen Arbeitsverzeichnis-Ebene zu prüfen. Fehlen sie, aufwärts traversieren, bis gefunden; dann abwärts prüfen.
   - **Memory- & Gardener-Preflight**: Pflicht-Preflight-Abfrage an `gardener` und `memoryhooker`, bevor destruktive oder komplexe Änderungen ausgeführt werden.

2. **Letter-Hooks-Katalog & Referenz-Links**:
   - Modulare `.md`-Instruktionsdateien unter `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`.
   - Injiziert explizite `file://`-Links direkt in den `sidecar.json`-Prompt-Text, damit Agenten bei Aufruf exakte Sicherheits- und Workflow-Protokolle lesen.

3. **Tägliche Stichwortliste & selbstheilende Prompt-Anreicherung**:
   - Pflegt eine tägliche `STICHWORTLISTE.json` aus aktiven/Standby-Tasks.
   - Analysiert Ausführungslogs (`AUTOMATIONS-MEMORY.md`) auf Fehlermuster (fehlender Kontext, fehlende Workflow-Anleitung, ungültige Pfade) und patcht Task-Prompts dynamisch.

4. **Skill- & Persona-Routing**:
   - Prüft Task-Schlüsselwörter und mappt sie auf passende `.SKILLS` (z. B. `infrastructure/condition`, `semantic-persona-routing`, `orchestrator`, `think`, `decide`).

---

## Wichtige Letter Hooks

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md)

---

## Workflow-Integration

```bash
# Letter-Hooker-Wartungs-Engine ausführen
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **Sidecars scannen**: Alle `sidecar.json`-Prompt-Texte in `~/.gemini/config/sidecars/` lesen.
2. **Stichwortliste aktualisieren**: Fachbegriffe extrahieren und nach `.SYNC/STICHWORTLISTE.json` speichern.
3. **Letter Hooks injizieren**: Bootloader-Regeln und `file://`-Referenz-Links an Prompts anhängen.
4. **Ergebnisse loggen**: Updates in `ANTIGRAVITY-LOG.txt` und `ANTIGRAVITY-REGISTRY.md` festhalten.
