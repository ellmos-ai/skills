---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "RSS फ़ीड और वेब स्रोतों से एक वैयक्तिकृत दैनिक समाचारपत्र बनाता है। BACH समाचार प्रणाली (news.py + newspaper_generator.py) से पोर्ट किया गया। अपना SQLite स्टोर (कोई Origin-DB नहीं)। feedparser वैकल्पिक है — stdlib के माध्यम से XML फ़ॉलबैक। Edge Headless (msedge.exe) के माध्यम से PDF निर्यात।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: hi
status: stable
visibility: public
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
translated_from_sha256: e42d847ea203fa764315a96678ddf6b5814633dd363b9ee8f9fbf87a4af5cce8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.759405+00:00"
---
<img src="banner.png" width="100%" alt="tageszeitung banner">

## उद्देश्य

कॉन्फ़िगर किए गए RSS फ़ीड और वेब स्रोतों से लेख प्राप्त करना, श्रेणियों के अनुसार क्रमबद्ध करना और HTML/PDF दैनिक समाचारपत्र के रूप में प्रस्तुत करना। लेख स्थानीय रूप से `tageszeitung/store.db` में संग्रहीत होते हैं और पढ़े हुए के रूप में चिह्नित किए जाते हैं।

---

## ट्रिगर

| वाक्यांश | क्रिया |
|---|---|
| „मेरा दैनिक समाचारपत्र बनाओ" | लेख प्राप्त करना + PDF प्रस्तुत करना |
| „आज का दैनिक समाचारपत्र" | आज का समाचारपत्र प्रस्तुत करना |
| „फ़ीड जोड़ो [URL]" | RSS स्रोत पंजीकृत करना |
| „मेरे स्रोत दिखाओ" | स्रोतों की सूची आउटपुट करना |
| „समाचार लाओ" | सभी स्रोत प्राप्त करना (कोई प्रस्तुति नहीं) |

---

## कार्यप्रवाह

1. **स्रोत जाँचें**: `news_sources` से सभी सक्रिय स्रोत पढ़ें।
2. **प्राप्त करना**: RSS feedparser के माध्यम से (या xml.etree फ़ॉलबैक), वेब urllib के माध्यम से।
3. **डुप्लिकेट हटाना**: UNIQUE(source_id, url) डुप्लिकेट को रोकता है।
4. **प्रस्तुति**: न पढ़े गए लेखों को श्रेणी के अनुसार समूहित करें → HTML → PDF।
5. **वितरण**: HTML/PDF को आउटपुट फ़ोल्डर में रखें (कॉन्फ़िगर करने योग्य पथ)।

---

## CLI प्रवेश

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

## स्टोर

| गुण | मान |
|---|---|
| प्रकार | SQLite |
| पथ (डिफ़ॉल्ट) | `skills/assist/tageszeitung/store.db` |
| ओवरराइड | `--store <pfad>` या Env `TAGESZEITUNG_STORE` |
| तालिकाएँ | `news_sources`, `news_items` |

### स्कीमा (BACH news.py से पोर्ट किया गया)

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

## दृष्टिकोण

- feedparser को प्राथमिकता दी जाती है; feedparser के बिना सरल RSS 2.0 फ़ीड के लिए xml.etree फ़ॉलबैक काम करता है।
- PDF निर्माण के लिए सिस्टम PATH में `msedge.exe` या `MSEDGE_PATH` Env आवश्यक है। Edge के बिना केवल HTML प्रस्तुत होता है।
- प्रति श्रेणी अधिकतम लेख: `assist/prefs.json` के माध्यम से कॉन्फ़िगर करने योग्य (`tageszeitung_max_per_category`, डिफ़ॉल्ट: 5)।

---

## गोपनीयता

- लेख की सामग्री `store.db` में स्थानीय रहती है।
- कोई बाहरी विश्लेषण सेवा नहीं — केवल कॉन्फ़िगर किए गए RSS/वेब स्रोतों को कॉल किया जाता है।

---

## संबंधित संसाधन

- BACH `hub/news.py` — Origin (केवल-पठन)
- BACH `hub/_services/newspaper/newspaper_generator.py` — Origin (केवल-पठन)

---

## परिवर्तन लॉग

| संस्करण | दिनांक | परिवर्तन |
|---|---|---|
| 0.1.0 | 2026-06-22 | प्रारंभिक निर्माण — BACH स्कीमा पोर्ट किया गया, अपना स्टोर, feedparser वैकल्पिक |
