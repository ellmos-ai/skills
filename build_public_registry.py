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
import subprocess
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "registry" / "components.json"
LANGUAGE_CODES = ("de", "en", "es", "zh", "ja", "ru", "fr", "hi", "ar", "bn", "pt")


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


def unknown_language_variant_errors(skill_dir: Path) -> list[str]:
    """Report language-like variants outside the canonical P-006 catalog."""
    errors: list[str] = []

    for path in sorted(skill_dir.glob("SKILL.*.md")):
        code = path.name.removeprefix("SKILL.").removesuffix(".md").lower()
        if code not in LANGUAGE_CODES:
            errors.append(f"{path.as_posix()}: unknown language suffix '{code}'")

    for directory in sorted(path for path in skill_dir.iterdir() if path.is_dir()):
        # Historical translations used two-letter language directories in
        # lower- or uppercase form. Other subdirectories (scripts, tests,
        # references) are not language variants and must remain untouched.
        if not re.fullmatch(r"[A-Za-z]{2}", directory.name):
            continue
        legacy_skill = directory / "SKILL.md"
        code = directory.name.lower()
        if legacy_skill.is_file() and code not in LANGUAGE_CODES:
            errors.append(
                f"{legacy_skill.as_posix()}: unknown legacy language directory '{directory.name}'"
            )

    return errors


def registry_language_errors(skill_files: list[Path] | None = None) -> list[str]:
    """Return unsupported translation variants in public canonical skill roots."""
    errors: list[str] = []
    paths = list_public_skill_files() if skill_files is None else skill_files

    for path in paths:
        if path.parent.parent.name.startswith("_"):
            continue
        metadata = read_frontmatter(path)
        visibility = str(metadata.get("visibility") or "public").strip().lower()
        if visibility in {"private", "private-only", "private profile", "no-push"}:
            continue
        errors.extend(unknown_language_variant_errors(path.parent))

    return errors


def canonical_core_language_errors(skill_files: list[Path] | None = None) -> list[str]:
    """Return P-006 violations for public canonical skill roots.

    The public registry intentionally recognises historical language layouts for
    discovery.  P-006 is stricter: every catalogued skill needs a German
    ``SKILL.md`` and an English ``SKILL.en.md`` at the skill root.  Keeping this
    check separate preserves backwards-compatible discovery while making the
    canonical contract directly auditable.
    """
    errors: list[str] = []
    paths = list_public_skill_files() if skill_files is None else skill_files

    for path in paths:
        if path.parent.parent.name.startswith("_"):
            continue
        metadata = read_frontmatter(path)
        visibility = str(metadata.get("visibility") or "public").strip().lower()
        if visibility in {"private", "private-only", "private profile", "no-push"}:
            continue

        relative_path = path.relative_to(REPOSITORY_ROOT).as_posix()
        if metadata.get("language") != "de":
            errors.append(f"{relative_path}: canonical SKILL.md must declare language: de")

        english_path = path.parent / "SKILL.en.md"
        if not english_path.is_file():
            errors.append(f"{relative_path}: missing canonical sibling SKILL.en.md")
            continue
        english_metadata = read_frontmatter(english_path)
        if english_metadata.get("language") != "en":
            english_relative = english_path.relative_to(REPOSITORY_ROOT).as_posix()
            errors.append(f"{english_relative}: must declare language: en")

    return errors


def list_public_skill_files() -> list[Path]:
    """List ``skills/<category>/<name>/SKILL.md`` files git actually tracks.

    A raw filesystem glob over ``skills/`` also picks up gitignored, private
    skill directories that happen to exist on whichever machine runs this
    script (see the "bekannter Privatblock" entries in .gitignore) -- this
    repository's published state is defined by what git tracks, not by what
    is physically present locally. Falls back to the plain glob when git is
    unavailable (e.g. an extracted archive, not a checkout).
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", "skills"],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    names = [chunk.decode("utf-8") for chunk in result.stdout.split(b"\0") if chunk]
    paths = []
    for name in names:
        parts = Path(name).parts
        # skills/<category>/<name>/SKILL.md -- matches the historical glob
        # pattern "*/*/SKILL.md" rooted at SKILLS_ROOT.
        if len(parts) == 4 and parts[-1] == "SKILL.md":
            paths.append(REPOSITORY_ROOT / name)
    return sorted(paths)


def build_registry() -> dict:
    components = []
    category_counts: Counter[str] = Counter()

    for path in list_public_skill_files():
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
    parser.add_argument(
        "--check-core",
        action="store_true",
        help="read-only P-006 audit for canonical SKILL.md + SKILL.en.md pairs",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if args.check_core:
        errors = canonical_core_language_errors()
        if errors:
            print(f"P-006 core-language audit failed: {len(errors)} issue(s)")
            for error in errors:
                print(f"- {error}")
            return 1
        print("P-006 core-language audit passed: every public skill has canonical DE+EN files")
        return 0

    language_errors = registry_language_errors()
    if language_errors:
        print(f"Public registry language audit failed: {len(language_errors)} issue(s)")
        for error in language_errors:
            print(f"- {error}")
        return 1

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
