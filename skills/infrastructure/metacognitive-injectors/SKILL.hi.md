---
name: metacognitive-injectors
version: 1.4.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-30
updated: 2026-07-30
description: "मेटाकॉग्निटिव इंजेक्टर और आत्म-वार्ता रणनीतियाँ (Self-Talk, Metacognitive Auditing, Evaluator Hooks, Pre-Flight Checklists, State Persistence & Personas)। इसमें सक्रिय सूचना-खोज (सिस्टम मेमोरी Gardener और USMC), Rehearsal (सक्रिय पुनर्प्राप्ति और पुनरुत्पादन), बैडेली का वर्किंग मेमोरी (State + Hooks), मियाके के एक्ज़ीक्यूटिव फ़ंक्शन तथा CBT/ACT चिकित्सीय रणनीतियाँ एकीकृत हैं।"
standalone: true
anthropic_compatible: true
bach_compatible: true
category: infrastructure
tags: [metacognition, self-talk, metacognitive-injectors, evaluator-hook, quality-gate, multi-agent, auditing, pre-flight-checklist, working-memory, active-retrieval, rehearsal, gardener, usmc, state-persistence, hooks, survival-routing, persona-routing]
aliases: [self-talk, metacognitive-self-talk, metacognitive-auditing, evaluator-hook, preflight-checklist, inner-speech, active-retrieval, rehearsal]
language: hi
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
translated_from_sha256: e692cdc2b2eb66f784fc25d0f36596e1342e828e67d91bc8aeca5eb3f456d8c2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:50.098377+00:00"
---
<img src="banner.png" width="100%" alt="metacognitive-injectors banner">

# मेटाकॉग्निटिव इंजेक्टर (Metacognitive-Injectors, Active Retrieval & Memory Search)

यह कौशल **Metacognitive-Injectors** (जिसे **`self-talk`**, **`metacognitive-auditing`**, **`evaluator-hook`**, **`preflight-checklist`**, **`inner-speech`**, **`active-retrieval`** और **`rehearsal`** के नाम से भी जाना जाता है) AI एजेंटों के लिए संज्ञानात्मक-मनोविज्ञान और चिकित्सीय रूप से आधारित स्व-निगरानी रणनीतियाँ स्थापित करती है।

---

## 1. सक्रिय सूचना-खोज और सिस्टम मेमोरी (Gardener और USMC)

### A. सिस्टम मेमोरी में सक्रिय सूचना-खोज
- धारणाएँ बनाने या जल्दबाज़ी में दावे करने से पहले सिस्टम मेमोरी में **सक्रिय रूप से खोजें**:
  1. **Gardener DB (`gardener.py` / `hb_garden_*`):** देखे गए सीखने के प्रभाव, उपयोगकर्ता के निर्णय और पथ-समझौते खोजता है (उदा. `Gardener().find("companion")`)।
  2. **USMC SQLite DB (`usmc_memory.db`):** संग्रहीत तथ्य, सबक और सत्र-इतिहास की क्वेरी करता है।
  3. **केंद्रीय नियम-फ़ाइलें (`CLAUDE.md`, `.SYNC`, `AGENTS.md`):** मौजूदा परंपराएँ और पथ-संदर्भ पढ़ता है।

### B. Rehearsal: सक्रिय पुनर्प्राप्ति और पुनरुत्पादन (Retrieval Practice)
- **सबवोकल रिहर्सल लूप (ध्वन्यात्मक लूप):**
  जानकारी को केवल निष्क्रिय रूप से न पढ़ें, बल्कि निष्पादन से पहले **सक्रिय रूप से पुनः प्राप्त करें, वर्किंग मेमोरी में पुनर्निर्मित करें और वास्तविकता से मिलान करें**।
  - *"क्या मैंने स्क्रिप्ट का सटीक पथ स्मृति में से पुनः प्राप्त किया है?"*
  - *"क्या कमांड सिंटैक्स सिस्टम मेमोरी में संग्रहीत उदाहरणों से मेल खाता है?"*

---

## 2. संज्ञानात्मक-विज्ञान और चिकित्सीय आधार

### A. वर्किंग मेमोरी = State + Hooks (Baddeley और Cowan)
- **State (मेमोरी-सामग्री):** प्रत्येक उप-चरण के बाद क्षणिक मध्यवर्ती स्थितियों को SQLite तालिकाओं (`usmc_memory.db`), `AUTOMATIONS-MEMORY.md` या स्थानीय State-Buffers में स्थायी रखता है।
- **Hooks (नियंत्रण-तंत्र):** Preflight-Bootloader, Letter-Hooks और PreToolUse/PostToolUse Evaluator-Hooks।

### B. मियाके के एक्ज़ीक्यूटिव फ़ंक्शन (Command & Control)
1. **Inhibition (आवेग-नियंत्रण):** जल्दबाज़ी में Sign-Off और काल्पनिक सफलता-संदेशों को दबाता है।
2. **Shifting (संज्ञानात्मक लचीलापन):** अवरोधों पर गतिशील रूप से Survival-Routing, Persona-मोड या वैकल्पिक समाधान-मार्गों पर स्विच करता है।
3. **Updating (वर्किंग मेमोरी-अपडेट):** कार्य-स्थिति को निरंतर अद्यतन करता है।

### C. चिकित्सीय प्रेरणाएँ (CBT, ACT और समाधान-केंद्रित चिकित्सा)
- **CBT संज्ञानात्मक पुनर्गठन:** त्रुटियों को मूल्यवान नैदानिक डेटा के रूप में पुनर्परिभाषित करना।
- **ACT संज्ञानात्मक डीफ्यूज़न और स्वीकृति:** अपनी अनिश्चितता को एक स्थिति के रूप में स्वीकार करना और उसे प्रकट करना।
- **व्यवहार-प्रयोग:** वास्तविक अनुभवजन्य प्रमाण जुटाने के लिए Smoke-Tests/Dry-Runs चलाना।

---

## 3. बहु-मॉडल फ़ॉलबैक-श्रृंखला और Codex Companion इंटरफ़ेस

| प्राथमिकता | सलाहकार / समीक्षक | इंटरफ़ेस / कमांड | कार्य / नियम |
| :--- | :--- | :--- | :--- |
| **प्राथमिक (1)** | **Gemini Subagent** | `invoke_subagent` / `define_subagent` | नियमित जाँच के लिए तेज़ आंतरिक समीक्षक। |
| **द्वितीयक (2)** | **Codex Companion (Native)** | `node "<USER_HOME>\.codex\.tmp\marketplaces\openai-codex\plugins\codex\scripts\codex-companion.mjs" task "..."` | समीक्षाओं और **`/goal`-स्वीकृति** के लिए नेटिव Codex-Companion। |
| **तृतीयक (3)** | **Codex CLI Direct** | `codex exec --skip-git-repo-check` | Codex CLI का प्रत्यक्ष आह्वान। |
| **चतुर्थक (4)** | **Claude CLI / Swarm** | `claude -p ...` / `hb_swarm_consensus` | टोकन-सीमाओं पर तृतीय मत। |

---

## 4. क्षेत्र-विशिष्ट प्रॉम्प्ट-इंजेक्शन (Tailored Injection Pattern)

इंजेक्टर (`agy_metacognitive_prompt_injector.py`) क्षेत्र के अनुसार उपयुक्त रणनीतियाँ चुनता है:

- **मूल-खंड (सभी Sidecars):** Anti-Hohl-Vollzug (खोखले/दिखावटी समापन की रोकथाम), बाहरी मॉडल द्वारा `/goal`-स्वीकृति, सक्रिय सूचना-खोज (Gardener/USMC), Rehearsal (सक्रिय पुनर्प्राप्ति), Pre-Flight Checklist।
- **Research-Sidecars (`research-*`):** *प्रमाण-आधारित शोध (क्वेरी-प्रमाण के बिना कोई स्रोत नहीं)*, *CBT पुनर्परिभाषा और संज्ञानात्मक डीफ्यूज़न (गैर-परिणाम भी निष्कर्ष के रूप में)* से विस्तारित।
- **Software-/Roblox-Sidecars (`software-*`, `roblox-*`):** *ध्वन्यात्मक लूप और रिहर्सल*, *वर्किंग मेमोरी State Persistence*, *Survival-Routing* से विस्तारित।
- **Maintainer और Generalists (`maintainer-*`, `generalist-*`):** *सक्रिय सूचना-खोज*, *Skill-Finder* और *Memory Hooks* से विस्तारित।
