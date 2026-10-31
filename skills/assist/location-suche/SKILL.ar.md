---
name: location-suche
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "البحث عن المواقع والمطاعم والفنادق عبر OpenStreetMap (Nominatim + Overpass API). يعيد نقاط الاهتمام (POIs) القريبة من موقع محدد أو يبحث بنص حر."
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
language: ar
visibility: public
translated_from_sha256: 93e16b5f7ddbd85797fd294d2251bb04189db2ac6f5f88f4061cc69b6189e0ba
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="location-suche banner">

# البحث عن المواقع

**البحث عن الأماكن والمطاعم والفنادق عبر OpenStreetMap**

---

## نظرة عامة

يبحث عن المطاعم والفنادق والمقاهي وأماكن أخرى باستخدام خدمات OpenStreetMap
Nominatim (الترميز الجغرافي) وOverpass (البحث عن نقاط الاهتمام). لا يتطلب مفتاح API.
لا يوجد مخزن دائم.

---

## المحفزات

| العبارة | الإجراء |
|---|---|
| „Such ein Restaurant in München" / «ابحث عن مطعم في ميونخ» | بحث عن نقاط الاهتمام: category=restaurant, near=München |
| „Hotels in der Nähe von Wien" / «فنادق بالقرب من فيينا» | بحث عن نقاط الاهتمام: category=hotel, near=Wien |
| „Wo ist der Eiffelturm?" / «أين برج إيفل؟» | بحث بنص حر عبر Nominatim |
| „Finde Cafés in Berlin" / «ابحث عن مقاهٍ في برلين» | بحث عن نقاط الاهتمام: category=cafe, near=Berlin |
| „Suche Apotheke nahe Potsdam" / «ابحث عن صيدلية قرب بوتسدام» | بحث عن نقاط الاهتمام: category=pharmacy, near=Potsdam |

---

## سير العمل

1. **التعرف على المحفز:** إذا تضمن الطلب فئة (مطعم، فندق، إلخ) ومكانًا → الخطوة 2. وإلا فالبحث بنص حر → الخطوة 4.
2. **ترميز المكان جغرافيًا:** يوفر Nominatim إحداثيات المكان المذكور.
3. **البحث عن نقاط الاهتمام:** تبحث Overpass API عن المرافق من الفئة ضمن نطاق محيط.
4. **عرض النتيجة:** إخراج قائمة بالاسم والعنوان والمسافة (م).
5. **البحث بالنص الحر (احتياطي):** يوفر نص Nominatim الحر نتائج مباشرة.

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

## المخزن

لا يوجد مخزن دائم. تُعرض النتائج فقط ولا تُحفظ.

---

## الفئات المدعومة

restaurant، cafe، bar، pub، fast_food، hotel، hostel، guest_house، supermarket،
pharmacy، hospital، bank، atm، fuel، parking، bus_stop، train_station، museum،
cinema، theatre، library، school، university، church

---

## الموقف

- اسأل المستخدم دائمًا عن المكان إذا لم يُذكر.
- عند وجود أكثر من 10 نتائج اعرض أقرب 5 فقط، والباقي عند الطلب.
- اذكر المسافة بالأمتار، وبالكيلومتر (برقم عشري واحد) من 1 كم فأكثر.
- الخصوصية: لا تُخزَّن بيانات الموقع ولا تُرسل إلا إلى
  واجهة Nominatim/Overpass العامة (openstreetmap.org).

---

## الخصوصية

تُرسل طلبات البحث إلى `nominatim.openstreetmap.org` و`overpass-api.de`.
لا تسجيل دخول، ولا مفتاح API، ولا تخزين دائم للبيانات.
يُضبط User-Agent وفقًا لسياسة Nominatim.

---

## الموارد ذات الصلة

- `reiseroute` — تخطيط المسار من A إلى B (يستخدم Nominatim أيضًا للترميز الجغرافي)
- `wetter` — الطقس في الموقع الحالي

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 1.0.0 | 2026-06-22 | أُنشئ من BACH location_search.py v1.1.0؛ أُزيل المخزن |
