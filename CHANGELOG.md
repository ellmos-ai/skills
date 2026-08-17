# Changelog

## 2026-08-17

- **orchestrator skill 1.2.0** (`skills/infrastructure/orchestrator/`):
  - Added optional resource-profile layer: `profiles.json` (named profiles `solo`/`spar`/`burst`) and `config.json` (active profile, overrides, session override) alongside `SKILL.md`.
  - Added optional token-credit-driven auto profile switching (`config.json.token_tracker`) that recycles an existing tracker instead of building a new one — read-only, no process spawn, two-threshold hysteresis, fail-closed on unreadable state.
  - Neutrality preserved: without both files the skill behaves exactly as before (documented spar-profile default); the canonical `config.json` ships with the tracker disabled and no host paths — real paths belong only in each user's local copy.
  - `registry/components.json` version bumped to `1.2.0`.

## 2026-08-16

- **Discoverability, README-Design, Badges & Metadata Parity Check (Pfad B)**:
  - Standardized project packaging with PEP 621 compliant `pyproject.toml` (`[project]`, `[tool.pytest.ini_options]`, `[tool.ruff]`).
  - Added automated metadata, manifest, and component parity test suite (`testing/test_metadata.py`) verifying schema v1 integrity, component existence, `llms.txt` synchronization, and multilingual README consistency.
  - Synchronized Shields.io badges in `README.md` and `README_de.md` (Pytest: 100 passed, Python >=3.10, `ellmos-ai` ecosystem, `open-bricks` umbrella, 132 public catalog components / 376 tracked skills, `llms.txt`).
  - Integrated interactive bilingual Mermaid System Architecture and execution fabric diagrams in both English and German READMEs.
  - Linked sibling tools and ecosystem matrix (`BACH`, `ellmos-core`, `ellmos-controlcenter-mcp`, `system-explorer`, `workflowhooker`, `sqlite-transit-sync`, `DevCenter`, `CodeBox`).
  - Updated `llms.txt` with latest 2026-08-16 timestamp, 100 passing tests, and updated category breakdown.
  - Rebuilt public catalog index `registry/components.json` with 132 public skills.
  - Verified full test suite 100% green (100 passed, 180 subtests passed in pytest; ruff check 100% clean).

## 2026-08-06

- **New skill: `piggyback-hosting`** (`skills/dev/piggyback-hosting/`): migrated from the standalone `lukisch/huckepack` repository. Hosting pattern for making a locally-built application safely hostable without building user management (host stores nothing, visitor's browser stores everything). Ships `references/DATA-FLOW-TEMPLATE.md`, `references/PRIVACY-TEMPLATE.md` and `references/RECHT.md` (German first-look legal assessment, GDPR/TDDDG/UWG). Rebuilt `registry/components.json` and `SKILLS-MAP.md` (116 components).

## 2026-08-03

- **Technical Hygiene & Maintenance Check (Pfad A)**: Synchronized `llms.txt` timestamp to 2026-08-03 and test assertion count (86 passed).
- **Public Registry & Test Suite Refinement**: Updated `build_public_registry.py` and `testing/test_public_registry.py` to filter out archived directories (`_archive`) and non-public visibility skills (`private-only`). Rebuilt `registry/components.json` and `SKILLS-MAP.md`. Verified test suite 100% green (86/86 passed).
- **Documentation Badges**: Added `Pytest: 86 passed`, `ellmos-ai` ecosystem, and `open-bricks` umbrella Shields.io badges to `README.md` and `README_de.md`.

## 2026-07-30

- Restored the public/private boundary after an early publication: neutral
  public method cores remain in this repository, while personal profiles,
  Store-operator workflows, app-specific adapters, databases, local paths, and
  personal defaults live in a separate private No-Push repository.
- Split the education workflow explicitly: `foerderplaner` handles teaching and
  support planning, the separate public `report-forge` project handles general
  report generation, and personal support-report templates remain private.
- Added a CI privacy gate for concrete user-home paths, known private hosts,
  token patterns, and accidentally tracked ignored files.
- Removed 19 imported HyperFrames skills from the public catalog. They are not
  Ellmos-authored and are retained only in a private vendor area with their
  actual HeyGen/HyperFrames provenance and Apache-2.0 license.
- Replaced the internal 142-component registry with a minimal public
  120-component discovery index. Ownership assessments, privacy
  classifications, branch data, warnings, and the full maintainer registry
  remain private.
- Rebuilt `SKILLS-MAP.md`, all six root README language versions and `llms.txt`
  from the 120 skills that are actually public.
- Added genuine German translations for the six infrastructure skills whose
  former `SKILL.de.md` files incorrectly contained English.
- Embedded existing skill banners consistently in the matching `SKILL*.md`
  language files. Skills without a banner asset remain unchanged.
- Rewrote the public `master` history to remove prematurely published private
  workflows, third-party skill copies, translation scratch scripts, and
  concrete local user/host markers.
- **Education Category Deep Multilingual Expansion**: Completed 100% deep, localized sentence-by-sentence multi-language translation (DE, EN, ES, FR, JA, ZH, RU) across all 5 skills in `skills/education/` (`academic-study-control`, `academic-study-learn`, `academic-study-test`, `foerderplaner`, `worksheet-generator`).
- **Metacognitive Skill & Injector Enhancements**: Integrated Baddeley's Working Memory (State + Hooks), Miyake's Central Executive functions (Inhibition, Shifting, Updating), CBT Cognitive Restructuring, ACT Defusion, Pre-Flight Goal Checklists, and Mandatory External Provider Sign-off into `skills/infrastructure/metacognitive-injectors` and `agy_metacognitive_prompt_injector.py`.

## 2026-07-28


- Refreshed the public catalog surfaces to 83 tracked skills / 108 definitions
  and regenerated the 83-component registry, including the two previously
  omitted After-Care skills.
- Extended the privacy gate for local catalog-analysis output and the
  host-specific `sync-procedure` skill so neither can enter the public repo
  accidentally.
- Added `automation-self-care` 1.0.0: provider-neutral discovery, planning and
  staged installation of a self-maintaining scheduler core set derived from the
  original ANTIGRAVITY maintenance family and its later F1-F6 adaptations.
- Added `semantic-persona-routing` 1.0.0: portable coordinator-role, expert,
  persona and live-skill routing maps with exact provenance resolution,
  conservative candidates and visible endpoint gaps.
- Updated catalog documentation to 82 tracked skills / 107 definitions and
  verified the complete suite with 52 passing tests.

## 2026-07-27

- `agent-config-sync` 0.3.0: provider/app-class discovery, topology offers and
  user-selected single or multi-file truth.
- `mcp-config-sync` 2.0.0: provider-neutral MCP entry point; the former Claude
  pair is now an explicit legacy profile.
- `agents-bridge` 2.0.0: removed the implicit personal CLAUDE.md/OneDrive truth,
  added neutral boot-surface discovery, ordered user-selected truth profiles
  and a read-only loader renderer.
- Refreshed public catalog counts to 80 tracked skills / 105 definitions and
  the verified test badge to 46 passing pytest tests.

## Unreleased

### Added (2026-07-29)

- `letter-hooker` 1.0.0: Extension of `automation-self-care` for prompt-level preflight bootloaders, document traversal, and self-healing context enrichment for systems without native JSON event-hooks (e.g. Antigravity / Gemini CLI).
- `staircase-routing` 1.0.0: Isolated navigation and routing strategy for searching upward and downward for signpost documents (`CLAUDE.md`, `AGENTS.md`, `README.md`) and user-configurable buzzwords.
- `wayfinding-routing` 1.0.0: Universal LLM navigation, self-orientation, and emergency recovery skill. Integrates synonym strategies: `survival-routing`, `dead-reckoning`, `pathfinder-routing`, and `celestial-routing`.
- **Stage 2 Translation Expansion**: Completed 1:1 German & English bilingual coverage across 100% of skills (116/116 skills at Stage 2).
- **Stage 3 Multilingual Expansion**: Elevated 100% of skills across the entire library to Stage 3 Multilingualism by adding Spanish translations (`SKILL.es.md`).
- **Full Stage 3+ Multi-Language Expansion**: Completed full 7-language coverage across 100% of skills (116/116 skills now available in DE, EN, ES, FR, JA, ZH, RU).

### Maintenance & Discoverability (2026-07-27)

- Updated `llms.txt` header (`Last-checked: 2026-07-27`) and documented test suite verification (56 passing test suite assertions, 100% green).
- Added Shields.io test suite badges (56 passed tests) to `README.md` and `README_de.md`.
- `catalog.py`: Normalized `fm["_path"]` using `.as_posix()` so that relative skill directory paths on Windows do not produce backslashes (`\`), preventing malformed category names in catalog listings.

### Maintenance & Discoverability (2026-07-26)

- Synchronized catalog metadata and README tracked skill counts (79 tracked runtime skills in 10 categories, 104 total catalog definitions).
- Updated `llms.txt` header (`Last-checked: 2026-07-26`), dev category skill count (15), and agent search context.
- Added visual Shields.io badges (Python 3.10+, 79 Tracked Skills, LLM-Ready llms.txt, Catalog Quality 4.8/5) to `README.md` and `README_de.md`.
- Added GFM `[!NOTE]` callout box for AI Agent & LLM Integration in both English and German landing pages.
- Added Mermaid System Architecture diagram visualizing `catalog.py` -> 10 Categories -> `SKILL.md` -> LLM Runtimes.

### Added (2026-07-23)

- 12 skills published after a full publication audit of the private skill pool
  (privacy-checked, user-neutralized, both validation gates green):
  - New category `assist` (9): `dev`, `dossier-briefing`, `kalender`,
    `location-suche`, `medizin-daten`, `reiseroute`, `tageszeitung`,
    `transkription`, `wetter` — key-free personal-assistant skills built on
    free/open endpoints (wttr.in, OSM/Nominatim/OSRM) or local SQLite stores.
  - New category `production` (1): `textproduction` — text-production router
    with a local LaTeX press-release compiler.
  - `game-dev/using-blender` — general Blender workflow for AI agents.
  - `utilities/privat-mail-writer` — privacy-by-design private-mail drafting
    with lazy, data-sparing per-contact style profiles.
  - Catalog grows 64 -> 76 tracked runtime skills; registry, README catalog
    tables, `SKILLS-MAP.md`, and `llms.txt` updated accordingly.
- `utilities/bewerbungsexperte` published after explicit owner decision
  (end-to-end job-application support with a database/folder-driven ASCII CV
  generator, standalone since v1.1) — catalog now 77.
- README (EN/DE): six additions to Featured Skills (`research-agent`,
  `agent-config-sync`, `dev-soft-agent`, `llm-text-hygiene`, `idea-mining`,
  and the 19-skill `therapy/` collection) based on a quality re-rating of the
  whole public catalog.
- README (EN/DE): monochrome 16px SVG icons for every category row and every
  Featured Skills entry (`assets/icons/`, 31 icons, neutral gray so they work
  in both GitHub themes).
- Banner rollout started: every skill will gradually receive its own banner
  (`banner.png`, 1200x300, embedded after the frontmatter in `SKILL.md`; design
  family matches the repository banner). First wave: all 20 featured skills
  plus a collection banner for `skills/therapy/`. New "Banner" section in
  `docs/CONVENTIONS.md`.

### Fixed (2026-07-23)

- `testing/skill_tester.py`: stdlib classification — `wave`, `__future__`,
  `ast`, `queue`, `zipfile`, `tarfile`, `gzip`, `pickle`, `array` are no longer
  miscounted as external pip dependencies in S003.

- `registry/components.json` regenerated (61 → 64 components): the three pointer
  skills `law-checker`, `steuer-assistent`, and `worksheet-generator` were tracked
  but missing from the catalog index. `llms.txt` skill count updated accordingly
  (61 → 64). All 64 skills validate against their type-matched schemas.

### Fixed (2026-07-13)

- `llms.txt`: Skill-Gesamtzahl korrigiert (66 → 61 getrackte Runtime-Skills, entsprach
  bereits `README.md`/`README_de.md`). Wird künftig über ein internes `readme-sync`-Tool
  gegen den git-getrackten Bestand geprüft, um erneute Zähl-Drift zu vermeiden.

- `utilities/video-transcriber`: YouTube-URL-Erkennung prüft jetzt exakte
  Hostnamen oder vertrauenswürdige Subdomains statt freier Suffix-Treffer.
### Added (2026-06-20)

- New public skill `game-dev/using-blender` 1.0.0 (user-agnostic Blender workflow routing across GUI, headless `bpy`, export/reimport validation, and reviewed MCP options; DE). Catalog counts updated to 66 public skills (game-dev 5) in `README.md`, `README_de.md`, and `llms.txt`.
- New private skill `game-dev/build-assets-with-blender` 1.0.0 for the local Roblox/game-asset pipeline; it is intentionally listed in `.gitignore` and not part of the public catalog.

### Changed (2026-06-20)

- Renamed `utilities/yt-transcriber` → `utilities/video-transcriber` (v1.1.0): YouTube branding
  policy prohibits „yt" as an abbreviation in product/tool names; script renamed from
  `yt_transcriber.py` to `video_transcriber.py`; usage disclaimer and dependency licenses
  (MIT / Unlicense) added; YouTube referenced descriptively only. Backward-compat wrapper
  `skills/utilities/yt-transcriber/yt_transcriber.py` retained for old references.
  Root `README.md` entry updated; `SKILL.md` + `SKILL.en.md` debrand to `video-transcriber`.

### Added (2026-06-20) — Versionierungs-Kern (Etappen 5, 6, 8)

- `versionctl.py` 1.0.0 (Etappe 5): Neues CLI mit vier Befehlen: `status` (Drift skills/ vs. Registry), `validate` (Skills gegen skill-v1-Schema + CONVENTIONS prüfen), `inventory` (reproduzierbarer Inventory-Report ohne absolute Pfade), `registry-generate` (produktive Registry aus realem Skill-Bestand erzeugen). Stdlib-only, kein externer JSON-Schema-Validator, eigener Inline-Validator mit allOf/$ref-Unterstützung. 22 pytest-Tests in `testing/test_versionctl.py` (tmp_path-Fixtures, keine echten Dateisystem-Zugriffe).
- `registry/components.json` + `registry/forks.json` + `registry/branches.json` + `registry/releases.json` + `registry/deployments.json` (Etappe 8): Produktive Registry, auto-generiert aus 52 öffentlichen Skills via `versionctl registry-generate`. Gitignorierte private Skills werden durch `git ls-files`-Filter automatisch ausgeschlossen. Schema-valide, reproduzierbar, privatsicher (kein absoluter Systempfad).
- `templates/SKILL.md`, `templates/PROMPT.md`, `templates/WORKFLOW.md`, `templates/AGENT.md` (Etappe 6): Neue Komponenten-Templates mit vollständigem Frontmatter (Pflichtfelder + Provenance-Block gemäß CONVENTIONS.md und Konzept). Additiv — keine bestehenden Skills geändert.
- `testing/test_versionctl.py`: 22 Tests für versionctl (Schema-Validation positiv+negativ, Registry-Generierung, Reproduzierbarkeit, Drift-Erkennung, Inventory-Privatsicherheit, Pfad-Leak-Check).

### Added (2026-06-20)

- New skill `education/academic-study-control` 1.0.0 (institution-neutral semester and deadline management: source-checked planning, optional calendar and mail integration, privacy-first data handling; fully generic placeholders for institution, LMS, module prefix, and status files; DE).
- New skill `education/academic-study-learn` 1.0.0 (source-based learning workflow: five-phase cycle of goal-setting, core-idea extraction, glossary, transfer, and retrieval practice; works with any field of study and material type; DE).
- New skill `education/academic-study-test` 1.0.0 (exam and test preparation: five modes — quick test, exam block, oral exam, assignment training, error diagnosis — with a five-criterion scoring rubric and strict ethics boundary against supporting live exams; DE).
- Catalog counts updated to 65 skills (education +3) in `README.md`, `README_de.md`, and `llms.txt`. `education` category added to public catalog in all three files.

### Added (2026-06-18)

- New skill `dev/github-repo-care` 1.0.0 (safe GitHub repository creation and maintenance workflow: local rules, locks, `.gitignore`, privacy gate, README/i18n/banner/metadata, release tag, GitHub release, CI verification, organization profile links, `llms.txt`, and registry updates; DE+EN). Catalog counts updated to 45 skills (dev 11) in `README.md`, `README_de.md`, and `llms.txt`.

### Added (2026-06-13)

- New skill `utilities/decision-briefing` 1.0.0 (work through many open decisions on one topic: capture and inventory, numbered briefing with A/B/C/D options and a marked recommendation, letter/batch answers like "1A 2C 3B", results table and write-back into source documents; ported from the BACH expert `decision-briefing`, scanner component deliberately removed; DE+EN). Catalog counts updated to 44 skills (utilities 11) in `README.md`, `README_de.md`, and `llms.txt`.
- New skill `utilities/structured-thinking` 1.0.0 (meta-skill combining think, brainstorm, and decide into a 3-phase workflow: analyze, ideate, decide; DE+EN). Catalog counts updated to 43 skills (utilities 10) in `README.md`, `README_de.md`, and `llms.txt`.
- New tool `skill_sync.py`: deploy/drift CLI between the repo (source of truth, `skills/<category>/<name>/`) and the local deployment (`~/.claude/skills/<name>/`, flat). Commands: `status` (drift report), `deploy [skill ...] [--dry-run]`, `diff <skill>`. Understands the local deregistration pattern (`SKILL.md` deployed as `CONTENT.md`) and a hold list (`.sync-hold`) for deliberate local forks; never deletes target-only skills. Tests in `testing/test_skill_sync.py` (24 cases, tmp-path fixtures).
- `dev/bugsweep` 1.1.0: backported the model rule for final review (newer model classes self-verify via tests + a real smoke run; no external review needed) from the local installation, DE+EN.
- New skill `dev/bugsweep` (systematic bug sweep with codebase-scaled target, doubling escalation, area tracking; published with full frontmatter, DE+EN).
- New skill `dev/pipeline-optimizer` 1.2.0 (6-step renovation procedure for pipelines and project folders; published with generic example structures instead of personal pipeline names, DE+EN, incl. `references/optimal-project-structure.md`).
- New skill `infrastructure/mcp-config-sync` 1.0.1 (MCP server sync between Claude Code and Claude Desktop; scripts and template use `%USERPROFILE%`/`$HOME` placeholders, DE+EN).
- `dev/dev-cycle` 1.1.0: new "phase-specific skills" table linking project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol, and bugsweep (DE+EN).
- English versions (`SKILL.en.md`) for `therapy/systemisch-loesungsfokussiert` and `utilities/yt-transcriber`; `dev/model-strategy` English version updated to 2.0.0.
- Catalog counts updated to 42 skills (dev 10, infrastructure 2) in `README.md`, `README_de.md`, and `llms.txt`.

### Added

- New skill `therapy/systemisch-loesungsfokussiert` (SFBT + systemic questioning, merged from `solution-focused-therapy` and `systemic-questioning`).
- New `SKILL.md` for `utilities/yt-transcriber` (was the only published skill without one).
- `model-strategy` 2.0.0: cross-agent delegation (Gemini, Codex, Ollama), advisor pairing, reachability matrix (examples use generic placeholders).
- `catalog.py`: `--language` filter, portable subprocess invocation of `skill_tester.py`.
- Cross-reference ("Siehe auch") sections and content deduplication across 12 therapy and 3 utilities skills.

### Fixed

- `testing/skill_tester.py`: crash (`ValueError`) when invoked with a relative skill path; paths are now resolved before `relative_to`.
- Catalog counts in `README.md`, `README_de.md`, and `llms.txt` updated to 39 skills; removed stale `skills/_examples/` listing (example moved to `skills/web/web-reading/`).

### Added (2026-06-11)

- Added current discovery metadata for LLM crawlers, including `Last-checked: 2026-06-11`, audience notes, and additional `SKILL.md` search phrases.
- Clarified that the repository is a portable skill catalog rather than an MCP server, SaaS marketplace, prompt pack, or private installer.

### Documentation

- `llms.txt`: `## Last-checked: 2026-06-11` als ersten Header gesetzt; `## Search Phrases` als fenced code block standardisiert (war Prosa-Absatz).
