---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: "এটি স্বতন্ত্র মডিউল steuer-assistent-এর দিকে নির্দেশ করে: জার্মান কর্মচারীদের আয়-সম্পর্কিত ব্যয় (Werbungskosten)-এর জন্য একটি স্থানীয়, অফলাইন-প্রথম রসিদ ওয়ার্কশিট -- রেকর্ড করা, সেন্ট পর্যন্ত যোগফল করা, ব্যক্তিগত ZIP এক্সপোর্ট। যখন Werbungskosten-এর রসিদ একটি কাঠামোগত উপায়ে প্রস্তুত করতে হবে তখন এই স্কিল ব্যবহার করুন -- একটি স্পষ্ট সীমানা সহ: এটি কর-পরামর্শ নয়, কর-যোগ্যতার যাচাই নয়, কর-রিটার্ন তৈরি বা জমাও নয় (সেটি ELSTER বা অনুমোদিত সফটওয়্যারের মাধ্যমে হয়)।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: bn
status: active
visibility: public
translated_from_sha256: 0beb350be5741675f21d27461094e9908be7de7c209e659bed7b55ab374c1bb3
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T01:22:42.649734+00:00"
---
<img src="banner.png" width="100%" alt="steuer-assistent banner">

# steuer-assistent -- Verweis-Skill

এই স্কিলটি একটি **সরল রেফারেন্স (র্যাপার)**, যা স্বতন্ত্র, সর্বজনীন মডিউল-রিপোজিটরি
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)-এর দিকে নির্দেশ করে
(MIT-লাইসেন্স, সর্বজনীন)। আসল স্কিলটি সেখানেই থাকে -- এই রিপোজিটরি শুধু লিংক করে এবং ইনস্টলেশন নথিভুক্ত করে।

## মডিউলটি কী করে

`steuer-assistent` স্বনির্ধারিত-শ্রেণিবদ্ধ Werbungskosten-রসিদের (কর্মচারী-Werbungskosten) জন্য একটি ছোট, অফলাইন-প্রথম Python-মডিউল:

- রসিদ রেকর্ড করা (শ্রেণি, পরিমাণ, তারিখ, ঐচ্ছিক নোট)।
- রেকর্ড করা Werbungskosten বছরভিত্তিক সেন্ট-নির্ভুলভাবে যোগ করা।
- একটি ব্যক্তিগত, সরকারি-নয় ZIP কর্মপত্র এক্সপোর্ট করা (CSV + সারাংশ + সরকারি-নয় সতর্কবার্তা, রসিদের ফাইল ছাড়া)।
- স্থানীয় স্টোর (ডিফল্ট `%USERPROFILE%\.steuer-assistent\steuer.db`), কোনো নেটওয়ার্ক অ্যাক্সেস নেই, কোনো ক্লাউড আপলোড নেই, অন্যের ডেটাবেসে অ্যাক্সেস নেই।

## সীমাবদ্ধতা (গুরুত্বপূর্ণ)

- **কোনো কর-পরামর্শ নয়।** মডিউলটি পৃথক আইটেমের কর-যোগ্যতা যাচাই করে না এবং কর-রিটার্ন তৈরি বা জমা দেয় না।
- সরকারি ইলেকট্রনিক জমা শুধুমাত্র ELSTER বা এর জন্য অনুমোদিত সফটওয়্যারের মাধ্যমে হয় -- এই মডিউলের মাধ্যমে নয়।
- পরিধি: কর্মচারী-Werbungskosten-এর জন্য ব্যক্তিগত কর্মপত্র; ব্যবসা বা ব্যবসায়িক ব্যয়ের রেকর্ড নয়।

## ইনস্টলেশন (সাধারণ, স্থানীয় নির্দিষ্ট পথ ছাড়া)

1. মডিউল ক্লোন করুন:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <klon-pfad>
   ```
2. মডিউল ইনস্টল ও যাচাই করুন:
   ```bash
   cd <klon-pfad>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. `<klon-pfad>/SKILL.md` নিজের স্কিল-পরিবেশে গ্রহণ করুন (যেমন
   `~/.claude/skills/steuer-assistent/`)। কোনো প্রকৃত স্থানীয় পথ বা হোস্টনাম সংস্করণ-নিয়ন্ত্রিত স্কিল-পরিবেশে কমিট করবেন না।
4. প্রয়োজনে `STEUER_ASSISTENT_DB=<pfad>` বা `--store <pfad>` দিয়ে স্টোর-পথ সামঞ্জস্য করুন; ডিফল্ট হলো ব্যবহারকারীর ডিরেক্টরি।
5. CLI কমান্ড, ডেটা সুরক্ষা ও সীমাবদ্ধতার বিস্তারিত: মডিউল-রিপোর README দেখুন।

## এই রেফারেন্স-স্কিলের উৎস

এই র্যাপারটি ২০২৬-০৭-২৩ তারিখে `ellmos-ai/skills` রিপোজিটরির জন্য একটি শোকেস এন্ট্রি হিসেবে প্রস্তুত করা হয়েছে। **কোনো কোড নকল** করা হয়নি -- রক্ষণাবেক্ষণ ও সংস্করণ নিয়ন্ত্রণ শুধুমাত্র মডিউল-রিপো `ellmos-ai/steuer-assistent`-এ থাকে।

## পরিবর্তনের ইতিহাস

### 0.1.0 (2026-07-23)
- `ellmos-ai/steuer-assistent`-এর উপর প্রাথমিক রেফারেন্স-স্কিল।
