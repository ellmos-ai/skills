---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "गेम डेवलपमेंट की प्रक्रिया के रूप में यह कैसे काम करता है — भूमिकाएँ, उप-कार्य, वर्कफ़्लो और भूमिका-विवरण, विशेष रूप से (पर केवल नहीं) Roblox के लिए। इस स्किल का उपयोग तब करें जब बात गेम डेवलपमेंट के ORGANIZATION की हो, न कि ठोस कोड की: कौन-सी भूमिकाएँ मौजूद हैं (Creative Director, Engineer, Artist, Polish/Audio, Business, QA-Tester, Game Critic)? कौन कौन-सा उप-कार्य करता है? डेवलपमेंट चेन (concept → backend → frontend → polish → test) कैसी दिखती है? Game Design Document / KONZEPT.md कैसे लिखा जाता है? कई (AI) एजेंट एक गेम को कैसे बाँटते हैं? इस स्किल को \"plan a new game\", \"create Game Design Document\", \"which roles do I need for my game\", \"development workflow for a game\", \"who tests the game\", \"structure a game idea\", \"Roblox genre/monetization (हिंदी समकक्ष: नया गेम प्लान करो, Game Design Document बनाओ, मेरे गेम के लिए कौन-सी भूमिकाएँ चाहिए, गेम के लिए डेवलपमेंट वर्कफ़्लो, गेम कौन टेस्ट करता है, गेम आइडिया की संरचना, Roblox शैली/मुद्रीकरण)\" जैसे वाक्यों पर भी ट्रिगर करें।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/game-design/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: e21ae8c9208280a65f748fd252d86404a38bd12ad05bb53c5f6b0531c56b0720
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="game-design banner">

# Game Design — भूमिकाएँ, उप-कार्य और वर्कफ़्लो

## उद्देश्य

गेम डेवलपमेंट स्पष्ट रूप से अलग विषयों वाला टीमवर्क है — भले ही एक व्यक्ति या एक KI-एजेंट उनमें से कई संभाले। यह स्किल **संगठनात्मक मॉडल** देती है: कौन-सी भूमिकाएँ होती हैं, किन उप-कार्यों में वे शामिल हैं, वे किस क्रम में मिलकर काम करते हैं, और एक गेम को कॉन्सेप्ट (GDD) के रूप में कैसे दर्ज किया जाता है। *तकनीकी* कैसे-करें के लिए देखें `/rojo` (Sync), `/rbx-studio` (Editor/Assets) और मेटास्किल `/rbx-dev` (Architektur)।

किसी नए गेम की योजना बनाते समय, कार्य बाँटते समय (कई KI-एजेंटों के बीच भी) और Game Design Document लिखते या जाँचते समय इस स्किल का उपयोग करें।

## भूमिकाएँ (5 विकास + 2 परीक्षण)

एक आज़माई हुई, संक्षिप्त भूमिका-विभाजन। सभी उप-कार्यों सहित पूर्ण विवरण:
[`references/roles-and-workflows.md`](references/roles-and-workflows.md).

| भूमिका | फ़ोकस | मुख्य उप-कार्य |
| --- | --- | --- |
| **Creative Director** | क्या और क्यों और किसके लिए | GDD/KONZEPT, मैकेनिक्स डिज़ाइन और बैलेंस, प्राथमिकता/Sprints, Story, UX-Flow |
| **Engineer** | कैसे (तकनीकी) | Server/Client/Shared-Code, Game-Loop, नेटवर्क/Remotes, DevOps (Rojo, Build), Bugfixing |
| **Artist** | दुनिया कैसी दिखती है | दुनिया/Level-निर्माण, रोशनी और वातावरण, पार्टिकल्स, एसेट-सोर्सिंग (Malware-Check सहित) |
| **Polish / Audio** | कैसा महसूस होता है और सुनाई देता है | SFX/संगीत/Ambient, एनिमेशन, UI/UX-Feinschliff, "Juice" (Screen-Shake, Hit-Stop), Feedback |
| **Business** | बाहर की ओर | स्टोर-पेज, Icon/Thumbnail, Monetarisierung (Gamepass/Products/Pass), Analytics, Community |
| **QA-Tester** | तकनीकी रूप से सही है? | कोड में Bug-Scans, Playtests + Console जाँच, दोहराने योग्य Reports, Regression, Performance |
| **Spielkritiker** | क्या यह मज़ेदार है? | खिलाड़ी की दृष्टि से First-/Long-Impression, ईमानदार मूल्यांकन (Fun, स्पष्टता, निष्पक्षता), सुझाव |

**मूल नियम:** विकास और परीक्षण **अलग** भूमिकाएँ हैं — आदर्श रूप से अलग व्यक्ति या एजेंट। जो कोड लिखता है, वह उसे निष्पक्ष रूप से नहीं परखता। Spielkritiker कठोर हो सकता है।

## वर्कफ़्लो (विकास-चेन)

कार्य एक भूमिका से दूसरी भूमिका तक श्रृंखला में बहता है। मुख्य पैटर्न:

**मानक Feature-Chain:**
```
Creative Director (plant Feature) → Engineer (Backend) → Artist (Frontend/Assets)
→ Polish/Audio (Sound + Feinschliff) → QA-Tester (technischer Test)
→ Spielkritiker (Spielerperspektive) → Creative Director (Feedback → nächste Iteration)
```

**Quick-Fix-Chain:** QA-Tester (Bug) → Engineer (Fix) → QA-Tester (verifiziert)।

**Asset-Chain:** Artist (Store-Suche) → Artist (Malware-Scan) → Artist (einbinden) → QA (visuell)।

**Polish-Chain:** Spielkritiker (Schwäche) → Polish/Audio → Artist → Spielkritiker (Re-Check)।

**मनुष्य-इन-द-लूप:** [Agenten-Chain] → menschlicher Tester → Creative Director (Feedback) → [Chain]।

हर iteration में एक छोटा Changelog छोड़ना चाहिए। रुकने की शर्त: समय-बजट पूरा हो **या** गुणवत्ता-लक्ष्य पूरा हो।

### Persona-आधारित परीक्षण

कोई गेम तभी टिकता है जब बहुत अलग-अलग खिलाड़ी उससे निपट पाएँ। इसलिए केवल अपने दृष्टिकोण से नहीं, बल्कि कई **Personas** से परखें (एजेंटों द्वारा सिम्युलेट भी) — उम्र, अनुभव, प्लेटफ़ॉर्म (PC/Mobile/Tablet/Konsole), ध्यान-अवधि, भाषा और सुलभता के अनुसार बदलते हुए। उदाहरण: Tablet पर एक 9 साल का Casual बच्चा जो बस बटन दबाना चाहता है; PC पर एक 12 साल का Core-खिलाड़ी जो Meta खोजता है; एक 60+ शुरुआती जिसे बड़े बटन चाहिए। Persona-परीक्षण **blind** होने चाहिए (परीक्षक को डिज़ाइन की मंशा पता न हो)।

## Game Design Document (KONZEPT.md)

हर गेम को एक संक्षिप्त GDD में दर्ज करें — टेम्पलेट:
[`assets/KONZEPT_template.md`](assets/KONZEPT_template.md)। न्यूनतम संरचना:

- **Vision** — 1–2 वाक्य: यह गेम क्या है?
- **शैली / प्रेरणा** — वर्गीकरण + संदर्भ-शीर्षक।
- **मुख्य मैकेनिक्स** — **अधिकतम 3–4** (फ़ोकस गुणवत्ता को बाध्य करता है)।
- **Gameplay-Loop** — खिलाड़ी का मिनट-दर-मिनट चक्र।
- **गेम मोड / समय-प्रारूप** — यदि प्रासंगिक हों।
- **Monetarisierung** — Gamepasses, Developer Products, Battle Pass, Shop।
- **Technik** — Stack (Rojo/Frameworks), मोटे तौर पर आर्किटेक्चर।
- **अगले कदम** — Implementierungs-Checkliste।
- **ज्ञात बग / खुले बिंदु**।

## Multi-Agent-कार्य-विभाजन

कई KI-एजेंट (या मनुष्य+AI) एक गेम को बाँट सकते हैं — दो मोड:

- **झुंड (Swarm)** — एक ही कार्य, अलग क्षेत्र (जैसे तीन एजेंट हर एक सिस्टम को बैलेंस करें)।
- **Team** — अलग भूमिकाएँ, एक-दूसरे से समन्वित (Engineer + Artist + Polish एक Feature पर समानांतर, Creative Director द्वारा समन्वित)।

व्यवहार में सिद्ध: विकास और परीक्षण **कभी** एक ही एजेंट को न दें; हर भूमिका के लिए रोल-प्रॉम्प्ट्स तय रखें (System-Prompt = भूमिका-विवरण); हर Chain-iteration Changelog + परीक्षण-रिपोर्ट के साथ समाप्त हो; मनुष्य गुणवत्ता-Gate बना रहे।

## Roblox-विशिष्ट बाज़ार-संदर्भ (दिशा-निर्देश)

प्लेटफ़ॉर्म-ज्ञान जो Roblox के लिए कॉन्सेप्ट-कार्य को ज़मीन पर रखता है (कोई गारंटी नहीं, केवल व्यावहारिक नियम):

- **लाभदायक Genres:** Simulator, RPG, Tycoon, Horror, Obby — बहुत अलग पैमाना और प्रयास।
- **कम सेवित निच (अधिक जोखिम, कम प्रतिस्पर्धा):** वास्तविक Strategie/RTS-Lite, गुणवत्तापूर्ण Sportspiele, Cozy/Life-Sim, Coop-Puzzle/Escape, Auto-Battler।
- **स्वर्णिम मुद्रीकरण-नियम:** (1) LiveOps अनिवार्य है (हर 2–4 सप्ताह में अपडेट), (2) Monetarisierung Gameplay को *समर्थन* करे, उसे बाधित न करे, (3) Social-Design (Trading, Coop) बुनियादी ढाँचा है, (4) Mobile-First (50 %+ मोबाइल पर खेलते हैं), (5) Content-Creator-उपयुक्तता (YouTube/TikTok) विपणन है।

> वर्तमान, विश्वसनीय बाज़ार-आंकड़ों के लिए अनुमान लगाने के बजाय शोध करें — ऊपर के बिंदु स्थिर heuristics हैं, लाइव डेटा नहीं।

## आगे की जानकारी

- सहयोगी स्किल: `/rojo`, `/rbx-studio`; मेटास्किल `/rbx-dev` (आर्किटेक्चर-पैटर्न, प्रोजेक्ट-संरचना, Luau-Lessons)।
- संदर्भ-Pipeline (यदि उपलब्ध हो): `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`, `IDEAS.md`, बाज़ार-विश्लेषण)।

## Changelog

### 1.0.0 (2026-06-17)
- प्रारंभिक संस्करण। सामान्य भूमिका-/वर्कफ़्लो-ढाँचा, `.ROBLOX/AGENT_ROLES.md` और `GUIDE.md` से निकाला गया, उपयोगकर्ता-तटस्थ (परियोजना-विशिष्ट पोर्टफ़ोलियो के बिना)।

## संबंधित स्किल

- `roblox-team-lock` — फ़ाइल-, Studio- और MCP-Claims, जब कई एजेंट एक ही परियोजना पर काम करें। पहले पढ़ें, फिर claim करें, फिर काम करें, फिर छोड़ें।
