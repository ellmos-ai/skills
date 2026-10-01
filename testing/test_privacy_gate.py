"""Regression tests for the repository privacy gate."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("privacy_gate.py")
SPEC = importlib.util.spec_from_file_location("privacy_gate", MODULE_PATH)
privacy_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(privacy_gate)


class PrivacyGateTests(unittest.TestCase):
    def test_rejects_concrete_windows_user_home(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            r"Load C:\Users\Alice\OneDrive\private.json"
        )
        self.assertEqual([r"C:\Users\Alice"], findings)

    def test_accepts_portable_windows_placeholder(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            r"Load C:\Users\<user>\project\config.json"
        )
        self.assertEqual([], findings)

    def test_rejects_concrete_posix_user_home(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            "Load /home/alice/project/config.json"
        )
        self.assertEqual(["/home/alice"], findings)

    def test_accepts_generic_posix_example(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            "Load /home/user/project/config.json"
        )
        self.assertEqual([], findings)

    def test_rejects_host_scoped_device_names(self) -> None:
        pattern = privacy_gate.CONTENT_PATTERNS["host-scoped device name"]
        self.assertIsNotNone(pattern.search("WORKSTATION-ABC"))
        self.assertIsNotNone(pattern.search("LAPTOP-123"))
        self.assertIsNone(pattern.search("desktop-app"))
        self.assertIsNone(pattern.search("Desktop-Registry-Sync"))

    def test_rejects_host_scoped_local_development_roots(self) -> None:
        pattern = privacy_gate.CONTENT_PATTERNS["host-scoped local development path"]
        self.assertIsNotNone(pattern.search(r"C:\_Local_DEV\repos\example"))
        self.assertIsNone(pattern.search("<local-checkout>/example"))

    def test_public_paveman_skill_is_host_neutral(self) -> None:
        path = MODULE_PATH.parent.parent / "skills" / "utilities" / "paveman" / "SKILL.md"
        self.assertEqual([], privacy_gate.content_findings(path))
        text = path.read_text(encoding="utf-8")
        self.assertNotIn("pip-installiert am", text)
        self.assertNotRegex(text, r"T-\d{8}-\d+")

    def test_rejects_private_skill_names(self) -> None:
        pattern = privacy_gate.CONTENT_PATTERNS["private skill name"]
        self.assertIsNotNone(pattern.search("load tom-lm"))
        self.assertIsNotNone(pattern.search("use /rechtsabteilung"))
        self.assertIsNone(pattern.search("use law-checker"))

    def test_forbids_private_and_vendor_skill_directories(self) -> None:
        forbidden = privacy_gate.FORBIDDEN_PUBLIC_SKILL_DIRECTORIES
        self.assertIn("skills/utilities/store-welle-usertest", forbidden)
        self.assertIn("skills/dev/hyperframes", forbidden)
        self.assertNotIn("skills/utilities/video-transcriber", forbidden)

    def test_gitless_cli_fails_closed_without_explicit_canonical_repo(self) -> None:
        import unittest.mock as mock

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = io.StringIO()
            with (
                mock.patch.object(privacy_gate, "REPOSITORY_ROOT", root),
                contextlib.redirect_stdout(output),
            ):
                exit_code = privacy_gate.main([])

        self.assertEqual(2, exit_code)
        self.assertIn("failed closed", output.getvalue())
        self.assertIn("--canonical-repo", output.getvalue())

    def test_gitless_cli_delegates_to_explicit_canonical_repo(self) -> None:
        import unittest.mock as mock

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projection = root / "projection"
            canonical = root / "canonical"
            projection.mkdir()
            (canonical / "testing").mkdir(parents=True)
            subprocess.run(
                ["git", "init", "-q"],
                cwd=canonical,
                check=True,
                capture_output=True,
            )
            (canonical / "testing" / "privacy_gate.py").write_text(
                "print('canonical privacy gate ran')\n",
                encoding="utf-8",
            )

            output = io.StringIO()
            with (
                mock.patch.object(privacy_gate, "REPOSITORY_ROOT", projection),
                contextlib.redirect_stdout(output),
            ):
                exit_code = privacy_gate.main(
                    ["--canonical-repo", str(canonical)]
                )

        self.assertEqual(0, exit_code)
        self.assertIn("canonical privacy gate ran", output.getvalue())

    def test_gitless_cli_rejects_non_git_canonical_repo(self) -> None:
        import unittest.mock as mock

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projection = root / "projection"
            candidate = root / "not-a-repository"
            projection.mkdir()
            candidate.mkdir()
            output = io.StringIO()
            with (
                mock.patch.object(privacy_gate, "REPOSITORY_ROOT", projection),
                contextlib.redirect_stdout(output),
            ):
                exit_code = privacy_gate.main(
                    ["--canonical-repo", str(candidate)]
                )

        self.assertEqual(2, exit_code)
        self.assertIn("not an exact Git worktree root", output.getvalue())

    def test_gitless_cli_preserves_canonical_failure_and_stderr(self) -> None:
        import unittest.mock as mock

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projection = root / "projection"
            canonical = root / "canonical"
            projection.mkdir()
            (canonical / "testing").mkdir(parents=True)
            subprocess.run(
                ["git", "init", "-q"],
                cwd=canonical,
                check=True,
                capture_output=True,
            )
            (canonical / "testing" / "privacy_gate.py").write_text(
                "import sys\n"
                "print('canonical privacy gate blocked', file=sys.stderr)\n"
                "raise SystemExit(7)\n",
                encoding="utf-8",
            )

            errors = io.StringIO()
            with (
                mock.patch.object(privacy_gate, "REPOSITORY_ROOT", projection),
                contextlib.redirect_stderr(errors),
            ):
                exit_code = privacy_gate.main(
                    ["--canonical-repo", str(canonical)]
                )

        self.assertEqual(7, exit_code)
        self.assertIn("canonical privacy gate blocked", errors.getvalue())

    def test_gate_has_no_host_specific_canonical_repo_default(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn(r"C:\_Local_DEV\repos\skills", source)


class ThirdPartyGateTests(unittest.TestCase):
    """Folder and flag must agree, and foreign material needs a usable licence.

    Every case here corresponds to a way the two switches can contradict each
    other. Two switches that nobody compares are what once left a private skill
    readable on GitHub -- so each direction gets its own test.
    """

    GOOD = (
        "name: demo-foreign\n"
        "description: A vendored foreign skill.\n"
        "third_party: true\n"
        "license: MIT\n"
        "upstream: https://github.com/someone/repo\n"
    )

    def setUp(self) -> None:
        self.root = privacy_gate.REPOSITORY_ROOT
        self.areal = self.root / "skills/third-party/zz-test-foreign"
        self.outside = self.root / "skills/utilities/zz-test-outside"
        self.addCleanup(self._cleanup)

    def _cleanup(self) -> None:
        import shutil

        for folder in (self.areal, self.outside):
            shutil.rmtree(folder, ignore_errors=True)

    def _write(self, folder: Path, frontmatter: str, licence_file: bool = True) -> str:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(
            f"---\n{frontmatter}---\n\n# Demo\n", encoding="utf-8"
        )
        licence = folder / "LICENSE"
        if licence_file:
            licence.write_text("MIT License\n", encoding="utf-8")
        elif licence.exists():
            licence.unlink()
        return (folder / "SKILL.md").relative_to(self.root).as_posix()

    def test_correct_foreign_skill_passes(self) -> None:
        relative = self._write(self.areal, self.GOOD)
        self.assertEqual([], privacy_gate.third_party_errors({relative}))

    def test_areal_without_flag_is_rejected(self) -> None:
        relative = self._write(self.areal, self.GOOD.replace("third_party: true\n", ""))
        self.assertTrue(privacy_gate.third_party_errors({relative}))

    def test_flag_outside_areal_is_rejected(self) -> None:
        relative = self._write(self.outside, self.GOOD)
        self.assertTrue(privacy_gate.third_party_errors({relative}))

    def test_foreign_skill_without_licence_is_rejected(self) -> None:
        relative = self._write(self.areal, self.GOOD.replace("license: MIT\n", ""))
        self.assertTrue(privacy_gate.third_party_errors({relative}))

    def test_non_commercial_licence_is_rejected(self) -> None:
        relative = self._write(self.areal, self.GOOD.replace("MIT", "CC-BY-NC-4.0"))
        self.assertTrue(privacy_gate.third_party_errors({relative}))

    def test_missing_upstream_licence_file_is_rejected(self) -> None:
        relative = self._write(self.areal, self.GOOD, licence_file=False)
        self.assertTrue(privacy_gate.third_party_errors({relative}))

    def test_missing_upstream_pointer_is_rejected(self) -> None:
        relative = self._write(
            self.areal, self.GOOD.replace("upstream: https://github.com/someone/repo\n", "")
        )
        self.assertTrue(privacy_gate.third_party_errors({relative}))

    def test_untracked_foreign_skill_is_not_checked(self) -> None:
        # Nothing to enforce while a skill is not tracked -- it is not published.
        self._write(self.areal, self.GOOD.replace("license: MIT\n", ""))
        self.assertEqual([], privacy_gate.third_party_errors(set()))

    def test_areal_skill_passes_the_visibility_gate_too(self) -> None:
        """The two gates must not contradict each other over the same skill.

        Regression for a bug found on 2026-08-23: the third-party contract omits
        ``visibility`` on purpose, but the visibility gate defaults a missing
        field to private -- so the first real foreign skill was tracked *and*
        counted as private, and would have been rejected by the very gate that
        was supposed to let it through. Checking only ``third_party_errors()``
        did not reveal this; both gates have to see the same skill.
        """
        relative = self._write(self.areal, self.GOOD)
        self.assertEqual([], privacy_gate.third_party_errors({relative}))
        offending = [
            error for error in privacy_gate.visibility_consistency_errors({relative})
            if error.startswith(relative)
        ]
        self.assertEqual([], offending)
        self.assertEqual("public", privacy_gate.declared_visibility(
            self.areal / "SKILL.md", relative))

    def test_explicit_visibility_still_wins_inside_the_areal(self) -> None:
        relative = self._write(
            self.areal, self.GOOD + "visibility: private-only\n"
        )
        self.assertEqual("private-only", privacy_gate.declared_visibility(
            self.areal / "SKILL.md", relative))

    def test_licence_allow_list_separates_permissive_and_copyleft(self) -> None:
        from build_public_registry import (
            COPYLEFT_LICENSES,
            PERMISSIVE_LICENSES,
            REDISTRIBUTABLE_LICENSES,
        )

        self.assertIn("MIT", PERMISSIVE_LICENSES)
        self.assertIn("GPL-3.0-or-later", COPYLEFT_LICENSES)
        self.assertEqual(REDISTRIBUTABLE_LICENSES, PERMISSIVE_LICENSES | COPYLEFT_LICENSES)
        # Non-commercial clauses stay out on purpose: "non-commercial" is not
        # cleanly separable here, and an unappliable rule is worse than none.
        self.assertNotIn("CC-BY-NC-4.0", REDISTRIBUTABLE_LICENSES)


class DependencyGateTests(unittest.TestCase):
    """T-20260927-285118525: a declared dependency the repo cannot verify is
    the same "looks portable, isn't" leak as a placeholder file:// link --
    just hidden in the frontmatter instead of the body. V1 is WARN_ONLY."""

    def setUp(self) -> None:
        self.root = privacy_gate.REPOSITORY_ROOT
        self.skill_dir = self.root / "skills/utilities/zz-test-deps"
        self.other_skill_dir = self.root / "skills/utilities/zz-test-deps-protocol"
        self.addCleanup(self._cleanup)

    def _cleanup(self) -> None:
        import shutil

        for folder in (self.skill_dir, self.other_skill_dir):
            shutil.rmtree(folder, ignore_errors=True)

    def _write(self, folder: Path, frontmatter_deps_line: str) -> str:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(
            "---\nname: zz-test\ndescription: test\n"
            f"{frontmatter_deps_line}\n---\n\n# Demo\n",
            encoding="utf-8",
        )
        return (folder / "SKILL.md").relative_to(self.root).as_posix()

    def test_missing_own_script_warns(self) -> None:
        relative = self._write(
            self.skill_dir, "dependencies:\n  python: [ghost_script.py]"
        )
        warnings = privacy_gate.dependency_warnings({relative})
        self.assertTrue(any("ghost_script.py" in w for w in warnings))

    def test_shipped_own_script_is_not_flagged(self) -> None:
        relative = self._write(
            self.skill_dir, "dependencies:\n  python: [present_script.py]"
        )
        (self.skill_dir / "present_script.py").write_text("", encoding="utf-8")
        warnings = privacy_gate.dependency_warnings(
            {relative, "skills/utilities/zz-test-deps/present_script.py"}
        )
        self.assertEqual([], warnings)

    def test_stdlib_module_is_not_flagged(self) -> None:
        relative = self._write(
            self.skill_dir, "dependencies:\n  python: [json, urllib.request]"
        )
        self.assertEqual([], privacy_gate.dependency_warnings({relative}))

    def test_bare_external_tool_is_not_flagged(self) -> None:
        relative = self._write(self.skill_dir, "dependencies:\n  tools: [git, gh]")
        self.assertEqual([], privacy_gate.dependency_warnings({relative}))

    def test_flow_style_dict_form_is_declared_external_and_skipped(self) -> None:
        relative = self._write(
            self.skill_dir,
            "dependencies: {'python': [{'name': 'feedparser', 'optional': True, "
            "'install': 'pip install feedparser'}]}",
        )
        self.assertEqual([], privacy_gate.dependency_warnings({relative}))

    def test_private_protocol_dependency_warns(self) -> None:
        protocol_relative = self._write(
            self.other_skill_dir, "visibility: private-only"
        )
        relative = self._write(
            self.skill_dir, "dependencies:\n  protocols: [zz-test-deps-protocol]"
        )
        warnings = privacy_gate.dependency_warnings({relative, protocol_relative})
        self.assertTrue(any("zz-test-deps-protocol" in w for w in warnings))

    def test_unresolvable_protocol_name_is_not_a_skill_ref(self) -> None:
        """A protocols entry not matching any skill directory is an external
        protocol description (e.g. "ICS / iCalendar"), not a broken link."""
        relative = self._write(
            self.skill_dir, "dependencies:\n  protocols: [some-external-protocol]"
        )
        self.assertEqual([], privacy_gate.dependency_warnings({relative}))

    def test_dependency_warnings_never_block(self) -> None:
        """V1 is WARN_ONLY: run_gate()'s errors must stay unaffected."""
        relative = self._write(
            self.skill_dir, "dependencies:\n  python: [ghost_script.py]"
        )
        self.assertTrue(privacy_gate.dependency_warnings({relative}))
        self.assertNotIn("ghost_script.py", "\n".join(privacy_gate.run_gate()))


if __name__ == "__main__":
    unittest.main()
