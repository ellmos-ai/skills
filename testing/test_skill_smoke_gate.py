#!/usr/bin/env python3
"""Unit and regression tests for skill_smoke_gate.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from testing.skill_smoke_gate import check_skill_smoke, main

SKILL_TEMPLATE = """\
---
name: {name}
version: 1.0.0
description: Test skill fixture for smoke test gate.
category: utilities
tags: [test]
standalone: true
visibility: public
---

# {name}

## Description
Fixture text.
"""


class SkillSmokeGateTests(unittest.TestCase):
    def make_skill(self, base_dir: Path, name: str = "smoke-fixture") -> Path:
        skill_dir = base_dir / "skills" / "utilities" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(SKILL_TEMPLATE.format(name=name), encoding="utf-8")
        return skill_dir

    def test_doc_only_skill_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))
            res = check_skill_smoke(skill_dir)
            self.assertEqual("PASS", res["status"])
            self.assertFalse(res["has_tests"])
            self.assertEqual(0, res["py_count"])

    def test_skill_with_valid_test_smoke_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))
            tests_dir = skill_dir / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_smoke.py").write_text("def test_smoke(): assert True\n", encoding="utf-8")

            res = check_skill_smoke(skill_dir)
            self.assertEqual("PASS", res["status"])
            self.assertTrue(res["has_tests"])
            self.assertTrue(any("test_smoke.py erfolgreich bestanden" in f for f in res["findings"]))

    def test_skill_with_failing_test_smoke_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))
            tests_dir = skill_dir / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_smoke.py").write_text("def test_smoke(): assert False\n", encoding="utf-8")

            res = check_skill_smoke(skill_dir)
            self.assertEqual("FAIL", res["status"])
            self.assertTrue(any("test_smoke.py fehlgeschlagen" in f for f in res["findings"]))

    def test_skill_with_syntax_error_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "broken.py").write_text("def bad syntax (\n", encoding="utf-8")

            res = check_skill_smoke(skill_dir)
            self.assertEqual("FAIL", res["status"])
            self.assertTrue(any("Syntaxfehler" in f for f in res["findings"]))

    def test_skill_with_valid_cli_script_warns_when_untested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))
            script = skill_dir / "cli_tool.py"
            script.write_text(
                'import sys, argparse\n'
                'if __name__ == "__main__":\n'
                '    parser = argparse.ArgumentParser()\n'
                '    parser.parse_args()\n',
                encoding="utf-8",
            )

            res = check_skill_smoke(skill_dir)
            self.assertEqual("WARN", res["status"])
            self.assertFalse(res["has_tests"])
            self.assertTrue(any("--help erfolgreich" in f for f in res["findings"]))

    def test_warn_only_mode_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp)
            skill_dir = self.make_skill(repo_dir, "warn-fixture")
            (skill_dir / "script.py").write_text("print('hello')\n", encoding="utf-8")

            # In warn-only mode (default), exit code must be 0
            code = main(["--repo", str(repo_dir)])
            self.assertEqual(0, code)

    def test_strict_mode_exits_one_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp)
            skill_dir = self.make_skill(repo_dir, "broken-fixture")
            (skill_dir / "broken.py").write_text("def broken syntax (\n", encoding="utf-8")

            code = main(["--repo", str(repo_dir), "--strict"])
            self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()
