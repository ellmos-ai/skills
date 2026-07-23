#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
wetter_core.py — Headless Wetter-Abfrage via wttr.in (kein API-Key).

Portiert aus: BACH hub/_services/weather/weather_service.py (MIT, wttr.in-Logik)
Store:        OPTIONAL — kurzlebiger JSON-Cache (assist/wetter/.cache.json), kein Pflicht-Store
Abhaengigkeit: nur Python-Stdlib (urllib, json) — kein BACH-Import, kein API-Key

Userneutral: KEIN hardcodierter Standort. Ort kommt als Argument oder aus den
Nutzerpraeferenzen (assist/prefs.json -> "wetter_default_location"). wttr.in
akzeptiert sowohl Ortsnamen ("Potsdam") als auch Koordinaten ("52.52,13.41").

Verwendung (CLI):
  python wetter_core.py "Potsdam"             # Wetter fuer Ort
  python wetter_core.py 52.6789 13.5878      # Wetter fuer Koordinaten
  python wetter_core.py --default            # Ort aus prefs.json
  python wetter_core.py --set-default "Potsdam"
"""

from __future__ import annotations

import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Optional

# --- Pfade (userneutral, relativ zum Skill) -------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_CACHE_FILE = _SKILL_DIR / ".cache.json"
_CACHE_TTL_SECONDS = 1800  # 30 min — Wetter aendert sich langsam


def _prefs_file() -> Optional[Path]:
    """assist/prefs.json (eine Ebene ueber den Skill-Ordnern)."""
    p = _SKILL_DIR.parent / "prefs.json"
    return p if p.exists() else None


def _read_pref(key: str) -> Optional[str]:
    pf = _prefs_file()
    if not pf:
        return None
    try:
        return json.loads(pf.read_text(encoding="utf-8")).get(key)
    except (json.JSONDecodeError, OSError):
        return None


def _write_pref(key: str, value: str) -> None:
    p = _SKILL_DIR.parent / "prefs.json"
    data = {}
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    data[key] = value
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# --- Wetter-Symbole (Teilmenge, wttr.in weatherCode) ----------------------

_ICONS = {
    "113": "☀️", "116": "⛅", "119": "☁️", "122": "☁️", "143": "🌫️",
    "176": "🌦️", "179": "🌨️", "182": "🌧️", "200": "⛈️", "230": "❄️",
    "248": "🌫️", "266": "🌦️", "293": "🌦️", "296": "🌧️", "302": "🌧️",
    "320": "🌨️", "338": "❄️", "353": "🌦️", "356": "🌧️", "386": "⛈️",
}


# --- Cache (optionaler Store) ---------------------------------------------

def _cache_get(location: str) -> Optional[dict]:
    if not _CACHE_FILE.exists():
        return None
    try:
        cache = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    entry = cache.get(location.lower())
    if not entry:
        return None
    age = (datetime.now().timestamp() - entry.get("_ts", 0))
    return entry.get("data") if age < _CACHE_TTL_SECONDS else None


def _cache_put(location: str, data: dict) -> None:
    cache = {}
    if _CACHE_FILE.exists():
        try:
            cache = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cache = {}
    cache[location.lower()] = {"_ts": datetime.now().timestamp(), "data": data}
    try:
        _CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass  # Cache ist best-effort


# --- Abruf ----------------------------------------------------------------

def get_weather(location: str, lang: str = "de", use_cache: bool = True) -> Optional[dict]:
    """Ruft Wetterdaten von wttr.in ab. location = Ortsname ODER 'lat,lon'."""
    if use_cache:
        cached = _cache_get(location)
        if cached:
            cached["_cached"] = True
            return cached

    loc_q = urllib.parse.quote(location.strip())
    url = f"https://wttr.in/{loc_q}?format=j1&lang={lang}"

    last_err = None
    for _ in range(2):  # 2 Versuche (SSL-Kaltstart)
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "ellmos-assist-wetter/0.1 (+sovereign)"}
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            last_err = None
            break
        except urllib.error.URLError as e:
            last_err = {"error": f"Netzwerkfehler: {e}"}
        except Exception as e:  # noqa: BLE001 — best-effort Wetter
            last_err = {"error": f"Fehler: {e}"}
    if last_err:
        return last_err

    try:
        cc = raw["current_condition"][0]
        area = raw.get("nearest_area", [{}])[0]
        area_name = area.get("areaName", [{}])[0].get("value", location)
        country = area.get("country", [{}])[0].get("value", "?")
        code = str(cc.get("weatherCode", "113"))
        desc = cc.get("weatherDesc", [{}])[0].get("value", "?")
        for entry in cc.get("lang_de", []):
            if entry.get("value"):
                desc = entry["value"]
                break
        data = {
            "location_name": area_name,
            "country": country,
            "temp_c": int(cc.get("temp_C", 0)),
            "feels_like_c": int(cc.get("FeelsLikeC", 0)),
            "humidity": int(cc.get("humidity", 0)),
            "windspeed_kmph": int(cc.get("windspeedKmph", 0)),
            "description": desc,
            "icon": _ICONS.get(code, "🌡️"),
            "uv_index": int(cc.get("uvIndex", 0)),
        }
        # 3-Tage-Vorschau (kompakt)
        forecast = []
        for day in raw.get("weather", [])[:3]:
            forecast.append({
                "date": day.get("date"),
                "min_c": int(day.get("mintempC", 0)),
                "max_c": int(day.get("maxtempC", 0)),
            })
        data["forecast"] = forecast
        if use_cache:
            _cache_put(location, data)
        return data
    except (KeyError, IndexError, ValueError) as e:
        return {"error": f"Parse-Fehler: {e}"}


def get_weather_text(location: str) -> str:
    """Lesbarer Wetter-String (fuer LLM-Prompt-Injektion)."""
    w = get_weather(location)
    if not w or "error" in w:
        err = w.get("error", "unbekannt") if w else "Timeout"
        return f"[Wetter: nicht verfuegbar — {err}]"
    lines = [
        f"{w['icon']} Wetter in {w['location_name']}, {w['country']}"
        + (" (Cache)" if w.get("_cached") else "") + ":",
        f"Temperatur: {w['temp_c']:+d}°C (gefuehlt: {w['feels_like_c']:+d}°C) | {w['description']}",
        f"Wind: {w['windspeed_kmph']} km/h | Luftfeuchte: {w['humidity']}% | UV: {w['uv_index']}",
    ]
    if w.get("forecast"):
        fc = " | ".join(f"{d['date']}: {d['min_c']}–{d['max_c']}°C" for d in w["forecast"])
        lines.append(f"Vorschau: {fc}")
    return "\n".join(lines)


# --- CLI ------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 0

    if argv[0] == "--set-default":
        if len(argv) < 2:
            print("Verwendung: wetter_core.py --set-default <Ort>")
            return 1
        loc = " ".join(argv[1:])
        _write_pref("wetter_default_location", loc)
        print(f"[wetter] Standort-Praeferenz gesetzt: {loc}")
        return 0

    if argv[0] == "--default":
        loc = _read_pref("wetter_default_location")
        if not loc:
            print("[wetter] Kein Standard-Ort in prefs.json. Setze einen mit:")
            print('         python wetter_core.py --set-default "Potsdam"')
            return 1
    elif len(argv) == 2 and _is_float(argv[0]) and _is_float(argv[1]):
        loc = f"{argv[0]},{argv[1]}"  # Koordinaten
    else:
        loc = " ".join(argv)

    print(get_weather_text(loc))
    return 0


def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
