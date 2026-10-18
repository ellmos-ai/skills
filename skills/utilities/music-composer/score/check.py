"""Acceptance check of built pieces: WAV format and length (complete decode) and a readable MIDI file.

    python check.py <out folder> [<out folder> ...] [--duration SECONDS]

Looks for music.wav, preview-mix.wav (optional) and score.mid in every folder. Exit code 1 if a file is
missing or damaged or, with --duration, if a WAV is more than 10 ms off that length. Needs no ffmpeg.
"""
import argparse
import pathlib
import struct
import sys
import wave


def wav_info(path):
    """Format and length; raises if the file is truncated (frames announced in the header are missing)."""
    with wave.open(str(path), "rb") as w:
        n, ch, width, rate = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        data = w.readframes(n)
    if len(data) != n * ch * width:
        raise ValueError(f"truncated: {len(data)} of {n * ch * width} bytes")
    return {"rate": rate, "channels": ch, "bits": 8 * width, "seconds": n / rate}


def _vlq(tr, i):
    v = 0
    while True:
        c = tr[i]
        i += 1
        v = (v << 7) | (c & 0x7F)
        if c < 0x80:
            return v, i


def midi_info(path):
    """Standard MIDI File summary: format, track count, note-on count, end of the last event in seconds."""
    b = pathlib.Path(path).read_bytes()
    if b[:4] != b"MThd":
        raise ValueError("not a MIDI file")
    _, fmt, ntrk, tpq = struct.unpack(">IHHH", b[4:14])
    pos, tracks = 14, []
    while pos < len(b):
        ln = struct.unpack(">I", b[pos + 4:pos + 8])[0]
        tracks.append(b[pos + 8:pos + 8 + ln])
        pos += 8 + ln
    tempo, notes, last_tick = [], 0, 0
    for tr in tracks:
        i, tick, status = 0, 0, 0
        while i < len(tr):
            v, i = _vlq(tr, i)
            tick += v
            if tr[i] == 0xFF:  # meta event
                typ = tr[i + 1]
                ln, j = _vlq(tr, i + 2)
                if typ == 0x51:
                    tempo.append((tick, int.from_bytes(tr[j:j + 3], "big")))
                i = j + ln
                continue
            if tr[i] & 0x80:
                status = tr[i]
                i += 1
            if status & 0xF0 == 0x90 and tr[i + 1] > 0:
                notes += 1
            i += 1 if status & 0xF0 in (0xC0, 0xD0) else 2
            last_tick = max(last_tick, tick)
    tempo.sort()
    sec, prev_t, prev_us = 0.0, 0, tempo[0][1]
    for t, us in tempo[1:]:
        sec += (t - prev_t) / tpq * prev_us / 1e6
        prev_t, prev_us = t, us
    sec += (last_tick - prev_t) / tpq * prev_us / 1e6
    return {"format": fmt, "tracks": ntrk, "notes": notes, "seconds": sec}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="+")
    ap.add_argument("--duration", type=float)
    args = ap.parse_args(argv)
    bad = 0
    for folder in map(pathlib.Path, args.folders):
        for name in ("music.wav", "preview-mix.wav", "score.mid"):
            path = folder / name
            if not path.exists():
                if name != "preview-mix.wav":  # only exists when narration was given
                    print(f"[{folder.name}] {name}: MISSING")
                    bad += 1
                continue
            try:
                if name.endswith(".wav"):
                    info = wav_info(path)
                    line = f"{info['rate']} Hz, {info['channels']} ch, {info['bits']} bit, {info['seconds']:.3f} s"
                    if args.duration is not None and abs(info["seconds"] - args.duration) > 0.01:
                        line += f"  LENGTH != {args.duration} s"
                        bad += 1
                else:
                    info = midi_info(path)
                    line = f"SMF type {info['format']}, {info['tracks']} tracks, {info['notes']} notes, last event ends at {info['seconds']:.2f} s"
            except (ValueError, IndexError, EOFError, wave.Error, struct.error) as e:
                line = f"DAMAGED ({e})"
                bad += 1
            print(f"[{folder.name}] {name}: {line}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
