---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "مساعد المطورين (خليفة ATI). يوفر نظرة عامة سريعة على المشروع عبر فحص بدون واجهة ويوجّه إلى أدوات البرمجة المتاحة: CodeCommander MCP (التحليل/إعادة الهيكلة/التشخيص) ووحدة ellmos-code-tools. توجيه أدوات خالص + فحص، بدون مخزن خاص."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: ar
status: active
visibility: public
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e0c349589cfe3b0cf418f3deb24b7fb097d45ef52358ad19a4958a96d7f5a0ef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:12.883738+00:00"
---
<img src="banner.png" width="100%" alt="dev banner">

# Dev — مساعد المطورين (ATI)

يوفر نظرة عامة ثم يحيل المهمة إلى الأدوات المناسبة.

## الغرض

خليفة ATI/وكيل المطورين الخاص بـ BACH. مهمتان:
1. **فحص المشروع** (بدون واجهة، مكتبة قياسية): نظرة عامة سريعة وموفرة للرموز على
   بنية المشروع ولغاته وعلامات البناء قبل تشغيل تحليل مكلف.
2. **توجيه الأدوات:** يحيل إلى أدوات البرمجة الموجودة بدلاً من تكرارها.

## المحفزات

| إدخال المستخدم | الإجراء |
|---|---|
| "أعطني نظرة عامة على المشروع X" | `dev_core.py scan <pfad>` |
| "ما هذا المشروع / ما المكدس المستخدم؟" | `dev_core.py scan <pfad>` |
| "حلّل هذا الملف / أعد هيكلته" | ← CodeCommander-MCP |
| "أنشئ/افحص كود Python" | ← CodeCommander-MCP / ellmos-code-tools |

## مشهد الأدوات (وجهات التوجيه)

- **CodeCommander-MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`،
  `cc_analyze_methods`، `cc_extract_classes`، `cc_diagnose_imports`،
  `cc_runtime_import_diagnose`، `cc_generate_python_code`، `cc_check_indentation` وغيرها.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): أدوات مطور سطر الأوامر (التحرير البنيوي، سياق pycutter، محلل الدوال).
- **FileCommander-MCP**: عمليات الملفات والمجلدات عبر الأشجار الكبيرة.

## نقطة الدخول عبر سطر الأوامر (dev_core.py)

```bash
python dev_core.py scan .              # aktuelles Projekt
python dev_core.py scan /pfad/projekt  # Struktur + Sprachen + Marker
```

يتعرف، من بين أمور أخرى، على: Python (pyproject/requirements/setup)، وNode/TypeScript، وRust، وGo،
وJava، وRoblox (Rojo)، وDocker، ومستودع Git.

## المخزن

لا يوجد مخزن. فحص خالص وتوجيه.

## الموقف

نوصي بـ CodeCommander/ellmos-code-tools كأدوات برمجة، لكننا منفتحون
على أدوات أخرى (مثل ruff/pylint/eslint) إذا فضّلها المستخدم.

## حماية البيانات

- `dev_core.py` يقرأ فقط أسماء الملفات/المجلدات (البنية)، ولا يقرأ المحتويات، ولا يرفع أي شيء.
- يتم تخطي، من بين أمور أخرى، `.git`، و`node_modules`، و`.venv`، و`__pycache__`.

## الموارد ذات الصلة

- `assist/AGENTS.md` — الموجّه الشامل
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## سجل التغييرات

### 0.1.0 (2026-06-22)
- الإصدار الأولي. خليفة ATI/وكيل المطورين: فحص مشروع بدون واجهة (مكتبة قياسية) + توجيه إلى CodeCommander-MCP / ellmos-code-tools. محايد تجاه المستخدم، بدون مخزن.
