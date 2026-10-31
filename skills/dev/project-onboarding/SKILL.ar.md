---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "إجراء قياسي لتأهيل مشاريع البرمجيات الجديدة: تحليل الميزات، ومراجعة جودة الكود، وقائمة التحقق من التأهيل، وإنشاء المهام."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 8e49954ab15704af930d6a8e717a5fd9c0109ed1378a2421998d889d8e90d359
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="project-onboarding banner">

# إجراء التأهيل القياسي لمشاريع البرمجيات الجديدة

**الإصدار:** 1.0
**التاريخ:** 2026-03-12

---

## نظرة عامة

يحدد هذا الإجراء الخطوات الواجب تنفيذها على مجلدات البرمجيات المكتشفة حديثًا قبل إدراجها في نظام إدارة المهام.

```
┌─────────────────────────────────────────────────────────┐
│           STANDARDAUFNAHMEVERFAHREN                     │
├─────────────────────────────────────────────────────────┤
│  1. Feature-Analyse erstellen                           │
│  2. Code-Qualitaetspruefung (Standard-Tests)            │
│  3. AUFGABEN.txt erstellen                              │
│  4. In Task-Management uebernehmen                      │
└─────────────────────────────────────────────────────────┘
```

---

## المرحلة 1: تحليل الميزات

**الغرض:** فهم الأداة ووظائفها وحالة تطويرها.

**إنشاء الملف:** `Feature_Analyse_<ToolName>.md`

### القالب

```markdown
# Feature-Analyse: <ToolName>

## Kurzbeschreibung
Ein kurzer Satz der beschreibt was das Tool macht.

---

## Highlights

| Feature | Beschreibung |
|---------|-------------|
| **Feature 1** | Beschreibung |
| **Feature 2** | Beschreibung |

---

## Bewertung der Ausbaustufe

### Aktueller Stand: **<Status> (<X>%)**

Moegliche Status:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Kategorie | Bewertung (1-5) | Details |
|-----------|:---------------:|---------|
| **Funktionsumfang** | 3 | |
| **UI/UX** | 3 | |
| **Stabilitaet** | 3 | |
| **Dokumentation** | 3 | |

---

## Empfohlene Erweiterungen

### Prioritaet: Hoch
1. ...

### Prioritaet: Mittel
2. ...

### Prioritaet: Niedrig
3. ...

---

## Technische Details

Framework:      <Framework>
Dateigroesse:   <X> Zeilen Python
Hauptdatei:     <main.py>

---
*Analyse erstellt: <Datum>*
```

---

## المرحلة 2: فحص جودة الكود

**الغرض:** ضمان الجودة التقنية وتحديد المشكلات المعروفة.

### الفحوصات الموصى بها

| الاختبار | الأداة | الوصف |
|------|--------|--------------|
| **الترميز** | أداة فحص الترميز (مثل `chardet`، `file`) | ضمان UTF-8 |
| **تحليل الدوال** | أداة فحص الشيفرة (Linter) (مثل `pylint`، `flake8`) | العثور على الدوال الكبيرة |
| **المسافات البادئة** | أداة التنسيق (مثل `black`، `autopep8`) | التحقق من الاتساق |
| **الاستيرادات** | أداة فحص الاستيرادات (مثل `isort`، `pylint`) | العثور على الاستيرادات غير المستخدمة |

### نقاط التحقق

- [ ] هل جميع ملفات .py مرمّزة بصيغة UTF-8؟
- [ ] هل تخلو الشيفرة من دوال كبيرة بشكل غير معتاد (>100 سطر)؟
- [ ] هل المسافات البادئة متسقة (مسافات مقابل تبويبات)؟
- [ ] هل أُزيلت الاستيرادات غير المستخدمة؟
- [ ] هل توجد تعليقات التوثيق (Docstrings)؟

### توثيق النتيجة

تسجيل المشكلات في ملف AUFGABEN.txt تحت القسم "QUALITAETSPRUEFUNG".

---

## المرحلة 3: إنشاء ملف AUFGABEN.txt

**الغرض:** تسجيل المهام المفتوحة بشكل منظم.

**إنشاء الملف:** `AUFGABEN.txt` في مجلد المشروع

### القالب

```
AUFGABEN - <ToolName> V<Version>
==============================
Status: <Status>
Stand: <Datum>

OFFENE AUFGABEN:
[ ] <Aufgabe 1> - Aufwand: <NIEDRIG|MITTEL|HOCH>
[ ] <Aufgabe 2> - Aufwand: <NIEDRIG|MITTEL|HOCH>

---
ERLEDIGT (Archiv):
- <Erledigte Aufgabe> (<Version>, <Datum>)
```

### قيم الحالة

| الحالة | المعنى |
|--------|-----------|
| NEU ENTDECKT | لم يتم تحليلها بعد |
| ANALYSE NOETIG | تحليل الميزات قيد التنفيذ |
| QUALITAETSPRUEFUNG | اختبارات الكود قيد التشغيل |
| VALIDIERT & BEREIT | جاهز للميزات |
| MVP | الحد الأدنى من المنتج القابل للاستخدام |
| NUR KOMPILIEREN | لم يتبقَّ سوى التجميع |
| GESPERRT | بانتظار اختبار المستخدم أو قرار |

---

## المرحلة 4: التكامل مع إدارة المهام

بعد إكمال المراحل 1-3:

1. **نقل المهام:** إنشاء مهام/قضايا من إدخالات ملف AUFGABEN.txt
2. **التحقق:** هل جميع المهام مصنفة بشكل صحيح؟
3. **التصنيف:** تصنيف المشروع ضمن الفئة المناسبة (أداة واحدة، حزمة، مكتبة وغيرها)

### مهام التأهيل التلقائية

عند المشاريع الجديدة، يتم إنشاء المهام القياسية التالية:

| المهمة | المهمة | الجهد |
|------|---------|---------|
| onb_1 | إنشاء تحليل الميزات | متوسط |
| onb_2 | فحص جودة الكود | منخفض |
| onb_3 | إنشاء ملف AUFGABEN.txt | منخفض |

للمهام تبعيات: onb_2 يعتمد على onb_1، وonb_3 يعتمد على onb_2.

---

## قائمة التحقق السريعة

```
[ ] 1. Feature_Analyse_<Name>.md erstellt
[ ] 2. Code-Qualitaetspruefung durchgefuehrt (Linter, Encoding, Imports)
[ ] 3. AUFGABEN.txt erstellt mit Status
[ ] 4. Tasks in Task-Management uebernommen
```

---

## مثال: أداة جديدة "MyTool"

```bash
# 1. Feature-Analyse
# -> Feature_Analyse_MyTool.md erstellen (siehe Template)

# 2. Code-Qualitaet
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Encoding pruefen

# 3. AUFGABEN.txt
# -> Im Tool-Ordner erstellen mit Status "QUALITAETSPRUEFUNG"

# 4. Tasks anlegen
# -> Eintraege aus AUFGABEN.txt als Issues/Tickets erfassen
```

---

*أُنشئ: 2026-01-10 | نُقل: 2026-03-12*
