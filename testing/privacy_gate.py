#!/usr/bin/env python3
"""Fail closed when tracked files cross the public repository privacy boundary.

Gitless projections cannot prove which physical files are public. Run their
copy of this gate with ``--canonical-repo <path>`` so the current gate from an
explicit Git checkout performs the authoritative scan.
"""

from __future__ import annotations

import argparse
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
from testing import repo_privacy_gate as generic_privacy  # noqa: E402

concrete_home_matches = generic_privacy.concrete_home_matches

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
    "skills/utilities/embedded-captions",
    "skills/utilities/faceless-explainer",
    "skills/utilities/general-video",
    "skills/utilities/media-use",
    "skills/utilities/motion-graphics",
    "skills/utilities/music-to-video",
    "skills/utilities/pr-to-video",
    "skills/utilities/product-launch-video",
    "skills/utilities/rechtsabteilung",
    "skills/utilities/slideshow",
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


def content_findings(path: Path) -> list[str]:
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


def run_gate() -> list[str]:
    errors = []
    tracked = git_lines("ls-files")
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
        for finding in content_findings(path):
            errors.append(f"{relative}: {finding}")
    errors.extend(visibility_consistency_errors(set(tracked)))
    errors.extend(third_party_errors(set(tracked)))
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
    if errors:
        print("Privacy gate failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Privacy gate passed: no tracked private paths, known hosts, or token patterns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
