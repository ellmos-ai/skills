---
name: reiseroute
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "OSRM (Open Source Routing Machine) के माध्यम से A से B तक मार्ग योजना। कार, साइकिल और पैदल यात्रा का समर्थन करता है। किसी API कुंजी की आवश्यकता नहीं है।"
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
language: hi
visibility: public
translated_from_sha256: 598018ba8fdf3068a89280c1782ab9dbccaabc08409765e920015816bda81aef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="reiseroute banner">

# यात्रा मार्ग

**OSRM (Open Source Routing Machine) के माध्यम से मार्ग योजना**

---

## अवलोकन

`router.project-osrm.org` के सार्वजनिक OSRM सेवा के माध्यम से दो स्थानों (नाम या निर्देशांक) के बीच मार्ग की योजना बनाता है। दूरी, यात्रा समय और परिवहन का साधन आउटपुट करता है। कोई API कुंजी नहीं, कोई खाता आवश्यक नहीं।

---

## ट्रिगर

| वाक्यांश | कार्रवाई |
|---|---|
| „बर्लिन से हैमबर्ग का मार्ग योजना बनाओ" | कार मार्ग, स्थान नामों का जियोकोडिंग |
| „कार से म्यूनिख से वियना तक की यात्रा में कितना समय लगेगा?" | कार मार्ग + समय की जानकारी |
| „बाइक से पोट्सडाम से बर्लिन तक का मार्ग" | साइकिल मोड |
| „क्रॉयत्सबर्ग से बर्लिन के मिटे तक पैदल" | पैदल मोड |
| „52.52,13.41 से 53.55,9.99 तक का मार्ग" | सीधे निर्देशांक |

---

## कार्यप्रवाह

1. उपयोगकर्ता के इनपुट से **प्रारंभ और गंतव्य स्थान निकालें**।
2. **मोड पहचानें:** कार (डिफ़ॉल्ट), साइकिल, पैदल।
3. **जियोकोडिंग:** स्थान नाम → निर्देशांक Nominatim के माध्यम से।
4. **OSRM से अनुरोध:** दूरी (km) + अवधि (स्वरूपित) लौटाता है।
5. **परिणाम आउटपुट:** स्पष्ट पाठ्य सारांश।

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

## मोड

| मोड | उपनाम | OSRM प्रोफ़ाइल |
|---|---|---|
| auto (डिफ़ॉल्ट) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Store

कोई स्थायी store नहीं। मार्ग संग्रहीत नहीं किए जाते।

---

## दृष्टिकोण

- गणना से पहले हमेशा प्रारंभ और गंतव्य बताएं।
- यदि कोई स्थान अस्पष्ट है तो स्पष्ट करें (उदा. „Wien" = ऑस्ट्रिया या उसी नाम का कोई शहर?)।
- सूचना: OSRM वास्तविक-समय यातायात के बिना सबसे तेज़ मार्ग देता है।
- बहुत लंबे पैदल मार्गों (> 20 km) पर एक सूचना दें।

---

## गोपनीयता

अनुरोध `nominatim.openstreetmap.org` (जियोकोडिंग) और `router.project-osrm.org` (रूटिंग) को भेजे जाते हैं। कोई लॉगिन नहीं, कोई API कुंजी नहीं, कोई स्थायी डेटा संग्रहण नहीं।

---

## संबंधित संसाधन

- `location-suche` — POI खोज (यह भी Nominatim का उपयोग करता है)
- `wetter` — गंतव्य का मौसम

---

## परिवर्तन लॉग

| संस्करण | तिथि | परिवर्तन |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH routing_service.py v1.0 से बनाया गया; जियोकोडिंग एकीकृत |
