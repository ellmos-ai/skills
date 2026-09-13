#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portable smoke tests for a deployed community-outreach runtime."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_ROOT = TEST_ROOT / "scripts" if (TEST_ROOT / "scripts" / "outreach_engine.py").exists() else TEST_ROOT
sys.path.insert(0, str(RUNTIME_ROOT))

from outreach_engine import CommunityOutreachEngine, canonicalize_url  # noqa: E402


def _minimal_workspace(path: Path) -> None:
    path.mkdir()
    (path / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "id": "org/tool",
                        "name": "tool",
                        "url": "https://github.com/org/tool",
                        "problems_solved": ["Ein konkretes Problem"],
                        "last_promoted_at": None,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (path / "POST-EINGANG.md").write_text("# Queue\n", encoding="utf-8")
    (path / "POST-AUSGANG.md").write_text("# Ausgang\n", encoding="utf-8")
    (path / "POSTVERZEICHNIS.md").write_text("# Register\n", encoding="utf-8")


def test_projected_core_is_importable_and_exact(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    _minimal_workspace(workspace)

    result = CommunityOutreachEngine(workspace, dry_run=True).run_full_cycle()

    assert result["status"] == "needs-action"
    assert canonicalize_url("https://example.org/thread/1") != canonicalize_url("https://example.org/thread/10")


def test_projected_runner_cli_is_write_free(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    _minimal_workspace(workspace)
    before = {path.name: path.read_bytes() for path in workspace.iterdir() if path.is_file()}

    completed = subprocess.run(
        [
            sys.executable,
            str(RUNTIME_ROOT / "outreach_runner.py"),
            "--workspace",
            str(workspace),
            "--full-run",
            "--dry-run",
            "--json",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    after = {path.name: path.read_bytes() for path in workspace.iterdir() if path.is_file()}
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["status"] == "needs-action"
    assert after == before
