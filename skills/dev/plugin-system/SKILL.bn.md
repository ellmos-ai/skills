---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "Python অ্যাপ্লিকেশনের জন্য সাধারণ প্লাগইন সিস্টেম। স্বয়ংক্রিয় আবিষ্কার, যাচাইকরণ, ত্রুটি-সহনশীলতা। কোনো বাহ্যিক নির্ভরতা নেই (শুধুমাত্র Python stdlib)।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: a2fea4a34859b7d2e08c4205a368e948ecacdb744e6d80b5d0246271076f3c70
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:53.391636+00:00"
---
<img src="banner.png" width="100%" alt="plugin-system banner">

# প্লাগইন সিস্টেম

Python CLI অ্যাপ্লিকেশনের জন্য ত্রুটি-সহনশীল প্লাগইন সিস্টেম।
একটি ত্রুটিপূর্ণ প্লাগইন কখনোই অ্যাপ্লিকেশনের বাকি অংশ থামিয়ে দেয় না।

## মূল বৈশিষ্ট্যসমূহ

- **স্বয়ংক্রিয় আবিষ্কার:** একটি ডিরেক্টরিতে স্বয়ংক্রিয়ভাবে প্লাগইন খুঁজে বের করে
- **যাচাইকরণ:** প্রতিটি প্লাগইন ক্লাসে `name`, `version`, `execute()` পরীক্ষা করে
- **ত্রুটি-সহনশীলতা:** ত্রুটিপূর্ণ প্লাগইন লগ করা হয় কিন্তু লোড করা হয় না
- **কোনো নির্ভরতা নেই:** শুধুমাত্র Python স্ট্যান্ডার্ড লাইব্রেরি

## ফাইলসমূহ

```
scripts/
  plugin_system.py       Kern: PluginBase (ABC) + PluginManager
  cli_demo.py            Demo-CLI mit argparse
  test_plugin_system.py  16+ Unit-Tests
examples/
  hello.py               Hello-World Plugin
  calculator.py          Rechner-Plugin
  systeminfo.py          System-Info Plugin
```

## দ্রুত শুরু

### ১. প্লাগইন তৈরি করুন

```python
from plugin_system import PluginBase

class MeinPlugin(PluginBase):
    name = "MeinPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hallo!"}
```

### ২. PluginManager ব্যবহার করুন

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./meine_plugins")
plugins = manager.discover_plugins()

# Alle Plugins auflisten
manager.list_plugins()

# Plugin ausfuehren
success, result = manager.execute_plugin("MeinPlugin", param="wert")
if success:
    print(result)
```

### ৩. নিজের অ্যাপে সংহত করুন

```python
class MeineApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## প্লাগইন ইন্টারফেস

প্রতিটি প্লাগইনকে অবশ্যই:

| প্রয়োজনীয়তা | বিবরণ |
|-------------|---------|
| `PluginBase` উত্তরাধিকারসূত্রে নিতে হবে | `from plugin_system import PluginBase` |
| `name` সেট করতে হবে | ক্লাস অ্যাট্রিবিউট, খালি নয় |
| `version` সেট করতে হবে | ক্লাস অ্যাট্রিবিউট, Semantic Versioning |
| `execute()` বাস্তবায়ন করতে হবে | যেকোনো `*args, **kwargs` |

## ত্রুটি-সহনশীলতা

| ত্রুটির ধরন | আচরণ |
|-----------|-----------|
| প্লাগইনে SyntaxError | প্লাগইন এড়িয়ে যাওয়া হয়, বাকিগুলো লোড হয় |
| অনুপস্থিত অ্যাট্রিবিউট | প্লাগইনটিকে `is_valid=False` হিসেবে চিহ্নিত করা হয় |
| `execute()`-এ ব্যতিক্রম | `(False, error_message)` ফেরত দেয় |
| ডিরেক্টরিতে কোনো প্লাগইন নেই | খালি তালিকা, কোনো ক্রাশ নেই |

## পরিবর্তনের ইতিহাস

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/plugins থেকে Skillbibliothek-এ স্থানান্তর
- PluginBase ABC + PluginManager
- ৩টি উদাহরণ প্লাগইন (Hello, Calculator, SystemInfo)
- ১৬+ ইউনিট টেস্ট
- argparse সহ CLI ডেমো
