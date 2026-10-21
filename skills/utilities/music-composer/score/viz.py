"""Visual check without listening: piano roll (notes over the speech windows) and spectrogram of the music as PNG.

    python viz.py <out folder> --speech-map speech-map.json [--png-dir DIR]

Reads <out folder>/notes.json and music.wav, writes pianoroll.png and spectrogram.png (default: <out folder>/qa).
Piano roll: grey = speech, black lines = scene cuts, one colour per instrument. Spectrogram: green lines mark 1 kHz and
4 kHz (the band that should stay free under speech), white bars on top mark the speech windows.
"""
import argparse
import json
import pathlib
import struct
import zlib

import numpy as np
from timeline import load_speech_map, load_wav

PAL = [(230, 80, 60), (60, 140, 230), (240, 180, 40), (90, 190, 110), (180, 90, 200), (40, 190, 190),
       (240, 120, 180), (150, 150, 150), (200, 200, 90), (110, 110, 230)]


def write_png(path, rgb):
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(h))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def pianoroll(notes, m, rows=3, w=1800, lo=36, hi=100, ph=5):
    dur = m["duration"]
    insts = sorted({n["inst"] for n in notes if n["midi"] is not None})
    span = dur / rows
    H = (hi - lo) * ph
    img = np.full((rows * (H + 12), w, 3), 255, np.uint8)
    for r in range(rows):
        y0 = r * (H + 12)
        t0 = r * span

        def px(t):
            return int((t - t0) / span * (w - 1))

        for v in m["voices"]:
            a, b = max(px(v["speech_start"]), 0), min(px(v["speech_end"]), w - 1)
            if b > a:
                img[y0:y0 + H, a:b] = (232, 232, 232)
        for mm in range(lo, hi, 12):
            img[y0 + (hi - mm) * ph - 1, :] = (200, 200, 255)
        for sc in m["scenes"]:
            x = px(sc["start"])
            if 0 <= x < w:
                img[y0:y0 + H, x] = (0, 0, 0)
        for n in notes:
            if n["midi"] is None or not (t0 <= n["t"] < t0 + span) or not (lo <= n["midi"] < hi):
                continue
            c = PAL[insts.index(n["inst"]) % len(PAL)]
            y = y0 + (hi - n["midi"]) * ph - ph
            a, b = px(n["t"]), max(px(n["t"]) + 1, min(px(n["t"] + n["dur"]), w - 1))
            img[y:y + ph - 1, a:b] = c
    return img, {i: PAL[k % len(PAL)] for k, i in enumerate(insts)}


def spectrogram(wav_path, m, w=1800, h=360):
    sr = 48000
    x = load_wav(wav_path).mean(axis=1)
    hop = len(x) // w
    win = 4096
    frames = np.array([np.abs(np.fft.rfft(x[i * hop:i * hop + win] * np.hanning(win))) if i * hop + win <= len(x)
                       else np.zeros(win // 2 + 1) for i in range(w)])
    f = np.fft.rfftfreq(win, 1 / sr)
    edges = np.geomspace(50, 14000, h + 1)
    img = np.zeros((h, w))
    for k in range(h):
        sel = (f >= edges[k]) & (f < edges[k + 1])
        if sel.any():
            img[h - 1 - k] = frames[:, sel].mean(axis=1)
    db = 20 * np.log10(img + 1e-9)
    db = np.clip((db - (db.max() - 70)) / 70, 0, 1)
    rgb = (np.stack([db ** 0.7, db ** 1.5, db ** 3], axis=2) * 255).astype(np.uint8)
    for fq in (1000, 4000):
        k = h - 1 - int(np.searchsorted(edges, fq))
        rgb[k, ::4] = (0, 255, 0)
    for v in m["voices"]:
        rgb[:4, int(v["speech_start"] / m["duration"] * w):int(v["speech_end"] / m["duration"] * w)] = (255, 255, 255)
    return rgb


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--speech-map", required=True)
    ap.add_argument("--png-dir")
    args = ap.parse_args(argv)
    folder = pathlib.Path(args.folder)
    png_dir = pathlib.Path(args.png_dir) if args.png_dir else folder / "qa"
    png_dir.mkdir(parents=True, exist_ok=True)
    m = load_speech_map(args.speech_map)
    notes = json.loads((folder / "notes.json").read_text(encoding="utf-8"))["notes"]
    img, colours = pianoroll(notes, m)
    write_png(png_dir / "pianoroll.png", img)
    write_png(png_dir / "spectrogram.png", spectrogram(folder / "music.wav", m))
    print(f"wrote {png_dir / 'pianoroll.png'} and {png_dir / 'spectrogram.png'}; instrument colours: {colours}")


if __name__ == "__main__":
    main()
