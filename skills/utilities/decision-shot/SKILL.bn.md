---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: "একটি সিদ্ধান্ত বা সিদ্ধান্ত-গোষ্ঠীর জন্য অত্যন্ত সংক্ষিপ্ত, অর্থবহ আউটপুট-ফরম্যাট, যখন এর পেছনের বিশ্লেষণ ইতিমধ্যে বিদ্যমান (চ্যাটে তৈরি, `decide` থেকে, `decision-briefing` থেকে, একটি টিকিট বা নথি থেকে): 2-3 লাইনে প্রেক্ষাপট, প্রতিটি বিকল্পের জন্য paveman/caveman-সংক্ষিপ্ত শৈলীতে Pro/Contra বুলেট, Talking Points, একটি যুক্তিসম্মত সুপারিশ, এবং সম্পূর্ণ পড়ার জন্য পূর্ণ বিশ্লেষণের পাথ/লিংক। এই স্কিল ব্যবহার করুন যখন \"এটা সংক্ষেপে Pro Contra ও সুপারিশসহ দাও\", \"সিদ্ধান্তের executive summary\", \"<Thema>-এর কুর্তপ্রেক্ষাপট\", \"সিদ্ধান্ত X-কে সংক্ষিপ্ত আকারে সারসংক্ষেপ করো\", /decision-shot, অথবা কোনো ফলাফল এমন কাউকে হস্তান্তর করতে হবে যার শুধু মূল সারকথা দরকার, সম্পূর্ণ যুক্তি নয়। এটি ব্যবহার করবেন না অনেক খোলা সিদ্ধান্ত সংগ্রহ করে অক্ষর দিয়ে জিজ্ঞাসা করতে -- সেটা করে decision-briefing; এবং সিদ্ধান্তকে প্রথমে বিশ্লেষণ করতে -- সেটা করে decide। decision-shot একটি তৈরি বিশ্লেষণ ধরে নেয় এবং শুধু তার উপস্থাপনাকে সংক্ষিপ্ত করে।"
visibility: public
language: bn
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
translated_from_sha256: 26ff135e844d526543d9f5df212d36e408a427a71cc13a9e744a55abdb5ed991
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.494554+00:00"
---
<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> বিশ্লেষণ হয়ে গেছে। এখন দরকার দ্বিতীয় যুক্তি নয়, বরং সারকথা এবং সম্পূর্ণ বিষয়ে ফিরে যাওয়ার পথ।

## কখন ব্যবহার করবেন

- একটি সিদ্ধান্ত (বা একটি ঘনিষ্ঠভাবে সম্পর্কিত গোষ্ঠী, যেমন একই বিষয়ের একাধিক উপপ্রশ্ন) ইতিমধ্যে ভেবে দেখা হয়েছে -- চ্যাটে, একটি টিকিটে, `decide`-ফ্রেমওয়ার্কে বা `decision-briefing`-এর Phase 2-তে -- এবং এখন সেটি কাউকে (ব্যবহারকারী, অন্য এজেন্ট, একটি হস্তান্তর-নথি) কয়েক সেকেন্ডে বোধগম্য করতে হবে।
- ট্রিগার-শব্দ: "সংক্ষেপে Pro Contra দাও", "executive summary", "কুর্তপ্রেক্ষাপট", "এ বিষয়ে talking points", "সংক্ষিপ্ত আকারে সুপারিশসহ দাও", `/decision-shot`।
- **না** যখন একাধিক এখনও খোলা, অমীমাংসিত বিষয় আছে যা ব্যবহারকারী একের পর এক/ব্যাচে অক্ষর দিয়ে উত্তর দেবেন -- সেটা [decision-briefing](../decision-briefing/SKILL.md)। **না**, সিদ্ধান্ত প্রথমে তৈরি করতে -- সেটা [decide](../decide/SKILL.md)। decision-shot কেবল একটি ইতিমধ্যে উপস্থিত বিশ্লেষণের উপস্থাপনা।

## পার্থক্য (সংক্ষেপে)

| স্কিল | কী করে | কখন সম্পন্ন |
|---|---|---|
| `decide` | একটি ফ্রেমওয়ার্ক দিয়ে একটি সিদ্ধান্ত তৈরি করে (Pro/Con-ম্যাট্রিক্স, Weighted Scoring, Decision Tree, ...) | বিশ্লেষণ এখনও বাকি |
| `decision-briefing` | একটি বিষয়ের অনেক খোলা সিদ্ধান্ত সংগ্রহ করে, A/B/C/D-ব্যাচ হিসেবে উপস্থাপন করে, অক্ষর-উত্তর গ্রহণ করে | একাধিক বিষয় এখনও অমীমাংসিত |
| `decision-shot` | একটি তৈরি বিশ্লেষণ (যেখান থেকেই আসুক) একটি executive সংক্ষিপ্ত রূপে ঘনীভূত করে পূর্ণ সংস্করণের লিংকসহ | বিশ্লেষণ আগেই আছে, শুধু উপস্থাপনা বাকি |
| `knappform` | সেশনের প্রতিটি উত্তরের জন্য সাধারণ উত্তর-শৈলী পরিবর্তক | সেশনজুড়ে, বিষয়-নিরপেক্ষ |
| `paveman` | বিদ্যমান গদ্য-ফাইল (নিয়ম-/মেমরি-ফাইল) নির্ধারকভাবে সংক্ষিপ্ত করে | একটি ফাইল সংক্ষিপ্ত করে, চ্যাট-আউটপুট নয় |

`decision-shot` এই চারটির কোনোটির সাথে প্রতিযোগিতা করে না -- এটি সেই ফরম্যাট যা `decide`-এর পরে বা `decision-briefing`-এর পাশে ব্যবহৃত হয়, যখন সারকথা হস্তান্তর করতে হয়। সংক্ষিপ্ত ভাষাশৈলী `knappform`/`paveman`-কে অনুসরণ করে (সম্পূর্ণ বর্জন-তালিকার জন্য সেখানে দেখুন), তবে এখানে একটি স্থির পাঁচ-অংশের ফরম্যাটে ধারাবাহিকভাবে প্রয়োগ করা হয়।

## ফরম্যাট (বাধ্যতামূলক, পাঁচ অংশ)

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## নিয়মাবলি

- **ব্যবহারকারীর লেখায় প্রযুক্তিগত নম্বর/সংক্ষেপ নেই (সাধারণ ভাষায় আমি-রূপ):** মানুষের জন্য দৃশ্যমান লেখায় (শিরোনাম, প্রেক্ষাপট, বিকল্প, Talking Points, সুপারিশ) কোনো **অভ্যন্তরীণ** সংক্ষেপ, টিকিট-নম্বর (`T-...`), D-শনাক্তকারী বা আপেক্ষিক ফাইল-পাথ থাকবে না।
  প্রেক্ষাপট পরিস্থিতি ও পরিকল্পিত পদক্ষেপ আমি-রূপে বর্ণনা করবে ("আমি প্রস্তাব করছি...")।
  প্রযুক্তিগত রেফারেন্স (টিকিট-ID, সুনির্দিষ্ট ফাইল-পাথ) কেবল শেষ লাইন `**Vollanalyse:**`-এ বা একটি রেফারেন্স-টেবিলে থাকবে।
- **লাইন হলো বাজেট, লক্ষ্য নয়।** 2-3 লাইন প্রেক্ষাপট, প্রতি বিকল্পে 2-4 বুলেট, 2-3 Talking Points, 1 বাক্য সুপারিশ -- বেশি হলে বাদ যাবে, সংক্ষিপ্ত করে রাখা হবে না। কোনো বিকল্প 4 বুলেটে না ধরলে তা এই স্কিলে নয়, পূর্ণ বিশ্লেষণে যাবে।
- **`knappform`/`paveman`-এর মতো সংক্ষিপ্ত শৈলী:** কোনো ফাঁকা শব্দ, ভূমিকা-বাক্য বা এড়িয়ে যাওয়া নয়। নেতিবাচক শব্দ (`nicht`, `nie`, `kein`, `nur`, `außer`) অক্ষত থাকবে -- এগুলো বাদ দিলে বক্তব্য উল্টে যায়।
- **Pro/Contra হলো বুলেট, বাক্য নয়।** `+`/`-` উপসর্গ হিসেবে, প্রতি লাইনে একটি চিন্তা, কোনো অনুবর্তী বাক্য নয়।
- **Talking Points যোগাযোগমূলক, বিশ্লেষণমূলক নয়।** এগুলো উত্তর দেয় "কেউ জিজ্ঞাসা করলে আমি কী বলব" -- "বিশ্লেষণে কী লেখা আছে" নয়। Pro/Contra তালিকার পুনরাবৃত্তি ইঙ্গিত দেয় যে এখনও ঘনীভূত করা হয়নি।
- **সুপারিশ নিজেই এক বাক্যে যুক্তি দেয়।** Pro-তালিকার পুনরাবৃত্তি নয়, "উপরে দেখুন" নয় -- এক বাক্যটি বাকি ব্লক ছাড়াও দাঁড়াতে হবে।
- **সম্পূর্ণ বিশ্লেষণের লিংক/পাথ বাধ্যতামূলক, ঐচ্ছিক নয়।** decision-shot বিশ্লেষণকে প্রতিস্থাপন করে না, এটি শুধু দ্রুত খুঁজে পেতে সাহায্য করে। যদি কোনো স্পষ্ট উৎস না থাকে (কেবল মৌখিকভাবে চ্যাটে তৈরি, কোনো নথি নেই), চ্যাট-/সেশন-সংশ্লিষ্টতা যতটা সম্ভব সুনির্দিষ্টভাবে উল্লেখ করুন (যেমন "এই সেশন, F4-এর উত্তর") ক্ষেত্রটি খালি না রেখে।
- **একাধিক সম্পর্কিত সিদ্ধান্ত** (গোষ্ঠী, যেমন একটি বিষয়ের একাধিক উপপ্রশ্ন): প্রতি সিদ্ধান্তের জন্য একটি ব্লক, `---` দিয়ে পৃথক; সাধারণ প্রেক্ষাপট শুধু একবার শুরুতে, যদি তা সত্যিই সবার জন্য প্রযোজ্য হয়।

### সংরক্ষিত Decision-Shot-এ সেশন-উৎস

যখন Decision-Shot একটি গুরুত্বপূর্ণ নতুন, স্থায়ী আর্টিফ্যাক্ট হিসেবে সংরক্ষিত হয়, ফাইলটি শেষ হবে এভাবে:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

সেশন-ID প্রথমে একটি স্পষ্ট রানটাইম/CLI-মান থেকে আসে, এরপর একটি কর্তৃত্বপূর্ণ প্রোভাইডার-পরিবেশ বা হুক থেকে; দুটোই না থাকলে `unbekannt` লেখা হয়। মান কখনো অনুমান করা হয় না। সাব-এজেন্ট প্যারেন্ট সেশন ব্যবহার করে। রুটিন চ্যাট, উৎস, নীতি, `CLAUDE.md`, README ও পুরোনো ফাইলে ঢালাওভাবে স্ট্যাম্প বা পুনঃস্ট্যাম্প দেওয়া হয় না।

## উদাহরণ

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## পরিবর্তন-ইতিহাস

### 1.2.0 (2026-09-18)
- বোধগম্য সিদ্ধান্ত-লেখার জন্য শৈলী-নিয়ম যুক্ত (T-20260913-883789445, ব্যবহারকারীর নির্দেশ 2026-09-13):
  - দৃশ্যমান লেখায় (শিরোনাম, প্রেক্ষাপট, Talking Points) টিকিট-নম্বর, D-শনাক্তকারী বা অভ্যন্তরীণ পাথ নেই।
  - প্রেক্ষাপট ও সুপারিশ সাধারণ ভাষায়, আমি-রূপে।
  - প্রযুক্তিগত টিকিট ও পাথ-রেফারেন্স কঠোরভাবে শেষ সম্পূর্ণ-বিশ্লেষণ লাইনে সীমাবদ্ধ।

### 1.1.0 (2026-09-09)
- P-018 যুক্ত: গুরুত্বপূর্ণ নতুন সংরক্ষিত Decision-Shot-এর জন্য সেশন-স্ট্যাম্প, সংকীর্ণ উৎস-অগ্রাধিকার ও বর্জনসহ।

### 1.0.0 (2026-08-24)
- প্রথম সংস্করণ।
