---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "استخدمه عندما يريد المستخدم إرسال المطالبة نفسها إلى عدة نماذج لغوية كبيرة ومقارنة إجاباتها — بالتسلسل (ساعة إيقاف، توقيت نظيف لكل مسار) أو بالتوازي (سباق حقيقي)، مع تكرارات اختيارية لكل نموذج، ويحكم عليها النموذج البادئ عبر الجودة والصحة والاكتمال والالتزام بالتعليمات والزمن (الوقت بُعد واحد فقط). يُفعَّل بالأمر /compare-race وبعبارات مثل «model race» و«سباق النماذج» و«vergleiche modelle» و«قارن النماذج» و«gleicher prompt an mehrere modelle» و«نفس المطالبة لعدة نماذج»."
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: ar
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — مهارة المؤشر (بالألمانية)

> **هذه المهارة مؤشر بحت. مصدر الحقيقة هو الوحدة.**

## مسار الوحدة

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

المستودع: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## تعليمات للوكيل

1. اقرأ مطالبة الدور **`prompts/RACE-STARTER.de.md`** في مجلد الوحدة واتبعها.
   أنت RACE-STARTER (بادئ السباق) — وافتراضيًا أيضًا **الحكم** (قرار المستخدم بتاريخ 2026-08-16).
2. افحص الإعداد (`compare-race config`؛ إعداد المضيف في `~/.compare-race/`).
   اختر الوضع: `sequential` = ساعة إيقاف (قياس فردي نظيف لكل مسار) ·
   `parallel` = سباق حقيقي. **ساعة الإيقاف مجرد صورة توضيحية** — الزمن بُعد واحد من بين الجودة والصحة والاكتمال والالتزام بالتعليمات والتكلفة.
3. ابدأ السباق (`compare-race run --prompt-file …`)؛ وبدون coma اسلك المسار اليدوي للنموذج عبر `compare-race record`.
4. بصفتك الحكم، املأ معيار التقييم في `RACE.md` داخل مجلد السباق — اقرأ كل ملف RUN بنفسك؛ وصرّح بالتحيز إذا كان نموذجك الخاص مشاركًا في السباق.
5. انضباط المحاور: لا تُسند نتيجة إلا إذا تغيّر محور واحد بالضبط
   (model = السباق · run = التباين · time = انجراف النموذج).

## تحذير الحصة

تكلّف السباقات **كل** حصة مشاركة (claude/codex/agy/kimi). قبل السباقات الكبيرة (مسارات كثيرة × تكرارات) اسأل المستخدم.
