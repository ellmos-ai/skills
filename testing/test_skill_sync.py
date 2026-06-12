"""Tests fuer skill_sync.py -- Mapping, Drift-Erkennung, Deploy, Dry-Run.

Alle Tests laufen gegen tmp_path-Fixtures, NIE gegen das echte ~/.claude/skills.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import skill_sync  # noqa: E402
from skill_sync import (  # noqa: E402
    ST_DRIFT,
    ST_OK,
    ST_SOURCE_ONLY,
    ST_TARGET_ONLY,
    build_mapping,
    compare_skill,
    deploy_skill,
    is_deregistered,
    map_filename,
    read_hold_list,
    scan,
)


# ─── Fixtures ───


@pytest.fixture
def roots(tmp_path):
    """Quelle (kategorisiert) + Ziel (flach) als tmp-Verzeichnisse."""
    source = tmp_path / "skills"
    target = tmp_path / "deployed"
    source.mkdir()
    target.mkdir()
    return source, target


def make_skill(root: Path, category: str, name: str, files: dict[str, str]):
    """Legt einen Quell-Skill mit Dateien an. files: relpath -> content."""
    d = root / category / name
    d.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return d


def make_target(root: Path, name: str, files: dict[str, str]):
    """Legt einen Deployment-Skill (flach) an."""
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return d


# ─── Mapping ───


def test_build_mapping_kategorisiert_zu_flach(roots):
    source, _ = roots
    make_skill(source, "dev", "alpha", {"SKILL.md": "a"})
    make_skill(source, "therapy", "beta", {"SKILL.md": "b"})
    mapping = build_mapping(source)
    assert set(mapping) == {"alpha", "beta"}
    assert mapping["alpha"].parent.name == "dev"


def test_build_mapping_ignoriert_underscore_ordner(roots):
    source, _ = roots
    make_skill(source, "_templates", "tmpl", {"SKILL.md": "t"})
    make_skill(source, "dev", "_draft", {"SKILL.md": "d"})
    make_skill(source, "dev", "real", {"SKILL.md": "r"})
    assert set(build_mapping(source)) == {"real"}


def test_build_mapping_kollision_wirft_fehler(roots):
    source, _ = roots
    make_skill(source, "dev", "doppelt", {"SKILL.md": "1"})
    make_skill(source, "utilities", "doppelt", {"SKILL.md": "2"})
    with pytest.raises(ValueError, match="Kollision"):
        build_mapping(source)


# ─── Drift-Erkennung ───


def test_status_ok_bei_identischen_dateien(roots):
    source, target = roots
    src = make_skill(source, "dev", "s1", {"SKILL.md": "x", "ref/a.md": "y"})
    make_target(target, "s1", {"SKILL.md": "x", "ref/a.md": "y"})
    st = compare_skill("s1", src, target)
    assert st.status == ST_OK


def test_status_drift_bei_geaenderter_datei(roots):
    source, target = roots
    src = make_skill(source, "dev", "s1", {"SKILL.md": "neu"})
    make_target(target, "s1", {"SKILL.md": "alt"})
    st = compare_skill("s1", src, target)
    assert st.status == ST_DRIFT
    assert st.changed == ["SKILL.md"]


def test_status_nur_quelle(roots):
    source, target = roots
    src = make_skill(source, "dev", "frisch", {"SKILL.md": "x"})
    st = compare_skill("frisch", src, target)
    assert st.status == ST_SOURCE_ONLY


def test_scan_meldet_nur_ziel_skills(roots):
    source, target = roots
    make_skill(source, "dev", "s1", {"SKILL.md": "x"})
    make_target(target, "s1", {"SKILL.md": "x"})
    make_target(target, "lokal-only", {"SKILL.md": "z"})
    results = {r.name: r for r in scan(source, target)}
    assert results["lokal-only"].status == ST_TARGET_ONLY
    assert results["s1"].status == ST_OK


def test_scan_zaehlt_quell_und_ziel_dateien(roots):
    source, target = roots
    make_skill(source, "dev", "s1", {"SKILL.md": "x", "SKILL.en.md": "e"})
    make_target(target, "s1", {"SKILL.md": "x", "extra.log": "stale"})
    st = {r.name: r for r in scan(source, target)}["s1"]
    assert st.status == ST_DRIFT
    assert st.source_only == ["SKILL.en.md"]
    assert st.target_only == ["extra.log"]


# ─── Deregistrierung (CONTENT.md-Muster) ───


def test_deregistriert_erkannt(roots):
    _, target = roots
    d = make_target(target, "dereg", {"CONTENT.md": "x"})
    assert is_deregistered(d) is True
    d2 = make_target(target, "normal", {"SKILL.md": "x"})
    assert is_deregistered(d2) is False


def test_map_filename_dereg():
    assert map_filename("SKILL.md", True) == "CONTENT.md"
    assert map_filename("SKILL.en.md", True) == "CONTENT.en.md"
    assert map_filename("SKILL.md", False) == "SKILL.md"
    assert map_filename("references/SKILL.md", True) == "references/SKILL.md"
    assert map_filename("notes.md", True) == "notes.md"


def test_dereg_vergleich_skill_gegen_content(roots):
    source, target = roots
    src = make_skill(source, "therapy", "t1", {"SKILL.md": "inhalt", "SKILL.en.md": "en"})
    make_target(target, "t1", {"CONTENT.md": "inhalt", "CONTENT.en.md": "en"})
    st = compare_skill("t1", src, target)
    assert st.status == ST_OK
    assert st.deregistered is True


def test_dereg_drift_erkannt(roots):
    source, target = roots
    src = make_skill(source, "therapy", "t1", {"SKILL.md": "neu"})
    make_target(target, "t1", {"CONTENT.md": "alt"})
    st = compare_skill("t1", src, target)
    assert st.status == ST_DRIFT
    assert st.changed == ["SKILL.md"]


# ─── Deploy ───


def test_deploy_kopiert_korrekt(roots):
    source, target = roots
    src = make_skill(source, "dev", "s1",
                     {"SKILL.md": "neu", "ref/a.md": "ref-inhalt"})
    make_target(target, "s1", {"SKILL.md": "alt"})
    actions = deploy_skill("s1", src, target, dry_run=False)
    assert (target / "s1" / "SKILL.md").read_text(encoding="utf-8") == "neu"
    assert (target / "s1" / "ref" / "a.md").read_text(encoding="utf-8") == "ref-inhalt"
    assert len(actions) == 2


def test_deploy_neuer_skill(roots):
    source, target = roots
    src = make_skill(source, "dev", "frisch", {"SKILL.md": "x"})
    deploy_skill("frisch", src, target, dry_run=False)
    assert (target / "frisch" / "SKILL.md").read_text(encoding="utf-8") == "x"


def test_dry_run_kopiert_nichts(roots):
    source, target = roots
    src = make_skill(source, "dev", "s1", {"SKILL.md": "neu", "neu.md": "n"})
    make_target(target, "s1", {"SKILL.md": "alt", "stale.md": "s"})
    actions = deploy_skill("s1", src, target, dry_run=True)
    # Aktionen geplant, aber nichts veraendert
    assert len(actions) == 3  # update SKILL.md, copy neu.md, prune stale.md
    assert (target / "s1" / "SKILL.md").read_text(encoding="utf-8") == "alt"
    assert not (target / "s1" / "neu.md").exists()
    assert (target / "s1" / "stale.md").exists()


def test_deploy_prunt_veraltete_dateien(roots):
    source, target = roots
    src = make_skill(source, "dev", "s1", {"SKILL.md": "x"})
    make_target(target, "s1", {"SKILL.md": "x", "veraltet.md": "weg"})
    deploy_skill("s1", src, target, dry_run=False)
    assert not (target / "s1" / "veraltet.md").exists()


def test_deploy_erhaelt_deregistrierung(roots):
    source, target = roots
    src = make_skill(source, "therapy", "t1", {"SKILL.md": "neu", "SKILL.en.md": "en-neu"})
    make_target(target, "t1", {"CONTENT.md": "alt", "CONTENT.en.md": "en-alt"})
    deploy_skill("t1", src, target, dry_run=False)
    td = target / "t1"
    assert (td / "CONTENT.md").read_text(encoding="utf-8") == "neu"
    assert (td / "CONTENT.en.md").read_text(encoding="utf-8") == "en-neu"
    assert not (td / "SKILL.md").exists()  # Deregistrierung bleibt erhalten
    assert not (td / "SKILL.en.md").exists()


def test_deploy_idempotent(roots):
    source, target = roots
    src = make_skill(source, "dev", "s1", {"SKILL.md": "x"})
    deploy_skill("s1", src, target, dry_run=False)
    actions = deploy_skill("s1", src, target, dry_run=False)
    assert actions == []


# ─── Hold-Liste ───


def test_hold_liste_lesen(roots):
    _, target = roots
    (target / ".sync-hold").write_text(
        "# lokale Forks\ncounseling-basics\n\nstabilization-techniques\n",
        encoding="utf-8")
    assert read_hold_list(target) == {"counseling-basics", "stabilization-techniques"}


def test_hold_liste_fehlt(roots):
    _, target = roots
    assert read_hold_list(target) == set()


def test_scan_markiert_hold(roots):
    source, target = roots
    make_skill(source, "dev", "s1", {"SKILL.md": "neu"})
    make_target(target, "s1", {"SKILL.md": "alt"})
    (target / ".sync-hold").write_text("s1\n", encoding="utf-8")
    st = {r.name: r for r in scan(source, target)}["s1"]
    assert st.on_hold is True
    assert st.status == ST_DRIFT


# ─── CLI-Ebene (cmd_deploy gegen tmp-Roots) ───


def test_cmd_deploy_alle_ueberspringt_hold(roots, capsys):
    source, target = roots
    make_skill(source, "dev", "auto", {"SKILL.md": "neu"})
    make_target(target, "auto", {"SKILL.md": "alt"})
    make_skill(source, "dev", "fork", {"SKILL.md": "neu"})
    make_target(target, "fork", {"SKILL.md": "lokal"})
    (target / ".sync-hold").write_text("fork\n", encoding="utf-8")

    args = type("A", (), {"skills": [], "dry_run": False, "force": False})()
    skill_sync.cmd_deploy(args, source_root=source, target_root=target)

    assert (target / "auto" / "SKILL.md").read_text(encoding="utf-8") == "neu"
    assert (target / "fork" / "SKILL.md").read_text(encoding="utf-8") == "lokal"
    assert "UEBERSPRUNGEN (HOLD): fork" in capsys.readouterr().out


def test_cmd_deploy_hold_mit_force(roots, capsys):
    source, target = roots
    make_skill(source, "dev", "fork", {"SKILL.md": "neu"})
    make_target(target, "fork", {"SKILL.md": "lokal"})
    (target / ".sync-hold").write_text("fork\n", encoding="utf-8")

    args = type("A", (), {"skills": ["fork"], "dry_run": False, "force": True})()
    skill_sync.cmd_deploy(args, source_root=source, target_root=target)
    assert (target / "fork" / "SKILL.md").read_text(encoding="utf-8") == "neu"


def test_cmd_deploy_alle_ueberspringt_nur_quelle(roots, capsys):
    source, target = roots
    make_skill(source, "dev", "nie-deployt", {"SKILL.md": "x"})
    args = type("A", (), {"skills": [], "dry_run": False, "force": False})()
    skill_sync.cmd_deploy(args, source_root=source, target_root=target)
    assert not (target / "nie-deployt").exists()
    assert "Nichts zu deployen" in capsys.readouterr().out
