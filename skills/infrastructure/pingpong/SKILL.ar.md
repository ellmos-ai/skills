---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "يُشغّل محطة راديو مؤقتة مرتبطة بالجلسة عبر مجلد مُزامَن بشكل مشترك. يمسح ListenSync بشكل منهجي بحثًا عن المهام والمستجدات؛ ويرسل WriteSync الفروقات والإيصالات. يُستخدم عند PingPong أو Dosentelefon (هاتف العلب المعدنية) أو ListenSync أو WriteSync أو Sync-Listener (مستمع المزامنة) أو Auftragswache (حارس المهام) أو News-Scan (فحص المستجدات) أو مراقبة Goal/Loop."
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: ar
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

شغّل نظامين أو أكثر كمحطات راديو عبر مجلد مزامنة مشترك. اجعل العقد الوظيفي محايدًا تجاه المزوّد؛ ولا يختلف إلا محوّل متابعة الاستمرار.

## تحديد الوضع

- ListenSync: مستمع منهجي واحد بالضبط لكل مضيف. يمسح، ويتولى المهام المطابقة، وينفّذ WriteSync أيضًا عند وصول الردود.
- WriteSync: يحق لكل جهة عاملة إرسال فروقاتها ومهامها ومستجداتها وإيصالاتها ذات الصلة. لا يبدأ هذا الوضع أي مستمع.
- إذا غاب الوضع، فاستخدم ListenSync.

## توضيح المشاركة (STATE وCALL)

قبل عقد التشغيل، يحدد الفحص ذو المرحلتين ما إذا كان هناك أحد يمكن الوصول إليه أصلًا. يجيب `scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` بثلاث قيم محددة بالضبط: الخروج 0 `call-for-me` (التفعيل وإنشاء وكيل)، والخروج 1 `idle` (أنا نشط بنفسي، فيُعطَّل)، والخروج 3 `check-failed` (غير قابل للقراءة، ولا يُعامَل أبدًا على أنه خمول). تتطلب المشاركة STATE وCALL معًا؛ ومن يستدعي CALL يُنهيه عند تحقق غرضه، وإلا تنتهي صلاحيته. القواعد الكاملة في references/protocol.md.

## تحديد عقد التشغيل

1. استخدم 24 ساعة افتراضيًا. اقبل أيضًا المدد النسبية مثل 15m أو 2h أو 3d أو وقت انتهاء مطلق بصيغة ISO-8601.
2. قِس وقت البدء المحلي، وسمِّ expires_at بالتاريخ والوقت والمنطقة الزمنية.
3. ابدأ بفاصل 15 دقيقة. استخدم إيقاع references/protocol.md ما لم يطلب المستخدم إيقاعًا ثابتًا.
4. عرّف تحقق الهدف بأنه: بلوغ وقت النهاية، وتوثيق فحص FileCommander النهائي، ومعالجة جميع المدخلات المطابقة المكتشفة حتى ذلك الوقت أو توثيق حجبها بدقة، وتحديث الحالة، وإنهاء المجدول الخاص.
5. لا تدّعِ أي فحص أو تحقق من الهدف دون دليل من FileCommander.

## استخدام محولات المزوّد

### Codex

أنشئ قبل الفحص الأول هدفًا (Goal) محفوظًا بصراحة يتضمن عقد التشغيل كاملًا وexpires_at. نفّذ في كل متابعة دورة فحص كاملة واحدة. لا تُنهِ الهدف بعد دورة فارغة أو ناجحة منفردة. بعد ذلك انتظر فعليًا حتى next_scan_at، مثلًا باستخدام:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

نفّذ دورة الإغلاق عند وقت الانتهاء. ضع علامة الإكمال على الهدف فقط عند استيفاء معيار النجاح.

### Claude Code

ابدأ المهمة كـ /loop <Kadenz> $pingpong. إذا كانت المهارة قادمة من تشغيل مجدول بالفعل، فلا تنشئ حلقة ثانية. عند تغيير الإيقاع استبدل مهمة Cron الخاصة بك فقط. احذفها بعد دورة الإغلاق.

## تنفيذ الدورة

اقرأ references/protocol.md كاملًا ونفّذ دورة واحدة بالضبط من الفحص والمعالجة وتحديث الحالة كما هو موصوف هناك. استخدم ellmos FileCommander لكل وصول إلى مجلد المزامنة. لا يُعد سرد الشل أو مدخل المجدول أو اسم الملف وحده دليلًا على الفحص.

لا تخترع عملًا عند الخمول. أبلغ بإيجاز: وقت الفحص، وملفات Freshness المقروءة، والإيقاع الحالي، وempty_runs، وnext_scan_at، وexpires_at.

## تنفيذ WriteSync

اكتب فقط في فتحة النظام الخاصة بك أو في قناة عامة مُصرَّح بها صراحة. اذكر المُرسِل والمستلم والوقت والمرجع والإجراء والنتيجة والنقاط المفتوحة والإيقاع المطلوب. ادمج بدل الكتابة فوق؛ لا بيانات اعتماد؛ واحترم الأقفال. اقرأ الملف القانوني مرة أخرى باستخدام FileCommander بعد الكتابة.

## سجل التغييرات

### 1.1.0 (2026-09-13)

- أُضيفت علامة مشاركة خاصة بالمضيف STATE (الحقل `pingpong` في `agents/registry/<slot>.state.json`) وملفات CALL موجهة إلى عنوان محدد `call-<von>-to-<an|all>.txt` مع انتهاء صلاحية؛ وتعرف `pingpong_runtime.py` لذلك `state` و`call` والفحص ذو المرحلتين `check` بنتيجة ثلاثية القيم. ما زالت الأسماء القديمة `pull-` تُقرأ بصورة انتقالية. تنفيذ T-20260830-425388998 وفق قرار المستخدم بتاريخ 2026-09-11 (أصغر تغيير ممكن: STATE وCALL والانتهاء فقط).

### 1.0.1 (2026-09-09)

- أُضيفت بيانات أدوار تصريحية وفق عقد أدوار الوحدة v2 الاختياري؛ لا يُصرّح أي مُشغّل محايد بذلك. تبقى هوية البروتوكول الحالية ومسار الاكتشاف دون تغيير.

### 1.0.0 (2026-08-04)

- عقد ListenSync/WriteSync محايد تجاه المزوّد، مع محولات Goal في Codex وLoop في Claude.
- أُضيف دليل FileCommander (Beleg) وحارس الحداثة والإيقاع التكيفي وشرط الانتهاء المطلق.
