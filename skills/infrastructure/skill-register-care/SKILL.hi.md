---
name: skill-register-care
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-09-20
description: "स्किल-रजिस्टर को सुसंगत रखने वाला रखरखाव-स्किल, जो तीन-भागी स्किल-रजिस्टर (code-skill-index-कैटलॉग, स्किल-इंडेक्स, SKILL-MAP फ़ैमिली-/रूटिंग-मैप) को संभालता है। वास्तविक स्किल-इन्वेंटरी और दस्तावेज़ीकृत रजिस्टर के बीच ड्रिफ़्ट-जाँच के लिए इस स्किल का उपयोग करें: गायब या अधिक प्रविष्टियों की रिपोर्ट करें, काउंट ठीक करें, स्थिति-तिथि सेट करें। „Skill-Register पflegen\", „Index aktualisieren\", „Register-Drift prüfen\", „welche Skills fehlen in der Map\" जैसे अनुरोधों पर भी सक्रिय करें; हिंदी समकक्ष अनुरोधों पर भी: ‘स्किल-रजिस्टर का रखरखाव करें’, ‘इंडेक्स अपडेट करें’, ‘रजिस्टर-ड्रिफ़्ट जाँचें’, ‘मैप में कौन-से स्किल गायब हैं’ पर सक्रिय करें।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
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
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.2.0"
translated_from_sha256: 6a187b857227bb33edb71c82f4b992a376877192b746a6eea17458e9819cae46
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="skill-register-care banner">
# स्किल-रजिस्टर-केयर

## उद्देश्य

**रजिस्टर** को ड्रिफ़्ट-मुक्त रखता है। रजिस्टर तीन आपस में जुड़े आर्टिफ़ैक्ट से बना है — कभी चौथा नहीं बनाना, हमेशा इन्हीं तीन का विस्तार करना:

| आर्टिफ़ैक्ट | भूमिका | रखरखाव |
|---|---|---|
| `~/.claude/skills/code-skill-index/references/catalog-*.md` | श्रेणी-कैटलॉग | क्यूरेटेड, हाथ से |
| `<USER_HOME>/OneDrive/.SYNC/CLAUDE-CODE-SKILLS.md` | क्रॉस-सिस्टम-इंडेक्स (Claude Desktop के लिए एकमात्र स्किल-दृश्य) | **स्वचालित**, नीचे देखें |
| `<USER_HOME>/OneDrive/.USR/SKILL-MAP.md` | फ़ैमिली-/रूटिंग-मैप | क्यूरेटेड, हाथ से |

## स्वचालित: क्रॉस-सिस्टम-इंडेक्स

इंडेक्स अब **हाथ से** अपडेट नहीं किया जाता — इसी कारण वह तीन महीने तक रुका रहा था (21.06. की स्थिति, 20.09.2026 के 152 वास्तविक स्किल्स के मुकाबले; 81 गायब थे)। इसके बजाय:

```bash
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --check
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --apply
```

यह वैसे भी **दैनिक `/sync` में चरण 2b** के रूप में चलता है; यहाँ मैन्युअली केवल तभी, जब अभी स्किल बने या deploy हुए हों और इंडेक्स तुरंत सही होना चाहिए। यह रन additiv और idempotent है: क्यूरेटेड संक्षिप्त विवरण बने रहते हैं, गायब स्किल्स Library-श्रेणी के अनुसार क्रमबद्ध होते हैं, और सक्रिय `SKILL.md` के बिना प्रविष्टियाँ **हटाई नहीं, बल्कि चिह्नित** की जाती हैं।

## ड्रिफ़्ट-जाँच-प्रक्रिया (दो क्यूरेटेड रजिस्टर)

1. **वर्तमान स्थिति जुटाएँ:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   केवल `source=user`-स्किल्स रजिस्टर-प्रासंगिक हैं (Plugin/बाहरी बाहर रहते हैं)।
2. **अपेक्षित स्थिति पढ़ें:** तीनों रजिस्टर-आर्टिफ़ैक्ट।
3. **अंतर निकालें:**
   - **गायब** (इन्वेंटरी में, रजिस्टर में नहीं) → जोड़ें।
   - **अनाथ** (रजिस्टर में, इन्वेंटरी में अब नहीं) → **पहले देखें, फिर निर्णय लें।**
     जिस स्किल-फ़ोल्डर का `SKILL.md` `CONTENT.md` में बदला गया है, वह *अपंजीकृत (डीरजिस्टर्ड)* है: जानबूझकर अब स्किल के रूप में लोड नहीं होता, पर सामग्री मौजूद है और `code-skill-index` के ज़रिए खोजा जा सकता है। इन्वेंटरी उसे नहीं गिनती, फिर भी हटाना नहीं है — चिह्नित करें। वास्तव में हटाएँ केवल तभी, जब फ़ोल्डर ही न रहे।
   - **काउंट-विचलन** (जैसे „18 स्किल्स" अब सही नहीं) → संख्या ठीक करें।
4. **जोड़ना:** हर नए स्किल के लिए उपयुक्त `catalog-<kategorie>.md` में एक पंक्ति, Skill-Index में एक पंक्ति (+ हेडर-तिथि), और — यदि नई/बदली हुई फ़ैमिली है — `SKILL-MAP.md` में एक खंड।
5. **स्थिति-तिथि** सभी प्रभावित फ़ाइलों में वर्तमान तिथि पर सेट करें।

## सहायक स्निपेट (गायब user-स्किल्स की सूची)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
आउटपुट को रजिस्टर-आर्टिफ़ैक्ट से मिलाएँ (मैन्युअली या grep से)।

## लौह नियम

- **कोई चौथा रजिस्टर नहीं** — केवल तीनों का विस्तार करें।
- केवल user-authored स्किल्स रजिस्टर में जाते हैं; तृतीय-पक्ष बाहरी पथ का अनुसरण करते हैं।
- तिथि का अनुमान न लगाएँ — वर्तमान तिथि सेट करें।
- क्रॉस-सिस्टम-इंडेक्स **हाथ से न संभालें**; `skill_index_care.py` चलाएँ। जो वहाँ मैन्युअली पंक्तियाँ जोड़ता है, वह अगला चुपचाप ड्रिफ़्ट बनाता है।

## Changelog

### 0.2.0 (2026-09-20)
- क्रॉस-सिस्टम-इंडेक्स `CLAUDE-CODE-SKILLS.md` को `.SYNC/scripts/skill_index_care.py` में बदला गया
  (additiv, चिह्नित करने वाला, idempotent) और दैनिक `/sync` में चरण 2b के रूप में जोड़ा गया। कारण:
  इंडेक्स 2026-06-21 से रुका था — 81 स्थानीय स्किल्स गायब थे, 15 प्रविष्टियाँ बिना चिह्न के
  अपंजीकृत प्रक्रियाओं की ओर इशारा कर रही थीं, और एक ऐसे फ़ोल्डर की ओर जिसमें `SKILL.md` नहीं था।
- „अनाथ" को सटीक किया गया: रजिस्टर से हटाए गए स्किल्स (`SKILL.md` के बजाय `CONTENT.md`) चिह्नित किए जाते हैं,
  हटाए नहीं — अन्यथा इंडेक्स को अद्यतन करते समय 15 क्यूरेटेड प्रविष्टियाँ मिट जातीं।

### 0.1.0 (2026-06-17)
- प्रारंभिक संस्करण। Audit-मोड (P2) से बना। कारण: 2026-06-17 के ऑडिट में SKILL-MAP में लगभग 10 user-स्किल्स गायब थे
  (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding,
  update-cli-docs, migrate-rename, plugin-system तथा Therapie- और Game-Dev-फ़ैमिली)।
