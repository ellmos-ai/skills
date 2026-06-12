# Changelog

## Unreleased

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
