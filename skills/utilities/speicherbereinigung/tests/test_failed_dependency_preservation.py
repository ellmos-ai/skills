"""A failed sandbox removal must preserve its entire object-source chain."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import prune_ephemeral  # noqa: E402


@pytest.mark.parametrize(
    ("failure", "expected"),
    [("A", ["A", "D"]), ("B", ["A", "B", "D"]), (None, ["A", "B", "C", "D"])],
)
def test_failed_removal_preserves_transitive_sources(tmp_path, monkeypatch, failure, expected):
    for name in ("A", "B", "C", "D"):
        (tmp_path / name).mkdir()
    dependencies = {"A": {"B"}, "B": {"C"}, "C": set(), "D": set()}
    monkeypatch.setattr(prune_ephemeral, "review_verdict", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        prune_ephemeral, "sandbox_dependencies",
        lambda full, root: dependencies[Path(full).name],
    )
    attempted = []

    def remove(full, root):
        name = Path(full).name
        attempted.append(name)
        return name != failure

    monkeypatch.setattr(prune_ephemeral, "remove_review_sandbox", remove)
    prune_ephemeral.prune_reviews(str(tmp_path), 24, True, lambda line: None)

    assert set(attempted) == set(expected)
    for child, sources in dependencies.items():
        for source in sources:
            if child in attempted and source in attempted:
                assert attempted.index(child) < attempted.index(source)
