# Changelog

## Unreleased

### Added (2026-06-13)

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
