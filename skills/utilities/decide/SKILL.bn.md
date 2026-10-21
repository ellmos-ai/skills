---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "কাঠামোবদ্ধ সিদ্ধান্ত গ্রহণ: Pro/Con ম্যাট্রিক্স, ওজনযুক্ত স্কোরিং, সিদ্ধান্ত বৃক্ষ, পরিস্থিতি বিশ্লেষণ এবং Eisenhower ম্যাট্রিক্স।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 1627b5e5d34c9cc5009de91ad5ce32eb203984c0416d715513c7f2489e5ca4f6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="decide banner">

# Decide — কাঠামোবদ্ধ সিদ্ধান্ত গ্রহণ

> যুক্তিসঙ্গত সিদ্ধান্ত কাঠামোবদ্ধ পদ্ধতি এবং মূল্যায়ন পদ্ধতির মাধ্যমে নিন

---

## কখন ব্যবহার করবেন?

- বিকল্পগুলোর মধ্যে সিদ্ধান্ত নিতে
- Pro/Con তালিকা প্রয়োজন হলে
- একাধিক মানদণ্ডভিত্তিক সিদ্ধান্তের ক্ষেত্রে
- গুরুত্বপূর্ণ সিদ্ধান্তে অনিশ্চিত থাকলে

**ট্রিগার-শব্দ:** entscheiden, waehlen, vergleichen, evaluieren, abwaegen, সিদ্ধান্ত নেওয়া, বেছে নেওয়া, তুলনা করা, মূল্যায়ন করা, ওজন করা

---

## কাঠামোসমূহ

### 1. Pro/Con ম্যাট্রিক্স (সহজ)

দুটি বিকল্পের মধ্যে দ্রুত সিদ্ধান্তের জন্য।

```
PRO A:                    CON A:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

PRO B:                    CON B:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

Empfehlung: [A/B] weil [Begruendung]
```

---

### 2. ওজনযুক্ত স্কোরিং (জটিল)

ওজনসহ বহু-মানদণ্ড সিদ্ধান্তের জন্য।

| মানদণ্ড | ওজন | বিকল্প A | স্কোর A | বিকল্প B | স্কোর B |
|-----------|---------|----------|---------|----------|---------|
| মানদণ্ড 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| মানদণ্ড 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| মোট | 100% | - | X.XX | - | X.XX |

**প্রক্রিয়া:**
1. মানদণ্ড সংগ্রহ করুন
2. ওজন নির্ধারণ করুন (যোগফল = 100%)
3. বিকল্পগুলো মূল্যায়ন করুন (1-10 স্কেল)
4. স্কোর গণনা করুন (মূল্যায়ন x ওজন)
5. তুলনা করে সুপারিশ করুন

---

### 3. সিদ্ধান্ত বৃক্ষ (ধারাবাহিক)

স্পষ্ট যদি-তাহলে পথসহ সিদ্ধান্তের জন্য:
1. প্রারম্ভিক প্রশ্ন সংজ্ঞায়িত করুন
2. প্রথম শাখাবিন্যাস (সবচেয়ে গুরুত্বপূর্ণ মানদণ্ড)
3. পরবর্তী স্তর (দ্বিতীয় গুরুত্বপূর্ণ)
4. চূড়ান্ত বিকল্প পর্যন্ত

---

### 4. পরিস্থিতি বিশ্লেষণ (অনিশ্চয়তা)

```
Best Case (X% Wahrscheinlichkeit):
  Ergebnis: +Y Punkte -> Erwartungswert: +Z

Realistic Case (X%):
  Ergebnis: +Y -> Erwartungswert: +Z

Worst Case (X%):
  Ergebnis: -Y -> Erwartungswert: -Z

Gesamt-Erwartungswert: [Summe]
```

---

### 5. Eisenhower ম্যাট্রিক্স (অগ্রাধিকার নির্ধারণ)

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

---

## গুণমান পরীক্ষার তালিকা

চূড়ান্ত সুপারিশের আগে যাচাই করুন:
- [ ] সকল প্রাসঙ্গিক মানদণ্ড চিহ্নিত হয়েছে?
- [ ] ব্যবহারকারীর মূল্যবোধ বিবেচনা করা হয়েছে?
- [ ] দীর্ঘমেয়াদী প্রভাব ভাবা হয়েছে?
- [ ] ঝুঁকি চিহ্নিত ও মূল্যায়ন করা হয়েছে?
- [ ] Bias-পরীক্ষা সম্পন্ন হয়েছে?
- [ ] বিপরীতযোগ্যতা যাচাই করা হয়েছে?

---

## সেরা অনুশীলন

### মানদণ্ড সংজ্ঞায়িত করা
- নির্দিষ্ট ও পরিমাপযোগ্য হওয়া
- অত্যধিক নয় (আদর্শভাবে 3-7)
- একে অপর থেকে স্বাধীন

### ওজন নির্ধারণ
- যোগফল = 100%
- সবচেয়ে গুরুত্বপূর্ণ মানদণ্ড >= 25%
- কোনো ওজন < 5% নয়

### সুপারিশ
- স্পষ্ট ও যুক্তিসম্মত
- বিকল্পগুলো উল্লেখ করা
- ঝুঁকি চিহ্নিত করা
- বিপরীতযোগ্যতা বিবেচনা করা

---

## কার্যপ্রবাহ

```
1. User Request
2. Entscheidung verstehen
3. Optionen identifizieren (2-5)
4. Framework waehlen
5. Kriterien sammeln
6. Framework anwenden
7. Bias-Check (optional)
8. Empfehlung aussprechen
9. Reasoning dokumentieren
```

---

## পরিবর্তনের লগ

### 1.0.0 (2026-03-15)
- BACH v3.8.0 থেকে পোর্ট করা হয়েছে

---

*BACH v3.8.0 থেকে পোর্ট করা | Standalone-সংস্করণ*

**আরও দেখুন:** [think](../think/SKILL.md) (বিশ্লেষণ, মূল কারণ, SWOT) | [brainstorm](../brainstorm/SKILL.md) (সৃজনশীল পদ্ধতি, ধারণা উদ্ভাবন) | [decision-shot](../decision-shot/SKILL.md) (এই বিশ্লেষণের আউটপুটকে সুপারিশ ও পূর্ণ সংস্করণের লিংকসহ একটি নির্বাহী সংক্ষিপ্ত রূপে ঘনীভূত করুন)
