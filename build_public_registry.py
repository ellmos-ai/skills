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
from pathlib import Path, PurePosixPath

REPOSITORY_ROOT = Path(__file__).resolve().parent
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "registry" / "components.json"
DEFAULT_SOURCE_MANIFEST = REPOSITORY_ROOT / "registry" / "public-skill-files.json"
SOURCE_MANIFEST_SCHEMA = "public-skill-files-v1"
LANGUAGE_CODES = ("de", "en", "es", "zh", "ja", "ru", "fr", "hi", "ar", "bn", "pt")


SCALAR_FIELDS = ("name", "type", "version", "status", "language", "visibility")


class SourceManifestError(ValueError):
    """The explicit public-source manifest is missing, unsafe, or stale."""


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


def is_registry_skill_artifact(relative: str) -> bool:
    """Return whether a tracked path can affect public registry discovery."""
    path = PurePosixPath(relative)
    parts = path.parts
    if path.is_absolute() or not parts or parts[0] != "skills":
        return False
    if any(part in {"", ".", ".."} for part in parts):
        return False
    if len(parts) < 2 or parts[1].startswith("_"):
        return False
    if len(parts) == 4:
        filename = parts[-1]
        return filename == "SKILL.md" or bool(re.fullmatch(r"SKILL\.[^.]+\.md", filename))
    return bool(
        len(parts) == 5
        and re.fullmatch(r"[A-Za-z]{2}", parts[-2])
        and parts[-1] == "SKILL.md"
    )


def _canonical_skill_artifact(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return len(parts) == 4 and parts[-1] == "SKILL.md"


def _private_visibility(metadata: dict) -> bool:
    visibility = str(metadata.get("visibility") or "public").strip().lower()
    return visibility in {"private", "private-only", "private profile", "no-push"}


def git_skill_artifacts(repository_root: Path | None = None) -> list[str] | None:
    """Return public registry inputs from Git, or ``None`` outside a worktree."""
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    try:
        probe = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError:
        return None
    if probe.returncode != 0 or not probe.stdout.strip():
        return None
    try:
        git_root = Path(probe.stdout.strip()).resolve(strict=True)
    except OSError:
        return None
    if git_root != root:
        # An extracted archive nested below some unrelated checkout is still
        # a gitless snapshot and must use its own versioned manifest.
        return None

    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", "skills"],
            cwd=root,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise SourceManifestError("cannot read public source authority from Git") from error

    tracked = sorted(
        chunk.decode("utf-8")
        for chunk in result.stdout.split(b"\0")
        if chunk and is_registry_skill_artifact(chunk.decode("utf-8"))
    )
    public_roots: set[tuple[str, str, str]] = set()
    for relative in tracked:
        if not _canonical_skill_artifact(relative):
            continue
        metadata = read_frontmatter(root / PurePosixPath(relative))
        if not _private_visibility(metadata):
            public_roots.add(PurePosixPath(relative).parts[:3])

    public_files: list[str] = []
    for relative in tracked:
        path = PurePosixPath(relative)
        if path.parts[:3] not in public_roots:
            continue
        if not _canonical_skill_artifact(relative):
            try:
                metadata = read_frontmatter(root / path)
            except ValueError:
                # Keep malformed or unknown variants visible to the language
                # audit instead of silently dropping a tracked public input.
                pass
            else:
                if _private_visibility(metadata):
                    continue
        public_files.append(relative)
    return sorted(public_files)


def source_manifest_payload(files: list[str]) -> dict:
    normalized = sorted(set(files))
    for relative in normalized:
        if not isinstance(relative, str) or not is_registry_skill_artifact(relative):
            raise SourceManifestError(f"unsafe or irrelevant manifested path: {relative!r}")
    return {
        "schema_version": SOURCE_MANIFEST_SCHEMA,
        "generated_by": "build_public_registry.py",
        "file_count": len(normalized),
        "files": normalized,
    }


def serialized_source_manifest(files: list[str]) -> str:
    return json.dumps(source_manifest_payload(files), ensure_ascii=False, indent=2) + "\n"


def validate_source_manifest(
    manifest_path: Path | None = None,
    *,
    repository_root: Path | None = None,
    expected_files: list[str] | None = None,
) -> list[str]:
    """Load and validate the non-circular public-source authority."""
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    manifest = root / "registry" / "public-skill-files.json" if manifest_path is None else manifest_path
    if not manifest.is_file():
        raise SourceManifestError(f"missing public source manifest: {manifest}")
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SourceManifestError(f"unreadable public source manifest: {manifest}") from error

    expected_keys = {"schema_version", "generated_by", "file_count", "files"}
    if not isinstance(payload, dict) or set(payload) != expected_keys:
        raise SourceManifestError("public source manifest has unexpected fields")
    if payload["schema_version"] != SOURCE_MANIFEST_SCHEMA:
        raise SourceManifestError("public source manifest has unsupported schema")
    if payload["generated_by"] != "build_public_registry.py":
        raise SourceManifestError("public source manifest has unexpected generator")
    files = payload["files"]
    if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
        raise SourceManifestError("public source manifest files must be a string list")
    if files != sorted(set(files)) or payload["file_count"] != len(files):
        raise SourceManifestError("public source manifest files/count are not canonical")

    root_resolved = root.resolve(strict=True)
    for relative in files:
        if not is_registry_skill_artifact(relative):
            raise SourceManifestError(f"unsafe or irrelevant manifested path: {relative}")
        candidate = root / PurePosixPath(relative)
        if not candidate.is_file():
            raise SourceManifestError(f"missing manifested file: {relative}")
        try:
            candidate.resolve(strict=True).relative_to(root_resolved)
        except (OSError, ValueError) as error:
            raise SourceManifestError(f"manifested file escapes repository root: {relative}") from error

    if expected_files is not None and files != sorted(set(expected_files)):
        raise SourceManifestError("public source manifest does not match git authority")
    return files


def resolve_source_files(
    *,
    repository_root: Path | None = None,
    manifest_path: Path | None = None,
) -> tuple[list[str], str]:
    """Resolve Git or the versioned manifest as the public-source authority."""
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    tracked = git_skill_artifacts(root)
    if tracked is not None:
        return tracked, "git"
    return (
        validate_source_manifest(manifest_path, repository_root=root),
        "manifest",
    )


def _source_relative(path: Path, repository_root: Path) -> str:
    return path.resolve().relative_to(repository_root.resolve()).as_posix()


def available_languages(
    skill_dir: Path,
    canonical: dict,
    *,
    source_files: set[str] | None = None,
    repository_root: Path | None = None,
) -> list[str]:
    languages = set()
    canonical_language = canonical.get("language")
    if isinstance(canonical_language, str) and canonical_language in LANGUAGE_CODES:
        languages.add(canonical_language)

    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()

    def is_public_source(candidate: Path) -> bool:
        if source_files is None:
            return candidate.is_file()
        try:
            relative = _source_relative(candidate, root)
        except ValueError:
            return False
        return relative in source_files and candidate.is_file()

    for code in LANGUAGE_CODES:
        if is_public_source(skill_dir / f"SKILL.{code}.md"):
            languages.add(code)
        if is_public_source(skill_dir / code / "SKILL.md"):
            languages.add(code)
        if is_public_source(skill_dir / code.upper() / "SKILL.md"):
            languages.add(code)

    return [code for code in LANGUAGE_CODES if code in languages]


def unknown_language_variant_errors(
    skill_dir: Path,
    *,
    source_files: set[str] | None = None,
    repository_root: Path | None = None,
) -> list[str]:
    """Report language-like variants outside the canonical P-006 catalog."""
    errors: list[str] = []
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()

    if source_files is None:
        flat_variants = sorted(skill_dir.glob("SKILL.*.md"))
        legacy_variants = sorted(
            directory / "SKILL.md"
            for directory in skill_dir.iterdir()
            if directory.is_dir()
            and re.fullmatch(r"[A-Za-z]{2}", directory.name)
            and (directory / "SKILL.md").is_file()
        )
    else:
        try:
            prefix = _source_relative(skill_dir, root).rstrip("/") + "/"
        except ValueError:
            return []
        candidates = [
            root / PurePosixPath(relative)
            for relative in source_files
            if relative.startswith(prefix)
        ]
        flat_variants = sorted(
            path
            for path in candidates
            if path.parent == skill_dir and re.fullmatch(r"SKILL\.[^.]+\.md", path.name)
        )
        legacy_variants = sorted(
            path
            for path in candidates
            if path.parent.parent == skill_dir
            and re.fullmatch(r"[A-Za-z]{2}", path.parent.name)
            and path.name == "SKILL.md"
        )

    for path in flat_variants:
        code = path.name.removeprefix("SKILL.").removesuffix(".md").lower()
        if code not in LANGUAGE_CODES:
            errors.append(f"{path.as_posix()}: unknown language suffix '{code}'")

    for legacy_skill in legacy_variants:
        directory = legacy_skill.parent
        code = directory.name.lower()
        if code not in LANGUAGE_CODES:
            errors.append(
                f"{legacy_skill.as_posix()}: unknown legacy language directory '{directory.name}'"
            )

    return errors


def registry_language_errors(
    skill_files: list[Path] | None = None,
    *,
    source_files: list[str] | None = None,
    repository_root: Path | None = None,
) -> list[str]:
    """Return unsupported translation variants in public canonical skill roots."""
    errors: list[str] = []
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    paths = (
        list_public_skill_files(source_files, repository_root=root)
        if skill_files is None
        else skill_files
    )
    source_set = None if source_files is None else set(source_files)

    for path in paths:
        if path.parent.parent.name.startswith("_"):
            continue
        metadata = read_frontmatter(path)
        visibility = str(metadata.get("visibility") or "public").strip().lower()
        if visibility in {"private", "private-only", "private profile", "no-push"}:
            continue
        errors.extend(
            unknown_language_variant_errors(
                path.parent,
                source_files=source_set,
                repository_root=root,
            )
        )

    return errors


def canonical_core_language_errors(
    skill_files: list[Path] | None = None,
    *,
    source_files: list[str] | None = None,
    repository_root: Path | None = None,
) -> list[str]:
    """Return P-006 violations for public canonical skill roots.

    The public registry intentionally recognises historical language layouts for
    discovery.  P-006 is stricter: every catalogued skill needs a German
    ``SKILL.md`` and an English ``SKILL.en.md`` at the skill root.  Keeping this
    check separate preserves backwards-compatible discovery while making the
    canonical contract directly auditable.
    """
    errors: list[str] = []
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    paths = (
        list_public_skill_files(source_files, repository_root=root)
        if skill_files is None
        else skill_files
    )
    source_set = None if source_files is None else set(source_files)

    for path in paths:
        if path.parent.parent.name.startswith("_"):
            continue
        metadata = read_frontmatter(path)
        visibility = str(metadata.get("visibility") or "public").strip().lower()
        if visibility in {"private", "private-only", "private profile", "no-push"}:
            continue

        relative_path = path.relative_to(root).as_posix()
        if metadata.get("language") != "de":
            errors.append(f"{relative_path}: canonical SKILL.md must declare language: de")

        english_path = path.parent / "SKILL.en.md"
        english_relative = english_path.relative_to(root).as_posix()
        if not english_path.is_file() or (
            source_set is not None and english_relative not in source_set
        ):
            errors.append(f"{relative_path}: missing canonical sibling SKILL.en.md")
            continue
        english_metadata = read_frontmatter(english_path)
        if english_metadata.get("language") != "en":
            errors.append(f"{english_relative}: must declare language: en")

    return errors


def list_public_skill_files(
    source_files: list[str] | None = None,
    *,
    repository_root: Path | None = None,
    manifest_path: Path | None = None,
) -> list[Path]:
    """List canonical public skills from Git or the explicit source manifest."""
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    if source_files is None:
        source_files, _ = resolve_source_files(
            repository_root=root,
            manifest_path=manifest_path,
        )
    return sorted(
        root / PurePosixPath(relative)
        for relative in source_files
        if _canonical_skill_artifact(relative)
    )


def build_registry(
    source_files: list[str] | None = None,
    *,
    repository_root: Path | None = None,
) -> dict:
    components = []
    category_counts: Counter[str] = Counter()
    root = REPOSITORY_ROOT if repository_root is None else repository_root.resolve()
    if source_files is None:
        source_files, _ = resolve_source_files(repository_root=root)
    source_set = set(source_files)

    for path in list_public_skill_files(source_files, repository_root=root):
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

        relative_path = path.relative_to(root).as_posix()
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
                "languages": available_languages(
                    path.parent,
                    metadata,
                    source_files=source_set,
                    repository_root=root,
                ),
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


def serialized_registry(
    source_files: list[str] | None = None,
    *,
    repository_root: Path | None = None,
) -> str:
    return (
        json.dumps(
            build_registry(source_files, repository_root=repository_root),
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--check-core",
        action="store_true",
        help="read-only P-006 audit for canonical SKILL.md + SKILL.en.md pairs",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=None,
        help=(
            "versioned public-source manifest; defaults to "
            "registry/public-skill-files.json below the repository root"
        ),
    )
    args = parser.parse_args()

    root = REPOSITORY_ROOT.resolve()
    manifest = (
        root / "registry" / "public-skill-files.json"
        if args.source_manifest is None
        else args.source_manifest.resolve()
    )
    try:
        source_files, authority = resolve_source_files(
            repository_root=root,
            manifest_path=manifest,
        )
        if authority == "git" and args.check:
            validate_source_manifest(
                manifest,
                repository_root=root,
                expected_files=source_files,
            )
    except SourceManifestError as error:
        print(f"Public source manifest check failed: {error}")
        return 1

    if args.check_core:
        errors = canonical_core_language_errors(
            source_files=source_files,
            repository_root=root,
        )
        if errors:
            print(f"P-006 core-language audit failed: {len(errors)} issue(s)")
            for error in errors:
                print(f"- {error}")
            return 1
        print("P-006 core-language audit passed: every public skill has canonical DE+EN files")
        return 0

    language_errors = registry_language_errors(
        source_files=source_files,
        repository_root=root,
    )
    if language_errors:
        print(f"Public registry language audit failed: {len(language_errors)} issue(s)")
        for error in language_errors:
            print(f"- {error}")
        return 1

    expected = serialized_registry(source_files, repository_root=root)
    output = args.output.resolve()
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != expected:
            print(f"Public registry is stale: {output}")
            return 1
        print(f"Public source manifest is current: {manifest} ({authority})")
        print(f"Public registry is current: {output}")
        return 0

    if authority == "git":
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            serialized_source_manifest(source_files),
            encoding="utf-8",
            newline="\n",
        )
        print(f"Wrote {manifest}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
