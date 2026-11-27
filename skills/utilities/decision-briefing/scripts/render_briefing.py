#!/usr/bin/env python3
"""Stdlib renderer and self-healing config loader for decision-briefing."""

from __future__ import annotations

import argparse
import copy
import html
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SKILL_ROOT = Path(__file__).resolve().parent.parent
BASE_CONFIG_NAME = "briefing-config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "schema": "ocean.skill-config.v2",
    "skill": "decision-briefing",
    "version": "1.6.0",
    "self_healing": {
        "enabled": True,
        "backup_suffix": ".corrupt.<ts>.bak",
        "atomic_writes": True,
    },
    "briefing": {
        "batch_threshold": 5,
        "block_size": 4,
        "max_options": 4,
        "option_letters": ["A", "B", "C", "D"],
        "include_appendix_table": True,
        "include_session_provenance": False,
        "hide_technical_ids_in_body": True,
    },
    "output": {
        "default_format": "md",
        "supported_formats": ["md", "html", "txt", "json"],
        "output_dir": "./output",
    },
    "templates": {
        "dir": "./templates",
        "md": "briefing.template.md",
        "html": "briefing.template.html",
        "custom_dir": None,
    },
    "delivery": {
        "enabled": False,
        "dry_run": True,
        "mode": "draft",
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


def load_briefing_config(
    *,
    skill_root: Path = SKILL_ROOT,
    channel: str | None = None,
    chat: str | None = None,
    cli_overrides: Mapping[str, Any] | None = None,
    repair: bool = False,
) -> dict[str, Any]:
    """Load briefing-config.json -> config.json -> profiles/* with self-healing."""
    warnings: list[str] = []
    healed: list[dict[str, str]] = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    base_path = skill_root / BASE_CONFIG_NAME
    effective = copy.deepcopy(DEFAULT_CONFIG)
    if base_path.is_file():
        try:
            raw_base = json.loads(base_path.read_text(encoding="utf-8-sig"))
            if not isinstance(raw_base, dict):
                raise ValueError("JSON root must be object")
            effective = deep_merge(effective, raw_base)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            warnings.append(f"{base_path.name}: corrupt base config ({exc}); fell back to defaults")
            if repair:
                bak = base_path.with_name(f"{base_path.name}.corrupt.{ts}.bak")
                shutil.copy2(str(base_path), str(bak))
                atomic_write_json(base_path, DEFAULT_CONFIG)
                healed.append({"path": str(base_path), "backup_path": str(bak)})

    candidates: list[Path] = [skill_root / "config.json"]
    if channel:
        candidates.append(skill_root / "profiles" / f"{channel}.json")
        if chat:
            candidates.append(skill_root / "profiles" / f"{channel}.{chat}.json")

    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            raw = json.loads(candidate.read_text(encoding="utf-8-sig"))
            if not isinstance(raw, dict):
                raise ValueError("JSON root must be object")
            effective = deep_merge(effective, raw)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            warnings.append(f"{candidate.name}: corrupt override ({exc}); skipped")
            if repair:
                bak = candidate.with_name(f"{candidate.name}.corrupt.{ts}.bak")
                shutil.copy2(str(candidate), str(bak))
                atomic_write_json(candidate, {})
                healed.append({"path": str(candidate), "backup_path": str(bak)})

    if cli_overrides:
        effective = deep_merge(effective, cli_overrides)

    return {"config": effective, "warnings": warnings, "healed": healed}


def _resolve_template(fmt: str, cfg: Mapping[str, Any], skill_dir: Path) -> str:
    tpl_cfg = cfg.get("templates") if isinstance(cfg.get("templates"), dict) else {}
    filename = str(tpl_cfg.get(fmt) or f"briefing.template.{fmt}")
    search_dirs: list[Path] = []
    custom_dir = tpl_cfg.get("custom_dir")
    if isinstance(custom_dir, str) and custom_dir.strip():
        cpath = Path(custom_dir)
        search_dirs.append(cpath if cpath.is_absolute() else (skill_dir / cpath))
    rel_dir = str(tpl_cfg.get("dir") or "./templates")
    dpath = Path(rel_dir)
    search_dirs.append(dpath if dpath.is_absolute() else (skill_dir / dpath))
    search_dirs.append(SKILL_ROOT / "templates")
    for folder in search_dirs:
        candidate = folder / filename
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Template {filename!r} not found in {search_dirs}")


def _chunk_items(items: list[dict[str, Any]], cfg: Mapping[str, Any]) -> list[list[tuple[int, dict[str, Any]]]]:
    brief_cfg = cfg.get("briefing") if isinstance(cfg.get("briefing"), dict) else {}
    threshold = max(1, int(brief_cfg.get("batch_threshold") or 5))
    block_size = max(1, int(brief_cfg.get("block_size") or 4))
    numbered = list(enumerate(items, start=1))
    if len(numbered) <= threshold:
        return [numbered] if numbered else []
    return [numbered[i : i + block_size] for i in range(0, len(numbered), block_size)]


def render_briefing(
    data: Mapping[str, Any],
    *,
    fmt: str | None = None,
    config: Mapping[str, Any] | None = None,
    skill_dir: Path = SKILL_ROOT,
) -> str:
    """Render structured briefing data into md, html, txt, or json."""
    cfg = dict(config or DEFAULT_CONFIG)
    out_cfg = cfg.get("output") if isinstance(cfg.get("output"), dict) else {}
    brief_cfg = cfg.get("briefing") if isinstance(cfg.get("briefing"), dict) else {}

    target_fmt = (fmt or str(out_cfg.get("default_format") or "md")).strip().lower()
    supported = tuple(out_cfg.get("supported_formats") or ("md", "html", "txt", "json"))
    if target_fmt not in supported:
        raise ValueError(f"Unsupported format {target_fmt!r}; expected one of {', '.join(supported)}")

    title = str(data.get("title") or "Decision Briefing")
    subtitle = str(data.get("subtitle") or "Strukturierte Entscheidungsvorlage")
    generated_at = str(data.get("generated_at") or datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    footer = str(data.get("footer") or "decision-briefing — Optionen A/B/C/D oder 'Passt so'")
    raw_items = data.get("items") if isinstance(data.get("items"), list) else []
    items = [dict(x) for x in raw_items if isinstance(x, dict)]
    letters = list(brief_cfg.get("option_letters") or ("A", "B", "C", "D"))
    max_opts = max(1, int(brief_cfg.get("max_options") or 4))
    include_appendix = bool(brief_cfg.get("include_appendix_table", True))

    if target_fmt == "json":
        payload = {
            "title": title,
            "subtitle": subtitle,
            "generated_at": generated_at,
            "item_count": len(items),
            "items": items,
        }
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    blocks = _chunk_items(items, cfg)

    if target_fmt == "html":
        tpl = _resolve_template("html", cfg, skill_dir)
        esc = html.escape
        body_parts: list[str] = []
        if not blocks:
            body_parts.append("<p><em>Keine offenen Entscheidungen.</em></p>")
        for b_idx, block in enumerate(blocks, start=1):
            if len(blocks) > 1:
                body_parts.append(f'<h2 class="block-heading">Block {b_idx}</h2>')
            for idx, item in block:
                code = f"E{idx:02d}"
                item_title = esc(str(item.get("title") or f"Punkt {idx}"))
                sit = esc(str(item.get("situation") or "-"))
                act = esc(str(item.get("action") or "-"))
                fb = esc(str(item.get("fallback") or "-"))
                opts = (item.get("options") or [])[:max_opts]
                opts_html = []
                for o_idx, opt in enumerate(opts):
                    if isinstance(opt, dict):
                        key = esc(str(opt.get("key") or letters[o_idx]))
                        label = esc(str(opt.get("label") or ""))
                    else:
                        key = esc(letters[o_idx] if o_idx < len(letters) else str(o_idx + 1))
                        label = esc(str(opt))
                    opts_html.append(f"<li><strong>{key})</strong> {label}</li>")
                rec_key = esc(str(item.get("recommendation") or ""))
                rec_reason = esc(str(item.get("recommendation_reason") or ""))
                rec_html = (
                    f'<div class="rec"><strong>Empfehlung: {rec_key}</strong>'
                    + (f" — {rec_reason}" if rec_reason else "")
                    + "</div>"
                    if rec_key
                    else ""
                )
                body_parts.append(
                    f'<section class="card"><h3>[{code}] {item_title}</h3>'
                    f'<div class="triad"><p><strong>Lage:</strong> {sit}</p>'
                    f'<p><strong>Handlung:</strong> {act}</p>'
                    f'<p><strong>Rückfall:</strong> {fb}</p></div>'
                    f'<ol class="options" style="list-style:none">{"".join(opts_html)}</ol>'
                    f"{rec_html}</section>"
                )
        appendix_html = ""
        if include_appendix and items:
            rows = []
            for idx, item in enumerate(items, start=1):
                rows.append(
                    f"<tr><td>E{idx:02d}</td><td>{esc(str(item.get('title') or ''))}</td>"
                    f"<td>{esc(str(item.get('recommendation') or '-'))}</td>"
                    f"<td>{esc(str(item.get('ref_id') or '-'))}</td>"
                    f"<td>{esc(str(item.get('source') or '-'))}</td></tr>"
                )
            appendix_html = (
                "<h2>Technische Referenztabelle (nur für Buchung &amp; Audit)</h2>"
                "<table><thead><tr><th>Nr.</th><th>Klartext-Titel</th><th>Empfehlung</th>"
                "<th>Referenz</th><th>Quelle</th></tr></thead>"
                f"<tbody>{''.join(rows)}</tbody></table>"
            )
        return (
            tpl.replace("{{title}}", esc(title))
            .replace("{{subtitle}}", esc(subtitle))
            .replace("{{generated_at}}", esc(generated_at))
            .replace("{{item_count}}", str(len(items)))
            .replace("{{body_html}}", "\n".join(body_parts))
            .replace("{{appendix_html}}", appendix_html)
            .replace("{{footer}}", esc(footer))
        )

    body_lines: list[str] = []
    if not blocks:
        body_lines.append("_Keine offenen Entscheidungen._" if target_fmt == "md" else "Keine offenen Entscheidungen.")
    for b_idx, block in enumerate(blocks, start=1):
        if len(blocks) > 1:
            body_lines.append(f"## Block {b_idx}" if target_fmt == "md" else f"--- Block {b_idx} ---")
            body_lines.append("")
        for idx, item in block:
            code = f"E{idx:02d}"
            item_title = str(item.get("title") or f"Punkt {idx}")
            body_lines.append(f"### [{code}] {item_title}" if target_fmt == "md" else f"[{code}] {item_title}")
            body_lines.append(f"  Lage: {item.get('situation') or '-'}")
            body_lines.append(f"  Handlung: {item.get('action') or '-'}")
            body_lines.append(f"  Rückfall: {item.get('fallback') or '-'}")
            for o_idx, opt in enumerate((item.get("options") or [])[:max_opts]):
                if isinstance(opt, dict):
                    key = str(opt.get("key") or letters[o_idx])
                    label = str(opt.get("label") or "")
                else:
                    key = letters[o_idx] if o_idx < len(letters) else str(o_idx + 1)
                    label = str(opt)
                body_lines.append(f"  {key}) {label}")
            rec_key = item.get("recommendation")
            if rec_key:
                reason = item.get("recommendation_reason") or ""
                tail = f" — {reason}" if reason else ""
                body_lines.append(f"  -> Meine Empfehlung: {rec_key}{tail}")
            body_lines.append("")

    appendix_lines: list[str] = []
    if include_appendix and items:
        if target_fmt == "md":
            appendix_lines.extend([
                "### Technische Referenztabelle (nur für Buchung & Audit)",
                "| Nummer | Klartext-Titel | Empfehlung | Referenz | Quelle |",
                "|---|---|---|---|---|",
            ])
            for idx, item in enumerate(items, start=1):
                appendix_lines.append(
                    f"| E{idx:02d} | {str(item.get('title') or '').replace('|', '/')} | "
                    f"{item.get('recommendation') or '-'} | {item.get('ref_id') or '-'} | "
                    f"{item.get('source') or '-'} |"
                )
        else:
            appendix_lines.append("Technische Referenztabelle:")
            for idx, item in enumerate(items, start=1):
                appendix_lines.append(
                    f"  E{idx:02d}: {item.get('title') or ''} | Rec={item.get('recommendation') or '-'} "
                    f"| Ref={item.get('ref_id') or '-'} | Quelle={item.get('source') or '-'}"
                )

    if target_fmt == "txt":
        header = [title, f"{subtitle} ({len(items)} Entscheidungen | Stand: {generated_at})", "=" * 60, ""]
        return "\n".join(header + body_lines + appendix_lines + ["", footer]) + "\n"

    tpl = _resolve_template("md", cfg, skill_dir)
    return (
        tpl.replace("{{title}}", title)
        .replace("{{subtitle}}", subtitle)
        .replace("{{generated_at}}", generated_at)
        .replace("{{item_count}}", str(len(items)))
        .replace("{{body_md}}", "\n".join(body_lines).rstrip())
        .replace("{{appendix_md}}", "\n".join(appendix_lines).rstrip())
        .replace("{{footer}}", footer)
    )


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="render_briefing", description=__doc__)
    parser.add_argument("input_json", nargs="?", help="Path to briefing input JSON")
    parser.add_argument("--format", dest="fmt", default=None, choices=["md", "html", "txt", "json"])
    parser.add_argument("--out", default=None)
    parser.add_argument("--channel", default=None)
    parser.add_argument("--chat", default=None)
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    loaded = load_briefing_config(channel=args.channel, chat=args.chat, repair=args.repair)
    cfg = loaded["config"]

    if args.dry_run or not args.input_json:
        payload: dict[str, Any] = {
            "title": "Beispiel-Briefing (Dry-Run)",
            "subtitle": "Vorschau auf das strukturierte Briefing",
            "items": [
                {
                    "title": "Beispiel-Entscheidung",
                    "situation": "Eine Konfigurationsfrage steht offen.",
                    "action": "Ich lagere die Parameter sauber in JSON aus.",
                    "fallback": "Bei Fehlern greift der sichere Standardwert.",
                    "options": [
                        {"key": "A", "label": "In JSON auslagern"},
                        {"key": "B", "label": "Status quo behalten"},
                    ],
                    "recommendation": "A",
                    "recommendation_reason": "Vermeidet harte Vorgaben im Skript.",
                    "ref_id": "DEMO-01",
                    "source": "dry-run",
                }
            ],
        }
    else:
        payload = json.loads(Path(args.input_json).read_text(encoding="utf-8-sig"))

    rendered = render_briefing(payload, fmt=args.fmt, config=cfg)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
