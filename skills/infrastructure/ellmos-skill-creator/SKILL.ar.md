---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "أنشئ مهارة أو أعد تحريرها **لهذا النظام البيئي**: يُفوَّض حلقة المقابلة/الصياغة/التقييم العامة إلى الإضافة الرسمية skill-creator (من Anthropic، ترخيص Apache-2.0)، لكنها تفرض بالإضافة إلى ذلك متطلبات ellmos التي لا تعرفها الإضافة الرسمية — الترويسة الداخلية (9 حقول)، وقواعد الفئة/الرؤية، والكشف المحايد تجاه المزوِّد والمستخدم وellmos مع الحساسية تجاه ellmos عبر grounding-seed، وملف config.json المرفق (بما في ذلك عقد التعلّم) وconnections.json، والوعي بالمزوِّدين/البائعين (اقتراح بدائل أحدث التقنيات بما فيها مكونات ellmos الخاصة)، وقسم للتحديث الذاتي، ومجموعة ملفات قابلة لإعادة الاستخدام للتعلّم والتغطية (user-usecases.json وusecase-gaps.json وknown-providers-and-abilities.json وgap-closing-analysis.json — مستوحاة من evals.json الخاص بـ skill-creator ومن A2A/AgentSkill، دون معيار موازٍ). استخدم هذه المهارة دائمًا عند إنشاء مهارة **جديدة** لهذا النظام أو عند ترقية مهارة موجودة لتتوافق مع معايير ellmos — حتى مع طلبات مثل «أنشئ مهارة»، و«ابنِ لي مهارة لـ X»، و«استخدم skill-creator»، و«أنشئ مهارة جديدة»، و«اجعل هذه المهارة متوافقة مع ellmos»، و«أنشئ عقد تعلّم/مدونة سلوك لمهارة»، و«تحقّق من تغطية حالات الاستخدام لمهارة». أما للبحث عن المهارات الموجودة أو توجيهها فاستخدم skill-finder بدلًا من ذلك، ولمراجعة المشهد العام استخدم skill-explorer."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: ar
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 1e6dace03eb8afc639fa08debace08a61441912a22399c11a49f7fe6e7dc3ecb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:53.391636+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## المصدر والقرار (تفرّع أم بناء خاص)

**القرار: بناء خاص، لا تفرّع.** التبرير مكتوب هنا حتى لا يضيع:

- `skill-creator` (من Anthropic، والسوق `claude-plugins-official`) مرخّصة بموجب **Apache-2.0**
  (نص الترخيص في النسخة المحلية مقروء ومتحقَّق منه، 2026-08-24) — التفرّع كان ممكنًا قانونيًا
  وهو النمط المعتمد في المستودع في أماكن أخرى (`skills/third-party/grilling`).
- لكن التفرّع كان سيجرّ معه كامل آلية التقييم والقياس الأصلية (`agents/{analyzer,comparator,grader}.md`،
  `eval-viewer/`، 7 سكربتات، وملف SKILL.md من 485 سطرًا) — وهي قدرة موجودة بالفعل ويمكن
  استدعاؤها مباشرة (`Skill: skill-creator:skill-creator`). وفق `.PLUGINS/CLAUDE.md` القاعدة 4 ("تحقّق من القدرات
  قبل إعادة بنائها") ونمط P10 ("مفتاحان لا يقارن بينهما أحد")، كان ذلك سيكون نسخة مكررة لا توسعة.
- الفجوة الحقيقية **خاصة بـ ellmos** وغير معروفة أصلًا للمشروع الأصلي: الترويسة الداخلية (`templates/SKILL.md`)،
  `docs/CONVENTIONS.md`، الحياد تجاه المزوِّد والمستخدم وellmos مع الحساسية تجاه ellmos، الربط بـ
  `grounding-seed`، الوعي بالبائعين، والتحديث الذاتي.
- لا تحتوي هذه المهارة على **أي نص من Anthropic** (الصياغة خاصة بها في كل موضع) — وبالتالي لا
  تُفعّل واجب نسب Apache-2.0 للتعديلات. وهي **تركّب** الأصل بدل نسخه: وهذا في الوقت نفسه أنظف مسار
  من الناحية القانونية وأقلّه عبئًا في الصيانة.

## متى تُفعَّل

- "أنشئ مهارة لـ X"، "ابنِ مهارة جديدة"، "استخدم skill-creator"
- "اجعل هذه المهارة متوافقة مع ellmos"، "رقِّ مهارة إلى المعيار الداخلي"
- كلما كان **الهدف** مهارة في `.AI/.SKILLS/skills/…` (أو نسختها المستنسخة وفق خطة D القانونية) — لا
  في الطلبات العامة غير المرتبطة بهذا النظام ("أنشئ لي أي مهارة Claude دون علاقة بهذا").

## الإجراء

### الخطوة 1 — تفويض المقابلة/الصياغة/التقييم

استدعِ `Skill: skill-creator:skill-creator` الرسمي من أجل: توضيح الغرض، وصياغة بنية SKILL.md،
وحالات الاختبار، وحلقة التقييم، وتحسين الوصف (`scripts/improve_description.py`). **لا تعِد
اختراع هذا الجزء** — فهو عام، ومحلول بشكل جيد في الأصل.

### الخطوة 2 — تركيب الهيكل الداخلي الخاص بـ ellmos (إلزامي، إضافي لتنسيق الأصل)

أضف إلى SKILL.md الناتج من الأصل الحقول التسعة الداخلية من
`.SKILLS/templates/SKILL.md` (أو `AGENT.md`/`WORKFLOW.md`/`PROMPT.md` حسب النوع)،
واقرأ مسبقًا `.SKILLS/docs/CONVENTIONS.md` لمعرفة مجلدات الفئات، وقاعدة التسطيح (أقل من 5 ملفات تكون
مسطحة)، واتفاقية الإصدارات (SemVer: MAJOR/MINOR/PATCH)، ومجموعات تعدد اللغات (الأساس: الألمانية
والإنجليزية إلزاميتان). **يبدأ `visibility` دائمًا على `private-only`** — النشر قرار لاحق
يتخذه المستخدم بعد التحقق (`.AI/VISIBILITY-POLICY.md`)، وليس افتراضيًا أبدًا. هذه الحقول **إضافية فقط** لتنسيق
Anthropic (مفاتيح YAML إضافية إلى جانب `name`/`description`) — فكل مهارة تُنتج بهذه
الطريقة تبقى `anthropic_compatible: true` بالكامل.

### الخطوة 3 — فرض المبادئ: الحياد تجاه المزوِّد والمستخدم، والحياد تجاه ellmos مع الحساسية تجاهها

النص الكامل والأنماط البرمجية: `references/ELLMOS-PRINCIPLES.md`. الخلاصة: يجب أن تكون المهارة الناتجة
**قادرة على العمل وحدها** (تحمل كل ما تحتاجه)، و**في الوقت نفسه** تستفيد من مكونات ellmos متى
توفرت — وهي تقرر ذلك بنفسها وقت التشغيل، ولا تُربط بشكل ثابت أبدًا. هذا هو النمط نفسه الذي
توفره `grounding-seed` أصلًا (README: "cultivated landscape, not wildflower" / "viable alone, more
productive together") — **لا يُخترع آلية كشف ثانية**، وهذه المهارة توجّه المهارات المنتَجة باستمرار
إلى `grounding_seed.detect_ecosystem()`.

### الخطوة 4 — تضمين config.json وconnections.json

`grounding-seed` قابل للاستيراد أصلًا كحزمة Python (متحقَّق منه بتاريخ 2026-08-24: يُحلّ
`import grounding_seed` بنجاح على شجرة المصدر المستنسخة محليًا `grounding-seed` وفق خطة D) — وهو
**نقطة الربط القانونية**، فلا داعي لاختراع ملف جديد. لكل مهارة منتَجة لها احتياج خارجي (برامج،
خدمات، مزوِّدون):

- **`config.json`** — إعدادات خاصة بالمهارة (القالب: `templates/skill-config.template.json`).
  يستخدم `grounding_seed.store.LocalStore(root)` هذا الاسم افتراضيًا لتخزين أدواره — لذا يمكن لمهارة منتَجة إما أن تستخدم
  `config.json` نفسه كخلفية لـ `LocalStore`، أو أن تُبقيه منفصلًا إذا احتاجت إلى
  إعدادات سلوكية إضافية إلى جانب الأدوار (ويكون حينها نسخة ثانية من `LocalStore(root, filename="connections.json")`).
- **`connections.json`** — نقاط الربط الخارجية **التي جرى حلّها فعلًا** (أي برنامج/خدمة عُثر عليه،
  ومنذ متى، وبأي مصدر) — القالب: `templates/skill-connections.template.json`، والمخطط `ellmos.source-resolver.user-config.v1`
  (مطابق لـ `source-resolver`، وقد اختير عمدًا وفق README الخاص بـ grounding-seed، حتى يكون النقل اللاحق
  إلى `source-resolver` الحقيقي بلا فقدان — انظر `migration.py` هناك).

التفاصيل وواجهة سطر الأوامر ومثال الكود: `references/ELLMOS-PRINCIPLES.md`، قسم "Docking".

### الخطوة 5 — تضمين الوعي بالمزوِّدين والبائعين

النص الكامل: `references/VENDOR-AWARENESS.md`. الخلاصة: تحصل المهارة المنتَجة على قسم
"المزوِّدون والبدائل" يقوم بما يلي: (أ) يسمّي المزوِّد أو المزوِّدين الرائدين في الموضوع
(مثلًا ElevenLabs لتحويل النص إلى كلام)، (ب) يذكر مزوِّدًا بديلًا واحدًا على الأقل، (ج) يدرج
**مكونات ellmos الخاصة صراحةً كمرشحين بالمرتبة نفسها** إذا كانت تغطي الموضوع (مثلًا
`ellmos-voice-io` بدلًا من ElevenLabs أو إلى جانبه) — و**يقترح** التثبيت أو الانتقال عند وجود
طلب مناسب من المستخدم، بدلًا من افتراضه ضمنيًا. الأساس لمعرفة "ما المتوفر على النظام":
`grounding_seed.scan.scan_resources([...])` (الذي يفحص `shutil.which`) إضافة إلى `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` لمرشحي ellmos.

### الخطوة 6 — إضافة التحديث الذاتي

النص الكامل: `references/SELF-UPDATE.md`. الخلاصة: تحصل كل مهارة منتَجة على قسم
"التحديث الذاتي" يقوم بما يلي: (أ) يقترح دوريًا بحثًا قصيرًا على الويب للبقاء على أحدث التقنيات،
(ب) يعرف المهارات وسير العمل ذات الصلة ويذكر البدائل الجديدة التي قد تناسب بشكل أفضل، (ج) يحتفظ
بملف JSON صغير للتعلّم (القالب: `templates/skill-connections.template.json`، الحقل `notizen`/`gelernt`)، والذي
يمكن نقله إلى مكون الذاكرة في ellmos (USMC/Gardener) عند توفره بدلًا من أن ينمو محليًا — وهنا أيضًا:
الكشف بدلًا من الربط الثابت (`grounding_seed.detect_ecosystem()`).

### الخطوة 6ب — إنشاء عقد التعلّم وتغطية حالات الاستخدام (نمط قابل لإعادة الاستخدام)

النص الكامل: `references/LEARNING-CONTRACT-AND-COVERAGE.md`. الخلاصة: لا تقتصر الحاجة على هذه المهارة نفسها، بل
**كل مهارة تنتجها** تحصل على مجموعة صغيرة وقابلة لإعادة الاستخدام من ملفات التعلّم والتغطية، وقد
رُوجعت وفق معايير معروفة دون إنشاء معيار موازٍ:

- `evals/evals.json` — **يُعاد استخدامه** ولا يُكرَّر: فهو بالفعل معيار skill-creator لحالات الاختبار
  التي يصوغها المؤلف.
- `user-usecases.json` — حالات استخدام فعلية يطرحها المستخدم، بنفس شكل
  `evals.json` (القالب: `templates/user-usecases.template.json`).
- `usecase-gaps.json` — مطابقة: أي حالات استخدام المستخدم غير مختبرة أو غير مغطاة
  (القالب: `templates/usecase-gaps.template.json`).
- `known-providers-and-abilities.json` — فضاء المرشحين من المزوِّدين المعروفين لكل دور، وحقوله مستوحاة من
  A2A/`AgentSkill` (id/name/description/tags) لا مخترعة (القالب: `templates/known-providers-and-abilities.template.json`).
- `gap-closing-analysis.json` — مسارات الإغلاق البنيوية لكل فجوة (وحدة ellmos، أو حزمة ellmos، أو وحدة
  خارجية، أو بناء جديد) — ليس نسخة من `grading.json.eval_feedback` (القالب: `templates/gap-closing-analysis.template.json`).
- الحقل `lernvertrag` في `config.json` — مدونة السلوك (اختيار أفضل خيار، و**المستخدم
  هو الملك**، وعدم التثبيت الذاتي أبدًا، وفترة التحديث) — وهو مقصود كتوسعة لـ `config.json`،
  لا كملف سابع.

المخططات: `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — وهي الاتفاقية الداخلية نفسها لـ `skill-v1.schema.json`.
وقد جرى التحقق من `grounding-seed` لهذه المجموعة من الملفات و**لم يُوسَّع عمدًا** (التبرير في
`LEARNING-CONTRACT-AND-COVERAGE.md`) — ويبقى `connections.json` جزءًا منه فقط.

### الخطوة 7 — التسجيل والاختبار والإيداع

- اختر مجلد الفئة وفق `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md`؛ وعند الشك اسأل `skill-finder`
  أو `controlcenter_find_skill` عمّا إذا كانت عائلة موجودة بالفعل.
- شغّل `testing/` (privacy_gate واختبارات البيانات الوصفية) قبل الإيداع.
- **لا تحرّر ملفات السجل** (`registry/components.json`، `SKILLS-MAP.md`، `llms.txt`) يدويًا؛ فهي
  تُولَّد آليًا (`build_public_registry.py`، `build_skills_map.py`، `catalog.py`). وإذا كانت جلسة أخرى غير
  مُودَعة تعمل حاليًا في النسخة القانونية، فلا تُعِد التوليد على مستوى المستودع كله (فذلك يخلط تغييرات
  الآخرين بتغييراتك في الملف نفسه) — بل أودِع مجلد المهارة الجديد وحده بشكل معزول، واترك إعادة توليد
  السجل للتشغيل النظيف التالي (`skill-register-care`).
- `git commit -- skills/<kategorie>/<name>/` — المسارات الجديدة الخاصة بك فقط.

## التوافق مع تنسيق Anthropic

جميع الحقول الإضافية توسعات YAML خالصة إلى جانب `name`/`description` — فـ Claude Code
العادي بدون هذا النظام البيئي يقرأ `name`/`description` فقط ويتجاهل الباقي. و
`config.json`/`connections.json` موارد مرفقة اختيارية (كما هو منصوص عليه في `docs/CONVENTIONS.md`)،
وليست تبعية إلزامية — فالمهارة بدونها تعمل دون تغيير.

## المهارات ذات الصلة

- `skill-creator:skill-creator` — حلقة المقابلة/التقييم العامة (يُفوَّض إليها، الخطوة 1).
- `skill-finder` — موجّه للمهارات الخاصة الموجودة (تحقق منه قبل البناء: هل هذه المهارة موجودة أصلًا؟).
- `skill-explorer` — مراجعة المشهد والبحث على الويب عن مهارات/إضافات جديدة (على مستوى أعلى: *مجموعة*
  مهاراتنا؛ أما هذه المهارة فتجعل كل مهارة *منتَجة بعينها* مدركة للمزوِّدين).
- `skill-family-care`، `skill-register-care` — الصيانة بعد البناء.
- `grounding-seed` (الوحدة، `.AI/.MODULES/.CONTROL/grounding-seed`) — منطق الربط الفعلي والاكتفاء الذاتي، ويُشار إليه هنا دون تكراره.

## سجل التغييرات

### 0.2.0 (2026-08-24)
- ملحق (التذكرة T-20260824-218233618، توسعة النطاق): أُضيف نمط التعلّم والتغطية القابل لإعادة الاستخدام
  لكل مهارة منتَجة — `user-usecases.json`،
  `usecase-gaps.json`، `known-providers-and-abilities.json`،
  `gap-closing-analysis.json` (مخططات منزلية جديدة في `.SKILLS/schemas/`) إضافة إلى حقل عقد التعلّم في
  `config.json`. أُعيد استخدام `evals/evals.json` (skill-creator) عمدًا بدلًا من تكراره.
  جرى التحقق من `grounding-seed` — لا حاجة إلى توسعة (التبرير في `references/LEARNING-CONTRACT-AND-COVERAGE.md`)، لذا لا
  توجد تذكرة متابعة. أُخذت أسماء الحقول لكتالوجات المزوِّدين من بروتوكول A2A (`AgentSkill`)
  بدلًا من ابتكار مفردات خاصة.

### 0.1.0 (2026-08-24)
- الإصدار الأول. اتُّخذ قرار البناء الخاص بدل التفرّع وجرى تبريره (التذكرة
  T-20260824-218233618). يفوّض إنشاء المهارات العام إلى `skill-creator:skill-creator`، ويضيف الهيكل الداخلي،
  ومبادئ ellmos، وربط `grounding-seed` (config.json/connections.json)، والوعي بالبائعين، والتحديث الذاتي.
