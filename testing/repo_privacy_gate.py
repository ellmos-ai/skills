#!/usr/bin/env python3
"""Generic, repository-agnostic privacy scan for tracked text files.

Extracted from `privacy_gate.py` (T-20260825-907516036, DM1=B, 2026-08-25):
this repository's own gate additionally checks skill-specific concerns
(SKILL.md visibility declarations, third-party licensing, forbidden skill
directories) that do not generalize to arbitrary repositories. This module
carries only the repo-agnostic core -- host/account names, local
development paths, concrete home directories, and common secret-token
shapes -- so any git repository can run the same scan via ``--repo <path>``.

Usage:
    python repo_privacy_gate.py --repo <path-to-git-repo>
    python repo_privacy_gate.py            # defaults to cwd

Scope: git-tracked text files only (respects .gitignore via `git ls-files`).
Exit code 0 = clean, 1 = findings, 0 with a skip message = not a git repo.

When to use (T-20260825-907516036, DM1=B): run this before flipping any
repository's visibility from private to public, and specifically on
borderline `DECISIONS.md`-style files (architecture-decision records that
mix genuinely public rationale with host paths, account names, or other
operational detail) -- the analysis behind that ticket found DECISIONS.md
files to be exactly this kind of grey area. A clean run is evidence, not a
guarantee: the pattern set is deliberately small (host/account names,
`_Local_DEV`/home paths, common secret-token shapes) and will not catch
everything a human reviewer would. Note the observed limitation from this
extraction's own smoke test: repositories that document their OWN canonical
`_Local_DEV` clone path as a matter of local convention (this ecosystem's
Plan-D pattern) will legitimately trip the "host-scoped local development
path" check in their own architecture docs -- that is an expected true
positive for this pattern, not a bug, and such repos should either treat it
as accepted noise or phrase the convention without the literal path.

Self-scan note (T-20260830-412369231): running THIS generic scan directly on
the skills repository itself flags files under ``testing/`` -- the gate's own
detection patterns (this module, ``skill_tester.py``) and the deliberately
"private-looking" positive fixtures in ``test_privacy_gate.py``/
``test_repo_privacy_gate.py`` (e.g. ``C:\\Users\\Alice``). These are expected
true positives of the pattern set, not leaks. The authoritative self-scan for
this repository is ``privacy_gate.py``, whose reviewed, per-file
``CONTENT_SCAN_EXCLUSIONS`` allowlist covers exactly those files with reasons;
this generic module intentionally stays strict (fail-closed) for arbitrary
repositories and takes no default exclusions.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".mjs",
    ".py", ".sh", ".svg", ".toml", ".ts", ".txt", ".yaml", ".yml",
}

ALLOWED_HOME_SEGMENTS = {
    "<user>", "<username>", "<user_home>", "%userprofile%", "${home}",
    "$home", "$userprofile", "...", "…", "public", "runner", "test",
    "user", "username", "|",
}
# On Windows, "user" is not a placeholder that can be trusted in general: a
# real Windows account can literally be named "User" (observed on this
# ecosystem's own hosts, 2026-08-23), which makes C:\Users\User\... a
# concrete path that merely looks generic. Treating it as a placeholder
# would make the check systematically blind on such hosts. Under POSIX,
# /home/user stays allowed: it is an established documentation convention.
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
}

WINDOWS_HOME = re.compile(r"(?i)(?:file:///)?[A-Z]:[\\/]+Users[\\/]+([^\\/\s\"'`]+)")
POSIX_HOME = re.compile(r"(?i)(?:^|[\s(\"'`])/(?:home|Users)/([^/\s\"'`)]+)")


def git_lines(repo_root: Path, *arguments: str) -> list[str]:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [line for line in completed.stdout.splitlines() if line]


def tracked_ignored_files(repo_root: Path, allowed: frozenset[str] = frozenset()) -> list[str]:
    return [
        path
        for path in git_lines(repo_root, "ls-files", "-ci", "--exclude-standard")
        if path not in allowed
    ]


def tracked_text_files(
    repo_root: Path, exclusions: frozenset[str] = frozenset()
) -> list[Path]:
    result = []
    for relative in git_lines(repo_root, "ls-files"):
        path = repo_root / relative
        if (
            relative not in exclusions
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


def run_generic_gate(
    repo_root: Path,
    content_scan_exclusions: frozenset[str] = frozenset(),
    allowed_tracked_ignored: frozenset[str] = frozenset(),
) -> list[str]:
    """Runs the repo-agnostic checks and returns a flat list of findings."""
    errors = []
    tracked = git_lines(repo_root, "ls-files")
    for path in tracked_ignored_files(repo_root, allowed_tracked_ignored):
        errors.append(f"tracked although ignored: {path}")
    for relative in tracked:
        pattern = CONTENT_PATTERNS["host-scoped device name"]
        if pattern.search(relative):
            errors.append(f"{relative}: host-scoped device name in tracked path")
    for path in tracked_text_files(repo_root, content_scan_exclusions):
        relative = path.relative_to(repo_root).as_posix()
        for finding in content_findings(path):
            errors.append(f"{relative}: {finding}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo", type=Path, default=Path.cwd(),
        help="Path to the git repository root to scan (default: cwd)",
    )
    args = parser.parse_args(argv)
    repo_root = args.repo.resolve()

    if not (repo_root / ".git").exists():
        print(f"Privacy gate skipped: {repo_root} is not a git repository root.")
        return 0

    errors = run_generic_gate(repo_root)
    if errors:
        print(f"Privacy gate failed for {repo_root}:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Privacy gate passed for {repo_root}: no tracked private paths, "
        "known hosts, or token patterns."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
