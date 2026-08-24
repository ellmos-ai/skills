from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "inventory_skills.py"
SPEC = importlib.util.spec_from_file_location("inventory_skills", SCRIPT)
assert SPEC and SPEC.loader
inventory_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory_skills)


def test_normalize_dependencies_accepts_legacy_python_repr() -> None:
    raw = "{'tools': ['git'], 'services': [], 'protocols': [], 'python': []}"

    assert inventory_skills.normalize_dependencies(raw) == {
        "tools": ["git"],
        "services": [],
        "protocols": [],
        "python": [],
    }


def test_normalize_dependencies_accepts_json_and_scalar_values() -> None:
    raw = '{"tools": "git", "services": ["web"], "protocols": null}'

    assert inventory_skills.normalize_dependencies(raw) == {
        "tools": ["git"],
        "services": ["web"],
        "protocols": [],
        "python": [],
    }


def test_inventory_root_degrades_malformed_dependencies_without_aborting(tmp_path: Path) -> None:
    skill_dir = tmp_path / "legacy-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: legacy-skill\n"
        "dependencies: definitely-not-a-mapping\n"
        "---\n"
        "# Legacy skill\n",
        encoding="utf-8",
    )

    result = inventory_skills.inventory_root(tmp_path)

    assert len(result) == 1
    assert result[0]["dependencies"] == {
        "tools": [],
        "services": [],
        "protocols": [],
        "python": [],
    }
