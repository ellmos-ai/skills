---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: "ইকোসিস্টেমের ellmos-এ নতুন এজেন্ট ভূমিকা তৈরি ও যাচাই করে: নেটিভ Claude-Code সাবএজেন্ট (স্থায়ী ভূমিকা সংজ্ঞা) এবং Companion-Worker (SendMessage-এর মাধ্যমে পুনর্ব্যবহৃত ইনস্ট্যান্স একটি টিকিট/কাজের ধারার জন্য)। এজেন্ট ভূমিকা তৈরির চলমান কাজ থেকে (ati-agent, bueroassistent, versicherungs-agent ইত্যাদি) এতদিন আনুষ্ঠানিক না করা নিজস্ব জ্ঞানকে একটি পুনঃব্যবহারযোগ্য Scaffold-plus-Verify প্রক্রিয়ায় আনুষ্ঠানিক করে। নতুন ভূমিকা তৈরি করতে হলে (\"neue Agentenrolle bauen\", \"Subagent anlegen\", \"Companion-Worker starten\") বা বিদ্যমান কোনো ভূমিকাকে হাউস-কনভেনশনের বিপরীতে যাচাই করতে হলে (\"ist dieser Agent richtig aufgesetzt?\") এই Skill ব্যবহার করুন। বাংলা সমতুল্য ট্রিগার: নতুন এজেন্ট ভূমিকা তৈরি করো; সাবএজেন্ট তৈরি করো; Companion-Worker চালু করো; এই এজেন্ট কি সঠিকভাবে সেটআপ করা হয়েছে?"
visibility: public
language: bn
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
translated_from_sha256: 55b76ad25a5d65f61987662e674bc9c74ea0f6a8586ad4748268bc9441711db5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="agent-role-scaffolder banner">

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agenten-Orchestrierung START -->
> **এজেন্ট অর্কেস্ট্রেশন পরিবার — দিকনির্দেশিকা:** মডেল বেছে নেওয়া/স্তরবিন্যাস ->
> `model-strategy`; অর্কেস্ট্রেশন প্যাটার্ন বেছে নেওয়া -> `choose-your-orchestrator`;
> সোয়ার্ম-অপারেশন (৫টি মৌলিক প্যাটার্ন + ২টি মোড) -> `swarm-operations`; কাজ ভাগ/অর্পণ/গ্রহণ ->
> `orchestrator`; প্রদানকারী-নিরপেক্ষ বার্তা/Presence/Locks -> `agents-bridge`; **একটি নতুন ভূমিকা
> তৈরি বা যাচাই করা -> এই Skill (agent-role-scaffolder)**.
<!-- FAMILY-ROUTER:Agenten-Orchestrierung END -->

## উদ্দেশ্য

এই ইকোসিস্টেমে ইতিমধ্যে অর্কেস্ট্রেশন-Skill-এর একটি পরিপক্ব পরিবার আছে
(`model-strategy`, `swarm-operations`, `orchestrator`, `choose-your-orchestrator`,
`agents-bridge`) — কিন্তু **এর কোনোটিই "কীভাবে সঠিকভাবে একটি নতুন ভূমিকা তৈরি হয়" প্রশ্নের
উত্তর দেয় না।** এই ফাঁক পূরণ করে `agent-role-scaffolder`। এটি উল্লিখিত Skill-গুলোর নকল করে না, বরং
স্তরবিন্যাস, অর্কেস্ট্রেশন প্যাটার্ন বা প্রদানকারী-নিরপেক্ষ মেসেজিং প্রয়োজন হলে **সেগুলোর দিকে রুট করে**।

**উৎস:** ব্যবহারকারীর সিদ্ধান্ত M5 থেকে টিকিট `T-20260825-935905816`
(Marketplace-পূর্ণ পর্যালোচনা): রায় (b) — এজেন্ট-বিল্ড সম্পর্কে নিজস্ব জ্ঞান ছিল, কিন্তু আনুষ্ঠানিক ছিল না।
সরকারি Claude-Code-প্লাগইন `agent-sdk-dev` (claude-plugins-official, Apache-2.0) **কাঠামোগত আদর্শ** হিসেবে
কাজ করেছে: একটি scaffolding-কমান্ড-ফাইল প্লাস দুটি বিষয়-নির্দিষ্ট Verifier-সাবএজেন্ট, চেকলিস্ট ও
PASS/PASS-WITH-WARNINGS/FAIL প্রতিবেদন-ফরম্যাট সহ। গৃহীত হয়েছে **রূপ** (Scaffold-প্রশ্ন-তালিকা → নির্মাণ →
কাঠামোবদ্ধ প্রতিবেদন সহ যাচাই-চেকলিস্ট), পাঠ্য বা বিষয়বস্তু নয়। সেই প্লাগইন কাঁচা Claude-Agent-SDK-অ্যাপ
(Python/TypeScript) তৈরি করে, এই Skill তৈরি করে **ellmos-নিজস্ব এজেন্ট ভূমিকা** (সাবএজেন্ট-সংজ্ঞা ও
Companion-Worker)। মূল প্লাগইন ইনস্টল করা নেই; এটি স্থানীয় Marketplace-Cache-এ শুধু-পঠনযোগ্য আছে এবং
শুধু পড়া হয়েছে (`.PLUGINS/CLAUDE.md` নিয়ম 5: ধারণা মুক্ত, শব্দবিন্যাস নয়)। রেজিস্টার-এন্ট্রি:
`.AI/.PLUGINS/PLUGIN-REGISTER.md`, অবস্থা `zitiert`।

## দুটি নির্মাণপথ — উভয়ই এখানে

ellmos-ইকোসিস্টেমে নতুন ভূমিকা দুটি কাঠামোগতভাবে ভিন্ন পথে তৈরি হয়, যেগুলো গুলিয়ে ফেলা যাবে না (আদর্শ
প্লাগইনের TS/Python-বিভাজনের অনুরূপ — তবে এখানে প্রকৃত সিস্টেম-সীমানা ধরে):

| | **নেটিভ Subagent** | **Companion-Worker** |
|---|---|---|
| কী তৈরি হয় | একটি স্থায়ী ভূমিকা-সংজ্ঞা (`~/.claude/agents/<name>.md`, `Agent`-টুল দিয়ে চালু করা যায়) | একটি ad-hoc নামযুক্ত, `SendMessage` দিয়ে পুনঃব্যবহৃত ইনস্ট্যান্স একটি মাত্র কাজের ধারার জন্য |
| আয়ুষ্কাল | স্থায়ী, সেশন জুড়ে পুনঃব্যবহারযোগ্য | একটি টিকিট/বিষয়ের ধারার সময়কাল, এরপর বাতিল |
| বিদ্যমান উদাহরণ | `ati-agent`, `bueroassistent`, `versicherungs-agent`, `gesundheitsassistent`, `persoenlicher-assistent`, `production`, `research-agent`, `reflection-agent`, `test-agent`, `entwickler-agent` | এই সেশন-মডেল নিজেই (যেমন `skillcreator-bau`, `policyreg-decisions`, `workflowhooker-ausbau` — টিকিট-সিস্টেমে নামযুক্ত Worker) |
| লাইফসাইকেল-স্তর | Claude-Code-নিজস্ব Agent-Registry | **COMA** (`.MODULES/.ORCHESTRATION/coma`) — যদি প্রসেস-জুড়ে চালু হয়, শুধু টুল-অভ্যন্তরীণ নয় |
| নির্মাণ-নির্দেশিকা এখানে | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**মূলনীতি:** সক্ষমতার যদি বহু সেশন জুড়ে পুনঃব্যবহারযোগ্য নিজস্ব নাম ও স্থির ট্রিগার-বর্ণনা লাগে (যেমন
"যখনই কর-রসিদ নিয়ে কথা হয়" (মূল: immer wenn es um Steuerbelege geht)) → নেটিভ Subagent। সীমিত কিন্তু বিষয়গতভাবে সংশ্লিষ্ট কাজের ধারা, যা একজন
সমন্বয়কারী এখন অর্পণ করছে (টিকিট-শৃঙ্খল, বিষয়-পরিবর্তন) → Companion-Worker।

## প্রক্রিয়া

1. **নির্মাণপথ বেছে নিন** (উপরের সারণি) — সন্দেহ হলে অনুমান না করে ব্যবহারকারীকে জিজ্ঞাসা করুন।
2. **Scaffold-প্রশ্নগুলো অতিক্রম করুন** (উপযুক্ত `references/*.md` দেখুন) — বিকল্প প্লাগইনের মতো একে একে,
   একসাথে নয়: উদ্দেশ্য/ট্রিগার, টুল-প্রয়োজন (`Tools:`), মডেল-নির্বাচন (→ **ধাপ 3**), সমন্বয়-প্রয়োজন
   (Boss-Agent বিশেষজ্ঞদের সাথে নাকি একক ভূমিকা?)।
3. **মডেল-নির্বাচন এখানে সিদ্ধান্ত নেবেন না — `model-strategy`-এ অর্পণ করুন।** স্কোর-ভিত্তিক নির্বাচন,
   Cross-Agent-Delegation, Advisor-Pairing, এসকেলেশন ট্রিগার সেখানে ইতিমধ্যে সমাধান করা আছে; এখানে শুধু
   রেফারেন্স। বিদ্যমান ভাণ্ডারের নিয়ম: Subagent-রা মূল মডেল নির্বিচারে উত্তরাধিকার সূত্রে পায় না
   (Feedback-Memory `feedback_subagenten_modellstaffelung` দেখুন)।
4. **অর্কেস্ট্রেশন প্যাটার্ন যাচাই করুন**, যদি নতুন ভূমিকাটি একাধিক অন্যের সাথে কাজ করবে — `choose-your-orchestrator`
   প্যাটার্ন বেছে নেয়, `swarm-operations` ৫টি মৌলিক প্যাটার্ন + ২টি মোড দেয়, `orchestrator` ভাগ/অর্পণ/গ্রহণ-
   প্রোটোকল।
5. **টিম-/মেসেজিং-কনভেনশন মানুন** (`references/
   model-staffing-and-messaging.md`): Cross-Agent-যোগাযোগের জন্য `SendMessage`,
   টিকেট-অর্পণে ফাইলনাম-দ্বারা Ticket-Claim, অর্পণের সময় "পুনরাবৃত্তি না করে উল্লেখ করুন" (কেন্দ্রীয় নিয়মগুলো
   প্রম্পটে পুনরায় বলবেন না, শুধু কাজ-নির্দিষ্ট অংশ)।
6. **যাচাই করুন** — নির্বাচিত `references/*.md`-ফাইলের উপযুক্ত চেকলিস্ট সম্পন্ন করুন, `PASS / PASS MIT WARNUNGEN / FAIL`
   ফরম্যাটে প্রতিবেদন তৈরি করুন (কাঠামো নিচে)।
7. **প্রয়োজনে তালিকাভুক্ত করুন** — স্থায়ী নতুন ভূমিকা উপযুক্ত রেজিস্টারে যায় (`~/.claude/agents/`, প্রয়োজনে
   প্লাগইন-বান্ডল); একটি Companion-Worker-এর রেজিস্টার-এন্ট্রি লাগে না, শুধু একটি স্পষ্ট প্রথম কাজ-হস্তান্তর।

## যাচাই-প্রতিবেদন ফরম্যাট (উভয় নির্মাণপথের জন্য)

কাঠামো ইচ্ছাকৃতভাবে আদর্শ প্লাগইন থেকে নেওয়া (রূপ, শব্দ নয়) — চারটি সংক্ষিপ্ত অংশ:

- **অবস্থা:** PASS | PASS MIT WARNUNGEN | FAIL
- **গুরুতর বিষয়:** যা ভূমিকাটিকে অকেজো করে (অনুপস্থিত ট্রিগার-বর্ণনা, `Tools:` খুব বিস্তৃত/খুব সংকীর্ণ,
  মডেল `model-strategy` দিয়ে ন্যায্যতা প্রমাণিত নয়, বিদ্যমান ভূমিকা থেকে পৃথকীকরণ যাচাই হয়নি)
- **সতর্কতা:** সর্বোত্তম নয়, তবে কার্যকর (যেমন মূল মডেল স্তরবিন্যাস ছাড়া উত্তরাধিকারে পাওয়া, দীর্ঘস্থায়ী
  Companion-Worker-এর জন্য কোনো পুনর্নবীকরণ-মানদণ্ড নেই)
- **উত্তীর্ণ যাচাই + সুপারিশ:** কী ঠিক আছে, পরবর্তীতে কী করতে হবে

## সংশ্লিষ্ট Skill

- `model-strategy` — মডেল-নির্বাচন/স্তরবিন্যাস (ধাপ 3, এখানে শুধু উল্লেখ)।
- `swarm-operations` — বহু-ভূমিকা সহযোগিতার জন্য সোয়ার্ম-প্যাটার্ন।
- `choose-your-orchestrator` — উপযুক্ত অর্কেস্ট্রেশন প্যাটার্ন বেছে নেয়।
- `orchestrator` — ভাগ/অর্পণ/গ্রহণের প্রোটোকল।
- `agents-bridge` — প্রদানকারী-নিরপেক্ষ মেসেজিং/Presence/Locks, যদি নতুন ভূমিকাকে Claude Code-এর বাইরে
  Codex/Gemini/Kimi-এর সাথে যোগাযোগ করতে হয়।
- `skill-explorer` — নতুন ভূমিকা তৈরির **আগে** পরীক্ষা করে সক্ষমতাটি ইতিমধ্যে আছে কিনা (নকল এড়ানো)।

## Changelog

### 1.0.0 (2026-08-25)
- প্রথম সংস্করণ। ব্যবহারকারীর সিদ্ধান্ত M5 (`T-20260825-935905816`) অনুযায়ী `ellmos-skill-creator`-এর মাধ্যমে
  নির্মিত। Companion-Worker-প্যাটার্ন আনুষ্ঠানিক করেছে (প্রাথমিক সূত্র: `_control-center/_TICKETS/README.md`, অংশ „Leitprinzip
  (Kontext-Ökonomie)"), COMA-লাইফসাইকেল (প্রাথমিক সূত্র: `.MODULES/.ORCHESTRATION/coma/README.md`), এবং বিদ্যমান ভূমিকাগুলোর
  পর্যবেক্ষিত „Boss-Agent koordiniert Experten"-প্যাটার্ন। ইচ্ছাকৃতভাবে `model-strategy`/`swarm-operations`/
  `orchestrator`/`choose-your-orchestrator`/`agents-bridge`-এর দিকে রুট করে, নকল না করে। আদর্শ `agent-sdk-dev`
  (claude-plugins-official) ইনস্টল করা হয়নি, শুধু পড়া ও কাঠামোগতভাবে উদ্ধৃত (`.PLUGINS/CLAUDE.md` নিয়ম 5)।
