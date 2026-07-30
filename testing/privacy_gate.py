#!/usr/bin/env python3
"""Fail closed when tracked files cross the public repository privacy boundary."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_TRACKED_IGNORED = {"registry/components.json"}
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
CONTENT_PATTERNS = {
    "known private host": re.compile(r"\b(?:<LOCAL_HOST>|<LOCAL_HOST>)\b", re.IGNORECASE),
    "GitHub token": re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "OpenAI-style key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
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
    for pattern in (WINDOWS_HOME, POSIX_HOME):
        for match in pattern.finditer(text):
            segment = match.group(1).lower()
            if segment not in ALLOWED_HOME_SEGMENTS and not segment.startswith(("<", "{", "$", "%")):
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


def run_gate() -> list[str]:
    errors = []
    for path in tracked_ignored_files():
        errors.append(f"tracked although ignored: {path}")
    for path in tracked_text_files():
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        for finding in content_findings(path):
            errors.append(f"{relative}: {finding}")
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
