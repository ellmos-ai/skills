---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "গেম ডেভেলপমেন্ট একটি প্রক্রিয়া হিসেবে কীভাবে কাজ করে — ভূমিকা, উপ-কাজ, ওয়ার্কফ্লো ও ভূমিকার বর্ণনা, বিশেষ করে (তবে শুধু নয়) Roblox-এর জন্য। যখন বিষয়টি গেম ডেভেলপমেন্টের সংগঠন নিয়ে, নির্দিষ্ট কোড নিয়ে নয়, তখন এই স্কিল ব্যবহার করুন: কোন ভূমিকাগুলো আছে (Creative Director, Engineer, Artist, Polish/Audio, Business, QA-Tester, Game Critic)? কে কোন উপ-কাজ করে? একটি ডেভেলপমেন্ট চেইন (concept → backend → frontend → polish → test) কেমন দেখায়? কীভাবে একটি Game Design Document / KONZEPT.md লেখা হয়? কয়েকটি (AI) এজেন্ট কীভাবে একটি গেম ভাগ করে নেয়? এছাড়াও এগুলোতে ট্রিগার করুন: \"plan a new game\" (একটি নতুন গেম পরিকল্পনা করো), \"create Game Design Document\" (গেম ডিজাইন ডকুমেন্ট তৈরি করো), \"which roles do I need for my game\" (আমার গেমের জন্য কোন ভূমিকা লাগবে), \"development workflow for a game\" (গেমের জন্য ডেভেলপমেন্ট ওয়ার্কফ্লো), \"who tests the game\" (গেমটি কে পরীক্ষা করে), \"structure a game idea\" (একটি গেম ধারণা সাজাও), \"Roblox genre/monetization\" (Roblox ঘরানা/মনিটাইজেশন)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/game-design/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: e21ae8c9208280a65f748fd252d86404a38bd12ad05bb53c5f6b0531c56b0720
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="game-design banner">

# Game Design — ভূমিকা, উপ-কাজ ও ওয়ার্কফ্লো

## উদ্দেশ্য

গেম ডেভেলপমেন্ট হলো স্পষ্টভাবে আলাদা বিষয়ের সমন্বয়ে গঠিত দলগত কাজ — যদিও একজন ব্যক্তি বা একটি AI এজেন্ট এর একাধিক অংশ একসাথে করতে পারে। এই স্কিল দেয় **সাংগঠনিক মডেল**: কী কী ভূমিকা আছে, কোন উপ-কাজ এর অন্তর্ভুক্ত, কোন ক্রমে এগুলো একসাথে কাজ করে এবং কীভাবে একটি গেমকে একটি ধারণাপত্র (GDD) হিসেবে লিপিবদ্ধ করা হয়। *প্রযুক্তিগত* দিকের জন্য দেখুন `/rojo` (Sync), `/rbx-studio` (Editor/Assets) এবং মেটাস্কিল `/rbx-dev` (Architektur)।

একটি নতুন গেম পরিকল্পনা করার সময়, কাজ ভাগ করার সময় (একাধিক AI এজেন্টের মধ্যেও) এবং একটি Game Design Document লেখা বা পর্যালোচনা করার সময় এই স্কিল ব্যবহার করুন।

## ভূমিকাসমূহ (৫টি উন্নয়ন + ২টি পরীক্ষা)

একটি প্রমাণিত, সংক্ষিপ্ত ভূমিকা-বিভাজন। সব উপ-কাজসহ সম্পূর্ণ বর্ণনা: [`references/roles-and-workflows.md`](references/roles-and-workflows.md)।

| ভূমিকা | মনোযোগ | মূল উপ-কাজ |
| --- | --- | --- |
| **Creative Director** | কী & কেন & কার জন্য | GDD/KONZEPT, মেকানিক্স ডিজাইন ও ব্যালেন্সিং, অগ্রাধিকার/Sprints, Story, UX-Flow |
| **Engineer** | কীভাবে (প্রযুক্তিগত) | Server/Client/Shared-Code, Game-Loop, নেটওয়ার্ক/Remotes, DevOps (Rojo, Build), বাগ ঠিক করা |
| **Artist** | জগৎ কেমন দেখায় | ওয়ার্ল্ড/লেভেল নির্মাণ, আলো ও পরিবেশ, পার্টিকল, অ্যাসেট সংগ্রহ (ম্যালওয়্যার যাচাই সহ) |
| **Polish / Audio** | কেমন লাগে ও শোনায় | SFX/মিউজিক/অ্যামবিয়েন্ট, অ্যানিমেশন, UI/UX-পালিশ, "Juice" (Screen-Shake, Hit-Stop), Feedback |
| **Business** | বাইরের জগতের সাথে | স্টোর পেজ, আইকন/থাম্বনেইল, Monetarisierung (Gamepass/Products/Pass), Analytics, Community |
| **QA-Tester** | প্রযুক্তিগতভাবে সঠিক? | কোডে বাগ স্ক্যান, Playtests + Console যাচাই, পুনরুৎপাদনযোগ্য রিপোর্ট, Regression, Performance |
| **Spielkritiker** | মজা লাগছে কি? | খেলোয়াড়ের দৃষ্টিতে প্রথম/দীর্ঘমেয়াদি ইমপ্রেশন, সৎ মূল্যায়ন (মজা, স্পষ্টতা, ন্যায্যতা), পরামর্শ |

**মূল নিয়ম:** উন্নয়ন ও পরীক্ষা **আলাদা** ভূমিকা — আদর্শভাবে আলাদা ব্যক্তি বা এজেন্ট। যে কোড লেখে, সে তা নিরপেক্ষভাবে পরীক্ষা করতে পারে না। Spielkritiker কঠোর হতে পারে।

## ওয়ার্কফ্লো (ডেভেলপমেন্ট-চেইন)

কাজ ভূমিকা থেকে ভূমিকায় একটি চেইন হিসেবে প্রবাহিত হয়। গুরুত্বপূর্ণ ধরনগুলো:

**স্ট্যান্ডার্ড-ফিচার-চেইন:**
```
Creative Director (plant Feature) → Engineer (Backend) → Artist (Frontend/Assets)
→ Polish/Audio (Sound + Feinschliff) → QA-Tester (technischer Test)
→ Spielkritiker (Spielerperspektive) → Creative Director (Feedback → nächste Iteration)
```


**Quick-Fix-Chain:** QA-Tester (Bug) → Engineer (Fix) → QA-Tester (verifiziert)।

**Asset-Chain:** Artist (Store-Suche) → Artist (Malware-Scan) → Artist (einbinden) → QA (visuell)।

**Polish-Chain:** Spielkritiker (Schwäche) → Polish/Audio → Artist → Spielkritiker (Re-Check)।

**Mensch-im-Loop:** [Agenten-Chain] → menschlicher Tester → Creative Director (Feedback) → [Chain]।

প্রতিটি পুনরাবৃত্তি একটি সংক্ষিপ্ত Changelog রেখে যাওয়া উচিত। থামার শর্ত: সময়সীমা পূর্ণ **বা** গুণমান-লক্ষ্য পূরণ।

### Persona-ভিত্তিক পরীক্ষা

একটি গেম তখনই টিকে থাকে যখন খুবই ভিন্ন ধরনের খেলোয়াড় এর সাথে মানিয়ে নিতে পারে। তাই নিজের দৃষ্টিকোণ থেকে শুধু নয়, **Personas** থেকেও পরীক্ষা করুন (এজেন্ট দিয়ে সিমুলেটেড হলেও) — বয়স, অভিজ্ঞতা, প্ল্যাটফর্ম (PC/Mobile/Tablet/Konsole), মনোযোগের সময়, ভাষা ও অ্যাক্সেসিবিলিটি অনুযায়ী ভিন্ন করুন। উদাহরণ: একটি ৯ বছরের Casual-শিশু Tablet-এ, যে শুধু বোতাম টিপতে চায়; একটি ১২ বছরের Core-খেলোয়াড় PC-তে, যে Meta খোঁজে; একজন ৬০+ নবাগত, যার বড় বোতাম দরকার। Persona-পরীক্ষা **blind** চালানো উচিত (পরীক্ষক ডিজাইনের উদ্দেশ্য জানে না)।

## Game Design Document (KONZEPT.md)

প্রতিটি গেম একটি সংক্ষিপ্ত GDD-তে লিপিবদ্ধ করুন — টেমপ্লেট: [`assets/KONZEPT_template.md`](assets/KONZEPT_template.md)। ন্যূনতম কাঠামো:

- **Vision** — ১–২ বাক্য: গেমটি কী?
- **ঘরানা / রেফারেন্স** — শ্রেণিবিভাগ + রেফারেন্স-শিরোনাম।
- **মূল মেকানিক্স** — **সর্বোচ্চ ৩–৪টি** (ফোকাস গুণমান নিশ্চিত করে)।
- **Gameplay-Loop** — খেলোয়াড়ের মিনিট-প্রতি-মিনিটের চক্র।
- **গেম মোড / সময়ের ফরম্যাট** — প্রাসঙ্গিক হলে।
- **Monetarisierung** — Gamepasses, Developer Products, Battle Pass, Shop।
- **Technik** — Stack (Rojo/Frameworks), মোটামুটি আর্কিটেকচার।
- **পরবর্তী ধাপ** — বাস্তবায়ন-চেকলিস্ট।
- **পরিচিত বাগ / খোলা বিষয়**।

## Multi-Agent-কাজের বিভাজন

একাধিক AI এজেন্ট (বা মানুষ+AI) একটি গেম ভাগ করে নিতে পারে — দুটি মোড:

- **Schwarm** — একই কাজ, ভিন্ন ক্ষেত্র (যেমন তিনটি এজেন্ট প্রতিটি একটি সিস্টেম ব্যালেন্স করে)।
- **Team** — ভিন্ন ভূমিকা, একে অপরের সাথে সমন্বিত (Engineer + Artist + Polish একটি ফিচারে সমান্তরালে, Creative Director দ্বারা সমন্বিত)।

চর্চায় প্রমাণিত: উন্নয়ন ও পরীক্ষা **কখনও** একই এজেন্টকে দেবেন না; প্রতি ভূমিকার জন্য রোল-প্রম্পট স্থির রাখুন (System-Prompt = ভূমিকার বর্ণনা); প্রতিটি Chain-পুনরাবৃত্তি Changelog + টেস্ট রিপোর্ট দিয়ে শেষ হওয়া উচিত; মানুষ গুণমান-Gate হিসেবে থাকে।

## Roblox-নির্দিষ্ট বাজার-প্রেক্ষাপট (দিকনির্দেশনা)

প্ল্যাটফর্ম-জ্ঞান যা Roblox-এর জন্য ধারণা-কাজকে বাস্তবভিত্তিক করে (কোনো গ্যারান্টি নয়, শুধু মোটা নিয়ম):

- **লাভজনক Genres:** Simulator, RPG, Tycoon, Horror, Obby — স্কেলিং ও প্রচেষ্টায় অনেক ভিন্ন।
- **কম-সরবরাহের নিশ (বেশি ঝুঁকি, কম প্রতিযোগিতা):** প্রকৃত Strategie/RTS-Lite, উচ্চমানের Sportspiele, Cozy/Life-Sim, Coop-Puzzle/Escape, Auto-Battler।
- **সোনালি Monetarisierungs-নিয়ম:** (১) LiveOps বাধ্যতামূলক (প্রতি ২–৪ সপ্তাহে Updates), (২) Monetarisierung Gameplay *সমর্থন* করা উচিত, বাধা নয়, (৩) Social-Design (Trading, Coop) অবকাঠামো, (৪) Mobile-First (৫০ %+ মোবাইলে খেলে), (৫) Content-Creator-উপযোগিতা (YouTube/TikTok) হলো Marketing।

> বর্তমান, নির্ভরযোগ্য বাজার-সংখ্যার জন্য অনুমান না করে গবেষণা করুন — উপরের বিষয়গুলো স্থিতিশীল হিউরিস্টিক, লাইভ ডেটা নয়।

## আরও জানতে

- সহোদর স্কিল: `/rojo`, `/rbx-studio`; মেটাস্কিল `/rbx-dev` (Architektur-Pattern, Projektstruktur, Luau-Lessons)।
- রেফারেন্স-Pipeline (যদি থাকে): `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`, `IDEAS.md`, Marktanalysen)।

## Changelog

### 1.0.0 (2026-06-17)
- প্রাথমিক সংস্করণ। সাধারণ ভূমিকা-/ওয়ার্কফ্লো-ফ্রেমওয়ার্ক, `.ROBLOX/AGENT_ROLES.md` ও `GUIDE.md` থেকে নিষ্কাশিত, ব্যবহারকারী-নিরপেক্ষ (কোনো প্রকল্প-নির্দিষ্ট পোর্টফোলিও ছাড়া)।

## সম্পর্কিত স্কিল

- `roblox-team-lock` — ফাইল-, Studio- ও MCP-Claims, একাধিক এজেন্ট একই প্রকল্পে কাজ করা শুরু করলে। আগে পড়ুন, তারপর Claim করুন, তারপর কাজ করুন, তারপর ছেড়ে দিন।
