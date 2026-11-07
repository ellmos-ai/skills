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

import clean_flutter_builds  # noqa: E402
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


def link_to(kind: str, link: Path, target: Path) -> None:
    if kind == "junction":
        junction(link, target)
        return
    try:
        os.symlink(target, link, target_is_directory=True)
    except OSError:
        pytest.skip("no right to create directory symlinks (Developer Mode / SeCreateSymbolicLinkPrivilege)")


@pytest.mark.parametrize("kind", ["junction", "symlink"])
def test_robocopy_fallback_never_purges_through_a_link(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str,
) -> None:
    """Long-path leftovers make rmtree leave the tree, so remove() falls back to purge_dir (robocopy /PURGE).
    A link left in the tree (e.g. a pnpm junction into the store) must go as a link; its target stays."""
    outside = precious(tmp_path)
    tree = tmp_path / "sb"
    (tree / "node_modules").mkdir(parents=True)
    link_to(kind, tree / "node_modules" / "pkg", outside)
    real_rmtree = prune_ephemeral.shutil.rmtree
    calls: list[str] = []

    def rmtree_leaves_the_tree_once(path, *args, **kwargs):
        calls.append(str(path))
        if len(calls) > 1:
            real_rmtree(path, *args, **kwargs)

    monkeypatch.setattr(prune_ephemeral.shutil, "rmtree", rmtree_leaves_the_tree_once)

    prune_ephemeral.remove(str(tree))

    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert not tree.exists()


def test_purge_dir_drops_a_junction_behind_a_long_path(tmp_path: Path) -> None:
    """The real leftover: a junction deeper than MAX_PATH, which only robocopy and \\\\?\\ paths reach."""
    import _winapi

    outside = precious(tmp_path)
    tree = tmp_path / "sb"
    deep = "\\\\?\\" + os.path.join(str(tree), *(["d" * 40] * 7))
    os.makedirs(deep)
    link = os.path.join(deep, "pkg")
    _winapi.CreateJunction(str(outside), link)
    assert len(link) > 260

    clean_flutter_builds.purge_dir(str(tree))

    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert not tree.exists()


def test_purge_dir_stays_away_when_a_link_cannot_be_dropped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    outside = precious(tmp_path)
    tree = tmp_path / "sb"
    tree.mkdir()
    junction(tree / "link", outside)
    real_rmdir = os.rmdir

    def rmdir_refuses_links(path, *args, **kwargs):
        if clean_flutter_builds.is_link(path):
            raise OSError("link in use")
        real_rmdir(path, *args, **kwargs)

    monkeypatch.setattr(clean_flutter_builds.os, "rmdir", rmdir_refuses_links)

    clean_flutter_builds.purge_dir(str(tree))

    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert (tree / "link").exists()


def test_clean_flutter_builds_apply_never_empties_a_junction_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Second caller path: clean_flutter_builds --apply purges build/ directly, without rmtree first."""
    outside = precious(tmp_path)
    app = tmp_path / "app"
    (app / "build").mkdir(parents=True)
    (app / "pubspec.yaml").write_text("name: demo\n", encoding="utf-8")
    junction(app / "build" / "link", outside)
    monkeypatch.setattr(sys, "argv", ["clean_flutter_builds.py", str(app), "--apply"])

    assert clean_flutter_builds.main() == 0

    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert not (app / "build").exists()


def test_purge_dir_on_a_junction_removes_only_the_link(tmp_path: Path) -> None:
    outside = precious(tmp_path)
    link = tmp_path / "link"
    junction(link, outside)

    clean_flutter_builds.purge_dir(str(link))

    assert not os.path.lexists(link)
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


def test_closeout_deletes_only_its_clean_worktree_sandbox(tmp_path: Path) -> None:
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


def test_closeout_preserves_an_unavailable_foreign_worktree_registration(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    foreign = tmp_path / "foreign"
    parked = tmp_path / "parked"
    git(canon, "worktree", "add", "--detach", str(foreign), "HEAD")
    # Simulate an unavailable mount without deleting its recoverable payload.
    foreign.rename(parked)
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))

    assert result["deleted"] is True
    listed = subprocess.run(
        ["git", "-C", str(canon), "worktree", "list", "--porcelain"],
        check=True, capture_output=True, text=True, creationflags=NO_WINDOW,
    ).stdout
    assert str(foreign).replace("\\", "/") in listed
    assert (parked / "f.txt").read_text(encoding="utf-8") == "one"
    assert str(Path(created["source"])).replace("\\", "/") not in listed


def test_closeout_keeps_a_git_locked_worktree_payload(tmp_path: Path) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))
    source = Path(created["source"])
    git(canon, "worktree", "lock", str(source))

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))

    assert result["deleted"] is False
    assert (source / "f.txt").read_text(encoding="utf-8") == "one"
    assert (Path(created["sandbox"]) / "owner.json").is_file()


def test_closeout_from_inside_sandbox_keeps_its_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "reviews"
    canon = make_repo(tmp_path / "canon")
    created = review_sandbox.create_sandbox("sb", str(canon), "tester", review_root=str(root))
    source = Path(created["source"])
    monkeypatch.chdir(source)

    result = review_sandbox.closeout_sandbox(created["sandbox"], review_root=str(root))

    assert result["deleted"] is False
    assert (source / "f.txt").read_text(encoding="utf-8") == "one"


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
