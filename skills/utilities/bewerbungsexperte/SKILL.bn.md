---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: "সম্পূর্ণ আবেদন প্রক্রিয়ার বিশেষজ্ঞ। চাকরির বিজ্ঞপ্তি বিশ্লেষণ করে, প্রোফাইল (LinkedIn/CV) অপ্টিমাইজ করে এবং ব্যক্তিগতকৃত কভার লেটার তৈরি করে। SQLite ডাটাবেস ও ফোল্ডার কাঠামো থেকে ASCII জীবনবৃত্তান্ত তৈরি করে। cv_generator.py স্বতন্ত্রভাবে পোর্ট করা হয়েছে -- কোনো BACH রানটাইমের প্রয়োজন নেই।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: bn
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

> আপনার পরবর্তী ক্যারিয়ার পদক্ষেপের জন্য কৌশলগত অংশীদার।

## সক্রিয়করণ

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


## সেবা তালিকা

### 1. CV-জেনারেশন (`cv_generator.py`)
- **ব্যক্তিগত তথ্য:** `assistant_user_profile`-টেবিল থেকে পড়া (key/value)
- **কর্মঅভিজ্ঞতা:** নিয়োগকর্তা-ফোল্ডার স্ক্যান (কর্মসনদ/রেফারেন্স পত্র, চুক্তি)
- **শিক্ষা:** ডিগ্রি-ফোল্ডার স্ক্যান
- **প্রশিক্ষণ:** সার্টিফিকেট-ফোল্ডার স্ক্যান
- **রেফারেন্স:** `contacts`-টেবিল থেকে (category='beruflich')
- **ড্রাই-রান:** ডাটাবেস ছাড়া -- পরীক্ষার জন্য নমুনা ডেটা

### 2. পদের বিশ্লেষণ
- **কীওয়ার্ড-ম্যাচিং:** CV-র সঙ্গে Job-Requirements-এর মিল (ATS-Safe)
- **প্রতিষ্ঠান-যাচাই:** কোম্পানির সংস্কৃতি ও সুবিধা সম্পর্কে গবেষণা

### 3. নথি-সেবা
- **CV-টিউনিং:** অভিজ্ঞতার গঠন ও তীক্ষ্ণ/জোরালো উপস্থাপন
- **কভার লেটার:** ব্যক্তিগত ও প্রভাবশালী চিঠি তৈরি
- **পোর্টফোলিও:** কাজের নমুনা ও রেফারেন্স সম্পর্কে পরামর্শ

## ডাটাবেস-টেবিল (ঐচ্ছিক)

`cv_generator.py` উপস্থিত থাকলে এই টেবিলগুলো থেকে পড়ে:

- `assistant_user_profile` (key TEXT, value TEXT) — ব্যক্তিগত তথ্য
  - ক্ষেত্রসমূহ: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — রেফারেন্স

অনুপস্থিত টেবিল উপেক্ষা করা হয় (CV-তে খালি বিভাগ)।

## ফোল্ডার কাঠামো (--career-path ইত্যাদির জন্য)

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


## CLI-বিকল্প

```
--db <pfad>           Pfad zur SQLite-Datenbank (Pflicht ohne --dry-run)
--output, -o          Ausgabedatei (ansonsten stdout)
--career-path         Pfad zum Arbeitgeber-Ordner
--education-path      Pfad zum Abschluesse-Ordner
--certs-path          Pfad zum Fortbildungen-Ordner
--dry-run             Beispiel-CV ohne Datenbankzugriff
```


## কর্মপ্রবাহ: CV-জেনারেশন

1. **প্রস্তুতি**
   - SQLite-DB প্রদান করুন (BACH-DB বা নিজস্ব)
   - নথি সহ ফোল্ডার কাঠামো তৈরি করুন (ঐচ্ছিক)

2. **ডাটাবেস ছাড়া পরীক্ষা**
   - `python cv_generator.py --dry-run` -- যাচাই করে টুল কাজ করছে কি না

3. **জেনারেশন**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - আউটপুট যাচাই করুন এবং প্রয়োজনে সমন্বয় করুন

4. **এক্সপোর্ট**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## নির্ভরতা

শুধু Python-Stdlib: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`।
pip-ইনস্টল প্রয়োজন নেই, BACH-রানটাইম-ইমপোর্টও নেই।

## পরিবর্তন-লগ

### 1.1.0 (2026-06-22)
- BACH v1.0.0 থেকে স্বতন্ত্রভাবে পোর্ট করা হয়েছে
- হার্ডকোডেড Origin-DB-পাথের পরিবর্তে `--db <pfad>`
- `--dry-run`-মোড যোগ করা হয়েছে
- `--scan-folders` সরানো হয়েছে (BACH user_data_folders-টেবিল প্রয়োজন ছিল)
- ফুটার-টেক্সট নিরপেক্ষ করা হয়েছে
- BACH-রানটাইম-স্বাধীনতা যাচাই করা হয়েছে

### 1.0.0 (2026-01-25, BACH-অভ্যন্তরীণ)
- BACH system/agents/_experts/bewerbungsexperte/-এ প্রাথমিক সংস্করণ

---
Status: AKTIV
Domain: Karriereberatung
