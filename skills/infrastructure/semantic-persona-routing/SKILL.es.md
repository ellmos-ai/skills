---
name: semantic-persona-routing
version: 1.0.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-28
description: [Español] Habilidad y protocolo de agente para semantic-persona-routing: Builds and uses a provider-neutral semantic routing graph from personas, coordinating roles, experts and live skill endpoints. Use when an LLM should route a request through boss-role to expert to skill, extract a portable persona router from an existing agent system, combine a semantic domain map with a lexical skill registry, or expose missing role-to-skill ports instead of silently falling back. Triggers on semantic persona routing, persona umbrella, role router, boss-agent expert skill routing, agent-role export, or requests to make personas reusable across LLM providers.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [persona, semantic-routing, agents, experts, skills, umbrella, provider-neutral]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': None, 'origin_version': None, 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Traducción al Español** — Versión oficial en español de `semantic-persona-routing` (Fase 3: Multilingüe).


# Semantic Persona Routing

Route by capability first and apply personality second. Build a portable map that
keeps semantic role choice, deterministic endpoint lookup and provider-specific
loading separate.

## Routing model

```text
request
  -> semantic domain/coordinator role
  -> expert capability
  -> explicit or live-resolved skill endpoint
  -> optional persona overlay
  -> provider adapter loads and executes
```

A persona controls communication style, priorities and interaction patterns. It
does not grant tools, permissions or subject-matter capability. A role coordinates;
an expert narrows the domain; a skill is the executable endpoint.

## Build the routing map

Use explicit metadata as authority and lexical similarity only as a candidate:

```bash
python scripts/build_routing_map.py \
  --roles-dir path/to/roles \
  --personas-dir path/to/personas \
  --skills-dir path/to/skills \
  --out routing-map.json
```

The builder understands common `SKILL.md` fields such as `type`,
`orchestrates.experts`, `parent_agents`, `skills`, descriptions and provenance.
It produces a runtime map without requiring the source system to be installed.
Read [routing-map-schema.md](references/routing-map-schema.md) before extending the
format.

Do not automatically promote `candidate_skills`. Confirm them against a live skill
resolver or source metadata first.

## Route a request

### 1. Select the coordinator role semantically

Compare the request with role names, descriptions and use cases. Prefer the
narrowest role that can coordinate the whole request. Keep multiple candidates
visible when confidence is low; ask the user only when the choice materially
changes the result.

### 2. Select an expert within the role

Use only experts connected to the chosen coordinator unless the request clearly
spans roles. A direct expert request may skip the coordinator for execution, but
retain the coordinator link in the route explanation.

### 3. Resolve executable endpoints

Resolve in this order:

1. `endpoint_skills` from explicit source metadata or exact provenance;
2. a current external skill resolver or local skill finder;
3. verified `candidate_skills`;
4. visible `GAP` when no endpoint exists.

Never route to an expert name as though it were an installed skill. A missing
endpoint is a porting gap, not permission to fabricate one.

Read [endpoint-resolution.md](references/endpoint-resolution.md) when connecting a
live registry, lexical finder or provider-specific skill loader.

### 4. Apply the persona overlay

Choose a persona attached to the selected role or expert. If several personas fit,
prefer one whose declared limits and style match the task. Apply no persona when
none is explicitly connected.

Persona instructions cannot override safety rules, locks, user decisions,
professional boundaries or tool permissions.

### 5. Load and execute

Use the provider's native skill/agent loading mechanism. Load the selected live
skill instructions before execution. Keep the router lean; execution belongs to
the worker or current agent with the resolved skills loaded.

## Route receipt

Return or record:

```text
ROLE: <coordinator or direct>
EXPERT: <expert or n/a>
SKILLS: <verified live endpoints>
PERSONA: <overlay or none>
RESOLUTION: explicit | provenance | live-resolver | verified-candidate | GAP
CONFIDENCE: high | medium | low
WHY: <one short reason>
GAPS: <missing endpoints or stale-map warnings>
```

Rebuild the map when source roles or skill inventory change. A live resolver may
supersede a stale map for endpoint availability, but it must not silently rewrite
the semantic role taxonomy.

## Example

Request: "Organize my receipts and prepare the tax-year overview."

The router selects an office coordinator, then the tax expert, resolves the
installed tax skill, and finally applies an explicitly linked meticulous tax
persona. If the tax expert exists but no portable tax skill is installed, report
`GAP` and continue only through an explicitly configured fallback.

## Changelog

### 1.0.0 (2026-07-28)

- Extracted the provider-neutral role/expert/skill chain from a proven domain
  router pattern and added portable map generation with visible endpoint gaps.
