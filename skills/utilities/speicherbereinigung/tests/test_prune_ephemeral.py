from __future__ import annotations

import importlib.util
import os
import sys
import time
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "prune_ephemeral.py"
SPEC = importlib.util.spec_from_file_location("prune_ephemeral", SCRIPT)
assert SPEC and SPEC.loader
prune_ephemeral = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prune_ephemeral)

OLD = time.time() - 30 * 86400


def make_old(root: Path, *parts: str) -> Path:
    path = root.joinpath(*parts)
    path.mkdir(parents=True)
    (path / "x.txt").write_text("x", encoding="utf-8")
    os.utime(path / "x.txt", (OLD, OLD))
    os.utime(path, (OLD, OLD))
    return path


def test_dry_run_reports_but_never_deletes(tmp_path: Path) -> None:
    reviews = tmp_path / "reviews"
    reviews.mkdir()
    old_review = make_old(reviews, "pr-1")
    temp = tmp_path / "temp"
    temp.mkdir()
    old_temp = make_old(temp, "stale")
    lines: list[str] = []

    prune_ephemeral.prune_reviews(str(reviews), 24, False, lines.append)
    prune_ephemeral.prune_temp(str(temp), 7, False, lines.append)

    assert old_review.is_dir() and old_temp.is_dir()
    assert any("wuerde loeschen" in line for line in lines)
    assert any("gefunden" in line for line in lines)


def test_lock_file_and_young_folders_are_kept_even_with_apply_flag_off(tmp_path: Path) -> None:
    reviews = tmp_path / "reviews"
    reviews.mkdir()
    locked = make_old(reviews, "locked", "sub")
    (locked / "LOCK.txt").write_text("x", encoding="utf-8")
    os.utime(locked, (OLD, OLD))
    os.utime(reviews / "locked", (OLD, OLD))
    young = reviews / "young"
    young.mkdir()
    cutoff = time.time() - 24 * 3600
    assert prune_ephemeral.review_verdict(str(reviews / "locked"), str(reviews), cutoff, {}) == "lock"
    assert prune_ephemeral.review_verdict(str(young), str(reviews), cutoff, {}) == "jung"


def test_claude_temp_folder_is_never_listed(tmp_path: Path) -> None:
    temp = tmp_path / "temp"
    temp.mkdir()
    make_old(temp, "claude")
    lines: list[str] = []
    prune_ephemeral.prune_temp(str(temp), 7, False, lines.append)
    assert "0 Eintraege" in lines[0]


@pytest.mark.skipif(sys.platform != "win32", reason="the janitor purges with robocopy on Windows")
def test_builtin_selftest_passes(capsys: pytest.CaptureFixture[str]) -> None:
    prune_ephemeral.selftest()
    assert "selftest ok" in capsys.readouterr().out
