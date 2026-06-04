# ellmos skills

[German version](README_de.md) | [Machine-readable context](llms.txt)

**Portable AI skill library for Claude Code-style `SKILL.md` workflows, Codex-compatible agent setups, BACH, and other local-first LLM agent runtimes.**

This repository is the reusable skill catalog of the ellmos ecosystem. It contains standalone process skills, development workflows, research helpers, therapy-oriented methods, infrastructure playbooks, and utility tools in an Anthropic-compatible `SKILL.md` format. Each skill carries its own metadata directly in YAML frontmatter, so runtimes can inspect provenance, compatibility, and dependencies without a central registry.

## Start Here

| Need | File or command |
|---|---|
| Browse all public skills | [`skills/`](skills/) |
| Understand the `SKILL.md` schema | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) |
| List skills locally | `python catalog.py list` |
| Filter by category | `python catalog.py list --category dev` |
| Check provenance and sync state | `python catalog.py sync-status` |
| Create a new skill skeleton | `python catalog.py create "my-skill" --category utilities --type skill` |
| Give crawlers and LLM agents a compact map | [`llms.txt`](llms.txt) |

## Catalog Snapshot

The current public catalog contains 37 runtime skills:

| Category | Count | Focus |
|---|---:|---|
| `dev` | 8 | Development protocols, debugging, migration, documentation, plugin systems |
| `infrastructure` | 1 | Portable AI setup and operating-system support |
| `research` | 1 | Research-agent workflow support |
| `therapy` | 18 | German-language psychoeducation and counseling method playbooks |
| `utilities` | 8 | Batch operations, thinking frameworks, document chunking, encoding repair |
| `web` | 1 | Web-reading protocol support |

## Repository Structure

```text
skills/
  <category>/
    <skill-name>/
      SKILL.md              # Definition, frontmatter, usage workflow
      scripts/              # Optional executable helpers
      references/           # Optional supporting documents
  _templates/               # Templates for new skills
  _examples/                # Example skills
docs/
  CONVENTIONS.md            # Frontmatter specification
catalog.py                  # CLI for listing, filtering, sync status, creation
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
- `portable AI skills`
- `Claude Code SKILL.md library`
- `Codex skills library`
- `local-first LLM agent skills`
- `BACH skill catalog`
- `Anthropic-compatible skills`

The name is intentionally generic, so use the canonical repository string `ellmos-ai/skills` when linking or indexing this project.

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
