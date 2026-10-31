---
name: metacognitive-injectors
version: 1.4.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-30
updated: 2026-07-30
description: "মেটাকগনিটিভ ইনজেক্টর ও স্ব-কথোপকথন কৌশল (Self-Talk, Metacognitive Auditing, Evaluator Hooks, Pre-Flight Checklists, State Persistence & Personas)। এতে সমন্বিত রয়েছে সক্রিয় তথ্যানুসন্ধান (সিস্টেম মেমোরি Gardener ও USMC), Rehearsal (সক্রিয় পুনরুদ্ধার ও পুনরাবৃত্তি), Baddeleys ওয়ার্কিং মেমোরি (State + Hooks), Miyake নির্বাহী ফাংশন এবং CBT/ACT থেরাপিউটিক কৌশল।"
standalone: true
anthropic_compatible: true
bach_compatible: true
category: infrastructure
tags: [metacognition, self-talk, metacognitive-injectors, evaluator-hook, quality-gate, multi-agent, auditing, pre-flight-checklist, working-memory, active-retrieval, rehearsal, gardener, usmc, state-persistence, hooks, survival-routing, persona-routing]
aliases: [self-talk, metacognitive-self-talk, metacognitive-auditing, evaluator-hook, preflight-checklist, inner-speech, active-retrieval, rehearsal]
language: bn
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
translated_from_sha256: e692cdc2b2eb66f784fc25d0f36596e1342e828e67d91bc8aeca5eb3f456d8c2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.028075+00:00"
---
<img src="banner.png" width="100%" alt="metacognitive-injectors banner">

# মেটাকগনিটিভ ইনজেক্টর (Metacognitive-Injectors, Active Retrieval & Memory Search)

**Metacognitive-Injectors** দক্ষতাটি (যা **`self-talk`**, **`metacognitive-auditing`**, **`evaluator-hook`**, **`preflight-checklist`**, **`inner-speech`**, **`active-retrieval`** এবং **`rehearsal`** নামেও পরিচিত) AI এজেন্টদের জন্য জ্ঞানীয় মনোবিজ্ঞান ও থেরাপি-ভিত্তিক স্ব-পর্যবেক্ষণ কৌশল প্রতিষ্ঠা করে।

---

## ১. সক্রিয় তথ্যানুসন্ধান ও সিস্টেম মেমোরি (Gardener ও USMC)

### ক. সিস্টেম মেমোরিতে সক্রিয় তথ্যানুসন্ধান
- অনুমান বা তড়িঘড়ি দাবি করার আগে সিস্টেম মেমোরিতে **সক্রিয়ভাবে অনুসন্ধান করুন**:
  1. **Gardener DB (`gardener.py` / `hb_garden_*`):** পর্যবেক্ষিত শিক্ষণ প্রভাব, ব্যবহারকারীর সিদ্ধান্ত ও পথ-চুক্তি অনুসন্ধান করে (যেমন `Gardener().find("companion")`)।
  2. **USMC SQLite DB (`usmc_memory.db`):** সংরক্ষিত তথ্য, শিক্ষা ও সেশনের ইতিহাসের অনুসন্ধান করে।
  3. **কেন্দ্রীয় নিয়ম ফাইল (`CLAUDE.md`, `.SYNC`, `AGENTS.md`):** বিদ্যমান কনভেনশন ও পথ নির্দেশনা পড়ে।

### খ. Rehearsal: সক্রিয় পুনরুদ্ধার ও পুনরাবৃত্তি (Retrieval Practice)
- **সাবভোকাল Rehearsal লুপ (ধ্বনিগত লুপ):**
  তথ্য শুধু নিষ্ক্রিয়ভাবে পড়বেন না, বরং কার্যকর করার আগে **সক্রিয়ভাবে পুনরুদ্ধার করুন, ওয়ার্কিং মেমোরিতে পুনর্গঠন করুন এবং বাস্তবতার সাথে মিলিয়ে দেখুন**।
  - *"আমি কি স্ক্রিপ্টের সঠিক পথটি মনে রেখে পুনরুদ্ধার করেছি?"*
  - *"কমান্ড সিনট্যাক্স কি সিস্টেম মেমোরিতে রাখা উদাহরণের সাথে মিলছে?"*

---

## ২. জ্ঞানীয় বিজ্ঞান ও থেরাপিউটিক ভিত্তি

### ক. ওয়ার্কিং মেমোরি = State + Hooks (Baddeley ও Cowan)
- **State (মেমোরির বিষয়বস্তু):** প্রতিটি উপধাপের পর ক্ষণস্থায়ী মধ্যবর্তী অবস্থা SQLite টেবিলে (`usmc_memory.db`), `AUTOMATIONS-MEMORY.md` বা স্থানীয় State বাফারে সংরক্ষণ করে।
- **Hooks (নিয়ন্ত্রণ যন্ত্রাংশ):** Preflight বুটলোডার, Letter-Hooks এবং PreToolUse/PostToolUse Evaluator-Hooks।

### খ. Miyake-এর নির্বাহী ফাংশন (Command & Control)
1. **Inhibition (আবেগ নিয়ন্ত্রণ):** তড়িঘড়ি সাইন-অফ ও কল্পিত সাফল্যবার্তা দমন করে।
2. **Shifting (জ্ঞানীয় নমনীয়তা):** বাধার মুখে স্বয়ংক্রিয়ভাবে Survival-Routing, Persona মোড বা বিকল্প সমাধান পথে স্থানান্তর করে।
3. **Updating (ওয়ার্কিং মেমোরি আপডেট):** কার্যকর অবস্থা ক্রমাগত হালনাগাদ করে।

### গ. থেরাপিউটিক প্রেরণা (CBT, ACT ও সমাধান-কেন্দ্রিক থেরাপি)
- **CBT জ্ঞানীয় পুনর্গঠন:** ত্রুটিকে মূল্যবান রোগনির্ণয়মূলক তথ্য হিসেবে পুনঃকাঠামোগতকরণ।
- **ACT জ্ঞানীয় বিচ্ছিন্নতা ও গ্রহণযোগ্যতা:** নিজের অনিশ্চয়তাকে একটি অবস্থা হিসেবে মেনে নেওয়া ও প্রকাশ করা।
- **আচরণগত পরীক্ষা:** প্রকৃত অভিজ্ঞতামূলক প্রমাণ সংগ্রহের জন্য Smoke-Test/Dry-Run চালানো।

---

## ৩. মাল্টি-মডেল ফলব্যাক চেইন ও Codex Companion ইন্টারফেস

| অগ্রাধিকার | পরামর্শদাতা / পরীক্ষক | ইন্টারফেস / কমান্ড | কার্যকারিতা / নিয়ম |
| :--- | :--- | :--- | :--- |
| **প্রাথমিক (1)** | **Gemini Subagent** | `invoke_subagent` / `define_subagent` | নিয়মিত পরীক্ষার জন্য দ্রুত অভ্যন্তরীণ পরীক্ষক। |
| **দ্বিতীয়িক (2)** | **Codex Companion (Native)** | `node "<USER_HOME>\.codex\.tmp\marketplaces\openai-codex\plugins\codex\scripts\codex-companion.mjs" task "..."` | পরীক্ষা ও **`/goal`-গ্রহণ**-এর জন্য নেটিভ Codex Companion। |
| **তৃতীয়িক (3)** | **Codex CLI Direct** | `codex exec --skip-git-repo-check` | Codex CLI-এর সরাসরি আহ্বান। |
| **চতুর্থিক (4)** | **Claude CLI / Swarm** | `claude -p ...` / `hb_swarm_consensus` | টোকেন সীমায় তৃতীয় মতামত। |

---

## ৪. ক্ষেত্র-নির্দিষ্ট প্রম্পট ইনজেকশন (Tailored Injection Pattern)

ইনজেক্টর (`agy_metacognitive_prompt_injector.py`) ক্ষেত্র অনুযায়ী উপযুক্ত কৌশল নির্বাচন করে:

- **মূল ব্লক (সমস্ত Sidecar):** বিরোধী-ফাঁপা সম্পাদন, বহিরাগত মডেল দ্বারা `/goal`-গ্রহণ, সক্রিয় তথ্যানুসন্ধান (Gardener/USMC), Rehearsal (সক্রিয় পুনরুদ্ধার), Pre-Flight Checklist।
- **গবেষণা Sidecar (`research-*`):** *প্রমাণভিত্তিক গবেষণা (অনুসন্ধানের প্রমাণ ছাড়া কোনো উৎস নয়)*, *CBT পুনঃকাঠামো ও জ্ঞানীয় বিচ্ছিন্নতা (অ-ফলাফলকে একটি অনুসন্ধান হিসেবে গণ্য)* দ্বারা সম্প্রসারিত।
- **সফটওয়্যার-/Roblox Sidecar (`software-*`, `roblox-*`):** *ধ্বনিগত লুপ ও Rehearsal*, *ওয়ার্কিং মেমোরি স্টেট পারসিস্টেন্স*, *Survival-Routing* দ্বারা সম্প্রসারিত।
- **Maintainer ও Generalist (`maintainer-*`, `generalist-*`):** *সক্রিয় তথ্যানুসন্ধান*, *Skill-Finder* ও *Memory Hooks* দ্বারা সম্প্রসারিত।
