---
name: location-suche
version: 1.0.0
category: assist
description: >
  Location, restaurant and hotel search via OpenStreetMap (Nominatim + Overpass API).
  Returns POIs (Points of Interest) near a location or searches by free text.
tags:
  - location
  - openstreetmap
  - poi
  - nominatim
  - overpass
  - restaurant
  - hotel
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages:
  - de
  - en
dependencies:
  python:
    - urllib.request
    - urllib.parse
    - urllib.error
    - json
    - time
runtime: python3
entry_point: location_suche_core.py
provenance:
  origin: BACH persoenlicher-assistent
  origin_path: system/agents/persoenlicher-assistent/tools/location_search.py
  origin_version: "1.1.0"
  origin_repo: github.com/ellmos-ai/bach
  origin_license: MIT
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: >
    Alle Origin-DB-Abhaengigkeiten entfernt (save_location, list_locations,
    _ensure_table, _get_db). Kein Store. Userneutral (keine privaten Pfade).
    Headless, nur Stdlib.
---

# Location Search

**Location, restaurant and hotel search via OpenStreetMap**

---

## Overview

Searches for restaurants, hotels, cafes and other places using the
OpenStreetMap services Nominatim (geocoding) and Overpass (POI search).
No API key required. No persistent store.

---

## Triggers

| Phrase | Action |
|---|---|
| "Find a restaurant in Munich" | POI search: category=restaurant, near=Munich |
| "Hotels near Vienna" | POI search: category=hotel, near=Vienna |
| "Where is the Eiffel Tower?" | Nominatim free-text search |
| "Find cafes in Berlin" | POI search: category=cafe, near=Berlin |
| "Search for pharmacy near Potsdam" | POI search: category=pharmacy, near=Potsdam |

---

## Workflow

1. **Detect trigger:** Does the request contain a category (restaurant, hotel etc.)
   and a location → step 2. Otherwise free text → step 4.
2. **Geocode location:** Nominatim provides coordinates for the named location.
3. **Search POIs:** Overpass API searches for venues of the category within radius.
4. **Display result:** List with name, address, distance (m).
5. **Free-text search (fallback):** Nominatim free-text provides direct hits.

---

## CLI

```bash
# POI search (category + location)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Geocode location
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburg Gate Berlin"

# Adjust radius (default: 1000 m)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Help
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## Store

No persistent store. Results are only displayed, not saved.

---

## Supported Categories

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## Attitude

- Always ask the user for a location if none was given.
- With more than 10 results only show the 5 nearest, rest on request.
- State distance in metres, from 1 km in km (1 decimal place).
- Privacy: no location data is stored or transmitted except to the
  public Nominatim/Overpass API (openstreetmap.org).

---

## Privacy

Search requests go to `nominatim.openstreetmap.org` and `overpass-api.de`.
No login, no API key, no persistent data storage.
User-Agent is set according to Nominatim policy.

---

## Related Resources

- `reiseroute` — route planning from A to B (also uses Nominatim for geocoding)
- `wetter` — weather at current location

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-06-22 | Created from BACH location_search.py v1.1.0; store removed |
