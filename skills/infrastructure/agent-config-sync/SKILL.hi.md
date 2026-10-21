---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: "एजेंट प्रदाताओं और ऐप वर्गों में MCP कॉन्फ़िगरेशन, skills और नियम फ़ाइलों को सिंक्रनाइज़ करने के लिए प्रदाता-निरपेक्ष प्लानर। यह प्रमाणित स्थानीय विकल्पों की खोज करता है और उपयोगकर्ता को सत्य स्रोत, लक्ष्य, दिशा और टकरावों को चुनने देता है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: hi
status: active
visibility: public
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 53ba3789a0734868d5d243eab03ffe02b5daee779a5ccf68036937081049010c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.545223+00:00"
---
<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# Agent Config Sync (Deutsch)

यह skill एंडपॉइंट चयन, संसाधनों और सत्य स्रोत को अलग रखता है। चलाएँ:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```


उपयोगकर्ता एक स्पष्ट एंडपॉइंट सूची, ऐप वर्गों में एक प्रदाता, प्रदाताओं में एक ऐप वर्ग, या सभी पाए गए एंडपॉइंट चुन सकता है। पहचान प्रमाण है, प्राधिकरण नहीं।

सत्य स्रोत एक एंडपॉइंट, एक फ़ाइल, फ़ाइलों का एक क्रमबद्ध समूह जैसे कई `AGENTS.md` परतें, या एक skills डायरेक्टरी हो सकता है। कोई फ़ाइलनाम या प्रदाता अंतर्निहित केंद्र नहीं है। चयनित सत्य स्रोत के बिना, योजनाएँ अवरुद्ध रहती हैं।

`--status` और `--plan` की समीक्षा करें; `--apply --yes` का उपयोग केवल स्वीकृति के बाद करें। MCP ब्लॉक और skill डायरेक्टरी लागू किए गए हैं। नियम-फ़ाइल टोपोलॉजी तब तक fail-closed रहती हैं जब तक उपयोगकर्ता कोई merge/redirect adapter नहीं चुनता।
