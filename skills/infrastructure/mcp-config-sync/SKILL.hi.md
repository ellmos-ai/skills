---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: "MCP कॉन्फ़िगरेशन की खोज, योजना बनाने और समन्वयन के लिए प्रदाता-निरपेक्ष प्रवेश बिंदु। उपयोगकर्ता सत्य-स्रोत, लक्ष्य और दायरा चुनता है; कोई भी प्रदाता अंतर्निहित केंद्र नहीं है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: hi
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: f28dce27691f8415486c17dfc3c7b37d7990885d89917c1d8986523de97609e7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **हिन्दी** — आधिकारिक हिन्दी संस्करण / Documento Oficial en Deutsch.

# MCP Config Sync (हिन्दी)

यह `agent-config-sync` का MCP-केंद्रित प्रवेश बिंदु है। यह किसी प्रदाता, ऐप या मास्टर फ़ाइल को मानकर नहीं चलता।

## Ablauf

1. उपयोगकर्ता से पूछें कि वह कौन-से ठोस एंडपॉइंट या अक्ष चाहता है: एक प्रदाता के भीतर विभिन्न ऐप वर्ग, एक ऐप वर्ग के भीतर विभिन्न प्रदाता, एक स्पष्ट सूची, या हर पहचाना गया प्रदाता और वर्ग।
2. `agent-config-sync/scripts/sync.py --discover` चलाएँ, फिर `--offer`।
3. पहचाने गए एंडपॉइंट को असत्यापित उम्मीदवारों से अलग करके प्रस्तुत करें।
4. उपयोगकर्ता को सत्य-स्रोत, लक्ष्य, दिशा और संघर्ष-नीति चुनने दें।
5. `registry.json` बनाएँ, `--plan` की समीक्षा करें, और तभी `--apply --yes` का उपयोग करें।

खोज और प्रस्ताव केवल-पठन हैं। कोई अंतर्निहित केंद्र नहीं है और कोई अंतर्निहित "सब कुछ समन्वयित करो" नहीं है। पूर्व के Claude Code↔Claude Desktop स्क्रिप्ट एक विरासती प्रोफ़ाइल हैं, सामान्य डिफ़ॉल्ट नहीं।

## Beispielaufruf

```
agent-config-sync/scripts/sync.py --discover
agent-config-sync/scripts/sync.py --offer
agent-config-sync/scripts/sync.py --plan
agent-config-sync/scripts/sync.py --apply --yes
```


## Änderungsprotokoll

- v2.0.0 (2026-07-27): समन्वयन को प्रदाता-निरपेक्ष बनाया गया -- अब कोई अंतर्निहित केंद्र/मास्टर फ़ाइल नहीं है, उपयोगकर्ता स्रोत, लक्ष्य, दिशा और संघर्ष-नीति स्वयं चुनता है।
- v1.0.1 (2026-06-13): Skill प्रकाशित (समन्वयन-स्क्रिप्ट + टेम्पलेट को सामान्य पथों में बदला गया, संदर्भ अनामित किए गए, EN संस्करण)।
