---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: "একটি কোডবেস-আকার অনুযায়ী লক্ষ্যমাত্রা, দ্বিগুণ-বৃদ্ধির স্তর-উন্নয়ন, এলাকা ট্র্যাকিং এবং চূড়ান্ত যাচাই সহ পদ্ধতিগত বাগ সুইপ। /bugsweep-এ বা ব্যবহারকারী যখনই পদ্ধতিগত বাগ পাস চান তখন ব্যবহার করুন।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 72c943e5f956ae19c2e36d0478108228b95866bb77faaadf3dca77a686d9f972
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="bugsweep banner">

# /bugsweep — পদ্ধতিগত Bug-Sweep ওয়ার্কফ্লো

পুনরাবৃত্তিমূলক Bug-অনুসন্ধান, যার একটি অভিসারী (convergent) সমাপ্তি-শর্ত আছে। এটি কোডবেসের আকারের সাথে মানিয়ে নেয়, অগভীর অনুসন্ধানের সন্দেহ হলে স্তর বাড়ায়, এবং এলাকা-ট্র্যাকিংয়ের মাধ্যমে পুনরাবৃত্তি প্রতিরোধ করে।

## 1. মৌলিক হার গণনা করুন

```
LOC = produktive Quellzeilen (src/, lib/ — ohne Tests, Configs, Docs, generated)
x = max(1, ceil(LOC / 1500))
Grundrate = x * 3
```

| LOC | x | মৌলিক হার |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

ব্যবহারকারীকে জানান: "কোডবেস: {LOC} LOC → মৌলিক হার = {Grundrate} পরিষ্কার অনুসন্ধান রান।"

## 2. অনুসন্ধান লুপ

```
zähler = 0
ziel = Grundrate
je_bug_gefunden = False
geprüft = []  # (bereich_name, typ: code|aufgabe)

LOOP:
  bereich = wähle_neuen_bereich()  # Siehe Bereichs-Regeln
  geprüft.append(bereich)
  
  Führe gründliche Bug-Suche durch
  
  IF Bug gefunden:
    je_bug_gefunden = True
    Fix nach bugfix-protocol (Phase 4+5)
    Review: siehe Modell-Regel (neuere Modellklassen: kein externer Review nötig)
    Commit + Push
    zähler = 0  # RESET
  ELSE:
    zähler += 1
    Melde: "✓ Sauber: {bereich} — {zähler}/{ziel}"
  
  IF zähler >= ziel:
    IF NOT je_bug_gefunden:
      # Verdoppelungs-Eskalation: kein einziger Bug → zu oberflächlich?
      ziel = Grundrate * 2
      je_bug_gefunden = True  # Eskalation nur EINMAL
      Melde: "⚠ Kein Bug in {Grundrate} Läufen → Ziel verdoppelt auf {ziel}."
      CONTINUE LOOP
    ELSE:
      GOTO Abschluss-Verifikation
```

### অনুসন্ধান লুপ সংক্রান্ত ব্যবহারিক টিপস (সুইপ থেকে শেখা)

- **Non-Git রেপোজিটরি:** যেখানে `git` নেই (যেমন ক্লাউড-সিঙ্ক্রোনাইজড প্রজেক্ট ফোল্ডার), সেখানে একটি **সংস্করণযুক্ত ব্যাকআপ** "Commit + Push"-এর স্থলাভিষিক্ত হয়: প্রথম ফিক্সের আগে `datei_<ts>.bak` তৈরি করুন। **সতর্কতা — প্রি-ফিক্স ব্যাকআপ কাজের সুরক্ষা নয়:** শেষ ফিক্সের পর একটি নতুন `_FINAL_` ব্যাকআপ নিন, নতুবা সিঙ্কের সমস্যায় পুরো ফিক্স-কাজ হারিয়ে যাবে।
- **অনেক আগে থেকে জানা বাগ:** শুরুতেই যদি N টি বাগ আগে থেকেই জানা থাকে (যেমন আগের রান থেকে), তবে "প্রতি বাগ: Fix → Review → Commit → Reset" অব্যবহারিক। তখন জানা বাগগুলো একটি একক ফিক্স-ব্লক হিসেবে সম্পন্ন করুন (শেষে একটি সম্মিলিত রিভিউ সহ) এবং মৌলিক হার/অনুসন্ধান লুপ প্রথম নতুন-পাওয়া বাগ থেকে গণনা করুন। Reset-যুক্তি সুইপ চলাকালে নতুন-পাওয়া বাগের ক্ষেত্রে প্রযোজ্য থাকবে।
- **একই বাগ একাধিক স্থানে:** একটি পাওয়া ত্রুটি (যেমন একটি ভুল Regex, একটি ভাঙা ফরম্যাট-অনুমান) প্রায়শই কপি হয়ে অন্য স্থানেও থাকে। প্রতিটি ফিক্সের পর অনুসন্ধান করে দেখুন একই প্যাটার্ন অন্য কোথাও আছে কিনা — এটি একটি আলাদা, লাভজনক "এলাকা"।

## 3. এলাকা-নিয়ম (Anti-Gaming)

একটি "এলাকা" হয় একটি **কোড-ফোকাস** অথবা একটি **কাজ** (কোডের উদ্দেশ্য)।

### কোড-ফোকাস
- রানগুলোর মধ্যে **প্রসারিত** (বেশি ফাইল) বা **স্থানান্তরিত** (কোডের অন্য অংশ) করা যাবে
- পূর্বের রানের সাথে হুবহু একই নির্বাচন হতে পারবে না
- উদাহরণ ঠিক আছে: রান 1 = `maintenance.py`, রান 5 = `maintenance.py + orchestrator.py` (প্রসারিত)
- উদাহরণ ঠিক নয়: রান 1 = `maintenance.py`, রান 5 = `maintenance.py` (অভিন্ন)

### কাজ (উদ্দেশ্য)
- **আরও সূক্ষ্মভাবে** (উপ-ফাংশন পরীক্ষা) বা **বিস্তৃতভাবে** (সংলগ্ন ফাংশনসমূহ) নির্ধারণ করা যাবে
- হুবহু একই কাজ হতে পারবে না
- উদাহরণ ঠিক আছে: রান 1 = "Watchdog-এ Thread-Safety", রান 5 = "Tray-এর সামগ্রিক Thread-Safety" (বিস্তৃত)
- উদাহরণ ঠিক আছে: রান 1 = "প্রসেস শনাক্তকরণ", রান 5 = "প্রসেস শনাক্তকরণে Store-Marker-Matching" (সূক্ষ্মতর)
- উদাহরণ ঠিক নয়: রান 1 = "Watchdog-এ Thread-Safety", রান 5 = "Watchdog-এ Thread-Safety" (অভিন্ন)

### নামকরণ
- এলাকাটি অনুসন্ধানের **আগে** নামকরণ করতে হবে (পরে বরাদ্দ করা যাবে না)
- ফরম্যাট: `"{Name}" ({typ}: code|aufgabe)`

## 4. চূড়ান্ত যাচাই

যখন zähler >= ziel এবং je_bug_gefunden উভয়ই সত্য হয়:

**ধাপ A — bugfix-protocol Phase 5:**
- [ ] সম্পূর্ণ টেস্ট-স্যুট সবুজ (`pytest`)
- [ ] **পরিবর্তিত এক্সিকিউশন-পাথ অন্তত একবার বাস্তবে চালান** — শুধু টেস্ট নয়। যে কোডের পরিবর্তিত স্থান আসলে কল করে না, তার সবুজ ইউনিট-টেস্ট হলো ভুয়া নিরাপত্তা। প্রকৃতপক্ষে পরিবর্তিত পাথটি চালান (ড্রাই-রান, স্মোক-রান, CLI-কল) এবং Tracebacks / সিগনেচার- / নামের ত্রুটি পরীক্ষা করুন। `py_compile` বা শুধু ইম্পোর্ট কেবল সিনট্যাক্স পরীক্ষা করে — পাথটি চলে কিনা তা নয়।
- [ ] **প্রতিটি ফিক্সের অন্তত একটি টেস্ট আছে যা সেটিকে স্পর্শ করে** — যে ফিক্সের পরিবর্তিত শাখা প্রকৃতপক্ষে ট্রিগার করে এমন টেস্ট ছাড়া ফিক্স অযাচাইকৃত গণ্য হয় (অর্কেস্ট্রেশন-/নেটওয়ার্ক-পাথের ক্ষেত্রে প্রয়োজনে Mock + Dry-Run একত্রিত করুন)।
- [ ] Type-Check (যদি কনফিগার করা থাকে)
- [ ] Lint (যদি কনফিগার করা থাকে)
- [ ] সেশন-ফিক্সগুলোর Edge Cases পরীক্ষা করা হয়েছে

**ধাপ B — রিভিউ (মডেল-নিয়ম):**
- **নতুন মডেল ক্লাস (যেমন Claude 5 / Fable-Klasse):** বাহ্যিক Advisor-/দ্বিতীয়-মডেল রিভিউ প্রয়োজন নেই।
  ধাপ A (টেস্ট + বাস্তব স্মোক-রান) হলো যাচাই। প্রকৃত অনিশ্চয়তায় ঐচ্ছিকভাবে: একটি তাজা রিভিউ-Subagent — তবে তার অনুসন্ধানগুলো বাগ হিসেবে গণ্য করার আগে পরীক্ষামূলকভাবে যাচাই করুন (অপরিবর্তিত কোডের বিপরীতে টেস্ট)।
  পটভূমি (সুইপ-অভিজ্ঞতা 2026-06-11): দ্বিতীয় রিভিউয়ার উপলব্ধ ছিল না, বিকল্প Subagent ১টি অনুসন্ধান দিয়েছিল (কনফিডেন্স 85), যা টেস্টের মাধ্যমে নন-বাগ প্রমাণিত হয়েছিল — বাহ্যিক রিভিউ ফলাফল বদলায়নি।
- **পুরোনো মডেল:** চূড়ান্ত আলোচনা Advisor-এর সাথে (ফ্যালব্যাক: দ্বিতীয় মডেল রিভিউয়ার হিসেবে); Advisor নিশ্চিত করে বা ফাঁক খুঁজে পায়।

**যাচাইয়ে বাগ পাওয়া গেলে:**
→ Fix + Test + Commit
→ RESET: zähler = 0, ziel = Grundrate (তাজা, কোনো দ্বিগুণকরণ নেই)
→ অনুসন্ধান লুপে ফিরে যান (geprüft-তালিকা থাকে, je_bug_gefunden = True)

**পরিষ্কার যাচাইয়ে:**
→ সমাপ্ত। Commit + Push। প্রোটোকল আউটপুট দিন।

## 5. প্রোটোকল (শেষে)

```markdown
## Bug-Sweep Ergebnis

- **Codebasis:** {LOC} LOC
- **Grundrate:** {Grundrate} (eskaliert: {ziel})
- **Geprüfte Bereiche:** {len(geprüft)}
- **Bugs gefunden:** {anzahl}
- **Resets:** {anzahl_resets}
- **Verdoppelung ausgelöst:** ja/nein
- **Fixes:**
  - {titel} — {commit_hash}
  - ...
- **Finale Test-Suite:** {passed}/{total} grün
- **Review-Verdict:** Selbstverifikation (neuere Modellklasse) / Advisor bestätigt / Lücken benannt
```

## কখন এই ওয়ার্কফ্লো ব্যবহার করবেন

- ফিচার ডেভেলপমেন্টের পরে (গুণমান নিশ্চিতকরণ)
- রিলিজের আগে (গ্রহণযোগ্যতা সুইপ)
- পর্যায়ক্রমে পরিচ্ছন্নতা-পরীক্ষা হিসেবে
- যখন ব্যবহারকারী `/bugsweep` টাইপ করেন

## অন্যান্য Skill-এর সাথে মিথস্ক্রিয়া

- **bugfix-protocol:** প্রতিটি পাওয়া বাগের জন্য ফিক্স-পদ্ধতি (Phase 4+5)
- **systematic-debugging:** সুইপের মধ্যে কঠিনভাবে পুনরুৎপাদনযোগ্য বাগের ক্ষেত্রে
- **code-review:** কাজ-এলাকা হিসেবে ব্যবহার করা যাবে

---

## পরিবর্তন-লগ (Changelog)

### 1.1.0 (2026-06-13)
- ধাপ B-এর মডেল-নিয়ম স্থানীয় Skill-ইনস্টলেশন (অবস্থা 2026-06-11) থেকে ফিরিয়ে আনা হয়েছে: নতুন মডেল ক্লাসগুলো টেস্ট + বাস্তব স্মোক-রান দিয়ে নিজেরাই যাচাই করে, বাহ্যিক রিভিউয়ের প্রয়োজন নেই; প্রোটোকল-ফিল্ড "Review-Verdict" সে অনুযায়ী প্রসারিত করা হয়েছে

### 1.0.0 (2026-06-13)
- Skill-লাইব্রেরিতে প্রথম প্রকাশ (স্থানীয় Skill-ইনস্টলেশন থেকে গৃহীত, অবস্থা 2026-06-01)
