#!/usr/bin/env python3
"""Validate canonical SKILL.md roots changed by the current push or pull request."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from pathlib import PurePosixPath

try:
    import skill_tester
except ModuleNotFoundError:  # unittest imports this file as testing.changed_skill_gate
    from testing import skill_tester


ZERO_SHA = "0" * 40
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
BANNER_LINE = re.compile(
    r'^\s*<img\s+src="banner\.png"\s+width="100%"\s+alt="[^"]*banner">\s*$'
)


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
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if completed.returncode == 0:
            return completed.stdout.splitlines()
        print(
            "Base commit is unavailable after a history rewrite; "
            "checking changed skill paths in the two newest commits."
        )
        completed = subprocess.run(
            ["git", "rev-list", "--max-count=2", head],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        changed = []
        for commit in completed.stdout.splitlines():
            commit_files = subprocess.run(
                [
                    "git", "diff-tree", "--root", "--no-commit-id",
                    "--name-only", "-r", commit, "--", "skills",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            changed.extend(commit_files.stdout.splitlines())
        return changed

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


def normalized_without_banner(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines() if not BANNER_LINE.match(line)]
    normalized = "\n".join(lines).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", normalized)


def git_text(revision: str, path: str) -> str | None:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        return None
    return completed.stdout


def comparison_base(base: str | None, head: str | None) -> str:
    if base and base != ZERO_SHA:
        available = subprocess.run(
            ["git", "cat-file", "-e", f"{base}^{{commit}}"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
        )
        if available.returncode == 0:
            return base
    return f"{head}^" if head else "HEAD"


def current_text(path: str, head: str | None) -> str | None:
    if head:
        return git_text(head, path)
    worktree_path = REPOSITORY_ROOT / path
    if not worktree_path.is_file():
        return None
    return worktree_path.read_text(encoding="utf-8")


def is_banner_only_change(path: str, base: str | None, head: str | None) -> bool:
    before = git_text(comparison_base(base, head), path)
    after = current_text(path, head)
    if before is None or after is None or before == after:
        return False
    return normalized_without_banner(before) == normalized_without_banner(after)


def main() -> int:
    changed = git_changed_files(
        os.environ.get("BASE_SHA"),
        os.environ.get("HEAD_SHA"),
    )
    canonical = sorted(
        {
            path
            for path in changed
            if is_canonical_skill_path(path)
            and current_text(path, os.environ.get("HEAD_SHA")) is not None
            and not is_banner_only_change(
                path,
                os.environ.get("BASE_SHA"),
                os.environ.get("HEAD_SHA"),
            )
        }
    )
    if not canonical:
        print(
            "Changed-skill gate passed: no existing canonical SKILL.md root "
            "changed beyond banner-only updates."
        )
        return 0
    print(f"Validating {len(canonical)} changed canonical skills.")
    return skill_tester.main(["batch", "--type", "static", "--ci", *canonical])


if __name__ == "__main__":
    raise SystemExit(main())
