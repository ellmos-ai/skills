---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "স্বায়ত্তশাসিত লুপের সমাপ্তির শর্ত: সম্ভব হলে যতদূর সম্ভব নিজে নিজে কাজ চালিয়ে যান এবং কোনো লুপ তখনই শেষ করুন, যখন প্রমাণিত হয় যে আর কোনো স্বয়ংক্রিয়ভাবে সম্পাদনযোগ্য কাজ অবশিষ্ট নেই। শুধু \"আর কিছু করার নেই\" এমন একটি ধারণা কোনোভাবেই যথেষ্ট নয় — এটি একটি চার-ধাপের যাচাই-শৃঙ্খল চালু করে (think/decide, _CONTROL/_DECISIONS, Gardener/USMC, decision-avatar/BYUM), যা লুপ শেষ হওয়ার আগে প্রথমে নতুন কাজ অর্জন করতে হবে। প্রতিটি শৃঙ্খল-ধাপ একটি বাইনারি ফলাফলের বদলে found/empty/unavailable জানায় — \"exhausted\" তখনই প্রযোজ্য, যখন সব উৎস সত্যিই প্রশ্নযোগ্য ছিল; অন্তত একটি উৎস unavailable হলে Skill \"exhausted\" নয়, \"blind\" জানায় এবং অযাচাইকৃত কিছুর দাবি করে না। এই Skill ব্যবহার করুন /work-autonomous, /waafap, \"arbeite autonom weiter bis nichts mehr zu tun ist\", আর কিছু করার না থাকা পর্যন্ত স্বায়ত্তশাসিতভাবে কাজ চালিয়ে যাও, একটি /loop-এর ভেতরে গোল-শর্ত হিসেবে, অথবা যখন যাচাই করতে হবে যে একটি লুপ/সেশন শেষ করার আগে সত্যিই আর কোনো স্বায়ত্তশাসিত কাজ বাকি আছে কিনা।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: bn
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: a8ee248e73bb81d9af36df2f3e82719bed0f31e89005ab64c35f4e236b15600c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — লুপ তখনই শেষ করুন, যখন প্রমাণিত হয় আর কোনো স্বায়ত্তশাসিত কাজ নেই

## উদ্দেশ্য

এই Skill একসাথে দুটি কাজ করে:

1. **যতদূর সম্ভব স্বায়ত্তশাসিতভাবে কাজ চালিয়ে যাওয়া** — স্বাভাবিক সেশন-কাজ, কোনো বিশেষ ব্যবস্থা নয়।
2. **একটি লুপ তখনই শেষ করা, যখন নিশ্চিতভাবে প্রমাণিত হয়** যে আর কোনো স্বয়ংক্রিয়ভাবে সম্পাদনযোগ্য কাজ নেই। "আমি এখন কিছু খুঁজে পাচ্ছি না" এই সন্দেহ **কোনো** সমাপ্তির কারণ নয় — এটি সেই যাচাই-শৃঙ্খলের **সূচনা**, যা প্রথমে নতুন কাজ **খুঁজে পেতে** চেষ্টা করে। শুধু যখন এই শৃঙ্খল সম্পূর্ণ ফলাফলহীন থাকে, তখনই সমাপ্তি প্রমাণিত ধরা হয়।

**ইচ্ছাকৃতভাবে কোনো অন্তর্নির্মিত `/goal` নেই:** এই Skill স্বতন্ত্রভাবেও ব্যবহারযোগ্য (যেমন একটি সাধারণ সেশনের ভেতরে সরাসরি `/work-autonomous`-আহ্বান হিসেবে) এবং একটি উচ্চতর লুপ-কাঠামোর ভেতরে শর্ত হিসেবেও: `/loop` স্বাভাবিকভাবে দিন, তারপর গোল হিসেবে শুধু এই Skill উল্লেখ করুন। গোল তখন মোটামুটি এরকম হবে: *"যখন আর কোনো স্বায়ত্তশাসিত কাজ না থাকে, লুপ শেষ করো — আর ততক্ষণ যতদূর সম্ভব স্বায়ত্তশাসিতভাবে কাজ চালিয়ে যাও।"* Skill নিজে কোনো `/goal`-কাঠামো আহ্বান করে না; এটি শুধু সেই স্পষ্ট সমাপ্তি-সংকেত দেয়, যা এমন কাঠামো পড়তে পারে (নিচে "সমাপ্তি-সংকেত" দেখুন)।

## পরিচালন মডেল — দুই স্তর

### স্তর 1 — স্বাভাবিক কাজ (প্রতিটি টিক)

#### TICKET-MASTER-ইনটেক-গেট (এই স্তরের অন্য সব কিছুর আগে অগ্রাধিকার)

**শুধু তখনই প্রাসঙ্গিক, যখন প্রসঙ্গের অংশ হিসেবে কোনো টিকেট-সিস্টেম (`_TICKETS/`) থাকে** — টিকেট-সিস্টেমবিহীন সেশন এই গেট সম্পূর্ণ এড়িয়ে যায়; টিকেট-সিস্টেম ছাড়াও এই Skill স্বতন্ত্রভাবে ব্যবহারযোগ্য থাকে (উপরে "উদ্দেশ্য" দেখুন)। প্রথমে যাচাই করতে হয়, `INBOX/` — ফর্মহীন, এখনো টিকেট-বিন্যাসে না আনা এন্ট্রিসহ — সম্পূর্ণ ফর্মালাইজড ও ট্রায়েজড কিনা। তা না হলে ঠিক সেটিই স্বয়ংক্রিয় কাজ হিসেবে গণ্য হয় (ফর্মালাইজ করা/ট্রায়েজ করা হলো ব্যবহারকারীর সিদ্ধান্ত ছাড়া কেরানি-কাজ, নিচের পার্থক্য দেখুন) — সেটি সম্পন্ন করুন, টিক শেষ হয়, স্তর 2 প্রবেশ করা হয় না, অন্য যেকোনো স্তর-1 উৎসের মতোই।

**যতক্ষণ INBOX খোলা থাকে, `NO_WORK`, কোনো ফলাফলহীনতার সংকেত (`exhausted`/`blind`), কোনো Guard-STOP বা অন্য কোনো সমাপ্তি-সংকেত তৈরি হতে পারবে না।** ইনটেক সম্পূর্ণ ট্রায়েজ হওয়ার পরেই শুধু `ACTIONABLE`, আনব্লক হওয়া `BLOCKED` এবং মেয়াদোত্তীর্ণ `WAITING` (নিচে) — এবং তারপর প্রয়োজনে স্তর 2 — যাচাই করা যায়।

*ঘটনাসূত্র:* `ACTIONABLE` সম্পন্ন করার পর একটি লুপ ফলাফলহীনতার যাচাই শুরু করেছিল, যখন একের পর এক নতুন `INBOX`-টিকেট আসছিল, যার মধ্যে দুটি ছিল P1 অগ্রাধিকারের। এই গেট ছাড়া লুপ `exhausted`/`blind` জানিয়ে দিত, যদিও ইনবক্স খোলা ছিল — ঠিক এটিই এই গেট প্রতিরোধ করে।

এরপর স্বাভাবিকভাবে আরও স্বয়ংক্রিয়ভাবে সম্পাদনযোগ্য কাজ খুঁজুন (নিচের পার্থক্য দেখুন) এবং সম্পন্ন করুন: খোলা `ACTIONABLE`-টিকেট, আনব্লক হওয়া `BLOCKED`-টিকেট, মেয়াদোত্তীর্ণ `WAITING`-টিকেট, ব্যবহারকারী-নির্ভরতাহীন প্রকল্পে খোলা `TODO.md`/`AUFGABEN.txt`-বিষয়, স্থানীয় নীতি অনুযায়ী মেয়াদোত্তীর্ণ রুটিন/হাইজিন-পরীক্ষা, শেষ সেশন থেকে শুরু হয়েও শেষ না হওয়া কাজ (USMC `working`), **প্রকল্পের মেয়াদোত্তীর্ণ `tidy-up`-রান** (সংযোজন 1.3.0, 2026-08-19 — Skill `tidy-up` দেখুন: যে প্রকল্পফোল্ডারে সেশন এখন কাজ করছে, তার জন্য Tasksolver+Writer+Maintainer-পাস; মেয়াদোত্তীর্ণতা `tidy-up` নিজের স্বতন্ত্র, সহজ USMC-লগ দিয়ে যাচাই করে, সেই অংশের "work-autonomous-এর সঙ্গে সম্পর্ক" দেখুন)।

→ **পাওয়া গেছে ও সম্পন্ন হয়েছে:** ফলাফল সংক্ষেপে জানান, টিক শেষ হয়, লুপ স্বাভাবিকভাবে চলতে থাকে। স্তর 2 প্রবেশ করা হয় **না** — দৃশ্যমান কাজ থাকা অবস্থায় চারটি ব্যয়বহুল যাচাই-ধাপের কোনোটিরই দরকার নেই।

### স্তর 2 — ফলাফলহীনতা-যাচাই (শুধু "আর কিছু করার নেই" সন্দেহে)

স্তর 1 **কিছুই** স্বায়ত্তশাসিত খুঁজে না পেলে সন্দেহ জন্মায়। এই সন্দেহ একাই যথেষ্ট নয়। এখন **বাধ্যতামূলকভাবে** নিচের শৃঙ্খলটি চলে, নতুন কাজ **অর্জন** করতে।

#### আত্ম-পরিচয় (শৃঙ্খলের আগে, পরে নয়)

কিছু জিজ্ঞেস করার আগে: Skill ঘোষণা করে কোন উৎসগুলো তার রায়ের জন্য দরকার। চারটি প্রয়োজন (`grounding_seed.self_knowledge.Need`, যদি `grounding-seed` ইনস্টল থাকে — নইলে একই তালিকা লাইব্রেরি-সংযোগ ছাড়া শুধু ঘোষণা হিসেবে গণ্য হয়):

| ভূমিকা | শৃঙ্খল-ধাপ | এর পেছনে যা আছে |
|---|---|---|
| `decisions.ledger` | 2 | কেন্দ্রীয় সিদ্ধান্ত-রেজিস্টার |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (ধাপ 1) ইচ্ছাকৃতভাবে কোনো ঘোষিত উৎস নয়।** এটি মডেলের নিজস্ব বিশ্লেষণ-ধাপ, এমন কোনো বাহ্যিক সিস্টেম নয় যা প্রাপ্য বা অপ্রাপ্য হতে পারে — এই পার্থক্যের অর্থে এটি সবসময় "উপলব্ধ"। শুধু ধাপ 2–4 `unavailable` হতে পারে।

শুধু অবস্থান-প্রশ্নের জন্য (found/unavailable, এখনও বিষয়বস্তু যাচাই ছাড়া) একটি ঐচ্ছিক, পরীক্ষাযোগ্য সরঞ্জাম এই Skill-ফোল্ডারে আছে: `scripts/exhaustion_check.py`। এটি `grounding_seed.resolve()` + `status_from_resolution()` ব্যবহার করে `decisions.ledger`/`user.model`-এর জন্য (সেখানে একটি প্রকৃত `source-resolver`-প্রদানকারী আছে), আর `memory.organic`/`memory.curated`-এর জন্য সবসময় সরাসরি CLI-প্রাপ্যতা (PATH-এ `gardener`/`usmc`) যাচাই করে — এই দুই ভূমিকার জন্য ২০২৬-০৮-১৫ পর্যন্ত কোনো নিবন্ধিত `source-resolver`-প্রদানকারী ছিল না; তাদের রেজোলভারের মাধ্যমে প্রশ্ন করলে Gardener/USMC সত্যিই ইনস্টল আছে কিনা তা-নির্বিশেষে শুধু `unavailable` ফেরত আসত। এটি `grounding-seed` ইনস্টল থাকুক বা না থাকুক একইভাবে চলে।

**আপডেট ২০২৬-০৮-২৫ (K3=C, `T-20260825-342866657`):** ফাঁকটি বন্ধ হয়েছে — `source-resolver` এখন `memory.organic` (Gardener) এবং `memory.curated` (USMC) উভয়কে একই CLI-উপস্থিতি-যাচাই (`shutil.which("gardener")`/`shutil.which("usmc")`) সহ স্তর-1-ভূমিকা হিসেবে নিবন্ধন করে, যা এই স্ক্রিপ্ট এখন পর্যন্ত নিজে হার্ডকোড করেছে। `exhaustion_check.py` তাই এখনই পুনর্গঠন করা হয়নি (কোনো কার্যকারিতা হারায়নি, বিদ্যমান যাচাইটি সঠিক থাকে) — পরবর্তী Skill-Care-রানে ধাপ 3 `source_resolver.resolve("memory.organic"/"memory.curated")`-এ রূপান্তর করা যাবে, ধাপ 2-এর মতো (`decisions.ledger`), যাতে CLI-যাচাই দুবার রক্ষণাবেক্ষণ করতে না হয়।

#### চার শৃঙ্খল-ধাপ — প্রতিটি found | empty | unavailable জানায়

প্রতিটি ধাপ দুই পর্যায়ে চলে: প্রথমে **অবস্থান-নির্ণয়** (কোনো প্রাপ্য স্থান জানি কিনা?), তারপর — শুধু অবস্থান নির্ণীত হলে — **বিষয়বস্তু-যাচাই** (মডেল নিজের সরঞ্জাম দিয়ে সত্যিই পড়ে দেখে সেখানে নতুন কিছু আছে কিনা)। যে উৎসের অবস্থান নির্ণয় করা যায়নি, তা কখনও বিষয়বস্তুতে যাচাই হয় না — সেটি `unavailable` গণ্য হয়, `empty` নয়।

1. **`/think` + `/decide`** প্রশ্নে প্রয়োগ করুন: "সত্যিই কি আর কোনো স্বয়ংক্রিয়ভাবে সম্পাদনযোগ্য কাজ নেই, নাকি আমি কিছু এড়িয়ে যাচ্ছি?" — অনুমানের বদলে কাঠামোগত বিশ্লেষণ। এখানে কোনো found/empty/unavailable অবস্থা নেই (উপরে দেখুন, কোনো উৎস নেই)।
2. **`decisions.ledger`** — `source_resolver.resolve("decisions.ledger")` / `grounding_seed.resolve(...)` দিয়ে অবস্থান-নির্ণয়, যদি ইনস্টল থাকে; নইলে পরিচিত ফলব্যাক-পথ (`_control-center/_CONTROL/_DECISIONS/`, `TO-DECIDE-USER*.txt`-শৃঙ্খল, হোস্ট-নিজস্ব `TO-DECIDE-USER-<HOST>.txt`, `DECIDED-AND-DONE.md`)। অবস্থান নির্ণীত → বিষয়বস্তু পড়ুন: সম্প্রতি কি এমন সিদ্ধান্ত হয়েছে, যা আগে অবরুদ্ধ বা অনুমোদনের অপেক্ষায় থাকা কাজ এখন মুক্ত করে? পাওয়া গেলে → `found`। পড়া হলো, নতুন কিছু নেই → `empty`। অবস্থান নির্ণয় অসম্ভব (রেজোলভার নেই এবং ফলব্যাক-পথও নেই) → `unavailable`।
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — দুটি পৃথক উৎস, একটি শৃঙ্খল-ধাপ। অবস্থান: PATH-এ CLI (`gardener`/`usmc`), উপরের আত্ম-পরিচয় দেখুন। প্রাপ্য → বিষয়বস্তু পড়ুন (`find()`/`recall()` বা `usmc facts|lessons|working|context`): খোলা Working-Memory-বিষয়, অমীমাংসিত পরবর্তী-কাজসহ Lessons, এমন তথ্য যা উপেক্ষিত কিন্তু সম্পাদনযোগ্য কাজের ইঙ্গিত দেয় (ঠিক এখানেই আগের সেশনগুলো অসম্পূর্ণ বিষয় — `RESUME:`-ক্ষেত্র, খোলা `note`-এন্ট্রি — রেখে যায়)। পাওয়া গেলে → `found`। পড়া হলো, নতুন কিছু নেই → `empty`। CLI PATH-এ নেই → `unavailable`।
4. **`user.model` (decision-avatar/BYUM)** — অবস্থান `decisions.ledger`-এর মতোই (রেজোলভার বা ফলব্যাক-পথ `_control-center/_CONTROL/_USER-MIND/`)। অবস্থান নির্ণীত → বিষয়বস্তু যাচাই: এমন কোনো প্রমাণিত ধরন আছে কি, যাতে ব্যবহারকারী এই জায়গায় একটি নির্দিষ্ট কাজ স্বয়ংক্রিয়ভাবে সম্পন্ন দেখতে চেয়েছিলেন? শুধু পর্যাপ্ত আত্মবিশ্বাসে (🟢/🟡) `found` গণ্য হয় — 🔴 `empty` গণ্য হয়, অর্জিত কাজ হিসেবে নয়, বরং নিচের "শুধু-ব্যবহারকারী-অবশিষ্ট" ধাপের জন্য খোলা বিষয় হিসেবে। অবস্থান নির্ণয় অসম্ভব → `unavailable`।

**"Exhausted" তখনই জানানো যায়, যখন সব চারটি উৎস (ধাপ 2–4, তিন ধাপ, চার ভূমিকা) সত্যিই প্রশ্নযোগ্য ছিল — অর্থাৎ `found` বা `empty`, একটিও `unavailable` নয়।** এটি `grounding_seed.self_knowledge.GroundingReport.all_answerable()`-এর সাথে মেলে। অন্তত একটি ভূমিকা `unavailable` হলে "exhausted" প্রযোজ্য নয়, বরং নিজস্ব সংকেত "blind" প্রযোজ্য (নিচে সমাপ্তি-সংকেত দেখুন) — লুপ তবুও শেষ হয় (যেহেতু সে এমনিতেই কিছু জিজ্ঞেস করতে পারে না), কিন্তু যা যাচাই করতে পারেনি তা যাচাই করেছে বলে আর দাবি করে না।

কোনো ধাপ নতুন কাজ খুঁজে পেলে → স্তর 1-এ ফিরে যান, কাজ সম্পন্ন করুন, Guard-অবস্থা (নিচে) "exhausted"/"blind"-এর বদলে "found"-এ সেট করুন।

### বিশেষ ক্ষেত্র: শুধু ব্যবহারকারী-সম্পৃক্ত অবশিষ্টাংশ

শৃঙ্খল **কোনো স্বয়ংক্রিয়** কাজ খুঁজে না পেলেও, যদি `USER/*`-টিকেট বা অমীমাংসিত `_DECISIONS`-বিষয় খোলা থাকে, তবুও এটি স্বায়ত্তশাসনের জন্য একটি **থামার** সংকেত — তবে "করার কিছু নেই" নয়, বরং "স্বয়ংক্রিয়ভাবে করার কিছু নেই"। এই বিষয়গুলো স্বায়ত্তশাসিত-লুপ-নিয়ম অনুযায়ী `ticket-master` থেকে **একত্রে** উপস্থাপন করা হয় (একটি সমষ্টিগত উপস্থাপনা, একক-একক প্রশ্ন নয়), একটি-একটি করে জিজ্ঞেস করা হয় না। সমাপ্তি-সংকেত এই ক্ষেত্রটিকে প্রকৃত শূন্যতা থেকে স্পষ্টভাবে আলাদা করে।

## পার্থক্য — "স্বয়ংক্রিয়ভাবে সম্পাদনযোগ্য" কী?

তুলনার জন্য: `ticket-master` শ্রেণি (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`)।

| ঘটনা | স্বয়ংক্রিয়? | যুক্তি |
|---|---|---|
| `INBOX/`, ফর্মহীন এন্ট্রিসহ, TICKET-MASTER-এর অধীনে (ট্রায়েজের আগে) | **হ্যাঁ, অগ্রাধিকারসহ** | ফর্মালাইজ/ট্রায়েজ হলো ব্যবহারকারীর সিদ্ধান্ত ছাড়া কেরানি-কাজ — `ACTIONABLE`/`BLOCKED`/`WAITING`-এর আগে যায় এবং ততক্ষণ যেকোনো সমাপ্তি-সংকেত আটকে রাখে (উপরের ইনটেক-গেট দেখুন)। |
| `ACTIONABLE`-টিকেট | **হ্যাঁ** | কোনো বাধা নেই, ব্যবহারকারী-নির্ভরতা নেই — সংজ্ঞা অনুযায়ী। |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | না, যতক্ষণ বাধা **প্রমাণসহ** না সরে | পর্যায়ক্রমিক পুনঃ-যাচাই অনুমোদিত (স্বায়ত্তশাসিত লুপ), "আছে" প্রমাণ হিসেবে যথেষ্ট নয় — প্রমাণ দরকার। |
| `WAITING/*` (scheduled, review-due, marker) সময়/মার্কারের আগে | না | সময়-নির্দিষ্ট। |
| `WAITING/*` সময়/মার্কার আসার পরে | **হ্যাঁ** | শর্ত পূরণ → `ACTIONABLE`-এ চলে যায়। |
| `USER/*` (decision, data, freigabe, hardware, session) | **কখনো স্বায়ত্তশাসিত নয়** | বাধ্যতামূলকভাবে ব্যবহারকারীর সিদ্ধান্ত/ডেটা/অনুমোদন/হার্ডওয়্যার/সেশন। উপরে দেখুন, একত্রে উপস্থাপন করুন। |
| `PARKED/*` (skip, backlog, until-trigger) | না, স্পষ্ট নির্দেশ/ট্রিগার ছাড়া | ইচ্ছাকৃতভাবে স্থগিত, স্বয়ংক্রিয় পুনঃ-যাচাই নেই। |
| অনুমোদন/সিদ্ধান্ত-নোট ছাড়া খোলা `TODO.md`/`AUFGABEN.txt`-বিষয় | **হ্যাঁ** | প্রকল্প-রেজিস্টার, স্বাভাবিক কাজ। |
| মেয়াদোত্তীর্ণ রুটিন/হাইজিন-পরীক্ষা (কুলডাউন শেষ, কোনো লক নেই) | **হ্যাঁ** | স্থানীয় নীতি অনুযায়ী নিয়মিত রক্ষণাবেক্ষণ। |
| `LOCK.user.*`-দ্বারা লক করা এলাকা | **কখনো না** | ব্যবহারকারী-লক — শুধু ব্যবহারকারী তুলতে পারেন, LOCK-SYSTEM দেখুন। |
| অপরিবর্তনীয়/বাইরে প্রভাবশালী ধাপ নীতি-অনুমোদন ছাড়া (Zenodo-আপলোড, মূল্যায়িত/সুরক্ষিত শাখায় পুশ, ল্যাপটপ-সীমার বাইরে সার্ভার-ব্যয় সিদ্ধান্ত, পূর্বদর্শন ছাড়া চূড়ান্ত মুছে ফেলা) | **না** | অনুমোদন/সিদ্ধান্ত দরকার, যদিও প্রযুক্তিগতভাবে সম্পাদনযোগ্য। |
| শুধু GUI/লগইন দিয়ে শুরু করা যায় এমন সেশন (যেমন Claude-Desktop-কাজ, ইন্টারঅ্যাকটিভ লগইন, ভৌত হার্ডওয়্যার-ক্রিয়া) | **কখনো না** | "শুধু ব্যবহারকারী-শুরু-করা সেশন" — কোনো লুপ এটি নিতে পারে না। |

মূল নিয়ম: স্বায়ত্তশাসিত তা-ই, যা **ব্যবহারকারীর সিদ্ধান্ত, অনুমোদন, ডেটা, হার্ডওয়্যার বা সেশন ছাড়া** শেষ করা যায় এবং যার জন্য কোনো অপরিবর্তনীয়/বাইরে প্রভাবশালী ক্রিয়া নথিবদ্ধ নীতি-অনুমোদন ছাড়া দরকার হয় না।

## অসীম-লুপের বিরুদ্ধে Guard (বাধ্যতামূলক)

**সমস্যা:** ব্রেক ছাড়া চার-ধাপের শৃঙ্খল প্রতিটি নতুন যাচাইয়ে আবার পুরোটা চলত, যদিও শেষ ফলাফলহীন যাচাইয়ের পর কিছুই বদলায়নি — ব্যয়বহুল ও অর্থহীন, বিশেষত যখন Skill কাছাকাছি সময়ে বারবার আহ্বান হয় (লুপ, নির্ধারিত টাস্ক, কাছাকাছি সময়ে পুনরায় ম্যানুয়াল আহ্বান)।

**অবস্থা USMC-এ স্থায়ী করা হয়** (এই সিস্টেমে প্রক্রিয়া-অবস্থা সেখানে থাকে, Markdown-ফাইলে নয়):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**ফিঙ্গারপ্রিন্ট দুটি উপাদান নিয়ে গঠিত — পরিস্থিতি এবং প্রাপ্যতা:**

1. **পরিস্থিতি-উপাদান** (আগের মতো): খোলা `ACTIONABLE`-টিকেটের সংখ্যা/ID, `_DECISIONS`-শৃঙ্খলের mtime (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), শেষ শৃঙ্খল-রানের পর থেকে নতুন USMC-`working`-এন্ট্রির সংখ্যা।
2. **প্রাপ্যতা-উপাদান (নতুন, 1.2.0 থেকে বাধ্যতামূলক):** আত্ম-পরিচয় যাচাই থেকে এই মুহূর্তে `unavailable`-হিসেবে প্রতিবেদিত ভূমিকাগুলোর সাজানো টুপল (`exhaustion_check.availability_fingerprint_component()`), যেমন `("memory.organic",)` বা `()`।

**কেন দ্বিতীয় উপাদান বাধ্যতামূলক — "নইলে Guard ফাঁকটি উত্তরাধিকারসূত্রে পায়":** এটি ছাড়া ফিঙ্গারপ্রিন্ট (উপাদান 1) অন্যান্যের মধ্যে `_DECISIONS`-শৃঙ্খলের mtime-এর উপর নির্ভর করে। যদি এই শৃঙ্খল কোনো সিস্টেমে পুরোপুরি না থাকে, তবে ফিঙ্গারপ্রিন্টের এই অংশটি চিরকাল স্থির থাকে — একবার ভুলভাবে সেট হওয়া `exhausted`/`blind` তখন কখনো পুনঃ-যাচাই হতো না, এমনকি পরে `source-resolver` ইনস্টল হলেও বা `_control-center/_CONTROL/_DECISIONS/` তৈরি হলেও। প্রাপ্যতা-উপাদান ঠিক এটি লক্ষ্যভিত্তিকভাবে সারায়: কোন ভূমিকাগুলো unavailable তা বদলালে (একটি উৎস যোগ হলে বা সরে গেলে), ফিঙ্গারপ্রিন্ট স্বয়ংক্রিয়ভাবে বদলায় — পরবর্তী আহ্বানে Guard তা টের পায় এবং শৃঙ্খল নতুন করে চালায়। এটি গ্রাউন্ডিং-রূপকের অর্থে "প্রতিস্থাপন" (T-20260815-371628859): পরিবেশ-পরিবর্তন নতুন অনুসন্ধান শুরু করে, কাউকে Guard ম্যানুয়ালি রিসেট করতে হয় না।

**প্রতিটি শৃঙ্খল-রানের আগে ক্রম:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```

একটি সম্পূর্ণ সম্পাদিত শৃঙ্খল-রান, যেখানে সব চার উৎস প্রশ্নযোগ্য ছিল এবং কোনোটিই ফলাফল দেয়নি, তা "আর কোনো স্বয়ংক্রিয় কাজ নেই"-এর প্রমাণ হিসেবে যথেষ্ট (টিকেট-শর্ত: "কেবল তখনই, যখন একটি রানের সব ধাপ ফলাফলহীন থাকে" — এখানে ফলাফলহীন স্পষ্টভাবে `empty`, `unavailable` নয়)। Guard নিজে নির্ধারণ আটকায় না, শুধু ঘন ঘন আহ্বানে **অপরিবর্তিত পুনঃ-নির্ধারণ** আটকায় — এবং `exhausted` ও `blind`-এর জন্য আলাদাভাবে, কখনো একে অপরের সাথে গুলিয়ে না।

`GUARD_INTERVAL` কনফিগারযোগ্য (ডিফল্ট 15 মিনিট) — অত্যন্ত ধীর পরিবেশে (বিরল নতুন টিকেট/সিদ্ধান্ত) বড় মান বেছে নেওয়া যায়, অত্যন্ত সক্রিয় পরিবেশে ছোট।

## সমাপ্তি-সংকেত

প্রতিটি রান **একটি** স্পষ্ট, grep-যোগ্য লাইনে শেষ হয়, যাতে আশেপাশের `/loop` বা ভবিষ্যৎ `/goal`-কাঠামো তা পড়ে বুঝতে পারে কাজ চালিয়ে যাওয়া উচিত কিনা:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE`-ই একমাত্র সংকেত, যেখানে উচ্চতর লুপ আরেকটি টিক চালাবে। সব `STOP`-রূপ হলো প্রমাণিত সমাপ্তি — কোন ঘটনা তা ব্যাখ্যাসহ।

**`exhausted` ও `blind`-এর পার্থক্য ব্যবহারকারীর কাছে গুরুত্বপূর্ণ, প্রসাধনী নয়:** `exhausted` মানে "যা যাচাই করার ছিল তা সব যাচাই করেছি — কাজ শেষ"। `blind` মানে "যাচাই করার জন্য আমার অবকাঠামো নেই — এটি কাজের অবস্থা নয়, একটি ফাঁক"। একটি `/loop`/`/goal`-কাঠামো যদি দুটিকে একইভাবে আচরণ করে (লুপ যেভাবেই শেষ হয়), তবুও দুটিকে ব্যবহারকারীর কাছে একই রকমভাবে জানানো উচিত নয় — নইলে ঠিক সেই তথ্য হারিয়ে যায়, যা T-20260815-205101335 দাবি করেছিল।

## অন্যান্য Skill-এর সাথে সম্পর্ক

- **`think`/`decide`** — শৃঙ্খল-ধাপ 1-এ কাঠামোগত বিশ্লেষণ/সিদ্ধান্ত দেয়। এখানে একটি উপাদান হিসেবে আহ্বান করা হয়, নতুন করে উদ্ভাবন করা হয় না।
- **`decision-avatar`** (এই Skill, ব্যবহারকারী-নিরপেক্ষ) — ধাপ 4 দেয়। একটি নির্দিষ্ট, অনুমোদিত প্রোফাইলসহ সিস্টেমে এটি `user-model` + `build-your-users-mind`-এর সাথে মেলে।
- **`orchestrator`** — সাব-এজেন্টদের কাছে কীভাবে ডেলিগেট করা হয় এবং তাদের সমাপ্তি-বার্তা কীভাবে যাচাই হয়, তা নিয়ন্ত্রণ করে। `work-autonomous` নিয়ন্ত্রণ করে কখন অনুসন্ধান থামাতে হবে; দুটি একত্রে ব্যবহারযোগ্য (অর্কেস্ট্রেটর স্তর-1-এর সম্পাদিত কাজের অংশ হিসেবে আসতে পারে)।
- **`bugsweep`** — অন্য একটি স্ব-সীমাবদ্ধ অনুসন্ধান-প্রোটোকলের উদাহরণ (চার-ধাপ শৃঙ্খলের বদলে দ্বিগুণ-বৃদ্ধি ক্রমবর্ধমানতা)। `work-autonomous` আরও সাধারণ: এটি শুধু কোডে বাগ খোঁজে না, স্বয়ংক্রিয় কাজের প্রতিটি উৎস যাচাই করে।
- **টিকেট-শ্রেণি (`ticket-master`)** — "স্বয়ংক্রিয়ভাবে সম্পাদনযোগ্য"-এর শব্দভাণ্ডার (পার্থক্য-সারণি দেখুন) এবং স্বায়ত্তশাসিত-লুপের টেমপ্লেট দেয় (BLOCKED-পুনঃ-যাচাই, USER-একত্রীকরণ, WAITING-সময়-টানা, PARKED-স্থবিরতা)।
- **`tidy-up`** (1.3.0 থেকে) — একটি অতিরিক্ত স্তর-1 উৎস দেয়: বর্তমানে কাজ-করা প্রকল্পফোল্ডারের জন্য একবারের Tasksolver+Writer+Maintainer-পাস। এর নিজস্ব মেয়াদোত্তীর্ণতা যাচাই নিজে করে (সহজ USMC-লগ, এখানকার মতো চার-ধাপ Guard নয়) — `work-autonomous` এটিকে বহু স্তর-1 উৎসের একটি হিসেবে ডাকে, এর যুক্তি নকল না করে।

## উদাহরণ প্রবাহ

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```

## পরিবর্তনের ইতিহাস

### 1.5.1 (2026-09-09)
- T-20260909-282509082: `decisions.ledger` ও `user.model`-এর নথিবদ্ধ ফলব্যাক যাচাই-করা Control-Center-স্থানান্তর অনুসরণ করে `_CONTROL/_DECISIONS` ও `_CONTROL/_USER-MIND`-এ যায়। রেজোলভার-অগ্রাধিকার এবং fail-closed আচরণ অপরিবর্তিত থাকে।

### 1.5.0 (2026-09-09)
- P-018: নতুন তৈরি ও স্থায়ীভাবে সংরক্ষিত গুরুত্বপূর্ণ কাজের প্রতিবেদন, হ্যান্ডঅফ ও রসিদ `session: <session-id> | <agent>@<host> | YYYY-MM-DD` দিয়ে শেষ হয়। উৎস-অগ্রাধিকার: স্পষ্ট রানটাইম/CLI-মান → কর্তৃপক্ষীয় প্রদানকারী-পরিবেশ/হুক → `unbekannt`। মান কখনো অনুমান করা হয় না; সাব-এজেন্ট মূল সেশন ব্যবহার করে। রুটিন চ্যাট, উৎস, নীতি, `CLAUDE.md`, README ও পুরনো ফাইল সাধারণ বা পশ্চাদগামী স্ট্যাম্পিং থেকে বাদ থাকে।

### 1.4.0 (2026-09-03)
- টিকেট T-20260902-729068782 থেকে ন্যূনতম-আক্রমণাত্মক সংযোজন: স্তর 1-এ নতুন **TICKET-MASTER-ইনটেক-গেট** (`ACTIONABLE`/`BLOCKED`/`WAITING`-এর আগে অগ্রাধিকার) — শুধু তখনই প্রাসঙ্গিক, যখন একটি টিকেট-সিস্টেম প্রসঙ্গের অংশ। যতক্ষণ `INBOX/` (ফর্মহীন এন্ট্রিসহ) সম্পূর্ণ ট্রায়েজ না হয়, কোনো `NO_WORK`/ফলাফলহীনতা-সংকেত/Guard-STOP তৈরি হতে পারবে না। ঘটনাসূত্র: একটি লুপ ফলাফলহীনতার যাচাই শুরু করেছিল, যখন `INBOX`-এ এখনও খোলা এন্ট্রি ছিল (দুটি P1-টিকেটসহ)। বিদ্যমান চার-ধাপ ফলাফলহীনতা-শৃঙ্খল, Guard এবং TICKET-MASTER-ছাড়া ব্যবহারযোগ্যতা অপরিবর্তিত — গেট শুধু স্তর 1-এ এবং শুধু TICKET-MASTER-এর অধীনে কাজ করে।
- নতুন, পরীক্ষিত সহায়ক ফাংশন `scripts/exhaustion_check.py::intake_gate_blocks_stop()` + `tests/test_exhaustion_check.py`-এ রিগ্রেশন-পরীক্ষা (আচরণ-ভিত্তিক: INBOX খোলা থাকলে গেট ব্লক করে, INBOX খালি থাকলে ছেড়ে দেয়)।

### 1.3.0 (2026-08-19)
- টিকেট T-20260819-461890468 থেকে ন্যূনতম-আক্রমণাত্মক সংযোজন (নতুন Skill `tidy-up`): স্তর 1 একটি অতিরিক্ত, স্বতন্ত্র উৎস পায় — "বর্তমান প্রকল্পের মেয়াদোত্তীর্ণ `tidy-up`-রান" (Tasksolver+Writer+Maintainer-পাস, Skill `tidy-up` দেখুন)। কোনো নতুন শৃঙ্খল-ধাপ নেই, স্তর 2/Guard/সমাপ্তি-সংকেতে পরিবর্তন নেই — `tidy-up` নিজের মেয়াদোত্তীর্ণতা একটি সহজ USMC-লগ দিয়ে যাচাই করে এবং এখানে শুধু আরেকটি স্তর-1 উৎস হিসেবে উল্লেখ করা হয়, বিদ্যমান উৎসগুলোর (টিকেট, TODO/AUFGABEN, রুটিন-চেক, USMC `working`) অনুরূপে। ফলে `tidy-up`-বিষয়গুলো স্বায়ত্তশাসিতভাবে সম্পাদনযোগ্য কাজ হিসেবে গণ্য হয়, এমন `/goal`-কাঠামোতে যা `/work-autonomous` + `/tidy-up` একত্রিত করে (টিকেটের মূল ব্যবহার-ক্ষেত্র)। ফলাফলহীনতা-শৃঙ্খল বা Guard-এ কোনো হস্তক্ষেপ নেই — স্তর 2 অপরিবর্তিত।

### 1.2.0 (2026-08-15)
- টিকেট T-20260815-205101335 থেকে পুনর্নির্মাণ (যাচাই-অনুরোধ: "দেখো সমাধানটি গ্রাউন্ডিং-রূপকের সাথে টেকে কিনা", Skill-এর বাস্তব ফলাফল: তিন বিন্দুতে টিকেছে, কিন্তু "প্রশ্ন করা হয়েছে ও ফলাফলহীন" বনাম "মোটেও প্রশ্ন করা যায়নি" — এই পার্থক্যে টেকেনি — শৃঙ্খল Gardener/USMC/`_DECISIONS`-বিহীন সিস্টেমেও `STOP (exhausted)` জানাত, কখনো যাচাই না করেই। `grounding-seed`-এর প্রথম বাস্তব প্রয়োগ, টিকেট T-20260815-371628859)।
- **আত্ম-পরিচয় যোগ করা হয়েছে:** শৃঙ্খলের আগে চারটি ঘোষিত প্রয়োজন (`decisions.ledger`, `memory.organic`, `memory.curated`, `user.model`), চারটি নির্দিষ্ট স্থানে অন্ধভাবে না খুঁজে।
- **প্রতিটি শৃঙ্খল-ধাপ (2–4) found | empty | unavailable জানায়** বাইনারি ফলাফলের বদলে — দুই পর্যায়ে: প্রথমে অবস্থান-নির্ণয় (`grounding-seed`/`source-resolver` `decisions.ledger`/`user.model`-এর জন্য, সরাসরি CLI-যাচাই `memory.organic`/`memory.curated`-এর জন্য যাদের এখনও `source-resolver`-প্রদানকারী নেই), বিষয়বস্তু-যাচাই শুধু অবস্থান নির্ণীত হলে।
- **`exhausted` তখনই প্রযোজ্য, যখন সব চার উৎস সত্যিই প্রশ্নযোগ্য ছিল** (সব found/empty, কোনো unavailable নেই)। অন্তত একটি উৎস প্রাপ্য না হলে একটি নতুন, পৃথক সংকেত `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` — লুপ তবুও শেষ হয়, কিন্তু আর কোনো যাচাই-করা ফলাফলের দাবি করে না।
- **Guard-ফিঙ্গারপ্রিন্টে প্রাপ্যতা-উপাদান যোগ করা হয়েছে** (এখন unavailable ভূমিকাগুলোর সাজানো টুপল)। পূর্ববর্তী Guard-অংশের "Guard ফাঁকটি উত্তরাধিকারসূত্রে পায়" সমস্যাটি সারায়: এই উপাদান ছাড়া একবার ভুলভাবে সেট হওয়া `exhausted`/`blind` চিরকাল বৈধ থাকত, যদি `_DECISIONS`-শৃঙ্খল পুরোপুরি না থাকে (বিদ্যমান ফিঙ্গারপ্রিন্ট-অংশ তখন স্থির)। এই উপাদানসহ নতুন প্রাপ্য উৎস স্বয়ংক্রিয়ভাবে আরেকটি শৃঙ্খল-রান ট্রিগার করে (গ্রাউন্ডিং-রূপকের অর্থে প্রতিস্থাপন)।
- নতুন, পরীক্ষিত সহায়ক স্ক্রিপ্ট `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`, 11টি পরীক্ষা, উভয় অবস্থা যাচাই: `grounding-seed` ইনস্টল থাকা ও না থাকা) — আত্ম-পরিচয়/অবস্থান-যাচাই নির্ধারিতভাবে দেয়, যাতে Skill প্রতিবার অনুমান না করে। ঐচ্ছিক থাকে: Skill এখনও প্রধানত একটি প্রোটোকল, যা একটি মডেল তার নিজের সরঞ্জাম দিয়ে অনুসরণ করে।
- নির্ভরতা: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` `grounding-seed` 0.2.0 থেকে — পুরোনো `grounding-seed`-অবস্থা (0.1.0)-এ একটি শ্রেণিগত ত্রুটি ছিল (`not_found` ভুলভাবে `empty` হতো), যা এখানে সংশোধিত পার্থক্যটি আবার ঝাপসা করত। `grounding-seed` ইনস্টল না থাকলে নথিবদ্ধ ফলব্যাক অভিন্নভাবে চলে।

### 1.1.0 (2026-08-15)
- টিকেট T-20260815-385400870 থেকে রেফারেন্স-পুনর্নির্মাণ: ধাপ 2 (সিদ্ধান্ত-রেজিস্টার) এখন তার অবস্থান ভূমিকা `decisions.ledger`-এর মাধ্যমে সমাধান করে (`source_resolver.resolve(...)`, মডিউল `source-resolver`), পথ হার্ডকোড না করে — রেজোলভার ইনস্টল না থাকলে নথিবদ্ধ ফলব্যাকসহ পূর্ববর্তী পথে। কার্যকারিতা অপরিবর্তিত।

### 1.0.0 (2026-08-15)
- টিকেট T-20260815-522639345 থেকে প্রথম সংস্করণ: দুই-স্তর পরিচালন মডেল, চার-ধাপ যাচাই-শৃঙ্খল, `ticket-master`-শ্রেণি অনুযায়ী পার্থক্য-সারণি, অসীম-লুপের বিরুদ্ধে USMC-সমর্থিত Guard, এবং `/loop`/`/goal`-কাঠামোর জন্য স্পষ্ট সমাপ্তি-সংকেত।
