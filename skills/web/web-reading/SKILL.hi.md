---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: "वेब सामग्री पढ़ने और निकालने के लिए राउटर और प्रोटोकॉल। पहले तय करता है कि किसकी आवश्यकता है (मुख्य पाठ बनाम संरचना बनाम स्क्रीनशॉट) और फिर सिस्टम पर कौन-सा उपलब्ध टूल उसे प्रदान करता है। यदि कोई उपयुक्त चीज़ मौजूद नहीं है, तो यह web-scraper मॉड्यूल इंस्टॉल करने की सलाह देता है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
translated_from_sha256: 13dd3196759f5a7bb4beca61b933139ae31924c478b553bcd9d91e2c2d6049bf
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="web-reading banner">

# वेबसाइट पढ़ना (राउटर)

## उद्देश्य

वेब सामग्री प्राप्त करना और उसे संसाधित करना — लेकिन बिना सोचे-समझे कोई टूल न चुनना।
यह स्किल रूट करता है: **पहले उद्देश्य, फिर सबसे अच्छा उपलब्ध टूल।**
वास्तविक कार्यान्वयन **`web-scraper`-मॉड्यूल** में रहता है; यह स्किल केवल दिखाती है कि अभी क्या उपलब्ध है और उसका उपयोग कैसे करें।

## चरण 1 — क्या चाहिए?

```
Webseite verarbeiten?
  |
  +-- Haupttext (Artikel/Fließtext) → "Content"      → Schritt 2A
  +-- Links / Formulare / Headers   → "Struktur"     → Schritt 2B
  +-- Gerendertes Bild der Seite    → "Screenshot"   → Schritt 2C
```


## चरण 2 — कौन-सा टूल? (राउटर)

संबंधित सूची में **पहला उपलब्ध** टूल लें। "उपलब्ध" का अर्थ है: टूल/स्किल/मॉड्यूल इस सत्र में वास्तव में मौजूद है।

### 2A — सामग्री (मुख्य पाठ, साफ़ Markdown)

| प्राथमिकता | टूल | उपलब्ध, यदि … | उपयोग |
|---|---|---|---|
| 1 | **`defuddle`**-स्किल | स्किल `defuddle` सूचीबद्ध है | सामान्य वेबपेजों से साफ़ Markdown |
| 2 | अंतर्निर्मित **`WebFetch`** | एजेंट के पास WebFetch-टूल है | किसी URL को तेज़ी से पढ़ना/सारांश बनाना |
| 3 | **`fc_web_fetch`** (MCP) | FileCommander-MCP लोड है | `mode: "extract"` |
| 4 | **`web-scraper`**-मॉड्यूल | मॉड्यूल इंस्टॉल/आयात योग्य है | `web-scraper extract <url>` या `extract(url)` |

> नोट: `.md`-URL पहले से Markdown हैं → सीधे `WebFetch`, कोई extractor नहीं।

### 2B — संरचना (लिंक, फ़ॉर्म, हेडर)

यहाँ `WebFetch`/`defuddle` **उपयुक्त नहीं** हैं (वे संसाधित पाठ देते हैं, कच्ची संरचना नहीं)। इसलिए लें:

| प्राथमिकता | टूल | उपलब्ध, यदि … | उपयोग |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | FileCommander-MCP लोड है | `mode: "links" \| "forms" \| "headers"` |
| 2 | **`web-scraper`**-मॉड्यूल | मॉड्यूल इंस्टॉल/आयात योग्य है | `web-scraper links\|forms\|headers <url>` |

### 2C — स्क्रीनशॉट

| प्राथमिकता | टूल | उपलब्ध, यदि … | उपयोग |
|---|---|---|---|
| 1 | **`web-scraper`**-मॉड्यूल | `[screenshot]`-Extra वाला मॉड्यूल | `web-scraper screenshot <url> --out bild.png` |
| 2 | ब्राउज़र-ऑटोमेशन टूल | उदा. Playwright/Computer-Use उपलब्ध | पेज-निर्भर |

## चरण 3 — फ़ॉलबैक: कुछ उपयुक्त नहीं मिला?

यदि उद्देश्य के लिए **कोई** टूल उपलब्ध नहीं है, तो **`web-scraper`-मॉड्यूल** इंस्टॉल करने की सलाह दें (पूर्ण रूप से: get/links/forms/headers/extract/screenshot):

```bash
# aus dem lokalen Modulordner (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] für Screenshots

# danach:
web-scraper extract <url>
```


लाइब्रेरी के रूप में:

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```


## आपातकालीन उपाय — स्टैंडअलोन स्निपेट (बिना किसी चीज़ के)

यदि वास्तव में केवल मानक लाइब्रेरी + `requests`/`bs4` उपलब्ध हैं:

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


## Changelog

### 1.1.0 (2026-07-05)
- शुद्ध प्रोटोकॉल से **राउटर** में बदलाव: मौजूदा वेब-क्षमताओं (`defuddle`, `WebFetch`, `fc_web_fetch`, `web-scraper`-मॉड्यूल) को पहचानता है और उद्देश्य (सामग्री/संरचना/स्क्रीनशॉट) के अनुसार रूट करता है; अन्यथा `web-scraper`-मॉड्यूल की सलाह देता है।
- नाम को `web-reading` पर एकीकृत किया गया (पहले DE `webseiten-lesen`)।
- मुख्य भाग से BACH-CLI उदाहरण हटाए गए (स्टैंडअलोन-अनुरूप; मूल जानकारी `bach_integration`-Frontmatter में दर्ज है)।

### 1.0.0 (2026-03-12)
- BACH v3.8.0 Workflow `webseiten-lesen.md` से निर्यात
