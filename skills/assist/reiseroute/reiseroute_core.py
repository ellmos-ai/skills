"""reiseroute_core.py — Routenplanung via OSRM (standalone, stdlib only).

Portiert aus BACH system/hub/_services/routing/routing_service.py v1.0.
Entfernt: Origin-DB, alle BACH-Imports.
Ergaenzt: geocode_place an den Modulkopf verschoben (war im Original nur im
  else-Zweig importiert), Nominatim-Rate-Limit, userneutrale Nutzung.
Behaelt: OSRM-Routing (auto/fahrrad/fuss), formatierte Ausgabe.

Wichtig: OSRM erwartet Koordinaten als lon,lat (nicht lat,lon)!
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

# ---------------------------------------------------------------------------
# Konstanten
# ---------------------------------------------------------------------------

OSRM_SERVERS: dict[str, str] = {
    "auto": "https://router.project-osrm.org/route/v1/driving",
    "fahrrad": "https://router.project-osrm.org/route/v1/cycling",
    "fuss": "https://router.project-osrm.org/route/v1/foot",
}

MODE_LABELS: dict[str, str] = {
    "auto": "Auto",
    "fahrrad": "Fahrrad",
    "fuss": "zu Fuß",
}

MODE_ICONS: dict[str, str] = {
    "auto": "🚗",
    "fahrrad": "🚲",
    "fuss": "🚶",
}

# Deutsche / englische Alias → Modus-Key
_MODE_ALIAS: dict[str, str] = {
    "auto": "auto", "car": "auto", "pkw": "auto", "fahren": "auto",
    "fahrrad": "fahrrad", "bike": "fahrrad", "rad": "fahrrad", "radfahren": "fahrrad",
    "fuss": "fuss", "fuß": "fuss", "foot": "fuss", "laufen": "fuss",
    "gehen": "fuss", "zu fuss": "fuss", "zu fuß": "fuss",
}

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "reiseroute-skill/1.0 (github.com/ellmos-ai/skills)"

_last_nominatim_call: float = 0.0


# ---------------------------------------------------------------------------
# Geocoding (Nominatim)
# ---------------------------------------------------------------------------

def _rate_limit_nominatim() -> None:
    """Nominatim: max. 1 Anfrage/Sekunde."""
    global _last_nominatim_call
    elapsed = time.time() - _last_nominatim_call
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _last_nominatim_call = time.time()


def geocode_place(place_name: str) -> Optional[dict]:
    """Ortsname → {'lat': float, 'lon': float, 'display_name': str}.

    Gibt None zurück wenn der Ort nicht gefunden wurde.
    """
    _rate_limit_nominatim()
    params = urllib.parse.urlencode({"q": place_name, "format": "json", "limit": 1})
    url = f"{NOMINATIM_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            results = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Geocoding-Fehler für '{place_name}': {exc}") from exc

    if not results:
        return None
    r = results[0]
    return {
        "lat": float(r["lat"]),
        "lon": float(r["lon"]),
        "display_name": r.get("display_name", place_name),
    }


def _parse_coords(s: str) -> Optional[tuple[float, float]]:
    """'lat,lon'-String → (lat, lon) oder None wenn kein gültiges Format."""
    parts = s.strip().split(",")
    if len(parts) == 2:
        try:
            return float(parts[0].strip()), float(parts[1].strip())
        except ValueError:
            pass
    return None


def _resolve_place(place: str) -> tuple[float, float, str]:
    """Ortsname oder 'lat,lon'-String → (lat, lon, display_name).

    Wirft RuntimeError wenn der Ort nicht aufgelöst werden kann.
    """
    coords = _parse_coords(place)
    if coords is not None:
        return coords[0], coords[1], place
    loc = geocode_place(place)
    if loc is None:
        raise RuntimeError(f"Ort nicht gefunden: '{place}'")
    return loc["lat"], loc["lon"], loc["display_name"]


# ---------------------------------------------------------------------------
# Routing (OSRM)
# ---------------------------------------------------------------------------

def _format_duration(seconds: float) -> str:
    """Sekunden → lesbarer String (z.B. '2 Std. 15 Min.')."""
    minutes = int(seconds / 60)
    hours, mins = divmod(minutes, 60)
    if hours > 0:
        return f"{hours} Std. {mins} Min." if mins > 0 else f"{hours} Std."
    return f"{mins} Min."


def _normalize_mode(raw: str) -> str:
    """Alias → Modus-Key ('auto', 'fahrrad', 'fuss')."""
    key = raw.lower().strip()
    result = _MODE_ALIAS.get(key)
    if result is None:
        raise ValueError(
            f"Unbekannter Modus: '{raw}'. Gültige Modi: {', '.join(sorted(OSRM_SERVERS))}"
        )
    return result


def get_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    mode: str = "auto",
) -> dict:
    """Route via OSRM berechnen.

    Parameters
    ----------
    start_lat, start_lon: Startkoordinaten (WGS84)
    end_lat, end_lon:     Zielkoordinaten (WGS84)
    mode:                 'auto', 'fahrrad' oder 'fuss'

    Returns
    -------
    dict mit:
      distance_km, duration_seconds, duration_str,
      mode, mode_label, mode_icon, start_coords, end_coords
    """
    mode = _normalize_mode(mode)
    base = OSRM_SERVERS[mode]
    # OSRM-Format: lon,lat (NICHT lat,lon)
    coords = f"{start_lon},{start_lat};{end_lon},{end_lat}"
    url = f"{base}/{coords}?overview=false"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"OSRM-Fehler: {exc}") from exc

    if data.get("code") != "Ok" or not data.get("routes"):
        raise RuntimeError(f"OSRM: Keine Route gefunden (Code: {data.get('code')})")

    route = data["routes"][0]
    dist_km = route["distance"] / 1000.0
    duration_sec = route["duration"]

    return {
        "distance_km": round(dist_km, 1),
        "duration_seconds": duration_sec,
        "duration_str": _format_duration(duration_sec),
        "mode": mode,
        "mode_label": MODE_LABELS[mode],
        "mode_icon": MODE_ICONS[mode],
        "start_coords": (start_lat, start_lon),
        "end_coords": (end_lat, end_lon),
    }


def get_route_text(
    start: str,
    end: str,
    mode: str = "auto",
) -> str:
    """Lesbare Routenbeschreibung von Start nach Ziel (Ortsnamen oder Koordinaten).

    Geocodiert Ortsnamen automatisch.
    """
    start_lat, start_lon, start_name = _resolve_place(start)
    end_lat, end_lon, end_name = _resolve_place(end)

    info = get_route(start_lat, start_lon, end_lat, end_lon, mode=mode)
    icon = info["mode_icon"]
    label = info["mode_label"]
    dist = info["distance_km"]
    dur = info["duration_str"]

    # Kurze Anzeigenamen (vor erstem Komma)
    def short(name: str) -> str:
        return name.split(",")[0].strip()

    return (
        f"{icon} {label}: {short(start_name)} → {short(end_name)}\n"
        f"   Distanz: {dist} km\n"
        f"   Fahrzeit: {dur}"
    )


# ---------------------------------------------------------------------------
# CLI / main
# ---------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="reiseroute_core",
        description="Routenplanung via OSRM (Open Source Routing Machine).",
    )
    parser.add_argument("start", nargs="?", help="Startort oder 'lat,lon'")
    parser.add_argument("ziel", nargs="?", help="Zielort oder 'lat,lon'")
    parser.add_argument(
        "--modus",
        default="auto",
        metavar="MODUS",
        help="Verkehrsmittel: auto (Standard), fahrrad, fuss",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Ausgabe als JSON",
    )

    args = parser.parse_args(argv)

    if not args.start or not args.ziel:
        parser.print_help()
        return 1

    try:
        if args.as_json:
            start_lat, start_lon, start_name = _resolve_place(args.start)
            end_lat, end_lon, end_name = _resolve_place(args.ziel)
            info = get_route(start_lat, start_lon, end_lat, end_lon, mode=args.modus)
            info["start_name"] = start_name
            info["end_name"] = end_name
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            text = get_route_text(args.start, args.ziel, mode=args.modus)
            print(text)
    except (RuntimeError, ValueError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
