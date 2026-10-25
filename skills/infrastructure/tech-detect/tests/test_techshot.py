"""Techshot contract tests use isolated seeds and no live inventory or network."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "techshot.py"
SPEC = importlib.util.spec_from_file_location("techshot", SCRIPT)
techshot = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(techshot)


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
            {"version": version, "version_quality": "observed"}]}]
        if include_extra:
            rows.append({"component_id": "pip:vendor:other", "installations": [
                {"version": "1.0", "version_quality": "reported"}]})
        return {"schema_version": techshot.SCHEMA, "host": {"slot": slot},
                "components": rows}
    report = techshot.compare(snapshot("laptop", "1.0", True),
                              snapshot("workstation", "2.0", False))
    assert [(item["component_id"], item["status"]) for item in report["changes"]] == [
        ("pip:vendor:other", "not-observed-on-one-host"),
        ("pip:vendor:widget", "version-drift"),
    ]
    assert "not proof" in report["meaning"]


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
    other = {**first, "host": {**first["host"], "slot": "workstation"},
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
    a = {"schema_version": techshot.SCHEMA, "host": {"slot": "a"}, "components": []}
    b = {"schema_version": techshot.SCHEMA, "host": {"slot": "b"}, "components": []}
    left, right, output = (tmp_path / name for name in ("a.json", "b.json", "out.json"))
    left.write_text(json.dumps(a), encoding="utf-8")
    right.write_text(json.dumps(b), encoding="utf-8")
    assert techshot.main(["compare", "--left", str(left), "--right", str(right),
                          "--output", str(output)]) == 0
    assert json.loads(output.read_text(encoding="utf-8"))["schema_version"] == techshot.COMPARE_SCHEMA
    with pytest.raises(SystemExit) as error:
        techshot.main(["compare", "--left", str(left), "--right", str(right),
                       "--output", str(output)])
    assert error.value.code == 1
