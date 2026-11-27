#!/usr/bin/env python3
"""Self-healing configuration loader and template renderer for decision-draw."""

from __future__ import annotations

import copy
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SKILL_ROOT = Path(__file__).resolve().parent.parent
BASE_CONFIG_NAME = "draw-config.json"

DEFAULT_DRAW_CONFIG: dict[str, Any] = {
    "schema": "ocean.skill-config.v2",
    "skill": "decision-draw",
    "version": "1.6.0",
    "self_healing": {
        "enabled": True,
        "backup_suffix": ".corrupt.<ts>.bak",
        "atomic_writes": True,
    },
    "defaults": {
        "mode": "short",
        "preselect": "none",
    },
    "viewer": {
        "theme": "clam",
        "bg": "#eef2f7",
        "fg": "#18304a",
        "card_bg": "white",
        "comment_bg": "#f7f9fc",
        "font_family": "Segoe UI",
        "font_size": 11,
        "title_font_size": 17,
        "max_width": 960,
        "min_width": 640,
        "min_height": 500,
        "watch_interval_ms": 1200,
        "confirmation_limit": 12,
    },
    "form": {
        "question_option": {
            "id": "rueckfrage",
            "label": "Rückfrage / mehr Info nötig",
        },
        "limits": {
            "titel": 80,
            "kontext_kurz": 400,
            "kontext": 250,
            "frage": 200,
            "label": 100,
            "wirkung": 160,
            "grund": 160,
            "kosten_aufwand": 160,
            "risiko_rueckgaengig": 160,
            "frist": 160,
            "folge_bei_nein": 160,
            "beschriftung": 120,
            "sensitiv_grund": 100,
            "alt": 200,
            "seite": 60,
            "variante": 60,
            "zielordner": 120,
            "details_markdown": 4000,
        },
        "images": {
            "max_bytes": 409600,
            "total_max_bytes": 8388608,
            "serie_max": 12,
            "polaroid_min": 2,
            "polaroid_max": 12,
            "swipe_max": 60,
        },
    },
    "server": {
        "host": "127.0.0.1",
        "max_bytes": 33554432,
        "idle_seconds": 300,
        "max_lifetime_seconds": 28800,
        "max_files": 4,
    },
    "output": {
        "default_format": "md",
        "supported_formats": ["md", "html", "json"],
    },
    "templates": {
        "dir": "./templates",
        "short_md": "decision-draw-short.template.md",
        "detailed_md": "decision-draw-detailed.template.md",
        "markdown_form_html": "markdown_form_shell.template.html",
        "custom_dir": None,
    },
}


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = copy.deepcopy(dict(base))
    for key, val in override.items():
        if key in ("_hinweis", "_comment") and key in merged:
            continue
        if isinstance(merged.get(key), dict) and isinstance(val, dict):
            merged[key] = deep_merge(merged[key], val)
        else:
            merged[key] = copy.deepcopy(val)
    return merged


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(dict(payload), ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
        os.replace(tmp_name, str(path))
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def load_draw_config(
    *,
    skill_root: Path = SKILL_ROOT,
    repair: bool = False,
) -> dict[str, Any]:
    """Load draw-config.json -> config.json with self-healing fallback."""
    warnings: list[str] = []
    healed: list[dict[str, str]] = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    effective = copy.deepcopy(DEFAULT_DRAW_CONFIG)

    for idx, filename in enumerate((BASE_CONFIG_NAME, "config.json")):
        candidate = skill_root / filename
        if not candidate.is_file():
            continue
        try:
            raw = json.loads(candidate.read_text(encoding="utf-8-sig"))
            if not isinstance(raw, dict):
                raise ValueError("JSON root must be object")
            effective = deep_merge(effective, raw)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            warnings.append(f"{candidate.name}: corrupt config ({exc}); fell back to defaults")
            if repair:
                bak = candidate.with_name(f"{candidate.name}.corrupt.{ts}.bak")
                shutil.copy2(str(candidate), str(bak))
                atomic_write_json(candidate, DEFAULT_DRAW_CONFIG if idx == 0 else {})
                healed.append({"path": str(candidate), "backup_path": str(bak)})

    return {"config": effective, "warnings": warnings, "healed": healed}


def resolve_template_path(
    template_key: str,
    *,
    skill_root: Path = SKILL_ROOT,
    config: Mapping[str, Any] | None = None,
) -> Path:
    cfg = config if config is not None else load_draw_config(skill_root=skill_root)["config"]
    tpl_cfg = cfg.get("templates") if isinstance(cfg.get("templates"), dict) else {}
    filename = str(tpl_cfg.get(template_key) or template_key)
    search_dirs: list[Path] = []
    custom_dir = tpl_cfg.get("custom_dir")
    if isinstance(custom_dir, str) and custom_dir.strip():
        cpath = Path(custom_dir)
        search_dirs.append(cpath if cpath.is_absolute() else (skill_root / cpath))
    rel_dir = str(tpl_cfg.get("dir") or "./templates")
    dpath = Path(rel_dir)
    search_dirs.append(dpath if dpath.is_absolute() else (skill_root / dpath))
    search_dirs.append(SKILL_ROOT / "templates")
    for folder in search_dirs:
        candidate = folder / filename
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Template {filename!r} not found in {search_dirs}")


def render_markdown_template(
    template_key: str,
    context: Mapping[str, str],
    *,
    skill_root: Path = SKILL_ROOT,
    config: Mapping[str, Any] | None = None,
) -> str:
    tpl_text = resolve_template_path(template_key, skill_root=skill_root, config=config).read_text(
        encoding="utf-8"
    )
    rendered = tpl_text
    for key, val in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(val))
    return rendered
