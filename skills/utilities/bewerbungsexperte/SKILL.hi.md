---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: "संपूर्ण नौकरी-आवेदन प्रक्रिया के लिए विशेषज्ञ। नौकरी के विज्ञापनों का विश्लेषण करता है, प्रोफ़ाइलों (LinkedIn/CV) को अनुकूलित करता है और अनुरूप कवर लेटर तैयार करता है। SQLite-डेटाबेस और फ़ोल्डर संरचना से ASCII-रेज़्यूमे तैयार करता है। cv_generator.py स्टैंडअलोन पोर्ट किया गया है -- किसी BACH-रनटाइम की आवश्यकता नहीं।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: hi
status: active
visibility: public
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
translated_from_sha256: c71218b5c90eba7666db1a407dc59752fa0e2eccd342deb8b728fba82d967e54
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="bewerbungsexperte banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **English Translation** — Official English version of `bewerbungsexperte`.

# BEWERBUNGSEXPERTE v1.1 (Deutsch)

> आपके अगले करियर चरण के लिए आपका रणनीतिक साथी।

## सक्रियण

```bash
# Beispiel-CV ohne Datenbankzugriff (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# CV aus SQLite-Datenbank generieren (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# CV in Datei speichern (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# Mit Ordner-Scan (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```


## सेवा-सूची

### 1. CV-निर्माण (`cv_generator.py`)
- **व्यक्तिगत डेटा:** `assistant_user_profile`-तालिका से पढ़ें (key/value)
- **कार्य-अनुभव:** नियोक्ता-फ़ोल्डर स्कैन करें (कार्य-प्रमाणपत्र, अनुबंध)
- **शिक्षा:** शैक्षणिक योग्यता-फ़ोल्डर स्कैन करें
- **प्रशिक्षण:** प्रमाणपत्र-फ़ोल्डर स्कैन करें
- **संदर्भ:** `contacts`-तालिका से (category='beruflich')
- **Dry-Run:** डेटाबेस के बिना -- परीक्षण के लिए उदाहरण डेटा

### 2. पद-निदान
- **कीवर्ड-मिलान:** CV और जॉब-आवश्यकताओं का मिलान (ATS-Safe)
- **कंपनी-जाँच:** कंपनी-संस्कृति और लाभों पर शोध

### 3. दस्तावेज़-सेवा
- **CV-ट्यूनिंग:** अनुभवों की संरचना और प्रभावी प्रस्तुति
- **कवर लेटर:** व्यक्तिगत और प्रभावशाली पत्रों का निर्माण
- **पोर्टफ़ोलियो:** कार्य-नमूनों और संदर्भों पर परामर्श

## डेटाबेस-तालिकाएँ (वैकल्पिक)

`cv_generator.py` उपलब्ध होने पर इन तालिकाओं से पढ़ता है:

- `assistant_user_profile` (key TEXT, value TEXT) — व्यक्तिगत डेटा
  - फ़ील्ड: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — संदर्भ

अनुपलब्ध तालिकाएँ अनदेखी की जाती हैं (CV में खाली अनुभाग)।

## फ़ोल्डर-संरचना (--career-path आदि के लिए)

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```


## CLI-विकल्प

```
--db <pfad>           Pfad zur SQLite-Datenbank (Pflicht ohne --dry-run)
--output, -o          Ausgabedatei (ansonsten stdout)
--career-path         Pfad zum Arbeitgeber-Ordner
--education-path      Pfad zum Abschluesse-Ordner
--certs-path          Pfad zum Fortbildungen-Ordner
--dry-run             Beispiel-CV ohne Datenbankzugriff
```


## कार्यप्रवाह: CV-निर्माण

1. **तैयारी**
   - SQLite-DB उपलब्ध कराएँ (BACH-DB या अपनी)
   - दस्तावेज़ों के साथ फ़ोल्डर-संरचना बनाएँ (वैकल्पिक)

2. **बिना DB परीक्षण**
   - `python cv_generator.py --dry-run` -- जाँचता है कि टूल काम करता है या नहीं

3. **निर्माण**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - आउटपुट जाँचें और आवश्यकतानुसार समायोजित करें

4. **निर्यात**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## निर्भरताएँ

केवल Python-Stdlib: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`।
कोई pip-इंस्टॉल आवश्यक नहीं, कोई BACH-रनटाइम-इंपोर्ट नहीं।

## परिवर्तन-लॉग

### 1.1.0 (2026-06-22)
- BACH v1.0.0 से स्टैंडअलोन पोर्ट किया गया
- हार्डकोडेड Origin-DB-पथ के स्थान पर `--db <pfad>`
- `--dry-run`-मोड जोड़ा गया
- `--scan-folders` हटाया गया (BACH user_data_folders-तालिका की आवश्यकता थी)
- फ़ूटर टेक्स्ट तटस्थ किया गया
- BACH-रनटाइम-स्वतंत्रता सत्यापित

### 1.0.0 (2026-01-25, BACH-intern)
- BACH system/agents/_experts/bewerbungsexperte/ में प्रारंभिक संस्करण

---
स्थिति: सक्रिय
डोमेन: करियर परामर्श
