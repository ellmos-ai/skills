from __future__ import annotations

import importlib.util
import json
import os
import re
from pathlib import Path
from time import time


SCRIPT = Path(__file__).parents[1] / "scripts" / "folder_organization.py"
SPEC = importlib.util.spec_from_file_location("folder_organization", SCRIPT)
assert SPEC and SPEC.loader
folder_organization = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(folder_organization)

EXPORT_SCRIPT = Path(__file__).parents[1] / "scripts" / "export_portable.py"
EXPORT_SPEC = importlib.util.spec_from_file_location("export_portable", EXPORT_SCRIPT)
assert EXPORT_SPEC and EXPORT_SPEC.loader
export_portable = importlib.util.module_from_spec(EXPORT_SPEC)
EXPORT_SPEC.loader.exec_module(export_portable)


def test_inventory_is_read_only_and_detects_version_chain(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("rules", encoding="utf-8")
    (tmp_path / "report_v1.md").write_text("first", encoding="utf-8")
    (tmp_path / "report_v2.md").write_text("second", encoding="utf-8")
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))

    report = folder_organization.build_inventory(
        tmp_path, folder_organization.load_config(None)
    )

    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert before == after
    assert report["mutation_performed"] is False
    assert report["summary"]["version_groups"] == 1
    assert all(
        item["action"] == "review-version-chain-member" and item["confidence"] == "low"
        for item in report["suggestions"]
    )
    assert not any("canonical" in item["action"] for item in report["suggestions"])
    readme = next(item for item in report["files"] if item["path"] == "README.md")
    assert readme["role"] == "control"


def test_old_log_is_a_review_candidate(tmp_path: Path) -> None:
    log = tmp_path / "worker.log"
    log.write_text("done", encoding="utf-8")
    old = time() - 40 * 24 * 60 * 60
    os.utime(log, (old, old))
    config = folder_organization.load_config(None)
    config["log_retention_days"] = 30

    report = folder_organization.build_inventory(tmp_path, config)

    assert any(
        item["action"] == "review-archive-log" and item["path"] == "worker.log"
        for item in report["suggestions"]
    )


def test_clue_markers_and_language_pair_are_visible(tmp_path: Path) -> None:
    (tmp_path / "guide_de.md").write_text("<!-- OUTDATED: see guide_en.md -->", encoding="utf-8")
    (tmp_path / "guide_en.md").write_text("current", encoding="utf-8")

    report = folder_organization.build_inventory(tmp_path, folder_organization.load_config(None))

    german = next(item for item in report["files"] if item["path"] == "guide_de.md")
    assert "OUTDATED" in german["clue_markers"]
    assert report["summary"]["related_sets"] == 1


def test_log_tokens_avoid_substrings_and_protect_active_and_evidence_logs(tmp_path: Path) -> None:
    paths = {
        "catalog.md": "catalog",
        "blog_notes.md": "blog",
        "stderr.txt": "error",
        "audit_history.md": "evidence",
        "current_worker.log": "active",
    }
    old = time() - 40 * 24 * 60 * 60
    for name, content in paths.items():
        path = tmp_path / name
        path.write_text(content, encoding="utf-8")
        os.utime(path, (old, old))

    report = folder_organization.build_inventory(tmp_path, folder_organization.load_config(None))
    roles = {item["path"]: item["role"] for item in report["files"]}

    assert roles["catalog.md"] == "document"
    assert roles["blog_notes.md"] == "document"
    assert roles["stderr.txt"] == "rotatable-log-candidate"
    assert roles["audit_history.md"] == "evidence-log"
    assert roles["current_worker.log"] == "active-log"
    archive_paths = {
        item["path"] for item in report["suggestions"]
        if item["action"] == "review-archive-log"
    }
    assert archive_paths == {"stderr.txt"}
    assert all(item["confidence"] == "low" for item in report["suggestions"])


def test_clue_detection_requires_marker_syntax_and_ignores_examples(tmp_path: Path) -> None:
    (tmp_path / "plain.md").write_text(
        "This discusses CLUE, OUTDATED, and SUPERSEDED as ordinary words.", encoding="utf-8"
    )
    (tmp_path / "example.md").write_text(
        "```markdown\n<!-- OUTDATED: example only -->\n```\n", encoding="utf-8"
    )
    (tmp_path / "inline.md").write_text(
        "Example: `<!-- OUTDATED: inline example -->`\n", encoding="utf-8"
    )
    (tmp_path / "indented.md").write_text(
        "    <!-- OUTDATED: indented code example -->\n", encoding="utf-8"
    )
    (tmp_path / "marked.md").write_text(
        "<!-- SUPERSEDED-BY: current.md -->\n", encoding="utf-8"
    )

    report = folder_organization.build_inventory(tmp_path, folder_organization.load_config(None))
    markers = {item["path"]: item["clue_markers"] for item in report["files"]}

    assert markers["plain.md"] == []
    assert markers["example.md"] == []
    assert markers["inline.md"] == []
    assert markers["indented.md"] == []
    assert markers["marked.md"] == ["SUPERSEDED"]


def test_language_pair_with_trailing_version_is_related(tmp_path: Path) -> None:
    (tmp_path / "guide_de_v2.md").write_text("Deutsch", encoding="utf-8")
    (tmp_path / "guide_en_v2.md").write_text("English", encoding="utf-8")

    report = folder_organization.build_inventory(tmp_path, folder_organization.load_config(None))

    assert report["summary"]["related_sets"] == 1


def test_mtime_does_not_nominate_a_canonical_version(tmp_path: Path) -> None:
    first = tmp_path / "plan_v1.md"
    second = tmp_path / "plan_v2.md"
    first.write_text("newer edit", encoding="utf-8")
    second.write_text("older edit", encoding="utf-8")
    now = time()
    os.utime(first, (now, now))
    os.utime(second, (now - 1000, now - 1000))

    report = folder_organization.build_inventory(tmp_path, folder_organization.load_config(None))

    assert not any("canonical" in item["action"] for item in report["suggestions"])
    assert not any("predecessor" in item["action"] for item in report["suggestions"])


def test_cli_refuses_overwrite_and_output_inside_root(tmp_path: Path) -> None:
    existing = tmp_path.parent / f"{tmp_path.name}-existing.json"
    existing.write_text("keep", encoding="utf-8")

    assert folder_organization.main([str(tmp_path), "--out", str(existing)]) == 2
    assert existing.read_text(encoding="utf-8") == "keep"

    inside = tmp_path / "inventory.json"
    assert folder_organization.main([str(tmp_path), "--out", str(inside)]) == 2
    assert not inside.exists()


def test_portable_export_is_self_contained_and_refuses_overwrite(tmp_path: Path) -> None:
    destination = tmp_path / "portable-folder-organization"

    created = export_portable.export(destination)

    content = (created / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", content, flags=re.DOTALL)
    assert frontmatter
    keys = {
        line.split(":", 1)[0]
        for line in frontmatter.group(1).splitlines()
        if ":" in line
    }
    assert keys == {"name", "description"}
    assert (created / "scripts" / "folder_organization.py").is_file()
    assert (created / "references" / "heuristics.md").is_file()

    assert export_portable.main([str(destination)]) == 2


def test_protected_secret_name_is_never_opened_or_hashed(
    tmp_path: Path, monkeypatch
) -> None:
    protected = tmp_path / ".env"
    protected.write_text("opaque protected fixture", encoding="utf-8")
    config = folder_organization.load_config(None)
    original_open = Path.open

    def guarded_open(self: Path, *args, **kwargs):
        if self == protected:
            raise AssertionError("protected secret content was opened")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    report = folder_organization.build_inventory(tmp_path, config, hash_all=True)

    item = report["files"][0]
    assert item["role"] == "protected-secret-candidate"
    assert item["sha256"] is None
    assert item["clue_markers"] == []
    assert item["secret_status"]["content_opened"] is False
    assert report["summary"]["protected_secret_files_not_opened"] == 1


def test_secret_template_exclusion_remains_readable(tmp_path: Path) -> None:
    template = tmp_path / ".env.production.example"
    template.write_text("EXAMPLE_NAME=placeholder", encoding="utf-8")

    report = folder_organization.build_inventory(
        tmp_path, folder_organization.load_config(None)
    )

    item = report["files"][0]
    assert item["role"] != "protected-secret-candidate"
    assert "secret_status" not in item
    assert item["sha256"] is not None


def test_incidental_secret_signal_is_redacted_from_report(tmp_path: Path) -> None:
    sensitive_line = "api_" + "key=" + "regression-value-" + ("x" * 16)
    (tmp_path / "notes.txt").write_text(sensitive_line, encoding="utf-8")

    report = folder_organization.build_inventory(
        tmp_path, folder_organization.load_config(None)
    )
    serialized = json.dumps(report, ensure_ascii=False)
    item = report["files"][0]

    assert item["role"] == "secret-candidate"
    assert item["sha256"] is None
    assert item["secret_status"]["signal_ids"] == ["secret-assignment"]
    assert sensitive_line not in serialized


def test_cloud_secret_creates_localization_plan_without_disclosing_local_path(
    tmp_path: Path,
) -> None:
    (tmp_path / ".env").write_text("opaque", encoding="utf-8")
    config = folder_organization.load_config(None)
    config["secret_policy"]["cloud_detection"]["configured_roots"] = [str(tmp_path)]
    config["secret_policy"]["local_secret_root"] = "C:/private/example-only"

    report = folder_organization.build_inventory(tmp_path, config)

    assert report["summary"]["cloud_secret_candidates"] == 1
    assert report["secret_policy"]["local_destination_configured"] is True
    assert report["secret_policy"]["local_path_disclosed_in_cloud_pointer"] is False
    assert any(item["action"] == "plan-localize-secret" for item in report["suggestions"])
    assert "C:/private/example-only" not in json.dumps(report)


def test_partial_secret_policy_config_keeps_safe_defaults(tmp_path: Path) -> None:
    custom = tmp_path / "config.json"
    custom.write_text(
        json.dumps({
            "secret_policy": {
                "cloud_action": "report-only",
                "protected_name_patterns": ["*.vaultsecret"],
            }
        }),
        encoding="utf-8",
    )

    config = folder_organization.load_config(custom)

    assert config["secret_policy"]["cloud_action"] == "report-only"
    assert config["secret_policy"]["pointer_mode"] == "control-file"
    assert config["secret_policy"]["protected_name_patterns"] == ["*.vaultsecret"]


def test_custom_local_pointer_map_is_always_protected(
    tmp_path: Path, monkeypatch
) -> None:
    pointer_map = tmp_path / "custom-map.example"
    pointer_map.write_text("opaque-id -> local path", encoding="utf-8")
    config = folder_organization.load_config(None)
    config["secret_policy"]["local_pointer_map"] = pointer_map.name
    original_open = Path.open

    def guarded_open(self: Path, *args, **kwargs):
        if self == pointer_map:
            raise AssertionError("configured local pointer map was opened")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    report = folder_organization.build_inventory(tmp_path, config, hash_all=True)

    item = report["files"][0]
    assert item["role"] == "protected-secret-candidate"
    assert item["sha256"] is None
    assert item["secret_status"]["rule"] == "local-pointer-map"
    assert item["secret_status"]["content_opened"] is False
