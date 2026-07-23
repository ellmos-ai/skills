#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
tageszeitung_core.py — Headless Tageszeitung aus RSS/Web-Quellen.

Portiert aus: BACH hub/news.py + hub/_services/newspaper/newspaper_generator.py
              (MIT, ellmos-ai/bach, privat) — userneutral, ohne Origin-DB-Pfad,
              ohne BaseHandler-Abhaengigkeit.
Store:        SQLite — assist/tageszeitung/store.db (eigener Store, kein Origin-DB)
Abhaengigkeit: Python-Stdlib + sqlite3. feedparser optional (sicherer Fallback:
              defusedxml wenn installiert, sonst Regex — KEIN ET.fromstring()
              auf Netz-Daten, da stdlib ET XXE-anfaellig ist).

Verwendung (CLI):
  python tageszeitung_core.py add-source "Name" rss <url> [--category Kat]
  python tageszeitung_core.py sources [--dry-run]
  python tageszeitung_core.py fetch [--dry-run]
  python tageszeitung_core.py items [--limit 50] [--category kat] [--dry-run]
  python tageszeitung_core.py read <item_id>
  python tageszeitung_core.py render [--date YYYY-MM-DD] [--out /pfad/] [--dry-run]
  python tageszeitung_core.py --store /tmp/t.db sources
"""

from __future__ import annotations

import html as _html
import json as _json
import os
import re
import sqlite3
import sys
import urllib.request
import urllib.error
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# xml.etree.ElementTree wird NICHT direkt fuer Netz-XML verwendet (XXE-Risiko).
# Stattdessen: defusedxml (optional) oder Regex-Fallback ohne Entity-Expansion.
# NIEMALS ET.fromstring() auf rohen Netz-Daten aufrufen.

# ---------------------------------------------------------------------------
# Pfade (userneutral, relativ zum Skill)
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEFAULT_STORE = _SKILL_DIR / "store.db"
_ENV_STORE = os.environ.get("TAGESZEITUNG_STORE")


def _store_path(cli_override: Optional[str] = None) -> Path:
    if cli_override:
        return Path(cli_override)
    if _ENV_STORE:
        return Path(_ENV_STORE)
    return _DEFAULT_STORE


def _prefs_file() -> Optional[Path]:
    p = _SKILL_DIR.parent / "prefs.json"
    return p if p.exists() else None


def _read_pref(key: str, default=None):
    pf = _prefs_file()
    if not pf:
        return default
    try:
        return _json.loads(pf.read_text(encoding="utf-8")).get(key, default)
    except Exception:  # noqa: BLE001
        return default


# ---------------------------------------------------------------------------
# Store (SQLite) — Schema aus BACH news.py portiert
# ---------------------------------------------------------------------------

_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
"""


def _open_store(store: Path) -> sqlite3.Connection:
    store.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(store))
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


# ---------------------------------------------------------------------------
# Quellen-Verwaltung
# ---------------------------------------------------------------------------

def add_source(store: Path, name: str, src_type: str, url: str,
               category: str = "Allgemein") -> str:
    """Fuegt eine Quelle hinzu; gibt die ID zurueck."""
    record_id = _short_id()
    conn = _open_store(store)
    conn.execute(
        """INSERT OR IGNORE INTO news_sources
           (id, name, type, url, category, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (record_id, name, src_type, url, category, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return record_id


def list_sources(store: Path) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    rows = conn.execute(
        "SELECT * FROM news_sources ORDER BY category, name"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# RSS-Fetch (feedparser bevorzugt, xml.etree-Fallback)
# ---------------------------------------------------------------------------

def _strip_html(text: str) -> str:
    """Entfernt HTML-Tags aus einem String."""
    clean = re.sub(r"<[^>]+>", " ", text or "")
    return _html.unescape(clean).strip()


def _fetch_rss_feedparser(url: str) -> list[dict]:
    """Holt RSS via feedparser (bevorzugt)."""
    import feedparser  # type: ignore
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        summary = _strip_html(
            getattr(entry, "summary", "") or getattr(entry, "description", "")
        )
        items.append({
            "title": getattr(entry, "title", "(kein Titel)"),
            "url": getattr(entry, "link", ""),
            "author": getattr(entry, "author", ""),
            "published_at": getattr(entry, "published", ""),
            "summary": summary[:500],
        })
    return items


def _fetch_rss_stdlib(url: str) -> list[dict]:
    """
    Holt RSS sicher ohne externe Abhaengigkeit.

    Strategie (XXE-sicher):
    1. defusedxml.ElementTree wenn installiert — verhindert XXE + billion-laughs.
    2. Regex-Fallback: extrahiert <item>-Bloecke als Text, parst Tags per Regex.
       Kein ET.fromstring() auf rohen Netz-Daten (stdlib ET ist XXE-anfaellig).
    """
    req = urllib.request.Request(
        url, headers={"User-Agent": "ellmos-tageszeitung/0.1 (+sovereign)"}
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        raw_bytes = resp.read(1_048_576)  # max 1 MB — Groessenbegrenzung

    # --- Versuch 1: defusedxml (optional, pip install defusedxml) ---
    try:
        from defusedxml import ElementTree as DET  # type: ignore
        root = DET.fromstring(raw_bytes)
        channel = root.find("channel") or root
        items = []
        for item in channel.findall("item"):
            def _t(tag: str) -> str:
                el = item.find(tag)
                return (el.text or "").strip() if el is not None else ""
            summary = _strip_html(_t("description"))
            items.append({
                "title": _t("title") or "(kein Titel)",
                "url": _t("link"),
                "author": _t("author"),
                "published_at": _t("pubDate"),
                "summary": summary[:500],
            })
        return items
    except ImportError:
        pass  # kein defusedxml — Regex-Fallback
    except Exception:  # noqa: BLE001
        pass  # Parse-Fehler im XML — Regex-Fallback

    # --- Versuch 2: Regex-Fallback (kein Entity-Parser, kein XXE-Risiko) ---
    raw_text = raw_bytes.decode("utf-8", errors="replace")

    def _tag(block: str, tag: str) -> str:
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", block,
                      re.DOTALL | re.IGNORECASE)
        if not m:
            return ""
        # CDATA auspackeln
        inner = m.group(1)
        inner = re.sub(r"<!\[CDATA\[(.*?)]]>", r"\1", inner, flags=re.DOTALL)
        return inner.strip()

    item_blocks = re.findall(r"<item[^>]*>(.*?)</item>", raw_text,
                             re.DOTALL | re.IGNORECASE)
    items = []
    for block in item_blocks:
        summary = _strip_html(_tag(block, "description"))
        items.append({
            "title": _tag(block, "title") or "(kein Titel)",
            "url": _tag(block, "link"),
            "author": _tag(block, "author"),
            "published_at": _tag(block, "pubDate"),
            "summary": summary[:500],
        })
    return items


def _fetch_web_title(url: str) -> list[dict]:
    """Holt den Seitentitel einer Web-URL (aus BACH news.py portiert)."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "ellmos-tageszeitung/0.1 (+sovereign)"}
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        content = resp.read(32768).decode("utf-8", errors="replace")
    m = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    title = _html.unescape(m.group(1).strip()) if m else "(kein Titel)"
    return [{"title": title, "url": url, "author": "", "published_at": "", "summary": ""}]


def fetch_source(store: Path, source: dict) -> tuple[int, Optional[str]]:
    """
    Holt Artikel fuer eine einzelne Quelle.
    Gibt (anzahl_neu, fehler_text) zurueck.
    """
    url = source["url"]
    src_type = source["type"]
    source_id = source["id"]
    category = source.get("category", "Allgemein")

    try:
        if src_type == "rss":
            try:
                import feedparser  # noqa: F401
                raw_items = _fetch_rss_feedparser(url)
            except ImportError:
                raw_items = _fetch_rss_stdlib(url)
        else:
            raw_items = _fetch_web_title(url)
    except Exception as exc:  # noqa: BLE001
        conn = _open_store(store)
        conn.execute(
            "UPDATE news_sources SET error_count = error_count + 1, last_error = ? WHERE id = ?",
            (str(exc), source_id),
        )
        conn.commit()
        conn.close()
        return 0, str(exc)

    conn = _open_store(store)
    fetched_at = datetime.now().isoformat()
    new_count = 0
    for item in raw_items:
        item_id = _short_id()
        try:
            conn.execute(
                """INSERT OR IGNORE INTO news_items
                   (id, source_id, title, summary, url, author, published_at, fetched_at, category)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item_id, source_id,
                    item.get("title", ""),
                    item.get("summary", ""),
                    item.get("url", ""),
                    item.get("author", ""),
                    item.get("published_at", ""),
                    fetched_at,
                    category,
                ),
            )
            if conn.execute(
                "SELECT changes()"
            ).fetchone()[0] > 0:
                new_count += 1
        except Exception:  # noqa: BLE001
            continue
    conn.execute(
        """UPDATE news_sources
           SET last_fetched = ?, fetch_count = fetch_count + 1
           WHERE id = ?""",
        (fetched_at, source_id),
    )
    conn.commit()
    conn.close()
    return new_count, None


# ---------------------------------------------------------------------------
# Artikel-Abfrage
# ---------------------------------------------------------------------------

def list_items(store: Path, limit: int = 50, category: Optional[str] = None,
               only_unread: bool = False) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    query = "SELECT * FROM news_items WHERE 1=1"
    params: list = []
    if category:
        query += " AND LOWER(category) = ?"
        params.append(category.lower())
    if only_unread:
        query += " AND is_read = 0"
    query += " ORDER BY fetched_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_read(store: Path, item_id: str) -> bool:
    if not store.exists():
        return False
    conn = _open_store(store)
    cursor = conn.execute(
        "UPDATE news_items SET is_read = 1 WHERE id = ?", (item_id,)
    )
    conn.commit()
    changed = cursor.rowcount > 0
    conn.close()
    return changed


# ---------------------------------------------------------------------------
# HTML/PDF-Render (aus BACH newspaper_generator.py portiert, userneutral)
# ---------------------------------------------------------------------------

def _render_html(items_by_category: dict[str, list[dict]], target_date: str,
                 title: str = "Tageszeitung") -> str:
    """Rendert Artikel als HTML-String."""
    lines = [
        "<!DOCTYPE html><html lang='de'><head>",
        "<meta charset='utf-8'>",
        f"<title>{_html.escape(title)} — {target_date}</title>",
        "<style>",
        "body{font-family:Georgia,serif;max-width:900px;margin:auto;padding:2em}",
        "h1{border-bottom:3px double #333;padding-bottom:.5em}",
        "h2{color:#555;margin-top:2em;border-bottom:1px solid #ccc}",
        "article{margin:1em 0;padding:.5em 0;border-bottom:1px solid #eee}",
        "article h3{margin:0 0 .3em}a{color:#0055aa}",
        ".meta{color:#888;font-size:.85em}",
        "</style></head><body>",
        f"<h1>{_html.escape(title)}</h1>",
        f"<p class='meta'>{target_date}</p>",
    ]
    for category, arts in items_by_category.items():
        lines.append(f"<h2>{_html.escape(category)}</h2>")
        for art in arts:
            url = art.get("url", "")
            t = _html.escape(art.get("title", "(kein Titel)"))
            summary = _html.escape(art.get("summary", ""))
            source = _html.escape(art.get("source_name", ""))
            lines.append("<article>")
            if url:
                lines.append(f"<h3><a href='{url}'>{t}</a></h3>")
            else:
                lines.append(f"<h3>{t}</h3>")
            if summary:
                lines.append(f"<p>{summary}</p>")
            if source:
                lines.append(f"<p class='meta'>{source}</p>")
            lines.append("</article>")
    lines.append("</body></html>")
    return "\n".join(lines)


def _html_to_pdf(html_path: Path, pdf_path: Path) -> bool:
    """Konvertiert HTML -> PDF via Edge Headless. Gibt True bei Erfolg zurueck."""
    import subprocess
    msedge = os.environ.get("MSEDGE_PATH", "msedge.exe")
    try:
        result = subprocess.run(
            [
                msedge,
                "--headless",
                "--disable-gpu",
                f"--print-to-pdf={pdf_path}",
                "--no-pdf-header-footer",
                str(html_path),
            ],
            timeout=30,
            capture_output=True,
        )
        return result.returncode == 0 and pdf_path.exists()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def render(store: Path, target_date: Optional[str] = None,
           out_dir: Optional[str] = None, dry_run: bool = False,
           title: str = "Tageszeitung") -> dict:
    """
    Rendert die Tageszeitung als HTML (+ PDF wenn Edge verfuegbar).
    Gibt {'html': pfad, 'pdf': pfad|None, 'article_count': n} zurueck.
    """
    if target_date is None:
        target_date = date.today().isoformat()
    max_per_cat = int(_read_pref("tageszeitung_max_per_category", 5))

    if dry_run:
        # Dummy-Artikel fuer Dry-Run
        items_by_category: dict[str, list[dict]] = {
            "Demo": [
                {"title": "Beispiel-Artikel 1", "url": "", "summary": "Demo-Inhalt",
                 "source_name": "dry-run"},
                {"title": "Beispiel-Artikel 2", "url": "", "summary": "Demo-Inhalt 2",
                 "source_name": "dry-run"},
            ]
        }
    else:
        # Quellen-Namen fuer Join nachladen
        source_names: dict[str, str] = {}
        if store.exists():
            conn = _open_store(store)
            for row in conn.execute("SELECT id, name FROM news_sources").fetchall():
                source_names[row["id"]] = row["name"]
            conn.close()

        raw_items = list_items(store, limit=500, only_unread=True)
        # Nach Kategorie gruppieren
        items_by_category = {}
        for item in raw_items:
            cat = item.get("category") or "Allgemein"
            if cat not in items_by_category:
                items_by_category[cat] = []
            if len(items_by_category[cat]) < max_per_cat:
                item["source_name"] = source_names.get(item.get("source_id", ""), "")
                items_by_category[cat].append(item)

    html_content = _render_html(items_by_category, target_date, title)

    output_dir = Path(out_dir) if out_dir else _SKILL_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / f"tageszeitung_{target_date}.html"
    html_path.write_text(html_content, encoding="utf-8")

    article_count = sum(len(v) for v in items_by_category.values())

    pdf_path = output_dir / f"tageszeitung_{target_date}.pdf"
    pdf_ok = _html_to_pdf(html_path, pdf_path) if not dry_run else False

    return {
        "html": str(html_path),
        "pdf": str(pdf_path) if pdf_ok else None,
        "article_count": article_count,
        "date": target_date,
        "dry_run": dry_run,
    }


# ---------------------------------------------------------------------------
# Dry-Run-Quelldaten
# ---------------------------------------------------------------------------

_DRY_SOURCES = [
    {"id": "src-1", "name": "Heise Online", "type": "rss",
     "url": "https://www.heise.de/rss/heise-atom.xml",
     "category": "Technik", "is_active": 1, "fetch_count": 0},
    {"id": "src-2", "name": "tagesschau.de", "type": "rss",
     "url": "https://www.tagesschau.de/xml/rss2/",
     "category": "Nachrichten", "is_active": 1, "fetch_count": 0},
]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolve_store_from_args(args: list[str]) -> tuple[Path, list[str]]:
    if "--store" in args:
        idx = args.index("--store")
        if idx + 1 < len(args):
            store = Path(args[idx + 1])
            remaining = args[:idx] + args[idx + 2:]
            return store, remaining
    return _store_path(), args


def main(argv: Optional[list] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 0

    store, argv = _resolve_store_from_args(argv)
    dry_run = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]

    if not argv:
        print(__doc__)
        return 0

    cmd = argv[0].lower()

    # --- add-source ---
    if cmd == "add-source":
        # add-source <name> <type> <url> [--category kat]
        args = argv[1:]
        if len(args) < 3:
            print("Verwendung: tageszeitung_core.py add-source <Name> <rss|web> <URL> [--category Kat]")
            return 1
        name, src_type, url = args[0], args[1], args[2]
        category = "Allgemein"
        if "--category" in args:
            idx = args.index("--category")
            if idx + 1 < len(args):
                category = args[idx + 1]
        src_id = add_source(store, name, src_type, url, category)
        print(f"[tageszeitung] Quelle hinzugefuegt: {name} [{src_id}] ({category})")
        return 0

    # --- sources ---
    if cmd == "sources":
        if dry_run:
            sources = _DRY_SOURCES
            print("[DRY-RUN] Beispiel-Quellen:")
        else:
            sources = list_sources(store)
        if not sources:
            print("[tageszeitung] Keine Quellen konfiguriert.")
            return 0
        print(f"=== Quellen ({len(sources)}) ===")
        for s in sources:
            status = "aktiv" if s.get("is_active", 1) else "inaktiv"
            print(f"  [{s['id']}] {s['name']} | {s['type']} | {s.get('category','?')} | {status}")
        return 0

    # --- fetch ---
    if cmd == "fetch":
        if dry_run:
            print("[DRY-RUN] Fetch uebersprungen.")
            return 0
        sources = [s for s in list_sources(store) if s.get("is_active", 1)]
        if not sources:
            print("[tageszeitung] Keine aktiven Quellen. Mit 'add-source' Quellen hinzufuegen.")
            return 0
        total_new = 0
        for s in sources:
            new_count, err = fetch_source(store, s)
            if err:
                print(f"  [FEHLER] {s['name']}: {err}")
            else:
                print(f"  {s['name']}: {new_count} neue Artikel")
                total_new += new_count
        print(f"[tageszeitung] Gesamt: {total_new} neue Artikel")
        return 0

    # --- items ---
    if cmd == "items":
        args = argv[1:]
        limit = 50
        category = None
        if "--limit" in args:
            idx = args.index("--limit")
            if idx + 1 < len(args):
                try:
                    limit = int(args[idx + 1])
                except ValueError:
                    pass
        if "--category" in args:
            idx = args.index("--category")
            if idx + 1 < len(args):
                category = args[idx + 1]
        items = list_items(store, limit, category, only_unread=True)
        if not items:
            print("[tageszeitung] Keine ungelesenen Artikel.")
            return 0
        print(f"=== Ungelesene Artikel ({len(items)}) ===")
        for it in items:
            cat = it.get("category", "—")
            print(f"  [{it['id']}] [{cat}] {it['title'][:70]}")
        return 0

    # --- read ---
    if cmd == "read":
        if len(argv) < 2:
            print("Verwendung: tageszeitung_core.py read <item_id>")
            return 1
        ok = mark_read(store, argv[1])
        if ok:
            print(f"[tageszeitung] Artikel {argv[1]} als gelesen markiert.")
        else:
            print(f"[tageszeitung] Artikel {argv[1]} nicht gefunden.")
        return 0 if ok else 1

    # --- render ---
    if cmd == "render":
        args = argv[1:]
        target_date = None
        out_dir = None
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                target_date = args[idx + 1]
        if "--out" in args:
            idx = args.index("--out")
            if idx + 1 < len(args):
                out_dir = args[idx + 1]
        result = render(store, target_date, out_dir, dry_run)
        print(f"[tageszeitung] {result['article_count']} Artikel | HTML: {result['html']}")
        if result["pdf"]:
            print(f"[tageszeitung] PDF:  {result['pdf']}")
        else:
            print("[tageszeitung] PDF: nicht erstellt (msedge.exe nicht gefunden oder Dry-Run)")
        return 0

    print(f"Unbekannter Befehl: {cmd!r}")
    print("Verfuegbar: add-source, sources, fetch, items, read, render")
    return 1


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
