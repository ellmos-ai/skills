#!/usr/bin/env python3
"""Fail closed when tracked files cross the public repository privacy boundary.

Gitless projections cannot prove which physical files are public. Run their
copy of this gate with ``--canonical-repo <path>`` so the current gate from an
explicit Git checkout performs the authoritative scan.
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

# Shared contracts are deliberately imported instead of copied, because two
# lists that drift apart are the very failure this gate exists to catch. The
# repo-agnostic scan engine carries host/account names, local-dev paths, home
# directories, and secret-token shapes; this file layers the checks specific to
# this repository on top.
sys.path.insert(0, str(REPOSITORY_ROOT))
from build_public_registry import (  # noqa: E402
    COPYLEFT_LICENSES,
    PRIVATE_VISIBILITY_VALUES,
    REDISTRIBUTABLE_LICENSES,
    THIRD_PARTY_AREAL,
    effective_visibility,
)
from testing import repo_link_visibility_gate  # noqa: E402
from testing import repo_privacy_gate as generic_privacy  # noqa: E402

concrete_home_matches = generic_privacy.concrete_home_matches

# Files carrying deliberately fictional org/repo names as test fixtures --
# real repos that never existed on GitHub, so an unauthenticated 404 lookup
# correctly (but uselessly) treats them as "not public". These are not the
# public docs the gate exists to protect; excluded the same way
# CONTENT_SCAN_EXCLUSIONS excludes this gate's own detection-pattern files.
LINK_VISIBILITY_SCAN_EXCLUSIONS = {
    "testing/test_repo_link_visibility_gate.py",
    "skills/dev/community-outreach/scripts/init_outreach_workspace.py",
    "skills/dev/community-outreach/tests/test_community_outreach.py",
    "skills/dev/community-outreach/tests/test_runtime_projection.py",
}

# Module-level cache so a single gate run only computes this once, shared
# between run_gate() (blocking findings) and main() (non-blocking warnings) --
# see repo_link_visibility_gate.py docstring for why unknown-visibility is a
# warning, never a blocker (T-20260926-820252321).
_LINK_VISIBILITY_RESULT: tuple[list[str], list[str]] | None = None


def _link_visibility_check() -> tuple[list[str], list[str]]:
    global _LINK_VISIBILITY_RESULT
    if _LINK_VISIBILITY_RESULT is None:
        scan_paths = [
            path for path in tracked_text_files()
            if path.relative_to(REPOSITORY_ROOT).as_posix() not in LINK_VISIBILITY_SCAN_EXCLUSIONS
        ]
        _LINK_VISIBILITY_RESULT = repo_link_visibility_gate.run_gate(REPOSITORY_ROOT, scan_paths)
    return _LINK_VISIBILITY_RESULT

ALLOWED_TRACKED_IGNORED: set[str] = set()

#: Foreign files whose *upstream text* legitimately trips the content scan --
#: example API keys in documentation, concrete paths in someone else's tutorial.
#: Each entry is a deliberate, reviewed decision and belongs here with a reason.
#:
#: Never fix such a hit by editing the upstream text: that would contradict
#: "vendored unmodified", inflate every diff against the source, and -- under
#: Apache-2.0 -- trigger the obligation to document modifications. An exception
#: is honest; a silent edit is not.
THIRD_PARTY_SCAN_EXCEPTIONS: set[str] = set()
CONTENT_SCAN_EXCLUSIONS = {
    "testing/privacy_gate.py",
    "testing/repo_privacy_gate.py",
    "testing/skill_tester.py",
    "testing/test_privacy_gate.py",
    "testing/test_repo_privacy_gate.py",
}

# This repository's content scan is the generic set plus one skill-specific
# addition (a fixed list of skill names that must never surface in tracked
# text, regardless of visibility declaration).
CONTENT_PATTERNS = {
    **generic_privacy.CONTENT_PATTERNS,
    "private skill name": re.compile(
        r"(?i)\b(?:tom-lm|store-welle-usertest|rechtsabteilung)\b"
    ),
}
FORBIDDEN_PUBLIC_SKILL_DIRECTORIES = {
    "skills/dev/figma",
    "skills/dev/trampelpfadanalyse",
    "skills/dev/hyperframes",
    "skills/dev/hyperframes-animation",
    "skills/dev/hyperframes-audio",
    "skills/dev/hyperframes-cli",
    "skills/dev/hyperframes-core",
    "skills/dev/hyperframes-creative",
    "skills/dev/hyperframes-keyframes",
    "skills/dev/hyperframes-registry",
    "skills/dev/remotion-to-hyperframes",
    "skills/dev/store-welle-usertest",
    "skills/production/hackathon-operator",
    "skills/utilities/auto-spar",
    "skills/utilities/embedded-captions",
    "skills/utilities/faceless-explainer",
    "skills/utilities/general-video",
    "skills/utilities/media-use",
    "skills/utilities/motion-graphics",
    "skills/utilities/music-to-video",
    "skills/utilities/notaus",
    "skills/utilities/pr-to-video",
    "skills/utilities/product-launch-video",
    "skills/utilities/rechtsabteilung",
    "skills/utilities/slideshow",
    "skills/utilities/sparmodus",
    "skills/utilities/store-welle-usertest",
    "skills/utilities/talking-head-recut",
    "skills/utilities/tom-lm",
}


def git_lines(*arguments: str) -> list[str]:
    return generic_privacy.git_lines(REPOSITORY_ROOT, *arguments)


def tracked_ignored_files() -> list[str]:
    return generic_privacy.tracked_ignored_files(
        REPOSITORY_ROOT, frozenset(ALLOWED_TRACKED_IGNORED)
    )


def tracked_text_files() -> list[Path]:
    return generic_privacy.tracked_text_files(
        REPOSITORY_ROOT, frozenset(CONTENT_SCAN_EXCLUSIONS)
    )


def content_findings(path: Path, tracked_posix_paths: frozenset[str] = frozenset()) -> list[str]:
    """Same as the generic scan, plus this repository's own patterns (e.g.
    'private skill name'), which CONTENT_PATTERNS already includes above."""
    text = path.read_text(encoding="utf-8", errors="replace")
    findings = []
    homes = concrete_home_matches(text)
    if homes:
        findings.append(f"concrete user-home path: {homes[0]}")
    for label, pattern in CONTENT_PATTERNS.items():
        if pattern.search(text):
            findings.append(label)
    for link in generic_privacy.unresolvable_file_links(text, tracked_posix_paths):
        findings.append(f"unresolvable local file reference: {link}")
    return findings


def declared_visibility(path: Path, relative: str | None = None) -> str:
    """Return the visibility that applies to a skill.

    Fail closed: a missing field counts as private. Silence is an unanswered
    question, and an unanswered question must never publish anything -- except
    inside the third-party areal, which runs on a smaller contract without the
    field. There, the location is the declaration (see effective_visibility).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""
    metadata: dict = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        match = re.search(r"^visibility:\s*(.+)$", text[:end] if end != -1 else text, re.M)
        if match:
            metadata["visibility"] = match.group(1).strip().strip("\"'")
    if relative is None:
        try:
            relative = path.resolve().relative_to(REPOSITORY_ROOT).as_posix()
        except ValueError:
            relative = None
    return effective_visibility(metadata, relative)


def visibility_consistency_errors(tracked: set[str]) -> list[str]:
    """Declared visibility and Git tracking must agree -- otherwise one of them lies.

    Both directions are reported, because both are wrong; only the damage differs:

    * ``declared private but tracked`` -- the file is readable on GitHub while no
      catalogue lists it. This is the dangerous direction: an unsupervised
      publication that no listing would ever reveal.
    * ``public (or undeclared) but excluded from Git`` -- the catalogue would
      promise something the public repository does not contain.
    """
    errors = []
    for path in sorted(REPOSITORY_ROOT.glob("skills/*/*/SKILL.md")):
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        if "/_" in relative:  # _archive and other underscore folders are not skills
            continue
        visibility = declared_visibility(path, relative)
        is_private = visibility in PRIVATE_VISIBILITY_VALUES
        is_tracked = relative in tracked
        if is_private and is_tracked:
            errors.append(
                f"{relative}: declares '{visibility}' but is tracked -- publicly "
                "readable while listed nowhere; add the directory to .gitignore "
                "and FORBIDDEN_PUBLIC_SKILL_DIRECTORIES, then 'git rm -r --cached'"
            )
        elif not is_private and not is_tracked:
            errors.append(
                f"{relative}: declares '{visibility}' but is excluded from Git -- "
                "either declare a private visibility or stop excluding it"
            )
    return errors


def _frontmatter_field(path: Path, field: str) -> str | None:
    """Read one top-level frontmatter value as raw text, or None if absent."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    match = re.search(rf"^{field}:\s*(.+)$", text[:end] if end != -1 else text, re.M)
    return match.group(1).strip().strip("\"'") if match else None


def third_party_errors(tracked: set[str]) -> list[str]:
    """Folder and flag must agree, and foreign material needs a usable licence.

    Two switches say the same thing here -- the areal a skill sits in and the
    ``third_party`` flag it carries. That is deliberate redundancy, but only
    because this function compares them. Two switches that nobody compares are
    exactly what let a private skill sit readable on GitHub (2026-08-23).

    The licence check is fail-closed without the asymmetry argument that applies
    to ``visibility``: redistributing without permission is a legal wrong,
    failing to redistribute is an inconvenience.
    """
    errors = []
    areal = f"{THIRD_PARTY_AREAL}/"

    for path in sorted(REPOSITORY_ROOT.glob("skills/*/*/SKILL.md")):
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        if "/_" in relative or relative not in tracked:
            continue
        in_areal = relative.startswith(areal)
        flag = (_frontmatter_field(path, "third_party") or "").lower() in {"true", "yes", "1"}

        if in_areal and not flag:
            errors.append(
                f"{relative}: lies in {THIRD_PARTY_AREAL}/ but does not declare "
                "'third_party: true' -- folder and flag must agree"
            )
        elif flag and not in_areal:
            errors.append(
                f"{relative}: declares 'third_party: true' but sits outside "
                f"{THIRD_PARTY_AREAL}/ -- move it there or drop the flag"
            )

        if not (in_areal or flag):
            continue

        licence = _frontmatter_field(path, "license")
        if not licence:
            errors.append(
                f"{relative}: foreign skill without 'license' -- no declared licence "
                "means all rights reserved, so it must not be redistributed here"
            )
        elif licence not in REDISTRIBUTABLE_LICENSES:
            errors.append(
                f"{relative}: licence '{licence}' is not on the redistributable "
                "allow-list (see REDISTRIBUTABLE_LICENSES in build_public_registry.py)"
            )
        elif licence in COPYLEFT_LICENSES and not (path.parent / "LICENSE").is_file():
            errors.append(
                f"{relative}: copyleft licence '{licence}' requires the upstream "
                "LICENSE file next to the skill"
            )

        if not (path.parent / "LICENSE").is_file():
            errors.append(
                f"{relative}: foreign skill without an upstream LICENSE file -- "
                "the licence text is the legally graspable unit, not a frontmatter field"
            )
        if not _frontmatter_field(path, "upstream"):
            errors.append(
                f"{relative}: foreign skill without 'upstream' -- provenance must stay "
                "traceable to its source"
            )
    return errors


#: Python's own top-level standard-library module names (3.10+). A bare
#: dependency entry naming one of these (or a dotted submodule of one, e.g.
#: "urllib.request") needs nothing shipped or declared -- it ships with
#: Python itself.
_STDLIB_MODULES = frozenset(getattr(sys, "stdlib_module_names", ()))

#: A dependency string entry is treated as "this skill's own file, must be
#: shipped in its directory" only when it looks like one -- has a familiar
#: extension and no spaces. Anything else (a bare command like "git", "gh",
#: a package name like "requests") is an external tool/package, not
#: something this repo can ship, so it is not checked for existence.
_OWN_FILE_LIKE = re.compile(r"^[\w.-]+\.(?:py|md|json|txt|sh|ps1)$", re.IGNORECASE)


def _dependencies_block(path: Path) -> dict:
    """Best-effort parse of the frontmatter ``dependencies:`` value.

    Two forms are used across this repo's ~45 skills that declare
    dependencies (T-20260927-285118525): a multi-line block style
    (``dependencies:\\n  python: [foo.py]``) and a single-line YAML flow
    style that happens to also be valid Python literal syntax
    (``dependencies: {'python': [{'name': 'feedparser', ...}]}``). The flow
    style is parsed with ``ast.literal_eval`` -- no PyYAML dependency, matching
    this repo's stdlib-only convention (see inventory_skills.py's own
    from-scratch YAML parser). Anything neither form recognizes returns {}:
    fail-open, same principle as the rest of this gate's uncertain cases --
    a parse miss must never itself become a false "missing dependency".
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    frontmatter = text[:end] if end != -1 else text
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("dependencies:"):
            continue
        rest = line[len("dependencies:"):].strip()
        if rest.startswith("{"):
            try:
                parsed = ast.literal_eval(rest)
            except (ValueError, SyntaxError):
                return {}
            return parsed if isinstance(parsed, dict) else {}
        if rest:
            return {}  # unrecognized scalar form
        block: dict = {}
        for sub in lines[index + 1:]:
            if not sub.strip():
                continue
            if not sub.startswith("  ") or sub.startswith("    "):
                break  # dedent (block ended) or deeper nesting (not in observed corpus)
            stripped = sub.strip()
            sub_match = re.match(r"^([A-Za-z_]+):\s*(.*)$", stripped)
            if not sub_match:
                continue
            key, value = sub_match.group(1), sub_match.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                block[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
            elif value:
                block[key] = [value.strip("'\"")]
            else:
                block[key] = []
        return block
    return {}


def dependency_warnings(tracked: set[str]) -> list[str]:
    """Non-blocking (V1 rollout, T-20260927-285118525): each declared
    dependency that this repo can check gets checked --

    * a bare ``dependencies.python``/``.tools`` entry that looks like this
      skill's own file (``_OWN_FILE_LIKE``) must exist under the skill's
      own directory -- a placeholder-dressed dead ``file://`` link
      (``unresolvable_file_links``) is one way to hide this, a bare
      frontmatter filename that was simply never shipped is another
      (letter-hooker's ``agy_kontext_and_workflow_loader.py``, found live).
    * a ``dependencies.protocols`` entry naming another skill must exist in
      this repo and be declared public -- generalizes the old fixed
      "private skill name" blocklist into a data-driven check.

    A dict-form entry (already carries ``name``/``optional``/``install``/
    ``external``/``path``) is a *declared* external dependency and is never
    checked for existence -- that is the documented escape hatch for a false
    positive from the filename heuristic, no schema migration required.

    WARN_ONLY for the first rollout, same as WARN_ONLY_LABELS above: ~45
    skills already use this field inconsistently, so this starts as a hint
    that surfaces every run, not a sudden mass CI failure. See the ticket for
    the planned switch to blocking after a fix pass over existing hits.
    """
    warnings: list[str] = []
    for path in sorted(REPOSITORY_ROOT.glob("skills/*/*/SKILL.md")):
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        if "/_" in relative or relative not in tracked:
            continue
        skill_dir_prefix = relative.rsplit("/", 1)[0] + "/"
        deps = _dependencies_block(path)
        for field in ("python", "tools"):
            for item in deps.get(field, []) or []:
                if not isinstance(item, str):
                    continue  # dict form: declared external/optional, not checked
                if item in _STDLIB_MODULES or item.split(".", 1)[0] in _STDLIB_MODULES:
                    continue
                if not _OWN_FILE_LIKE.match(item):
                    continue  # bare tool/package name, not something this repo ships
                if not any(t.startswith(skill_dir_prefix) and t.endswith("/" + item) or t == skill_dir_prefix + item for t in tracked):
                    warnings.append(
                        f"{relative}: dependencies.{field} names '{item}' but no such "
                        f"file is tracked under {skill_dir_prefix} (informational only, "
                        "not blocking -- ship it, or mark it {'name': ..., 'external': true} "
                        "if it is not this skill's own file)"
                    )
        for item in deps.get("protocols", []) or []:
            if not isinstance(item, str):
                continue
            match = next(
                (p for p in tracked if p.count("/") == 3 and p.endswith(f"/{item}/SKILL.md")),
                None,
            )
            if match is None:
                continue  # not a skill name at all -- an external protocol description
            if declared_visibility(REPOSITORY_ROOT / match) in PRIVATE_VISIBILITY_VALUES:
                warnings.append(
                    f"{relative}: dependencies.protocols names '{item}', which exists "
                    "but is declared private -- a public skill cannot depend on it "
                    "(informational only, not blocking)"
                )
    return warnings


def run_gate() -> list[str]:
    errors = []
    tracked = git_lines("ls-files")
    tracked_posix_paths = frozenset(tracked)
    for path in tracked_ignored_files():
        errors.append(f"tracked although ignored: {path}")
    for relative in tracked:
        for forbidden in FORBIDDEN_PUBLIC_SKILL_DIRECTORIES:
            if relative == forbidden or relative.startswith(f"{forbidden}/"):
                errors.append(f"{relative}: private or third-party skill directory")
                break
        pattern = CONTENT_PATTERNS["host-scoped device name"]
        if pattern.search(relative):
            errors.append(f"{relative}: host-scoped device name in tracked path")
    for path in tracked_text_files():
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        if relative in THIRD_PARTY_SCAN_EXCEPTIONS:
            continue
        # content_findings() here uses this repo's CONTENT_PATTERNS (generic
        # set + "private skill name"), not run_generic_gate()'s narrower one.
        for finding in content_findings(path, tracked_posix_paths):
            errors.append(f"{relative}: {finding}")
    errors.extend(visibility_consistency_errors(set(tracked)))
    errors.extend(third_party_errors(set(tracked)))
    link_findings, _link_warnings = _link_visibility_check()
    errors.extend(link_findings)
    return errors


def _is_exact_git_worktree_root(path: Path) -> bool:
    """Return whether *path* is the exact top level of a Git worktree."""
    try:
        candidate = path.resolve(strict=True)
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=candidate,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if completed.returncode != 0 or not completed.stdout.strip():
            return False
        return Path(completed.stdout.strip()).resolve(strict=True) == candidate
    except OSError:
        return False


def _delegate_to_canonical_repo(canonical_repo: Path) -> int:
    """Run the canonical checkout's own gate after validating its Git root."""
    canonical_repo = canonical_repo.resolve()
    if not _is_exact_git_worktree_root(canonical_repo):
        print(
            "Privacy gate failed closed: --canonical-repo is not an exact "
            f"Git worktree root: {canonical_repo}"
        )
        return 2

    canonical_gate = canonical_repo / "testing" / "privacy_gate.py"
    if not canonical_gate.is_file():
        print(
            "Privacy gate failed closed: canonical checkout has no "
            f"testing/privacy_gate.py: {canonical_repo}"
        )
        return 2

    try:
        completed = subprocess.run(
            [sys.executable, str(canonical_gate)],
            cwd=canonical_repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError as error:
        print(f"Privacy gate failed closed: cannot run canonical gate: {error}")
        return 2

    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--canonical-repo",
        type=Path,
        help=(
            "explicit canonical Git checkout whose current privacy gate must "
            "run; required when this script lives in a gitless projection"
        ),
    )
    args = parser.parse_args(argv)

    if args.canonical_repo is not None:
        return _delegate_to_canonical_repo(args.canonical_repo)

    if not _is_exact_git_worktree_root(REPOSITORY_ROOT):
        print(
            "Privacy gate failed closed: this is not a Git worktree root. "
            "In a gitless projection, pass --canonical-repo <path>."
        )
        return 2

    errors = run_gate()
    _link_findings, link_warnings = _link_visibility_check()
    for warning in link_warnings:
        print(f"WARNING (non-blocking): {warning}")
    for warning in dependency_warnings(set(git_lines("ls-files"))):
        print(f"WARNING (non-blocking): {warning}")
    if errors:
        print("Privacy gate failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Privacy gate passed: no tracked private paths, known hosts, or token patterns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
