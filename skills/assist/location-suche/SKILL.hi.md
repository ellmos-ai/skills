---
name: location-suche
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "OpenStreetMap (Nominatim + Overpass API) के माध्यम से स्थान, रेस्तरां और होटल खोज। किसी स्थान के निकट POIs (Points of Interest) लौटाता है या मुक्त-पाठ से खोजता है।"
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
language: hi
visibility: public
translated_from_sha256: 93e16b5f7ddbd85797fd294d2251bb04189db2ac6f5f88f4061cc69b6189e0ba
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="location-suche banner">

# स्थान-खोज

**OpenStreetMap के माध्यम से स्थान, रेस्तरां और होटल की खोज**

---

## अवलोकन

OpenStreetMap की सेवाओं Nominatim (जियोकोडिंग) और Overpass (POI-खोज) का उपयोग करके रेस्तरां, होटल, कैफ़े और अन्य स्थानों की खोज की जाती है।
कोई API-Key आवश्यक नहीं है। कोई स्थायी स्टोर नहीं है।

---

## ट्रिगर

| वाक्यांश | कार्रवाई |
|---|---|
| „München में एक रेस्तरां खोजो" | POI-खोज: category=restaurant, near=München |
| „Wien के पास होटल" | POI-खोज: category=hotel, near=Wien |
| „Eiffelturm कहाँ है?" | Nominatim मुक्त-पाठ खोज |
| „Berlin में कैफ़े खोजो" | POI-खोज: category=cafe, near=Berlin |
| „Potsdam के पास फ़ार्मेसी खोजो" | POI-खोज: category=pharmacy, near=Potsdam |

---

## कार्यप्रवाह

1. **ट्रिगर पहचानें:** यदि अनुरोध में कोई श्रेणी (रेस्तरां, होटल आदि) और कोई स्थान है → चरण 2। अन्यथा मुक्त-पाठ → चरण 4।
2. **स्थान जियोकोड करें:** Nominatim उल्लिखित स्थान के निर्देशांक देता है।
3. **POIs खोजें:** Overpass-API परिधि में उस श्रेणी की सुविधाएँ खोजता है।
4. **परिणाम दिखाएँ:** नाम, पता, दूरी (m) की सूची दिखाएँ।
5. **मुक्त-पाठ खोज (फ़ॉलबैक):** Nominatim मुक्त-पाठ सीधे मिलान देता है।

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

## स्टोर

कोई स्थायी स्टोर नहीं है। परिणाम केवल दिखाए जाते हैं, सहेजे नहीं जाते।

---

## समर्थित श्रेणियाँ

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## रुख

- यदि कोई स्थान नहीं बताया गया है, तो हमेशा उपयोगकर्ता से स्थान पूछें।
- 10 से अधिक परिणाम होने पर केवल निकटतम 5 दिखाएँ, शेष अनुरोध पर।
- दूरी मीटर में बताएँ, 1 km या उससे अधिक होने पर km में (1 दशमलव स्थान)।
- गोपनीयता: स्थान डेटा संग्रहीत या प्रेषित नहीं किया जाता, सिवाय सार्वजनिक
  Nominatim/Overpass-API (openstreetmap.org) के।

---

## गोपनीयता

खोज अनुरोध `nominatim.openstreetmap.org` और `overpass-api.de` को भेजे जाते हैं।
कोई लॉगिन नहीं, कोई API-Key नहीं, कोई स्थायी डेटा भंडारण नहीं।
User-Agent Nominatim-नीति के अनुसार सेट किया जाता है।

---

## संबंधित संसाधन

- `reiseroute` — A से B तक मार्ग योजना (जियोकोडिंग के लिए भी Nominatim का उपयोग करती है)
- `wetter` — वर्तमान स्थान का मौसम

---

## परिवर्तन-इतिहास

| संस्करण | तिथि | परिवर्तन |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH location_search.py v1.1.0 से बनाया गया; स्टोर हटाया गया |
