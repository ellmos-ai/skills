"""Tests for the score mode: the real build code runs on the neutral example speech map with a minimal score
and synthetic narration clips. Skipped when numpy/scipy are missing (they are only needed for this mode)."""
import contextlib
import hashlib
import importlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

try:
    import numpy as np
    from scipy.io import wavfile
except ImportError:
    np = None

SCORE_DIR = Path(__file__).resolve().parents[1] / "score"
EXAMPLES = SCORE_DIR / "examples"
MODULES = ("build", "check", "engine", "grid", "synth", "timeline", "viz")  # they import each other by plain name

# Minimal score for the first scene of the example speech map (8 bars as printed by grid.py at 116 BPM, 2 beats per bar).
MINI = '''
import synth

BARS = {"intro": 8}
SCORE = {
    "id": "mini", "title": "Mini test score", "key": "C major", "bpm": 116, "bpb": 2,
    "beat_quarters": 1.0, "ts_den": 4, "ts_num_per_beat": 1, "scale": [0, 2, 4, 5, 7, 9, 11],
    "instruments": {
        "lead": dict(fn=synth.fm_bell, pan=0.0, send=0.2, gain=1.0, program=9, fg=True),
        "bass": dict(fn=synth.chip_tri, pan=0.0, send=0.05, gain=0.8, program=38),
    },
    "melody": ["lead"],
    "reverb": dict(t60=0.8, predelay=0.01, damp=4000, wet=0.15),
    "default_parts": {"bass": dict(inst="bass", pattern=[(0, .8, "R")], range=(36, 47), vel=0.7)},
    "sections": {
        sid: {"chords": " | ".join(["C"] * n), "phrases": []} for sid, n in BARS.items()
    },
}
# melody C5 E5 G5 C6 in the pause at the end of the speech, then a ringing C5 as final note
SCORE["sections"]["intro"]["phrases"] = [("lead", "6:1", "C5:1 E5:1 | G5:1 C6:1"), ("lead", "8:1", "C5*:2")]
'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@unittest.skipIf(np is None, "numpy/scipy not installed (needed for the score mode only)")
class ScoreModeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._saved = {name: sys.modules.pop(name) for name in MODULES if name in sys.modules}
        sys.path.insert(0, str(SCORE_DIR))
        cls.addClassCleanup(cls._restore_modules)
        cls.build = importlib.import_module("build")
        cls.check = importlib.import_module("check")
        cls.timeline = importlib.import_module("timeline")
        cls.engine = importlib.import_module("engine")
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        cls.tmp = Path(tmp.name)
        cls.speech_map = EXAMPLES / "speech-map.json"
        full = json.loads(cls.speech_map.read_text(encoding="utf-8"))  # first scene only: keeps the render short
        cls.short_map = cls.tmp / "speech-map-short.json"
        cls.short_map.write_text(json.dumps({"duration": 8.3, "scenes": full["scenes"][:1], "voices": full["voices"][:1]}),
                                 encoding="utf-8")
        cls.mini = cls.tmp / "mini_score.py"
        cls.mini.write_text(MINI, encoding="utf-8")
        cls.narration = cls.tmp / "narration"
        cls.narration.mkdir()
        for v in cls.timeline.load_speech_map(cls.short_map)["voices"]:  # synthetic voice: 140 Hz harmonics with a syllable-like envelope, 48 kHz mono
            t = np.arange(int(v["clip_dur"] * 48000)) / 48000
            x = sum(np.sin(2 * np.pi * 140 * k * t) / k for k in range(1, 20)) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.5 * t))
            wavfile.write(cls.narration / f"{v['id']}.wav", 48000, (0.1 * x).astype(np.float32))
        cls.refs = {}
        for name, midis in (("same.notes.json", [60, 64, 67, 72, 60]), ("other.notes.json", [60, 61, 62, 63, 64, 65])):
            notes = [{"t": i * 0.5, "layer": "lead", "midi": mm, "dur": 0.5} for i, mm in enumerate(midis)]
            (cls.tmp / name).write_text(json.dumps({"notes": notes}), encoding="utf-8")
            cls.refs[name] = cls.tmp / name
        cls.out = cls.tmp / "out"
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cls.engine, "HAVE_FFMPEG", False):  # cross-check: own test below
            cls.build.main(["--speech-map", str(cls.short_map), "--variant", str(cls.mini), "--out", str(cls.out),
                            "--narration-dir", str(cls.narration), "--compare", *map(str, cls.refs.values())])

    @classmethod
    def _restore_modules(cls):
        sys.path.remove(str(SCORE_DIR))
        for name in MODULES:
            sys.modules.pop(name, None)
        sys.modules.update(cls._saved)

    def test_outputs_exist_and_are_valid(self):
        for name in ("music.wav", "preview-mix.wav", "score.mid", "score.json", "notes.json", "levels.json",
                     "novelty.json", "ARRANGEMENT.md"):
            self.assertTrue((self.out / name).is_file(), name)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.check.main([str(self.out), "--duration", "8.3"]), 0)
        rate, x = wavfile.read(self.out / "music.wav")
        self.assertEqual((rate, x.shape), (48000, (int(8.3 * 48000), 2)))
        self.assertGreater(np.abs(x).max(), 0)

    def test_levels_follow_the_fixed_steps(self):
        lv = json.loads((self.out / "levels.json").read_text(encoding="utf-8"))
        self.assertTrue(all(-36.3 <= v <= -35.7 for v in lv["bed_lufs_min_max"]), lv["bed_lufs_min_max"])
        self.assertLessEqual(lv["foreground_lufs_max"], -23.5)
        self.assertAlmostEqual(lv["mix_own"]["I_lufs"], -16.0, delta=0.2)
        self.assertLessEqual(lv["mix_own"]["true_peak_dbtp"], -1.4)
        kinds = {r["kind"] for r in lv["segments"]}
        self.assertEqual(kinds, {"bed", "fg", "gap"})

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed (optional cross-check)")
    def test_own_loudness_meter_agrees_with_ffmpeg(self):
        lv = json.loads((self.out / "levels.json").read_text(encoding="utf-8"))
        bed = next(r for r in lv["segments"] if r["kind"] == "bed")
        with mock.patch.object(self.engine, "HAVE_FFMPEG", True):
            ff = self.engine.ffmpeg_lufs(self.out / "music.wav", bed["start"], bed["end"])[0]
        self.assertAlmostEqual(ff + lv["normalization_db"], bed["music_lufs_final"], delta=0.3)

    def test_novelty_detects_shared_intervals_and_has_a_negative_control(self):
        nov = json.loads((self.out / "novelty.json").read_text(encoding="utf-8"))
        same = nov["compare"]["same.notes.json"]["lead"]["ngram"]
        other = nov["compare"]["other.notes.json"]["lead"]["ngram"]
        self.assertEqual(nov["melody_notes"], 5)
        self.assertEqual((same["3"]["shared"], same["4"]["shared"]), (2, 1))  # same interval pattern as the reference
        self.assertEqual({other[n]["shared"] for n in ("3", "4", "5")}, {0})  # unrelated reference: nothing shared

    def test_refuses_a_non_empty_output_folder_and_leaves_it_alone(self):
        before = sha(self.out / "music.wav")
        with self.assertRaises(SystemExit) as cm:
            self.build.main(["--speech-map", str(self.short_map), "--variant", str(self.mini), "--out", str(self.out)])
        self.assertIn("not empty", str(cm.exception))
        self.assertEqual(sha(self.out / "music.wav"), before)

    def test_example_score_matches_the_example_speech_map(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.build.main(["--speech-map", str(self.speech_map), "--variant", str(EXAMPLES / "march.py"), "--check"])
        self.assertIn("check ok: 4 sections", buf.getvalue())
        self.assertIn("foreground overlaps 0", buf.getvalue())

    def test_wrong_bar_count_is_rejected(self):
        bad = self.tmp / "bad_score.py"
        bad.write_text(MINI + '\nSCORE["sections"]["intro"]["chords"] = "C | C"\n', encoding="utf-8")
        with self.assertRaises(AssertionError) as cm:
            self.build.main(["--speech-map", str(self.short_map), "--variant", str(bad), "--check"])
        self.assertIn("chord bars", str(cm.exception))

    def test_speech_map_derives_pauses(self):
        m = self.timeline.load_speech_map(self.speech_map)
        self.assertEqual([p["before"] for p in m["pauses"]],
                         ["v1_intro", "v2_problem", "v3_solution_a", "v4_solution_b", "v5_outro", "END"])
        self.assertAlmostEqual(m["pauses"][-1]["len"], 4.0, places=3)


if __name__ == "__main__":
    unittest.main()
