---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "عمليات الملفات الدفعية (الحذف، والنقل، والنسخ، والإدراج) باستخدام أنماط Glob. أداة سطر أوامر لعمليات نظام الملفات بكفاءة. بدون تبعيات."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
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
  origin_path: "system/tools/batch_file_ops.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6fd8057d502337926d541fe4b66208c94e661e7d8c83fe0a4847094e90c5e024
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.844352+00:00"
---
<img src="banner.png" width="100%" alt="batch-file-ops banner">

# batch_file_ops - عمليات الملفات الدفعية

أداة سطر أوامر للعمليات الدفعية الفعالة على الملفات باستخدام أنماط Glob.
تدعم: delete وmove وcopy وlist. بدون تبعيات (مكتبة Python القياسية فقط).

---

## الإجراءات

| الإجراء | الوصف |
|--------|-------------|
| `delete` | حذف الملفات حسب النمط |
| `move` | نقل الملفات حسب النمط |
| `copy` | نسخ الملفات حسب النمط |
| `list` | إدراج الملفات حسب النمط |

## استخدام سطر الأوامر

```bash
python batch_file_ops.py <aktion> <quelle> [<ziel>] --pattern "<glob>" [--dry-run] [--recursive]
```

### الوسائط

| الوسيط | الوصف |
|----------|-------------|
| `aktion` | `delete` أو `move` أو `copy` أو `list` |
| `quelle` | مجلد المصدر |
| `ziel` | مجلد الوجهة (فقط لـ `move` و`copy`) |
| `--pattern`، `-p` | نمط Glob (مثل `*.py`، `TOOLS_*.py`) - الافتراضي: `*` |
| `--dry-run`، `-n` | عرض فقط دون تغيير أي شيء |
| `--recursive`، `-r` | البحث بشكل متكرر في المجلدات الفرعية |

---

## أمثلة

```bash
# Alle Python-Dateien in einem Ordner auflisten
python batch_file_ops.py list /pfad/zum/ordner --pattern "*.py"

# Alle .tmp Dateien loeschen (erst Dry-Run!)
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp"

# Dateien verschieben
python batch_file_ops.py move /quelle /ziel --pattern "*.txt"

# Dateien kopieren (rekursiv)
python batch_file_ops.py copy /quelle /ziel --pattern "*.md" --recursive

# Pattern-Beispiele
python batch_file_ops.py delete /pfad --pattern "TOOLS_*.py"
python batch_file_ops.py list /pfad --pattern "backup_202?-*"
```

---

## ملاحظات

- **التشغيل التجريبي أولاً:** مع `delete` و`move` استخدم دائماً `--dry-run` أولاً
- **أنماط Glob:** تستخدم `pathlib.glob()` / `pathlib.rglob()` في Python
- **متوافق مع Windows:** ترميز إخراج UTF-8 تلقائي
- **الملفات فقط:** يتم تخطي المجلدات (تتم معالجة الملفات فقط)
