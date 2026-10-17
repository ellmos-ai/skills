---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: "ওয়েব কন্টেন্ট পড়া ও নিষ্কাশনের জন্য রাউটার ও প্রোটোকল। প্রথমে নির্ধারণ করে কী প্রয়োজন (মূল পাঠ্য বনাম কাঠামো বনাম স্ক্রিনশট), তারপর সিস্টেমে উপলব্ধ কোন টুল তা সরবরাহ করতে পারে। উপযুক্ত কিছু না থাকলে web-scraper মডিউল ইনস্টল করার পরামর্শ দেয়।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
translated_from_sha256: 13dd3196759f5a7bb4beca61b933139ae31924c478b553bcd9d91e2c2d6049bf
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.189937+00:00"
---
<img src="banner.png" width="100%" alt="web-reading banner">

# ওয়েবপেজ পড়া (রাউটার)

## উদ্দেশ্য

ওয়েব কন্টেন্ট আনা ও প্রক্রিয়া করা — তবে অন্ধভাবে কোনো টুল বেছে নেওয়া নয়।
এই স্কিল রাউট করে: **প্রথমে উদ্দেশ্য, তারপর সেরা উপলব্ধ টুল।**
আসল বাস্তবায়ন থাকে **`web-scraper`-মডিউলে**; এই স্কিল শুধু দেখায় এখন কী আছে এবং কীভাবে ব্যবহার করতে হয়।

## ধাপ ১ — কী প্রয়োজন?

```
Webseite verarbeiten?
  |
  +-- Haupttext (Artikel/Fließtext) → "Content"      → Schritt 2A
  +-- Links / Formulare / Headers   → "Struktur"     → Schritt 2B
  +-- Gerendertes Bild der Seite    → "Screenshot"   → Schritt 2C
```

## ধাপ ২ — কোন টুল? (রাউটার)

প্রতিটি তালিকায় **প্রথম উপলব্ধ** টুলটি নিন। "উপলব্ধ" মানে: টুল/স্কিল/মডিউলটি এই সেশনে সত্যিই বিদ্যমান।

### 2A — কন্টেন্ট (মূল পাঠ্য, পরিষ্কার Markdown)

| অগ্রাধিকার | টুল | উপলব্ধ, যখন … | ব্যবহার |
|---|---|---|---|
| 1 | **`defuddle`**-স্কিল | স্কিল `defuddle` তালিকাভুক্ত | সাধারণ ওয়েবপেজ থেকে পরিষ্কার Markdown |
| 2 | Built-in **`WebFetch`** | এজেন্টের কাছে WebFetch-টুল আছে | একটি URL দ্রুত পড়া/সারসংক্ষেপ |
| 3 | **`fc_web_fetch`** (MCP) | FileCommander-MCP লোড করা | `mode: "extract"` |
| 4 | **`web-scraper`**-মডিউল | মডিউল ইনস্টল/ইমপোর্টযোগ্য | `web-scraper extract <url>` বা `extract(url)` |

> মন্তব্য: `.md`-URL ইতিমধ্যে Markdown → সরাসরি `WebFetch`, কোনো extractor নয়।

### 2B — কাঠামো (লিংক, ফর্ম, হেডার)

এখানে `WebFetch`/`defuddle` **উপযুক্ত নয়** (এগুলো প্রক্রিয়াকৃত পাঠ্য দেয়, কাঁচা কাঠামো নয়)। তাই নিন:

| অগ্রাধিকার | টুল | উপলব্ধ, যখন … | ব্যবহার |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | FileCommander-MCP লোড করা | `mode: "links" \| "forms" \| "headers"` |
| 2 | **`web-scraper`**-মডিউল | মডিউল ইনস্টল/ইমপোর্টযোগ্য | `web-scraper links\|forms\|headers <url>` |

### 2C — স্ক্রিনশট

| অগ্রাধিকার | টুল | উপলব্ধ, যখন … | ব্যবহার |
|---|---|---|---|
| 1 | **`web-scraper`**-মডিউল | `[screenshot]`-Extra সহ মডিউল | `web-scraper screenshot <url> --out bild.png` |
| 2 | Browser-Automations-Tool | যেমন Playwright/Computer-Use আছে | পেজ-নির্ভর |

## ধাপ ৩ — ফলব্যাক: উপযুক্ত কিছু পাওয়া না গেলে?

উদ্দেশ্যের জন্য **কোনো** টুল উপলব্ধ না থাকলে **`web-scraper`-মডিউল** ইনস্টল করার পরামর্শ দিন (পূর্ণাঙ্গ: get/links/forms/headers/extract/screenshot):

```bash
# aus dem lokalen Modulordner (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] für Screenshots

# danach:
web-scraper extract <url>
```

লাইব্রেরি হিসেবে:

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## শেষ অবলম্বন — স্ট্যান্ডএলোন স্নিপেট (কিছু ছাড়াই)

যদি শুধু স্ট্যান্ডার্ড লাইব্রেরি + `requests`/`bs4` থাকে:

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Einfache Content-Extraktion."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)
```

## চেঞ্জলগ

### 1.1.0 (2026-07-05)
- বিশুদ্ধ প্রোটোকল থেকে **রাউটারে** রূপান্তর: বিদ্যমান ওয়েব-সক্ষমতা শনাক্ত করে
  (`defuddle`, `WebFetch`, `fc_web_fetch`, `web-scraper`-মডিউল) এবং উদ্দেশ্য অনুযায়ী রাউট করে
  (কন্টেন্ট/কাঠামো/স্ক্রিনশট); অন্যথায় `web-scraper`-মডিউল সুপারিশ করে।
- নাম `web-reading`-এ একীভূত (আগে DE `webseiten-lesen`)।
- BACH-CLI-উদাহরণ মূল অংশ থেকে সরানো হয়েছে (স্ট্যান্ডএলোন-সামঞ্জস্যপূর্ণ; উৎস
  `bach_integration`-ফ্রন্টম্যাটারে নথিভুক্ত থাকে)।

### 1.0.0 (2026-03-12)
- BACH v3.8.0 ওয়ার্কফ্লো `webseiten-lesen.md` থেকে এক্সপোর্ট
