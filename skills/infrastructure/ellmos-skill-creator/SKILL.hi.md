---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "इस इकोसिस्टम के लिए एक Skill बनाता या संशोधित करता है: सामान्य इंटरव्यू-/ड्राफ्ट-/Eval-लूप को आधिकारिक skill-creator-Plugin (Anthropic, Apache-2.0) को सौंपता है, लेकिन साथ ही वे ellmos-आवश्यकताएँ भी लागू करता है जिन्हें आधिकारिक Plugin नहीं जानता — हाउस-Frontmatter (9 फ़ील्ड), Kategorie/Sichtbarkeits-नियम, grounding-seed के माध्यम से प्रदाता-/उपयोगकर्ता-/ellmos-निरपेक्ष पर ellmos-संवेदनशील पहचान, साथ में प्रदान की गई config.json (जिसमें Lernvertrag शामिल है) + connections.json, प्रदाता-/Vendor-जागरूकता (State-of-the-Art-विकल्प सुझाना, जिनमें ellmos के अपने घटक शामिल हैं), एक स्व-अद्यतन खंड और एक पुन: उपयोग योग्य Lern-/Abdeckungs-फ़ाइलसेट (user-usecases.json, usecase-gaps.json, known-providers-and-abilities.json, gap-closing-analysis.json — skill-creator की evals.json और A2A/AgentSkill से प्रेरित, कोई समानांतर मानक नहीं)। जब भी इस सिस्टम के लिए कोई NEUER Skill बनना हो या किसी मौजूदा Skill को ellmos-अनुरूपता में अपग्रेड करना हो तो इसे हमेशा उपयोग करें — \"erstelle einen Skill\", \"bau mir einen Skill für X\", \"skill-creator nutzen\", \"neuen Skill anlegen\", \"diesen Skill ellmos-konform machen\", \"Lernvertrag/Verhaltenscodex für einen Skill anlegen\", \"Usecase-Abdeckung eines Skills prüfen\" जैसे अनुरोधों पर भी। केवल Skill-खोज/रूटिंग के लिए इसके बजाय skill-finder, और लैंडस्केप-ऑडिट के लिए skill-explorer का उपयोग करें।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: hi
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 1e6dace03eb8afc639fa08debace08a61441912a22399c11a49f7fe6e7dc3ecb
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T04:00:36.052261+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## उत्पत्ति और निर्णय (Fork बनाम स्वनिर्माण)

**निर्णय: स्वनिर्माण, कोई Fork नहीं।** कारण, ताकि यह न खो जाए:

- `skill-creator` (Anthropic, Marketplace `claude-plugins-official`) **Apache-2.0** के अंतर्गत लाइसेंसित है
  (क्लोन में LICENSE-पाठ पढ़ा और सत्यापित किया गया, 2026-08-24) — एक Fork कानूनी रूप से साफ़ संभव होता और
  रेपो में अन्यत्र यह पहले से स्थापित पैटर्न है (`skills/third-party/grilling`)।
- लेकिन एक Fork मूल की पूरी Eval-/Benchmark-मशीनरी साथ ले आता (`agents/{analyzer,comparator,grader}.md`, `eval-viewer/`, 7 Scripts,
  485-पंक्ति SKILL.md) — वह क्षमता जो पहले से मौजूद है और सीधे कॉल की जा सकती है (`Skill: skill-creator:skill-creator`)।
  `.PLUGINS/CLAUDE.md` के नियम 4 ("दोबारा बनाने से पहले क्षमताएँ जाँचें") और पैटर्न P10 ("दो स्विच, जिनकी कोई तुलना नहीं
  करता") के अनुसार यह विस्तार नहीं, दोहराव होता।
- असली कमी **पूरी तरह ellmos-विशिष्ट** है और मूल को मूलतः अज्ञात है:
  हाउस-Frontmatter (`templates/SKILL.md`), `docs/CONVENTIONS.md`, प्रदाता-/User-/ellmos-निरपेक्षता ellmos-संवेदनशीलता के
  साथ, `grounding-seed`-संबंध, Vendor-Awareness, स्व-अद्यतन।
- इस Skill में **कोई Anthropic-पाठ नहीं** है (हर जगह अपनी शब्दावली) — इसलिए संशोधनों के लिए Apache-2.0-
  श्रेय-दायित्व भी उत्पन्न नहीं होता। यह मूल को **संयोजित** करता है, नकल नहीं करता: यही कानूनी रूप से सबसे साफ़
  और रखरखाव में सबसे कम खर्चीला रास्ता है।

## कब सक्रिय करें

- "erstelle einen Skill für X", "neuen Skill bauen", "skill-creator nutzen"
- "mach diesen Skill ellmos-konform", "Skill auf Haus-Standard nachrüsten"
- हमेशा जब **लक्ष्य-स्थान** `.AI/.SKILLS/skills/…` में एक Skill हो (या उसका कैनोनिकल Plan-D-क्लोन)। सामान्य, इस
  ईकोसिस्टम से असंबंधित अनुरोधों ("मुझे बिना किसी संदर्भ के कोई भी Claude-Skill बनाओ") पर नहीं।

## प्रक्रिया

### चरण 1 — इंटरव्यू/ड्राफ्ट/Eval सौंपें

`Skill: skill-creator:skill-creator` को कॉल करें: इरादा स्पष्ट करने, SKILL.md-संरचना का ड्राफ्ट बनाने, टेस्ट-केस, Eval-लूप और
Description-अनुकूलन (`scripts/improve_description.py`) के लिए। **इसे दोबारा न बनाएँ** — यह भाग सामान्य है और मूल में पहले से
अच्छी तरह हल है।

### चरण 2 — ellmos-हाउस-Scaffold लगाएँ (अनिवार्य, मूल फ़ॉर्मेट में जोड़ते हुए)

मूल द्वारा बनाए गए SKILL.md में `.SKILLS/templates/SKILL.md` से नौ हाउस-फ़ील्ड जोड़ें (प्रकार के अनुसार `AGENT.md`/
`WORKFLOW.md`/`PROMPT.md`), पहले `.SKILLS/docs/CONVENTIONS.md` पढ़ें — Kategorie-फ़ोल्डर, Flat-नियम (<5 फ़ाइलें
फ्लैट), Versions-परंपरा (SemVer: MAJOR/MINOR/PATCH) और बहुभाषी सेट (Core: DE+EN अनिवार्य)। **`visibility` सदैव
`private-only` से शुरू होता है** — प्रकाशन एक बाद का, जाँचा हुआ उपयोगकर्ता-निर्णय है (`.AI/VISIBILITY-POLICY.md`), कभी
डिफ़ॉल्ट नहीं। ये फ़ील्ड Anthropic-फ़ॉर्मेट के **अतिरिक्त** हैं (`name`/`description` के पास अतिरिक्त
YAML-कुंजियाँ) — इस तरह बना हर Skill पूरी तरह `anthropic_compatible: true` रहता है।

### चरण 3 — सिद्धांत लागू करें: प्रदाता-निरपेक्ष, उपयोगकर्ता-निरपेक्ष, ellmos-निरपेक्ष-पर-ellmos-संवेदनशील

पूरा पाठ + कोड-पैटर्न: `references/ELLMOS-PRINCIPLES.md`। सार: बनाया गया Skill **अकेले चलने योग्य** होना चाहिए (जो चाहिए सब
साथ लाए) और **साथ ही** ellmos-घटक उपलब्ध होते ही उनका उपयोग करे — यह रनटाइम पर स्वयं तय करता है, कभी स्थिर
रूप से जुड़ा हुआ नहीं। यह ठीक वही पैटर्न है जो `grounding-seed` पहले से देता है (README: "cultivated landscape,
not wildflower" / "viable alone, more productive together") — **कोई दूसरी पहचान-व्यवस्था नहीं गढ़ी जाती**; यह
Skill उत्पादित Skills को लगातार `grounding_seed.detect_ecosystem()` की ओर भेजता है।

### चरण 4 — config.json + connections.json साथ दें

`grounding-seed` पहले से एक Python-पैकेज के रूप में इम्पोर्ट योग्य है (सत्यापित 2026-08-24: `import grounding_seed`
स्थानीय क्लोन किए गए `grounding-seed`-स्रोत-वृक्ष पर सफलतापूर्वक हल होता है, Plan-D-क्लोन) — यह **कैनोनिकल
जुड़ाव-बिंदु** है, कोई नई फ़ाइल नहीं गढ़ी जाती। हर उत्पादित Skill के लिए जिसकी बाहरी आवश्यकताएँ हों (प्रोग्राम,
सेवाएँ, प्रदाता):

- **`config.json`** — Skill-अपनी सेटिंग्स (टेम्पलेट: `templates/skill-config.template.json`)। `grounding_seed.store.LocalStore(root)` इस फ़ाइल-नाम का
  डिफ़ॉल्ट रूप से अपनी Rollen-फ़ाइल के लिए उपयोग करता है — यानी एक उत्पादित Skill या तो अपना `config.json`
  सीधे `LocalStore`-बैकएंड के रूप में उपयोग कर सकता है, या अलग रखे यदि उसे भूमिकाओं के अलावा शुद्ध
  व्यवहार-सेटिंग्स भी चाहिए (तब दूसरा `LocalStore(root, filename="connections.json")`-इंस्टेंस)।
- **`connections.json`** — वास्तव में **हल किए गए** बाहरी जुड़ाव-बिंदु (कौन सा प्रोग्राम/सेवा मिली, कब से, किस
  स्रोत से) — टेम्पलेट: `templates/skill-connections.template.json`, स्कीमा `ellmos.source-resolver.user-config.v1` (`source-resolver` के समान; grounding-seed-
  README के अनुसार जानबूझकर ऐसा चुना गया ताकि बाद में वास्तविक `source-resolver` में माइग्रेशन बिना हानि हो — वहाँ
  `migration.py` देखें)।

विवरण, CLI और कोड-उदाहरण: `references/ELLMOS-PRINCIPLES.md`, खंड "Docking"।

### चरण 5 — प्रदाता-/Vendor-जागरूकता जोड़ें

पूरा पाठ: `references/VENDOR-AWARENESS.md`। सार: उत्पादित Skill को "प्रदाता & विकल्प" नाम का खंड मिलता है, जो (a) विषय के
State-of-the-Art-प्रदाता(ओं) का नाम देता है (जैसे TTS के लिए ElevenLabs), (b) कम से कम एक वैकल्पिक प्रदाता, (c)
ellmos-अपने घटकों को स्पष्ट रूप से समान-स्तर के उम्मीदवार के रूप में सूचीबद्ध करता है, यदि वे विषय कवर करते हों
(जैसे ElevenLabs के बदले या साथ में `ellmos-voice-io`) — और उपयुक्त उपयोगकर्ता-आवश्यकता पर इंस्टॉलेशन/बदलाव
**सुझाता है**, उसे चुपचाप मानकर नहीं चलता। इस सिस्टम पर "क्या उपलब्ध है" का आधार: `grounding_seed.scan.scan_resources([...])` (जाँचता
है `shutil.which`) के साथ `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` ellmos-उम्मीदवारों के लिए।

### चरण 6 — स्व-अद्यतन स्थापित करें

पूरा पाठ: `references/SELF-UPDATE.md`। सार: हर उत्पादित Skill को "Selbstaktualisierung" नाम का खंड मिलता है, जो (a)
State-of-the-Art पर बने रहने के लिए समय-समय पर संक्षिप्त वेब-शोध सुझाता है, (b) संबंधित Skills/Workflows जानता है
और नए विकल्प नाम देता है जो बेहतर बैठ सकते हैं, (c) एक छोटी Lern-JSON रखता है (टेम्पलेट: `templates/skill-connections.template.json`, फ़ील्ड
`notizen`/`gelernt`), जिसे ellmos-Memory-घटक (USMC/Gardener) उपलब्ध होने पर स्थानीय रूप से बढ़ने
के बजाय वहाँ ले जाया जा सकता है — यहाँ भी: स्थिर रूप से जोड़ने के बजाय पहचानना (`grounding_seed.detect_ecosystem()`)।

### चरण 6b — Lernvertrag + Usecase-Abdeckung स्थापित करें (पुन: उपयोग योग्य पैटर्न)

पूरा पाठ: `references/LEARNING-CONTRACT-AND-COVERAGE.md`। सार: केवल यह Skill ही नहीं, बल्कि **उसके द्वारा उत्पादित हर Skill** को एक छोटा,
पुन: उपयोग योग्य Lern-/Abdeckungs-फ़ाइलसेट मिलता है — स्थापित मानकों के विरुद्ध जाँचा हुआ, कोई समानांतर मानक
नहीं:

- `evals/evals.json` — **पुन: उपयोग करें**, दोहराएँ नहीं: यह पहले से लेखक द्वारा बनाए गए टेस्ट-केसों का
  skill-creator-मानक है।
- `user-usecases.json` — उपयोगकर्ता द्वारा वास्तव में रखे गए उपयोग-मामले, `evals.json` के समान रूप में
  (टेम्पलेट: `templates/user-usecases.template.json`)।
- `usecase-gaps.json` — मिलान: कौन से उपयोगकर्ता-Usecases अपरीक्षित/अनकवर्ड हैं (टेम्पलेट: `templates/usecase-gaps.template.json`)।
- `known-providers-and-abilities.json` — प्रति भूमिका ज्ञात प्रदाताओं का उम्मीदवार-स्थान, फ़ील्ड A2A/`AgentSkill`
  (id/name/description/tags) से प्रेरित, गढ़े हुए नहीं (टेम्पलेट: `templates/known-providers-and-abilities.template.json`)।
- `gap-closing-analysis.json` — हर कमी के लिए संरचनात्मक बंद करने के रास्ते (ellmos-मॉड्यूल, ellmos-Bundle, बाहरी मॉड्यूल,
  नया निर्माण) — `grading.json.eval_feedback` का दोहराव नहीं (टेम्पलेट: `templates/gap-closing-analysis.template.json`)।
- `config.json` का फ़ील्ड `lernvertrag` — Verhaltenscodex (सर्वोत्तम विकल्प चुनना, **उपयोगकर्ता सर्वोपरि** [अंतिम निर्णय हमेशा उपयोगकर्ता का],
  कभी स्वयं इंस्टॉल न करना, Update-Intervall) — जानबूझकर `config.json` के विस्तार के रूप में, सातवीं फ़ाइल
  नहीं।

स्कीमा: `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — वही हाउस-परंपरा जो `skill-v1.schema.json` में है। `grounding-seed` इस फ़ाइलसेट के लिए
जाँचा गया और जानबूझकर **नहीं** बढ़ाया गया (कारण `LEARNING-CONTRACT-AND-COVERAGE.md` में) — उसका हिस्सा केवल `connections.json` रहता है।

### चरण 7 — रजिस्टर करें, परीक्षण करें, कमिट करें

- `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md` के अनुसार Kategorie-फ़ोल्डर चुनें; संदेह होने पर `skill-finder` या
  `controlcenter_find_skill` से पूछें कि कोई परिवार पहले से है या नहीं।
- कमिट से पहले `testing/` (privacy_gate + Metadaten-Tests) चलाएँ।
- Registry-फ़ाइलें (`registry/components.json`, `SKILLS-MAP.md`, `llms.txt`) **हाथ से संपादित न करें** — वे
  जनरेट होती हैं (`build_public_registry.py`, `build_skills_map.py`, `catalog.py`)। यदि कैनोनिकल क्लोन में अभी कोई
  बाहरी, बिना कमिट की सत्र चल रही हो, तो वैश्विक रूप से पुनः जनरेट न करें (एक ही फ़ाइल में बाहरी और अपने बदलाव
  मिल जाएँगे) — इसके बजाय नए Skill-फ़ोल्डर को अलग से कमिट करें और Registry-पुनर्जनन अगली साफ़ चलाई (`skill-register-care`)
  पर छोड़ें।
- `git commit -- skills/<kategorie>/<name>/` — केवल अपने नए पथ।

## Anthropic-फ़ॉर्मेट के साथ संगतता

सभी अतिरिक्त फ़ील्ड `name`/`description` के बगल में शुद्ध YAML-विस्तार हैं — इस ईकोसिस्टम के बिना
मानक Claude Code अब भी केवल `name`/`description` पढ़ता है और बाकी को अनदेखा करता है।
`config.json`/`connections.json` वैकल्पिक Bundled Resources हैं (जैसा `docs/CONVENTIONS.md` में परिकल्पित),
अनिवार्य निर्भरता नहीं — इनके बिना भी Skill अपरिवर्तित काम करता है।

## संबंधित Skills

- `skill-creator:skill-creator` — सामान्य इंटरव्यू-/Eval-लूप (जिसे सौंपा जाता है, चरण 1)।
- `skill-finder` — मौजूदा अपने Skills के लिए राउटर (बनाने से पहले जाँचें: क्या यह पहले से है?)।
- `skill-explorer` — लैंडस्केप-ऑडिट + नए Skills/Plugins की वेब-खोज (मेटा-स्तर: हमारा Skill-*बेस्टांड*; यह
  Skill इसके बजाय हर *अलग उत्पादित* Skill को स्वयं प्रदाता-जागरूक बनाता है)।
- `skill-family-care`, `skill-register-care` — निर्माण के बाद का रखरखाव।
- `grounding-seed` (मॉड्यूल, `.AI/.MODULES/.CONTROL/grounding-seed`) — वास्तविक जुड़ाव-/स्व-आपूर्ति-तर्क, यहाँ केवल संदर्भित, दोहराया नहीं गया।

## Changelog

### 0.2.0 (2026-08-24)
- परिशिष्ट (Ticket T-20260824-218233618, दायरा-विस्तार): हर उत्पादित Skill के लिए पुन: उपयोग योग्य
  Lern-/Abdeckungs-पैटर्न जोड़ा गया — `user-usecases.json`, `usecase-gaps.json`, `known-providers-and-abilities.json`,
  `gap-closing-analysis.json` (नए हाउस-स्कीमा `.SKILLS/schemas/` में) plus `config.json` में Lernvertrag-फ़ील्ड।
  `evals/evals.json` (skill-creator) जानबूझकर दोहराने के बजाय पुन: उपयोग किया गया। `grounding-seed` जाँचा गया —
  विस्तार की आवश्यकता नहीं (कारण `references/LEARNING-CONTRACT-AND-COVERAGE.md` में), इसलिए कोई अनुवर्ती टिकट नहीं। प्रदाता-कैटलॉग के
  फ़ील्ड-नाम A2A-प्रोटोकॉल (`AgentSkill`) से प्रेरित, अपनी शब्दावली गढ़ने के बजाय।

### 0.1.0 (2026-08-24)
- प्रथम संस्करण। स्वनिर्माण बनाम Fork का निर्णय लिया और उसका कारण दर्ज किया गया (Ticket
  T-20260824-218233618)। सामान्य Skill-निर्माण को `skill-creator:skill-creator` को सौंपता है, साथ में हाउस-Scaffold,
  ellmos-सिद्धांत, `grounding-seed`-संबंध (config.json/connections.json), Vendor-Awareness और स्व-अद्यतन जोड़ता है।
