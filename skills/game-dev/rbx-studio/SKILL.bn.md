---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Roblox Studio ব্যবহার করে গেম ডেভেলপমেন্ট পরিচালনা — সেই ভিজ্যুয়াল এডিটর যেখানে 3D দৃশ্য নির্মাণ, পরীক্ষা এবং প্রকাশ করা হয়। এই স্কিলটি ব্যবহার করুন: Studio-র মূল বিষয়গুলো (Explorer, Workspace, play-test, place-কে .rbxl হিসেবে সংরক্ষণ), Rojo-র সাথে সংযোগ (Connect, scene-বনাম-code মোড), Roblox-Studio-MCP-এর মাধ্যমে Studio-র AI নিয়ন্ত্রণ (execute_luau, insert_from_creator_store, generate_material, screen_capture, Play/Stop, Console পড়া), সম্পূর্ণ asset-pipeline ওয়ার্কফ্লো (Creator Store → পরিষ্কার করা → kit → scene → .rbxl → Rojo দিয়ে প্রাণ সঞ্চার), এবং সর্বোপরি marketplace asset-এর জন্য বাধ্যতামূলক malware scan। \"embed an asset from the Store\", \"Studio MCP not working\", \"studios: []\", \"generate material\", \"save scene\", \"is this Roblox asset safe\", \"scripts disappear after Play\" — এসব বাক্যাংশেও এটি সক্রিয় হবে। বাংলা সমতুল্য বাক্যাংশ: \"Store থেকে asset যুক্ত করুন\", \"Studio MCP কাজ করছে না\", \"material তৈরি করুন\", \"scene সংরক্ষণ করুন\", \"এই Roblox asset কি নিরাপদ\", \"Play-এর পর script হারিয়ে যায়\"।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: bn
status: active
visibility: public
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 9d0fca2a40692abba63ce104ab8f69627490f5cd4adf2ead8a6da3ad00f4d7b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="rbx-studio banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **Note:** Roblox Corporation-এর সাথে কোনো সম্পর্ক নেই; "Roblox" তাদের মালিকানাধীন ট্রেডমার্ক। "rbx" হলো সাধারণ কমিউনিটি সংক্ষেপ।

# Roblox Studio — Editor, Test, Assets, MCP (Deutsch)

## Übersicht & Zweck

Roblox Studio হলো অফিসিয়াল এডিটর: 3D দৃশ্য নির্মাণ, play mode-এ গেম পরীক্ষা, Creator Store থেকে asset যুক্ত করা এবং place প্রকাশ করা। Rojo ওয়ার্কফ্লোতে Studio **scene** (Workspace, Terrain, স্থাপিত model) এবং **testing** নিয়ন্ত্রণ করে — **code** আসে Rojo-র মাধ্যমে filesystem থেকে (দেখুন skill `/rojo`)।

এই skill-এ রয়েছে: Studio-র মূল বিষয়, scene ও code কাজের স্পষ্ট বিচ্ছেদ, Roblox-Studio-MCP-এর মাধ্যমে AI নিয়ন্ত্রণ, এবং প্রতিটি marketplace asset-এর জন্য **বাধ্যতামূলক malware scan** সহ asset ওয়ার্কফ্লো।

## Basics

- **Explorer** — সব instance-এর ট্রি (Workspace, ServerScriptService, ReplicatedStorage, …)। Rojo সক্রিয় থাকলে ম্যাপ করা অংশগুলো filesystem থেকে লাইভ পূর্ণ হয়।
- **Play-Test** — সবুজ Play বোতাম (বা F5) একটি লোকাল server+client সেশন শুরু করে। প্রতিটি শুরুর পর **Output console-এ ত্রুটি পরীক্ষা করুন** — এটি সবচেয়ে গুরুত্বপূর্ণ debug অভ্যাস।
- **Place সংরক্ষণ** — File → Save As → `.rbxl` (binary) অথবা `.rbxlx` (XML, diff-যোগ্য)। সংরক্ষিত place-এ থাকে **scene**। Code থাকে filesystem-এ, place-এ নয়।

## Critical workflow: scene mode বনাম code mode

Connect করার সময় Rojo সব ম্যাপ করা script অংশ filesystem-এর কনটেন্ট দিয়ে ওভাররাইট করে। `Workspace` (3D scene) ম্যাপ করা থাকে না এবং অক্ষত থাকে। এখান থেকেই দৈনন্দিন কাজের সবচেয়ে গুরুত্বপূর্ণ নিয়ম আসে — দুই মোড কখনো মেশাবেন না:

**Mode A — scene সম্পাদনা (Rojo OFF):**
1. Rojo server বন্ধ করুন (`taskkill //F //IM rojo.exe` বা Ctrl+C)।
2. Studio-তে place খুলুন, asset বসান, জগৎ নির্মাণ ও সাজান।
3. File → Save → `.rbxl`-এ এখন নতুন scene থাকে।

**Mode B — code পরীক্ষা (Rojo ON):**
1. Studio-তে একই place খুলুন।
2. `rojo serve` চালু করুন → Studio-র Rojo plugin-এ → Connect।
3. Play চাপুন এবং পরীক্ষা করুন। Rojo script-গুলো সিঙ্ক করে; Workspace আসে `.rbxl` থেকে।
4. Rojo চলাকালীন **সংরক্ষণ করবেন না** (অন্যথায় Rojo-র অবস্থা `.rbxl`-এ জমে যাবে)।

এভাবে scene কাজ (Studio) ও code কাজ (editor + Rojo) সমান্তরালে এবং দ্বন্দ্বহীনভাবে চলতে পারে — শিল্পীরা scene নির্মাণ করেন, ডেভেলপাররা code লেখেন।

## Roblox-Studio-MCP — AI Studio নিয়ন্ত্রণ করে

Roblox-Studio-MCP Claude/Gemini/Codex-কে একটি **চলমান** Studio instance সরাসরি নিয়ন্ত্রণ করতে দেয়: code চালানো, পরিদর্শন, Play/Stop, Console পড়া, asset যুক্ত করা। এটি Rojo-র জায়গা নেয় না — পরিপূরক: স্থায়ী code পরিবর্তনের জন্য Rojo, আর পরিদর্শন, পরীক্ষা, asset যুক্তকরণ ও material তৈরির জন্য MCP।

```
Editor + Rojo  ──(persistenter Code-Sync)──►  Studio (laufend)  ◄──(Inspektion/Test/Insert)──  MCP ◄── KI
```


### উপলব্ধ MCP টুল (সাধারণ)

| Tool | উদ্দেশ্য |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | খোলা instance-গুলোর তালিকা / সক্রিয়টি নির্বাচন |
| `search_game_tree` / `inspect_instance` | hierarchy-তে অনুসন্ধান / properties পড়া |
| `execute_luau` | সরাসরি Studio-তে Luau code চালানো |
| `script_read` / `script_grep` / `script_search` | script বিশ্লেষণ |
| `multi_edit` | ব্যাচে একাধিক instance/script পরিবর্তন |
| `start_stop_play` | Play/Stop নিয়ন্ত্রণ |
| `get_console_output` | Output log পড়া |
| `screen_capture` | দৃশ্যের স্ক্রিনশট |
| `insert_from_creator_store` | Creator Store থেকে asset যুক্ত করা |
| `generate_material` | AI material/texture (MaterialVariant) তৈরি |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | input সিমুলেট করা |

### সেটআপ (ব্যবহারকারী-নিরপেক্ষ)

MCP Studio-র সাথে আসা একটি server হিসেবে চলে, প্রায়শই একটি পাতলা JSON-filter wrapper-এর মাধ্যমে সংযুক্ত (এটি কিছু client-কে অন্যথায় পার্স করতে না পারা non-JSON banner ফিল্টার করে):

- MCP batch (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- ঐচ্ছিক wrapper: `<your roblox-mcp wrapper>`
  (এই সিস্টেমে থাকলে; Claude/Codex/Gemini একসাথে ব্যবহার করে)
- Client configs: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

উদাহরণ entry (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```


### সাধারণ MCP সমস্যা

| লক্ষণ | অর্থ / সমাধান |
| --- | --- |
| `studios: []` বা `Not connected to WS host` | তাৎক্ষণিকভাবে "ভাঙা" নয়: `initialize` পাঠান → 2–3 সেকেন্ড অপেক্ষা করুন → `list_roblox_studios`; অন্যথায় Studio পুনরায় চালু করুন |
| `Error: connection closed: initialized request` | Studio আদৌ খোলা নেই — Studio চালু করুন, place লোড করুন, আবার চেষ্টা করুন |
| MCP দিয়ে লেখা script Play/Stop-এর পর হারিয়ে গেছে | MCP-এর code সম্পাদনা স্থায়ী নয় — স্থায়ী code পরিবর্তনের জন্য **Rojo** ব্যবহার করুন |
| plugin VM-এ `require()` দিয়ে মান ভুল | plugin VM-এর নিজস্ব require cache আছে — যাচাই করতে `.Source` সরাসরি পড়ুন বা Play-এর পর server log দেখুন |

## Asset pipeline (Creator Store → গেম)

প্রথমে greybox (gameplay), পরে asset (release-এর আগে)। প্রমাণিত ক্রম:

```
STORE DURCHSUCHEN   → z. B. "medieval" → mehrere Kandidaten laden
AUSSORTIEREN        → stilfremde/hässliche raus, 5–8 passende behalten
BEREINIGEN          → ALLE Scripts entfernen (Malware!), nur Geometrie/Meshes behalten
KIT / SET BAUEN     → aus Basis-Assets Varianten ableiten (gleiche Materials/Proportionen)
SZENE BAUEN (Studio)→ Assets zur Kulisse zusammensetzen (Dorf, Arena, Park)
ALS .RBXL SPEICHERN → die Kulisse ist die "Bühne"
ROJO BELEBT ES      → Scripts/Gameplay/HUD kommen per Rojo dazu; Workspace bleibt unangetastet
```


**Variant কৌশল ("modular kit"):** একটি ভালো base asset নিন এবং তা থেকে একটি পুরো সেট তৈরি করুন (ঘর → টাওয়ার, খামার, কামারশালা, ধ্বংসাবশেষ)। সবাই material, রং ও অনুপাত ভাগ করে → কম প্রচেষ্টায় একই রকম চেহারা, পেশাদার স্টুডিওগুলো যেভাবে করে।

**Asset উৎস (অগ্রাধিকার):** Creator Store (বিনামূল্যে, বিশাল, **malware check বাধ্যতামূলক**) → AI material (`generate_material`) → নিজের mesh (Blender → .fbx) → কেনা asset pack।

## বাধ্যতামূলক: marketplace asset-এর জন্য malware scan

Creator Store asset-এ obfuscated ক্ষতিকর script থাকতে পারে (backdoor, remote code, bot-network hook)। ব্যবহারের আগে **প্রতিটি** আমদানি করা asset scan করুন এবং সব script সরান — শুধু geometry/mesh রাখুন।

- Pattern reference: [`references/malware-patterns.md`](references/malware-patterns.md) — 8টি পরিচিত obfuscation pattern (উল্টানো attribute payload, নকল system script, remote `require()`, `loadstring`, `string.char`, `getfenv/setfenv`, লুকানো Values, বিলম্বিত execution)।
- Scanner: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — `execute_luau`-এর মাধ্যমে (বা Command Bar-এ) Studio-তে চালান; এটি একটি instance সব pattern-এর সাথে মিলিয়ে দেখে এবং প্রাপ্তি জানায়।

**তাৎক্ষণিক লাল পতাকা:** শুধু সাজসজ্জার model-এ একটি বড় script · attribute-এ উল্টানো string · `require(<number>)` · `loadstring` · `HttpService` এমন asset-এ যার networking-এর প্রয়োজন নেই। সন্দেহ হলে: script মুছে ফেলুন। প্রাপ্তি নথিভুক্ত করুন (যেমন reference pipeline-এ `_malware_reports/YYYY-MM-DD_*.md`)।

## গুরুত্বপূর্ণ Luau/Studio ফাঁদ (অংশবিশেষ)

Studio-তে সবচেয়ে সাধারণ যেগুলো সমস্যা করে — সম্পূর্ণ তালিকা রাখে skill `/rbx-dev`:

- `Model.Position` বিদ্যমান নেই → `model:GetPivot().Position`।
- `tick()` অপ্রচলিত → `os.clock()` / `workspace:GetServerTimeNow()`।
- `SetPrimaryPartCFrame()` অপ্রচলিত → `model:PivotTo(cf)`।
- DataStore কল **সর্বদা** `pcall`-এর ভেতরে।
- একই উচ্চতায় Baseplate + procedural floor → Z-fighting (ঝিকিমিকি): baseplate সরান বা floor +0.1 stud উঁচু করুন।
- প্রতি procedurally তৈরি ঘরে part budget (~50–80 part) লক্ষ্য রাখুন।

## আরও পড়া

- সহোদর skill: `/rojo` (সিঙ্ক, প্রকল্প সেটআপ), `/game-design` (ভূমিকা, ওয়ার্কফ্লো, GDD), meta skill `/rbx-dev` (architecture pattern + সব Luau শিক্ষা)।
- Engine/Creator docs: Context7 MCP (`/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) বা <https://create.roblox.com/docs>।
- Reference pipeline (থাকলে): `<your Roblox project pipeline>` (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`)।

## Änderungsprotokoll

### 1.0.0 (2026-06-17)
- প্রাথমিক সংস্করণ। `.ROBLOX` pipeline (ROBLOX_MCP_FAQ, ASSET_PIPELINE, PATTERNS, LESSONS_LEARNED) থেকে সংকলিত, ব্যবহারকারী-নিরপেক্ষভাবে লেখা।
