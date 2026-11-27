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

import copy
import html as _html
import json as _json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

# xml.etree.ElementTree wird NICHT direkt fuer Netz-XML verwendet (XXE-Risiko).
# Stattdessen: defusedxml (optional) oder Regex-Fallback ohne Entity-Expansion.
# NIEMALS ET.fromstring() auf rohen Netz-Daten aufrufen.

# ---------------------------------------------------------------------------
# Pfade & Konfiguration (userneutral, relativ zum Skill, mit Selbstheilung)
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEFAULT_STORE = _SKILL_DIR / "store.db"
_ENV_STORE = os.environ.get("TAGESZEITUNG_STORE")
_BASE_CONFIG_NAME = "zeitung-config.json"

_DEFAULT_ZEITUNG_CONFIG: dict[str, Any] = {
    "schema": "ocean.skill-config.v2",
    "skill": "tageszeitung",
    "version": "0.2.0",
    "self_healing": {
        "enabled": True,
        "backup_suffix": ".corrupt.<ts>.bak",
        "atomic_writes": True,
    },
    "edition": {
        "default_title": "Tageszeitung",
        "default_category": "Allgemein",
        "max_per_category": 5,
        "summary_max_chars": 500,
        "fetch_limit": 500,
    },
    "sections": ["Nachrichten", "Technik", "Wissenschaft", "Wirtschaft", "Allgemein"],
    "fetch": {
        "timeout_seconds": 12,
        "max_feed_bytes": 1048576,
        "max_web_bytes": 32768,
        "user_agent": "ellmos-tageszeitung/0.2 (+sovereign)",
    },
    "layout": {
        "max_width_px": 900,
        "font_family": "Georgia,serif",
        "accent_color": "#0055aa",
    },
    "output": {
        "default_format": "html",
        "supported_formats": ["html", "md", "pdf"],
        "output_dir": "./output",
        "pdf_timeout_seconds": 30,
    },
    "templates": {
        "dir": "./templates",
        "html": "ausgabe.template.html",
        "md": "ausgabe.template.md",
        "custom_dir": None,
    },
    "delivery": {
        "enabled": False,
        "dry_run": True,
        "mode": "draft",
    },
}


def _deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = copy.deepcopy(dict(base))
    for key, val in override.items():
        if key in ("_hinweis", "_comment") and key in merged:
            continue
        if isinstance(merged.get(key), dict) and isinstance(val, dict):
            merged[key] = _deep_merge(merged[key], val)
        else:
            merged[key] = copy.deepcopy(val)
    return merged


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = _json.dumps(dict(payload), ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp_name, str(path))
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def load_zeitung_config(
    *,
    skill_root: Path = _SKILL_DIR,
    repair: bool = False,
) -> dict[str, Any]:
    """Laedt zeitung-config.json -> config.json (plus Legacy-prefs.json) mit Selbstheilung."""
    warnings: list[str] = []
    healed: list[dict[str, str]] = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    effective = copy.deepcopy(_DEFAULT_ZEITUNG_CONFIG)

    for idx, fname in enumerate((_BASE_CONFIG_NAME, "config.json")):
        candidate = skill_root / fname
        if not candidate.is_file():
            continue
        try:
            raw = _json.loads(candidate.read_text(encoding="utf-8-sig"))
            if not isinstance(raw, dict):
                raise ValueError("JSON root must be object")
            effective = _deep_merge(effective, raw)
        except (OSError, UnicodeDecodeError, ValueError, _json.JSONDecodeError) as exc:
            warnings.append(f"{candidate.name}: corrupt config ({exc}); fell back to defaults")
            if repair:
                bak = candidate.with_name(f"{candidate.name}.corrupt.{ts}.bak")
                shutil.copy2(str(candidate), str(bak))
                _atomic_write_json(candidate, _DEFAULT_ZEITUNG_CONFIG if idx == 0 else {})
                healed.append({"path": str(candidate), "backup_path": str(bak)})

    legacy_max = _read_pref("tageszeitung_max_per_category", None)
    if legacy_max is not None:
        try:
            effective["edition"]["max_per_category"] = int(legacy_max)
        except (TypeError, ValueError):
            warnings.append("prefs.json: invalid tageszeitung_max_per_category ignored")

    return {"config": effective, "warnings": warnings, "healed": healed}


def _resolve_template_text(fmt_key: str, cfg: Mapping[str, Any], skill_root: Path = _SKILL_DIR) -> str:
    tpl_cfg = cfg.get("templates") if isinstance(cfg.get("templates"), dict) else {}
    filename = str(tpl_cfg.get(fmt_key) or f"ausgabe.template.{fmt_key}")
    search_dirs: list[Path] = []
    custom_dir = tpl_cfg.get("custom_dir")
    if isinstance(custom_dir, str) and custom_dir.strip():
        cpath = Path(custom_dir)
        search_dirs.append(cpath if cpath.is_absolute() else (skill_root / cpath))
    rel_dir = str(tpl_cfg.get("dir") or "./templates")
    dpath = Path(rel_dir)
    search_dirs.append(dpath if dpath.is_absolute() else (skill_root / dpath))
    search_dirs.append(_SKILL_DIR / "templates")
    for folder in search_dirs:
        candidate = folder / filename
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Template {filename!r} not found in {search_dirs}")


def _store_path(cli_override: Optional[str] = None) -> Path:
    if cli_override:
        return Path(cli_override)
    env_override = os.environ.get("TAGESZEITUNG_STORE") or _ENV_STORE
    if env_override:
        return Path(env_override)
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


def _fetch_rss_feedparser(url: str, *, summary_max_chars: int = 500) -> list[dict]:
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
            "summary": summary[:summary_max_chars],
        })
    return items


def _fetch_rss_stdlib(
    url: str,
    *,
    cfg: Optional[Mapping[str, Any]] = None,
) -> list[dict]:
    """
    Holt RSS sicher ohne externe Abhaengigkeit.

    Strategie (XXE-sicher):
    1. defusedxml.ElementTree wenn installiert — verhindert XXE + billion-laughs.
    2. Regex-Fallback: extrahiert <item>-Bloecke als Text, parst Tags per Regex.
       Kein ET.fromstring() auf rohen Netz-Daten (stdlib ET ist XXE-anfaellig).
    """
    eff = cfg or load_zeitung_config()["config"]
    fetch_cfg = eff.get("fetch", {})
    edition_cfg = eff.get("edition", {})
    timeout_s = int(fetch_cfg.get("timeout_seconds", 12))
    max_bytes = int(fetch_cfg.get("max_feed_bytes", 1_048_576))
    summary_max = int(edition_cfg.get("summary_max_chars", 500))
    ua = str(fetch_cfg.get("user_agent", "ellmos-tageszeitung/0.2 (+sovereign)"))

    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        raw_bytes = resp.read(max_bytes)

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
                "summary": summary[:summary_max],
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
            "summary": summary[:summary_max],
        })
    return items


def _fetch_web_title(url: str, *, cfg: Optional[Mapping[str, Any]] = None) -> list[dict]:
    """Holt den Seitentitel einer Web-URL (aus BACH news.py portiert)."""
    eff = cfg or load_zeitung_config()["config"]
    fetch_cfg = eff.get("fetch", {})
    timeout_s = int(fetch_cfg.get("timeout_seconds", 12))
    max_bytes = int(fetch_cfg.get("max_web_bytes", 32768))
    ua = str(fetch_cfg.get("user_agent", "ellmos-tageszeitung/0.2 (+sovereign)"))
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        content = resp.read(max_bytes).decode("utf-8", errors="replace")
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
# HTML/MD/PDF-Render (Template-basiert aus templates/ + Edge-PDF optional)
# ---------------------------------------------------------------------------

def _render_html(
    items_by_category: dict[str, list[dict]],
    target_date: str,
    title: Optional[str] = None,
    *,
    cfg: Optional[Mapping[str, Any]] = None,
    skill_root: Path = _SKILL_DIR,
) -> str:
    """Rendert Artikel ueber templates/ausgabe.template.html als HTML-String."""
    eff = cfg or load_zeitung_config(skill_root=skill_root)["config"]
    layout = eff.get("layout", {})
    edition = eff.get("edition", {})
    eff_title = title or str(edition.get("default_title", "Tageszeitung"))
    tpl = _resolve_template_text("html", eff, skill_root)

    article_parts: list[str] = []
    for category, arts in items_by_category.items():
        article_parts.append(f"<h2>{_html.escape(category)}</h2>")
        for art in arts:
            url = str(art.get("url") or "")
            t = _html.escape(str(art.get("title") or "(kein Titel)"))
            summary = _html.escape(str(art.get("summary") or ""))
            source = _html.escape(str(art.get("source_name") or ""))
            article_parts.append("<article>")
            if url:
                article_parts.append(f"<h3><a href='{_html.escape(url, quote=True)}'>{t}</a></h3>")
            else:
                article_parts.append(f"<h3>{t}</h3>")
            if summary:
                article_parts.append(f"<p>{summary}</p>")
            if source:
                article_parts.append(f"<p class='meta'>{source}</p>")
            article_parts.append("</article>")

    return (
        tpl.replace("{{title}}", _html.escape(eff_title))
        .replace("{{date}}", _html.escape(target_date))
        .replace("{{font_family}}", _html.escape(str(layout.get("font_family", "Georgia,serif"))))
        .replace("{{max_width_px}}", str(int(layout.get("max_width_px", 900))))
        .replace("{{accent_color}}", _html.escape(str(layout.get("accent_color", "#0055aa"))))
        .replace("{{articles_html}}", "\n".join(article_parts))
    )


def _render_markdown(
    items_by_category: dict[str, list[dict]],
    target_date: str,
    title: Optional[str] = None,
    *,
    cfg: Optional[Mapping[str, Any]] = None,
    skill_root: Path = _SKILL_DIR,
) -> str:
    """Rendert Artikel ueber templates/ausgabe.template.md als Markdown-String."""
    eff = cfg or load_zeitung_config(skill_root=skill_root)["config"]
    edition = eff.get("edition", {})
    eff_title = title or str(edition.get("default_title", "Tageszeitung"))
    tpl = _resolve_template_text("md", eff, skill_root)

    md_parts: list[str] = []
    for category, arts in items_by_category.items():
        md_parts.append(f"## {category}\n")
        for art in arts:
            t = str(art.get("title") or "(kein Titel)")
            url = str(art.get("url") or "")
            summary = str(art.get("summary") or "")
            source = str(art.get("source_name") or "")
            heading = f"### [{t}]({url})" if url else f"### {t}"
            md_parts.append(heading)
            if summary:
                md_parts.append(summary)
            if source:
                md_parts.append(f"_{source}_")
            md_parts.append("")
    return (
        tpl.replace("{{title}}", eff_title)
        .replace("{{date}}", target_date)
        .replace("{{articles_md}}", "\n".join(md_parts).rstrip())
    )


def _html_to_pdf(html_path: Path, pdf_path: Path, *, timeout_seconds: int = 30) -> bool:
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
            timeout=timeout_seconds,
            capture_output=True,
        )
        return result.returncode == 0 and pdf_path.exists()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def render(
    store: Path,
    target_date: Optional[str] = None,
    out_dir: Optional[str] = None,
    dry_run: bool = False,
    title: Optional[str] = None,
    fmt: Optional[str] = None,
    *,
    skill_root: Path = _SKILL_DIR,
    repair: bool = False,
) -> dict:
    """
    Rendert die Tageszeitung als HTML (+ optional PDF via Edge) oder Markdown.
    Gibt {'html': pfad|None, 'md': pfad|None, 'pdf': pfad|None, 'article_count': n} zurueck.
    """
    cfg_res = load_zeitung_config(skill_root=skill_root, repair=repair)
    cfg = cfg_res["config"]
    edition = cfg.get("edition", {})
    out_cfg = cfg.get("output", {})

    if target_date is None:
        target_date = date.today().isoformat()
    eff_title = title or str(edition.get("default_title", "Tageszeitung"))
    default_cat = str(edition.get("default_category", "Allgemein"))
    max_per_cat = int(edition.get("max_per_category", 5))
    fetch_limit = int(edition.get("fetch_limit", 500))
    target_fmt = (fmt or str(out_cfg.get("default_format", "html"))).strip().lower()
    pdf_timeout = int(out_cfg.get("pdf_timeout_seconds", 30))

    if dry_run:
        items_by_category: dict[str, list[dict]] = {
            "Demo": [
                {"title": "Beispiel-Artikel 1", "url": "", "summary": "Demo-Inhalt",
                 "source_name": "dry-run"},
                {"title": "Beispiel-Artikel 2", "url": "", "summary": "Demo-Inhalt 2",
                 "source_name": "dry-run"},
            ]
        }
    else:
        source_names: dict[str, str] = {}
        if store.exists():
            conn = _open_store(store)
            for row in conn.execute("SELECT id, name FROM news_sources").fetchall():
                source_names[row["id"]] = row["name"]
            conn.close()

        raw_items = list_items(store, limit=fetch_limit, only_unread=True)
        items_by_category = {}
        for item in raw_items:
            cat = item.get("category") or default_cat
            if cat not in items_by_category:
                items_by_category[cat] = []
            if len(items_by_category[cat]) < max_per_cat:
                item["source_name"] = source_names.get(item.get("source_id", ""), "")
                items_by_category[cat].append(item)

    if out_dir:
        output_dir = Path(out_dir)
    else:
        rel_out = Path(str(out_cfg.get("output_dir", "./output")))
        output_dir = rel_out if rel_out.is_absolute() else (skill_root / rel_out)
    output_dir.mkdir(parents=True, exist_ok=True)

    article_count = sum(len(v) for v in items_by_category.values())
    html_path_str: Optional[str] = None
    md_path_str: Optional[str] = None
    pdf_path_str: Optional[str] = None

    if target_fmt == "md":
        md_content = _render_markdown(
            items_by_category, target_date, eff_title, cfg=cfg, skill_root=skill_root
        )
        md_path = output_dir / f"tageszeitung_{target_date}.md"
        md_path.write_text(md_content, encoding="utf-8")
        md_path_str = str(md_path)
    else:
        html_content = _render_html(
            items_by_category, target_date, eff_title, cfg=cfg, skill_root=skill_root
        )
        html_path = output_dir / f"tageszeitung_{target_date}.html"
        html_path.write_text(html_content, encoding="utf-8")
        html_path_str = str(html_path)

        pdf_path = output_dir / f"tageszeitung_{target_date}.pdf"
        if not dry_run and _html_to_pdf(html_path, pdf_path, timeout_seconds=pdf_timeout):
            pdf_path_str = str(pdf_path)

    return {
        "html": html_path_str,
        "md": md_path_str,
        "pdf": pdf_path_str,
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
        fmt = None
        repair = "--repair" in args
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                target_date = args[idx + 1]
        if "--out" in args:
            idx = args.index("--out")
            if idx + 1 < len(args):
                out_dir = args[idx + 1]
        if "--format" in args:
            idx = args.index("--format")
            if idx + 1 < len(args):
                fmt = args[idx + 1]
        result = render(store, target_date, out_dir, dry_run, fmt=fmt, repair=repair)
        if result.get("md"):
            print(f"[tageszeitung] {result['article_count']} Artikel | MD: {result['md']}")
        else:
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
