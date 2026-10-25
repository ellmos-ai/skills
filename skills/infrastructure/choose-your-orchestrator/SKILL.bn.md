---
name: choose-your-orchestrator
version: 1.1.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-10-03
description: "ব্যবহারকারীর সাথে যৌথভাবে একটি উপযুক্ত ও সীমিত অর্কেস্ট্রেশন বেছে নিয়ে জটিল মাল্টি-এজেন্ট কাজের আগে একটি সংক্ষিপ্ত সেশন-চুক্তি তৈরি করে। /choose-your-orchestrator এ, অর্কেস্ট্রেটর, সোয়ার্ম, মডেল রাউটিং বা ব্যবহারকারী-পছন্দ মডেলের সংমিশ্রণ অনিশ্চিত হলে, এবং এজেন্ট প্রোগ্রামে মডেল স্লট, সমান্তরালতা, স্পন গভীরতা, লেখার সীমা, গ্রহণযোগ্যতা ও এস্কেলেশন স্পষ্টভাবে নির্ধারণ করতে হলে এই Skill ব্যবহার করুন।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: bn
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar, budgetierung]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 0b3feaa40d5c9d5310977fbc0e9c92572c1504e201baad19e7b73c7b64e4e846
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="choose-your-orchestrator banner">

# Choose Your Orchestrator

## উদ্দেশ্য

জটিল মাল্টি-এজেন্ট কাজের আগে প্রেক্ষাপটের শর্তগুলো স্পষ্ট করুন, বিদ্যমান Skill-এর ক্ষুদ্রতম কার্যকর সংমিশ্রণের সুপারিশ করুন এবং একটি বাধ্যতামূলক সেশন-অর্কেস্ট্রেশন চুক্তি প্রদান করুন। বর্তমান Runtime-এর Skill-প্রক্রিয়ার মাধ্যমে নির্বাচিত Skill লোড করুন এবং তাদের লাইভ নির্দেশনা অনুসরণ করুন। তাদের পদ্ধতি এই Skill-এ কপি করবেন না।

প্রতিনিধিত্ব কখনো কর্তৃত্ব বাড়ায় না। প্রকাশ, পাঠানো, মোছা, অর্থ প্রদান বা উৎপাদন পরিবর্তনের মতো বাহ্যিক বা অপ্রত্যাবর্তনযোগ্য কার্যক্রম ব্যবহারকারীর অনুমোদন-সাপেক্ষ (gated) থাকবে, যদি বর্তমান কাজ সেগুলো স্পষ্টভাবে অনুমোদন না করে।

## উপাদানসমূহ

| উপাদান | চুক্তিতে কাজ | যা এর কাজ নয় |
|---|---|---|
| `orchestrator` | কাজের প্যাকেজ, Scope, প্রমাণ ও গ্রহণযোগ্যতা | মডেল নির্বাচন বা সোয়ার্ম প্যাটার্ন উদ্ভাবন |
| `swarm-operations` | সোয়ার্ম প্যাটার্ন, ব্যয়-গেট এবং ঐচ্ছিক Matruschka স্তরবিন্যাস | একক কাজগুলোকে কৃত্রিমভাবে সমান্তরাল করা |
| `model-strategy` | লাইভ উপলব্ধতার ভিত্তিতে সক্ষমতা ও মডেল-সম্পর্কিত রুট | নির্দিষ্ট মডেল সংস্করণ বা অনুমতি আগে থেকে নির্ধারণ |
| `clutch` | ঐচ্ছিক বাহ্যিক রাউটিং প্রস্তাব | Dispatch বা Scope-এর একক কর্তৃপক্ষ |
| `decision-avatar` | প্রত্যাবর্তনযোগ্য অনিশ্চয়তায় ঐচ্ছিক অনুমোদিত পছন্দ-সংকেত | ব্যবহারকারীর অনুমোদন প্রতিস্থাপন বা কর্তৃত্ব বৃদ্ধি |
| `budgetierung` | ব্যয়বহুল মডেল/রিভিউয়ার/অ্যাডভাইজারের জন্য সময়-উইন্ডোভিত্তিক আলোচিত কোটা, অ্যাকাউন্ট এবং এস্কেলেশনের আগের প্রক্রিয়া | মডেল সক্ষমতা অনুযায়ী নির্বাচন (তা করে `model-strategy`) বা কোটা একতরফাভাবে নির্ধারণ |

`clutch route "<kurze Aufgabenbeschreibung>" --json` শুধু তখনই ব্যবহার করুন যখন `clutch` বাস্তবে উপলব্ধ। JSON উত্তরকে একটি প্রস্তাব হিসেবে বিবেচনা করুন এবং উপলব্ধ Runtime-স্লট, বাজেট, প্রকল্পের নিয়ম ও ব্যবহারকারীর সীমার সাথে মিলিয়ে দেখুন। `clutch` অনুপলব্ধ হলে বা তার আউটপুট অপাঠ্য হলে `model-strategy` এবং Runtime-এর লাইভ সক্ষমতা ব্যবহার করুন। চুক্তিতে বর্তমান মডেলের নাম বা সংস্করণ হার্ডকোড করবেন না।

## সুপারিশ-আলাপ

### ১. কাজটি শ্রেণিবদ্ধ করুন

লক্ষ্য, কাজের ধরন, সাফল্যের মানদণ্ড, নেতিবাচক Scope, বর্তমান অনুমতি, বিদ্যমান Lock এবং স্বাধীন কাজের প্যাকেজ চিহ্নিত করুন। প্রথমে নিচের টেবিল থেকে ক্ষুদ্রতম উপযুক্ত রুট-প্রস্তাবটি বেছে নিন।

### ২. চুক্তির প্রস্তাব

একটি সংক্ষিপ্ত খসড়া দেখান, যাতে থাকবে:

1. উপাদান ও ভূমিকা,
2. মডেল-/বাজেট-স্লট (বহু-ঘণ্টার রান বা সীমিত/ব্যয়বহুল মডেলের ক্ষেত্রে `budgetierung` মাধ্যমে আলোচনা করে হিসাব রাখুন),
3. সর্বাধিক সমান্তরালতা ও স্পন গভীরতা,
4. লেখার সীমা ও Lock,
5. গ্রহণযোগ্যতা ও প্রমাণ,
6. এস্কেলেশন ও ব্যবহারকারীর প্রশ্ন,
7. কর্তৃত্বের সীমা।

নির্দিষ্ট মান সুপারিশ করুন এবং এক বাক্যে প্রধান Trade-off উল্লেখ করুন। শুধু সেই সিদ্ধান্তগুলো জিজ্ঞাসা করুন যা ফলাফল বস্তুগতভাবে বদলায়। খোলা প্রশ্নগুলো সর্বোচ্চ তিনটি স্পষ্টভাবে আলাদা গোষ্ঠীতে সাজান; প্রতিটি গোষ্ঠীতে সুপারিশকৃত বিকল্পটি প্রথমে রাখুন। সব দিক ইতিমধ্যে স্পষ্টভাবে নির্ধারিত থাকলে আবার জিজ্ঞাসা করবেন না।

### ৩. নিশ্চিত করুন বা কমান

কোনো বস্তুগত বাজেট-, লেখা- বা কর্তৃত্ব-প্রশ্ন খোলা থাকলে Multi-Agent Dispatch শুরু করবেন না। শুধু সমান্তরালতার সুবিধা অস্পষ্ট হলে একক-এজেন্ট মোডে কমান। স্পষ্টভাবে অনুমোদিত কাজ নিরাপদ ডিফল্ট দিয়ে শুরু হতে পারে, যদি কোনো বস্তুগত ব্যবহারকারী-সিদ্ধান্ত বাকি না থাকে।

### ৪. চুক্তি প্রদান

নিশ্চিত চুক্তি Chat-এ প্রদান করুন। `usmc` কমান্ড উপলব্ধ হলে প্রথমে তার সহায়তা দেখুন এবং সেখানে নথিভুক্ত Note-/Write-কমান্ডের মাধ্যমে অতিরিক্তভাবে একটি গোপনীয়তা-নিরপেক্ষ সেশন-নোট লিখুন। নতুন Subcommand উদ্ভাবন করবেন না এবং কাঁচা প্রম্পট, Secret বা ব্যক্তিগত বিষয়বস্তু সংরক্ষণ করবেন না। উপলব্ধ USMC-লেখার পথ না থাকলে Chat-এর চুক্তিই কর্তৃত্বপূর্ণ।

## রাউটিং টেবিল

| কাজের ধরন | সুপারিশ | ডিফল্ট বিন্যাস |
|---|---|---|
| Audit / Sweep | `orchestrator` + `swarm-operations`; ভিন্ন সক্ষমতা-শ্রেণিতে `model-strategy` | স্বাধীন ক্ষেত্র, ছোট `parallel-chunks`- বা `specialist`-গোষ্ঠী, কেন্দ্রীয় Merge |
| Build-প্রোগ্রাম | `orchestrator` + `model-strategy`; সোয়ার্ম শুধু সত্যিকারের স্বাধীন ধারার জন্য | প্রধান পরিকল্পনা করে ও গ্রহণ করে, Worker পৃথক ক্ষেত্রে তৈরি করে |
| একক Build | একক-এজেন্ট মোড; ঐচ্ছিকভাবে রুটের জন্য `model-strategy` বা `clutch` | সোয়ার্ম বা হায়ারার্কির অতিরিক্ত ব্যয় নেই |
| Ticket-পরিচালনা | Ticket-System নেতৃত্বে থাকে; `orchestrator` কাজের চুক্তি ও প্রমাণ যোগ করে | বিদ্যমান Router-/Score-ব্যবস্থা প্রতিস্থাপন না করা, Ticket-Lifecycle মেনে চলা |

## নিরাপদ ডিফল্ট

ব্যবহারকারী, Runtime বা প্রকল্পের নিয়ম কঠোরতর কিছু না বললে এই মানগুলো ব্যবহার করুন:

- সর্বাধিক দুটি সক্রিয় Worker; প্রথমে একটি শুরু করুন এবং দ্বিতীয়টির সুবিধা প্রমাণ করুন,
- Matruschka বন্ধ, সর্বাধিক স্পন গভীরতা `0`,
- স্পষ্ট অনুমোদন ছাড়া Worker-নিজস্ব Subagent নয়,
- প্রতি Repository বা স্পষ্টভাবে সীমাবদ্ধ ক্ষেত্রে একজন লেখক,
- প্রতিটি Write-এর আগে পৃথক ফাইল-Claim ও প্রকল্প-প্রচলিত Lock,
- প্রধান/Orchestrator নিজে Artefact, Diff ও Test যাচাই করে,
- সমাপ্তির বার্তা শুধু প্রমাণ গ্রহণের পরে বৈধ,
- অপ্রত্যাবর্তনযোগ্য বা বাহ্যিক কার্যক্রম ব্যবহারকারীর অনুমোদন-সাপেক্ষ (gated),
- অনিশ্চয়তা একাধিক ছোট বাধা হিসেবে নয়, একত্রে জানানো হবে।

Matruschka তখনই সক্রিয় করুন যখন ব্যবহারকারী তা স্পষ্টভাবে নিশ্চিত করেন এবং চুক্তিতে প্রতি স্তরের মডেল-/সক্ষমতা-শ্রেণি, সক্রিয় স্লট-সীমা, অনুমোদিত উপ-কাজ ও সর্বাধিক গভীরতা উল্লেখ থাকে। শুধু উপস্থিত নয়, সক্রিয় এজেন্ট গণনা করুন। এমনকি তখনও প্রতি ক্ষেত্রে ঠিক একজন লেখক থাকবে।

## চুক্তির বিন্যাস

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze; Budget/Konto: <budgetierung-Konto, Pfad>>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## উদাহরণ

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## থামার শর্ত

Scope overlap করলে, Lock অস্পষ্ট হলে, Runtime প্রস্তাবিত স্লট না দিলে, বাজেট নিশ্চিত না হলে, বা স্বাধীনভাবে গ্রহণযোগ্যতা প্রমাণ করা না গেলে অর্কেস্ট্রেশন থামান বা কমান। নতুন পণ্য, গোপনীয়তা বা কর্তৃত্বের সিদ্ধান্ত অনুমান না করে ব্যবহারকারীকে জিজ্ঞাসা করুন।

## পরিবর্তনের ইতিহাস

### 1.1.0 (2026-10-03)
- মডেল-কোটা/অ্যাকাউন্টের জন্য আলোচিত উপাদান হিসেবে `budgetierung` যোগ করা হয়েছে
  (উপাদান-টেবিল, চুক্তি-আলাপে মডেল-/বাজেট-স্লট, চুক্তি-বিন্যাসে Worker-স্লট সারি)।

### 1.0.0 (2026-08-20)
- সুপারিশ-আলাপ, রাউটিং টেবিল ও সংক্ষিপ্ত সেশন-চুক্তি প্রবর্তিত।
- সমান্তরালতা, Matruschka, লেখার সীমা, প্রমাণ ও বাহ্যিক কার্যক্রমের জন্য নিরাপদ ডিফল্ট নির্ধারিত।
- `clutch` এবং একটি অনুমোদিত পছন্দ-মডেলের ঐচ্ছিক সংযোজন বর্ণিত, স্থির মডেল-বন্ধন বা কর্তৃত্ব-বৃদ্ধি ছাড়া।
