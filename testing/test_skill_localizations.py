from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from skill_localizations import (
    document_title,
    legacy_locale_paths,
    retirement_plan,
    schema_graph,
    skill_localizations,
)


def write_skill(root: Path, relative: str, name="sample", language="de", title="Beispiel") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\nlanguage: {language}\ndescription: Localized instructions\n"
        f"visibility: public\n---\n# {title}\n\nInstructions.\n", encoding="utf-8"
    )
    return path


def test_locales_are_grouped_with_native_titles_and_one_identity(tmp_path):
    canonical = "skills/utilities/sample/SKILL.md"
    english = "skills/utilities/sample/SKILL.en.md"
    path = write_skill(tmp_path, canonical)
    write_skill(tmp_path, english, language="en", title="Useful sample")
    # Untracked/private sibling is deliberately absent from source authority.
    write_skill(tmp_path, "skills/utilities/sample/SKILL.es.md", language="es", title="Ejemplo")
    rows, issues = skill_localizations(path, {canonical, english}, tmp_path)
    assert issues == []
    assert [(r["language"], r["title"]) for r in rows] == [("de", "Beispiel"), ("en", "Useful sample")]
    assert all("/sample/" in r["path"] for r in rows)


@pytest.mark.parametrize("name,language,title", [("en", "en", "Useful sample"),
                                                 ("sample", "zh", "Useful sample"),
                                                 ("sample", "en", "EN")])
def test_ambiguous_metadata_is_not_advertised(tmp_path, name, language, title):
    canonical = "skills/utilities/sample/SKILL.md"
    variant = "skills/utilities/sample/SKILL.en.md"
    path = write_skill(tmp_path, canonical)
    write_skill(tmp_path, variant, name=name, language=language, title=title)
    rows, issues = skill_localizations(path, {canonical, variant}, tmp_path)
    assert [r["language"] for r in rows] == ["de"]
    assert len(issues) == 1


def test_marker_stub_is_not_an_advertised_translation(tmp_path):
    canonical = "skills/utilities/sample/SKILL.md"
    variant = "skills/utilities/sample/SKILL.en.md"
    path = write_skill(tmp_path, canonical)
    (tmp_path / variant).write_text("---\nlanguage: en\n---\n# English\nSame text", encoding="utf-8")
    rows, issues = skill_localizations(path, {canonical, variant}, tmp_path)
    assert len(rows) == 1
    assert len(issues) == 1


def test_title_ignores_frontmatter_comments_and_fenced_examples():
    assert document_title("---\nname: x\n---\n<!-- # Not title -->\n```md\n# en\n```\n# Real title") == "Real title"


def test_retirement_preserves_divergent_bytes_and_rejects_missing_flat(tmp_path):
    legacy = "skills/utilities/sample/EN/SKILL.md"
    flat = "skills/utilities/sample/SKILL.en.md"
    old = write_skill(tmp_path, legacy, title="Older text")
    write_skill(tmp_path, flat, title="Different text")
    raw = old.read_bytes()
    plan = retirement_plan(tmp_path, [legacy, flat])
    assert legacy_locale_paths([legacy, flat]) == [legacy]
    source, target = plan[0]
    source.rename(target)
    assert target.read_bytes() == raw
    assert not source.exists()
    old.write_bytes(raw)
    with pytest.raises(ValueError, match="destination already exists"):
        retirement_plan(tmp_path, [legacy, flat])
    target.unlink()
    with pytest.raises(ValueError, match="No canonical flat"):
        retirement_plan(tmp_path, [legacy])


def test_foreign_locale_layout_is_not_migrated_by_house_rules():
    assert legacy_locale_paths(["skills/third-party/vendor/en/SKILL.md"]) == []


def test_schema_org_graph_links_translations_without_changing_identity():
    registry = {"components": [{"id": "skill:utilities:sample", "path": "skills/utilities/sample/SKILL.md",
                                "localizations": [{"path": "skills/utilities/sample/SKILL.md", "language": "de",
                                                   "title": "Beispiel", "description": "Beschreibung"},
                                                  {"path": "skills/utilities/sample/SKILL.en.md", "language": "en",
                                                   "title": "Sample", "description": "Description"}]}]}
    graph = schema_graph(registry, "https://example.org/source/")
    primary, translated = graph["@graph"]
    assert translated["translationOfWork"] == {"@id": primary["@id"]}
    assert primary["workTranslation"] == [{"@id": translated["@id"]}]
    assert primary["identifier"] == translated["identifier"]
    assert json.loads(json.dumps(graph))["@context"] == "https://schema.org"


def test_tracked_private_translation_is_excluded_by_public_source_authority(tmp_path):
    from build_public_registry import build_registry, git_skill_artifacts

    canonical = "skills/utilities/sample/SKILL.md"
    variant = "skills/utilities/sample/SKILL.en.md"
    write_skill(tmp_path, canonical)
    path = write_skill(tmp_path, variant, language="en", title="Private variant")
    path.write_text(path.read_text(encoding="utf-8").replace("visibility: public", "visibility: private-only"),
                    encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "skills"], cwd=tmp_path, check=True)
    files = git_skill_artifacts(tmp_path)
    assert files == [canonical]
    registry = build_registry(files, repository_root=tmp_path)
    assert [item["language"] for item in registry["components"][0]["localizations"]] == ["de"]
