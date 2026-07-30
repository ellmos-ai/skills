#!/usr/bin/env python3
"""Validate canonical SKILL.md roots changed by the current push or pull request."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import PurePosixPath

import skill_tester


ZERO_SHA = "0" * 40


def is_canonical_skill_path(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return (
        len(parts) == 4
        and parts[0] == "skills"
        and parts[-1] == "SKILL.md"
    )


def git_changed_files(base: str | None, head: str | None) -> list[str]:
    if base and head and base != ZERO_SHA:
        completed = subprocess.run(
            ["git", "diff", "--name-only", f"{base}..{head}", "--", "skills"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return completed.stdout.splitlines()

    completed = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--", "skills"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    staged = completed.stdout.splitlines()
    if staged:
        return staged

    completed = subprocess.run(
        ["git", "diff", "--name-only", "HEAD^", "HEAD", "--", "skills"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.splitlines()


def main() -> int:
    changed = git_changed_files(
        os.environ.get("BASE_SHA"),
        os.environ.get("HEAD_SHA"),
    )
    canonical = sorted({path for path in changed if is_canonical_skill_path(path)})
    if not canonical:
        print("Changed-skill gate passed: no canonical SKILL.md root changed.")
        return 0
    print(f"Validating {len(canonical)} changed canonical skills.")
    return skill_tester.main(["batch", "--type", "static", "--ci", *canonical])


if __name__ == "__main__":
    raise SystemExit(main())
