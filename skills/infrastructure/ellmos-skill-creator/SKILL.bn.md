---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "এই ইকোসিস্টেমের জন্য একটি Skill তৈরি বা সংশোধন করে: সাধারণ ইন্টারভিউ/খসড়া/মূল্যায়ন চক্রটি অফিসিয়াল skill-creator-Plugin (Anthropic, Apache-2.0)-এ অর্পণ করে, কিন্তু অতিরিক্তভাবে সেই ellmos-প্রয়োজনীয়তাগুলো প্রয়োগ করে যেগুলো অফিসিয়াল Plugin জানে না — হাউস-ফ্রন্টম্যাটার (9টি ক্ষেত্র), ক্যাটাগরি/দৃশ্যমানতার নিয়ম, অ্যানবিটার/ব্যবহারকারী/ellmos-নিরপেক্ষ কিন্তু ellmos-সংবেদনশীল শনাক্তকরণ grounding-seed-এর মাধ্যমে, সরবরাহকৃত config.json (শিক্ষা-চুক্তিসহ) + connections.json, অ্যানবিটার/ভেন্ডর-সচেতনতা (অত্যাধুনিক বিকল্পসমূহ প্রস্তাব করে, নিজস্ব ellmos-উপাদানসহ), একটি স্ব-হালনাগাদ বিভাগ এবং একটি পুনঃব্যবহারযোগ্য শিক্ষা-/কভারেজ ফাইল-সেট (user-usecases.json, usecase-gaps.json, known-providers-and-abilities.json, gap-closing-analysis.json — skill-creator-এর evals.json এবং A2A/AgentSkill-এর আদলে, কোনো সমান্তরাল মানদণ্ড নয়)। যখনই এই সিস্টেমের জন্য একটি নতুন Skill তৈরি হবে বা একটি বিদ্যমান Skill ellmos-সামঞ্জস্যে পুনর্গঠন করতে হবে তখন সর্বদা ব্যবহার করুন — \"একটি Skill তৈরি করো\", \"X-এর জন্য একটি Skill বানাও\", \"skill-creator ব্যবহার করো\", \"নতুন Skill তৈরি করো\", \"এই Skill-টিকে ellmos-সামঞ্জস্যপূর্ণ করো\", \"কোনো Skill-এর জন্য শিক্ষা-চুক্তি/আচরণ-কোড তৈরি করো\", \"কোনো Skill-এর usecase-কভারেজ যাচাই করো\" — এমন অনুরোধেও। শুধু Skill খোঁজা/রাউটিংয়ের জন্য পরিবর্তে skill-finder, ল্যান্ডস্কেপ অডিটের জন্য skill-explorer ব্যবহার করুন।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: bn
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 1e6dace03eb8afc639fa08debace08a61441912a22399c11a49f7fe6e7dc3ecb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:12.458049+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## উৎস ও সিদ্ধান্ত (Fork বনাম নিজস্ব তৈরি)

**সিদ্ধান্ত: নিজস্ব তৈরি, Fork নয়।** কারণটি যাতে হারিয়ে না যায়:

- `skill-creator` (Anthropic, Marketplace `claude-plugins-official`) **Apache-2.0** লাইসেন্সপ্রাপ্ত (ক্লোনে LICENSE-পাঠ পড়া ও যাচাই করা হয়েছে, 2026-08-24) — একটি Fork আইনগতভাবে নিরাপদভাবে সম্ভব এবং রিপোজিটরিতে অন্যত্র ইতিমধ্যে এটি প্রতিষ্ঠিত প্যাটার্ন (`skills/third-party/grilling`)।
- তবে একটি Fork মূলের সম্পূর্ণ মূল্যায়ন/বেঞ্চমার্ক যন্ত্রপাতি সঙ্গে টেনে আনত (`agents/{analyzer,comparator,grader}.md`, `eval-viewer/`, 7টি Script, 485-লাইনের SKILL.md) — যে সক্ষমতা ইতিমধ্যে বিদ্যমান এবং সরাসরি আহ্বানযোগ্য (`Skill: skill-creator:skill-creator`)। `.PLUGINS/CLAUDE.md`-এর নিয়ম 4 ("পুনর্নির্মাণের আগে সক্ষমতা যাচাই করো") এবং P10 প্যাটার্ন ("দুটি সুইচ, যা কেউ তুলনা করে না") অনুযায়ী এটি হতো নকল, সম্প্রসারণ নয়।
- প্রকৃত ঘাটতি **সম্পূর্ণভাবে ellmos-নির্দিষ্ট** এবং মূলের কাছে মূলত অজানা: হাউস-ফ্রন্টম্যাটার (`templates/SKILL.md`), `docs/CONVENTIONS.md`, অ্যানবিটার/ব্যবহারকারী/ellmos-নিরপেক্ষতা ellmos-সংবেদনশীলতার সঙ্গে, `grounding-seed`-সংযোগ, ভেন্ডর-সচেতনতা, স্ব-হালনাগাদ।
- এই Skill-এ **কোনো Anthropic-পাঠ নেই** (সর্বত্র নিজস্ব শব্দচয়ন) — তাই পরিবর্তনের জন্য Apache-2.0 অ্যাট্রিবিউশন বাধ্যবাধকতাও সৃষ্টি করে না। এটি মূলকে কপি না করে **সংযুক্ত** করে: এটি একই সঙ্গে আইনগতভাবে সবচেয়ে পরিষ্কার এবং রক্ষণাবেক্ষণে সবচেয়ে কম খরচের পথ।

## কখন সক্রিয় হবে

- "একটি Skill তৈরি করো X-এর জন্য", "নতুন Skill বানাও", "skill-creator ব্যবহার করো"
- "এই Skill-টিকে ellmos-সামঞ্জস্যপূর্ণ করো", "Skill-কে হাউস-মানদণ্ডে পুনর্গঠন করো"
- যখনই **গন্তব্য** এই ইকোসিস্টেমের `.AI/.SKILLS/skills/…` (বা এর ক্যানোনিকাল Plan-D ক্লোন) এর একটি Skill — ইকোসিস্টেম-বহির্ভূত সাধারণ অনুরোধে ("এখানে সম্পর্কহীন যেকোনো Claude-Skill বানাও") নয়।

## কার্যপ্রণালী

### ধাপ 1 — ইন্টারভিউ/খসড়া/মূল্যায়ন অর্পণ

অফিসিয়াল `Skill: skill-creator:skill-creator` আহ্বান করো: উদ্দেশ্য স্পষ্টকরণ, SKILL.md-কাঠামোর খসড়া, পরীক্ষার ক্ষেত্রসমূহ, মূল্যায়ন-লুপ, বিবরণ-অপ্টিমাইজেশন (`scripts/improve_description.py`)। **নতুন করে উদ্ভাবন করো না** — এই অংশটি সাধারণ এবং মূলে ইতিমধ্যে ভালোভাবে সমাধান করা।

### ধাপ 2 — ellmos হাউস-স্ক্যাফোল্ড স্থাপন (বাধ্যতামূলক, মূল ফরম্যাটের সংযোজন হিসেবে)

মূল দ্বারা তৈরি SKILL.md-এ `.SKILLS/templates/SKILL.md`-এর নয়টি হাউস-ক্ষেত্র যোগ করো (ধরন অনুযায়ী `AGENT.md`/`WORKFLOW.md`/`PROMPT.md`)। আগে ক্যাটাগরি-ফোল্ডার, Flat-নিয়ম (<5 ফাইল হলে সমতল), সংস্করণ-রীতি (SemVer: MAJOR/MINOR/PATCH) এবং বহুভাষিকতা-সেট (Core: DE+EN বাধ্যতামূলক) জানতে `.SKILLS/docs/CONVENTIONS.md` পড়ো। **`visibility` সর্বদা `private-only`-এ শুরু হয়** — প্রকাশ একটি পরবর্তী, যাচাইকৃত ব্যবহারকারী-সিদ্ধান্ত (`.AI/VISIBILITY-POLICY.md`), কখনোই ডিফল্ট নয়। এই ক্ষেত্রগুলো Anthropic-ফরম্যাটের সঙ্গে সম্পূর্ণ **সংযোজন** (`name`/`description`-এর পাশে অতিরিক্ত YAML-কী) — এভাবে তৈরি প্রতিটি Skill সম্পূর্ণ `anthropic_compatible: true` থাকে।

### ধাপ 3 — নীতি প্রয়োগ: অ্যানবিটার-নিরপেক্ষ, ব্যবহারকারী-নিরপেক্ষ, ellmos-নিরপেক্ষ-কিন্তু-ellmos-সংবেদনশীল

পূর্ণ পাঠ + কোড-প্যাটার্ন: `references/ELLMOS-PRINCIPLES.md`। সংক্ষেপে: উৎপাদিত Skill-কে **একাই চলতে সক্ষম** হতে হবে (যা প্রয়োজন সব সঙ্গে আনে) এবং **একই সঙ্গে** ellmos-উপাদান উপস্থিত থাকলে সেগুলো ব্যবহার করতে হবে — এটি রানটাইমে নিজে সিদ্ধান্ত নেয়, কখনোই হার্ডকোড করা হয় না। এটিই ঠিক সেই প্যাটার্ন যা `grounding-seed` ইতিমধ্যে সরবরাহ করে (README: "cultivated landscape, not wildflower" / "viable alone, more productive together") — **কোনো দ্বিতীয় শনাক্তকরণ-প্রক্রিয়া উদ্ভাবিত হয় না**, এই Skill উৎপাদিত Skill-গুলোকে নিয়মিতভাবে `grounding_seed.detect_ecosystem()`-এর দিকে নির্দেশ করে।

### ধাপ 4 — config.json + connections.json সরবরাহ

`grounding-seed` ইতিমধ্যে একটি Python-প্যাকেজ হিসেবে আমদানিযোগ্য (2026-08-24-এ যাচাই করা: `import grounding_seed` স্থানীয়ভাবে ক্লোন করা `grounding-seed`-সোর্স-ট্রিতে সফলভাবে সমাধান হয় — Plan-D ক্লোন) — এটি **ক্যানোনিকাল সংযোগ-বিন্দু**, নতুন ফাইল উদ্ভাবন নয়। বাহ্যিক প্রয়োজনযুক্ত প্রতিটি উৎপাদিত Skill-এর জন্য (প্রোগ্রাম, সেবা, সরবরাহকারী):

- **`config.json`** — Skill-নিজস্ব সেটিংস (টেমপ্লেট: `templates/skill-config.template.json`)। `grounding_seed.store.LocalStore(root)` ডিফল্টভাবে এই ফাইলনামটি তার ভূমিকা-সংরক্ষণে ব্যবহার করে — তাই একটি উৎপাদিত Skill হয় তার নিজের `config.json`-কে `LocalStore`-ব্যাকএন্ড হিসেবে ব্যবহার করতে পারে, অথবা ভূমিকার পাশাপাশি বিশুদ্ধ আচরণ-সেটিংস প্রয়োজন হলে আলাদা রাখতে পারে (তখন দ্বিতীয় `LocalStore(root, filename="connections.json")`-ইনস্ট্যান্স)।
- **`connections.json`** — প্রকৃতপক্ষে **সমাধানকৃত** বাহ্যিক সংযোগ-বিন্দুসমূহ (কোন প্রোগ্রাম/সেবা পাওয়া গেছে, কখন থেকে, কোন উৎস থেকে) — টেমপ্লেট: `templates/skill-connections.template.json`, স্কিমা `ellmos.source-resolver.user-config.v1` (`source-resolver`-এর সঙ্গে অভিন্ন, grounding-seed-README অনুযায়ী ইচ্ছাকৃতভাবে তা বেছে নেওয়া হয়েছে যাতে পরবর্তীতে প্রকৃত `source-resolver`-তে স্থানান্তর ক্ষতিহীন হয় — সেখানে `migration.py` দেখো)।

বিস্তারিত, CLI এবং কোড-উদাহরণ: `references/ELLMOS-PRINCIPLES.md`-এর "Docking" বিভাগ।

### ধাপ 5 — অ্যানবিটার-/ভেন্ডর-সচেতনতা যুক্ত করো

পূর্ণ পাঠ: `references/VENDOR-AWARENESS.md`। সংক্ষেপে: উৎপাদিত Skill-এ একটি "সরবরাহকারী ও বিকল্পসমূহ" বিভাগ যোগ হয়, যা (ক) বিষয়ের অত্যাধুনিক সরবরাহকারী/গুলো উল্লেখ করে (যেমন TTS-এর জন্য ElevenLabs), (খ) অন্তত একটি বিকল্প সরবরাহকারী, (গ) **ellmos-নিজস্ব উপাদানসমূহ স্পষ্টভাবে সমমানের প্রার্থী হিসেবে** তালিকাভুক্ত করে যখন সেগুলো বিষয়টি ঢাকে (যেমন ElevenLabs-এর পরিবর্তে বা পাশাপাশি `ellmos-voice-io`) — এবং উপযুক্ত ব্যবহারকারী-প্রয়োজনে ইনস্টলেশন/স্থানান্তর **প্রস্তাব করে**, নীরবে ধরে না নিয়ে। "সিস্টেমে কী আছে" তার ভিত্তি: `grounding_seed.scan.scan_resources([...])` (যাচাই করে `shutil.which`) এবং ellmos-প্রার্থীদের জন্য `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md`।

### ধাপ 6 — স্ব-হালনাগাদ স্থাপন

পূর্ণ পাঠ: `references/SELF-UPDATE.md`। সংক্ষেপে: প্রতিটি উৎপাদিত Skill-এ একটি "স্ব-হালনাগাদ" বিভাগ যোগ হয়, যা (ক) অত্যাধুনিক অবস্থায় থাকতে পর্যায়ক্রমে একটি সংক্ষিপ্ত ওয়েব-অনুসন্ধান প্রস্তাব করে, (খ) সংশ্লিষ্ট Skill/ওয়ার্কফ্লো চেনে এবং উপযুক্ত হতে পারে এমন নতুন বিকল্পের নাম দেয়, (গ) একটি ছোট শিক্ষা-JSON রাখে (টেমপ্লেট: `templates/skill-connections.template.json`, ক্ষেত্র `notizen`/`gelernt`), যা ellmos-মেমরি-উপাদান (USMC/Gardener) উপস্থিত থাকলে স্থানীয়ভাবে না বেড়ে সেখানে স্থানান্তর করা যায় — এখানেও: শনাক্ত করো, হার্ডওয়্যার করো না (`grounding_seed.detect_ecosystem()`)।

### ধাপ 6b — শিক্ষা-চুক্তি + usecase-কভারেজ স্থাপন (পুনঃব্যবহারযোগ্য প্যাটার্ন)

পূর্ণ পাঠ: `references/LEARNING-CONTRACT-AND-COVERAGE.md`। সংক্ষেপে: শুধু এই Skill নয়, **এটি উৎপাদিত প্রতিটি Skill**-এ একটি ছোট, পুনঃব্যবহারযোগ্য শিক্ষা-/কভারেজ ফাইল-সেট থাকে — প্রতিষ্ঠিত মানদণ্ডের বিপরীতে যাচাইকৃত, কোনো সমান্তরাল মানদণ্ড নয়:

- `evals/evals.json` — **পুনঃব্যবহার করো**, নকল নয়: এটি লেখক-খসড়া পরীক্ষার ক্ষেত্রের জন্য ইতিমধ্যে skill-creator-মানদণ্ড।
- `user-usecases.json` — ব্যবহারকারী প্রকৃতপক্ষে যে ব্যবহার-ক্ষেত্রগুলো এনেছে, `evals.json`-এর সঙ্গে আকারে অভিন্ন (টেমপ্লেট: `templates/user-usecases.template.json`)।
- `usecase-gaps.json` — মিল: কোন ব্যবহারকারী-usecase অপরীক্ষিত/অনাবৃত (টেমপ্লেট: `templates/usecase-gaps.template.json`)।
- `known-providers-and-abilities.json` — প্রতি ভূমিকায় পরিচিত সরবরাহকারীর প্রার্থী-স্থান, ক্ষেত্রগুলো A2A/`AgentSkill` (id/name/description/tags)-এর সঙ্গে সংগতিপূর্ণ, উদ্ভাবিত নয় (টেমপ্লেট: `templates/known-providers-and-abilities.template.json`)।
- `gap-closing-analysis.json` — প্রতিটি ঘাটতির কাঠামোগত সমাধান-পথ (ellmos-মডিউল, ellmos-বান্ডেল, বহিরাগত মডিউল, নতুন নির্মাণ) — `grading.json.eval_feedback`-এর নকল নয় (টেমপ্লেট: `templates/gap-closing-analysis.template.json`)।
- `config.json` ক্ষেত্র `lernvertrag` — আচরণ-কোড (সেরা বিকল্প বেছে নেওয়া, **ব্যবহারকারী রাজা**, কখনো নিজে থেকে ইনস্টল না করা, হালনাগাদ-ব্যবধান) — ইচ্ছাকৃতভাবে `config.json`-এর সম্প্রসারণ, সপ্তম ফাইল নয়।

স্কিমা: `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — `skill-v1.schema.json`-এর মতো একই হাউস-রীতি। `grounding-seed` এই ফাইল-সেটের জন্য যাচাই করা হয়েছে এবং ইচ্ছাকৃতভাবে **সম্প্রসারিত করা হয়নি** (যুক্তি `LEARNING-CONTRACT-AND-COVERAGE.md`-এ) — শুধু `connections.json` তার অংশ থাকে।

### ধাপ 7 — নিবন্ধন, পরীক্ষা, কমিট

- `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md` অনুযায়ী ক্যাটাগরি-ফোল্ডার বেছে নাও; সন্দেহ হলে `skill-finder` বা `controlcenter_find_skill`কে জিজ্ঞাসা করো যে একটি পরিবার আগে থেকেই আছে কিনা।
- কমিট করার আগে `testing/` (privacy_gate + মেটাডেটা-পরীক্ষা) চালাও।
- Registry-ফাইল (`registry/components.json`, `SKILLS-MAP.md`, `llms.txt`) **হাতে সম্পাদনা করো না** — সেগুলো উৎপন্ন হয় (`build_public_registry.py`, `build_skills_map.py`, `catalog.py`)। ক্যানোনিকাল ক্লোনে যদি এখন একটি অন্যের, অ-কমিটকৃত সেশন চলে, তবে বিশ্বব্যাপী পুনরুৎপাদন করো না (এটি অন্যের ও নিজের পরিবর্তন একটি ফাইলে মিশিয়ে দেয়) — বরং নতুন Skill-ফোল্ডার আলাদাভাবে কমিট করো এবং Registry-পুনরুৎপাদন পরবর্তী পরিষ্কার চালানোর (`skill-register-care`) ওপর ছেড়ে দাও।
- `git commit -- skills/<kategorie>/<name>/` — শুধু নিজের, নতুন পথগুলো।

## Anthropic-ফরম্যাটের সঙ্গে সামঞ্জস্য

সব সংযোজিত ক্ষেত্র `name`/`description`-এর পাশে বিশুদ্ধ YAML-সম্প্রসারণ — এই ইকোসিস্টেম ছাড়া একটি স্ট্যান্ডার্ড Claude-Code এখনও শুধু `name`/`description` পড়ে এবং বাকিটা উপেক্ষা করে। `config.json`/`connections.json` ঐচ্ছিক Bundled Resources (`docs/CONVENTIONS.md`-এ যেমন নির্দিষ্ট), বাধ্যতামূলক নির্ভরতা নয় — এগুলো ছাড়া একটি Skill অপরিবর্তিতভাবে কাজ করে।

## সম্পর্কিত Skill

- `skill-creator:skill-creator` — সাধারণ ইন্টারভিউ/মূল্যায়ন লুপ (যাকে অর্পণ করা হয়, ধাপ 1)।
- `skill-finder` — বিদ্যমান নিজস্ব Skill-এর রাউটার (তৈরির আগে যাচাই করো: এটি কি আগে থেকেই আছে?)।
- `skill-explorer` — ল্যান্ডস্কেপ-অডিট + নতুন Skill/Plugin-এর জন্য ওয়েব-অনুসন্ধান (মেটা-স্তর: আমাদের Skill-*ভান্ডার*; এই Skill-টি বরং উৎপাদিত *প্রতিটি আলাদা* Skill-কে নিজে সরবরাহকারী-সচেতন করে)।
- `skill-family-care`, `skill-register-care` — তৈরির পরের রক্ষণাবেক্ষণ।
- `grounding-seed` (মডিউল, `.AI/.MODULES/.CONTROL/grounding-seed`) — প্রকৃত সংযোগ-/স্ব-সরবরাহ-যুক্তি, এখানে শুধু উল্লেখ, নকল নয়।

## পরিবর্তনের ইতিহাস

### 0.2.0 (2026-08-24)
- সংযোজন (Ticket T-20260824-218233618, পরিধি-সংযোজন): উৎপাদিত প্রতিটি Skill-এর জন্য পুনঃব্যবহারযোগ্য শিক্ষা-/কভারেজ প্যাটার্ন যুক্ত — `user-usecases.json`, `usecase-gaps.json`, `known-providers-and-abilities.json`, `gap-closing-analysis.json` (নতুন হাউস-স্কিমা `.SKILLS/schemas/`-এ) এবং `config.json`-এ শিক্ষা-চুক্তি-ক্ষেত্র। `evals/evals.json` (skill-creator) ইচ্ছাকৃতভাবে নকলের বদলে পুনঃব্যবহার করা হয়েছে। `grounding-seed` যাচাই করা হয়েছে — সম্প্রসারণ প্রয়োজন নেই (যুক্তি `references/LEARNING-CONTRACT-AND-COVERAGE.md`-এ), তাই কোনো অনুসরণ-টিকিট নেই। সরবরাহকারী-ক্যাটালগের ক্ষেত্রনাম A2A-প্রোটোকল (`AgentSkill`)-এর সঙ্গে সংগতিপূর্ণ, নিজস্ব শব্দভান্ডার নয়।

### 0.1.0 (2026-08-24)
- প্রথম সংস্করণ। নিজস্ব তৈরি, Fork নয় — সিদ্ধান্ত নেওয়া ও যুক্তি দেওয়া হয়েছে (Ticket T-20260824-218233618)। সাধারণ Skill-তৈরি অর্পণ করা হয় `skill-creator:skill-creator`-এ; যোগ করা হয় হাউস-স্ক্যাফোল্ড, ellmos-নীতি, `grounding-seed`-সংযোগ (config.json/connections.json), ভেন্ডর-সচেতনতা এবং স্ব-হালনাগাদ।
