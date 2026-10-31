from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).parents[1]
SCRIPT = SKILL_DIR / "scripts" / "agy_kontext_and_workflow_loader.py"
SPEC = importlib.util.spec_from_file_location("agy_kontext_and_workflow_loader", SCRIPT)
assert SPEC and SPEC.loader
loader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(loader)


def test_prompt_standard_is_idempotent_and_replaces_an_old_footer() -> None:
    once = loader.format_prompt_standard("task", "[TITEL] x\nZWECK y\nAUFGABE z")
    twice = loader.format_prompt_standard("task", once)
    assert once == twice
    assert once.count("--- GOVERNANCE, WORKFLOW & HOOKS ---") == 1
    assert once.startswith("[TITEL] x")


def test_footer_links_the_bundled_hooks() -> None:
    footer = loader.format_letter_hooks_footer()
    for hook in (SKILL_DIR / "hooks").glob("*.md"):
        assert hook.name in footer


def test_config_example_is_valid_and_keys_match_the_defaults() -> None:
    example = json.loads((SKILL_DIR / "config.example.json").read_text(encoding="utf-8"))
    assert set(loader.DEFAULT_PATHS) <= set(example)
    assert set(example["skill_mappings"]) == set(loader.DEFAULT_SKILL_MAPPINGS)


def test_invalid_configuration_values_are_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = tmp_path / "config.json"
    monkeypatch.setattr(loader, "CONFIG_JSON", config)
    config.write_text(json.dumps({"sync_dir": ""}), encoding="utf-8")
    with pytest.raises(ValueError):
        loader._load_runtime_settings()
    config.write_text(json.dumps({"host_slot": "../other-host"}), encoding="utf-8")
    with pytest.raises(ValueError):
        loader._load_runtime_settings()


def test_local_config_stays_untracked() -> None:
    assert "config.json" in (SKILL_DIR / ".gitignore").read_text(encoding="utf-8").splitlines()
