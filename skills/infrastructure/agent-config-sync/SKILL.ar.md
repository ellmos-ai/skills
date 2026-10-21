---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: "مخطط محايد تجاه المزوّد لمزامنة إعدادات MCP وملفات المهارات والقواعد عبر مزوّدي الوكلاء وفئات التطبيقات. يكتشف الخيارات المحلية الموثّقة بالأدلة، ويتيح للمستخدم اختيار المصدر الموثوق والأهداف والاتجاه والتعارضات."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: ar
status: active
visibility: public
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 53ba3789a0734868d5d243eab03ffe02b5daee779a5ccf68036937081049010c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **العربية** — النسخة الرسمية بالعربية.

# مزامنة إعدادات الوكلاء (العربية)

تفصل المهارة بين اختيار نقاط النهاية والموارد والمصدر الموثوق. شغّل:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

يمكن للمستخدم اختيار قائمة صريحة من نقاط النهاية، أو مزوّدًا واحدًا عبر فئات التطبيقات،
أو فئة تطبيق واحدة عبر المزوّدين، أو جميع نقاط النهاية المكتشفة. الاكتشاف دليل وليس تفويضًا.

يمكن أن يكون المصدر الموثوق نقطة نهاية واحدة، أو ملفًا واحدًا، أو مجموعة مرتبة من الملفات مثل
طبقات `AGENTS.md` المتعددة، أو دليل مهارات. لا يوجد اسم ملف أو مزوّد يُعدّ المحور الضمني. وبدون
مصدر موثوق محدّد، تبقى الخطط محجوبة.

راجع `--status` و `--plan`؛ ولا تستخدم `--apply --yes` إلا بعد الموافقة.
كتل MCP ودلائل المهارات منفّذة. أما طوبولوجيات ملفات القواعد فتبقى مغلقة عند الفشل
حتى يختار المستخدم محوّل الدمج أو إعادة التوجيه.
