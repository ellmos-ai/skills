from __future__ import annotations

import unittest

from testing.changed_skill_gate import (
    is_canonical_skill_path,
    normalized_without_banner,
)


class ChangedSkillGateTests(unittest.TestCase):
    def test_recognizes_only_canonical_skill_roots(self) -> None:
        self.assertTrue(is_canonical_skill_path("skills/dev/example/SKILL.md"))
        self.assertFalse(is_canonical_skill_path("skills/dev/example/SKILL.en.md"))
        self.assertFalse(is_canonical_skill_path("skills/dev/example/en/SKILL.md"))

    def test_banner_insertion_does_not_change_normalized_content(self) -> None:
        before = "---\nname: example\n---\n\n# Example\n"
        after = (
            "---\nname: example\n---\n\n"
            '<img src="banner.png" width="100%" alt="example banner">\n\n'
            "# Example\n"
        )
        self.assertEqual(
            normalized_without_banner(before),
            normalized_without_banner(after),
        )

    def test_non_banner_edit_remains_visible(self) -> None:
        before = "---\nname: example\n---\n\n# Example\n"
        after = "---\nname: example\n---\n\n# Changed\n"
        self.assertNotEqual(
            normalized_without_banner(before),
            normalized_without_banner(after),
        )


if __name__ == "__main__":
    unittest.main()
