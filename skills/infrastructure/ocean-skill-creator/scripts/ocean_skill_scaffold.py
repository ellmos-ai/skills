#!/usr/bin/env python3
"""Ocean Skill Creator (v0.4.0) — Stdlib Scaffolding, Self-Healing Config & Skill Auditor.

Provides:
- 5-stage configuration cascade loader with self-healing backup & atomic writes:
  ``default-config.json -> config.json -> <channel>.json -> <channel>.<chat>.json -> CLI``
- Standard multi-format report rendering (``html``, ``pdf`` via pure-stdlib ``%PDF-1.4``,
  ``md``, ``txt``, ``json``) backed by replaceable ``templates/``.
- CLI subcommands:
  - ``scaffold <name> --category <cat> --out <dir> [--with-reports] [--with-profiles] [--json]``
  - ``validate-config --default <path> [--config <path>] [--profile <path> ...] [--repair] [--json]``
  - ``audit-skill <skill_dir> [--json]``
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SKILL_CREATOR_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_CREATOR_ROOT / "templates"
OUTPUT_TEMPLATES_DIR = TEMPLATES_DIR / "output"

SKILL_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRIGGER_RE = re.compile(
    r"\b(use (when|for|this|whenever|it|to)|when the user|when you|trigger|invoke|"
    r"verwenden|verwende|nutzen|nutze|einsetzen|aktiviert sich|immer wenn|wenn der nutzer)\b"
    r"|(?:^|\s)/[a-z][\w-]+",
    re.IGNORECASE,
)
REPORT_SIGNAL_RE = re.compile(
    r"\b(report|bericht|protokoll|export|digest|zusammenfassung|kalenderblatt|"
    r"summary|overview|dossier|pdf|html)\b",
    re.IGNORECASE,
)
HARDCODED_PATH_RE = re.compile(
    r"""(?ix)
    (?:[A-Z]:[\\/]{1,2}(?:Users|Program\s+Files|Temp|tmp)[\\/][^\s"'`]+)
    | (?:(?<=[\s("'=`])/(?:Users|home|opt|var|srv)/[A-Za-z0-9._-]+/[^\s"'`)]+)
    """
)
INLINE_HTML_RE = re.compile(r"<!DOCTYPE\s+html|<html\b|<style\b|@media\s+print", re.IGNORECASE)
HARDCODED_FORMAT_RE = re.compile(
    r"""(?ix)
    \b(?:default_format|output_format|target_format)\s*=\s*["'](?:html|pdf|md|txt|csv|xlsx)["']
    """
)
MAGIC_THRESHOLD_RE = re.compile(
    r"\b(?:MAX_[A-Z0-9_]+|DEFAULT_TIMEOUT|THRESHOLD_[A-Z0-9_]+|LIMIT_[A-Z0-9_]+)\s*=\s*\d+"
)

REQUIRED_FRONTMATTER_KEYS = (
    "name",
    "version",
    "type",
    "author",
    "created",
    "updated",
    "description",
    "standalone",
    "visibility",
)
SUPPORTED_REPORT_FORMATS = ("html", "pdf", "md", "txt", "json")


# ---------------------------------------------------------------------------
# Atomic JSON & Self-Healing Configuration Cascade
# ---------------------------------------------------------------------------

def utc_compact_timestamp(now: datetime | None = None) -> str:
    dt = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def atomic_write_json(path: str | Path, data: Mapping[str, Any]) -> Path:
    """Atomically write UTF-8 JSON via same-directory temp file + os.replace."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(dict(data), ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
            handle.flush()
            try:
                os.fsync(handle.fileno())
            except OSError:
                pass
        os.replace(str(tmp_path), str(target))
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise
    return target


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively merge nested dictionaries without mutating inputs."""
    merged: dict[str, Any] = copy.deepcopy(dict(base))
    for key, value in override.items():
        if key in ("_hinweis", "_comment") and key in merged:
            continue
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = deep_merge(existing, value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def additive_migrate(
    default_cfg: Mapping[str, Any],
    user_cfg: Mapping[str, Any],
    *,
    _prefix: str = "",
) -> tuple[dict[str, Any], list[str]]:
    """Backfill newly added keys from default_cfg into user_cfg without overwriting user values."""
    migrated: dict[str, Any] = copy.deepcopy(dict(user_cfg))
    added_paths: list[str] = []
    for key, default_val in default_cfg.items():
        if str(key).startswith("_"):
            continue
        dotted = f"{_prefix}.{key}" if _prefix else str(key)
        if key not in migrated:
            migrated[key] = copy.deepcopy(default_val)
            added_paths.append(dotted)
        elif isinstance(default_val, dict) and isinstance(migrated[key], dict):
            sub_migrated, sub_added = additive_migrate(
                default_val, migrated[key], _prefix=dotted
            )
            migrated[key] = sub_migrated
            added_paths.extend(sub_added)
    return migrated, added_paths


def _parse_cli_value(raw: str) -> Any:
    stripped = raw.strip()
    if stripped.lower() in {"true", "false", "null"}:
        return json.loads(stripped.lower())
    if stripped and stripped[0] in ('"', "[", "{", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass
    return raw


def dotted_pairs_to_dict(pairs: Sequence[str]) -> dict[str, Any]:
    """Convert ``['output.default_format=pdf', 'delivery.dry_run=true']`` to nested dict."""
    root: dict[str, Any] = {}
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"CLI override must have form key=value, got {item!r}")
        key_raw, val_raw = item.split("=", 1)
        parts = [seg.strip() for seg in key_raw.split(".") if seg.strip()]
        if not parts:
            raise ValueError(f"Empty key in CLI override {item!r}")
        cursor = root
        for part in parts[:-1]:
            nxt = cursor.get(part)
            if not isinstance(nxt, dict):
                nxt = {}
                cursor[part] = nxt
            cursor = nxt
        cursor[parts[-1]] = _parse_cli_value(val_raw)
    return root


def resolve_profile_chain(
    skill_dir: str | Path,
    *,
    config_path: str | Path | None = None,
    channel: str | None = None,
    chat: str | None = None,
    extra_profiles: Sequence[str | Path] = (),
) -> list[Path]:
    """Build the standard override path list above ``default-config.json``."""
    root = Path(skill_dir)
    chain: list[Path] = [Path(config_path) if config_path is not None else (root / "config.json")]
    profiles_dir = root / "profiles"
    clean_channel = (channel or "").strip()
    clean_chat = (chat or "").strip()
    if clean_channel:
        chain.append(profiles_dir / f"{clean_channel}.json")
        if clean_chat:
            chain.append(profiles_dir / f"{clean_channel}.{clean_chat}.json")
    for extra in extra_profiles:
        chain.append(Path(extra))
    return chain


def _backup_corrupt_file(path: Path, ts: str) -> Path:
    backup = path.with_name(f"{path.name}.corrupt.{ts}.bak")
    counter = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.corrupt.{ts}.{counter}.bak")
        counter += 1
    shutil.copy2(str(path), str(backup))
    return backup


def _sanitize_override_against_default(
    default_cfg: Mapping[str, Any],
    override_cfg: Mapping[str, Any],
    *,
    layer_label: str,
    warnings: list[str],
) -> tuple[dict[str, Any], bool]:
    """Ensure dict sections in default_cfg are not replaced by non-dict scalars."""
    cleaned: dict[str, Any] = {}
    had_type_error = False
    for key, val in override_cfg.items():
        default_val = default_cfg.get(key)
        if isinstance(default_val, dict) and not isinstance(val, dict):
            warnings.append(
                f"{layer_label}: key {key!r} expected JSON object, got {type(val).__name__}; kept default section"
            )
            had_type_error = True
            continue
        cleaned[key] = copy.deepcopy(val)
    return cleaned, had_type_error


def load_effective_config(
    default_path: str | Path,
    override_paths: Sequence[str | Path] = (),
    *,
    cli_overrides: Mapping[str, Any] | None = None,
    repair: bool = False,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Load, validate, deep-merge, and optionally self-heal a skill config cascade.

    Precedence:
    ``default-config.json -> config.json -> <channel>.json -> <channel>.<chat>.json -> cli_overrides``
    """
    def_path = Path(default_path)
    if not def_path.is_file():
        raise ValueError(f"default-config.json not found: {def_path}")
    try:
        default_raw = json.loads(def_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"default-config.json is invalid JSON ({def_path}): {exc}") from exc
    if not isinstance(default_raw, dict):
        raise ValueError(f"default-config.json root must be a JSON object: {def_path}")

    ts = timestamp or utc_compact_timestamp()
    effective: dict[str, Any] = copy.deepcopy(default_raw)
    layers_applied: list[str] = [str(def_path)]
    layers_skipped: list[str] = []
    warnings: list[str] = []
    healed: list[dict[str, str]] = []
    migrated_keys: list[str] = []

    for index, raw_override_path in enumerate(override_paths):
        ov_path = Path(raw_override_path)
        is_primary_config = index == 0 and ov_path.name == "config.json"
        if not ov_path.exists():
            layers_skipped.append(str(ov_path))
            continue
        if ov_path.is_dir():
            warnings.append(f"{ov_path}: expected JSON file, found directory; skipped")
            layers_skipped.append(str(ov_path))
            continue

        try:
            parsed = json.loads(ov_path.read_text(encoding="utf-8-sig"))
            if not isinstance(parsed, dict):
                raise ValueError(f"JSON root must be object, got {type(parsed).__name__}")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            warnings.append(f"{ov_path}: corrupt override ({exc}); fell back to default-config.json")
            if repair:
                backup_path = _backup_corrupt_file(ov_path, ts)
                replacement: dict[str, Any] = copy.deepcopy(default_raw) if is_primary_config else {}
                atomic_write_json(ov_path, replacement)
                healed.append({
                    "path": str(ov_path),
                    "backup_path": str(backup_path),
                    "reason": str(exc),
                    "action": "restored_from_default" if is_primary_config else "reset_empty_profile",
                })
                layers_applied.append(str(ov_path))
            else:
                layers_skipped.append(str(ov_path))
            continue

        sanitized, had_section_mismatch = _sanitize_override_against_default(
            default_raw,
            parsed,
            layer_label=str(ov_path),
            warnings=warnings,
        )
        if repair and had_section_mismatch:
            backup_path = _backup_corrupt_file(ov_path, ts)
            healed_payload = (
                additive_migrate(default_raw, sanitized)[0] if is_primary_config else sanitized
            )
            atomic_write_json(ov_path, healed_payload)
            healed.append({
                "path": str(ov_path),
                "backup_path": str(backup_path),
                "reason": "invalid section type sanitized",
                "action": "sanitized_and_saved",
            })
            sanitized = healed_payload
        elif repair and is_primary_config:
            migrated_payload, added = additive_migrate(default_raw, sanitized)
            if added:
                atomic_write_json(ov_path, migrated_payload)
                migrated_keys.extend(added)
                sanitized = migrated_payload

        effective = deep_merge(effective, sanitized)
        layers_applied.append(str(ov_path))

    if cli_overrides:
        cleaned_cli, _ = _sanitize_override_against_default(
            default_raw,
            cli_overrides,
            layer_label="cli_overrides",
            warnings=warnings,
        )
        effective = deep_merge(effective, cleaned_cli)
        layers_applied.append("cli_overrides")

    return {
        "ok": len(warnings) == 0 or bool(repair and len(healed) >= len(warnings)),
        "config": effective,
        "default_path": str(def_path),
        "layers_applied": layers_applied,
        "layers_skipped": layers_skipped,
        "warnings": warnings,
        "healed": healed,
        "migrated_keys": migrated_keys,
    }


# ---------------------------------------------------------------------------
# Pure-Stdlib Multi-Format Report & %PDF-1.4 Fallback Renderer
# ---------------------------------------------------------------------------

def _pdf_escape_ascii(text: str) -> str:
    translit = (
        text.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("Ä", "Ae")
        .replace("Ö", "Oe")
        .replace("Ü", "Ue")
        .replace("ß", "ss")
        .replace("—", "-")
        .replace("–", "-")
        .replace("·", "|")
    )
    safe = translit.encode("latin-1", errors="replace").decode("latin-1")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def render_minimal_pdf(title: str, lines: Sequence[str]) -> bytes:
    """Generate a deterministic, valid %PDF-1.4 document using only the Python stdlib."""
    all_lines = [title, "=" * min(max(len(title), 12), 72), ""] + list(lines)
    lines_per_page = 46
    chunks = [
        all_lines[idx : idx + lines_per_page]
        for idx in range(0, max(len(all_lines), 1), lines_per_page)
    ]

    objects: list[bytes] = []

    def add_obj(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    pages_placeholder_id = add_obj(b"")
    page_ids: list[int] = []

    for chunk in chunks:
        ops = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]
        for row_idx, raw_line in enumerate(chunk):
            escaped = _pdf_escape_ascii(str(raw_line)[:105])
            if row_idx == 0:
                ops.append(f"({escaped}) Tj")
            else:
                ops.append(f"T* ({escaped}) Tj")
        ops.append("ET")
        stream_bytes = "\n".join(ops).encode("ascii")
        content_id = add_obj(
            f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
            + stream_bytes
            + b"\nendstream"
        )
        page_id = add_obj(
            f"<< /Type /Page /Parent {pages_placeholder_id} 0 R "
            f"/MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>".encode("ascii")
        )
        page_ids.append(page_id)

    kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[pages_placeholder_id - 1] = (
        f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>".encode("ascii")
    )
    catalog_id = add_obj(f"<< /Type /Catalog /Pages {pages_placeholder_id} 0 R >>".encode("ascii"))

    buf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: list[int] = [0]
    for obj_num, body in enumerate(objects, start=1):
        offsets.append(len(buf))
        buf.extend(f"{obj_num} 0 obj\n".encode("ascii"))
        buf.extend(body)
        buf.extend(b"\nendobj\n")

    xref_pos = len(buf)
    buf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    buf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        buf.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    buf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    return bytes(buf)


def _resolve_template_text(
    fmt_key: str,
    config: Mapping[str, Any] | None,
    skill_dir: Path | None,
) -> str:
    templates_cfg = (config or {}).get("templates") if isinstance(config, dict) else None
    templates_cfg = templates_cfg if isinstance(templates_cfg, dict) else {}
    filename_map = {
        "html": str(templates_cfg.get("html") or "report.template.html"),
        "md": str(templates_cfg.get("md") or "report.template.md"),
        "txt": str(templates_cfg.get("txt") or "report.template.txt"),
    }
    filename = filename_map[fmt_key]
    search_dirs: list[Path] = []
    custom_dir = templates_cfg.get("custom_dir")
    if isinstance(custom_dir, str) and custom_dir.strip():
        cpath = Path(custom_dir)
        search_dirs.append(cpath if cpath.is_absolute() or skill_dir is None else (skill_dir / cpath))
    if skill_dir is not None:
        rel_dir = str(templates_cfg.get("dir") or "./templates")
        dpath = Path(rel_dir)
        search_dirs.append(dpath if dpath.is_absolute() else (skill_dir / dpath))
    search_dirs.append(OUTPUT_TEMPLATES_DIR)

    for folder in search_dirs:
        candidate = folder / filename
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Report template {filename!r} not found in {search_dirs}")


def render_report(
    report_data: Mapping[str, Any],
    *,
    fmt: str = "md",
    config: Mapping[str, Any] | None = None,
    skill_dir: str | Path | None = None,
) -> bytes | str:
    """Render structured report data to html, pdf, md, txt, or json."""
    target_fmt = fmt.strip().lower()
    if target_fmt not in SUPPORTED_REPORT_FORMATS:
        raise ValueError(
            f"Unsupported format {fmt!r}; expected one of {', '.join(SUPPORTED_REPORT_FORMATS)}"
        )
    sdir = Path(skill_dir) if skill_dir is not None else None
    title = str(report_data.get("title") or "Skill Report")
    subtitle = str(report_data.get("subtitle") or "Ocean Standard Report")
    generated_at = str(
        report_data.get("generated_at") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    summary = str(report_data.get("summary") or "-")
    items = report_data.get("items") if isinstance(report_data.get("items"), list) else []
    footer = str(report_data.get("footer") or "Generated with Ocean Skill Standard (dry-run safe)")

    if target_fmt == "json":
        return json.dumps(dict(report_data), ensure_ascii=False, indent=2) + "\n"

    if target_fmt == "pdf":
        lines = [
            f"{subtitle} | {generated_at}",
            "",
            f"Summary: {summary}",
            "",
            "Items:",
        ]
        for idx, item in enumerate(items, start=1):
            lines.append(f"  {idx}. {item}")
        lines.extend(["", footer])
        return render_minimal_pdf(title, lines)

    if target_fmt == "html":
        tpl = _resolve_template_text("html", config, sdir)
        items_html = (
            "<ul>\n" + "\n".join(f"  <li>{html.escape(str(i))}</li>" for i in items) + "\n</ul>"
            if items
            else "<p><em>Keine Einträge.</em></p>"
        )
        return (
            tpl.replace("{{title}}", html.escape(title))
            .replace("{{subtitle}}", html.escape(subtitle))
            .replace("{{generated_at}}", html.escape(generated_at))
            .replace("{{summary}}", html.escape(summary))
            .replace("{{body_html}}", items_html)
            .replace("{{footer}}", html.escape(footer))
        )

    if target_fmt == "md":
        tpl = _resolve_template_text("md", config, sdir)
        body_md = "\n".join(f"- {i}" for i in items) if items else "_Keine Einträge._"
        return (
            tpl.replace("{{title}}", title)
            .replace("{{subtitle}}", subtitle)
            .replace("{{generated_at}}", generated_at)
            .replace("{{summary}}", summary)
            .replace("{{body_md}}", body_md)
            .replace("{{footer}}", footer)
        )

    tpl = _resolve_template_text("txt", config, sdir)
    body_txt = "\n".join(f"  * {i}" for i in items) if items else "  (keine Eintraege)"
    return (
        tpl.replace("{{title}}", title)
        .replace("{{subtitle}}", subtitle)
        .replace("{{generated_at}}", generated_at)
        .replace("{{summary}}", summary)
        .replace("{{body_txt}}", body_txt)
        .replace("{{footer}}", footer)
    )


# ---------------------------------------------------------------------------
# Skill Scaffolding (scaffold subcommand)
# ---------------------------------------------------------------------------

def _build_scaffold_skill_md_de(
    name: str,
    category: str,
    today_iso: str,
    *,
    with_reports: bool,
) -> str:
    snake = name.replace("-", "_")
    desc = (
        f"Verwenden, wenn Aufgaben rund um {name} ausgeführt oder geprüft werden sollen "
        f"(z. B. '{name} starten', '{name} ausführen', /{name}). Nutzt ausgelagerte "
        f"Einstellungen über default-config.json samt Selbstheilung"
        + (
            " und erzeugt Berichte über austauschbare Vorlagen (html/pdf/md/txt/json)."
            if with_reports
            else "."
        )
        + " NICHT verwenden für allgemeine Skill-Suche (dafür skill-finder)."
    )
    report_section = ""
    if with_reports:
        report_section = f"""
## Berichte, Ausgabeformate & Vorlagen

Die Darstellung ist strikt von der Fachlogik getrennt (`templates/report.template.{{html,md,txt}}`):

- Unterstützte Ausgabeformate: `html`, `pdf` (inkl. reinem Stdlib-`%PDF-1.4`-Fallback), `md`, `txt`, `json`.
- Eigene Vorlagen können ohne Codeänderung über `templates.custom_dir` in `config.json` oder einem Kanalprofil hinterlegt werden.
- Zustellungswege (`delivery`) stehen standardmäßig sicher auf **Entwurf / Dry-Run** (`enabled: false`, `dry_run: true`, `mode: "draft"`).

```bash
python scripts/{snake}_core.py --format pdf --out output/report.pdf
```
"""
    return f"""---
name: {name}
version: 0.1.0
type: skill
author: Ocean Contributors
created: {today_iso}
updated: {today_iso}
description: {json.dumps(desc, ensure_ascii=False)}
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: {category}
tags: [{name}, {category}, ocean-standard, config-cascade]
language: de
status: active
visibility: private-only

dependencies:
  tools: []
  services: []
  protocols: []
  python: []
  skills: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# {name}

## Wann aktivieren

- „{name} starten“, „{name} ausführen“, `/{name}`
- Wenn strukturierte Läufe in der Kategorie `{category}` mit nachvollziehbarer Konfiguration benötigt werden.

## Konfiguration & Selbstheilung

Dieser Skill vermeidet feste Parameter im Code und lädt seine Einstellungen über die 5-stufige Ocean-Kaskade:

`default-config.json` -> `config.json` -> `profiles/<kanal>.json` -> `profiles/<kanal>.<chat>.json` -> CLI-Flags (`--set schluessel=wert`).

Beschädigte lokale Override-Dateien fallen automatisch auf `default-config.json` zurück und werden mit `--repair` verlustfrei als `.corrupt.<ts>.bak` gesichert.
{report_section}
## Anbieter & Alternativen

- **Eigenständiger Betrieb:** Läuft ohne externe Pflichtabhängigkeiten mit der Python-Standardbibliothek.
- **Ökosystem-Andockung:** Optionale externe Werkzeuge werden in `connections.json` aufgelöst (`grounding-seed`-kompatibel), niemals eigenmächtig installiert.

## Selbstaktualisierung

- Prüfe regelmäßig `letzter_update_check` in `default-config.json` / `config.json` sowie Nachbarskills über `skill-finder`.
- Halte neue Erkenntnisse datiert in `connections.json` (`gelernt`) und reale Nutzerfälle in `user-usecases.json` fest.

## Changelog

### 0.1.0 ({today_iso})
- Erstfassung erzeugt über `ocean-skill-creator` (`v0.4.0`) mit `default-config.json`, Selbstheilungs-Loader und Testgerüst.
"""


def _build_scaffold_skill_md_en(
    name: str,
    category: str,
    today_iso: str,
    *,
    with_reports: bool,
) -> str:
    snake = name.replace("-", "_")
    desc = (
        f"Use when running or inspecting {name} workflows (e.g. 'run {name}', "
        f"'execute {name}', /{name}). Loads externalized settings via default-config.json "
        f"with self-healing fallback"
        + (
            " and renders reports through replaceable templates (html/pdf/md/txt/json)."
            if with_reports
            else "."
        )
        + " Do NOT use for general skill routing (use skill-finder)."
    )
    report_section = ""
    if with_reports:
        report_section = f"""
## Reports, output formats & templates

Presentation is strictly separated from domain logic (`templates/report.template.{{html,md,txt}}`):

- Supported output formats: `html`, `pdf` (including a pure-stdlib `%PDF-1.4` fallback), `md`, `txt`, `json`.
- Custom templates can be configured via `templates.custom_dir` in `config.json` or channel profiles without code edits.
- Delivery settings (`delivery`) default safely to **draft / dry-run** (`enabled: false`, `dry_run: true`, `mode: "draft"`).

```bash
python scripts/{snake}_core.py --format pdf --out output/report.pdf
```
"""
    return f"""---
name: {name}
version: 0.1.0
type: skill
author: Ocean Contributors
created: {today_iso}
updated: {today_iso}
description: {json.dumps(desc, ensure_ascii=False)}
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: {category}
tags: [{name}, {category}, ocean-standard, config-cascade]
language: en
status: active
visibility: private-only

dependencies:
  tools: []
  services: []
  protocols: []
  python: []
  skills: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# {name} (English)

## When to activate

- "run {name}", "execute {name}", `/{name}`
- Whenever structured `{category}` tasks with auditable configuration are requested.

## Configuration & self-healing

This skill avoids hardcoded settings and resolves configuration through the 5-stage Ocean cascade:

`default-config.json` -> `config.json` -> `profiles/<channel>.json` -> `profiles/<channel>.<chat>.json` -> CLI flags (`--set key=value`).

Corrupt local override files automatically fall back to `default-config.json` and are preserved as `.corrupt.<ts>.bak` when `--repair` is passed.
{report_section}
## Providers & alternatives

- **Standalone execution:** Runs on the Python standard library with zero mandatory third-party packages.
- **Ecosystem docking:** Optional external bindings live in `connections.json` (`grounding-seed` compatible) and are never installed without user consent.

## Self-update

- Check `letzter_update_check` in `default-config.json` / `config.json` periodically and consult `skill-finder` for adjacent skills.
- Record dated findings in `connections.json` (`gelernt`) and real user requests in `user-usecases.json`.

## Changelog

### 0.1.0 ({today_iso})
- Initial scaffold generated via `ocean-skill-creator` (`v0.4.0`) with `default-config.json`, self-healing config loader, and test suite.
"""


def _build_scaffold_core_py(name: str, *, with_reports: bool) -> str:
    return f'''#!/usr/bin/env python3
"""Core runtime for {name} — stdlib-only self-healing config cascade{ " + multi-format reports" if with_reports else ""}."""

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
DEFAULT_CONFIG_PATH = SKILL_ROOT / "default-config.json"


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
    text = json.dumps(dict(payload), ensure_ascii=False, indent=2) + "\\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{{path.name}}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\\n") as handle:
            handle.write(text)
        os.replace(tmp_name, str(path))
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def load_skill_config(
    *,
    skill_root: Path = SKILL_ROOT,
    channel: str | None = None,
    chat: str | None = None,
    cli_overrides: Mapping[str, Any] | None = None,
    repair: bool = False,
) -> dict[str, Any]:
    default_cfg = json.loads((skill_root / "default-config.json").read_text(encoding="utf-8-sig"))
    effective = copy.deepcopy(default_cfg)
    warnings: list[str] = []
    candidates = [skill_root / "config.json"]
    if channel:
        candidates.append(skill_root / "profiles" / f"{{channel}}.json")
        if chat:
            candidates.append(skill_root / "profiles" / f"{{channel}}.{{chat}}.json")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for idx, candidate in enumerate(candidates):
        if not candidate.is_file():
            continue
        try:
            raw = json.loads(candidate.read_text(encoding="utf-8-sig"))
            if not isinstance(raw, dict):
                raise ValueError("JSON root must be object")
            effective = deep_merge(effective, raw)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            warnings.append(f"{{candidate.name}}: {{exc}}")
            if repair:
                bak = candidate.with_name(f"{{candidate.name}}.corrupt.{{ts}}.bak")
                shutil.copy2(str(candidate), str(bak))
                atomic_write_json(candidate, default_cfg if idx == 0 else {{}})
    if cli_overrides:
        effective = deep_merge(effective, cli_overrides)
    return {{"config": effective, "warnings": warnings}}


def render_minimal_pdf(title: str, lines: Sequence[str]) -> bytes:
    rows = [title, "=" * min(max(len(title), 10), 68), ""] + [str(x) for x in lines]
    ops = ["BT", "/F1 10 Tf", "50 790 Td", "14 TL"]
    for idx, line in enumerate(rows[:46]):
        safe = line.encode("latin-1", errors="replace").decode("latin-1")
        safe = safe.replace("\\\\", "\\\\\\\\").replace("(", "\\\\(").replace(")", "\\\\)")
        ops.append(f"({{safe}}) Tj" if idx == 0 else f"T* ({{safe}}) Tj")
    ops.append("ET")
    stream = "\\n".join(ops).encode("ascii")
    objs = [
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Pages /Kids [4 0 R] /Count 1 >>",
        f"<< /Length {{len(stream)}} >>\\nstream\\n".encode("ascii") + stream + b"\\nendstream",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 1 0 R >> >> /Contents 3 0 R >>",
        b"<< /Type /Catalog /Pages 2 0 R >>",
    ]
    buf = bytearray(b"%PDF-1.4\\n")
    offs = [0]
    for i, body in enumerate(objs, 1):
        offs.append(len(buf))
        buf.extend(f"{{i}} 0 obj\\n".encode("ascii") + body + b"\\nendobj\\n")
    xref = len(buf)
    buf.extend(f"xref\\n0 {{len(objs) + 1}}\\n0000000000 65535 f \\n".encode("ascii"))
    for off in offs[1:]:
        buf.extend(f"{{off:010d}} 00000 n \\n".encode("ascii"))
    buf.extend(f"trailer\\n<< /Size {{len(objs) + 1}} /Root 5 0 R >>\\nstartxref\\n{{xref}}\\n%%EOF\\n".encode("ascii"))
    return bytes(buf)


def render_output(payload: Mapping[str, Any], fmt: str, cfg: Mapping[str, Any]) -> bytes | str:
    fmt = fmt.lower()
    if fmt == "json":
        return json.dumps(dict(payload), ensure_ascii=False, indent=2) + "\\n"
    title = str(payload.get("title") or "{name}")
    summary = str(payload.get("summary") or "OK")
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if fmt == "pdf":
        return render_minimal_pdf(title, [f"Generated: {{now_iso}}", f"Summary: {{summary}}"])
    tpl_cfg = cfg.get("templates") if isinstance(cfg.get("templates"), dict) else {{}}
    tpl_dir = Path(tpl_cfg.get("custom_dir") or (SKILL_ROOT / str(tpl_cfg.get("dir") or "templates")))
    tpl_file = tpl_dir / f"report.template.{{fmt}}"
    if tpl_file.is_file():
        tpl = tpl_file.read_text(encoding="utf-8")
        return (
            tpl.replace("{{{{title}}}}", html.escape(title) if fmt == "html" else title)
            .replace("{{{{subtitle}}}}", "{name}")
            .replace("{{{{generated_at}}}}", now_iso)
            .replace("{{{{summary}}}}", html.escape(summary) if fmt == "html" else summary)
            .replace("{{{{body_html}}}}", f"<p>{{html.escape(summary)}}</p>")
            .replace("{{{{body_md}}}}", summary)
            .replace("{{{{body_txt}}}}", summary)
            .replace("{{{{footer}}}}", "{name} v0.1.0")
        )
    return f"{{title}}\\n{{summary}}\\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="{name}")
    parser.add_argument("--channel", default=None)
    parser.add_argument("--chat", default=None)
    parser.add_argument("--format", dest="fmt", default=None, choices=["html", "pdf", "md", "txt", "json"])
    parser.add_argument("--out", default=None)
    parser.add_argument("--repair", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    loaded = load_skill_config(channel=args.channel, chat=args.chat, repair=args.repair)
    cfg = loaded["config"]
    fmt = args.fmt or cfg.get("output", {{}}).get("default_format", "json")
    rendered = render_output({{"skill": "{name}", "title": "{name} Report", "summary": "Ready", "warnings": loaded["warnings"]}}, fmt, cfg)
    if args.out:
        out_p = Path(args.out)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(rendered, bytes):
            out_p.write_bytes(rendered)
        else:
            out_p.write_text(rendered, encoding="utf-8")
    elif isinstance(rendered, bytes):
        sys.stdout.buffer.write(rendered)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def _build_scaffold_test_py(name: str, *, with_reports: bool) -> str:
    snake = name.replace("-", "_")
    report_assertion = (
        f"""
def test_{snake}_pdf_and_html_rendering():
    mod = _load_core()
    loaded = mod.load_skill_config()
    pdf_bytes = mod.render_output({{"title": "Test", "summary": "All good"}}, "pdf", loaded["config"])
    assert pdf_bytes.startswith(b"%PDF-1.4")
    html_text = mod.render_output({{"title": "Test", "summary": "All good"}}, "html", loaded["config"])
    assert "<html" in html_text
"""
        if with_reports
        else ""
    )
    return f'''"""Self-healing config and runtime smoke tests for {name}."""

from __future__ import annotations

import importlib.util
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def _load_core():
    script = SKILL_ROOT / "scripts" / "{snake}_core.py"
    spec = importlib.util.spec_from_file_location("{snake}_core", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_{snake}_default_config_and_corrupt_self_healing(tmp_path):
    mod = _load_core()
    (tmp_path / "default-config.json").write_text(
        (SKILL_ROOT / "default-config.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    corrupt_cfg = tmp_path / "config.json"
    corrupt_cfg.write_text("{{broken json", encoding="utf-8")
    loaded = mod.load_skill_config(skill_root=tmp_path, repair=True)
    assert loaded["config"]["skill"] == "{name}"
    assert loaded["warnings"]
    assert list(tmp_path.glob("config.json.corrupt.*.bak"))
{report_assertion}'''


def scaffold_skill(
    name: str,
    *,
    category: str,
    out_dir: str | Path,
    with_reports: bool = False,
    with_profiles: bool = False,
    today: str | None = None,
) -> dict[str, Any]:
    """Create a standard-conformant Ocean skill directory."""
    clean_name = name.strip()
    clean_category = category.strip()
    if not SKILL_SLUG_RE.fullmatch(clean_name):
        raise ValueError(f"Skill name must be kebab-case, got {name!r}")
    if not SKILL_SLUG_RE.fullmatch(clean_category):
        raise ValueError(f"Category must be kebab-case, got {category!r}")

    base_out = Path(out_dir)
    skill_dir = base_out if base_out.name == clean_name else (base_out / clean_name)
    if skill_dir.exists() and any(skill_dir.iterdir()):
        raise FileExistsError(f"Target skill directory already exists and is non-empty: {skill_dir}")

    today_iso = today or date.today().isoformat()
    snake = clean_name.replace("-", "_")
    created_files: list[str] = []

    def _write_text(rel: str, content: str) -> None:
        target = skill_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        created_files.append(rel)

    # 1. SKILL.md & SKILL.en.md
    _write_text(
        "SKILL.md",
        _build_scaffold_skill_md_de(clean_name, clean_category, today_iso, with_reports=with_reports),
    )
    _write_text(
        "SKILL.en.md",
        _build_scaffold_skill_md_en(clean_name, clean_category, today_iso, with_reports=with_reports),
    )

    # 2. default-config.json & connections.json from bundled templates
    default_tpl = json.loads(
        (TEMPLATES_DIR / "default-config.template.json").read_text(encoding="utf-8")
    )
    default_tpl["skill"] = clean_name
    if not with_reports:
        default_tpl["output"]["default_format"] = "json"
    atomic_write_json(skill_dir / "default-config.json", default_tpl)
    created_files.append("default-config.json")

    conn_tpl = json.loads(
        (TEMPLATES_DIR / "skill-connections.template.json").read_text(encoding="utf-8")
    )
    atomic_write_json(skill_dir / "connections.json", conn_tpl)
    created_files.append("connections.json")

    # 3. Optional profiles (<channel>.json & <channel>.<chat>.json)
    if with_profiles:
        chan_tpl = json.loads(
            (TEMPLATES_DIR / "channel-profile.template.json").read_text(encoding="utf-8")
        )
        example_channel = copy.deepcopy(chan_tpl)
        example_channel["channel"] = "example"
        example_channel["delivery"]["channel"] = "example"
        atomic_write_json(skill_dir / "profiles" / "example.json", example_channel)
        created_files.append("profiles/example.json")

        example_chat = copy.deepcopy(example_channel)
        example_chat["chat"] = "team-digest"
        example_chat["output"] = {"default_format": "html" if with_reports else "json"}
        atomic_write_json(skill_dir / "profiles" / "example.team-digest.json", example_chat)
        created_files.append("profiles/example.team-digest.json")

    # 4. Optional replaceable report templates
    if with_reports:
        for tpl_name in ("report.template.html", "report.template.md", "report.template.txt"):
            src = OUTPUT_TEMPLATES_DIR / tpl_name
            _write_text(f"templates/{tpl_name}", src.read_text(encoding="utf-8"))

    # 5. Stdlib core script & pytest suite
    _write_text(f"scripts/{snake}_core.py", _build_scaffold_core_py(clean_name, with_reports=with_reports))
    _write_text(f"tests/test_{snake}.py", _build_scaffold_test_py(clean_name, with_reports=with_reports))

    return {
        "ok": True,
        "skill": clean_name,
        "category": clean_category,
        "skill_dir": str(skill_dir),
        "with_reports": with_reports,
        "with_profiles": with_profiles,
        "created_files": sorted(created_files),
    }


# ---------------------------------------------------------------------------
# Read-Only Skill Conformance Auditor (audit-skill subcommand)
# ---------------------------------------------------------------------------

def _extract_frontmatter_dict(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line.strip() or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            val = v.strip()
            if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
                try:
                    val = json.loads(val)
                except json.JSONDecodeError:
                    val = val[1:-1]
            data[k.strip()] = val
    return data


def audit_skill(skill_dir: str | Path) -> dict[str, Any]:
    """Inspect an existing skill directory read-only against Ocean v0.4.0 standards."""
    root = Path(skill_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Skill directory not found: {root}")

    skill_md = root / "SKILL.md"
    skill_en = root / "SKILL.en.md"
    has_skill_md = skill_md.is_file()
    has_skill_en_md = skill_en.is_file()

    md_text = skill_md.read_text(encoding="utf-8", errors="replace") if has_skill_md else ""
    fm = _extract_frontmatter_dict(md_text)
    skill_name = fm.get("name") or root.name
    desc = fm.get("description", "")

    missing_fm = [k for k in REQUIRED_FRONTMATTER_KEYS if not fm.get(k)]
    frontmatter_complete = has_skill_md and len(missing_fm) == 0
    trigger_in_250 = bool(desc and TRIGGER_RE.search(desc[:250]))

    default_cfg_path = root / "default-config.json"
    config_json_path = root / "config.json"
    has_default_config = default_cfg_path.is_file()
    has_config_json = config_json_path.is_file()
    has_profiles_dir = (root / "profiles").is_dir()

    parsed_cfg: dict[str, Any] = {}
    for candidate in (default_cfg_path, config_json_path):
        if candidate.is_file():
            try:
                loaded = json.loads(candidate.read_text(encoding="utf-8-sig"))
                if isinstance(loaded, dict):
                    parsed_cfg = deep_merge(parsed_cfg, loaded)
            except (OSError, json.JSONDecodeError):
                pass

    py_files = sorted(
        p
        for p in root.rglob("*.py")
        if "__pycache__" not in p.parts and not p.name.startswith("test_")
    )
    test_files = sorted(
        p
        for p in root.rglob("*.py")
        if "__pycache__" not in p.parts
        and (p.name.startswith("test_") or p.name.endswith("_test.py") or "tests" in p.parts)
    )
    has_scripts = len(py_files) > 0
    has_tests = len(test_files) > 0

    py_corpus = "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in py_files
    )
    has_self_healing = bool(
        isinstance(parsed_cfg.get("self_healing"), dict)
        or ".corrupt." in py_corpus
        or "load_effective_config" in py_corpus
        or "load_skill_config" in py_corpus
    )

    templates_root = root / "templates"
    template_files = (
        sorted(p.relative_to(root).as_posix() for p in templates_root.rglob("*") if p.is_file())
        if templates_root.is_dir()
        else []
    )
    has_report_templates = any(
        p.endswith((".html", ".md", ".txt")) for p in template_files
    )
    produces_reports = bool(
        has_report_templates
        or isinstance(parsed_cfg.get("output"), dict)
        or REPORT_SIGNAL_RE.search(desc)
    )

    hardcoding_signals: list[dict[str, str]] = []
    for p in py_files:
        rel = p.relative_to(root).as_posix()
        src = p.read_text(encoding="utf-8", errors="replace")
        path_match = HARDCODED_PATH_RE.search(src)
        if path_match:
            hardcoding_signals.append({
                "file": rel,
                "kind": "hardcoded_path",
                "detail": f"Hardcoded user/system path literal detected ({path_match.group(0)[:48]})",
            })
        if INLINE_HTML_RE.search(src) and not has_report_templates:
            hardcoding_signals.append({
                "file": rel,
                "kind": "inline_html_without_templates",
                "detail": "Inline HTML/CSS found in script without replaceable templates/ directory",
            })
        if HARDCODED_FORMAT_RE.search(src) and not (has_default_config or has_config_json):
            hardcoding_signals.append({
                "file": rel,
                "kind": "hardcoded_output_format",
                "detail": "Default output format hardcoded in script without default-config.json",
            })
        if MAGIC_THRESHOLD_RE.search(src) and not (has_default_config or has_config_json):
            hardcoding_signals.append({
                "file": rel,
                "kind": "magic_thresholds_without_config",
                "detail": "Numeric thresholds/limits hardcoded as module constants without JSON config",
            })

    delivery_cfg = parsed_cfg.get("delivery")
    if isinstance(delivery_cfg, dict) and (
        delivery_cfg.get("enabled") is True and delivery_cfg.get("dry_run") is False
    ):
        hardcoding_signals.append({
            "file": "default-config.json",
            "kind": "unsafe_delivery_default",
            "detail": "delivery.enabled=true with dry_run=false violates safe draft default",
        })

    # Deterministic 0..100 score + actionable recommendations
    score = 0
    recommendations: list[str] = []

    if frontmatter_complete:
        score += 20
    else:
        recommendations.append(
            f"Complete 9-field Ocean frontmatter in SKILL.md (missing: {', '.join(missing_fm) or 'SKILL.md'})"
        )

    if has_skill_en_md:
        score += 10
    else:
        recommendations.append("Add structural English counterpart SKILL.en.md (Core P-006)")

    if trigger_in_250:
        score += 10
    else:
        recommendations.append(
            "Place WHEN trigger ('Verwenden, wenn ...' / 'Use when ...') within the first 250 chars of description"
        )

    if has_default_config:
        score += 20
    elif has_config_json:
        score += 10
        recommendations.append(
            "Add tracked neutral default-config.json so local config.json can remain a clean override"
        )
    else:
        recommendations.append(
            "Externalize settings into default-config.json (plus optional config.json & profiles/<channel>.json)"
        )

    if has_self_healing:
        score += 15
    else:
        recommendations.append(
            "Wire self-healing config loading (graceful fallback to default-config.json + .corrupt.<ts>.bak backup)"
        )

    if produces_reports:
        if has_report_templates:
            score += 15
        else:
            recommendations.append(
                "Move report layout into replaceable templates/ (report.template.html/md/txt) and support html/pdf/md/txt/json"
            )
    else:
        score += 15

    if has_scripts:
        if has_tests:
            score += 10
        else:
            score += 4
            recommendations.append("Add automated pytest coverage under tests/ for scripts and config cascade")
    else:
        score += 10

    penalty = min(len(hardcoding_signals) * 10, 30)
    score = max(0, min(100, score - penalty))
    if hardcoding_signals:
        recommendations.append(
            "Eliminate hardcoding signals by moving paths, formats, thresholds, and HTML markup into default-config.json and templates/"
        )

    if score >= 85 and not hardcoding_signals:
        status = "conformant"
    elif score >= 55:
        status = "needs_upgrade"
    else:
        status = "minimal"

    return {
        "skill": skill_name,
        "skill_dir": str(root),
        "score": score,
        "status": status,
        "checks": {
            "has_skill_md": has_skill_md,
            "has_skill_en_md": has_skill_en_md,
            "frontmatter_complete": frontmatter_complete,
            "missing_frontmatter_keys": missing_fm,
            "trigger_in_first_250_chars": trigger_in_250,
            "has_default_config": has_default_config,
            "has_config_json": has_config_json,
            "has_profiles_dir": has_profiles_dir,
            "has_self_healing": has_self_healing,
            "produces_reports": produces_reports,
            "has_templates_dir": templates_root.is_dir(),
            "has_report_templates": has_report_templates,
            "template_files": template_files,
            "has_scripts": has_scripts,
            "has_tests": has_tests,
        },
        "hardcoding_signals": hardcoding_signals,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ocean_skill_scaffold",
        description="Ocean Skill Creator v0.4.0 — Scaffold, Self-Healing Config Validator & Skill Auditor.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_scaf = sub.add_parser("scaffold", help="Create a new Ocean-conformant skill scaffold")
    p_scaf.add_argument("name", help="Skill slug in kebab-case (e.g. invoice-digest)")
    p_scaf.add_argument("--category", required=True, help="Target skill category folder (e.g. utilities)")
    p_scaf.add_argument("--out", required=True, help="Parent output directory (creates <out>/<name>/)")
    p_scaf.add_argument("--with-reports", action="store_true", help="Include templates/ and html/pdf/md/txt/json report support")
    p_scaf.add_argument("--with-profiles", action="store_true", help="Include sample channel/chat override profiles/")
    p_scaf.add_argument("--json", action="store_true", help="Emit JSON result")

    p_val = sub.add_parser("validate-config", help="Validate, merge, and optionally self-heal a config cascade")
    p_val.add_argument("--default", required=True, dest="default_path", help="Path to default-config.json")
    p_val.add_argument("--config", default=None, dest="config_path", help="Optional path to local config.json")
    p_val.add_argument("--channel", default=None, help="Optional channel name (<channel>.json under profiles/)")
    p_val.add_argument("--chat", default=None, help="Optional chat/target name (<channel>.<chat>.json under profiles/)")
    p_val.add_argument("--profile", action="append", default=[], dest="profiles", help="Explicit profile JSON path(s) in cascade order")
    p_val.add_argument("--set", action="append", default=[], dest="cli_sets", help="CLI override key.path=value")
    p_val.add_argument("--repair", action="store_true", help="Backup corrupt overrides (.corrupt.<ts>.bak) and self-heal atomically")
    p_val.add_argument("--json", action="store_true", help="Emit JSON result")

    p_aud = sub.add_parser("audit-skill", help="Audit an existing skill directory read-only")
    p_aud.add_argument("skill_dir", help="Path to the skill directory")
    p_aud.add_argument("--json", action="store_true", help="Emit JSON audit report")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        if args.command == "scaffold":
            res = scaffold_skill(
                args.name,
                category=args.category,
                out_dir=args.out,
                with_reports=args.with_reports,
                with_profiles=args.with_profiles,
            )
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(f"Scaffolded {res['skill']} -> {res['skill_dir']} ({len(res['created_files'])} files)")
            return 0

        if args.command == "validate-config":
            def_p = Path(args.default_path)
            chain: list[Path] = []
            if args.config_path or args.channel or args.chat:
                chain.extend(
                    resolve_profile_chain(
                        def_p.parent,
                        config_path=args.config_path,
                        channel=args.channel,
                        chat=args.chat,
                        extra_profiles=args.profiles,
                    )
                )
            elif args.profiles:
                chain.extend(Path(p) for p in args.profiles)
            cli_dict = dotted_pairs_to_dict(args.cli_sets) if args.cli_sets else None
            res = load_effective_config(
                def_p,
                chain,
                cli_overrides=cli_dict,
                repair=args.repair,
            )
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(
                    f"OK={res['ok']} applied={len(res['layers_applied'])} "
                    f"warnings={len(res['warnings'])} healed={len(res['healed'])}"
                )
            return 0 if res["ok"] else 1

        if args.command == "audit-skill":
            res = audit_skill(args.skill_dir)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(
                    f"SKILL={res['skill']} SCORE={res['score']}/100 STATUS={res['status']} "
                    f"RECOMMENDATIONS={len(res['recommendations'])}"
                )
            return 0
    except (ValueError, OSError, FileExistsError, FileNotFoundError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
