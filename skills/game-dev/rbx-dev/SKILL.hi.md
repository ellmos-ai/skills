---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Roblox गेम विकास के लिए मेटा-स्किल, Rojo के साथ — वह प्रवेश बिंदु जो तीन विशेषज्ञ स्किल्स `/rojo` (फ़ाइलसिस्टम→Studio सिंक, प्रोजेक्ट सेटअप), `/rbx-studio` (एडिटर, MCP, एसेट्स, मैलवेयर स्कैन) और `/game-design` (भूमिकाएँ, वर्कफ़्लो, GDD) को जानता और एकीकृत करता है। इस स्किल का उपयोग किसी भी Roblox गेम-डेव कार्य के लिए करें: Roblox गेम की योजना बनाना/निर्माण करना/सेटअप करना, नया प्रोजेक्ट स्कैफ़ोल्ड करना, कोड आर्किटेक्चर परिभाषित करना (Main + manager modules, _G.ClientState + HUD, GameEnums में remotes), Luau/Roblox की समस्याओं से बचना, या जब यह स्पष्ट न हो कि कौन सी Roblox विशेषज्ञ स्किल उपयुक्त है — रूटिंग यहीं से होती है। \"develop Roblox game\", \"build Roblox game\", \"new Roblox project\", \"Luau project structure\", \"how do I organize Roblox code\", \"Roblox dev setup\" „Roblox गेम विकसित करें“, „Roblox गेम बनाएँ“, „नया Roblox प्रोजेक्ट“, „Luau प्रोजेक्ट संरचना“, „Roblox कोड को कैसे व्यवस्थित करूँ“, „Roblox डेव सेटअप“ पर भी ट्रिगर करें।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: hi
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 0a489cbd24500517df731518ee92ae3d5881d249873c48d16af4a4d86f6b63a4
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="rbx-dev banner">

> **नोट:** Roblox Corporation से संबद्ध नहीं; „Roblox" उनके स्वामियों का ट्रेडमार्क है। „rbx" समुदाय का प्रचलित संक्षेप है।

# Roblox-Dev — Roblox-गेम विकास के लिए मेटा-स्किल

## उद्देश्य

Rojo-आधारित, संस्करण-नियंत्रित वर्कफ़्लो के साथ Roblox game dev का केंद्रीय प्रवेश बिंदु।
यह स्किल समग्र ज्ञान — प्रोजेक्ट संरचना, आर्किटेक्चर पैटर्न और सबसे महत्वपूर्ण Luau-समस्याएँ — एकत्र करती है
और विशेष प्रश्नों के लिए तीन उप-स्किल्स की ओर भेजती है:

| उप-स्किल | किसके लिए |
| --- | --- |
| **`/rojo`** | फ़ाइलसिस्टम→Studio सिंक, `default.project.json`, rokit/Wally/Lune, प्रोजेक्ट ढाँचा, सिंक-समस्याएँ |
| **`/rbx-studio`** | Studio संचालन, Scene-बनाम-Code मोड, Studio-MCP, एसेट पाइपलाइन, **मैलवेयर स्कैन** |
| **`/game-design`** | भूमिकाएँ और उप-कार्य, विकास-चेन, Game Design Document (KONZEPT.md), Multi-Agent |

> रूटिंग नियम: **सिंक/बिल्ड/सेटअप** के बारे में हो → `/rojo`। **एडिटर/एसेट्स/Studio में परीक्षण** के बारे में हो
> → `/rbx-studio`। **अवधारणा/भूमिकाएँ/प्रक्रिया** के बारे में हो → `/game-design`। **कोड-आर्किटेक्चर,
> Luau-समस्याएँ या समग्र प्रवाह** के बारे में हो → यहीं रहें।

## एक नज़र में स्टैक

- **भाषा:** Luau (`.luau`, `.lua` नहीं)। कोड अंग्रेज़ी में, टिप्पणियाँ/दस्तावेज़ीकरण जर्मन में, UI-टेक्स्ट जर्मन में।
- **सिंक:** rokit के माध्यम से Rojo (पिन किए गए टूल-संस्करण)। फ़ाइलसिस्टम = सत्य का स्रोत।
- **टूल्स:** Rojo (सिंक/बिल्ड), Lune (Studio के बाहर परीक्षण/स्क्रिप्ट), Wally (Packages),
  वैकल्पिक Knit (Service-/Controller-Framework, नए प्रोजेक्ट), Selene (Linter)।
- **नियंत्रण:** AI-संचालित निरीक्षण/परीक्षण/एसेट-इंसर्शन के लिए Roblox-Studio-MCP।

## प्रोजेक्ट संरचना (मानक)

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

एक ढाँचा `/rojo` द्वारा `scaffold_roblox_project.sh` के माध्यम से बनाया जाता है।

## आर्किटेक्चर पैटर्न

**Server — Main + Manager-Modules।** प्रति प्रोजेक्ट केवल **एक** Script: `Main.server.luau`। यह केंद्रीय रूप से Remotes-फ़ोल्डर बनाता है और सभी Feature-Modules को `require()` के माध्यम से लोड करता है:
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
अन्य सभी Server-फ़ाइलें `.luau` (ModuleScripts) हैं।

**Client — साझा State + HUD।** GameClient एक साझा State लिखता है, और HUD उसे Heartbeat में पढ़ता है:
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — GameEnums में केंद्रीय।** Remote-नाम एक बार `GameEnums.Remotes` में परिभाषित करें; Server उन्हीं के माध्यम से Events बनाता है, Client उन्हीं नामों से उन्हें खोजता है। इस तरह Server और Client के बीच स्ट्रिंग-असंगति नहीं होती।

## गेम का समग्र प्रवाह

1. **अवधारणा** (`/game-design`): KONZEPT.md — शैली, USP, 3–4 मुख्य मैकेनिक्स, मोनेटाइज़ेशन।
2. **सेटअप** (`/rojo`): ढाँचा स्कैफ़ोल्ड करें, `default.project.json`-मैपिंग तय करें।
3. **Backend**: Config → GameEnums → *Defs → Main.server → *Manager।
4. **Frontend**: GameClient → HUD।
5. **Greybox-Playtest** (`/rbx-studio`): पहले Gameplay, Parts + आवश्यकता होने पर AI-Materials।
6. **Asset-Upgrade** (`/rbx-studio`): Creator-Store-Assets, **मैलवेयर स्कैन**, Scene के रूप में .rbxl।
7. **परीक्षण** (`/game-design`): QA + गेम-समीक्षक + Persona-Blindtests, दोहराव।
8. **Release** (`/game-design` बिज़नेस भूमिका): स्टोर पेज, मोनेटाइज़ेशन, Live-Ops।

## Luau-/Roblox-समस्याएँ (संक्षिप्त सूची)

सबसे आम समस्याएँ — पूर्ण, टिप्पणी-सहित सूची:
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md)।

- जब उसी पंक्ति में और कोड आए, तो `task.wait(x)` के बाद Semicolon।
- `Model.Position` मौजूद नहीं → `model:GetPivot().Position`।
- Dictionaries पर `#table` = 0 → मैन्युअली गिनें।
- `mouse.Hit` nil हो सकता है → उपयोग से पहले जाँचें।
- DataStore-Calls **हमेशा** `pcall` में।
- `tick()` deprecated → `os.clock()`; `SetPrimaryPartCFrame` → `PivotTo`।
- Event-नाम केंद्रीय रूप से `GameEnums.Remotes` में; सभी Remotes `Main.server.luau` में बनाएँ।
- कोई चक्रीय `require`s नहीं (अन्यथा Deadlock)।
- `require()` केवल `.luau`-ModuleScripts पर, कभी Scripts/LocalScripts पर नहीं।

## हर Commit से पहले (चेकलिस्ट)

- [ ] बहु-कथन वाले स्टेटमेंट्स में `task.wait(...)` के बाद Semicolons
- [ ] कोई `Model.Position` नहीं, कोई `tick()` नहीं, कोई `SetPrimaryPartCFrame` नहीं
- [ ] DataStore `pcall` में, `mouse.Hit` की nil के लिए जाँच
- [ ] Event-नाम Server↔Client से मेल खाते हैं (GameEnums के माध्यम से)
- [ ] सभी RemoteEvents `Main.server.luau` में बनाए गए
- [ ] कोई चक्रीय Requires नहीं
- [ ] Marketplace-Assets स्कैन किए गए (`/rbx-studio` → मैलवेयर स्कैन), Reports संग्रहीत

## ज्ञान-स्रोत

- **वर्तमान Engine-/Creator-दस्तावेज़ीकरण:** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine` (Engine-API) और `/roblox/creator-docs`
  (Tutorials/Guides); फ़ॉलबैक <https://create.roblox.com/docs>।
- **संदर्भ-पाइपलाइन** (यदि इस सिस्टम पर उपलब्ध हो): `<your Roblox project pipeline>` —
  जिनमें `SKILL.md`, `GUIDE.md`, `LESSONS_LEARNED.md`, `ROJO_FAQ.md`, `ROBLOX_MCP_FAQ.md`,
  `AGENT_ROLES.md`, `_malware_reports/PATTERNS.md`, `_knowledge/` शामिल हैं (स्थानीय API-Cache)।

## Changelog

### 1.0.0 (2026-06-17)
- प्रारंभिक संस्करण। `/rojo`, `/rbx-studio`, `/game-design` पर मेटा-स्किल; प्रोजेक्ट संरचना,
  आर्किटेक्चर-पैटर्न और Luau-Lessons `.ROBLOX`-Pipeline से निकाले गए, उपयोगकर्ता-तटस्थ।
