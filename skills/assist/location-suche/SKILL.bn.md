---
name: location-suche
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "OpenStreetMap-এর মাধ্যমে অবস্থান, রেস্টুরেন্ট ও হোটেল অনুসন্ধান (Nominatim + Overpass API)। কোনো অবস্থানের কাছাকাছি POI (Points of Interest) ফেরত দেয় অথবা মুক্ত টেক্সটে অনুসন্ধান করে।"
tags: [location, openstreetmap, poi, nominatim, overpass, restaurant, hotel]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json', 'time']}
runtime: python3
entry_point: location_suche_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/location_search.py', 'origin_version': '1.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (save_location, list_locations, _ensure_table, _get_db). Kein Store. Userneutral (keine privaten Pfade). Headless, nur Stdlib.\n'}
language: bn
visibility: public
translated_from_sha256: 93e16b5f7ddbd85797fd294d2251bb04189db2ac6f5f88f4061cc69b6189e0ba
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="location-suche banner">

# অবস্থান-অনুসন্ধান

**OpenStreetMap-এর মাধ্যমে অবস্থান, রেস্টুরেন্ট ও হোটেল অনুসন্ধান**

---

## সংক্ষিপ্ত বিবরণ

OpenStreetMap-এর পরিষেবা Nominatim (Geocoding) এবং Overpass (POI-অনুসন্ধান) ব্যবহার করে
রেস্টুরেন্ট, হোটেল, ক্যাফে এবং অন্যান্য স্থান খোঁজা হয়।
কোনো API-Key প্রয়োজন নেই। কোনো স্থায়ী Store নেই।

---

## ট্রিগার

| বাক্যাংশ | কার্য |
|---|---|
| „München-এ একটি রেস্টুরেন্ট খোঁজো" | POI-অনুসন্ধান: category=restaurant, near=München |
| „Wien-এর কাছে হোটেল" | POI-অনুসন্ধান: category=hotel, near=Wien |
| „Eiffelturm কোথায়?" | Nominatim-মুক্ত টেক্সট-অনুসন্ধান |
| „Berlin-এ ক্যাফে খোঁজো" | POI-অনুসন্ধান: category=cafe, near=Berlin |
| „Potsdam-এর কাছে ফার্মেসি খোঁজো" | POI-অনুসন্ধান: category=pharmacy, near=Potsdam |

---

## কার্যপ্রবাহ

1. **ট্রিগার শনাক্ত করা:** অনুরোধে যদি একটি বিভাগ (রেস্টুরেন্ট, হোটেল ইত্যাদি)
   এবং একটি স্থান থাকে → ধাপ 2। অন্যথায় মুক্ত টেক্সট → ধাপ 4।
2. **স্থানের Geocoding:** Nominatim উল্লিখিত স্থানের স্থানাঙ্ক দেয়।
3. **POI খোঁজা:** Overpass-API পরিধির মধ্যে ওই বিভাগের প্রতিষ্ঠান খোঁজে।
4. **ফলাফল দেখানো:** নাম, ঠিকানা, দূরত্ব (m) সহ তালিকা প্রদর্শন।
5. **মুক্ত টেক্সট-অনুসন্ধান (বিকল্প):** Nominatim-মুক্ত টেক্সট সরাসরি মিল দেয়।

---

## CLI

```bash
# POI-Suche (Kategorie + Ort)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Ort geocodieren
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburger Tor Berlin"

# Radius anpassen (Standard: 1000 m)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## Store

কোনো স্থায়ী Store নেই। ফলাফল শুধু দেখানো হয়, সংরক্ষণ করা হয় না।

---

## সমর্থিত বিভাগসমূহ

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## নীতি

- কোনো স্থান উল্লেখ না থাকলে সবসময় ব্যবহারকারীকে স্থানটি জিজ্ঞাসা করুন।
- 10টির বেশি ফলাফল হলে কেবল নিকটতম 5টি দেখান, বাকিগুলো অনুরোধে।
- দূরত্ব মিটারে উল্লেখ করুন, 1 km থেকে কিলোমিটারে (1 দশমিক স্থান)।
- গোপনীয়তা: কোনো অবস্থান-তথ্য সংরক্ষিত বা প্রেরিত হয় না, শুধু
  জনসাধারণের Nominatim/Overpass-API (openstreetmap.org)-এ ছাড়া।

---

## গোপনীয়তা

অনুসন্ধান-অনুরোধ যায় `nominatim.openstreetmap.org` এবং `overpass-api.de`-এ।
কোনো লগইন নেই, কোনো API-Key নেই, কোনো স্থায়ী তথ্য সংরক্ষণ নেই।
User-Agent Nominatim-নীতি অনুযায়ী সেট করা হয়।

---

## সংশ্লিষ্ট সম্পদ

- `reiseroute` — A থেকে B পর্যন্ত রুট পরিকল্পনা (Geocoding-এর জন্য Nominatim-ও ব্যবহার করে)
- `wetter` — বর্তমান স্থানের আবহাওয়া

---

## পরিবর্তনের ইতিহাস

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH location_search.py v1.1.0 থেকে তৈরি; Store সরানো হয়েছে |
