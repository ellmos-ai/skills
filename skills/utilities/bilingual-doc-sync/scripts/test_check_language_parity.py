"""Tests fuer check_language_parity.py (T-20260926-967984806)."""
from __future__ import annotations

from pathlib import Path

import check_language_parity as clp


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_file_lang_infers_from_filename(tmp_path: Path) -> None:
    assert clp.file_lang(Path("README.md")) == "en"
    assert clp.file_lang(Path("README_de.md")) == "de"
    assert clp.file_lang(Path("README-zh.md")) == "zh"


def test_file_lang_recognizes_region_code(tmp_path: Path) -> None:
    assert clp.file_lang(Path("README_zh-CN.md")) == "zh-cn"
    assert clp.file_lang(Path("README_zh_CN.md")) == "zh-cn"


def test_lang_only_unknown_code_is_reported_fail_closed(tmp_path: Path) -> None:
    en = _write(
        tmp_path,
        "README.md",
        "<!-- lang-only: cn -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    zh = _write(tmp_path, "README_zh.md", "Kein Skills-Link hier.")
    conflicts, notes = clp.check_parity([en, zh])
    assert len(conflicts) == 1
    assert "lang-only-Code 'cn'" in conflicts[0]
    assert "skilery.com" in conflicts[0]
    assert notes == []


def test_lang_only_prefix_covers_region_variant_link_present(tmp_path: Path) -> None:
    en = _write(
        tmp_path,
        "README.md",
        "<!-- lang-only: zh -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    zh_cn = _write(
        tmp_path,
        "README_zh-CN.md",
        "<!-- lang-only: zh -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    # Basis-Code "zh" deckt die Regionsvariante "zh-cn" ab -> kein Konflikt.
    conflicts, notes = clp.check_parity([en, zh_cn])
    assert conflicts == []


def test_lang_only_prefix_missing_in_region_variant_is_conflict(tmp_path: Path) -> None:
    en = _write(
        tmp_path,
        "README.md",
        "<!-- lang-only: zh -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    zh_cn = _write(tmp_path, "README_zh-CN.md", "Kein Skills-Link hier.")
    # "zh" deckt "zh-cn" ab, also IST README_zh-CN.md relevant -> fehlender
    # Link dort ist ein echter Konflikt.
    conflicts, notes = clp.check_parity([en, zh_cn])
    assert len(conflicts) == 1
    assert "README_zh-CN.md" in conflicts[0]


def test_lang_only_code_missing_from_subset_is_note_not_conflict(tmp_path: Path) -> None:
    en = _write(
        tmp_path,
        "README.md",
        "<!-- lang-only: zh -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    de = _write(tmp_path, "README_de.md", "Kein Skills-Link hier.")
    # README_zh.md existiert im selben Verzeichnis, wird aber in diesem
    # Aufruf NICHT uebergeben (Teilmengen-Aufruf) -- "zh" bleibt trotzdem
    # ein gueltiger Code, nur ein Hinweis, kein Exit-1-Konflikt.
    _write(tmp_path, "README_zh.md", "Skills宝-Link lebt hier.")
    conflicts, notes = clp.check_parity([en, de])
    assert conflicts == []
    assert len(notes) == 1
    assert "zh" in notes[0]


def test_identical_links_no_conflict(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", "See [docs](https://example.com/docs).")
    de = _write(tmp_path, "README_de.md", "Siehe [Doku](https://example.com/docs).")
    conflicts, notes = clp.check_parity([en, de])
    assert conflicts == []


def test_missing_link_is_reported(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", "See [docs](https://example.com/docs).")
    de = _write(tmp_path, "README_de.md", "Kein Link hier.")
    conflicts, notes = clp.check_parity([en, de])
    assert len(conflicts) == 1
    assert "example.com/docs" in conflicts[0]
    assert "README_de.md" in conflicts[0]


def test_lang_only_marker_scopes_link_to_named_languages(tmp_path: Path) -> None:
    en = _write(
        tmp_path,
        "README.md",
        "<!-- lang-only: zh -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    zh = _write(
        tmp_path,
        "README_zh.md",
        "<!-- lang-only: zh -->\n[Skills宝](https://skilery.com)\n<!-- /lang-only -->",
    )
    de = _write(tmp_path, "README_de.md", "Kein Skills-Link hier.")
    # de ist nicht in der Markierung genannt -> kein Konflikt
    conflicts, notes = clp.check_parity([en, zh, de])
    assert conflicts == []


def test_lang_only_marker_still_reports_missing_within_scope(tmp_path: Path) -> None:
    en = _write(
        tmp_path,
        "README.md",
        "<!-- lang-only: zh,ja -->\n[link](https://example.com/x)\n<!-- /lang-only -->",
    )
    zh = _write(tmp_path, "README_zh.md", "Fehlt hier.")
    ja = _write(
        tmp_path,
        "README_ja.md",
        "<!-- lang-only: zh,ja -->\n[link](https://example.com/x)\n<!-- /lang-only -->",
    )
    conflicts, notes = clp.check_parity([en, zh, ja])
    assert len(conflicts) == 1
    assert "lang-only: ja,zh" in conflicts[0]
    assert "README_zh.md" in conflicts[0]


def test_badge_urls_filtered_by_default(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", "![status](https://img.shields.io/badge/Public-green)")
    de = _write(tmp_path, "README_de.md", "Kein Badge.")
    conflicts, notes = clp.check_parity([en, de])
    assert conflicts == []


def test_badge_urls_reported_with_include_badges(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", "![status](https://img.shields.io/badge/Public-green)")
    de = _write(tmp_path, "README_de.md", "Kein Badge.")
    conflicts, notes = clp.check_parity([en, de], include_badges=True)
    assert len(conflicts) == 1


def test_html_links_are_extracted(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", '<a href="https://example.com/site">Site</a>')
    de = _write(tmp_path, "README_de.md", "Kein Link hier.")
    conflicts, notes = clp.check_parity([en, de])
    assert len(conflicts) == 1
    assert "example.com/site" in conflicts[0]


def test_html_img_src_is_extracted(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", '<img src="https://example.com/banner.png" alt="banner">')
    de = _write(tmp_path, "README_de.md", "Kein Bild hier.")
    conflicts, notes = clp.check_parity([en, de])
    assert len(conflicts) == 1
    assert "banner.png" in conflicts[0]


def test_mixed_markdown_and_html_links_match(tmp_path: Path) -> None:
    en = _write(tmp_path, "README.md", "[docs](https://example.com/docs)")
    de = _write(tmp_path, "README_de.md", '<a href="https://example.com/docs">Doku</a>')
    # dieselbe URL in Markdown- bzw. HTML-Form -> kein Konflikt
    conflicts, notes = clp.check_parity([en, de])
    assert conflicts == []


def test_non_utf8_file_raises_unicode_decode_error(tmp_path: Path) -> None:
    p = tmp_path / "README_broken.md"
    p.write_bytes(b"\xff\xfe garbage not utf-8 \x00\x01")
    try:
        clp.extract_links(p)
        assert False, "erwartete UnicodeDecodeError"
    except UnicodeDecodeError:
        pass


def test_main_exits_2_on_non_utf8_file(tmp_path: Path, capsys) -> None:
    good = _write(tmp_path, "README.md", "[docs](https://example.com/docs)")
    broken = tmp_path / "README_de.md"
    broken.write_bytes(b"\xff\xfe garbage \x00\x01")
    exit_code = clp.main(["prog", str(good), str(broken)])
    assert exit_code == 2
    err = capsys.readouterr().err
    assert "UTF-8" in err


def test_main_missing_args_exits_2(capsys) -> None:
    exit_code = clp.main(["prog", "onefile.md"])
    assert exit_code == 2


def test_main_missing_file_exits_2(tmp_path: Path, capsys) -> None:
    good = _write(tmp_path, "README.md", "text")
    exit_code = clp.main(["prog", str(good), str(tmp_path / "nope.md")])
    assert exit_code == 2
