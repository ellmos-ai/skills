---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "उपयोगकर्ता-अनुकूली बैकएंड चयन (Flag 3) के साथ कैलेंडर स्किल। डिफ़ॉल्ट: स्थानीय SQLite स्टोर। वैकल्पिक: Google Calendar MCP, Routinika या UpToday को बैकएंड के रूप में — assist/prefs.json के माध्यम से नियंत्रित। कोई प्राथमिकता न होने पर LLM उपयोगकर्ता से इंटरैक्टिव रूप से पूछता है।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: hi
status: stable
visibility: public
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
translated_from_sha256: 3dd9e7b8d86095d63dd54e3d9c4c3b825eef0dd3affffd992b54bbc8a03cdd7e
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T12:48:27.813836+00:00"
---
<img src="banner.png" width="100%" alt="kalender banner">

## उद्देश्य

नियुक्तियाँ दर्ज करें, पूछें और प्रबंधित करें — अपनी पसंद का बैकएंड चुनकर। कोर
(`kalender_core.py`) हमेशा **स्थानीय SQLite स्टोर** के साथ काम करता है, जो
डिफ़ॉल्ट है। आवश्यकता पड़ने पर LLM प्राथमिकता की इस फ़ाइल के आधार पर दूसरा बैकएंड चुनता है:
`assist/prefs.json`.

**Flag 3 — बैकएंड-चयन:**

| `kalender_backend` का prefs.json में मान | व्यवहार |
|---|---|
| `local` (मानक/डिफ़ॉल्ट) | इस स्किल फ़ोल्डर में SQLite स्टोर |
| `google` | Google-Calendar-MCP (केवल LLM के माध्यम से, core.py में नहीं) |
| `routinika` | module-installer के ज़रिये Routinika कैलेंडर (v0.1 में लागू नहीं) |
| `uptoday` | module-installer के ज़रिये UpToday कैलेंडर (v0.1 में लागू नहीं) |
| नहीं सेट | LLM उपयोगकर्ता से इंटरैक्टिव रूप से पसंदीदा बैकएंड पूछता है |

> `kalender_core.py` केवल `local`-बैकएंड लागू करता है।
> Google-Calendar-MCP और अन्य बैकएंड LLM द्वारा नियंत्रित होते हैं और
> SKILL.md में दर्ज हैं, कोर में नहीं।

---

## ट्रिगर

| वाक्यांश | कार्रवाई |
|---|---|
| „एक अपॉइंटमेंट दर्ज करो" | नई नियुक्ति दर्ज करें |
| „आज क्या तय है?" | आज की नियुक्तियाँ पूछें |
| „इस सप्ताह क्या तय है?" | सात दिनों का अवलोकन |
| „[तारीख] को [शीर्षक] की नियुक्ति" | तारीख सहित नियुक्ति बनाएँ |
| „[महीने] की सभी नियुक्तियाँ" | महीने का अवलोकन |
| „[ID] वाली नियुक्ति हटाओ" | नियुक्ति हटाएँ |
| „नियुक्ति निर्यात करो" | सभी या किसी एक नियुक्ति का ICS निर्यात |

---

## कार्यप्रवाह

1. **बैकएंड जाँचें**: `assist/prefs.json` → `kalender_backend` पढ़ें।
2. **प्राथमिकता न होने पर**: LLM उपयोगकर्ता से पूछता है: स्थानीय कैलेंडर, Google Calendar या कोई अन्य?
3. **स्थानीय बैकएंड**: core.py — SQLite स्टोर में नियुक्ति जोड़ना, पूछना या हटाना।
4. **Google बैकएंड**: LLM सीधे Google-Calendar-MCP को कॉल करता है (core.py शामिल नहीं है)।
5. **आउटपुट**: पढ़ने योग्य नियुक्ति-सूची या पुष्टि।

---

## CLI-प्रवेश

```bash
# Termin anlegen
python kalender_core.py add "Zahnarzt" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Praxis Dr. X"]

# Heutige Termine
python kalender_core.py today

# Wochenübersicht
python kalender_core.py week [--from 2026-06-22]

# Monatsübersicht
python kalender_core.py month [--month 2026-07]

# Alle Termine (optional mit Suchbegriff)
python kalender_core.py list [--search "Zahnarzt"] [--limit 50]

# Termin löschen
python kalender_core.py delete <id>

# ICS-Export
python kalender_core.py export [--id <id>] [--out kalender.ics]

# Backend-Check
python kalender_core.py check-backend

# Alternativer Store (z.B. für Tests)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## स्टोर

| गुण | मान |
|---|---|
| प्रकार | SQLite (स्थानीय बैकएंड) |
| पथ (डिफ़ॉल्ट) | `skills/assist/kalender/store.db` |
| वैकल्पिक सेटिंग | `--store <pfad>` या पर्यावरण चर `KALENDER_STORE` |
| तालिकाएँ | `events` |

### स्कीमा

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (kurz: 8 Hex)
    title        TEXT NOT NULL,         -- Termin-Bezeichnung
    date         TEXT NOT NULL,         -- ISO-Datum YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- Dauer in Minuten (optional)
    location     TEXT,                  -- Ort (optional)
    description  TEXT,                  -- Notiz/Beschreibung
    recurrence   TEXT,                  -- ICS RRULE (optional, z.B. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID für Import/Export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## दृष्टिकोण

- कोर केवल `local`-बैकएंड लागू करता है — हल्का है और बाहरी निर्भरताएँ नहीं हैं।
- ICS निर्यात एक वैध RFC 5545 उपसमुच्चय (VCALENDAR + VEVENT) बनाता है, जिसे आम कैलेंडर ऐप आयात कर सकते हैं।
- ICS आयात (पार्सिंग) v0.1 में अभी लागू नहीं है — v0.2 के लिए नियोजित है।
- पुनरावृत्ति के नियम (`recurrence`/RRULE) सहेजे जाते हैं, पर उनका मूल्यांकन नहीं होता — यह v0.2 के लिए नियोजित है।

---

## गोपनीयता

- स्थानीय नियुक्तियाँ `store.db` में रहती हैं — कोर नेटवर्क का उपयोग नहीं करता।
- Google-Calendar बैकएंड का उपयोग करते समय Google-Calendar-MCP डेटा संसाधित करता है — Google की गोपनीयता नीतियाँ लागू होती हैं।
- `store.db` को Git में कमिट न करें (सुझाव: `.gitignore`).

---

## संबंधित संसाधन

- Google-Calendar-MCP (`mcp__claude_ai_Google_Calendar__*`) — वैकल्पिक बैकएंड, LLM द्वारा नियंत्रित
- स्किल `assist/haushalt-manager` — Routinika एकीकरण (उपस्थिति-जाँच का पैटर्न)
- `tools/module-installer/module_installer.py` — भविष्य में Routinika/UpToday बैकएंड एकीकरण के लिए

---

## परिवर्तन लॉग

| संस्करण | दिनांक | परिवर्तन |
|---|---|---|
| 0.1.0 | 2026-06-22 | पहला संस्करण — Flag 3 का तर्क, स्थानीय बैकएंड, ICS निर्यात |
