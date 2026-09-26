"""Tests for org_profile_gate.py's pure detection logic -- no network calls
(the gh-calling functions are thin I/O wrappers around this core)."""
import unittest

import org_profile_gate as gate


class FindBannerPathTests(unittest.TestCase):
    def test_finds_assets_banner_png(self) -> None:
        self.assertEqual(
            "assets/banner.png",
            gate.find_banner_path(["README.md", "assets/banner.png", "src/main.py"]),
        )

    def test_finds_root_banner_svg(self) -> None:
        self.assertEqual("banner.svg", gate.find_banner_path(["banner.svg", "README.md"]))

    def test_no_banner_returns_none(self) -> None:
        self.assertIsNone(gate.find_banner_path(["README.md", "assets/icon.png"]))

    def test_ignores_unrelated_files_containing_banner_substring_wrongly(self) -> None:
        # "bannerless.txt" should not match -- word must end at "banner"
        self.assertIsNone(gate.find_banner_path(["docs/bannerless.txt"]))


class RepoMentionedInProfileTests(unittest.TestCase):
    def test_mentioned_via_table_link(self) -> None:
        profile = "| Tool | [CodeBox](https://github.com/dev-bricks/CodeBox) |"
        self.assertTrue(gate.repo_mentioned_in_profile(profile, "dev-bricks", "CodeBox"))

    def test_mentioned_via_banner_gallery_href(self) -> None:
        profile = '<a href="https://github.com/dev-bricks/zombie-killer-tray"><img .../></a>'
        self.assertTrue(gate.repo_mentioned_in_profile(profile, "dev-bricks", "zombie-killer-tray"))

    def test_not_mentioned(self) -> None:
        profile = "| Tool | [CodeBox](https://github.com/dev-bricks/CodeBox) |"
        self.assertFalse(gate.repo_mentioned_in_profile(profile, "dev-bricks", "NewTool"))

    def test_case_insensitive(self) -> None:
        profile = "https://GITHUB.com/Dev-Bricks/NewTool"
        self.assertTrue(gate.repo_mentioned_in_profile(profile, "dev-bricks", "NewTool"))


class FindMissingEntriesTests(unittest.TestCase):
    def test_repo_with_banner_and_no_mention_is_a_finding(self) -> None:
        repos = [gate.RepoInfo(name="NewTool", tree_paths=["assets/banner.png"], default_branch="main")]
        findings = gate.find_missing_entries("dev-bricks", repos, profile_text="nothing here")
        self.assertEqual(1, len(findings))
        self.assertEqual("NewTool", findings[0]["repo"])
        self.assertEqual("assets/banner.png", findings[0]["banner_path"])
        self.assertIn("github.com/dev-bricks/NewTool", findings[0]["snippet"])
        self.assertIn(
            "https://raw.githubusercontent.com/dev-bricks/NewTool/main/assets/banner.png",
            findings[0]["snippet"],
        )

    def test_repo_with_banner_already_mentioned_is_not_a_finding(self) -> None:
        repos = [gate.RepoInfo(name="CodeBox", tree_paths=["assets/banner.svg"], default_branch="main")]
        profile = "[CodeBox](https://github.com/dev-bricks/CodeBox)"
        findings = gate.find_missing_entries("dev-bricks", repos, profile)
        self.assertEqual([], findings)

    def test_repo_without_banner_is_never_a_finding(self) -> None:
        repos = [gate.RepoInfo(name="NoBanner", tree_paths=["README.md"], default_branch="main")]
        findings = gate.find_missing_entries("dev-bricks", repos, profile_text="")
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
