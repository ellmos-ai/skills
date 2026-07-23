---
name: reiseroute
version: 1.0.0
category: assist
description: >
  Route planning from A to B via OSRM (Open Source Routing Machine).
  Supports car, bicycle and pedestrian. No API key required.
tags:
  - routing
  - navigation
  - osrm
  - openstreetmap
  - reise
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
runtime: python3
entry_point: reiseroute_core.py
provenance:
  origin: BACH hub routing-service
  origin_path: system/hub/_services/routing/routing_service.py
  origin_version: "1.0"
  origin_repo: github.com/ellmos-ai/bach
  origin_license: MIT
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: >
    urllib.parse-Import an den Kopf verschoben (war im Original nur im else-Zweig).
    geocode_place (Nominatim) integriert. Keine Origin-DB. Kein Store.
    Userneutral, headless, nur Stdlib.
---

# Travel Route

**Route planning via OSRM (Open Source Routing Machine)**

---

## Overview

Plans routes between two locations (names or coordinates) via the public
OSRM service (`router.project-osrm.org`). Returns distance, travel time and
mode of transport. No API key, no account required.

---

## Triggers

| Phrase | Action |
|---|---|
| "Plan the route from Berlin to Hamburg" | Car route, geocode place names |
| "How long does the drive from Munich to Vienna take by car?" | Car route + time |
| "Cycle route from Potsdam to Berlin" | Bicycle mode |
| "Walk from Kreuzberg to Mitte, Berlin" | Pedestrian mode |
| "Route from 52.52,13.41 to 53.55,9.99" | Direct coordinates |

---

## Workflow

1. **Extract start and destination** from the user input.
2. **Detect mode:** car (default), bicycle, foot.
3. **Geocode:** place names → coordinates via Nominatim.
4. **Query OSRM:** returns distance (km) + duration (formatted).
5. **Output result:** concise text summary.

---

## CLI

```bash
# Car route between two places
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# Bicycle
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# On foot
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Coordinates directly (lat,lon)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# JSON output
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Munich" "Vienna" --json

# Help
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## Modes

| Mode | Alias | OSRM profile |
|---|---|---|
| auto (default) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Store

No persistent store. Routes are not saved.

---

## Attitude

- Always name start and destination before calculating.
- Clarify if a place is ambiguous (e.g. "Vienna" = Austria or a city of the same name?).
- Note: OSRM provides the fastest route without real-time traffic.
- Issue a note for very long pedestrian routes (> 20 km).

---

## Privacy

Requests go to `nominatim.openstreetmap.org` (geocoding) and
`router.project-osrm.org` (routing). No login, no API key,
no persistent data storage.

---

## Related Resources

- `location-suche` — POI search (also uses Nominatim)
- `wetter` — weather at the destination

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-06-22 | Created from BACH routing_service.py v1.0; geocoding integrated |
