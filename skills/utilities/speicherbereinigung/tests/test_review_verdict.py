"""review_verdict must keep real work and nothing else (T-20261031-617335048).

Two false positives kept clean, closed-out sandboxes forever (`deleted: false`):
- every file named LOCK* counted as a lock, for example LOCK-SYSTEM.md in a lock-master checkout;
- `git stash list` inside a linked worktree lists the stash of the canonical repository, so every
  worktree sandbox looked like it held a stash whenever the canonical clone had one.
Real locks, a stash of the sandbox's own repository and uncommitted work must still keep it.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import prune_ephemeral  # noqa: E402
import review_sandbox  # noqa: E402

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows-only janitor")

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
        cwd=cwd, check=True, capture_output=True, creationflags=NO_WINDOW,
    )


def make_repo(path: Path) -> Path:
    path.mkdir(parents=True)
    git(path, "init", "-q")
    (path / "f.txt").write_text("one", encoding="utf-8")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "c1")
    return path


def stash_something(repo: Path) -> None:
    (repo / "f.txt").write_text("changed", encoding="utf-8")
    git(repo, "stash", "push", "-q")


def closed_folder(root: Path, name: str) -> Path:
    folder = root / name
    folder.mkdir(parents=True)
    (folder / "closeout.json").write_text(json.dumps({"status": "closed"}), encoding="utf-8")
    return folder


def verdict(folder: Path, root: Path):
    return prune_ephemeral.review_verdict(str(folder), str(root), time.time() - 86400, {})


@pytest.mark.parametrize(
    ("name", "is_lock"),
    [
        ("LOCK.txt", True),
        ("lock.txt", True),
        ("LOCK.docs.txt", True),
        ("LOCK.team.docs.ASUS-GEI.txt", True),
        ("LOCK.user.txt", True),
        ("LOCK-SYSTEM.md", False),
        ("LOCK-SYSTEM_de.md", False),
        ("LOCKED.txt", False),
        ("LOCK.txt.guard", False),
        ("LOCK", False),
        ("MYLOCK.txt", False),
    ],
)
def test_is_lock_file_matches_the_lock_scan_pattern(name: str, is_lock: bool) -> None:
    assert prune_ephemeral.is_lock_file(name) is is_lock


def test_a_doc_named_lock_something_does_not_keep_a_closed_sandbox(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    folder = closed_folder(root, "lockmaster")
    (folder / "LOCK-SYSTEM.md").write_text("docs", encoding="utf-8")
    (folder / "source").mkdir()
    (folder / "source" / "LOCK-SYSTEM_de.md").write_text("docs", encoding="utf-8")

    assert verdict(folder, root) is None


@pytest.mark.parametrize("relative", ["LOCK.txt", "LOCK.docs.txt", "source/LOCK.team.x.PC.txt"])
def test_a_real_lock_file_still_keeps_the_sandbox(tmp_path: Path, relative: str) -> None:
    root = tmp_path / "reviews"
    folder = closed_folder(root, "locked")
    target = folder / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("lock", encoding="utf-8")

    assert verdict(folder, root) == "lock"


def test_canonical_stash_does_not_keep_a_clean_worktree_sandbox(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    stash_something(canon)
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root), delete_now=False)
    assert result["verdict"] is None

    deleted = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))
    assert deleted["deleted"] is True and not Path(created["sandbox"]).exists()
    assert subprocess.run(["git", "-C", str(canon), "stash", "list"], capture_output=True, text=True,
                          creationflags=NO_WINDOW).stdout.strip(), "the canonical stash must survive"


def test_a_stash_inside_a_shared_clone_still_keeps_the_sandbox(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", mode="shared", review_root=str(root))
    stash_something(Path(created["source"]))

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))

    assert str(result["verdict"]).startswith("stash:")
    assert result["deleted"] is False and Path(created["source"]).is_dir()


def test_uncommitted_work_in_a_worktree_sandbox_is_still_kept_when_the_canon_has_a_stash(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    stash_something(canon)
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))
    (Path(created["source"]) / "mine.txt").write_text("work", encoding="utf-8")

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))

    assert str(result["verdict"]).startswith("dirty:") and result["deleted"] is False
    assert (Path(created["source"]) / "mine.txt").is_file()
