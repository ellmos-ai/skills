---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "এই স্কিলটি ব্যবহার করুন যখন ব্যবহারকারী একই প্রম্পট একাধিক LLM-এ পাঠাতে এবং উত্তরগুলো তুলনা করতে চান — ধারাবাহিকভাবে (স্টপওয়াচ, প্রতিটি লেনের পরিষ্কার সময়নির্ধারণ) অথবা সমান্তরালে (প্রকৃত রেস), প্রতি মডেলের জন্য ঐচ্ছিক পুনরাবৃত্তিসহ, এবং শুরুর মডেল দ্বারা মূল্যায়িত হয় গুণমান, সঠিকতা, সম্পূর্ণতা, নির্দেশনার বিশ্বস্ততা ও বিলম্ব বিবেচনায় (সময় কেবল একটি মাত্রা)। /compare-race, 'model race', 'vergleiche modelle', 'gleicher prompt an mehrere modelle', 'মডেল রেস', 'মডেলগুলো তুলনা করুন', 'একাধিক মডেলে একই প্রম্পট' ট্রিগারে সক্রিয় হয়।"
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: bn
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — পয়েন্টার-স্কিল (বাংলা)

> **এই স্কিলটি একটি বিশুদ্ধ পয়েন্টার। সত্যের উৎস হলো মডিউল।**

## মডিউল-পাথ

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

Repo: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## এজেন্টের প্রতি নির্দেশনা

1. মডিউল-ফোল্ডারে রোল-প্রম্পট **`prompts/RACE-STARTER.de.md`** পড়ুন এবং তা অনুসরণ করুন।
   আপনি RACE-STARTER — এবং ডিফল্ট হিসেবে **Judge**ও (ব্যবহারকারীর সিদ্ধান্ত
   2026-08-16)।
2. Config যাচাই করুন (`compare-race config`; Host-Config আছে `~/.compare-race/`-এ)।
   মোড বেছে নিন: `sequential` = স্টপওয়াচ (প্রতি লেনের পরিষ্কার একক পরিমাপ) ·
   `parallel` = প্রকৃত রেস। **স্টপওয়াচ কেবল একটি চিত্র** — সময় গুণমান, সঠিকতা, সম্পূর্ণতা, নির্দেশনার বিশ্বস্ততা, খরচের নিচের একটি মাত্রা।
3. রেস শুরু করুন (`compare-race run --prompt-file …`); coma ছাড়া মডেল-ম্যানুয়াল পথে যান `compare-race record`-এর মাধ্যমে।
4. Judge হিসেবে রেস-ফোল্ডারের `RACE.md`-এ রুব্রিক পূরণ করুন — প্রতিটি RUN-ফাইল নিজে পড়ুন; নিজের মডেল অংশ নিলে পক্ষপাত উল্লেখ করুন।
5. অক্ষের শৃঙ্খলা: কেবল একটি অক্ষ পরিবর্তিত হলে কারণ আরোপ করুন (model = রেস · run = ভ্যারিয়েন্স · time = মডেল-ড্রিফট)।

## কোটা-সতর্কতা

রেস **প্রতিটি** জড়িত কোটায় খরচ হয় (claude/codex/agy/kimi)। বড় রেসের আগে (অনেক লেন × পুনরাবৃত্তি) ব্যবহারকারীকে জিজ্ঞাসা করুন।
