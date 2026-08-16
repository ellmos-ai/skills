"""Tests fuer work-autonomous scripts/exhaustion_check.py.

Deckt beide Betriebsarten ab (advisor-Vorgabe: "test it both ways: with
grounding-seed importable and with the import forced to fail") -- der Skill
muss sich identisch verhalten, ob grounding_seed installiert ist oder nicht.

Run:
    PYTHONIOENCODING=utf-8 python -m pytest skills/infrastructure/work-autonomous/tests/ -v
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import exhaustion_check as ec  # noqa: E402


# --- Hilfsmittel: ein Fake-grounding_seed-Modul fuer den "installiert"-Pfad ---

class _FakeResolutionResult:
    def __init__(self, status):
        self.status = status


def _make_fake_grounding_seed(role_to_status: dict[str, str]):
    """Baut ein minimales Fake-Modul mit `.resolve()` und
    `.status_from_resolution()`, wie `grounding_seed` es exportiert."""
    fake = types.SimpleNamespace()

    def resolve(rolle):
        return _FakeResolutionResult(role_to_status.get(rolle, "not_found"))

    def status_from_resolution(result):
        return "found" if result.status in ("resolved", "proposed") else "unavailable"

    fake.resolve = resolve
    fake.status_from_resolution = status_from_resolution
    return fake


@pytest.fixture()
def isolated_home(tmp_path):
    """Ein leeres Verzeichnis ohne _control-center -- simuliert ein System
    ganz ohne Oekosystem-Infrastruktur."""
    return tmp_path


@pytest.fixture(autouse=True)
def _clear_grounding_seed_cache(monkeypatch):
    """Stellt sicher, dass ein evtl. echtes `grounding_seed` im Testlauf
    nicht ungewollt gefunden wird, ausser ein Test setzt es explizit."""
    monkeypatch.setitem(sys.modules, "grounding_seed", None)
    yield


# --- Fall A: grounding_seed NICHT importierbar (haeufigster isolierter Fall) ---

def test_all_unavailable_on_isolated_system_without_any_infrastructure(isolated_home, monkeypatch):
    """Kernszenario des Tickets: System ohne Gardener/USMC/_DECISIONS/BYUM.
    `shutil.which` wird gemockt, weil auf DIESEM (echten) System usmc/gardener
    tatsaechlich auf PATH liegen -- der Test simuliert ein System, auf dem das
    nicht der Fall ist, unabhaengig vom Testlauf-Host."""
    monkeypatch.setattr(ec.shutil, "which", lambda name: None)
    checks = ec.assess_locations(home=isolated_home)
    assert {c.rolle for c in checks} == set(ec.FOUR_NEEDS)
    assert ec.all_locatable(checks) is False
    assert set(ec.unavailable_roles(checks)) == set(ec.FOUR_NEEDS)


def test_decisions_ledger_found_via_fallback_path_when_present(isolated_home):
    (isolated_home / "_control-center" / "_DECISIONS").mkdir(parents=True)
    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["decisions.ledger"].status == ec.FOUND
    assert by_role["decisions.ledger"].weg == "fallback-pfad"


def test_user_model_found_via_fallback_path_when_present(isolated_home):
    profile = isolated_home / "_control-center" / "_TOM-lm" / "avatar"
    profile.mkdir(parents=True)
    (profile / "START.md").write_text("x", encoding="utf-8")
    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["user.model"].status == ec.FOUND


def test_memory_roles_use_cli_check_never_fallback_path(isolated_home, monkeypatch):
    """memory.organic/memory.curated duerfen NIE ueber den Pfad-Fallback
    entschieden werden -- nur ueber den direkten CLI-Check (Moduldoku)."""
    # Ein Pfad, der zufaellig wie die Fallback-Konvention aussieht, darf nichts bewirken.
    monkeypatch.setattr(ec.shutil, "which", lambda name: None)
    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["memory.organic"].weg == "cli-check"
    assert by_role["memory.curated"].weg == "cli-check"
    assert by_role["memory.organic"].status == ec.UNAVAILABLE
    assert by_role["memory.curated"].status == ec.UNAVAILABLE


def test_memory_roles_found_when_cli_on_path(isolated_home, monkeypatch):
    monkeypatch.setattr(ec.shutil, "which", lambda name: f"/usr/bin/{name}")
    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["memory.organic"].status == ec.FOUND
    assert by_role["memory.curated"].status == ec.FOUND


# --- Fall B: grounding_seed IST importierbar ---

def test_resolver_backed_roles_prefer_grounding_seed_when_available(isolated_home, monkeypatch):
    fake_gs = _make_fake_grounding_seed({"decisions.ledger": "resolved", "user.model": "not_found"})
    monkeypatch.setitem(sys.modules, "grounding_seed", fake_gs)

    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["decisions.ledger"].status == ec.FOUND
    assert by_role["decisions.ledger"].weg == "resolver"
    # user.model: resolver sagt not_found -> unavailable, OBWOHL kein
    # Fallback-Pfad geprueft wird (Resolver hat Vorrang und liefert ein
    # gueltiges Ergebnis -- kein Fallback-Fallthrough noetig).
    assert by_role["user.model"].status == ec.UNAVAILABLE
    assert by_role["user.model"].weg == "resolver"


def test_memory_roles_ignore_grounding_seed_even_when_available(isolated_home, monkeypatch):
    """Kernpunkt der Moduldoku: memory.organic/memory.curated haben KEINEN
    source-resolver-Provider -- ein installiertes grounding_seed darf hier
    nicht befragt werden, das waere immer 'unavailable', egal ob usmc/
    gardener echt erreichbar sind."""
    fake_gs = _make_fake_grounding_seed({"memory.organic": "resolved", "memory.curated": "resolved"})
    monkeypatch.setitem(sys.modules, "grounding_seed", fake_gs)
    monkeypatch.setattr(ec.shutil, "which", lambda name: f"/usr/bin/{name}")

    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["memory.organic"].weg == "cli-check"
    assert by_role["memory.curated"].weg == "cli-check"
    assert by_role["memory.organic"].status == ec.FOUND  # via CLI, nicht via Fake-Resolver


def test_resolver_exception_falls_back_to_direct_path_check(isolated_home, monkeypatch):
    def _boom(rolle):
        raise RuntimeError("Resolver kaputt")

    fake_gs = types.SimpleNamespace(resolve=_boom, status_from_resolution=lambda r: "found")
    monkeypatch.setitem(sys.modules, "grounding_seed", fake_gs)
    (isolated_home / "_control-center" / "_DECISIONS").mkdir(parents=True)

    checks = ec.assess_locations(home=isolated_home)
    by_role = {c.rolle: c for c in checks}
    assert by_role["decisions.ledger"].status == ec.FOUND
    assert by_role["decisions.ledger"].weg == "fallback-pfad"


# --- format_blind_signal() / all_locatable() / Fingerprint-Baustein ---

def test_format_blind_signal_matches_ticket_example_shape(isolated_home, monkeypatch):
    monkeypatch.setattr(ec.shutil, "which", lambda name: None)
    checks = ec.assess_locations(home=isolated_home)
    signal = ec.format_blind_signal(checks)
    assert signal.startswith("WORK-AUTONOMOUS: STOP (blind, 4/4 Quellen nicht verfuegbar:")
    for rolle in ec.FOUR_NEEDS:
        assert rolle in signal


def test_availability_fingerprint_component_changes_when_a_source_appears(isolated_home):
    """Der Kern der 'Verpflanzung': kommt eine Quelle hinzu, aendert sich
    dieser Fingerprint-Baustein -- der Guard erkennt es beim naechsten Lauf."""
    before = ec.availability_fingerprint_component(ec.assess_locations(home=isolated_home))
    (isolated_home / "_control-center" / "_DECISIONS").mkdir(parents=True)
    after = ec.availability_fingerprint_component(ec.assess_locations(home=isolated_home))
    assert before != after
    assert "decisions.ledger" in before
    assert "decisions.ledger" not in after


def test_all_locatable_true_when_everything_present(isolated_home, monkeypatch):
    (isolated_home / "_control-center" / "_DECISIONS").mkdir(parents=True)
    profile = isolated_home / "_control-center" / "_TOM-lm" / "avatar"
    profile.mkdir(parents=True)
    (profile / "START.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(ec.shutil, "which", lambda name: f"/usr/bin/{name}")

    checks = ec.assess_locations(home=isolated_home)
    assert ec.all_locatable(checks) is True
    assert ec.unavailable_roles(checks) == []
