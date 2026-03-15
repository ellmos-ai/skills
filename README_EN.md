# Skills Library

**Standalone skill library** -- portable AI skills in Anthropic-compatible format.

Skills can be used independently (standalone) or as part of a larger system (e.g. BACH). Origin, sync status, and dependencies are stored **directly in each SKILL.md** via YAML frontmatter -- no central control file needed.

## Structure

```
skills/
  <category>/
    <skill-name>/
      SKILL.md              # Definition + Provenance + Dependencies
      scripts/              # Optional: executable code
      references/           # Optional: reference documents
  _templates/               # Templates for new skills
  _examples/                # Example skills
docs/
  CONVENTIONS.md            # Frontmatter specification
catalog.py                  # CLI: catalog, sync status, search
```

## Skill Types

| Type | Description |
|------|------------|
| `skill` | General capability (default) |
| `agent` | Orchestrates other skills/experts |
| `expert` | Deep domain knowledge |
| `service` | Background service |
| `protocol` | Process/workflow guide |
| `tool` | Executable tool (with script) |

## Standalone vs. System-bound

Each SKILL.md declares via frontmatter fields whether it works independently:

```yaml
standalone: true             # Works without external system
bach_compatible: true        # Can be loaded in BACH
bach_origin: true            # Originated from BACH
```

Details: [docs/CONVENTIONS.md](docs/CONVENTIONS.md)

## Quick Start

```bash
# Show catalog
python catalog.py list

# Filter by category
python catalog.py list --category productivity

# Check sync status (which skills are outdated?)
python catalog.py sync-status

# Create new skill from template
python catalog.py create "my-skill" --category productivity --type skill
```

## Provenance System

Each skill carries its own origin metadata:

```yaml
provenance:
  origin: "bach"                          # bach | custom | community
  origin_path: "system/skills/therapie/"  # Source path in origin system
  origin_version: "1.0.0"                # Version at time of export
  last_sync_from_origin: "2026-03-12"    # Last import from source
  last_sync_to_origin: null              # Last backflow to source
  local_changes_since_sync: false        # Local changes?
```

This ensures full traceability: Where does the skill come from? What version is it at? Has it been locally modified?

## License

MIT License -- see [LICENSE](LICENSE)
