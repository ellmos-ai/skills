#!/usr/bin/env python3
"""Build the deliberately minimal public skill catalog.

The public registry is a discovery index, not the maintainer registry. Internal
ownership assessments, privacy classifications, branch metadata, warnings and
review scores belong in the separate private No-Push repository.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "registry" / "components.json"
LANGUAGE_CODES = ("de", "en", "es", "ja", "ru", "zh")


SCALAR_FIELDS = ("name", "type", "version", "status", "language", "visibility")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError as error:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from error

    # The historical catalog contains a few unquoted colons in long scalar
    # descriptions. The public index needs only top-level discovery fields, so
    # parse those deliberately instead of accepting the full private schema.
    data: dict[str, str] = {}
    lines = frontmatter.splitlines()
    for field in SCALAR_FIELDS:
        pattern = re.compile(rf"^{re.escape(field)}:\s*(.*)$")
        for line in lines:
            match = pattern.match(line)
            if match:
                data[field] = unquote(match.group(1))
                break

    description_lines: list[str] = []
    for index, line in enumerate(lines):
        match = re.match(r"^description:\s*(.*)$", line)
        if not match:
            continue
        first = match.group(1).strip()
        if first in {">", ">-", "|", "|-"}:
            for continuation in lines[index + 1 :]:
                if continuation and not continuation[0].isspace():
                    break
                if continuation.strip():
                    description_lines.append(continuation.strip())
            data["description"] = " ".join(description_lines)
        else:
            data["description"] = unquote(first)
        break

    return data


def available_languages(skill_dir: Path, canonical: dict) -> list[str]:
    languages = set()
    canonical_language = canonical.get("language")
    if isinstance(canonical_language, str) and canonical_language in LANGUAGE_CODES:
        languages.add(canonical_language)

    for code in LANGUAGE_CODES:
        if (skill_dir / f"SKILL.{code}.md").is_file():
            languages.add(code)
        if (skill_dir / code / "SKILL.md").is_file():
            languages.add(code)
        if (skill_dir / code.upper() / "SKILL.md").is_file():
            languages.add(code)

    return [code for code in LANGUAGE_CODES if code in languages]


def build_registry() -> dict:
    components = []
    category_counts: Counter[str] = Counter()

    for path in sorted(SKILLS_ROOT.glob("*/*/SKILL.md")):
        if path.parent.parent.name.startswith("_"):
            continue
        metadata = read_frontmatter(path)
        visibility = str(metadata.get("visibility") or "public").strip().lower()
        if visibility in {"private", "private-only", "private profile", "no-push"}:
            # Host- oder personengebundene Skills gehoeren nicht in den oeffentlichen
            # Katalog (siehe SKILLS-MAP-PRIVATE.md).
            continue
        category = path.parent.parent.name
        name = path.parent.name
        component_type = str(metadata.get("type") or "skill")
        description = metadata.get("description")
        if not isinstance(description, str):
            description = ""

        relative_path = path.relative_to(REPOSITORY_ROOT).as_posix()
        components.append(
            {
                "id": f"{component_type}:{category}:{name}",
                "name": name,
                "type": component_type,
                "category": category,
                "path": relative_path,
                "version": str(metadata.get("version") or "0.0.0"),
                "status": str(metadata.get("status") or "active"),
                "description": " ".join(description.split()),
                "languages": available_languages(path.parent, metadata),
            }
        )
        category_counts[category] += 1

    return {
        "summary": {
            "generated_by": "build_public_registry.py",
            "schema_version": "public-catalog-v1",
            "component_count": len(components),
            "categories": dict(sorted(category_counts.items())),
        },
        "components": components,
    }


def serialized_registry() -> str:
    return json.dumps(build_registry(), ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    expected = serialized_registry()
    output = args.output.resolve()
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != expected:
            print(f"Public registry is stale: {output}")
            return 1
        print(f"Public registry is current: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
