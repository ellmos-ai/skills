---
name: dev-cycle
version: 1.2.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-08-22
description: "دورة تطوير من 8 مراحل: طلبات الميزات، والحالة الراهنة، والتخطيط الوظيفي، والواجهة الأمامية، والتخطيط الخلفي، وكود الخلفية، والاختبارات، وحالات الاستخدام. إطار عمل تكراري لتطوير البرمجيات بصورة منهجية."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 3d82b648971c28906aeabf5b953a28ac162897503581e5cb5a6af8d9f0b1ae8f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="dev-cycle banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# دورة التطوير (Dev Cycle) (Deutsch)

> **الهدف:** عملية منظمة من طلب الميزة وصولًا إلى نظام مُتحقَّق منه.
> تمرّ كل عملية تطوير عبر هذه المراحل الثماني.

> 📐 **ملحق:** `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` —
> "مخطط دائرة هندسة البرمجيات" القابل للقراءة البشرية (HTML، يُفتح في المتصفح):
> خريطة شاملة مُستقاة من البحث تضم المراحل والحلقات التنظيمية والأدوار وسلاسل العمليات وبوابات الاختبار
> (بحث ويب 08/2026)، ويندرج ضمنها دورة المراحل الثماني هذه.

---

## نظرة عامة والغرض

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                           |
  +--------------------------------------------------------------+
  |                                                                |
  |  Phase 1   Feature Requests (functional requirements)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 2   Check Current State (What already exists?)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 3   Functional Planning                                 |
  |            (Workflows, Agents, Experts, Skills, Services)      |
  |     |                                                          |
  |     v                                                          |
  |  Phase 4   Implement Functional Frontend                       |
  |            (Skill files, workflow markdown, agent profiles)     |
  |     |                                                          |
  |     v                                                          |
  |  Phase 5   Plan and Align Backend                              |
  |            (CLI handlers, DB schema, API endpoints)            |
  |     |                                                          |
  |     v                                                          |
  |  Phase 6   Implement Backend Tasks                             |
  |            (Python code, tools, DB migrations)                 |
  |     |                                                          |
  |     v                                                          |
  |  Phase 7   Test Execution, Review Gate and Bugfixes           |
  |            (B/O/E tests, bugfix protocol, code review)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 8   Functional and Feature Test: USE CASES              |
  |            (End-to-end validation from user perspective)        |
  |                                                                |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
  - Shift-Left: tests are DESIGNED early (phases 1/3/5) and WRITTEN
    with the code (phase 6) - phase 7 only EXECUTES them
```


---

## المرحلة 1: طلبات الميزات (المتطلبات الوظيفية)

**ما هي:** جمع المتطلبات الوظيفية وصياغتها.

**المدخلات:**
- رغبات المستخدمين وأفكارهم ومشكلاتهم
- اقتراحات الشركاء (مساعدو LLM)
- رؤى من حالات الاستخدام (حلقة تغذية راجعة!)

**المخرجات:**
- مهام في نظام المهام (مثلاً كمسألة (issue) أو تذكرة أو قائمة TODO)
- تصف المتطلبات ما هو مطلوب، لا كيفية تنفيذه
- يحمل كل متطلب معايير قبول قابلة للاختبار (Shift-Left: تصبح حالات الاستخدام في المرحلة 8 وقائمة التحقق من القبول)

**القواعد:**
- صِغ المتطلبات دائمًا بصيغة وظيفية ("يستطيع المستخدم أن يفعل X")
- لا تصغها بصيغة تقنية ("نفّذ نقطة نهاية REST للـ X")
- استخدم حالات الاستخدام كمصدر للمتطلبات (المرحلة 8 ← المرحلة 1)

---

## المرحلة 2: التحقق من الحالة الراهنة

**ما هي:** جرد الوظائف الموجودة.

**قائمة التحقق:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**المخرجات:**
- توثيق لما هو موجود، وما هو مفقود، وما يحتاج إلى توسيع
- تجنّب التكرار

---

## المرحلة 3: التخطيط الوظيفي

**ما هي:** التخطيط على المستوى الوظيفي - لا تكتب الكود فورًا.

**مستويات التخطيط:**

| المستوى | السؤال | المُخرَج |
|---------|--------|--------|
| سير العمل | متى/كيف يتم التنسيق؟ | workflows/*.md |
| الوكيل | من ينفّذ؟ | agents/*.txt |
| الخبير | من يملك المعرفة المتخصصة؟ | experts/*/ |
| المهارة | ماذا يُنجز؟ | skills/*.md |
| الخدمة | كيف يُنجز تقنيًا؟ | services/*/ |

**القواعد:**
- فكّر وظيفيًا أولًا، ثم تقنيًا
- Shift-Left: لكل مستوى تخطيط، خطّط للفحص الخاص به أيضًا — متطلب ← معيار قبول، خدمة/واجهة ← اختبار تكامل، وحدة ← اختبار وحدة (اختيار مستوى الاختبار وتقنيته: [software-testing](../software-testing/SKILL.md))
- تصف سير العمل العمليات، لا تفاصيل التنفيذ
- يحتاج كل وكيل إلى ملف تعريف واضح
- يجب أن تعمل الخدمات دون بيانات المستخدم

---

## المرحلة 4: تنفيذ الواجهة الأمامية الوظيفية

**ما هي:** إنشاء ملفات المهارات وملفات سير العمل بصيغة Markdown وملفات تعريف الوكلاء.

"الواجهة الأمامية" هنا هي طبقة الوصف الوظيفي:
- ملفات سير العمل (.md)
- ملفات تعريف الوكلاء (.txt)
- المعرفة الخبيرة
- أوصاف الخدمات
- ملفات المساعدة

**المخرجات:**
- توجد كل الأوصاف الوظيفية
- يستطيع شريك LLM أن يقرأ سير العمل ويفهمه
- الطبقة الوظيفية موثقة بالكامل

---

## المرحلة 5: تخطيط الخلفية ومواءمتها

**ما هي:** مواءمة البنية التقنية مع الواجهة الأمامية الوظيفية.

**مجالات التخطيط:**

| المجال | السؤال | الموقع |
|--------|--------|--------|
| معالجات CLI | أي الأوامر؟ | handlers/*.py |
| مخطط قاعدة البيانات | أي الجداول/الأعمدة؟ | schema/*.sql |
| نقاط نهاية API | أي نقاط نهاية للواجهة الرسومية؟ | server.py |
| الأدوات | أي سكربتات Python؟ | tools/*.py |

**المخرجات:**
- خطة تقنية متوافقة مع الواجهة الأمامية الوظيفية
- تصميم مخطط قاعدة البيانات
- بنية أوامر CLI

---

## المرحلة 6: تنفيذ مهام الخلفية

**ما هي:** كتابة كود Python وترحيلات قاعدة البيانات ومعالجات CLI.

**قائمة التحقق (لكل مهمة):**
```
  [ ] Unit tests written (TDD: test before code) and green locally?
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## المرحلة 7: تنفيذ الاختبارات وبوابة المراجعة وإصلاح الأخطاء

**ما هي:** ضمان الصحة التقنية. صُمّمت الاختبارات في المراحل 1/3/5 وكُتبت في المرحلة 6 (Shift-Left) — تقوم المرحلة 7 بتنفيذها في بوابات متدرجة ومانعة: الاختبارات السريعة عند كل commit، والاختبارات المكلفة (الانحدار الكامل، والاختبار الشامل E2E، والحمل) ليلًا أو قبل الإصدار. تعيين البوابات واختيار الاختبارات: [software-testing](../software-testing/SKILL.md).

**أنواع الاختبارات (B/O/E):**

| النوع | المنظور | الوصف |
|-------|---------|-------|
| اختبارات B | خارجي/مؤتمت | اختبارات مؤتمتة، CI/CD |
| اختبارات O | وظيفي (إدخال←إخراج) | تحقق وظيفي يدوي |
| اختبارات E | ذاتي/تجريبي | تقييم تجربة المستخدم وأرغونوميا الاستخدام |

**بوابة المراجعة (قبل المرحلة 8):**
- مراجعة الكود من زوج آخر من العيون (زميل، أو وكيل مراجع، أو مستشار)
- لا يدخل شيء إلى التحقق بحالات الاستخدام دون مراجعة
- تعود نتائج المراجعة إلى المرحلة 6 كطلبات تغيير

**عند وجود أخطاء:**
- طبّق بروتوكول إصلاح الأخطاء
- التزم بقاعدة الـ 20 دقيقة (غيّر النهج بعد 20 دقيقة)
- وثّق الدروس المستفادة

---

## المرحلة 8: اختبار وظيفي وخاص بالميزات - حالات الاستخدام

**ما هي:** التحقق من البداية إلى النهاية من منظور المستخدم.

**تخدم حالات الاستخدام غرضين معًا:**
1. **مؤشرات الميزات** - ماذا يُراد؟ وماذا ينبغي أن يكون ممكنًا؟
2. **سيناريوهات الاختبار** - هل يعمل فعلًا من الألف إلى الياء؟

**صيغة حالة الاستخدام:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**حلقة التغذية الراجعة:**
- حالات الاستخدام الفاشلة ← مهام جديدة في المرحلة 1
- حالات الاستخدام الناجحة ← ميزات مُتحقَّق منها
- أفكار حالات استخدام جديدة ← تُسجَّل كمهام

---

## الخلاصة: الدورة

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

الدورة حلقة متكررة: تتحقق حالات الاستخدام من الميزات وتولّد في الوقت نفسه متطلبات جديدة.

---

## حلقات التحكم (Regelkreise)

دورة المراحل الثماني هي حلقة التحكم الخارجية. وداخلها تعمل حلقات أسرع بالتوازي — وكلما كانت الحلقة أقرب إلى الداخل زادت سرعة إيقاعها وانخفضت تكلفة الإصلاح:

| الحلقة | الإيقاع | موقعها في الدورة |
|--------|---------|-------------------|
| TDD (أحمر–أخضر–إعادة الهيكلة) | ثوانٍ–دقائق | داخل المرحلة 6 |
| تنفيذ الاختبارات / بوابات CI | أقل من 10 دقائق لكل commit | المرحلة 7 ← المرحلة 6 عند الفشل |
| بوابة المراجعة (4 أعين) | ساعات | بين المرحلة 7 والمرحلة 8 |
| حلقة إصلاح الأخطاء | ساعات | المرحلة 7 ← المرحلة 6 (بروتوكول الإصلاح) |
| حلقة حالات الاستخدام | لكل دورة | المرحلة 8 ← المرحلة 1 |
| التغذية الراجعة التشغيلية | مستمرة | المراقبة/الحوادث ← المرحلة 1 |

قاعدة عامة: أبقِ الزمن من الـ commit حتى التغذية الراجعة دون 10 دقائق — فالحلقة البطيئة يتم تجاوزها. خريطة مرئية لجميع الحلقات مع أزمنتها: الملحق المرفق `SCHALTPLAN-SOFTWAREENTWICKLUNG.html`، الورقة BL-2.

---

## مهارات خاصة بالمراحل

| المرحلة | المهارة المتخصصة | المحفّز |
|---------|------------------|---------|
| المراحل 1-3 | Project bootstrapper (إن توفّر) | إنشاء مشروع جديد (Greenfield) |
| المرحلة 2 | [project-onboarding](../project-onboarding/SKILL.en.md) | تولّي مشروع قائم |
| المراحل 2-3 | [docs-analysis](../docs-analysis/SKILL.en.md) | مقارنة وثائق المتطلبات بالكود |
| المراحل 5-6 | [pipeline-optimizer](../pipeline-optimizer/SKILL.en.md) | تجديد الهياكل القائمة |
| المرحلة 7 | [bugfix-protocol](../bugfix-protocol/SKILL.en.md) | تصحيح الأخطاء المنهجي من 6 مراحل |
| المراحل 7-8 | [bugsweep](../bugsweep/SKILL.en.md) | مسح متقارب للأخطاء قبل الإصدار |
| المراحل 1 و3 و7 | [software-testing](../software-testing/SKILL.md) | اختيار مستويات الاختبار وأنواعه وتقنيات تصميمه؛ تعيين بوابات CI/CD |
| بعد المرحلة 8 | [github-repo-care](../github-repo-care/SKILL.en.md) | الإصدار: نشر المستودع وصيانته |

إذا كانت مجموعة المهارات لديك تحتوي على فهرس للمهارات، فابحث فيه عن مهارات إضافية خاصة بالمراحل.

---

## سجل التغييرات

### 1.2.0 (2026-08-22)
- ترسيخ Shift-Left (مواءمة مع نتائج البحث ومخطط الملحق): معايير القبول كمخرج للمرحلة 1، وتصميم الاختبارات لكل مستوى تخطيط في المرحلة 3، واختبارات الوحدة (TDD) كأول بند في قائمة التحقق للمرحلة 6؛ أُعيدت تسمية المرحلة 7 إلى "تنفيذ الاختبارات وبوابة المراجعة وإصلاح الأخطاء" — تُنفَّذ الاختبارات هناك ولا تُكتب فقط
- بوابة المراجعة (مبدأ الأربع أعين) كخطوة صريحة قبل المرحلة 8
- قسم جديد "حلقات التحكم (Regelkreise)" مع أزمنة الإيقاع (TDD وCI والمراجعة وإصلاح الأخطاء وحالات الاستخدام والتشغيل)
- توسيع جدول مهارات المراحل: software-testing (المراحل 1/3/7)، github-repo-care (بعد المرحلة 8)؛ وإحالات إلى software-testing في المرحلتين 3 و7

### 1.1.1 (2026-08-22)
- الملحق `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (الخريطة الشاملة القابلة للقراءة البشرية: المراحل والحلقات التنظيمية والأدوار وسلاسل العمليات وبوابات الاختبار — تركيب من بحث ويب 08/2026) مع إحالة في رأس الملف

### 1.1.0 (2026-06-13)
- جدول "مهارات خاصة بالمراحل" جديد مع إحالات إلى project-onboarding وdocs-analysis وpipeline-optimizer وbugfix-protocol وbugsweep

### 1.0.0 (2026-03-12)
- نُقل من BACH (dev-zyklus v1.0.0)

---

*أُنشئ: 2026-01-28 | نُقل: 2026-03-12*
