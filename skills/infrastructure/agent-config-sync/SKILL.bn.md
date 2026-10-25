---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-07-27
description: "প্রদানকারী-নিরপেক্ষ একটি প্ল্যানার, যা এজেন্ট প্রদানকারী এবং অ্যাপ শ্রেণিজুড়ে MCP কনফিগারেশন, skills এবং rule ফাইল সমন্বয় করে। এটি প্রমাণিত স্থানীয় বিকল্পগুলো খুঁজে বের করে এবং ব্যবহারকারীকে সত্য-উৎস, লক্ষ্য, দিক এবং দ্বন্দ্ব বেছে নিতে দেয়।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: bn
status: active
visibility: public
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 53ba3789a0734868d5d243eab03ffe02b5daee779a5ccf68036937081049010c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.567943+00:00"
---
<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# Agent Config Sync (Deutsch)

এই skill এন্ডপয়েন্ট নির্বাচন, রিসোর্স এবং সত্য-উৎসকে আলাদা করে। চালান:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

ব্যবহারকারী একটি স্পষ্ট এন্ডপয়েন্ট তালিকা, অ্যাপ শ্রেণিজুড়ে একটি প্রদানকারী, প্রদানকারীজুড়ে একটি অ্যাপ শ্রেণি, অথবা সনাক্ত করা সকল এন্ডপয়েন্ট নির্বাচন করতে পারে। সনাক্তকরণ হলো প্রমাণ, অনুমোদন নয়।

সত্য-উৎস হতে পারে একটি এন্ডপয়েন্ট, একটি ফাইল, ফাইলের একটি ক্রমবদ্ধ সেট যেমন একাধিক `AGENTS.md` স্তর, অথবা একটি skills ডিরেক্টরি। কোনো ফাইলের নাম বা প্রদানকারী স্বয়ংক্রিয়ভাবে কেন্দ্র হিসেবে গণ্য হয় না। কোনো সত্য-উৎস নির্বাচিত না হলে পরিকল্পনাগুলো অবরুদ্ধ থাকে।

`--status` এবং `--plan` পর্যালোচনা করুন; অনুমোদনের পরেই কেবল `--apply --yes` ব্যবহার করুন। MCP ব্লক এবং skill ডিরেক্টরিগুলো বাস্তবায়িত। একটি merge/redirect অ্যাডাপ্টার নির্বাচন না করা পর্যন্ত rule-ফাইল topology গুলো fail-closed অবস্থায় থাকে।
