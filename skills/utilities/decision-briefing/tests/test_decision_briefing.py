"""Tests for decision-briefing config cascade, self-healing, and multi-format rendering."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def _load_renderer():
    script = SKILL_ROOT / "scripts" / "render_briefing.py"
    spec = importlib.util.spec_from_file_location("render_briefing", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_config_cascade_and_self_healing_repair(tmp_path):
    mod = _load_renderer()
    shutil.copy2(SKILL_ROOT / "briefing-config.json", tmp_path / "briefing-config.json")
    corrupt = tmp_path / "config.json"
    corrupt.write_text("{corrupt json", encoding="utf-8")

    loaded = mod.load_briefing_config(skill_root=tmp_path, repair=True)
    assert loaded["warnings"]
    assert loaded["healed"]
    assert loaded["config"]["briefing"]["batch_threshold"] == 5
    assert list(tmp_path.glob("config.json.corrupt.*.bak"))
    # Optional override config.json heals to {} rather than duplicating DEFAULT_CONFIG
    assert json.loads(corrupt.read_text(encoding="utf-8")) == {}


def test_corrupt_base_briefing_config_repairs_to_defaults(tmp_path):
    mod = _load_renderer()
    corrupt_base = tmp_path / "briefing-config.json"
    corrupt_base.write_text("{corrupt base", encoding="utf-8")

    loaded = mod.load_briefing_config(skill_root=tmp_path, repair=True)
    assert loaded["warnings"]
    assert loaded["healed"]
    assert list(tmp_path.glob("briefing-config.json.corrupt.*.bak"))
    repaired = json.loads(corrupt_base.read_text(encoding="utf-8"))
    assert repaired["skill"] == "decision-briefing"
    assert repaired["briefing"]["batch_threshold"] == 5


def test_render_md_html_txt_json_and_xss_escape():
    mod = _load_renderer()
    cfg = mod.load_briefing_config()["config"]
    data = {
        "title": "Projekt-Briefing <script>alert(1)</script>",
        "subtitle": "Kernentscheidungen",
        "generated_at": "2026-11-27",
        "items": [
            {
                "title": "Datenformat vereinheitlichen",
                "situation": "Zwei Formate laufen parallel.",
                "action": "Ich stelle auf JSON um.",
                "fallback": "Alter Parser bleibt lesend aktiv.",
                "options": [
                    {"key": "A", "label": "Auf JSON umstellen"},
                    {"key": "B", "label": "Beide behalten"},
                ],
                "recommendation": "A",
                "recommendation_reason": "Spart Wartung.",
                "ref_id": "E-REF-1",
                "source": "konzept.md",
            }
        ],
    }

    md_out = mod.render_briefing(data, fmt="md", config=cfg)
    assert "### [E01] Datenformat vereinheitlichen" in md_out
    assert "E-REF-1" in md_out

    html_out = mod.render_briefing(data, fmt="html", config=cfg)
    assert "<html" in html_out
    assert "@media print" in html_out
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html_out
    assert "<script>alert(1)</script>" not in html_out

    txt_out = mod.render_briefing(data, fmt="txt", config=cfg)
    assert "[E01] Datenformat vereinheitlichen" in txt_out

    json_out = mod.render_briefing(data, fmt="json", config=cfg)
    parsed = json.loads(json_out)
    assert parsed["item_count"] == 1


def test_cli_dry_run_writes_output_file(tmp_path):
    mod = _load_renderer()
    out_file = tmp_path / "briefing.html"
    rc = mod.main(["--dry-run", "--format", "html", "--out", str(out_file)])
    assert rc == 0
    assert out_file.is_file()
    assert "Beispiel-Entscheidung" in out_file.read_text(encoding="utf-8")
