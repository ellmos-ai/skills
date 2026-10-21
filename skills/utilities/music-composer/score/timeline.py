"""Speech map: scenes, speech windows (activity-trimmed) and speech pauses.

The voice is the time axis of the piece. A speech map is a JSON file:

    {"duration": 42.0,
     "scenes": [{"id": "intro", "start": 0.0, "end": 8.0}, ...],
     "voices": [{"id": "v1", "clip_start": 0.7, "clip_dur": 4.7,
                 "speech_start": 0.8, "speech_end": 5.2}, ...],
     "pauses": [{"start": 5.2, "end": 8.75, "len": 3.55, "before": "v2"}, ...]}

`voices` are the speech windows (first/last audible moment of each narration clip), `pauses` the gaps
between them (`before` = id of the next voice, "END" for the gap after the last word). `pauses` is optional:
load_speech_map() derives it from the voices. Scenes must be contiguous and end at `duration`.

Build a map from narration clips:
    python timeline.py --timeline timeline.json --narration-dir clips/ -o speech-map.json [--extend-last-scene SEC]
where timeline.json is {"duration": s, "scenes": [{"id", "start", "duration"}], "voices": [{"id", "start"}]} and
clips/<voice id>.wav are the 48 kHz narration clips placed at `start`.
"""
import argparse
import json
import pathlib

import numpy as np
from scipy.io import wavfile

SR = 48000


def load_wav(path):
    """Read a 48 kHz WAV (16/24/32 bit or float) as float64 array of shape (n, 2)."""
    sr, x = wavfile.read(path)
    assert sr == SR, f"{path}: expected {SR} Hz, got {sr} Hz"
    if x.dtype == np.int32:  # scipy returns 24-bit PCM as left-aligned int32
        x = x.astype(np.float64) / 2**31
    elif x.dtype == np.int16:
        x = x.astype(np.float64) / 2**15
    else:
        x = x.astype(np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    return x


def active_span(x, thresh_db=-50.0, frame=0.01):
    """First/last frame whose RMS is above thresh_db (dBFS)."""
    mono = x.mean(axis=1)
    n = int(frame * SR)
    frames = len(mono) // n
    rms = np.sqrt((mono[: frames * n].reshape(frames, n) ** 2).mean(axis=1) + 1e-20)
    db = 20 * np.log10(rms)
    idx = np.where(db > thresh_db)[0]
    return idx[0] * frame, (idx[-1] + 1) * frame


def derive_pauses(voices, duration):
    """Gaps between speech windows (longer than 50 ms), plus the gap after the last word (`before` = "END")."""
    pauses, t = [], 0.0
    for v in voices:
        if v["speech_start"] - t > 0.05:
            pauses.append({"start": round(t, 3), "end": v["speech_start"],
                           "len": round(v["speech_start"] - t, 3), "before": v["id"]})
        t = v["speech_end"]
    pauses.append({"start": t, "end": duration, "len": round(duration - t, 3), "before": "END"})
    return pauses


def load_speech_map(path):
    """Load and check a speech map; derive `pauses` if the file has none."""
    m = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    assert m["scenes"] and m["voices"], f"{path}: needs at least one scene and one voice"
    assert abs(m["scenes"][-1]["end"] - m["duration"]) < 0.01, f"{path}: last scene must end at `duration`"
    for a, b in zip(m["scenes"], m["scenes"][1:]):
        assert abs(a["end"] - b["start"]) < 0.01, f"{path}: scenes {a['id']} / {b['id']} are not contiguous"
    m.setdefault("pauses", derive_pauses(m["voices"], m["duration"]))
    return m


def build(timeline_path, narration_dir, extend_last_scene=0.0):
    """Speech map from a scene/clip timeline and the narration clips (see module docstring)."""
    tl = json.loads(pathlib.Path(timeline_path).read_text(encoding="utf-8"))
    voices = []
    for v in tl["voices"]:
        x = load_wav(pathlib.Path(narration_dir) / f"{v['id']}.wav")
        a, b = active_span(x)
        voices.append({
            "id": v["id"], "clip_start": round(v["start"], 6),
            "clip_dur": round(len(x) / SR, 4),
            "speech_start": round(v["start"] + a, 3),
            "speech_end": round(v["start"] + b, 3),
        })
    duration = round(tl["duration"] + extend_last_scene, 4)
    scenes = [{"id": s["id"], "start": round(s["start"], 4), "end": round(s["start"] + s["duration"], 4)}
              for s in tl["scenes"]]
    scenes[-1]["end"] = duration
    return {"duration": duration, "scenes": scenes, "voices": voices, "pauses": derive_pauses(voices, duration),
            "source": f"{pathlib.Path(timeline_path).name} + narration clips (activity threshold -50 dBFS, 10 ms frames)"
                      + (f"; last scene extended by {extend_last_scene} s" if extend_last_scene else "")}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a speech map from a timeline and narration clips.")
    ap.add_argument("--timeline", required=True, help="timeline.json (duration, scenes, voices with start)")
    ap.add_argument("--narration-dir", required=True, help="directory with <voice id>.wav clips (48 kHz)")
    ap.add_argument("-o", "--out", required=True, help="speech map JSON to write")
    ap.add_argument("--extend-last-scene", type=float, default=0.0,
                    help="seconds to add to the end of the last scene (e.g. a longer end card)")
    args = ap.parse_args(argv)
    m = build(args.timeline, args.narration_dir, args.extend_last_scene)
    pathlib.Path(args.out).write_text(json.dumps(m, indent=1), encoding="utf-8")
    print("SCENES")
    for s in m["scenes"]:
        print(f"  {s['id']:13s} {s['start']:7.3f} - {s['end']:7.3f}")
    print("SPEECH")
    for v in m["voices"]:
        print(f"  {v['id']:20s} {v['speech_start']:7.3f} - {v['speech_end']:7.3f}")
    print("PAUSES")
    for p in m["pauses"]:
        print(f"  {p['start']:7.3f} - {p['end']:7.3f}  {p['len']:6.3f}s  before {p['before']}")


if __name__ == "__main__":
    main()
