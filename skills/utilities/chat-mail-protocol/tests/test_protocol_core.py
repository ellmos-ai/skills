"""Comprehensive tests (>=16 cases) for skills/utilities/chat-mail-protocol (v0.1.0)."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parents[2]
CORE_SCRIPT = SKILL_DIR / "scripts" / "protocol_core.py"
OCEAN_SCAFFOLD_SCRIPT = (
    REPO_ROOT / "skills" / "infrastructure" / "ocean-skill-creator" / "scripts" / "ocean_skill_scaffold.py"
)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


core = _load_module("protocol_core", CORE_SCRIPT)
ocean_scaffold = _load_module("ocean_skill_scaffold", OCEAN_SCAFFOLD_SCRIPT)


WHATSAPP_FIXTURE = """[27.11.2026, 09:12:04] Mara Klein: Guten Morgen zusammen, kurzes Sync zum Release.
[27.11.2026, 09:14:10] Jonas Berg: Beschlossen: Wir nutzen das neue SQLite-Schema v2 für den Export.
Fortsetzung: Die Migration bleibt rein additiv.
[27.11.2026, 09:16:22] Mara Klein: @Jonas bitte die Migrationsprüfung bis 2026-12-04 aktualisieren.
[27.11.2026, 09:17:05] Clara Vogt: Ich übernehme die Testdaten für das PDF-Layout.
[27.11.2026, 09:18:40] Jonas Berg: Blocker: Der Staging-Zugang wartet auf die Freigabe vom Infrastruktur-Team.
[27.11.2026, 09:19:15] Clara Vogt: Brauchen wir zusätzlich ein englisches Deckblatt?
"""

EMAIL_THREAD_FIXTURE = """From: "Dr. Nora Sommer" <nora.sommer@example.org>
To: Projektkreis <team@example.org>
Date: 2026-11-27 11:30
Subject: Re: Abstimmung Quartalsbericht Q4

Hallo zusammen,

Beschluss: Wir geben die Druckfassung im A4-Layout frei.
TODO: @Milan erstellt die finale Tabellenübersicht bis 10.12.2026.
Offen: Welche Kostenstelle trägt den Sonderdruck?

Viele Grüße
Nora

> Am 27.11.2026 schrieb Milan Roth:
> Alter zitierter Text, der nicht doppelt gezählt werden darf.

--- Original Message ---
From: Milan Roth <milan.roth@example.org>
To: Projektkreis <team@example.org>
Date: 2026-11-27 08:15
Subject: Abstimmung Quartalsbericht Q4

Guten Morgen,
ich bereite heute den Entwurf für den Quartalsbericht vor.
"""


# ---------------------------------------------------------------------------
# 1. Multi-Format Chat & Email Parsing
# ---------------------------------------------------------------------------

def test_parse_whatsapp_brackets_and_multiline_continuation() -> None:
    parsed = core.parse_messages(WHATSAPP_FIXTURE)
    assert parsed["channel"] == "whatsapp"
    assert len(parsed["messages"]) == 6
    assert parsed["messages"][1]["author"] == "Jonas Berg"
    assert "Die Migration bleibt rein additiv." in parsed["messages"][1]["text"]


def test_parse_whatsapp_android_dash_format() -> None:
    raw = (
        "27.11.26, 14:05 - Anna: Wir starten um 15 Uhr.\n"
        "27.11.26, 14:06 - Ben: Ich kümmere mich um die Agenda.\n"
    )
    parsed = core.parse_messages(raw)
    assert parsed["channel"] == "whatsapp"
    assert [m["author"] for m in parsed["messages"]] == ["Anna", "Ben"]


def test_parse_slack_iso_and_json_export() -> None:
    slack_txt = (
        "[2026-11-27 10:00] DevLead: Agreed: we will use stdlib-only rendering.\n"
        "OpsEng [10:02]: TODO: verify CI matrix on Linux and Windows\n"
    )
    p1 = core.parse_messages(slack_txt)
    assert p1["channel"] == "slack"
    assert len(p1["messages"]) == 2

    json_export = json.dumps({
        "channel": "slack",
        "messages": [
            {"user": "Elena", "ts": "2026-11-27T12:00:00Z", "text": "Beschlossen: Release am Freitag."},
            {"user": "Tariq", "ts": "2026-11-27T12:02:00Z", "text": "Ich übernehme den Changelog."},
        ],
    })
    p2 = core.parse_messages(json_export)
    assert p2["channel"] == "slack"
    assert len(p2["messages"]) == 2
    assert p2["messages"][0]["author"] == "Elena"


def test_parse_discord_two_line_blocks() -> None:
    discord_raw = (
        "ModAlpha — 27.11.2026 18:20\n"
        "Entschieden: Der Release-Channel bleibt schreibgeschützt.\n"
        "BuilderBeta — 27.11.2026 18:22\n"
        "TODO: @ModAlpha Rechte im Staging prüfen\n"
    )
    parsed = core.parse_messages(discord_raw)
    assert parsed["channel"] == "discord"
    assert len(parsed["messages"]) == 2
    assert parsed["messages"][0]["author"] == "ModAlpha"


def test_parse_email_thread_chronological_and_strips_quotes() -> None:
    parsed = core.parse_messages(EMAIL_THREAD_FIXTURE)
    assert parsed["channel"] == "email"
    assert parsed["subject"] == "Abstimmung Quartalsbericht Q4"
    assert len(parsed["messages"]) == 2
    # Chronological order: 08:15 Milan first, 11:30 Nora second, and '>' quote stripped
    assert parsed["messages"][0]["author"] == "Milan Roth"
    assert parsed["messages"][1]["author"] == "Dr. Nora Sommer"
    assert "doppelt gezählt" not in parsed["messages"][1]["text"]


# ---------------------------------------------------------------------------
# 2. Source-Grounded Extraction & Participant Anonymization
# ---------------------------------------------------------------------------

def test_analyze_conversation_extracts_decisions_tasks_due_questions_and_blockers() -> None:
    analysis = core.analyze_conversation(WHATSAPP_FIXTURE, chat="Release Sync")
    assert analysis["channel"] == "whatsapp"
    assert analysis["chat"] == "release-sync"
    assert analysis["participant_count"] == 3
    assert analysis["message_count"] == 6

    assert len(analysis["decisions"]) == 1
    assert "SQLite-Schema v2" in analysis["decisions"][0]["text"]
    assert analysis["decisions"][0]["source_index"] == 2

    assert len(analysis["action_items"]) == 2
    by_owner = {item["owner"]: item for item in analysis["action_items"]}
    assert by_owner["Jonas Berg"]["due"] == "2026-12-04"
    assert by_owner["Clara Vogt"]["due"] is None  # never invent missing due dates!

    assert len(analysis["blockers"]) == 1
    assert analysis["blockers"][0]["source_index"] == 5
    assert len(analysis["open_questions"]) == 1
    assert analysis["open_questions"][0]["source_index"] == 6


def test_anonymize_participants_replaces_authors_and_mentions() -> None:
    analysis = core.analyze_conversation(
        WHATSAPP_FIXTURE,
        chat="Vertraulich",
        anonymize_participants=True,
    )
    assert analysis["participants"] == ["Person A", "Person B", "Person C"]
    serialized = json.dumps(analysis, ensure_ascii=False)
    for real_name in ("Mara", "Klein", "Jonas", "Berg", "Clara", "Vogt"):
        assert real_name not in serialized


# ---------------------------------------------------------------------------
# 3. 4-Stage Channel/Chat Config Cascade & Self-Healing
# ---------------------------------------------------------------------------

def test_four_stage_channel_and_chat_profile_cascade(tmp_path: Path) -> None:
    # Copy bundled whatsapp & whatsapp.projekt-alpha example profiles as active overrides
    (tmp_path / "config.json").write_text(
        json.dumps({"presentation": {"language": "de", "anonymize_participants": False}}),
        encoding="utf-8",
    )
    (tmp_path / "whatsapp.json").write_text(
        (SKILL_DIR / "profiles" / "whatsapp.example.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "whatsapp.projekt-alpha.json").write_text(
        (SKILL_DIR / "profiles" / "whatsapp.projekt-alpha.example.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    # Generic WhatsApp chat gets whatsapp.json (txt + pdf, compact)
    res_generic_wa = core.load_effective_channel_config(
        config_dir=tmp_path,
        channel="whatsapp",
        chat="allgemein",
    )
    assert res_generic_wa["ok"] is True
    assert res_generic_wa["config"]["formats"] == ["txt", "pdf"]
    assert res_generic_wa["config"]["presentation"]["detail_level"] == "compact"

    # Specific chat 'projekt-alpha' overrides whatsapp.json via whatsapp.projekt-alpha.json!
    res_alpha = core.load_effective_channel_config(
        config_dir=tmp_path,
        channel="whatsapp",
        chat="projekt-alpha",
    )
    assert res_alpha["ok"] is True
    assert res_alpha["config"]["formats"] == ["html", "pdf", "md"]
    assert res_alpha["config"]["presentation"]["detail_level"] == "detailed"
    assert res_alpha["config"]["delivery"]["handoff_tasks_to"] == "ticket-master"
    assert len(res_alpha["loaded_layers"]) == 4


def test_missing_channel_profile_falls_back_to_default_cleanly(tmp_path: Path) -> None:
    res = core.load_effective_channel_config(
        config_dir=tmp_path,
        channel="telegram",
        chat="ops-feed",
    )
    assert res["ok"] is True
    assert res["warnings"] == []
    assert res["config"]["template"] == "ergebnisprotokoll"
    assert len(res["loaded_layers"]) == 1
    assert len(res["skipped_layers"]) == 3


def test_corrupt_channel_config_falls_back_and_self_heals_with_backup(tmp_path: Path) -> None:
    corrupt_slack = tmp_path / "slack.json"
    raw_corrupt = b'{"formats": ["md", BROKEN_JSON'
    corrupt_slack.write_bytes(raw_corrupt)

    # Without repair_config -> no crash, falls back to default-config.json, records warning
    res_no_repair = core.load_effective_channel_config(
        config_dir=tmp_path,
        channel="slack",
        repair_config=False,
    )
    assert res_no_repair["ok"] is False
    assert len(res_no_repair["warnings"]) == 1
    assert res_no_repair["config"]["formats"] == ["md", "html", "pdf"]
    assert corrupt_slack.read_bytes() == raw_corrupt

    # With repair_config=True -> creates .corrupt.<ts>.bak and restores valid JSON atomically
    res_repaired = core.load_effective_channel_config(
        config_dir=tmp_path,
        channel="slack",
        repair_config=True,
        timestamp="20261127T040000Z",
    )
    assert res_repaired["ok"] is True
    assert len(res_repaired["healed"]) == 1
    bak = tmp_path / "slack.json.corrupt.20261127T040000Z.bak"
    assert bak.read_bytes() == raw_corrupt
    assert json.loads(corrupt_slack.read_text(encoding="utf-8")) == {}


# ---------------------------------------------------------------------------
# 4. Rendering All 5 Formats, WinAnsi PDF Umlaute/xref, Custom Templates & XSS Escape
# ---------------------------------------------------------------------------

def test_render_all_five_formats_including_pdf_umlaute_and_valid_xref() -> None:
    analysis = core.analyze_conversation(EMAIL_THREAD_FIXTURE)

    html_str = core.render_protocol(analysis, fmt="html")
    assert isinstance(html_str, str)
    assert "@media print" in html_str
    assert "Abstimmung Quartalsbericht Q4" in html_str
    assert "2026-12-10" in html_str

    md_str = core.render_protocol(analysis, fmt="md")
    assert isinstance(md_str, str)
    assert "| A-01 |" in md_str
    assert "Dr. Nora Sommer" in md_str

    tasks_md = core.render_protocol(analysis, fmt="md", template="aufgabenliste")
    assert "# Aufgabenliste — Abstimmung Quartalsbericht Q4" in str(tasks_md)

    txt_str = core.render_protocol(analysis, fmt="txt")
    assert "1. BESCHLUESSE & ERGEBNISSE" in str(txt_str)

    json_str = core.render_protocol(analysis, fmt="json")
    assert json.loads(str(json_str))["channel"] == "email"

    pdf_bytes = core.render_protocol(analysis, fmt="pdf")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"/WinAnsiEncoding" in pdf_bytes
    # Verify German Umlaut 'ü' ('Tabellenübersicht' / 'Beschlüsse') is encoded as WinAnsi \374!
    assert b"\\374" in pdf_bytes
    # Verify exact startxref byte offset points directly to 'xref\n'!
    m_xref = re.search(rb"startxref\n(\d+)\n%%EOF\s*$", pdf_bytes)
    assert m_xref is not None
    xref_pos = int(m_xref.group(1))
    assert pdf_bytes[xref_pos : xref_pos + 5] == b"xref\n"


def test_html_renderer_escapes_script_injection_in_messages() -> None:
    xss_chat = "[27.11.2026, 10:00:00] Mallroy: Beschlossen: <script>alert('xss')</script> wird blockiert."
    analysis = core.analyze_conversation(xss_chat)
    rendered_html = str(core.render_protocol(analysis, fmt="html"))
    assert "<script>" not in rendered_html
    assert "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" in rendered_html


def test_custom_template_dir_override(tmp_path: Path) -> None:
    custom_dir = tmp_path / "my_templates"
    custom_dir.mkdir()
    (custom_dir / "custom-board.md").write_text(
        "BOARD={{chat_label}}|DECISIONS={{decision_count}}|TASKS={{task_count}}\n",
        encoding="utf-8",
    )
    analysis = core.analyze_conversation(WHATSAPP_FIXTURE, chat="Board Sync")
    out = core.render_protocol(
        analysis,
        fmt="md",
        template="custom-board",
        config={"templates": {"custom_dir": str(custom_dir)}},
    )
    assert out == "BOARD=Board Sync|DECISIONS=1|TASKS=2\n"


# ---------------------------------------------------------------------------
# 5. Safe Delivery Plan (reply_in_chat + Handoff) & End-to-End CLI
# ---------------------------------------------------------------------------

def test_delivery_plan_reply_in_chat_and_safe_dry_run_defaults(tmp_path: Path) -> None:
    (tmp_path / "slack.json").write_text(
        (SKILL_DIR / "profiles" / "slack.example.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    in_file = tmp_path / "slack_chat.txt"
    in_file.write_text(
        "[2026-11-27 09:00] Lea: Beschlossen: Deployment startet um 16:00.\n"
        "[2026-11-27 09:02] Lea: TODO: @Max Smoke-Tests bis 2026-11-28 ausführen.\n",
        encoding="utf-8",
    )
    out_dir = tmp_path / "exports"

    bundle = core.process_conversation(
        in_file.read_text(encoding="utf-8"),
        config_dir=tmp_path,
        channel="slack",
        chat="deploy-room",
        out_dir=out_dir,
    )
    dplan = bundle["delivery_plan"]
    assert dplan["dry_run"] is True
    assert dplan["mode"] == "draft"
    assert dplan["sent_externally"] is False
    assert dplan["reply_in_chat"]["enabled"] is True
    assert dplan["reply_in_chat"]["template"] == "kompakt-chat"
    assert "Kurzprotokoll: deploy-room" in dplan["reply_in_chat"]["payload"]
    assert (out_dir / "slack_deploy-room.md").is_file()
    assert (out_dir / "slack_deploy-room.json").is_file()


def test_cli_process_show_config_and_list_templates(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    chat_file = tmp_path / "input.txt"
    chat_file.write_text(WHATSAPP_FIXTURE, encoding="utf-8")
    out_dir = tmp_path / "out"

    rc1 = core.main([
        "process",
        "--input", str(chat_file),
        "--chat", "projekt-alpha",
        "--doc-types", "zusammenfassung,ergebnisprotokoll,aufgabenliste,protokoll",
        "--formats", "html,pdf,md,txt,json",
        "--out-dir", str(out_dir),
        "--json",
    ])
    assert rc1 == 0
    proc_json = json.loads(capsys.readouterr().out)
    assert proc_json["ok"] is True
    for ext in ("html", "pdf", "md", "txt", "json"):
        assert (out_dir / f"whatsapp_projekt-alpha.{ext}").is_file()

    rc2 = core.main(["show-config", "--channel", "whatsapp", "--json"])
    assert rc2 == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True

    rc3 = core.main(["list-templates", "--json"])
    assert rc3 == 0
    tpls = json.loads(capsys.readouterr().out)["templates"]
    assert {"ergebnisprotokoll.html", "ergebnisprotokoll.md", "ergebnisprotokoll.txt", "kompakt-chat.txt", "aufgabenliste.md"} <= set(tpls.keys())


# ---------------------------------------------------------------------------
# 6. Ocean Skill Creator v0.4.0 Audit Gate & Public Privacy Cleanliness
# ---------------------------------------------------------------------------

def test_ocean_skill_creator_audits_chat_mail_protocol_as_conformant() -> None:
    audit = ocean_scaffold.audit_skill(SKILL_DIR)
    assert audit["skill"] == "chat-mail-protocol"
    assert audit["status"] == "conformant", f"Expected conformant audit, got: {audit}"
    assert audit["score"] >= 95
    assert audit["hardcoding_signals"] == []
    assert audit["checks"]["has_default_config"] is True
    assert audit["checks"]["has_self_healing"] is True
    assert audit["checks"]["has_report_templates"] is True
    assert audit["checks"]["trigger_in_first_250_chars"] is True


def test_bundled_profiles_and_files_are_valid_json_and_privacy_clean() -> None:
    profile_files = sorted((SKILL_DIR / "profiles").glob("*.example.json"))
    assert len(profile_files) == 5
    for pf in profile_files:
        data = json.loads(pf.read_text(encoding="utf-8"))
        assert data["schema"] == "ocean.skill-profile.v1"
        assert data["delivery"]["dry_run"] is True

    private_ip_re = re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
    )
    for fpath in SKILL_DIR.rglob("*"):
        if not fpath.is_file() or "__pycache__" in fpath.parts:
            continue
        if fpath.suffix.lower() in {".md", ".json", ".py", ".html", ".txt"}:
            txt = fpath.read_text(encoding="utf-8")
            assert private_ip_re.search(txt) is None, f"Private LAN IP found in {fpath.name}"
