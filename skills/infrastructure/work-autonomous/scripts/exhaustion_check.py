"""Selbstkenntnis + Verortungs-Check fuer die vier Quellen der Exhaustion-Kette
(work-autonomous, Ebene 2, Ticket T-20260815-205101335).

Der Skill selbst bleibt in erster Linie ein Protokoll-Dokument, das ein Modell
liest und mit seinen eigenen Werkzeugen befolgt -- kein Daemon, keine eigene
Laufzeit. Dieses Skript liefert dem Modell VOR dem eigentlichen Inhalts-Check
ein deterministisches, testbares Ergebnis fuer die reine Frage "kann ich diese
Quelle ueberhaupt erreichen?" (found/unavailable). Ob an einer erreichbaren
Stelle tatsaechlich NEUE Arbeit liegt (empty vs. echter Treffer), bleibt
bewusst Sache des aufrufenden Modells -- das liest den Inhalt mit seinen
eigenen Werkzeugen (Bash/usmc-CLI/Gardener/Read), nicht dieses Skript.

Vier Bedarfe (Selbstkenntnis, deklariert statt geraten):
  decisions.ledger   zentrales Entscheidungsregister
  memory.organic     Gardener (find()/put())
  memory.curated     USMC (facts/lessons/working/context)
  user.model         decision-avatar / BYUM

Wichtig, ehrlich benannt: nur `decisions.ledger` und `user.model` sind
tatsaechlich als KNOWN_MODULE_PROVIDERS in source-resolver registriert (Stand
2026-08-15). `memory.organic`/`memory.curated` haben dort (noch) KEINEN
eingetragenen Provider -- eine Anfrage ueber grounding_seed/source_resolver
wuerde fuer diese zwei Rollen immer nur "nicht verortet" liefern, egal ob
usmc/gardener tatsaechlich installiert sind. Deshalb werden diese zwei Rollen
IMMER ueber einen direkten, domaenenspezifischen Check (CLI auf PATH)
entschieden -- die generische Rollenaufloesung waere hier weniger genau als
das, was der Skill selbst schon weiss.

Laeuft identisch mit UND ohne installiertes `grounding_seed` (Stufenordnung
bleibt gleich, siehe grounding-seed README "KEIN zweiter Resolver").
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

FOUND = "found"
UNAVAILABLE = "unavailable"

# Reihenfolge = Kettenschritt-Zuordnung: decisions.ledger -> Schritt 2,
# memory.organic + memory.curated -> Schritt 3 (zwei Quellen, ein Schritt),
# user.model -> Schritt 4. think/decide (Schritt 1) ist KEINE Quelle, sondern
# der eigene Analyseschritt des Modells -- taucht hier bewusst nicht auf.
FOUR_NEEDS = ("decisions.ledger", "memory.organic", "memory.curated", "user.model")

# Rollen, fuer die source-resolver/grounding_seed einen echten, verlaesslichen
# KNOWN_MODULE_PROVIDER hat (Stand 2026-08-15, ladder.py KNOWN_MODULE_PROVIDERS).
_RESOLVER_BACKED_ROLES = {"decisions.ledger", "user.model"}

# Direkter Fallback-Pfad je Rolle, falls grounding_seed nicht importierbar ist
# (dieselbe Stelle, die grounding_seed/source_resolver ohnehin pruefen wuerden).
_FALLBACK_PATHS: dict[str, tuple[str, ...]] = {
    "decisions.ledger": ("_control-center/_DECISIONS",),
    "user.model": ("_control-center/_TOM-lm/avatar/START.md", "_control-center/_TOM-lm"),
}

# Domaenenspezifischer CLI-Check fuer die zwei Rollen ohne source-resolver-Provider.
_DIRECT_CLI_CHECK: dict[str, str] = {
    "memory.organic": "gardener",
    "memory.curated": "usmc",
}


@dataclass
class LocationCheck:
    rolle: str
    status: str  # FOUND | UNAVAILABLE -- NIE "empty", reine Verortung
    weg: str      # "resolver" | "fallback-pfad" | "cli-check" -- womit ermittelt
    nachricht: str = ""


def _try_grounding_seed():
    try:
        import grounding_seed  # noqa: F401
        return grounding_seed
    except Exception:
        return None


def _via_resolver(rolle: str, gs) -> str | None:
    """Nutzt grounding_seed.resolve() + status_from_resolution(). Liefert
    None, wenn der Aufruf selbst scheitert (dann faellt der Aufrufer auf den
    direkten Pfad-Fallback zurueck -- kein Crash)."""
    try:
        result = gs.resolve(rolle)
        return gs.status_from_resolution(result)
    except Exception:
        return None


def _via_fallback_path(rolle: str, home: Path) -> str:
    for rel in _FALLBACK_PATHS.get(rolle, ()):
        if (home / rel).exists():
            return FOUND
    return UNAVAILABLE


def _via_cli_check(rolle: str) -> str:
    cli = _DIRECT_CLI_CHECK[rolle]
    return FOUND if shutil.which(cli) else UNAVAILABLE


def assess_locations(home: Path | None = None) -> list[LocationCheck]:
    """Fuehrt die Selbstkenntnis-Pruefung fuer alle vier Bedarfe aus."""
    home = home or Path.cwd()
    gs = _try_grounding_seed()
    checks: list[LocationCheck] = []

    for rolle in FOUR_NEEDS:
        if rolle in _DIRECT_CLI_CHECK:
            # memory.organic/memory.curated: IMMER direkter CLI-Check, siehe
            # Moduldoku oben -- die generische Rollenaufloesung kennt diese
            # Rollen (noch) nicht und waere hier ungenauer.
            checks.append(LocationCheck(rolle, _via_cli_check(rolle), "cli-check"))
            continue

        status = None
        weg = "fallback-pfad"
        if gs is not None and rolle in _RESOLVER_BACKED_ROLES:
            status = _via_resolver(rolle, gs)
            weg = "resolver"
        if status is None:
            status = _via_fallback_path(rolle, home)
            weg = "fallback-pfad"
        checks.append(LocationCheck(rolle, status, weg))

    return checks


def unavailable_roles(checks: list[LocationCheck]) -> list[str]:
    return [c.rolle for c in checks if c.status == UNAVAILABLE]


def all_locatable(checks: list[LocationCheck]) -> bool:
    """True, wenn KEINE der vier Quellen unavailable ist -- Vorbedingung
    dafuer, dass ein 'exhausted'-Urteil ueberhaupt in Frage kommt."""
    return len(unavailable_roles(checks)) == 0


def format_blind_signal(checks: list[LocationCheck]) -> str:
    missing = unavailable_roles(checks)
    return (
        f"WORK-AUTONOMOUS: STOP (blind, {len(missing)}/{len(checks)} "
        f"Quellen nicht verfuegbar: {', '.join(missing)})"
    )


def intake_gate_blocks_stop(inbox_open_count: int) -> bool:
    """TICKET-MASTER-Intake-Gate (SKILL.md, Ebene 1, Ticket T-20260902-729068782).

    Nur relevant, wenn ueberhaupt ein Ticketsystem (`_TICKETS/`) Teil des
    Kontexts ist -- Sitzungen ohne Ticketsystem rufen diese Funktion nicht
    auf. Solange `INBOX/` (inklusive formloser, noch nicht triagierter
    Eintraege) nicht auf 0 steht, darf KEIN Abbruchsignal entstehen
    (`NO_WORK`/`exhausted`/`blind`/Guard-STOP) -- Ebene 2 wird gar nicht
    erst betreten. Das Zaehlen selbst (wie viele Eintraege liegen in
    `INBOX/`?) macht das aufrufende Modell mit seinen eigenen Werkzeugen,
    genau wie bei den vier Kettenschritten oben.
    """
    return inbox_open_count > 0


def availability_fingerprint_component(checks: list[LocationCheck]) -> tuple[str, ...]:
    """Fuer den Guard-Fingerprint (siehe SKILL.md): sortiertes Tupel der
    UNAVAILABLE-Rollen. Aendert sich dieser Anteil (weil eine Quelle
    dazukommt oder verschwindet), muss der Guard neu pruefen -- das ist die
    'Verpflanzung' im Sinne der Metapher."""
    return tuple(sorted(unavailable_roles(checks)))


if __name__ == "__main__":  # pragma: no cover -- manuelle Diagnose
    import sys

    result = assess_locations()
    for c in result:
        print(f"{c.rolle}: {c.status} ({c.weg})")
    if not all_locatable(result):
        print(format_blind_signal(result))
        sys.exit(0)
    print("Alle vier Quellen verortet -- Inhaltspruefung durch das Modell kann laufen.")
