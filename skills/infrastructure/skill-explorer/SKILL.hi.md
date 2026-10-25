---
name: skill-explorer
version: 1.1.1
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-08-24
description: "अपने स्वयं के skill परिदृश्य का प्रबंधन करता है: मौजूदा skills का सर्वेक्षण और तुलना करता है (Audit mode), नई skills/plugins के लिए वेब पर शोध करता है (Explore mode), और साथ ही वह installer भी है जो एक monolith लोड करने के बजाय हल्के subskills (Skill-Finder, family umbrella, maintenance skills) उत्पन्न करता है। इस skill का उपयोग \"compare/audit skills, skills की तुलना/ऑडिट करें\", \"which skills are duplicated, कौन से skills डुप्लिकेट हैं\", \"form skill families, skill families बनाएँ\", \"clean up/consolidate skills, skills की सफ़ाई/समेकन करें\", \"maintain the skill register, skill register का रखरखाव करें\", \"find skills/plugins for topic X, विषय X के लिए skills/plugins खोजें\", \"install new skills, नए skills install करें\", \"browse the skill marketplace, skill marketplace ब्राउज़ करें\" के लिए करें, या `/skill-explorer` के लिए। यह प्रति family एक sub-report और एक वैश्विक रूप से क्रमांकित निर्णय सूची देता है; सुरक्षा जांच और स्पष्ट स्वीकृति के बाद ही install/uninstall करता है।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: hi
status: active
visibility: public
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 290cc943766331f12d02c48949c72ba33065d7b80c835a1d9a3edfa08a17bf21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="skill-explorer banner">

# Skill-Explorer — Skill-परिदृश्य का प्रबंधन (Audit · Explore · Installer)

## उद्देश्य

Skill-भंडार बढ़ने पर डुप्लिकेट, अप्रयुक्त संसाधन और अस्पष्ट "कौन सा skill किसकी जगह" वाली स्थितियाँ बनती हैं — और बाहर लगातार नए Skills/Plugins आते रहते हैं। `skill-explorer` तीन भूमिकाओं को एक उपकरण में जोड़ता है:

| भूमिका | वह क्या करती है | विवरण |
| --- | --- | --- |
| **Audit-Modus** (अंदर की ओर) | सभी Skills का अवलोकन, families में clustering, क्षमताओं/निर्भरताओं/संसाधनों का संग्रह, प्रति family उप-रिपोर्ट + क्रमांकित सिफ़ारिशें | `references/audit-mode.md` |
| **Explore-Modus** (बाहर की ओर) | वेब (Web/GitHub/Reddit, द्विभाषी) पर किसी विषय के लिए नए Skills/Plugins की खोज, तुलना, गेटेड installation | `references/explore-mode.md` |
| **Installer** | हल्के subskills *उत्पन्न* करता है, monolith के बजाय — Skill-Finder, Family-Umbrella, Maintenance-Skills | नीचे + `references/family-care.md` |

आह्वान: `/skill-explorer` (Audit डिफ़ॉल्ट) या "… के लिए विषय X खोजें" (Explore)। दोनों मोड टैक्सोनॉमी (`references/clustering.md`), रिपोर्ट प्रारूप (`references/report-format.md`) और क्रमांकन योजना साझा करते हैं, ताकि उपयोगकर्ता एक ही संख्या-सूची से उत्तर दे सके।

## Installer-सिद्धांत और स्थायित्व

स्वयं monolithic रूप से बढ़ने के बजाय, `skill-explorer` आवश्यकता पड़ने पर हल्के, अलग-अलग लोड होने योग्य subskills *उत्पन्न* करता है — इसलिए कोई अति लंबा एकल skill कभी लोड नहीं करना पड़ता:

- **Skill-Finder** ([F]) — सक्रिय finder/router, "using-superpowers" द्वारपाल के समान, जो हर कार्य से पहले register पढ़ता है और उपयुक्त family की ओर route करता है (`references/skill-finder.md`, टेम्पलेट `assets/skill-finder-template.md`)।
- **Family-Umbrella** (c1) — एक meta-skill जो पूरी family को जानता है (`assets/family-umbrella-template.md`)।
- **Maintenance-Skills** ([P1] families, [P2] register) — families/register को अद्यतन रखते हैं (`references/family-care.md`)।

निर्णय `~/.claude/skills/skill-explorer/config.json` में संग्रहीत होते हैं (`references/config.md`, टेम्पलेट `assets/config.example.json`): आरंभ में पढ़े जाते हैं (ज्ञात families/routers/उत्पन्न subskills), निष्पादन के बाद अद्यतन होते हैं — इस प्रकार पुनः-रन कुछ भी दोबारा नहीं बनाता।

## Branch-तंत्र (तृतीय-पक्ष को अनुकूलित करना)

एक केवल-पठनीय skill (plugin, आयातित तृतीय-पक्ष) को मूल को बदले बिना अनुकूलित किया जा सकता है: मूल निर्देशिका पूरी तरह कॉपी की जाती है (**Branch**); फिर केवल प्रति को संपादित किया जाता है। Branch में चार अनिवार्य विवरण होते हैं: मूल का संदर्भ, Branch-तिथि, संपादक और कारण। जैसे ही Branch मूल का स्थान लेता है, मूल को runtime के लिए deregister किया जाता है (`SKILL.md` → `CONTENT.md`) या family-router को Branch की ओर इंगित किया जाता है, ताकि दो लगभग समान skills टकराएँ नहीं। तृतीय-पक्ष Branches **निजी** रहते हैं — वे सार्वजनिक `.AI/.SKILLS`-library में नहीं जाते। विवरण: `references/skill-branching.md`।

## प्रक्रिया

1. **मोड चुनें:** भंडार का अवलोकन/सफ़ाई → Audit-Modus। बाहर से खोजना/install करना → Explore-Modus। (Explore किसी पिछले Audit/`config.json` पर आधारित हो सकता है।)
2. **Audit-Modus** (`references/audit-mode.md`): सूची (स्क्रिप्ट) → Family-Cluster → उप-रिपोर्ट → **एक वैश्विक रूप से क्रमांकित निर्णय सूची** (a/b/c1/c2/c3, साथ में R/F/P1/P2)।
3. **Explore-Modus** (`references/explore-mode.md`): द्विभाषी बहु-स्रोत शोध → प्रति उम्मीदवार 3 श्रेणियाँ → प्रभाव-सिमुलेशन → क्रमांकित Install/Remove सिफ़ारिशें।
4. **निष्पादन** केवल उपयोगकर्ता की संख्या-पुष्टि के बाद; skill-निर्माण/परिवर्तन पंजीकृत करें और `config.json` अद्यतन करें।

## लौह नियम

- **Survey ≠ Mutation:** सब कुछ clustering करें, लेकिन केवल **उपयोगकर्ता-स्वामित्व वाले** skills संपादित करें; Plugin/तृतीय-पक्ष skills केवल-पठनीय हैं (कभी हेडर/हटाना नहीं)। जो तृतीय-पक्ष skill बदलना चाहता है, वह इसके बजाय एक **Branch** (fork-प्रति) बनाए — मूल अछूता रहता है, परिवर्तन केवल प्रति पर होता है (→ `references/skill-branching.md`)।
- **Register बढ़ाएँ, डुप्लिकेट न करें:** यदि skill-register मौजूद है (index + family-map + index-skill), तो उसे बढ़ाएँ, चौथा न बनाएँ।
- **सुरक्षा मुख्यतः मैन्युअल:** किसी भी installation से पहले मॉडल स्वयं skill पढ़ता है और निर्णय लेता है; `scripts/scan_skill_security.py` केवल सहायक triage है, ज्ञात सीमाओं के साथ। कभी auto-install नहीं।
- **उत्पत्ति के अनुसार पंजीकरण:** उपयोगकर्ता-लिखित → Library; तृतीय-पक्ष → बाहरी पथ, **Library में नहीं**।

## ऑर्केस्ट्रेशन (मॉडल-तटस्थ)

Family उप-रिपोर्ट या स्रोत/भाषाएँ स्वतंत्र कार्य-पथ हैं। यदि प्लेटफ़ॉर्म orchestrator से सस्ते subagents देता है, तो प्रति family/स्रोत एक subagent सौंपें और orchestrator के रूप में केवल समेकित/जाँचें (विशेषज्ञ-झुंड)। अन्यथा स्वयं क्रमिक रूप से।

## संसाधन

- **मोड:** `references/audit-mode.md`, `references/explore-mode.md`
- **साझा:** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Audit:** `references/family-care.md`, `references/skill-finder.md`
- **Explore:** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Branch:** `references/skill-branching.md`
- **स्क्रिप्ट:** `scripts/inventory_skills.py` (सूची), `scripts/inject_family_header.py` (हेडर-router), `scripts/scan_skill_security.py` (सुरक्षा-triage)
- **टेम्पलेट:** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`, `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Changelog

### 1.1.1 (2026-08-24)
- सूची-सहायक अब पुराने, एक-पंक्ति में क्रमबद्ध `dependencies` मैपिंग भी स्वीकार करता है और खराब मानों को सहनशीलता से संभालता है, पूरे Audit को रोकने के बजाय। इसका समापन संदेश Windows कंसोल के साथ भी संगत है।

### 1.1.0 (2026-06-17)
- Branch-तंत्र जोड़ा गया: तृतीय-पक्ष/केवल-पठनीय skills को fork-प्रति (Branch) द्वारा अनुकूलित किया जा सकता है — मूल के संदर्भ, तिथि, संपादक और कारण के साथ; मूल अछूता रहता है। नियम "Survey ≠ Mutation" में Branch-मार्ग जोड़ा गया। नया खंड `## Branch-Mechanismus`। नए: `references/skill-branching.md`, `assets/branch-header.example.md`।

### 1.0.0 (2026-06-17)
- प्रारंभिक संस्करण। भंडार-Audit (family-clustering, क्रमांकित निर्णय) और वेब-शोध (सुरक्षा-triage के साथ गेटेड install) को एक installer में जोड़ा गया, जो हल्के subskills उत्पन्न करता है।
