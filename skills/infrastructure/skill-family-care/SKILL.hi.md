---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "स्किल-परिवारों को अद्यतन रखने वाला रखरखाव-स्किल, बिना पूरे skill-explorer-ऑडिट के। इस स्किल का उपयोग तब करें जब किसी नए स्किल को सही परिवार में जोड़ना हो, परिवार बदलने के बाद परिवार-हेडर राउटर को अद्यतन करना हो, या किसी अनाथ राउटर को हटाना हो। \"परिवारों का रखरखाव करो\", \"नए स्किल को एक परिवार को सौंपो\", \"राउटर अद्यतन करो\", \"परिवार-हेडर सेट/हटाओ\" जैसे संकेतों पर भी सक्रिय करें।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: hi
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
translated_from_sha256: b4d39973bb0e97c3190c0f821fe0a351a0f338cdfd1ea6fff26d44d1ca476c21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="skill-family-care banner">
# स्किल-परिवार-रखरखाव

## उद्देश्य

स्किल-**परिवारों** को अद्यतन रखता है — `skill-explorer` के पूर्ण ऑडिट-रन के बिना। इसे इंस्टॉलर-सिद्धांत के अनुसार अलग किया गया है (मोनोलिथ के बजाय हल्का उप-स्किल)। यह `skill-explorer` की स्क्रिप्टों को संदर्भित करता है, उन्हें कॉपी नहीं करता।

## स्रोत (दोहराएँ नहीं)

- **परिवार-सूची:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (आधिकारिक परिवार-/रूटिंग-मैप)।
- **सूची (वर्तमान स्थिति):** `skill-explorer/scripts/inventory_skills.py`।
- **राउटर सेट/हटाना:** `skill-explorer/scripts/inject_family_header.py`।
- **कॉन्फ़िग (कौन से परिवार जुड़े हैं):** `~/.claude/skills/skill-explorer/config.json`।

## कार्य

### A — किसी नए स्किल को एक परिवार को सौंपना
1. सूची नए सिरे से एकत्र करें:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. `SKILL-MAP.md` से उपयुक्त परिवार चुनें (अक्ष: चरण/चौड़ाई/कठोरता/प्रभाव/कच्चा माल)।
3. स्किल को `config.json` (`families[<fam>].members`) में सदस्य के रूप में और `SKILL-MAP.md` में दर्ज करें।

### B — परिवार बदलने के बाद हेडर-राउटर अद्यतन करना
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- इडेम्पोटेंट: उसी परिवार का मौजूदा ब्लॉक बदल दिया जाता है।
- केवल `editable`/`source=user` स्किल बदले जाते हैं (स्क्रिप्ट में गेट)।

### C — अनाथ राउटर हटाना
`--remove` के साथ वही स्क्रिप्ट (`--router` की आवश्यकता नहीं)।

## लौह नियम

- **सर्वे ≠ परिवर्तन:** केवल उपयोगकर्ता के अपने स्किल को हेडर मिलता है। प्लगइन/बाहरी स्किल को कभी न छुएँ।
- हर परिवर्तन के बाद `config.json` (`families[*].linked`, `updated`) अद्यतन करें।
- परिवार-मैप की सामग्री को एकल स्किलों में कॉपी न करें — केवल मार्गदर्शक ब्लॉक।

## परिवर्तन-लॉग

### 0.1.0 (2026-06-17)
- प्रारंभिक संस्करण। ऑडिट-मोड (P1) द्वारा निर्मित।
