---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "automation-self-care কে Letter Hooks, Preflight-Bootloader, ডকুমেন্ট-ট্র্যাভার্সাল নিয়ম এবং স্ব-নিরাময়ী প্রম্পট-কনটেক্সট সমৃদ্ধকরণ দিয়ে প্রসারিত করে, যা নেটিভ, ইভেন্ট-চালিত JSON লাইফসাইকেল হুক না থাকা AI এজেন্ট ও CLI-এর জন্য (যেমন Antigravity / Gemini CLI)। যখন কোনো এজেন্টকে Preflight নিয়ম ইনজেক্ট করতে, কাজ শুরুর আগে Memory/Gardener অনুসন্ধান করতে, ডিরেক্টরি-ডকুমেন্ট পাঠের কৌশল (CLAUDE.md / AGENTS.md) বাধ্যতামূলক করতে, অথবা Sidecar-টাস্কগুলোকে গতিশীলভাবে Skills ও নিরাপত্তা প্রোটোকলে রাউট করতে হয়, তখন এটি ব্যবহার করুন।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: bn
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: cb03d9a06cc52ced2695c952c855b3d57c168dc5b0a9ad1c412e72da13de1765
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="letter-hooker banner">

# Letter-Hooker (প্রম্পট-লেভেল Preflight ও Governance Engine)

**Letter-Hooker** স্কিল `automation-self-care`-কে এমন AI এজেন্ট ফ্রেমওয়ার্কের (যেমন **Antigravity / Gemini CLI**) জন্য প্রসারিত করে, যাদের নেটিভ, ইভেন্ট-চালিত JSON লাইফসাইকেল হুক লোডার নেই (যেমন `~/.claude/settings.json` বা `~/.codex/hooks.json`)।

প্রতি-কী-প্রেস প্যাসিভ হুকের উপর নির্ভর না করে, `letter-hooker` নির্ধারিত টাস্ক ও Maintainer-স্ক্রিপ্ট (`agy_kontext_and_workflow_loader.py`) এর মাধ্যমে একটি **সক্রিয় প্রম্পট-লেভেল Preflight-Bootloader ও Letter-Hook Injection Loop** পরিচালনা করে।

---

## মূল সক্ষমতা

1. **Preflight-Bootloader ও ডকুমেন্ট-ট্র্যাভার্সাল নিয়ম**:
   - **উর্ধ্ব ও নিম্ন অনুসন্ধান**: এজেন্টদের বর্তমান ওয়ার্কিং ডিরেক্টরি স্তরে `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md` এবং `README.md` পরীক্ষা করার কঠোর নির্দেশনা বাধ্যতামূলক করে। না পাওয়া গেলে খুঁজে পাওয়া পর্যন্ত উপরের দিকে ট্র্যাভার্স করে; তারপর নিচের দিকে পরীক্ষা করে।
   - **Memory ও Gardener Preflight**: ধ্বংসাত্মক বা জটিল পরিবর্তন কার্যকর করার আগে `gardener` ও `memoryhooker`-এ বাধ্যতামূলক Preflight কোয়েরি করে।

2. **Letter-Hooks ক্যাটালগ ও রেফারেন্স লিংক**:
   - `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`-এর অধীনে মডুলার `.md` নির্দেশনা ফাইল।
   - `sidecar.json`-প্রম্পট টেক্সটে সরাসরি স্পষ্ট `file://` লিংক ইনজেক্ট করে, যাতে আহ্বানের সময় এজেন্ট সঠিক নিরাপত্তা ও ওয়ার্কফ্লো প্রোটোকল পড়ে।

3. **দৈনিক কীওয়ার্ড তালিকা ও স্ব-নিরাময়ী প্রম্পট সমৃদ্ধকরণ**:
   - সক্রিয়/Standby টাস্ক থেকে একটি দৈনিক `STICHWORTLISTE.json` বজায় রাখে।
   - এক্সিকিউশন লগ (`AUTOMATIONS-MEMORY.md`) বিশ্লেষণ করে ত্রুটির প্যাটার্ন (অনুপস্থিত কনটেক্সট, অনুপস্থিত ওয়ার্কফ্লো নির্দেশনা, অবৈধ পাথ) খুঁজে বের করে এবং টাস্ক-প্রম্পট গতিশীলভাবে প্যাচ করে।

4. **Skill ও Persona রাউটিং**:
   - টাস্কের কীওয়ার্ড পরীক্ষা করে সেগুলোকে উপযুক্ত `.SKILLS`-এ ম্যাপ করে (যেমন `infrastructure/condition`, `semantic-persona-routing`, `orchestrator`, `think`, `decide`)।

---

## গুরুত্বপূর্ণ Letter Hooks

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](hooks/path_validation_and_authority.md)

---

## ওয়ার্কফ্লো ইন্টিগ্রেশন

```bash
# Letter-Hooker-Wartungs-Engine ausführen
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **Sidecar স্ক্যান করা**: `~/.gemini/config/sidecars/`-এর সমস্ত `sidecar.json`-প্রম্পট টেক্সট পড়া।
2. **কীওয়ার্ড তালিকা হালনাগাদ করা**: পরিভাষা বের করে `.SYNC/STICHWORTLISTE.json`-এ সংরক্ষণ করা।
3. **Letter Hooks ইনজেক্ট করা**: প্রম্পটে Bootloader নিয়ম ও `file://` রেফারেন্স লিংক যুক্ত করা।
4. **ফলাফল লগ করা**: `ANTIGRAVITY-LOG.txt` ও `ANTIGRAVITY-REGISTRY.md`-এ হালনাগাদ রেকর্ড করা।
