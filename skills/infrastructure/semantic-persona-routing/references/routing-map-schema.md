# Routing map schema

## Top-level structure

```json
{
  "schema": "semantic-persona-routing.map.v1",
  "roles": {
    "coordinators": [],
    "experts": []
  },
  "personas": [],
  "skills": [],
  "gaps": [],
  "issues": []
}
```

## Coordinator role

```json
{
  "id": "office-coordinator",
  "name": "office-coordinator",
  "description": "Coordinates administrative work",
  "experts": ["tax-expert"],
  "personas": ["clara"]
}
```

## Expert

```json
{
  "id": "tax-expert",
  "name": "tax-expert",
  "description": "Handles employee tax records",
  "parent_roles": ["office-coordinator"],
  "endpoint_skills": [
    {
      "skill": "employee-tax",
      "resolution": "explicit"
    }
  ],
  "candidate_skills": [],
  "personas": ["theodor"]
}
```

`candidate_skills` are hints, never authoritative endpoints.

## Persona

```json
{
  "id": "theodor",
  "display_name": "Theodor",
  "description": "Meticulous and precise",
  "roles": ["tax-expert"],
  "skills": ["employee-tax"]
}
```

Persona `skills` describe intended compatibility. They do not prove that a skill
is installed. They contain only known canonical skill IDs: malformed or unknown
source references are omitted fail-closed and reported in `issues`.

## Issue records

The builder reports source ambiguity and non-canonical references rather than
silently selecting an arbitrary runtime target.

```json
{
  "kind": "duplicate-skill-id",
  "skill": "employee-tax",
  "canonical_source_ref": "employee-tax/SKILL.md",
  "duplicate_source_refs": ["translations/SKILL.md"]
}
```

For a reference such as `employee-tax # legacy source path`, the map preserves
the safe resolved ID `employee-tax` and additionally emits a
`normalized-skill-reference` issue. `unknown-skill-reference` and
`invalid-skill-reference` entries have `owner_kind`, `owner`, and `reference`
fields; unknown and invalid references never become executable endpoints.
Invalid source declarations such as `name: ###` are skipped entirely and emit
`invalid-skill-id` with the relative `source_ref` and declared `reference`.

## Portability rules

- Use stable logical IDs, not absolute paths.
- Keep source paths relative and informational.
- Keep prompts, private data, credentials and runtime secrets outside the map.
- Preserve unresolved references in `issues`.
- Emit each skill ID at most once; report duplicate source declarations in
  `issues` with a deterministic canonical source.
- Preserve experts without endpoints in `gaps`.
- Increment the schema version only for incompatible field changes.
