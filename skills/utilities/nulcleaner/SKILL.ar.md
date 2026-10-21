---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "يعثر على ملفات NUL المحجوزة في Windows التي تنشأ عند استخدام /dev/null في Git Bash ويحذفها. يعمل بدون واجهة رسومية أو مع واجهة رسومية."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: ar
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/nulcleaner.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 684d3a24e9aa64d125877cb5f27fc613d89bcf44a2f5e213ea1b65d91cc44a39
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.649939+00:00"
---
<img src="banner.png" width="100%" alt="nulcleaner banner">

# nulcleaner - تنظيف ملفات NUL في Windows

## المشكلة

عند استخدام `/dev/null` في Git Bash على Windows ضمن الأوامر (مثلاً `> /dev/null`)،
بدلاً من إعادة التوجيه إلى العدم، يُنشأ **ملف فعلي باسم `nul`** في الدليل الحالي. يحجز Windows الاسم "NUL" كاسم جهاز، ولهذا لا يمكن حذف هذه الملفات بالطريقة المعتادة.

يعثر هذا الأداة على ملفات NUL هذه ويحذفها عبر المسار الموسّع لـ UNC (`\\?\`).

---

## الأوضاع

| الوضع | الوصف |
|-------|-------------|
| `scan` | البحث عن ملفات NUL بشكل متكرر في الدليل |
| `delete` | العثور على ملفات NUL وحذفها |
| `gui` | واجهة رسومية مع اختيار الملفات |

---

## استخدام سطر الأوامر

```bash
# Nur scannen (zeigt gefundene NUL-Dateien)
python nulcleaner.py scan /pfad/zum/verzeichnis

# Scannen und loeschen
python nulcleaner.py delete /pfad/zum/verzeichnis

# GUI-Modus starten
python nulcleaner.py gui
```

---

## واجهة برمجية بدون واجهة (للتكامل)

توفر الأداة أيضاً واجهة برمجية بلغة Python للتشغيل بدون واجهة رسومية:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/pfad/zum/verzeichnis", verbose=True)
print(f"Gefunden: {result['found']}, Geloescht: {result['deleted']}")
```

**القيمة المُرجعة:** `{'found': int, 'deleted': int, 'errors': list}`

---

## التفاصيل التقنية

- يستخدم المسار الموسّع لـ UNC (`\\?\`) لحذف الملفات ذات الأسماء المحجوزة في Windows
- فحص متكرر باستخدام `os.walk()`
- واجهة رسومية بمكتبة tkinter (بدون تبعيات خارجية)
- يعمل فقط على Windows (حيث تنشأ المشكلة)

---

## الوقاية

الأفضل تجنب `/dev/null` في Git Bash. وبدلاً من ذلك:
- حذف المخرجات ببساطة
- استخدام `2>&1` لإعادة توجيه الخطأ القياسي
- مراعاة التوافق مع Windows في نصوص الصدفة
