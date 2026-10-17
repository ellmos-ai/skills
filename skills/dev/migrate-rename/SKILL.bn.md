---
name: migrate-rename
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-09-06
description: "ওয়্যারাপার ফাইলের মাধ্যমে বিবর্তনমূলক ফাইল নামপরিবর্তন, এবং সম্পূর্ণ ফোল্ডার/ফাইল স্থানান্তরের জন্য সংক্ষিপ্ত MOVED-স্টাব মান। কঠোর ভাঙন ছাড়াই নামপরিবর্তন সম্ভব করে — ব্যবহারের মাধ্যমে রেফারেন্সগুলো স্বাভাবিকভাবে হালনাগাদ হয়।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 16d2b6f4499cdc4c454bcd8244fff5811ae232e7703095f43a59eb663238d837
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:50.098377+00:00"
---
<img src="banner.png" width="100%" alt="migrate-rename banner">

# ওয়্যারাপারের মাধ্যমে ফাইল নামপরিবর্তন (বিবর্তনমূলক স্থানান্তর)

> কঠোর ভাঙন ছাড়াই ফাইল নামপরিবর্তন সম্ভব করে। রেফারেন্সগুলো প্রতিদিনের ব্যবহারের মাধ্যমে স্বাভাবিকভাবে হালনাগাদ হয়।

---

## নীতি: বিবর্তনমূলক স্থানান্তর

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

যে পুরোনো পাথ কল করে:
1. ওয়্যারাপার ফাইলে পৌঁছায়
2. লগে নিজেকে নথিভুক্ত করে
3. যে তাকে এখানে পাঠিয়েছে সেই রেফারেন্স সংশোধন করে
4. আসল ফাইলে যায়

---

## ধাপে ধাপে

### ১. ফাইল নামপরিবর্তন

```bash
mv alte_datei.md neue_datei.md
```

### ২. ওয়্যারাপার ফাইল তৈরি

`alte_datei.md` তৈরি করুন নিচের বিষয়বস্তু সহ:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |

---

## Anleitung

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` -> `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: `neue_datei.md`

---

**Zieldatei:** `neue_datei.md`
```

### ৩. গুরুত্বপূর্ণ রেফারেন্স অবিলম্বে সংশোধন
- Help-ফাইল (প্রাথমিক ডকুমেন্টেশন)
- System-Prompt রেফারেন্স
- যে CLI-কোড সরাসরি পাথ ব্যবহার করে

### ৪. বাকি রেফারেন্স বিবর্তনমূলকভাবে স্থানান্তর
অবশিষ্টগুলো ব্যবহারের সময় স্বয়ংক্রিয়ভাবে সংশোধিত হবে।

---

## কখন ওয়্যারাপার পদ্ধতি ব্যবহার করবেন?

**হ্যাঁ - ওয়্যারাপার উপযুক্ত:**
- অনেক সম্ভাব্য রেফারেন্স রয়েছে
- ফাইলটি বিভিন্ন অংশীদার/টুল দ্বারা রেফারেন্স করা হয়
- কোনো গুরুত্বপূর্ণ সিস্টেম-ফাইল নয়

**না - সরাসরি সব পরিবর্তন করুন:**
- অল্প সংখ্যক, পরিচিত রেফারেন্স
- গুরুত্বপূর্ণ সিস্টেম-ফাইল (config, DB-Schema)
- কর্মক্ষমতা-সংবেদনশীল পাথ

---

## MOVED-স্টাব সহ ফোল্ডার-/ফাইল স্থানান্তর

> 2026-09-06 তারিখে আনুষ্ঠানিক করা হয়েছে (টিকেট T-20260906-688261413)। পূর্বদৃষ্টান্ত স্বতঃস্ফূর্তভাবে তৈরি হয়েছিল
> `.ELLMOS.MIGRATED.md` (2026-08-11) এবং `_control-center/_CONTROL`-স্টাবে (2026-09-06)।

উপরের ওয়্যারাপার থেকে ভিন্ন পরিস্থিতি: এখানে একটি **পুরো ফোল্ডার** বা **যে ফাইলের অনেক সক্রিয় রেফারেন্স নেই** সম্পূর্ণভাবে নতুন স্থানে সরে যায় (একীকরণ, নামপরিবর্তন, পাইপলাইন পুনর্গঠন)। কোনো মাইগ্রেশন-লগ নেই, "রেফারেন্স সংশোধন" নেই — শুধু একটি সংক্ষিপ্ত নির্দেশক, যা বলে: এটি এখন এখানে।

**উপরের ওয়্যারাপার-পদ্ধতি থেকে পার্থক্য:**

| | ওয়্যারাপার (উপরের ধাপ ১-৪) | MOVED-স্টাব |
|---|---|---|
| ব্যবহার | একক ফাইল, অনেক সক্রিয় রেফারেন্স, স্বাভাবিকভাবে অনুসরণ করবে | ফোল্ডার বা ফাইল, সম্পূর্ণ স্থানান্তর |
| বিষয়বস্তু | মাইগ্রেশন-লগ-টেবিল, ব্যবহারের সাথে বাড়ে | স্থির মেটাডেটা, ১-৩ লাইন সাধারণ পাঠ্য |
| আয়ুষ্কাল | লগে আর নতুন এন্ট্রি না দেখা পর্যন্ত | `remove_when` পূরণ হওয়া পর্যন্ত |

### নাম, অবস্থান, বাধ্যতামূলক ক্ষেত্র

সম্পূর্ণ স্কিমা, উদাহরণ ও ক্ষেত্রের অর্থ ellmos-টেমপ্লেট `MOVED-STUB.md`-এ রয়েছে
(`.TOPICS/.AI/_templates/project-docs/MOVED-STUB.md`, এই স্বতন্ত্র রেপোর অংশ নয় —
সংক্ষিপ্ত সারাংশই এখানে যথেষ্ট):

- **নাম/অবস্থান:** `<alter-Name>.MOVED.md` সেখানে থাকে, যেখানে ফোল্ডার/ফাইলটি **আগে** ছিল।
- **বাধ্যতামূলক ক্ষেত্র** (`key: value`, এই ক্রমে): `moved_to`, `moved_on`, `ticket`,
  `reason`, `moved_by`, `remove_when` (ডিফল্ট: `90 Tage UND 0 lebende Referenzen`)।
- **এরপর** মানুষের জন্য ১-৩ লাইন সাধারণ পাঠ্য। কোনো লগ, টেবিল বা ইতিহাস নয় — সেটি উল্লেখিত টিকেটে থাকে।
- **অপসারণ:** স্টাব **মুছে ফেলা** হয়, কখনো আর্কাইভ করা হয় না।

### নীতি

`.SYNC/_policies/library/P-017_umzugs-stub.md` হিসেবে বাধ্যতামূলক।

### যাচাই স্ক্রিপ্ট

`scripts/moved_stub_check.py` (এই Skill-ফোল্ডারে) একটি মূল ডিরেক্টরির অধীনে সব `*.MOVED.md`/`*.MIGRATED.md`-
স্টাব তালিকাভুক্ত করে, অনুপস্থিত বাধ্যতামূলক ক্ষেত্র জানায় এবং অপসারণযোগ্য
স্টাব (`remove_when` দিনের চেয়ে পুরোনো) চিহ্নিত করে। আহ্বান:

```bash
python scripts/moved_stub_check.py <wurzelverzeichnis>
```

---

## ক্লিনআপ

প্রায় ৩০ দিন পর বা লগে নতুন এন্ট্রি না দেখালে:
1. ওয়্যারাপার ফাইল `_archive/deprecated/`-এ সরান
2. অথবা সম্পূর্ণ মুছে ফেলুন (যদি আর কোনো এন্ট্রি না থাকে)

---

## পরিবর্তনের ইতিহাস

### 1.1.0 (2026-09-06)
- বিভাগ "MOVED-স্টাব সহ ফোল্ডার-/ফাইল স্থানান্তর" যোগ করা হয়েছে (টিকেট T-20260906-688261413):
  পুরো ফোল্ডার/ফাইলের জন্য সংক্ষিপ্ত স্থানান্তর-নির্দেশক আনুষ্ঠানিক করে (মান `<alter-Name>.MOVED.md`,
  বাধ্যতামূলক ক্ষেত্র moved_to/moved_on/ticket/reason/moved_by/remove_when), উপরের
  ওয়্যারাপার-পদ্ধতি থেকে আলাদা করা হয়েছে। যাচাই স্ক্রিপ্ট `scripts/moved_stub_check.py` যোগ করা হয়েছে।

### 1.0.0 (2026-03-15)
- BACH v3.8.0 থেকে পোর্ট করা হয়েছে

---

*BACH v3.8.0 থেকে পোর্ট করা | স্বতন্ত্র সংস্করণ*
