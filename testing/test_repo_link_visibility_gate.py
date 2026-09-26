"""Regression tests for the generic repo-link visibility gate (T-20260926-820252321)."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
import unittest.mock
import urllib.error
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

    # Round-2 merge-reviewer evasion examples on PR #39 (T-20260926-820252321):
    # the previous lookahead-based regex silently produced an EMPTY match for
    # the first three, and mis-extracted the repo name (still 404 -> merely
    # "unknown", not a finding) for the last two.

    def test_extracts_link_with_fragment(self) -> None:
        text = "https://github.com/ellmos-ai/ellmos-core#readme"
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_query_string(self) -> None:
        text = "https://github.com/ellmos-ai/ellmos-core?tab=readme-ov-file"
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_trailing_comma(self) -> None:
        text = "See https://github.com/ellmos-ai/ellmos-core, for details."
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_trailing_period(self) -> None:
        text = "See https://github.com/ellmos-ai/ellmos-core."
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_git_suffix(self) -> None:
        text = "git clone https://github.com/ellmos-ai/ellmos-core.git"
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_git_suffix_and_trailing_punctuation(self) -> None:
        text = "clone it (https://github.com/ellmos-ai/ellmos-core.git)."
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))

    def test_extracts_link_with_trailing_bracket(self) -> None:
        text = "[link](https://github.com/ellmos-ai/ellmos-core)"
        self.assertEqual({("ellmos-ai", "ellmos-core")}, gate.extract_github_repo_links(text))


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

    def test_unknown_result_is_never_cached(self) -> None:
        """Round-2 merge-reviewer finding: caching "unknown" would make a
        transient rate limit silence the check for the whole TTL."""
        cache: dict = {}

        def fake_prober(org: str, repo: str) -> str:
            return "unknown"

        result = gate.check_visibility("some-org", "some-repo", cache=cache, prober=fake_prober)
        self.assertEqual("unknown", result)
        self.assertEqual({}, cache, "an unknown result must not be written to the cache")

    def test_unknown_result_is_re_queried_every_time(self) -> None:
        cache: dict = {}
        calls: list[tuple[str, str]] = []

        def fake_prober(org: str, repo: str) -> str:
            calls.append((org, repo))
            return "unknown"

        gate.check_visibility("some-org", "some-repo", cache=cache, prober=fake_prober)
        gate.check_visibility("some-org", "some-repo", cache=cache, prober=fake_prober)
        self.assertEqual(2, len(calls), "an uncached 'unknown' must be re-probed, not skipped")


class DefaultProberTests(unittest.TestCase):
    """Unit-tests the real HTTP classification logic (no network): mocks
    urllib.request.urlopen so the unauthenticated-GET decision table itself
    (200/404/403/network-error) is verified, not just the injectable seam."""

    def test_200_is_public(self) -> None:
        class FakeResponse:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *exc): return False

        with unittest.mock.patch("urllib.request.urlopen", return_value=FakeResponse()):
            self.assertEqual("public", gate._default_prober("ellmos-ai", "usmc"))

    def test_404_is_private(self) -> None:
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/ellmos-ai/ellmos-core", 404, "Not Found", {}, None
        )
        with unittest.mock.patch("urllib.request.urlopen", side_effect=error):
            self.assertEqual("private", gate._default_prober("ellmos-ai", "ellmos-core"))

    def test_403_rate_limit_is_unknown(self) -> None:
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/some-org/some-repo", 403, "rate limited", {}, None
        )
        with unittest.mock.patch("urllib.request.urlopen", side_effect=error):
            self.assertEqual("unknown", gate._default_prober("some-org", "some-repo"))

    def test_429_rate_limit_is_unknown(self) -> None:
        error = urllib.error.HTTPError(
            "https://api.github.com/repos/some-org/some-repo", 429, "too many requests", {}, None
        )
        with unittest.mock.patch("urllib.request.urlopen", side_effect=error):
            self.assertEqual("unknown", gate._default_prober("some-org", "some-repo"))

    def test_network_error_is_unknown(self) -> None:
        with unittest.mock.patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("no network")
        ):
            self.assertEqual("unknown", gate._default_prober("some-org", "some-repo"))


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
            self.assertIn("not a public repo", findings[0])
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
