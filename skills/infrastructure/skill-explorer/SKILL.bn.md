---
name: skill-explorer
version: 1.1.1
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-08-24
description: "নিজের Skill-ল্যান্ডস্কেপ পরিচালনা করে: বিদ্যমান skills সমীক্ষা ও তুলনা করে (Audit mode), নতুন skills/plugins-এর জন্য ওয়েব গবেষণা করে (Explore mode), এবং একই সাথে একটি মনোলিথ লোড না করে lean subskills (Skill-Finder, family umbrella, maintenance skills) তৈরি করার installer হিসেবে কাজ করে। \"compare/audit skills\", \"which skills are duplicated\", \"form skill families\", \"clean up/consolidate skills\", \"maintain the skill register\", \"find skills/plugins for topic X\", \"install new skills\", \"browse the skill marketplace\" বা `/skill-explorer`-এর জন্য এই skill ব্যবহার করুন। বাংলা ট্রিগার: \"skills তুলনা/audit করো\", \"কোন skills ডুপ্লিকেট\", \"skill families গঠন করো\", \"skills পরিষ্কার/একত্র করো\", \"skill register রক্ষণাবেক্ষণ করো\", \"বিষয় X-এর জন্য skills/plugins খোঁজো\", \"নতুন skills ইনস্টল করো\", \"skill marketplace ব্রাউজ করো\"। প্রতি family-এর জন্য একটি sub-report এবং একটি globally numbered decision list প্রদান করে; নিরাপত্তা পরীক্ষা ও স্পষ্ট অনুমোদনের পরেই install/uninstall করে।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: bn
status: active
visibility: public
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 290cc943766331f12d02c48949c72ba33065d7b80c835a1d9a3edfa08a17bf21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="skill-explorer banner">

# Skill-Explorer — Skill-ল্যান্ডস্কেপ পরিচালনা (Audit · Explore · Installer)

## উদ্দেশ্য

Skill-এর ভাণ্ডার বাড়ার সাথে সাথে ডুপ্লিকেট, অব্যবহৃত সম্পদ এবং অস্পষ্ট "কোনটির পরিবর্তে কোনটি"-পরিস্থিতি তৈরি হয় — আর বাইরে ক্রমাগত নতুন Skills/Plugins আসছে। `skill-explorer` একটি টুলে তিনটি ভূমিকা একত্র করে:

| ভূমিকা | এটি কী করে | বিস্তারিত |
| --- | --- | --- |
| **Audit-Modus** (ভিতরের দিকে) | সব Skills পর্যালোচনা, families-এ ক্লাস্টারিং, সক্ষমতা/নির্ভরতা/সম্পদ সংগ্রহ, প্রতি family-এর জন্য sub-report + সংখ্যাযুক্ত সুপারিশ | `references/audit-mode.md` |
| **Explore-Modus** (বাইরের দিকে) | একটি বিষয়ের জন্য ওয়েবে (Web/GitHub/Reddit, দ্বিভাষিক) নতুন Skills/Plugins খোঁজা, তুলনা করা, গেটেড ইনস্টল | `references/explore-mode.md` |
| **Installer** | Monolith-এর পরিবর্তে lean subskills *তৈরি* করা — Skill-Finder, Family-Umbrella, Maintenance-Skills | নিচে + `references/family-care.md` |

আহ্বান: `/skill-explorer` (ডিফল্ট হিসেবে Audit) বা "… বিষয় X-এর জন্য খুঁজুন" (Explore)। উভয় মোড একই Taxonomy (`references/clustering.md`), Reporting format (`references/report-format.md`) এবং Numbering scheme শেয়ার করে, যাতে user একটিমাত্র সংখ্যা-তালিকা দিয়ে উত্তর দিতে পারে।

## Installer-নীতি ও Persistence

নিজে monolithic হয়ে না বেড়ে, `skill-explorer` প্রয়োজনে lean, আলাদাভাবে লোড করা যায় এমন subskills *তৈরি* করে — ফলে কখনো একটি দীর্ঘ একক skill লোড করতে হয় না:

- **Skill-Finder** ([F]) — সক্রিয় finder/router, "using-superpowers" gatekeeper-এর মতো, যা প্রতিটি কাজের আগে register পড়ে এবং উপযুক্ত family-তে route করে (`references/skill-finder.md`, টেমপ্লেট `assets/skill-finder-template.md`)।
- **Family-Umbrella** (c1) — একটি meta-skill যে পুরো family জানে (`assets/family-umbrella-template.md`)।
- **Maintenance-Skills** ([P1] families, [P2] register) — families/register হালনাগাদ রাখে (`references/family-care.md`)।

সিদ্ধান্তগুলো `~/.claude/skills/skill-explorer/config.json`-এ persist করা হয় (`references/config.md`, টেমপ্লেট `assets/config.example.json`): শুরুতে পড়ুন (পরিচিত families/routers/তৈরি subskills), চালানোর পরে হালনাগাদ করুন — এভাবে re-run কিছু দ্বিতীয়বার তৈরি করে না।

## Branch-প্রক্রিয়া (তৃতীয় পক্ষের Skill মানিয়ে নেওয়া)

একটি read-only skill (plugin, আমদানিকৃত তৃতীয় পক্ষের) মূলটি পরিবর্তন না করেই মানিয়ে নেওয়া যায়: মূল directory সম্পূর্ণ কপি করা হয় (**Branch**); এরপর শুধু কপিটি সম্পাদনা করা হয়। Branch-এ চারটি বাধ্যতামূলক তথ্য থাকে: মূলের উল্লেখ, Branch-তারিখ, সম্পাদক ও কারণ। Branch মূলকে প্রতিস্থাপন করলে runtime-এর জন্য মূলটি deregistered হয় (`SKILL.md` → `CONTENT.md`) অথবা family-router Branch-এর দিকে নির্দেশ করে, যাতে প্রায় অভিন্ন দুটি skill সংঘাত না করে। তৃতীয় পক্ষের Branches **ব্যক্তিগত** থাকে — সেগুলো সর্বজনীন `.AI/.SKILLS` library-তে যায় না। বিস্তারিত: `references/skill-branching.md`।

## প্রক্রিয়া

1. **মোড বাছুন:** ভাণ্ডার দেখা/পরিষ্কার করা → Audit-Modus। বাইরে থেকে খোঁজা/ইনস্টল করা → Explore-Modus। (Explore আগের Audit/`config.json`-এর উপর ভিত্তি করে চলতে পারে।)
2. **Audit-Modus** (`references/audit-mode.md`): Inventory (script) → Family-Cluster → Sub-reports → **একটি globally সংখ্যাযুক্ত সিদ্ধান্ত-তালিকা** (a/b/c1/c2/c3, পাশাপাশি R/F/P1/P2)।
3. **Explore-Modus** (`references/explore-mode.md`): দ্বিভাষিক বহু-উৎস গবেষণা → প্রতি candidate-এ 3টি category → Impact simulation → সংখ্যাযুক্ত Install/Remove সুপারিশ।
4. **কার্যকর করা** শুধু user-এর সংখ্যা-নিশ্চিতকরণের পরে; Skill-সৃষ্টি/পরিবর্তন register করুন এবং `config.json` হালনাগাদ করুন।

## অপরিবর্তনীয় নিয়ম

- **Survey ≠ Mutation:** সব কিছু ক্লাস্টার করা যায়, কিন্তু সম্পাদনা শুধু **user-নিজের** Skills-এ; Plugin/তৃতীয় পক্ষের Skills read-only (কখনো header বা মুছে ফেলা নয়)। তৃতীয় পক্ষের skill মানিয়ে নিতে চাইলে বদলে একটি **Branch** (fork-কপি) তৈরি করা হয় — মূল অক্ষত থাকে, পরিবর্তন শুধু কপিতে হয় (→ `references/skill-branching.md`)।
- **Register বাড়ান, ডুপ্লিকেট করবেন না:** একটি Skill-register (Index + Family-Map + Index-Skill) থাকলে সেটি বাড়ান, চতুর্থ একটি তৈরি করবেন না।
- **নিরাপত্তা প্রধানত ম্যানুয়াল:** যেকোনো ইনস্টলের আগে মডেল নিজে Skill পড়ে বিচার করে; `scripts/scan_skill_security.py` শুধু জ্ঞাত সীমাবদ্ধতাসহ সহায়ক triage। কখনো auto-install নয়।
- **উৎস অনুযায়ী Registration:** user-authored → Library; তৃতীয় পক্ষ → বাহ্যিক path, **Library নয়**।

## অর্কেস্ট্রেশন (মডেল-নিরপেক্ষ)

Family sub-reports বা উৎস/ভাষাগুলো স্বাধীন কাজের পথ। প্ল্যাটফর্ম যদি orchestrator-এর চেয়ে সস্তা subagents দেয়, প্রতি family/উৎসের জন্য একটি subagent নিয়োগ করুন এবং orchestrator হিসেবে শুধু একত্র ও যাচাই করুন (বিশেষজ্ঞ-ঝাঁক)। অন্যথায় নিজে ধারাবাহিকভাবে করুন।

## সম্পদ

- **মোড:** `references/audit-mode.md`, `references/explore-mode.md`
- **শেয়ার্ড:** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Audit:** `references/family-care.md`, `references/skill-finder.md`
- **Explore:** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Branch:** `references/skill-branching.md`
- **Scripts:** `scripts/inventory_skills.py` (Inventory), `scripts/inject_family_header.py` (Header-Router), `scripts/scan_skill_security.py` (Security-Triage)
- **টেমপ্লেট:** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`, `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Changelog

### 1.1.1 (2026-08-24)
- Inventory helper এখন পুরোনো, এক-লাইনে serialized `dependencies` mappings-ও গ্রহণ করে এবং দূষিত মানগুলো ত্রুটি-সহনশীলভাবে সামলায়, পুরো Audit বাতিল না করে। এর সমাপ্তি বার্তাটিও Windows console-এর সাথে সামঞ্জস্যপূর্ণ।

### 1.1.0 (2026-06-17)
- Branch-প্রক্রিয়া যোগ করা হয়েছে: তৃতীয় পক্ষের/read-only Skills fork-কপি (Branch) দিয়ে মানিয়ে নেওয়া যায় — মূলের উল্লেখ, তারিখ, সম্পাদক ও কারণসহ; মূল অক্ষত থাকে। "Survey ≠ Mutation" নিয়মে Branch-পথ যুক্ত হয়েছে। নতুন বিভাগ `## Branch-Mechanismus`। নতুন: `references/skill-branching.md`, `assets/branch-header.example.md`।

### 1.0.0 (2026-06-17)
- প্রাথমিক সংস্করণ। ভাণ্ডার-Audit (family-ক্লাস্টারিং, সংখ্যাযুক্ত সিদ্ধান্ত) এবং ওয়েব-গবেষণা (security-triage সহ গেটেড ইনস্টল) একটি installer-এ একত্র করে, যা lean subskills তৈরি করে।
