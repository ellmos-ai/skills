"""Tests for tageszeitung config cascade, self-healing, RSS parsing, and templates."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path
from unittest import mock

SKILL_ROOT = Path(__file__).resolve().parent.parent


def _load_core():
    path = SKILL_ROOT / "tageszeitung_core.py"
    spec = importlib.util.spec_from_file_location("tageszeitung_core", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tageszeitung_core"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_zeitung_config_and_self_healing_repair(tmp_path):
    tc = _load_core()
    shutil.copy2(SKILL_ROOT / "zeitung-config.json", tmp_path / "zeitung-config.json")
    corrupt = tmp_path / "config.json"
    corrupt.write_text("{broken json", encoding="utf-8")

    loaded = tc.load_zeitung_config(skill_root=tmp_path, repair=True)
    assert loaded["warnings"]
    assert loaded["healed"]
    assert list(tmp_path.glob("config.json.corrupt.*.bak"))
    assert loaded["config"]["edition"]["max_per_category"] >= 1
    assert isinstance(json.loads(corrupt.read_text(encoding="utf-8")), dict)


def test_source_crud_store_and_template_rendering(tmp_path):
    tc = _load_core()
    store = tmp_path / "news.db"
    src_id = tc.add_source(store, "TechFeed", "rss", "https://example.invalid/feed.xml", category="Technik")
    sources = tc.list_sources(store)
    assert len(sources) == 1
    assert sources[0]["id"] == src_id

    rss_xml = (
        b"<rss><channel>"
        b"<item><title>Meldung &lt;script&gt;alert(1)&lt;/script&gt;</title>"
        b"<link>https://example.invalid/1</link>"
        b"<description><![CDATA[<p>Zusammenfassung</p>]]></description></item>"
        b"<item><title>Zweite Meldung</title>"
        b"<link>https://example.invalid/2</link>"
        b"<description>Text zwei</description></item>"
        b"</channel></rss>"
    )

    class _FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self, limit=None):
            return rss_xml[:limit] if limit else rss_xml

    with mock.patch.object(tc.urllib.request, "urlopen", return_value=_FakeResp()):
        # Ensure stdlib parser path works cleanly regardless of feedparser presence
        with mock.patch.object(tc, "_fetch_rss_feedparser", side_effect=ImportError):
            new_cnt, err = tc.fetch_source(store, sources[0])
    assert err is None
    assert new_cnt == 2

    items = tc.list_items(store, only_unread=True)
    assert len(items) == 2

    out_dir = tmp_path / "out"
    with mock.patch.object(tc, "_html_to_pdf", return_value=False):
        html_res = tc.render(store, target_date="2026-11-27", out_dir=str(out_dir), fmt="html")
    assert html_res["article_count"] == 2
    html_text = Path(html_res["html"]).read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html_text
    assert "@media print" in html_text
    assert "<script>alert(1)</script>" not in html_text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html_text

    md_res = tc.render(store, target_date="2026-11-27", out_dir=str(out_dir), fmt="md")
    md_text = Path(md_res["md"]).read_text(encoding="utf-8")
    assert "# Tageszeitung — 2026-11-27" in md_text
    assert "## Technik" in md_text

    assert tc.mark_read(store, items[0]["id"]) is True
    assert len(tc.list_items(store, only_unread=True)) == 1


def test_dry_run_render_cli(tmp_path):
    tc = _load_core()
    out_dir = tmp_path / "dry"
    rc = tc.main(["--store", str(tmp_path / "empty.db"), "render", "--date", "2026-11-27", "--out", str(out_dir), "--dry-run"])
    assert rc == 0
    assert (out_dir / "tageszeitung_2026-11-27.html").is_file()
