"""Tests for agent-config-sync scripts/sync.py.

All tests use tmp_path fixtures -- no real agent configs are read or written.
The AGENT_CONFIG_SYNC_TEST_ROOT env var is set per test to block accidental
real path resolution when --root is not passed.

Run:
    PYTHONIOENCODING=utf-8 python -m pytest skills/infrastructure/agent-config-sync/tests/ -v
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

# Make scripts/ importable from tests/
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sync  # noqa: E402 -- must come after sys.path manipulation


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture()
def fixture_root(tmp_path: Path) -> Path:
    """Create a minimal fixture tree mirroring a real multi-agent setup."""
    home = tmp_path / "home"
    appdata = tmp_path / "appdata"

    # Claude Code profile (JSON, source)
    claude_profiles = home / ".claude" / "profiles"
    claude_profiles.mkdir(parents=True)
    (claude_profiles / "shared.json").write_text(
        json.dumps({"mcpServers": {
            "test-server": {"command": "node", "args": ["server.js"]}
        }}, indent=2),
        encoding="utf-8",
    )

    # Claude Desktop target (JSON)
    claude_desktop = appdata / "Claude"
    claude_desktop.mkdir(parents=True)
    (claude_desktop / "claude_desktop_config.json").write_text(
        json.dumps({"mcpServers": {}, "theme": "dark"}, indent=2),
        encoding="utf-8",
    )

    # Codex CLI target (TOML)
    codex_dir = home / ".codex"
    codex_dir.mkdir(parents=True)
    (codex_dir / "config.toml").write_text(
        '[other_setting]\nvalue = "keep-me"\n',
        encoding="utf-8",
    )

    return tmp_path


@pytest.fixture()
def skill_dir(tmp_path: Path, fixture_root: Path) -> Path:
    """Create a minimal skill_dir with config.json + registry.json."""
    sd = tmp_path / "skill"
    sd.mkdir()
    scripts_dir = sd / "scripts"
    scripts_dir.mkdir()

    # Minimal config.json
    config = {
        "providers": {
            "claude-code": {
                "display_name": "Claude Code",
                "kind": "cli",
                "mcp": {"path": "<HOME>/.claude/profiles/shared.json",
                        "format": "json", "key": "mcpServers", "merge": "file"},
                "skills": {"path": "<HOME>/.claude/skills/", "kind": "dir"},
            },
            "claude-desktop": {
                "display_name": "Claude Desktop",
                "kind": "app",
                "mcp": {"path": "<APPDATA>/Claude/claude_desktop_config.json",
                        "format": "json", "key": "mcpServers", "merge": "block-replace"},
                "skills": {"path": None, "kind": "redirect"},
            },
            "codex-cli": {
                "display_name": "Codex CLI",
                "kind": "cli",
                "mcp": {"path": "<HOME>/.codex/config.toml",
                        "format": "toml", "key": "mcp_servers", "merge": "block-replace"},
                "skills": {"path": "<HOME>/.codex/", "kind": "dir"},
            },
        }
    }
    (sd / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    # Minimal registry.json
    registry = {
        "host": "TEST-HOST",
        "tools": {
            "claude-code": {"installed": True, "role": "hub"},
            "claude-desktop": {"installed": True, "role": "member"},
            "codex-cli": {"installed": True, "role": "leaf"},
        },
        "relations": [
            {
                "name": "claude-pair",
                "members": ["claude-code", "claude-desktop"],
                "mode": "pull",
                "source": "claude-code",
                "scope": "mcp",
                "notes": "Legacy mcp-config-sync case",
            },
            {
                "name": "cli-mcp-fanout",
                "members": ["claude-code", "codex-cli"],
                "mode": "push",
                "source": "claude-code",
                "scope": "mcp",
                "notes": "Push MCP to Codex TOML",
            },
        ],
    }
    (sd / "registry.json").write_text(json.dumps(registry, indent=2), encoding="utf-8")

    return sd


# ── Placeholder resolution ────────────────────────────────────────────────────


def test_resolve_placeholders_test_root(tmp_path: Path) -> None:
    result = sync._resolve_placeholders("<HOME>/.claude/profiles/x.json", test_root=tmp_path)
    assert str(tmp_path / "home") in result
    assert "<HOME>" not in result


def test_resolve_placeholders_blocks_without_root(monkeypatch) -> None:
    monkeypatch.setenv(sync._TEST_ROOT_ENV, "1")
    with pytest.raises(RuntimeError, match="blocked"):
        sync._resolve_placeholders("<HOME>/.claude/test.json", test_root=None)


def test_resolve_placeholders_passthrough_none() -> None:
    assert sync._resolve_placeholders(None) is None


# ── JSON block-replace ────────────────────────────────────────────────────────


def test_json_block_replace_preserves_other_keys() -> None:
    original = json.dumps({"mcpServers": {}, "theme": "dark"}, indent=2)
    new_block = {"my-server": {"command": "python", "args": ["srv.py"]}}
    result = sync._json_block_replace(original, "mcpServers", new_block)
    parsed = json.loads(result)
    assert parsed["theme"] == "dark"
    assert parsed["mcpServers"] == new_block


def test_json_block_replace_creates_key_if_missing() -> None:
    original = json.dumps({"theme": "light"}, indent=2)
    result = sync._json_block_replace(original, "mcpServers", {"srv": {}})
    assert json.loads(result)["mcpServers"] == {"srv": {}}
    assert json.loads(result)["theme"] == "light"


# ── TOML MCP block-replace ────────────────────────────────────────────────────


def test_toml_mcp_block_replace_adds_servers() -> None:
    original = '[other_setting]\nvalue = "keep-me"\n'
    mcp = {"test-srv": {"command": "node", "args": ["s.js"]}}
    result = sync._toml_mcp_block_replace(original, mcp)
    assert "[mcp_servers.test-srv]" in result
    assert 'command = "node"' in result
    assert "keep-me" in result


def test_toml_mcp_block_replace_removes_old_servers() -> None:
    original = '[mcp_servers.old-srv]\ncommand = "old"\n\n[keep]\nval = 1\n'
    mcp = {"new-srv": {"command": "new"}}
    result = sync._toml_mcp_block_replace(original, mcp)
    assert "old-srv" not in result
    assert "[mcp_servers.new-srv]" in result


def test_toml_mcp_block_replace_empty_servers_cleans() -> None:
    original = '[mcp_servers.x]\ncommand = "x"\n'
    result = sync._toml_mcp_block_replace(original, {})
    assert "mcp_servers" not in result


# ── --apply with JSON target ──────────────────────────────────────────────────


def test_apply_json_mcp_writes_and_verifies(tmp_path: Path) -> None:
    target = tmp_path / "claude_desktop_config.json"
    target.write_text(json.dumps({"mcpServers": {}, "theme": "dark"}, indent=2), encoding="utf-8")

    mcp_data = {"my-srv": {"command": "node", "args": ["x.js"]}}
    ok, msg = sync._apply_json_mcp(target, "mcpServers", mcp_data)

    assert ok, msg
    parsed = json.loads(target.read_text(encoding="utf-8"))
    assert parsed["mcpServers"] == mcp_data
    assert parsed["theme"] == "dark"
    # Backup created
    backups = list(tmp_path.glob("*.bak.*"))
    assert len(backups) == 1


def test_apply_json_mcp_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "new_config.json"
    ok, msg = sync._apply_json_mcp(target, "mcpServers", {"s": {}})
    assert ok, msg
    assert target.exists()


# ── --apply with TOML target ──────────────────────────────────────────────────


def test_apply_toml_mcp_writes_and_verifies(tmp_path: Path) -> None:
    target = tmp_path / "config.toml"
    target.write_text('[other]\nval = "x"\n', encoding="utf-8")

    mcp = {"file-server": {"command": "python", "args": ["fs.py"]}}
    ok, msg = sync._apply_toml_mcp(target, mcp)

    assert ok, msg
    text = target.read_text(encoding="utf-8")
    assert "[mcp_servers.file-server]" in text
    assert "val" in text  # other content preserved


# ── --status command ──────────────────────────────────────────────────────────


def test_cmd_status_writes_cache(skill_dir: Path, fixture_root: Path,
                                 monkeypatch, capsys) -> None:
    monkeypatch.chdir(skill_dir)
    # Redirect SKILL_DIR for the module
    original_skill_dir = sync.SKILL_DIR
    monkeypatch.setattr(sync, "SKILL_DIR", skill_dir)

    args = type("Args", (), {"root": str(fixture_root), "yes": False, "dry_run": False})()
    ret = sync.cmd_status(args)
    assert ret == 0

    cache_file = skill_dir / "cache.json"
    assert cache_file.exists()
    cache = json.loads(cache_file.read_text(encoding="utf-8"))
    assert "providers" in cache
    assert "claude-code" in cache["providers"]

    monkeypatch.setattr(sync, "SKILL_DIR", original_skill_dir)


# ── --plan command ────────────────────────────────────────────────────────────


def test_cmd_plan_prints_relations(skill_dir: Path, fixture_root: Path,
                                   monkeypatch, capsys) -> None:
    monkeypatch.setattr(sync, "SKILL_DIR", skill_dir)
    args = type("Args", (), {"root": str(fixture_root), "yes": False, "dry_run": False})()
    ret = sync.cmd_plan(args)
    assert ret == 0
    out = capsys.readouterr().out
    assert "claude-pair" in out
    assert "cli-mcp-fanout" in out
    assert "ControlCenter" in out  # Claude delegation message


# ── --apply guard without --yes ──────────────────────────────────────────────


def test_apply_requires_yes(capsys) -> None:
    args = type("Args", (), {"yes": False, "root": None, "dry_run": False})()
    ret = sync.cmd_apply(args)
    assert ret == 2
    err = capsys.readouterr().err
    assert "--yes" in err


# ── --apply full integration (fixtures only) ──────────────────────────────────


def test_apply_full_integration(skill_dir: Path, fixture_root: Path, monkeypatch) -> None:
    """Full apply run: claude-pair (Claude->Desktop skipped via ControlCenter),
    cli-mcp-fanout writes TOML for Codex."""
    monkeypatch.setattr(sync, "SKILL_DIR", skill_dir)
    # Build cache first
    args_status = type("Args", (), {"root": str(fixture_root), "yes": False, "dry_run": False})()
    sync.cmd_status(args_status)

    args = type("Args", (), {"yes": True, "root": str(fixture_root), "dry_run": False})()
    ret = sync.cmd_apply(args)
    # Codex TOML should have been written
    toml_path = fixture_root / "home" / ".codex" / "config.toml"
    toml_text = toml_path.read_text(encoding="utf-8")
    assert "[mcp_servers.test-server]" in toml_text
    assert "keep-me" in toml_text  # other content preserved
    assert ret == 0
