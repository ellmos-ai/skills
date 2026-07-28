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
is installed.

## Portability rules

- Use stable logical IDs, not absolute paths.
- Keep source paths relative and informational.
- Keep prompts, private data, credentials and runtime secrets outside the map.
- Preserve unresolved references in `issues`.
- Preserve experts without endpoints in `gaps`.
- Increment the schema version only for incompatible field changes.
