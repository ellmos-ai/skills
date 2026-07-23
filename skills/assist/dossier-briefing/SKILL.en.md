---
name: dossier-briefing
version: 1.0.0
category: assist
description: >
  Generates a structured research briefing for a topic or person
  as a Markdown scaffold (stdout or file). No persistent store.
tags:
  - briefing
  - dossier
  - recherche
  - markdown
  - research
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages:
  - de
  - en
dependencies:
  python:
    - datetime
    - pathlib
    - textwrap
runtime: python3
entry_point: dossier_briefing_core.py
provenance:
  origin: BACH persoenlicher-assistent
  origin_path: system/agents/persoenlicher-assistent/tools/dossier_generator.py
  origin_version: "1.0.0"
  origin_repo: github.com/ellmos-ai/bach
  origin_license: MIT
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: >
    Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier,
    DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden).
    Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt).
    Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.
---

# Dossier-Briefing

**Structured research briefing for a topic or person**

---

## Overview

Generates an empty, structured Markdown briefing for any subject
(person, company, event, concept). The scaffold serves as a starting point for
subsequent research with `research-agent` or `web-reading`.

---

## Triggers

| Phrase | Action |
|---|---|
| "Create a briefing on Marie Curie" | Scaffold: person, type=person |
| "Dossier on OpenAI" | Scaffold: company, type=organization |
| "Briefing on quantum computing" | Scaffold: topic, type=topic |
| "Prepare a research briefing on COP30" | Scaffold: event, type=event |

---

## Workflow

1. **Name the subject:** Extract name/title of the briefing from the user input.
2. **Detect type:** person, organization, topic, event (or unspecified).
3. **Generate scaffold:** Create Markdown with all relevant sections.
4. **Output:** stdout or optionally write to a file (`-o file.md`).
5. **Start research:** Hand scaffold to `research-agent` or `web-reading`
   to fill in missing sections.

---

## CLI

```bash
# Briefing to stdout
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# Write to file
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Topic briefing
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantum computing" --typ topic

# Event
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Without type (generic)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "My topic"

# Help
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## Briefing Types and Sections

| Type | Sections |
|---|---|
| `person` | Basic data, biography/background, work & contributions, sources, notes |
| `organization` | Profile, history, products/services, key people, sources, notes |
| `topic` | Overview, background/context, current developments, key sources, open questions, notes |
| `event` | Key facts, participants, background/timeline, significance, sources, notes |
| `unspecified` | Overview, background, details, sources, notes |

---

## Store

No persistent store. The scaffold is only output (stdout or file),
not stored in a database.

---

## Attitude

- Always emphasise that the scaffold is empty and must be filled through research.
- Never invent content or hallucinate — only provide structure.
- Ask if the type is unclear or use `unspecified`.

---

## Privacy

No network access. No store. Purely local processing.

---

## Related Resources

- `research-agent` — fills the briefing scaffold with research results
- `web-reading` — reads web pages and extracts content for the briefing

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-06-22 | Created from BACH dossier_generator.py v1.0.0; store removed, generalised |
