---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "إصلاح ترميز Mojibake لنص UTF-8 المرمّز مرتين أو ثلاث مرات. يصلح سوء تفسير Windows cp1252/Latin-1. بدون تبعيات."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: ar
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
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="encoding-fix banner">

# إصلاح الترميز

يصلح Mojibake (نص UTF-8 مرمّز مرتين أو ثلاث مرات) الناتج عن سوء تفسير cp1252/Latin-1 في Windows.
بدون أي تبعيات — مكتبة Python القياسية فقط.

## المشكلة النموذجية

```
"ue" (U+00FC) → UTF-8 \xc3\xbc → als cp1252 gelesen → "Ã¼"
```

## الاستخدام

### كمكتبة
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # → "Würge"
```

### مخرجات العملية الفرعية
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### سطر الأوامر
```bash
python encoding_fix.py "WÃ¼rge"    # Einzelnen String prüfen
python encoding_fix.py              # Selbst-Test
```

## الميزات

- **Idempotent (لا تتغير النتيجة عند التكرار):** لا يتم تعديل النص المرمّز بشكل صحيح
- **حتى 3 جولات:** يصلح حتى السلاسل المرمّزة ثلاث مرات
- **مفكك ترميز العمليات الفرعية:** بديل UTF-8/cp1252 لمخرجات العملية
- **بدون تبعيات:** مكتبة Python القياسية فقط

## سجل التغييرات

### 1.0.0 (2026-03-12)
- منقول من BACH system/tools/encoding_fix.py
