---
name: video-transcriber
version: 1.2.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-08-24
description: "অনলাইন ভিডিও উৎস থেকে ভিডিওর ট্রান্সক্রিপ্ট (সাবটাইটেল) এবং মেটাডেটা সংগ্রহ করে Markdown, JSON বা সাধারণ টেক্সট (plain text) হিসেবে আউটপুট দেয়। বর্তমানে সমর্থিত: YouTube। ম্যানুয়ালি তৈরি সাবটাইটেলকে অগ্রাধিকার দেয়, এবং সেগুলো না থাকলে স্বয়ংক্রিয়ভাবে তৈরি সাবটাইটেলে ফিরে যায়।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: caf55e3434119acd935dad208f5461f7a08e72d34b595314abd52b58469cd299
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="video-transcriber banner">

# ভিডিও-ট্রান্সক্রিপ্টার

অনলাইন ভিডিও থেকে ট্রান্সক্রিপ্ট (সাবটাইটেল) এবং মেটাডেটা (শিরোনাম, চ্যানেল, তারিখ, ভিউ,
বিবরণ) সংগ্রহ করে। ম্যানুয়ালি তৈরি সাবটাইটেলকে অগ্রাধিকার দেওয়া হয়, এবং সেগুলো না থাকলে স্বয়ংক্রিয়ভাবে
তৈরি সাবটাইটেল ব্যবহার করা হয়। আউটপুট Markdown, JSON বা সাধারণ টেক্সট হিসেবে পাওয়া যায়।

প্রাথমিক পদ্ধতি (`youtube-transcript-api`) কোনো ফল না দিলে yt-dlp-মেটাডেটার মাধ্যমে একটি দ্বিতীয় পদ্ধতি স্বয়ংক্রিয়ভাবে কাজ
শুরু করে। এই পদ্ধতি শুধু সেই সাবটাইটেল ট্র্যাকটি পড়ে, যা প্ল্যাটফর্ম এমনিতেই প্লেব্যাকের জন্য সরবরাহ করে — **কোনো
ভিডিও বা অডিও ডাউনলোড হয় না**। কোন পদ্ধতি কাজ করেছে, তা JSON আউটপুটের `source` ক্ষেত্রে এবং stderr-এ দেখানো হয়।

প্রতিটি কাঙ্ক্ষিত ভাষার জন্য ফলব্যাক প্রথমে ম্যানুয়াল সঠিক ও বেস ভাষা কোডের ট্র্যাকগুলোকে, তারপর স্বয়ংক্রিয় সঠিক ও বেস ভাষা কোডের
ট্র্যাকগুলোকে অগ্রাধিকার দেয়; যেকোনো ট্র্যাক এর পরে আসে। একটি পড়া যায় না এমন JSON3 ট্র্যাক পেলে আরেকটি বিকল্প ট্র্যাক
উপলব্ধ থাকলে সংগ্রহ বন্ধ হয় না।

বর্তমানে সমর্থিত উৎস: **YouTube** (youtube.com, youtu.be, youtube-nocookie.com)।

ভিডিওর ক্ষেত্রে বিষয়বস্তু নিজে হাতে সারাংশ না লিখে এই টুল ব্যবহার করুন — ট্রান্সক্রিপ্টই নির্ভরযোগ্য উৎস।

> **দ্রষ্টব্য:** এই টুলটি YouTube বা Google-এর সঙ্গে সংযুক্ত নয় এবং তাদের দ্বারা সমর্থিত বা অনুমোদিতও নয়।
> ব্যবহার সম্পূর্ণ নিজের দায়িত্বে। সংশ্লিষ্ট প্ল্যাটফর্মের ব্যবহারের শর্তাবলী এবং প্রযোজ্য কপিরাইট মেনে চলার দায়িত্ব
> ব্যবহারকারীর নিজের। DRM, পেওয়াল বা প্রবেশাধিকার সীমাবদ্ধতা এড়ানো যাবে না; গণহারে তথ্য সংগ্রহ করা যাবে না;
> অধিকারধারীদের সম্মতি ছাড়া সুরক্ষিত ট্রান্সক্রিপ্ট পুনরায় প্রকাশ করা যাবে না।

## নির্ভরতা ও লাইসেন্স

```bash
pip install youtube-transcript-api   # Transkripte (Pflicht) — MIT-Lizenz
pip install yt-dlp                   # Metadaten (optional, Fallback: noembed) — Unlicense (Public Domain)
```


## ব্যবহার

> **Windows-এর দ্রষ্টব্য:** সবসময় `PYTHONIOENCODING=utf-8` সেট করুন, নাহলে আউটপুটে উমলাউট ও বিশেষ অক্ষর ভেঙে যাবে
> (cp1252-এনকোডিং)।

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


### বিকল্পসমূহ

| বিকল্প | প্রভাব |
|--------|---------|
| `--format markdown\|json\|plain` | আউটপুট ফরম্যাট (ডিফল্ট: markdown) |
| `--output, -o <datei>` | stdout-এর পরিবর্তে ফাইলে লেখা |
| `--lang <codes...>` | পছন্দের সাবটাইটেল ভাষা (ডিফল্ট: de en) |
| `--meta-only` | শুধু মেটাডেটা, কোনো ট্রান্সক্রিপ্ট নয় |
| `--transcript-only` | শুধু ট্রান্সক্রিপ্ট, কোনো মেটাডেটা নয় |
| `--no-timestamps` | সময়চিহ্ন ছাড়া ট্রান্সক্রিপ্ট |
| `--no-meta` | দ্রুততর: yt-dlp-মেটাডেটা এড়িয়ে যাওয়া |
| `--allow-empty-transcript` | খালি ট্রান্সক্রিপ্টকে সফল হিসেবে গণ্য করা (Exit 3-এর বদলে Exit 0) |

### Exit-কোড

একটি খালি ট্রান্সক্রিপ্ট **সফলতা নয়**। 1.2.0-এর আগে এই ক্ষেত্রে Exit 0 দিয়ে শেষ হতো: আউটপুট ফাইল লেখা হতো,
সেগমেন্ট-অ্যারে খালি থাকত, এবং প্রতিটি আহ্বানকারী স্বয়ংক্রিয় প্রক্রিয়া এটিকে সফল ধরে নিত। এই নীরব ব্যর্থতাই
সেই মূল ত্রুটি, যা 1.2.0 দূর করেছে।

| কোড | অর্থ |
|------|-----------|
| `0` | সফল — ট্রান্সক্রিপ্ট আছে, অথবা `--meta-only`, অথবা `--allow-empty-transcript` |
| `1` | বৈধ ভিডিও-URL/-ID নেই |
| `2` | আহ্বান-ত্রুটি (argparse দ্বারা নির্ধারিত, যেমন অজানা বিকল্প) |
| `3` | কোনো ট্রান্সক্রিপ্ট পাওয়া যায়নি — দুটি পদ্ধতিই খালি |

`2` argparse-এর জন্য সংরক্ষিত, যাতে আহ্বানের বানান ভুল এবং সাবটাইটেলবিহীন ভিডিও আলাদা করা যায়।

```bash
# In Skripten
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o out.md || {
  code=$?
  [ "$code" -eq 3 ] && echo "Video hat keine Untertitel" || echo "Fehler: $code"
}
```


### Python-লাইব্রেরি হিসেবে

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


দুটি পদ্ধতিই আলাদাভাবে আহ্বান করা যায়: `fetch_transcript_primary()` (শুধু
`youtube-transcript-api`) এবং `fetch_transcript_ytdlp()` (শুধু ফলব্যাক পদ্ধতি)। `fetch_transcript()` এদের একসঙ্গে যুক্ত করে এবং
`segments`, `language`, `is_generated`, `full_text`, `source` ক্ষেত্রগুলোর নিশ্চয়তা দেয়, ব্যর্থতার ক্ষেত্রে `error`-ও।

## সাধারণ ব্যবহারক্ষেত্র

- গবেষণা: ভিডিওর বিষয়বস্তু উদ্ধৃতিযোগ্য পাঠ্য হিসেবে বিশ্লেষণ
- উৎস-বিশ্লেষণ: বক্তৃতায় যুক্তি বা রূপক পরীক্ষা
- সারসংক্ষেপ: হ্যালুসিনেশনের বদলে ট্রান্সক্রিপ্টকে নির্ভরযোগ্য ভিত্তি হিসেবে ব্যবহার

## সীমাবদ্ধতা

- শুধু তখনই কাজ করে যখন ভিডিওতে সাবটাইটেল আছে (ম্যানুয়াল বা স্বয়ংক্রিয়)
- স্বয়ংক্রিয় সাবটাইটেলে শনাক্তকরণের ভুল থাকতে পারে
- কোনো অডিও ডাউনলোড নেই, নিজস্ব বক্তৃতা-শনাক্তকরণও নেই — ফলব্যাক পদ্ধতিও শুধু সাবটাইটেল ট্র্যাক লোড করে,
  কখনো ভিডিও বা অডিও নয়
- ফলব্যাক পদ্ধতির জন্য একটি JSON3 ট্র্যাক প্রয়োজন; প্ল্যাটফর্ম শুধু অন্য ফরম্যাট দিলে আংশিক আউটপুটের বদলে
  Exit 3-এ রান শেষ হয়

## পরিবর্তনের ইতিহাস

### 1.2.0 (2026-08-24)
- **Exit-আচরণ:** খালি ট্রান্সক্রিপ্ট নীরবে Exit `0`-এর বদলে Exit `3` দিয়ে শেষ হয়। অবৈধ URL এখন
  `1` হিসেবে নামকৃত ধ্রুবক। `--meta-only` সফল থাকে, কারণ সেখানে ট্রান্সক্রিপ্ট প্রত্যাশিত নয়।
- **নতুন বিকল্প `--allow-empty-transcript`:** খালি ট্রান্সক্রিপ্টকে ইচ্ছাকৃতভাবে সফল ধরে — যারা সাবটাইটেলকে ঐচ্ছিক মনে করে
  তাদের জন্য।
- **yt-dlp সাবটাইটেল-ফলব্যাক:** প্রাথমিক পদ্ধতি সেগমেন্ট না দিলেই কাজ শুরু করে (শুধু ব্যতিক্রম ঘটলে নয়)। `extract_info(download=False)`
  ব্যবহার করে এবং শুধু সাবটাইটেল URL পড়ে — কোনো ভিডিও নয়, কোনো অডিও নয়, প্রবেশাধিকার সীমাবদ্ধতা এড়ানো নয়।
- **ভাষা-নির্বাচন শক্তিশালী:** `de-orig`/`de-DE` `--lang de`-এর জন্য খুঁজে পাওয়া যায় (বেস ভাষা কোডের মিল)। ম্যানুয়াল সাবটাইটেল এখনও স্বয়ংক্রিয়গুলোর আগে।
- ফলাফলে **ক্ষেত্র `source`**: `youtube_transcript_api` বা `yt-dlp`।
- রিগ্রেশন টেস্ট: নকল উত্তর সহ 29টি টেস্ট (UTF-8, তিনটি আউটপুট ফরম্যাট, Exit-কোড, ভাষা-নির্বাচন, JSON3-পার্সিং)।

### 1.1.0 (2026-06-20)
- নাম পরিবর্তন: `yt-transcriber` → `video-transcriber` (YouTube-ব্র্যান্ড নির্দেশিকা: „yt" একটি স্পষ্টভাবে নিষিদ্ধ সংক্ষিপ্ত রূপ;
  সুপারিশ: RECHTSCHECK_2026-06-20.md)
- স্ক্রিপ্ট: `yt_transcriber.py` → `video_transcriber.py`
- দায়মুক্তি ও নির্ভরতার লাইসেন্স যোগ করা হয়েছে (ব্যবহারকারীর দায়িত্ব, ToS, কোনো অনুমোদন নেই)
- YouTube এখন শুধু বর্ণনামূলক উৎস-উল্লেখ, নাম বা ব্র্যান্ডের অংশ নয়
- পুরনো পথে সামঞ্জস্য-র‍্যাপার `yt_transcriber.py` রাখা হয়েছে

### 1.0.0 (2026-06-12)
- SKILL.md যোগ করা হয়েছে (টুলটি আগে থেকেই স্ক্রিপ্ট + README হিসেবে ছিল)
- স্ক্রিপ্ট v1.0.0: ট্রান্সক্রিপ্ট + মেটাডেটা, ৩টি আউটপুট ফরম্যাট, ভাষার পছন্দ
