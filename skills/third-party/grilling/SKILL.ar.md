---
name: grilling
description: "استجوب المستخدم بلا هوادة حول خطة أو قرار أو فكرة. استخدم هذه المهارة عندما يريد المستخدم اختبار تفكيره بصرامة، أو يقول «grill me» أو «grill-me» (الأمر السابق /grill-me استُبدل بالأمر /grilling)، أو يستخدم أي عبارة تشغيل أخرى مرتبطة بـ«grill»، بما فيها العبارات الألمانية «grill mich» و«grill mich zu diesem Plan» و«zerpflück meinen Plan im Grill-Modus» والعبارات العربية «استجوبني» و«استجوبني حول هذه الخطة» و«فكّك خطتي بأسلوب الاستجواب». استخدمها أيضًا عندما تنتهي جلسة التخطيط ويسأل المستخدم إن كان هناك شيء ما زال مفتوحًا."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: ar
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
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

## إضافات محلية

توسّع هذه القواعد المنهج الأصلي ولا تغيّره.

1. **ابدأ الشجرة مما كُتب بالفعل.** قبل الجولة الأولى، اقرأ الخطة والمكان الذي يسجّل فيه المشروع قراراته، واجمع كل بند ما زال مفتوحًا أو مقترحًا أو غير مؤكّد. لا تُعد طرح نقطة حُسمت؛ أشر إليها بدلًا من ذلك.
2. **دوّن كل إجابة قبل الجولة التالية.** سجّل كل إجابة في سجل قرارات المشروع بوصفها محسومة، مع التاريخ والمصدر. فالإجابة الموجودة في المحادثة وحدها تضيع بعد إعادة ضبط السياق.
3. **أوقف مؤقتًا ولا تبدأ من جديد عند المقاطعة.** إذا طلب المستخدم إنجاز شيء آخر أولًا، فأنجزه ثم تابع من الأسئلة المفتوحة المتبقية. تظل النقاط المحسومة محسومة.
4. **ادعم كل توصية بسبب واحد.** قدّم الإجابة التي توصي بها واذكر الحقيقة أو القاعدة الواحدة التي تستند إليها. لا تصبح التوصية قرارًا إلا بعد أن يؤكدها المستخدم.
5. **اعرض الحقائق التي تحققت منها.** عندما يستند سؤال إلى معلومة بحثت عنها، اذكر النتيجة ومصدرها كي يقرر المستخدم استنادًا إلى الأدلة.
6. **اسأل بلغة المستخدم.** اجعل الأسئلة والتوصيات بلغة المستخدم؛ وتبقى المعرّفات كما هي.
7. **اختم بسجل.** عندما تنتهي الأسئلة المفتوحة، اذكر ما تقرر وما تُرك مفتوحًا عمدًا، ثم اطلب تأكيد أن الفهم مشترك.

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" /
  "grill-me" phrases, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the phrase triggers moved into
this description. The native /grill-me command no longer exists; /grilling
replaces it. The description only adds semantic matching and registers no
alias command. Rules 1-7 come from a planning session of the same day.
-->
