---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "شرط إنهاء الحلقات المستقلة: متابعة العمل ذاتياً قدر الإمكان، وعدم إنهاء الحلقة إلا عندما يثبت أنه لم تعد هناك مهمة قابلة للتنفيذ بشكل مستقل. مجرد الانطباع بأنه \"لم يعد هناك ما يمكن فعله\" لا يكفي — فهو يُطلق سلسلة تحقق من أربع مراحل (think/decide, _CONTROL/_DECISIONS, Gardener/USMC, decision-avatar/BYUM)، يجب أن تكسب أولاً مهامَّ جديدة قبل أن يُسمح بانتهاء الحلقة. تُبلغ كل خطوة من خطوات السلسلة عن found/empty/unavailable بدلاً من نتيجة ثنائية — ولا يُعتبر \"exhausted\" إلا إذا كانت جميع المصادر قابلة للاستعلام فعلاً؛ وإذا كان مصدر واحد على الأقل unavailable، يُبلغ المهارة عن \"blind\" بدلاً من \"exhausted\" ولا تدّعي شيئاً لم يُتحقق منه. استخدم هذه المهارة مع /work-autonomous و/waafap و\"arbeite autonom weiter bis nichts mehr zu tun ist\"، أو كشرط هدف ضمن /loop، أو عندما يُراد التحقق مما إذا كان لم يبقَ فعلاً أي عمل مستقل قبل إنهاء حلقة أو جلسة."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: ar
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: a8ee248e73bb81d9af36df2f3e82719bed0f31e89005ab64c35f4e236b15600c
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T11:58:01.178661+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — إنهاء الحلقة فقط بعد التحقق من عدم وجود مهام مستقلة

## الغرض

تحقق هذه المهارة أمرين في آن واحد:

1. **متابعة العمل ذاتياً قدر الإمكان** — عمل جلسة عادي تماماً، دون أي خصوصية.
2. **عدم إنهاء الحلقة إلا بعد إثبات** أنه لم تعد توجد أي مهمة قابلة للتنفيذ بشكل مستقل. إن الشعور بأنه "لم أعد أجد ما أفعله" **ليس** سبباً للإنهاء — بل هو **المُحفِّز** لسلسلة تحقق تحاول أولاً **كسب** مهام جديدة. ولا يُعتبر الإنهاء مثبتاً إلا عندما تبقى هذه السلسلة بلا أي نتيجة بالكامل.

**بدون `/goal` مدمج عن قصد:** المهارة قابلة للاستخدام المستقل (مثلاً مباشرةً كاستدعاء `/work-autonomous` ضمن جلسة عادية)، وكذلك كشرط داخل بنية حلقة أعلى منها: تُمنح `/loop` بشكل عادي، ثم يُذكر هذه المهارة وحدها كهدف. ويكون الهدف حينئذٍ بالمعنى: *"أنهِ الحلقة عندما لا تعود توجد مهام مستقلة — وتابع العمل ذاتياً قدر الإمكان حتى ذلك الحين."* ولا تستدعي المهارة نفسها أي بنية `/goal`؛ بل تقدم فقط إشارة الإنهاء الواضحة التي يمكن لتلك البنية قراءتها (انظر "إشارة الإنهاء" أدناه).

## نموذج التشغيل — مستويان

### المستوى 1 — العمل الاعتيادي (كل دورة)

#### بوابة استيعاب TICKET-MASTER (لها الأولوية على كل ما عداها في هذا المستوى)

**ذات صلة فقط عندما يكون نظام التذاكر (`_TICKETS/`) جزءاً من السياق أصلاً** — الجلسات دون نظام تذاكر تتجاوز هذه البوابة دون أي أثر، وتبقى المهارة قابلة للاستخدام المستقل تماماً دون أي نظام تذاكر (انظر "الغرض" أعلاه). يجب أولاً التحقق مما إذا كانت `INBOX/` — بما في ذلك المدخلات غير الرسمية التي لم تُصغ بعد بصيغة التذاكر — مُهيكلةً ومُصنَّفةً بالكامل. وإذا لم يكن الأمر كذلك، يُحتسب ذلك بالضبط كعمل مستقل وُجد (فالهيكلة والتصنيف عمل كتابي دون قرار من المستخدم، انظر التمييز أدناه) — يُنجز، وتنتهي الدورة، ولا يُدخل المستوى 2، كما في أي مصدر آخر من مصادر المستوى 1.

**طالما كانت INBOX مفتوحة، لا يجوز أن تنشأ `NO_WORK`، ولا إشارة استنفاد (`exhausted`/`blind`)، ولا Guard-STOP، ولا أي إشارة إنهاء أخرى.** فقط بعد اكتمال تصنيف الاستيعاب بالكامل يجوز فحص `ACTIONABLE`، والتذاكر المفتوحة `BLOCKED`، والتذاكر المستحقة `WAITING` (أدناه) — ثم، إن لزم، المستوى 2.

*حالة تطبيقية:* بدأت حلقة فحص الاستنفاد بعد إنجاز `ACTIONABLE`، بينما كانت تصل باستمرار تذاكر `INBOX` جديدة، منها تذكرتان بالأولوية P1. دون هذه البوابة كانت الحلقة ستُبلغ عن `exhausted`/`blind` رغم أن المدخل كان مفتوحاً — وهذا بالضبط ما تمنعه البوابة.

ثم ابحث بشكل اعتيادي عن أي عمل آخر قابل للتنفيذ بشكل مستقل (انظر التمييز أدناه) ونفّذه: تذاكر `ACTIONABLE` المفتوحة، وتذاكر `BLOCKED` المفكوكة من الحجب، وتذاكر `WAITING` المستحقة، والنقاط المفتوحة `TODO.md`/`AUFGABEN.txt` في المشاريع التي لا تعتمد على المستخدم، وفحوص الروتين/الصيانة المستحقة وفق السياسة المحلية، والعمل المبدوء ولكن غير المكتمل من الجلسة الأخيرة (USMC `working`)، **وتشغيلات `tidy-up` المستحقة للمشروع النشط** (إضافة 1.3.0، 2026-08-19 — انظر المهارة `tidy-up`: تمرير Tasksolver+Writer+Maintainer على مجلد المشروع الذي كانت الجلسة تعمل فيه؛ ويتحقق `tidy-up` من الاستحقاق بنفسه عبر سجل USMC الخاص به والمختصر، انظر قسمه "العلاقة مع work-autonomous").

→ **وُجد وأُنجز:** أبلغ بالنتيجة باختصار، تنتهي الدورة، وتستمر الحلقة بشكل طبيعي. لا يُدخل المستوى 2 — فلا حاجة لأي من خطوات التحقق الأربع المكلفة ما دام هناك عمل مرئي.

### المستوى 2 — فحص الاستنفاد (فقط عند الاشتباه في "لم يعد هناك ما يُفعل")

لا ينشأ الاشتباه إلا عندما لا يجد المستوى 1 **أي** عمل مستقل. ولا يكفي هذا الاشتباه وحده. عندها تُنفَّذ **وجوباً** السلسلة التالية لكسب مهام جديدة.

#### معرفة الذات (قبل السلسلة، لا بعدها)

قبل الاستعلام عن أي شيء: تُعلن المهارة أي المصادر تحتاجها لحكمها. أربعة احتياجات (`grounding_seed.self_knowledge.Need`، إذا كانت `grounding-seed` مثبتة — وإلا تبقى القائمة نفسها إعلاناً فقط دون ربط بالمكتبة):

| الدور | خطوة السلسلة | ما وراءه |
|---|---|---|
| `decisions.ledger` | 2 | سجل القرارات المركزي |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (الخطوة 1) ليس مصدرًا معلنًا عن قصد.** إنه خطوة التحليل الخاصة بالنموذج نفسه، وليس نظامًا خارجيًا قد يكون متاحًا أو غير متاح — فهو دائمًا "متاح" بالمعنى المقصود في هذا التمييز. يمكن فقط للخطوات 2–4 أن تصبح `unavailable`.

أداة اختيارية قابلة للاختبار للسؤال المحض عن التحديد المكاني (found/unavailable، دون فحص للمحتوى بعد): `scripts/exhaustion_check.py` في مجلد المهارة هذا. وهي تستخدم `grounding_seed.resolve()` + `status_from_resolution()` من أجل `decisions.ledger`/`user.model` (يوجد هناك مزوّد `source-resolver` حقيقي)، وتتحقق من `memory.organic`/`memory.curated` مقابل ذلك **دائمًا** مباشرةً عبر إمكانية الوصول إلى CLI (`gardener`/`usmc` في PATH) — فلهذين الدورين لم يكن هناك حتى 2026-08-15 أي مزوّد `source-resolver` مسجَّل؛ وكان الاستعلام عنهما عبر المحلل سيُبلغ فقط عن `unavailable`، بصرف النظر عما إذا كانت Gardener/USMC مثبتتين فعلًا. وتعمل الأداة بالطريقة نفسها سواء كان `grounding-seed` مثبتًا أم لا.

**تحديث 2026-08-25 (K3=C، `T-20260825-342866657`):** تم سد الفجوة — إذ يسجّل `source-resolver` الآن `memory.organic` (Gardener) و`memory.curated` (USMC) كلاهما بوصفهما دورًا من المستوى 1 مع فحص الحضور نفسه عبر CLI (`shutil.which("gardener")`/`shutil.which("usmc")`)، الذي كان هذا السكربت يُنفّذه بشكل مُشفّر داخليًا حتى الآن. ولذلك لم يُعَد بناء `exhaustion_check.py` فورًا (لا توجد خسارة في الوظيفة، فالفحص الحالي يبقى صحيحًا) — ويمكن في تشغيل صيانة المهارة التالي تحويل الخطوة 3 إلى `source_resolver.resolve("memory.organic"/"memory.curated")`، على غرار الخطوة 2 (`decisions.ledger`)، بدلًا من الحفاظ على فحص CLI بشكل مزدوج.

#### الخطوات الأربع للسلسلة — كل خطوة تُبلغ found | empty | unavailable

تسير كل خطوة على مرحلتين: أولًا **التحديد المكاني** (هل أعرف أصلًا موقعًا يمكن الوصول إليه؟)، ثم — فقط إذا تم تحديده — **فحص المحتوى** (يقرأ النموذج فعليًا ما إذا كان هناك شيء جديد، باستخدام أدواته الخاصة). ولا يُفحَص مصدر لم يمكن تحديد موقعه من حيث المحتوى أبدًا — إذ يُحتسب `unavailable`، لا `empty`.

1. تطبيق **`/think` + `/decide`** على السؤال: "هل لم يعد هناك أي عمل قابل للتنفيذ ذاتيًا، أم أنني أغفل شيئًا؟" — تحليل منظَّم بدلًا من الحدس. لا توجد حالة found/empty/unavailable لهذه الخطوة (انظر أعلاه، لا يوجد مصدر).
2. **`decisions.ledger`** — التحديد المكاني عبر `source_resolver.resolve("decisions.ledger")` / `grounding_seed.resolve(...)`، إن كان مثبتًا؛ وإلا المسار الاحتياطي المعروف (`_control-center/_CONTROL/_DECISIONS/`، سلسلة `TO-DECIDE-USER*.txt`، و`TO-DECIDE-USER-<HOST>.txt` الخاص بالمضيف، و`DECIDED-AND-DONE.md`). إذا تم التحديد → قراءة المحتوى: هل اتُّخذت مؤخرًا قرارات تُفكّ بموجبها أعمال كانت محجوبة أو تنتظر الموافقة؟ إن وُجد ما يطابق → `found`. قُرئ ولا جديد → `empty`. تعذّر التحديد (المحلل مفقود **و**المسار الاحتياطي غير موجود) → `unavailable`.
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — مصدران منفصلان، لكنهما خطوة واحدة في السلسلة. التحديد المكاني: CLI في PATH (`gardener`/`usmc`)، انظر "الوعي الذاتي" أعلاه. إذا كان الوصول ممكنًا → قراءة المحتوى (`find()`/`recall()` أو `usmc facts|lessons|working|context`): نقاط ذاكرة العمل المفتوحة، والدروس ذات المهام اللاحقة غير المنجزة، والحقائق التي تشير إلى عمل قابل للتنفيذ لكنه أُغفل (وهذا بالضبط المكان الذي تترك فيه الجلسات السابقة نقاطًا غير مكتملة — حقل `RESUME:`، وإدخالات `note` المفتوحة). إن وُجد ما يطابق → `found`. قُرئ ولا جديد → `empty`. إذا لم يكن CLI في PATH → `unavailable`.
4. **`user.model` (decision-avatar/BYUM)** — التحديد المكاني كما في `decisions.ledger` (المحلل أو المسار الاحتياطي `_control-center/_CONTROL/_USER-MIND/`). إذا تم التحديد → فحص المحتوى: هل هناك نمط موثَّق يبيّن أن المستخدم أراد رؤية إجراء معين يُنفَّذ ذاتيًا في هذا الموضع؟ لا يُحتسب هذا `found` إلا عند ثقة كافية (🟢/🟡)؛ أما 🔴 فيُحتسب `empty`، لا بوصفه مهمة مكتسَبة، بل بوصفه نقطة مفتوحة لخطوة "بقايا تخص المستخدم وحده" أدناه. تعذّر التحديد → `unavailable`.

**لا يجوز الإبلاغ عن "Exhausted" إلا إذا كانت المصادر الأربعة كلها (الخطوات 2–4، ثلاث خطوات، أربعة أدوار) قد **أمكن** استعلامها فعليًا — أي `found` أو `empty`، ولا مصدر واحد منها `unavailable`.** وهذا يطابق `grounding_seed.self_knowledge.GroundingReport.all_answerable()`.
إذا كان دور واحد على الأقل `unavailable`، فلا ينطبق "exhausted"، بل تُستخدم إشارة "blind" الخاصة بالحلقة (انظر إشارة الإيقاف أدناه) — تنتهي الحلقة مع ذلك (فهي لا تستطيع الاستعلام عن شيء على أي حال)، لكنها لا تدّعي بعد الآن أنها فحصت ما لم تستطع فحصه.

إذا وجدت أي خطوة عملًا جديدًا → العودة إلى المستوى 1، وإنجاز العمل، وضبط حالة الحارس (انظر أدناه) على "found" بدلًا من "exhausted"/"blind".

### الحالة الخاصة: بقايا مرتبطة بالمستخدم فقط

إذا لم تجد السلسلة أي مهمة **ذاتية** التنفيذ، لكن توجد تذاكر `USER/*` أو نقاط `_DECISIONS` غير محسومة مفتوحة، فإن ذلك يظل **إيقافًا للاستقلالية** — لكن ليس بمعنى "لا يوجد ما يُفعل"، بل بمعنى "لا يوجد ما يُفعل *ذاتيًا*". وتُعرض هذه النقاط وفق قاعدة حلقة الاستقلالية في شكل **حزمة مجمّعة** من `ticket-master` (قالب تجميعي واحد، لا إشعارات فردية)، ولا يُستفسر عنها بشكل منفصل. ويميّز إشارة الإيقاف هذه الحالة صراحةً عن الفراغ الحقيقي.

## التمييز — ما الذي يُعدّ "قابلًا للتنفيذ ذاتيًا"؟

المرجع: فئات `ticket-master` (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`).

| الحالة | مستقل؟ | التبرير |
|---|---|---|
| `INBOX/` بما في ذلك الإدخالات غير الرسمية، ضمن TICKET-MASTER (قبل الفرز) | **نعم، بأولوية** | التشكيل والفرز عمل إداري دون قرار من المستخدم — يسبق `ACTIONABLE`/`BLOCKED`/`WAITING` ويحجب حتى ذلك الحين أي إشارة إيقاف (انظر بوابة الاستقبال أعلاه). |
| تذكرة `ACTIONABLE` | **نعم** | لا يوجد عائق ولا اعتماد على المستخدم — بحكم التعريف. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | لا، ما دام العائق لم يزل **تجريبياً** | إعادة الفحص الدورية مسموحة (حلقة الاستقلالية)، و„الوجود" وحده لا يكفي كدليل — يلزم إثبات. |
| `WAITING/*` (scheduled, review-due, marker) قبل الموعد/العلامة | لا | مرتبط بالوقت. |
| `WAITING/*` بعد حلول الموعد/العلامة | **نعم** | الشرط مستوفى ← ينتقل إلى `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **أبداً مستقل** | يتطلب حتماً قرار المستخدم/بياناته/موافقته/عتاده/جلسته. يُعرض مجمّعاً، انظر أعلاه. |
| `PARKED/*` (skip, backlog, until-trigger) | لا، إلا بتكليف/مشغّل صريح | مؤجل عمداً، دون إعادة فحص تلقائية. |
| نقاط `TODO.md`/`AUFGABEN.txt` المفتوحة دون ملاحظة موافقة/قرار | **نعم** | سجل المشروع، عمل اعتيادي. |
| فحوص الصيانة/النظافة الروتينية المستحقة (انتهت فترة التهدئة، لا قفل) | **نعم** | أعمال صيانة منتظمة وفق السياسة المحلية. |
| المناطق المقفلة من قِبل `LOCK.user.*` | **أبداً** | قفل من المستخدم — لا يرفعه إلا المستخدم، انظر LOCK-SYSTEM. |
| خطوات لا رجعة فيها/ذات أثر خارجي دون موافقة السياسة (رفع إلى Zenodo، دفع إلى فروع محمية/محكومة، قرار إنفاق الخادم خارج عتبة الحاسوب المحمول، حذف نهائي دون معاينة) | **لا** | تتطلب موافقة/قراراً، حتى لو كانت قابلة للتنفيذ تقنياً. |
| جلسة لا تبدأ إلا عبر الواجهة الرسومية/تسجيل الدخول (مثل مهمة Claude-Desktop، تسجيل دخول تفاعلي، إجراء عتادي فعلي) | **أبداً** | „جلسة لا يبدأها إلا المستخدم" — لا يمكن لأي حلقة تولّيها. |

القاعدة العملية: المستقل هو ما يمكن إنجازه **دون** قرار المستخدم أو موافقته أو بياناته أو عتاده أو
جلسته، **ولا** يستلزم خطوة لا رجعة فيها أو ذات أثر خارجي دون موافقة سياسة موثّقة.

## الحارس ضد الحلقات اللانهائية (إلزامي)

**المشكلة:** بدون كابح ستعمل سلسلة الخطوات الأربع كاملةً عند كل فحص جديد، رغم أنه لم يتغير شيء منذ آخر
تشغيل بلا نتيجة — مكلف وعديم الفائدة، خصوصاً عند استدعاء المهارة مراراً (حلقة، مهمة مجدولة، استدعاء يدوي
متكرر في وقت قصير).

**تُحفظ الحالة في USMC** (حالة العملية تنتمي إلى هذا النظام، لا إلى ملفات Markdown):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**تتكون البصمة من جزأين — الوضع والوصول معاً:**

1. **جزء الوضع** (كما سبق): عدد/معرّفات تذاكر `ACTIONABLE` المفتوحة، وتاريخ التعديل (mtime) لسلسلة
   `_DECISIONS` (`TO-DECIDE-USER*.txt`، `DECIDED-AND-DONE.md`)، وعدد إدخالات USMC-`working` الجديدة منذ آخر تشغيل للسلسلة.
2. **جزء التوفر (جديد، إلزامي منذ 1.2.0):** المجموعة المرتبة للأدوار التي أبلغ عنها للتو فحص الإدراك الذاتي
   (`exhaustion_check.availability_fingerprint_component()`) بوصفها `unavailable`، مثلاً `("memory.organic",)` أو `()`.

**لماذا الجزء الثاني إلزامي — „وإلا يرث الحارس الثغرة":** بدونه تعتمد البصمة (الجزء 1) بين أمور أخرى على
تاريخ التعديل لسلسلة `_DECISIONS`. إذا غابت هذه السلسلة كلياً عن نظام ما، يبقى هذا الجزء من البصمة ثابتاً إلى الأبد —
فلن يُعاد فحص `exhausted`/`blind` الذي ضُبط خطأً مرة، حتى لو تم لاحقاً تثبيت `source-resolver` أو إنشاء `_control-center/_CONTROL/_DECISIONS/`. يعالج جزء
التوفر هذه المشكلة تحديداً: إذا تغيّرت الأدوار غير المتاحة (يُضاف مصدر أو يُفقد)، تتغير البصمة تلقائياً —
يكتشف الحارس ذلك عند الاستدعاء التالي ويعيد تشغيل السلسلة. وهذا هو „الزرع" بالمعنى الوارد في استعارة التأسيس (T-20260815-371628859): تغيير البيئة يُطلق بحثاً جديداً،
دون أن يحتاج أحد إلى إعادة ضبط الحارس يدوياً.

**التسلسل قبل كل تشغيل للسلسلة:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```

يكفي تشغيل واحد كامل للسلسلة، تكون فيه جميع المصادر الأربعة قابلة للاستعلام ولم يُسفر أيّ منها عن نتيجة،
دليلاً على „لم تعد هناك مهام مستقلة" (نص التذكرة: „فقط عندما تبقى جميع خطوات تشغيل واحد دون نتيجة" — و„دون نتيجة" تعني هنا
صراحةً `empty`، لا `unavailable`). لا يمنع الحارس الإثبات نفسه، بل يمنع فقط
**إعادة الإثبات المتكررة دون تغيير** عند الاستدعاءات المتلاحقة الكثيفة — وذلك
لـ `exhausted` و لـ `blind` كلٍّ على حدة، ولا يُخلط بينهما أبداً.

`GUARD_INTERVAL` قابل للضبط (الافتراضي 15 دقيقة) — في البيئات الخاملة (تذاكر/قرارات جديدة نادرة) يجوز اختيار مدة أطول، وفي البيئات النشطة جداً أقصر.

## إشارة الإيقاف

ينتهي كل تشغيل بسطر **واحد** واضح قابل للبحث بـ grep، حتى يتمكن `/loop` المحيط أو بنية `/goal` مستقبلية من قراءته لتحديد ما إذا كان ينبغي المتابعة:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` هي الإشارة الوحيدة التي ينبغي فيها للحلقة الأعلى أن تطلق دورة إضافية. جميع متغيرات `STOP` هي الإيقاف الموثّق — مع بيان السبب وأي حالة تنطبق.

الفرق بين `exhausted` و`blind` جوهري بالنسبة إلى المستخدم، وليس تجميلياً:
`exhausted` يعني „لقد فحصتُ كل ما كان يجب فحصه — العمل منجز". أما `blind` فيعني „تنقصني البنية التحتية اللازمة لإجراء الفحص أصلاً — هذا ليس حالة عمل، بل ثغرة".
لا ينبغي لبنية `/loop`/`/goal` التي تعالج الحالتين بالطريقة نفسها (تنتهي الحلقة في كلتا الحالتين) أن تُبلغ المستخدم بهما بالطريقة ذاتها، وإلا فستضيع بالضبط المعلومة التي طالب بها التذكرة T-20260815-205101335.

## العلاقة بالمهارات الأخرى

- **`think`/`decide`** — توفران التحليل والقرار المنظمين في خطوة السلسلة 1. يُستدعيان هنا كلبنة بناء، ولا يُعاد اختراعهما.
- **`decision-avatar`** (هذه المهارة، محايدة تجاه المستخدم) — توفر خطوة السلسلة 4. وفي الأنظمة ذات ملف تعريف محدد ومفوَّض، يقابل ذلك `user-model` + `build-your-users-mind`.
- **`orchestrator`** — يحدد كيفية تفويض المهام إلى الوكلاء الفرعيين وكيفية التحقق من إشعار إنجازهم. أما `work-autonomous` فيحدد متى يتوقف البحث أصلاً؛ ويمكن الجمع بينهما (فقد يظهر المنسّق كجزء من العمل المنجز في المستوى 1).
- **`bugsweep`** — مثال على بروتوكول بحث آخر يحد من نفسه (تصعيد بالمضاعفة بدلاً من سلسلة الأربع خطوات). أما `work-autonomous` فهو أعم: إذ يفحص ليس الكود بحثاً عن الأخطاء فحسب، بل كل مصدر للعمل المستقل.
- **فئات التذاكر (`ticket-master`)** — توفر المفردات الخاصة بـ„القابل للتنفيذ الذاتي" (انظر جدول التمييز) والقالب لحلقة الاستقلالية (إعادة فحص BLOCKED، تجميع USER، سحب موعد WAITING، توقف PARKED).
- **`tidy-up`** (منذ الإصدار 1.3.0) — يوفر مصدراً إضافياً في المستوى 1: تشغيلاً واحداً لـ Tasksolver+Writer+Maintainer لمجلد المشروع الذي يُعمل عليه حالياً. يتحقق بنفسه من استحقاقه (سجل USMC مختصر، دون حارس السلسلة ذات الأربع خطوات كما هنا)، ولا يستدعيه `work-autonomous` إلا بوصفه أحد عدة مصادر في المستوى 1، دون تكرار منطقه.

## مثال تسلسل

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```


## سجل التغييرات

### 1.5.1 (2026-09-09)
- T-20260909-282509082: يتبع الاحتياطي الموثّق لـ `decisions.ledger` و`user.model` عملية نقل مركز التحكم الموثّقة إلى `_CONTROL/_DECISIONS` و`_CONTROL/_USER-MIND`. تبقى أولوية المحلل وسلوك الإغلاق الآمن (fail-closed) دون تغيير.

### 1.5.0 (2026-09-09)
- P-018: تنتهي التقارير المهمة للعمل المنشأة حديثاً والمحفوظة بشكل دائم، وملفات التسليم والإيصالات، بـ `session: <session-id> | <agent>@<host> | YYYY-MM-DD`. وأولوية المصادر هي: التصريح الصريح عند التشغيل/سطر الأوامر، ثم بيئة المزود/الخطاف الموثوقة، ثم `unbekannt`؛ ولا تُخمَّن القيم أبداً، ويستخدم الوكلاء الفرعيون جلسة الأصل. وتُستثنى المحادثات الروتينية والمصادر والسياسات و`CLAUDE.md` وملفات README والملفات القديمة من الختم الشامل أو بأثر رجعي.

### 1.4.0 (2026-09-03)
- إضافة محدودة التأثير من التذكرة T-20260902-729068782: بوابة استقبال جديدة **TICKET-MASTER-Intake-Gate** في المستوى 1 (تسبق `ACTIONABLE`/`BLOCKED`/`WAITING`) — وتكون ذات صلة فقط عندما يكون نظام التذاكر جزءاً من السياق. ما دام `INBOX/` (بما في ذلك الإدخالات غير الرسمية) غير مفروز بالكامل، لا يجوز أن ينشأ `NO_WORK` أو إشارة الاستنفاد أو إيقاف الحارس. حالة الدليل: بدأت حلقة فحص الاستنفاد بينما كان `INBOX` ما زال يضم إدخالات مفتوحة (من بينها تذكرتان من الأولوية P1). تبقى سلسلة الاستنفاد ذات الخطوات الأربع القائمة، والحارس، وقابلية الاستخدام خارج TICKET-MASTER دون تغيير — وتعمل البوابة حصراً في المستوى 1 وتحت TICKET-MASTER فقط.
- دالة مساعدة جديدة ومختبرة `scripts/exhaustion_check.py::intake_gate_blocks_stop()` + اختبارات انحدار في `tests/test_exhaustion_check.py` (سلوكية: تحجب البوابة عند وجود INBOX مفتوح، وتسمح عند فراغ INBOX).

### 1.3.0 (2026-08-19)
- إضافة محدودة التأثير من التذكرة T-20260819-461890468 (مهارة جديدة `tidy-up`): يحصل المستوى 1 على مصدر إضافي مستقل هو „تشغيلات `tidy-up` المستحقة للمشروع النشط" (تشغيل Tasksolver+Writer+Maintainer، انظر مهارة `tidy-up`). لا توجد خطوة سلسلة جديدة، ولا تغيير في المستوى 2 أو الحارس أو إشارة الإيقاف — ويتحقق `tidy-up` من استحقاقه بنفسه عبر سجل USMC مختصر، ويُشار إليه هنا فقط كمصدر إضافي من المستوى 1، على غرار المصادر القائمة بالفعل (التذاكر، TODO/AUFGABEN، الفحوصات الروتينية، USMC `working`). وبذلك تُحتسب نقاط `tidy-up` كمهمة قابلة للتنفيذ الذاتي بالمعنى الذي تقتضيه بنية `/goal`، التي تجمع `/work-autonomous` + `/tidy-up` (حالة الاستخدام الأساسية للتذكرة). لا تدخّل في سلسلة الاستنفاد ذات الخطوات الأربع أو في الحارس — ويبقى المستوى 2 دون تغيير.

### 1.2.0 (2026-08-15)
- إعادة هيكلة من التذكرة T-20260815-205101335 (طلب المراجعة: „تحقّق مما إذا كان الحل يصمد هناك بالاقتران مع استعارة التأريض"، والنتيجة في المهارة المُسلَّمة: صمد في ثلاث نقاط، لكنه لم يصمد في التمييز بين „تم الاستعلام وكان فارغاً" و„لم يكن الاستعلام ممكناً أصلاً" — أبلغت السلسلة عن `STOP (exhausted)` أيضاً على أنظمة لا تحتوي على Gardener/USMC/`_DECISIONS`، دون أن تتحقق من ذلك قط). أول حالة استخدام فعلية لـ `grounding-seed`، التذكرة T-20260815-371628859.
- **إضافة معرفة الذات:** أربع احتياجات معلنة (`decisions.ledger`، `memory.organic`، `memory.curated`، `user.model`) قبل السلسلة، بدلاً من البحث الأعمى في أربعة مواضع محددة مسبقاً.
- **يُبلغ كل خطوة من السلسلة (2–4) عن found | empty | unavailable** بدلاً من نتيجة ثنائية — على مرحلتين: التحديد أولاً (`grounding-seed`/`source-resolver` لـ `decisions.ledger`/`user.model`، وفحص CLI مباشر لـ `memory.organic`/`memory.curated` التي لا يوجد لها بعد مزوّد `source-resolver`)، ثم فحص المحتوى فقط عند نجاح التحديد.
- **لا يبقى `exhausted` صالحاً إلا إذا كانت المصادر الأربعة كلها قابلة للاستعلام فعلاً** (جميعها found/empty، دون أي unavailable). إشارة جديدة ومميزة `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` لحالة لم تكن فيها مصدر واحد على الأقل قابلاً للوصول — تنتهي الحلقة مع ذلك، لكنها لم تعد تدّعي نتيجة مُتحقَّقاً منها.
- **توسيع بصمة الحارس بعنصر توفّر** (مجموعة مرتّبة من الأدوار غير المتاحة حالياً). يعالج ملاحظة المتابعة „الحارس يرث الفجوة": من دون هذا العنصر يبقى `exhausted`/`blind` المُعيَّن خطأً صالحاً إلى الأبد إذا كانت سلسلة `_DECISIONS` مفقودة بالكامل (يصبح جزء البصمة السابق ثابتاً حينها). مع هذا العنصر، يُطلق أي مصدر أصبح متاحاً من جديد تشغيلاً تلقائياً لتكرار السلسلة (زرع بالمعنى المقصود في استعارة التأريض).
- سكربت مساعد جديد ومُختبَر `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`، 11 اختباراً، وتم فحص وضعي التشغيل: مع تثبيت `grounding-seed` وبدونه) — يوفّر فحص معرفة الذات/التحديد بشكل حتمي، حتى لا تضطر المهارة إلى تخمينه في كل تشغيل. يبقى اختيارياً: المهارة لا تزال في المقام الأول بروتوكولاً يتبعه نموذج باستخدام أدواته الخاصة.
- الاعتماد: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` منذ `grounding-seed` 0.2.0 — إصدارات `grounding-seed` الأقدم (0.1.0) كانت تحتوي على خطأ في الفئات (`not_found` صُنِّفت خطأً على أنها `empty`)، وهذا كان سيطمس مجدداً التمييز الذي عُولج هنا. من دون تثبيت `grounding-seed`، يعمل الاحتياطي الموثّق بالطريقة نفسها.

### 1.1.0 (2026-08-15)
- إعادة هيكلة مرجعية من التذكرة T-20260815-385400870: تحدّد الخطوة 2 (سجل القرارات) موقعها الآن عبر الدور `decisions.ledger` (`source_resolver.resolve(...)`، الوحدة `source-resolver`)، بدلاً من توصيله صلباً — مع احتياطي موثّق يعود إلى المسار السابق إذا لم يكن المحلّل مثبتاً. السلوك الوظيفي دون تغيير.

### 1.0.0 (2026-08-15)
- الإصدار الأول من التذكرة T-20260815-522639345: نموذج تشغيل من مستويين، وسلسلة تحقق من أربع خطوات، وجدول تمييز حسب فئات `ticket-master`، وحارس مدعوم بـ USMC ضد الحلقات اللانهائية، وإشارة إنهاء واضحة لبنى `/loop`/`/goal`.
