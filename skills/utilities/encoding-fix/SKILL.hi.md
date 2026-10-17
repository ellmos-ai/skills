---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "डबल/ट्रिपल एन्कोडेड UTF-8 के लिए Mojibake-मरम्मत। Windows-cp1252/Latin-1 की गलत व्याख्या को ठीक करता है। बिना निर्भरताओं के।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: hi
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/encoding_fix.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c637d841765295aae889df92b106b3dfa66071f13ab32be04e1d1cfe21520d56
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.226464+00:00"
---
<img src="banner.png" width="100%" alt="encoding-fix banner">

# एन्कोडिंग फिक्स

Mojibake (डबल/ट्रिपल एन्कोडेड UTF-8) की मरम्मत करता है जो Windows cp1252/Latin-1
की गलत व्याख्या से उत्पन्न होता है। शून्य निर्भरताएँ — केवल Python stdlib।

## विशिष्ट समस्या

```
"ue" (U+00FC) → UTF-8 \xc3\xbc → als cp1252 gelesen → "Ã¼"
```

## उपयोग

### लाइब्रेरी के रूप में
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # → "Würge"
```

### सबप्रोसेस-आउटपुट
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Einzelnen String prüfen
python encoding_fix.py              # Selbst-Test
```

## विशेषताएँ

- **इडेम्पोटेंट:** सही ढंग से एन्कोडेड टेक्स्ट में बदलाव नहीं होता
- **3 राउंड तक:** ट्रिपल-एन्कोडेड स्ट्रिंग्स की भी मरम्मत करता है
- **सबप्रोसेस डिकोडर:** प्रोसेस आउटपुट के लिए UTF-8/cp1252 फॉलबैक
- **शून्य निर्भरताएँ:** केवल Python stdlib

## चेंजलॉग

### 1.0.0 (2026-03-12)
- BACH system/tools/encoding_fix.py से पोर्ट किया गया
