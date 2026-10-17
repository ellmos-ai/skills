---
name: wayfinding-routing
version: 1.1.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-09-27
description: "LLM नेविगेशन, अभिविन्यास और विफलता-सहिष्णुता के लिए सार्वभौमिक skill। जब एजेंट संदर्भ विचलन, विफल होते टूल, लूप या बंद गलियों का सामना करते हैं, तब यह सक्रिय wayfinding, आत्म-अभिविन्यास और पुनर्प्राप्ति heuristics प्रदान करता है। इसमें पर्यायवाची रणनीतियाँ survival-routing, dead-reckoning, pathfinder-routing और celestial-routing शामिल हैं।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, self-orientation, resilience, recovery, heuristics]
language: hi
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: 6baf14f778df95316188563ad6be21be8f223d9dd79ec73d7388514b77d45f01
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="wayfinding-routing banner">

# Wayfinding-Routing (आत्म-अभिविन्यास और आपातकालीन fallback engine)

**Wayfinding-Routing** skill, जिसे **`survival-routing`**,
**`dead-reckoning`**, **`pathfinder-routing`** और **`celestial-routing`** के नाम से भी जाना जाता है,
LLM एजेंटों के लिए नेविगेशन और आपातकालीन पुनर्प्राप्ति का बाध्यकारी ढाँचा है।

यह एजेंटों को सामान्य निष्पादन के लिए सक्रिय wayfinding heuristics से, और संदर्भ विचलन, बार-बार होने वाली
निष्पादन विफलताओं, विफल APIs या बंद गलियों के लिए आपातकालीन प्रोटोकॉल से सुसज्जित करता है।

---

## पर्यायवाची और रणनीतियों का अवलोकन

| पर्यायवाची रणनीति | रूपक और मूल सिद्धांत | उपयोग का मामला |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (प्राथमिक) | **Wayfinding / स्थानिक अभिविन्यास:** बाहरी GPS के बिना संकेतों और परिवेश के सुरागों से नेविगेशन। | Sidecars, `workflowhooker` और `automation-self-care` के लिए प्राथमिक नेविगेशन नियंत्रण-चक्र। |
| **`survival-routing`** | **आपातकालीन fallback और आत्म-संरक्षण:** टूल विफल होने या लूप बनने पर circuit-breaking और नियंत्रित degradation। | Timeouts, बार-बार होने वाली विफलताओं या अनुमति सीमाओं पर आपातकालीन पुनर्प्राप्ति। |
| **`dead-reckoning`** | **नौवहन में dead reckoning:** बिना बाहरी स्थिति-स्रोत के क्रमिक breadcrumbs से सटीक स्थिति का पुनर्निर्माण। | Scratch फ़ाइलों या `TODO.md` में निष्पादन चरणों को ट्रैक करना, ताकि सटीक रूप से वापस जाया जा सके। |
| **`pathfinder-routing`** | **Pathfinder और अग्रिम दल:** बहु-एजेंट टीमों के लिए मार्गों की पहले से जाँच और तैयारी। | डायरेक्टरी ट्री, locks और कार्य निर्भरताओं की preflight जाँच। |
| **`celestial-routing`** | **खगोल-नौवहन:** जब स्थानीय संदर्भ शोर-भरा हो, तब अपरिवर्तनीय ध्रुव-तारा anchor दस्तावेज़ों के साथ संरेखण। | जब Prompt निर्देश परस्पर विरोधी हों, तब `CLAUDE.md`, `AGENTS.md` और `START.md` पर fallback। |
| **रणनीति `likelihood-routing`** (अलग skill, यदि स्थापित हो) | **संभावना-प्रवणता को warmer/colder सेंसर के रूप में:** conditional अगले-शब्द संभावना (Likelihood Scoring) से लक्ष्य शब्द के आधार पर नियंत्रण फ़ाइलों का मूल्यांकन और प्रवणता ($\Delta S$) का अनुसरण। | Memory सेवा के बिना fallback, जब कोई परियोजना-विशिष्ट तकनीकी शब्द किसी session इतिहास में न मिले। |

---

## पाँच केंद्रीय आपातकालीन और अभिविन्यास प्रोटोकॉल

### 1. `PROTOCOL-ANCHOR-RESET` (ध्रुव-तारा fallback / Celestial Routing)

- **ट्रिगर:** संदर्भ विचलन, परस्पर विरोधी उपयोगकर्ता निर्देश, या लंबे, अनेक turns वाले sessions में
  अभिविन्यास का खोना।
- **Heuristic नियम:** मुक्त पाठ-निर्माण रोकें। क्षणिक धारणाएँ त्याग दें। Root anchor दस्तावेज़ों
  (`CLAUDE.md`, `AGENTS.md`, `START.md`) को फिर से पढ़ें। आगे की किसी कार्रवाई से पहले
  लक्ष्य स्थिति को अधिकृत root निर्देश पर रीसेट करें।

### 2. `PROTOCOL-STOP-EXPLAIN` (Rubber-Duck परावर्तन लूप)

- **ट्रिगर:** कोई terminal कमांड, फ़ाइल परिवर्तन या API अनुरोध एक ही त्रुटि के साथ दो बार विफल हो।
- **Heuristic नियम:** **कमांड निष्पादन लॉक करें।** तीसरे प्रयास से पहले एजेंट को औपचारिक आत्म-परावर्तन देना होगा:
  1. *प्रयास 1 और 2 में ठीक कौन-सी त्रुटि आई?*
  2. *पिछली निदान परिकल्पना क्यों विफल रही?*
  3. *कौन-सा नया वैकल्पिक दृष्टिकोण चुना जा रहा है?*
  यह स्पष्ट तर्क देने के बाद ही निष्पादन फिर से खुलेगा।

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (बहु-स्तरीय fallback कैस्केड)

- **ट्रिगर:** प्राथमिक टूल, MCP सर्वर या बाहरी API अनुपलब्ध है या त्रुटि लौटा रहा है।
- **Heuristic नियम:** कभी अचानक विफल न हों और न ही अंधाधुंध लूप करें। चरणबद्ध रूप से degrade करें:
  - **स्तर 1 (इष्टतम):** पूर्ण native API या MCP टूल
  - **स्तर 2 (विकल्प टूल):** स्थानीय Python CLI या स्क्रिप्ट
  - **स्तर 3 (केवल-पढ़ने की स्थिति):** सीधे फ़ाइल-विश्लेषण
    (`view_file` या कच्चा पाठ)
  - **स्तर 4 (हस्तांतरण):** उपयोगकर्ता के लिए संरचित स्थिति-रिपोर्ट और खुले विकल्प प्रस्तुत करें।

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead reckoning और बंद गली की पहचान)

- **ट्रिगर:** एक जटिल बहु-चरणीय refactoring या workflow पथ चरण N पर अनसुलझे अवरोध से टकराता है।
- **Heuristic नियम:** विनाशकारी परिवर्तनों से पहले breadcrumbs दर्ज करें। यदि कोई पथ विफल हो:
  1. बिना commit के परिवर्तन वापस लें और स्थिति पुनर्स्थापित करें।
  2. अंतिम स्वच्छ breadcrumb checkpoint तक वापस जाएँ।
  3. विफल मार्ग को `TODO.md` में अवरुद्ध के रूप में चिह्नित करें।
  4. वैकल्पिक पथ B आज़माएँ।

### 5. `PROTOCOL-CIRCUIT-BREAKER` (आपातकालीन रोक और सुरक्षित निकास)

- **ट्रिगर:** निष्पादन सीमा पहुँच गई, अनंत लूप पहचाना गया, या गंभीर सिस्टम लॉक त्रुटि।
- **Heuristic नियम:** आपातकालीन शटडाउन चलाएँ:
  1. स्वयं अर्जित सभी फ़ाइल और Git locks मुक्त करें
     (`python -m workflowhooker check`)।
  2. वर्तमान आंशिक स्थिति को `.SYNC/SURVIVAL_STATE.json` या
     `AUTOMATIONS-MEMORY.md` में सहेजें।
  3. घटना को `ANTIGRAVITY-LOG.txt` में दर्ज करें।
  4. उपयोगकर्ता या orchestrator के लिए एक कार्रवाई-योग्य सारांश के साथ व्यवस्थित रूप से समाप्त करें।

---

## `automation-self-care` और `workflowhooker` के साथ एकीकरण

`wayfinding-routing` निम्न के लिए अंतर्निहित नेविगेशन तर्क प्रदान करता है:

- **`automation-self-care`**: पाँच प्रोटोकॉल के आधार पर sidecar prompts की आत्म-उपचार क्षमता की जाँच करता है।
- **`workflowhooker`**: क्रमिक lock जाँच और breadcrumb लॉगिंग के लिए मानक heuristics प्रदान करता है।
- **`staircase-routing`**: ऊर्ध्वाधर डायरेक्टरी नेविगेशन के लिए `PROTOCOL-ANCHOR-RESET` का उपयोग करता है।
- **रणनीति `likelihood-routing`** (अलग skill, यदि स्थापित हो): जब नियंत्रण फ़ाइलें कई संभावित शाखाओं की ओर अस्पष्ट रूप से इशारा करें, तब `PROTOCOL-ANCHOR-RESET` के लिए संभावना-प्रवणता को warmer/colder सेंसर के रूप में प्रदान करता है — यह `staircase-routing` का पूरक है, जो प्रवणता के बजाय कीवर्ड मिलान के आधार पर खोजता है।

## Changelog

### 1.1.0 (2026-09-27)
- तालिका के अवलोकन और एकीकरण खंड में रणनीति `likelihood-routing` का उल्लेख जोड़ा गया
  (बिना लिंक -- यह skill केवल निजी है और अभी इस सार्वजनिक repo का हिस्सा नहीं है; दृश्यता का प्रश्न
  उपयोगकर्ता के पास है।)
