---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  Eigenständige Navigations- und Routing-Strategie, die
  Verzeichnishierarchien nach oben und unten nach Wegweiser-Dokumenten wie
  CLAUDE.md, AGENTS.md, README.md und RULES.md sowie nach
  nutzerkonfigurierbaren Stichwörtern durchsucht. Die Konfiguration erfolgt
  über staircase-config.json oder config.json. Auch als Up-and-Down Routing
  oder Walking Bass Routing bekannt.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
language: de
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
---

<img src="banner.png" width="100%" alt="staircase-routing banner">

# Staircase-Routing (Up-and-Down / Walking Bass Routing)

Der Skill **Staircase-Routing**, auch *Up-and-Down Routing* oder *Walking Bass
Routing* genannt, kapselt die Strategie zur Prüfung von
Verzeichnisdokumenten für KI-Agenten.

Wenn ein Agent ein Verzeichnis betritt oder an einer Datei arbeitet, nutzt er
diese Strategie, um maßgeblichen Kontext, Regeln und Wegweiser-Dokumente zu
finden, bevor er Code ändert oder eine Aktion ausführt.

---

## 1. Standards für Wegweiser-Dokumente

Staircase-Routing sucht standardmäßig nach diesen Wegweiser-Dokumenten:

- **Globale und projektbezogene Steuerung:** `CLAUDE.md`, `AGENTS.md`,
  `START.md`, `RULES.md`
- **Projektübersicht und Aufgaben:** `README.md`, `TODO.md`, `NOTIZ.md`,
  `BEWEISNOTIZ.md`
- **Benutzerdefinierte Stichwörter:** Konfiguriert über
  `staircase-config.json` oder `config.json`.

---

## 2. Traversal-Algorithmus

```text
                           [ Root- / Workspace-Ebene ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Schritt 2: Root-Wegweiser lesen)
                           └───────────▲────────────┘
                                       │ (Treppe aufwärts)
                           ┌───────────┴────────────┐
                           │ Unterordner / Ziel     │ ◄── (Schritt 1: Im CWD beginnen)
                           └───────────┬────────────┘
                                       │ (Treppe abwärts)
                           ┌───────────▼────────────┐
                           │ Kind- / Modulordner    │ ◄── (Schritt 3: Untergeordnete Wegweiser finden)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### Schritt 1: Aktuelles Arbeitsverzeichnis (CWD) prüfen

- Prüfe das Verzeichnis der Zieldatei oder das aktive Arbeitsverzeichnis.
- Sind Wegweiser-Dokumente vorhanden, lies sie sofort.

### Schritt 2: Nach oben traversieren

- Wird im CWD **kein** Wegweiser-Dokument gefunden, gehe in das
  Elternverzeichnis (`..`).
- Wiederhole dies schrittweise nach oben, bis ein Root-Wegweiser-Dokument
  (`CLAUDE.md` oder `AGENTS.md`) oder die Workspace-Grenze erreicht ist.
- Lies alle gefundenen Root-Wegweiser, um globale Vorgaben und Projektregeln
  festzustellen.

### Schritt 3: Nach unten prüfen

- Gehe vom festgestellten Root-Verzeichnis nach unten in die für die Aufgabe
  relevanten Unterverzeichnisse.
- Finde spezialisierte Wegweiser auf Modulebene, Domänenregeln oder
  Komponentenkonfigurationen und lies sie.

---

## 3. Nutzerkonfigurierbare Stichwörter (`staircase-config.json`)

Agenten können eine lokale oder globale `staircase-config.json` lesen, um die
gesuchten Wegweiser anzupassen:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. Integration mit `letter-hooker` und geplanten Aufgaben

`staircase-routing` ist als zentraler Preflight-Bootloader in den Skill
**`letter-hooker`** und die geplante Aufgabe
**`antigravity-kontext-and-workflow-loader-and-divider`** eingebettet. Dadurch
finden und befolgen Agenten Wegweiser-Dokumente, bevor sie Änderungen beginnen.
