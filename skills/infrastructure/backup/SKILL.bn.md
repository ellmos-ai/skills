---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "ফাইলগুলো স্পষ্টভাবে fail-closed mac-backup কোরের মাধ্যমে প্ল্যান, মিরর, যাচাই, পুনরুদ্ধার বা আর্কাইভ করে। ব্যবহারকারীর নিজস্ব হোস্ট-জুড়ে ব্যাকআপ জবের জন্য ব্যবহার করুন; সাধারণ ক্লাউড সিঙ্ক্রোনাইজেশন বা আনুষঙ্গিক ফাইল কপির জন্য নয়।"
visibility: public
language: bn
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T13:14:33.874711+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# ব্যাকআপ

ইনস্টল করা `mac-backup`-CLI-কেই একমাত্র ট্রান্সফার বাস্তবায়ন হিসেবে ব্যবহার করুন। কাঁচা `scp`, `rsync`, SSHFS, Explorer-এর কার্যক্রম বা অ্যাড-হক মুছে ফেলা দিয়ে প্রবাহটি পুনর্নির্মাণ করবেন না।

## অনুরোধ রাউট করা

- সাধারণ "ব্যাকআপ" অনুরোধের অর্থ `mirror`; উৎস অপরিবর্তিত থাকে।
- `archive` মানে উৎস পরিষ্কার করা, এবং এটি একটি আলাদা, ধ্বংসাত্মক উদ্দেশ্য। "backup", "copy" বা "free some space" থেকে কখনও এটি অনুমান করবেন না।
- `restore` একটি নতুন গন্তব্যে লেখে এবং কখনও নীরবে ওভাররাইট করে না।
- যাচাইকৃত জব JSON না থাকলে একটি জব প্রস্তাব প্রস্তুত করুন এবং `init-target` বা ট্রান্সফারের আগে থামুন।

## কার্যকর করা

1. জবটি পড়ুন এবং `mac-backup plan <job> --json` চালান।
2. নিশ্চিত করুন যে ফেরত আসা উৎস শ্রেণি, ফাইল সংখ্যা, বাইট সংখ্যা, গন্তব্য Volume ID, এনক্রিপশন অবস্থা এবং হোস্ট ফিঙ্গারপ্রিন্ট অনুরোধ ও বর্তমান ডিভাইসের প্রমাণের সাথে মেলে।
3. Mirror-এর জন্য `mac-backup mirror <job> --json` চালান, তারপর `mac-backup verify <job> --json`।
4. Restore-এর জন্য একটি নতুন, সম্পূর্ণ পথের গন্তব্য ব্যবহার করুন এবং কমান্ডের Manifest ফলাফলের মাধ্যমে পুনরুদ্ধার করা ফাইলগুলো যাচাই করুন।
5. Archive-এর জন্য `--confirm-delete` শুধু তখনই পাস করুন যখন ব্যবহারকারী স্পষ্টভাবে উৎস অপসারণ চেয়েছেন এবং যাচাইকৃত পরিকল্পনা ঠিক সেই উৎসের নাম উল্লেখ করেছে। একটি Policy ব্লক হওয়া সঠিক ফলাফল; `target_encryption_required`, `source_class_unknown_cleanup_blocked`, `onedrive_dehydrate_not_implemented`, কোনো Lock, পরিচয়ের অমিল বা অনুপস্থিত অ্যাঙ্কর কখনও বাইপাস করবেন না।

`init-target` হলো বিশেষাধিকার-সম্পন্ন সেটআপ, নিয়মিত কার্যকর করার জন্য নয়। এর জন্য Volume ID ও এনক্রিপশনের জন্য একটি স্বতন্ত্রভাবে সংগৃহীত অপারেটিং সিস্টেম প্রমাণ লাগে; প্রস্তাবিত জব থেকে কপি করা মান কোনো প্রমাণ নয়।

গন্তব্যের Verify এবং একটি প্রকৃত Restore পরীক্ষা উভয়ই সফল না হওয়া পর্যন্ত কখনও দাবি করবেন না যে Mirror একটি সম্পূর্ণ ব্যাকআপ। টিকিট, Git এবং OneDrive থেকে গোপন তথ্য, প্রকৃত জব ফাইল, স্থানীয় অ্যাঙ্কর এবং ব্যবহারকারীর ফাইলের নাম দূরে রাখুন।

## Changelog

### 1.0.0 (2026-08-24)
- `~/.claude/skills/backup/`-deployment মাস্টারের একটি নিরপেক্ষ অনুলিপি শ্রেণিবদ্ধ লাইব্রেরিতে যুক্ত করা হয়েছে। সিঙ্ক ফাঁকের কারণ: Skill-টি ডিপ্লয় করা ছিল, কিন্তু `skills/<category>/`-এর অধীনে এর কোনো উৎস এন্ট্রি ছিল না। ফলে `skill_sync.py status` এটিকে `NUR-ZIEL` (শুধু গন্তব্য) হিসেবে রিপোর্ট করত, এবং `catalog.py`/`build_public_registry.py` (যা শুধু `skills/` স্ক্যান করে) এটি কখনও দেখত না। ফলে ডিপ্লয়মেন্ট কপি যেভাবেই সম্পাদনা করা হোক না কেন, এটি কখনও পাবলিক রেজিস্ট্রি বা `SKILLS-MAP.md` পর্যন্ত পৌঁছাতে পারত না।
