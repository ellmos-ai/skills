---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "স্থানীয়, ব্যক্তিগত মেডিকেল ডেটা সংগ্রহ: রোগ নির্ণয়, উপসর্গের ইতিহাস এবং পরীক্ষার পরিকল্পনা। কোনো BACH উৎস নেই — নিজস্ব SQLite স্টোরসহ কাস্টম ডিজাইন। সম্পূর্ণ স্থানীয়, কোনো ক্লাউড ট্রান্সফার নেই।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: bn
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
translated_from_sha256: b345b47fc6f0ea659604ac06a0d5bda40fadb7770d2f3b2899ce95ccb9ee463c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="medizin-daten banner">

## উদ্দেশ্য

নিজের মেডিকেল ডেটা নিরাপদে ও স্থানীয়ভাবে সংগ্রহ করা: রোগ নির্ণয় (ঐচ্ছিক ICD-10-কোডসহ), তারিখ ধরে উপসর্গের ধারাবাহিক ইতিহাস এবং পরীক্ষার পরিকল্পনা। সব ডেটা শুধুমাত্র `medizin-daten/store.db`-এ স্থানীয়ভাবে থাকে।

এই স্কিল চিকিৎসকের পরামর্শের বিকল্প নয় এবং কোনো চিকিৎসা-সংক্রান্ত বক্তব্য দেয় না — এটি ব্যক্তিগত স্বাস্থ্য ডেটার জন্য একটি কাঠামোবদ্ধ নোটবুক।

---

## ট্রিগার

| বাক্যাংশ | কার্যক্রম |
|---|---|
| „Diagnose erfassen" / „রোগ নির্ণয় লিপিবদ্ধ করুন" | নতুন রোগ নির্ণয় তৈরি করা |
| „Diagnose [Name] hinzufügen" / „রোগ নির্ণয় [Name] যোগ করুন" | নামযুক্ত রোগ নির্ণয় তৈরি করা |
| „Symptomverlauf" / „উপসর্গের ইতিহাস" | আজকের উপসর্গ লিপিবদ্ধ করা |
| „Symptom [Name] erfassen" / „উপসর্গ [Name] লিপিবদ্ধ করুন" | একটি নির্দিষ্ট উপসর্গ লিপিবদ্ধ করা |
| „Untersuchungsplan" / „পরীক্ষার পরিকল্পনা দেখান" | পরবর্তী অ্যাপয়েন্টমেন্ট/পরীক্ষাগুলো দেখানো |
| „Termin hinzufügen" / „অ্যাপয়েন্টমেন্ট যোগ করুন" | পরীক্ষার অ্যাপয়েন্টমেন্ট যোগ করা |
| „Zeig meine Diagnosen" / „আমার রোগ নির্ণয়গুলো দেখাও" | রোগ নির্ণয়ের তালিকা প্রদর্শন করা |

---

## কর্মপ্রবাহ

1. **মোড শনাক্ত করা**: রোগ নির্ণয় / উপসর্গ / পরীক্ষার পরিকল্পনা
2. **ইনপুট কাঠামোবদ্ধ করা**: তারিখ, শিরোনাম, নোট, ঐচ্ছিক ICD-10-কোড
3. **সংরক্ষণ করা**: `store.db`-এ (স্থানীয়, কোনো নেটওয়ার্ক অ্যাক্সেস নেই)
4. **আউটপুট দেওয়া**: LLM-প্রসঙ্গের জন্য পঠনযোগ্য সারসংক্ষেপ

---

## CLI-এন্ট্রি

```bash
# Diagnose anlegen
python medizin_daten_core.py add-diagnosis "Hypertonie" [--icd I10] [--note "Anmerkung"]

# Diagnosen auflisten
python medizin_daten_core.py diagnoses

# Symptom erfassen
python medizin_daten_core.py add-symptom "Kopfschmerzen" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptomverlauf für eine Bezeichnung
python medizin_daten_core.py symptom-history "Kopfschmerzen" [--limit 30]

# Untersuchung planen
python medizin_daten_core.py add-exam "Blutbild" [--date 2026-07-01] [--note "nüchtern"]

# Anstehende Untersuchungen
python medizin_daten_core.py exams [--upcoming]

# Alternativer Store (z.B. für Tests)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## স্টোর

| বৈশিষ্ট্য | মান |
|---|---|
| ধরন | SQLite |
| পথ (ডিফল্ট) | `skills/assist/medizin-daten/store.db` |
| ওভাররাইড | `--store <pfad>` বা Env `MEDIZIN_STORE` |
| টেবিলসমূহ | `diagnoses`, `symptoms`, `examination_plans` |

### স্কিমা

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (kurz: 8 Hex)
    name        TEXT NOT NULL,        -- Bezeichnung (z.B. "Hypertonie")
    icd_code    TEXT,                 -- ICD-10-Code optional (z.B. "I10")
    onset_date  TEXT,                 -- Beginn (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- Freitext-Notiz
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    name         TEXT NOT NULL,       -- Bezeichnung (z.B. "Kopfschmerzen")
    severity     INTEGER,             -- 1–10 Skala (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 Zeitstempel
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    exam_name    TEXT NOT NULL,       -- Untersuchungsbezeichnung
    planned_date TEXT,                -- Geplantes Datum (ISO-8601)
    done_date    TEXT,                -- Durchgeführt am (NULL = ausstehend)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## নীতি ও অবস্থান

- কোনো চিকিৎসা-সংক্রান্ত সুপারিশ নয়; স্কিল নিজে রোগ নির্ণয় করে না।
- ICD-10-কোড ফ্রিটেক্স্ট হিসেবে সংরক্ষিত হয় — কোনো বাহ্যিক ডেটাবেসের সাথে যাচাই করা হয় না।
- ১–১০ তীব্রতা স্কেল ব্যবহারকারীর ব্যক্তিগত মূল্যায়ন।
- অনুপস্থিত মান (তারিখ, তীব্রতা) সবসময় অনুমোদিত — নোটবুক-নীতি প্রযোজ্য।

---

## ডেটা সুরক্ষা (প্রাইভেসি-গেট)

> **সতর্কতা: মেডিকেল ডেটা বিশেষভাবে সুরক্ষিত রাখা প্রয়োজন।**

- `store.db`-এ অত্যন্ত সংবেদনশীল স্বাস্থ্য ডেটা থাকে — **কখনোই Git-এ কমিট করবেন না**।
- **কোনো নেটওয়ার্ক অ্যাক্সেস নেই** — সব অপারেশন সম্পূর্ণ স্থানীয়ভাবে চলে।
- **বাহ্যিক সেবায় হস্তান্তর নয়**, কোনো ক্লাউড ব্যাকএন্ডের সাথে সিঙ্ক নয়।
- ব্যাকআপ সুপারিশ: এনক্রিপ্টেড স্থানীয় ব্যাকআপ (যেমন `age`/`gpg`)।
- স্কিল শুরুতে পরীক্ষা করে যে `store.db` স্থানীয় ফাইলসিস্টেমের বাইরে আছে কি না,
  এবং পথটি কোনো সিঙ্ক ফোল্ডারে (OneDrive ইত্যাদি) থাকলে সতর্কবার্তা দেয়।
- `~/.gitignore_global` বা স্থানীয় `.gitignore`-এ `store.db` বাদ দেওয়া উচিত।

---

## সংশ্লিষ্ট সম্পদ

- স্কিল `assist/gesundheit` — সাধারণ স্বাস্থ্য সহায়তা (মেডিকেল ডেটা নয়)
- MediPlaner (`tools/module-installer` → `mediplaner`) — ওষুধ ব্যবস্থাপনা (আলাদা প্রোগ্রাম)

---

## পরিবর্তনের ইতিহাস

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 0.1.0 | 2026-06-22 | প্রাথমিক তৈরি — স্বতন্ত্র নকশা, প্রাইভেসি-গেট, ৩-টেবিল স্কিমা |
