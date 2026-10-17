---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "অডিও/ভিডিও ফাইলকে টেক্সটে রূপান্তর করে। ঐচ্ছিক ব্যাকএন্ড হিসেবে Whisper (openai-whisper) বা Vosk (offline) ব্যবহার করে — উভয়ই উপস্থিতি পরীক্ষার মাধ্যমে শনাক্ত করা হয়। কোনো ব্যাকএন্ড ছাড়া: প্লেসহোল্ডার মোডে ডামি আউটপুট সহ (dry-run)।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: bn
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
translated_from_sha256: a65e028046b1d74694d3835cfe35daeab1bc4f0f259665d6e5a8647fd0fff859
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="transkription banner">

## উদ্দেশ্য

অডিও-/ভিডিও ফাইলকে টেক্সটে রূপান্তর করা — স্থানীয়ভাবে, ক্লাউডের বাধ্যবাধকতা ছাড়াই। এই স্কিল নিজে শনাক্ত করে যে Whisper বা Vosk ইনস্টল আছে কিনা, এবং সর্বোত্তম উপলব্ধ ব্যাকএন্ড বেছে নেয়। কোনো ব্যাকএন্ড না থাকলে এটি Dry-Run মোডে চলে এবং একটি প্লেসহোল্ডার টেক্সট ফেরত দেয়, যাতে ওয়ার্কফ্লো সর্বদা কাজ করে।

ট্রান্সক্রিপ্টগুলো স্থানীয়ভাবে `transkription/store.db`-এ সংরক্ষিত হয় এবং পরে অনুসন্ধান করা যায়।

---

## ট্রিগার

| বাক্যাংশ | কার্যক্রম |
|---|---|
| „Transkribiere diese Audio" / „এই অডিও ট্রান্সক্রাইব করো" | অডিও ফাইল ট্রান্সক্রাইব করা |
| „Transkribiere [Datei]" / „এই ফাইলটি ট্রান্সক্রাইব করো [Datei]" | নামযুক্ত ফাইল ট্রান্সক্রাইব করা |
| „Zeig meine Transkripte" / „আমার ট্রান্সক্রিপ্টগুলো দেখাও" | সাম্প্রতিক ট্রান্সক্রিপ্ট তালিকাভুক্ত করা |
| „Suche Transkript [Begriff]" / „ট্রান্সক্রিপ্ট খোঁজো [Begriff]" | ট্রান্সক্রিপ্টে পূর্ণ-টেক্সট অনুসন্ধান |
| „Exportiere Transkript [ID]" / „ট্রান্সক্রিপ্ট রপ্তানি করো [ID]" | ট্রান্সক্রিপ্টকে TXT হিসেবে রপ্তানি করা |

---

## ওয়ার্কফ্লো

1. **ব্যাকএন্ড-পরীক্ষা**: `whisper` বা `vosk` আমদানিযোগ্য কিনা তা পরীক্ষা করা।
2. **ফাইল-পরীক্ষা**: ইনপুট ফাইল অবশ্যই বিদ্যমান থাকতে হবে (অডিও: wav, mp3, m4a, ogg, flac; ভিডিও: mp4, mkv, webm — ffmpeg দিয়ে নিষ্কাশন)।
3. **ট্রান্সক্রিপশন**: ব্যাকএন্ড কল করে কাঁচা টেক্সট পাওয়া।
4. **সংরক্ষণ**: ফলাফল মেটাডেটা সহ (ফাইল, সময়কাল, ভাষা, ব্যাকএন্ড, টাইমস্ট্যাম্প) `store.db`-এ সংরক্ষণ।
5. **আউটপুট**: টেক্সট ফেরত দেওয়া; ঐচ্ছিকভাবে `.txt` হিসেবে রপ্তানি।

---

## CLI-প্রবেশবিন্দু

```bash
# Datei transkribieren
python transkription_core.py transcribe audio.wav

# Mit expliziter Sprache
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-Run (kein Backend nötig)
python transkription_core.py transcribe audio.wav --dry-run

# Transkripte auflisten
python transkription_core.py list [--limit 20]

# Volltextsuche
python transkription_core.py search "Begriff"

# Exportieren
python transkription_core.py export <id> [--out datei.txt]

# Backend-Check
python transkription_core.py check

# Alternativer Store-Pfad (z.B. für Tests)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## Store

| বৈশিষ্ট্য | মান |
|---|---|
| ধরন | SQLite |
| পথ (ডিফল্ট) | `skills/assist/transkription/store.db` |
| ওভাররাইড | `--store <pfad>` বা Env `TRANSKRIPTION_STORE` |
| টেবিল | `transcripts` |

### Schema `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (kurz: 8 Hex)
    file_path   TEXT NOT NULL,     -- Originalpfad der Audiodatei
    file_name   TEXT NOT NULL,     -- Dateiname (ohne Pfad, für Anzeige)
    text        TEXT NOT NULL,     -- Transkribierter Text
    language    TEXT,              -- Sprache (z.B. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- Dauer in Sekunden (wenn bekannt)
    created_at  TEXT NOT NULL,     -- ISO-8601 Timestamp
    tags        TEXT               -- Komma-getrennte Tags (optional)
);
```

---

## নীতি

- ইনস্টল করা ব্যাকএন্ড না থাকলে স্কিল Dry-Run মোডে (ডেমো-টেক্সট) কাজ করে।
- Vosk-এর চেয়ে Whisper-কে অগ্রাধিকার দেওয়া হয় (জার্মান ভাষায় ভালো মান)।
- Whisper ও Vosk-এর মধ্যে পছন্দ `assist/prefs.json` (`transkription_backend: "whisper"|"vosk"|"auto"`) দিয়ে নির্ধারণ করা যায়।
- ভিডিও নিষ্কাশনের জন্য ffmpeg আলাদাভাবে প্রয়োজন এবং এটি স্কিলের অন্তর্ভুক্ত নয়।

---

## ডেটা-সুরক্ষা

- **সমস্ত ট্রান্সক্রিপ্ট স্থানীয় থাকে** — Whisper-Online-মোড ছাড়া কোনো ক্লাউড-স্থানান্তর নেই।
- Whisper স্থানীয়ভাবে (tiny/base/medium-মডেল) বা OpenAI-API-এর মাধ্যমে ব্যবহার করা যায়। ডিফল্টভাবে স্থানীয় মডেল ব্যবহৃত হয়।
- `store.db`-এ সম্ভাব্যভাবে সংবেদনশীল কথোপকথনের বিষয়বস্তু থাকে — **Git-এ কমিট করবেন না**।
- সুপারিশ: `.gitignore`-এ `store.db` যোগ করুন।

---

## সংশ্লিষ্ট সম্পদ

- BACH `hub/_services/voice/voice_stt.py` — ব্যাকএন্ড-প্যাটার্ন (অনুপ্রেরণা, শুধু-পঠনযোগ্য)
- স্কিল `utilities/yt-transcriber` — YouTube-ট্রান্সক্রিপশন (আলাদা স্কিল, নকল নয়: YT-নির্দিষ্ট)
- `tools/module-installer/module_installer.py` — রেজিস্ট্রিতে whisper + vosk অন্তর্ভুক্ত

---

## পরিবর্তনের ইতিহাস

| সংস্করণ | তারিখ | পরিবর্তন |
|---|---|---|
| 0.1.0 | 2026-06-22 | প্রথম সৃষ্টি — নিজস্ব SQLite-Store, Whisper/Vosk-উপস্থিতি-পরীক্ষা |
