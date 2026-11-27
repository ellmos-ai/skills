"""Tests for mermaid-lint external JSON config and self-healing loader."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def test_mermaid_lint_config_schema():
    cfg = json.loads((SKILL_ROOT / "mermaid-lint-config.json").read_text(encoding="utf-8"))
    assert cfg["skill"] == "mermaid-lint"
    assert cfg["self_healing"]["enabled"] is True
    assert cfg["mermaid"]["security_level"] == "loose"
    assert "node_modules" in cfg["scan"]["ignore_dirs"]
    assert ".md" in cfg["scan"]["file_extensions"]
    assert cfg["readback"]["retries"] == 2
    assert cfg["readback"]["channel"] == "msedge"


def test_node_syntax_and_self_healing_loader(tmp_path):
    node = shutil.which("node")
    if node is None:
        return

    for js_name in ("lint_config.mjs", "mermaid_lint.mjs", "readback.mjs", "selftest.mjs"):
        res = subprocess.run(
            [node, "--check", str(SKILL_ROOT / js_name)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert res.returncode == 0, f"node --check failed for {js_name}: {res.stderr}"

    # Verify self-healing fallback & backup on corrupt JSON using stdlib Node loader only
    shutil.copy2(SKILL_ROOT / "mermaid-lint-config.json", tmp_path / "mermaid-lint-config.json")
    corrupt_overlay = tmp_path / "config.json"
    corrupt_overlay.write_text("{corrupt json", encoding="utf-8")

    loader_uri = (SKILL_ROOT / "lint_config.mjs").as_uri()
    script = (
        f"import {{ loadMermaidLintConfig }} from {json.dumps(loader_uri)}; "
        f"const res = loadMermaidLintConfig({{ skillRoot: {json.dumps(str(tmp_path))}, repair: true }}); "
        "console.log(JSON.stringify(res));"
    )
    proc = subprocess.run(
        [node, "--input-type=module", "-e", script],
        capture_output=True,
        text=True,
        check=True,
    )
    loaded = json.loads(proc.stdout)
    assert loaded["warnings"], "expected corrupt overlay warning"
    assert loaded["healed"], "expected backup healing record"
    assert loaded["config"]["readback"]["retries"] == 2
    assert list(tmp_path.glob("config.json.corrupt.*.bak"))
