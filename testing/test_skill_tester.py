"""Regression tests for the static skill gate."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("skill_tester.py")
SPEC = importlib.util.spec_from_file_location("skill_tester", MODULE_PATH)
skill_tester = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(skill_tester)


VALID_SKILL = """\
---
name: example-skill
version: 1.0.0
type: skill
author: Example Maintainer
created: 2026-07-15
updated: 2026-07-15
description: >
  A portable example skill used only to exercise the static validation gate.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [example, test]
language: en
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
---

# Example skill

## Usage

Use this fixture to verify that the complete static gate accepts a well-formed,
standalone skill. The body is deliberately long enough to satisfy the content
checks and contains no runtime-specific paths, imports, services, or personal
data. It therefore represents the smallest realistic public skill fixture.

## Workflow

1. Read the request.
2. Apply the documented process.
3. Report the result and any remaining limitation.

## Changelog

### 1.0.0 (2026-07-15)

- Initial test fixture.
"""


class StaticGateTests(unittest.TestCase):
    def make_skill(self, root: Path, text: str = VALID_SKILL) -> Path:
        skill_dir = root / "skills" / "utilities" / "example-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")
        return skill_dir

    def test_complete_frontmatter_has_no_gate_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))

            self.assertEqual([], skill_tester.frontmatter_gate_errors(skill_dir))

    def test_missing_updated_field_is_a_gate_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            text = VALID_SKILL.replace("updated: 2026-07-15\n", "")
            skill_dir = self.make_skill(Path(tmp), text)

            errors = skill_tester.frontmatter_gate_errors(skill_dir)

            self.assertIn("Pflichtfeld fehlt: updated", errors)

    def test_ci_batch_returns_failure_for_invalid_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            text = VALID_SKILL.replace("standalone: true\n", "")
            skill_dir = self.make_skill(Path(tmp), text)

            passed = skill_tester.cmd_batch(
                profile_name="STATIC",
                test_type="static",
                ci_mode=True,
                identifiers=[str(skill_dir / "SKILL.md")],
            )

            self.assertFalse(passed)

    def test_ci_batch_accepts_valid_changed_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))

            passed = skill_tester.cmd_batch(
                profile_name="STATIC",
                test_type="static",
                ci_mode=True,
                identifiers=[str(skill_dir / "SKILL.md")],
            )

            self.assertTrue(passed)

    def test_cli_returns_one_for_invalid_changed_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            text = VALID_SKILL.replace("updated: 2026-07-15\n", "")
            skill_dir = self.make_skill(Path(tmp), text)

            exit_code = skill_tester.main([
                "batch",
                "--type",
                "static",
                "--ci",
                str(skill_dir / "SKILL.md"),
            ])

            self.assertEqual(1, exit_code)

    def test_cli_returns_zero_for_valid_changed_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.make_skill(Path(tmp))

            exit_code = skill_tester.main([
                "batch",
                "--type",
                "static",
                "--ci",
                str(skill_dir / "SKILL.md"),
            ])

            self.assertEqual(0, exit_code)


if __name__ == "__main__":
    unittest.main()
