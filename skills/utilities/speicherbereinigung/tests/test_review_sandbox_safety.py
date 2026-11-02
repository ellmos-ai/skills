"""Deletion safety of the review-sandbox janitor and of `review_sandbox.py closeout`.

Every path that can delete a directory gets a positive case and a negative control: a path outside the
review root, or one that is not a sandbox, must never be touched.  The janitor is Windows-only by design.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import prune_ephemeral  # noqa: E402
import review_sandbox  # noqa: E402

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows-only janitor (robocopy purge, junctions)")

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


def junction(link: Path, target: Path) -> None:
    subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True,
                   creationflags=NO_WINDOW)


def precious(base: Path, name: str = "precious") -> Path:
    folder = base / name
    folder.mkdir()
    (folder / "keep.txt").write_text("keep", encoding="utf-8")
    return folder


def test_remove_review_sandbox_only_removes_direct_children_of_the_root(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    (root / "nested" / "deep").mkdir(parents=True)
    outside = precious(tmp_path)
    inside = root / "sb"
    inside.mkdir()
    (inside / "x.txt").write_text("x", encoding="utf-8")

    assert prune_ephemeral.remove_review_sandbox(str(outside), str(root)) is False
    assert (outside / "keep.txt").is_file()
    assert prune_ephemeral.remove_review_sandbox(str(root / "nested" / "deep"), str(root)) is False
    assert (root / "nested" / "deep").is_dir()
    assert prune_ephemeral.remove_review_sandbox(str(root), str(root)) is False
    assert root.is_dir()

    assert prune_ephemeral.remove_review_sandbox(str(inside), str(root)) is True
    assert not inside.exists()


def test_remove_review_sandbox_refuses_drive_root_and_empty_arguments(tmp_path: Path) -> None:
    outside = precious(tmp_path)
    drive_root = os.path.splitdrive(str(tmp_path))[0] + "\\"
    assert prune_ephemeral.remove_review_sandbox(str(outside), drive_root) is False
    assert prune_ephemeral.remove_review_sandbox("", str(tmp_path)) is False
    assert prune_ephemeral.remove_review_sandbox(str(outside), "") is False
    assert (outside / "keep.txt").is_file()


def test_junction_inside_a_sandbox_is_removed_without_touching_its_target(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    root.mkdir()
    outside = precious(tmp_path)
    sandbox = root / "sb"
    sandbox.mkdir()
    junction(sandbox / "link", outside)
    assert (sandbox / "link" / "keep.txt").is_file()

    assert prune_ephemeral.remove_review_sandbox(str(sandbox), str(root)) is True
    assert not sandbox.exists()
    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"


def test_sandbox_that_is_itself_a_junction_is_never_removed(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    root.mkdir()
    outside = precious(tmp_path)
    junction(root / "sb", outside)

    assert prune_ephemeral.remove_review_sandbox(str(root / "sb"), str(root)) is False
    assert (outside / "keep.txt").is_file()


def test_prune_temp_keeps_young_entries_and_junction_targets(tmp_path: Path) -> None:
    temp = tmp_path / "temp"
    temp.mkdir()
    young = temp / "young"
    young.mkdir()
    outside = precious(tmp_path)
    junction(temp / "link", outside)
    old = time.time() - 30 * 86400
    os.utime(outside, (old, old))
    lines: list[str] = []

    prune_ephemeral.prune_temp(str(temp), 7, True, lines.append)

    assert young.is_dir()
    assert (outside / "keep.txt").is_file()


def test_closeout_refuses_a_directory_outside_the_review_root(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    root.mkdir()
    outside = precious(tmp_path)

    with pytest.raises(ValueError):
        review_sandbox.closeout_sandbox(str(outside), review_root=str(root))

    assert (outside / "keep.txt").is_file()
    assert not (outside / "closeout.json").exists()


def test_closeout_needs_an_explicit_or_configured_review_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(review_sandbox, "LOCAL_DEV", "")
    outside = precious(tmp_path)

    with pytest.raises(ValueError):
        review_sandbox.closeout_sandbox(str(outside))

    assert (outside / "keep.txt").is_file()
    assert not (outside / "closeout.json").exists()


def test_closeout_refuses_a_folder_without_owner_json(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    root.mkdir()
    not_a_sandbox = precious(root, "not-a-sandbox")

    with pytest.raises(ValueError):
        review_sandbox.closeout_sandbox(str(not_a_sandbox), review_root=str(root))

    assert (not_a_sandbox / "keep.txt").is_file()
    assert not (not_a_sandbox / "closeout.json").exists()


def test_create_needs_a_review_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(review_sandbox, "LOCAL_DEV", "")
    canon = make_repo(tmp_path / "canon")
    before = set(os.listdir(os.getcwd()))

    with pytest.raises(ValueError):
        review_sandbox.create_sandbox("sb", str(canon), "tester")

    assert set(os.listdir(os.getcwd())) == before


def test_closeout_deletes_a_clean_worktree_sandbox_and_prunes_the_canonical_repo(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))
    assert Path(created["source"]).is_dir()

    result = review_sandbox.closeout_sandbox(created["sandbox"], head="abc", review_root=str(root))

    assert result["deleted"] is True and result["verdict"] is None
    assert not Path(created["sandbox"]).exists()
    listed = subprocess.run(["git", "-C", str(canon), "worktree", "list"], capture_output=True, text=True,
                            creationflags=NO_WINDOW).stdout
    assert "sb" not in listed


def test_closeout_keeps_a_sandbox_with_uncommitted_work(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))
    (Path(created["source"]) / "new.txt").write_text("work", encoding="utf-8")

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))

    assert result["deleted"] is False and str(result["verdict"]).startswith("dirty:")
    assert (Path(created["source"]) / "new.txt").is_file()


def test_safe_review_roots_accepts_only_plain_names_directly_under_local_dev(tmp_path: Path) -> None:
    local_dev = str(tmp_path)
    entries = ["reviews", "..", "", ".", "sub/x", "sub\\x", "reviews/..", "C:\\Windows", "\\\\server\\share", None, 7]

    assert prune_ephemeral.safe_review_roots(local_dev, entries) == [os.path.join(local_dev, "reviews")]
    assert prune_ephemeral.safe_review_roots(local_dev, "reviews") == [os.path.join(local_dev, "reviews")]
    assert prune_ephemeral.safe_review_roots(local_dev, {"reviews": 1}) == []
    assert prune_ephemeral.safe_review_roots("", ["reviews"]) == []
