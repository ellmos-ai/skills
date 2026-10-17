---
name: software-testing
version: 1.0.1
type: knowledge-protocol
author: Lukas Geiger
created: 2026-08-22
updated: 2026-08-22
description: "সফটওয়্যার প্রকল্পের জন্য টেস্ট-কৌশল পরামর্শদাতা — পরিস্থিতি এবং SDLC-/CI-পর্যায় অনুযায়ী সঠিক টেস্ট-স্তর (Unit/Integration/System/Abnahme), টেস্টের ধরন (funktional, nicht-funktional, änderungsbezogen) এবং টেস্ট-ডিজাইন পদ্ধতি (Äquivalenzklassen, Grenzwerte, Entscheidungstabellen, explorativ) নির্বাচন করে, এর মধ্যে টেস্ট-পিরামিড, CI/CD-Gates, Shift-Left এবং সেরা অনুশীলনও অন্তর্ভুক্ত। টেস্ট লেখা, পরিকল্পনা, অগ্রাধিকার নির্ধারণ বা মূল্যায়ন করতে হলে এই Skill সর্বদা ব্যবহার করুন — \"টেস্ট লিখুন\", \"টেস্ট-কৌশল\", \"টেস্ট প্ল্যান\", \"কী/কীভাবে টেস্ট করব\", \"schreibe Tests\", \"Teststrategie\", \"Testplan\", \"Testkonzept\", \"was/wie soll ich testen\", \"welche Tests fehlen\", \"Testabdeckung verbessern\", \"QA aufsetzen\", Regression/Smoke/Sanity/Last/Stress/Security-Tests সম্পর্কিত প্রশ্ন বা Test-Pipeline সেটআপের সময় — যদিও \"Test\" কথাটি শুধু প্রাসঙ্গিকভাবে আসে। সীমানা — TDD-লুপের জন্য superpowers:test-driven-development, বাগ-ডায়াগনসিসের জন্য bugfix-protocol, এবং পদ্ধতিগত বাগ-অনুসন্ধানের জন্য bugsweep ব্যবহার করুন।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [testing, teststrategie, qa, unit-test, integration, regression, testpyramide, shift-left, ci-cd, istqb]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'claude-code-recherche', 'origin_version': '1.0.0', 'created_from': 'Online-Recherche 2026-08-22 (ISTQB-Systematik, Testpyramide, Agile Testing Quadrants, moderne Verfahren); Quellen siehe testarten-katalog.md'}
translated_from_sha256: 85a9672454c8df2d2e0dfd1a87d5468a7ebc030e45a1fa2843f361bba80c8b80
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T02:34:25.375180+00:00"
---
<img src="banner.png" width="100%" alt="software-testing banner">

# Software-Testing: টেস্ট-কৌশল ও টেস্ট-নির্বাচন

এই Skill প্রশ্নের উত্তর দেয় **„আমার এখানে, এখন, কোন কোন টেস্ট দরকার, এবং কেন?"** —
অনুমানের বদলে পদ্ধতিগতভাবে। এটি সিদ্ধান্ত-যুক্তি প্রদান করে; সব টেস্ট-ধরন, পদ্ধতি ও
সংজ্ঞার সম্পূর্ণ তালিকা একই ফোল্ডারের `testarten-katalog.md`-এ রয়েছে (বিস্তারিত প্রশ্নে সেখানে দেখুন)।

---

## 1. কাঠামো: তিন মাত্রায় চিন্তা করুন

টেস্ট পরিকল্পনা বা লেখার আগে কাজটিকে তিনটি অক্ষে স্থাপন করুন (ISTQB)।
যে শুধু „একটি টেস্ট-তালিকা" রাখে, সে অক্ষগুলো মিশিয়ে ফেলে এবং অসম্পূর্ণ পরিকল্পনা করে:

| অক্ষ | প্রশ্ন | ধরন |
|---|---|---|
| **Teststufe (টেস্ট-স্তর)** | কোন স্তরে? | Unit → Integration → System → Abnahme |
| **Testart (টেস্টের ধরন)** | কোন বৈশিষ্ট্য? | funktional / nicht-funktional / strukturbezogen / änderungsbezogen |
| **Testverfahren (টেস্ট-পদ্ধতি)** | টেস্ট-কেসগুলো কীভাবে তৈরি হয়? | Black-Box / White-Box / erfahrungsbasiert |

এর সাথে আড়াআড়ি: **statisch** (Reviews, statische Analyse — কার্যকর না করেই, সবচেয়ে আগে ও সস্তায় ত্রুটি খোঁজা) বনাম **dynamisch** (কোড চালানো হয়)।

---

## 2. পরিস্থিতি-রাউটার: কী সামনে আছে?

প্রকৃত পরিস্থিতি অনুযায়ী শুরুর বিন্দু বেছে নিন:

| পরিস্থিতি | করণীয় |
|---|---|
| **নতুন Feature বানানো** | কোড লেখার আগে Abnahme-Kriterien স্পষ্ট করুন (ATDD/BDD-চিন্তাধারা)। বাস্তবায়নের সাথে সমান্তরালে Unit-Tests (Äquivalenzklassen + Grenzwerte)। নতুন ইন্টারফেসের জন্য Integrationstest। শুধু একটি E2E-Happy-Path, এর বেশি নয়। |
| **Bug ফিক্স করা** | প্রথমে বাগ পুনরুৎপাদনকারী টেস্ট (rot), তারপর Fix (grün) = **Re-Test**। এরপর পরিবেশের **Regression**। নিজের Diagnose → `bugfix-protocol`। |
| **Refactoring** | কোনো নতুন Feature-Tests নয় — বিদ্যমান Suite-ই নিরাপত্তা-জাল। আগে যাচাই করুন Suite আচরণটি সত্যিই ঢেকেছে কি না (প্রয়োজনে ক্যারেক্টারাইজেশন টেস্ট যোগ করুন)। Coverage/Mutation কে ঘাটতির সূচক হিসেবে ব্যবহার করুন। |
| **টেস্ট-বিহীন Legacy-Code** | প্রতিটি ফাংশনের Unit-Tests দিয়ে শুরু করবেন না। প্রথমে System-/API-স্তরে বিদ্যমান আচরণের উপর ক্যারেক্টারাইজেশন টেস্ট বসান, তারপর যখন কোনো অংশে হাত দেবেন তখন Unit-Tests যোগ করুন। |
| **API / Microservices** | Service-স্তরে API-Tests-এ জোর দিন (পিরামিডের মধ্যম স্তর)। আলাদা টিম/Deployment হলে একসাথে Staging-Integrationstests-এর বদলে **Contract Testing** (যেমন Pact)। |
| **Release প্রস্তুতি** | ক্রম: Smoke (Build স্থিতিশীল?) → পূর্ণ Regression → nicht-funktionale Tests (Last, Security) → UAT/Abnahme → Release-Kandidat-এ Smoke। |
| **Performance-উদ্বেগ** | আগে একটি পরিমাপযোগ্য লক্ষ্য নির্ধারণ করুন (যেমন „P95 < 300 ms, 1,000 ব্যবহারকারীতে"), নইলে কোনো টেস্টের ফলাফল মূল্যায়ন করা যাবে না। Lasttest = স্বাভাবিক লোড, Stresstest = ভাঙনবিন্দু + পুনরুদ্ধার। উৎপাদনের কাছাকাছি পরিবেশ বাধ্যতামূলক। |
| **Test-Pipeline সেটআপ** | Abschnitt 4-এর CI/CD-Gates বাস্তবায়ন করুন; প্রতি Commit-এ Unit + Lint দিয়ে শুরু করে ধাপে ধাপে বাড়ান। |
| **Teststrategie/Testkonzept লেখা** | 3 মাত্রা + Phasen-Mapping (Abschnitt 4) + ঝুঁকি-ভিত্তিক অগ্রাধিকার (Abschnitt 6, Punkt 10) অনুযায়ী কাঠামো গড়ুন। |

---

## 3. Teststufen: বিষয়বস্তু, লক্ষ্য, সময়

| স্তর | যাচাই করে | কখন | মোটা নিয়ম |
|---|---|---|---|
| **Unit/Komponente** | একটি ফাংশন/ক্লাস আলাদাভাবে (Mocks/Stubs সহ) | Implementierung চলাকালীন, প্রতি Commit | Pyramide-এর বিস্তৃত ভিত্তি; দ্রুত (< সেকেন্ড), নির্ধারণবাদী |
| **Integration** | পারস্পরিক ক্রিয়া, Schnittstellen, DB-সংযোগ | Unit-Tests-এর পরে, প্রতি Merge-এ | ধাপে ধাপে ইন্টিগ্রেট করুন (Top-Down/Bottom-Up), বড় সিস্টেমে কখনো Big Bang নয় |
| **System** | পুরো সিস্টেম technische Anforderungen-এর বিপরীতে | ইন্টিগ্রেটেড Build তৈরি হলেই | Funktional এবং nicht-funktional উভয়ই; স্বাধীন Tester মূল্যবান |
| **Abnahme** | ব্যবসায়িক প্রত্যাশা, বাস্তব ব্যবহার | Go-Live-এর আগের শেষ স্তর | ব্যবসায়িক বিভাগের দ্বারা UAT; পরিচালনাগত দিক (Backup/Deploy/Monitoring) ভুলবেন না; প্রয়োজনে Alpha/Beta |

**Testpyramide** একটি অনুপাত হিসেবে: অনেক Unit-, লক্ষ্যভিত্তিক Integrations-/API-, কম E2E-Tests (শুরুর বিন্দু হিসেবে আনুমানিক ~70/20/10 — প্রকৃত ত্রুটির উৎস দেখে সমন্বয় করুন)। উল্টো পিরামিড (অনেক UI-Tests) = ধীর + flaky → এড়িয়ে চলুন।

---

## 4. Phasen-Mapping: কখন কী যাচাই করবেন?

### CI/CD-Gates (আধুনিক স্ট্যান্ডার্ড-ম্যাপিং)

| Pipeline-স্তর | Gate |
|---|---|
| প্রতি Commit | Unit-Tests, Linter, statische Analyse (সেকেন্ড–মিনিট) |
| Pull Request | Code-Review, SAST/SCA, লক্ষ্যভিত্তিক Komponententests |
| Merge | Integrations-/API-/Contract-Tests, Testumgebung-এ Smoke |
| Nightly / Pre-Release | পূর্ণ Regression, E2E, Performance-/Lasttests, DAST |
| Release-Kandidat | Staging-এ Smoke, UAT, Abnahme |
| Produktion (Shift-Right) | Monitoring/Observability, Canary/Blue-Green, Feature Flags, প্রয়োজনে Chaos-Experimente |

**সময়-বাজেট ও Blockier-Regeln (অনুশীলন থেকে আনুমানিক মান):**

- **Commit থেকে Feedback < 10 মিনিট** দ্রুত পথের জন্য (Lint + Unit + গুরুত্বপূর্ণ Integrationstests); Staging পর্যন্ত মোট Pipeline **< 30–45 মিনিট**; পূর্ণ Regression nightly বা Release-এর আগে। যে নিয়ন্ত্রণ-চক্র এর চেয়ে ধীরে চলে, তাকে এড়িয়ে যাওয়া হয়।
- **Blockierend বনাম meldend:** Unit-, Integrations- ও Smoke-Gates সর্বদা ব্লক করে (লাল হলে কোনো Merge/Deploy নয়)। Nightly-স্তর (Regression, Last, DAST) Ticket/Fix-এর মাধ্যমে জানায়, কিন্তু প্রতিটি Commit ব্লক করে না। Prod-Deploy-এর পরে: Smoke + Monitoring — লাল হলে Rollback + Incident।
- **হস্তান্তর-বিন্দু:** Commit (git push) Inner Loop (লোকাল: TDD, Unit, দ্রুত পুনরাবৃত্তি) কে Outer Loop (Gates সহ শেয়ার্ড Pipeline) থেকে আলাদা করে। যা Inner Loop-এ সরানো যায়, সেখানে সবচেয়ে সস্তায় ধরা পড়ে (Shift-Left)।

### ক্লাসিক (V-Modell): স্পেসিফিকেশনের সময় টেস্ট ডিজাইন করা

Anforderungen↔Abnahmetest · Systemdesign↔Systemtest · Architektur↔Integrationstest ·
Code↔Unit-Test। মূল ধারণা: একটি স্তরের টেস্টগুলো **সংশ্লিষ্ট স্পেসিফিকেশন তৈরির সময়** ডিজাইন করা হয় — শেষে নয়। Anforderungen/Designs-এর Reviews (statisches Testen) হলো সবচেয়ে আগের ত্রুটি-সন্ধান।

### Agile Testing Quadrants (Sprint-পরিকল্পনার গ্রিড)

Q1 Unit/TDD + Q2 Story-Tests/BDD ধারাবাহিকভাবে চলে এবং ত্রুটি **প্রতিরোধ** করে;
Q3 explorativ/Usability/UAT + Q4 Performance/Security পণ্যকে **মূল্যায়ন** করে, যখন পর্যাপ্ত পণ্য তৈরি হয়। বিস্তারিত ক্যাটালগে।

---

## 5. টেস্ট-ডিজাইন পদ্ধতি নির্বাচন

| টেস্ট-ভিত্তি যদি … | … তবে পদ্ধতি |
|---|---|
| ইনপুট-পরিসর/মানের সেট থাকে | **Äquivalenzklassen** (প্রতি শ্রেণি থেকে একটি প্রতিনিধি) + **Grenzwertanalyse** (প্রতিটি সীমায় এবং সীমার ঠিক বাইরে: 5–50-এর ক্ষেত্রে 4, 5, 50, 51 পরীক্ষা) — প্রায় প্রতিটি Unit-Test-এর মৌলিক সরঞ্জাম |
| জটিল ব্যবসায়িক নিয়ম/শর্ত-সংমিশ্রণ থাকে | **Entscheidungstabellentest** |
| অবস্থা ও রূপান্তর থাকে (Workflow, Session, Gerät) | **Zustandsübergangstest** (নিষিদ্ধ রূপান্তরও পরীক্ষা করুন) |
| ব্যবহারকারীর প্রবাহ বর্ণনা করে | **Use-Case-/Szenariotest** সহ ত্রুটি- ও ব্যতিক্রম-পথ |
| কোড আছে এবং কভারেজ মাপতে হবে | **Anweisungs-/Zweigüberdeckung** — ঘাটতির সূচক হিসেবে, লক্ষ্য হিসেবে নয় (100 % Coverage ≠ সঠিক) |
| অস্পষ্ট/অসম্পূর্ণ বা সময় কম | **Exploratives Testen** (Charter সহ সময়-সীমাবদ্ধ Sessions) + **Error Guessing** (Null, খালি স্ট্রিং, বিশেষ অক্ষর, সময়ক্ষেত্র, Race Conditions) |

পদ্ধতিগত পদ্ধতি আগে, অভিজ্ঞতাভিত্তিক পদ্ধতি ইচ্ছাকৃতভাবে **পরিপূরক** হিসেবে — এগুলো সেই ত্রুটি খুঁজে পায়, যা স্ক্রিপ্ট এড়িয়ে যায়।

---

## 6. সেরা অনুশীলন (টেস্ট পরিকল্পনা/রিভিউয়ের চেকলিস্ট)

1. **Shift-Left:** Anforderungsphase থেকে Reviews + statische Analyse — ত্রুটি যত দেরিতে ধরা পড়ে, তত ব্যয়বহুল (Boehm-এর অনুসরণে প্রচলিত মোটা নিয়ম; দিক নিয়ে মতভেদ নেই, সঠিক গুণক নিয়ে বিতর্ক আছে)।
2. **Testpyramide মেনে চলুন** — E2E-Tests সংযত, Unit-ভিত্তি বিস্তৃত।
3. **যা বারবার হয়, তা স্বয়ংক্রিয় করুন** (Smoke, Regression, API, Unit) এবং CI/CD-Gates-এ স্থাপন করুন; ম্যানুয়াল সক্ষমতা explorativ + Usability-এর জন্য রাখুন।
4. **টেস্ট-কেস পদ্ধতিগতভাবে ডিজাইন করুন** (Abschnitt 5), এলোমেলোভাবে নয়।
5. **নন-ফাংশনাল প্রয়োজনীয়তা পরিমাপযোগ্য করুন** — সংখ্যাগত লক্ষ্য ছাড়া কোনো মূল্যায়নযোগ্য Performance-/Lasttest হয় না।
6. **Re-Test ≠ Regression:** আগে Fix নিশ্চিত করুন, তারপর পার্শ্বপ্রতিক্রিয়া। ক্রম Smoke → Sanity/Re-Test → Regression।
7. **Flaky Tests অবিলম্বে মোকাবিলা করুন** — কোয়ারেন্টাইন, কারণ ঠিক করুন বা মুছে ফেলুন; অস্থির Suites Pipeline-এর উপর আস্থা নষ্ট করে।
8. **Testdaten/-umgebungen পরিচালনা করুন:** পুনরুৎপাদনযোগ্য (Container/IaC), উৎপাদনের কাছাকাছি, বেনামী বা সিন্থেটিক ডেটা।
9. **টেস্টের গুণমান নিজেই মাপুন:** Coverage ঘাটতির সূচক হিসেবে; যেখানে Coverage-সংখ্যা প্রতারণা করতে পারে সেখানে **Mutation Testing**।
10. **ঝুঁকি-ভিত্তিক অগ্রাধিকার:** ব্যর্থতার প্রভাব × ত্রুটির সম্ভাবনা অনুযায়ী টেস্টের গভীরতা — সমানভাবে বণ্টন নয়।
11. **গুণমান দলের দায়িত্ব** (Whole-Team-Approach): Anforderungen-এ Tester আগে থেকে যুক্ত করুন; BDD/ATDD-কে ব্যবসায়িক বিভাগের সাথে যৌথ বাহন হিসেবে ব্যবহার করুন।
12. **Shift-Right ভুলবেন না:** Monitoring, Canary, Feature Flags; পরিণত Observability-এর পরেই Chaos Engineering।

---

## 7. আধুনিক পদ্ধতি — কখন অতিরিক্ত ব্যবহার করবেন

| পদ্ধতি | কখন ব্যবহার করবেন … |
|---|---|
| **Contract Testing** (Pact) | আলাদা Deployment/টিমে Microservices থাকলে |
| **Mutation Testing** (Stryker, PIT, mutmut) | বিদ্যমান টেস্ট-Suite-এর মান মূল্যায়ন করতে হলে |
| **Property-Based Testing** (Hypothesis, fast-check) | অপরিবর্তনীয় নিয়ম আছে („সাজানো idempotent") এবং প্রান্তিক ক্ষেত্রের ভয় থাকলে |
| **Fuzzing** | Parser, Deserialisierung, নিরাপত্তা-সংবেদনশীল ইনপুট |
| **Chaos Engineering** | বণ্টিত সিস্টেম + পরিণত Observability + পরিষ্কার Rollbacks |

---

## প্রতিবেশী Skills (পুনরাবৃত্তি করবেন না)

- **`superpowers:test-driven-development`** — কোড লেখার সময় নির্দিষ্ট Red-Green-Refactor-লুপ।
- **`bugfix-protocol`** — একটি নির্দিষ্ট বাগের 6-পর্যায়ের ডায়াগনসিস।
- **`bugsweep`** — একটি কোডবেস জুড়ে পদ্ধতিগত বাগ-অনুসন্ধান।
- **`dev-cycle`** — 8-পর্যায়ের সামগ্রিক চক্র (v1.2.0 থেকে: Tests পর্যায় 1/3/5-এ ডিজাইন, পর্যায় 6-এ লেখা এবং পর্যায় 7-এ চালানো হয়; এই Skill পূরণ করে কোন Tests কোথায় চলবে)।

## রেফারেন্স

সম্পূর্ণ ক্যাটালগ (সব Teststufen, Testarten সহ nicht-funktionaler বিস্তারিত সারণি, সব Entwurfsverfahren, Agile Quadrants, statisch/dynamisch, V-Modell, উৎস):
→ `testarten-katalog.md` (একই ফোল্ডারে)

দৃশ্যমান সামগ্রিক মানচিত্র — ধাপ, নিয়ন্ত্রণ-চক্র, ভূমিকা এবং Test-Gates „সফটওয়্যার উন্নয়নের সার্কিট-ডায়াগ্রাম" হিসেবে (Blatt BL-5 = Test-সংযোগ, BL-2 = Regelkreis-Takte):
→ `../dev-cycle/SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (ব্রাউজারে খুলুন)

---

## পরিবর্তন-লগ

### 1.0.1 (2026-08-22)
- CI/CD-Gates-এর জন্য সময়-বাজেট ও Blockier-Regeln যোগ করা হয়েছে (< 10 মিনিট Fast Path,
  < 30–45 মিনিট Pipeline; blockierend বনাম meldend; Prod-Rot-এ Rollback) এবং
  Commit-কে Inner/Outer Loop-এর হস্তান্তর-বিন্দু হিসেবে যোগ করা হয়েছে
- dev-cycle-Skill-এর Schaltplan-Beilage-এর উল্লেখ যোগ; dev-cycle-সীমানা তার
  v1.2.0 (Shift-Left: ডিজাইন 1/3/5, লেখা 6, চালানো 7) অনুযায়ী সমন্বিত

### 1.0.0 (2026-08-22)
- Online-গবেষণা থেকে প্রথম সংস্করণ (ISTQB-পদ্ধতি, Testpyramide, Agile Testing
  Quadrants, CI/CD-Gates, আধুনিক পদ্ধতি)
