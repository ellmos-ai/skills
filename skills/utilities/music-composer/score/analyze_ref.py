"""Rough analysis of a reference recording (for comparison only): tempo by onset autocorrelation, pitch classes by chroma.

    python analyze_ref.py <wav> <start> <end> [<start> <end> ...]     (48 kHz WAV, windows in seconds)
"""
import sys

import numpy as np
from timeline import SR, load_wav

NAMES = "C C# D D# E F F# G G# A A# B".split()


def analyze(x):
    mono = x.mean(axis=1)
    hop, win = 512, 2048
    frames = 1 + (len(mono) - win) // hop
    w = np.hanning(win)
    spec = np.abs(np.array([np.fft.rfft(mono[i * hop:i * hop + win] * w) for i in range(frames)]))
    flux = np.maximum(np.diff(np.log1p(spec * 100), axis=0), 0).sum(axis=1)
    flux -= flux.mean()
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    fr = SR / hop
    lags = np.arange(len(ac)) / fr
    sel = (lags > 60 / 180) & (lags < 60 / 70)
    bpm = 60 / lags[sel][np.argmax(ac[sel])]
    freqs = np.fft.rfftfreq(win, 1 / SR)
    chroma = np.zeros(12)
    band = (freqs > 80) & (freqs < 2000)
    midi = np.round(69 + 12 * np.log2(freqs[band] / 440)).astype(int) % 12
    e = (spec[:, band] ** 2).sum(axis=0)
    np.add.at(chroma, midi, e)
    chroma /= chroma.max()
    top = np.argsort(chroma)[::-1][:7]
    return bpm, [(NAMES[i], round(float(chroma[i]), 2)) for i in top]


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    x = load_wav(sys.argv[1])
    args = list(map(float, sys.argv[2:]))
    for a, b in zip(args[::2], args[1::2]):
        bpm, ch = analyze(x[int(a * SR):int(b * SR)])
        print(f"{a:6.1f}-{b:6.1f}s  ~{bpm:5.1f} BPM  Chroma: {ch}")
