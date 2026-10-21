---
name: reiseroute
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "تخطيط المسار من النقطة A إلى النقطة B عبر OSRM (Open Source Routing Machine). يدعم السيارة والدراجة الهوائية والمشي. لا يتطلب مفتاح API."
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
language: ar
visibility: public
translated_from_sha256: 598018ba8fdf3068a89280c1782ab9dbccaabc08409765e920015816bda81aef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="reiseroute banner">

# مسار الرحلة

**تخطيط المسار عبر OSRM (Open Source Routing Machine)**

---

## نظرة عامة

يخطط المسارات بين مكانين (بالأسماء أو الإحداثيات) عبر خدمة OSRM العامة
`router.project-osrm.org`. يعرض المسافة ووقت الرحلة ووسيلة النقل. لا يتطلب مفتاح API ولا حسابًا.

---

## المحفزات

| العبارة | الإجراء |
|---|---|
| „خطط المسار من برلين إلى هامبورغ" | مسار بالسيارة، وترميز أسماء الأماكن جغرافيًا |
| „كم تستغرق الرحلة من ميونخ إلى فيينا بالسيارة؟" | مسار بالسيارة + معلومات الوقت |
| „مسار بالدراجة من بوتسدام إلى برلين" | وضع الدراجة |
| „سيرًا على الأقدام من كرويتسبرغ إلى ميته في برلين" | وضع المشي |
| „المسار من 52.52,13.41 إلى 53.55,9.99" | إحداثيات مباشرة |

---

## سير العمل

1. **استخراج نقطة البداية والوجهة** من إدخال المستخدم.
2. **تحديد الوضع:** سيارة (افتراضي)، دراجة، مشي.
3. **الترميز الجغرافي:** أسماء الأماكن ← إحداثيات عبر Nominatim.
4. **طلب OSRM:** يعيد المسافة (كم) + المدة (بتنسيق منسق).
5. **عرض النتيجة:** ملخص نصي واضح.

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

## الأوضاع

| الوضع | الأسماء البديلة | ملف التعريف (profile) |
|---|---|---|
| سيارة (افتراضي) | car, pkw, fahren | driving |
| دراجة | bike, rad, radfahren | cycling |
| مشي | foot, laufen, gehen, zu fuss | foot |

---

## المخزن

لا يوجد مخزن دائم. لا تُحفظ المسارات.

---

## التوجيهات

- ذكر نقطة البداية والوجهة دائمًا قبل الحساب.
- التوضيح عندما يكون المكان ملتبسًا (مثلًا „فيينا" = النمسا أم مدينة بالاسم نفسه؟).
- ملاحظة: يقدم OSRM المسار الأسرع دون حركة مرور فورية.
- إصدار تنبيه عند مسارات المشي الطويلة جدًا (أكثر من 20 كم).

---

## الخصوصية

تُرسل الطلبات إلى `nominatim.openstreetmap.org` (الترميز الجغرافي) و
`router.project-osrm.org` (التوجيه). لا تسجيل دخول، ولا مفتاح API،
ولا تخزين دائم للبيانات.

---

## الموارد ذات الصلة

- `location-suche` — البحث عن نقاط الاهتمام (يستخدم Nominatim أيضًا)
- `wetter` — الطقس في وجهة السفر

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 1.0.0 | 2026-06-22 | أُنشئ من BACH routing_service.py v1.0؛ دُمج الترميز الجغرافي |
