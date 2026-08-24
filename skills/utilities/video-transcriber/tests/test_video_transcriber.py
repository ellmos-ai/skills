import json
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import video_transcriber as vt
from video_transcriber import extract_video_id


# --------------------------------------------------------------------------
# Bestand: URL-Erkennung
# --------------------------------------------------------------------------

def test_extract_video_id_accepts_trusted_youtube_hosts():
    assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_video_id_rejects_lookalike_hosts():
    assert extract_video_id("https://evil-youtube.com/watch?v=dQw4w9WgXcQ") == ""
    assert extract_video_id("https://youtube.com.evil.test/watch?v=dQw4w9WgXcQ") == ""
    assert extract_video_id("https://youtube-nocookie.com.evil.test/embed/dQw4w9WgXcQ") == ""


# --------------------------------------------------------------------------
# Sprachwahl: de-orig, Basis-Sprache, manuell vor auto  (Ticketpunkt 3)
# --------------------------------------------------------------------------

def test_base_language_normalisierung():
    assert vt._base_lang("de-orig") == "de"
    assert vt._base_lang("de-DE") == "de"
    assert vt._base_lang("de") == "de"
    assert vt._base_lang("en-US") == "en"
    assert vt._base_lang("") == ""


def test_sprachwahl_exakt_vor_basis():
    """Ein exakter Treffer schlaegt den Basis-Sprachtreffer."""
    tracks = {"de-orig": [{"ext": "json3", "url": "u-orig"}],
              "de": [{"ext": "json3", "url": "u-de"}]}
    gewaehlt = vt._pick_caption_track(tracks, ["de"])
    assert gewaehlt[0] == "de"


def test_sprachwahl_findet_de_orig_ueber_basis():
    """de-orig muss ueber die Basis-Sprache gefunden werden -- das war der Defekt."""
    tracks = {"de-orig": [{"ext": "json3", "url": "u-orig"}]}
    gewaehlt = vt._pick_caption_track(tracks, ["de"])
    assert gewaehlt is not None
    assert gewaehlt[0] == "de-orig"


def test_sprachwahl_respektiert_reihenfolge_der_wunschsprachen():
    tracks = {"en": [{"ext": "json3", "url": "u-en"}],
              "de": [{"ext": "json3", "url": "u-de"}]}
    assert vt._pick_caption_track(tracks, ["de", "en"])[0] == "de"
    assert vt._pick_caption_track(tracks, ["en", "de"])[0] == "en"


def test_sprachwahl_verlangt_json3():
    tracks = {"de": [{"ext": "vtt", "url": "u-vtt"}]}
    assert vt._pick_caption_track(tracks, ["de"]) is None


def test_ytdlp_fallback_bevorzugt_manuell_vor_auto():
    """Auch im Fallback gilt: manuelle Untertitel vor automatischen."""
    info = {
        "subtitles": {"de": [{"ext": "json3", "url": "MANUELL"}]},
        "automatic_captions": {"de": [{"ext": "json3", "url": "AUTO"}]},
    }
    geholt = {}

    def fake_get(url):
        geholt["url"] = url
        return json.dumps({"events": [{"tStartMs": 0, "dDurationMs": 1000,
                                       "segs": [{"utf8": "Hallo"}]}]})

    _patch_ytdlp(info)
    vt._http_get_text = fake_get
    ergebnis = vt.fetch_transcript_ytdlp("vid00000001", ["de"])
    assert geholt["url"] == "MANUELL"
    assert ergebnis["is_generated"] is False


# --------------------------------------------------------------------------
# JSON3-Parser  (Ticketpunkt 1)
# --------------------------------------------------------------------------

def test_json3_parser_baut_segmente_in_primaerform():
    """Der Fallback muss dieselbe Segmentform liefern wie der Primaerweg."""
    roh = json.dumps({"events": [
        {"tStartMs": 1500, "dDurationMs": 2000, "segs": [{"utf8": "Guten "}, {"utf8": "Tag"}]},
    ]})
    segmente = vt._parse_json3(roh)
    assert segmente == [{"start": 1.5, "duration": 2.0, "text": "Guten Tag"}]
    assert isinstance(segmente[0]["start"], float)
    assert isinstance(segmente[0]["duration"], float)


def test_json3_parser_ueberspringt_ereignisse_ohne_segs():
    """Padding-Ereignisse duerfen keine leeren Segmente erzeugen."""
    roh = json.dumps({"events": [
        {"tStartMs": 0, "dDurationMs": 500},
        {"tStartMs": 500, "dDurationMs": 500, "segs": [{"utf8": "\n"}]},
        {"tStartMs": 1000, "dDurationMs": 500, "segs": [{"utf8": "Text"}]},
    ]})
    segmente = vt._parse_json3(roh)
    assert len(segmente) == 1
    assert segmente[0]["text"] == "Text"


def test_json3_parser_haelt_utf8_unversehrt():
    roh = json.dumps({"events": [
        {"tStartMs": 0, "dDurationMs": 1000, "segs": [{"utf8": "Grüße über Ähren – ßß"}]},
        {"tStartMs": 1000, "dDurationMs": 1000, "segs": [{"utf8": "日本語のテスト"}]},
    ]}, ensure_ascii=False)
    segmente = vt._parse_json3(roh)
    assert segmente[0]["text"] == "Grüße über Ähren – ßß"
    assert segmente[1]["text"] == "日本語のテスト"


# --------------------------------------------------------------------------
# Fallback-Verkettung  (Ticketpunkt 1)
# --------------------------------------------------------------------------

def _patch_ytdlp(info):
    """Ersetzt yt_dlp.YoutubeDL durch einen Stub, der `info` liefert."""
    class FakeYDL:
        def __init__(self, opts=None):
            FakeYDL.opts = opts or {}

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def extract_info(self, url, download=False):
            FakeYDL.download_arg = download
            return info

    fake_modul = type(sys)("yt_dlp")
    fake_modul.YoutubeDL = FakeYDL
    sys.modules["yt_dlp"] = fake_modul
    return FakeYDL


def test_fallback_springt_ein_wenn_primaerweg_leer_bleibt(monkeypatch):
    """Der reproduzierte Fall: primaer 'no element found', Fallback liefert Text."""
    monkeypatch.setattr(vt, "fetch_transcript_primary",
                        lambda vid, langs: {"segments": [], "language": "", "is_generated": False,
                                            "full_text": "", "error": "no element found: line 1, column 0"})
    _patch_ytdlp({"automatic_captions": {"de-orig": [{"ext": "json3", "url": "U"}]}})
    monkeypatch.setattr(vt, "_http_get_text",
                        lambda url: json.dumps({"events": [{"tStartMs": 0, "dDurationMs": 1000,
                                                            "segs": [{"utf8": "Inhalt"}]}]}))

    ergebnis = vt.fetch_transcript("vid00000001", ["de"])
    assert ergebnis["segments"]
    assert ergebnis["source"] == "yt-dlp"
    assert ergebnis["full_text"] == "Inhalt"
    assert "error" not in ergebnis or not ergebnis["error"]


def test_primaerweg_gewinnt_wenn_er_liefert(monkeypatch):
    monkeypatch.setattr(vt, "fetch_transcript_primary",
                        lambda vid, langs: {"segments": [{"start": 0.0, "duration": 1.0, "text": "Primaer"}],
                                            "language": "de", "is_generated": False, "full_text": "Primaer"})
    def darf_nicht(*a, **k):
        raise AssertionError("Fallback haette nicht laufen duerfen")
    monkeypatch.setattr(vt, "fetch_transcript_ytdlp", darf_nicht)

    ergebnis = vt.fetch_transcript("vid00000001", ["de"])
    assert ergebnis["source"] == "youtube_transcript_api"
    assert ergebnis["full_text"] == "Primaer"


def test_fallback_laedt_kein_video(monkeypatch):
    """Ticketauflage: kein Video-/Audio-Download."""
    fake = _patch_ytdlp({"automatic_captions": {"de": [{"ext": "json3", "url": "U"}]}})
    monkeypatch.setattr(vt, "_http_get_text",
                        lambda url: json.dumps({"events": [{"tStartMs": 0, "dDurationMs": 1,
                                                            "segs": [{"utf8": "x"}]}]}))
    vt.fetch_transcript_ytdlp("vid00000001", ["de"])
    assert fake.download_arg is False
    assert fake.opts.get("skip_download") is True
    # Keine Option, die yt-dlp Dateien schreiben laesst
    for verboten in ("writesubtitles", "writeautomaticsub", "outtmpl"):
        assert verboten not in fake.opts


def test_beide_wege_leer_meldet_fehler(monkeypatch):
    monkeypatch.setattr(vt, "fetch_transcript_primary",
                        lambda vid, langs: {"segments": [], "language": "", "is_generated": False,
                                            "full_text": "", "error": "no element found"})
    _patch_ytdlp({"automatic_captions": {}, "subtitles": {}})
    ergebnis = vt.fetch_transcript("vid00000001", ["de"])
    assert ergebnis["segments"] == []
    assert ergebnis.get("error")


# --------------------------------------------------------------------------
# Exit-Semantik  (Ticketpunkt 2 -- der eigentliche Defekt)
# --------------------------------------------------------------------------

def _run_main(monkeypatch, argv, transcript, meta=None):
    monkeypatch.setattr(sys, "argv", ["video_transcriber.py"] + argv)
    monkeypatch.setattr(vt, "fetch_metadata", lambda vid: meta or {"title": "T", "url": "u", "video_id": vid})
    monkeypatch.setattr(vt, "fetch_transcript", lambda vid, langs: transcript)
    with pytest.raises(SystemExit) as exc:
        vt.main()
    return exc.value.code


LEER = {"segments": [], "language": "", "is_generated": False, "full_text": "",
        "error": "no element found: line 1, column 0", "source": None}
VOLL = {"segments": [{"start": 0.0, "duration": 1.0, "text": "Da"}], "language": "de",
        "is_generated": True, "full_text": "Da", "source": "yt-dlp"}


def test_leeres_transkript_ist_kein_erfolg(monkeypatch, capsys):
    """Kern des Tickets: Exit 0 bei leerem Transkript war der Defekt."""
    code = _run_main(monkeypatch, ["https://youtu.be/dQw4w9WgXcQ"], LEER)
    assert code == vt.EXIT_NO_TRANSCRIPT
    assert code != 0


def test_gefuelltes_transkript_ist_erfolg(monkeypatch):
    assert _run_main(monkeypatch, ["https://youtu.be/dQw4w9WgXcQ"], VOLL) == 0


def test_meta_only_bleibt_erfolg_trotz_leerem_transkript(monkeypatch):
    """Wer kein Transkript anfordert, darf nicht an dessen Fehlen scheitern."""
    assert _run_main(monkeypatch, ["https://youtu.be/dQw4w9WgXcQ", "--meta-only"], LEER) == 0


def test_allow_empty_erzwingt_erfolg(monkeypatch):
    code = _run_main(monkeypatch, ["https://youtu.be/dQw4w9WgXcQ", "--allow-empty-transcript"], LEER)
    assert code == 0


def test_ungueltige_url_bleibt_exit_1(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["video_transcriber.py", "https://evil-youtube.com/watch?v=x"])
    with pytest.raises(SystemExit) as exc:
        vt.main()
    assert exc.value.code == vt.EXIT_BAD_URL


def test_no_meta_mit_transkript_ist_erfolg(monkeypatch):
    assert _run_main(monkeypatch, ["https://youtu.be/dQw4w9WgXcQ", "--no-meta"], VOLL) == 0


# --------------------------------------------------------------------------
# Ausgabeformate  (Ticketpunkt 4)
# --------------------------------------------------------------------------

META = {"title": "Prüfung", "channel": "Kanal", "url": "https://youtu.be/x", "video_id": "x"}
TRANS_UTF8 = {"segments": [{"start": 65.0, "duration": 2.0, "text": "Grüße – 日本語"}],
              "language": "de-orig", "is_generated": True, "full_text": "Grüße – 日本語",
              "source": "yt-dlp"}


@pytest.mark.parametrize("formatierer", ["markdown", "plain", "json"])
def test_alle_drei_formate_halten_utf8(formatierer):
    if formatierer == "markdown":
        out = vt.format_markdown(META, TRANS_UTF8)
    elif formatierer == "plain":
        out = vt.format_plain(META, TRANS_UTF8)
    else:
        out = vt.format_json(META, TRANS_UTF8)
    assert "Grüße" in out
    assert "日本語" in out


def test_json_ausgabe_nennt_die_quelle():
    """Ohne dieses Feld bleibt unsichtbar, ob der Fallback gegriffen hat."""
    daten = json.loads(vt.format_json(META, TRANS_UTF8))
    assert daten["transcript"]["source"] == "yt-dlp"


def test_markdown_und_plain_zeigen_zeitstempel():
    assert "1:05" in vt.format_markdown(META, TRANS_UTF8)
    assert "1:05" in vt.format_plain(META, TRANS_UTF8)


def test_formate_zeigen_fehler_statt_leerer_stille():
    for out in (vt.format_markdown(META, LEER), vt.format_plain(META, LEER)):
        assert "no element found" in out
