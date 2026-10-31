---
name: reiseroute
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "OSRM (Open Source Routing Machine) ব্যবহার করে A থেকে B পর্যন্ত রুট পরিকল্পনা। গাড়ি, সাইকেল এবং পায়ে হাঁটা সমর্থিত। কোনো API key প্রয়োজন নেই।"
tags: [routing, navigation, osrm, openstreetmap, reise]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json']}
runtime: python3
entry_point: reiseroute_core.py
provenance: {'origin': 'BACH hub routing-service', 'origin_path': 'system/hub/_services/routing/routing_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'urllib.parse-Import an den Kopf verschoben (war im Original nur im else-Zweig). geocode_place (Nominatim) integriert. Keine Origin-DB. Kein Store. Userneutral, headless, nur Stdlib.\n'}
language: bn
visibility: public
translated_from_sha256: 598018ba8fdf3068a89280c1782ab9dbccaabc08409765e920015816bda81aef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.200507+00:00"
---
<img src="banner.png" width="100%" alt="reiseroute banner">

# ভ্রমণ রুট

**OSRM (Open Source Routing Machine) এর মাধ্যমে রুট পরিকল্পনা**

---

## বিহঙ্গম দৃষ্টি

দুটি স্থানের মধ্যে (নাম বা স্থানাঙ্ক) রুট পরিকল্পনা করে সার্বজনীন
`router.project-osrm.org` পরিষেবার মাধ্যমে। দূরত্ব, ভ্রমণের সময় এবং পরিবহন মাধ্যম
প্রদর্শন করে। কোনো API-Key বা অ্যাকাউন্ট প্রয়োজন নেই।

---

## ট্রিগার

| বাক্যাংশ | কার্যক্রম |
|---|---|
| „বার্লিন থেকে হামবুর্গের রুট পরিকল্পনা করো" | গাড়ির রুট, স্থানের নাম জিওকোড |
| „গাড়িতে মিউনিখ থেকে ভিয়েনা যেতে কতক্ষণ লাগবে?" | গাড়ির রুট + সময়ের হিসাব |
| „পොটসডাম থেকে বার্লিন সাইকেলে রুট" | সাইকেল মোড |
| „ক্রয়েৎসবের্গ থেকে বার্লিন মিটে পায়ে হেঁটে" | পায়ে হাঁটার মোড |
| „52.52,13.41 থেকে 53.55,9.99 পর্যন্ত পথ" | সরাসরি স্থানাঙ্ক |

---

## কর্মপ্রবাহ

1. ব্যবহারকারীর ইনপুট থেকে **শুরু ও গন্তব্যস্থল নিষ্কাশন** করো।
2. **মোড শনাক্ত করো:** গাড়ি (ডিফল্ট), সাইকেল, পায়ে হাঁটা।
3. **জিওকোড করো:** স্থানের নাম → Nominatim এর মাধ্যমে স্থানাঙ্ক।
4. **OSRM-এ অনুরোধ পাঠাও:** দূরত্ব (km) + সময় (বিন্যস্ত) ফেরত দেয়।
5. **ফলাফল প্রদর্শন করো:** স্পষ্ট পাঠ্য সারসংক্ষেপ।

---

## CLI

```bash
# Auto-Route zwischen zwei Orten
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# Fahrrad
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# Zu Fuß
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Koordinaten direkt (lat,lon)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# JSON-Ausgabe
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "München" "Wien" --json

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## মোড

| মোড | বিকল্প নাম | OSRM প্রোফাইল |
|---|---|---|
| auto (ডিফল্ট) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## স্টোর

কোনো স্থায়ী স্টোর নেই। রুট সংরক্ষণ করা হয় না।

---

## আচরণ

- গণনার আগে সর্বদা শুরু ও গন্তব্য উল্লেখ করো।
- কোনো স্থান অস্পষ্ট হলে স্পষ্ট করো (যেমন „Wien" কি অস্ট্রিয়া নাকি একই নামের অন্য শহর?)।
- উল্লেখ্য: OSRM রিয়েল-টাইম ট্রাফিক ছাড়া দ্রুততম রুট দেয়।
- অত্যন্ত দীর্ঘ পায়ে হাঁটার রুটে (> 20 km) একটি সতর্কবার্তা দাও।

---

## গোপনীয়তা

অনুরোধগুলো যায় `nominatim.openstreetmap.org` (জিওকোডিং) এবং
`router.project-osrm.org` (রাউটিং)-এর কাছে। কোনো লগইন, কোনো API-Key নেই,
কোনো স্থায়ী ডেটা সংরক্ষণ নেই।

---

## সম্পর্কিত সম্পদ

- `location-suche` — POI অনুসন্ধান (এটিও Nominatim ব্যবহার করে)
- `wetter` — গন্তব্যের আবহাওয়া

---

## পরিবর্তনের ইতিহাস

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH routing_service.py v1.0 থেকে তৈরি; জিওকোডিং যুক্ত |
