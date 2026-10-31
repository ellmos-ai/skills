"""Techshot contract tests use isolated seeds and no live inventory or network."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "techshot.py"
SPEC = importlib.util.spec_from_file_location("techshot", SCRIPT)
techshot = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(techshot)


def _snapshot(slot: str, hostname: str, components: list[dict],
              captured_at: str = "2026-10-25T04:00:00Z") -> dict:
    return {"schema_version": techshot.SCHEMA, "captured_at_utc": captured_at,
            "host": {"slot": slot, "hostname": hostname},
            "inventory": {"seed_sha256": "a" * 64, "seed_stand": "2026-10-24", "slot": slot},
            "coverage": {"native_package_source": "fixture", "native_package_errors": [],
                         "path_entries_considered": 0, "python_candidates": 0,
                         "complete_installation_inventory": False},
            "components": components}


def _installation(install_id: str, version: str | None,
                  quality: str = "observed") -> dict:
    return {"install_id": install_id, "version": version,
            "version_quality": quality, "source": "synthetic-fixture"}


def _seed(path: Path, hostname: str = "host-a") -> Path:
    path.write_text(json.dumps({"_stand": "2026-10-25",
                                "system": {"name": "laptop", "hostname": hostname,
                                           "cpu": "Example CPU", "ram_gb": 16},
                                "software": [{"name": "Python", "version": "3.x",
                                              "install_method": "system"},
                                             {"name": "Widget", "version": None,
                                              "install_method": "winget"}]}), encoding="utf-8")
    return path


def test_capture_keeps_seed_uncertainty_and_native_installations_separate(tmp_path, monkeypatch):
    monkeypatch.setattr(techshot.platform, "system", lambda: "Windows")
    monkeypatch.setattr(techshot, "_python_candidates",
                        lambda paths: [("C:/trusted/python.exe", "running-interpreter"),
                                       ("C:/venv/python.exe", "PATH")])
    seed = _seed(tmp_path / "laptop.json")
    snapshot = techshot.capture(seed, slot="laptop", hostname="host-a", package_rows=[
        {"name": "Widget", "publisher": "Vendor", "version": "2.4.1",
         "install_id": "HKLM:64:widget"}])
    assert snapshot["schema_version"] == techshot.SCHEMA
    assert snapshot["host"]["hardware_seed_quality"] == "inventory-reported-not-live-verified"
    assert snapshot["inventory"]["seed_sha256"]
    assert snapshot["coverage"]["complete_installation_inventory"] is False
    assert snapshot["python_context"]["running_executable"]
    assert snapshot["python_context"]["running_venv"] is (
        techshot.sys.prefix != techshot.sys.base_prefix)
    assert snapshot["python_context"]["path_candidates_in_order"] == ["C:/venv/python.exe"]
    seed_python = next(row for row in snapshot["components"]
                       if row["component_id"] == "system:unknown:python")
    assert seed_python["installations"][0]["version_quality"] == "uncertain"
    runtime = next(row for row in snapshot["components"]
                   if row["component_id"] == "python-runtime:python-software-foundation:python")
    assert {item["version_quality"] for item in runtime["installations"]} == {"observed", "unknown"}
    native = next(row for row in snapshot["components"]
                  if row["component_id"] == "windows-uninstall:vendor:widget")
    assert native["installations"][0]["version"] == "2.4.1"


def test_component_ids_preserve_distinct_unicode_names():
    assert techshot._component_id("Müller", "Vendor", "winget") != (
        techshot._component_id("Mller", "Vendor", "winget"))


def test_homebrew_multiple_versions_are_separate_installations(monkeypatch):
    monkeypatch.setattr(techshot.shutil, "which", lambda name: "/usr/local/bin/brew")

    class Result:
        returncode = 0
        stdout = "widget 1.0 2.0\n"

    monkeypatch.setattr(techshot.subprocess, "run", lambda *args, **kwargs: Result())
    rows, errors = techshot._native_package_rows("Darwin")
    assert errors == []
    assert [(row["version"], row["install_id"]) for row in rows] == [
        ("1.0", "homebrew:widget:1.0"), ("2.0", "homebrew:widget:2.0")]


def test_explicit_probe_is_observed_as_separate_venv_without_running_it(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", "")
    venv = tmp_path / "venv"
    executable = venv / "Scripts" / "python.exe"
    executable.parent.mkdir(parents=True)
    executable.write_bytes(b"fixture")
    (venv / "pyvenv.cfg").write_text("home = fixture\n", encoding="utf-8")
    monkeypatch.setattr(techshot, "_probe_python", lambda path: "9.8.7")
    snapshot = techshot.capture(_seed(tmp_path / "seed.json"), slot="laptop",
                                hostname="host-a", package_rows=[],
                                probe_paths=[str(executable)])
    runtime = next(row for row in snapshot["components"]
                   if row["component_id"] == "python-runtime:python-software-foundation:python")
    assert any(item["version"] == "9.8.7" and item["source"] == "explicit"
               for item in runtime["installations"])
    assert str(executable) in snapshot["python_context"]["observed_venv_markers"]


def test_capture_refuses_foreign_seed_and_does_not_write(tmp_path):
    with pytest.raises(ValueError, match="does not belong"):
        techshot.capture(_seed(tmp_path / "seed.json", "another-host"),
                         slot="laptop", hostname="host-a", package_rows=[])


def test_compare_distinguishes_drift_from_missing_observation():
    def snapshot(slot, version, include_extra):
        rows = [{"component_id": "pip:vendor:widget", "installations": [
            _installation("widget-install", version)]}]
        if include_extra:
            rows.append({"component_id": "pip:vendor:other", "installations": [
                _installation("other-install", "1.0", "reported")]})
        return _snapshot(slot, f"fixture-{slot}", rows)
    report = techshot.compare(snapshot("laptop", "1.0", True),
                              snapshot("workstation", "2.0", False))
    assert [(item["component_id"], item["status"]) for item in report["changes"]] == [
        ("pip:vendor:other", "not-observed-on-one-host"),
        ("pip:vendor:widget", "version-drift"),
    ]
    assert "not proof" in report["meaning"]


def test_compare_keeps_unknown_installation_beside_equal_known_version():
    known = _installation("runtime", "3.12.10")
    unknown = _installation("path-candidate", None, "unknown")
    left = _snapshot("host-a", "fixture-a", [{"component_id": "python", "installations":
                                                [known, unknown]}])
    right = _snapshot("host-b", "fixture-b", [{"component_id": "python", "installations":
                                                 [known]}])
    result = techshot.compare(left, right)
    assert len(result["changes"]) == 1
    change = result["changes"][0]
    assert change["status"] == "version-uncertain"
    assert change["versions"] == {"left": ["3.12.10"], "right": ["3.12.10"]}
    assert change["unresolved_installations"]["left"] == [unknown]
    assert change["unresolved_installations"]["right"] == []
    assert result["inputs"]["left"]["hash_basis"] == "canonical-json"


def test_version_drift_keeps_additional_uncertain_installation():
    uncertain = _installation("other-install", "3.x", "uncertain")
    left = _snapshot("a", "fixture-a", [
        {"component_id": "python", "installations": [_installation("runtime", "3.11"), uncertain]}
    ])
    right = _snapshot("b", "fixture-b", [
        {"component_id": "python", "installations": [_installation("runtime", "3.12")]}
    ])
    change = techshot.compare(left, right)["changes"][0]
    assert change["status"] == "version-drift"
    assert change["unresolved_installations"]["left"] == [uncertain]


def test_same_host_history_uses_stable_identity_and_direction():
    old = _snapshot("server", "fixture-server", [
        {"component_id": "openssl", "installations": [_installation("package", "3.0.6")]}
    ], "2020-01-01T00:00:00Z")
    new = _snapshot("server", "fixture-server", [
        {"component_id": "openssl", "installations": [_installation("package", "3.0.23")]}
    ], "2026-10-25T04:00:00Z")
    result = techshot.compare(old, new)
    assert result["axis"] == "same-host-time"
    assert result["chronology"] == "left-before-right"
    assert result["hosts"] == ["server", "server"]
    assert result["changes"][0]["status"] == "version-drift"
    assert techshot.compare(new, old)["chronology"] == "right-before-left"
    with pytest.raises(ValueError, match="distinct capture times"):
        techshot.compare(old, {**new, "captured_at_utc": old["captured_at_utc"]})
    with pytest.raises(ValueError, match="asset continuity"):
        techshot.compare(old, {**new, "host": {"slot": "server", "hostname": "renamed-server"}})


def test_distinct_slots_may_share_a_hostname_without_claiming_same_asset():
    left = _snapshot("asset-a", "localhost", [])
    right = _snapshot("asset-b", "localhost", [])
    result = techshot.compare(left, right)
    assert result["axis"] == "cross-host"
    assert "share a hostname" in result["identity_note"]


def test_same_host_history_cli_preserves_capture_times(tmp_path):
    old = _snapshot("server", "fixture-server", [], "2020-01-01T00:00:00Z")
    new = _snapshot("server", "fixture-server", [], "2026-10-25T04:00:00Z")
    left, right, output = (tmp_path / name for name in ("old.json", "new.json", "compare.json"))
    left.write_text(json.dumps(old), encoding="utf-8")
    right.write_text(json.dumps(new), encoding="utf-8")
    assert techshot.main(["compare", "--left", str(left), "--right", str(right),
                          "--output", str(output)]) == 0
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["axis"] == "same-host-time"
    assert result["inputs"]["left"]["captured_at_utc"] == "2020-01-01T00:00:00Z"
    assert result["inputs"]["right"]["captured_at_utc"] == "2026-10-25T04:00:00Z"


@pytest.mark.parametrize("missing", ["captured_at_utc", "inventory", "coverage"])
def test_compare_refuses_missing_snapshot_provenance(missing):
    left = _snapshot("a", "fixture-a", [])
    right = _snapshot("b", "fixture-b", [])
    del right[missing]
    with pytest.raises(ValueError):
        techshot.compare(left, right)


@pytest.mark.parametrize("damage", ["missing-seed-stand", "empty-coverage-source"])
def test_compare_refuses_incomplete_nested_provenance(damage):
    left = _snapshot("a", "fixture-a", [])
    right = _snapshot("b", "fixture-b", [])
    if damage == "missing-seed-stand":
        del right["inventory"]["seed_stand"]
    else:
        right["coverage"]["native_package_source"] = ""
    with pytest.raises(ValueError):
        techshot.compare(left, right)


def test_hardware_live_evidence_separate_from_seed_and_unknown_not_drift(tmp_path, monkeypatch):
    monkeypatch.setattr(techshot, "_python_candidates", lambda paths: [])
    monkeypatch.setattr(techshot, "_hardware_observations", lambda: {
        "os": {"value": "Windows 11", "quality": "observed", "source": "platform"},
        "gpu_model": {"value": None, "quality": "unknown", "source": "unavailable"},
    })
    first = techshot.capture(_seed(tmp_path / "seed.json"), slot="laptop",
                             hostname="host-a", package_rows=[])
    assert first["host"]["hardware_seed"]["cpu"] == "Example CPU"
    assert first["host"]["hardware_seed_quality"] == "inventory-reported-not-live-verified"
    assert first["hardware_observations"]["os"]["source"] == "platform"
    other = {**first, "host": {**first["host"], "slot": "workstation",
                               "hostname": "fixture-workstation"},
             "inventory": {**first["inventory"], "slot": "workstation"},
             "hardware_observations": {
                 "os": {"value": "Linux 6", "quality": "observed", "source": "platform"},
                 "gpu_model": {"value": None, "quality": "unknown", "source": "unavailable"},
             }}
    report = techshot.compare(first, other)
    assert {item["field"]: item["status"] for item in report["hardware_changes"]} == {
        "os": "different", "architecture": "unknown", "cpu_model": "unknown",
        "logical_cpu_count": "unknown", "ram_total_bytes": "unknown",
        "gpu_model": "unknown", "system_filesystem_total_bytes": "unknown",
    }


def test_compare_cli_writes_new_versioned_file_and_refuses_overwrite(tmp_path):
    a = _snapshot("a", "fixture-a", [], "2020-01-01T00:00:00Z")
    b = _snapshot("b", "fixture-b", [])
    left, right, output = (tmp_path / name for name in ("a.json", "b.json", "out.json"))
    left.write_text(json.dumps(a), encoding="utf-8")
    right.write_text(json.dumps(b), encoding="utf-8")
    assert techshot.main(["compare", "--left", str(left), "--right", str(right),
                          "--output", str(output)]) == 0
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["schema_version"] == techshot.COMPARE_SCHEMA
    assert result["axis"] == "cross-host"
    assert result["inputs"]["left"]["sha256"] == hashlib.sha256(left.read_bytes()).hexdigest()
    assert result["inputs"]["left"]["hash_basis"] == "file-bytes"
    assert result["inputs"]["left"]["captured_at_utc"] == "2020-01-01T00:00:00Z"
    assert result["inputs"]["right"]["inventory"] == b["inventory"]
    assert result["inputs"]["right"]["coverage"] == b["coverage"]
    with pytest.raises(SystemExit) as error:
        techshot.main(["compare", "--left", str(left), "--right", str(right),
                       "--output", str(output)])
    assert error.value.code == 1


def test_compare_cli_missing_coverage_writes_no_result(tmp_path):
    a = _snapshot("a", "fixture-a", [])
    b = _snapshot("b", "fixture-b", [])
    del b["coverage"]
    left, right, output = (tmp_path / name for name in ("a.json", "b.json", "out.json"))
    left.write_text(json.dumps(a), encoding="utf-8")
    right.write_text(json.dumps(b), encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        techshot.main(["compare", "--left", str(left), "--right", str(right),
                       "--output", str(output)])
    assert error.value.code == 1
    assert not output.exists()
