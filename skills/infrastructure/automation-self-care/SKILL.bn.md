---
name: automation-self-care
version: 1.3.1
type: skill
author: Lukas Geiger + OpenAI + Google Gemini
created: 2026-07-28
updated: 2026-09-09
description: "একটি প্রদানকারী-নিরপেক্ষ স্ব-রক্ষণাবেক্ষণ মূল সেট তৈরি ও পরিচালনা করে, যা নির্ধারিত LLM কাজ এবং ডেস্কটপ অ্যাপ অটোমেশনের জন্য। নির্ধারক নীতি লিন্টিং, লক ও মডেল গভর্ন্যান্স, সিম্যান্টিক প্রম্পট পরীক্ষা, সামঞ্জস্যপূর্ণ বহু-পৃষ্ঠ আপডেট, মিনি-চেক এবং নিয়ম-ফাইল পরিচ্ছন্নতা যুক্ত করে। যখন কোনো এজেন্টকে তার নেটিভ শিডিউলার আবিষ্কার করতে হয় অথবা রোলব্যাক, রিডব্যাক ও মুছে ফেলা-সুরক্ষা সহ একটি বিদ্যমান অটোমেশন বহর ক্রমাগত উন্নত করতে হয়, তখন এটি ব্যবহার করুন। এটি automation self-care (স্ব-রক্ষণাবেক্ষণকারী অটোমেশন), Scheduler-Task-Pflege (নির্ধারিত কাজের রক্ষণাবেক্ষণ), Desktop-App-Automations-Wartung (ডেস্কটপ অ্যাপ অটোমেশনের রক্ষণাবেক্ষণ), Automations-Flotten-Audit (অটোমেশন বহরের নিরীক্ষা), selbstheilende Zeitpläne (স্ব-নিরাময়কারী সময়সূচি), core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-governance-automations বা textbased-desktopapp-automations দ্বারা সক্রিয় হয়।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system, governance, token-governance, mini-check, policy-linter]
language: bn
status: active
visibility: public
aliases: [textbased-governance-automations-seed, tgas, textbasierte-governance-automationen-seed, textbased-governance-automations, textbasierte-governance-automationen, textbased-governance-automatisations-seed, core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: a4c4c991d5459d5b4fe3a7e80c0877791d79adbd1d9ff38b20798636c19cf5d0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---
<img src="banner.png" width="100%" alt="automation-self-care banner">

# Automation Self-Care

একটিমাত্র প্রদানকারী-নিরপেক্ষ নিয়ম-লুপ থেকে একটি নেটিভ, প্রদানকারী-নির্দিষ্ট রক্ষণাবেক্ষণ বহর তৈরি করে। ANTIGRAVITY-Task-পরিবারের মূল উদ্দেশ্য সংরক্ষণ করে, তবে প্রমাণ, বিপরীতযোগ্য পরিবর্তন এবং নেটিভ রিডব্যাক দাবি করে।

## অলঙ্ঘনীয় সীমা

- আবিষ্কার, পরিকল্পনা, অনুমোদন, Mutation এবং Readback-কে আলাদা পর্যায় হিসেবে বিবেচনা করুন।
- লক্ষ্য অ্যাপের সমর্থিত অটোমেশন API, কমান্ড বা UI ব্যবহার করুন। কখনও ধরে নেবেন না যে স্টোরেজ ফাইল সম্পাদনা করলে লাইভ অ্যাপ-স্টেট বদলায়।
- কোনো Task প্রস্তাব করার আগে স্থানীয় নিয়ম, Locks, মুছে ফেলা/Suppression-লগ এবং বিদ্যমান শিডিউল পড়ুন।
- Scheduler-সমর্থন উদ্ভাবন করবেন না। Create/Update/Readback প্রমাণ করা না গেলে একটি ম্যানুয়াল ইনস্টলেশন পরিকল্পনা তৈরি করুন এবং Mutation-এর আগে থামুন।
- প্রতি Care-Lauf-এ সর্বাধিক একটি স্বতন্ত্রভাবে পরীক্ষাযোগ্য Tuning-পরিবর্তন।
- Care-Tasks নিজেদের নিষ্ক্রিয় না করে এবং নিজেদের নির্ধারিত ব্যবধান কনফিগার করা Recovery Floor-এর নিচে না নামায়, এটি সুরক্ষিত রাখুন। শুধুমাত্র একটি সুস্পষ্ট ব্যবহারকারী-সিদ্ধান্ত, একটি নিরাপত্তা-গেট বা প্রমাণিত জরুরি অবস্থা একটি নিয়ন্ত্রিত বিরতি অনুমোদন করতে পারে।
- দৃশ্যমান শিরোনাম থেকে স্বতন্ত্র স্থিতিশীল মেশিন-Task-IDs বজায় রাখুন। App-Präfix-কে অতিরিক্ত চেনার সুরক্ষা হিসেবে বিবেচনা করুন, কখনও পরিচয় হিসেবে নয় বা Recovery-, Suppression-, Rollback- ও Readback-নিয়ন্ত্রণের বিকল্প হিসেবে নয়।
- পূর্ববর্তী Prompt, Zeitplan, Modell, Berechtigungen এবং Aktiv-Status সংরক্ষণ করুন, যাতে প্রতিটি Mutation রোলব্যাক করা যায়।
- শুধু Scheduler-Start বা Exit 0-এর ভিত্তিতে নয়, ফলাফল-প্রমাণের পরেই সাফল্য গণ্য করুন।
- কোনো গোপন তথ্য, ব্যক্তিগত Prompt বা ব্যক্তিগত ডেটা একটি ভাগ করা Registry-তে কপি করবেন না।
- প্রতিটি Mutation-এর আগে প্রদানকারী-প্রোফাইলে নামকৃত একটি নির্ধারক Policy-Linter চালান। প্রকল্প-পথ, যাচাই-স্ক্রিপ্ট এবং Policies Adapter-ক্ষেত্র বা নিরপেক্ষ প্লেসহোল্ডারের মাধ্যমে সমাধান করুন; সর্বজনীন Skill-এ কোনো Host-, Konto- বা ব্যক্তিগত ডিরেক্টরি-পথ নেবেন না।
- ফাইল-, Scheduler-, Commit- বা Push-ক্রিয়ার আগে লক্ষ্য-সিস্টেমের প্রামাণিক Lock-কর্তৃপক্ষ যাচাই করুন। Lock-কর্তৃপক্ষ অজানা, অগম্য বা পরস্পরবিরোধী হলে Fail-Closed ও Read-only প্রযোজ্য।
- স্থির-কোডকৃত পণ্য-সংস্করণ বা অপ্রমাণিত গুণমান-ধারণার ভিত্তিতে মডেল পরিবর্তন করবেন না। বর্তমান প্রদানকারী-পৃষ্ঠ ও বৈধ স্থানীয় Policy থেকে অনুমোদিত মডেল ও ন্যূনতম মান নির্ধারণ করুন। Downgrade ও Upgrade-এর জন্য সেখানে নির্ধারিত কর্তৃপক্ষ লাগবে; অস্পষ্ট হলে মডেল অপরিবর্তিত থাকে।
- শুধু চালনা-লগ থেকে Prompt-Tuning নির্ধারণ করবেন না। Mutation-এর আগে প্রস্তাবটি লক্ষ্য প্রকল্পের প্রযোজ্য Policies-এর বিপরীতে সিম্যান্টিকভাবে যাচাই করুন এবং নিরাপত্তা-, গবেষণা- বা অনুমোদন-সীমা অক্ষুণ্ণ রাখুন।
- একাধিক প্রামাণিক স্টেট-পৃষ্ঠকে একটি লেনদেন হিসেবে বিবেচনা করুন: পূর্ব-অবস্থা সংরক্ষণ করুন, সমস্ত ঘোষিত লক্ষ্য আপডেট করুন, প্রতিটি লক্ষ্য পুনরায় পড়ুন এবং আংশিক সাফল্যে সম্পূর্ণ রোলব্যাক করুন। কোনো নির্দিষ্ট সংখ্যা বা স্থানীয় ডিরেক্টরি-কাঠামোকে সর্বজনীনভাবে ধরে নেবেন না।
- চালনা-প্রতিবেদন শুধু নির্ধারিত স্থানীয় প্রমাণ- ও স্ট্যাটাস-স্টোরেজে রাখুন, কখনও এজেন্ট-নিয়মফাইলে নয়। এসব স্টোরেজের নাম ও অবস্থান প্রদানকারী-প্রোফাইল থেকে আসে।
- ভারী রক্ষণাবেক্ষণ অল্প পরিসরের Mini-Checks দিয়ে পরিপূরক হতে পারে। চালনার সময়সীমা, পরীক্ষার পরিধি, মূল Task এবং উচ্চতর স্তরে বৃদ্ধির পথ প্রদানকারী-প্রোফাইলে থাকতে হবে; একটি Mini-Check গভীর মেরামত চালাতে পারবে না।

## প্রবাহ

### 1. নেটিভ অটোমেশন-পৃষ্ঠ আবিষ্কার করুন

বর্তমান অভিনেতা, প্রদানকারী, অ-সংবেদনশীল `app_display_name`, অ্যাপ-শ্রেণি, Scheduler-ইন্টারফেস, সমর্থিত অপারেশন, State-Dateien, চালনা-ইতিহাস, ব্যবহার-টেলিমেট্রি এবং Readback-পদ্ধতির তালিকা করুন। সক্ষমতাগুলো [provider-adapter-contract.md](references/provider-adapter-contract.md)-এর প্রোফাইল-চুক্তির মাধ্যমে লিপিবদ্ধ করুন।

নেটিভ Desktop-App-Zeitpläne, CLI-/Headless-Ausführung, OS-Scheduler বা Service-Starter, সাধারণ Scheduler-Dienst, Workflow-Engine এবং অসমর্থিত বা শুধু-UI অটোমেশন আলাদা করুন। একটি কনফিগারেশন-ফাইলের অস্তিত্ব কে সমর্থিত Mutation-পথের সমতুল্য ধরবেন না।

### 2. বহর তালিকাভুক্ত করুন

প্রতিটি Task-এর জন্য একটি স্থিতিশীল স্থানীয় Identifier, সিম্যান্টিক ভূমিকা, দৃশ্যমান শিরোনাম, উদ্দেশ্য, Prompt-Fingerprint, সময়সূচি, সক্রিয়-অবস্থা, Modell, Reasoning, Berechtigungen, লক্ষ্যপথ, সর্বশেষ Scheduler-ইভেন্ট, সর্বশেষ সফল ফলাফল এবং বর্তমান Owner রেকর্ড করুন। Prompt-বিষয়বস্তু স্থানীয়ভাবে রাখুন।

নতুন তৈরির প্রস্তাবের আগে বিদ্যমান Tasks সিম্যান্টিকভাবে মেলান। প্রথমে স্থিতিশীল Task-ID, তারপর প্রদানকারী-নেটিভ ID, সিম্যান্টিক ভূমিকা এবং পরিচিত Legacy-শিরোনাম অগ্রাধিকার দিন। ভিন্ন দৃশ্যমান শিরোনাম নতুন Task প্রয়োজন হওয়ার প্রমাণ নয়। অস্পষ্ট মিল পরিকল্পনাকে আটকে দেয়; একটি ডুপ্লিকেট তৈরি করা হয় না।

যদি অ্যাপ স্টেট স্মৃতি থেকে পুনর্লিখতে পারে, তাহলে প্রতিটি Mutation-এর আগে প্রামাণিক লাইভ পৃষ্ঠ দুইবার যাচাই করুন।

### 3. Core-Set নকশা করুন

[core-set.md](references/core-set.md) পড়ুন। নিম্নলিখিতের মধ্যে বাছুন:

- `compact`: পাঁচটি Care-Task, যা ফ্রিকোয়েন্সিকে লোড-বণ্টনের সঙ্গে মেলায়; বা
- `full`: মূল রক্ষণাবেক্ষণ-পরিবার অনুযায়ী নয়টি কেন্দ্রীভূত Task।

একটি প্রদানকারী-নিরপেক্ষ পরিকল্পনা তৈরি করুন:

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
python scripts/build_core_set.py --lint-plan automation-care-plan.json
```

জেনারেটর কখনও Tasks ইনস্টল করে না। পরিকল্পনা প্রয়োগের আগে প্রতিটি `blocked`-সক্ষমতা যাচাই করুন এবং সংঘর্ষমুক্ত স্থানীয় সময় বাছুন। নতুন প্রদানকারী-প্রোফাইল `app_display_name` স্পষ্টভাবে সেট করে; CI এটি `--strict-profile` দিয়ে বাধ্যতামূলক করতে পারে। তৈরি দৃশ্যমান শিরোনাম `<APP_DISPLAY_NAME> — <CARE_TITLE>` ব্যবহার করে, যেখানে `automation-care.*`-Task-IDs অপরিবর্তিত থাকে। একটি Codex-Profil `CODEX` ব্যবহার করে।

### 4. ধাপে ধাপে ইনস্টল করুন

নেটিভ প্রদানকারী-Adapter-এর মাধ্যমে ইনস্টল করুন:

1. Read-only মোডে Hygiene দিয়ে শুরু করুন।
2. সম্পদ-সুরক্ষা যোগ করুন।
3. রোলব্যাকসহ Prompt-গুণমান-টিউনিং যোগ করুন।
4. পর্যাপ্ত চালনা-প্রমাণ জমার পরেই ফ্রিকোয়েন্সি ও লোড-টিউনিং যোগ করুন।
5. সবশেষে Cross-System-Koordination যোগ করুন।

শুধু শিরোনাম-Migration-এর জন্য সিম্যান্টিকভাবে মেলানো Task সমর্থিত নেটিভ পৃষ্ঠের মাধ্যমে in-place আপডেট করুন। স্থিতিশীল ID ও শিরোনাম-ছাড়া সমস্ত ক্ষেত্র পুনরায় পড়ুন; যেকোনো অপ্রত্যাশিত অপারেশনাল Delta-র জন্য Rollback দরকার। দ্বিতীয় Plan-/Apply-চক্র কোনো পরিবর্তন জানাবে না এবং আরও কোনো Task তৈরি করবে না।

ব্যবহারকারী সক্রিয় ইনস্টলেশন সুস্পষ্টভাবে অনুমোদন না করলে নতুন বা আমদানিকৃত Tasks নিষ্ক্রিয় অবস্থায় তৈরি হয়। তত্ত্বাবধানহীন পাইলট-চালনার জন্য প্রথমে একটি মুছে ফেলার লগ, একটি আগের-স্টেট Snapshot, একটি চালনা-প্রমাণ এবং একটি Rollback-পথ দাবি করুন।

### 5. Care-লুপ চালান

প্রতিটি Care-Task অনুসরণ করে:

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

[core-set.md](references/core-set.md)-এর অনুমান-তালিকা ও প্রমাণ-নিয়ম ব্যবহার করুন। অজানা কারণ মানে পর্যবেক্ষণ, অনুমতি সীমিত করা বা নিরাপদে বিরতি দেওয়া; কখনও মেরামত অনুমান করবেন না।

### 6. অভিনেতাদের মধ্যে সমন্বয় করুন

স্থানীয় App-State-কে প্রামাণিক রাখুন। শুধু Task-চুক্তি, কভারেজ, স্ট্যাটাস, প্রমাণ এবং পরিচ্ছন্ন Fingerprints ভাগ করুন। অতিরিক্ত Read-only-পর্যালোচনা অনুমোদিত; Single-Writer-Mutationগুলোর জন্য একটি Claim বা সমতুল্য নেটিভ Lock লাগে।

### 7. নেটিভ Event-Hooks ছাড়া সিস্টেম (Letter-Hooker-Erweiterung)

Token- বা Abo-Limitierung-কে ভাঙা অভিনেতা নয়, বরং একটি ক্ষমতার অবস্থা হিসেবে বিবেচনা করুন। মূল অভিনেতা সফল প্রমাণ দেওয়ার পর অর্পিত কভারেজ ফেরত দিন।

## বাধ্যতামূলক আউটপুট

প্রতিটি Setup- বা Care-Lauf-এর জন্য প্রতিবেদন দিন:

- আবিষ্কৃত নেটিভ পৃষ্ঠ এবং অসমর্থিত সক্ষমতা;
- নির্বাচিত টোপোলজি এবং তৈরি, প্রস্তাবিত বা এড়িয়ে যাওয়া Tasks;
- সঠিক Mutation এবং আগে/পরের Readback;
- ফলাফল-প্রমাণ বা খোলা পর্যবেক্ষণ-উইন্ডো;
- Rollback-অবস্থান ও ফেরত-শর্ত;
- একটি সমন্বয়-Registry থাকলে ভাগ করা কভারেজ-আপডেট।

## উদাহরণ

ব্যবহারকারী: "এই Desktop-App-এ নিজে রক্ষণাবেক্ষণ করা Zeitpläne সেট আপ করো।"

যাচাই করুন অ্যাপ নির্ধারিত Tasks তালিকাভুক্ত, তৈরি, আপডেট ও যাচাই করতে পারে কি না। সংক্ষিপ্ত পরিকল্পনা তৈরি করুন, অসমর্থিত সক্ষমতা ব্যাখ্যা করুন, তারপর শুধু অনুমোদিত Tasks নেটিভ পৃষ্ঠের মাধ্যমে ইনস্টল করুন। Task-Prompt সহ একটি ফোল্ডার, যার লাইভ-Scheduler-নিবন্ধন নেই, সম্পূর্ণ সেটআপ নয়।

## Changelog

### 1.3.1 (2026-09-09)

- Version 1.2 ও 1.3-এর সুস্পষ্টভাবে নির্দেশিত Self-Care-কঠোরীকরণ প্রদানকারী-নিরপেক্ষভাবে একীভূত।
- সর্বজনীন নির্দেশিকা থেকে Host-, Konto- ও ব্যক্তিগত Projektpfade সরানো হয়েছে এবং Adapter-ক্ষেত্র বা নিরপেক্ষ প্লেসহোল্ডার দিয়ে প্রতিস্থাপিত হয়েছে।
- মডেল পরিবর্তন বর্তমান প্রদানকারী-সক্ষমতা, স্থানীয় Policy ও প্রমাণিত কর্তৃপক্ষের সঙ্গে যুক্ত; স্থির সংস্করণ-ক্রম ও অপ্রমাণিত গুণমান-দাবি সরানো হয়েছে।
- Policy-Linting, সিম্যান্টিক Prompt-পরীক্ষা, Lock-Gate, লেনদেনভিত্তিক বহু-পৃষ্ঠ আপডেট, নিয়মফাইল-পরিচ্ছন্নতা এবং Mini-Checks পোর্টেবল চুক্তি হিসেবে বর্ণিত।

### 1.3.0 (2026-09-09)

- নির্ধারক Policy-Linting ও সিম্যান্টিক Policy-পরীক্ষা যুক্ত।
- বহু-পৃষ্ঠ সমতা এবং পরস্পরবিরোধী অবস্থার পরিচ্ছন্নতা সুরক্ষিত।

### 1.2.0 (2026-09-06)

- Lock-Governance, Modell-Anti-Regression, নিয়মফাইল-পরিচ্ছন্নতা এবং Mini-Check-Architektur যুক্ত।

### 1.1.0 (2026-08-30)

- প্রদানকারী-নিরপেক্ষ `app_display_name` এবং দৃশ্যমান শিরোনাম-ফরম্যাট `<APP_DISPLAY_NAME> — <CARE_TITLE>` যুক্ত, সঙ্গে Codex-Adapter-প্রোফাইলের মাধ্যমে `CODEX — ...`।
- Plan-Linting, স্থিতিশীল-ID-/সিম্যান্টিক মিলকরণ এবং Duplikat-সুরক্ষা যুক্ত।
- স্পষ্ট করা হয়েছে যে Naming Recovery Floor-এর পাশাপাশি প্রযোজ্য এবং শুধু শিরোনাম-Migration-এ প্রতিটি Nicht-Titel-Fingerprint সংরক্ষণ করতে হবে।

### 1.0.1 (2026-07-30)

- প্রদানকারী-নিরপেক্ষ Text-Automations- ও Desktop-App-Automations-Aliase যুক্ত।

### 1.0.0 (2026-07-28)

- মূল ANTIGRAVITY-রক্ষণাবেক্ষণ-পরিবার, F1-F6-নিয়মলুপ এবং পরবর্তী প্রদানকারী-নির্দিষ্ট সমন্বয়গুলো একটি নিরপেক্ষ Core-Set-Skill-এ একীভূত।
