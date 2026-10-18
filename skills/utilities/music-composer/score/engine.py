"""Score -> note ledger -> audio / MIDI / levels.

The score (a Python file defining SCORE, see examples/march.py) is hand-written: chord chart per bar,
written-out melody phrases with bar/beat position, accompaniment figures per section. This file only
turns it into notes and sound. Section = scene of the speech map; levels follow a fixed step per
speech window / pause (a bed about 20 LU under the speech, foreground only in pauses), no ducking.

Module state: call configure(speech_map) once before anything else; all timing below works on that map.
"""
import pathlib
import re
import shutil
import struct
import subprocess
import wave
from fractions import Fraction as Fr

import grid
import numpy as np
import synth
from scipy import signal
from timeline import load_wav

SR = 48000
FG_MIN = 1.3  # pauses at least this long get a foreground level
MAP = DUR = SPEECH = PAUSES = None
HAVE_FFMPEG = shutil.which("ffmpeg") is not None


def configure(speech_map):
    """Select the speech map (see timeline.load_speech_map) that all later calls work on."""
    global MAP, DUR, SPEECH, PAUSES
    MAP, DUR, PAUSES = speech_map, speech_map["duration"], speech_map["pauses"]
    SPEECH = [(v["speech_start"], v["speech_end"]) for v in speech_map["voices"]]


def is_fg(t):
    return any(p["start"] <= t < p["end"] and (p["len"] >= FG_MIN or p["before"] == "END") and p["start"] > 0
               for p in PAUSES)


# ------------------------------------------------------------------ pitches and chords
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def pc(name):
    return (PC[name[0]] + name[1:].count("#") - name[1:].count("b")) % 12


def midi(name):
    m = re.fullmatch(r"([A-G][#b]?)(\d)", name)
    assert m, f"note name? {name}"
    base = PC[m[1][0]] + (1 if "#" in m[1] else -1 if "b" in m[1][1:] else 0)
    return 12 * (int(m[2]) + 1) + base


QUAL = {"": (0, 4, 7), "m": (0, 3, 7), "7": (0, 4, 7, 10), "m7": (0, 3, 7, 10), "maj7": (0, 4, 7, 11),
        "sus4": (0, 5, 7), "sus2": (0, 2, 7), "add9": (0, 4, 7, 2), "6": (0, 4, 7, 9), "dim": (0, 3, 6),
        "7sus4": (0, 5, 7, 10)}


def parse_chord(sym):
    main, _, bass = sym.partition("/")
    m = re.fullmatch(r"([A-G][#b]?)(.*)", main)
    assert m and m[2] in QUAL, f"chord? {sym}"
    root = pc(m[1])
    return {"sym": sym, "root": root, "pcs": [(root + i) % 12 for i in QUAL[m[2]]], "bass": pc(bass) if bass else root,
            "has7": 10 in QUAL[m[2]] or 11 in QUAL[m[2]]}


def F(x):
    return Fr(x).limit_denominator(96) if isinstance(x, float) else Fr(x)


def frac(s):
    return sum(Fr(x) for x in s.split("+"))


# ------------------------------------------------------------------ sections
def sections_for(score):
    out = {}
    for s in grid.build_grid(MAP, score["bpm"], score["bpb"]):
        s["bar_beat"] = [sum(s["bars"][:k]) for k in range(len(s["bars"]) + 1)]
        out[s["id"]] = s
    return out


def sec_pos(sec, at):
    bar, _, beat = at.partition(":")
    bar = int(bar)
    assert 1 <= bar <= len(sec["bars"]), f"{sec['id']}: bar {bar} does not exist"
    return Fr(sec["bar_beat"][bar - 1]) + (frac(beat) - 1 if beat else 0)


def sec_time(sec, p):
    return sec["start"] + float(p) * sec["beat_sec"]


def bar_of(sec, p):
    for k in range(len(sec["bars"])):
        if sec["bar_beat"][k] <= p < sec["bar_beat"][k + 1]:
            return k + 1, float(p - sec["bar_beat"][k]) + 1
    return len(sec["bars"]), float(p - sec["bar_beat"][-2]) + 1


def parse_chart(sec, text):
    bars = [b.split() for b in text.split("|")]
    assert len(bars) == len(sec["bars"]), f"{sec['id']}: {len(bars)} chord bars, the grid has {len(sec['bars'])}"
    segs = []
    for k, toks in enumerate(bars):
        length = Fr(sec["bars"][k])
        fixed = sum((Fr(t.split(":")[1]) for t in toks if ":" in t), Fr(0))
        free = [t for t in toks if ":" not in t]
        each = (length - fixed) / len(free) if free else Fr(0)
        p = Fr(sec["bar_beat"][k])
        for t in toks:
            sym, _, d = t.partition(":")
            d = Fr(d) if d else each
            segs.append((p, p + d, parse_chord(sym)))
            p += d
        assert p == sec["bar_beat"][k + 1], f"{sec['id']} bar {k + 1}: chord length {p - sec['bar_beat'][k]} != {length}"
    return segs


def chord_at(segs, p):
    for a, b, c in segs:
        if a <= p < b:
            return c
    return segs[-1][2]


# ------------------------------------------------------------------ accompaniment
def voicing(ch, lo, hi, n, prev):
    tones = [m for m in range(lo, hi + 1) if m % 12 in ch["pcs"]]
    cands = [tones[i:i + n] for i in range(len(tones) - n + 1)] or [tones]
    if prev is None:
        mid = (lo + hi) / 2
        return min(cands, key=lambda v: abs(np.mean(v) - mid))
    return min(cands, key=lambda v: sum(abs(a - b) for a, b in zip(v, prev)))


def bass_note(ch, lo, pcv=None):
    target = ch["bass"] if pcv is None else pcv
    return next(m for m in range(lo, lo + 12) if m % 12 == target)


def resolve(spec, ch, nxt, part, state):
    """Accompaniment note spec -> list of MIDI pitches."""
    lo, hi = part.get("range", (40, 84))
    m = re.fullmatch(r"([A-Za-z]+)(\d*)([+-]\d+)?", spec)
    kind, idx, off = m[1], m[2], int(m[3] or 0)
    if kind == "R":
        return [bass_note(ch, lo) + off]
    if kind == "app":  # chromatic approach to the next root
        return [bass_note(nxt, lo) - 1 + off] if nxt["bass"] != ch["bass"] else [bass_note(ch, lo) + 7 + off]
    key = (ch["sym"], lo, hi)
    if state.get("key") != key:
        state["v"] = voicing(ch, lo, hi, part.get("voices", 3), state.get("v"))
        state["key"] = key
    v = state["v"]
    if kind == "v":
        return [x + off for x in (v if not idx else [v[int(idx) % len(v)]])]
    if kind == "a":
        ext = v + [x + 12 for x in v]
        return [ext[int(idx) % len(ext)] + off]
    raise ValueError(spec)


def resolve_interval(spec, ch, part):
    lo = part.get("range", (40, 84))[0]
    m = re.fullmatch(r"(\d)([+-]\d+)?", spec)
    step = {"5": 7, "3": 4 if (ch["root"] + 4) % 12 in ch["pcs"] else 3, "7": 10 if (ch["root"] + 10) % 12 in ch["pcs"] else 12}[m[1]]
    return [bass_note(ch, lo, ch["root"]) + step + int(m[2] or 0)]


def expand_pattern(sec, segs, name, part, notes):
    state = {}
    bars = part.get("bars")
    for k, blen in enumerate(sec["bars"]):
        if bars and not (bars[0] <= k + 1 <= bars[1]):
            continue
        for ev in part["pattern"]:
            off, d, spec = F(ev[0]), F(ev[1]), ev[2]
            vel = ev[3] if len(ev) > 3 else 1.0
            if off >= blen:
                continue
            p = Fr(sec["bar_beat"][k]) + off
            t = sec_time(sec, p)
            fg = is_fg(t)
            if (part.get("when") == "speech" and fg) or (part.get("when") == "pause" and not (fg and is_fg(t + min(float(d) * sec["beat_sec"], 0.3)))):
                continue
            ch, nxt = chord_at(segs, p), chord_at(segs, min(p + d, Fr(sec["bar_beat"][-1]) - Fr(1, 100)))
            if part.get("drum"):
                pitches = [None]
            elif spec[0] in "537":
                pitches = resolve_interval(spec, ch, part)
            else:
                pitches = resolve(spec, ch, nxt, part, state)
            for mm in pitches:
                notes.append(note(sec, p, d, mm, part.get("vel", 0.7) * vel, spec if part.get("drum") else part["inst"],
                                  name, fg, part))


def guide_line(sec, segs, name, part, notes, prev):
    """Guide-tone counter line: per chord the nearest chord tone (third / seventh preferred); thirds-sized
    leaps are filled with a passing tone. Gives the bed under the voice a calm melodic thread."""
    lo, hi = part["range"]
    pas = Fr(part.get("pass", "1/2"))
    for a, b, ch in segs:
        if (part.get("when") == "speech" and is_fg(sec_time(sec, a))) or (part.get("when") == "pause" and not is_fg(sec_time(sec, a))):
            prev.clear()
            continue
        cands = [m for m in range(lo, hi + 1) if m % 12 in ch["pcs"]]
        pref = [m for m in cands if (m - ch["root"]) % 12 in (3, 4, 10, 11)] or cands
        ref = prev.get("m", (lo + hi) // 2)
        target = min(pref, key=lambda m: (abs(m - ref), m))
        last = prev.get("note")
        if last is not None and prev["sec"] == sec["id"] and prev["end"] == a and prev["len"] >= 3 * pas and 3 <= abs(target - prev["m"]) <= 4:
            step = 1 if target > prev["m"] else -1
            mid = next(m for m in range(prev["m"] + step, target, step) if m % 12 in part["scale"])
            last["dur"] -= float(pas) * sec["beat_sec"]
            notes.append(note(sec, a - pas, pas, mid, part["vel"] * 0.85, part["inst"], name, False, part))
        n = note(sec, a, b - a, target, part["vel"], part["inst"], name, False, part)
        notes.append(n)
        prev.update(m=target, note=n, end=b, sec=sec["id"], len=b - a)


# ------------------------------------------------------------------ phrases
def parse_phrase(sec, ph, notes, scale):
    inst, at, text = ph[0], ph[1], ph[2]
    vel = ph[3] if len(ph) > 3 else 0.8
    p = sec_pos(sec, at)
    graces = []
    for tok in text.split():
        if tok == "|":
            assert p in sec["bar_beat"], f"{sec['id']} {at}: bar line at beat {p} is not on a downbeat"
            continue
        if tok.startswith("g:"):
            graces.append(tok[2:])
            continue
        name, _, d = tok.partition(":")
        d = Fr(d) if d else Fr(1)
        if name not in ("r",):
            ring = name.endswith("*")  # final chord: let it ring out naturally
            name = name.rstrip("*")
            rev = name.endswith("<")
            trill = name.rstrip("<").endswith("~")
            base = name.rstrip("<~")
            fg = is_fg(sec_time(sec, p))
            accent = 1.0 if p in sec["bar_beat"] else (0.93 if p.denominator == 1 else 0.86)
            drum = name in ("x", "X")
            for gname in graces:
                n = note(sec, p, Fr(0), midi(gname), vel * 0.7, inst, "phrase", fg, {})
                n["t"] -= 0.05
                n["dur"] = 0.05
                n["legato"] = True
                notes.append(n)
            if drum:
                notes.append(note(sec, p, d, None, vel * (1.0 if name == "X" else 0.7) * accent, inst, "phrase", fg, {}))
            elif trill:
                notes.extend(trill_notes(sec, p, d, midi(base), vel * accent, inst, fg, scale))
            else:
                n = note(sec, p, d, midi(base), vel * accent, inst, "phrase", fg, {})
                n["rev"] = rev
                n["ring"] = ring
                notes.append(n)
        graces = []
        p += d
    assert p <= sec["bar_beat"][-1], f"{sec['id']} {at}: phrase runs past the section end ({p} > {sec['bar_beat'][-1]})"


def trill_notes(sec, p, d, m, vel, inst, fg, scale):
    upper = next(x for x in range(m + 1, m + 4) if x % 12 in scale)
    t0, total = sec_time(sec, p), float(d) * sec["beat_sec"]
    k = max(2, int(total / 0.07))
    out = []
    for i in range(k):
        n = note(sec, p, Fr(0), m if i % 2 == 0 or i == k - 1 else upper, vel * (1 if i == 0 else 0.8), inst, "phrase", fg, {})
        n["t"] = t0 + i * total / k
        n["dur"] = total / k
        n["legato"] = i > 0
        n["trill"] = True
        out.append(n)
    return out


def note(sec, p, d, m, vel, inst, part, fg, partspec):
    bar, beat = bar_of(sec, p)
    return {"t": sec_time(sec, p), "dur": float(d) * sec["beat_sec"], "midi": m, "vel": float(vel), "inst": inst,
            "part": part, "section": sec["id"], "bar": bar, "beat": round(beat, 4), "fg": fg,
            "bright": 1.0 if fg else partspec.get("bright_speech", 0.3)}


# ------------------------------------------------------------------ score -> notes
def compose(score):
    secs = sections_for(score)
    notes, guide_prev = [], {}
    for sid, sec in secs.items():
        assert sid in score["sections"], f"the score has no section for scene '{sid}'"
        spec = score["sections"][sid]
        segs = parse_chart(sec, spec["chords"])
        sec["segs"] = segs
        parts = dict(score["default_parts"])
        parts.update(spec.get("parts", {}))
        for name, part in parts.items():
            if part is None:
                continue
            if part.get("guide"):
                guide_line(sec, segs, name, dict(part, scale=score["scale"]), notes, guide_prev.setdefault(name, {}))
            else:
                expand_pattern(sec, segs, name, part, notes)
        for ph in spec.get("phrases", []):
            parse_phrase(sec, ph, notes, score["scale"])
    notes = [n for n in notes if n["vel"] > 0 and n["t"] < DUR]
    notes.sort(key=lambda n: (n["t"], n["inst"]))
    return secs, notes


def fg_overlap_report(score, notes):
    """Foreground voices (melody) must not reach into a word."""
    issues = []
    for n in notes:
        if not score["instruments"][n["inst"]].get("fg") or not (n["part"] == "phrase" or n["fg"]):
            continue
        a, b = n["t"], n["t"] + n["dur"]
        for s, e in SPEECH:
            ov = min(b, e) - max(a, s)
            if ov > 0.12:
                issues.append(f"{n['section']} bar {n['bar']} {n['inst']} midi {n['midi']} @ {a:.2f}s overlaps speech at {s:.2f}s by {ov:.2f}s")
    return issues


# ------------------------------------------------------------------ rendering
def render(score, notes):
    n = int(DUR * SR) + SR * 3
    dry = np.zeros((n, 2), np.float32)
    send = np.zeros((n, 2), np.float32)
    echo = np.zeros((n, 2), np.float32)
    for nt in notes:
        ins = score["instruments"][nt["inst"]]
        fn, opt = ins["fn"], dict(ins.get("opt", {}))
        if ins.get("drum") is not None:
            y = fn(nt["vel"], nt["bright"], **opt)
        else:
            f = 440.0 * 2 ** ((nt["midi"] - 69) / 12)
            y = fn(f, max(nt["dur"], 0.03), nt["vel"], nt["bright"], legato=nt.get("legato", False),
                   rev=nt.get("rev", False), **opt)
        if nt.get("ring"):  # a held note decays exponentially (instead of hold + fade)
            y = y * np.exp(-np.arange(len(y)) / SR / (0.4 * max(nt["dur"], 0.1)))
        y = (y * ins.get("gain", 1.0)).astype(np.float32)
        i0 = int(round(nt["t"] * SR))
        if i0 < 0:
            y, i0 = y[-i0:], 0
        y = y[: n - i0]
        pan = ins.get("pan", 0.0)
        lr = np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)], np.float32) * np.float32(np.sqrt(2))
        st = y[:, None] * lr[None, :]
        dry[i0:i0 + len(y)] += st
        if ins.get("send"):
            send[i0:i0 + len(y)] += st * np.float32(ins["send"])
        if ins.get("echo"):
            echo[i0:i0 + len(y)] += st
    rv = score["reverb"]
    ir = synth.make_ir(rv["t60"], rv["predelay"], rv["damp"], 7)
    wet = np.stack([signal.fftconvolve(send[:, c], ir[:, c])[:n] for c in range(2)], axis=1)
    out = dry + np.float32(rv["wet"]) * wet.astype(np.float32)
    if score.get("echo"):
        ec = score["echo"]
        dly = int(ec["delay_sec"] * SR)
        for k in range(1, 5):
            g = ec["wet"] * ec["fb"] ** (k - 1)
            sh = np.zeros_like(echo)
            sh[k * dly:] = echo[: n - k * dly]
            if k % 2:  # ping-pong
                sh = sh[:, ::-1]
            out += np.float32(g) * lp_st(sh, 5000)
    out = signal.sosfilt(signal.butter(2, 30, "high", fs=SR, output="sos"), out, axis=0)
    return out[: int(DUR * SR)].astype(np.float64)


def lp_st(x, fc):
    return signal.sosfilt(signal.butter(1, fc, "low", fs=SR, output="sos"), x, axis=0).astype(np.float32)


# ------------------------------------------------------------------ loudness (BS.1770-4, 48 kHz)
_K1 = ([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585])
_K2 = ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])


def kweight(x):
    y = signal.lfilter(*_K1, x, axis=0)
    return signal.lfilter(*_K2, y, axis=0)


def lufs(x, gated=True):
    """Integrated loudness (LUFS) with absolute and relative gate."""
    z = kweight(x)
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    if len(z) < blk:
        ms = (z ** 2).mean(axis=0).sum()
        return -0.691 + 10 * np.log10(ms + 1e-20)
    c = np.concatenate(([0.0], np.cumsum((z ** 2).sum(axis=1))))  # running power sum -> block means without a Python loop
    starts = np.arange(0, len(z) - blk + 1, hop)
    ms = (c[starts + blk] - c[starts]) / blk
    lk = -0.691 + 10 * np.log10(ms + 1e-20)
    if not gated:
        return -0.691 + 10 * np.log10(ms.mean() + 1e-20)
    keep = lk > -70
    if not keep.any():
        return -99.0
    rel = -0.691 + 10 * np.log10(ms[keep].mean()) - 10
    keep &= lk > rel
    return -0.691 + 10 * np.log10(ms[keep].mean() + 1e-20)


def true_peak_db(x):
    up = signal.resample_poly(x, 4, 1, axis=0)
    return 20 * np.log10(np.abs(up).max() + 1e-20)


def band_share(x, lo=1000, hi=4000):
    """Share of the spectral energy (above 30 Hz) that lies in the lo..hi band."""
    mono = x.mean(axis=1)
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    return float(spec[(f >= lo) & (f < hi)].sum() / (spec[f > 30].sum() + 1e-20))


# ------------------------------------------------------------------ level steps
def segments():
    """Segments with a fixed gain: speech windows (bed) and pauses (foreground from FG_MIN on)."""
    segs = []
    for i, (s, e) in enumerate(SPEECH):
        segs.append({"kind": "bed", "i": i, "start": s, "end": e, "label": MAP["voices"][i]["id"], "final": False})
    for p in PAUSES:
        fg = p["start"] > 0 and (p["len"] >= FG_MIN or p["before"] == "END")
        segs.append({"kind": "fg" if fg else "gap", "start": p["start"], "end": p["end"], "label": f"pause before {p['before']}",
                     "final": p["before"] == "END"})
    return sorted(segs, key=lambda s: s["start"])


def gain_curve(segs):
    bed = [s for s in segs if s["kind"] == "bed"]
    t_in = min(0.55, max(0.05, bed[0]["start"] - 0.08))  # fade-in, ends before the first word
    pts = [(0.0, -60.0), (t_in, bed[0]["g"])]
    for s in segs:
        if s["kind"] == "bed":
            pts += [(s["start"] - 0.08, s["g"]), (s["end"], s["g"])]
        elif s["kind"] == "fg":
            L = s["end"] - s["start"]
            nxt = next((b for b in bed if b["start"] >= s["end"] - 1e-6), None)
            up0 = s["start"] + 0.04
            up1 = up0 + min(0.35, 0.2 * L)
            if nxt is None:  # end: fixed level to the end, the chord rings out by itself; only 0.15 s click guard
                pts += [(up0, pts[-1][1]), (up1, s["g"]), (DUR - 0.15, s["g"]), (DUR, -60.0)]
                s["plateau"] = (up1, DUR - 0.15)
                continue
            dn1 = s["end"] - 0.1
            dn0 = dn1 - min(0.8, 0.3 * L)
            pts += [(up0, pts[-1][1]), (up1, s["g"]), (dn0, s["g"]), (dn1, nxt["g"])]
            s["plateau"] = (up1, dn0)
    pts.sort(key=lambda p: p[0])
    t = np.arange(int(DUR * SR)) / SR
    db = np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
    return 10 ** (db / 20), pts


def win(x, a, b):
    return x[int(a * SR):int(b * SR)]


def stage_gains(raw, t_bed, t_fg, fg_cap=12.0):
    """Derive a fixed gain per segment from the measured music (gain = target - LUFS), then re-measure
    with the ramps in place and correct. Foreground: at most t_fg, never quieter than the bed before/after."""
    segs = segments()
    for s in segs:
        if s["kind"] == "bed":
            s["g"] = t_bed - lufs(win(raw, s["start"], s["end"]))
    beds = [s for s in segs if s["kind"] == "bed"]
    for s in segs:
        if s["kind"] == "fg":
            s["ref"] = max(b["g"] for b in beds if abs(b["end"] - s["start"]) < 0.01 or abs(b["start"] - s["end"]) < 0.01)
            # short transition pauses get a lower step (filler figure instead of a motif statement, no pumping):
            # full step from 3 s, below that 2.5 dB less per second, at most 4 dB
            # (exception: the final chord after the last word gets the full step)
            s["target"] = t_fg - (0.0 if s["final"] else float(np.clip((3.0 - (s["end"] - s["start"])) * 2.5, 0, 4)))
            # inset 0.1 s per side; a pause too short for that is measured whole (an empty window gives NaN)
            a, b = (s["start"] + 0.1, s["end"] - 0.1) if s["end"] - s["start"] > 0.3 else (s["start"], s["end"])
            s["g"] = float(np.clip(s["target"] - lufs(win(raw, a, b)), s["ref"], s["ref"] + fg_cap))
    for _ in range(3):
        curve, _ = gain_curve(segs)
        y = raw * curve[:, None]
        for s in segs:
            if s["kind"] == "bed":
                s["g"] += t_bed - lufs(win(y, s["start"], s["end"]))
            elif s["kind"] == "fg":
                # end (ringing chord): regulate over the whole pause, the gate reacts to the decay
                a, b = s["plateau"] if s["plateau"][1] - s["plateau"][0] > 0.45 and not s["final"] else (s["start"], s["end"])
                s["g"] = float(np.clip(s["g"] + s["target"] - lufs(win(y, a, b)), s["ref"], s["ref"] + fg_cap))
    curve, pts = gain_curve(segs)
    return segs, curve, pts


# ------------------------------------------------------------------ voice track, mix
def voice_track(narration_dir):
    """All narration clips (<narration_dir>/<voice id>.wav) placed at their clip_start."""
    n = int(DUR * SR)
    v = np.zeros((n, 2))
    for c in MAP["voices"]:
        x = load_wav(pathlib.Path(narration_dir) / f"{c['id']}.wav")
        i0 = int(round(c["clip_start"] * SR))
        x = x[: n - i0]
        v[i0:i0 + len(x)] += x
    return v


def limiter(x, ceiling_db=-1.6, look=0.005, release=0.08):
    """Simple look-ahead limiter (only used if the voice gets too spiky after normalisation)."""
    from scipy.ndimage import maximum_filter1d
    c = 10 ** (ceiling_db / 20)
    peak = maximum_filter1d(np.abs(x).max(axis=1), int(look * SR) * 2 + 1)
    g = np.minimum(1.0, c / (peak + 1e-12))
    a = np.exp(-1 / (release * SR))
    inst = g
    g, _ = signal.lfilter([1 - a], [1, -a], g, zi=signal.lfilter_zi([1 - a], [1, -a]) * g[0])  # soft release
    g = np.minimum(g, inst)
    return x * g[:, None], float(20 * np.log10(g.min())), int((g < 0.999).sum())


def write_wav(path, x):
    """24-bit PCM WAV written directly (no ffmpeg, no temp file renamed over a file a player may hold open)."""
    pcm = np.round(np.clip(x, -1, 1 - 2 ** -23) * 2 ** 23).astype("<i4")
    raw = np.frombuffer(pcm.tobytes(), np.uint8).reshape(-1, 4)[:, :3].tobytes()  # drop the high byte: 4 -> 3 bytes
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(raw)


def ffmpeg_lufs(path, a=None, b=None):
    """Independent cross-check: ffmpeg ebur128 integrated loudness and true peak, optionally for a window.
    Returns (None, None, "") if ffmpeg is not on PATH."""
    if not HAVE_FFMPEG:
        return None, None, ""
    cmd = ["ffmpeg", "-hide_banner", "-nostats"]
    if a is not None:
        cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}"]
    cmd += ["-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    summ = out[out.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+|-inf)", summ)[1].replace("-inf", "-99"))
    tp = re.search(r"Peak:\s+(-?[\d.]+|-inf)", summ)
    return i, (float(tp[1].replace("-inf", "-99")) if tp else None), out


def ffmpeg_short_term(path, times):
    """Short-term loudness S (3 s window) of the full mix at the given window ends (None without ffmpeg)."""
    out = ffmpeg_lufs(path)[2]
    rows = [(float(m[1]), float(m[2])) for m in re.finditer(r"t:\s*([\d.]+).*?S:\s*(-?[\d.]+|-inf)", out.replace("-inf", "-99"))]
    return {round(t, 2): (min(rows, key=lambda r: abs(r[0] - t))[1] if rows else None) for t in times}


# ------------------------------------------------------------------ MIDI (SMF type 1, stdlib only)
def _vlq(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.insert(0, (v & 0x7F) | 0x80)
        v >>= 7
    return bytes(out)


def _track(events):
    events.sort(key=lambda e: (e[0], e[1]))
    data, last = b"", 0
    for tick, _, msg in events:
        data += _vlq(tick - last) + msg
        last = tick
    data += b"\x00\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + data


def write_midi(path, score, secs, notes):
    tpq = 480
    bq = score["beat_quarters"]
    tpb = int(tpq * bq)
    ts_den = score["ts_den"]
    tick0, t_ev, k = {}, [], 0
    prev_bar = None
    for sid, sec in secs.items():
        tick0[sid] = k
        t_ev.append((k, 0, b"\xff\x51\x03" + int(round(sec["beat_sec"] / bq * 1e6)).to_bytes(3, "big")))
        for b, blen in enumerate(sec["bars"]):
            num = int(round(blen * score["ts_num_per_beat"]))
            if num != prev_bar:
                cc = 36 if ts_den == 8 else 24
                t_ev.append((k + sec["bar_beat"][b] * tpb, 1, bytes([0xFF, 0x58, 4, num, int(np.log2(ts_den)), cc, 8])))
                prev_bar = num
        k += sec["bar_beat"][-1] * tpb
    t_ev.append((0, 0, b"\xff\x03" + _vlq(len(score["title"].encode())) + score["title"].encode()))
    tracks = [_track(t_ev)]
    chan = 0
    for inst, spec in score["instruments"].items():
        ns = [n for n in notes if n["inst"] == inst]
        if not ns:
            continue
        drum = spec.get("drum") is not None
        ch = 9 if drum else chan
        if not drum:
            chan = chan + 2 if chan == 8 else chan + 1
        ev = [(0, 0, b"\xff\x03" + _vlq(len(inst)) + inst.encode())]
        if not drum:
            ev.append((0, 0, bytes([0xC0 | ch, spec.get("program", 0)])))
        for n in ns:
            sec = secs[n["section"]]
            on = tick0[n["section"]] + int(round((n["t"] - sec["start"]) / sec["beat_sec"] * tpb))
            off = on + max(1, int(round(n["dur"] / sec["beat_sec"] * tpb)))
            key = spec["drum"] if drum else n["midi"]
            v = int(np.clip(round(n["vel"] * 110) + 10, 1, 127))
            ev += [(max(on, 0), 2, bytes([0x90 | ch, key, v])), (off, 1, bytes([0x80 | ch, key, 0]))]
        tracks.append(_track(ev))
    head = b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), tpq)
    path.write_bytes(head + b"".join(tracks))
