---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: >
  Answers weather questions for a location or coordinates via wttr.in
  (free, no API key). Current weather + 3-day forecast. Location comes
  from the user request or preferences; optional short cache.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: assist
tags: [wetter, wttr, vorschau, assist]
language: en
status: active

dependencies:
  tools: [wetter_core.py]
  services: []
  protocols: []
  python: [urllib, json]

provenance:
  origin: "bach"
  origin_path: "system/hub/_services/weather/weather_service.py"
  origin_version: "1.0"
  origin_repo: "github.com/ellmos-ai/bach"
  origin_license: "MIT"
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Weather

Fast, key-free weather information for everyday use.

## Purpose

Answers "What will the weather be like?" questions without an API key (data source: wttr.in).
Delivers current weather (temperature, feels-like, wind, humidity, UV) plus a
compact 3-day forecast. **User-neutral:** no fixed location in the code — the location
comes from the request or from `assist/prefs.json` (`wetter_default_location`),
which the LLM fills in interactively with the user.

## Triggers

| User input | Action |
|---|---|
| "Weather for Potsdam?" / "What will the weather be like in Hamburg?" | `wetter_core.py "<location>"` |
| "Weather tomorrow?" (without location) | `wetter_core.py --default` (location from prefs) |
| "My default weather location is Potsdam" | `wetter_core.py --set-default "Potsdam"` |
| Coordinates known | `wetter_core.py <lat> <lon>` |

## Workflow

```
1. Determine location: from request; else prefs.json (wetter_default_location);
   else ask user interactively + optionally save as default.
2. Query wetter_core.py (wttr.in, 2 attempts, 30-min cache).
3. Present readable weather text + 3-day forecast.
```

## CLI Entry Point (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # location
python wetter_core.py 52.6789 13.5878   # coordinates
python wetter_core.py --default         # location from prefs.json
python wetter_core.py --set-default "Potsdam"
```

## Store (optional)

- **No mandatory store.** Optional short cache `assist/wetter/.cache.json`
  (TTL 30 min, best-effort) — avoids repeated network calls.
- Location preference in `assist/prefs.json` (`wetter_default_location`).

## Attitude

We use wttr.in as the key-free default source, but are open to other weather
backends (e.g. DWD/OpenWeather) if the user prefers them.

## Privacy

- Only the location name/coordinates go to wttr.in (required for the query).
- No telemetry, no account. Cache + preference stay local.

## Related Resources

- `assist/AGENTS.md` — Umbrella router
- `assist/reiseroute/` — uses weather for travel planning (planned)

## Changelog

### 0.1.0 (2026-06-22)
- Initial version. Ported from BACH `hub/_services/weather/weather_service.py` (MIT).
- Extended: location name support (not just coordinates), 3-day forecast,
  optional cache, prefs-based default location. User-neutral.
