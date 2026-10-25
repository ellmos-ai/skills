---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "स्वतंत्र नेविगेशन और रूटिंग रणनीति, जो निर्देशिका पदानुक्रमों को ऊपर और नीचे की ओर CLAUDE.md, AGENTS.md, README.md और RULES.md जैसे मार्गदर्शक दस्तावेज़ों के लिए तथा उपयोगकर्ता द्वारा कॉन्फ़िगर किए जा सकने वाले कीवर्ड के लिए खंगालती है। कॉन्फ़िगरेशन staircase-config.json या config.json के माध्यम से किया जाता है। इसे Up-and-Down Routing या Walking Bass Routing के नाम से भी जाना जाता है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
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
translated_from_sha256: 28ec74023759355f5a974506a065cb0c737455ec4d3d59d23129276e63011200
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.357015+00:00"
---
<img src="banner.png" width="100%" alt="staircase-routing banner">

# Staircase-Routing (Up-and-Down / Walking Bass Routing)

**Staircase-Routing** कौशल, जिसे *Up-and-Down Routing* या *Walking Bass
Routing* भी कहा जाता है, AI एजेंटों के लिए निर्देशिका दस्तावेज़ों की जाँच की
रणनीति को समाहित करता है।

जब कोई एजेंट किसी निर्देशिका में प्रवेश करता है या किसी फ़ाइल पर काम करता है, तो
वह कोड बदलने या कोई कार्रवाई करने से पहले प्रासंगिक संदर्भ, नियम और मार्गदर्शक
दस्तावेज़ खोजने के लिए इस रणनीति का उपयोग करता है।

---

## 1. मार्गदर्शक दस्तावेज़ों के मानक

Staircase-Routing डिफ़ॉल्ट रूप से इन मार्गदर्शक दस्तावेज़ों को खोजता है:

- **वैश्विक और परियोजना-स्तरीय नियंत्रण:** `CLAUDE.md`, `AGENTS.md`,
  `START.md`, `RULES.md`
- **परियोजना अवलोकन और कार्य:** `README.md`, `TODO.md`, `NOTIZ.md`,
  `BEWEISNOTIZ.md`
- **उपयोगकर्ता-परिभाषित कीवर्ड:** `staircase-config.json` या `config.json` के माध्यम से
  कॉन्फ़िगर किए गए।

---

## 2. ट्रैवर्सल एल्गोरिदम

```text
                           [ Root- / Workspace-Ebene ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Schritt 2: Root-Wegweiser lesen)
                           └───────────▲────────────┘
                                       │ (Treppe aufwärts)
                           ┌───────────┴────────────┐
                           │ Unterordner / Ziel     │ ◄── (Schritt 1: Im CWD beginnen)
                           └───────────┬────────────┘
                                       │ (Treppe abwärts)
                           ┌───────────▼────────────┐
                           │ Kind- / Modulordner    │ ◄── (Schritt 3: Untergeordnete Wegweiser finden)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### चरण 1: वर्तमान कार्यशील निर्देशिका (CWD) की जाँच करें

- लक्ष्य फ़ाइल की निर्देशिका या सक्रिय कार्यशील निर्देशिका की जाँच करें।
- यदि मार्गदर्शक दस्तावेज़ मौजूद हों, तो उन्हें तुरंत पढ़ें।

### चरण 2: ऊपर की ओर ट्रैवर्स करें

- यदि CWD में **कोई** मार्गदर्शक दस्तावेज़ नहीं मिलता, तो मूल निर्देशिका
  (`..`) में जाएँ।
- यह प्रक्रिया तब तक चरणबद्ध रूप से दोहराएँ जब तक कोई रूट मार्गदर्शक दस्तावेज़
  (`CLAUDE.md` या `AGENTS.md`) या workspace की सीमा न मिल जाए।
- वैश्विक निर्देशों और परियोजना नियमों को पहचानने के लिए मिले सभी रूट मार्गदर्शकों
  को पढ़ें।

### चरण 3: नीचे की ओर जाँच करें

- पहचाने गए रूट निर्देशिका से उन उप-निर्देशिकाओं की ओर नीचे जाएँ जो कार्य से
  संबंधित हैं।
- मॉड्यूल-स्तर के विशेष मार्गदर्शक, डोमेन नियम या घटक कॉन्फ़िगरेशन खोजें और
  उन्हें पढ़ें।

---

## 3. उपयोगकर्ता-कॉन्फ़िगर करने योग्य कीवर्ड (`staircase-config.json`)

एजेंट खोजे जाने वाले मार्गदर्शकों को अनुकूलित करने के लिए स्थानीय या वैश्विक
`staircase-config.json` पढ़ सकते हैं:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. `letter-hooker` और निर्धारित कार्यों के साथ एकीकरण

`staircase-routing` को केंद्रीय preflight बूटलोडर के रूप में **`letter-hooker`**
कौशल और निर्धारित कार्य **`antigravity-kontext-and-workflow-loader-and-divider`** में एम्बेड किया गया है। इससे एजेंट
परिवर्तन शुरू करने से पहले मार्गदर्शक दस्तावेज़ खोजते और उनका पालन करते हैं।
