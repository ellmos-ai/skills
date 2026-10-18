"""Example score "Small adventure march": B-flat major, 2/4, about 116 BPM, FM brass, tuba, snare, bells.

Build (from the skill folder, with the neutral example speech map next to this file):
    python score/build.py --speech-map score/examples/speech-map.json --variant score/examples/march.py --out out/march

The score is plain Python data. How many bars a scene has comes from the speech map: run
    python score/grid.py --speech-map score/examples/speech-map.json --bpm 116 --beats-per-bar 2
first and write exactly that many bars into each section's chord chart.

SCORE keys
  id, title, key            labels for the ledgers
  bpm, bpb                  base tempo in beats per minute, beats per bar (the grid bends the tempo per scene
                            by a few percent so that every scene start is a downbeat)
  beat_quarters, ts_den, ts_num_per_beat   length of one beat in quarter notes and the time signature (MIDI export only)
  scale                     pitch classes of the key (passing tones, trill neighbours)
  instruments               {name: dict(fn=<synth voice>, opt={...}, pan=-1..1, send=<reverb send>, gain=...,
                            fg=True for melody voices (must not reach into words), drum=<GM drum note> for percussion,
                            program=<GM program> for the MIDI file, desc=<text>)}
  melody                    instruments that carry the melody (novelty proof); default: all fg instruments
  reverb, echo              room {t60, predelay, damp, wet}; optional ping-pong echo {delay_sec, fb, wet}
  default_parts, sections   accompaniment for every section / per-section chords, phrases and part overrides

Chord chart ("chords")      bars separated by "|"; per bar chord symbols (Bb, Gm, Cm7, F7, Fsus4, Ebmaj7, Bb7sus4, Bb/D);
                            "Cm7:1 F7:1" gives lengths in beats, chords without a length share the rest of the bar.
Phrases (instrument, "bar:beat", "tokens", velocity)
                            tokens: Bb4:.5 note with length in beats, r:.5 rest, | bar line (checked), g:A4 grace note,
                            D5< reversed envelope, F5~:1 trill, Bb5*:2 ring out (final chord), x:.25 / X:.25 soft / hard
                            percussion hit. Positions and lengths are fractions of a beat ("2+1/2" = beat 2.5).
Parts (accompaniment)       dict(inst=..., pattern=[(offset, length, spec, velocity)], range=(low, high) MIDI, voices=3, vel=...,
                            when="speech" (only under speech) / "pause" (only in foreground pauses), bars=(first, last),
                            drum=True, guide=True for a guide-tone counter line). spec: R root, 5/3/7 interval above the root,
                            app chromatic approach to the next root, v chord voicing (v0, v1, v2 single tones), a0, a1 .. arpeggio
                            tone; "+12" / "-12" shifts an octave. For percussion the spec is the instrument name.
"""
import synth  # synth.py sits next to build.py, which puts its folder on sys.path

SCALE = [10, 0, 2, 3, 5, 7, 9]  # B-flat major

INSTRUMENTS = {
    "trumpet": dict(fn=synth.fm_brass, opt=dict(imax=3.2, att=0.04, rel=0.08), pan=0.0, send=0.25, gain=1.0, program=56, fg=True,
                    desc="2-operator FM 1:1, index follows the envelope (brass-like), slight scoop at the attack, ensemble detune"),
    "bells": dict(fn=synth.fm_bell, pan=0.3, send=0.3, gain=0.55, program=9, fg=True,
                  desc="FM bell 1:3.5 with decaying index, octave doublings and bird calls"),
    "horn": dict(fn=synth.fm_brass, opt=dict(imax=1.1, att=0.06, rel=0.12), pan=-0.25, send=0.28, gain=0.42, program=60,
                 desc="FM horn, soft index, off-beat chords"),
    "hornline": dict(fn=synth.fm_brass, opt=dict(imax=0.8, att=0.08, rel=0.14), pan=0.2, send=0.3, gain=0.5, program=60,
                     desc="FM horn as counter line under the voice"),
    "tuba": dict(fn=synth.fm_brass, opt=dict(imax=1.4, att=0.035, rel=0.08, lp=900), pan=0.0, send=0.1, gain=0.85, program=58,
                 desc="FM tuba, oom-pah bass"),
    "snare": dict(fn=synth.snare, drum=38, pan=0.1, send=0.15, gain=0.5, desc="noise 1.5-8 kHz + drum head tone"),
    "brush": dict(fn=synth.snare, opt=dict(brush=True), drum=40, pan=0.1, send=0.1, gain=0.5, desc="brush (low-passed noise)"),
    "bdrum": dict(fn=synth.bdrum, drum=35, pan=0.0, send=0.08, gain=0.75, desc="bass drum, sine with pitch drop"),
    "cymbal": dict(fn=synth.cymbal, drum=49, pan=-0.2, send=0.2, gain=0.45, desc="high-passed noise, long decay"),
}

OOM = [(0, .45, "R"), (1, .45, "5")]  # oom-pah: tuba root on 1, fifth on 2
OOM1 = [(0, .6, "R")]
PAH = [(.5, .28, "v", .8), (1.5, .28, "v", .7)]  # off-beat chords
PAH2 = [(1.5, .28, "v", .7)]
PAD = [(0, 1.9, "v", .55)]
SNARE_M = [(0, .2, "snare", 1), (.5, .15, "snare", .55), (.75, .15, "snare", .65), (1, .2, "snare", .9),
           (1.5, .15, "snare", .55), (1.75, .15, "snare", .65)]
BRUSH = [(.5, .2, "brush", .6), (1.5, .2, "brush", .6)]
RIM = [(i * .5, .1, "brush", .7 if i % 2 == 0 else .45) for i in range(4)]
BD = [(0, .3, "bdrum", 1), (1, .3, "bdrum", .7)]
ROLL = "x:1/8 x:1/8 x:1/8 x:1/8 X:1/8 X:1/8 X:1/8 X:1/8"  # one beat of drum roll, crescendo

SCORE = {
    "id": "march", "title": "Example score - Small adventure march", "key": "B-flat major", "bpm": 116, "bpb": 2,
    "beat_quarters": 1.0, "ts_den": 4, "ts_num_per_beat": 1, "scale": SCALE, "instruments": INSTRUMENTS,
    "melody": ["trumpet"],
    "reverb": dict(t60=1.6, predelay=0.025, damp=4500, wet=0.2),
    "default_parts": {
        "tuba": dict(inst="tuba", pattern=OOM, range=(34, 45), vel=0.75),
        "pah": dict(inst="horn", pattern=PAH, range=(53, 67), voices=3, vel=0.6),
        "guide": dict(inst="hornline", guide=True, range=(55, 67), when="speech", vel=0.5),
        "snare": dict(drum=True, pattern=SNARE_M, vel=0.6, when="pause"),
        "brush": dict(drum=True, pattern=BRUSH, vel=0.55, when="speech"),
        "bd": dict(drum=True, pattern=BD, vel=0.6),
    },
    "sections": {
        "intro": {
            "desc": "Quiet drum roll as fade-in, oom-pah bed; in the pause before the cut the theme head with a cymbal lands on the scene start.",
            "chords": "Bb | Bb | Eb | F | Bb | Gm | Bb | F",
            "phrases": [
                ("snare", "1:1", ROLL, 0.3),
                ("snare", "6:2", ROLL, 0.7),
                ("trumpet", "7:1", "Bb4:.5 Bb4:.25 C5:.25 D5:.5 Bb4:.5 | F5:1 D5:.5 r:.5"),
                ("bells", "7:1", "Bb5:.5 Bb5:.25 C6:.25 D6:.5 Bb5:.5 | F6:1 D6:.5 r:.5", 0.35),
                ("cymbal", "7:1", "X:2", 0.6),
            ],
        },
        "problem": {
            "desc": "Thoughtful bed: held horn chords, tuba only on the downbeat; the short pause answers with the theme line and stays open on a suspended chord.",
            "chords": "Eb | F | Dm | Gm | Eb | Cm7 | Fsus4 | F | Eb | Cm7 | Fsus4",
            "parts": {
                "tuba": dict(inst="tuba", pattern=OOM1, range=(34, 45), vel=0.7),
                "pah": dict(inst="horn", pattern=PAD, range=(53, 67), voices=3, vel=0.5),
            },
            "phrases": [
                ("bells", "1:1", "G6:.5", 0.5),
                ("trumpet", "10:1", "Eb5:.5 Eb5:.25 F5:.25 G5:.5 Eb5:.5 | Bb5:1"),
            ],
        },
        "solution": {
            "desc": "Brighter bed with ticking brushes; the pause between the two statements carries a short bugle call with a suspended landing; a roll leads into the cut.",
            "chords": "Bb | F | Gm | Eb | Bb | F | Eb | Eb | Bb7sus4 | Gm | Cm | D7 | Gm:1 F7:1 | F7",
            "parts": {"brush": dict(drum=True, pattern=RIM, vel=0.55, when="speech")},
            "phrases": [
                ("trumpet", "7:2", "Bb4:.5 Eb5:.5 | Bb4:.5 Eb5:.5 G5:.75 F5:.25 | Eb5:1.5 r:.5", 0.8),
                ("bells", "7:2", "Bb5:.5 Eb6:.5 | Bb5:.5 Eb6:.5 G6:.75 F6:.25 | Eb6:1.5 r:.5", 0.3),
                ("snare", "14:1", ROLL, 0.6),
            ],
        },
        "outro": {
            "desc": "Answer of the theme as a quiet horn line under the voice; after the last word a pickup and the theme head with march accompaniment, then a tutti final chord with cymbal that rings out.",
            "chords": "Bb | Bb/D | Cm7:1 F7:1 | F7 | Bb | Eb:1 F7:1 | Bb | Bb | Bb",
            "phrases": [
                ("trumpet", "1:1", "F5:1"),
                ("hornline", "2:1", "D4:.5 F4:.5 Bb4:.5 D5:.5 | C5:.75 Bb4:.25 A4:.5 G4:.5 | F4:.5 A4:.5 C5:.5 Eb5:.5 | D5:1 Bb4:1", 0.6),
                ("trumpet", "6:2+1/2", "F4:.25 A4:.25 | Bb4:.5 Bb4:.25 C5:.25 D5:.5 Bb4:.5 | Bb5*:2"),
                ("horn", "8:1", "D5*:2", 0.8), ("horn", "8:1", "F4*:2", 0.8), ("horn", "8:1", "Bb4*:2", 0.8),
                ("tuba", "8:1", "Bb1*:2", 0.9),
                ("bells", "8:1", "Bb6:2", 0.5),
                ("bdrum", "8:1", "X:2", 0.8), ("cymbal", "8:1", "X:2", 0.6),
            ],
        },
    },
}

# The accompaniment stops before the final chord (bar 8) so that it can ring out; no guide line in the last scene.
SCORE["sections"]["outro"]["parts"] = {**{k: dict(v, bars=(1, 7)) for k, v in SCORE["default_parts"].items()}, "guide": None}

DOC = {
    "idea": "A small, good-humoured adventure march: friendly, never threatening. Under the voice only oom-pah (tuba / horn "
            "off-beats), brushes and a quiet horn counter line; trumpet, bells and snare step forward in the pauses.",
    "motif": "Head: Bb4 Bb4-C5 D5 Bb4 | F5 (repeated note with a sixteenth upbeat, then a leap of a fifth), stated in the pauses: "
             "at the end of the intro, as a sequence on Eb in the problem scene (open ending on a suspended chord), as a bugle call "
             "(Bb4 Eb5, fourths) in the solution scene, and as a pickup plus the full head before the final chord in the outro.",
    "harmony": "B-flat major with I-IV-V and a sequence through Eb - Cm7 - F; the problem scene hangs on suspended and seventh chords "
               "(open), the solution scene turns to G minor and D7 (deceptive cadence) before it returns with F7 into B-flat major.",
    "instrumentation": "Trumpet, horns, tuba (2-operator FM with envelope-controlled index), FM bells (1:3.5), snare and brush "
                       "(filtered noise + drum head tone), bass drum (sine with pitch drop), cymbal (high-passed noise).",
    "different": "Why it sounds different from a storyline-template score: brass march in 2/4 instead of an electronic pulse, a "
                 "major key, dotted march rhythms and an oom-pah accompaniment instead of pad plus arpeggio; the theme is "
                 "written out phrase by phrase and appears only where the voice is silent.",
}
