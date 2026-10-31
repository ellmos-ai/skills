---
name: kontaktbuch
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "يرتّب بيانات الاتصال المقدَّمة طوعًا بأسلوب يقلل جمع البيانات، ويكشف التكرارات المحتملة."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [contacts, organization, deduplication, privacy]
language: ar
status: stable
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
translated_from_sha256: d9b3652c9acade9d21c9d30f6b8f92c205df1426c25ada123ddd434f7ab397ff
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.185489+00:00"
---
<img src="banner.png" width="100%" alt="kontaktbuch banner">

# نظرة عامة على جهات الاتصال

## الغرض

تنظيم جهات الاتصال لمهمة محددة، دون تقديم دفتر عناوين شخصي.

**النتيجة:** حقول موحّدة، وتكرارات محتملة، وبيانات ناقصة.

## سير العمل

1. توضيح الهدف والسياق وصيغة المخرجات المطلوبة.
2. استخدام المعلومات المقدَّمة في المهمة الحالية فقط.
3. إعداد النتيجة بصورة منظمة وقابلة للتتبع.
4. تمييز الافتراضات، وطلب التأكيد قبل إجراء أي تغييرات خارجية.

## مثال

**المدخل:** افحص قائمة جهات الاتصال المجهولة الهوية هذه بحثًا عن التكرارات.

**النتيجة:** حقول موحّدة، وتكرارات محتملة، وبيانات ناقصة.

## النواة العامة والإضافات الخاصة

تحتوي هذه المهارة العامة على المنهجية القابلة للنقل فقط. تنتمي المهايئات الخاصة بالتطبيقات، والحسابات، والمسارات المحلية، وقواعد البيانات، والإعدادات الشخصية المفضلة إلى ملف إضافي خاص أو إلى نسخة خاصة (fork)، ولا يجوز نقلها إلى هذا المستودع.

بدون ملف خاص، تعمل المهارة فقط مع المعلومات المقدَّمة صراحةً في المهمة الحالية.

## الحدود وحماية البيانات

- لا تُخزَّن البيانات افتراضيًا.
- لا يُفتح أي مصدر أو ملف أو واجهة برمجية أو يُعدَّل دون إذن صريح.

## سجل التغييرات

### 2.0.0 (2026-07-30)

- نواة عامة محايدة للمستخدم؛ أُزيلت التكاملات الخاصة والملفات الشخصية.
