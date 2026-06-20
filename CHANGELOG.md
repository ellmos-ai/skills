# Changelog

## Unreleased

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
