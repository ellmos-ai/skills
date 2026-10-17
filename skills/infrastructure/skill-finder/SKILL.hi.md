---
name: skill-finder
version: 0.9.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-10-03
description: "अपने स्थानीय skills के लिए सक्रिय Finder/Router (using-superpowers के समकक्ष)। किसी भी गैर-तुच्छ कार्य की शुरुआत में हमेशा उपयोग करें, यह जाँचने के लिए कि कोई user-skill उपयुक्त है या नहीं, और सही skill की ओर रूट करने के लिए। यह तब सक्रिय होता है जब „कौन सा skill उपयुक्त है\", „क्या इसके लिए कोई skill है\", „skill खोजो\" जैसे वाक्य आएँ, या सामान्य रूप से उन कार्यों से पहले जिन्हें कोई स्थानीय skill ad-hoc काम से बेहतर हल करता है।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: hi
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
translated_from_sha256: 999cd705d5357d1c4244d420001f12dea37a1b2a9a204c49a7eadf18767228f7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="skill-finder banner">
# Skill-Finder

## नियम

किसी भी गैर-तुच्छ कार्य से पहले जाँचें कि कोई स्थानीय skill उसे बेहतर हल करता है या नहीं। थोड़े से भी संदेह पर उपयुक्त skill लोड करें और **उसकी लाइव मार्गदर्शिका का पालन करें** (फ़ाइल पढ़ें, स्मृति से काम न करें)। यदि कोई skill लागू नहीं होता, तो सामान्य रूप से आगे बढ़ें।

## परिवार-रूटिंग

<!-- Generiert/aktualisiert aus SKILL-MAP.md + inventory_skills.py. Thema -> Familie -> Skill.
     Pflege: Subskill skill-family-care oder neuer skill-explorer-Audit-Lauf. Stand: 2026-06-17 -->

| विषय / इरादा | परिवार | Skill(s) |
|-----------------|---------|----------|
| समस्या पर विचार करना / विश्लेषण करना | विचार-उपकरण | `/structured-thinking` (चलाता है `/think` → `/brainstorm` → `/decide`) |
| नए विचार / रचनात्मकता | विचार-उपकरण | `/brainstorm` (बनाम `/think` विश्लेषण, `/decide` चयन) |
| निर्णय-स्टैक | विचार-उपकरण | `/decision-briefing` |
| कौन सा निर्णय किस पर निर्भर है / क्या सिफ़ारिशें आपस में टकराती हैं? | विचार-उपकरण | `decision-path` (`/decision-path`; ASCII-निर्भरता-ग्राफ़, कोई निर्णय नहीं लेता) |
| अनुशंसित समग्र विकल्प को EIN अवधारणा-/कार्यान्वयन-पाठ के रूप में स्वीकृत करवाना | विचार-उपकरण | `decision-draw` (`/decision-draw`; समग्र रूप से स्वीकृति, सुधार → एकल निर्णय) |
| अधिकृत उपयोगकर्ता प्रोफ़ाइल बनाना या उपयोग करना | मल्टी-एजेंट | `build-your-users-mind` (निर्माण) · `decision-avatar` (उपयोग) |
| Bug / टेस्ट-त्रुटि | कोडिंग और डिबगिंग | `/bugfix-protocol` (1 बग), `/bugsweep` (कई, रिलीज़ से पहले) |
| नया/मौजूदा प्रोजेक्ट या पाइपलाइन | प्रोजेक्ट/पाइपलाइन | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Roblox-गेम | गेम-डेव | `/rbx-dev` (→ `/rojo`, `/rbx-studio`, `/game-design`) |
| थेरेपी / परामर्श / संकट | थेरेपी | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| प्रस्तुति / स्लाइड्स | कार्यालय | `/academic-pptx` (सामग्री) + `/pptx` (फ़ाइल) |
| जटिल मल्टी-एजेंट कार्य से पहले ऑर्केस्ट्रेशन को मिलकर सीमित करना | मल्टी-एजेंट | `choose-your-orchestrator` (`/choose-your-orchestrator`) |
| पुष्ट मल्टी-एजेंट समन्वय चलाना | मल्टी-एजेंट | `orchestrator`, `/swarm-operations`, `/model-strategy` |
| आवेदन / स्व-प्रबंधन | व्यक्तिगत | `/bewerbungsexperte`, `/selbstmanagement` |
| skills की तुलना/सफ़ाई/खोज | सिस्टम/मेटा | `skill-explorer` (ऑडिट/एक्सप्लोर), `code-skill-index` (सूची) |
| सिस्टम सेट करना / MCP सिंक करना / एजेंट जोड़ना | सिस्टम/मेटा | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| फ़ाइल-उपकरण | यूटिलिटीज़ | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| चैट-इतिहास → skill में संरक्षित करना | सिस्टम/मेटा | `skill-extractor` (`/skill-extract`) |
| चैट-इतिहास / बाहरी ऑटोमेशन → ऑटोमेशन | सिस्टम/मेटा | `workflow-extract` (`/automations-extract`) |
| कई प्रोजेक्ट्स पर आवर्ती जाँच | कोडिंग और डिबगिंग | `rotation-check` (Registry/Log-ढाँचा) |
| अटकी हुई समस्या, विचार खोजना | विचार-उपकरण | `idea-mining` (बनाम `/brainstorm` = मुक्त/व्यापक) |
| DE/EN-दस्तावेज़ संस्करणों को समकालिक रखना | यूटिलिटीज़ | `bilingual-doc-sync` |
| अत्यधिक विवादित merge / अलग-अलग branches (main बनाम master) / पुराना PR | कोडिंग और डिबगिंग | `reissverschluss-merge` (`/reissverschluss-merge` · `/zipper-merge`; एस्केलेशन: merge के बजाय rebuild) |
| पाठों से AI के निशान/चैट-अवशेष, AI-खुलासा | यूटिलिटीज़ | `llm-text-hygiene` |
| कार्य में शर्त/समय/क्रम („पहले तभी", „6 बजे से", „जैसे ही X पूरा हो") | प्रक्रिया | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |
| किसी फ़ोल्डर से फ़ाइलें नियम-आधारित तरीके से इकट्ठा करना/छाँटना („X से हमेशा Y लाओ और उन्हें Z में इकट्ठा करो", „फ़ोल्डर को अपने-आप छाँटो") | यूटिलिटीज़ | `file-collect-sort-action` |
| App-/GUI-श्रृंखला को उपयोगकर्ता के साथ मिलकर टेस्ट करना (लाइव टेस्ट करना, फ़ीडबैक तुरंत आँकना + मरम्मत सौंपना) | कोडिंग और डिबगिंग | `human-loop-audit` |
| सत्र समाप्त होने पर प्रोजेक्ट साफ़ करना (रजिस्टर सुलझाना/सही जगह रखना, दस्तावेज़ों को वर्तमान स्थिति पर लाना, स्ट्रे फ़ाइलें हटाना) | कोडिंग और डिबगिंग | `tidy-up` (`/tidy-up`; `work-autonomous`-स्तर-1-स्रोत के रूप में गिना जाता है) |
| नियम-/स्मृति-फ़ाइल संक्षिप्त करना, सामग्री बदले बिना („CLAUDE.md बहुत लंबी है", „कट रही है") | यूटिलिटीज़ | `paveman` (नियतात्मक, कोई मॉडल-कॉल नहीं; बनाम `knappform` = LLM-बोलचाल शैली) |
| Mermaid-आरेख GitHub पर रेंडर नहीं होता („Unable to render rich display", „आरेख नहीं दिखाया जा रहा है"), Mermaid-ब्लॉक्स की पूरे org में जाँच करना | कोडिंग और डिबगिंग | `mermaid-lint` (वास्तविक पार्सर, बिना ब्राउज़र + जीवित पेज पर रीडबैक) |
| मॉडल-बजट, कोटा, महंगे reviewers/advisors को सीमित रूप से उपयोग करना | मल्टी-एजेंट | `budgetierung` (खाता + बातचीत; मॉडल-चयन स्वयं: `/model-strategy`) |

पूरी सूची: Skill `code-skill-index`।

## Red Flags (तर्कसंगत बहाने जिनका अर्थ STOP है)

| विचार | वास्तविकता |
|---------|----------|
| „यह तो बस एक छोटा सा सवाल है।" | सवाल भी कार्य होते हैं — पहले skill-जाँच करें। |
| „मैं इस अवधारणा को जानता हूँ।" | अवधारणा जानना ≠ skill का उपयोग करना। लाइव फ़ाइल पढ़ें। |
| „यह skill ज़रूरत से ज़्यादा है।" | सरल चीज़ें जटिल बन जाती हैं — उपयोग करें। |
| „मैं पहले खुद खोजबीन करता हूँ।" | Skills बताते हैं कि खोजबीन कैसे करें। पहले जाँचें। |

## रखरखाव

परिवार में बदलाव होने पर रूटिंग-तालिका अपडेट करें (Subskill `skill-family-care` या `skill-explorer` से नया `inventory_skills.py`-रन)।

## चेंजलॉग

### 0.9.0 (2026-10-03)
- नए skill `budgetierung` (परिवार Multi-Agent) के लिए रूटिंग-पंक्ति: मॉडल-कोटा पर बातचीत करना, उसका संचालन और समायोजन — `model-strategy` के पूरक के रूप में खाता-बही (वहाँ लिखा है कि *कौन सा* मॉडल उपयुक्त है; `budgetierung` तय करता है कि उसमें से *कितना*)।

### 0.8.0 (2026-09-20)
- नए skill `mermaid-lint` के लिए रूटिंग-पंक्ति जोड़ी गई (परिवार Coding & Debugging): Mermaid-आरेख, जिन्हें GitHub „Unable to render rich display" के साथ अस्वीकार करता है, तथा सभी ```mermaid-ब्लॉक्स पर पूरे org में जाँच-चक्र।

### 0.7.0 (2026-08-20)
- `choose-your-orchestrator` को जटिल मल्टी-एजेंट कार्य के लिए पूर्ववर्ती सिफ़ारिश और अनुबंध-संवाद के रूप में जोड़ा गया; निष्पादन-रूटिंग `orchestrator`, `swarm-operations` और `model-strategy` की ओर उससे अलग रखी गई।

### 0.6.0 (2026-08-19)
- नए skill paveman के लिए रूटिंग-पंक्ति („नियम-/स्मृति-फ़ाइल संक्षिप्त करना, सामग्री बदले बिना"): पहले से इंस्टॉल नियतात्मक संक्षेपण-मॉड्यूल `paveman` (T-20260819-213392123) के ऊपर पतला रैपर; `knappform` से सीमांकन (फ़ाइल-एडिट के बजाय LLM-बोलचाल शैली)।

### 0.5.0 (2026-08-19)
- नए skill tidy-up के लिए रूटिंग-पंक्ति („सत्र समाप्त होने पर प्रोजेक्ट साफ़ करना": सक्रिय प्रोजेक्ट फ़ोल्डर के लिए एक बार का Tasksolver+Writer+Maintainer-चक्र; `/goal`-निर्माणों के लिए `work-autonomous`-स्तर-1-स्रोत के रूप में गिना जाता है)।

### 0.4.0 (2026-08-18)
- नए skill human-loop-audit के लिए रूटिंग-पंक्ति („App-/GUI-श्रृंखला को उपयोगकर्ता के साथ मिलकर टेस्ट करना", ज़िपर-ऑडिट समानांतर मरम्मत-सौंपने के साथ; उस समान-नाम पर लगने वाले, किंतु सामग्री में भिन्न reissverschluss-merge से सीमांकित)।

### 0.3.0 (2026-08-18)
- नए skill file-collect-sort-action के लिए रूटिंग-पंक्ति („फ़ाइलें नियम-आधारित तरीके से इकट्ठा करना/छाँटना", T-20260818-916568570 से रखे गए f-csa-ट्रिगर-वाक्यों की पहचान)।
- बाद में जोड़ा गया: reissverschluss-merge की रूटिंग-पंक्ति skills-Repo के स्रोत में नहीं थी (केवल deployment `~/.claude/skills/` में मौजूद थी) — संपादन के समय विचलन (drift) दिखा और यहाँ पुनर्स्थापित किया गया, ताकि भविष्य का deploy उसे अधिलेखित न करे।
- `version:`-फ़ील्ड को अब तक पहुँचे चेंजलॉग-स्तर (0.2.0) से मिलाया गया और 0.3.0 तक आगे बढ़ाया गया — पहले यह 0.1.0 पर रुका हुआ था।

### 0.2.0 (2026-07-03)
- नए skills के लिए रूटिंग-पंक्तियाँ: skill-extractor, workflow-extract, rotation-check, idea-mining, bilingual-doc-sync (Codex-Automations-निष्कर्षण)।

### 0.1.0 (2026-06-17)
- प्रारंभिक संस्करण। ऑडिट-मोड ([F]) द्वारा using-superpowers के समकक्ष के रूप में बनाया गया। 2026-06-17 के ऑडिट से रूटिंग-तालिका (10 user-परिवार)।
