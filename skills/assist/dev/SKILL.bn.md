---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "ডেভেলপার সহায়ক (ATI-এর উত্তরসূরি)। হেডলেস স্ক্যানের মাধ্যমে প্রকল্পের দ্রুত সারসংক্ষেপ দেয় এবং উপলব্ধ কোডিং টুলগুলোতে রাউট করে: CodeCommander MCP (বিশ্লেষণ/রিফ্যাক্টর/ডায়াগনোজ) এবং ellmos-code-tools মডিউল। শুধুমাত্র টুল রাউটিং ও স্ক্যান, নিজস্ব কোনো স্টোর নেই।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: bn
status: active
visibility: public
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e0c349589cfe3b0cf418f3deb24b7fb097d45ef52358ad19a4958a96d7f5a0ef
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:32:12.965503+00:00"
---
<img src="banner.png" width="100%" alt="dev banner">

# Dev — ডেভেলপার সহায়ক (ATI)

প্রকল্পের একটি সারসংক্ষেপ দেয়, তারপর সঠিক টুলগুলোর কাছে হস্তান্তর করে।

## উদ্দেশ্য

BACH-এর ATI/entwickler-এজেন্টের উত্তরসূরি। দুটি কাজ:
1. **প্রকল্প স্ক্যান** (হেডলেস, stdlib): ব্যয়বহুল বিশ্লেষণ চালানোর আগে কোনো প্রকল্পের কাঠামো, ভাষা ও বিল্ড মার্কারের একটি দ্রুত, টোকেন-সাশ্রয়ী সারসংক্ষেপ।
2. **টুল রাউটিং:** নিজস্ব টুল পুনরাবৃত্তি না করে বিদ্যমান কোডিং টুলগুলোতে পাঠায়।

## ট্রিগার

| ব্যবহারকারীর ইনপুট | কার্যক্রম |
|---|---|
| „প্রকল্প X সম্পর্কে একটি সারসংক্ষেপ দাও" | `dev_core.py scan <pfad>` |
| „এটি কী ধরনের প্রকল্প / কোন স্ট্যাক?" | `dev_core.py scan <pfad>` |
| „এই ফাইলটি বিশ্লেষণ করো / রিফ্যাক্টর করো" | → CodeCommander-MCP |
| „Python কোড তৈরি/যাচাই করো" | → CodeCommander-MCP / ellmos-code-tools |

## টুল পরিমণ্ডল (রাউটিং লক্ষ্য)

- **CodeCommander-MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`,
  `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`,
  `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation` ইত্যাদি।
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): CLI ডেভটুল (Structural-Edit,
  pycutter-কনটেক্সট, Method-Analyzer)।
- **FileCommander-MCP**: বড় ডিরেক্টরি ট্রি জুড়ে ফাইল/ডিরেক্টরি অপারেশন।

## CLI প্রবেশপথ (dev_core.py)

```bash
python dev_core.py scan .              # aktuelles Projekt
python dev_core.py scan /pfad/projekt  # Struktur + Sprachen + Marker
```

যা শনাক্ত করে: Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go,
Java, Roblox (Rojo), Docker, Git রিপোজিটরি।

## স্টোর

কোনো স্টোর নেই। শুধুমাত্র স্ক্যান ও রাউটিং।

## অবস্থান

আমরা CodeCommander/ellmos-code-tools-কে কোডিং টুল হিসেবে সুপারিশ করি, তবে ব্যবহারকারী চাইলে অন্য টুলগুলো (যেমন ruff/pylint/eslint) গ্রহণে আমরা উন্মুক্ত।

## গোপনীয়তা

- `dev_core.py` শুধুমাত্র ফাইল/ডিরেক্টরির নাম (কাঠামো) পড়ে, কোনো বিষয়বস্তু নয়, কোনো আপলোড নয়।
- যেগুলো এড়িয়ে যাওয়া হয় তার মধ্যে রয়েছে `.git`, `node_modules`, `.venv`, `__pycache__`।

## সম্পর্কিত সম্পদ

- `assist/AGENTS.md` — আমব্রেলা রাউটার
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## পরিবর্তনের ইতিহাস

### 0.1.0 (2026-06-22)
- প্রাথমিক সংস্করণ। ATI/entwickler-এর উত্তরসূরি: হেডলেস প্রকল্প স্ক্যান (stdlib) + CodeCommander-MCP / ellmos-code-tools-এ রাউটিং। ব্যবহারকারী-নিরপেক্ষ, কোনো স্টোর নেই।
