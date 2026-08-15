#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for community-outreach Skill
"""

import sys
import json
import shutil
import pytest
from pathlib import Path

# Add scripts directory to path
SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from outreach_engine import CommunityOutreachEngine
from init_outreach_workspace import bootstrap_workspace

@pytest.fixture
def temp_workspace(tmp_path):
    ws = tmp_path / "test_outreach"
    sample_repos = [
        {
            "name": "super-tool",
            "org": "my-org",
            "url": "https://github.com/my-org/super-tool",
            "description": "Ein fantastisches Werkzeug.",
            "usecases": ["Testing", "Automation"],
            "solved_problems": ["Manuelle Tests", "Hohe Fehlerquote"],
            "last_promoted": None
        },
        {
            "name": "data-cruncher",
            "org": "my-org",
            "url": "https://github.com/my-org/data-cruncher",
            "description": "Schnelle Datenanalyse.",
            "usecases": ["Data Processing"],
            "solved_problems": ["Langsame Auswertung"],
            "last_promoted": "2026-08-01T00:00:00"
        }
    ]
    bootstrap_workspace(ws, repo_list=sample_repos)
    return ws

def test_workspace_bootstrap(temp_workspace):
    assert (temp_workspace / "USECASES.md").exists()
    assert (temp_workspace / "usecases.json").exists()
    assert (temp_workspace / "POST-EINGANG.md").exists()
    assert (temp_workspace / "POST-AUSGANG.md").exists()
    assert (temp_workspace / "POSTVERZEICHNIS.md").exists()
    assert (temp_workspace / "ACCOUNTVERZEICHNIS.md").exists()

def test_round_robin_selection(temp_workspace):
    engine = CommunityOutreachEngine(temp_workspace)
    # First candidate should be super-tool because last_promoted is None
    cand = engine.phase3_research_and_stage()
    assert cand is not None
    assert cand["repo_name"] == "super-tool"
    assert cand["platform"] == "Reddit"

    # Verify that inbox contains the new draft with [ ] checkbox
    inbox_text = (temp_workspace / "POST-EINGANG.md").read_text(encoding="utf-8")
    assert "### Post-Entwurf -- super-tool (Reddit)" in inbox_text
    assert "- [ ] Genehmigt" in inbox_text

def test_approval_and_publishing_workflow(temp_workspace):
    engine = CommunityOutreachEngine(temp_workspace)
    # Stage candidate
    engine.phase3_research_and_stage()

    # Simulate user approving by checking the box [x]
    inbox_file = temp_workspace / "POST-EINGANG.md"
    inbox_text = inbox_file.read_text(encoding="utf-8")
    inbox_approved = inbox_text.replace("- [ ] Genehmigt", "- [x] Genehmigt")
    inbox_file.write_text(inbox_approved, encoding="utf-8")

    # Run outbound phase
    published = engine.phase2_outbound_execution()
    assert len(published) == 1
    assert published[0]["repo_name"] == "super-tool"

    # Check that outbox and registry got updated
    outbox_text = (temp_workspace / "POST-AUSGANG.md").read_text(encoding="utf-8")
    assert "super-tool" in outbox_text
    assert "Reddit" in outbox_text

    reg_text = (temp_workspace / "POSTVERZEICHNIS.md").read_text(encoding="utf-8")
    assert "super-tool" in reg_text

    # Inbox should now be empty of approved posts
    remaining_inbox = inbox_file.read_text(encoding="utf-8")
    assert "- [x] Genehmigt" not in remaining_inbox
