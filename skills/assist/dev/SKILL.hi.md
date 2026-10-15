---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "डेवलपर सहायक (ATI का उत्तराधिकारी)। हेडलेस स्कैन के माध्यम से त्वरित प्रोजेक्ट अवलोकन प्रदान करता है और उपलब्ध कोडिंग टूल्स की ओर रूट करता है: CodeCommander MCP (विश्लेषण/रिफैक्टर/निदान) और ellmos-code-tools मॉड्यूल। शुद्ध टूल रूटिंग + स्कैन, कोई अपना स्टोर नहीं।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: hi
status: active
visibility: public
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e0c349589cfe3b0cf418f3deb24b7fb097d45ef52358ad19a4958a96d7f5a0ef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.382387+00:00"
---
<img src="banner.png" width="100%" alt="dev banner">

# Dev — डेवलपर-सहायक (ATI)

अवलोकन प्राप्त कराता है, फिर सही टूल्स को कार्य सौंपता है।

## उद्देश्य

BACH के ATI/entwickler-एजेंट का उत्तराधिकारी। दो कार्य:
1. **प्रोजेक्ट-स्कैन** (हेडलेस, stdlib): महंगे विश्लेषण से पहले किसी प्रोजेक्ट की संरचना, भाषाओं और बिल्ड-मार्करों का तेज़, टोकन-बचत वाला अवलोकन।
2. **टूल-रूटिंग:** अपने टूल दोहराने के बजाय उपलब्ध कोडिंग टूल्स की ओर भेजता है।

## ट्रिगर

| उपयोगकर्ता इनपुट | कार्रवाई |
|---|---|
| „प्रोजेक्ट X का अवलोकन दो" | `dev_core.py scan <pfad>` |
| „यह किस तरह का प्रोजेक्ट है / कौन सा स्टैक?" | `dev_core.py scan <pfad>` |
| „इस फ़ाइल का विश्लेषण करो / रिफैक्टर करो" | → CodeCommander-MCP |
| „Python-कोड बनाओ/जाँचो" | → CodeCommander-MCP / ellmos-code-tools |

## टूल-परिदृश्य (रूटिंग-लक्ष्य)

- **CodeCommander-MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`,
  `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`,
  `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation` आदि।
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): CLI-डेवटूल्स (Structural-Edit,
  pycutter-संदर्भ, Method-Analyzer)।
- **FileCommander-MCP**: बड़े वृक्षों पर फ़ाइल-/डायरेक्टरी-संचालन।

## CLI-प्रवेश (dev_core.py)

```bash
python dev_core.py scan .              # aktuelles Projekt
python dev_core.py scan /pfad/projekt  # Struktur + Sprachen + Marker
```

पहचानता है: अन्य के साथ Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go,
Java, Roblox (Rojo), Docker, Git-रिपॉज़िटरी।

## स्टोर

कोई स्टोर नहीं। केवल स्कैन + रूटिंग।

## दृष्टिकोण

हम CodeCommander/ellmos-code-tools को कोडिंग टूल्स के रूप में अनुशंसित करते हैं, लेकिन यदि उपयोगकर्ता चाहे तो अन्य (जैसे ruff/pylint/eslint) के लिए भी खुले हैं।

## डेटा-गोपनीयता

- `dev_core.py` केवल फ़ाइल-/डायरेक्टरी-नाम (संरचना) पढ़ता है, कोई सामग्री नहीं, कोई अपलोड नहीं।
- छोड़ी जाने वाली चीज़ों में अन्य के साथ `.git`, `node_modules`, `.venv`, `__pycache__` शामिल हैं।

## संबंधित संसाधन

- `assist/AGENTS.md` — अंब्रेला-राउटर
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## परिवर्तन-लॉग

### 0.1.0 (2026-06-22)
- प्रारंभिक संस्करण। ATI/entwickler का उत्तराधिकारी: हेडलेस प्रोजेक्ट-स्कैन (stdlib) + CodeCommander-MCP / ellmos-code-tools पर रूटिंग। उपयोगकर्ता-तटस्थ, कोई स्टोर नहीं।
