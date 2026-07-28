# Endpoint resolution

## Separation of responsibilities

| Layer | Purpose |
|---|---|
| semantic router | infer intent, domain, role and expert |
| routing map | preserve explicit role/persona relationships |
| live endpoint resolver | rank currently available skills |
| skill loader | load the selected live instructions |
| worker | execute with local rules and permissions |

A lexical registry is useful for current availability and aliases, but does not
replace semantic domain selection. An LLM-backed skill finder may interpret intent,
but a static family table does not replace explicit persona/role relationships.

## Resolver contract

A live resolver should accept a query plus optional category/tags and return:

```json
{
  "skill": "stable-skill-id",
  "score": 0.82,
  "match_kind": "lexical-or-semantic",
  "source": "resolver-name",
  "load_reference": "provider-specific reference"
}
```

The router must know whether the score is lexical, semantic or exact. Do not compare
scores from different methods as though they had the same meaning.

## Resolution policy

1. Exact explicit link wins when the skill is live.
2. Exact provenance link wins over a fuzzy candidate.
3. A live resolver can confirm, replace or reject a stale endpoint.
4. Fuzzy candidates require a second signal: source inspection, live resolver or
   user confirmation.
5. No endpoint produces a visible gap with the unresolved expert ID.

## Provider adapters

Adapters translate a stable skill ID into a provider-specific action such as:

- load a local `SKILL.md`;
- attach an agent/role definition;
- invoke a tool registry;
- pass the skill set to a worker;
- report that the provider cannot load skills dynamically.

Provider adapters must not change the semantic taxonomy or invent missing
capabilities.
