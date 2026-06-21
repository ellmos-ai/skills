<img src="assets/banner_v2.svg" width="100%" alt="ellmos skills Banner">

# ellmos skills

**[🇩🇪 German version](README_de.md)** · **🇬🇧 English** · [Machine-readable context](llms.txt)

> Portable AI skill library for Claude Code-style `SKILL.md` workflows, Codex-compatible agent setups, BACH, and other local-first LLM agent runtimes.

[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Quick links:** [Start Here](#start-here) · [Featured Skills](#featured-skills) · [Skills](skills/) · [Conventions](docs/CONVENTIONS.md) · [Changelog](CHANGELOG.md)

This repository is the reusable skill catalog of the ellmos ecosystem. It contains standalone process skills, development workflows, research helpers, therapy-oriented methods, infrastructure playbooks, and utility tools in an Anthropic-compatible `SKILL.md` format. Each skill carries its own metadata directly in YAML frontmatter, so runtimes can inspect provenance, compatibility, and dependencies without a central registry.

## Start Here

| Need | File or command |
|---|---|
| Browse all public skills | [`skills/`](skills/) |
| Understand the `SKILL.md` schema | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) |
| Machine-readable catalog index | [`registry/components.json`](registry/components.json) |
| Browse by category | [`skills/`](skills/) (one subfolder per category) |
| Use a skill | Copy `skills/<category>/<name>/` into your agent's skills directory (e.g. `~/.claude/skills/`) |
| Review public changes | [`CHANGELOG.md`](CHANGELOG.md) |
| Give crawlers and LLM agents a compact map | [`llms.txt`](llms.txt) |

## Catalog Snapshot

The current public catalog contains 66 tracked runtime skills:

| Category | Count | Focus |
|---|---:|---|
| `dev` | 11 | Development protocols, debugging, bug sweeps, pipeline renovation, migration, documentation, plugin systems, repository publication |
| `education` | 3 | Academic planning, source-based learning, and exam preparation workflows |
| `game-dev` | 5 | Blender, Roblox, Rojo, Studio, asset safety, and game-design workflows |
| `infrastructure` | 3 | Portable AI setup, skill landscape management, MCP config sync between agent apps |
| `research` | 1 | Research-agent workflow support |
| `therapy` | 19 | German-language psychoeducation and counseling method playbooks |
| `utilities` | 11 | Batch operations, thinking frameworks, decision briefings, document chunking, encoding repair, YouTube transcripts |
| `web` | 1 | Web-reading protocol support |

## Featured Skills

Some skills are especially useful as entry points because they coordinate other tools, prevent messy agent workflows, or turn local procedures into repeatable playbooks:

| Skill | Why it stands out |
|---|---|
| [`skill-explorer`](skills/infrastructure/skill-explorer/SKILL.md) | Meta-skill for managing the skill landscape: audits existing skills, clusters them into families, researches external skills/plugins, and installs only after safety review and explicit approval. |
| [`model-strategy`](skills/dev/model-strategy/SKILL.md) | Multi-model routing for Claude, Codex, Gemini, and Ollama with score-based selection, delegation paths, escalation triggers, and cost/quality tradeoffs. |
| [`pipeline-optimizer`](skills/dev/pipeline-optimizer/SKILL.md) | Six-step renovation protocol for existing project folders, documentation systems, and software stacks; designed to avoid duplicate standards and broken workflows. |
| [`github-repo-care`](skills/dev/github-repo-care/SKILL.md) | Publication and maintenance gate for GitHub repos: local rules, locks, `.gitignore`, privacy checks, README/i18n, releases, and repository metadata. |
| [`mcp-config-sync`](skills/infrastructure/mcp-config-sync/SKILL.md) | Synchronizes MCP server configuration between Claude Code and Claude Desktop with a shared master file and Windows/macOS helper scripts. |
| [`video-transcriber`](skills/utilities/video-transcriber/SKILL.md) | Extracts video subtitles/transcripts plus metadata (supports YouTube sources) into Markdown, JSON, or plain text so video analysis starts from source-backed text. |
| [`roblox-studio`](skills/game-dev/roblox-studio/SKILL.md) | Covers Studio/Rojo scene-vs-code work, MCP control of Roblox Studio, asset-pipeline handoff, and mandatory malware checks for Creator Store assets. |
| [`using-blender`](skills/game-dev/using-blender/SKILL.md) | Routes Blender work between GUI, headless `bpy`, export/reimport checks, and reviewed MCP options without forcing a specific local setup. |
| [`decision-briefing`](skills/utilities/decision-briefing/SKILL.md) | Turns many open decisions into a numbered A/B/C/D briefing with recommendations, accepts batch replies, and records the chosen outcomes. |

## Education Skills

Three institution-neutral skills for academic study. Placeholders (`<INSTITUTION>`, `<LMS>`, `<MODULE_PREFIX>`, etc.) are resolved to the concrete context on first use. All three skills are available in German (base) and English; ES, JA, RU, ZH are planned for Stage 2.

| Skill | What it does |
|---|---|
| [`academic-study-control`](skills/education/academic-study-control/SKILL.md) | Semester planning, deadline tracking, exam registration, re-enrollment, mail/portal checks, and calendar reminders with source verification and privacy guardrails. |
| [`academic-study-learn`](skills/education/academic-study-learn/SKILL.md) | Five-phase source-based learning cycle: clarify objective → extract key ideas → build glossary → transfer/apply → retrieval practice with gap tracking. |
| [`academic-study-test`](skills/education/academic-study-test/SKILL.md) | Five test modes (quick test, exam block, oral exam, assignment training, error diagnosis) with a rubric-based assessment system and a strict ethics boundary against live-exam support. |

## Repository Structure

```text
skills/
  <category>/
    <skill-name>/
      SKILL.md              # Definition, frontmatter, usage workflow
      scripts/              # Optional executable helpers
      references/           # Optional supporting documents
  _templates/               # Templates for new skills
docs/
  CONVENTIONS.md            # Frontmatter specification
registry/components.json    # Machine-readable catalog index
llms.txt                    # Compact project map for LLM crawlers
```

## Skill Metadata

Every `SKILL.md` declares whether it works standalone, whether it is compatible with BACH, and where it came from:

```yaml
standalone: true
bach_compatible: true
bach_origin: true
provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/"
  origin_version: "1.0.0"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
```

Supported skill types are `skill`, `agent`, `expert`, `service`, `protocol`, and `tool`.

## Search Context

Use this repository when searching for:

- `ellmos skills`
- `ellmos-ai/skills`
- `agent skill library`
- `SKILL.md catalog`
- `portable AI skills`
- `Claude Code SKILL.md library`
- `Codex skills library`
- `Claude Code and Codex skills`
- `local-first LLM agent skills`
- `BACH skill catalog`
- `Anthropic-compatible skills`

The name is intentionally generic, so use the canonical repository string `ellmos-ai/skills` when linking or indexing this project. It is a reusable skill catalog, not an MCP server, hosted SaaS marketplace, prompt pack, or private skill installer.

## Related ellmos Projects

| Project | Role |
|---|---|
| [BACH](https://github.com/ellmos-ai/bach) | Full text-based LLM operating system |
| [Rinnsal](https://github.com/ellmos-ai/rinnsal) | Lightweight local-first LLM agent infrastructure |
| [USMC](https://github.com/ellmos-ai/usmc) | Shared memory primitive for agent systems |
| [Gardener](https://github.com/ellmos-ai/gardener) | Database-based operating-system counterpart |
| [MarbleRun / llmauto](https://github.com/ellmos-ai/MarbleRun) | LLM chain-execution framework |

## License

MIT License. See [LICENSE](LICENSE).

## Liability

This project is an unpaid open-source donation. Liability is limited to intent and gross negligence under Section 521 of the German Civil Code. Use at your own risk. No warranty, maintenance guarantee, availability guarantee, or fitness-for-purpose guarantee is provided.
