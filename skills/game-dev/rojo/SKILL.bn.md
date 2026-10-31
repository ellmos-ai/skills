---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Rojo পরিচালনা — পেশাদার Roblox ডেভেলপমেন্টের জন্য একটি ফাইলসিস্টেম-থেকে-Roblox-Studio সিঙ্ক টুল, যা Studio এডিটরের পরিবর্তে VS Code / Claude Code-এ ব্যবহার করা হয়। Rojo জড়িত যেকোনো ক্ষেত্রে এই skill ব্যবহার করুন: `rojo serve`/`rojo build`, `default.project.json` লেখা বা ডিবাগ করা, rokit/rokit.toml এবং টুলের সংস্করণ (Rojo, Lune, Wally), nested বনাম flat path mapping (ReplicatedStorage.Project.shared), connect/port/sync সমস্যা, অথবা যখন কোনো Roblox প্রজেক্টের skeleton তৈরি করতে হবে। \"rojo connect not working\", \"scripts end up in the wrong place in Studio\", \"how do I map src/ to Studio\", \"port 34872 in use\", \"ModuleScript vs Script in Rojo\" — এই ধরনের ট্রিগারেও এটি সক্রিয় হবে। বাংলা ট্রিগার: \"rojo connect কাজ করছে না\", \"স্ক্রিপ্টগুলো Studio-তে ভুল জায়গায় যাচ্ছে\", \"src/ কীভাবে Studio-তে map করব\", \"পোর্ট 34872 ব্যবহৃত হচ্ছে\", \"Rojo-তে ModuleScript বনাম Script\"।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: bn
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 2901142af2c1b72480d9cfaea5111557a8c6003c6b51aefa4bab02a0e168b742
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="rojo banner">

# Rojo — ফাইলসিস্টেম → Roblox Studio Sync

## উদ্দেশ্য

Rojo একটি সাধারণ ফাইলসিস্টেম প্রজেক্ট (`.luau` ফাইল, `src/`-এ থাকা, Git দিয়ে ভার্সন নিয়ন্ত্রিত) কে Roblox Studio-র সাথে সংযুক্ত করে।
আপনি আপনার পছন্দের এডিটরে (VS Code, Claude Code) কোড লেখেন, Rojo সেটি একটি চলমান Studio ইনস্ট্যান্সে লাইভ সিঙ্ক করে। এভাবে Roblox কোড ভার্সন-নিয়ন্ত্রণযোগ্য, diff-যোগ্য এবং প্রকৃত টুল দিয়ে সম্পাদনাযোগ্য হয় — Studio-র বিল্ট-ইন স্ক্রিপ্ট এডিটরে আটকে থাকতে হয় না।

Rojo-র setup, `default.project.json` mapping, টুলচেইন (rokit/Wally/Lune) এবং সাধারণ sync সমস্যার সব কিছুর জন্য এই skill ব্যবহার করুন।

## মানসিক মডেল

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**মূল নিয়ম:** ফাইলসিস্টেমই সত্যের উৎস। প্রতিটি connect-এ Rojo ম্যাপ করা Studio অংশগুলোকে ফাইলসিস্টেমের কনটেন্ট দিয়ে ওভাররাইট করে। তাই কোড **কখনোই** Studio-তে সম্পাদনা করবেন না (পরের sync-এ হারিয়ে যাবে), শুধু এডিটরে করুন। `Workspace` (3D দৃশ্য, Terrain) Rojo দ্বারা ম্যাপ করা হয় **না** এবং অক্ষত থাকে — দৃশ্য-বনাম-কোড ওয়ার্কফ্লোর জন্য `/rbx-studio` skill দেখুন।

## ফাইল এক্সটেনশন → Roblox টাইপ (Rojo কনভেনশন)

Rojo ফাইলের এক্সটেনশন থেকে ইনস্ট্যান্সের টাইপ নির্ধারণ করে। এটি সবচেয়ে সাধারণ ভুলের উৎস:

| ফাইল              | Roblox টাইপ    | `require()`-যোগ্য | ভূমিকা                     |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **হ্যাঁ**          | লজিক মডিউল, সংজ্ঞা |
| `Foo.server.luau`  | Script        | না              | Server entry point        |
| `Foo.client.luau`  | LocalScript   | না              | Client entry point        |
| `init.luau`        | নিজেই ফোল্ডার নোডে পরিণত হয় | হ্যাঁ | ফোল্ডারকে ModuleScript বানায় |

> সাধারণ নিয়ম: শুধু **entry point** গুলো `.server.luau`/`.client.luau`। `require()` দিয়ে যা লোড হয়, তা **অবশ্যই** `.luau` ModuleScript হতে হবে। Script/LocalScript-এর উপর `require()` করলে "Attempted to call require with invalid argument(s)" ত্রুটি আসে।

## CLI কমান্ড

```bash
rojo serve default.project.json     # Live-Sync-Server starten (Standard-Port 34872)
rojo serve                          # nutzt default.project.json automatisch
rojo build default.project.json -o game.rbxlx   # einmaliger Build → Place-Datei (XML)
rojo build default.project.json -o game.rbxl    # Build → Place-Datei (binär)
rojo plugin install                 # Rojo-Studio-Plugin installieren (einmalig)
rojo --version                      # installierte Version prüfen
```

`rojo serve`-এর পর: Studio-তে Rojo প্লাগইন খুলুন → **Connect** (localhost:34872)।
`rojo build`-এর জন্য চলমান Studio দরকার নেই — CI, smoke test এবং রিলিজের জন্য আদর্শ।

## `default.project.json` — mapping

এই ফাইলটি ফাইলসিস্টেমের পথগুলোকে Roblox datamodel হায়ারার্কিতে ম্যাপ করে। কী (key):

- `name` — প্রজেক্টের নাম (প্রদর্শনের জন্য)
- `$className` — নোডের Roblox ক্লাস (`DataModel`, `ServerScriptService`, `Folder`, …)
- `$path` — এই নোডের অধীনে সিঙ্ক হওয়া ফাইলসিস্টেম পথ (প্রজেক্টের রুট থেকে আপেক্ষিক)

একটি ব্যবহারযোগ্য স্ট্যান্ডার্ড টেমপ্লেট রয়েছে [`assets/default.project.json`](assets/default.project.json)-এ।

### Flat বনাম nested — সবচেয়ে গুরুত্বপূর্ণ সিদ্ধান্ত

আপনার কোডকে অবশ্যই mapping-এর সাথে মিলতে হবে। দুটি বিকল্প:

**Flat** — `src/server`-এর কনটেন্ট সরাসরি `ServerScriptService`-তে যায়:
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ কোড রেফার করে যেমন `ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`।

**Nested** — কনটেন্ট `ServerScriptService.ProjektName`-এর ভেতরে যায়:
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ কোড রেফার করে `ReplicatedStorage.ProjektName.shared.Config` ইত্যাদি।

দুটিই বৈধ। প্রজেক্টজুড়ে **একটি** বিকল্প বেছে নিন এবং প্রতিটি `require`/`WaitForChild` পথ তার সাথে সামঞ্জস্যপূর্ণ রাখুন। Mismatch হলে লক্ষণ: `WaitForChild(...)` অনির্দিষ্টকাল ঝুলে থাকে (Infinite yield), কারণ প্রত্যাশিত নোডটি অন্য জায়গায় আছে।

## rokit-এর মাধ্যমে টুলচেইন

[rokit](https://github.com/rojo-rbx/rokit) হলো টুলচেইন ম্যানেজার। প্রজেক্টে (বা প্যারেন্ট ফোল্ডারে) একটি `rokit.toml` সঠিক টুল সংস্করণ পিন করে → সব মেশিনে পুনরুৎপাদনযোগ্য বিল্ড। এটি না থাকলে `Failed to find tool 'rojo' in any project manifest file` আসে।

স্ট্যান্ডার্ড `rokit.toml` (দেখুন [`assets/rokit.toml`](assets/rokit.toml)):
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> সংস্করণ নোট: 7.4.4 হলো রেফারেন্স পাইপলাইনে সর্বত্র পিন করা সংস্করণ। নতুন প্রজেক্ট 7.6.x-এ যেতে পারে — আগে `rojo build` দিয়ে প্রজেক্টের বিপরীতে যাচাই করুন, কারণ মেজর ভার্সনের মধ্যে প্রজেক্ট ফরম্যাট বদলাতে পারে।

ক্লোন/সেটআপের পর: `rokit install` সব পিন করা টুল নামিয়ে আনে।

- **Lune** — Studio-র বাইরে Luau রানার (unit test, build স্ক্রিপ্ট, asset প্রক্রিয়াকরণ)।
- **Wally** — প্যাকেজ ম্যানেজার: `wally install` → `Packages/` → Studio-তে `ReplicatedStorage.Packages`-এর অধীনে। ডিপেন্ডেন্সি `wally.toml`-এ থাকে (দেখুন [`assets/wally.toml`](assets/wally.toml)), যেমন ফ্রেমওয়ার্ক `sleitnick/knit@1.7.0`।

## নতুন প্রজেক্ট তৈরি

[`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) স্ক্রিপ্টটি একটি সম্পূর্ণ Rojo skeleton তৈরি করে (project.json, rokit.toml, wally.toml, `src/{shared,server,client,gui}/`-এর starter ফাইল, KONZEPT স্টাব):

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # flaches Mapping (Default)
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # verschachteltes Mapping
```

এরপর: `cd MeinSpiel && rokit install && rojo serve`।

## সমস্যা সমাধান

| লক্ষণ | কারণ | সমাধান |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | `rokit.toml` নেই | প্রজেক্ট/প্যারেন্ট ফোল্ডারে Rojo পিনসহ `rokit.toml` তৈরি করুন, `rokit install` চালান |
| `require` "invalid argument(s)" ছোঁড়ে | `require()` একটি Script/LocalScript-এর উপর | শুধু `.luau` ModuleScript-ই require-যোগ্য; এক্সটেনশন যাচাই করুন |
| Port 34872 ব্যস্ত (`os error 10048`) | পুরোনো Rojo প্রক্রিয়া চলছে | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F`, তারপর আবার `rojo serve` |
| Scripts Studio-তে ভুল জায়গায় যায় | Flat বনাম nested mapping-এর অমিল (বা উল্টো) | `default.project.json` কোড পথের সাথে মিলিয়ে সামঞ্জস্য করুন (উপরে দেখুন) |
| `WaitForChild` অনির্দিষ্টকাল ঝুলে থাকে | প্রত্যাশিত নোড নেই / তৈরির আগে সার্ভার ত্রুটি | **প্রথমে Server console-এ ত্রুটি দেখুন**; mapping ও তৈরির ক্রম যাচাই করুন |
| ফাইল নাম বদলের পর sync হয় না | Rojo rename তাৎক্ষণিক ধরতে পারে না | সার্ভার বন্ধ (Ctrl+C) করে নতুন করে চালান, Studio-তে Disconnect→Reconnect |
| Reconnect-এর পর Studio-তে পরিবর্তন হারায় | Filesystem-এর বদলে Studio-তে সম্পাদনা | কোড **শুধু** এডিটরে বদলান; Rojo ম্যাপ করা অংশ ওভাররাইট করে |

### জানা Rojo সীমাবদ্ধতা

1. **Terrain/Workspace sync নেই** — 3D দৃশ্য ও Terrain Studio-তে বানান বা কোড দিয়ে তৈরি করুন।
2. **`.rbxl` merge নেই** — Place ফাইল বাইনারি, git-এ merge করা যায় না। কখনোই প্রাথমিক উৎস হিসেবে নয়।
3. **Play মোডে লাইভ sync নেই** — Play চলাকালীন পরিবর্তন Stop-এ বাতিল হয়ে যায়।
4. **Git Bash path translation** — `/c/...` `C:/...`-তে অনুবাদ হতে পারে এবং Rojo পথ ভেঙে দিতে পারে; সন্দেহ হলে আপেক্ষিক পথ বা নেটিভ Windows পথ ব্যবহার করুন।

## Linting (Selene)

Roblox Luau প্রজেক্ট সাধারণত **Selene** দিয়ে lint করা হয় (`selene.toml` রুটে,
`std = "roblox"`)। `_G`-এর মতো globals প্রজেক্ট শেয়ার্ড client-state-এর জন্য ব্যবহার করলে `global_usage = "allow"` দিয়ে অনুমতি দিন। Roblox API সংজ্ঞা সম্বলিত ডিরেক্টরি (`roblox.yml`) থেকে Selene চালান।

## আরও পড়াশোনা

- সহোদর skills: `/rbx-studio` (Studio ব্যবহার, MCP, assets), `/game-design`
  (ভূমিকা, ওয়ার্কফ্লো, GDD), মেটা-skill `/rbx-dev` (তিনটিকে একত্র করে + আর্কিটেকচার প্যাটার্ন)।
- বর্তমান engine/Rojo ডকুমেন্টেশন: Context7 MCP (`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) অথবা
  <https://rojo.space/docs/>।
- এই সিস্টেমে থাকলে, একটি প্রজেক্ট-সমৃদ্ধ রেফারেন্স পাইপলাইন রয়েছে
  `<your Roblox project pipeline>`-এর অধীনে (যেমন `ROJO_FAQ.md`, `SKILL.md`)।

## Changelog

### 1.0.0 (2026-06-17)
- প্রাথমিক সংস্করণ। `.ROBLOX` পাইপলাইন (ROJO_FAQ, ROJO_START, _template) থেকে সংকলিত, ব্যবহারকারী-নিরপেক্ষভাবে উপস্থাপিত।

## সম্পর্কিত Skills

- `roblox-team-lock` — একই প্রজেক্টে একাধিক এজেন্ট কাজ করলে ফাইল, Studio ও MCP claims। আগে পড়ুন, তারপর claim করুন, তারপর কাজ করুন, তারপর ছেড়ে দিন।
