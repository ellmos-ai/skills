import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from video_transcriber import extract_video_id


def test_extract_video_id_accepts_trusted_youtube_hosts():
    assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_video_id_rejects_lookalike_hosts():
    assert extract_video_id("https://evil-youtube.com/watch?v=dQw4w9WgXcQ") == ""
    assert extract_video_id("https://youtube.com.evil.test/watch?v=dQw4w9WgXcQ") == ""
    assert extract_video_id("https://youtube-nocookie.com.evil.test/embed/dQw4w9WgXcQ") == ""
