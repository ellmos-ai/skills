---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "स्थानीय, निजी मेडिकल डेटा कैप्चर: निदान, लक्षण इतिहास और परीक्षा योजनाएँ। BACH से कोई संबंध नहीं — अपने SQLite स्टोर के साथ कस्टम डिज़ाइन। सख़्ती से स्थानीय, कोई क्लाउड ट्रांसफर नहीं।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: hi
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
translated_from_sha256: b345b47fc6f0ea659604ac06a0d5bda40fadb7770d2f3b2899ce95ccb9ee463c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="medizin-daten banner">

## उद्देश्य

मेडिकल व्यक्तिगत डेटा को सुरक्षित और स्थानीय रूप से कैप्चर करना: निदान (वैकल्पिक ICD-10-कोड), तिथि-क्रम के साथ लक्षण-पाठ्यक्रम और परीक्षा योजनाएँ। सभी डेटा केवल `medizin-daten/store.db` में स्थानीय रहता है।

यह स्किल चिकित्सीय परामर्श का स्थान नहीं लेता और कोई चिकित्सीय कथन नहीं देता — यह व्यक्तिगत स्वास्थ्य डेटा के लिए एक संरचित नोटबुक है।

---

## ट्रिगर

| वाक्यांश | कार्रवाई |
|---|---|
| „Diagnose erfassen" / „निदान दर्ज करें" | नया निदान बनाएँ |
| „Diagnose [Name] hinzufügen" / „निदान [Name] जोड़ें" | नामित निदान बनाएँ |
| „Symptomverlauf" / „लक्षण-क्रम" | आज के लक्षण दर्ज करें |
| „Symptom [Name] erfassen" / „लक्षण [Name] दर्ज करें" | एक लक्षण दर्ज करें |
| „Untersuchungsplan" / „जाँच-योजना" | अगली अपॉइंटमेंट/जाँचें दिखाएँ |
| „Termin hinzufügen" / „अपॉइंटमेंट जोड़ें" | जाँच अपॉइंटमेंट दर्ज करें |
| „Zeig meine Diagnosen" / „मेरे निदान दिखाएँ" | निदानों की सूची दिखाएँ |

---

## कार्यप्रवाह

1. **मोड पहचानें**: निदान / लक्षण / परीक्षा योजना
2. **इनपुट संरचित करें**: तिथि, नाम, नोट्स, वैकल्पिक ICD-10-कोड
3. **सहेजें**: `store.db` में (स्थानीय, कोई नेटवर्क एक्सेस नहीं)
4. **आउटपुट दें**: LLM संदर्भ के लिए पठनीय सारांश

---

## CLI-प्रवेश

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

## स्टोर

| गुण | मान |
|---|---|
| प्रकार | SQLite |
| पथ (डिफ़ॉल्ट) | `skills/assist/medizin-daten/store.db` |
| ओवरराइड | `--store <pfad>` या Env `MEDIZIN_STORE` |
| तालिकाएँ | `diagnoses`, `symptoms`, `examination_plans` |

### स्कीमा

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

## दृष्टिकोण

- कोई चिकित्सीय अनुशंसा नहीं, स्किल द्वारा कोई निदान नहीं।
- ICD-10-कोड मुक्त-पाठ के रूप में सहेजे जाते हैं — किसी बाहरी डेटाबेस से सत्यापन नहीं।
- गंभीरता पैमाना 1–10 उपयोगकर्ता-व्यक्तिपरक है।
- लापता मान (तिथि, गंभीरता) हमेशा अनुमत हैं — नोटबुक का सिद्धांत लागू होता है।

---

## गोपनीयता (Privacy-Gate)

> **चेतावनी: मेडिकल डेटा विशेष रूप से संरक्षित किया जाना चाहिए।**

- `store.db` में अत्यधिक संवेदनशील स्वास्थ्य डेटा है — **इसे कभी Git में commit न करें**।
- **कोई नेटवर्क एक्सेस नहीं** — सभी संचालन पूरी तरह स्थानीय रूप से चलते हैं।
- **बाहरी सेवाओं को कोई साझाकरण नहीं**, क्लाउड बैकएंड के साथ कोई सिंक नहीं।
- बैकअप अनुशंसा: एन्क्रिप्टेड स्थानीय बैकअप (जैसे `age`/`gpg`)।
- स्किल शुरू होने पर जाँचती है कि `store.db` स्थानीय फ़ाइल सिस्टम के बाहर स्थित है या नहीं —
  और यदि पथ किसी सिंक फ़ोल्डर (OneDrive आदि) में है तो चेतावनी देती है।
- `~/.gitignore_global` या स्थानीय `.gitignore` में `store.db` को अपवर्जित (ignore) किया जाना चाहिए।

---

## संबंधित संसाधन

- स्किल `assist/gesundheit` — सामान्य स्वास्थ्य सहायता (गैर-चिकित्सीय डेटा)
- MediPlaner (`tools/module-installer` → `mediplaner`) — दवा प्रबंधन (अलग प्रोग्राम)

---

## परिवर्तन-लॉग

| संस्करण | तिथि | परिवर्तन |
|---|---|---|
| 0.1.0 | 2026-06-22 | प्रारंभिक निर्माण — स्व-डिज़ाइन, Privacy-Gate, 3-तालिका स्कीमा |
