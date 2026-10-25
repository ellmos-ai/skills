---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "बैच फ़ाइल ऑपरेशन (हटाना, स्थानांतरित करना, कॉपी करना, सूचीबद्ध करना) ग्लोब पैटर्न के साथ। कुशल फ़ाइल सिस्टम ऑपरेशन के लिए CLI टूल। बिना किसी निर्भरता के।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
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
  origin_path: "system/tools/batch_file_ops.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6fd8057d502337926d541fe4b66208c94e661e7d8c83fe0a4847094e90c5e024
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.937989+00:00"
---
<img src="banner.png" width="100%" alt="batch-file-ops banner">

# batch_file_ops - बैच फ़ाइल ऑपरेशन

ग्लोब पैटर्न के साथ फ़ाइलों पर कुशल बैच ऑपरेशन के लिए CLI टूल।
समर्थित: delete, move, copy, list। शून्य निर्भरताएँ (केवल Python stdlib)।

---

## क्रियाएँ

| क्रिया | विवरण |
|--------|-------------|
| `delete` | पैटर्न के अनुसार फ़ाइलें हटाएँ |
| `move` | पैटर्न के अनुसार फ़ाइलें स्थानांतरित करें |
| `copy` | पैटर्न के अनुसार फ़ाइलें कॉपी करें |
| `list` | पैटर्न के अनुसार फ़ाइलें सूचीबद्ध करें |

## CLI उपयोग

```bash
python batch_file_ops.py <aktion> <quelle> [<ziel>] --pattern "<glob>" [--dry-run] [--recursive]
```

### आर्गुमेंट

| आर्गुमेंट | विवरण |
|----------|-------------|
| `aktion` | `delete`, `move`, `copy` या `list` |
| `quelle` | स्रोत फ़ोल्डर |
| `ziel` | गंतव्य फ़ोल्डर (केवल `move` और `copy` के लिए) |
| `--pattern`, `-p` | ग्लोब पैटर्न (जैसे `*.py`, `TOOLS_*.py`) - डिफ़ॉल्ट: `*` |
| `--dry-run`, `-n` | केवल दिखाएँ, कुछ न बदलें |
| `--recursive`, `-r` | उप-फ़ोल्डरों में पुनरावृत्त रूप से खोजें |

---

## उदाहरण

```bash
# Alle Python-Dateien in einem Ordner auflisten
python batch_file_ops.py list /pfad/zum/ordner --pattern "*.py"

# Alle .tmp Dateien loeschen (erst Dry-Run!)
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp"

# Dateien verschieben
python batch_file_ops.py move /quelle /ziel --pattern "*.txt"

# Dateien kopieren (rekursiv)
python batch_file_ops.py copy /quelle /ziel --pattern "*.md" --recursive

# Pattern-Beispiele
python batch_file_ops.py delete /pfad --pattern "TOOLS_*.py"
python batch_file_ops.py list /pfad --pattern "backup_202?-*"
```

---

## टिप्पणियाँ

- **पहले ड्राई-रन:** `delete` और `move` के साथ हमेशा पहले `--dry-run` का उपयोग करें
- **ग्लोब पैटर्न:** Python `pathlib.glob()` / `pathlib.rglob()` का उपयोग करता है
- **Windows-संगत:** स्वचालित UTF-8 आउटपुट एन्कोडिंग
- **केवल फ़ाइलें:** फ़ोल्डर छोड़ दिए जाते हैं (केवल फ़ाइलों पर कार्रवाई होती है)
