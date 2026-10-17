---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "ব্যবহারকারী-অভিযোজিত ব্যাকএন্ড নির্বাচনসহ ক্যালেন্ডার স্কিল (Flag 3)। ডিফল্ট: স্থানীয় SQLite স্টোর। ঐচ্ছিক: Google Calendar MCP, Routinika বা UpToday ব্যাকএন্ড হিসেবে — assist/prefs.json এর মাধ্যমে নিয়ন্ত্রিত। পছন্দ সেট না থাকলে LLM ব্যবহারকারীকে ইন্টারঅ্যাকটিভভাবে জিজ্ঞাসা করে।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: bn
status: stable
visibility: public
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
translated_from_sha256: 3dd9e7b8d86095d63dd54e3d9c4c3b825eef0dd3affffd992b54bbc8a03cdd7e
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.347183+00:00"
---
<img src="banner.png" width="100%" alt="kalender banner">

## উদ্দেশ্য

ইভেন্ট (অ্যাপয়েন্টমেন্ট) রেকর্ড, অনুসন্ধান ও পরিচালনা করা — নির্বাচনযোগ্য ব্যাকএন্ড সহ। Core (`kalender_core.py`) ডিফল্ট হিসেবে সর্বদা **স্থানীয় SQLite স্টোর** নিয়ে কাজ করে। প্রয়োজনে LLM `assist/prefs.json` এর ভিত্তিতে একটি বিকল্প ব্যাকএন্ড নির্বাচন করে।

**Flag 3 — ব্যাকএন্ড নির্বাচন:**

| `kalender_backend`-এর মান (prefs.json) | আচরণ |
|---|---|
| `local` (মানক/ডিফল্ট) | এই স্কিল-ফোল্ডারের SQLite স্টোর |
| `google` | Google-Calendar-MCP (শুধু LLM-পথ, core.py-তে নয়) |
| `routinika` | module-installer এর মাধ্যমে Routinika-ক্যালেন্ডার (v0.1-এ বাস্তবায়িত নয়) |
| `uptoday` | module-installer এর মাধ্যমে UpToday-ক্যালেন্ডার (v0.1-এ বাস্তবায়িত নয়) |
| সেট করা নেই | LLM ব্যবহারকারীকে ইন্টারঅ্যাকটিভভাবে পছন্দের ব্যাকএন্ড জিজ্ঞাসা করে |

> `kalender_core.py` শুধুমাত্র `local` ব্যাকএন্ড বাস্তবায়ন করে।
> Google-Calendar-MCP এবং অন্যান্য ব্যাকএন্ড LLM-নিয়ন্ত্রিত এবং
> SKILL.md-তে ডকুমেন্টেড, Core-এ নয়।

---

## ট্রিগার

| বাক্যাংশ | কর্ম |
|---|---|
| „একটি অ্যাপয়েন্টমেন্ট যোগ করো" | নতুন ইভেন্ট রেকর্ড করা |
| „আজ কী কী অ্যাপয়েন্টমেন্ট আছে?" | আজকের ইভেন্ট জিজ্ঞাসা করা |
| „এই সপ্তাহে কী কী অ্যাপয়েন্টমেন্ট আছে?" | ৭-দিনের সারসংক্ষেপ |
| „[তারিখ]-এ [শিরোনাম] অ্যাপয়েন্টমেন্ট" | তারিখসহ ইভেন্ট তৈরি করা |
| „[মাস]-এর সব অ্যাপয়েন্টমেন্ট দেখাও" | মাসিক সারসংক্ষেপ |
| „[ID] অ্যাপয়েন্টমেন্টটি মুছে ফেলো" | ইভেন্ট মুছে ফেলা |
| „অ্যাপয়েন্টমেন্ট রপ্তানি করো" | সব/একক ইভেন্টের ICS-রপ্তানি |

---

## কার্যপ্রবাহ

1. **ব্যাকএন্ড যাচাই**: `assist/prefs.json` → `kalender_backend` পড়া।
2. **পছন্দ না থাকলে**: LLM ব্যবহারকারীকে জিজ্ঞাসা করে: স্থানীয় ক্যালেন্ডার, Google Calendar, নাকি অন্য কিছু?
3. **স্থানীয় ব্যাকএন্ড**: core.py — SQLite স্টোরে ইভেন্ট তৈরি/অনুসন্ধান/মুছে ফেলা।
4. **Google-ব্যাকএন্ড**: LLM সরাসরি Google-Calendar-MCP কল করে (core.py জড়িত নয়)।
5. **আউটপুট**: পড়ার উপযোগী ইভেন্ট-তালিকা বা নিশ্চিতকরণ।

---

## CLI-প্রবেশ

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

## স্টোর

| বৈশিষ্ট্য | মান |
|---|---|
| ধরন | SQLite (local-ব্যাকএন্ড) |
| পথ (ডিফল্ট) | `skills/assist/kalender/store.db` |
| ওভাররাইড | `--store <pfad>` বা Env `KALENDER_STORE` |
| টেবিল | `events` |

### স্কিমা

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

## নীতি

- Core শুধু `local` ব্যাকএন্ড বাস্তবায়ন করে — হালকা, কোনো বাহ্যিক নির্ভরতা নেই।
- ICS-রপ্তানি বৈধ RFC 5545-সাবসেট (VCALENDAR + VEVENT) তৈরি করে, যা সব প্রচলিত ক্যালেন্ডার-অ্যাপে আমদানিযোগ্য।
- ICS-আমদানি (পার্সিং) v0.1-এ এখনও বাস্তবায়িত নয় — v0.2-এর জন্য পরিকল্পিত।
- পুনরাবৃত্তি-নিয়ম (`recurrence`/RRULE) সংরক্ষিত হয় কিন্তু মূল্যায়ন করা হয় না — মূল্যায়ন v0.2-এ।

---

## গোপনীয়তা

- স্থানীয় ইভেন্ট `store.db`-তে থাকে — Core-এ কোনো নেটওয়ার্ক অ্যাক্সেস নেই।
- Google-Calendar-ব্যাকএন্ড পথে Google-Calendar-MCP ডেটা প্রক্রিয়া করে — Google-এর গোপনীয়তা নীতি প্রযোজ্য।
- `store.db` Git-এ কমিট না করা (সুপারিশকৃত: `.gitignore`)।

---

## সংশ্লিষ্ট সম্পদ

- Google-Calendar-MCP (`mcp__claude_ai_Google_Calendar__*`) — বিকল্প ব্যাকএন্ড, LLM-নিয়ন্ত্রিত
- স্কিল `assist/haushalt-manager` — Routinika-ইন্টিগ্রেশন (Presence-Check-প্যাটার্ন)
- `tools/module-installer/module_installer.py` — ভবিষ্যৎ Routinika/UpToday-ব্যাকএন্ড-ইন্টিগ্রেশনের জন্য

---

## চেঞ্জলগ

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 0.1.0 | 2026-06-22 | প্রাথমিক সৃষ্টি — Flag-3-যুক্তি, local-ব্যাকএন্ড, ICS-রপ্তানি |
