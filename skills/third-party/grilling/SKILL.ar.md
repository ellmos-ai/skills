---
name: grilling
description: "استجوب المستخدم بلا هوادة حول خطة أو قرار أو فكرة. استخدمه عندما يريد المستخدم اختبار تفكيره بصرامة، أو عندما يستخدم أيًّا من عبارات التشغيل المرتبطة بـ'grill' ومنها «استجوبني» و«استجوبني حول هذه الخطة» و«فكّك خطتي بأسلوب الاستجواب» — بما في ذلك العبارات الألمانية مثل \"grill mich\"، أو \"grill mich zu diesem Plan\"، أو \"zerpflück meinen Plan im Grill-Modus\". هو نقطة الدخول لأمر /grill-me ويمكن استدعاؤه مباشرةً أيضًا."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: ar
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

استجوب المستخدم بلا هوادة حتى تصلا إلى فهم مشترك. ضع هذا على شكل **شجرة تصميم**: كل قرار يتفرع إلى القرارات المتعلقة به.

اعمل على الشجرة في **جولات**. **الجبهة** هي كل قرار تكون متطلباته السابقة قد حُسمت بالفعل: الأسئلة التي يمكنك طرحها _الآن_ دون تخمين إجابات لم تسمعها بعد. اطرح الجبهة كاملةً في جولة واحدة: رقّم كل سؤال وقدّم الإجابة التي توصي بها. ثم انتظر إجابات المستخدم قبل الجولة التالية.

نسّق الجولة على النحو التالي:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

تعيد كل إجابة يقدّمها المستخدم تشكيل الشجرة: القرارات المحسومة تدفع الجبهة إلى الخارج وتفتح الأسئلة التي كانت تعتمد عليها. أعد حساب الجبهة واطرح الجولة التالية. السؤال الذي تعتمد إجابته على سؤال آخر لا يزال مفتوحًا في هذه الجولة ينتمي إلى جولة _لاحقة_ لا إلى هذه الجولة.

إيجاد _الحقائق_ من مهامك أنت، لا من مهام المستخدم. عندما يحتاج سؤال في الجبهة إلى حقيقة من البيئة (نظام الملفات، الأدوات، إلخ)، أرسل وكيلًا فرعيًا لإيجادها؛ لا تسأل المستخدم عن أي شيء يمكنك البحث عنه بنفسك. لا تعطّل العمل بسببه: الاستكشاف الجاري متطلب مسبق غير محسوم، لذا فقط الأسئلة اللاحقة له تنتظر تقرير الوكيل الفرعي؛ اطرح بقية الجبهة الآن. أما _القرارات_ فهي للمستخدم: اعرض كل قرار عليه وانتظر.

تنتهي الجلسة عندما تصبح الجبهة فارغة: كل فرع من شجرة التصميم قد زُار، ولا يبقى أي افتراض مُضمَر دون تصريح. لا تبدأ بالتنفيذ قبل أن يؤكد المستخدم أنكما وصلتما إلى فهم مشترك.

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich"). The `category` and `language` fields and this
comment were added; all are local convention (recommended, not one of the
nine house fields), not upstream content, and `language: en` reflects that
the vendored body is unmodified English. The body (the design tree / frontier
/ rounds method) is unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458 alongside skills/third-
party/grill-me/ (the thin, explicit-only entry point that calls this skill).
-->
