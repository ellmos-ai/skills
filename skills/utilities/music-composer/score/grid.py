"""Bar grid per piece: section = scene, section start = picture cut = downbeat.

Every section gets whole bars; the tempo is adjusted slightly per section (the deviation from the base
tempo is reported) so that every picture cut falls on a beat one. Prints a spotting sheet:
bar -> start time, speech (#) / pause (.) per beat.

    python grid.py --speech-map speech-map.json --bpm 116 --beats-per-bar 2
"""
import argparse

from timeline import load_speech_map


def build_grid(speech_map, bpm, beats_per_bar):
    """Sections with their bar list. Whole beats per section; a remainder becomes a short closing bar
    before the cut (e.g. 2/4 within 4/4). In 4/4 there is no 1-beat remainder."""
    beat0 = 60.0 / bpm
    sections = []
    for sc in speech_map["scenes"]:
        dur = sc["end"] - sc["start"]
        k0 = round(dur / beat0)
        cands = [k for k in (k0 - 1, k0, k0 + 1) if k > 0 and not (beats_per_bar == 4 and k % 4 == 1)]
        k = min(cands, key=lambda k: abs(dur / k - beat0))
        bars = [beats_per_bar] * (k // beats_per_bar) + ([k % beats_per_bar] if k % beats_per_bar else [])
        beat = dur / k
        t, starts = sc["start"], []
        for b in bars:
            starts.append(t)
            t += b * beat
        sections.append({
            "id": sc["id"], "start": sc["start"], "end": sc["end"], "bars": bars, "bar_starts": starts,
            "beat_sec": beat, "beats_per_bar": beats_per_bar, "bpm": round(60.0 / beat, 2),
            "tempo_dev_pct": round(100 * (beat0 / beat - 1), 2),
        })
    return sections


def speech_fraction(speech_map, t0, t1):
    s = 0.0
    for v in speech_map["voices"]:
        s += max(0.0, min(t1, v["speech_end"]) - max(t0, v["speech_start"]))
    return s / (t1 - t0)


def sheet(speech_map, bpm, bpb):
    out = []
    for sec in build_grid(speech_map, bpm, bpb):
        out.append(f"== {sec['id']}  {sec['start']:.3f}-{sec['end']:.3f}  {len(sec['bars'])} bars "
                   f"(closing bar {sec['bars'][-1]}/{bpb} beats)  {sec['bpm']} BPM ({sec['tempo_dev_pct']:+.2f} %)")
        for k, (t0, nb) in enumerate(zip(sec["bar_starts"], sec["bars"])):
            b = sec["beat_sec"]
            beats = "".join("#" if speech_fraction(speech_map, t0 + j * b, t0 + (j + 1) * b) > 0.3 else "." for j in range(nb))
            out.append(f"  bar {k + 1:02d}  {t0:7.2f}  {beats}")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Print the bar grid / spotting sheet for a speech map.")
    ap.add_argument("--speech-map", required=True)
    ap.add_argument("--bpm", type=float, required=True, help="base tempo in beats per minute")
    ap.add_argument("--beats-per-bar", type=int, required=True)
    a = ap.parse_args()
    print(sheet(load_speech_map(a.speech_map), a.bpm, a.beats_per_bar))
