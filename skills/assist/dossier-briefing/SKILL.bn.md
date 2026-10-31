---
name: dossier-briefing
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "একটি বিষয় বা ব্যক্তির জন্য একটি কাঠামোগত গবেষণা ব্রিফিং একটি Markdown স্ক্যাফোল্ড হিসেবে তৈরি করে (stdout বা ফাইলে)। কোনো স্থায়ী স্টোর নেই।"
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: bn
visibility: public
translated_from_sha256: dbe880eee63e64ccec3db2527c516d0aace0924b5b7a8137e36639ad7136c356
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.407563+00:00"
---
<img src="banner.png" width="100%" alt="dossier-briefing banner">

# ডসিয়ার-ব্রিফিং

**কোনো বিষয় বা ব্যক্তি সম্পর্কে কাঠামোগত গবেষণা ব্রিফিং**

---

## সংক্ষিপ্ত বিবরণ

যেকোনো বিষয়ের (ব্যক্তি, কোম্পানি, ঘটনা, ধারণা) জন্য একটি খালি, কাঠামোগত Markdown ব্রিফিং তৈরি করে। এই স্ক্যাফোল্ডটি `research-agent` বা `web-reading` ব্যবহার করে পরবর্তী গবেষণার ভিত্তি হিসেবে কাজ করে।

---

## ট্রিগার

| বাক্যাংশ | কার্যক্রম |
|---|---|
| „মেরি কুরি সম্পর্কে একটি ব্রিফিং তৈরি করো" | স্ক্যাফোল্ড: ব্যক্তি, ধরন=person |
| „OpenAI সম্পর্কে একটি ডসিয়ার তৈরি করো" | স্ক্যাফোল্ড: কোম্পানি, ধরন=organization |
| „কোয়ান্টাম কম্পিউটিং নিয়ে একটি ব্রিফিং তৈরি করো" | স্ক্যাফোল্ড: বিষয়, ধরন=topic |
| „COP30 নিয়ে একটি গবেষণা ব্রিফিং প্রস্তুত করো" | স্ক্যাফোল্ড: ঘটনা, ধরন=event |

---

## কর্মপ্রবাহ

1. **বিষয় নির্ধারণ:** ব্যবহারকারীর ইনপুট থেকে ব্রিফিংয়ের নাম/শিরোনাম বের করুন।
2. **ধরন শনাক্ত:** person, organization, topic, event (বা unspecified)।
3. **স্ক্যাফোল্ড তৈরি:** সমস্ত প্রাসঙ্গিক বিভাগসহ Markdown তৈরি করুন।
4. **আউটপুট:** stdout-এ লিখুন, অথবা ঐচ্ছিকভাবে একটি ফাইলে লিখুন (`-o datei.md`)।
5. **গবেষণা শুরু:** অনুপস্থিত বিভাগ পূরণ করতে স্ক্যাফোল্ডটি `research-agent` বা `web-reading`-এ পাঠান।

---

## CLI

```bash
# Briefing zu stdout
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# In Datei schreiben
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Themen-Briefing
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantencomputing" --typ topic

# Ereignis
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Ohne Typ-Angabe (generisch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Mein Thema"

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## ব্রিফিংয়ের ধরন ও বিভাগ

| ধরন | বিভাগসমূহ |
|---|---|
| `person` | মৌলিক তথ্য, জীবনী/পটভূমি, কর্ম ও অবদান, সূত্র, নোট |
| `organization` | প্রোফাইল, ইতিহাস, পণ্য/সেবা, মূল ব্যক্তিবর্গ, সূত্র, নোট |
| `topic` | সংক্ষিপ্ত বিবরণ, পটভূমি/প্রেক্ষাপট, সাম্প্রতিক উন্নয়ন, মূল সূত্র, খোলা প্রশ্ন, নোট |
| `event` | মূল তথ্য, সংশ্লিষ্ট পক্ষ, ক্রম/পটভূমি, গুরুত্ব, সূত্র, নোট |
| `unspecified` | সংক্ষিপ্ত বিবরণ, পটভূমি, বিবরণ, সূত্র, নোট |

---

## স্টোর

কোনো স্থায়ী স্টোর নেই। স্ক্যাফোল্ড শুধু আউটপুট হয় (stdout বা ফাইল), কোনো ডাটাবেসে সংরক্ষিত হয় না।

---

## দৃষ্টিভঙ্গি

- সর্বদা উল্লেখ করুন যে স্ক্যাফোল্ডটি খালি এবং গবেষণার মাধ্যমে পূরণ করা প্রয়োজন।
- কখনো তথ্য উদ্ভাবন বা কল্পনা করবেন না — শুধু কাঠামো প্রদান করুন।
- ধরন অস্পষ্ট হলে জিজ্ঞাসা করুন, অথবা `unspecified` ব্যবহার করুন।

---

## গোপনীয়তা

কোনো নেটওয়ার্ক অ্যাক্সেস নেই। কোনো স্টোর নেই। সম্পূর্ণ স্থানীয় প্রক্রিয়াকরণ।

---

## সংশ্লিষ্ট সম্পদ

- `research-agent` — গবেষণার ফলাফল দিয়ে ব্রিফিং স্ক্যাফোল্ড পূরণ করে
- `web-reading` — ওয়েবপেজ পড়ে ব্রিফিংয়ের জন্য বিষয়বস্তু বের করে

---

## পরিবর্তন লগ

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH dossier_generator.py v1.0.0 থেকে তৈরি; স্টোর সরানো হয়েছে, সাধারণীকরণ করা হয়েছে |
