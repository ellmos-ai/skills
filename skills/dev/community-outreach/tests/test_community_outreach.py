#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Behavior and regression tests for the community-outreach core."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import deploy_runtime
import outreach_engine
import setup_scheduler
from init_outreach_workspace import bootstrap_workspace
from outreach_engine import CommunityOutreachEngine


@pytest.fixture
def sample_repos() -> list[dict]:
    return [
        {
            "name": "super-tool",
            "org": "my-org",
            "url": "https://github.com/my-org/super-tool",
            "description": "Ein fantastisches Werkzeug.",
            "usecases": ["Testing", "Automation"],
            "solved_problems": ["Manuelle Tests", "Hohe Fehlerquote"],
            "last_promoted": None,
        },
        {
            "name": "data-cruncher",
            "org": "my-org",
            "url": "https://github.com/my-org/data-cruncher",
            "description": "Schnelle Datenanalyse.",
            "usecases": ["Data Processing"],
            "solved_problems": ["Langsame Auswertung"],
            "last_promoted": "2026-08-01T00:00:00",
        },
    ]


@pytest.fixture
def temp_workspace(tmp_path: Path, sample_repos: list[dict]) -> Path:
    workspace = tmp_path / "test_outreach"
    bootstrap_workspace(workspace, repo_list=sample_repos)
    return workspace


class RecordingPublisher:
    def __init__(self, receipt: dict):
        self.receipt = receipt
        self.calls: list[dict] = []

    def publish(self, proposal: dict) -> dict:
        self.calls.append(proposal)
        return dict(self.receipt)


class DynamicPublisher:
    def __init__(self):
        self.calls: list[dict] = []

    def publish(self, proposal: dict) -> dict:
        self.calls.append(proposal)
        return verified_receipt(f"remote-{len(self.calls)}", proposal["target_url"])


def verified_receipt(post_id: str, target_url: str) -> dict:
    return {
        "verified": True,
        "platform_post_id": post_id,
        "published_url": target_url,
        "target_url": target_url,
        "platform": "Reddit",
        "published_at": "2026-08-29T08:00:00+02:00",
    }


def proposal_block(
    proposal_id: str,
    *,
    approved: bool,
    target_url: str,
    repo: str = "my-org/super-tool",
) -> str:
    checked = "x" if approved else " "
    return f"""### [{proposal_id}] Lösungsvorschlag
- **Plattform:** Reddit
- **Ziel-URL / Thread:** [{target_url}]({target_url})
- **Lösungs-Repo:** `{repo}`
- [{checked}] Genehmigt

#### Textvorschlag:
```markdown
Eine konkrete, hilfreiche Antwort.
```

"""


def snapshot_tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_workspace_bootstrap(temp_workspace: Path) -> None:
    for filename in (
        "USECASES.md",
        "usecases.json",
        "POST-EINGANG.md",
        "POST-AUSGANG.md",
        "POSTVERZEICHNIS.md",
        "ACCOUNTVERZEICHNIS.md",
    ):
        assert (temp_workspace / filename).exists()


def test_workspace_bootstrap_respects_explicit_empty_repo_list(tmp_path: Path) -> None:
    workspace = tmp_path / "empty-bootstrap"

    bootstrap_workspace(workspace, repo_list=[])

    data = json.loads((workspace / "usecases.json").read_text(encoding="utf-8"))
    assert data["repositories"] == []


def test_phase3_is_needs_action_until_a_valid_draft_is_persisted(temp_workspace: Path) -> None:
    before = snapshot_tree(temp_workspace)

    result = CommunityOutreachEngine(temp_workspace).phase3_research_and_stage()

    assert result is not None
    assert result["repo_name"] == "super-tool"
    assert result["platform"] == "Reddit"
    assert result["status"] == "needs-action"
    assert snapshot_tree(temp_workspace) == before


def test_missing_usecases_never_reports_completed(tmp_path: Path) -> None:
    workspace = tmp_path / "empty-workspace"
    workspace.mkdir()

    result = CommunityOutreachEngine(workspace, dry_run=True).run_full_cycle()

    assert result["status"] == "needs-action"
    assert result["staged_candidate"]["reason"] == "no-active-repositories"


def test_runtime_schema_is_read_compatibly(tmp_path: Path) -> None:
    workspace = tmp_path / "runtime-schema"
    workspace.mkdir()
    (workspace / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "id": "org/recent",
                        "name": "recent",
                        "url": "https://example.invalid/recent",
                        "problems_solved": ["Aktuelles Problem"],
                        "last_promoted_at": "2026-08-20T00:00:00+00:00",
                    },
                    {
                        "id": "org/never",
                        "name": "never",
                        "url": "https://example.invalid/never",
                        "problems_solved": ["Noch ungelöst"],
                        "last_promoted_at": None,
                    },
                ],
                "last_platform": "Reddit",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = CommunityOutreachEngine(workspace, dry_run=True).phase3_research_and_stage()

    assert result is not None
    assert result["repo_name"] == "never"
    assert result["platform"] == "YouTube"
    assert result["target_problem"] == "Noch ungelöst"
    assert result["status"] == "needs-action"


def test_dry_run_is_byte_and_directory_pure(tmp_path: Path, sample_repos: list[dict]) -> None:
    workspace = tmp_path / "dry-run"
    workspace.mkdir()
    (workspace / "usecases.json").write_text(
        json.dumps({"repositories": sample_repos}, ensure_ascii=False), encoding="utf-8"
    )
    (workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n"
        + proposal_block(
            "OUTBOUND-PROPOSAL-DRY-1",
            approved=True,
            target_url="https://www.reddit.com/r/python/comments/dry/thread/",
        ),
        encoding="utf-8",
    )
    entries = "\n".join(
        f"### [OLD-{index}] Veröffentlicht\n- **Ziel-URL:** https://example.invalid/{index}\n- **Status:** published\n"
        for index in range(30)
    )
    (workspace / "POST-AUSGANG.md").write_text("# Ausgang\n\n" + entries, encoding="utf-8")
    (workspace / "POSTVERZEICHNIS.md").write_text("# Register\n", encoding="utf-8")
    before_files = snapshot_tree(workspace)
    before_dirs = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_dir())
    publisher = RecordingPublisher(verified_receipt("must-not-run", "https://example.invalid/dry"))

    result = CommunityOutreachEngine(workspace, dry_run=True, publisher=publisher).run_full_cycle()

    after_dirs = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_dir())
    assert result["status"] == "needs-action"
    assert publisher.calls == []
    assert snapshot_tree(workspace) == before_files
    assert after_dirs == before_dirs


def test_unverified_receipt_keeps_approval_and_state_unchanged(temp_workspace: Path) -> None:
    target_url = "https://www.reddit.com/r/python/comments/receipt/thread/"
    inbox = "# Queue\n\n" + proposal_block(
        "OUTBOUND-PROPOSAL-RECEIPT-1", approved=True, target_url=target_url
    )
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    before = snapshot_tree(temp_workspace)
    publisher = RecordingPublisher({"verified": False, "reason": "no remote id"})

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["needs-action"]
    assert len(publisher.calls) == 1
    assert snapshot_tree(temp_workspace) == before


@pytest.mark.parametrize("receipt", [True, None, {"verified": True}])
def test_bool_missing_or_malformed_receipt_cannot_publish_or_rotate(temp_workspace: Path, receipt: object) -> None:
    target_url = "https://example.invalid/malformed"
    inbox = "# Queue\n\n" + proposal_block(
        "OUTBOUND-PROPOSAL-MALFORMED-1", approved=True, target_url=target_url
    )
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    before = snapshot_tree(temp_workspace)
    publisher = RecordingPublisher(receipt if isinstance(receipt, dict) else {})
    publisher.receipt = receipt

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["needs-action"]
    assert snapshot_tree(temp_workspace) == before


@pytest.mark.parametrize("broken_field", ["published_at", "published_url"])
def test_receipt_requires_valid_timestamp_and_permalink(temp_workspace: Path, broken_field: str) -> None:
    target_url = "https://dev.to/example/real-thread"
    inbox = "# Queue\n\n" + proposal_block(
        "OUTBOUND-PROPOSAL-BROKEN-RECEIPT-1", approved=True, target_url=target_url
    )
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    receipt = verified_receipt("remote-broken", target_url)
    receipt[broken_field] = "not-a-valid-value"
    publisher = RecordingPublisher(receipt)
    before = snapshot_tree(temp_workspace)

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["needs-action"]
    assert snapshot_tree(temp_workspace) == before


def test_duplicate_url_blocks_publisher_and_preserves_queue(temp_workspace: Path) -> None:
    target_url = "https://www.reddit.com/r/Python/comments/AbC123/example_thread/?utm_source=test"
    (temp_workspace / "posts_history.json").write_text(
        json.dumps(
            [
                {
                    "post_id": "OLDER",
                    "target_url": "https://reddit.com/r/python/comments/abc123/example_thread/",
                    "status": "published",
                    "receipt_verified": True,
                }
            ]
        ),
        encoding="utf-8",
    )
    inbox = "# Queue\n\n" + proposal_block(
        "OUTBOUND-PROPOSAL-DUP-1", approved=True, target_url=target_url
    )
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    publisher = RecordingPublisher(verified_receipt("remote-2", target_url))

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["duplicate"]
    assert publisher.calls == []
    assert (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8") == inbox


def test_invalid_target_blocks_publisher_and_preserves_queue(temp_workspace: Path) -> None:
    target_url = "not-a-valid-thread-url"
    inbox = "# Queue\n\n" + proposal_block(
        "OUTBOUND-PROPOSAL-INVALID-1", approved=True, target_url=target_url
    )
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    publisher = RecordingPublisher(verified_receipt("must-not-run", target_url))

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["invalid-target"]
    assert publisher.calls == []
    assert (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8") == inbox


def test_mixed_queue_removes_only_receipted_span(temp_workspace: Path) -> None:
    target_url = "https://example.invalid/approved"
    approved = proposal_block(
        "OUTBOUND-PROPOSAL-APPROVED-1", approved=True, target_url=target_url
    )
    pending = proposal_block(
        "OUTBOUND-PROPOSAL-PENDING-1",
        approved=False,
        target_url="https://example.invalid/pending",
    )
    inbox = "# Queue mit eigener Einleitung\n\n" + approved + "<!-- Trenner bleibt -->\n" + pending + "TAIL\n"
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    publisher = RecordingPublisher(verified_receipt("remote-approved-1", target_url))

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    updated = (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8")
    assert [item["status"] for item in results] == ["published"]
    assert "OUTBOUND-PROPOSAL-APPROVED-1" not in updated
    assert pending in updated
    assert "<!-- Trenner bleibt -->" in updated
    assert updated.endswith("TAIL\n")


def test_restart_finalizes_existing_verified_receipt_without_republishing(temp_workspace: Path) -> None:
    proposal_id = "OUTBOUND-PROPOSAL-RESTART-1"
    target_url = "https://example.invalid/restart"
    inbox = "# Queue\n\n" + proposal_block(proposal_id, approved=True, target_url=target_url)
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    (temp_workspace / "posts_history.json").write_text(
        json.dumps(
            [
                {
                    "post_id": proposal_id,
                    "target_url": target_url,
                    "repo": "my-org/super-tool",
                    "platform": "Reddit",
                    "content": "Eine konkrete, hilfreiche Antwort.",
                    "status": "published",
                    "receipt_verified": True,
                    "platform_post_id": "remote-restart-1",
                    "published_url": target_url + "#comment-1",
                    "published_at": "2026-08-29T08:00:00+02:00",
                    "date": "2026-08-29",
                }
            ]
        ),
        encoding="utf-8",
    )
    publisher = RecordingPublisher(verified_receipt("must-not-run", target_url))

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["recovered"]
    assert publisher.calls == []
    assert proposal_id not in (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8")
    assert proposal_id in (temp_workspace / "POST-AUSGANG.md").read_text(encoding="utf-8")


def test_registry_projection_excludes_unverified_legacy_claims(temp_workspace: Path) -> None:
    (temp_workspace / "posts_history.json").write_text(
        json.dumps(
            [
                {
                    "post_id": "LEGACY-WITHOUT-RECEIPT",
                    "target_url": "https://dev.to/example/legacy",
                    "platform": "Reddit",
                    "status": "published",
                }
            ]
        ),
        encoding="utf-8",
    )
    target_url = "https://dev.to/example/verified"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n"
        + proposal_block("OUTBOUND-PROPOSAL-VERIFIED-1", approved=True, target_url=target_url),
        encoding="utf-8",
    )

    CommunityOutreachEngine(temp_workspace, publisher=DynamicPublisher()).phase2_outbound_execution()

    registry = (temp_workspace / "POSTVERZEICHNIS.md").read_text(encoding="utf-8")
    assert "OUTBOUND-PROPOSAL-VERIFIED-1" in registry
    assert "LEGACY-WITHOUT-RECEIPT" not in registry


def test_recovery_rejects_same_id_bound_to_another_target(temp_workspace: Path) -> None:
    proposal_id = "OUTBOUND-PROPOSAL-CONFLICT-1"
    target_url = "https://dev.to/example/new-target"
    inbox = "# Queue\n\n" + proposal_block(proposal_id, approved=True, target_url=target_url)
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    (temp_workspace / "posts_history.json").write_text(
        json.dumps(
            [
                {
                    "post_id": proposal_id,
                    "target_url": "https://dev.to/example/different-target",
                    "platform": "Reddit",
                    "status": "published",
                    "receipt_verified": True,
                    "platform_post_id": "remote-old",
                }
            ]
        ),
        encoding="utf-8",
    )
    publisher = DynamicPublisher()

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["receipt-conflict"]
    assert publisher.calls == []
    assert (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8") == inbox


def test_recovery_rejects_same_basename_from_another_organization(temp_workspace: Path) -> None:
    proposal_id = "OUTBOUND-PROPOSAL-ORG-CONFLICT-1"
    target_url = "https://dev.to/example/same-target"
    inbox = "# Queue\n\n" + proposal_block(
        proposal_id, approved=True, target_url=target_url, repo="org-b/tool"
    )
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    (temp_workspace / "posts_history.json").write_text(
        json.dumps(
            [
                {
                    "post_id": proposal_id,
                    "target_url": target_url,
                    "repo": "org-a/tool",
                    "platform": "Reddit",
                    "status": "published",
                    "receipt_verified": True,
                    "platform_post_id": "remote-org-a",
                }
            ]
        ),
        encoding="utf-8",
    )

    results = CommunityOutreachEngine(temp_workspace, publisher=DynamicPublisher()).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["receipt-conflict"]
    assert (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8") == inbox


def test_only_one_approved_post_can_reach_publisher_per_cycle(temp_workspace: Path) -> None:
    first = proposal_block(
        "OUTBOUND-PROPOSAL-LIMIT-1", approved=True, target_url="https://dev.to/example/first"
    )
    second = proposal_block(
        "OUTBOUND-PROPOSAL-LIMIT-2", approved=True, target_url="https://dev.to/example/second"
    )
    (temp_workspace / "POST-EINGANG.md").write_text("# Queue\n\n" + first + second, encoding="utf-8")
    publisher = DynamicPublisher()

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert len(publisher.calls) == 1
    assert [item["status"] for item in results] == ["published", "deferred"]
    remaining = (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8")
    assert "OUTBOUND-PROPOSAL-LIMIT-1" not in remaining
    assert "OUTBOUND-PROPOSAL-LIMIT-2" in remaining


def test_markdown_heading_inside_post_text_is_not_a_queue_boundary(temp_workspace: Path) -> None:
    target_url = "https://dev.to/example/markdown-heading"
    block = proposal_block(
        "OUTBOUND-PROPOSAL-MARKDOWN-1", approved=True, target_url=target_url
    ).replace(
        "Eine konkrete, hilfreiche Antwort.",
        "Eine konkrete Antwort mit Beispiel:\n### [OUTBOUND-PROPOSAL-NOT-REAL] Nur Text",
    )
    (temp_workspace / "POST-EINGANG.md").write_text("# Queue\n\n" + block, encoding="utf-8")
    publisher = DynamicPublisher()

    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert [item["status"] for item in results] == ["published"]
    assert len(publisher.calls) == 1


def test_rotation_matches_repo_identity_not_substring(tmp_path: Path) -> None:
    workspace = tmp_path / "repo-identity"
    workspace.mkdir()
    (workspace / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {"id": "org/tool", "name": "tool", "last_promoted_at": None},
                    {"id": "org/toolbox", "name": "toolbox", "last_promoted_at": None},
                ]
            }
        ),
        encoding="utf-8",
    )
    (workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n"
        + proposal_block(
            "OUTBOUND-PROPOSAL-TOOLBOX-1",
            approved=True,
            target_url="https://dev.to/example/toolbox",
            repo="org/toolbox",
        ),
        encoding="utf-8",
    )
    publisher = DynamicPublisher()

    CommunityOutreachEngine(workspace, publisher=publisher).phase2_outbound_execution()

    repositories = json.loads((workspace / "usecases.json").read_text(encoding="utf-8"))["repositories"]
    assert repositories[0]["last_promoted_at"] is None
    assert repositories[0].get("total_promotions", 0) == 0
    assert repositories[1]["total_promotions"] == 1


def test_rotation_distinguishes_same_basename_across_organizations(tmp_path: Path) -> None:
    workspace = tmp_path / "same-basename"
    workspace.mkdir()
    (workspace / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {"id": "org-a/tool", "name": "tool", "last_promoted_at": None},
                    {"id": "org-b/tool", "name": "tool", "last_promoted_at": None},
                ]
            }
        ),
        encoding="utf-8",
    )
    (workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n"
        + proposal_block(
            "OUTBOUND-PROPOSAL-ORG-B-1",
            approved=True,
            target_url="https://dev.to/example/org-b-tool",
            repo="org-b/tool",
        ),
        encoding="utf-8",
    )

    CommunityOutreachEngine(workspace, publisher=DynamicPublisher()).phase2_outbound_execution()

    repositories = json.loads((workspace / "usecases.json").read_text(encoding="utf-8"))["repositories"]
    assert repositories[0]["last_promoted_at"] is None
    assert repositories[0].get("total_promotions", 0) == 0
    assert repositories[1]["total_promotions"] == 1


@pytest.mark.parametrize(
    ("left", "right", "same"),
    [
        (
            "https://www.reddit.com/r/Python/comments/AbC123/thread/?utm_source=x",
            "https://reddit.com/r/python/comments/abc123/thread",
            True,
        ),
        (
            "http://reddit.com/r/python/comments/abc123/thread",
            "https://www.reddit.com/r/Python/comments/AbC123/thread/",
            True,
        ),
        ("https://youtu.be/Video42?t=7", "https://www.youtube.com/watch?v=Video42", True),
        ("https://example.invalid/thread/1", "https://example.invalid/thread/10", False),
        ("https://example.invalid/thread?a=1", "https://example.invalid/thread?a=2", False),
    ],
)
def test_url_canonicalization_is_exact(left: str, right: str, same: bool) -> None:
    assert (outreach_engine.canonicalize_url(left) == outreach_engine.canonicalize_url(right)) is same


def test_archive_keeps_newest_complete_entries_and_is_idempotent(temp_workspace: Path) -> None:
    entries = [
        f"### [POST-{index}] Veröffentlicht\n- **Zeile A:** {index}\n- **Zeile B:** vollständig-{index}\n"
        for index in range(1, 6)
    ]
    (temp_workspace / "POST-AUSGANG.md").write_text(
        "# Ausgang\n\nEinleitung bleibt.\n\n" + "\n".join(entries), encoding="utf-8"
    )
    engine = CommunityOutreachEngine(temp_workspace)

    archived = engine.phase4_cut_and_clue_archive(max_outbox_entries=2)

    live = (temp_workspace / "POST-AUSGANG.md").read_text(encoding="utf-8")
    archive_files = sorted((temp_workspace / "_archive").glob("POST-AUSGANG_*.md"))
    assert archived == 3
    assert len(archive_files) == 1
    archive = archive_files[0].read_text(encoding="utf-8")
    assert all(f"vollständig-{index}" in archive for index in range(1, 4))
    assert all(f"vollständig-{index}" in live for index in range(4, 6))
    assert "vollständig-3" not in live
    before_second_run = snapshot_tree(temp_workspace)
    assert engine.phase4_cut_and_clue_archive(max_outbox_entries=2) == 0
    assert snapshot_tree(temp_workspace) == before_second_run


def test_archive_ignores_heading_like_text_inside_fenced_content(temp_workspace: Path) -> None:
    entries = [
        "### [POST-1] Veröffentlicht\n```text\nAntwort\n### [NOT-AN-ENTRY] Textinhalt\n```\n",
        "### [POST-2] Veröffentlicht\n```text\nAntwort 2\n```\n",
        "### [POST-3] Veröffentlicht\n```text\nAntwort 3\n```\n",
    ]
    (temp_workspace / "POST-AUSGANG.md").write_text("# Ausgang\n\n" + "\n".join(entries), encoding="utf-8")

    archived = CommunityOutreachEngine(temp_workspace).phase4_cut_and_clue_archive(max_outbox_entries=2)

    assert archived == 1
    live = (temp_workspace / "POST-AUSGANG.md").read_text(encoding="utf-8")
    archive = next((temp_workspace / "_archive").glob("POST-AUSGANG_*.md")).read_text(encoding="utf-8")
    assert "POST-1" in archive
    assert "NOT-AN-ENTRY" in archive
    assert "POST-2" in live and "POST-3" in live


def test_cli_dry_run_and_runtime_adapter_are_read_only(temp_workspace: Path, tmp_path: Path) -> None:
    deployed = tmp_path / "deployed"
    deployed.mkdir()
    shutil.copy2(SCRIPTS_DIR / "outreach_engine.py", deployed / "outreach_engine.py")
    shutil.copy2(SCRIPTS_DIR / "outreach_runner.py", deployed / "outreach_runner.py")
    before = snapshot_tree(temp_workspace)

    completed = subprocess.run(
        [
            sys.executable,
            str(deployed / "outreach_runner.py"),
            "--workspace",
            str(temp_workspace),
            "--full-run",
            "--dry-run",
            "--json",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["status"] == "needs-action"
    assert snapshot_tree(temp_workspace) == before


def test_runtime_deployer_is_path_agnostic_and_preserves_data(tmp_path: Path) -> None:
    target = tmp_path / "runtime with spaces"
    target.mkdir()
    sentinel = target / "usecases.json"
    sentinel.write_text('{"sentinel": true}\n', encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "deploy_runtime.py"), "--target", str(target), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    receipt = json.loads(completed.stdout)
    assert receipt["status"] == "deployed"
    assert set(receipt["files"]) == {"README.md", "outreach_engine.py", "outreach_runner.py", "tests/test_outreach.py"}
    assert sentinel.read_text(encoding="utf-8") == '{"sentinel": true}\n'
    assert (target / "outreach_engine.py").read_bytes() == (SCRIPTS_DIR / "outreach_engine.py").read_bytes()
    assert (target / "outreach_runner.py").read_bytes() == (SCRIPTS_DIR / "outreach_runner.py").read_bytes()

    checked = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "deploy_runtime.py"), "--target", str(target), "--check", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert checked.returncode == 0, checked.stderr
    assert json.loads(checked.stdout)["status"] == "current"


def test_deployed_runner_dry_run_does_not_create_workspace_bytecode(tmp_path: Path) -> None:
    target = tmp_path / "deployed-runtime"
    target.mkdir()
    (target / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "id": "org/tool",
                        "name": "tool",
                        "url": "https://github.com/org/tool",
                        "problems_solved": ["Ein Problem"],
                        "last_promoted_at": None,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    deploy_runtime.deploy(target)
    before = snapshot_tree(target)
    before_dirs = sorted(path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_dir())

    completed = subprocess.run(
        [
            sys.executable,
            str(target / "outreach_runner.py"),
            "--workspace",
            str(target),
            "--full-run",
            "--dry-run",
            "--json",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    after_dirs = sorted(path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_dir())
    assert completed.returncode == 0, completed.stderr
    assert snapshot_tree(target) == before
    assert after_dirs == before_dirs


def test_runtime_deployer_rolls_back_all_files_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "rollback-runtime"
    old = b"old-runtime-content\n"
    for relative in deploy_runtime.SOURCE_FILES:
        destination = target / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(old)
    original_write = deploy_runtime._atomic_write
    calls = 0

    def fail_second_write(path: Path, content: bytes) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("injected deployment failure")
        original_write(path, content)

    monkeypatch.setattr(deploy_runtime, "_atomic_write", fail_second_write)

    with pytest.raises(RuntimeError, match="injected deployment failure"):
        deploy_runtime.deploy(target)

    assert all((target / Path(relative)).read_bytes() == old for relative in deploy_runtime.SOURCE_FILES)


def test_unix_cron_quotes_executable_script_and_workspace_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workspace = tmp_path / "workspace with spaces"
    workspace.mkdir()
    (workspace / "outreach_runner.py").write_text("# runner\n", encoding="utf-8")
    monkeypatch.setattr(setup_scheduler.sys, "executable", "/opt/Python With Space/python")

    setup_scheduler.setup_unix_cron(workspace, schedule_cron="0 9 * * *")

    output = capsys.readouterr().out
    assert "'/opt/Python With Space/python'" in output
    assert f"'{workspace / 'outreach_runner.py'}'" in output
    assert f"'{workspace}'" in output
