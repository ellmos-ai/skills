---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "स्टोरीलाइन JSON से स्थानीय waveform synthesis (numpy + ffmpeg) द्वारा वीडियो-सिंक्रोनाइज़्ड बैकग्राउंड संगीत की रचना करता है। शैलियाँ: Chiptune, Ambient, Electronic। नियतात्मक, ऑफ़लाइन, कोई क्लाउड सेवा नहीं।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: hi
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
translated_at: "2026-10-15T12:49:14.059080+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

वीडियो के नाटकीय चाप का अनुसरण करने वाला एक बैकग्राउंड स्कोर पूरी तरह स्थानीय रूप से रचता है:
numpy waveform synthesis (ऑसिलेटर, ADSR, लेयरिंग, delay-reverb) + MP3 एन्कोडिंग के लिए ffmpeg। कोई सैंपल नहीं,
कोई MIDI हार्डवेयर नहीं, कोई क्लाउड API नहीं।

## कब उपयोग करें

- किसी वीडियो/पॉडकास्ट को ऐसे बैकग्राउंड संगीत की ज़रूरत है जो कहानी के बीट्स को सटीक टाइमस्टैम्प पर मिलाए
  (ओपनिंग, तनाव की घाटी, ड्राइव खंड, चरमोत्कर्ष, outro)।
- एक नियतात्मक, दोबारा रेंडर होने योग्य स्कोर चाहिए (वही seed → वही ऑडियो)।
- Chiptune, Ambient या Electronic शैलियाँ स्वीकार्य हैं।

## कब उपयोग न करें (ईमानदार शैली-सीमाएँ)

Waveform synthesis **Chiptune, Ambient और Electronic** बैकग्राउंड बेड दे सकता है। वह अपने अंतर्निर्मित synth से
**Pop, Rock, Classical या Orchestra फ़िल्म संगीत** नहीं दे सकता — परंतु व्यवस्था (arrangement) backend-neutral है:
नीचे "Waveform synthesis से आगे" देखें, ताकि वही रचना SoundFonts, orchestral libraries या बाहरी generation के
माध्यम से रेंडर हो सके।

## प्रक्रिया: Storyline → Score

संदर्भ स्कोर (179.5 s, C minor) में जैसे पुनर्निर्मित किया गया:

1. **कहानी के acts को संगीत खंडों पर मैप करें।** जो acts एक भावनात्मक अवस्था साझा करते हैं, वे एक खंड में मिल जाते हैं
   (संदर्भ: 7 acts → 5 खंड; acts 1–3 एक ही 62-s शांत ओपनिंग बने)। हर खंड को सेकंड में सटीक
   `start`/`end` मिलता है।
2. **प्रत्येक खंड को emotion + intensity दें।**
   - *Emotion* chord progression चुनता है (scale degrees, minor उदाहरण):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V harmonic-minor major है)।
   - *Intensity* (0–1) tempo की अनुभूति (BPM), layer count और volume ramp चलाती है। Layers इन thresholds पर
     जुड़ती हैं: pads हमेशा → विरल घंटियाँ (<0.3) → arp (≥0.25) → bass (≥0.4) → lead (≥0.45) →
     drums (≥0.5) → drive extras (≥0.65) → pad octave doubling (≥0.85)।
3. **विशेष events को timeline पर रखें।**
   - `damp`: Gaussian volume duck — `1 - depth · exp(-((t-T)²)/(2σ²))`।
     संदर्भ: depth 0.5, σ 1 s पर T=84 s, बोले गए beat
     "Two databases. Same cluster." (~1:24) पर।
   - `climax`: एक समय-खिड़की जो पूरी layering, शिखर volume, octave-doubled pads लागू करती है
     (संदर्भ: 154–170 s = 2:34–2:50, 2D→3D morph पर)।
   - `outro`: अपने आरंभ से drums/bass/lead हट जाते हैं और घंटियाँ 20% तक फ़ेड होती हैं
     (संदर्भ: 170–179.5 s, end-credit card)।
4. **जोड़ना (stitching)।** खंड सीमाओं पर raised-cosine smoothing (~2.5 s), वैश्विक fade-in/-out,
   feedback delay-reverb (100 ms, decay 0.25), tanh drive + peak normalization एक बैकग्राउंड स्तर तक
   (मापा गया संदर्भ master: औसत ≈ −22 dB, अधिकतम ≈ −1.6 dB)।
5. **Voiceover के पीछे रहें।** "background" चिह्नित खंड अपने volume ramp को सीमित करते हैं; स्कोर एक बेड है, lead नहीं।

## उपयोग

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

आउटपुट: `score.wav` (stereo 16-bit 44.1 kHz), `score.mp3` (192k, ffmpeg PATH में होना चाहिए;
अन्यथा चेतावनी के साथ छोड़ दिया जाता है), `score.notes.json` (arrangement/नोट लॉग: हर रखे गए नोट का समय, layer,
MIDI pitch, अवधि, velocity) और `score.mid` — एक वास्तविक **Standard MIDI File** (Type 1:
tempo track जिसमें हर खंड के लिए एक tempo event है, नोट track जिसमें हर शैली के लिए GM program hints हैं,
drums GM channel 10 पर)। यह बिना किसी निर्भरता के लिखी गई है; pretty_midi/mido की आवश्यकता नहीं।

नियतात्मकता: वही storyline + वही `seed` → byte-identical WAV।

## Storyline JSON संदर्भ

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

- `duration` (अनिवार्य, सेकंड), `sections` (अनिवार्य, ≥1, क्रमबद्ध,
  अतिव्यापी नहीं, अवधि के भीतर)।
- खंड फ़ील्ड: `start`, `end` (अनिवार्य); `emotion` ∈ calm | tense |
  alive | driving | epic | outro; `intensity` 0–1 (emotion के अनुसार डिफ़ॉल्ट);
  `bpm` (डिफ़ॉल्ट: वैश्विक `bpm`); `melody` (वैकल्पिक MIDI सूची, चक्रीय;
  अन्यथा scale tones पर seeded random walk बनता है)।
- `key`: नोट नाम (C, C#, Db, …), `mode`: minor | major।
- `style`: chiptune | ambient | electronic (नीचे देखें)।
- Event `damp`: `time` (s), `depth` 0–1, `width` = सेकंड में σ।
- Fades/Crossfade/Peak/Drive/Reverb के डिफ़ॉल्ट ऊपर दिखाए अनुसार; सभी वैकल्पिक।

पूर्ण गणना किया गया उदाहरण (संदर्भ वीडियो का पुनर्निर्माण):
[`example-storyline.json`](example-storyline.json) — एक 179.5-s स्कोर रेंडर करता है जो मूल के master level से मेल खाता है
(औसत ≈ −22 dB, अधिकतम ≈ −1.6 dB)।

## शैली Presets

| शैली | Lead | Bass/Arp | Drums | चरित्र |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle bass, तेज़ square arps | Noise-आधारित kick/hat/snare | Retro कंसोल, arpeggio-प्रधान (संदर्भ शैली) |
| `ambient` | नरम triangle/sine | धीमे arps, long-attack pads | केवल intensity ≥ 0.75 पर | विरल, घंटी-प्रधान, चौड़ा reverb अहसास |
| `electronic` | sawtooth + detune + sub | दमदार bass, saw arps | पूरा kit | ड्राइविंग EDM-निकट बेड |

## Waveform synthesis से आगे: बेहतर Sound Backends

उल्लिखित शैली-सीमा **sound backend की है, रचना की नहीं**। Storyline→Score प्रक्रिया एक backend-neutral
arrangement बनाती है; साथ दिया गया numpy synth केवल निःशुल्क offline डिफ़ॉल्ट renderer है। हर रन अतिरिक्त
रूप से एक Standard MIDI File (`<out>.mid`) लिखता है — बेहतर instruments से रेंडर करें:

- **पथ A — SoundFont (अनुशंसित: स्थानीय, निःशुल्क, कोई क्लाउड नहीं)।**
  FluidSynth इंस्टॉल करें (fluidsynth.org, Windows: `winget install FluidSynth`)
  और एक निःशुल्क GM SoundFont (GeneralUser GS, S. Christian Collins द्वारा, या MuseScore_General.sf2)।
  फिर: `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3 ffmpeg के माध्यम से। इससे Pop/Rock band ध्वनियाँ, पियानो, सरल स्ट्रिंग्स खुलते हैं।
- **पथ B — ऑर्केस्ट्रा/फ़िल्म।** निःशुल्क orchestral libraries: VSCO 2 Community Edition, Soni Musicae,
  Salamander Grand Piano। बेहतर स्ट्रिंग्स/ब्रास, अधिक महाकाव्यात्मक। ईमानदार संकेत: articulation और
  humanization (velocity variation, legato, dynamic curves) सैंपल सेट से अधिक मायने रखते हैं — और वास्तविक
  फ़िल्म-स्कोर महाकाव्यता के लिए अतिरिक्त arrangement परिपक्वता चाहिए; अकेला backend पर्याप्त नहीं।
- **पथ C — बाहरी AI generation (Suno आदि)।** संभव है, पर डेटा-गोपनीयता/अधिकार के प्रश्न उठाता है — केवल
  उपयोगकर्ता की स्पष्ट सहमति से, कभी डिफ़ॉल्ट के रूप में नहीं।

योजनाबद्ध, परंतु **अभी लागू नहीं**: engine में `humanize` विकल्प (हर नोट पर velocity/timing jitter), ताकि
sample-आधारित रेंडरिंग यांत्रिक न लगे (engine docstring में TODO के रूप में चिह्नित)।

## सीमाएँ

- अंग्रेज़ी और जर्मन storyline टिप्पणियाँ समस्या नहीं हैं; keys/values स्थायी रूप से अंग्रेज़ी हैं।
- बहुत छोटी अवधि (< ~10 s) काम करती है, परंतु नाटकीयता सिकुड़ जाती है (fades और crossfades स्वतः 20% अवधि /
  सबसे छोटे खंड के 50% तक सीमित हो जाते हैं)।
- नोट लॉग (`*.notes.json`) विश्लेषण-अनुकूल डेटासेट है; `*.mid` फ़ाइल DAWs/SoundFont renderers
  के लिए आदान-प्रदान प्रारूप है (GM program numbers मोटे शैली-संकेत हैं — अपनी पसंद अनुसार remap करें)।
