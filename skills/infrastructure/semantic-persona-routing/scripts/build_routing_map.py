#!/usr/bin/env python3
"""Build a portable persona-role-expert-skill routing map from Markdown sources."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SCHEMA = "semantic-persona-routing.map.v1"
STABLE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GENERIC_TOKENS = {
    "agent",
    "assistant",
    "assistent",
    "expert",
    "experte",
    "manager",
    "management",
    "service",
    "skill",
    "the",
    "and",
    "for",
    "with",
    "und",
    "fuer",
    "für",
}


def parse_scalar(value: str):
    """Parse the small YAML subset used by common skill frontmatter."""
    value = value.strip()
    if value in {"null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1]
        return [
            item.strip().strip("\"'")
            for item in inner.split(",")
            if item.strip()
        ]
    return value.strip("\"'")


def parse_frontmatter(text: str) -> dict:
    """Parse scalars, folded text, lists and one-level nested mappings."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next(
        (index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"),
        None,
    )
    if end is None:
        return {}
    body = lines[1:end]
    result: dict = {}
    index = 0
    while index < len(body):
        line = body[index]
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == ">":
            index += 1
            parts = []
            while index < len(body) and (
                not body[index].strip() or body[index].startswith((" ", "\t"))
            ):
                if body[index].strip():
                    parts.append(body[index].strip())
                index += 1
            result[key] = " ".join(parts)
            continue
        if value == "":
            index += 1
            indented = []
            while index < len(body) and (
                not body[index].strip() or body[index].startswith((" ", "\t"))
            ):
                if body[index].strip():
                    indented.append(body[index].strip())
                index += 1
            if indented and all(item.startswith("- ") for item in indented):
                result[key] = [parse_scalar(item[2:]) for item in indented]
            else:
                nested = {}
                for item in indented:
                    if ":" in item:
                        nested_key, nested_value = item.split(":", 1)
                        nested[nested_key.strip()] = parse_scalar(nested_value)
                result[key] = nested
            continue
        result[key] = parse_scalar(value)
        index += 1
    return result


def slug(value: str) -> str:
    """Normalize a logical identifier."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def variants(value: str) -> set[str]:
    """Return conservative role-name variants."""
    base = slug(value)
    result = {base}
    for suffix in ("-agent", "-expert", "-experte"):
        if base.endswith(suffix):
            result.add(base[: -len(suffix)])
        else:
            result.add(base + suffix)
    return {item for item in result if item}


def tokens(value: str) -> set[str]:
    """Tokenize text for non-authoritative candidate ranking."""
    words = {
        word
        for word in re.findall(r"[^\W\d_]+|\d+", value.lower())
        if len(word) >= 4
    }
    return words - GENERIC_TOKENS


def scan_markdown(root: Path | None, filename: str | None = None) -> list[dict]:
    """Read frontmatter records below a root."""
    if root is None or not root.exists():
        return []
    pattern = filename or "*.md"
    records = []
    for path in sorted(root.rglob(pattern)):
        if not path.is_file():
            continue
        metadata = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        if not metadata.get("name"):
            continue
        records.append(
            {
                "metadata": metadata,
                "source_ref": path.relative_to(root).as_posix(),
            }
        )
    return records


def classify_roles(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split role records into coordinators and experts."""
    coordinators = []
    experts = []
    for record in records:
        metadata = record["metadata"]
        role_type = str(metadata.get("type") or "").lower()
        if role_type in {"boss-agent", "coordinator", "agent"} or metadata.get(
            "orchestrates"
        ):
            coordinators.append(record)
        elif role_type == "expert" or metadata.get("parent_agents"):
            experts.append(record)
    return coordinators, experts


def skill_record(record: dict, identifier: str) -> dict:
    """Convert a source record to a portable skill entry."""
    metadata = record["metadata"]
    return {
        "id": identifier,
        "name": str(metadata["name"]),
        "description": str(metadata.get("description") or ""),
        "category": metadata.get("category"),
        "tags": metadata.get("tags") if isinstance(metadata.get("tags"), list) else [],
        "source_ref": record["source_ref"],
        "provenance": metadata.get("provenance")
        if isinstance(metadata.get("provenance"), dict)
        else {},
    }


def canonical_skill_id(value: object) -> str | None:
    """Accept only an already stable source-skill ID."""
    identifier = str(value).strip()
    return identifier if STABLE_ID_RE.fullmatch(identifier) else None


def normalize_skill_reference(value: object) -> tuple[str | None, bool]:
    """Normalize a skill reference without accepting an empty reference.

    A trailing ``#`` comment is a common source-format annotation, not part of
    the portable ID.  The caller must still verify that the normalized ID is a
    known skill before treating it as a usable endpoint.
    """
    raw = str(value)
    without_comment = raw.split("#", 1)[0].strip()
    identifier = slug(without_comment)
    if not STABLE_ID_RE.fullmatch(identifier):
        identifier = None
    if not identifier:
        return None, raw.strip() != ""
    return identifier, raw.strip() != identifier


def deduplicate_skills(skill_records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Choose one deterministic source per stable skill ID and report duplicates."""
    grouped: dict[str, list[dict]] = {}
    issues = []
    for record in skill_records:
        identifier = canonical_skill_id(record["metadata"]["name"])
        if identifier is None:
            issues.append(
                {
                    "kind": "invalid-skill-id",
                    "source_ref": record["source_ref"],
                    "reference": str(record["metadata"]["name"]),
                }
            )
            continue
        skill = skill_record(record, identifier)
        grouped.setdefault(skill["id"], []).append(skill)

    skills = []
    for identifier in sorted(grouped):
        sources = sorted(grouped[identifier], key=lambda item: item["source_ref"])
        skills.append(sources[0])
        if len(sources) > 1:
            issues.append(
                {
                    "kind": "duplicate-skill-id",
                    "skill": identifier,
                    "canonical_source_ref": sources[0]["source_ref"],
                    "duplicate_source_refs": [
                        source["source_ref"] for source in sources[1:]
                    ],
                }
            )
    return skills, issues


def append_skill_reference_issue(
    issues: list[dict],
    *,
    kind: str,
    owner_kind: str,
    owner: str,
    reference: object,
    normalized: str | None = None,
) -> None:
    """Record a non-authoritative skill reference without silently accepting it."""
    issue = {
        "kind": kind,
        "owner_kind": owner_kind,
        "owner": owner,
        "reference": str(reference),
    }
    if normalized is not None:
        issue["normalized"] = normalized
    issues.append(issue)


def normalized_known_skill_references(
    references: object,
    known_skill_ids: set[str],
    issues: list[dict],
    *,
    owner_kind: str,
    owner: str,
) -> list[str]:
    """Resolve declared references only to known canonical IDs, fail-closed."""
    if not isinstance(references, list):
        return []
    resolved = []
    seen = set()
    for reference in references:
        identifier, changed = normalize_skill_reference(reference)
        if identifier is None:
            append_skill_reference_issue(
                issues,
                kind="invalid-skill-reference",
                owner_kind=owner_kind,
                owner=owner,
                reference=reference,
            )
            continue
        if changed:
            append_skill_reference_issue(
                issues,
                kind="normalized-skill-reference",
                owner_kind=owner_kind,
                owner=owner,
                reference=reference,
                normalized=identifier,
            )
        if identifier not in known_skill_ids:
            append_skill_reference_issue(
                issues,
                kind="unknown-skill-reference",
                owner_kind=owner_kind,
                owner=owner,
                reference=reference,
                normalized=identifier,
            )
            continue
        if identifier not in seen:
            resolved.append(identifier)
            seen.add(identifier)
    return resolved


def lexical_candidates(expert: dict, skills: list[dict], limit: int) -> list[dict]:
    """Rank hints without turning them into executable endpoint links."""
    haystack = " ".join(
        str(expert["metadata"].get(field) or "")
        for field in ("name", "domain")
    )
    expert_tokens = tokens(haystack)
    ranked = []
    for skill in skills:
        skill_tokens = tokens(
            " ".join(
                [
                    skill["name"],
                    " ".join(skill["tags"]),
                    str(skill["category"] or ""),
                ]
            )
        )
        overlap = sorted(expert_tokens & skill_tokens)
        compound = sorted(
            expert_token
            for expert_token in expert_tokens
            if len(expert_token) >= 6
            and any(
                len(skill_token) >= 6
                and (
                    expert_token in skill_token
                    or skill_token in expert_token
                )
                for skill_token in skill_tokens
            )
        )
        signals = sorted(set(overlap + compound))
        if signals:
            ranked.append(
                {
                    "skill": skill["id"],
                    "score": len(signals),
                    "signals": signals,
                    "resolution": "lexical-candidate",
                }
            )
    return sorted(
        ranked,
        key=lambda item: (-item["score"], item["skill"]),
    )[:limit]


def explicit_endpoints(
    expert: dict, skills: list[dict], issues: list[dict]
) -> list[dict]:
    """Resolve explicit skill lists and exact provenance references."""
    metadata = expert["metadata"]
    by_id = {skill["id"]: skill for skill in skills}
    endpoints = []
    seen = set()
    expert_id = slug(str(metadata["name"]))
    explicit = normalized_known_skill_references(
        metadata.get("skills"),
        set(by_id),
        issues,
        owner_kind="expert",
        owner=expert_id,
    )
    for identifier in explicit:
        if identifier not in seen:
            endpoints.append({"skill": identifier, "resolution": "explicit"})
            seen.add(identifier)

    expert_variants = variants(str(metadata["name"]))
    for skill in skills:
        provenance = skill.get("provenance") or {}
        origin = slug(str(provenance.get("origin_path") or ""))
        padded_origin = f"-{origin}-"
        if origin and any(
            f"-{candidate}-" in padded_origin for candidate in expert_variants
        ):
            if skill["id"] not in seen:
                endpoints.append(
                    {"skill": skill["id"], "resolution": "provenance"}
                )
                seen.add(skill["id"])
    return endpoints


def build_map(
    role_records: list[dict],
    persona_records: list[dict],
    skill_records: list[dict],
    candidate_limit: int,
) -> dict:
    """Build the portable graph and preserve unresolved relationships."""
    coordinators_raw, experts_raw = classify_roles(role_records)
    skills, skill_issues = deduplicate_skills(skill_records)
    expert_lookup = {}
    for record in experts_raw:
        for variant in variants(str(record["metadata"]["name"])):
            expert_lookup.setdefault(variant, record)

    issues = skill_issues
    coordinators = []
    expert_parents: dict[str, set[str]] = {}
    for record in coordinators_raw:
        metadata = record["metadata"]
        coordinator_id = slug(str(metadata["name"]))
        orchestrates = metadata.get("orchestrates")
        expert_names = (
            orchestrates.get("experts", [])
            if isinstance(orchestrates, dict)
            else []
        )
        resolved = []
        for name in expert_names:
            match = next(
                (
                    expert_lookup[candidate]
                    for candidate in variants(str(name))
                    if candidate in expert_lookup
                ),
                None,
            )
            if match:
                expert_id = slug(str(match["metadata"]["name"]))
                resolved.append(expert_id)
                expert_parents.setdefault(expert_id, set()).add(coordinator_id)
            else:
                issues.append(
                    {
                        "kind": "missing-expert",
                        "coordinator": coordinator_id,
                        "reference": str(name),
                    }
                )
        coordinators.append(
            {
                "id": coordinator_id,
                "name": str(metadata["name"]),
                "description": str(metadata.get("description") or ""),
                "experts": sorted(set(resolved)),
                "personas": [],
                "source_ref": record["source_ref"],
            }
        )

    experts = []
    for record in experts_raw:
        metadata = record["metadata"]
        expert_id = slug(str(metadata["name"]))
        declared_parents = (
            metadata.get("parent_agents")
            if isinstance(metadata.get("parent_agents"), list)
            else []
        )
        parents = expert_parents.setdefault(expert_id, set())
        parents.update(slug(str(parent)) for parent in declared_parents)
        endpoints = explicit_endpoints(record, skills, issues)
        candidates = lexical_candidates(record, skills, candidate_limit)
        candidates = [
            item
            for item in candidates
            if item["skill"] not in {endpoint["skill"] for endpoint in endpoints}
        ]
        experts.append(
            {
                "id": expert_id,
                "name": str(metadata["name"]),
                "description": str(metadata.get("description") or ""),
                "parent_roles": sorted(parents),
                "endpoint_skills": endpoints,
                "candidate_skills": candidates,
                "personas": [],
                "source_ref": record["source_ref"],
            }
        )

    role_ids = {item["id"] for item in coordinators + experts}
    personas = []
    for record in persona_records:
        metadata = record["metadata"]
        persona_id = slug(
            str(
                (metadata.get("persona") or {}).get("short_name")
                if isinstance(metadata.get("persona"), dict)
                else metadata["name"]
            )
        )
        if not persona_id:
            persona_id = slug(str(metadata["name"]))
        persona_roles = []
        for role_id in role_ids:
            if variants(role_id) & variants(str(metadata["name"])):
                persona_roles.append(role_id)
        for parent in (
            metadata.get("parent_agents")
            if isinstance(metadata.get("parent_agents"), list)
            else []
        ):
            parent_id = slug(str(parent))
            if parent_id in role_ids:
                persona_roles.append(parent_id)
        persona_block = metadata.get("persona")
        display_name = (
            persona_block.get("display_name")
            if isinstance(persona_block, dict)
            else metadata["name"]
        )
        personas.append(
            {
                "id": persona_id,
                "display_name": str(display_name),
                "description": str(metadata.get("description") or ""),
                "roles": sorted(set(persona_roles)),
                "skills": normalized_known_skill_references(
                    metadata.get("skills"),
                    {skill["id"] for skill in skills},
                    issues,
                    owner_kind="persona",
                    owner=persona_id,
                ),
                "source_ref": record["source_ref"],
            }
        )

    for persona in personas:
        for role in coordinators + experts:
            if role["id"] in persona["roles"]:
                role["personas"].append(persona["id"])
    for role in coordinators + experts:
        role["personas"] = sorted(set(role["personas"]))

    gaps = [
        {"expert": expert["id"], "reason": "no-verified-endpoint"}
        for expert in experts
        if not expert["endpoint_skills"]
    ]
    return {
        "schema": SCHEMA,
        "roles": {
            "coordinators": sorted(coordinators, key=lambda item: item["id"]),
            "experts": sorted(experts, key=lambda item: item["id"]),
        },
        "personas": sorted(personas, key=lambda item: item["id"]),
        "skills": sorted(skills, key=lambda item: item["id"]),
        "gaps": sorted(gaps, key=lambda item: item["expert"]),
        "issues": sorted(
            issues,
            key=lambda item: (
                item["kind"],
                item.get("skill", ""),
                item.get("owner_kind", ""),
                item.get("owner", ""),
                item.get("reference", ""),
            ),
        ),
    }


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roles-dir", type=Path, required=True)
    parser.add_argument("--personas-dir", type=Path)
    parser.add_argument("--skills-dir", type=Path, required=True)
    parser.add_argument("--candidate-limit", type=int, default=3)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.candidate_limit < 0:
        parser.error("--candidate-limit must be non-negative")

    routing_map = build_map(
        scan_markdown(args.roles_dir, "SKILL.md"),
        scan_markdown(args.personas_dir),
        scan_markdown(args.skills_dir, "SKILL.md"),
        args.candidate_limit,
    )
    args.out.write_text(
        json.dumps(routing_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.out}: "
        f"{len(routing_map['roles']['coordinators'])} coordinators, "
        f"{len(routing_map['roles']['experts'])} experts, "
        f"{len(routing_map['gaps'])} gaps"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
