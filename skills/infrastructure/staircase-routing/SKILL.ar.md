---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "استراتيجية ملاحة وتوجيه مستقلة تبحث في تسلسل المجلدات صعودًا وهبوطًا عن مستندات الإرشاد مثل CLAUDE.md وAGENTS.md وREADME.md وRULES.md، وكذلك عن الكلمات المفتاحية القابلة للتهيئة من قبل المستخدم. يتم الإعداد عبر staircase-config.json أو config.json. وتُعرف أيضًا باسم التوجيه صعودًا وهبوطًا أو توجيه Walking Bass."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
language: ar
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: 28ec74023759355f5a974506a065cb0c737455ec4d3d59d23129276e63011200
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.752002+00:00"
---
<img src="banner.png" width="100%" alt="staircase-routing banner">

# توجيه Staircase (Up-and-Down / Walking Bass Routing)

تُغلّف مهارة **توجيه Staircase**، والمعروفة أيضًا باسم *Up-and-Down Routing* أو
*Walking Bass Routing*، استراتيجية فحص مستندات المجلدات لوكلاء الذكاء الاصطناعي.

عندما يدخل الوكيل مجلدًا أو يعمل على ملف، فإنه يستخدم هذه الاستراتيجية للعثور على
السياق المعتمد والقواعد ومستندات الإرشاد قبل تعديل الشيفرة أو تنفيذ أي إجراء.

---

## 1. معايير مستندات الإرشاد

يبحث توجيه Staircase افتراضيًا عن مستندات الإرشاد التالية:

- **التحكم العام والخاص بالمشروع:** `CLAUDE.md`، `AGENTS.md`،
  `START.md`، `RULES.md`
- **نظرة عامة على المشروع والمهام:** `README.md`، `TODO.md`، `NOTIZ.md`،
  `BEWEISNOTIZ.md`
- **الكلمات المفتاحية المخصصة:** تُهيَّأ عبر
  `staircase-config.json` أو `config.json`.

---

## 2. خوارزمية الاجتياز

```text
                           [ Root- / Workspace-Ebene ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Schritt 2: Root-Wegweiser lesen)
                           └───────────▲────────────┘
                                       │ (Treppe aufwärts)
                           ┌───────────┴────────────┐
                           │ Unterordner / Ziel     │ ◄── (Schritt 1: Im CWD beginnen)
                           └───────────┬────────────┘
                                       │ (Treppe abwärts)
                           ┌───────────▼────────────┐
                           │ Kind- / Modulordner    │ ◄── (Schritt 3: Untergeordnete Wegweiser finden)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### الخطوة 1: فحص دليل العمل الحالي (CWD)

- تحقق من مجلد الملف الهدف أو من دليل العمل النشط.
- إذا وُجدت مستندات إرشاد، فاقرأها فورًا.

### الخطوة 2: الاجتياز صعودًا

- إذا **لم** يُعثر على مستند إرشاد في CWD، فانتقل إلى المجلد الأب
  (`..`).
- كرر ذلك خطوة بخطوة نحو الأعلى، حتى يُعثر على مستند إرشاد جذري
  (`CLAUDE.md` أو `AGENTS.md`) أو تُبلغ حدود مساحة العمل.
- اقرأ جميع مستندات الإرشاد الجذرية التي وُجدت لتحديد التوجيهات العامة وقواعد المشروع.

### الخطوة 3: الفحص هبوطًا

- انطلق من الدليل الجذري الذي حُدد نحو المجلدات الفرعية ذات الصلة بالمهمة.
- ابحث عن مستندات الإرشاد المتخصصة على مستوى الوحدات أو قواعد النطاقات أو إعدادات المكونات واقرأها.

---

## 3. الكلمات المفتاحية القابلة للتهيئة من قبل المستخدم (`staircase-config.json`)

يمكن للوكلاء قراءة `staircase-config.json` محلي أو عام لتخصيص أدلة الإرشاد التي يبحثون عنها:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. التكامل مع `letter-hooker` والمهام المجدولة

`staircase-routing` مُدمج بوصفه محمّل الفحص الأولي المركزي في المهارة
**`letter-hooker`** والمهمة المجدولة
**`antigravity-kontext-and-workflow-loader-and-divider`**. وبذلك يعثر الوكلاء على مستندات الإرشاد ويتبعونها
قبل بدء أي تعديلات.
