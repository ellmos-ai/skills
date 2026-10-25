---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: "نقطة دخول محايدة تجاه المزوّدين لاكتشاف إعدادات MCP وتخطيطها ومزامنتها بين المزوّدين وفئات التطبيقات التي يختارها المستخدم. يحدد المستخدم مصدر الحقيقة والأهداف والنطاق؛ ولا يوجد مزوّد يعمل كمحور ضمني."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: ar
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: f28dce27691f8415486c17dfc3c7b37d7990885d89917c1d8986523de97609e7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# مزامنة إعدادات MCP (Deutsch)

هذه نقطة الدخول المركّزة على MCP إلى `agent-config-sync`. وهي لا تفترض وجود
مزوّد أو تطبيق أو ملف رئيسي.

## سير العمل

1. اسأل عن نقاط النهاية أو المحاور المحددة التي يريدها المستخدم: ضمن مزوّد واحد
   عبر فئات التطبيقات، أو ضمن فئة تطبيق واحدة عبر المزوّدين، أو قائمة صريحة، أو
   كل المزوّدين وفئات التطبيقات المكتشفة.
2. شغّل `agent-config-sync/scripts/sync.py --discover`، ثم `--offer`.
3. اعرض نقاط النهاية المكتشفة منفصلةً عن المرشحين غير المتحقَّق منهم.
4. دع المستخدم يختار مصدر الحقيقة والأهداف والاتجاه وسياسة التعارض.
5. أنشئ `registry.json`، وراجع `--plan`، ولا تستخدم
   `--apply --yes` إلا بعد ذلك.

الاكتشاف والعروض للقراءة فقط. لا يوجد محور ضمني ولا "مزامنة للكل" ضمنية. أما
البرامج النصية القديمة للمزامنة ثنائية الاتجاه بين Claude Code وClaude Desktop فهي ملف تعريف قديم
وليست الافتراضي العام.

## مثال على الاستدعاء

```
agent-config-sync/scripts/sync.py --discover
agent-config-sync/scripts/sync.py --offer
agent-config-sync/scripts/sync.py --plan
agent-config-sync/scripts/sync.py --apply --yes
```


## سجل التغييرات

- v2.0.0 (2026-07-27): جُعلت المزامنة محايدة تجاه المزوّدين -- لم يعد هناك ملف
  محور/رئيسي ضمني، ويختار المستخدم المصدر والأهداف والاتجاه وسياسة التعارض بنفسه.
- v1.0.1 (2026-06-13): نُشرت المهارة (نُقلت البرامج النصية للمزامنة والقالب إلى
  مسارات عامة، وجُعلت المراجع مجهولة المصدر (anonymized)، وأُضيفت النسخة الإنجليزية).
