"""Regression tests for the generic repo-link visibility gate (T-20260926-820252321)."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("repo_link_visibility_gate.py")
SPEC = importlib.util.spec_from_file_location("repo_link_visibility_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(gate)


class ExtractLinksTests(unittest.TestCase):
    def test_extracts_plain_link(self) -> None:
        text = "See [ellmos-core](https://github.com/ellmos-ai/ellmos-core) for details."
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_trailing_path(self) -> None:
        text = "CI: https://github.com/ellmos-ai/skills/actions/workflows/tests.yml"
        self.assertEqual({("ellmos-ai", "skills")}, gate.extract_github_repo_links(text))

    def test_deduplicates_repeated_links(self) -> None:
        text = (
            "https://github.com/ellmos-ai/bach and again "
            "[BACH](https://github.com/ellmos-ai/bach)"
        )
        self.assertEqual({("ellmos-ai", "bach")}, gate.extract_github_repo_links(text))

    def test_ignores_non_repo_org_paths(self) -> None:
        text = "https://github.com/marketplace/actions/checkout"
        self.assertEqual(set(), gate.extract_github_repo_links(text))

    def test_no_links_found(self) -> None:
        self.assertEqual(set(), gate.extract_github_repo_links("Just plain text."))


class CheckVisibilityTests(unittest.TestCase):
    def test_uses_prober_result_and_populates_cache(self) -> None:
        cache: dict = {}
        calls: list[tuple[str, str]] = []

        def fake_prober(org: str, repo: str) -> str:
            calls.append((org, repo))
            return "private"

        result = gate.check_visibility("ellmos-ai", "ellmos-core", cache=cache, prober=fake_prober)
        self.assertEqual("private", result)
        self.assertEqual([("ellmos-ai", "ellmos-core")], calls)
        self.assertIn("ellmos-ai/ellmos-core", cache)

    def test_cached_result_skips_prober(self) -> None:
        cache = {"ellmos-ai/skills": {"visibility": "public", "checked_at": __import__("time").time()}}
        calls: list[tuple[str, str]] = []

        def fake_prober(org: str, repo: str) -> str:
            calls.append((org, repo))
            return "private"  # would be wrong if actually called

        result = gate.check_visibility("ellmos-ai", "skills", cache=cache, prober=fake_prober)
        self.assertEqual("public", result)
        self.assertEqual([], calls, "cached entry must skip the prober entirely")

    def test_stale_cache_entry_is_refreshed(self) -> None:
        stale_time = __import__("time").time() - gate._CACHE_TTL_SECONDS - 10
        cache = {"ellmos-ai/skills": {"visibility": "public", "checked_at": stale_time}}
        calls: list[tuple[str, str]] = []

        def fake_prober(org: str, repo: str) -> str:
            calls.append((org, repo))
            return "private"

        result = gate.check_visibility("ellmos-ai", "skills", cache=cache, prober=fake_prober)
        self.assertEqual("private", result)
        self.assertEqual([("ellmos-ai", "skills")], calls)


class RunGateTests(unittest.TestCase):
    def _prober_factory(self, visibility_map: dict[tuple[str, str], str]):
        def prober(org: str, repo: str) -> str:
            return visibility_map.get((org, repo), "unknown")
        return prober

    def test_confirmed_private_repo_is_a_blocking_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "[ellmos-core](https://github.com/ellmos-ai/ellmos-core)", encoding="utf-8"
            )
            findings, warnings = gate.run_gate(
                Path(tmp), [readme],
                prober=self._prober_factory({("ellmos-ai", "ellmos-core"): "private"}),
                use_cache=False,
            )
            self.assertEqual(1, len(findings))
            self.assertIn("ellmos-ai/ellmos-core", findings[0])
            self.assertIn("PRIVATE", findings[0])
            self.assertEqual([], warnings)

    def test_public_repo_is_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "[BACH](https://github.com/ellmos-ai/bach)", encoding="utf-8"
            )
            findings, warnings = gate.run_gate(
                Path(tmp), [readme],
                prober=self._prober_factory({("ellmos-ai", "bach"): "public"}),
                use_cache=False,
            )
            self.assertEqual([], findings)
            self.assertEqual([], warnings)

    def test_unknown_visibility_is_a_warning_not_a_finding(self) -> None:
        """Network down / rate-limited / 404 -- team-lead instruction: warn, never block."""
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "[some-repo](https://github.com/some-org/some-repo)", encoding="utf-8"
            )
            findings, warnings = gate.run_gate(
                Path(tmp), [readme],
                prober=self._prober_factory({}),  # not in map -> "unknown"
                use_cache=False,
            )
            self.assertEqual([], findings)
            self.assertEqual(1, len(warnings))
            self.assertIn("some-org/some-repo", warnings[0])


if __name__ == "__main__":
    unittest.main()
