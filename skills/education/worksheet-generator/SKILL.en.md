---
name: worksheet-generator
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: >
  Points to the standalone module worksheet-generator: generates
  individualized worksheets and practice material for educational and
  therapeutic professionals from a support goal (free text + optional ICF
  codes), level, and age -- optionally enriched by a scan of existing
  material. Use this skill when a worksheet, exercise sheet, or support
  material should be created. No client/person reference (only
  goal/level/age). The ICF reference is bring-your-own -- with a clear
  boundary: a material generator, not a therapy program; generated sheets
  must be professionally reviewed before use.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

provenance:
  origin: "external"
  origin_repo: "https://github.com/ellmos-ai/worksheet-generator"
  origin_path: "SKILL.md, worksheet_generator/ (Python module), _tools/icf_fetch.py"
  origin_version: null
  last_sync_from_origin: "2026-07-23"
  last_sync_to_origin: null
  local_changes_since_sync: false

category: education
tags: [worksheets, icf, education, therapy-support, wrapper, pointer-skill]
language: en
status: active
---

# worksheet-generator -- Pointer Skill

This skill is a **thin pointer (wrapper)** to the standalone, public module
repository
[`ellmos-ai/worksheet-generator`](https://github.com/ellmos-ai/worksheet-generator)
(MIT license, public). The actual skill lives there -- this repository only
links to it and documents installation.

Note: the module's CLI, config, and documentation are German-language by
design (built for German-speaking educational/therapeutic professionals);
this pointer skill's own instructions are in English for discoverability.

## What the module does

`worksheet-generator` turns a support goal (free text + optional ICF codes),
level, and age into a structured worksheet JSON, then rendered to Markdown,
HTML, or DOCX:

- **Deterministic and offline** -- no LLM calls, no network access inside
  the generator itself; topic-specific placeholders are marked
  `(ANZUPASSEN)` ("to be adapted"); fine-grained content elaboration is left
  to the calling LLM agent.
- **Material folder scan:** `config.json` (`material_dirs`) can pull in
  existing material (txt/md/docx), and already-researched bullet points are
  carried over directly as concrete task prompts.
- **Renderers:** Markdown and HTML always available, DOCX optional (needs
  `python-docx`); PDF/PowerPoint/Canva only as external delegation.
- **No client/person reference:** controlled exclusively via
  goal/level/age -- never by name or diagnosis.

## ICF reference: bring-your-own (important)

The module contains **no** ICF short titles or full texts -- only official
ICF codes as neutral identifiers (this repo's MIT license does NOT extend to
ICF content; separate WHO/BfArM licensing applies). The bundled fetch script
`_tools/icf_fetch.py` builds a local, gitignored `icf_local.json` (code +
short title, source + retrieval date in the file header):

- **Mode A** (no network access): read your own CSV/JSON source file.
- **Mode B** (live lookup): WHO ICD-11 API with your own registration
  (`icd.who.int/icdapi`, your own `WHO_ICD_CLIENT_ID`/`_SECRET`).

## Boundaries (important)

- **A material generator, not a therapy program and not a promise of
  healing.** Does not replace professional judgment by qualified
  educational/therapeutic professionals.
- **Generated worksheets must be professionally reviewed and adapted before
  use** -- the module delivers raw material, not ready-to-use documents.
- No client/person reference: this module is not meant for reports or
  client data.

## Installation (generic, no local paths)

1. Clone the module:
   ```bash
   git clone https://github.com/ellmos-ai/worksheet-generator.git <clone-path>
   ```
2. No mandatory dependencies (pure Python stdlib, Python >= 3.10).
   Optional, for the DOCX renderer:
   ```bash
   pip install python-docx
   ```
3. Adopt `<clone-path>/SKILL.md` into your own skill environment (e.g.
   `~/.claude/skills/worksheet-generator/`). Do NOT commit real local paths
   or hostnames into a versioned skill environment.
4. Local overrides (`material_dirs`, `icf_source`, ...) belong in
   `config.local.json` (gitignored) -- template: `config.local.example.json`.
5. Load the ICF reference: `python <clone-path>/_tools/icf_fetch.py --source
   <path>` (Mode A) or with your own WHO registration (Mode B, see above).
6. For CLI, schema, and renderer details, see the module repo's README.

## Origin of this pointer skill

This wrapper was added on 2026-07-23 as a showcase entry for the
`ellmos-ai/skills` repository. There is **no code duplication** -- maintenance
and versioning stay solely in the `ellmos-ai/worksheet-generator` module
repo.

## Changelog

### 0.1.0 (2026-07-23)
- Initial pointer skill for `ellmos-ai/worksheet-generator`.
