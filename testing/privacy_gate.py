#!/usr/bin/env python3
"""Fail closed when tracked files cross the public repository privacy boundary."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

# Single source for the visibility contract -- deliberately imported instead of
# copied, because two lists that drift apart are the very failure this gate exists
# to catch.
sys.path.insert(0, str(REPOSITORY_ROOT))
from build_public_registry import (  # noqa: E402
    COPYLEFT_LICENSES,
    PRIVATE_VISIBILITY_VALUES,
    REDISTRIBUTABLE_LICENSES,
    THIRD_PARTY_AREAL,
    effective_visibility,
)

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
    "testing/skill_tester.py",
    "testing/test_privacy_gate.py",
}
TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".mjs",
    ".py", ".sh", ".svg", ".toml", ".ts", ".txt", ".yaml", ".yml",
}
ALLOWED_HOME_SEGMENTS = {
    "<user>", "<username>", "<user_home>", "%userprofile%", "${home}",
    "$home", "$userprofile", "...", "…", "public", "runner", "test",
    "user", "username", "|",
}
# On Windows, "user" is not a placeholder we may trust: this host's real account
# name IS "User", so C:\Users\User\... is a concrete path that merely looks
# generic. Treating it as a placeholder made the check systematically blind here
# -- it waved through eight real paths across three skills (found 2026-08-23).
# Under POSIX, /home/user stays allowed: it is an established documentation
# convention, and the detector that matches it lives in the repository itself.
ALLOWED_WINDOWS_HOME_SEGMENTS = ALLOWED_HOME_SEGMENTS - {"user", "username"}
CONTENT_PATTERNS = {
    "host-scoped device name": re.compile(
        r"\b(?:ASUS|WORKSTATION|DESKTOP|LAPTOP|MACSTUDIO)-"
        r"[A-Z0-9][A-Z0-9-]*\b"
    ),
    "host-scoped local development path": re.compile(
        r"(?i)(?:file:///)?[A-Z]:[\\/]+_Local_DEV(?:[\\/]|$)"
    ),
    "GitHub token": re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "OpenAI-style key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private skill name": re.compile(
        r"(?i)\b(?:tom-lm|store-welle-usertest|rechtsabteilung)\b"
    ),
}
FORBIDDEN_PUBLIC_SKILL_DIRECTORIES = {
    "skills/dev/figma",
    "skills/dev/hyperframes",
    "skills/dev/hyperframes-animation",
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
WINDOWS_HOME = re.compile(r"(?i)(?:file:///)?[A-Z]:[\\/]+Users[\\/]+([^\\/\s\"'`]+)")
POSIX_HOME = re.compile(r"(?i)(?:^|[\s(\"'`])/(?:home|Users)/([^/\s\"'`)]+)")


def git_lines(*arguments: str) -> list[str]:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [line for line in completed.stdout.splitlines() if line]


def tracked_ignored_files() -> list[str]:
    return [
        path
        for path in git_lines("ls-files", "-ci", "--exclude-standard")
        if path not in ALLOWED_TRACKED_IGNORED
    ]


def tracked_text_files() -> list[Path]:
    result = []
    for relative in git_lines("ls-files"):
        path = REPOSITORY_ROOT / relative
        if (
            relative not in CONTENT_SCAN_EXCLUSIONS
            and path.is_file()
            and path.suffix.lower() in TEXT_SUFFIXES
        ):
            result.append(path)
    return result


def concrete_home_matches(text: str) -> list[str]:
    findings = []
    for pattern, allowed in (
        (WINDOWS_HOME, ALLOWED_WINDOWS_HOME_SEGMENTS),
        (POSIX_HOME, ALLOWED_HOME_SEGMENTS),
    ):
        for match in pattern.finditer(text):
            segment = match.group(1).lower()
            if segment not in allowed and not segment.startswith(("<", "{", "$", "%")):
                findings.append(match.group(0).strip())
    return findings


def content_findings(path: Path) -> list[str]:
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
        for finding in content_findings(path):
            errors.append(f"{relative}: {finding}")
    errors.extend(visibility_consistency_errors(set(tracked)))
    errors.extend(third_party_errors(set(tracked)))
    return errors


def main() -> int:
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
