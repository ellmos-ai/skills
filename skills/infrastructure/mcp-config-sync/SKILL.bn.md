---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: "প্রদানকারী-নিরপেক্ষ প্রবেশবিন্দু, যা ব্যবহারকারী-নির্বাচিত প্রদানকারী এবং অ্যাপ শ্রেণির মধ্যে MCP কনফিগারেশন আবিষ্কার, পরিকল্পনা ও সমন্বয় করে। ব্যবহারকারী উৎস, গন্তব্য এবং পরিসর নির্বাচন করেন; কোনো প্রদানকারীই অন্তর্নিহিত কেন্দ্র নয়।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: bn
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: f28dce27691f8415486c17dfc3c7b37d7990885d89917c1d8986523de97609e7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **বাংলা** — অফিসিয়াল বাংলা সংস্করণ।

# MCP কনফিগ সিঙ্ক (বাংলা)

এটি `agent-config-sync`-এর MCP-কেন্দ্রিক প্রবেশবিন্দু। এটি কোনো প্রদানকারী, অ্যাপ বা মাস্টার ফাইল ধরে নেয় না।

## প্রক্রিয়া

1. ব্যবহারকারী কোন নির্দিষ্ট endpoint বা অক্ষ চান তা জিজ্ঞাসা করুন: একটি প্রদানকারীর মধ্যে বিভিন্ন অ্যাপ শ্রেণি জুড়ে, একটি অ্যাপ শ্রেণির মধ্যে বিভিন্ন প্রদানকারী জুড়ে, একটি স্পষ্ট তালিকা, অথবা সনাক্ত করা প্রতিটি প্রদানকারী ও শ্রেণি।
2. `agent-config-sync/scripts/sync.py --discover` চালান, তারপর `--offer`।
3. সনাক্ত করা endpoint গুলো যাচাই-না-করা প্রার্থী থেকে আলাদাভাবে উপস্থাপন করুন।
4. ব্যবহারকারীকে উৎস, গন্তব্য, দিক এবং সংঘাত নীতি বেছে নিতে দিন।
5. `registry.json` তৈরি করুন, `--plan` পর্যালোচনা করুন, এবং তারপরই কেবল `--apply --yes` ব্যবহার করুন।

আবিষ্কার ও প্রস্তাব শুধু-পঠনযোগ্য। কোনো অন্তর্নিহিত কেন্দ্র নেই এবং কোনো অন্তর্নিহিত "সব সিঙ্ক" নেই। পূর্বের Claude Code↔Claude Desktop স্ক্রিপ্টগুলো একটি legacy প্রোফাইল, সাধারণ ডিফল্ট নয়।

## উদাহরণ আহ্বান

```
agent-config-sync/scripts/sync.py --discover
agent-config-sync/scripts/sync.py --offer
agent-config-sync/scripts/sync.py --plan
agent-config-sync/scripts/sync.py --apply --yes
```


## পরিবর্তন লগ

- v2.0.0 (2026-07-27): সিঙ্ক প্রদানকারী-নিরপেক্ষ করা হয়েছে -- আর কোনো অন্তর্নিহিত হাব/মাস্টার ফাইল নেই, ব্যবহারকারী উৎস, গন্তব্য, দিক ও সংঘাত নীতি নিজে বেছে নেন।
- v1.0.1 (2026-06-13): Skill প্রকাশিত (সিঙ্ক স্ক্রিপ্ট + টেমপ্লেট সাধারণ পথে রূপান্তরিত, রেফারেন্স বেনামী করা, EN সংস্করণ)।
