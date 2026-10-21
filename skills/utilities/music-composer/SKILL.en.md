---
name: music-composer
version: 1.1.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-10-18
description: >
  Compose video-synced background music with local synthesis (numpy + scipy,
  ffmpeg optional). Recommended: the score mode (a hand-written score on the
  speech time axis, fixed level steps without ducking, a novelty proof against
  earlier pieces). Alongside it the fast storyline mode as a sketch (chiptune,
  ambient, electronic). Deterministic, offline, no samples, no cloud service.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, partitur, chiptune, ambient, electronic, video-sync, waveform-synthesis, fm-synthesis, loudness]
language: en
status: stable
visibility: public
dependencies:
  tools: [ffmpeg]
  services: []
  protocols: []
  python: [numpy, scipy]
provenance:
  origin: local-reconstruction
  origin_license: MIT
  notes: >
    Storyline mode: method reconstructed from a video-synced score composed for
    a 179.5 s explainer video (5 music sections mapped from 7 story acts).
    Canonical engine: ai-media-editor repo, tools/compose_music.py
    (github.com/ellmos-ai/ai-media-editor). A standalone copy is bundled here
    for offline use. Score mode (score/): generalised from the scoring of a
    demo video (hand-written score, own synthesis, level steps derived from
    measurement); project data was removed, the example speech map and the
    example score are neutral.
---

<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Score → Audio (recommended) and Storyline → Score (sketch)

Compose background music for video or podcast, fully local: own synthesis with
numpy/scipy (FM brass, modal marimba/glockenspiel, Karplus-Strong pizzicato,
chip waves, percussion, synthetic reverb), no samples, no MIDI hardware, no
cloud API. Two modes:

| | Score mode (`score/`) | Storyline mode (`compose_music.py`) |
|---|---|---|
| Role | **Recommended for video music** | Fast sketch mode |
| Input | Speech map (JSON) + hand-written score (Python) | Storyline JSON (sections, emotion, intensity) |
| Structure | Chords per bar, written-out melody phrases, accompaniment figures per scene | Template: chord progression per emotion, four-note figures from a seeded random walk |
| Time axis | The voice: scene cut = section change = downbeat | Section timestamps |
| Levels | Fixed step per speech window and pause, derived from measurement, no ducking | Volume ramp per section, peak normalisation |
| Dependencies | numpy, scipy (ffmpeg only as an optional cross-check) | numpy (ffmpeg only for MP3) |
| Limit | The score has to be written | Same template → across projects it sounds like the same song (see "Storyline mode") |

## When to use

- **Score mode:** video music that should be perceived as a piece of its own:
  melody in the speech pauses, accompaniment under the voice, levels to a
  specification, variant comparison with evidence.
- **Storyline mode:** a fast, deterministic score draft that hits story beats at
  exact timestamps (opening, tension dip, drive section, climax, outro);
  chiptune, ambient or electronic styles are acceptable.

## When NOT to use (honest genre limits)

Waveform synthesis can deliver **chiptune, ambient and electronic** background
beds, and in score mode additionally a brass march and marimba, flute and
glockenspiel pieces. It cannot deliver **pop, rock, classical or orchestral film
music** with its built-in synth — but the arrangement is backend-neutral: see
"Beyond waveform synthesis" below.

# Score mode (recommended)

A real, composed-out score instead of a template: the agent writes chords per bar
and the melody phrases by hand (Python data), and `score/` turns them into notes,
audio, MIDI and level measurements.

## Workflow

All paths are relative to this skill folder.

```bash
# 1. Build a speech map from narration clips (or write it by hand, schema below)
python score/timeline.py --timeline timeline.json --narration-dir clips/ -o speech-map.json [--extend-last-scene 2.0]

# 2. Bar grid / spotting sheet: bars per scene, start time, speech (#) and pause (.) per beat
python score/grid.py --speech-map speech-map.json --bpm 116 --beats-per-bar 2

# 3. Write the score (template: score/examples/march.py), validate in seconds - writes nothing
python score/build.py --speech-map speech-map.json --variant my_score.py --check

# 4. Build; the target folder must be new or empty, otherwise the run aborts
python score/build.py --speech-map speech-map.json --variant my_score.py --out out/v1 \
    --narration-dir clips/ --compare earlier/notes.json other.notes.json

# 5. Check: formats/length/MIDI, piano roll + spectrogram as PNG
python score/check.py out/v1 --duration 180.6
python score/viz.py out/v1 --speech-map speech-map.json
```

Without narration the build still runs (leave out `--narration-dir`): the speech
is then assumed to sit at −16 LUFS already, and no `preview-mix.wav` is written.
Complete example with the neutral example map (42 s, four scenes, a march in
B-flat major, 2/4):

```bash
python score/build.py --speech-map score/examples/speech-map.json \
    --variant score/examples/march.py --out out/march
```

Outputs of each build (everything in `--out`):

| File | Content |
|---|---|
| `music.wav` | Music alone, 48 kHz, stereo, 24 bit, full length, fixed level steps applied |
| `preview-mix.wav` | Narration + music, normalised to −16 LUFS, ≤ −1.5 dBTP (only with `--narration-dir`) |
| `score.mid` | Standard MIDI File (type 1, tempo and time-signature track, GM programs) |
| `score.json`, `notes.json` | Score and note ledgers (every note with time, bar, beat, voice, velocity) |
| `levels.json` | Level steps and measurements per segment (own BS.1770 meter, ffmpeg cross-check if available) |
| `novelty.json` | Novelty proof (interval n-grams of the melody against `--compare`) |
| `ARRANGEMENT.md` | Idea, motif, harmony, instrumentation, sections, levels, novelty (texts from the score's `DOC`) |
| `qa/pianoroll.png`, `qa/spectrogram.png` | from `viz.py`: notes over the speech windows, spectrum with 1–4 kHz markers |

The run is deterministic (fixed noise keys). Tools in `score/`:

| File | Job |
|---|---|
| `timeline.py` | Build, load and check the speech map from a scene timeline and narration clips |
| `grid.py` | Bar grid per scene and spotting sheet |
| `engine.py` | Score → notes → audio/MIDI, level steps, BS.1770 meter, limiter |
| `synth.py` | Sound generators (see below), synthetic reverb |
| `build.py` | Build one piece completely, ledgers, novelty proof, `ARRANGEMENT.md` |
| `check.py`, `viz.py` | Acceptance check (no ffmpeg needed), piano roll and spectrogram |
| `analyze_ref.py` | Rough analysis of a reference recording (tempo, pitch classes), for comparison only |
| `examples/` | Neutral example speech map and example score `march.py` |

## The speech map: the voice is the time axis

`speech-map.json` (example: `score/examples/speech-map.json`):

```json
{"duration": 42.0,
 "scenes": [{"id": "intro", "start": 0.0, "end": 8.3}, {"id": "problem", "start": 8.3, "end": 19.2}],
 "voices": [{"id": "v1_intro", "clip_start": 0.7, "clip_dur": 4.7, "speech_start": 0.8, "speech_end": 5.2}],
 "pauses": [{"start": 5.2, "end": 9.05, "len": 3.85, "before": "v2_problem"}]}
```

- `scenes`: contiguous, the last one ends at `duration`; one scene = one section of the score (picture cut = section change).
- `voices`: speech windows (first to last audible moment of each narration clip); `clip_start`/`clip_dur` place the clip for the mix (`<voice id>.wav` in `--narration-dir`, 48 kHz).
- `pauses` (optional, derived from the speech windows): gaps between the windows; `before` is the id of the next voice, `"END"` for the gap after the last word.
- `timeline.py` builds the map from `timeline.json` (`{"duration", "scenes": [{"id","start","duration"}], "voices": [{"id","start"}]}`) and the clips; speech window = activity threshold −50 dBFS. `--extend-last-scene` lengthens the last scene (e.g. a longer end card).

`grid.py` gives every scene whole bars and bends the tempo slightly per scene
(the deviation is printed in the grid) so that **every cut falls on a downbeat**;
a remainder is written as a short closing bar before the cut. The score must
have exactly as many chord bars per scene as the grid reports.

## Writing the score

A score is a Python file with `SCORE` (and optionally `DOC` for `ARRANGEMENT.md`).
The complete format dictionary is the header comment of
[`score/examples/march.py`](score/examples/march.py); in short:

| Building block | Syntax |
|---|---|
| Chord chart `chords` | Bars separated by `\|`, chord symbols per bar (`Bb`, `Gm`, `Cm7`, `F7`, `Fsus4`, `Ebmaj7`, `Bb/D`); lengths in beats: `Cm7:1 F7:1` |
| Phrase `(voice, "bar:beat", "tokens", velocity)` | `Bb4:.5` note with length in beats, `r:.5` rest, `\|` bar line (checked), `g:A4` grace note, `D5<` reversed envelope, `F5~:1` trill, `Bb5*:2` rings out (final chord), `x`/`X` soft/hard hit (percussion) |
| Accompaniment `default_parts` / `parts` | `dict(inst=…, pattern=[(offset, length, spec, velocity)], range=(low, high), voices=3, when="speech"\|"pause", bars=(first, last), drum=True, guide=True)`; spec: `R` root, `5`/`3`/`7`, `app` chromatic approach, `v` chord voicing, `a0`… arpeggio, `+12` octave |
| Voices `instruments` | `dict(fn=synth.…, opt={…}, pan, send, gain, fg=True, drum=<GM note>, program=<GM program>)`; `fg=True` marks melody voices |

Sound generators in `score/synth.py`: `chip_pulse`, `chip_tri`, `chip_hat`,
`chip_snare`, `chip_kick` (8-bit); `marimba`, `glock`, `pizz` (Karplus-Strong),
`flute` (also ocarina), `shaker`, `woodblock`, `framedrum` (acoustic-sounding);
`fm_brass`, `fm_bell`, `snare`, `bdrum`, `cymbal` (brass and march). New voices:
add a function `f(freq, dur, vel, bright, …)` (percussion `f(vel, bright)`) to
`synth.py`.

## Rules for good video music

- **Write two or three variants** and spread them over character and instrumentation
  (another key, another time signature, another motif, other voices) instead of
  iterating on one version. Examples of the spread: an 8-bit quest theme in D major
  4/4 (pulse and triangle waves), a cosy 6/8 village square in F major (marimba,
  plucked bass, flute), a light B-flat march (FM brass, tuba, snare); only the march
  ships as an example score. One score file and one output folder per variant.
- **The voice is the time axis:** scene change in the picture = section change in
  the music; the motif is played **in the speech pauses** (intro, title card,
  scene transitions, ending), not under the voice. Pauses of 1.3 s and more count
  as foreground; melody voices (`fg=True`) must not reach more than 0.12 s into a
  word (`build.py` reports every overlap).
- **Accompaniment register under speech:** middle register (e.g. MIDI 53–67), few
  overtones (`bright_speech` per accompaniment figure, default 0.3), a bed of
  oom-pah, off-beats, held chords or a quiet counter line (`guide=True`); the
  1–4 kHz band stays largely free. Measure it: `levels.json` →
  `midband_1_4khz_share_pct.under_speech` (as close to 0 as possible).
- **Ending:** after the last word a motif or cadence, then a final chord
  (`Bb5*:2`) that rings out freely; the accompaniment stops in the bar before it
  (`bars=(1, <bar before the final chord>)`).
- **Write anew instead of reusing:** compose melody and chord progression anew
  for each project; a carried-over template is the reason pieces sound like "the
  same song".
- **Purely synthetic:** no foreign samples, no SoundFonts, no downloads, no music
  AI service, no quotations of known melodies. This keeps the piece its own and
  the rights question trivial.

## Levels without ducking

A fixed gain per section instead of sidechain or carving:

- **Bed under speech:** about 20 LU below the speech, ≈ −36 LUFS (±2) at a
  −16 LUFS overall mix.
- **Foreground in pauses without speech:** at most −24 LUFS (target −24.5 LUFS
  from a 3 s pause). Shorter transition pauses sit 2.5 dB lower per missing
  second (at most 4 dB) so that nothing pumps between two sentences; the final
  chord after the last word gets the full step.
- **Ramps end before the first word:** up at most 0.35 s after the speech ends,
  down at most 0.8 s and 0.1 s before the next word; the fade-in takes up to
  0.55 s and ends 0.08 s before the first word. The final sound rings out at a
  fixed step (only 0.15 s of click guard at the very end).
- **How:** every step is derived from the measured music (`gain = target − LUFS`),
  re-measured three times with the ramps in place and corrected; the whole mix is
  then brought linearly to −16 LUFS. A look-ahead limiter (ceiling −1.6 dB) only
  acts if the true peak exceeds −1.5 dBTP, and then only touches speech peaks.
  `levels.json` and `ARRANGEMENT.md` show every step and measurement.

## Novelty proof

With `--compare` (the `notes.json` of earlier pieces, also the `*.notes.json` of
the storyline mode) `build.py` compares the melody (`SCORE["melody"]`, default:
all `fg` voices) with every pitched track of every earlier piece over interval
3-, 4- and 5-grams and counts the shared ones. The result is in `novelty.json`
and `ARRANGEMENT.md`. Rule of thumb: few shared 4-grams and no shared 5-grams,
plus a different rhythm variety (distinct note durations), show a new piece; many
shared 4-/5-grams mean: write it anew.

## Checking: listening samples and the mix

- **Play listening samples only as a frozen copy.** A listening sample was once
  overwritten while it was playing and audibly hissed. That is why `build.py`
  aborts if the target folder is not empty; only a copy is played, and every new
  build goes into a new folder (`out/v2`).
- **Check a mix against a reference down to the waveform, not only by LUFS.** Equal
  loudness does not prove the waveform is right: an ffmpeg `alimiter` without
  `latency=1` shifted the waveform by the attack time (correlation −0.17 instead of
  0.99999) while the LUFS stayed the same. Check:

  ```python
  import numpy as np
  from scipy.io import wavfile
  (_, a), (_, b) = wavfile.read("mix.wav"), wavfile.read("reference.wav")
  n = min(len(a), len(b))
  print(np.corrcoef(a[:n].astype(float).ravel(), b[:n].astype(float).ravel())[0, 1])  # expect ~0.99999
  ```

- **The agent cannot listen:** an agent backs pieces with measurement, piano roll
  and spectrogram; whether they please is decided by listening to the
  `preview-mix.wav` (one at a time, in turn, against the video in a second player).
- `check.py` fully decodes every WAV, checks format and length and reads the MIDI
  file; it needs no ffmpeg.

## Limits of the score mode

- The score is written by hand. That takes time and musical judgement; the engine
  only takes over the placing and the measuring.
- Timbre: pure FM brass sounds artificial sooner than wood and glass; whether a
  variant convinces only the listening sample shows.
- All pieces share `synth.py` and the grid/level logic. For a series of pieces
  change instrumentation and timbre, not just the notes.
- The grid is tied to whole beats per scene; scenes of only a few beats allow
  hardly any phrases.

# Storyline mode (sketch)

The fast mode: one storyline JSON file, one run, one score. Good for drafts and
placeholders, **not** for music that should stand as a piece of its own.

> **Documented limit:** The storyline mode builds every piece from the same
> template (fixed chord progression per emotion, four-note figures from a seeded
> random walk, the same waveform voices). If only seed, key, tempo or style
> change, the basic pattern stays recognisable: across several projects or video
> versions it sounds like the same song in variations (in one project exactly that
> was criticised after three versions). The cause is the template, not the seed.
> That is what the score mode is for.

## The method: Storyline → Score

Reconstructed as-is from the reference score (179.5 s, C minor):

1. **Map story acts to music sections.** Acts that share one emotional state
   merge into one section (reference: 7 acts → 5 sections; acts 1–3 formed a
   single 62 s calm opening). Each section gets exact `start`/`end` in seconds.
2. **Assign emotion + intensity per section.**
   - *Emotion* selects the chord progression (scale degrees, minor example):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V is harmonic-minor major).
   - *Intensity* (0–1) drives tempo feel (BPM), layer count and volume ramp.
     Layers join at thresholds: pads always → sparse bells (<0.3) → arp (≥0.25)
     → bass (≥0.4) → lead (≥0.45) → drums (≥0.5) → drive extras (≥0.65) →
     pad octave doubling (≥0.85).
3. **Place special events on the timeline.**
   - `damp`: Gaussian volume duck — `1 - depth · exp(-((t-T)²)/(2σ²))`.
     Reference: depth 0.5, σ 1 s at T=84 s, on the spoken beat
     "Two databases. Same cluster." (~1:24).
   - `climax`: time window forcing full layering, peak volume, octave-doubled
     pads (reference: 154–170 s = 2:34–2:50, on the 2D→3D morph).
   - `outro`: from its start, drums/bass/lead drop out and bells fade to 20 %
     (reference: 170–179.5 s, closing card).
4. **Glue.** Raised-cosine smoothing at section boundaries (~2.5 s), global
   fade-in/out, feedback-delay reverb (100 ms, decay 0.25), tanh drive +
   peak normalization to a background level (reference master measured:
   mean ≈ −22 dB, max ≈ −1.6 dB).
5. **Stay behind the voiceover.** Sections marked "background" cap their
   volume ramp; the score is a bed, not a lead.

## Usage

```bash
# Bundled standalone copy (this skill folder):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # print a storyline template
python compose_music.py --selftest   # 3 s render + verification

# Canonical engine (preferred when the repo is available):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Output: `score.wav` (stereo 16-bit 44.1 kHz), `score.mp3` (192k, needs ffmpeg
on PATH; skipped with a warning otherwise), `score.notes.json` (the
arrangement/note log: every placed note with time, layer, MIDI pitch,
duration, velocity), and `score.mid` — a real **Standard MIDI File** (type 1:
tempo track with one tempo event per section, note track with GM program
hints per style, drums on GM channel 10). Written dependency-free; no
pretty_midi/mido needed.

Determinism: same storyline + same `seed` → byte-identical WAV.

## Storyline JSON reference

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

- `duration` (required, seconds), `sections` (required, ≥1, sorted,
  non-overlapping, within duration).
- Section fields: `start`, `end` (required); `emotion` ∈ calm | tense | alive |
  driving | epic | outro; `intensity` 0–1 (default per emotion); `bpm`
  (default: global `bpm`); `melody` (optional MIDI list, cycled; otherwise a
  seeded random walk over scale tones is generated).
- `key`: note name (C, C#, Db, …), `mode`: minor | major.
- `style`: chiptune | ambient | electronic (see below).
- Event `damp`: `time` (s), `depth` 0–1, `width` = σ in seconds.
- Defaults for fades/crossfade/peak/drive/reverb shown above; all optional.

Full worked example (the reference video's reconstruction):
[`example-storyline.json`](example-storyline.json) — renders a 179.5 s score
matching the original's master level (mean ≈ −22 dB, max ≈ −1.6 dB).

## Style presets

| Style | Lead | Bass/Arp | Drums | Character |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle bass, fast square arps | noise-based kick/hat/snare | retro console, arpeggio-driven (the reference style) |
| `ambient` | soft triangle/sine | slow arps, long-attack pads | only from intensity ≥ 0.75 | sparse, bell-focused, wide reverb feel |
| `electronic` | sawtooth + detune + sub | punchy bass, saw arps | full kit | driving EDM-adjacent bed |

# Beyond waveform synthesis: better sound backends

The genre ceiling above is the **sound backend, not the composition**. Both modes
produce a backend-neutral arrangement; the bundled numpy synth is just the free,
offline default renderer. Every run also writes a Standard MIDI File
(`<out>.mid` or `score.mid`) — render it through better instruments (the score
mode stays purely synthetic by default, see above; this section applies only when
a different sound is explicitly wanted):

- **Path A — SoundFont (recommended: local, free, no cloud).**
  Install FluidSynth (fluidsynth.org, Windows: `winget install FluidSynth`)
  plus a free GM SoundFont (GeneralUser GS by S. Christian Collins, or
  MuseScore_General.sf2). Then:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3 via
  ffmpeg. This unlocks pop/rock band sounds, piano, basic strings.
- **Path B — orchestral / film.** Free orchestral libraries: VSCO 2 Community
  Edition, Soni Musicae, Salamander Grand Piano. Better strings/brass, more
  epic. Honest note: articulation and humanization (velocity variation,
  legato, dynamics curves) matter more than the sample set — and true
  film-score epicness additionally needs arrangement maturity; a backend
  alone is not enough.
- **Path C — external AI generation (Suno etc.).** Possible, but raises
  privacy/rights questions — only after explicit user approval, never the
  default.

Planned but **not yet implemented**: a `humanize` option in the engine
(per-note velocity/timing jitter) so sample-based rendering does not sound
mechanical (marked as TODO in the engine docstring).

## Boundaries

- English and German storyline comments are fine; keys/values are fixed English.
- Very short durations (< ~10 s) work but compress the dramaturgy (fades and
  crossfades are auto-capped at 20 % of duration / 50 % of the shortest section).
- The note log (`*.notes.json`) is the analysis-friendly record; the `*.mid`
  file is the interchange format for DAWs/SoundFont renderers (GM program
  numbers are rough per-style hints — remap them to taste).

## Changelog

### 1.1.0 (2026-10-18)

- New: score mode (`score/`) as the recommended way to make video music: speech
  map (`timeline.py`), bar grid (`grid.py`), score → notes/audio/MIDI (`engine.py`,
  `synth.py`), build with fixed level steps without ducking and a novelty proof
  (`build.py`), check tools (`check.py`, `viz.py`, `analyze_ref.py`), neutral
  example map and example score (march), test (`tests/test_score_mode.py`).
- Storyline mode (`compose_music.py`) unchanged, now marked as the sketch mode
  with its documented limit.
- Dependency `scipy` added (score mode only).

### 1.0.0 (2026-07-31)

- Initial version: storyline mode (`compose_music.py`).
