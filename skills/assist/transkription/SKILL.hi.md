---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "ऑडियो/वीडियो फ़ाइलों को टेक्स्ट में ट्रांसक्राइब करता है। वैकल्पिक बैकएंड के रूप में Whisper (openai-whisper) या Vosk (ऑफ़लाइन) का उपयोग करता है — दोनों की पहचान उपस्थिति-जाँच के माध्यम से होती है। बैकएंड के बिना: प्लेसहोल्डर मोड, डमी आउटपुट के साथ (dry-run)।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: hi
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
translated_from_sha256: a65e028046b1d74694d3835cfe35daeab1bc4f0f259665d6e5a8647fd0fff859
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="transkription banner">

## उद्देश्य

ऑडियो-/वीडियो-फ़ाइलों को टेक्स्ट में बदलना — स्थानीय रूप से, क्लाउड की अनिवार्यता के बिना। यह स्किल स्वयं पहचानता है कि Whisper या Vosk इंस्टॉल है या नहीं, और उपलब्ध सर्वोत्तम बैकएंड चुनता है। बैकएंड के बिना यह Dry-Run मोड में चलता है और एक प्लेसहोल्डर-टेक्स्ट लौटाता है, ताकि वर्कफ़्लो हमेशा काम करे।

ट्रांसक्राइप्ट स्थानीय रूप से `transkription/store.db` में सहेजे जाते हैं और उन्हें क्वेरी किया जा सकता है।

---

## ट्रिगर

| वाक्यांश | क्रिया |
|---|---|
| „Transkribiere diese Audio" / „इस ऑडियो को ट्रांसक्राइब करो" | ऑडियो-फ़ाइल ट्रांसक्राइब करें |
| „Transkribiere [Datei]" / „[फ़ाइल] को ट्रांसक्राइब करो" | नामित फ़ाइल ट्रांसक्राइब करें |
| „Zeig meine Transkripte" / „मेरे ट्रांसक्राइप्ट दिखाओ" | हाल के ट्रांसक्राइप्ट सूचीबद्ध करें |
| „Suche Transkript [Begriff]" / „ट्रांसक्राइप्ट में [शब्द] खोजो" | ट्रांसक्राइप्ट में पूर्ण-पाठ खोज करें |
| „Exportiere Transkript [ID]" / „ट्रांसक्राइप्ट [ID] निर्यात करो" | ट्रांसक्राइप्ट को TXT के रूप में निर्यात करें |

---

## वर्कफ़्लो

1. **बैकएंड-जाँच**: जाँचें कि `whisper` या `vosk` इम्पोर्ट योग्य है या नहीं।
2. **फ़ाइल-जाँच**: इनपुट-फ़ाइल मौजूद होनी चाहिए (Audio: wav, mp3, m4a, ogg, flac; Video: mp4, mkv, webm — ffmpeg द्वारा निष्कर्षण)।
3. **ट्रांसक्रिप्शन**: बैकएंड को कॉल करें और कच्चा टेक्स्ट प्राप्त करें।
4. **सहेजना**: मेटाडेटा (फ़ाइल, अवधि, भाषा, बैकएंड, टाइमस्टैम्प) के साथ परिणाम `store.db` में सहेजें।
5. **आउटपुट**: टेक्स्ट लौटाएँ; वैकल्पिक रूप से `.txt` के रूप में निर्यात करें।

---

## CLI-प्रवेश

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

## स्टोर

| गुण | मान |
|---|---|
| प्रकार | SQLite |
| पथ (मानक) | `skills/assist/transkription/store.db` |
| ओवरराइड | `--store <pfad>` या Env `TRANSKRIPTION_STORE` |
| तालिकाएँ | `transcripts` |

### स्कीमा `transcripts`

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

## दृष्टिकोण

- कोई बैकएंड इंस्टॉल न होने पर स्किल Dry-Run मोड में चलता है (डेमो-टेक्स्ट)।
- Vosk की तुलना में Whisper को प्राथमिकता दी जाती है (जर्मन की बेहतर गुणवत्ता)।
- Whisper और Vosk के बीच का चुनाव `assist/prefs.json` (`transkription_backend: "whisper"|"vosk"|"auto"`) के माध्यम से निर्धारित किया जा सकता है।
- वीडियो-निष्कर्षण के लिए ffmpeg अलग से आवश्यक है और स्किल में शामिल नहीं है।

---

## डेटा-सुरक्षा

- **सभी ट्रांसक्राइप्ट स्थानीय रहते हैं** — Whisper-Online-Modus के बिना कोई क्लाउड-स्थानांतरण नहीं।
- Whisper स्थानीय रूप से (tiny/base/medium-मॉडल) या OpenAI-API के माध्यम से उपयोग किया जा सकता है। मानक रूप से स्थानीय मॉडल का उपयोग होता है।
- `store.db` में संभवतः संवेदनशील बातचीत की सामग्री होती है — **Git में कमिट न करें**।
- अनुशंसा: `.gitignore` में `store.db` जोड़ें।

---

## संबंधित संसाधन

- BACH `hub/_services/voice/voice_stt.py` — बैकएंड-पैटर्न (प्रेरणा, केवल-पठन)
- स्किल `utilities/yt-transcriber` — YouTube-ट्रांसक्रिप्शन (अलग स्किल, कोई डुप्लिकेट नहीं: YT-विशिष्ट)
- `tools/module-installer/module_installer.py` — रजिस्ट्री में whisper + vosk शामिल हैं

---

## चेंजलॉग

| संस्करण | तिथि | परिवर्तन |
|---|---|---|
| 0.1.0 | 2026-06-22 | प्रारंभिक निर्माण — अपना SQLite-स्टोर, Whisper/Vosk-उपस्थिति-जाँच |
