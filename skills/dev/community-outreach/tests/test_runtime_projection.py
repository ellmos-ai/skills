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


def test_parse_traffic_report_extracts_metrics_and_exclusions() -> None:
    from githubbot_bridge import parse_traffic_report

    sample_md = """## GitHub Traffic Report -- 2026-09-08
**ellmos-ai/skills**
  Views (14d): 215 gesamt / 63 unique
  Clones (14d): 1767 gesamt / 513 unique

**ellmos-ai/bach**
  Views (14d): 77 gesamt / 17 unique
  Clones (14d): 490 gesamt / 130 unique

### Diese Module sind privat:
- **ellmos-ai** (2): internal-core, secret-tool
- **lukisch** (1): private-notes

### Archiviert:
- **ellmos-ai** (1): old-legacy
"""
    traffic_map, private_set, archived_set = parse_traffic_report(sample_md)

    assert "ellmos-ai/skills" in traffic_map
    assert traffic_map["ellmos-ai/skills"].clones_total == 1767
    assert traffic_map["ellmos-ai/skills"].clones_unique == 513
    assert traffic_map["ellmos-ai/skills"].views_unique == 63
    assert traffic_map["ellmos-ai/skills"].traffic_score() == 513 * 2 + 63

    assert "internal-core" in private_set
    assert "ellmos-ai/internal-core" in private_set
    assert "old-legacy" in archived_set


def test_classify_repo_blocks_private_archived_and_forks() -> None:
    from githubbot_bridge import classify_repo

    registry = {
        "org/fork-tool": {"github": {"visibility": "public", "fork": True, "archived": False}},
        "org/private-tool": {"github": {"visibility": "private", "fork": False, "archived": False}},
        "org/archived-tool": {"github": {"visibility": "public", "fork": False, "archived": True}},
        "org/good-tool": {"github": {"visibility": "public", "fork": False, "archived": False}},
    }

    # Fork check
    c_fork = classify_repo("org/fork-tool", "org", "fork-tool", registry, set(), set())
    assert not c_fork.is_active
    assert c_fork.reason == "foreign_fork"

    # Private check
    c_priv = classify_repo("org/private-tool", "org", "private-tool", registry, set(), set())
    assert not c_priv.is_active
    assert c_priv.reason == "private"

    # Archived check
    c_arch = classify_repo("org/archived-tool", "org", "archived-tool", registry, set(), set())
    assert not c_arch.is_active
    assert c_arch.reason == "archived"

    # Meta profile check
    c_meta = classify_repo("lukisch/lukisch", "lukisch", "lukisch", registry, set(), set())
    assert not c_meta.is_active
    assert c_meta.reason == "profile_meta"

    # Good tool check
    c_good = classify_repo("org/good-tool", "org", "good-tool", registry, set(), set())
    assert c_good.is_active
    assert c_good.reason == "eligible"


def test_select_candidate_repository_prioritizes_traffic_and_enforces_cooldown() -> None:
    from datetime import datetime, timezone

    from outreach_engine import select_candidate_repository

    now = datetime(2026, 9, 8, 12, 0, 0, tzinfo=timezone.utc)

    repos = [
        # Candidate 1: High traffic, promoted 2 days ago (on cooldown!)
        {
            "id": "org/high-traffic-recent",
            "name": "high-traffic-recent",
            "active": True,
            "last_promoted_at": "2026-09-06T12:00:00+00:00",
            "priority": "high",
            "traffic": {"clones_unique_14d": 500, "views_unique_14d": 100, "traffic_score": 1100},
        },
        # Candidate 2: Medium traffic, never promoted (ready!)
        {
            "id": "org/medium-traffic-ready",
            "name": "medium-traffic-ready",
            "active": True,
            "last_promoted_at": None,
            "priority": "high",
            "traffic": {"clones_unique_14d": 50, "views_unique_14d": 20, "traffic_score": 120},
        },
        # Candidate 3: Low traffic, never promoted
        {
            "id": "org/low-traffic",
            "name": "low-traffic",
            "active": True,
            "last_promoted_at": None,
            "priority": "normal",
            "traffic": {"clones_unique_14d": 1, "views_unique_14d": 1, "traffic_score": 3},
        },
        # Candidate 4: Private tool (should be completely excluded)
        {
            "id": "org/secret",
            "name": "secret",
            "active": False,
            "exclusion_reason": "private",
            "traffic": {"clones_unique_14d": 1000, "views_unique_14d": 1000, "traffic_score": 3000},
        },
    ]

    candidate, meta = select_candidate_repository(repos, cooldown_days=7.0, now=now)

    assert candidate is not None
    # Candidate 2 should be selected because Candidate 1 is on cooldown and Candidate 4 is excluded
    assert candidate["id"] == "org/medium-traffic-ready"
    assert meta["clones_unique_14d"] == 50
    assert not meta["is_cooldown"]


def test_phase3_skips_queued_proposals(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "id": "org/queued-tool",
                        "name": "queued-tool",
                        "url": "https://github.com/org/queued-tool",
                        "priority": "high",
                        "last_promoted_at": None,
                        "traffic": {"clones_unique_14d": 500, "views_unique_14d": 50, "traffic_score": 1050},
                    },
                    {
                        "id": "org/next-tool",
                        "name": "next-tool",
                        "url": "https://github.com/org/next-tool",
                        "priority": "normal",
                        "last_promoted_at": None,
                        "traffic": {"clones_unique_14d": 100, "views_unique_14d": 10, "traffic_score": 210},
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    inbox_content = """# POST-EINGANG

### [OUTBOUND-PROPOSAL-QUEUED-20260921-1200] Forum
- **Plattform:** Reddit
- **Ziel-URL:** https://example.com/thread/1
- **Lösungs-Repo:** org/queued-tool
- [ ] Genehmigt

#### Textvorschlag:
```text
Sample text
```
"""
    (workspace / "POST-EINGANG.md").write_text(inbox_content, encoding="utf-8")
    (workspace / "POST-AUSGANG.md").write_text("# Ausgang\n", encoding="utf-8")
    (workspace / "POSTVERZEICHNIS.md").write_text("# Register\n", encoding="utf-8")

    engine = CommunityOutreachEngine(workspace)
    result = engine.phase3_research_and_stage()

    assert result is not None
    assert result["repo_name"] == "next-tool"
