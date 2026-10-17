---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "একটি সময়সীমাবদ্ধ, সেশন-নির্ভর রেডিও স্টেশন চালায় যা একটি যৌথভাবে সিঙ্ক্রোনাইজড ফোল্ডারের মাধ্যমে কাজ করে। ListenSync নিয়মিতভাবে কাজের অনুরোধ ও নতুন তথ্য স্ক্যান করে; WriteSync ডেল্টা ও রিসিপ্ট পাঠায়। PingPong, Dosentelefon, ListenSync, WriteSync, Sync-Listener, Auftragswache, News-Scan বা Goal-/Loop-পর্যবেক্ষণ বলা হলে ব্যবহার করুন।"
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: bn
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
translated_at: "2026-10-15T12:34:25.723027+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

একটি সাধারণ Sync-ফোল্ডারের মাধ্যমে দুই বা ততোধিক সিস্টেমকে রেডিও স্টেশন হিসেবে চালান। ফলাফল-সংক্রান্ত চুক্তি প্রদানকারী-নিরপেক্ষ রাখুন; শুধু ধারাবাহিকতার অ্যাডাপ্টারটি আলাদা।

## মোড নির্ধারণ করুন

- ListenSync: প্রতি হোস্টে ঠিক একটি নিয়মিত listener। এটি স্ক্যান করে, উপযুক্ত কাজ গ্রহণ করে এবং উত্তর থাকলে WriteSync-ও চালায়।
- WriteSync: প্রতিটি সক্রিয় অভিনেতা নিজের প্রাসঙ্গিক ডেল্টা, কাজ, নতুন তথ্য ও রিসিপ্ট পাঠাতে পারে। এই মোড কোনো listener চালু করে না।
- মোড উল্লেখ না থাকলে ListenSync ব্যবহার করুন।

## অংশগ্রহণ স্পষ্ট করুন (STATE ও CALL)

লেনদেন-চুক্তির আগে দ্বিস্তরীয় যাচাই নির্ধারণ করে কাউকে আদৌ পাওয়া যাবে কি না। `scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` ঠিক তিনটি মান দিয়ে উত্তর দেয়: Exit 0 `call-for-me` (সক্রিয় করুন এবং একটি এজেন্ট চালু করুন), Exit 1 `idle` (আমি নিজে সক্রিয়, নিষ্ক্রিয় করুন), Exit 3 `check-failed` (পড়া যায় না, কখনো নিষ্ক্রিয় বলে ধরবেন না)। অংশগ্রহণে STATE ও CALL দুটোই লাগে; যিনি কল আহ্বান করেন তিনি উদ্দেশ্য পূরণ হলে তা শেষ করেন, নয়তো তা মেয়াদোত্তীর্ণ হয়। সম্পূর্ণ নিয়ম references/protocol.md-এ।

## চালানোর চুক্তি স্থির করুন

1. ডিফল্ট হিসেবে 24h ব্যবহার করুন। 15m, 2h, 3d-এর মতো আপেক্ষিক সময়কাল বা একটি নির্দিষ্ট ISO-8601 শেষ সময়ও গ্রহণ করুন।
2. স্থানীয় শুরুর সময় মাপুন এবং expires_at তারিখ, সময় ও সময়অঞ্চলসহ উল্লেখ করুন।
3. 15 মিনিট দিয়ে শুরু করুন। ব্যবহারকারী নির্দিষ্ট কাডেন্স না চাইলে references/protocol.md-এর কাডেন্স ব্যবহার করুন।
4. লক্ষ্য পূরণের সংজ্ঞা: শেষ সময় পৌঁছেছে, চূড়ান্ত FileCommander-স্ক্যান প্রমাণিত, ততক্ষণ পর্যন্ত শনাক্ত সব উপযুক্ত ইনপুট প্রক্রিয়াজাত বা সুনির্দিষ্টভাবে বাধাগ্রস্ত হিসেবে নথিবদ্ধ, State হালনাগাদ এবং নিজস্ব scheduler বন্ধ।
5. FileCommander-প্রমাণ ছাড়া স্ক্যান বা লক্ষ্য পূরণের দাবি করবেন না।

## প্রদানকারী-অ্যাডাপ্টার ব্যবহার করুন

### Codex

প্রথম স্ক্যানের আগে সম্পূর্ণ চালানোর চুক্তি ও expires_at-সহ একটি স্থায়ী Goal স্পষ্টভাবে তৈরি করুন। প্রতিটি ধারাবাহিকতায় ঠিক একটি সম্পূর্ণ স্ক্যান-চক্র চালান। খালি বা সফল একক চক্রের পরে Goal শেষ করবেন না। এরপর প্রকৃতভাবে next_scan_at পর্যন্ত অপেক্ষা করুন, যেমন:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

মেয়াদ শেষের সময়ে সমাপনী চক্র চালান। সফলতার মানদণ্ড পূরণ হলেই Goal সম্পন্ন হিসেবে চিহ্নিত করুন।

### Claude Code

কাজটি এভাবে শুরু করুন: /loop <Kadenz> $pingpong। নির্ধারিত চালনা থেকে স্কিলটি এলে দ্বিতীয় loop তৈরি করবেন না। কাডেন্স বদলালে শুধু নিজের Cron-জব প্রতিস্থাপন করুন। সমাপনী চক্রের পরে সেটি মুছে ফেলুন।

## চক্র চালান

references/protocol.md সম্পূর্ণ পড়ুন এবং সেখানে বর্ণিত ঠিক একটি স্ক্যান, প্রক্রিয়াকরণ ও State-চক্র চালান। Sync-ফোল্ডারের প্রতিটি প্রবেশের জন্য ellmos FileCommander ব্যবহার করুন। শুধু shell-তালিকা, scheduler-এন্ট্রি বা ফাইলের নাম স্ক্যানের প্রমাণ নয়।

নিষ্ক্রিয়তায় কাজ বানাবেন না। সংক্ষেপে জানান: স্ক্যানের সময়, পড়া Freshness-ফাইল, বর্তমান কাডেন্স, empty_runs, next_scan_at ও expires_at।

## WriteSync চালান

শুধু নিজের সিস্টেম-স্লটে বা স্পষ্টভাবে বৈশ্বিক চ্যানেলে লিখুন। প্রেরক, প্রাপক, সময়, সূত্র, কার্যক্রম, ফলাফল, খোলা বিষয় ও কাঙ্ক্ষিত কাডেন্স উল্লেখ করুন। ওভাররাইট না করে মার্জ করুন; কোনো credential নয়; Lock মেনে চলুন। লেখার পরে FileCommander দিয়ে কানোনিক্যাল ফাইলটি আবার পড়ে যাচাই করুন।

## Changelog

### 1.1.0 (2026-09-13)

- হোস্টভিত্তিক অংশগ্রহণ-চিহ্ন STATE (`agents/registry/<slot>.state.json`-এর ভেতরে `pingpong` ক্ষেত্র) এবং মেয়াদসহ ঠিকানাযুক্ত CALL-ফাইল `call-<von>-to-<an|all>.txt` যোগ করা হয়েছে; `pingpong_runtime.py` এর জন্য `state`, `call` এবং তিন-মানের ফলাফলসহ দ্বিস্তরীয় যাচাই `check` জানে। পুরোনো `pull-` নামগুলো অন্তর্বর্তীভাবে এখনো পড়া হয়। 2026-09-11-এর ব্যবহারকারী সিদ্ধান্ত অনুযায়ী T-20260830-425388998 বাস্তবায়িত (ক্ষুদ্রতম পরিবর্তন: শুধু STATE, CALL ও মেয়াদ)।

### 1.0.1 (2026-09-09)

- ঐচ্ছিক Modul-v2-ভূমিকা-চুক্তি অনুযায়ী ঘোষণামূলক ভূমিকা-মেটাডেটা যোগ করা হয়েছে; কোনো নিরপেক্ষ স্টার্টার তা ঘোষণা করে না। বিদ্যমান প্রোটোকল-পরিচয় ও Discovery-পথ অক্ষুণ্ণ।

### 1.0.0 (2026-08-04)

- Codex-Goal ও Claude-Loop অ্যাডাপ্টারসহ প্রদানকারী-নিরপেক্ষ ListenSync-/WriteSync-চুক্তি।
- FileCommander-প্রমাণ, Freshness-Guard, অভিযোজিত কাডেন্স ও নিরঙ্কুশ মেয়াদ-শর্ত যোগ করা হয়েছে।
