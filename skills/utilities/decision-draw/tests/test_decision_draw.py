"""Unit tests for decision-draw external config, self-healing, templates, and form tooling."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, rel_path: str):
    path = SKILL_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_draw_config_loading_override_and_self_healing(tmp_path):
    cfg_mod = _load_module("draw_config", "scripts/draw_config.py")
    shutil.copy2(SKILL_ROOT / "draw-config.json", tmp_path / "draw-config.json")

    corrupt_override = tmp_path / "config.json"
    corrupt_override.write_text("{broken json", encoding="utf-8")

    loaded = cfg_mod.load_draw_config(skill_root=tmp_path, repair=True)
    assert loaded["warnings"]
    assert loaded["healed"]
    assert list(tmp_path.glob("config.json.corrupt.*.bak"))
    assert loaded["config"]["viewer"]["bg"] == "#eef2f7"
    assert loaded["config"]["form"]["limits"]["kontext"] == 250
    assert loaded["config"]["server"]["max_files"] == 4

    # Valid override merges cleanly without losing sibling defaults
    corrupt_override.write_text(json.dumps({"viewer": {"confirmation_limit": 5}}), encoding="utf-8")
    overridden = cfg_mod.load_draw_config(skill_root=tmp_path, repair=False)
    assert overridden["warnings"] == []
    assert overridden["config"]["viewer"]["confirmation_limit"] == 5
    assert overridden["config"]["viewer"]["bg"] == "#eef2f7"


def test_templates_exist_and_render_short_and_detailed():
    cfg_mod = _load_module("draw_config", "scripts/draw_config.py")
    short = cfg_mod.render_markdown_template(
        "short_md",
        {
            "intro_line": "Zwei offene Entscheidungen:",
            "items_numbered": "1. **Testpunkt:** Umsetzung erfolgt direkt.",
            "item_count": "zwei",
        },
    )
    assert "Zwei offene Entscheidungen:" in short
    assert "**Passt so**" in short

    detailed = cfg_mod.render_markdown_template(
        "detailed_md",
        {
            "title": "Systemverbund",
            "bundle_items": "- **A:** Kurztext",
            "concept": "Klarer Zielzustand.",
            "interaction": "End-to-End Ablauf.",
            "implementation": "Parallele Stränge.",
            "boundaries": "Keine Außenwirkung.",
            "acceptance": "Passt so.",
            "return_transfer": "Nur über Phase 4.",
            "appendix_table": "| Titel | ID |\n|---|---|\n| A | A1 |",
        },
    )
    assert "# DECISION-DRAW: Systemverbund" in detailed
    assert "## 8. Anhang: Technische Referenztabelle" in detailed


def test_build_form_and_serve_form_consume_draw_config():
    bf = _load_module("build_form", "scripts/formular/build_form.py")
    sf = _load_module("serve_form", "scripts/formular/serve_form.py")

    example = json.loads((SKILL_ROOT / "scripts" / "formular" / "example_form.json").read_text(encoding="utf-8"))
    if importlib.util.find_spec("markdown") is None:
        for group in example.get("buendel", []):
            for item in group.get("posten", []):
                item.pop("details_markdown", None)
    page, digest, items = bf.build(example, SKILL_ROOT / "scripts" / "formular")
    assert len(items) == 3
    assert len(digest) == 64
    assert "<html" in page
    assert bf.LIMITS["kontext"] == 250
    assert sf.MAX_FILES == 4
    assert sf.IDLE_SECONDS == 300
