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

    def test_forbidden_internal_filenames_are_found(self) -> None:
        """T-20260926-510472849: agent-internal files must never be tracked,
        even under a name that isn't the exact match GITHUB-POLICY.md lists."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _git("init", "-q", cwd=root)
            (root / "BEFUNDE.md").write_text("intern\n", encoding="utf-8")
            (root / "MARKETING-LOG.txt").write_text("intern\n", encoding="utf-8")
            (root / "STORE_CONTRACT.md").write_text("intern\n", encoding="utf-8")
            (root / "_WARTUNG" / "msix_staging").mkdir(parents=True)
            (root / "_WARTUNG" / "msix_staging" / "AppxManifest.xml").write_text("x\n", encoding="utf-8")
            (root / "_WARTUNG" / "generate_store_screenshots.py").write_text("x\n", encoding="utf-8")
            _git("add", "-A", cwd=root)
            errors = repo_privacy_gate.run_generic_gate(root)
            joined = "\n".join(errors)
            self.assertIn("BEFUNDE.md: agent findings log", joined)
            self.assertIn("STORE_CONTRACT.md: release/store internal state doc", joined)
            self.assertIn("_WARTUNG/msix_staging/AppxManifest.xml: build/packaging staging directory", joined)
            self.assertNotIn("_WARTUNG/generate_store_screenshots.py", joined)  # maintenance script, not staged output
            # MARKETING-LOG.txt is WARN_ONLY (team-lead correction 2026-09-26): several
            # repos wire it in deliberately (pyproject.toml project.url, a dedicated
            # test) -- it must never fail CI, only surface as a hint.
            self.assertNotIn("MARKETING-LOG.txt", joined)
            warnings = repo_privacy_gate.warning_findings(root)
            self.assertTrue(
                any("MARKETING-LOG.txt: agent marketing/status log" in w for w in warnings)
            )

    def test_legitimate_contract_docs_are_not_flagged(self) -> None:
        """CI_CONTRACT.md / PRODUCT_BOUNDARIES.md document behavior for
        readers, not agent state -- they must stay unflagged (see the
        FORBIDDEN_INTERNAL_FILENAME_PATTERNS docstring note)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _git("init", "-q", cwd=root)
            (root / "CI_CONTRACT.md").write_text("The CI workflow ...\n", encoding="utf-8")
            (root / "PRODUCT_BOUNDARIES.md").write_text("Product A vs B ...\n", encoding="utf-8")
            _git("add", "-A", cwd=root)
            errors = repo_privacy_gate.run_generic_gate(root)
            self.assertEqual([], errors)

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


class SelfScanHintTests(unittest.TestCase):
    """Der Hinweis darf NUR dort erscheinen, wo er stimmt -- und er darf das
    strikte Verhalten nirgends aufweichen. Zweimal wurde die Ausgabe dieses
    Moduls auf dem eigenen Repo als Defekt gemeldet ("das Gate blockiert sich
    selbst"); der Hinweis beantwortet das an der Stelle, an der die Frage
    entsteht."""

    def _repo_with_leak(self, root: Path) -> None:
        _git("init", "-q", cwd=root)
        (root / "notes.md").write_text(
            r"See C:\_Local_DEV\repos\example for details." + "\n",
            encoding="utf-8",
        )
        _git("add", "-A", cwd=root)

    def _run(self, root: Path) -> "subprocess.CompletedProcess[str]":
        return subprocess.run(
            ["python", str(MODULE_PATH), "--repo", str(root)],
            capture_output=True, text=True, encoding="utf-8",
        )

    def test_foreign_repo_stays_strict_and_silent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._repo_with_leak(root)
            completed = self._run(root)
            self.assertEqual(1, completed.returncode)
            self.assertNotIn("authoritative", completed.stdout)

    def test_repo_with_own_gate_gets_the_hint_but_same_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._repo_with_leak(root)
            (root / "testing").mkdir()
            (root / "testing" / "privacy_gate.py").write_text("", encoding="utf-8")
            _git("add", "-A", cwd=root)
            completed = self._run(root)
            # Exit code unveraendert: der Hinweis erklaert, er entschuldigt nicht.
            self.assertEqual(1, completed.returncode)
            self.assertIn("privacy_gate.py is authoritative", completed.stdout)


if __name__ == "__main__":
    unittest.main()
