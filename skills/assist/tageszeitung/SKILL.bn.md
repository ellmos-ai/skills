---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "RSS ফিড এবং ওয়েব উৎস থেকে একটি ব্যক্তিগতকৃত দৈনিক সংবাদপত্র তৈরি করে। BACH news system (news.py + newspaper_generator.py) থেকে পোর্ট করা। নিজস্ব SQLite store (কোনো Origin-DB নেই)। feedparser ঐচ্ছিক — stdlib দিয়ে XML fallback। Edge Headless (msedge.exe) দিয়ে PDF export।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: bn
status: stable
visibility: public
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
translated_from_sha256: e42d847ea203fa764315a96678ddf6b5814633dd363b9ee8f9fbf87a4af5cce8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="tageszeitung banner">

## উদ্দেশ্য

কনফিগার করা RSS ফিড ও ওয়েব উৎস থেকে নিবন্ধ সংগ্রহ করা, বিভাগ অনুযায়ী সাজানো এবং HTML/PDF আকারে একটি দৈনিক সংবাদপত্র হিসেবে রেন্ডার করা। নিবন্ধগুলি স্থানীয়ভাবে `tageszeitung/store.db`-এ সংরক্ষিত হয় এবং পঠিত হিসেবে চিহ্নিত করা হয়।

---

## ট্রিগার

| বাক্যাংশ | কার্যক্রম |
|---|---|
| „Erstell meine Tageszeitung" / „আমার দৈনিক সংবাদপত্র তৈরি করো" | নিবন্ধ সংগ্রহ + PDF রেন্ডার |
| „Tageszeitung für heute" / „আজকের সংবাদপত্র দেখাও" | আজকের সংবাদপত্র রেন্ডার |
| „Füge Feed hinzu [URL]" / „ফিড যোগ করো [URL]" | RSS উৎস নিবন্ধন |
| „Zeig meine Quellen" / „আমার উৎসগুলো দেখাও" | উৎসের তালিকা প্রদর্শন |
| „Fetch News" / „সংবাদ সংগ্রহ করো" | সমস্ত উৎস সংগ্রহ (রেন্ডার ছাড়া) |

---

## কর্মপ্রবাহ

1. **উৎস পরীক্ষা**: `news_sources` থেকে সমস্ত সক্রিয় উৎস পড়া।
2. **Fetch**: RSS-এর জন্য feedparser (বা xml.etree fallback), ওয়েবের জন্য urllib।
3. **ডুপ্লিকেট অপসারণ**: UNIQUE(source_id, url) ডুপ্লিকেট রোধ করে।
4. **Render**: অপঠিত নিবন্ধগুলি বিভাগ অনুযায়ী গোষ্ঠীভুক্ত করা → HTML → PDF।
5. **সরবরাহ**: HTML/PDF আউটপুট ফোল্ডারে রাখা (কনফিগারযোগ্য পথ)।

---

## CLI প্রবেশপথ

```bash
# Quelle hinzufügen
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Alle Quellen abrufen
python tageszeitung_core.py fetch

# Tageszeitung rendern (HTML + PDF wenn Edge verfügbar)
python tageszeitung_core.py render [--date 2026-06-22] [--out /pfad/]

# Quellen auflisten
python tageszeitung_core.py sources

# Ungelesene Artikel
python tageszeitung_core.py items [--limit 50] [--category tech]

# Artikel als gelesen markieren
python tageszeitung_core.py read <item_id>

# Alternativer Store (z.B. für Tests)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Store

| বৈশিষ্ট্য | মান |
|---|---|
| ধরন | SQLite |
| পথ (ডিফল্ট) | `skills/assist/tageszeitung/store.db` |
| Override | `--store <pfad>` বা Env `TAGESZEITUNG_STORE` |
| টেবিল | `news_sources`, `news_items` |

### স্কিমা (BACH news.py থেকে পোর্ট করা)

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## নীতি

- feedparser অগ্রাধিকার পায়; feedparser ছাড়া সরল RSS 2.0 ফিডের জন্য একটি xml.etree fallback কাজ করে।
- PDF তৈরির জন্য সিস্টেম PATH-এ `msedge.exe` বা `MSEDGE_PATH` Env প্রয়োজন। Edge ছাড়া শুধু HTML রেন্ডার হয়।
- প্রতি বিভাগে সর্বোচ্চ নিবন্ধ: `assist/prefs.json` দিয়ে কনফিগারযোগ্য (`tageszeitung_max_per_category`, ডিফল্ট: 5)।

---

## গোপনীয়তা

- নিবন্ধের বিষয়বস্তু স্থানীয়ভাবে `store.db`-এ থাকে।
- কোনো বহিরাগত বিশ্লেষণ সেবা নেই — শুধু কনফিগার করা RSS/ওয়েব উৎসগুলিতে অনুরোধ পাঠানো হয়।

---

## সংশ্লিষ্ট সম্পদ

- BACH `hub/news.py` — Origin (শুধু-পঠন)
- BACH `hub/_services/newspaper/newspaper_generator.py` — Origin (শুধু-পঠন)

---

## পরিবর্তনের ইতিহাস

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 0.1.0 | 2026-06-22 | প্রথম সংস্করণ — BACH স্কিমা পোর্ট, নিজস্ব store, feedparser ঐচ্ছিক |
