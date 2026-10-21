---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: "يشير إلى الوحدة المستقلة steuer-assistent: ورقة عمل محلية تعمل دون اتصال بالإنترنت أولاً لإيصالات نفقات الدخل المرتبطة بالعمل الألمانية (Werbungskosten) -- تسجيل، وجمع حتى السنت، وتصدير ZIP خاص. استخدم هذه المهارة عندما ينبغي إعداد إيصالات نفقات الدخل المرتبطة بالعمل (Werbungskosten) بطريقة منظمة -- مع حدّ واضح: ليست نصيحة ضريبية، ولا فحص لقابلية الخصم، ولا إنشاء أو تقديم لإقرار ضريبي (ويتم ذلك عبر ELSTER أو البرامج المعتمدة)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: ar
status: active
visibility: public
translated_from_sha256: 0beb350be5741675f21d27461094e9908be7de7c209e659bed7b55ab374c1bb3
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="steuer-assistent banner">

# steuer-assistent -- مهارة مرجعية

هذه المهارة **غلاف مرجعي خفيف (Wrapper)** يشير إلى مستودع الوحدة المستقل والعام
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
(ترخيص MIT، عام). المهارة الفعلية موجودة هناك -- هذا المستودع يربط ويوثّق التثبيت فقط.

## ما تفعله الوحدة

`steuer-assistent` وحدة Python صغيرة تعمل دون اتصال بالإنترنت أولاً، لإيصالات Werbungskosten (نفقات الموظف المرتبطة بالعمل) المصنفة ذاتياً:

- تسجيل الإيصالات (الفئة، والمبلغ، والتاريخ، وملاحظة اختيارية).
- جمع نفقات Werbungskosten المسجلة حسب السنة بدقة السنت.
- تصدير ملف ZIP خاص وغير رسمي كورقة عمل (CSV + ملخص + تنبيه بأن الملف غير رسمي، دون ملفات الإيصالات).
- مخزن محلي (الافتراضي `%USERPROFILE%\.steuer-assistent\steuer.db`)، دون وصول إلى الشبكة، ودون رفع إلى السحابة، ودون وصول إلى قواعد بيانات تخص جهات أخرى.

## الحدود (مهم)

- **ليست استشارة ضريبية.** لا تفحص الوحدة قابلية خصم البنود الفردية، ولا تُنشئ إقراراً ضريبياً أو تقدّمه.
- يتم الإرسال الرسمي الإلكتروني حصراً عبر ELSTER أو البرامج المعتمدة لذلك -- وليس عبر هذه الوحدة.
- النطاق: ورقة عمل خاصة لنفقات Werbungskosten للموظفين؛ لا تسجيل لنفقات الأعمال التجارية أو نفقات التشغيل.

## التثبيت (عام، دون مسارات محلية محددة)

1. استنساخ الوحدة:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <klon-pfad>
   ```
2. تثبيت الوحدة والتحقق منها:
   ```bash
   cd <klon-pfad>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. نقل `<klon-pfad>/SKILL.md` إلى بيئة المهارات الخاصة بك (مثلاً
   `~/.claude/skills/steuer-assistent/`). لا تُدرج أي مسارات محلية حقيقية أو أسماء مضيفين في بيئة مهارات مُدارة بالإصدارات.
4. عدّل مسار المخزن عند الحاجة عبر `STEUER_ASSISTENT_DB=<pfad>` أو
   `--store <pfad>`؛ والافتراضي هو دليل المستخدم.
5. تفاصيل أوامر CLI والخصوصية والحدود: راجع README في مستودع الوحدة.

## أصل هذه المهارة المرجعية

أُعدّ هذا الغلاف في 2026-07-23 كمدخل عرض توضيحي لمستودع `ellmos-ai/skills`. **لا يحدث أي تكرار للشيفرة** -- تبقى الصيانة والإصدارات حصراً في مستودع الوحدة `ellmos-ai/steuer-assistent`.

## سجل التغييرات

### 0.1.0 (2026-07-23)
- مهارة مرجعية أولية تشير إلى `ellmos-ai/steuer-assistent`.
