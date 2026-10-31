---
name: agents-bridge
version: 3.0.1
type: skill
author: Lukas Geiger + Codex
created: 2026-07-04
updated: 2026-08-22
description: "agents-bridge — the Lifeboat، ويُعرف أيضًا باسم Time Capsule. جسر ملفات محايد تجاه المزوّدين وقابل للنقل لأسطح الإقلاع، ومؤشرات الحقيقة، وصوامع الذاكرة المنفصلة، والمراسلة، والحضور، والأقفال التعاونية، والاستعادة العكسية للمضيف."
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [multi-agent, bootstrap, recovery, messaging, memory, provider-neutral]
language: ar
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
translated_from_sha256: 332b9782849063f2901c750f364f3d66446b1f1f236d8fd8a6f5b67e9757e2f5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="agents-bridge banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# AGENTS-BRIDGE — the Lifeboat، ويُعرف أيضًا باسم Time Capsule (Deutsch)

> **اللقبان „Lifeboat“ (بالألمانية: قارب النجاة) و„Time Capsule“:** agents-bridge
> هو مجموعة استعادة ملفات قواعد الوكلاء (CLAUDE.md/
> GEMINI.md/GPT.md/AGENTS.md) — وقد كانت هذه الوظيفة حتى الآن بلا اسم واضح. يتناسب „Lifeboat“ مع
> العائلة البحرية للاستعارة الجسرية (Wheelhouse، Deep-Diver، Lower Decks)؛ ويؤكد „Time Capsule“
> الجانب الثاني للوظيفة نفسها — حالة مختومة ومتحققة بالتجزئة (hash) يمكن استعادتها لاحقًا سليمة.
> لا توجد إعادة تسمية: يبقى الاسم التقني `agents-bridge`، واللقبان مرادفان معبّران.

استخدم هذه المهارة لالتقاط نظام ملفات صغير متعدد المزوّدين وفحصه ونقله أو استعادته.
لكل نسخة ملف مزوّد رئيسي واحد مختار صراحةً. لا يُعتبر أي مزوّد أو اسم ملف أو مضيف أو مجلد سحابي مرجعيًا ضمنيًا.

## سير العمل والإجراء

1. اقرأ جميع التعليمات المحلية والأقفال وقواعد الخصوصية للمصدر والهدف. حافظ على تغييرات الآخرين.
2. نفّذ `python scripts/bridge.py discover --root <instanz>`. يجوز لـ `discover`
   أن يعتمد فقط على علامة `agents-bridge-primary: true` واحدة وفريدة.
   عند عدم وجود أي مطالبة أو وجود أكثر من واحدة يتوقف سير العمل ببيان قرار؛ ولا توجد قيمة افتراضية لاسم الملف.
3. أنشئ ملف تعريف وفقًا لـ `references/profile-v3.schema.json`. يسمّي هذا الملف السطح الرئيسي،
   وأسطح المزوّدين، ومصادر الحقيقة، ورسم المؤشرات، والاستعادة، وصوامع الذاكرة، والمراسلة، والحضور، والأقفال، وقوائم التضمين/الاستثناء الخاصة بالخصوصية.
4. تحقّق من ملف التعريف وسجّل النسخة دون تعديل المصدر:

   ```text
   python scripts/bridge.py profile-validate --profile <profil.json>
   python scripts/bridge.py capture --profile <profil.json> --root <quelle> --output <neues-paket>
   ```

5. تحقّق من الحزمة باستخدام `doctor`، وأنشئ معاينة باستخدام `plan` أو `restore` دون
   `--apply`. لا يتم أبدًا الكتابة فوق الملفات الموجودة بشكل أعمى (دون فحص).
6. طبّق الاستعادة فقط بعد التحقق بواسطة `--apply --yes --backup-dir
   <backup> --receipt <receipt.json>`. ثم تُنفَّذ `verify` واختبار قراءة أصلي حقيقي لـ Claude أو Codex/GPT أو Gemini أو المزوّد المحايد.
7. عند وقوع أخطاء: احسم الانحراف أو تراجع عن الاستعادة باستخدام الإيصال الدقيق عبر `rollback --yes`.
   يجب أن تُبلغ الاستعادة الثانية عن `idempotent`.
8. استخدم `message send|ack|status` و`memory` و`presence` و`lock claim|release|status` فقط بوصفها عقود ملفات صغيرة.
   لا يحل المراسل محل Ticket-Master أو المجدول؛ ولا تُدمج صوامع الذاكرة تلقائيًا أبدًا.

## حدود الأمان

- يُفضَّل المحمّل أو إعادة التوجيه. لا يُسمح بالإسقاط إلا عندما تفشل المراجع الأصلية؛ ويتضمن ذلك تجزئات المصدر ومعلومات المنشأ و`generated_at` ومعرّف الانحراف. لا تتم إعادة التوليد المضبوطة إلا في حزمة جديدة تحمل `capture --regenerate-projections`.
- جميع مسارات ملفات التعريف مرمّزة بـ UTF-8 ونسبية ومحايدة للمنصة. الصادرات موثّقة في بيان (manifest) ومحصورة في التضمينات/الاستثناءات.
- تُرفض الأسرار وبيانات الاعتماد والمسارات المطلقة الشخصية بشكل مغلق (fail closed)، أو تُستبدل مع تسجيلها في وضع `redact` الصريح.
- عند وجود Controlroom يبقى هو سلطة التنسيق. ويكون `agents-bridge` حينها مجرد محوّل إقلاع واستعادة وملفات فقط، ولا يكرر أي بيئة تشغيل مركزية.

توجد العقود والأمثلة في `references/contracts.de.md`،
و`references/truth-topologies.md`، و`references/inventory-contract.md`، و`references/migration-2-to-3.de.md`. والنسخة الإنجليزية هي `SKILL.en.md`.
