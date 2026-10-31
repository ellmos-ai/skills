"""Build one piece completely: notes, music.wav, preview-mix.wav, score.mid, ledgers, ARRANGEMENT.md.

    python build.py --speech-map speech-map.json --variant my_score.py --out out/v1
                    [--narration-dir clips/] [--compare other.notes.json ...]
    python build.py --speech-map speech-map.json --variant my_score.py --check

--check         only compose: validates chord charts, phrases and foreground/word overlaps in seconds, writes nothing

--variant       Python file defining SCORE (and optionally DOC), see examples/march.py
--out           target folder, must be new or empty: listening versions that may be playing are never overwritten
--narration-dir folder with <voice id>.wav clips (48 kHz); enables preview-mix.wav and calibrates the
                levels against the real speech. Without it the speech is assumed to sit at -16 LUFS.
--compare       notes.json of earlier pieces (this tool's notes.json or compose_music.py's *.notes.json);
                the melody is checked against every pitched layer for shared interval n-grams (novelty proof)
"""
import argparse
import importlib.util
import json
import pathlib
import platform
import sys
from collections import Counter

import engine
import numpy as np
import scipy
from timeline import load_speech_map

MIX_LUFS = -16.0  # loudness of the final mix (speech + music)
BED_LUFS = -36.0  # bed under speech, about 20 LU below the speech
FG_LUFS = -24.5   # foreground in pauses (the limit is -24; short transition pauses sit lower)


def load_score(path):
    spec = importlib.util.spec_from_file_location("score_module", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def melody_seq(notes, insts):
    seq = sorted((n for n in notes if n["inst"] in insts and n["midi"] is not None and not n.get("legato")), key=lambda n: n["t"])
    return [n["midi"] for n in seq], [round(n["dur"], 3) for n in seq]


def ngrams(pitches, n):
    iv = np.diff(pitches).tolist()
    return Counter(tuple(iv[i:i + n]) for i in range(len(iv) - n + 1))


def load_reference(path):
    """Pitched notes per layer from a notes.json of this tool (key `inst`) or of compose_music.py (key `layer`)."""
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    layers = {}
    for n in sorted(data["notes"], key=lambda n: n["t"]):
        if n.get("midi") is not None and not n.get("legato"):
            layers.setdefault(n.get("inst") or n.get("layer"), []).append(n)
    return layers


def novelty(notes, melody_insts, compare_paths):
    """Interval n-gram overlap of the melody with every pitched layer of every reference piece."""
    mine, durs = melody_seq(notes, melody_insts)
    res = {"melody_notes": len(mine), "distinct_durations": len(set(durs)), "compare": {}}
    for path in compare_paths:
        res["compare"][pathlib.Path(path).name] = {}
        for layer, ref_notes in load_reference(path).items():
            pitches = [n["midi"] for n in ref_notes]
            row = {"notes": len(pitches), "distinct_durations": len({round(n["dur"], 3) for n in ref_notes}), "ngram": {}}
            for n in (3, 4, 5):
                a, b = ngrams(mine, n), ngrams(pitches, n)
                shared = set(a) & set(b)
                row["ngram"][n] = {
                    "distinct_own": len(a), "distinct_reference": len(b), "shared": len(shared),
                    "own_occurrences_shared_pct": round(100 * sum(a[k] for k in shared) / max(1, sum(a.values())), 1),
                }
            res["compare"][pathlib.Path(path).name][layer] = row
    return res


def band_share_safe(x):
    return engine.band_share(x) if len(x) else float("nan")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--speech-map", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--narration-dir")
    ap.add_argument("--compare", nargs="*", default=[])
    args = ap.parse_args(argv)

    if not args.check and not args.out:
        ap.error("--out is required unless --check is given")
    out = pathlib.Path(args.out) if args.out else None
    if out and out.exists() and any(out.iterdir()):
        sys.exit(f"Abort: {out} is not empty - existing versions are never overwritten.")
    engine.configure(load_speech_map(args.speech_map))
    DUR, MAP = engine.DUR, engine.MAP
    mod = load_score(args.variant)
    score = mod.SCORE
    melody = score.get("melody") or [k for k, v in score["instruments"].items() if v.get("fg")]

    secs, notes = engine.compose(score)
    issues = engine.fg_overlap_report(score, notes)
    if args.check:
        print(f"[{score['id']}] check ok: {len(secs)} sections, {len(notes)} notes, foreground overlaps {len(issues)}")
        for i in issues[:20]:
            print("   !", i)
        return
    out.mkdir(parents=True, exist_ok=True)
    raw = engine.render(score, notes)
    voice = engine.voice_track(args.narration_dir) if args.narration_dir else None
    # Without narration the speech is assumed to sit at MIX_LUFS already: music steps are set relative to that.
    G = MIX_LUFS - engine.lufs(voice) if voice is not None else 0.0
    for _ in range(3):
        segs, curve, pts = engine.stage_gains(raw, BED_LUFS - G, FG_LUFS - G)
        music = raw * curve[:, None]
        if voice is None:
            break
        mix = voice + music
        G_new = MIX_LUFS - engine.lufs(mix)
        converged = abs(G_new - G) < 0.05
        G = G_new
        if converged:
            break
    lim_db, lim_n, mix_own, mix_ff, short_term = 0.0, 0, None, {"I_lufs": None, "true_peak_dbtp": None}, []
    engine.write_wav(out / "music.wav", music)
    if voice is not None:
        mixn = mix * 10 ** (G / 20)
        tp = engine.true_peak_db(mixn)
        if tp > -1.5:
            mixn, lim_db, lim_n = engine.limiter(mixn)
            tp = engine.true_peak_db(mixn)
        engine.write_wav(out / "preview-mix.wav", mixn)
        mix_own = {"I_lufs": round(float(engine.lufs(mixn)), 1), "true_peak_dbtp": round(float(tp), 1)}
        mix_i, mix_tp, _ = engine.ffmpeg_lufs(out / "preview-mix.wav")
        mix_ff = {"I_lufs": mix_i, "true_peak_dbtp": mix_tp}
        if engine.HAVE_FFMPEG:
            long_pauses = [p for p in MAP["pauses"] if p["len"] >= 3.0]
            st = engine.ffmpeg_short_term(out / "preview-mix.wav", [p["end"] - 0.15 for p in long_pauses])
            short_term = [{"pause": f"{p['start']:.2f}-{p['end']:.2f}", "window": f"{p['end'] - 3.15:.2f}-{p['end'] - 0.15:.2f}",
                           "S_lufs_mix": st[round(p["end"] - 0.15, 2)]} for p in long_pauses]
    engine.write_midi(out / "score.mid", score, secs, notes)

    # ---------------- measurements (own BS.1770 meter, ffmpeg ebur128 as independent cross-check)
    rows = []
    for s in segs:
        if s["end"] - s["start"] < 0.4:
            continue
        own = engine.lufs(engine.win(music, s["start"], s["end"]))
        ff = engine.ffmpeg_lufs(out / "music.wav", s["start"], s["end"])[0]
        rows.append({"kind": s["kind"], "label": s["label"], "start": round(s["start"], 3), "end": round(s["end"], 3),
                     "gain_db": round(s["g"], 2) if "g" in s else "ramp",
                     "music_lufs_final": round(own + G, 1),
                     "music_lufs_final_ffmpeg": round(ff + G, 1) if ff is not None else None})
    sp = np.concatenate([engine.win(music, s["start"], s["end"]) for s in segs if s["kind"] == "bed"])
    pz = np.concatenate([engine.win(music, s["start"], s["end"]) for s in segs if s["kind"] == "fg"])
    bed_vals = [r["music_lufs_final"] for r in rows if r["kind"] == "bed"]
    fg_vals = [r["music_lufs_final"] for r in rows if r["kind"] == "fg"]
    nov = novelty(notes, melody, args.compare)
    levels = {
        "rule": f"bed {BED_LUFS:.0f} LUFS (+-2) under speech, foreground without speech at most -24 LUFS, whole mix {MIX_LUFS:.0f} LUFS, "
                f"<= -1.5 dBTP, no ducking. Foreground target {FG_LUFS} LUFS for pauses of 3 s and more; shorter transition "
                "pauses 2.5 dB lower per missing second (at most 4 dB).",
        "mix_rule": ("narration clips + music.wav, both at gain 1.0, then one linear gain of "
                     f"{G:+.2f} dB -> {MIX_LUFS:.0f} LUFS") if voice is not None else
                    f"no narration given: speech assumed at {MIX_LUFS:.0f} LUFS, music.wav is calibrated for that",
        "normalization_db": round(G, 2), "limiter_max_db": round(lim_db, 2), "limiter_samples": lim_n,
        "mix_own": mix_own, "mix_ffmpeg": mix_ff,
        "bed_lufs_min_max": [min(bed_vals), max(bed_vals)], "foreground_lufs_max": max(fg_vals) if fg_vals else None,
        "midband_1_4khz_share_pct": {"under_speech": round(100 * band_share_safe(sp), 2), "in_pauses": round(100 * band_share_safe(pz), 2)},
        "segments": rows, "short_term_3s_in_long_pauses": short_term, "gain_points": [(round(a, 3), round(b, 2)) for a, b in pts],
    }
    (out / "levels.json").write_text(json.dumps(levels, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / "notes.json").write_text(json.dumps({
        "variant": score["id"], "melody_instruments": melody,
        "units": "t/dur in seconds from the start; bar/beat per section (1-based); midi=None for percussion",
        "notes": [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in n.items()} for n in notes]},
        ensure_ascii=False), encoding="utf-8")
    (out / "novelty.json").write_text(json.dumps(nov, indent=1, ensure_ascii=False), encoding="utf-8")
    score_json = {
        "title": score["title"], "key": score["key"], "base_tempo_bpm": score["bpm"], "beats_per_bar": score["bpb"],
        "beat_in_quarters": score["beat_quarters"], "duration_s": DUR,
        "sections": [{"id": sid, "start": round(s["start"], 3), "end": round(s["end"], 3), "bars": s["bars"],
                      "bpm": s["bpm"], "tempo_deviation_pct": s["tempo_dev_pct"],
                      "chords": score["sections"][sid]["chords"],
                      "phrases": [list(p) for p in score["sections"][sid].get("phrases", [])],
                      "accompaniment": sorted(k for k, v in {**score["default_parts"], **score["sections"][sid].get("parts", {})}.items() if v)}
                     for sid, s in secs.items()],
        "accompaniment_patterns": {k: v for k, v in score["default_parts"].items()},
        "instruments": {k: {"synthesis": v["fn"].__name__, "parameters": v.get("opt", {}), "pan": v.get("pan"), "reverb_send": v.get("send"),
                            "gain": v.get("gain"), "description": v.get("desc", "")} for k, v in score["instruments"].items()},
        "room": score["reverb"], "echo": score.get("echo"),
        "tooling": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                    "score_file": pathlib.Path(args.variant).name},
    }
    (out / "score.json").write_text(json.dumps(score_json, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    write_arrangement(out, mod, score, secs, levels, nov, issues, pathlib.Path(args.variant).name)
    print(f"[{score['id']}] notes {len(notes)}, foreground overlaps {len(issues)}, G {G:+.2f} dB, mix {mix_own and mix_own['I_lufs']} LUFS / {mix_own and mix_own['true_peak_dbtp']} dBTP, "
          f"bed {min(bed_vals)}..{max(bed_vals)}, foreground max {max(fg_vals) if fg_vals else None}")
    for i in issues[:20]:
        print("   !", i)


def write_arrangement(out, mod, score, secs, levels, nov, issues, score_file):
    d = getattr(mod, "DOC", {})
    L = [f"# {score['title']}", "",
         f"**Key** {score['key']} · **Base tempo** {score['bpm']} BPM · **Length** {engine.DUR:.1f} s (speech-map time axis) · "
         "**Files** `music.wav`, `preview-mix.wav` (if narration was given), `score.mid`, `score.json`, `notes.json`, "
         "`levels.json`, `novelty.json`", "",
         "## Idea", d.get("idea", ""), "", "## Motif", d.get("motif", ""), "", "## Harmony", d.get("harmony", ""), "",
         "## Instrumentation (own synthesis, no samples)", d.get("instrumentation", ""), ""]
    L += ["| Voice | Synthesis | Role |", "|---|---|---|"]
    L += [f"| {k} | `{v['fn'].__name__}` {v.get('opt', '') or ''} | {v.get('desc', '')} |" for k, v in score["instruments"].items()]
    L += ["", "## Sections (section = scene, picture cut = downbeat)", "",
          "| Scene | Time (s) | Bars | BPM | Content |", "|---|---|---|---|---|"]
    for sid, s in secs.items():
        bars = s["bars"]
        meter = f"{len(bars)}" + (f" (closing bar {bars[-1]} beats)" if bars[-1] != score["bpb"] else "")
        L.append(f"| {sid} | {s['start']:.2f}-{s['end']:.2f} | {meter} | {s['bpm']} | {score['sections'][sid].get('desc', '')} |")
    mix, mix_ff = levels["mix_own"], levels["mix_ffmpeg"]
    L += ["", "## Levels (fixed step per section, no ducking)", "",
          f"- Mix rule: {levels['mix_rule']}."]
    if mix:
        L.append(f"- Whole mix (own BS.1770 meter): **{mix['I_lufs']} LUFS**, true peak **{mix['true_peak_dbtp']} dBTP**"
                 + (f"; ffmpeg ebur128 cross-check: {mix_ff['I_lufs']} LUFS, {mix_ff['true_peak_dbtp']} dBTP" if mix_ff["I_lufs"] is not None else "")
                 + f"; limiter (speech peaks only) max. {levels['limiter_max_db']} dB on {levels['limiter_samples']} samples.")
    L += [f"- Bed under speech: {levels['bed_lufs_min_max'][0]} to {levels['bed_lufs_min_max'][1]} LUFS (target {BED_LUFS:.0f} +-2); "
          f"foreground in pauses max. {levels['foreground_lufs_max']} LUFS (limit -24; target {FG_LUFS} from 3 s pause, "
          "shorter transition pauses up to 4 dB lower so that nothing pumps).",
          f"- Band 1-4 kHz, share of the music energy: under speech {levels['midband_1_4khz_share_pct']['under_speech']} %, "
          f"in pauses {levels['midband_1_4khz_share_pct']['in_pauses']} %.",
          "- Column 'Step': fixed gain raw mix -> music.wav per segment (derived from the measurement); "
          "music LUFS on the final scale (after normalising the whole mix).", "",
          "| Kind | Window | Time (s) | Step (dB) | Music LUFS (own) | Music LUFS (ffmpeg) |", "|---|---|---|---|---|---|"]
    for r in levels["segments"]:
        L.append(f"| {r['kind']} | {r['label']} | {r['start']:.2f}-{r['end']:.2f} | {r['gain_db']} | {r['music_lufs_final']} | {r['music_lufs_final_ffmpeg']} |")
    if levels["short_term_3s_in_long_pauses"]:
        L += ["", "Short-term loudness S (3 s window) of the whole mix in pauses of 3 s and more (only music sounds there):", "",
              "| Pause (s) | Window (s) | S (LUFS) |", "|---|---|---|"]
        L += [f"| {r['pause']} | {r['window']} | {r['S_lufs_mix']} |" for r in levels["short_term_3s_in_long_pauses"]]
    L += ["", "## Novelty proof (interval n-grams of the melody against earlier pieces)", "",
          f"Melody of this piece: {nov['melody_notes']} notes, {nov['distinct_durations']} distinct durations."]
    if nov["compare"]:
        L += ["", "| Reference | Layer | n | distinct own | distinct reference | shared | own occurrences also in reference |",
              "|---|---|---|---|---|---|---|"]
        for ref, layers in nov["compare"].items():
            for layer, row in layers.items():
                for n, g in row["ngram"].items():
                    L.append(f"| {ref} | {layer} | {n} | {g['distinct_own']} | {g['distinct_reference']} | {g['shared']} | "
                             f"{g['own_occurrences_shared_pct']} % |")
    else:
        L += ["", "No reference given (`--compare`), nothing to compare against."]
    L += ["", d.get("different", ""), "", "## Production", "",
          f"- Score written by hand in `{score_file}`: chord chart per bar, "
          "written-out melody phrases with bar/beat position, accompaniment figures per section; realised by `engine.py`, sound by `synth.py`.",
          f"- Python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}; 48 kHz, stereo, 24 bit; deterministic (fixed noise keys).",
          f"- Room: synthetic reverb impulse response T60 {score['reverb']['t60']} s, wet {score['reverb']['wet']}"
          + (f"; echo {score['echo']['delay_sec']} s, feedback {score['echo']['fb']}" if score.get("echo") else "") + ".",
          f"- Foreground voices reaching more than 0.12 s into a word: {len(issues)}.", ""]
    (out / "ARRANGEMENT.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
