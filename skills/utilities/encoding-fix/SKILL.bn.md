---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "ডবল/ট্রিপল এনকোড করা UTF-8-এর জন্য মোজিবেক মেরামত। Windows-cp1252/Latin-1 ভুল ব্যাখ্যা সংশোধন করে। কোনো নির্ভরতা ছাড়াই।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
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
  origin_path: "system/tools/encoding_fix.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c637d841765295aae889df92b106b3dfa66071f13ab32be04e1d1cfe21520d56
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.385229+00:00"
---
<img src="banner.png" width="100%" alt="encoding-fix banner">

# এনকোডিং ফিক্স

Windows cp1252/Latin-1 ভুল ব্যাখ্যার কারণে সৃষ্ট মোজিবেক (ডবল/ট্রিপল এনকোড করা UTF-8) মেরামত করে।
শূন্য নির্ভরতা — শুধুমাত্র Python stdlib।

## সাধারণ সমস্যা

```
"ue" (U+00FC) → UTF-8 \xc3\xbc → als cp1252 gelesen → "Ã¼"
```

## ব্যবহার

### লাইব্রেরি হিসেবে
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # → "Würge"
```

### সাবপ্রসেস আউটপুট
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Einzelnen String prüfen
python encoding_fix.py              # Selbst-Test
```

## বৈশিষ্ট্য

- **ইডেম্পোটেন্ট:** সঠিকভাবে এনকোড করা টেক্সট পরিবর্তিত হয় না
- **সর্বোচ্চ 3 রাউন্ড:** ট্রিপল-এনকোড করা স্ট্রিংও মেরামত করে
- **সাবপ্রসেস ডিকোডার:** প্রসেস আউটপুটের জন্য UTF-8/cp1252 ফলব্যাক
- **শূন্য নির্ভরতা:** শুধুমাত্র Python stdlib

## চেঞ্জলগ

### 1.0.0 (2026-03-12)
- BACH system/tools/encoding_fix.py থেকে পোর্ট করা হয়েছে
