---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "بروتوكول منهجي لتصحيح الأخطاء من 6 مراحل. نهج منظم للأخطاء يشمل فحوصات سريعة، واختبارًا معزولًا، وقاعدة الـ20 دقيقة، وقالب تقرير الخطأ."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 5deea0b6bd5cb1acc3495ebe481c63468b2231bb09d3e15f3da8163dde433e40
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.364887+00:00"
---
<img src="banner.png" width="100%" alt="bugfix-protocol banner">

# بروتوكول إصلاح الأخطاء: تصحيح منهجي للأخطاء في 6 مراحل

نهج منظم في التعامل مع الأخطاء — من تحليل الأعراض حتى التحقق.
يمنع التجربة العشوائية غير المخططة ويضمن أن الإصلاحات دائمة.

---

## نظرة عامة

| المرحلة | الاسم | الهدف | الحد الأقصى للوقت |
|---------|-------|-------|-------------------|
| 1 | الفحوصات السريعة | استبعاد الأسباب الواضحة | 2 دقيقة |
| 2 | التشخيص | تحديد موقع السبب | 10 دقائق |
| 3 | الاختبار المعزول | جعل الخطأ قابلًا للتكرار | 5 دقائق |
| 4 | الإصلاح | تصحيح أدنى | 10 دقائق |
| 5 | التحقق | فحص الإصلاح والآثار الجانبية | 5 دقائق |
| 6 | التوثيق | حفظ المعرفة | 2 دقيقة |

**قاعدة الـ20 دقيقة:** إذا لم يحدث أي تقدم بعد 20 دقيقة ← غيّر النهج أو اطلب المساعدة.

---

## المرحلة 1: الفحوصات السريعة (2 دقيقة)

قبل التعمق — افحص الأسباب الأكثر شيوعًا:

### قائمة التحقق

- [ ] **أخطاء في بناء الجملة؟** اقرأ رسالة الخطأ بدقة وافحص السطر
- [ ] **أخطاء في الاستيراد؟** هل الوحدة مثبتة؟ هل الاسم صحيح؟ استيراد دائري؟
- [ ] **أخطاء مطبعية؟** هل أسماء المتغيرات والدوال صحيحة؟
- [ ] **نوع بيانات خاطئ؟** نص بدلًا من عدد صحيح؟ None حيث يُتوقع كائن؟
- [ ] **ذاكرة تخزين مؤقت قديمة؟** احذف `__pycache__` وأعد التشغيل
- [ ] **بيئة خاطئة؟** هل البيئة الافتراضية الصحيحة مفعلة؟ هل إصدار Python صحيح؟
- [ ] **الترميز؟** UTF-8 مقابل cp1252 (المشكلة الكلاسيكية في Windows)

### إجراءات سريعة

```bash
# Cache leeren
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# Imports pruefen
python -c "import modulname"

# Syntax pruefen
python -m py_compile datei.py
```

---

## المرحلة 2: التشخيص (10 دقائق)

### الاستراتيجية: من الخارج إلى الداخل

1. **تحليل رسالة الخطأ** — اقرأ Traceback من الأسفل إلى الأعلى
2. **فحص التغييرات الأخيرة** — `git diff`، `git log --oneline -10`
3. **استخدام أدوات التشخيص** — استخدم أدوات التشخيص الخاصة بك حسب المشروع

### أدوات التشخيص (أمثلة)

حسب المشروع، قد تكون سكربتات التشخيص المتخصصة مفيدة:

| الأداة | الغرض |
|--------|-------|
| `import_diagnose.py` | تحليل مشكلات الاستيراد |
| `method_analyzer.py` | فحص توقيعات الدوال |
| `env_checker.py` | التحقق من متغيرات البيئة والمسارات |

> **ملاحظة:** أنشئ أدوات تشخيص خاصة بك حسب المشروع، أو استخدم أدوات
> المشروع الموجودة. المهم هو النهج المنظم، وليست الأداة المحددة.

### تقنيات تصحيح الأخطاء

```python
# 1. Print-Debugging (schnell aber effektiv)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. Breakpoint (interaktiv)
breakpoint()  # Python 3.7+

# 3. Traceback erweitern
import traceback
traceback.print_exc()

# 4. Logging statt Print
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## المرحلة 3: الاختبار المعزول (5 دقائق)

### أدنى مثال قابل للتكرار (MRE)

الهدف: إعادة إنتاج الخطأ بأقل قدر من الشيفرة.

```python
# test_bug.py — Minimaler Reproduktions-Test
"""
Bug: [Kurze Beschreibung]
Erwartet: [Was sollte passieren]
Tatsaechlich: [Was passiert stattdessen]
"""

# Minimaler Setup
# ... nur das Noetigste

# Bug-Ausloeser
# ... exakter Code der den Bug triggert

# Erwartetes Ergebnis
# assert result == expected, f"Got {result}"
```

### استراتيجيات العزل

1. **ملف جديد:** أعد إنتاج الخطأ في ملف مستقل
2. **إزالة التبعيات:** واحدة تلو الأخرى حتى يختفي الخطأ
3. **التنصيف:** قسّم كتلة الشيفرة إلى نصفين وافحص أيهما يحتوي الخطأ
4. **Git Bisect:** `git bisect start`، `git bisect bad`، `git bisect good <commit>`

---

## المرحلة 4: الإصلاح (10 دقائق)

### المبادئ

1. **الحد الأدنى:** غيّر أقل قدر ممكن
2. **الفهم:** لا تُصلح بشكل أعمى — افهم لماذا تعطل الشيء
3. **أمر واحد:** إصلاح واحد لكل commit، لا عدة مشكلات في آن واحد
4. **التوافق مع الإصدارات السابقة:** لا تكسر الوظائف القائمة

### أنماط الإصلاح

```python
# SCHLECHT: Symptom behandeln
try:
    result = broken_function()
except:  # Alles schlucken
    result = default_value

# GUT: Ursache beheben
def broken_function():
    if input_data is None:  # Eigentliche Ursache: None-Check fehlte
        return default_value
    return process(input_data)
```

### فئات الإصلاح الشائعة

| الفئة | الإصلاح النموذجي |
|-------|------------------|
| None/Null | شرط حماية: `if x is None: return default` |
| خطأ الفهرس | فحص الحدود: `if i < len(lst)` |
| خطأ النوع | تحويل صريح: `str(x)`، `int(x)` |
| خطأ الاستيراد | تصحيح المسار، تثبيت الحزمة |
| الترميز | تحديد UTF-8 صراحةً: `encoding='utf-8'` |
| حالة السباق | قفل/Mutex، أو تغيير الترتيب |
| خطأ الحالة | فحص التهيئة، إضافة إعادة ضبط |

---

## المرحلة 5: التحقق (5 دقائق)

### قائمة التحقق

- [ ] **الخطأ مُصلح:** المشكلة الأصلية لم تعد تظهر
- [ ] **MRE ينجح:** الاختبار المعزول يمر بنجاح
- [ ] **لا توجد تراجعات:** الاختبارات القائمة ما زالت تعمل
- [ ] **الحالات الطرفية:** تم اختبار المدخلات الفارغة وNone والبيانات الكبيرة
- [ ] **أدوات المشروع:** ابحث في دليل أدوات المشروع عن أدوات الاختبار/التحقق ذات الصلة

### أوامر الاختبار

```bash
# Unit-Tests
python -m pytest tests/ -v

# Nur betroffene Tests
python -m pytest tests/test_modul.py -v -k "test_name"

# Type-Check
python -m mypy datei.py

# Lint
python -m flake8 datei.py
```

---

## المرحلة 6: التوثيق (2 دقيقة)

### قالب تقرير الخطأ

```markdown
## Bug-Report: [Kurztitel]

**Datum:** YYYY-MM-DD
**Schwere:** kritisch / hoch / mittel / niedrig
**Komponente:** [Modul/Datei]

### Symptom
[Was der User sieht / Fehlermeldung]

### Ursache
[Technische Root-Cause]

### Fix
[Was geaendert wurde + warum]

### Betroffene Dateien
- `datei1.py` — [Aenderung]
- `datei2.py` — [Aenderung]

### Praevention
[Wie kann dieser Bug-Typ in Zukunft vermieden werden?]
```

### تنسيق رسالة الـ Commit

```
fix: [Kurze Beschreibung des Fixes]

Ursache: [Root-Cause in einem Satz]
Fix: [Was geaendert wurde]
Test: [Wie verifiziert]
```

---

## تصحيح أخطاء PyQt6 / الواجهة الرسومية — المزالق الشائعة

> هذا القسم مهم لمشاريع الواجهات الرسومية المكتبية باستخدام PyQt6/PySide6.

### أهم 5 مزالق في PyQt6

| المزلق | المشكلة | الحل |
|--------|---------|------|
| **فصل Signal-Slot** | الإشارة متصلة لكن المعالج لا يعمل | `print` داخل المعالج، وافحص التوقيع |
| **أمان الخيوط** | تحديث الواجهة من خيط العامل | `QMetaObject.invokeMethod` أو استخدم الإشارات |
| **تتالي التخطيط** | الأداة غير مرئية أو موضوعة بشكل خاطئ | `widget.show()`، وافحص هرمية التخطيط |
| **حجب حلقة الأحداث** | الواجهة تتجمد | انقل العمليات طويلة الأمد إلى QThread |
| **جمع المهملات** | الأداة تختفي فجأة | احتفظ بالمرجع كـ `self.widget` |

### مساعدات تصحيح PyQt6

```python
# Widget-Hierarchie ausgeben
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# Signal-Debugging
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## مرجع سريع

```
BUG GEFUNDEN?
     │
     ▼
[Phase 1: Schnell-Checks]  ──── Offensichtlich? → FIX
     │
     ▼
[Phase 2: Diagnose]  ────────── Ursache klar? → Phase 4
     │
     ▼
[Phase 3: Isolierter Test]  ── Reproduzierbar? → Phase 4
     │                              │
     │                         Nicht reproduzierbar?
     │                              │
     │                         Logging einbauen,
     │                         auf erneutes Auftreten warten
     ▼
[Phase 4: Fix]  ─────────────── Minimal + verstanden
     │
     ▼
[Phase 5: Verifikation]  ────── Tests gruen? → Phase 6
     │                              │
     │                         Tests rot? → Zurueck zu Phase 4
     ▼
[Phase 6: Dokumentation]  ───── Bug-Report + Commit
```

### قاعدة الـ20 دقيقة

إذا علقت بعد 20 دقيقة:

1. **غيّر النهج** — جرّب تقنية تصحيح أخرى
2. **بطة المطاط** — اشرح المشكلة بصوت عالٍ (أو اكتبها)
3. **استراحة** — ابتعد 5 دقائق، ثم عد بنظرة جديدة
4. **اطلب المساعدة** — اسأل زميلًا، أو Stack Overflow، أو التوثيق
5. **إعادة الضبط** — `git stash`، وابدأ من جديد تمامًا
