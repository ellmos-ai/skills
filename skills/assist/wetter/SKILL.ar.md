---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "يجيب عن أسئلة الطقس لموقع أو إحداثيات عبر wttr.in (مجاني، دون مفتاح API). الطقس الحالي مع توقعات لثلاثة أيام. يأتي الموقع من طلب المستخدم أو تفضيلاته؛ تخزين مؤقت قصير اختياري."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: ar
status: active
visibility: public
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 77159e7ab4dc0541cb58d038cfb353076dc2d32699dba8cd2e69761042b86b8c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="wetter banner">

# الطقس

خدمة سريعة للطقس دون مفاتيح، مناسبة للاستخدام اليومي.

## الغرض

تجيب عن أسئلة «كيف سيكون الطقس؟» دون الحاجة إلى مفتاح API (مصدر البيانات: wttr.in).
تقدم الطقس الحالي (درجة الحرارة، درجة الحرارة المحسوسة، الرياح، الرطوبة، مؤشر الأشعة فوق البنفسجية) إضافةً إلى معاينة مختصرة لثلاثة أيام. **محايدة تجاه المستخدم:** لا يوجد موقع ثابت في الشيفرة — يأتي الموقع من الطلب أو من `assist/prefs.json` (`wetter_default_location`)، ويملؤه النموذج اللغوي تفاعليًا مع المستخدم.

## المحفزات

| إدخال المستخدم | الإجراء |
|---|---|
| «ما حال الطقس في بوتسدام؟» / «كيف سيكون الطقس في هامبورغ؟» | `wetter_core.py "<Ort>"` |
| «كيف سيكون الطقس غدًا؟» (دون ذكر مكان) | `wetter_core.py --default` (الموقع من التفضيلات) |
| «موقع الطقس الافتراضي لي هو بوتسدام» | `wetter_core.py --set-default "Potsdam"` |
| الإحداثيات معروفة | `wetter_core.py <lat> <lon>` |

## سير العمل

```
1. Ort bestimmen: aus Anfrage; sonst prefs.json (wetter_default_location);
   sonst Nutzer interaktiv fragen + optional als Default speichern.
2. wetter_core.py abfragen (wttr.in, 2 Versuche, 30-min-Cache).
3. Lesbaren Wetter-Text + 3-Tage-Vorschau praesentieren.
```

## نقطة الدخول عبر سطر الأوامر (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # Ort
python wetter_core.py 52.6789 13.5878   # Koordinaten
python wetter_core.py --default         # Ort aus prefs.json
python wetter_core.py --set-default "Potsdam"
```

## المخزن (اختياري)

- **لا يوجد مخزن إلزامي.** تخزين مؤقت قصير اختياري `assist/wetter/.cache.json`
  (مدة الصلاحية 30 دقيقة، بأفضل جهد) — يتجنب طلبات الشبكة المتكررة.
- تفضيل الموقع يُحفظ في `assist/prefs.json` (`wetter_default_location`).

## التوجّه

نستخدم wttr.in كمصدر افتراضي لا يتطلب مفاتيح، ونحن منفتحون على خدمات طقس أخرى (مثل DWD أو OpenWeather) إذا رغب المستخدم في ذلك.

## حماية البيانات

- يُرسل اسم الموقع أو الإحداثيات فقط إلى wttr.in (وهو ضروري لتنفيذ الاستعلام).
- لا يوجد تتبع عن بُعد ولا حساب مستخدم. يبقى التخزين المؤقت والتفضيلات محليًا.

## الموارد ذات الصلة

- `assist/AGENTS.md` — الموجّه الشامل
- `assist/reiseroute/` — يستخدم الطقس عند الحاجة لتخطيط الرحلات (مخطط)

## سجل التغييرات

### 0.1.0 (2026-06-22)
- الإصدار الأولي. نُقل من BACH `hub/_services/weather/weather_service.py` (ترخيص MIT).
- توسيع: دعم أسماء المواقع (وليس الإحداثيات فقط)، ومعاينة لثلاثة أيام، وتخزين مؤقت اختياري، وموقع افتراضي قائم على التفضيلات. محايد تجاه المستخدم.
