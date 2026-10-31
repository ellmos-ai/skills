---
name: video-transcriber
version: 1.2.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-08-24
description: "ऑनलाइन वीडियो स्रोतों से वीडियो ट्रांसक्रिप्ट (सबटाइटल) और मेटाडेटा प्राप्त करें और उन्हें Markdown, JSON, या सादे टेक्स्ट के रूप में आउटपुट करें। वर्तमान में समर्थित: YouTube। मैन्युअल रूप से बनाए गए सबटाइटल को प्राथमिकता देता है, और उनके न होने पर स्वचालित रूप से उत्पन्न सबटाइटल पर लौटता है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: caf55e3434119acd935dad208f5461f7a08e72d34b595314abd52b58469cd299
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:53.391636+00:00"
---
<img src="banner.png" width="100%" alt="video-transcriber banner">

# वीडियो-ट्रांसक्राइबर

ऑनलाइन वीडियो से ट्रांसक्रिप्ट (सबटाइटल) और मेटाडेटा (शीर्षक, चैनल, तारीख, व्यूज़, विवरण) प्राप्त करता है।
मैन्युअल रूप से बनाए गए सबटाइटल को प्राथमिकता देता है, और उनके न होने पर स्वचालित रूप से उत्पन्न सबटाइटल पर लौटता है। आउटपुट Markdown, JSON या प्लेनटेक्स्ट में होता है।

यदि प्राथमिक मार्ग (`youtube-transcript-api`) कुछ नहीं लौटाता, तो yt-dlp मेटाडेटा के माध्यम से एक दूसरा मार्ग स्वतः सक्रिय होता है। यह केवल सबटाइटल ट्रैक पढ़ता है, जिसे प्लेटफ़ॉर्म पहले से ही प्लेबैक के लिए भेजता है — **कोई वीडियो या ऑडियो डाउनलोड नहीं होता।** किस मार्ग ने काम किया, यह JSON आउटपुट में `source` फ़ील्ड में और stderr पर दर्ज होता है।

प्रत्येक वांछित भाषा के लिए फ़ॉलबैक पहले मैन्युअल सटीक और बेस ट्रैक को, फिर स्वचालित सटीक और बेस ट्रैक को प्राथमिकता देता है; कोई भी अन्य ट्रैक केवल उसके बाद आते हैं। एक अपठनीय JSON3 ट्रैक से प्राप्ति समाप्त नहीं होती, जब तक कोई अन्य उम्मीदवार उपलब्ध हो।

वर्तमान में समर्थित स्रोत: **YouTube** (youtube.com, youtu.be, youtube-nocookie.com)।

वीडियो के मामले में सामग्री को हाथ से सारांशित करने के बजाय इस टूल का उपयोग करें — ट्रांसक्रिप्ट विश्वसनीय स्रोत है।

> **सूचना:** यह उपकरण YouTube या Google से संबद्ध नहीं है और इन द्वारा समर्थित या अनुमोदित नहीं है। उपयोग अपनी जिम्मेदारी पर होता है। संबंधित प्लेटफ़ॉर्म की उपयोग शर्तों और लागू कॉपीराइट का पालन करने की जिम्मेदारी उपयोगकर्ताओं की स्वयं की है। DRM, पेवॉल या पहुँच प्रतिबंधों को बायपास न करें; बड़े पैमाने पर डेटा संग्रह न करें; अधिकार धारकों की सहमति के बिना संरक्षित ट्रांसक्रिप्ट को पुनः प्रकाशित न करें।

## निर्भरताएँ और लाइसेंस

```bash
pip install youtube-transcript-api   # Transkripte (Pflicht) — MIT-Lizenz
pip install yt-dlp                   # Metadaten (optional, Fallback: noembed) — Unlicense (Public Domain)
```

## उपयोग

> **Windows सूचना:** हमेशा `PYTHONIOENCODING=utf-8` सेट करें, अन्यथा आउटपुट में umlaut और विशेष अक्षर (cp1252 एन्कोडिंग) बिगड़ जाएँगे।

```bash
# Standard: Markdown mit Timestamps
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Ausgabeformat waehlen
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# In Datei speichern
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Sprachen bevorzugen (Default: de en)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### विकल्प

| विकल्प | प्रभाव |
|--------|---------|
| `--format markdown\|json\|plain` | आउटपुट प्रारूप (डिफ़ॉल्ट: markdown) |
| `--output, -o <datei>` | stdout के बजाय फ़ाइल में लिखें |
| `--lang <codes...>` | पसंदीदा सबटाइटल भाषाएँ (डिफ़ॉल्ट: de en) |
| `--meta-only` | केवल मेटाडेटा, कोई ट्रांसक्रिप्ट नहीं |
| `--transcript-only` | केवल ट्रांसक्रिप्ट, कोई मेटाडेटा नहीं |
| `--no-timestamps` | टाइमस्टैम्प के बिना ट्रांसक्रिप्ट |
| `--no-meta` | तेज़: yt-dlp मेटाडेटा छोड़ें |
| `--allow-empty-transcript` | खाली ट्रांसक्रिप्ट को सफलता मानें (Exit 3 के बजाय Exit 0) |

### Exit-कोड

खाली ट्रांसक्रिप्ट **सफलता नहीं** है। संस्करण 1.2.0 से पहले यह स्थिति Exit 0 के साथ समाप्त होती थी: आउटपुट फ़ाइल लिखी जाती थी, सेगमेंट-array खाली रहता था, और हर कॉलिंग ऑटोमेशन इसे सफल मान लेता था। यही मूक विफलता वह वास्तविक दोष था, जिसे 1.2.0 ने दूर किया।

| कोड | अर्थ |
|------|-----------|
| `0` | सफलता — ट्रांसक्रिप्ट उपलब्ध, या `--meta-only`, या `--allow-empty-transcript` |
| `1` | मान्य वीडियो URL/ID नहीं |
| `2` | आह्वान त्रुटि (argparse द्वारा दी गई, जैसे अज्ञात विकल्प) |
| `3` | कोई ट्रांसक्रिप्ट नहीं मिला — दोनों मार्ग खाली |

`2` argparse के लिए आरक्षित है, ताकि आह्वान में टाइपो और बिना सबटाइटल वाले वीडियो में अंतर बना रहे।

```bash
# In Skripten
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o out.md || {
  code=$?
  [ "$code" -eq 3 ] && echo "Video hat keine Untertitel" || echo "Fehler: $code"
}
```

### Python लाइब्रेरी के रूप में

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)

# Immer pruefen -- fetch_transcript wirft nicht, es meldet:
if not transcript["segments"]:
    raise RuntimeError(transcript["error"])
print(transcript["source"])  # "youtube_transcript_api" oder "yt-dlp"
```

दोनों मार्ग अलग-अलग कॉल किए जा सकते हैं: `fetch_transcript_primary()` (केवल
`youtube-transcript-api`) और `fetch_transcript_ytdlp()` (केवल दूसरा मार्ग)।
`fetch_transcript()` दोनों को जोड़ता है और फ़ील्ड `segments`,
`language`, `is_generated`, `full_text`, `source` की गारंटी देता है, और विफलता की स्थिति में `error`।

## सामान्य उपयोग के मामले

- शोध: वीडियो सामग्री को उद्धरण-योग्य पाठ के रूप में खोजना
- स्रोत विश्लेषण: व्याख्यानों में तर्क/रूपक की जाँच
- सारांश: हैलुसिनेशन (मनगढ़ंत सामग्री) के बजाय ट्रांसक्रिप्ट को विश्वसनीय आधार के रूप में उपयोग

## सीमाएँ

- केवल तभी काम करता है जब वीडियो में सबटाइटल हों (मैन्युअल या स्वचालित)
- स्वचालित सबटाइटल में पहचान त्रुटियाँ हो सकती हैं
- कोई ऑडियो डाउनलोड नहीं, कोई अपनी स्पीच-रिकग्निशन नहीं — दूसरा मार्ग भी केवल सबटाइटल ट्रैक लोड करता है, कभी वीडियो या ऑडियो नहीं
- दूसरे मार्ग को JSON3 ट्रैक चाहिए; यदि प्लेटफ़ॉर्म केवल अन्य प्रारूप देता है, तो आंशिक आउटपुट के बजाय रन Exit 3 के साथ समाप्त होता है

## परिवर्तन-लॉग

### 1.2.0 (2026-08-24)
- **Exit-शब्दार्थ:** खाली ट्रांसक्रिप्ट अब चुपचाप Exit `0` के बजाय Exit `3` के साथ समाप्त होता है। अमान्य URL अब नामित स्थिरांक के रूप में `1` देता है। `--meta-only` सफल रहता है, क्योंकि वहाँ ट्रांसक्रिप्ट अपेक्षित नहीं है।
- **नया विकल्प `--allow-empty-transcript`:** खाली ट्रांसक्रिप्ट को जानबूझकर सफलता मानता है — उन कॉलर्स के लिए जो सबटाइटल को वैकल्पिक मानते हैं।
- **yt-dlp सबटाइटल फ़ॉलबैक:** तब सक्रिय होता है जब प्राथमिक मार्ग कोई सेगमेंट नहीं लौटाता (केवल अपवाद पर नहीं)। `extract_info(download=False)` का उपयोग करता है और केवल सबटाइटल URL पढ़ता है — कोई वीडियो नहीं, कोई ऑडियो नहीं, पहुँच प्रतिबंधों को बायपास नहीं।
- **भाषा-चयन सुदृढ़:** `de-orig`/`de-DE` अब `--lang de` के लिए मिलते हैं (बेस-भाषा मिलान)। मैन्युअल सबटाइटल अब भी स्वचालित से पहले।
- परिणाम में **फ़ील्ड `source`**: `youtube_transcript_api` या `yt-dlp`।
- रिग्रेशन टेस्ट: मॉक्ड प्रतिक्रियाओं के साथ 29 टेस्ट (UTF-8, सभी तीनों आउटपुट प्रारूप, Exit-कोड, भाषा-चयन, JSON3 पार्सिंग)।

### 1.1.0 (2026-06-20)
- नाम बदला गया `yt-transcriber` → `video-transcriber` (YouTube ब्रांड दिशानिर्देश: „yt" एक स्पष्ट रूप से निषिद्ध संक्षिप्ति है; अनुशंसा: RECHTSCHECK_2026-06-20.md)
- स्क्रिप्ट: `yt_transcriber.py` → `video_transcriber.py`
- Disclaimer और निर्भरता-लाइसेंस जोड़े गए (उपयोगकर्ता की जिम्मेदारी, ToS, कोई अनुमोदन नहीं)
- YouTube अब केवल वर्णनात्मक स्रोत-उल्लेख के रूप में है, नाम/ब्रांड का हिस्सा नहीं
- पुराने पथ पर बैकवर्ड-कंपैटिबिलिटी रैपर `yt_transcriber.py` बनाए रखा गया

### 1.0.0 (2026-06-12)
- SKILL.md जोड़ा गया (टूल स्क्रिप्ट + README के रूप में पहले से मौजूद था)
- स्क्रिप्ट v1.0.0: ट्रांसक्रिप्ट + मेटाडेटा, 3 आउटपुट प्रारूप, भाषा-प्राथमिकताएँ
