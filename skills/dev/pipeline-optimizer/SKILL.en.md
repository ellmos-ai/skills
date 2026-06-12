---
name: pipeline-optimizer
version: 1.2.0
type: protocol
author: Lukas Geiger (method) + Claude (write-up)
created: 2026-05-16
updated: 2026-06-13
aliases: [project-folder-optimizer, pipeline-renovator, project-renovator]
description: >
  Structured 6-step procedure for improving, renovating, or rebuilding existing pipelines, individual project folders, documentation structures, or software stacks. Addressable as "pipeline optimizer" (for whole topic pipelines, e.g. a software, research, or game-dev pipeline) or "project-folder optimizer" (for individual project folders within a pipeline, e.g. a single software tool or paper project). Triggers on tasks like "improve pipeline X", "optimize the stack", "rebuild Y", "renovation", "pipeline refactoring", "clean up project folder", "improve folder structure", "unify conventions", "documentation consolidation", "integrate into existing system", or any substantial intervention in established structures. Delivers building-stock analysis, purpose clarification, ideal sketch, gap plan, empirical pain-point identification, and retests with fresh subagents. Prevents parallel standards, duplication, and pipeline breaks.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [pipeline, renovation, refactoring, stack, workflow, lessons-learned]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/pipeline-optimizer/"
  origin_version: "1.1.1"
  last_sync_from_origin: "2026-05-16"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Pipeline Optimizer / Project-Folder Optimizer

**6-step renovation without incompatibilities** — applicable at two scales:

| Trigger name | Scope | Example |
|---|---|---|
| **Pipeline optimizer** | Whole pipelines, stacks, documentation structures | Your topic pipelines, e.g. `software/`, `research/`, `games/`, an agent system |
| **Project-folder optimizer** | Individual project folders within a pipeline | A software tool, a paper project, a game project |

A **pipeline** here means a topic-oriented top-level structure in which multiple projects live under shared conventions (e.g. a software pipeline with release rules, a research pipeline with a publication procedure).

Both use the same 6-step workflow — the only difference is the **scope** (pipeline-wide vs. single project) and, accordingly, the depth of the building-stock survey in step A.

## When this skill applies

The skill applies as soon as you are asked to improve, rebuild, or extend an **existing** structure — not for greenfield construction. Concrete triggers:

**Pipeline level** (scope: whole pipeline):
- "Make pipeline X better"
- "Optimize the stack"
- "Renovate the software pipeline"
- "Documentation consolidation in the research pipeline"
- Substantial intervention in a topic pipeline, central `_tools/`, or system components

**Project-folder level** (scope: single project folder):
- "Clean up / optimize project folder X"
- "Improve the folder structure in Y"
- "Refactor a single tool"
- "Unify a paper-project setup"
- "Align a game project folder with the pipeline standard"

**Cross-cutting:**
- "Rebuild X / integrate it into existing Y"
- "Refactoring", "consolidation"
- "Unify conventions"
- "Integrate into an existing system"

## The building-stock metaphor

Renovating a house first requires knowing **what it is made of** (stone, wood, plastic), **what it is for** (mountain hut, software forge), and **where it already fulfills functions**. The same discipline applies to pipelines.

---

## Procedure — 6 steps (do NOT skip, do NOT reorder)

### Step A — Survey the building stock

**Question:** What is the house made of?

**Pipeline scope** (all root docs + tools + templates):
- [ ] **Read all root documents completely** (not just snippets/insertion points)
- [ ] Go through template folders (`_templates/`, `_TEMPLATES/`) and tool folders (`_tools/`)
- [ ] Policy files: e.g. GITHUB-POLICY.md, RELEASE-MANAGEMENT.md, QUALITY_RULES.md, NAMING-SYSTEM.md, publication procedures, …
- [ ] Status snapshots: e.g. PROJECT_STATUS.md, status overviews, releases.json, registry files
- [ ] Checklists: e.g. release checklists, build/PDF checklists
- [ ] Workflows: AGENTS.md, GUIDE.md, SKILL.md
- [ ] Lessons-learned files: LESSONS_LEARNED.md, MEMORY.md, loop-state files

**Project-folder scope** (single-project substance + relevant pipeline conventions):
- [ ] **Read all markdown and control files in the project folder** (README, CHANGELOG, TASKS/TODO, DONE, CONCEPT, action plan, proof notes, …)
- [ ] **Survey the code structure:** src/, tests/, build configuration (pyproject.toml, requirements.txt, project manifests, toolchain files, …)
- [ ] **Take the parent pipeline's conventions into account** (e.g. for a software project: GitHub policy, naming system, release management, templates)
- [ ] **Scan existing tools/scripts in the project** (`_tools/`, `_scripts/`, build_*.bat, START scripts)
- [ ] **Configuration files:** `.gitignore`, LICENSE, NOTICE, SECURITY.md, CODE_OF_CONDUCT.md

**Anti-pattern:** Using `grep -l "<keyword>"` to find insertion points and inserting there without knowing the file's context.

**Output:** Inventory note with all relevant conventions, tools, and templates at the chosen scope.

### Step B — Identify the purpose

**Question:** What does the house exist for?

State the purpose explicitly in 1-2 sentences.

**Pipeline examples:**

| Pipeline | Purpose |
|---|---|
| Software pipeline | Develop, test, and release desktop apps + browser tools to stores/GitHub |
| Research pipeline | Write scientific papers, peer-review them, publish to repositories/preprint servers |
| Game pipeline | Develop games and publish them on the target platform |
| Agent system | LLM system for multi-agent orchestration |

**Project-folder examples:**

| Project folder | Purpose |
|---|---|
| `software/PlannerApp` | Planning desktop app, commercial, private repo |
| `research/CosmologyModel` | Model paper series + numerical computations |
| `games/SortingChaos` | Sorting game, alpha stage, level progression |

The purpose **steers every intervention** — measures that do not serve the purpose are dropped.

### Step C — Sketch the ideal picture

**Question:** What would a perfect house for this purpose look like?

- Sketch it from your own perspective (short, max. 10 points)
- Bring in a best-practice comparison (e.g. Vercel stack for SaaS, scientific-python stack for research)
- Do not descend into detail optimization — a top-level sketch is enough

**Output:** 5-10 points "ideal state per pipeline"

### Step D — Gap analysis + plan

**Four questions per pipeline:**

1. **What does the house already have?** — Even if solved differently from the ideal but **functionally equivalent**.
   *Example:* The ideal says "pip-licenses for third-party licenses". Reality: a custom generator script wraps it → functionally equivalent, no intervention needed.

2. **What impedes the function?** — Existing structures that cause breaks or extra effort today.

3. **What is non-functional?** — Dead code, outdated conventions, unused tools.

4. **What would measurably improve functions?** — Concrete interventions with expected benefit.

→ From this, a **concrete plan**:
- What gets **newly built**?
- What gets **extended**?
- What gets **demolished**?
- What stays **unchanged** (important to name!)

**Output:** Plan table with columns *Intervention* / *Existing* / *Measure* / *Rationale*

### Step E — Work empirically

Do not only plan top-down — collect pain points:

- [ ] **Known bugs**: issue tracker, TASKS/TODO/DONE files
- [ ] **Error history**: lessons-learned files, bugfix logs, check registries
- [ ] **Automation breaks**: "What do I always have to do manually?"
- [ ] **User interview**: ask specifically — pain points, wishes, workarounds
- [ ] **Self-test**: walk through the pipeline (create a new project, run a build, simulate a release) — where does it break?

The empirically found pain points **prioritize the plan** from step D.

### Step F — Retests after implementation

- [ ] Commission **fresh subagents** (unburdened by the renovation context) to walk through the changed workflow
- [ ] **Measurable before/after values**: setup time, error rate, number of manual steps, build time
- [ ] **Anti-regression check**: do existing workflows still work after the change?
- [ ] If there is **no measurable improvement** or a regression: **roll back** the renovation or readjust

## Anti-patterns (forbidden)

| Anti-pattern | Damage | Antidote |
|---|---|---|
| Searching insertion points instead of reading docs | Parallel standards | Step A in full |
| Transferring "best practice from X" 1:1 | Incompatibility | Step D compares functionally |
| Creating a new file without checking conventions | Duplication (e.g. NOTICE.md ↔ THIRD_PARTY_LICENSES.txt) | Step A + step D |
| Planning top-down without empirics | Solution misses the pain point | Step E before finalizing the plan |
| Not testing your own change | Undetected regression | Step F with a fresh agent |
| "Clarify later" with unclear status | User discovers the conflict afterwards | When unsure, walk step D through with the user again |

## Case study — the NOTICE.md incident

**Assignment:** Implement pipeline improvements across several topic pipelines (software, research, games).

**Mistake:** Step A skipped — only insertion points searched instead of reading the full policy files.

**Consequence:** `NOTICE.md` introduced as a "new license file" in 7 files, although `THIRD_PARTY_LICENSES.txt` + a custom license generator (wrapper around `pip-licenses`) were already established — documented in the pipeline's GitHub policy (mandatory files + license checklist). All software projects already had THIRD_PARTY files.

**Detection:** Only after the user asked ("I'm fairly sure we already had rights management").

**Correction:** NOTICE.md removed from the project template, 6 further files adjusted, the existing license generator referenced instead of `pip-licenses`.

**Lesson:** Had step A been executed in full, the conflict would have been detected before writing.

## Rules of thumb

1. **For "improve the pipeline", first read as long as you write.**
2. **No new standard without proof that no existing one exists.**
3. **Use existing tools/wrappers instead of new parallel ones.**
4. **"More of the same" is usually worse than "extend what exists".**
5. **Rolling back on conflict** is always better than running two parallel standards.

## Completion checklist

Before reporting a pipeline renovation as "done":

- [ ] Step A: all relevant root docs read?
- [ ] Step B: pipeline purpose stated in 1-2 sentences?
- [ ] Step C: ideal picture sketched (5-10 points)?
- [ ] Step D: gap analysis with table (what stays / what is extended / what is new / what goes)?
- [ ] Step E: empirics checked (bugs, lessons, self-test, user interview)?
- [ ] Plan agreed with the user?
- [ ] Step F: tested with a fresh subagent — improvement measurable?
- [ ] No parallel standards introduced?
- [ ] On conflicts: rolled back or honestly accounted for?

## Optimal project-folder structure (for the project-folder optimizer)

When the skill is applied to **a single project folder**, the following combined recommendation helps as an ideal reference (step C):

### Anthropic standard (Claude Code)

| File/folder | Function |
|---|---|
| `CLAUDE.md` (root) | Auto-loaded by Claude Code, project-specific instructions |
| `.claude/settings.json` | Permissions, env vars, model selection (committed) |
| `.claude/settings.local.json` | Local overrides (do NOT commit, add to `.gitignore`) |
| `.claude/commands/*.md` | Custom slash commands |
| `.claude/agents/*.md` | Custom subagents |
| `.claude/skills/<name>/SKILL.md` | Project skills |

### Your own project-docs template (recommended)

If you maintain your own project documentation template (e.g. under `<your-workspace>/_templates/project-docs/`), **three build-out profiles** pay off. Example split: **MINIMAL** provides the session core set with 7 root files (`AGENTS.md`, `CLAUDE.md`, `README.md`, `START.md`, `STATE.md`, `TODO.md`, `DONE.md`) plus `_tools/`. **STANDARD** adds `CHANGELOG.md`, `DECISIONS.md`, and `PATTERNS.md`. **FULL** expands to 14 root files and additionally adds `ARCHITECTURE.md`, `WORKFLOWS.md`, `TOOLS.md`, `GLOSSARY.md` as well as `workflows/` and `.github/`.

→ **Use such a template as the base for new projects** (copy instead of creating manually).

### Pipeline-specific additions (examples)

Depending on the pipeline, further mandatory files come on top — typical patterns:

- **Software project:** LICENSE, CODE_OF_CONDUCT.md, SECURITY.md, CONTRIBUTING.md, THIRD_PARTY_LICENSES.txt (generated), pyproject.toml/requirements.txt, entry in the pipeline's central release registry. → If available: use the pipeline's cookiecutter template.
- **Research project:** concept document, action plan, publication plan, archive/source/result/data folders (`_archive/`, `_sources/`, `_results/`, `_data/`), `paper/` for LaTeX. For proof projects: a proof-note file with the proof chain and status.
- **Game project:** project manifest and toolchain files of the engine (e.g. for Roblox/Rojo: default.project.json, rokit.toml, wally.toml, selene.toml), game design document, `src/{server,client,shared}/` per engine convention.

### Full detail reference

→ See **`references/optimal-project-structure.md`** in this skill folder (German). Contains:
- Example `settings.json` (Anthropic schema)
- Mandatory `.gitignore` entries
- Anti-patterns (what does NOT belong in project folders)
- Recommended workflows per pipeline type (software/research/game)
- YAML header convention for documentation files
- Auto-check sketch

## Related skills (when to use instead of this one?)

| Skill | When to use |
|---|---|
| **`project-onboarding`** | Take an EXTERNAL existing repo into your own system |
| Project bootstrapper (if available) | Create a NEW project in an existing pipeline (greenfield, no rebuild) |
| Pipeline bootstrapper (if available) | Create a COMPLETELY NEW pipeline (rare case) |
| System onboarding (if available) | Set up a new machine |

The **pipeline optimizer** is responsible for **renovation**, not new construction or adoption. If your skill collection has a skill index, search it for matching bootstrapping skills.

## Cross-references

- Detail reference: `references/optimal-project-structure.md` (in this skill folder)
- Anthropic Claude Code docs: `https://docs.claude.com/en/docs/claude-code`
- If available: global user rules (e.g. a "renovations" section in your `~/CLAUDE.md`) and pipeline-specific stack descriptions

## Scope choice: pipeline vs. project folder

If it is unclear which scope is meant, **clarify before step A**:

| Clue | Scope |
|---|---|
| "Improve the whole software pipeline" | Pipeline |
| "Clean up the folder of tool X" | Project folder |
| "Synchronize the central release registry" | Pipeline (central asset) |
| "Refactor the AssetBuilder in game Y" | Project folder |
| "Introduce a check convention pipeline-wide" | Pipeline |
| "Create a check file in project Z" | Project folder |

At **project-folder scope**, additionally always briefly check the parent pipeline's conventions (step A extended) so the intervention stays compatible with the pipeline.

---

## Changelog

### 1.2.0 (2026-06-13)
- First publication in the skill library: personal paths, concrete pipeline/project names, and references to private skills replaced with generic examples; the procedure itself (6 steps, anti-patterns, case study, checklists) unchanged

### 1.1.1 (2026-06-01) and earlier
- Internal versions (private skill directory, before publication)
