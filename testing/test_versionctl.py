"""Tests fuer versionctl.py -- status, validate, inventory, registry-generate.

Alle Tests laufen gegen tmp_path-Fixtures, NIE gegen das echte skills/-Verzeichnis.
"""

import argparse
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import versionctl  # noqa: E402
from versionctl import (  # noqa: E402
    _build_registry_entry,
    _derive_component_id,
    find_all_skills,
    parse_frontmatter,
    sha256_file,
    validate_against_schema,
)

SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"

# ─── Hilfsfunktionen ───


def make_skill_md(directory: Path, content: str = "") -> Path:
    """Legt eine SKILL.md in einem Verzeichnis an."""
    directory.mkdir(parents=True, exist_ok=True)
    p = directory / "SKILL.md"
    p.write_text(content, encoding="utf-8")
    return p


MINIMAL_FRONTMATTER = """\
---
name: test-skill
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-01-01
updated: 2026-01-01
description: Ein Test-Skill fuer automatisierte Tests.
language: de
standalone: true
status: active
provenance:
  origin: custom
---

# Test-Skill
Inhalt des Skills.
"""

INVALID_FRONTMATTER = """\
---
name: fehlerhaft
version: keine-semver-version
type: unbekannter-typ
---

# Fehlerhafter Skill
"""


# ─── parse_frontmatter ───


def test_parse_frontmatter_liest_felder(tmp_path):
    p = make_skill_md(tmp_path / "cat" / "skill", MINIMAL_FRONTMATTER)
    fm = parse_frontmatter(p)
    assert fm is not None
    assert fm["name"] == "test-skill"
    assert fm["version"] == "1.0.0"
    assert fm["standalone"] is True
    assert fm["type"] == "skill"


def test_parse_frontmatter_fehlende_trennzeichen(tmp_path):
    p = make_skill_md(tmp_path / "a" / "b", "kein frontmatter hier\n")
    fm = parse_frontmatter(p)
    assert fm is None


# ─── sha256_file ───


def test_sha256_file_format(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("hallo", encoding="utf-8")
    h = sha256_file(p)
    assert h.startswith("sha256:")
    assert len(h) == 71  # "sha256:" (7) + 64 hex chars


def test_sha256_file_aenderung_erkannt(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("alt", encoding="utf-8")
    h1 = sha256_file(p)
    p.write_text("neu", encoding="utf-8")
    h2 = sha256_file(p)
    assert h1 != h2


# ─── validate_against_schema ───


def test_validate_positive_minimal(tmp_path):
    """Valider minimaler Eintrag soll 0 Fehler haben."""
    p = make_skill_md(tmp_path / "cat" / "test-skill", MINIMAL_FRONTMATTER)
    fm = parse_frontmatter(p)
    fm["_path"] = "cat/test-skill"
    entry = _build_registry_entry(p, fm, tmp_path)

    schema_file = SCHEMAS_DIR / "component-v1.schema.json"
    if not schema_file.exists():
        pytest.skip("schemas/ nicht vorhanden (kein Checkout)")

    errors = validate_against_schema(entry, schema_file)
    assert errors == [], f"Unerwartete Fehler: {errors}"


def test_validate_negative_fehlende_pflichtfelder(tmp_path):
    """Eintrag ohne Pflichtfelder soll Fehler produzieren."""
    schema_file = SCHEMAS_DIR / "component-v1.schema.json"
    if not schema_file.exists():
        pytest.skip("schemas/ nicht vorhanden")

    # Absichtlich unvollstaendiges Objekt
    incomplete = {
        "id": "skill:cat:test",
        "name": "test",
        # 'type', 'path', 'version', 'schema_version', ... fehlen
    }
    errors = validate_against_schema(incomplete, schema_file)
    assert len(errors) > 0
    missing = [e for e in errors if "Pflichtfeld fehlt" in e]
    assert len(missing) > 0


def test_validate_negative_ungueltige_version(tmp_path):
    """Eintrag mit ungueltigem version-Pattern soll Fehler melden."""
    schema_file = SCHEMAS_DIR / "component-v1.schema.json"
    if not schema_file.exists():
        pytest.skip("schemas/ nicht vorhanden")

    p = make_skill_md(tmp_path / "cat" / "test-skill", MINIMAL_FRONTMATTER)
    fm = parse_frontmatter(p)
    fm["_path"] = "cat/test-skill"
    entry = _build_registry_entry(p, fm, tmp_path)
    entry["version"] = "keine-semver"  # ungueltig

    errors = validate_against_schema(entry, schema_file)
    pattern_errors = [e for e in errors if "Pattern" in e and "version" in e]
    assert len(pattern_errors) > 0, f"Kein Pattern-Fehler fuer version, erhalten: {errors}"


def test_validate_negative_ungueltige_hash_format(tmp_path):
    """Eintrag mit ungueltigem content_hash soll Fehler melden."""
    schema_file = SCHEMAS_DIR / "component-v1.schema.json"
    if not schema_file.exists():
        pytest.skip("schemas/ nicht vorhanden")

    p = make_skill_md(tmp_path / "cat" / "test-skill", MINIMAL_FRONTMATTER)
    fm = parse_frontmatter(p)
    fm["_path"] = "cat/test-skill"
    entry = _build_registry_entry(p, fm, tmp_path)
    entry["content_hash"] = "md5:abc123"  # falsches Format

    errors = validate_against_schema(entry, schema_file)
    hash_errors = [e for e in errors if "content_hash" in e]
    assert len(hash_errors) > 0


# ─── _derive_component_id ───


def test_derive_component_id_format():
    cid = _derive_component_id("dev", "bugfix-protocol", "protocol")
    assert cid == "protocol:dev:bugfix-protocol"
    # Muss nur erlaubte Zeichen enthalten
    import re
    assert re.match(r"^[a-z]+:[a-z0-9_.-]+(:[a-z0-9_.-]+)*$", cid), f"ID ungueltig: {cid}"


def test_derive_component_id_keine_backslashes():
    """Windows-Pfadtrenner duerfen nicht in IDs auftauchen."""
    cid = _derive_component_id("game-dev", "roblox-dev", "skill")
    assert "\\" not in cid
    assert "/" not in cid


# ─── find_all_skills (gegen tmp_path) ───


def test_find_all_skills_findet_skills(tmp_path):
    make_skill_md(tmp_path / "dev" / "alpha", MINIMAL_FRONTMATTER)
    make_skill_md(tmp_path / "therapy" / "beta", MINIMAL_FRONTMATTER)
    results = find_all_skills(skills_dir=tmp_path)
    names = [fm.get("name") for _, fm in results]
    assert "test-skill" in names
    assert len(results) == 2


def test_find_all_skills_ignoriert_underscore_ordner(tmp_path):
    make_skill_md(tmp_path / "_templates" / "tmpl", MINIMAL_FRONTMATTER)
    make_skill_md(tmp_path / "dev" / "real", MINIMAL_FRONTMATTER)
    results = find_all_skills(skills_dir=tmp_path)
    assert len(results) == 1


# ─── cmd_registry_generate ───


def _make_test_skills_dir(tmp_path: Path) -> Path:
    """Erzeugt ein minimales skills/-Verzeichnis fuer Registry-Tests."""
    skills = tmp_path / "skills"
    make_skill_md(skills / "dev" / "alpha", MINIMAL_FRONTMATTER)
    make_skill_md(skills / "therapy" / "beta", MINIMAL_FRONTMATTER)
    return skills


def test_registry_generate_erzeugt_datei(tmp_path, monkeypatch):
    """registry-generate schreibt eine valide components.json."""
    skills = _make_test_skills_dir(tmp_path)
    registry_dir = tmp_path / "registry"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", registry_dir)

    args = argparse.Namespace(dry_run=False)
    rc = versionctl.cmd_registry_generate(args)
    assert rc == 0

    out = registry_dir / "components.json"
    assert out.exists()

    data = json.loads(out.read_text(encoding="utf-8"))
    assert "components" in data
    assert len(data["components"]) == 2
    assert "summary" in data
    assert data["summary"]["component_count"] == 2


def test_registry_generate_reproducibel(tmp_path, monkeypatch):
    """Zwei aufeinanderfolgende Laeufe erzeugen identische Komponenten-Daten."""
    skills = _make_test_skills_dir(tmp_path)
    registry_dir = tmp_path / "registry"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", registry_dir)

    args = argparse.Namespace(dry_run=False)
    versionctl.cmd_registry_generate(args)
    out = registry_dir / "components.json"
    data1 = json.loads(out.read_text(encoding="utf-8"))
    components1 = data1["components"]

    versionctl.cmd_registry_generate(args)
    data2 = json.loads(out.read_text(encoding="utf-8"))
    components2 = data2["components"]

    # Komponenten-Daten (ohne volatile summary.generated_at) identisch
    assert components1 == components2


def test_registry_generate_dry_run(tmp_path, monkeypatch):
    """Dry-run schreibt keine Datei."""
    skills = _make_test_skills_dir(tmp_path)
    registry_dir = tmp_path / "registry"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", registry_dir)

    args = argparse.Namespace(dry_run=True)
    rc = versionctl.cmd_registry_generate(args)
    assert rc == 0
    assert not (registry_dir / "components.json").exists()


def test_registry_generate_keine_absoluten_pfade(tmp_path, monkeypatch):
    """Keine absoluten System-Pfade in der generierten Registry."""
    skills = _make_test_skills_dir(tmp_path)
    registry_dir = tmp_path / "registry"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", registry_dir)

    args = argparse.Namespace(dry_run=False)
    versionctl.cmd_registry_generate(args)

    content = (registry_dir / "components.json").read_text(encoding="utf-8")
    # Kein Windows-Laufwerksbuchstabe und kein "Users" in den Pfad-Feldern der Komponenten
    data = json.loads(content)
    for comp in data["components"]:
        path_val = comp.get("path", "")
        assert not path_val.startswith("C:"), f"Absoluter Pfad in Komponente: {path_val}"
        assert not path_val.startswith("/Users"), f"Absoluter Pfad in Komponente: {path_val}"
        assert "Users" not in path_val or path_val.startswith("skills/"), \
            f"Verdaechtiger Pfad: {path_val}"


# ─── cmd_status ───


def test_status_ohne_registry(tmp_path, monkeypatch, capsys):
    """status gibt Fehler wenn keine Registry vorhanden."""
    monkeypatch.setattr(versionctl, "SKILLS_DIR", tmp_path / "skills")
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", tmp_path / "registry")

    args = argparse.Namespace()
    rc = versionctl.cmd_status(args)
    assert rc == 1
    out = capsys.readouterr().out
    assert "registry-generate" in out.lower() or "registry" in out.lower()


def test_status_null_drift_nach_generate(tmp_path, monkeypatch, capsys):
    """Nach registry-generate zeigt status 0 Drift."""
    skills = _make_test_skills_dir(tmp_path)
    registry_dir = tmp_path / "registry"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", registry_dir)

    # Registry erzeugen
    args_gen = argparse.Namespace(dry_run=False)
    versionctl.cmd_registry_generate(args_gen)

    # Status pruefen
    capsys.readouterr()  # Buffer leeren
    args_status = argparse.Namespace()
    rc = versionctl.cmd_status(args_status)
    assert rc == 0
    out = capsys.readouterr().out
    assert "DRIFT: 0" in out
    assert "NEU: 0" in out
    assert "Registry ist aktuell" in out


def test_status_erkennt_drift(tmp_path, monkeypatch, capsys):
    """Status erkennt wenn ein Skill nach dem Generieren geaendert wurde."""
    skills = _make_test_skills_dir(tmp_path)
    registry_dir = tmp_path / "registry"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REGISTRY_DIR", registry_dir)

    # Registry erzeugen
    versionctl.cmd_registry_generate(argparse.Namespace(dry_run=False))

    # Skill aendern NACH dem Generieren
    skill_file = skills / "dev" / "alpha" / "SKILL.md"
    skill_file.write_text(MINIMAL_FRONTMATTER + "\n## Geaendert\n", encoding="utf-8")

    # Status muss Drift melden
    capsys.readouterr()
    versionctl.cmd_status(argparse.Namespace())
    out = capsys.readouterr().out
    assert "DRIFT" in out


# ─── cmd_validate ───


def test_validate_findet_missing_conventions(tmp_path, monkeypatch, capsys):
    """validate meldet fehlende CONVENTIONS-Pflichtfelder."""
    skills = tmp_path / "skills"
    bad = """\
---
name: schlecht
---
# Schlecht
"""
    make_skill_md(skills / "dev" / "schlecht", bad)

    schema_file = SCHEMAS_DIR / "skill-v1.schema.json"
    if not schema_file.exists():
        pytest.skip("schemas/ nicht vorhanden")

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "SCHEMAS_DIR", SCHEMAS_DIR)

    args = argparse.Namespace(verbose=False)
    rc = versionctl.cmd_validate(args)
    assert rc == 1
    out = capsys.readouterr().out
    assert "CONVENTIONS" in out


# ─── cmd_inventory ───


def test_inventory_schreibt_datei(tmp_path, monkeypatch):
    """inventory schreibt eine JSON-Datei ohne absolute Systempfade."""
    skills = _make_test_skills_dir(tmp_path)
    reports_dir = tmp_path / "_reports"
    out_file = tmp_path / "inv-test.json"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REPORTS_DIR", reports_dir)

    args = argparse.Namespace(output=str(out_file))
    rc = versionctl.cmd_inventory(args)
    assert rc == 0
    assert out_file.exists()

    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert "summary" in data
    assert data["summary"]["skill_count"] == 2
    assert "root" not in data["summary"], "Kein absoluter 'root'-Pfad im Summary"

    content = out_file.read_text(encoding="utf-8")
    assert "C:\\Users" not in content
    assert "/Users/User" not in content
    assert "/Users/lukas" not in content


def test_inventory_reproduzierbar(tmp_path, monkeypatch):
    """Zwei inventory-Laeufe erzeugen identische skill-Eintraege."""
    skills = _make_test_skills_dir(tmp_path)
    reports_dir = tmp_path / "_reports"

    monkeypatch.setattr(versionctl, "SKILLS_DIR", skills)
    monkeypatch.setattr(versionctl, "REPORTS_DIR", reports_dir)

    out1 = tmp_path / "inv1.json"
    out2 = tmp_path / "inv2.json"

    versionctl.cmd_inventory(argparse.Namespace(output=str(out1)))
    versionctl.cmd_inventory(argparse.Namespace(output=str(out2)))

    d1 = json.loads(out1.read_text(encoding="utf-8"))
    d2 = json.loads(out2.read_text(encoding="utf-8"))

    # Skills-Eintraege (ohne volatile generated_at im summary) identisch
    assert d1["skills"] == d2["skills"]
