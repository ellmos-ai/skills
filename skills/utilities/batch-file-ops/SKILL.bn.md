---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "ব্যাচ ফাইল অপারেশন (মোছা, সরানো, কপি করা, তালিকাভুক্ত করা) গ্লব প্যাটার্ন ব্যবহার করে। দক্ষ ফাইল সিস্টেম অপারেশনের জন্য CLI টুল। কোনো নির্ভরতা ছাড়াই।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
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
  origin_path: "system/tools/batch_file_ops.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6fd8057d502337926d541fe4b66208c94e661e7d8c83fe0a4847094e90c5e024
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.724989+00:00"
---
<img src="banner.png" width="100%" alt="batch-file-ops banner">

# batch_file_ops - ব্যাচ ফাইল অপারেশন

গ্লব প্যাটার্ন ব্যবহার করে ফাইলের উপর দক্ষ ব্যাচ অপারেশনের জন্য CLI টুল।
সমর্থিত: delete, move, copy, list। শূন্য নির্ভরতা (শুধু Python stdlib)।

---

## অ্যাকশন

| অ্যাকশন | বিবরণ |
|--------|-------------|
| `delete` | প্যাটার্ন অনুযায়ী ফাইল মুছে ফেলা |
| `move` | প্যাটার্ন অনুযায়ী ফাইল সরানো |
| `copy` | প্যাটার্ন অনুযায়ী ফাইল কপি করা |
| `list` | প্যাটার্ন অনুযায়ী ফাইল তালিকাভুক্ত করা |

## CLI ব্যবহার

```bash
python batch_file_ops.py <aktion> <quelle> [<ziel>] --pattern "<glob>" [--dry-run] [--recursive]
```

### আর্গুমেন্ট

| আর্গুমেন্ট | বিবরণ |
|----------|-------------|
| `aktion` | `delete`, `move`, `copy` বা `list` |
| `quelle` | উৎস ফোল্ডার |
| `ziel` | গন্তব্য ফোল্ডার (শুধু `move` এবং `copy` এর জন্য) |
| `--pattern`, `-p` | গ্লব প্যাটার্ন (যেমন `*.py`, `TOOLS_*.py`) - ডিফল্ট: `*` |
| `--dry-run`, `-n` | শুধু দেখানো, কিছু পরিবর্তন না করা |
| `--recursive`, `-r` | উপ-ফোল্ডারে পুনরাবৃত্তভাবে খোঁজা |

---

## উদাহরণ

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

## টীকা

- **প্রথমে ড্রাই-রান:** `delete` এবং `move` এর ক্ষেত্রে সবসময় প্রথমে `--dry-run` ব্যবহার করুন
- **গ্লব প্যাটার্ন:** Python `pathlib.glob()` / `pathlib.rglob()` ব্যবহার করে
- **Windows-সামঞ্জস্যপূর্ণ:** স্বয়ংক্রিয় UTF-8 আউটপুট এনকোডিং
- **শুধু ফাইল:** ফোল্ডার এড়িয়ে যাওয়া হয় (শুধু ফাইল প্রক্রিয়া করা হয়)
