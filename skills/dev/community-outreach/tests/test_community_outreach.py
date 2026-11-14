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
    (githubbot / "config" / "repo_registry.json").write_text(
        json.dumps({"repos": {"org/tool": {"github": PUBLIC_META}}}), encoding="utf-8")
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


ANCHOR_TRAFFIC = "**lukisch/impressum**\n  Views (14d): 1 gesamt / 1 unique\n  Clones (14d): 1 gesamt / 1 unique\n\n"


def _githubbot_fixture(tmp_path: Path, registry: dict, traffic: str) -> tuple[Path, Path]:
    # a blocked meta repo keeps both sources non-empty without entering the catalog
    registry = {"lukisch/impressum": {"github": {"visibility": "public", "fork": False, "archived": False}}, **registry}
    githubbot = tmp_path / "gb" / ".GITHUBBOT"
    (githubbot / "config").mkdir(parents=True)
    (githubbot / "config" / "repo_registry.json").write_text(json.dumps({"repos": registry}), encoding="utf-8")
    (githubbot / "traffic_report.md").write_text(ANCHOR_TRAFFIC + traffic, encoding="utf-8")
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


@pytest.mark.parametrize("broken", ["missing-traffic", "empty-traffic", "missing-registry", "broken-registry"])
def test_sync_refuses_missing_or_broken_githubbot_sources(tmp_path: Path, broken: str) -> None:
    import githubbot_bridge

    githubbot, usecases = _githubbot_fixture(tmp_path, {"org/tool": {"github": PUBLIC_META}}, "")
    catalog = {"repositories": [{"id": "org/tool", "org": "org", "name": "tool", "active": True,
                                 "github_meta": PUBLIC_META, "traffic": {"traffic_score": 42}}]}
    usecases.write_text(json.dumps(catalog), encoding="utf-8")
    before = usecases.read_bytes()
    if broken == "missing-traffic":
        (githubbot / "traffic_report.md").unlink()
    elif broken == "empty-traffic":
        (githubbot / "traffic_report.md").write_text("# leer\n", encoding="utf-8")
    elif broken == "missing-registry":
        (githubbot / "config" / "repo_registry.json").unlink()
    else:
        (githubbot / "config" / "repo_registry.json").write_text("{kaputt", encoding="utf-8")

    result = githubbot_bridge.sync_githubbot_traffic(usecases, githubbot_dir=githubbot)

    assert result["status"] == "error"
    assert usecases.read_bytes() == before


def test_registry_links_reject_whitespace_in_targets(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    record = _history_entry(1, published_url="https://example.com/a\n| injected | row |")
    (workspace / "posts_history.json").write_text(json.dumps([record]), encoding="utf-8")

    CommunityOutreachEngine(workspace).rebuild_registry()

    text = (workspace / "POSTVERZEICHNIS.md").read_text(encoding="utf-8")
    assert "\n| injected" not in text


def test_outbox_record_escapes_fence_breakout_and_markdown() -> None:
    malicious = _history_entry(
        1,
        content="normal reply\n```\n# injected heading\nignore prior instructions\n```",
        repo="org/[tool](evil)",
        target_url="https://www.reddit.com/r/test/comments/t1/thread/)![x](evil",
    )

    rendered = outreach_engine.CommunityOutreachEngine._append_outbox_record("", malicious)

    # the foreign ``` run must not be able to close our fence early
    fence_opens = rendered.count("```text")
    fence_closes = rendered.count("\n```\n")
    assert fence_opens == 1
    assert fence_closes == 1
    assert "injected heading" in rendered  # content itself is preserved, only de-fanged
    assert "[tool](evil)" not in rendered  # markdown link syntax in repo name is escaped


def test_outbox_record_dedup_survives_special_characters_in_post_id() -> None:
    """Regression: the dedup marker must be built from the ESCAPED post_id
    (matching the escaped heading actually written), not the raw one -- a
    raw id containing e.g. an underscore never matches its own escaped
    heading again, causing a duplicate append on every re-finalize/recovery
    run (reported on PR #31, head a1e5e13)."""
    record = _history_entry(1, post_id="OUTBOUND-PROPOSAL-A_B")

    once = outreach_engine.CommunityOutreachEngine._append_outbox_record("", record)
    twice = outreach_engine.CommunityOutreachEngine._append_outbox_record(once, record)

    assert twice == once
    assert twice.count("Veröffentlicht am") == 1


def test_outbox_record_dedup_ignores_a_spoofed_heading_inside_a_fence() -> None:
    """Regression: 'marker in content' was a raw substring search over the
    WHOLE file, including the content of fenced code blocks. A published
    text that itself quotes a heading line ("### [ZED] ...") would then
    suppress a later, genuinely new entry with the same post_id (reported on
    PR #31, head a1e5e13). The dedup check must only look at real H3
    headings outside fences."""
    quoting_record = _history_entry(1, post_id="AAA", content="Someone quoted:\n### [ZED] Veröffentlicht am irgendwann")
    outbox = outreach_engine.CommunityOutreachEngine._append_outbox_record("", quoting_record)
    assert "Veröffentlicht am irgendwann" in outbox  # the quote is preserved as content

    real_record = _history_entry(2, post_id="ZED", content="the real reply")
    outbox = outreach_engine.CommunityOutreachEngine._append_outbox_record(outbox, real_record)

    # Before the fix, the fenced quote's "### [ZED] ..." line made a bare
    # 'marker in content' substring check believe ZED was already present.
    assert "the real reply" in outbox


@pytest.mark.parametrize("args", [["--rebuild-registry"], ["--process-approvals"], ["--full-run"]])
def test_unreadable_history_is_an_error_and_nothing_is_overwritten(temp_workspace: Path, args: list[str]) -> None:
    (temp_workspace / "posts_history.json").write_text("{kaputt", encoding="utf-8")
    (temp_workspace / "POSTVERZEICHNIS.md").write_text("# bestehendes Verzeichnis\n", encoding="utf-8")
    (temp_workspace / "_archive").mkdir(exist_ok=True)
    (temp_workspace / "_archive" / "POSTVERZEICHNIS_ARCHIV_v1.md").write_text("# Archiv\n", encoding="utf-8")
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-H-1", approved=True, target_url="https://example.com/t"),
        encoding="utf-8",
    )
    before = snapshot_tree(temp_workspace)

    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "outreach_engine.py"), "--workspace", str(temp_workspace), *args],
        capture_output=True, text=True, encoding="utf-8", check=False,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert json.loads(completed.stdout)["status"] == "error"
    assert snapshot_tree(temp_workspace) == before


# --- Produktzuschnitt je App: Stufe 1 (eigener Bereich) -> Stufe 2 (Pool) -> Stufe 3
# (neuer Vorschlag), T-20260926-665406367 -------------------------------------------

def test_phase3_stage1_picks_only_from_org_allow(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repos = [
        {"id": "own-org/tool", "name": "tool", "org": "own-org",
         "url": "https://github.com/own-org/tool", "github_meta": PUBLIC_META},
        {"id": "other-org/tool2", "name": "tool2", "org": "other-org",
         "url": "https://github.com/other-org/tool2", "github_meta": PUBLIC_META,
         "traffic": {"traffic_score": 999}},
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")

    result = CommunityOutreachEngine(workspace, org_allow=["own-org"]).phase3_research_and_stage()

    # other-org/tool2 has the far higher traffic_score but is outside org_allow -> ignored in stage 1
    assert result["repo_name"] == "tool", result
    assert result["stage"] == 1
    assert result["fallback_used"] is False


def test_phase3_stage2_falls_back_to_whole_pool_when_own_org_is_empty(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repos = [
        {"id": "other-org/tool", "name": "tool", "org": "other-org",
         "url": "https://github.com/other-org/tool", "github_meta": PUBLIC_META},
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")

    # own-org has zero repos at all -> stage 1 empty -> stage 2 must pick from the whole pool
    result = CommunityOutreachEngine(workspace, org_allow=["own-org"]).phase3_research_and_stage()

    assert result["repo_name"] == "tool", result
    assert result["stage"] == 2
    assert result["fallback_used"] is True


def test_phase3_stage3_proposes_new_angle_when_pool_is_exhausted(tmp_path: Path) -> None:
    from datetime import datetime, timedelta, timezone

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    repos = [
        {"id": "own-org/tool", "name": "tool", "org": "own-org",
         "url": "https://github.com/own-org/tool", "last_promoted_at": recent,
         "total_promotions": 3, "github_meta": PUBLIC_META},
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")

    # The only repo everywhere is in cooldown -> stage 1 and stage 2 both empty -> stage 3
    result = CommunityOutreachEngine(workspace, org_allow=["own-org"]).phase3_research_and_stage()

    assert result["action"] == "propose-new-item", result
    assert result["stage"] == 3
    assert result["fallback_used"] is True
    assert result["candidates_for_new_angle"][0]["repo_name"] == "tool"


def test_phase3_org_allow_defaults_from_constructor(tmp_path: Path) -> None:
    """--org-allow via CLI / Konstruktor gilt auch ohne expliziten Aufrufparameter."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repos = [
        {"id": "own-org/tool", "name": "tool", "org": "own-org",
         "url": "https://github.com/own-org/tool", "github_meta": PUBLIC_META},
        {"id": "other-org/tool2", "name": "tool2", "org": "other-org",
         "url": "https://github.com/other-org/tool2", "github_meta": PUBLIC_META,
         "traffic": {"traffic_score": 999}},
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")

    engine = CommunityOutreachEngine(workspace, org_allow=["own-org"])
    result = engine.phase3_research_and_stage()  # kein expliziter org_allow-Parameter

    assert result["repo_name"] == "tool", result
    assert result["stage"] == 1


# --- Posting je App: injizierbarer Datei-Receipt-Publisher, T-20260926-665406367 -----
# Der eigentliche Post (open-compute/Playwright/Claude-in-Chrome/API) geschieht in der
# Session der aufrufenden App VOR diesem Aufruf; dieser Publisher fuehrt selbst keine
# Netzwerk-/Browseraktion aus, er reicht nur das schon eingesammelte Ergebnis weiter.

def test_file_receipt_publisher_applies_a_matching_receipt(temp_workspace: Path, tmp_path: Path) -> None:
    from outreach_engine import FileReceiptPublisher

    target = "https://example.com/thread"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target),
        encoding="utf-8",
    )
    receipt_file = tmp_path / "receipt.json"
    receipt_file.write_text(json.dumps({
        "proposal_id": "OUTBOUND-PROPOSAL-P-1",
        **verified_receipt("t1_abc123", target),
    }), encoding="utf-8")

    publisher = FileReceiptPublisher(receipt_file, "OUTBOUND-PROPOSAL-P-1")
    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert results == [{"id": "OUTBOUND-PROPOSAL-P-1", "status": "published", "receipt": "t1_abc123"}], results


def test_file_receipt_publisher_refuses_a_receipt_for_a_different_proposal(
    temp_workspace: Path, tmp_path: Path
) -> None:
    """A receipt file bound to the wrong proposal id must never be applied to this one."""
    from outreach_engine import FileReceiptPublisher

    target = "https://example.com/thread"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target),
        encoding="utf-8",
    )
    receipt_file = tmp_path / "receipt.json"
    receipt_file.write_text(json.dumps({
        "proposal_id": "OUTBOUND-PROPOSAL-SOME-OTHER-POST",
        **verified_receipt("t1_abc123", target),
    }), encoding="utf-8")

    publisher = FileReceiptPublisher(receipt_file, "OUTBOUND-PROPOSAL-P-1")
    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert len(results) == 1
    assert results[0]["id"] == "OUTBOUND-PROPOSAL-P-1"
    assert results[0]["status"] == "needs-action"
    assert "publisher-error" in results[0]["reason"]


def test_bound_publisher_does_not_consume_cycle_limit_on_unbound_proposals(
    temp_workspace: Path, tmp_path: Path
) -> None:
    """merge-reviewer finding: an unbound proposal must not count against max_posts_per_cycle.

    Two approved proposals, the bound one SECOND. With max_posts_per_cycle=1 (the default),
    the old code counted an attempt for P-1 (the unbound one) before publish() even ran and
    raised -- so P-2, the one with the real receipt, hit "deferred: cycle-limit" and its
    already-real evidence was lost. Must be red without the fix.
    """
    from outreach_engine import FileReceiptPublisher

    target_1 = "https://example.com/thread-1"
    target_2 = "https://example.com/thread-2"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n"
        + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target_1)
        + proposal_block("OUTBOUND-PROPOSAL-P-2", approved=True, target_url=target_2),
        encoding="utf-8",
    )
    receipt_file = tmp_path / "receipt.json"
    receipt_file.write_text(json.dumps({
        "proposal_id": "OUTBOUND-PROPOSAL-P-2",
        **verified_receipt("t1_abc123", target_2),
    }), encoding="utf-8")

    publisher = FileReceiptPublisher(receipt_file, "OUTBOUND-PROPOSAL-P-2")
    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    by_id = {r["id"]: r for r in results}
    assert by_id["OUTBOUND-PROPOSAL-P-1"]["status"] == "needs-action", by_id
    assert by_id["OUTBOUND-PROPOSAL-P-1"]["reason"] == "publisher-unbound"
    assert by_id["OUTBOUND-PROPOSAL-P-2"]["status"] == "published", by_id
    assert by_id["OUTBOUND-PROPOSAL-P-2"]["receipt"] == "t1_abc123"


def test_file_receipt_publisher_missing_file_fails_closed(temp_workspace: Path, tmp_path: Path) -> None:
    from outreach_engine import FileReceiptPublisher

    target = "https://example.com/thread"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target),
        encoding="utf-8",
    )
    publisher = FileReceiptPublisher(tmp_path / "does-not-exist.json", "OUTBOUND-PROPOSAL-P-1")
    results = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()

    assert results[0]["status"] == "needs-action"
    assert "publisher-error" in results[0]["reason"]


def test_cli_receipt_flags_must_be_given_together(temp_workspace: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "outreach_engine.py"), "--workspace", str(temp_workspace),
         "--process-approvals", "--receipt-file", "somewhere.json", "--json"],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert json.loads(completed.stdout)["status"] == "error"


def test_cli_process_approvals_with_receipt_file_publishes(temp_workspace: Path, tmp_path: Path) -> None:
    target = "https://example.com/thread"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target),
        encoding="utf-8",
    )
    receipt_file = tmp_path / "receipt.json"
    receipt_file.write_text(json.dumps({
        "proposal_id": "OUTBOUND-PROPOSAL-P-1",
        **verified_receipt("t1_abc123", target),
    }), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "outreach_engine.py"), "--workspace", str(temp_workspace),
         "--process-approvals", "--receipt-file", str(receipt_file),
         "--receipt-proposal-id", "OUTBOUND-PROPOSAL-P-1", "--json"],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    result = json.loads(completed.stdout)
    assert result["outbound_results"] == [{"id": "OUTBOUND-PROPOSAL-P-1", "status": "published", "receipt": "t1_abc123"}]


# --- Sicherheitsfund merge-reviewer (T-20260926-665406367): Stufe 3 umging das
# Sichtbarkeits-Gate von select_candidate_repository und konnte private, archivierte,
# geforkte oder nie synchronisierte Repos vorschlagen -- am gefaehrlichsten genau dann,
# wenn der Grund "visibility-unverified" war (ein fehlender Sync durfte das nie umgehen).

def test_stage3_never_proposes_private_or_unsynced_repos(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    repos = [
        {"id": "own-org/private-tool", "name": "private-tool", "org": "own-org",
         "url": "https://github.com/own-org/private-tool", "total_promotions": 9,
         "github_meta": {"visibility": "private", "archived": False, "fork": False}},
        {"id": "own-org/never-synced", "name": "never-synced", "org": "own-org",
         "url": "https://github.com/own-org/never-synced", "total_promotions": 9},
        # kein github_meta -> nie synchronisiert
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")

    result = CommunityOutreachEngine(workspace, org_allow=["own-org"]).phase3_research_and_stage()

    # Ohne Fix: action == "propose-new-item" mit genau diesen beiden Repos in
    # candidates_for_new_angle -- das ist der Sicherheitsfund. Mit Fix: Stufe 3 feuert bei
    # unverified_visibility gar nicht, es bleibt bei der alten "run --sync-githubbot"-Meldung.
    assert result["action"] == "configure-repositories", result
    assert result["reason"] == "visibility-unverified: run --sync-githubbot"
    assert "candidates_for_new_angle" not in result


def test_stage3_filters_archived_and_forked_repos_even_when_pool_is_otherwise_exhausted(
    tmp_path: Path,
) -> None:
    """Second _public_repo_gate condition (archived/fork), separate from visibility."""
    from datetime import datetime, timedelta, timezone

    workspace = tmp_path / "workspace"
    workspace.mkdir()
    recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    repos = [
        # Public, but archived -- must never be a stage-3 candidate either.
        {"id": "own-org/archived-tool", "name": "archived-tool", "org": "own-org",
         "url": "https://github.com/own-org/archived-tool", "total_promotions": 9,
         "github_meta": {"visibility": "public", "archived": True, "fork": False}},
        # Public, not archived, in cooldown -- the one legitimate stage-3 candidate.
        {"id": "own-org/cooling-tool", "name": "cooling-tool", "org": "own-org",
         "url": "https://github.com/own-org/cooling-tool", "total_promotions": 3,
         "last_promoted_at": recent, "github_meta": PUBLIC_META},
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")

    result = CommunityOutreachEngine(workspace, org_allow=["own-org"]).phase3_research_and_stage()

    assert result["action"] == "propose-new-item", result
    names = [c["repo_name"] for c in result["candidates_for_new_angle"]]
    assert names == ["cooling-tool"], names


# --- Posting je App: read-only Vorschau vor dem eigentlichen Post, T-20260926-665406367 ---
# preview_post() ruehrt keinen Zustand an; sie liefert nur, was ein Browser-Automations-Schritt
# (open-compute/Playwright/Claude-in-Chrome/API) komponieren wuerde, damit eine App das per
# Screenshot zeigen und VOR dem Absenden abbrechen kann.

def test_preview_post_renders_an_approved_proposal_read_only(temp_workspace: Path) -> None:
    target = "https://example.com/thread"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target),
        encoding="utf-8",
    )
    before = snapshot_tree(temp_workspace)

    result = CommunityOutreachEngine(temp_workspace).preview_post("OUTBOUND-PROPOSAL-P-1")

    assert result["status"] == "preview", result
    assert result["target_url"] == target
    assert result["platform"] == "Reddit"
    assert "Eine konkrete, hilfreiche Antwort." in result["text"]
    assert snapshot_tree(temp_workspace) == before  # touched nothing


def test_preview_post_refuses_an_unapproved_proposal(temp_workspace: Path) -> None:
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-2", approved=False, target_url="https://example.com/t"),
        encoding="utf-8",
    )

    result = CommunityOutreachEngine(temp_workspace).preview_post("OUTBOUND-PROPOSAL-P-2")

    assert result["status"] == "error"
    assert "not approved" in result["message"]


def test_preview_post_unknown_id_is_an_error(temp_workspace: Path) -> None:
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-3", approved=True, target_url="https://example.com/t"),
        encoding="utf-8",
    )

    result = CommunityOutreachEngine(temp_workspace).preview_post("OUTBOUND-PROPOSAL-DOES-NOT-EXIST")

    assert result["status"] == "error"
    assert "not found" in result["message"]


def test_cli_preview_post_exits_nonzero_on_error(temp_workspace: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "outreach_engine.py"), "--workspace", str(temp_workspace),
         "--preview-post", "OUTBOUND-PROPOSAL-DOES-NOT-EXIST", "--json"],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert json.loads(completed.stdout)["status"] == "error"


def test_cli_preview_post_of_approved_proposal(temp_workspace: Path) -> None:
    target = "https://example.com/thread"
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n" + proposal_block("OUTBOUND-PROPOSAL-P-1", approved=True, target_url=target),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "outreach_engine.py"), "--workspace", str(temp_workspace),
         "--preview-post", "OUTBOUND-PROPOSAL-P-1", "--json"],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    result = json.loads(completed.stdout)
    assert result["status"] == "preview"
    assert result["target_url"] == target


def test_verify_proposals_checks_real_files_and_blacklist(temp_workspace: Path, tmp_path: Path) -> None:
    repos_root = tmp_path / "repos"
    (repos_root / "super-tool" / "src").mkdir(parents=True)
    (repos_root / "super-tool" / "src" / "engine.py").write_text("class Engine: pass\n", encoding="utf-8")

    (temp_workspace / "config.json").write_text(
        json.dumps({"compliance": {"require_code_evidence": True}}),
        encoding="utf-8",
    )
    (temp_workspace / "rejected_proposals.json").write_text(
        json.dumps(
            {
                "platform_exclusions": [{"platform": "Dev.to"}],
                "rejected_proposals": [
                    {
                        "proposal_id": "OUTBOUND-PROPOSAL-REJECTED-1",
                        "canonical_url": "https://reddit.com/r/python/comments/rejected1/thread",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    inbox = """# Queue

### [OUTBOUND-PROPOSAL-VERIFIED-1] Verified
- **Plattform:** Reddit
- **Ziel-URL / Thread:** [https://www.reddit.com/r/python/comments/ok1/thread/](https://www.reddit.com/r/python/comments/ok1/thread/)
- **Lösungs-Repo:** `my-org/super-tool`
- **Code-Beleg (Verifiziert):** `src/engine.py` (`Engine`)
- [x] Genehmigt

#### Textvorschlag:
```markdown
Geprüfter Beitrag.
```

### [OUTBOUND-PROPOSAL-MISSING-FILE-1] Missing File
- **Plattform:** Reddit
- **Ziel-URL / Thread:** [https://www.reddit.com/r/python/comments/ok2/thread/](https://www.reddit.com/r/python/comments/ok2/thread/)
- **Lösungs-Repo:** `my-org/super-tool`
- **Code-Beleg (Verifiziert):** `src/nonexistent.py`
- [x] Genehmigt

#### Textvorschlag:
```markdown
Halluzinierte Datei.
```
"""
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    engine = CommunityOutreachEngine(temp_workspace)
    report = engine.verify_proposals(repos_root=repos_root)
    assert report["status"] == "failed"
    assert report["verified_count"] == 1
    assert report["failed_count"] == 1
    assert report["results"][0]["status"] == "verified"
    assert report["results"][1]["status"] == "failed"
    assert report["results"][1]["missing_files"] == ["src/nonexistent.py"]


def test_verify_proposals_and_phase2_reject_ai_essay_style(temp_workspace: Path, tmp_path: Path) -> None:
    repos_root = tmp_path / "repos"
    (repos_root / "super-tool" / "src").mkdir(parents=True)
    (repos_root / "super-tool" / "src" / "engine.py").write_text("class Engine: pass\n", encoding="utf-8")

    (temp_workspace / "config.json").write_text(
        json.dumps({"compliance": {"require_code_evidence": True, "require_natural_style": True}}),
        encoding="utf-8",
    )

    inbox = """# Queue

### [OUTBOUND-PROPOSAL-AI-ESSAY-1] AI Essay Style
- **Plattform:** Reddit
- **Ziel-URL / Thread:** [https://www.reddit.com/r/softwarearchitecture/comments/1s6lc2e/thread/](https://www.reddit.com/r/softwarearchitecture/comments/1s6lc2e/thread/)
- **Lösungs-Repo:** `my-org/super-tool`
- **Code-Beleg (Verifiziert):** `src/engine.py`
- **Umgebungs-Check (Ton & Länge):** Umgebungs-Kommentare sind 2-4 kurze Sätze ohne Überschriften.
- [x] Genehmigt

#### Textvorschlag:
```markdown
Here are three practical patterns that solve this problem — and why they matter:

### 1. Deterministic Schema
- **Full Snapshot:** Always export a **deterministic** snapshot.
- **Delta Bundle:** Sign every bundle.
- **Idempotent Apply:** Never overwrite newer rows.

Treating sync as a transit problem gives you a resilient architecture.
```
"""
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    engine = CommunityOutreachEngine(temp_workspace)
    report = engine.verify_proposals(repos_root=repos_root)
    assert report["status"] == "failed"
    item = report["results"][0]
    assert item["natural_style_ok"] is False
    assert "markdown-headings-forbidden" in item["style_violations"]
    assert "bold-markup-forbidden" in item["style_violations"]
    assert "em-dash-forbidden" in item["style_violations"]
    assert "structured-list-essay-forbidden" in item["style_violations"]
    assert "ai-cliche-phrasing" in item["style_violations"]
    assert item["has_context_check"] is True

    outbound = engine.phase2_outbound_execution()
    assert outbound == [
        {
            "id": "OUTBOUND-PROPOSAL-AI-ESSAY-1",
            "status": "needs-action",
            "reason": "ai-style-violation",
            "violations": item["style_violations"],
        }
    ]
    preview = engine.preview_post("OUTBOUND-PROPOSAL-AI-ESSAY-1")
    assert preview["status"] == "error"
    assert "violates natural human style" in preview["message"]


def test_biotec_line_is_permanently_excluded_across_selection_verification_preview_and_outbound(
    temp_workspace: Path,
) -> None:
    repos = [
        {
            "id": "biotec-line/VFDistiller",
            "name": "VFDistiller",
            "org": "biotec-line",
            "url": "https://github.com/biotec-line/VFDistiller",
            "github_meta": PUBLIC_META,
            "traffic": {"traffic_score": 9999},
        },
        {
            "id": "ellmos-ai/agent-orchestrator",
            "name": "agent-orchestrator",
            "org": "ellmos-ai",
            "url": "https://github.com/ellmos-ai/agent-orchestrator",
            "github_meta": PUBLIC_META,
            "traffic": {"traffic_score": 50},
        },
    ]
    (temp_workspace / "usecases.json").write_text(
        json.dumps({"repositories": repos}), encoding="utf-8"
    )
    (temp_workspace / "POST-EINGANG.md").write_text(
        "# Queue\n\n"
        + proposal_block(
            "OUTBOUND-PROPOSAL-BIOTEC-1",
            approved=True,
            target_url="https://www.reddit.com/r/bioinformatics/comments/1abc/thread/",
            repo="biotec-line/VFDistiller",
        ),
        encoding="utf-8",
    )

    engine = CommunityOutreachEngine(temp_workspace)

    # 1. Phase 3 never selects biotec-line even if it has highest traffic or org_allow requests it
    staged = engine.phase3_research_and_stage()
    assert staged["repo_name"] == "agent-orchestrator"
    staged_forced = engine.phase3_research_and_stage(org_allow=["biotec-line"])
    assert staged_forced["repo_name"] != "VFDistiller"

    # 2. verify_proposals marks biotec-line proposals as failed & blacklisted (excluded_org)
    report = engine.verify_proposals()
    assert report["status"] == "failed"
    assert report["results"][0]["blacklisted"] is True
    assert report["results"][0]["excluded_org"] is True

    # 3. preview_post refuses biotec-line proposals
    preview = engine.preview_post("OUTBOUND-PROPOSAL-BIOTEC-1")
    assert preview["status"] == "error"
    assert "blacklisted" in preview["message"]

    # 4. phase2_outbound_execution blocks biotec-line proposals as blacklisted without calling publisher
    publisher = DynamicPublisher()
    outbound = CommunityOutreachEngine(temp_workspace, publisher=publisher).phase2_outbound_execution()
    assert outbound == [
        {"id": "OUTBOUND-PROPOSAL-BIOTEC-1", "status": "blacklisted"}
    ]
    assert publisher.calls == []


def test_primary_orgs_focus_and_research_line_discourse_mode(tmp_path: Path) -> None:
    workspace = tmp_path / "org_policy_ws"
    workspace.mkdir()
    repos = [
        {
            "id": "research-line/functional-stability-theory",
            "name": "functional-stability-theory",
            "org": "research-line",
            "url": "https://github.com/research-line/functional-stability-theory",
            "outreach_mode": "discourse_positioning",
            "github_meta": PUBLIC_META,
            "traffic": {"traffic_score": 5000},
        },
        {
            "id": "um-bruch/web",
            "name": "web",
            "org": "um-bruch",
            "url": "https://github.com/um-bruch/web",
            "github_meta": PUBLIC_META,
            "traffic": {"traffic_score": 2000},
        },
        {
            "id": "dev-bricks/api-probe",
            "name": "api-probe",
            "org": "dev-bricks",
            "url": "https://github.com/dev-bricks/api-probe",
            "github_meta": PUBLIC_META,
            "traffic": {"traffic_score": 100},
        },
    ]
    (workspace / "usecases.json").write_text(json.dumps({"repositories": repos}), encoding="utf-8")
    (workspace / "config.json").write_text(
        json.dumps(
            {
                "compliance": {
                    "primary_orgs": ["ellmos-ai", "dev-bricks", "file-bricks", "doc-bricks", "open-bricks"],
                    "excluded_orgs": ["biotec-line"],
                    "discourse_only_orgs": ["research-line"],
                }
            }
        ),
        encoding="utf-8",
    )

    engine = CommunityOutreachEngine(workspace)

    # Default routine run selects from primary_orgs (dev-bricks/api-probe) and skips research-line
    routine = engine.phase3_research_and_stage()
    assert routine["repo_name"] == "api-probe"
    assert routine["stage"] == 1
    assert routine["outreach_mode"] == "solution-outreach"

    # Explicit discourse run with org_allow=["research-line"] selects research-line in discourse-positioning mode
    discourse = engine.phase3_research_and_stage(org_allow=["research-line"])
    assert discourse["repo_name"] == "functional-stability-theory"
    assert discourse["outreach_mode"] == "discourse-positioning"
    assert "wissenschaftliche Stellungnahme" in discourse["reason"]


def test_three_stage_quality_and_attention_selection_model(tmp_path: Path) -> None:
    import githubbot_bridge
    from outreach_engine import select_candidate_repository

    # 1. classify_repo activates ellmos-ai/skills ("skills allgemein")
    reg = {"ellmos-ai/skills": {"github": {"visibility": "public", "fork": False, "archived": False}}}
    cls_skills = githubbot_bridge.classify_repo(
        repo_id="ellmos-ai/skills",
        org="ellmos-ai",
        name="skills",
        registry_repos=reg,
        private_set=set(),
        archived_set=set(),
        all_catalog_repos=[],
    )
    assert cls_skills.is_active is True

    # 2. compute_selection_tier classifies Tier 1, Tier 2, and Tier 3 accurately
    t1_module = {
        "id": "ellmos-ai/workflowhooker",
        "total_promotions": 0,
        "traffic": {"views_unique_14d": 0, "clones_unique_14d": 54, "traffic_score": 108},
    }
    tier1, label1, q1 = githubbot_bridge.compute_selection_tier(t1_module)
    assert (tier1, label1, q1) == (1, "tier1_quality_low_medium_attention", 98)

    t1_flagship = {
        "id": "ellmos-ai/bach",
        "total_promotions": 1,
        "traffic": {"views_unique_14d": 28, "clones_unique_14d": 93, "traffic_score": 214},
    }
    assert githubbot_bridge.compute_selection_tier(t1_flagship) == (1, "tier1_core_flagship", 99)

    t1_skill = {
        "id": "skills/infrastructure/skill-extractor",
        "total_promotions": 0,
        "traffic": {},
    }
    assert githubbot_bridge.compute_selection_tier(t1_skill) == (1, "tier1_standout_skill", 95)

    t2_module = {
        "id": "file-bricks/ExplorerPro",
        "total_promotions": 0,
        "traffic": {"views_unique_14d": 15, "clones_unique_14d": 120, "traffic_score": 255},
    }
    assert githubbot_bridge.compute_selection_tier(t2_module) == (2, "tier2_quality_existing_attention", 92)

    t3_smaller = {
        "id": "ellmos-ai/source-resolver",
        "total_promotions": 0,
        "traffic": {"views_unique_14d": 0, "clones_unique_14d": 63, "traffic_score": 126},
    }
    assert githubbot_bridge.compute_selection_tier(t3_smaller) == (3, "tier3_smaller_modules", 60)

    # 3. select_candidate_repository strictly orders Tier 1 -> Tier 2 -> Tier 3
    candidates = [
        {
            "id": "ellmos-ai/source-resolver",
            "name": "source-resolver",
            "org": "ellmos-ai",
            "url": "https://github.com/ellmos-ai/source-resolver",
            "selection_tier": 3,
            "selection_tier_label": "tier3_smaller_modules",
            "quality_score": 60,
            "total_promotions": 0,
            "github_meta": PUBLIC_META,
            "traffic": {"views_unique_14d": 0, "clones_unique_14d": 500, "traffic_score": 1000},
        },
        {
            "id": "file-bricks/ExplorerPro",
            "name": "ExplorerPro",
            "org": "file-bricks",
            "url": "https://github.com/file-bricks/ExplorerPro",
            "selection_tier": 2,
            "selection_tier_label": "tier2_quality_existing_attention",
            "quality_score": 92,
            "total_promotions": 0,
            "github_meta": PUBLIC_META,
            "traffic": {"views_unique_14d": 15, "clones_unique_14d": 300, "traffic_score": 615},
        },
        {
            "id": "ellmos-ai/workflowhooker",
            "name": "workflowhooker",
            "org": "ellmos-ai",
            "url": "https://github.com/ellmos-ai/workflowhooker",
            "selection_tier": 1,
            "selection_tier_label": "tier1_quality_low_medium_attention",
            "quality_score": 98,
            "total_promotions": 0,
            "github_meta": PUBLIC_META,
            "traffic": {"views_unique_14d": 0, "clones_unique_14d": 54, "traffic_score": 108},
        },
    ]
    selected, meta = select_candidate_repository(candidates)
    assert selected is not None and selected["id"] == "ellmos-ai/workflowhooker"
    assert meta["selection_tier"] == 1
    assert meta["quality_score"] == 98

    # When Tier 1 is removed, Tier 2 beats Tier 3 even if Tier 3 has higher raw clone traffic
    selected2, meta2 = select_candidate_repository(candidates[:2])
    assert selected2 is not None and selected2["id"] == "file-bricks/ExplorerPro"
    assert meta2["selection_tier"] == 2


def test_verify_proposals_resolves_specific_skill_paths(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    workspace.mkdir()
    repos_root = tmp_path / "repos"
    skill_dir = repos_root / "skills" / "skills" / "infrastructure" / "skill-extractor"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: skill-extractor\n---\n", encoding="utf-8")

    (workspace / "POST-EINGANG.md").write_text(
        """# POST-EINGANG

### [OUTBOUND-PROPOSAL-SKILL-EXTRACTOR-1] Skill Extractor
- **Plattform:** Reddit
- **Ziel-URL:** https://www.reddit.com/r/ClaudeAI/comments/abc123/reusable_skills/
- **Lösungs-Repo:** skills/infrastructure/skill-extractor
- **Code-Beleg (Verifiziert):** `SKILL.md`
- **Umgebungs-Check (Ton & Länge):** Geprüft am 2026-11-09
- [x] Genehmigt
#### Textvorschlag:
```text
We handle session-to-skill distillation in ellmos-ai/skills under skills/infrastructure/skill-extractor by segmenting long transcripts into stations first and scoring each station before generating a SKILL.md package.
```
""",
        encoding="utf-8",
    )
    report = CommunityOutreachEngine(workspace).verify_proposals(repos_root=repos_root)
    assert report["status"] == "verified", report
    assert report["verified_count"] == 1
    assert report["failed_count"] == 0


def _init_git_repo(repo_dir: Path, files: dict[str, str]) -> None:
    repo_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, content in files.items():
        full_path = repo_dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
    subprocess.run(["git", "-C", str(repo_dir), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "add", "."], check=True)


def test_claim_contract_valid_zero_dep_and_sister_repo_publishes_and_cleans_span(
    temp_workspace: Path, tmp_path: Path
) -> None:
    repos_root = tmp_path / "repos"
    _init_git_repo(
        repos_root / "super-tool",
        {
            "pyproject.toml": '[project]\nname = "super-tool"\ndependencies = []\n',
            "src/lock_guard.py": (
                "class LockGuard:\n"
                "    def acquire_fenced_lease(self, fence: int) -> bool:\n"
                "        return fence > 0\n"
            ),
        },
    )
    _init_git_repo(
        repos_root / "clutch",
        {
            "clutch/router.py": (
                "class ModelRouter:\n"
                "    def select_gear(self, budget_ratio: float) -> str:\n"
                "        return 'eco' if budget_ratio < 0.2 else 'pro'\n"
            ),
        },
    )

    (temp_workspace / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "id": "ellmos-ai/super-tool",
                        "name": "super-tool",
                        "org": "ellmos-ai",
                        "url": "https://example.org/super-tool",
                        "github_meta": PUBLIC_META,
                    },
                    {
                        "id": "ellmos-ai/clutch",
                        "name": "clutch",
                        "org": "ellmos-ai",
                        "url": "https://github.com/ellmos-ai/clutch",
                        "github_meta": PUBLIC_META,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    (temp_workspace / "config.json").write_text(
        json.dumps(
            {
                "compliance": {
                    "require_code_evidence": True,
                    "require_natural_style": True,
                    "require_claim_contract": True,
                },
                "verification": {"local_repos_root": str(repos_root)},
            }
        ),
        encoding="utf-8",
    )

    contract = [
        {
            "text_anchor": "We built ellmos-ai/super-tool in Python with zero dependencies and monotonic fenced leases in lock_guard.py.",
            "repo": "ellmos-ai/super-tool",
            "file": "src/lock_guard.py",
            "lines": "L1-L3",
            "verbatim_code": "class LockGuard:\n    def acquire_fenced_lease(self, fence: int) -> bool:",
        },
        {
            "text_anchor": "with zero dependencies",
            "repo": "ellmos-ai/super-tool",
            "file": "pyproject.toml",
            "lines": "L1-L3",
            "verbatim_code": 'name = "super-tool"\ndependencies = []',
        },
        {
            "text_anchor": "When routing models alongside it, we pair it with Clutch for budget-aware gear selection in router.py.",
            "repo": "ellmos-ai/clutch",
            "file": "clutch/router.py",
            "lines": "L1-L3",
            "verbatim_code": "class ModelRouter:\n    def select_gear(self, budget_ratio: float) -> str:",
        },
    ]

    inbox = f"""# Queue

### [OUTBOUND-PROPOSAL-CONTRACT-OK-1] Verified Contract
- **Plattform:** Reddit
- **Ziel-URL / Thread:** [https://www.reddit.com/r/python/comments/okcontract/thread/](https://www.reddit.com/r/python/comments/okcontract/thread/)
- **Lösungs-Repo:** `ellmos-ai/super-tool`
- **Code-Beleg (Verifiziert):** `src/lock_guard.py`, `pyproject.toml`
- **Umgebungs-Check (Ton & Länge):** Kurzer Kommentar ohne Listen
#### Claim-Beleg-Vertrag (Verifiziert):
```json
{json.dumps(contract, indent=2)}
```
- [x] Genehmigt

#### Textvorschlag:
```text
Stale lock files after crashes bit us constantly too. We built ellmos-ai/super-tool in Python with zero dependencies and monotonic fenced leases in lock_guard.py. When routing models alongside it, we pair it with Clutch for budget-aware gear selection in router.py.
```
"""
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")

    engine = CommunityOutreachEngine(temp_workspace, publisher=DynamicPublisher())
    report = engine.verify_proposals()
    assert report["status"] == "verified", report
    item = report["results"][0]
    assert item["claim_contract_ok"] is True
    assert item["verified_claims"] == 3
    assert item["software_sentence_count"] == 2
    assert item["covered_sentence_count"] == 2

    preview = engine.preview_post("OUTBOUND-PROPOSAL-CONTRACT-OK-1")
    assert preview["status"] == "preview", preview

    outbound = engine.phase2_outbound_execution()
    assert len(outbound) == 1 and outbound[0]["status"] == "published", outbound
    remaining_inbox = (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8")
    assert "OUTBOUND-PROPOSAL-CONTRACT-OK-1" not in remaining_inbox
    assert "Claim-Beleg-Vertrag" not in remaining_inbox


def test_claim_contract_missing_blocks_verify_preview_and_outbound(
    temp_workspace: Path, tmp_path: Path
) -> None:
    repos_root = tmp_path / "repos"
    _init_git_repo(repos_root / "super-tool", {"src/engine.py": "class Engine:\n    pass\n"})
    (temp_workspace / "config.json").write_text(
        json.dumps(
            {
                "compliance": {"require_code_evidence": True, "require_claim_contract": True},
                "verification": {"local_repos_root": str(repos_root)},
            }
        ),
        encoding="utf-8",
    )
    inbox = """# Queue

### [OUTBOUND-PROPOSAL-NO-CONTRACT-1] Missing Contract
- **Plattform:** Reddit
- **Ziel-URL / Thread:** https://www.reddit.com/r/python/comments/nocontract/thread/
- **Lösungs-Repo:** `ellmos-ai/super-tool`
- **Code-Beleg (Verifiziert):** `src/engine.py`
- [x] Genehmigt

#### Textvorschlag:
```text
We built ellmos-ai/super-tool with a deterministic Engine class.
```
"""
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    publisher = DynamicPublisher()
    engine = CommunityOutreachEngine(temp_workspace, publisher=publisher)

    report = engine.verify_proposals()
    assert report["status"] == "failed"
    assert report["results"][0]["contract_violations"] == ["missing-claim-contract"]

    preview = engine.preview_post("OUTBOUND-PROPOSAL-NO-CONTRACT-1")
    assert preview["status"] == "error"
    assert "missing-claim-contract" in preview["contract_violations"]

    outbound = engine.phase2_outbound_execution()
    assert outbound == [
        {
            "id": "OUTBOUND-PROPOSAL-NO-CONTRACT-1",
            "status": "needs-action",
            "reason": "missing-claim-contract",
            "violations": ["missing-claim-contract"],
        }
    ]
    assert publisher.calls == []


def test_claim_contract_rejects_verbatim_mismatch_untracked_uncovered_and_false_predicates(
    temp_workspace: Path, tmp_path: Path
) -> None:
    repos_root = tmp_path / "repos"
    _init_git_repo(
        repos_root / "super-tool",
        {
            "pyproject.toml": '[project]\nname = "super-tool"\ndependencies = ["hook-master>=0.2.0"]\n',
            "src/engine.py": "class Engine:\n    def run_gate(self) -> bool:\n        return True\n",
        },
    )
    # Create an untracked file on disk that is NOT in git index
    (repos_root / "super-tool" / "src" / "untracked.py").write_text(
        "def secret_untracked_helper() -> int:\n    return 42\n", encoding="utf-8"
    )
    _init_git_repo(
        repos_root / "clutch",
        {"clutch/router.py": "class ModelRouter:\n    pass\n"},
    )

    (temp_workspace / "usecases.json").write_text(
        json.dumps(
            {
                "repositories": [
                    {"id": "ellmos-ai/super-tool", "name": "super-tool", "org": "ellmos-ai", "github_meta": PUBLIC_META},
                    {"id": "ellmos-ai/clutch", "name": "clutch", "org": "ellmos-ai", "github_meta": PUBLIC_META},
                ]
            }
        ),
        encoding="utf-8",
    )
    (temp_workspace / "config.json").write_text(
        json.dumps(
            {
                "compliance": {"require_code_evidence": True, "require_claim_contract": True},
                "verification": {"local_repos_root": str(repos_root)},
            }
        ),
        encoding="utf-8",
    )

    bad_contract = [
        {
            "text_anchor": "We built ellmos-ai/super-tool with zero runtime dependencies in engine.py.",
            "repo": "ellmos-ai/super-tool",
            "file": "src/engine.py",
            "lines": "L1-L3",
            "verbatim_code": "class Engine:\n    def run_gate(self) -> bool:",
        },
        {
            "text_anchor": "We built ellmos-ai/super-tool with zero runtime dependencies in engine.py.",
            "repo": "ellmos-ai/super-tool",
            "file": "src/engine.py",
            "lines": "L1-L3",
            "verbatim_code": "def hallucinated_method_that_does_not_exist():",
        },
        {
            "text_anchor": "We built ellmos-ai/super-tool with zero runtime dependencies in engine.py.",
            "repo": "ellmos-ai/super-tool",
            "file": "src/untracked.py",
            "lines": "L1-L2",
            "verbatim_code": "def secret_untracked_helper() -> int:",
        },
    ]
    inbox = f"""# Queue

### [OUTBOUND-PROPOSAL-BAD-CLAIMS-1] Bad Claims
- **Plattform:** Reddit
- **Ziel-URL / Thread:** https://www.reddit.com/r/python/comments/badclaims/thread/
- **Lösungs-Repo:** `ellmos-ai/super-tool`
- **Code-Beleg (Verifiziert):** `src/engine.py`
- [x] Genehmigt
#### Claim-Beleg-Vertrag (Verifiziert):
```json
{json.dumps(bad_contract, indent=2)}
```

#### Textvorschlag:
```text
We built ellmos-ai/super-tool with zero runtime dependencies in engine.py. Our package also ships a distributed consensus layer alongside Clutch and router.py.
```
"""
    (temp_workspace / "POST-EINGANG.md").write_text(inbox, encoding="utf-8")
    engine = CommunityOutreachEngine(temp_workspace)

    report = engine.verify_proposals()
    assert report["status"] == "failed"
    violations = report["results"][0]["contract_violations"]
    assert any(v.startswith("verbatim-code-mismatch:1:") for v in violations), violations
    assert any(v.startswith("untracked-claim-file:2:") for v in violations), violations
    assert any(v.startswith("uncovered-software-sentence:") for v in violations), violations
    assert "predicate-contradiction:zero-dependency:super-tool" in violations, violations
    assert "unverified-sister-repo:ellmos-ai/clutch" in violations, violations
    assert "unverified-mentioned-file:router.py" in violations, violations

    outbound = engine.phase2_outbound_execution()
    assert outbound[0]["status"] == "needs-action"
    assert outbound[0]["reason"] == "invalid-claim-contract"
