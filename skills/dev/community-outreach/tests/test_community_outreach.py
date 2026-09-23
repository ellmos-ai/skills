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

PUBLIC_META = {"visibility": "public", "archived": False, "fork": False}

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
            "github_meta": PUBLIC_META,
        },
        {
            "name": "data-cruncher",
            "org": "my-org",
            "url": "https://github.com/my-org/data-cruncher",
            "description": "Schnelle Datenanalyse.",
            "usecases": ["Data Processing"],
            "solved_problems": ["Langsame Auswertung"],
            "last_promoted": "2026-08-01T00:00:00",
            "github_meta": PUBLIC_META,
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
                        "github_meta": PUBLIC_META,
                    },
                    {
                        "id": "org/never",
                        "name": "never",
                        "url": "https://example.invalid/never",
                        "problems_solved": ["Noch ungelöst"],
                        "last_promoted_at": None,
                        "github_meta": PUBLIC_META,
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
    published, unconfirmed = registry.split("## Unbestätigt", 1)
    assert "OUTBOUND-PROPOSAL-VERIFIED-1" in published
    assert "LEGACY-WITHOUT-RECEIPT" not in published
    assert "LEGACY-WITHOUT-RECEIPT" in unconfirmed


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
    assert set(receipt["files"]) == {
        "README.md",
        "githubbot_bridge.py",
        "outreach_engine.py",
        "outreach_runner.py",
        "tests/test_outreach.py",
    }
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


def _queued_inbox(repo: str) -> str:
    return f"""# POST-EINGANG

### [OUTBOUND-PROPOSAL-Q-20260923-1200] Forum
- **Plattform:** Reddit
- **Ziel-URL:** https://example.com/thread/1
- **Lösungs-Repo:** {repo}
- [ ] Genehmigt

#### Textvorschlag:
```text
Sample text
```
"""


def test_phase3_never_falls_back_to_already_queued_repositories(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repo = {"id": "org/only-tool", "name": "only-tool", "url": "https://github.com/org/only-tool", "last_promoted_at": None}
    (workspace / "usecases.json").write_text(json.dumps({"repositories": [repo]}), encoding="utf-8")
    (workspace / "POST-EINGANG.md").write_text(_queued_inbox("org/only-tool"), encoding="utf-8")

    result = CommunityOutreachEngine(workspace).phase3_research_and_stage()

    assert result is not None
    assert result.get("repo_name") != "only-tool"
    assert result["action"] == "configure-repositories"


def test_sync_githubbot_respects_dry_run(tmp_path: Path) -> None:
    githubbot = tmp_path / ".GITHUBBOT"
    (githubbot / "config").mkdir(parents=True)
    (githubbot / "config" / "repo_registry.json").write_text(json.dumps({"repos": {}}), encoding="utf-8")
    (githubbot / "traffic_report.md").write_text(
        "**org/tool**\n  Views (14d): 5 gesamt / 2 unique\n  Clones (14d): 9 gesamt / 4 unique\n", encoding="utf-8")
    workspace = tmp_path / "workspace"
    deploy_runtime.deploy(workspace)  # deployed layout: engine and bridge live inside the workspace
    (workspace / "usecases.json").write_text(json.dumps({"repositories": []}), encoding="utf-8")
    before = snapshot_tree(workspace)
    before_dirs = sorted(p.relative_to(workspace).as_posix() for p in workspace.rglob("*") if p.is_dir())
    env = {k: v for k, v in __import__("os").environ.items() if k != "PYTHONDONTWRITEBYTECODE"}

    completed = subprocess.run(
        [sys.executable, str(workspace / "outreach_engine.py"), "--workspace", str(workspace),
         "--sync-githubbot", "--dry-run"],
        capture_output=True, text=True, encoding="utf-8", check=False,
        env={**env, "GITHUBBOT_DIR": str(githubbot)},
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["status"] == "dry-run"
    assert snapshot_tree(workspace) == before
    assert sorted(p.relative_to(workspace).as_posix() for p in workspace.rglob("*") if p.is_dir()) == before_dirs


def test_skill_profiles_only_reference_published_public_skills() -> None:
    import githubbot_bridge

    repo_root = SKILL_DIR.parent.parent.parent
    for profile in githubbot_bridge.SPECIFIC_SKILL_PROFILES:
        skill_md = repo_root / profile["id"] / "SKILL.md"
        assert skill_md.exists(), profile["id"]
        assert "visibility: public" in skill_md.read_text(encoding="utf-8"), profile["id"]
        assert profile["url"].endswith(profile["id"]), profile["id"]
        assert "traffic" not in profile, f"{profile['id']}: per-skill traffic is not measured by GitHub"


def test_scripts_contain_no_user_specific_home_paths() -> None:
    import re

    home_path = re.compile(r"[a-z]:/users/[^/\"']+/")
    for script in SCRIPTS_DIR.glob("*.py"):
        text = script.read_text(encoding="utf-8").replace("\\", "/").casefold()
        assert not home_path.search(text), script.name


def _githubbot_fixture(tmp_path: Path, registry: dict, traffic: str) -> tuple[Path, Path]:
    githubbot = tmp_path / "gb" / ".GITHUBBOT"
    (githubbot / "config").mkdir(parents=True)
    (githubbot / "config" / "repo_registry.json").write_text(json.dumps({"repos": registry}), encoding="utf-8")
    (githubbot / "traffic_report.md").write_text(traffic, encoding="utf-8")
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "usecases.json").write_text(json.dumps({"repositories": []}), encoding="utf-8")
    return githubbot, workspace / "usecases.json"


def test_sync_imports_only_repos_positively_known_as_public(tmp_path: Path) -> None:
    import githubbot_bridge

    traffic = (
        "**org/known**\n  Views (14d): 5 gesamt / 2 unique\n  Clones (14d): 9 gesamt / 4 unique\n\n"
        "**org/unknown**\n  Views (14d): 5 gesamt / 2 unique\n  Clones (14d): 9 gesamt / 4 unique\n"
    )
    registry = {"org/known": {"github": {"visibility": "public", "fork": False, "archived": False}}}
    githubbot, usecases = _githubbot_fixture(tmp_path, registry, traffic)

    githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)

    data = json.loads(usecases.read_text(encoding="utf-8"))
    assert [repo["id"] for repo in data["repositories"] if repo["id"].startswith("org/")] == ["org/known"]
    assert str(tmp_path) not in json.dumps(data)


def test_repeated_sync_is_idempotent_for_skill_profiles(tmp_path: Path) -> None:
    import githubbot_bridge

    githubbot, usecases = _githubbot_fixture(tmp_path, {}, "")
    first = githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)
    snapshot = json.loads(usecases.read_text(encoding="utf-8"))["repositories"]
    second = githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)
    repos = json.loads(usecases.read_text(encoding="utf-8"))["repositories"]

    profiles = len(githubbot_bridge.SPECIFIC_SKILL_PROFILES)
    assert (first["active_repos"], first["excluded_repos"]) == (profiles, 0)
    assert (second["active_repos"], second["excluded_repos"]) == (profiles, 0)
    assert [r["github_meta"] for r in repos] == [r["github_meta"] for r in snapshot]
    assert all(r["github_meta"]["visibility"] == "public" for r in repos)


def test_phase3_queue_match_is_organisation_exact(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repos = [
        {"id": "org-a/tool", "name": "tool", "url": "https://github.com/org-a/tool", "last_promoted_at": None, "github_meta": PUBLIC_META},
        {"id": "org-b/tool", "name": "tool", "url": "https://github.com/org-b/tool", "last_promoted_at": None, "github_meta": PUBLIC_META},
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")
    (workspace / "POST-EINGANG.md").write_text(_queued_inbox("org-a/tool"), encoding="utf-8")

    result = CommunityOutreachEngine(workspace).phase3_research_and_stage()

    assert result is not None and result.get("repo_url") == "https://github.com/org-b/tool", result


def test_phase3_respects_cooldown_when_every_candidate_is_cooling_down(tmp_path: Path) -> None:
    from datetime import datetime, timedelta, timezone

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    repo = {"id": "org/tool", "name": "tool", "url": "https://github.com/org/tool", "last_promoted_at": recent, "github_meta": PUBLIC_META}
    (workspace / "usecases.json").write_text(json.dumps({"repositories": [repo]}), encoding="utf-8")

    result = CommunityOutreachEngine(workspace).phase3_research_and_stage()

    assert result is not None and result.get("repo_name") is None
    assert result["reason"] == "all-in-cooldown"


def test_sync_drops_stale_per_skill_traffic(tmp_path: Path) -> None:
    import githubbot_bridge

    githubbot, usecases = _githubbot_fixture(tmp_path, {}, "")
    profile = dict(githubbot_bridge.SPECIFIC_SKILL_PROFILES[0])
    profile["traffic"] = {"clones_unique_14d": 32, "views_unique_14d": 18, "traffic_score": 82}
    usecases.write_text(json.dumps({"repositories": [profile]}), encoding="utf-8")

    githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)

    repo = json.loads(usecases.read_text(encoding="utf-8"))["repositories"][0]
    assert set(repo["traffic"]) == {"updated_at"}
    assert "32 Clones" not in (usecases.parent / "USECASES.md").read_text(encoding="utf-8")


def test_synced_catalog_selects_only_confirmed_public_repositories(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    public_meta = {"visibility": "public", "archived": False, "fork": False}
    repos = [
        {"id": "org/unknown", "name": "unknown", "url": "https://github.com/org/unknown",
         "github_meta": {"visibility": "unknown"}, "traffic": {"traffic_score": 999}},
        {"id": "org/missing", "name": "missing", "url": "https://github.com/org/missing",
         "traffic": {"traffic_score": 999}},
        {"id": "org/public", "name": "public", "url": "https://github.com/org/public", "github_meta": public_meta},
    ]
    data = {"repositories": repos, "githubbot_sync": {"githubbot_source": ".GITHUBBOT"}}
    (workspace / "usecases.json").write_text(json.dumps(data), encoding="utf-8")

    result = CommunityOutreachEngine(workspace).phase3_research_and_stage()

    assert result is not None and result.get("repo_name") == "public", result


def test_failed_markdown_export_is_not_reported_as_success(tmp_path: Path) -> None:
    import githubbot_bridge

    githubbot, usecases = _githubbot_fixture(tmp_path, {}, "")
    (usecases.parent / "USECASES.md").mkdir()  # export target cannot be written

    result = githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)

    assert result["status"] == "error"
    assert "nothing changed" in result["message"]
    assert sorted(p.name for p in usecases.parent.iterdir()) == ["USECASES.md", "usecases.json"]


def test_failed_json_swap_restores_markdown_and_leaves_no_temp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import githubbot_bridge

    githubbot, usecases = _githubbot_fixture(tmp_path, {}, "")
    md = usecases.parent / "USECASES.md"
    md.write_text("old catalog\n", encoding="utf-8")
    before_json = usecases.read_bytes()
    real_replace = Path.replace

    def failing_replace(self: Path, target: Path) -> Path:
        if Path(target) == usecases:
            raise PermissionError("locked")
        return real_replace(self, target)

    monkeypatch.setattr(Path, "replace", failing_replace)
    result = githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)

    assert result["status"] == "error"
    assert usecases.read_bytes() == before_json
    assert md.read_text(encoding="utf-8") == "old catalog\n"
    assert sorted(p.name for p in usecases.parent.iterdir()) == ["USECASES.md", "usecases.json"]


def test_rebuild_registry_neutralises_stale_archives(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    size = outreach_engine.REGISTRY_MAX_ROWS
    history = [_history_entry(i) for i in range(size)]
    (workspace / "posts_history.json").write_text(json.dumps(history), encoding="utf-8")
    engine = CommunityOutreachEngine(workspace)
    engine.rebuild_registry()
    history[0]["publication_status"] = "unbestaetigt"
    (workspace / "posts_history.json").write_text(json.dumps(history), encoding="utf-8")

    engine.rebuild_registry()

    archive = (workspace / "_archive" / "POSTVERZEICHNIS_ARCHIV_v1.md").read_text(encoding="utf-8")
    active = (workspace / "POSTVERZEICHNIS.md").read_text(encoding="utf-8")
    assert "P-0000" not in archive
    published, unconfirmed = active.split("## Unbestätigt", 1)
    assert "P-0000" in unconfirmed and "P-0000" not in published
    assert "veraltet" in archive and "POSTVERZEICHNIS.md" in archive


def test_existing_catalog_entries_are_classified_fail_closed(tmp_path: Path) -> None:
    import githubbot_bridge

    registry = {
        "Org/Secret": {"github": {"visibility": "private", "fork": False, "archived": False}},
        "Org/Public": {"github": {"visibility": "public", "fork": False, "archived": False}},
    }
    githubbot, usecases = _githubbot_fixture(tmp_path, registry, "")
    usecases.write_text(
        json.dumps({"repositories": [
            {"id": "org/secret", "org": "org", "name": "secret", "active": True},
            {"id": "org/unregistered", "org": "org", "name": "unregistered", "active": True},
            {"id": "org/public", "org": "org", "name": "public", "active": True},
        ]}),
        encoding="utf-8",
    )

    githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot, import_missing_public=False)

    data = {r["id"]: r for r in json.loads(usecases.read_text(encoding="utf-8"))["repositories"]}
    assert data["org/secret"]["active"] is False and data["org/secret"]["exclusion_reason"] == "private"
    assert data["org/unregistered"]["active"] is False
    assert data["org/public"]["active"] is True
    assert "secret" not in (usecases.parent / "USECASES.md").read_text(encoding="utf-8").casefold()


def test_usecases_markdown_escapes_foreign_metadata_and_hides_excluded_ids(tmp_path: Path) -> None:
    import githubbot_bridge

    output = tmp_path / "USECASES.md"
    githubbot_bridge.export_usecases_markdown(
        {
            "repositories": [
                {
                    "id": "org/tool",
                    "org": "org",
                    "name": "tool<img src=x onerror=alert(1)>",
                    "url": "javascript:alert(1)",
                    "summary": "<script>alert(1)</script> | [x](javascript:alert(2))",
                    "problems_solved": ["<b>p</b>"],
                    "active": True,
                },
                {"id": "org/secret-internal", "org": "org", "active": False, "exclusion_reason": "private"},
            ]
        },
        output,
    )

    text = output.read_text(encoding="utf-8")
    assert "<img" not in text and "<script" not in text and "<b>" not in text
    assert "javascript:" not in text
    assert "secret-internal" not in text
    assert "https://github.com/org/tool" in text


def _history_entry(index: int, *, verified: bool = True, **extra: object) -> dict:
    record = {
        "post_id": f"P-{index:04d}",
        "date": "2026-09-01",
        "platform": "Reddit",
        "target_url": f"https://www.reddit.com/r/test/comments/t{index}/thread/",
        "published_url": f"https://www.reddit.com/r/test/comments/t{index}/thread/c{index}/",
        "platform_post_id": f"t1_c{index}",
        "repo": "org/tool",
        "status": "published",
        "receipt_verified": verified,
    }
    record.update(extra)
    return record


@pytest.mark.parametrize(
    ("record", "expected"),
    [
        (_history_entry(1), "veroeffentlicht"),
        (_history_entry(2, verified=False), "unbestaetigt"),
        (_history_entry(3, publication_status="unbestaetigt"), "unbestaetigt"),
        (_history_entry(4, verified=False, publication_status="veroeffentlicht"), "unbestaetigt"),
        ({"post_id": "legacy", "status": "published"}, "unbestaetigt"),
    ],
)
def test_every_history_record_has_exactly_one_publication_status(record: dict, expected: str) -> None:
    assert outreach_engine.publication_status(record) == expected
    assert expected in outreach_engine.PUBLICATION_STATUSES


def test_registry_is_split_by_cut_and_clue_with_bidirectional_pointers(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    size = outreach_engine.REGISTRY_MAX_ROWS
    history = [_history_entry(i) for i in range(2 * size + 5)] + [_history_entry(9999, verified=False)]
    (workspace / "posts_history.json").write_text(json.dumps(history), encoding="utf-8")
    (workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-Q-1", approved=False, target_url="https://example.com/a")
        + proposal_block("OUTBOUND-PROPOSAL-Q-2", approved=True, target_url="https://example.com/b"),
        encoding="utf-8",
    )
    engine = CommunityOutreachEngine(workspace)

    first = engine.rebuild_registry()
    second = engine.rebuild_registry()

    v1 = (workspace / "_archive" / "POSTVERZEICHNIS_ARCHIV_v1.md").read_text(encoding="utf-8")
    v2 = (workspace / "_archive" / "POSTVERZEICHNIS_ARCHIV_v2.md").read_text(encoding="utf-8")
    active = (workspace / "POSTVERZEICHNIS.md").read_text(encoding="utf-8")
    assert "P-0000" in v1 and f"P-{size:04d}" in v2 and f"P-{2 * size + 4:04d}" in active
    assert "POSTVERZEICHNIS_ARCHIV_v2.md" in v1 and "POSTVERZEICHNIS_ARCHIV_v1.md" in v2
    assert "POSTVERZEICHNIS.md" in v2 and "_archive/POSTVERZEICHNIS_ARCHIV_v2.md" in active
    assert "P-0000" not in active
    published, unconfirmed = active.split("## Unbestätigt", 1)
    assert "P-9999" in unconfirmed and "P-9999" not in published
    assert "freigegeben 1 · entwurf 1" in active
    assert len(active.splitlines()) < 200
    assert first["status"] == "completed" and second["written"] == []


def test_registry_neutralises_foreign_cells_and_links(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    record = _history_entry(1, post_id="<script>x</script>|", published_url="javascript:alert(1)")
    (workspace / "posts_history.json").write_text(json.dumps([record]), encoding="utf-8")

    CommunityOutreachEngine(workspace).rebuild_registry()

    text = (workspace / "POSTVERZEICHNIS.md").read_text(encoding="utf-8")
    assert "<script>" not in text and "](javascript:" not in text


def test_rebuild_registry_dry_run_is_pure(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / "posts_history.json").write_text(json.dumps([_history_entry(1)]), encoding="utf-8")
    before = snapshot_tree(workspace)

    result = CommunityOutreachEngine(workspace, dry_run=True).rebuild_registry()

    assert result["status"] == "dry-run"
    assert snapshot_tree(workspace) == before


def test_cli_sync_error_exits_nonzero_and_changes_nothing(tmp_path: Path) -> None:
    githubbot, usecases = _githubbot_fixture(tmp_path, {}, "")
    (usecases.parent / "USECASES.md").mkdir()
    before = usecases.read_bytes()

    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "outreach_engine.py"), "--workspace", str(usecases.parent), "--sync-githubbot"],
        capture_output=True, text=True, encoding="utf-8", check=False,
        env={**__import__("os").environ, "GITHUBBOT_DIR": str(githubbot), "PYTHONDONTWRITEBYTECODE": "1"},
    )

    assert completed.returncode == 1
    assert json.loads(completed.stdout)["status"] == "error"
    assert usecases.read_bytes() == before


def test_catalog_without_visibility_evidence_selects_nothing(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    repo = {"id": "private-org/private-only", "name": "private-only", "url": "https://github.com/private-org/private-only"}
    (workspace / "usecases.json").write_text(json.dumps({"repositories": [repo]}), encoding="utf-8")

    result = CommunityOutreachEngine(workspace).phase3_research_and_stage()

    assert result is not None and result.get("repo_name") is None
    assert result["reason"].startswith("visibility-unverified")
