---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Roblox Studio में गेम डेवलपमेंट के लिए काम करना — वह विज़ुअल एडिटर जिसमें 3D सीन बनाया, परखा और प्रकाशित किया जाता है। इस स्किल का उपयोग इन कार्यों के लिए करें: Studio की मूल बातें (Explorer, Workspace, play-test, प्लेस को .rbxl के रूप में सहेजना), Rojo के साथ परस्पर क्रिया (Connect, scene-vs-code mode), Roblox-Studio-MCP के माध्यम से Studio का AI नियंत्रण (execute_luau, insert_from_creator_store, generate_material, screen_capture, Play/Stop, Console पढ़ना), संपूर्ण asset-pipeline वर्कफ़्लो (Creator Store → साफ़-सफ़ाई → kit → scene → .rbxl → Rojo उसे जीवंत बनाता है), और सबसे ऊपर marketplace assets के लिए अनिवार्य malware scan। \"Store से asset embed करें\", \"Studio MCP काम नहीं कर रहा\", \"studios: []\", \"मटीरियल जनरेट करें\", \"सीन सहेजें\", \"क्या यह Roblox asset सुरक्षित है\", \"Play के बाद scripts गायब हो जाते हैं\" जैसे वाक्यांशों पर भी यह ट्रिगर हो।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: hi
status: active
visibility: public
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 9d0fca2a40692abba63ce104ab8f69627490f5cd4adf2ead8a6da3ad00f4d7b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T02:34:25.375180+00:00"
---
<img src="banner.png" width="100%" alt="rbx-studio banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **नोट:** Roblox Corporation से संबद्ध नहीं; "Roblox" उनके मालिकों का ट्रेडमार्क है। "rbx" समुदाय में प्रचलित संक्षिप्त नाम है।

# Roblox Studio — एडिटर, परीक्षण, Assets, MCP (Deutsch)

## अवलोकन और उद्देश्य

Roblox Studio आधिकारिक एडिटर है: 3D सीन बनाएँ, play mode में गेम परखें, Creator Store से assets डालें और place प्रकाशित करें। Rojo वर्कफ़्लो में Studio **सीन** (Workspace, Terrain, रखे गए models) और **परीक्षण** का स्वामी होता है — **कोड** फ़ाइल-सिस्टम से Rojo के ज़रिए आता है (स्किल `/rojo` देखें)।

यह स्किल कवर करती है: Studio की मूल बातें, सीन और कोड कार्य का स्पष्ट पृथक्करण, Roblox-Studio-MCP के माध्यम से AI नियंत्रण, और हर marketplace asset के लिए **अनिवार्य malware scan** सहित asset वर्कफ़्लो।

## मूल बातें

- **Explorer** — सभी instances का ट्री (Workspace, ServerScriptService, ReplicatedStorage, …)। Rojo सक्रिय होने पर मैप किए गए क्षेत्र फ़ाइल-सिस्टम से लाइव भरे जाते हैं।
- **Play-Test** — हरा Play बटन (या F5) स्थानीय server+client सत्र शुरू करता है। हर शुरुआत के बाद **Output console में errors जाँचें** — यह सबसे महत्वपूर्ण debug प्रतिक्रिया है।
- **Place सहेजें** — File → Save As → `.rbxl` (binary) या `.rbxlx` (XML, diffable)। सहेजी गई place में **सीन** होता है। कोड फ़ाइल-सिस्टम में रहता है, place में नहीं।

## महत्वपूर्ण वर्कफ़्लो: scene mode बनाम code mode

Connect पर Rojo सभी मैप किए गए script क्षेत्रों को फ़ाइल-सिस्टम की सामग्री से overwrite कर देता है। `Workspace` (3D सीन) मैप नहीं होता और अक्षुण्ण रहता है। इससे दैनिक कार्य का सबसे महत्वपूर्ण नियम निकलता है — दोनों मोड कभी न मिलाएँ:

**Mode A — सीन संपादित करें (Rojo OFF):**
1. Rojo server रोकें (`taskkill //F //IM rojo.exe` या Ctrl+C)।
2. Studio में place खोलें, assets रखें, दुनिया बनाएँ, व्यवस्थित करें।
3. File → Save → `.rbxl` अब नया सीन रखता है।

**Mode B — कोड परखें (Rojo ON):**
1. उसी place को Studio में खोलें।
2. `rojo serve` शुरू करें → Studio के Rojo plugin में → Connect।
3. Play दबाएँ और परखें। Rojo scripts सिंक करता है; Workspace `.rbxl` से आता है।
4. Rojo चलते समय **सहेजें नहीं** (अन्यथा Rojo की स्थिति `.rbxl` में जम जाती है)।

इस प्रकार सीन कार्य (Studio) और कोड कार्य (editor + Rojo) समानांतर और बिना टकराव के चल सकते हैं — कलाकार सीन बनाते हैं, डेवलपर कोड लिखते हैं।

## Roblox-Studio-MCP — AI Studio को नियंत्रित करता है

Roblox-Studio-MCP Claude/Gemini/Codex को **चल रहे** Studio instance को सीधे नियंत्रित करने देता है: कोड चलाना, निरीक्षण, Play/Stop, Console पढ़ना, assets डालना। यह Rojo की जगह नहीं लेता — उसका पूरक है: स्थायी कोड बदलावों के लिए Rojo, निरीक्षण, परीक्षण, asset insertion और material generation के लिए MCP।

```
Editor + Rojo  ──(persistenter Code-Sync)──►  Studio (laufend)  ◄──(Inspektion/Test/Insert)──  MCP ◄── KI
```


### उपलब्ध MCP tools (विशिष्ट)

| Tool | उद्देश्य |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | खुले instances की सूची / सक्रिय चुनें |
| `search_game_tree` / `inspect_instance` | hierarchy खोजें / properties पढ़ें |
| `execute_luau` | Studio में सीधे Luau कोड चलाएँ |
| `script_read` / `script_grep` / `script_search` | scripts का विश्लेषण |
| `multi_edit` | एक बैच में कई instances/scripts बदलें |
| `start_stop_play` | Play/Stop नियंत्रित करें |
| `get_console_output` | Output log पढ़ें |
| `screen_capture` | सीन का स्क्रीनशॉट |
| `insert_from_creator_store` | Creator Store से asset डालें |
| `generate_material` | AI material/texture (MaterialVariant) बनाएँ |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | input सिमुलेट करें |

### सेटअप (उपयोगकर्ता-तटस्थ)

MCP Studio के साथ आने वाले server के रूप में चलता है, जो अक्सर एक पतले JSON-filter wrapper से जुड़ता है (कुछ clients जो non-JSON banners पार्स नहीं कर सकते, उन्हें यह छाँटता है):

- MCP batch (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- वैकल्पिक wrapper: `<your roblox-mcp wrapper>`
  (यदि इस system पर मौजूद हो; Claude/Codex/Gemini द्वारा साझा)
- Client configs: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

उदाहरण प्रविष्टि (`~/.claude/mcp.json`):
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


### सामान्य MCP समस्याएँ

| लक्षण | अर्थ / समाधान |
| --- | --- |
| `studios: []` या `Not connected to WS host` | तुरंत "टूटा" नहीं: `initialize` भेजें → 2–3 सेकंड प्रतीक्षा → `list_roblox_studios`; अन्यथा Studio पुनः आरंभ करें |
| `Error: connection closed: initialized request` | Studio बिल्कुल नहीं खुला — Studio शुरू करें, place लोड करें, फिर प्रयास करें |
| MCP से लिखे scripts Play/Stop के बाद गायब | MCP से कोड में किए बदलाव स्थायी नहीं हैं — स्थायी कोड बदलावों के लिए **Rojo** उपयोग करें |
| plugin VM में `require()` का मान गलत | plugin VM का अपना require cache है — सत्यापन के लिए `.Source` सीधे पढ़ें या Play के बाद server log जाँचें |

## Asset पाइपलाइन (Creator Store → गेम)

पहले greybox (gameplay), बाद में assets (release से पहले)। सिद्ध क्रम:

```
STORE DURCHSUCHEN   → z. B. "medieval" → mehrere Kandidaten laden
AUSSORTIEREN        → stilfremde/hässliche raus, 5–8 passende behalten
BEREINIGEN          → ALLE Scripts entfernen (Malware!), nur Geometrie/Meshes behalten
KIT / SET BAUEN     → aus Basis-Assets Varianten ableiten (gleiche Materials/Proportionen)
SZENE BAUEN (Studio)→ Assets zur Kulisse zusammensetzen (Dorf, Arena, Park)
ALS .RBXL SPEICHERN → die Kulisse ist die "Bühne"
ROJO BELEBT ES      → Scripts/Gameplay/HUD kommen per Rojo dazu; Workspace bleibt unangetastet
```


**Variant तकनीक ("modular kit"):** एक अच्छा base asset लें और उससे पूरा सेट निकालें (घर → टावर, बार्न, स्मिथी, खंडहर)। सभी materials, रंग और अनुपात साझा करते हैं → न्यूनतम प्रयास में एकसमान रूप, जैसे प्रो स्टूडियो करते हैं।

**Asset स्रोत (प्राथमिकता):** Creator Store (मुफ़्त, विशाल, **malware जाँच अनिवार्य**) → AI materials (`generate_material`) → अपने meshes (Blender → .fbx) → खरीदे गए asset packs।

## अनिवार्य: marketplace assets के लिए malware scan

Creator Store assets में obfuscated दुर्भावनापूर्ण scripts (backdoors, remote code, bot-network hooks) हो सकते हैं। उपयोग से पहले **हर** आयातित asset स्कैन करें और सभी scripts हटाएँ — केवल geometry/meshes रखें।

- Pattern संदर्भ: [`references/malware-patterns.md`](references/malware-patterns.md) — 8 ज्ञात obfuscation patterns (उल्टा attribute payload, नकली system script, remote `require()`, `loadstring`, `string.char`, `getfenv/setfenv`, छिपे हुए Values, विलंबित निष्पादन)।
- Scanner: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — `execute_luau` (या Command Bar) के माध्यम से Studio में चलाएँ; यह किसी instance को सभी patterns से जाँचता है और मिलानों की रिपोर्ट देता है।

**तुरंत लाल झंडे:** pure decoration model में बड़ी script · attributes में उल्टे strings · `require(<number>)` · `loadstring` · `HttpService` ऐसे asset में जिसे networking की ज़रूरत नहीं। संदेह हो तो script हटाएँ। मिले निष्कर्षों का दस्तावेज़ीकरण करें (जैसे संदर्भ pipeline में `_malware_reports/YYYY-MM-DD_*.md`)।

## महत्वपूर्ण Luau/Studio गलतियाँ (अंश)

Studio में सबसे आम गलतियाँ — पूरी सूची स्किल `/rbx-dev` रखती है:

- `Model.Position` मौजूद नहीं → `model:GetPivot().Position`।
- `tick()` पदावनत है → `os.clock()` / `workspace:GetServerTimeNow()`।
- `SetPrimaryPartCFrame()` पदावनत → `model:PivotTo(cf)`।
- DataStore calls **हमेशा** `pcall` में।
- एक ही ऊँचाई पर Baseplate + procedural floor → Z-fighting (झिलमिलाहट): baseplate हटाएँ या floor को +0.1 studs ऊपर उठाएँ।
- Part budget पर नज़र रखें (procedurally generated कमरे में ~50–80 parts)।

## आगे पढ़ने के लिए

- सहोदर स्किल: `/rojo` (sync, project setup), `/game-design` (भूमिकाएँ, वर्कफ़्लो, GDD),
  मेटा स्किल `/rbx-dev` (architecture patterns + सभी Luau सबक)।
- Engine/Creator docs: Context7 MCP (`/websites/create_roblox_reference_engine`,
  `/roblox/creator-docs`) या <https://create.roblox.com/docs>।
- संदर्भ pipeline (यदि मौजूद हो): `<your Roblox project pipeline>`
  (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`)।

## परिवर्तन लॉग

### 1.0.0 (2026-06-17)
- प्रारंभिक संस्करण। `.ROBLOX` pipeline (ROBLOX_MCP_FAQ, ASSET_PIPELINE, PATTERNS, LESSONS_LEARNED) से निकाला गया, उपयोगकर्ता-तटस्थ रूप में लिखा गया।
