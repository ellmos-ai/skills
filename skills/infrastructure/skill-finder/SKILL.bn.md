---
name: skill-finder
version: 0.9.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-10-03
description: "নিজের স্থানীয় Skill-গুলোর জন্য সক্রিয় ফাইন্ডার/রাউটার (using-superpowers-এর অনুরূপ)। প্রতিটি অ-তুচ্ছ কাজের শুরুতে সর্বদা ব্যবহার করুন, যাচাই করতে যে কোনো user-Skill মেলে কিনা এবং সঠিক Skill-এ রাউট করতে। „কোন Skill মেলে\", „এর জন্য কি কোনো Skill আছে\", „skill খুঁজুন\" বা সাধারণভাবে এমন কাজের আগে সক্রিয় হয় যেখানে একটি স্থানীয় Skill ad-hoc কাজের চেয়ে ভালোভাবে সমাধান করে।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: bn
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
translated_from_sha256: 999cd705d5357d1c4244d420001f12dea37a1b2a9a204c49a7eadf18767228f7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="skill-finder banner">
# Skill-Finder

## নিয়মটি

যেকোনো অ-তুচ্ছ কাজের আগে প্রথমে পরীক্ষা করুন একটি স্থানীয় Skill সেটি ভালোভাবে সমাধান করে কিনা। সামান্যতম সন্দেহেও উপযুক্ত Skill লোড করুন এবং **তার Live-নির্দেশনা অনুসরণ করুন** (ফাইলটি পড়ুন, স্মৃতি থেকে কাজ করবেন না)। কোনো Skill প্রযোজ্য না হলে স্বাভাবিকভাবে এগিয়ে যান।

## পরিবার-রাউটিং

<!-- Generiert/aktualisiert aus SKILL-MAP.md + inventory_skills.py. Thema -> Familie -> Skill.
     Pflege: Subskill skill-family-care oder neuer skill-explorer-Audit-Lauf. Stand: 2026-06-17 -->

| বিষয় / উদ্দেশ্য | পরিবার | Skill(s) |
|-----------------|---------|----------|
| সমস্যা চিন্তা করা / বিশ্লেষণ | Denkwerkzeuge | `/structured-thinking` (চালায় `/think` → `/brainstorm` → `/decide`) |
| নতুন ধারণা / সৃজনশীলতা | Denkwerkzeuge | `/brainstorm` (বনাম `/think` বিশ্লেষণ, `/decide` নির্বাচন) |
| সিদ্ধান্তের স্তূপ | Denkwerkzeuge | `/decision-briefing` |
| কোন সিদ্ধান্ত কোনটির উপর নির্ভর করে / সুপারিশগুলো কি পরস্পরবিরোধী? | Denkwerkzeuge | `decision-path` (`/decision-path`; ASCII-নির্ভরতা গ্রাফ, কিছু সিদ্ধান্ত নেয় না) |
| সুপারিশকৃত সামগ্রিক বিকল্পটি একটি ধারণা-/বাস্তবায়ন-পাঠ্য হিসেবে অনুমোদন করানো | Denkwerkzeuge | `decision-draw` (`/decision-draw`; সামগ্রিক অনুমোদন, সংশোধন → পৃথক সিদ্ধান্ত) |
| অনুমোদিত ব্যবহারকারী-প্রোফাইল গড়া বা ব্যবহার করা | Multi-Agent | `build-your-users-mind` (গঠন) · `decision-avatar` (ব্যবহার) |
| Bug / পরীক্ষার ব্যর্থতা | Coding & Debugging | `/bugfix-protocol` (১টি Bug), `/bugsweep` (অনেকগুলো, রিলিজের আগে) |
| নতুন/বিদ্যমান প্রকল্প বা পাইপলাইন | Projekt/Pipeline | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Roblox-গেম | Game-Dev | `/rbx-dev` (→ `/rojo`, `/rbx-studio`, `/game-design`) |
| থেরাপি / পরামর্শ / সংকট | Therapie | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| উপস্থাপনা / Slides | Office | `/academic-pptx` (বিষয়বস্তু) + `/pptx` (ফাইল) |
| জটিল Multi-Agent কাজের আগে অর্কেস্ট্রেশন একসাথে সীমাবদ্ধ করা | Multi-Agent | `choose-your-orchestrator` (`/choose-your-orchestrator`) |
| নিশ্চিত Multi-Agent সমন্বয় চালানো | Multi-Agent | `orchestrator`, `/swarm-operations`, `/model-strategy` |
| আবেদন / আত্ম-ব্যবস্থাপনা | Persönlich | `/bewerbungsexperte`, `/selbstmanagement` |
| Skill তুলনা/পরিষ্কার/খোঁজা | System/Meta | `skill-explorer` (Audit/Explore), `code-skill-index` (তালিকা) |
| সিস্টেম সেটআপ / MCP সিঙ্ক / এজেন্ট সংযুক্ত করা | System/Meta | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| ফাইল-সরঞ্জাম | Utilities | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| চ্যাট-ইতিহাস → Skill সংরক্ষণ | System/Meta | `skill-extractor` (`/skill-extract`) |
| চ্যাট-ইতিহাস/বাহ্যিক Automation → স্বয়ংক্রিয়করণ | System/Meta | `workflow-extract` (`/automations-extract`) |
| বহু প্রকল্পজুড়ে পুনরাবৃত্ত পরীক্ষা | Coding & Debugging | `rotation-check` (Registry/Log-কাঠামো) |
| আটকে থাকা সমস্যা, ধারণা খনন | Denkwerkzeuge | `idea-mining` (বনাম `/brainstorm` = মুক্ত/বিস্তৃত) |
| DE/EN দস্তাবেজ-সংস্করণ সমান্তরাল রাখা | Utilities | `bilingual-doc-sync` |
| খুব সংঘাতপূর্ণ Merge / ভিন্নমুখী শাখা (main বনাম master) / পুরোনো PR | Coding & Debugging | `reissverschluss-merge` (`/reissverschluss-merge` · `/zipper-merge`; এস্কেলেশন: Merge-এর বদলে Rebuild) |
| লেখা থেকে AI-চিহ্ন/চ্যাট-অবশিষ্ট, AI-Disclosure | Utilities | `llm-text-hygiene` |
| নির্দেশে শর্ত/সময়/ক্রম („শুধু যখন", „ভোর ৬টা থেকে", „X শেষ হলেই") | Prozess | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |
| একটি ফোল্ডার থেকে নিয়মভিত্তিকভাবে ফাইল সংগ্রহ/সাজানো („X থেকে সবসময় Y নিয়ে Z-তে জমা করো", „ফোল্ডার স্বয়ংক্রিয়ভাবে সাজাও") | Utilities | `file-collect-sort-action` |
| App-/GUI-সিরিজ ব্যবহারকারীর সাথে একযোগে পরীক্ষা (লাইভ পরীক্ষা, প্রতিক্রিয়া সঙ্গে সঙ্গে মূল্যায়ন + মেরামত অর্পণ) | Coding & Debugging | `human-loop-audit` |
| সেশন শেষে প্রকল্প গুছিয়ে রাখা (Register সমাধান/সাজানো, দস্তাবেজ বাস্তব অবস্থায় আনা, Strays সরানো) | Coding & Debugging | `tidy-up` (`/tidy-up`; `work-autonomous`-স্তর-১ উৎস হিসেবে গণ্য) |
| নিয়ম-/স্মৃতি-ফাইল সংক্ষিপ্ত করা, বিষয়বস্তু না বদলে („CLAUDE.md অনেক বড়", „কেটে যাচ্ছে") | Utilities | `paveman` (নির্ধারক, কোনো মডেল-কল নেই; বনাম `knappform` = LLM-ভাষারীতি) |
| GitHub-এ Mermaid-ডায়াগ্রাম রেন্ডার হচ্ছে না („Unable to render rich display", „Schaltplan wird nicht angezeigt" / „স্কিমেটিক দেখানো হচ্ছে না"), সংগঠনজুড়ে Mermaid-ব্লক যাচাই | Coding & Debugging | `mermaid-lint` (ব্রাউজার ছাড়া প্রকৃত পার্সার + লাইভ পাতায় Readback) |
| মডেল-বাজেট, কোটা, ব্যয়বহুল Reviewer/Advisor সীমিত ব্যবহার | Multi-Agent | `budgetierung` (অ্যাকাউন্ট + আলোচনা; মডেল-নির্বাচন নিজে: `/model-strategy`) |

সম্পূর্ণ তালিকা: Skill `code-skill-index`।

## Red Flags (যুক্তিসঙ্গতকরণ, যার অর্থ STOP)

| চিন্তা | বাস্তবতা |
|---------|----------|
| „এটা শুধু একটা ছোট প্রশ্ন।" | প্রশ্নও কাজ — আগে Skill-পরীক্ষা। |
| „ধারণাটি আমি জানি।" | ধারণা জানা ≠ Skill ব্যবহার। Live-ফাইল পড়ুন। |
| „Skill-টি অতিরিক্ত।" | সহজ জিনিস জটিল হয়ে যায় — ব্যবহার করুন। |
| „আমি আগে নিজে অন্বেষণ করি।" | Skill বলে অন্বেষণ কীভাবে করতে হয়। আগে পরীক্ষা। |

## রক্ষণাবেক্ষণ

পরিবার পরিবর্তন হলে রাউটিং-সারণি হালনাগাদ করুন (উপ-Skill `skill-family-care` বা `skill-explorer` থেকে নতুন `inventory_skills.py`-রান)।

## Changelog

### 0.9.0 (2026-10-03)
- নতুন Skill `budgetierung`-এর জন্য রাউটিং-সারি (পরিবার Multi-Agent): মডেল-কোটা আলোচনা, পরিচালনা ও সমন্বয় — `model-strategy`-এর পরিপূরক হিসাবরক্ষণ (সেখানে থাকে, *কোন* মডেল মানায়; `budgetierung` নিয়ন্ত্রণ করে, *কতটা* তার)।

### 0.8.0 (2026-09-20)
- নতুন Skill `mermaid-lint`-এর জন্য রাউটিং-সারি যোগ (পরিবার Coding & Debugging): Mermaid-ডায়াগ্রাম, যেগুলো GitHub „Unable to render rich display" দিয়ে প্রত্যাখ্যান করে, এবং সব ```mermaid-ব্লকজুড়ে সংগঠনব্যাপী পরীক্ষা-রান।

### 0.7.0 (2026-08-20)
- জটিল Multi-Agent কাজের জন্য পূর্বসংযুক্ত সুপারিশ ও চুক্তি-সংলাপ হিসেবে `choose-your-orchestrator` যোগ; এর থেকে আলাদাভাবে `orchestrator`, `swarm-operations` ও `model-strategy`-এ কার্যকরকরণ-রাউটিং।

### 0.6.0 (2026-08-19)
- নতুন Skill paveman-এর জন্য রাউটিং-সারি („নিয়ম-/স্মৃতি-ফাইল সংক্ষিপ্ত করা, বিষয়বস্তু না বদলে"): ইতিমধ্যে ইনস্টল করা, নির্ধারক সংক্ষেপণ-মডিউল `paveman`-এর পাতলা র‍্যাপার (T-20260819-213392123); `knappform` থেকে পার্থক্য (LLM-ভাষারীতি বনাম ফাইল-সম্পাদনা)।

### 0.5.0 (2026-08-19)
- নতুন Skill tidy-up-এর জন্য রাউটিং-সারি („সেশন শেষে প্রকল্প গুছিয়ে রাখা": সক্রিয় প্রকল্পফোল্ডারের জন্য একবারের Tasksolver+Writer+Maintainer-রান; `/goal`-নির্মাণের জন্য `work-autonomous`-স্তর-১ উৎস হিসেবে গণ্য)।

### 0.4.0 (2026-08-18)
- নতুন Skill human-loop-audit-এর জন্য রাউটিং-সারি („App-/GUI-সিরিজ ব্যবহারকারীর সাথে একযোগে পরীক্ষা", সমান্তরাল মেরামত-অর্পণসহ Reißverschluss-Audit; একই নামের কিন্তু ভিন্ন বিষয়বস্তুর reissverschluss-merge থেকে পৃথক)।

### 0.3.0 (2026-08-18)
- নতুন Skill file-collect-sort-action-এর জন্য রাউটিং-সারি („ফাইল নিয়মভিত্তিকভাবে সংগ্রহ/সাজানো", T-20260818-916568570 থেকে স্থগিত f-csa-ট্রিগার-বাক্যের শনাক্তকরণ)।
- পরবর্তীতে যোগ: reissverschluss-merge-এর রাউটিং-সারি Skills-রেপোর উৎসে অনুপস্থিত ছিল (শুধু `~/.claude/skills/`-ডিপ্লয়মেন্টে ছিল) — সম্পাদনার সময় ড্রিফট লক্ষ্য করে এখানে পুনরুদ্ধার, যাতে ভবিষ্যৎ ডিপ্লয় তা মুছে না দেয়।
- `version:`-ক্ষেত্রটি আগে পৌঁছানো Changelog-অবস্থা (0.2.0)-এর সাথে মিলানো এবং 0.3.0 পর্যন্ত গণনা — আগে 0.1.0-এ থেমে ছিল।

### 0.2.0 (2026-07-03)
- নতুন Skill-গুলোর জন্য রাউটিং-সারি: skill-extractor, workflow-extract, rotation-check, idea-mining, bilingual-doc-sync (Codex-Automations-নিষ্কাশন)।

### 0.1.0 (2026-06-17)
- প্রাথমিক সংস্করণ। using-superpowers-এর অনুরূপ হিসেবে Audit-মোড ([F]) দ্বারা তৈরি। 2026-06-17-এর Audit থেকে রাউটিং-সারণি (10টি user-পরিবার)।
