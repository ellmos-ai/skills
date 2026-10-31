---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "স্টোরিলাইন JSON থেকে ভিডিও-সিঙ্ক্রোনাইজড ব্যাকগ্রাউন্ড মিউজিক তৈরি করে, স্থানীয় ওয়েভফর্ম সিন্থেসিসের মাধ্যমে (numpy + ffmpeg)। স্টাইল: Chiptune, Ambient, Electronic। ডিটারমিনিস্টিক, অফলাইন, কোনো ক্লাউড সার্ভিস নেই।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: bn
status: stable
visibility: public
dependencies:
  tools: [ffmpeg]
  services: []
  protocols: []
  python: [numpy]
provenance:
  origin: local-reconstruction
  origin_license: MIT
  notes: >
    Verfahren rekonstruiert aus einem video-synchronisierten Score, komponiert
    für ein 179,5-s-Erklärvideo (5 Musikabschnitte aus 7 Story-Akten
    gemappt). Kanonische Engine: ai-media-editor-Repo, tools/compose_music.py
    (github.com/ellmos-ai/ai-media-editor). Eine eigenständige Kopie liegt
    hier für Offline-Nutzung bei.
translated_from_sha256: 4920ef9c05d0ed853c0ddf7723ca56bac953af15b025feb2f32bdbc8c446fc23
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

ভিডিওর নাটকীয় চাপের রূপরেখা অনুসরণ করে একটি ব্যাকগ্রাউন্ড স্কোর তৈরি করে, সম্পূর্ণ স্থানীয়ভাবে: numpy-ওয়েভফর্ম সিন্থেসিস (অসিলেটর, ADSR, লেয়ারিং, Delay-Reverb) + MP3 এনকোডিংয়ের জন্য ffmpeg। কোনো স্যাম্পল নয়, কোনো MIDI হার্ডওয়্যার নয়, কোনো ক্লাউড API নয়।

## কখন ব্যবহার করবেন

- কোনো ভিডিও/পডকাস্টে এমন ব্যাকগ্রাউন্ড মিউজিক দরকার, যা স্টোরি-বিটগুলোকে সঠিক টাইমস্ট্যাম্পে মেলায় (Opening, উত্তেজনার ভাটা, Drive-অংশ, Climax, Outro)।
- একটি ডিটারমিনিস্টিক, পুনরায়-রেন্ডারযোগ্য স্কোর দরকার (একই seed → একই অডিও)।
- Chiptune-, Ambient- বা Electronic-স্টাইল গ্রহণযোগ্য।

## কখন ব্যবহার করবেন না (সৎ genre-সীমাবদ্ধতা)

ওয়েভফর্ম সিন্থেসিস **Chiptune-, Ambient- ও Electronic**-ব্যাকগ্রাউন্ড বেড দিতে পারে। এর অন্তর্নির্মিত synth দিয়ে এটি **Pop, Rock, ক্লাসিক্যাল বা Orchestra-ফিল্মমিউজিক** দিতে পারে না — তবে arrangement backend-নিরপেক্ষ: একই কম্পোজিশন SoundFont, Orchestra-লাইব্রেরি বা বাইরের জেনারেশনের মাধ্যমে রেন্ডার করতে নিচের "ওয়েভফর্ম-সিন্থেসিসের বাইরে" অংশটি দেখুন।

## পদ্ধতি: Storyline → Score

রেফারেন্স স্কোর (179,5 s, C-minor) যেভাবে পুনর্গঠিত হয়েছিল:

1. **স্টোরি-Act গুলোকে মিউজিক-সেকশনে ম্যাপ করুন।** যে Act গুলো একই মানসিক অবস্থা ভাগ করে, সেগুলো একটি সেকশনে মিশে যায় (রেফারেন্স: 7 Act → 5 সেকশন; Act 1–3 মিলে একটি 62-s শান্ত Opening তৈরি করে)। প্রতিটি সেকশন সেকেন্ডে `start`/`end` পায়।
2. **প্রতিটি সেকশনে Emotion + Intensity নির্ধারণ করুন।**
   - *Emotion* কর্ড-প্রোগ্রেশন বেছে নেয় (স্কেল-ডিগ্রি, মাইনর-উদাহরণ):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V হলো হারমনিক-মাইনর মেজর কর্ড)।
   - *Intensity* (0–1) টেম্পোর অনুভূতি (BPM), লেয়ার-সংখ্যা এবং ভলিউম-র‍্যাম্প চালায়। থ্রেশহোল্ডে লেয়ার যোগ হয়: Pads সবসময় → বিরল ঘণ্টা (<0,3) → Arp (≥0,25) → Bass (≥0,4) → Lead (≥0,45) → Drums (≥0,5) → Drive-Extras (≥0,65) → Pad-অষ্টাভ-ডাবলিং (≥0,85)।
3. **টাইমলাইনে বিশেষ ইভেন্ট বসান।**
   - `damp`: Gauß-আকৃতির ভলিউম-Duck — `1 - depth · exp(-((t-T)²)/(2σ²))`।
     রেফারেন্স: depth 0,5, σ 1 s, T=84 s-এ, কথিত বিট "Two databases. Same cluster." ("দুটি ডেটাবেস। একই ক্লাস্টার।", ~1:24)-এ।
   - `climax`: একটি সময়-উইন্ডো যা পূর্ণ লেয়ারিং, সর্বোচ্চ ভলিউম এবং অষ্টাভ-ডাবলড Pads বাধ্য করে (রেফারেন্স: 154–170 s = 2:34–2:50, 2D→3D মরফের সময়)।
   - `outro`: এর শুরু থেকে Drums/Bass/Lead বাদ পড়ে এবং ঘণ্টাগুলো 20%-এ নেমে আসে (রেফারেন্স: 170–179,5 s, ক্রেডিট-কার্ড)।
4. **জোড়া লাগান।** সেকশন-সীমায় Raised-Cosine-স্মুথিং (~2,5 s), গ্লোবাল Fade-in/-out, Feedback-Delay-Reverb (100 ms, Decay 0,25), Tanh-Drive + ব্যাকগ্রাউন্ড-লেভেলে পিক নরমালাইজেশন (পরিমাপ করা রেফারেন্স-মাস্টার: গড় ≈ −22 dB, সর্বোচ্চ ≈ −1,6 dB)।
5. **ভয়েসওভারের পেছনে থাকুন।** "background" (ব্যাকগ্রাউন্ড) হিসেবে চিহ্নিত সেকশনগুলো তাদের ভলিউম-র‍্যাম্প সীমাবদ্ধ করে; স্কোরটি একটি বেড, লিড নয়।

## ব্যবহার

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

আউটপুট: `score.wav` (Stereo 16-bit 44,1 kHz), `score.mp3` (192k, PATH-এ ffmpeg দরকার; না থাকলে সতর্কবার্তাসহ এড়িয়ে যাওয়া হয়), `score.notes.json` (arrangement-/নোট-লগ: প্রতিটি বসানো নোট সময়, লেয়ার, MIDI-পিচ, দৈর্ঘ্য, Velocity সহ) এবং `score.mid` — একটি আসল **Standard-MIDI-ফাইল** (টাইপ 1: প্রতি সেকশনে একটি টেম্পো-ইভেন্টসহ টেম্পো-ট্র্যাক, স্টাইল অনুযায়ী GM-প্রোগ্রাম-হিন্ট সহ নোট-ট্র্যাক, GM-চ্যানেল 10-এ Drums)। কোনো নির্ভরতা ছাড়া লেখা; pretty_midi/mido লাগে না।

ডিটারমিনিজম: একই storyline + একই `seed` → বাইট-অভিন্ন WAV।

## Storyline-JSON রেফারেন্স

```json
{
  "title": "my-score",
  "duration": 179.5,
  "bpm": 100,
  "key": "C",
  "mode": "minor",
  "style": "chiptune",
  "seed": 42,
  "fade_in": 3.0,
  "fade_out": 5.0,
  "crossfade": 2.5,
  "peak": 0.85,
  "drive": 2.0,
  "reverb": {"delay_ms": 100, "decay": 0.25},
  "sections": [
    {"start": 0.0, "end": 62.0, "emotion": "calm", "intensity": 0.18, "bpm": 60,
     "comment": "optional note"},
    {"start": 62.0, "end": 88.0, "emotion": "tense", "intensity": 0.4, "bpm": 72}
  ],
  "events": [
    {"type": "damp", "time": 84.0, "depth": 0.5, "width": 1.0},
    {"type": "climax", "start": 154.0, "end": 170.0},
    {"type": "outro", "start": 170.0}
  ]
}
```

- `duration` (বাধ্যতামূলক, সেকেন্ড), `sections` (বাধ্যতামূলক, ≥1, সাজানো, ওভারল্যাপহীন, সময়কালের ভেতরে)।
- সেকশন-ফিল্ড: `start`, `end` (বাধ্যতামূলক); `emotion` ∈ calm | tense | alive | driving | epic | outro; `intensity` 0–1 (Emotion অনুযায়ী ডিফল্ট); `bpm` (ডিফল্ট: গ্লোবাল `bpm`); `melody` (ঐচ্ছিক MIDI-তালিকা, চক্রাকার; নয়তো স্কেল-টোনের উপর seed-করা Random Walk তৈরি হয়)।
- `key`: নোটের নাম (C, C#, Db, …), `mode`: minor | major।
- `style`: chiptune | ambient | electronic (নিচে দেখুন)।
- ইভেন্ট `damp`: `time` (s), `depth` 0–1, `width` = সেকেন্ডে σ।
- Fades/Crossfade/Peak/Drive/Reverb-এর ডিফল্ট মান উপরে দেখানো মতোই; সবগুলো ঐচ্ছিক।

সম্পূর্ণ হিসাব-করা উদাহরণ (রেফারেন্স ভিডিওর পুনর্গঠন): [`example-storyline.json`](example-storyline.json) — একটি 179,5-s স্কোর রেন্ডার করে, যা মূল ভিডিওর মাস্টার-লেভেলের সঙ্গে মেলে (গড় ≈ −22 dB, সর্বোচ্চ ≈ −1,6 dB)।

## স্টাইল-প্রিসেট

| স্টাইল | Lead | Bass/Arp | Drums | চরিত্র |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle bass, দ্রুত square arps | Noise-ভিত্তিক Kick/Hat/Snare | Retro-কনসোল, arpeggio-চালিত (রেফারেন্স স্টাইল) |
| `ambient` | নরম triangle/sine | ধীর Arps, Long-Attack-Pads | কেবল Intensity ≥ 0,75 থেকে | বিরল, ঘণ্টা-কেন্দ্রিক, প্রশস্ত Reverb-অনুভূতি |
| `electronic` | sawtooth + detune + sub | জোরালো Bass, saw Arps | পূর্ণ Kit | EDM-ঘেঁষা চালিত বেড |

## ওয়েভফর্ম-সিন্থেসিসের বাইরে: ভালো Sound-Backend

উল্লিখিত genre-সীমা **Sound-Backend-এর, কম্পোজিশনের নয়**। Storyline→Score পদ্ধতি একটি backend-নিরপেক্ষ arrangement তৈরি করে; সঙ্গে দেওয়া numpy-Synth কেবল বিনামূল্যের অফলাইন ডিফল্ট রেন্ডারার। প্রতিটি রানে অতিরিক্তভাবে একটি Standard-MIDI-ফাইল (`<out>.mid`) লেখা হয় — ভালো যন্ত্র দিয়ে রেন্ডার করতে:

- **পথ A — SoundFont (প্রস্তাবিত: স্থানীয়, বিনামূল্যে, কোনো ক্লাউড নেই).**
  FluidSynth ইনস্টল করুন (fluidsynth.org, Windows: `winget install FluidSynth`) এবং একটি বিনামূল্যের GM-SoundFont (GeneralUser GS, S. Christian Collins-এর; অথবা MuseScore_General.sf2)। তারপর:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3 ffmpeg দিয়ে। এতে Pop-/Rock-ব্যান্ডের শব্দ, পিয়ানো, সরল স্ট্রিংস খুলে যায়।
- **পথ B — Orchestra/ফিল্ম।** বিনামূল্যের অর্কেস্ট্রা-লাইব্রেরি: VSCO 2 Community Edition, Soni Musicae, Salamander Grand Piano। আরও ভালো স্ট্রিংস/ব্রাস, আরও মহাকাব্যিক। সৎ সতর্কতা: আর্টিকুলেশন ও হিউম্যানাইজেশন (ভেলোসিটি-ভিন্নতা, লেগাটো, ডায়নামিক কার্ভ) স্যাম্পল-সেটের চেয়ে বেশি গুরুত্বপূর্ণ — এবং প্রকৃত ফিল্মস্কোরের মহাকাব্যিকতার জন্য arrangement-পরিপক্বতাও লাগে; কেবল একটি backend যথেষ্ট নয়।
- **পথ C — বাইরের AI-জেনারেশন (Suno ইত্যাদি).** সম্ভব, তবে ডেটা-গোপনীয়তা/অধিকারের প্রশ্ন তোলে — কেবল ব্যবহারকারীর স্পষ্ট অনুমোদনে, কখনো ডিফল্ট হিসেবে নয়।

পরিকল্পিত, তবে **এখনও বাস্তবায়িত নয়**: ইঞ্জিনে একটি `humanize`-অপশন (প্রতি নোটে Velocity-/Timing-Jitter), যাতে স্যাম্পল-ভিত্তিক রেন্ডারিং যান্ত্রিক না শোনায় (ইঞ্জিন-Docstring-এ TODO হিসেবে চিহ্নিত)।

## সীমাবদ্ধতা

- ইংরেজি ও জার্মান storyline-মন্তব্য সমস্যা নয়; Keys/Values স্থিরভাবে ইংরেজি।
- খুব ছোট সময়কাল (< ~10 s) কাজ করে, তবে নাটকীয়তা সংকুচিত করে (Fades ও Crossfade স্বয়ংক্রিয়ভাবে সময়কালের 20% / সবচেয়ে ছোট সেকশনের 50%-এ সীমাবদ্ধ হয়)।
- নোট-লগ (`*.notes.json`) বিশ্লেষণ-বান্ধব ডেটাসেট; `*.mid`-ফাইল DAW/SoundFont-রেন্ডারারের জন্য বিনিময় ফরম্যাট (GM-প্রোগ্রাম-নম্বর মোটা স্টাইল-হিন্ট — পছন্দমতো রিম্যাপ করুন)।
