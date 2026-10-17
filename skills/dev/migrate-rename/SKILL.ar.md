---
name: migrate-rename
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-09-06
description: "إعادة تسمية الملفات تطوريًا باستخدام ملفات الغلاف (Wrapper)، إضافةً إلى معيار MOVED-Stub الموجز لنقل المجلدات والملفات بالكامل. يتيح إعادة التسمية دون كسر حاد — إذ تُحدَّث المراجع تدريجيًا عبر الاستخدام."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 16d2b6f4499cdc4c454bcd8244fff5811ae232e7703095f43a59eb663238d837
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="migrate-rename banner">

# إعادة تسمية الملفات باستخدام Wrapper (الترحيل التطوري)

> يتيح تغيير أسماء الملفات دون كسور حادة. تُحدَّث المراجع تدريجيًا من خلال الاستخدام اليومي.

---

## المبدأ: الترحيل التطوري

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

من يستدعي المسار القديم:
1. يصل إلى ملف الغلاف (Wrapper)
2. يسجّل نفسه في السجل
3. يصحّح المرجع الذي أحاله إليه
4. ينتقل إلى الملف الفعلي

---

## خطوة بخطوة

### 1. إعادة تسمية الملف

```bash
mv alte_datei.md neue_datei.md
```

### 2. إنشاء ملف الغلاف (Wrapper)

أنشئ `alte_datei.md` بالمحتوى التالي:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |

---

## Anleitung

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` -> `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: `neue_datei.md`

---

**Zieldatei:** `neue_datei.md`
```

### 3. تصحيح المراجع الحرجة فورًا
- ملفات المساعدة (التوثيق الأساسي)
- مراجع موجّه النظام (System-Prompt)
- شيفرة CLI التي تستخدم المسار مباشرةً

### 4. ترحيل بقية المراجع تطوريًا
يُصحَّح الباقي تلقائيًا عند الاستخدام.

---

## متى تُستخدم طريقة Wrapper؟

**نعم - Wrapper مناسب:**
- مراجع محتملة كثيرة
- يُشار إلى الملف من شركاء/أدوات مختلفة
- ليس ملف نظام حرجًا

**لا - غيّر الكل مباشرةً:**
- مراجع قليلة ومعروفة
- ملفات النظام الحرجة (الإعدادات، مخطط قاعدة البيانات)
- مسارات حساسة للأداء

---

## نقل المجلدات/الملفات باستخدام MOVED-Stub

> اعتُمد رسميًا بتاريخ 2026-09-06 (التذكرة T-20260906-688261413). نشأت السابقة تلقائيًا في
> `.ELLMOS.MIGRATED.md` (2026-08-11) وفي ملفات `_control-center/_CONTROL` الموجزة (2026-09-06).

وضع مختلف عن Wrapper أعلاه: هنا ينتقل **مجلد كامل** أو **ملف دون مراجع نشطة كثيرة** بالكامل إلى
موقع جديد (دمج، إعادة تسمية، إعادة تنظيم خط المعالجة). لا يوجد سجل ترحيل ولا "تصحيح للمراجع" — فقط
مؤشر موجز يقول: الملف الآن هنا.

**الفرق عن إجراء Wrapper أعلاه:**

| | Wrapper (الخطوات 1-4 أعلاه) | MOVED-Stub |
|---|---|---|
| الاستخدام | ملف مفرد، مراجع نشطة كثيرة، يُفترض أن تتبعه تدريجيًا | مجلد أو ملف، نقل كامل |
| المحتوى | جدول سجل ترحيل ينمو مع الاستخدام | بيانات وصفية ثابتة، من 1 إلى 3 أسطر نصية |
| مدة البقاء | حتى يُظهر السجل: لا إدخالات جديدة | حتى يتحقق `remove_when` |

### الاسم والموقع والحقول الإلزامية

المخطط الكامل والمثال ودلالات الحقول موجودة في قالب ellmos `MOVED-STUB.md`
(`.TOPICS/.AI/_templates/project-docs/MOVED-STUB.md`، وليس جزءًا من مستودع standalone هذا —
يكفي الملخص هنا):

- **الاسم/الموقع:** `<alter-Name>.MOVED.md` يقع في المكان الذي كان فيه المجلد/الملف **سابقًا**.
- **الحقول الإلزامية** (`key: value`، بهذا الترتيب): `moved_to`، `moved_on`، `ticket`،
  `reason`، `moved_by`، `remove_when` (الافتراضي: `90 Tage UND 0 lebende Referenzen`).
- **بعدها** من 1 إلى 3 أسطر نصية للقرّاء. لا سجل، لا جدول، لا تاريخ — فذلك موجود في التذكرة المرجعية.
- **الإزالة:** يُحذف Stub، ولا يُؤرشف أبدًا.

### السياسة

ملزِمة بوصفها `.SYNC/_policies/library/P-017_umzugs-stub.md`.

### سكربت الفحص

`scripts/moved_stub_check.py` (في مجلد هذه المهارة) يسرد جميع ملفات `*.MOVED.md`/`*.MIGRATED.md`
الموجزة ضمن دليل جذر، ويبلّغ عن الحقول الإلزامية المفقودة، ويُعلِّم الملفات الموجزة المستحقة للتراجع (الأقدم من
`remove_when` يومًا). الاستدعاء:

```bash
python scripts/moved_stub_check.py <wurzelverzeichnis>
```

---

## التنظيف

بعد نحو 30 يومًا أو عندما يُظهر السجل عدم وجود إدخالات جديدة:
1. انقل ملف الغلاف إلى `_archive/deprecated/`
2. أو احذفه نهائيًا (إذا لم تعد توجد إدخالات)

---

## سجل التغييرات

### 1.1.0 (2026-09-06)
- أُضيف القسم "نقل المجلدات/الملفات باستخدام MOVED-Stub" (التذكرة T-20260906-688261413):
  يُضفي الطابع الرسمي على مؤشر النقل الموجز للمجلدات/الملفات الكاملة (المعيار `<alter-Name>.MOVED.md`،
  الحقول الإلزامية moved_to/moved_on/ticket/reason/moved_by/remove_when)، مع تمييزه عن
  إجراء Wrapper أعلاه. أُضيف سكربت الفحص `scripts/moved_stub_check.py`.

### 1.0.0 (2026-03-15)
- نُقل من BACH v3.8.0

---

*منقول من BACH v3.8.0 | النسخة المستقلة*
