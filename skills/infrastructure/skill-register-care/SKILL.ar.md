---
name: skill-register-care
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-09-20
description: "مهارة صيانة تُبقي سجل المهارات الثلاثي متسقًا (فهارس كتالوج code-skill-index، وفهرس المهارات، وخريطة SKILL-MAP للعائلات/التوجيه). استخدم هذه المهارة لفحص الانحراف بين جرد المهارات الفعلي والسجل الموثّق: الإبلاغ عن الإدخالات المفقودة أو الزائدة، وتصحيح الأعداد، وتعيين تاريخ الحالة. وتُفعَّل أيضًا عند عبارات مثل „صيانة سجل المهارات\"، „تحديث الفهرس\"، „فحص انحراف السجل\"، „أي المهارات مفقودة في الخريطة\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: ar
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.2.0"
translated_from_sha256: 6a187b857227bb33edb71c82f4b992a376877192b746a6eea17458e9819cae46
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:34:28.865145+00:00"
---
<img src="banner.png" width="100%" alt="skill-register-care banner">
# صيانة سجل المهارات

## الغرض

يُبقي **السجل** خاليًا من الانحراف. يتكون السجل من ثلاثة عناصر مترابطة — لا تُنشئ عنصرًا رابعًا أبدًا، بل وسّع هذه العناصر الثلاثة دائمًا:

| العنصر | الدور | الصيانة |
|---|---|---|
| `~/.claude/skills/code-skill-index/references/catalog-*.md` | كتالوجات الفئات | مُنسّقة يدويًا |
| `<USER_HOME>/OneDrive/.SYNC/CLAUDE-CODE-SKILLS.md` | الفهرس عبر الأنظمة (المصدر الوحيد للمهارات في Claude Desktop) | **آلية**، انظر أدناه |
| `<USER_HOME>/OneDrive/.USR/SKILL-MAP.md` | خريطة العائلات/التوجيه | مُنسّقة يدويًا |

## آلي: الفهرس عبر الأنظمة

لم يعد الفهرس يُضاف يدويًا — فقد أدى ذلك إلى توقفه لمدة ثلاثة أشهر (آخر تحديث بتاريخ 21.06 مقابل 152 مهارة فعلية في 20.09.2026؛ وكانت 81 مفقودة). وبدلًا من ذلك:

```bash
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --check
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --apply
```

يعمل هذا الأمر أصلًا كـ **الخطوة 2b ضمن `/sync` اليومي**؛ ويُشغَّل هنا يدويًا فقط عند بناء المهارات أو نشرها للتو وعندما يجب أن يصبح الفهرس متطابقًا فورًا. والتشغيل إضافي وidempotent: تبقى الأوصاف المختصرة المُنسّقة كما هي، وتُصنَّف المهارات المفقودة حسب فئة المكتبة، أما الإدخالات التي لا تملك `SKILL.md` نشطًا فتُ**وسَم ولا تُحذف**.

## إجراء فحص الانحراف (السجلان المُنسّقان يدويًا)

1. **جمع الحالة الفعلية:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   فقط مهارات `source=user` تهم السجل (المكونات الإضافية/الخارجية تبقى خارج الحساب).
2. **قراءة الحالة المرجعية:** عناصر السجل الثلاثة.
3. **تكوين الفرق:**
   - **مفقود** (في الجرد، وليس في السجل) ← يُضاف.
   - **يتيم** (في السجل، وليس في الجرد) ← **تحقق أولًا، ثم احكم.**
     مجلد مهارة أُعيدت تسميته إلى `CONTENT.md` من `SKILL.md` يكون *مُلغى التسجيل*:
     وهو غير محمّل عمدًا كمهارة، لكنه موجود من حيث المحتوى ويمكن العثور عليه عبر `code-skill-index`.
     لا يحسبه الجرد، ومع ذلك لا يجوز حذفه — بل يُوسَم.
     لا تُزَل فعليًا إلا إذا اختفى المجلد.
   - **فرق في العدد** (مثلًا „18 مهارة" لم يعد صحيحًا) ← صحّح الرقم.
4. **الإضافة:** لكل مهارة جديدة سطر في `catalog-<kategorie>.md` المناسب، وسطر في
   فهرس المهارات (مع تاريخ الرأس)، وإذا كانت هناك عائلة جديدة أو مُعدَّلة ← قسم في `SKILL-MAP.md`.
5. **تعيين تاريخ الحالة** في جميع الملفات المتأثرة إلى التاريخ الحالي.

## مقتطف مساعد (سرد مهارات user المفقودة)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
قارن المخرجات بعناصر السجل (يدويًا أو عبر grep).

## قواعد حديدية

- **لا سجل رابع** — وسّع الثلاثة فقط.
- تنتمي إلى السجل المهارات المكتوبة من المستخدم فقط؛ أما مهارات الجهات الخارجية فتتبع المسار الخارجي.
- لا تُخمّن التاريخ — عيّن التاريخ الحالي.
- **لا تُصنْ** فهرس الأنظمة عبر المنصات **يدويًا**؛ شغّل `skill_index_care.py`. فمن يُضيف إدخالات يدويًا هناك يصنع الانحراف الصامت التالي.

## سجل التغييرات

### 0.2.0 (2026-09-20)
- تحويل فهرس الأنظمة عبر المنصات `CLAUDE-CODE-SKILLS.md` إلى `.SYNC/scripts/skill_index_care.py`
  (إضافي، ووسمي، وidempotent) وإلحاقه بوصفه الخطوة 2b في `/sync` اليومي. والسبب:
  كان الفهرس متوقفًا منذ 2026-06-21 — كانت 81 مهارة محلية مفقودة، وأشارت 15 إدخالًا دون وسم إلى إجراءات مُلغاة التسجيل، وأشار واحد إلى مجلد بلا `SKILL.md`.
- تدقيق تعريف „اليتيم": تُوسَم المهارات المُلغاة التسجيل (`CONTENT.md` بدلًا من `SKILL.md`) ولا تُزال — وإلا لحُذفت 15 مدخلًا مُنسّقًا عند إعادة الإدماج.

### 0.1.0 (2026-06-17)
- النسخة الأولية. أُنشئت بواسطة وضع التدقيق (P2). والسبب: أثناء تدقيق 2026-06-17 كانت حوالي 10 مهارات user مفقودة من SKILL-MAP (swarm-operations وmodel-strategy وagents-bridge وmcp-config-sync وsystem-onboarding وupdate-cli-docs وmigrate-rename وplugin-system، إضافةً إلى عائلتي العلاج وتطوير الألعاب).
