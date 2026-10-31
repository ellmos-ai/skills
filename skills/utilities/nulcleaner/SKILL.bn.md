---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Windows-এ Git Bash-এ /dev/null ব্যবহারের ফলে তৈরি হওয়া Windows-সংরক্ষিত NUL ফাইল খুঁজে বের করে মুছে ফেলে। হেডলেস বা GUI উভয় মোডে।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: bn
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
translated_at: "2026-10-15T11:49:45.996524+00:00"
---
<img src="banner.png" width="100%" alt="nulcleaner banner">

# nulcleaner - Windows NUL-ফাইল পরিষ্কার

## সমস্যা

Git Bash-এ Windows-এ `/dev/null` কমান্ডে ব্যবহার করলে (যেমন `> /dev/null`),
কোনো শূন্যে পুনর্নির্দেশের বদলে বর্তমান ডিরেক্টরিতে একটি প্রকৃত **`nul` নামের ফাইল** তৈরি হয়। Windows "NUL" কে একটি ডিভাইস নাম হিসেবে সংরক্ষিত রাখে, তাই এই ফাইলগুলো সাধারণভাবে মোছা যায় না।

এই টুল সম্প্রসারিত UNC পথ (`\\?\`) ব্যবহার করে এমন NUL ফাইল খুঁজে বের করে মুছে ফেলে।

---

## মোড

| মোড | বিবরণ |
|-------|-------------|
| `scan` | ডিরেক্টরি পুনরাবৃত্তিমূলকভাবে NUL ফাইলের জন্য অনুসন্ধান |
| `delete` | NUL ফাইল খুঁজে বের করে মুছে ফেলা |
| `gui` | ফাইল নির্বাচনসহ গ্রাফিক্যাল ইন্টারফেস |

---

## CLI ব্যবহার

```bash
# Nur scannen (zeigt gefundene NUL-Dateien)
python nulcleaner.py scan /pfad/zum/verzeichnis

# Scannen und loeschen
python nulcleaner.py delete /pfad/zum/verzeichnis

# GUI-Modus starten
python nulcleaner.py gui
```

---

## হেডলেস API (ইন্টিগ্রেশনের জন্য)

এই টুল হেডলেস অপারেশনের জন্য একটি Python API-ও সরবরাহ করে:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/pfad/zum/verzeichnis", verbose=True)
print(f"Gefunden: {result['found']}, Geloescht: {result['deleted']}")
```

**ফেরত মান:** `{'found': int, 'deleted': int, 'errors': list}`

---

## প্রযুক্তিগত বিবরণ

- Windows-সংরক্ষিত ফাইলের নাম মোছার জন্য সম্প্রসারিত UNC পথ (`\\?\`) ব্যবহার করে
- `os.walk()` দিয়ে পুনরাবৃত্তিমূলক স্ক্যান
- tkinter দিয়ে GUI (কোনো বাহ্যিক নির্ভরতা নেই)
- শুধু Windows-এ কাজ করে (সমস্যাটি সেখানেই ঘটে)

---

## প্রতিরোধ

সবচেয়ে ভালো হলো Git Bash-এ `/dev/null` এড়িয়ে চলা। বরং:
- আউটপুট সরাসরি বাদ দিন
- স্ট্যান্ডার্ড এরর পুনর্নির্দেশের জন্য `2>&1` ব্যবহার করুন
- শেল স্ক্রিপ্টে Windows সামঞ্জস্যের দিকে নজর দিন
