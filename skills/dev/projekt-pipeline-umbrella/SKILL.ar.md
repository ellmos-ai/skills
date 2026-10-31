---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "مهارة فوقية/شاملة (Meta-/Umbrella-Skill) لعائلة „إنشاء المشاريع/خطوط المعالجة وإعادة هيكلتها\". تعرف جميع المهارات الخاصة بإنشاء المشاريع وخطوط المعالجة وتسجيلها وإعادة هيكلتها وتحليلها، وتحيل إلى المهارة المناسبة. استخدم هذه المهارة عندما يكون غير واضح ما إذا كان يجب إنشاء شيء جديد (Greenfield) أو إعادة هيكلة شيء قائم (Bestand)، أو ما إذا كان الأمر يتعلق بمشروع واحد أم بخط معالجة كامل. تُفعَّل أيضًا عند عبارات مثل „إنشاء مشروع/خط معالجة جديد\"، „إعادة هيكلة قائم\"، „تسجيل مشروع\"، „تجديد بنية المجلدات\"، „أي أداة تهيئة مناسبة\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: ar
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
translated_from_sha256: 4a9761a120e11fee3911e26619e8d3b27f0b91e19925d6bc41ba7e44792a96c9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.802083+00:00"
---
<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">
# إنشاء المشاريع/خطوط المعالجة وإعادة هيكلتها — مهارة شاملة (Umbrella)

## الغرض

نقطة الدخول لعائلة „إنشاء المشاريع/خطوط المعالجة وإعادة هيكلتها". تصنّف الأعضاء نفسها وفق محورين: **Greenfield مقابل Bestand** و**مستوى المشروع مقابل مستوى خط المعالجة**. تمنع هذه المهارة الشاملة الخلط الشائع بين „bootstrap" و„optimize" و„onboard".

## الأعضاء والتوجيه

| المهارة | الغرض | متى تُستخدم بدلًا من الأخرى |
|---------|-------|-------------------------------|
| `/project-bootstrapper` | إنشاء مشروع جديد **داخل** خط معالجة قائم | Greenfield، مستوى المشروع |
| `/pipeline-bootstrapper` | إنشاء خط معالجة جديد على المستوى الأعلى بالكامل | Greenfield، مستوى خط المعالجة (نادرًا) |
| `/project-onboarding` | تسجيل/توثيق مشروع قائم | Bestand، مستوى المشروع |
| `/pipeline-optimizer` | تجديد خط معالجة/بنية قائمة (إجراء من 6 خطوات) | Bestand، إعادة هيكلة |
| `/docs-analysis` | التحقق من مستندات المتطلبات/المفاهيم مقابل الشيفرة الحالية | Bestand، تحليل (دون إعادة هيكلة) |
| `/dev-cycle` | إطار تطوير من 8 مراحل للبناء الفعلي | بشكل عرضي: الكيفية التي يتم بها التطوير |

> قاعدة التوجيه: **جديد + مشروع** ← `/project-bootstrapper` · **جديد + خط معالجة** ←
> `/pipeline-bootstrapper` · **تسجيل قائم** ← `/project-onboarding` · **إعادة هيكلة قائم** ←
> `/pipeline-optimizer` · **التحقق فقط** ← `/docs-analysis` · **البناء** ← `/dev-cycle`.

## مجموعات متصلة جيدًا

- `/project-onboarding` (أولًا: تسجيل الوضع القائم) ← `/pipeline-optimizer` (لاحقًا: إعادة هيكلة موجهة) —
  افهم أولًا ثم جدِّد (يغطي مبدأ الإجراء من 6 خطوات „اقرأ أولًا، ثم اكتب").
- `/docs-analysis` (إيجاد الثغرات) ← `/dev-cycle` (سد الثغرات).
- `/project-bootstrapper` (الهيكل الأساسي) ← `/dev-cycle` (تطوير المحتوى).

## الاتفاقيات المشتركة

- اقرأ دائمًا اتفاقيات خط المعالجة القائم (السجل، والقوالب، وCLAUDE.md) أولًا — لا تُنشئ معايير موازية.
- مهارات Greenfield تنشئ، ومهارات Bestand تُجدِّد — لا تخلط بينهما.
- اقرأ الملفات الحية للمهارات الفردية قبل التطبيق.

## سجل التغييرات

### 0.1.0 (2026-06-17)
- نسخة أولية. أُنشئت بواسطة وضع التدقيق (3c1) لعائلة مشروع/خط المعالجة.
