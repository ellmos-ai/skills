#!/usr/bin/env python3
"""Export folder-organization with portable base frontmatter.

The source remains unchanged. The destination must be new and outside the source
skill directory. Only Python's standard library is required.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]


def portable_skill_text(content: str) -> str:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md has no valid frontmatter block")
    frontmatter = match.group(1)
    name_match = re.search(r"(?m)^name:\s*([^\r\n]+?)\s*$", frontmatter)
    description_match = re.search(
        r"(?ms)^description:\s*>-?\s*\r?\n((?:[ \t]+[^\r\n]*(?:\r?\n|$))+)",
        frontmatter,
    )
    if not name_match or not description_match:
        raise ValueError("SKILL.md must contain name and folded description fields")
    name = name_match.group(1).strip().strip("'\"")
    description_lines = [line.strip() for line in description_match.group(1).splitlines()]
    description = " ".join(line for line in description_lines if line).strip()
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        raise ValueError("skill name is not portable hyphen-case")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        raise ValueError("skill description is not portable")
    body = content[match.end():]
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "---\n"
        f"{body}"
    )


def export(destination: Path) -> Path:
    source = SOURCE.resolve(strict=True)
    destination = destination.resolve(strict=False)
    try:
        destination.relative_to(source)
    except ValueError:
        pass
    else:
        raise ValueError("destination must be outside the source skill directory")
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    if not destination.parent.is_dir():
        raise ValueError("destination parent must already exist")

    skill_text = portable_skill_text((source / "SKILL.md").read_text(encoding="utf-8"))
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )
    (destination / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a portable folder-organization skill copy.")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    try:
        destination = export(args.destination)
    except (OSError, ValueError) as exc:
        print(f"export-portable: {exc}", file=sys.stderr)
        return 2
    print(f"export-portable: created {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
