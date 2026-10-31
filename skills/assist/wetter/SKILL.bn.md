---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "আবহাওয়া প্রশ্নের উত্তর দেয় কোনো স্থান বা স্থানাঙ্কের জন্য wttr.in-এর মাধ্যমে (বিনামূল্যে, কোনো API key লাগে না)। বর্তমান আবহাওয়া + ৩-দিনের পূর্বাভাস। স্থান আসে ব্যবহারকারীর অনুরোধ বা পছন্দ থেকে; ঐচ্ছিক সংক্ষিপ্ত cache।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: bn
status: active
visibility: public
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 77159e7ab4dc0541cb58d038cfb353076dc2d32699dba8cd2e69761042b86b8c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="wetter banner">

# আবহাওয়া

দৈনন্দিন ব্যবহারের জন্য দ্রুত, API key ছাড়া আবহাওয়ার তথ্য।

## উদ্দেশ্য

API key ছাড়াই „আবহাওয়া কেমন হবে?" ধরনের প্রশ্নের উত্তর দেয় (তথ্যের উৎস: wttr.in)।
বর্তমান আবহাওয়া (তাপমাত্রা, অনুভূত তাপমাত্রা, বাতাস, আর্দ্রতা, UV) এবং একটি সংক্ষিপ্ত
৩-দিনের পূর্বাভাস দেয়। **ব্যবহারকারী-নিরপেক্ষ:** কোডে কোনো নির্দিষ্ট অবস্থান স্থির করা নেই — স্থান আসে
অনুরোধ থেকে বা `assist/prefs.json` (`wetter_default_location`) থেকে, যা LLM ব্যবহারকারীর সঙ্গে কথোপকথনের মাধ্যমে পূরণ করে।

## ট্রিগার

| ব্যবহারকারীর ইনপুট | ক্রিয়া |
|---|---|
| „Potsdam-এ আবহাওয়া কেমন?" / „Hamburg-এ আবহাওয়া কেমন হবে?" | `wetter_core.py "<Ort>"` |
| „কাল আবহাওয়া কেমন?" (স্থান ছাড়া) | `wetter_core.py --default` (স্থান prefs থেকে) |
| „আমার ডিফল্ট আবহাওয়ার স্থান Potsdam" | `wetter_core.py --set-default "Potsdam"` |
| স্থানাঙ্ক জানা থাকলে | `wetter_core.py <lat> <lon>` |

## কার্যপ্রবাহ

```
1. Ort bestimmen: aus Anfrage; sonst prefs.json (wetter_default_location);
   sonst Nutzer interaktiv fragen + optional als Default speichern.
2. wetter_core.py abfragen (wttr.in, 2 Versuche, 30-min-Cache).
3. Lesbaren Wetter-Text + 3-Tage-Vorschau praesentieren.
```

## CLI ব্যবহার শুরু (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # Ort
python wetter_core.py 52.6789 13.5878   # Koordinaten
python wetter_core.py --default         # Ort aus prefs.json
python wetter_core.py --set-default "Potsdam"
```

## Store (ঐচ্ছিক)

- **বাধ্যতামূলক Store নেই।** ঐচ্ছিক সংক্ষিপ্ত cache `assist/wetter/.cache.json`
  (TTL 30 মিনিট, best-effort) — বারবার নেটওয়ার্ক অনুরোধ এড়ায়।
- স্থানের পছন্দ `assist/prefs.json`-এ থাকে (`wetter_default_location`)।

## দৃষ্টিভঙ্গি

আমরা wttr.in-কে কী-বিহীন ডিফল্ট উৎস হিসেবে ব্যবহার করি, তবে ব্যবহারকারী চাইলে অন্য আবহাওয়া
backend (যেমন DWD/OpenWeather)-এর জন্যও আমরা উন্মুক্ত।

## গোপনীয়তা

- শুধু স্থানের নাম/স্থানাঙ্ক wttr.in-এ যায় (অনুরোধের জন্য প্রয়োজনীয়)।
- কোনো telemetry নেই, কোনো অ্যাকাউন্ট নেই। Cache ও পছন্দ স্থানীয়ভাবে থাকে।

## সংশ্লিষ্ট সম্পদ

- `assist/AGENTS.md` — Umbrella router
- `assist/reiseroute/` — ভ্রমণ পরিকল্পনায় প্রয়োজনে আবহাওয়া ব্যবহার করে (পরিকল্পিত)

## পরিবর্তনের ইতিহাস

### 0.1.0 (2026-06-22)
- প্রাথমিক সংস্করণ। BACH `hub/_services/weather/weather_service.py` (MIT) থেকে পোর্ট করা হয়েছে।
- উন্নত করা হয়েছে: স্থানের নাম সমর্থন (শুধু স্থানাঙ্ক নয়), ৩-দিনের পূর্বাভাস,
  ঐচ্ছিক cache, prefs-ভিত্তিক ডিফল্ট স্থান। ব্যবহারকারী-নিরপেক্ষ।
