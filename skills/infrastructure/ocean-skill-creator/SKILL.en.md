---
name: ocean-skill-creator
version: 0.4.1
type: skill
author: Ocean Contributors
created: 2026-08-24
updated: 2026-11-27
description: "Use when creating a new skill or upgrading an existing one to Ocean standards (e.g. 'create a skill', 'scaffold a new skill', 'make this skill Ocean-conformant', /ocean-skill-creator, transition alias /ellmos-skill-creator). Delegates generic authoring to skill-creator while applying pragmatic Ocean standards: 9-field frontmatter, externalized .json configs where needed (default-config.json or expressive custom filename) with self-healing, optional report templates (html/pdf/md/txt/json), grounding-seed, learning contract, and init/audit-skill CLI. Do NOT use for skill discovery (skill-finder) or catalog audits (skill-explorer)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: infrastructure
tags: [skill-authoring, ocean, config-cascade, self-healing, templates, grounding-seed, vendor-awareness]
language: en
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: ["grounding-seed (optional, recommended)"]
  skills: ["skill-creator:skill-creator (plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="ocean-skill-creator banner">

# ocean-skill-creator — Ocean Skill Builder

> **Successor Note (`v0.4.1`):** `ocean-skill-creator` is the canonical successor to `ellmos-skill-creator`. Existing `ellmos.*` schemas, `grounding-seed` docking points, and the transition trigger `/ellmos-skill-creator` remain fully backward-compatible.

> **Pragmatism Principle ("Only where genuinely useful"):**
> 1. **Expressive `.json` filenames are equally first-class:** `default-config.json` is a recommended default convention, **not a mandatory filename**. Domain-specific names such as `models.local.json`, `kalender-profiles.json`, `routing-defaults.json`, `prefs.json`, or `<channel>.json` are recognized on equal footing by the loader and `audit-skill`.
> 2. **Zero artificial boilerplate:** `.json` config files, `templates/`, and `scripts/` belong **only in skills where they add real value**. Pure guideline, advisory, therapy, thinking, or router/umbrella skills require neither dummy templates nor empty scripts and score a full `100/100 conformant` with clean `SKILL.md` + `SKILL.en.md` files alone.

## Origin and decision (fork vs. native composition)

**Decision: standalone composition, no fork.** Documented so the rationale stays explicit:

- `skill-creator` (Anthropic, marketplace `claude-plugins-official`) is **Apache-2.0** licensed — a fork would be legally clean, but would duplicate the entire generic eval and benchmark machinery (`agents/`, `eval-viewer/`, 7 helper scripts) that is already directly invocable via `Skill: skill-creator:skill-creator`.
- The real gap solved here consists of **pragmatic Ocean standards (backward-compatible with ellmos components)** that upstream cannot know about:
  9-field house frontmatter, bilingual DE+EN core parity, anti-hardcoding via externalized `.json` settings with self-healing fallback (whenever a skill has configurable parameters), replaceable report templates (`html`/`pdf`/`md`/`txt`/`json`, whenever a skill renders documents/reports), `grounding-seed` docking (`connections.json`), vendor awareness, and the learning/coverage file set.
- This skill contains **no upstream text** and **composes** the original instead of copying it. In addition, it ships [ocean_skill_scaffold.py](scripts/ocean_skill_scaffold.py), a pure Python standard-library CLI for right-sized scaffolding (`init`/`scaffold`), self-healing config validation (`validate-config`), and non-dogmatic skill audits (`audit-skill`).

## When to activate

- "create a skill for X", "scaffold a new skill", "use skill-creator", `/ocean-skill-creator` (or transition alias `/ellmos-skill-creator`)
- "upgrade this skill to Ocean standards", "check whether this skill needs externalized JSON settings or report templates"
- "audit this skill for hardcoded settings" (`audit-skill`)
- Whenever the target is a skill in our Ocean/ellmos skill catalog — not for ad-hoc one-off prompts outside the ecosystem.

## Procedure

### Step 1 — delegate interview, design, and eval

Invoke the official `Skill: skill-creator:skill-creator` when needed for: intent clarification, workflow drafting, test cases (`evals/evals.json`), eval loops, and trigger refinement. **Do not reinvent** generic authoring steps that upstream already handles well — `ocean-skill-creator` layers the Ocean architecture and quality contract on top.

### Step 1b — description = trigger (mandatory, not optional)

The `description` field alone determines whether a skill is ever selected; the Markdown body is invisible during routing. Verify before completion:

- **Put WHEN first** ("Use when ..."), followed by what the skill delivers. The trigger phrase plus 2–3 representative user phrasings must appear within the **first 250 characters**, because agent runtimes truncate long skill-list entries and drop overflowing descriptions.
- **Include typical phrasings** in single quotes together with the slash command (`/my-skill`).
- **State explicit boundaries** to neighbouring skills ("Do NOT use for ... (use other-skill)").
- **Wrap the YAML value in double quotes**, keep it at or below 1024 characters across every localization.
- Confirm `python testing/skill_frontmatter_gate.py` flags neither a missing trigger nor a trigger starting after character 250.

### Step 2 — create a right-sized Ocean house scaffold (`init` / `scaffold`)

Pick the footprint that matches the skill's actual nature — from a lean prompt skill (`--minimal`) up to a full report engine (`--with-reports --with-profiles`):

```bash
# A) Lean guideline, advisory, thinking, or router skill (SKILL.md + SKILL.en.md only)
python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py init <name> --category <category> --out skills/<category> --minimal --json

# B) Configurable skill with an expressive .json filename and no report templates
python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py init <name> --category <category> --out skills/<category> --config-name <name>-defaults.json --no-templates --json

# C) Full report/export skill with replaceable templates (html/pdf/md/txt/json) & channel profiles
python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py init <name> --category <category> --out skills/<category> --with-reports --with-profiles --json
```

Frontmatter and layout requirements (`docs/CONVENTIONS.md`):

- Include all **nine house required fields** (`name`, `version`, `type`, `author`, `created`, `updated`, `description`, `standalone`, `visibility`) plus `category`, `language`, `status`, `tags`, `dependencies`, and `provenance`.
- **Always start `visibility` at `private-only`** for newly created skills — switching to `public` is a separate, explicitly reviewed user decision.
- **Bilingual core (P-006):** Provide both `SKILL.md` (German primary) and `SKILL.en.md` (English counterpart with identical `name:` and matching structure).
- Every house key is purely additive alongside `name`/`description` (`anthropic_compatible: true`).

### Step 3 — enforce Ocean principles: provider-neutral, user-neutral, Ocean/ellmos-sensitive

Full details and code patterns: [OCEAN-PRINCIPLES.md](references/OCEAN-PRINCIPLES.md). Summary:

- **Viable standalone (`standalone`):** Any bundled configs, templates, or scripts run cleanly on the Python standard library with zero mandatory third-party packages.
- **Ecosystem-sensitive at runtime:** When Ocean or backward-compatible ellmos modules (`grounding_seed.detect_ecosystem()`, `source-resolver`) are installed, the skill detects and uses them dynamically via `try/except ImportError` — never hard-wired and without inventing a second discovery mechanism.
- **Strictly user-neutral in version control:** Zero personal names, internal hostnames, local development paths, or private IP addresses in tracked files (`author: Ocean Contributors` or neutral team attribution).

### Step 4 — externalized `.json` settings, profile cascade & self-healing (where parameters exist)

Full specification, naming flexibility, and self-healing protocol: [CONFIG-AND-SELF-HEALING.md](references/CONFIG-AND-SELF-HEALING.md).

1. **When external `.json` configuration is appropriate — and when it is not:**
   - Whenever a skill has configurable thresholds, model/routing tables, paths, time windows, output formats, or channel profiles -> **externalize them into `.json` instead of hardcoding them in scripts or prompts**.
   - When a skill is a pure guideline, counseling, thinking, or routing prompt with no configurable parameters -> **do not add an artificial `.json` file**.
2. **Expressive custom filenames + recommended cascade:**
   - `default-config.json` is the standard convention when no domain name is clearer; expressive filenames like `models.local.json`, `routing-defaults.json`, `kalender-profiles.json`, or `prefs.json` (`--config-name <file.json>`) are equally valid.
   - For multi-layer overrides, merge from general to specific:
     `<base-config>.json` (tracked, user-neutral fallback) -> `config.json` (local override) -> `<channel>.json` (e.g. `profiles/mail.json`) -> `<channel>.<chat>.json` (e.g. `profiles/mail.ops-weekly.json`) -> **CLI override** (`--set key=value`).
   - Templates: [default-config.template.json](templates/default-config.template.json), [skill-config.template.json](templates/skill-config.template.json), and [channel-profile.template.json](templates/channel-profile.template.json).
3. **Self-healing configuration loader (`load_effective_config`):**
   - Missing optional overrides fall back seamlessly to the base JSON file.
   - Corrupt JSON files (`JSONDecodeError`), non-object roots, or invalid section types never crash the skill; the loader falls back gracefully and emits structured `warnings`.
   - With `--repair` (`repair=True`), corrupt files are first preserved verbatim as `<filename>.corrupt.<UTC-timestamp>.bak`, newly introduced keys are merged additively without clobbering valid user values, and healed JSON is persisted atomically (`tmp` + `os.replace`).
4. **Separate `connections.json`:** Resolved external binaries and service bindings live in `connections.json` when needed ([skill-connections.template.json](templates/skill-connections.template.json), schema `ellmos.source-resolver.user-config.v1`).

### Step 4b — report/output options & replaceable `templates/` (only for report/export skills)

Full specification and rendering rules: [OUTPUT-AND-TEMPLATES.md](references/OUTPUT-AND-TEMPLATES.md).

**Applicability check:** Does the skill generate reports, audit logs, summaries, schedules, digests, or formatted document exports?

- **No** (pure guideline, router, stateless checker, converter): **No `templates/` directory needed** (`--no-templates` or `--minimal`).
- **Yes:** Separate data computation from presentation via a replaceable `templates/` folder ([report.template.html](templates/output/report.template.html) with `@media print`, [report.template.md](templates/output/report.template.md), [report.template.txt](templates/output/report.template.txt)), support the relevant formats (`html`, `pdf` with a mandatory 100% stdlib `%PDF-1.4` fallback and zero browser profile interference, `md`, `txt`, `json`), and keep `delivery` defaults safe (`enabled: false`, `dry_run: true`, `mode: "draft"`).

### Step 5 — build in provider and vendor awareness

Full text: [VENDOR-AWARENESS.md](references/VENDOR-AWARENESS.md). Summary: Any skill fulfilling a role backed by external tools or services includes a "Providers & alternatives" section listing (a) current state-of-the-art options, (b) at least one local/offline or open alternative, and (c) Ocean/ellmos components as equal-footing candidates (`grounding_seed.scan.scan_resources([...])`). Always propose installations rather than installing autonomously.

### Step 6 — configure self-update

Full text: [SELF-UPDATE.md](references/SELF-UPDATE.md). Summary: Every produced skill includes a "Self-update" section consulting `skill-finder` for better-fitting sibling skills and recording dated findings cleanly.

### Step 6b — attach learning contract + usecase coverage (reusable pattern where helpful)

Full text: [LEARNING-CONTRACT-AND-COVERAGE.md](references/LEARNING-CONTRACT-AND-COVERAGE.md). Reusable file set without inventing parallel schemas (`evals/evals.json`, [user-usecases.template.json](templates/user-usecases.template.json), [usecase-gaps.template.json](templates/usecase-gaps.template.json), [known-providers-and-abilities.template.json](templates/known-providers-and-abilities.template.json), [gap-closing-analysis.template.json](templates/gap-closing-analysis.template.json), and `lernvertrag`).

### Step 7 — validate (`audit-skill` & `validate-config`), register, and commit

1. **Run pragmatic conformance and config checks (never penalizes lean skills without templates/scripts!):**
   ```bash
   python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py audit-skill skills/<cat>/<name> --json
   # When the skill uses a JSON configuration file:
   python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py validate-config --default skills/<cat>/<name>/<config-file>.json --json
   ```
2. **Run repository verification gates:** `skill_frontmatter_gate.py`, `language_gate.py`, `privacy_gate.py`, `changed_skill_gate.py`, unit tests (`pytest`), and `ruff check`.
3. **Generate catalog artifacts instead of hand-editing:** On a clean checkout, run `python build_public_registry.py` and `python build_skills_map.py` (verify with `--check`).

## Compatibility with Anthropic format and ellmos components

All extra YAML frontmatter keys sit cleanly alongside `name` and `description`, so standard Claude Code installations consume produced skills unchanged. Likewise, the loader and auditor accept `ocean.skill-config.v2`, `ellmos.skill-config.v1`, and expressive domain-specific `.json` filenames seamlessly.

## Related skills

- `skill-creator:skill-creator` — generic interview, drafting, and eval workflow (Step 1).
- `skill-finder` — checks whether an existing local skill already covers the task before authoring a new one.
- `skill-explorer` — catalog-wide skill inventory and landscape audit.
- `skill-family-care`, `skill-register-care` — family header routing and registry maintenance after creation.
- `dual-use-software-design` — design standard for tools operable by both humans and LLMs.

## Changelog

### 0.4.1 (2026-11-27)
- Pragmatic refinement ("only where genuinely useful"):
  - `audit-skill` and the config loader recognize any expressive skill-specific `.json` configuration file (e.g. `models.local.json`, `routing-defaults.json`, `kalender-profiles.json`, `prefs.json`, `*.example.json`) alongside `default-config.json` (`config_files`, `has_external_config`).
  - Lean guideline, advisory, therapy, thinking, and router/umbrella skills that need no `.json` config, `templates/`, or `scripts/` achieve `100/100 conformant` (`recommendations == []`) with zero boilerplate.
  - Added CLI subcommand alias `init` plus `--config-name <file.json>`, `--no-templates`, `--no-scripts`, `--no-config`, and `--minimal`.

### 0.4.0 (2026-11-27)
- Renamed `ellmos-skill-creator` to `ocean-skill-creator` (preserving `/ellmos-skill-creator` transition alias), added 5-stage self-healing config cascade, report/template architecture (`html`/`pdf`/`md`/`txt`/`json`), and stdlib CLI `scripts/ocean_skill_scaffold.py`.

### 0.3.1 (2026-11-15)
- Step 1b: trigger belongs in the first 250 characters of `description`.

### 0.3.0 (2026-11-06)
- Step 1b: mandatory trigger-first `description` rule.

### 0.2.0 (2026-08-24)
- Added reusable learning contract and usecase-coverage file set.

### 0.1.0 (2026-08-24)
- Initial version as `ellmos-skill-creator`.
