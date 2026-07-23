"""location_suche_core.py — Ort-/POI-Suche via OpenStreetMap (standalone, stdlib only).

Portiert aus BACH system/agents/persoenlicher-assistent/tools/location_search.py v1.1.0.
Entfernt: save_location, list_locations, _ensure_table, _get_db, Origin-DB-Abhaengigkeit.
Behaelt: geocode, search, search_nearby (Nominatim + Overpass).
"""
from __future__ import annotations

import json
import math
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

# ---------------------------------------------------------------------------
# Konstanten
# ---------------------------------------------------------------------------

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
USER_AGENT = "location-suche-skill/1.0 (github.com/ellmos-ai/skills)"

# Bekannte OSM-Amenity-Kategorien (Overpass-Typ)
OVERPASS_CATEGORIES = {
    "restaurant", "cafe", "bar", "pub", "fast_food",
    "hotel", "hostel", "guest_house",
    "supermarket", "pharmacy", "hospital",
    "bank", "atm", "fuel", "parking",
    "bus_stop", "train_station",
    "museum", "cinema", "theatre", "library",
    "school", "university", "church",
}

# Deutsche Alias-Begriffe → OSM-Kategorie
_DE_ALIAS: dict[str, str] = {
    "restaurant": "restaurant",
    "restaurants": "restaurant",
    "café": "cafe",
    "cafes": "cafe",
    "cafés": "cafe",
    "kaffee": "cafe",
    "bar": "bar",
    "bars": "bar",
    "kneipe": "pub",
    "kneipen": "pub",
    "pub": "pub",
    "pubs": "pub",
    "imbiss": "fast_food",
    "fast food": "fast_food",
    "hotel": "hotel",
    "hotels": "hotel",
    "hostel": "hostel",
    "pension": "guest_house",
    "supermarkt": "supermarket",
    "apotheke": "pharmacy",
    "apotheken": "pharmacy",
    "krankenhaus": "hospital",
    "klinik": "hospital",
    "bank": "bank",
    "banken": "bank",
    "geldautomat": "atm",
    "tankstelle": "fuel",
    "parkplatz": "parking",
    "bushaltestelle": "bus_stop",
    "bahnhof": "train_station",
    "museum": "museum",
    "kino": "cinema",
    "theater": "theatre",
    "bibliothek": "library",
    "schule": "school",
    "universität": "university",
    "kirche": "church",
}

_last_nominatim_call: float = 0.0


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _rate_limit() -> None:
    """Nominatim erlaubt max. 1 Anfrage/Sekunde."""
    global _last_nominatim_call
    elapsed = time.time() - _last_nominatim_call
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _last_nominatim_call = time.time()


def _nominatim_request(params: dict) -> list[dict]:
    """Nominatim-API aufrufen; gibt Liste von Ergebnis-Dicts zurück."""
    _rate_limit()
    params["format"] = "json"
    params["limit"] = params.get("limit", 5)
    url = NOMINATIM_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Nominatim-Fehler: {exc}") from exc


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Luftlinie in Metern zwischen zwei WGS84-Koordinaten."""
    r = 6_371_000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _format_distance(meters: float) -> str:
    if meters < 1000:
        return f"{int(meters)} m"
    return f"{meters / 1000:.1f} km"


def _normalize_category(raw: str) -> Optional[str]:
    """Deutschen oder englischen Begriff → OSM-Kategorie; None wenn unbekannt."""
    key = raw.lower().strip()
    if key in OVERPASS_CATEGORIES:
        return key
    return _DE_ALIAS.get(key)


# ---------------------------------------------------------------------------
# Öffentliche API
# ---------------------------------------------------------------------------

def geocode(address: str) -> Optional[dict]:
    """Adresse/Ortsname → {'lat': float, 'lon': float, 'display_name': str}.

    Gibt None zurück wenn kein Ergebnis gefunden wurde.
    """
    results = _nominatim_request({"q": address, "limit": 1})
    if not results:
        return None
    r = results[0]
    return {
        "lat": float(r["lat"]),
        "lon": float(r["lon"]),
        "display_name": r.get("display_name", address),
    }


def search_nearby(
    lat: float,
    lon: float,
    category: str,
    radius: int = 1000,
    limit: int = 10,
) -> list[dict]:
    """POIs via Overpass-API in `radius` Metern um (lat, lon).

    Gibt Liste von Dicts zurück:
      {'name', 'lat', 'lon', 'address', 'distance_m', 'distance_str', 'osm_id'}
    """
    cat = _normalize_category(category)
    if cat is None:
        raise ValueError(f"Unbekannte Kategorie: '{category}'. Bekannt: {sorted(OVERPASS_CATEGORIES)}")

    # Overpass QL — Nodes und Ways
    query = (
        f"[out:json][timeout:25];"
        f"("
        f"  node[\"amenity\"=\"{cat}\"](around:{radius},{lat},{lon});"
        f"  way[\"amenity\"=\"{cat}\"](around:{radius},{lat},{lon});"
        f"  node[\"tourism\"=\"{cat}\"](around:{radius},{lat},{lon});"
        f"  way[\"tourism\"=\"{cat}\"](around:{radius},{lat},{lon});"
        f");"
        f"out center {limit * 2};"  # mehr holen, dann nach Distanz sortieren
    )
    data = urllib.parse.urlencode({"data": query}).encode()
    req = urllib.request.Request(OVERPASS_URL, data=data, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Overpass-Fehler: {exc}") from exc

    results = []
    for el in raw.get("elements", []):
        # Koordinaten: Node hat lat/lon direkt, Way hat center
        if el["type"] == "node":
            el_lat, el_lon = el.get("lat"), el.get("lon")
        else:
            center = el.get("center", {})
            el_lat, el_lon = center.get("lat"), center.get("lon")
        if el_lat is None or el_lon is None:
            continue

        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("name:de") or "(ohne Namen)"
        # Adresse aus Tags zusammensetzen
        addr_parts = [
            tags.get("addr:street", ""),
            tags.get("addr:housenumber", ""),
            tags.get("addr:city", ""),
        ]
        address = " ".join(p for p in addr_parts if p).strip() or "Adresse unbekannt"

        dist = _haversine_m(lat, lon, el_lat, el_lon)
        results.append({
            "name": name,
            "lat": el_lat,
            "lon": el_lon,
            "address": address,
            "distance_m": dist,
            "distance_str": _format_distance(dist),
            "osm_id": f"{el['type']}/{el['id']}",
        })

    results.sort(key=lambda x: x["distance_m"])
    return results[:limit]


def search(query: str, near: Optional[str] = None, limit: int = 5) -> list[dict]:
    """Kombinierte Suche: Kategorie+Ort → search_nearby; sonst Nominatim-Freitext.

    Gibt Liste von Dicts zurück (Format abhängig vom Pfad):
    - Overpass: {'name', 'lat', 'lon', 'address', 'distance_m', 'distance_str', 'osm_id'}
    - Nominatim: {'name', 'lat', 'lon', 'address', 'display_name'}
    """
    cat = _normalize_category(query)
    if cat is not None and near:
        # Kategorie + Ort: erst Ort geocodieren, dann Overpass
        loc = geocode(near)
        if loc is None:
            raise RuntimeError(f"Ort '{near}' nicht gefunden.")
        return search_nearby(loc["lat"], loc["lon"], cat, limit=limit)

    # Freitext: Nominatim
    full_query = f"{query} {near}" if near else query
    results = _nominatim_request({"q": full_query, "limit": limit})
    out = []
    for r in results:
        out.append({
            "name": r.get("name") or r.get("display_name", "").split(",")[0],
            "lat": float(r["lat"]),
            "lon": float(r["lon"]),
            "address": r.get("display_name", ""),
            "display_name": r.get("display_name", ""),
        })
    return out


# ---------------------------------------------------------------------------
# CLI / main
# ---------------------------------------------------------------------------

def _print_results(results: list[dict]) -> None:
    if not results:
        print("Keine Ergebnisse gefunden.")
        return
    for i, r in enumerate(results, 1):
        dist = f"  ({r['distance_str']})" if "distance_str" in r else ""
        print(f"{i:2}. {r['name']}{dist}")
        addr = r.get("address") or r.get("display_name", "")
        if addr and addr != "Adresse unbekannt":
            print(f"    {addr}")
        print(f"    {r['lat']:.5f}, {r['lon']:.5f}  [osm:{r.get('osm_id', '')}]")


def main(argv: Optional[list] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="location_suche_core",
        description="Ort-/POI-Suche via OpenStreetMap (Nominatim + Overpass).",
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Suchanfrage (z.B. 'restaurant' oder Freitext 'Eiffelturm Paris')",
    )
    parser.add_argument(
        "near",
        nargs="?",
        help="Ort für POI-Suche (z.B. 'München')",
    )
    parser.add_argument(
        "--geocode",
        metavar="ADRESSE",
        help="Adresse geocodieren (Koordinaten ausgeben)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=1000,
        metavar="METER",
        help="Suchradius in Metern (Standard: 1000)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        metavar="N",
        help="Max. Ergebnisse (Standard: 5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Ausgabe als JSON",
    )

    args = parser.parse_args(argv)

    try:
        if args.geocode:
            result = geocode(args.geocode)
            if result is None:
                print(f"Ort nicht gefunden: {args.geocode}", file=sys.stderr)
                return 1
            if args.as_json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"Ort:   {result['display_name']}")
                print(f"Lat:   {result['lat']}")
                print(f"Lon:   {result['lon']}")
            return 0

        if not args.query:
            parser.print_help()
            return 1

        # POI-Suche mit gesondertem Radius-Argument (nur wenn Kategorie erkannt)
        cat = _normalize_category(args.query)
        if cat is not None and args.near:
            loc = geocode(args.near)
            if loc is None:
                print(f"Ort '{args.near}' nicht gefunden.", file=sys.stderr)
                return 1
            results = search_nearby(loc["lat"], loc["lon"], cat, radius=args.radius, limit=args.limit)
        else:
            results = search(args.query, near=args.near, limit=args.limit)

        if args.as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            _print_results(results)

    except RuntimeError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
