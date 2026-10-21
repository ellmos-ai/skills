---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Windows-आरक्षित NUL-फ़ाइलों को खोजता और हटाता है, जो Git Bash में /dev/null के उपयोग से बनती हैं। Headless या GUI के साथ।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
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
  origin_path: "system/tools/nulcleaner.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 684d3a24e9aa64d125877cb5f27fc613d89bcf44a2f5e213ea1b65d91cc44a39
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.533170+00:00"
---
<img src="banner.png" width="100%" alt="nulcleaner banner">

# nulcleaner - Windows NUL-फ़ाइल सफ़ाई

## समस्या

जब Git Bash में Windows पर `/dev/null` को कमांड में उपयोग किया जाता है (जैसे `> /dev/null`),
तो किसी "कहीं नहीं" के रीडायरेक्शन के बजाय वर्तमान
डायरेक्टरी में एक वास्तविक **`nul` नाम की फ़ाइल** बन जाती है। Windows "NUL" को एक डिवाइस-नाम के रूप में
आरक्षित रखता है, इसलिए ये फ़ाइलें सामान्य तरीके से हटाई नहीं जा सकतीं।

यह टूल ऐसी NUL-फ़ाइलों को विस्तृत UNC पथ (`\\?\`) के माध्यम से खोजता और हटाता है।

---

## मोड

| मोड | विवरण |
|-------|-------------|
| `scan` | डायरेक्टरी में NUL-फ़ाइलों के लिए पुनरावर्ती खोज करें |
| `delete` | NUL-फ़ाइलें खोजें और हटाएँ |
| `gui` | फ़ाइल चयन के साथ ग्राफ़िकल इंटरफ़ेस |

---

## CLI उपयोग

```bash
# Nur scannen (zeigt gefundene NUL-Dateien)
python nulcleaner.py scan /pfad/zum/verzeichnis

# Scannen und loeschen
python nulcleaner.py delete /pfad/zum/verzeichnis

# GUI-Modus starten
python nulcleaner.py gui
```

---

## Headless API (एकीकरण के लिए)

यह टूल headless संचालन के लिए एक Python API भी प्रदान करता है:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/pfad/zum/verzeichnis", verbose=True)
print(f"Gefunden: {result['found']}, Geloescht: {result['deleted']}")
```

**वापसी मान:** `{'found': int, 'deleted': int, 'errors': list}`

---

## तकनीकी विवरण

- Windows-आरक्षित फ़ाइलनामों को हटाने के लिए विस्तृत UNC पथ (`\\?\`) का उपयोग करता है
- `os.walk()` के साथ पुनरावर्ती स्कैन
- tkinter के साथ GUI (कोई बाहरी निर्भरता नहीं)
- केवल Windows पर काम करता है (समस्या वहीं उत्पन्न होती है)

---

## रोकथाम

सबसे अच्छा है Git Bash में `/dev/null` से बचना। इसके बजाय:
- आउटपुट को बस छोड़ दें
- Stderr रीडायरेक्शन के लिए `2>&1` का उपयोग करें
- Shell स्क्रिप्ट में Windows-संगतता का ध्यान रखें
