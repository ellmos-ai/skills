---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "এই রক্ষণাবেক্ষণ-স্কিল স্কিল-পরিবারগুলো আপ-টু-ডেট রাখে, পুরো skill-explorer-অডিট না চালিয়ে। নতুন স্কিলকে সঠিক পরিবারে বরাদ্দ করতে, পরিবার পরিবর্তনের পর একটি পরিবার-হেডার রাউটার পুনর্বিন্যাস করতে, অথবা একটি এতিম রাউটার অপসারণ করতে এই স্কিল ব্যবহার করো। „পরিবার রক্ষণাবেক্ষণ করো“ (Familien pflegen), „নতুন স্কিলকে পরিবারে বরাদ্দ করো“ (neuen Skill einer Familie zuordnen), „রাউটার আপডেট করো“ (Router aktualisieren), „পরিবার-হেডার সেট/অপসারণ করো“ (Familien-Header setzen/entfernen) বাক্যাংশেও এটি সক্রিয় হয়।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: bn
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
translated_from_sha256: b4d39973bb0e97c3190c0f821fe0a351a0f338cdfd1ea6fff26d44d1ca476c21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="skill-family-care banner">
# স্কিল-পরিবার-রক্ষণাবেক্ষণ

## উদ্দেশ্য

আপ-টু-ডেট রাখে স্কিল-**পরিবারগুলো** — `skill-explorer`-এর পূর্ণ অডিট-রানের প্রয়োজন ছাড়াই। ইনস্টলার-নীতি অনুসরণ করে (একটি একক মনোলিথের বদলে হালকা সাবস্কিল) আলাদা করা হয়েছে। `skill-explorer`-এর স্ক্রিপ্টগুলোকে উল্লেখ করে, সেগুলো কপি করে না।

## উৎস (নকল করো না)

- **পরিবার-তালিকা:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (প্রামাণিক family-/routing-মানচিত্র)।
- **ইনভেন্টরি (বর্তমান অবস্থা):** `skill-explorer/scripts/inventory_skills.py`।
- **রাউটার সেট/অপসারণ:** `skill-explorer/scripts/inject_family_header.py`।
- **কনফিগ (কোন পরিবারগুলো সংযুক্ত):** `~/.claude/skills/skill-explorer/config.json`।

## কাজসমূহ

### A — নতুন স্কিলকে একটি পরিবারে বরাদ্দ করা
1. ইনভেন্টরি নতুন করে সংগ্রহ করো:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. `SKILL-MAP.md` থেকে উপযুক্ত পরিবার বাছাই করো (অক্ষসমূহ: Phase/Breite/Rigidität/Wirkung/Rohstoff)।
3. স্কিলটিকে `config.json`-এ (`families[<fam>].members`) সদস্য হিসেবে এবং `SKILL-MAP.md`-এ যুক্ত করো।

### B — পরিবার পরিবর্তনের পর হেডার-রাউটার পুনর্বিন্যাস
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Idempotent: একই পরিবারের বিদ্যমান ব্লক প্রতিস্থাপিত হয়।
- শুধু `editable`/`source=user`-স্কিলগুলো পরিবর্তিত হয় (স্ক্রিপ্টের গেট দ্বারা)।

### C — এতিম রাউটার অপসারণ
একই স্ক্রিপ্ট `--remove` দিয়ে চালাও (`--router` লাগে না)।

## কঠোর নিয়মাবলি

- **Survey ≠ Mutation:** শুধু ব্যবহারকারী-নিজস্ব স্কিল হেডার পায়। Plugin/বহিরাগত কখনো স্পর্শ করা হয় না।
- প্রতিটি পরিবর্তনের পর `config.json` (`families[*].linked`, `updated`) আপডেট করো।
- Family-মানচিত্র থেকে কোনো বিষয়বস্তু এককী স্কিলে নকল করো না — শুধু পথনির্দেশক ব্লক।

## পরিবর্তনের ইতিহাস

### 0.1.0 (2026-06-17)
- প্রাথমিক সংস্করণ। অডিট-মোড (P1) থেকে তৈরি।
