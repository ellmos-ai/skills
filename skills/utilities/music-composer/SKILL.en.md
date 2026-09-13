---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: >
  Compose video-synced background scores from a storyline JSON using local
  waveform synthesis (numpy + ffmpeg). Styles: chiptune, ambient, electronic.
  Deterministic, offline, no cloud service.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: en
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
    Method reconstructed from a video-synced score composed for a 179.5 s
    explainer video (5 music sections mapped from 7 story acts). Canonical
    engine: ai-media-editor repo, tools/compose_music.py (github.com/ellmos-ai/ai-media-editor).
    A standalone copy is bundled here for offline use.
---

<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

Compose a background score that follows a video's dramatic arc, fully local:
numpy waveform synthesis (oscillators, ADSR, layering, delay reverb) + ffmpeg
for MP3 encoding. No samples, no MIDI hardware, no cloud API.

## When to use

- A video/podcast needs background music that hits story beats at exact
  timestamps (opening, tension dip, drive section, climax, outro).
- You want a deterministic, re-renderable score (same seed → same audio).
- Chiptune, ambient, or electronic styles are acceptable.

## When NOT to use (honest genre limits)

Waveform synthesis can deliver **chiptune, ambient, and electronic** background
beds. It cannot deliver **pop, rock, classical, or orchestral film music** with
its built-in synth — but the arrangement is backend-neutral: see "Beyond
waveform synthesis" below for rendering the same composition through
SoundFonts, orchestral libraries, or external generation.

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

## Beyond waveform synthesis: better sound backends

The genre ceiling above is the **sound backend, not the composition**. The
Storyline→Score method produces a backend-neutral arrangement; the bundled
numpy synth is just the free, offline default renderer. Every run also writes
a Standard MIDI File (`<out>.mid`) — render it through better instruments:

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
