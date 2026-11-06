"""Tests for worldset_coverage.py (pure functions only, no network)."""
from __future__ import annotations

import worldset_coverage as wc


def test_languages_in_detects_file_and_dir_variants() -> None:
    paths = ["README.md", "README_de.md", "README.es.md", "docs/README-zh-CN.md",
             "docs/i18n/ja/guide.md", "i18n/pt/README.md", "README_xx.md", "src/readme_fr.txt"]
    assert wc.languages_in(paths) == {"de", "es", "zh", "ja", "pt"}


def test_languages_in_ignores_non_world_set_and_source_readme() -> None:
    assert wc.languages_in(["README.md", "README_it.md", "CHANGELOG_de.md"]) == set()


def test_summarize_counts_target_slots_without_source() -> None:
    rows = [
        {"repo": "o/a", "stars": 1, "readme": True, "langs": ["de"]},
        {"repo": "o/b", "stars": 0, "readme": True, "langs": wc.WORLD_SET},  # 11 variants cap at 10
        {"repo": "o/c", "stars": 0, "readme": False, "langs": []},
    ]
    s = wc.summarize(rows)
    assert (s["repos"], s["repos_with_readme"], s["slots"], s["filled"], s["open"]) == (3, 2, 20, 11, 9)
    assert s["complete"] == ["o/b"]
