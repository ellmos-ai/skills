---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Roblox গেম ডেভেলপমেন্টের জন্য Rojo সহ সম্পূর্ণ মেটা-স্কিল — সেই এন্ট্রি পয়েন্ট যা তিনটি বিশেষজ্ঞ স্কিল `/rojo` (ফাইলসিস্টেম→Studio সিঙ্ক, প্রজেক্ট সেটআপ), `/rbx-studio` (এডিটর, MCP, অ্যাসেট, ম্যালওয়্যার স্ক্যান) এবং `/game-design` (ভূমিকা, ওয়ার্কফ্লো, GDD) সম্পর্কে জানে এবং এগুলোকে একত্রিত করে। যেকোনো Roblox গেম-ডেভ কাজের জন্য এই স্কিল ব্যবহার করুন: Roblox গেম পরিকল্পনা/নির্মাণ/সেটআপ, নতুন প্রজেক্টের স্ক্যাফোল্ডিং, কোড আর্কিটেকচার সংজ্ঞায়িত করা (Main + ম্যানেজার মডিউল, _G.ClientState + HUD, GameEnums-এ remotes), Luau/Roblox-এর ফাঁদ এড়ানো, অথবা কোন Roblox বিশেষজ্ঞ স্কিল উপযুক্ত তা স্পষ্ট না হলে — রাউটিং এখান থেকেই হয়। \"develop Roblox game\", \"build Roblox game\", \"new Roblox project\", \"Luau project structure\", \"how do I organize Roblox code\", \"Roblox dev setup\" — এসব ক্ষেত্রেও ট্রিগার হয়। বাংলা ট্রিগার: \"Roblox গেম তৈরি করো\", \"নতুন Roblox প্রজেক্ট\", \"Luau প্রজেক্ট কাঠামো\", \"Roblox কোড কীভাবে সাজাব\", \"Roblox ডেভ সেটআপ\" — এগুলোতেও ট্রিগার হয়।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: bn
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 0a489cbd24500517df731518ee92ae3d5881d249873c48d16af4a4d86f6b63a4
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="rbx-dev banner">

> **দ্রষ্টব্য:** Roblox Corporation-এর সাথে সম্পর্কিত/অধিভুক্ত নয়; „Roblox" তাদের মালিকদের ট্রেডমার্ক। „rbx" হলো প্রচলিত কমিউনিটি সংক্ষেপ।

# Roblox-Dev — Roblox গেম ডেভেলপমেন্টের জন্য মেটা-স্কিল

## উদ্দেশ্য

Rojo-ভিত্তিক, ভার্সন-নিয়ন্ত্রণযোগ্য ওয়ার্কফ্লো সহ Roblox গেম-ডেভের কেন্দ্রীয় এন্ট্রি পয়েন্ট।
এই স্কিল সামগ্রিক জ্ঞান — প্রজেক্ট কাঠামো, আর্কিটেকচার প্যাটার্ন এবং মূল Luau-ফাঁদ — একত্রিত করে
এবং বিশেষ প্রশ্নের জন্য তিনটি সাব-স্কিলে পাঠায়:

| সাব-স্কিল | কিসের জন্য |
| --- | --- |
| **`/rojo`** | ফাইলসিস্টেম→Studio সিঙ্ক, `default.project.json`, rokit/Wally/Lune, প্রজেক্ট কঙ্কাল, সিঙ্ক সমস্যা |
| **`/rbx-studio`** | Studio-পরিচালনা, Scene-বনাম-Code মোড, Studio-MCP, অ্যাসেট পাইপলাইন, **ম্যালওয়্যার স্ক্যান** |
| **`/game-design`** | ভূমিকা ও উপকাজ, ডেভেলপমেন্ট-চেইন, Game Design Document (KONZEPT.md), Multi-Agent |

> রাউটিং নিয়ম: **সিঙ্ক/বিল্ড/সেটআপ** নিয়ে হলে → `/rojo`। **এডিটর/অ্যাসেট/Studio-এ পরীক্ষা** নিয়ে হলে
> → `/rbx-studio`। **কনসেপ্ট/ভূমিকা/প্রক্রিয়া** নিয়ে হলে → `/game-design`। **কোড-আর্কিটেকচার,
> Luau-ফাঁদ বা সামগ্রিক ধারা** নিয়ে হলে → এখানেই থাকুন।

## এক নজরে স্ট্যাক

- **ভাষা:** Luau (`.luau`, `.lua` নয়)। কোড ইংরেজিতে, মন্তব্য/ডকুমেন্টেশন জার্মানে, UI-টেক্সট জার্মানে।
- **সিঙ্ক:** rokit-এর মাধ্যমে Rojo (পিন করা টুল-ভার্সন)। ফাইলসিস্টেম = সত্যের উৎস।
- **টুল:** Rojo (সিঙ্ক/বিল্ড), Lune (Studio-এর বাইরে টেস্ট/স্ক্রিপ্ট), Wally (প্যাকেজ),
  ঐচ্ছিক Knit (Service-/Controller-ফ্রেমওয়ার্ক, নতুন প্রজেক্ট), Selene (Linter)।
- **নিয়ন্ত্রণ:** AI-চালিত ইন্সপেকশন/টেস্ট/অ্যাসেট-ইনসার্শনের জন্য Roblox-Studio-MCP।

## প্রজেক্ট কাঠামো (স্ট্যান্ডার্ড)

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

একটি কঙ্কাল `/rojo` দ্বারা `scaffold_roblox_project.sh`-এর মাধ্যমে তৈরি হয়।

## আর্কিটেকচার প্যাটার্ন

**সার্ভার — Main + ম্যানেজার-মডিউল।** প্রতি প্রজেক্টে শুধুমাত্র **একটি** স্ক্রিপ্ট: `Main.server.luau`। এটি কেন্দ্রীয়ভাবে Remotes-ফোল্ডার তৈরি করে এবং `require()`-এর মাধ্যমে সমস্ত ফিচার-মডিউল লোড করে:
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
সার্ভারের অন্যান্য সব ফাইল `.luau` (ModuleScripts)।

**ক্লায়েন্ট — শেয়ার্ড State + HUD।** GameClient একটি শেয়ার্ড State লেখে, HUD সেটি Heartbeat-এ পড়ে:
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — GameEnums-এ কেন্দ্রীভূত।** Remote-নামগুলো একবার `GameEnums.Remotes`-এ সংজ্ঞায়িত করুন; সার্ভার সেখান থেকে Events তৈরি করে, ক্লায়েন্ট একই নাম দিয়ে সেগুলো খোঁজে। এতে সার্ভার ও ক্লায়েন্টের মধ্যে কোনো স্ট্রিং-অমিল হয় না।

## একটি গেমের সামগ্রিক ধারা

1. **কনসেপ্ট** (`/game-design`): KONZEPT.md — ধরন, USP, 3–4 মূল মেকানিক, মনিটাইজেশন।
2. **সেটআপ** (`/rojo`): কঙ্কাল স্ক্যাফোল্ড করা, `default.project.json`-ম্যাপিং নির্ধারণ।
3. **ব্যাকএন্ড**: Config → GameEnums → *Defs → Main.server → *Manager।
4. **ফ্রন্টএন্ড**: GameClient → HUD।
5. **Greybox-প্লেটেস্ট** (`/rbx-studio`): প্রথমে Gameplay, Parts + প্রয়োজনে AI-Materials।
6. **অ্যাসেট-আপগ্রেড** (`/rbx-studio`): Creator-Store-অ্যাসেট, **ম্যালওয়্যার স্ক্যান**, Scene হিসেবে .rbxl।
7. **টেস্ট** (`/game-design`): QA + গেম-সমালোচক + Persona ব্লাইন্ড টেস্ট, পুনরাবৃত্তি।
8. **রিলিজ** (`/game-design` Business-ভূমিকা): Store-পেজ, মনিটাইজেশন, Live-Ops।

## Luau-/Roblox-ফাঁদ (সংক্ষিপ্ত তালিকা)

সবচেয়ে সাধারণ ফাঁদগুলো — সম্পূর্ণ, মন্তব্যসহ তালিকা:
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md)।

- একই লাইনে আরও কোড থাকলে `task.wait(x)`-এর পরে Semicolon।
- `Model.Position` নেই → `model:GetPivot().Position`।
- Dictionary-তে `#table` = 0 → ম্যানুয়ালি গণনা করুন।
- `mouse.Hit` nil হতে পারে → ব্যবহারের আগে যাচাই করুন।
- DataStore-কল **সবসময়** `pcall`-এর ভেতরে।
- `tick()` deprecated → `os.clock()`; `SetPrimaryPartCFrame` → `PivotTo`।
- Event-নামগুলো কেন্দ্রীয়ভাবে `GameEnums.Remotes`-এ; সব Remotes `Main.server.luau`-এ তৈরি করুন।
- কোনো বৃত্তাকার `require` নয় (নইলে Deadlock)।
- `require()` শুধু `.luau`-ModuleScripts-এ, কখনো Scripts/LocalScripts-এ নয়।

## প্রতিটি Commit-এর আগে (চেকলিস্ট)

- [ ] মাল্টি-স্টেটমেন্টে `task.wait(...)`-এর পরে Semicolon
- [ ] কোনো `Model.Position` নেই, কোনো `tick()` নেই, কোনো `SetPrimaryPartCFrame` নেই
- [ ] DataStore `pcall`-এ, `mouse.Hit`-এর nil-পরীক্ষা হয়েছে
- [ ] Event-নাম Server↔Client-এ মেলে (GameEnums-এর মাধ্যমে)
- [ ] সব RemoteEvents `Main.server.luau`-এ তৈরি
- [ ] কোনো বৃত্তাকার Require নেই
- [ ] Marketplace-অ্যাসেট স্ক্যান করা হয়েছে (`/rbx-studio` → ম্যালওয়্যার স্ক্যান), রিপোর্ট সংরক্ষিত

## জ্ঞানের উৎস

- **সাম্প্রতিক Engine-/Creator-ডকুমেন্টেশন:** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine` (Engine-API) এবং `/roblox/creator-docs`
  (Tutorials/Guides); বিকল্প <https://create.roblox.com/docs>।
- **রেফারেন্স-পাইপলাইন** (যদি এই সিস্টেমে থাকে): `<your Roblox project pipeline>` —
  যার মধ্যে আছে `SKILL.md`, `GUIDE.md`, `LESSONS_LEARNED.md`, `ROJO_FAQ.md`, `ROBLOX_MCP_FAQ.md`,
  `AGENT_ROLES.md`, `_malware_reports/PATTERNS.md`, `_knowledge/` (স্থানীয় API-ক্যাশ)।

## Changelog

### 1.0.0 (2026-06-17)
- প্রাথমিক সংস্করণ। `/rojo`, `/rbx-studio`, `/game-design`-এর উপর মেটা-স্কিল; প্রজেক্ট কাঠামো,
  আর্কিটেকচার প্যাটার্ন এবং `.ROBLOX`-পাইপলাইন থেকে নির্যাস নেওয়া Luau-শিক্ষা, ব্যবহারকারী-নিরপেক্ষ।
