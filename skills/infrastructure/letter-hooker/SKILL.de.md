---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  Erweitert automation-self-care um Letter Hooks, Preflight-Bootloader,
  Regeln zum Durchlaufen von Dokumenten und selbstheilende
  Prompt-Kontextanreicherung für KI-Agenten und CLIs ohne native,
  ereignisgesteuerte JSON-Lifecycle-Hooks, etwa Antigravity oder die Gemini
  CLI. Verwenden, wenn ein Agent Preflight-Regeln einfügen, vor Arbeitsbeginn
  Memory oder Gardener durchsuchen, Strategien zum Lesen von
  Verzeichnisdokumenten wie CLAUDE.md und AGENTS.md durchsetzen oder
  Sidecar-Aufgaben dynamisch an Skills und Sicherheitsprotokolle weiterleiten
  soll.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: de
status: active
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

Der Skill **Letter-Hooker** erweitert `automation-self-care` für
KI-Agenten-Frameworks wie **Antigravity / Gemini CLI**, die keine nativen,
ereignisgesteuerten JSON-Lifecycle-Hook-Loader besitzen, beispielsweise
`~/.claude/settings.json` oder `~/.codex/hooks.json`.

Anstelle passiver Hooks bei jedem Tastendruck betreibt `letter-hooker` über
geplante Aufgaben und Wartungsskripte
(`agy_kontext_and_workflow_loader.py`) einen **aktiven
Preflight-Bootloader auf Prompt-Ebene und einen Letter-Hook-Einfügeregelkreis**.

---

## Kernfähigkeiten

1. **Preflight-Bootloader und Regeln zum Durchlaufen von Dokumenten**:
   - **Suche nach oben und unten**: Weist Agenten verbindlich an, im aktuellen
     Arbeitsverzeichnis `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md` und
     `README.md` zu prüfen. Fehlen sie, wird nach oben gesucht, bis sie gefunden
     werden; danach folgt die Prüfung nach unten.
   - **Memory- und Gardener-Preflight**: Vor zerstörerischen oder komplexen
     Änderungen ist eine Preflight-Abfrage bei `gardener` und `memoryhooker`
     verpflichtend.

2. **Letter-Hook-Katalog und Referenzlinks**:
   - Modulare `.md`-Anweisungsdateien liegen unter
     `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`.
   - Fügt ausdrückliche `file://`-Links direkt in den Prompttext von
     `sidecar.json` ein, damit Agenten beim Aufruf die genauen Sicherheits- und
     Workflow-Protokolle lesen.

3. **Tägliche Stichwortliste und selbstheilende Prompt-Anreicherung**:
   - Pflegt täglich eine `STICHWORTLISTE.json` aus aktiven und wartenden
     Aufgaben.
   - Analysiert Ausführungsprotokolle (`AUTOMATIONS-MEMORY.md`) auf
     Fehlermuster wie fehlenden Kontext, fehlende Workflow-Anleitung oder
     ungültige Pfade und passt Aufgaben-Prompts dynamisch an.

4. **Skill- und Persona-Routing**:
   - Prüft Aufgabenstichwörter und ordnet sie passenden `.SKILLS` zu, etwa
     `infrastructure/condition`, `semantic-persona-routing`, `orchestrator`,
     `think` oder `decide`.

---

## Wichtige Letter Hooks

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

1. **Sidecars prüfen**: Alle Prompttexte aus `sidecar.json` unter
   `~/.gemini/config/sidecars/` lesen.
2. **Stichwortliste aktualisieren**: Domänenbegriffe extrahieren und in
   `.SYNC/STICHWORTLISTE.json` speichern.
3. **Letter Hooks einfügen**: Bootloader-Regeln und `file://`-Referenzlinks an
   Prompts anhängen.
4. **Ergebnisse protokollieren**: Aktualisierungen in
   `ANTIGRAVITY-LOG.txt` und `ANTIGRAVITY-REGISTRY.md` festhalten.
