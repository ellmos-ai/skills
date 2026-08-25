"""Regression tests for the generic, repository-agnostic privacy gate."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("repo_privacy_gate.py")
SPEC = importlib.util.spec_from_file_location("repo_privacy_gate", MODULE_PATH)
repo_privacy_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(repo_privacy_gate)


class RepoPrivacyGateEngineTests(unittest.TestCase):
    """Same regex contract as privacy_gate.py -- this is the shared source."""

    def test_rejects_concrete_windows_user_home(self) -> None:
        findings = repo_privacy_gate.concrete_home_matches(
            r"Load C:\Users\Alice\OneDrive\private.json"
        )
        self.assertEqual([r"C:\Users\Alice"], findings)

    def test_accepts_portable_windows_placeholder(self) -> None:
        findings = repo_privacy_gate.concrete_home_matches(
            r"Load C:\Users\<user>\project\config.json"
        )
        self.assertEqual([], findings)

    def test_windows_user_is_not_a_trusted_placeholder(self) -> None:
        """The 2026-08-23 lesson: a real account can be literally named
        'User', so C:\\Users\\User\\... must NOT be treated as generic."""
        findings = repo_privacy_gate.concrete_home_matches(
            r"Load C:\Users\User\OneDrive\private.json"
        )
        self.assertEqual([r"C:\Users\User"], findings)

    def test_posix_home_user_stays_a_trusted_placeholder(self) -> None:
        findings = repo_privacy_gate.concrete_home_matches(
            "Load /home/user/project/config.json"
        )
        self.assertEqual([], findings)

    def test_rejects_host_scoped_device_names(self) -> None:
        pattern = repo_privacy_gate.CONTENT_PATTERNS["host-scoped device name"]
        self.assertIsNotNone(pattern.search("WORKSTATION-ABC"))
        self.assertIsNone(pattern.search("desktop-app"))

    def test_rejects_host_scoped_local_development_roots(self) -> None:
        pattern = repo_privacy_gate.CONTENT_PATTERNS["host-scoped local development path"]
        self.assertIsNotNone(pattern.search(r"C:\_Local_DEV\repos\example"))
        self.assertIsNone(pattern.search("<local-checkout>/example"))

    def test_rejects_github_token(self) -> None:
        pattern = repo_privacy_gate.CONTENT_PATTERNS["GitHub token"]
        self.assertIsNotNone(pattern.search("ghp_" + "a" * 36))

    def test_rejects_aws_key(self) -> None:
        pattern = repo_privacy_gate.CONTENT_PATTERNS["AWS access key"]
        self.assertIsNotNone(pattern.search("AKIA" + "A" * 16))


def _git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class RepoPrivacyGateCliTests(unittest.TestCase):
    """CLI behaviour against a throwaway repo -- proves portability, the
    entire point of the extraction (T-20260825-907516036)."""

    def test_clean_repo_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _git("init", "-q", cwd=root)
            (root / "README.md").write_text("Nothing sensitive here.\n", encoding="utf-8")
            _git("add", "-A", cwd=root)
            errors = repo_privacy_gate.run_generic_gate(root)
            self.assertEqual([], errors)

    def test_leaked_host_path_is_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _git("init", "-q", cwd=root)
            (root / "notes.md").write_text(
                r"See C:\_Local_DEV\repos\example for details." + "\n", encoding="utf-8"
            )
            _git("add", "-A", cwd=root)
            errors = repo_privacy_gate.run_generic_gate(root)
            self.assertTrue(
                any("host-scoped local development path" in e for e in errors)
            )

    def test_non_git_directory_is_skipped_not_failed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                ["python", str(MODULE_PATH), "--repo", tmp],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(0, completed.returncode)
            self.assertIn("skipped", completed.stdout)

    def test_main_exits_1_on_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _git("init", "-q", cwd=root)
            (root / "notes.md").write_text(
                "AKIA" + "A" * 16 + "\n", encoding="utf-8"
            )
            _git("add", "-A", cwd=root)
            completed = subprocess.run(
                ["python", str(MODULE_PATH), "--repo", str(root)],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(1, completed.returncode)
            self.assertIn("AWS access key", completed.stdout)


if __name__ == "__main__":
    unittest.main()
