from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "clean_flutter_builds.py"
SPEC = importlib.util.spec_from_file_location("clean_flutter_builds", SCRIPT)
assert SPEC and SPEC.loader
clean_flutter_builds = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(clean_flutter_builds)


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, list[str]]:
    """A Flutter project with build/ and .dart_tool/; purge_dir only records, nothing is deleted."""
    (tmp_path / "pubspec.yaml").write_text("name: demo\n", encoding="utf-8")
    (tmp_path / "build").mkdir()
    (tmp_path / ".dart_tool").mkdir()
    purged: list[str] = []
    monkeypatch.setattr(clean_flutter_builds, "purge_dir", lambda path: purged.append(Path(path).name))
    return tmp_path, purged


def run(monkeypatch: pytest.MonkeyPatch, *args: str) -> int:
    monkeypatch.setattr(sys, "argv", ["clean_flutter_builds.py", *args])
    return clean_flutter_builds.main()


def test_default_is_a_dry_run(project, monkeypatch, capsys) -> None:
    root, purged = project
    assert run(monkeypatch, str(root)) == 0
    assert purged == []
    assert "DRY-RUN" in capsys.readouterr().out


def test_old_dry_run_flag_still_accepted_and_changes_nothing(project, monkeypatch) -> None:
    root, purged = project
    assert run(monkeypatch, str(root), "--dry-run") == 0
    assert purged == []


def test_apply_deletes_exactly_the_cache_folders(project, monkeypatch) -> None:
    root, purged = project
    assert run(monkeypatch, str(root), "--apply") == 0
    assert sorted(purged) == [".dart_tool", "build"]
