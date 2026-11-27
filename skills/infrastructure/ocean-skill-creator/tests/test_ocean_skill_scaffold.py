"""Comprehensive tests for ocean-skill-creator v0.4.1 (pragmatic config names, optional templates/scripts, self-healing, scaffold/init, audit)."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
SCAFFOLD_SCRIPT = SKILL_DIR / "scripts" / "ocean_skill_scaffold.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("ocean_skill_scaffold", SCAFFOLD_SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


osc = _load_module()


# ---------------------------------------------------------------------------
# 1. 5-Stage Config Cascade (base .json -> config -> channel -> channel.chat -> CLI)
# ---------------------------------------------------------------------------

def test_five_stage_config_cascade_precedence(tmp_path: Path) -> None:
    default_cfg = {
        "schema": "ocean.skill-config.v2",
        "skill": "digest-demo",
        "settings": {"max_items": 20, "language": "de", "include_summary": True},
        "output": {"default_format": "md", "supported_formats": ["html", "pdf", "md", "txt", "json"]},
        "delivery": {"enabled": False, "dry_run": True, "mode": "draft", "channel": None},
    }
    osc.atomic_write_json(tmp_path / "default-config.json", default_cfg)
    osc.atomic_write_json(
        tmp_path / "config.json",
        {"settings": {"max_items": 35}, "output": {"default_format": "txt"}},
    )
    osc.atomic_write_json(
        tmp_path / "profiles" / "mail.json",
        {"output": {"default_format": "html"}, "delivery": {"channel": "mail"}},
    )
    osc.atomic_write_json(
        tmp_path / "profiles" / "mail.weekly-board.json",
        {"settings": {"language": "en"}, "output": {"default_format": "pdf"}},
    )

    chain = osc.resolve_profile_chain(tmp_path, channel="mail", chat="weekly-board")
    res = osc.load_effective_config(
        tmp_path / "default-config.json",
        chain,
        cli_overrides=osc.dotted_pairs_to_dict(["settings.max_items=99"]),
    )

    assert res["ok"] is True
    assert res["warnings"] == []
    eff = res["config"]
    assert eff["settings"]["include_summary"] is True
    assert eff["delivery"]["channel"] == "mail"
    assert eff["settings"]["language"] == "en"
    assert eff["output"]["default_format"] == "pdf"
    assert eff["output"]["supported_formats"] == ["html", "pdf", "md", "txt", "json"]
    assert eff["settings"]["max_items"] == 99


def test_missing_optional_overrides_fall_back_cleanly(tmp_path: Path) -> None:
    osc.atomic_write_json(
        tmp_path / "default-config.json",
        {"schema": "ocean.skill-config.v2", "skill": "solo", "settings": {"limit": 10}},
    )
    chain = osc.resolve_profile_chain(tmp_path, channel="chat", chat="general")
    res = osc.load_effective_config(tmp_path / "default-config.json", chain)
    assert res["ok"] is True
    assert res["warnings"] == []
    assert res["config"]["settings"]["limit"] == 10
    assert len(res["layers_skipped"]) == 3


# ---------------------------------------------------------------------------
# 2. Self-Healing (corrupt JSON, .corrupt.<ts>.bak backup, section guard, additive migration)
# ---------------------------------------------------------------------------

def test_corrupt_config_graceful_fallback_without_repair(tmp_path: Path) -> None:
    osc.atomic_write_json(
        tmp_path / "default-config.json",
        {"schema": "ocean.skill-config.v2", "skill": "safe-skill", "output": {"default_format": "md"}},
    )
    bad_cfg = tmp_path / "config.json"
    bad_cfg.write_text("{ broken: json, missing_quotes ", encoding="utf-8")

    res = osc.load_effective_config(tmp_path / "default-config.json", [bad_cfg], repair=False)
    assert res["ok"] is False
    assert len(res["warnings"]) == 1
    assert res["healed"] == []
    assert res["config"]["output"]["default_format"] == "md"
    assert bad_cfg.read_text(encoding="utf-8").startswith("{ broken:")


def test_corrupt_config_and_profile_self_heal_with_timestamped_backup(tmp_path: Path) -> None:
    default_payload = {
        "schema": "ocean.skill-config.v2",
        "skill": "heal-me",
        "settings": {"threshold": 5},
    }
    osc.atomic_write_json(tmp_path / "default-config.json", default_payload)

    bad_cfg = tmp_path / "config.json"
    corrupt_bytes = b'{"settings": {"threshold": '
    bad_cfg.write_bytes(corrupt_bytes)

    bad_prof = tmp_path / "profiles" / "slack.json"
    bad_prof.parent.mkdir(parents=True, exist_ok=True)
    bad_prof.write_text('["wrong-root-array"]', encoding="utf-8")

    res = osc.load_effective_config(
        tmp_path / "default-config.json",
        [bad_cfg, bad_prof],
        repair=True,
        timestamp="20261127T030000Z",
    )
    assert res["ok"] is True
    assert len(res["healed"]) == 2

    cfg_bak = tmp_path / "config.json.corrupt.20261127T030000Z.bak"
    prof_bak = tmp_path / "profiles" / "slack.json.corrupt.20261127T030000Z.bak"
    assert cfg_bak.read_bytes() == corrupt_bytes
    assert prof_bak.read_text(encoding="utf-8") == '["wrong-root-array"]'

    assert json.loads(bad_cfg.read_text(encoding="utf-8")) == default_payload
    assert json.loads(bad_prof.read_text(encoding="utf-8")) == {}


def test_additive_migration_backfills_new_keys_without_clobbering_user_values(tmp_path: Path) -> None:
    default_v2 = {
        "schema": "ocean.skill-config.v2",
        "skill": "migratable",
        "settings": {"keep_me": 10, "new_flag": True},
        "self_healing": {"enabled": True, "backup_corrupt": True},
    }
    user_v1 = {
        "schema": "ellmos.skill-config.v1",
        "skill": "migratable",
        "settings": {"keep_me": 42},
    }
    osc.atomic_write_json(tmp_path / "default-config.json", default_v2)
    osc.atomic_write_json(tmp_path / "config.json", user_v1)

    res = osc.load_effective_config(
        tmp_path / "default-config.json",
        [tmp_path / "config.json"],
        repair=True,
    )
    assert res["ok"] is True
    assert "settings.new_flag" in res["migrated_keys"]
    assert "self_healing" in res["migrated_keys"]
    persisted = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert persisted["settings"]["keep_me"] == 42
    assert persisted["settings"]["new_flag"] is True
    assert persisted["self_healing"]["enabled"] is True


def test_section_type_mismatch_is_guarded_and_repaired(tmp_path: Path) -> None:
    osc.atomic_write_json(
        tmp_path / "default-config.json",
        {"schema": "ocean.skill-config.v2", "output": {"default_format": "md"}},
    )
    osc.atomic_write_json(tmp_path / "config.json", {"output": "broken-scalar"})

    res = osc.load_effective_config(
        tmp_path / "default-config.json",
        [tmp_path / "config.json"],
        repair=True,
        timestamp="20261127T031500Z",
    )
    assert res["config"]["output"] == {"default_format": "md"}
    assert len(res["healed"]) == 1
    assert (tmp_path / "config.json.corrupt.20261127T031500Z.bak").is_file()


# ---------------------------------------------------------------------------
# 3. Output Rendering & Templates (html, pdf, md, txt, json + custom_dir)
# ---------------------------------------------------------------------------

def test_render_report_all_five_formats_and_custom_template_override(tmp_path: Path) -> None:
    payload = {
        "title": "Quartalsübersicht & Prüfbericht",
        "subtitle": "Silo Infrastruktur",
        "generated_at": "2026-11-27T03:00:00Z",
        "summary": "3 Komponenten geprüft, 0 kritische Abweichungen.",
        "items": ["Config-Kaskade aktiv", "PDF-Fallback verifiziert"],
        "footer": "Ocean Standard v0.4.1",
    }
    html_out = osc.render_report(payload, fmt="html")
    assert isinstance(html_out, str)
    assert "@media print" in html_out
    assert "Quartalsübersicht &amp; Prüfbericht" in html_out

    md_out = osc.render_report(payload, fmt="md")
    assert isinstance(md_out, str)
    assert "# Quartalsübersicht & Prüfbericht" in md_out
    assert "- Config-Kaskade aktiv" in md_out

    txt_out = osc.render_report(payload, fmt="txt")
    assert isinstance(txt_out, str)
    assert "KURZFASSUNG" in txt_out
    assert "* PDF-Fallback verifiziert" in txt_out

    json_out = osc.render_report(payload, fmt="json")
    assert json.loads(str(json_out))["summary"].startswith("3 Komponenten")

    pdf_out = osc.render_report(payload, fmt="pdf")
    assert isinstance(pdf_out, bytes)
    assert pdf_out.startswith(b"%PDF-1.4")
    assert b"Quartalsuebersicht" in pdf_out
    assert pdf_out.rstrip().endswith(b"%%EOF")

    custom_tpl_dir = tmp_path / "custom_tpl"
    custom_tpl_dir.mkdir()
    (custom_tpl_dir / "report.template.md").write_text("CUSTOM::{{title}}::{{summary}}\n", encoding="utf-8")
    custom_md = osc.render_report(
        payload,
        fmt="md",
        config={"templates": {"custom_dir": str(custom_tpl_dir)}},
    )
    assert custom_md == "CUSTOM::Quartalsübersicht & Prüfbericht::3 Komponenten geprüft, 0 kritische Abweichungen.\n"


# ---------------------------------------------------------------------------
# 4. Pragmatic v0.4.1 Regressions (lean skills, custom .json names, init flags)
# ---------------------------------------------------------------------------

def test_lean_guideline_skill_without_json_templates_or_scripts_scores_100_conformant(
    tmp_path: Path,
) -> None:
    """v0.4.1 Regression #1: Lean guideline/counseling/router skill (SKILL.md + SKILL.en.md only) scores 100/100."""
    lean_dir = tmp_path / "structured-reflection"
    lean_dir.mkdir()
    (lean_dir / "SKILL.md").write_text(
        """---
name: structured-reflection
version: 0.2.0
type: skill
author: Ocean Contributors
created: 2026-11-27
updated: 2026-11-27
description: "Verwenden, wenn komplexe Entscheidungen strukturiert durchdacht werden sollen (z. B. 'Entscheidung reflektieren', 'Überblick und Optionen klären', /structured-reflection). Bietet einen klaren Leitfaden ohne Skript-Ballast. NICHT verwenden für Dateivergleiche."
standalone: true
visibility: public
---

# structured-reflection — Reflexionsleitfaden

Reiner Denk- und Beratungsleitfaden ohne Konfigurationsdateien, Vorlagen oder Skripte.
""",
        encoding="utf-8",
    )
    (lean_dir / "SKILL.en.md").write_text(
        """---
name: structured-reflection
version: 0.2.0
type: skill
author: Ocean Contributors
created: 2026-11-27
updated: 2026-11-27
description: "Use when reflecting on complex decisions systematically (e.g. 'reflect on this choice', 'decision overview and summary', /structured-reflection). Provides a clear thinking framework without script boilerplate. Do NOT use for file diffs."
standalone: true
visibility: public
---

# structured-reflection — Reflection Guide

Pure advisory and thinking framework without JSON configs, templates, or scripts.
""",
        encoding="utf-8",
    )

    audit = osc.audit_skill(lean_dir)
    assert audit["status"] == "conformant"
    assert audit["score"] == 100
    assert audit["recommendations"] == []
    assert audit["hardcoding_signals"] == []
    assert audit["config_files"] == []
    assert audit["has_external_config"] is False
    assert audit["checks"]["needs_templates"] is False


def test_skill_with_custom_json_config_name_and_self_healing_is_conformant(tmp_path: Path) -> None:
    """v0.4.1 Regression #2: Expressive custom .json filename (routing-defaults.json) is recognized on equal footing."""
    skill_dir = tmp_path / "tier-router"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "tests").mkdir(parents=True)

    (skill_dir / "SKILL.md").write_text(
        """---
name: tier-router
version: 0.1.0
type: skill
author: Ocean Contributors
created: 2026-11-27
updated: 2026-11-27
description: "Verwenden, wenn Aufgaben nach Komplexität geroutet werden sollen (z. B. 'Aufgabe routen', /tier-router). Lädt Stufengrenzen aus routing-defaults.json. NICHT verwenden für Skill-Suche (skill-finder)."
standalone: true
visibility: private-only
---

# tier-router
""",
        encoding="utf-8",
    )
    (skill_dir / "SKILL.en.md").write_text(
        """---
name: tier-router
version: 0.1.0
type: skill
author: Ocean Contributors
created: 2026-11-27
updated: 2026-11-27
description: "Use when routing tasks by complexity tier (e.g. 'route task', /tier-router). Loads thresholds from routing-defaults.json. Do NOT use for skill discovery (skill-finder)."
standalone: true
visibility: private-only
---

# tier-router (English)
""",
        encoding="utf-8",
    )
    osc.atomic_write_json(
        skill_dir / "routing-defaults.json",
        {"tiers": {"light": 10, "heavy": 30}},
    )
    (skill_dir / "scripts" / "router_core.py").write_text(
        """import json
from pathlib import Path

def load_tiers(root: Path) -> dict:
    fallback = json.loads((root / "routing-defaults.json").read_text(encoding="utf-8"))
    local = root / "routing.local.json"
    if not local.is_file():
        return fallback
    try:
        return {**fallback, **json.loads(local.read_text(encoding="utf-8"))}
    except json.JSONDecodeError:
        return fallback
""",
        encoding="utf-8",
    )
    (skill_dir / "tests" / "test_router.py").write_text(
        "def test_placeholder():\n    assert True\n",
        encoding="utf-8",
    )

    audit = osc.audit_skill(skill_dir)
    assert audit["status"] == "conformant"
    assert audit["score"] == 100
    assert audit["recommendations"] == []
    assert audit["config_files"] == ["routing-defaults.json"]
    assert audit["has_external_config"] is True
    assert audit["checks"]["has_default_config"] is True
    assert audit["checks"]["has_literal_default_config"] is False


def test_init_cli_with_custom_config_name_and_no_templates_creates_lean_structure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """v0.4.1 Regression #3: `init --config-name custom-prefs.json --no-templates` produces exact structure & passes tests."""
    rc = osc.main([
        "init",
        "smart-router",
        "--category", "infrastructure",
        "--out", str(tmp_path),
        "--config-name", "custom-prefs.json",
        "--no-templates",
        "--json",
    ])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    sdir = Path(payload["skill_dir"])
    assert (sdir / "custom-prefs.json").is_file()
    assert not (sdir / "default-config.json").exists()
    assert not (sdir / "templates").exists()
    assert (sdir / "scripts" / "smart_router_core.py").is_file()
    assert (sdir / "tests" / "test_smart_router.py").is_file()

    # Generated pytest suite runs cleanly against custom-prefs.json!
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(sdir / "tests")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert proc.returncode == 0, f"Generated custom-config tests failed:\n{proc.stdout}\n{proc.stderr}"

    audit = osc.audit_skill(sdir)
    assert audit["status"] == "conformant"
    assert audit["score"] == 100
    assert audit["config_files"] == ["custom-prefs.json"]
    assert audit["recommendations"] == []


def test_init_cli_minimal_creates_pure_prompt_skill_scoring_100(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = osc.main([
        "init",
        "calm-grounding",
        "--category", "therapy",
        "--out", str(tmp_path),
        "--minimal",
        "--json",
    ])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    sdir = Path(payload["skill_dir"])
    assert sorted(p.name for p in sdir.iterdir()) == ["SKILL.en.md", "SKILL.md"]
    audit = osc.audit_skill(sdir)
    assert audit["status"] == "conformant"
    assert audit["score"] == 100
    assert audit["recommendations"] == []


# ---------------------------------------------------------------------------
# 5. Full Scaffold Subcommand & Audit-Skill on Hardcoded Fixtures
# ---------------------------------------------------------------------------

def test_scaffold_with_reports_and_profiles_creates_working_skill(tmp_path: Path) -> None:
    res = osc.scaffold_skill(
        "weekly-status-digest",
        category="utilities",
        out_dir=tmp_path,
        with_reports=True,
        with_profiles=True,
        today="2026-11-27",
    )
    assert res["ok"] is True
    sdir = Path(res["skill_dir"])
    assert (sdir / "SKILL.md").is_file()
    assert (sdir / "SKILL.en.md").is_file()
    assert (sdir / "default-config.json").is_file()
    assert (sdir / "connections.json").is_file()
    assert (sdir / "profiles" / "example.json").is_file()
    assert (sdir / "profiles" / "example.team-digest.json").is_file()
    assert (sdir / "templates" / "report.template.html").is_file()
    assert (sdir / "templates" / "report.template.md").is_file()
    assert (sdir / "templates" / "report.template.txt").is_file()

    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(sdir / "tests")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert proc.returncode == 0, f"Generated skill tests failed:\n{proc.stdout}\n{proc.stderr}"

    audit = osc.audit_skill(sdir)
    assert audit["status"] == "conformant"
    assert audit["score"] == 100
    assert audit["hardcoding_signals"] == []


def test_audit_skill_detects_minimal_and_hardcoding_signals(tmp_path: Path) -> None:
    legacy_dir = tmp_path / "legacy-hardcoded-skill"
    (legacy_dir / "scripts").mkdir(parents=True)
    (legacy_dir / "SKILL.md").write_text(
        "---\nname: legacy-hardcoded-skill\ndescription: \"Generates HTML reports.\"\n---\n# Legacy\n",
        encoding="utf-8",
    )
    synthetic_path = "/" + "opt" + "/fixed_account/output/report.html"
    (legacy_dir / "scripts" / "run.py").write_text(
        f'DEFAULT_TIMEOUT = 120\ndefault_format = "html"\nOUT = "{synthetic_path}"\n'
        'HTML = "<!DOCTYPE html><html><body>Hardcoded</body></html>"\n',
        encoding="utf-8",
    )

    report = osc.audit_skill(legacy_dir)
    assert report["status"] in {"minimal", "needs_upgrade"}
    assert report["score"] < 55
    signal_kinds = {sig["kind"] for sig in report["hardcoding_signals"]}
    assert "hardcoded_path" in signal_kinds
    assert "inline_html_without_templates" in signal_kinds
    assert "hardcoded_output_format" in signal_kinds
    assert "magic_thresholds_without_config" in signal_kinds
    assert len(report["recommendations"]) >= 4


def test_ocean_skill_creator_audits_itself_cleanly() -> None:
    report = osc.audit_skill(SKILL_DIR)
    assert report["skill"] == "ocean-skill-creator"
    assert report["status"] == "conformant"
    assert report["score"] == 100
    assert report["hardcoding_signals"] == []


def test_cli_subcommands_scaffold_validate_and_audit_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc_scaf = osc.main([
        "scaffold", "ops-briefing",
        "--category", "infrastructure",
        "--out", str(tmp_path),
        "--with-reports",
        "--with-profiles",
        "--json",
    ])
    assert rc_scaf == 0
    scaf_payload = json.loads(capsys.readouterr().out)
    skill_path = Path(scaf_payload["skill_dir"])

    rc_val = osc.main([
        "validate-config",
        "--default", str(skill_path / "default-config.json"),
        "--channel", "example",
        "--chat", "team-digest",
        "--set", "settings.max_items=77",
        "--json",
    ])
    assert rc_val == 0
    val_payload = json.loads(capsys.readouterr().out)
    assert val_payload["ok"] is True
    assert val_payload["config"]["settings"]["max_items"] == 77
    assert val_payload["config"]["output"]["default_format"] == "html"

    rc_aud = osc.main(["audit-skill", str(skill_path), "--json"])
    assert rc_aud == 0
    aud_payload = json.loads(capsys.readouterr().out)
    assert aud_payload["status"] == "conformant"


def test_all_bundled_json_templates_and_configs_are_valid_and_privacy_clean() -> None:
    json_files = [
        SKILL_DIR / "default-config.json",
        SKILL_DIR / "config.json",
        *sorted((SKILL_DIR / "templates").glob("*.json")),
    ]
    assert len(json_files) >= 8
    for jf in json_files:
        parsed = json.loads(jf.read_text(encoding="utf-8"))
        assert isinstance(parsed, dict), f"{jf.name} must be a JSON object"

    for tpl_name in ("report.template.html", "report.template.md", "report.template.txt"):
        tpl_path = SKILL_DIR / "templates" / "output" / tpl_name
        assert tpl_path.is_file()
        assert "{{title}}" in tpl_path.read_text(encoding="utf-8")

    private_ip_re = re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
    )
    for text_file in SKILL_DIR.rglob("*"):
        if not text_file.is_file() or text_file.suffix.lower() not in {".md", ".json", ".py", ".html", ".txt"}:
            continue
        if "__pycache__" in text_file.parts:
            continue
        content = text_file.read_text(encoding="utf-8")
        assert private_ip_re.search(content) is None, f"Private IP in {text_file.name}"
