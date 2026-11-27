#!/usr/bin/env python3
"""Core runtime for chat-mail-protocol (v0.1.0) — 100% Python Standard Library.

Capabilities:
- Hierarchical self-healing configuration cascade:
  ``default-config.json -> config.json -> <channel>.json -> <channel>.<chat>.json -> CLI``
  with graceful fallback, ``.corrupt.<YYYYMMDDTHHMMSSZ>.bak`` backup, and atomic writes.
- Multi-format chat & email thread parser (WhatsApp, Slack, Discord, Telegram, Teams,
  JSON message exports, multi-message Email threads, generic transcripts) + optional
  participant anonymization.
- Source-anchored, hallucination-free extractor for summaries, decisions, action items
  (owner + explicit due date only), open questions, blockers, and chronology.
- Replaceable template renderer across ``html``, ``pdf`` (pure-stdlib ``%PDF-1.4`` with
  ``WinAnsiEncoding`` Umlaut support & verified ``xref`` offsets), ``md``, ``txt``, ``json``.
- Safe draft/dry-run delivery & ``reply_in_chat`` planner.
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
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = SKILL_ROOT / "default-config.json"
BUNDLED_TEMPLATES_DIR = SKILL_ROOT / "templates"

VALID_CHANNELS = ("auto", "whatsapp", "slack", "discord", "telegram", "teams", "email", "generic")
VALID_DOC_TYPES = ("zusammenfassung", "protokoll", "ergebnisprotokoll", "aufgabenliste")
VALID_FORMATS = ("html", "pdf", "md", "txt", "json")

# Chat / Email parsing patterns
_WA_BRACKET_RE = re.compile(
    r"^\[(?P<ts>\d{1,2}[./]\d{1,2}[./]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\]\s+"
    r"(?P<author>[^:\n]{1,80}):\s*(?P<text>.*)$"
)
_WA_DASH_RE = re.compile(
    r"^(?P<ts>\d{1,2}\.\d{1,2}\.\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?)\s+-\s+"
    r"(?P<author>[^:\n]{1,80}):\s*(?P<text>.*)$"
)
_SLACK_ISO_BRACKET_RE = re.compile(
    r"^\[(?P<ts>\d{4}-\d{2}-\d{2}[T\s]\d{1,2}:\d{2}(?::\d{2})?)\]\s+"
    r"(?P<author>[^:\n]{1,80}):\s*(?P<text>.*)$"
)
_AUTHOR_TIME_INLINE_RE = re.compile(
    r"^(?P<author>[A-Za-zÄÖÜäöüß0-9_.\- ]{1,60}?)\s+"
    r"\[(?P<ts>(?:\d{4}-\d{2}-\d{2}\s+)?\d{1,2}:\d{2}(?::\d{2})?)\]:\s*(?P<text>.*)$"
)
_DISCORD_HEADER_RE = re.compile(
    r"^(?P<author>[A-Za-zÄÖÜäöüß0-9_.\- ]{1,60}?)\s*(?:—|--|-)\s*"
    r"(?P<ts>(?:\d{1,2}\.\d{1,2}\.\d{2,4}|\d{4}-\d{2}-\d{2}|Heute|Gestern|Today|Yesterday)[^\n]{0,24})$"
)
_GENERIC_COLON_RE = re.compile(
    r"^(?P<author>[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß0-9_.\- ]{0,48}):\s+(?P<text>.+)$"
)

_EMAIL_HEADER_KEY_RE = re.compile(
    r"^(?P<key>From|Von|To|An|Cc|Date|Datum|Sent|Gesendet|Subject|Betreff):\s*(?P<val>.*)$",
    re.IGNORECASE,
)
_EMAIL_SPLIT_RE = re.compile(
    r"(?m)^(?:\s*-{2,}\s*(?:Original Message|Ursprüngliche Nachricht|Ursprungliche Nachricht|Forwarded message)\s*-{2,}\s*$"
    r"|(?:On\s+.+?\s+wrote:|Am\s+.+?\s+schrieb\s+.+?:)\s*$)"
)

# Rule-based extraction patterns
_DECISION_RE = re.compile(
    r"\b(?:"
    r"beschlossen|entschieden|vereinbart|festgelegt|verabschiedet|freigegeben|"
    r"machen\s+wir\s+so|wir\s+nehmen|wir\s+nutzen|wir\s+bleiben\s+bei|"
    r"beschluss\s*:|ergebnis\s*:|konsens\s*:|"
    r"agreed|decided|approved|we\s+will\s+use|let's\s+go\s+with|decision\s*:"
    r")\b",
    re.IGNORECASE,
)
_TASK_PREFIX_RE = re.compile(
    r"^(?:[-*]\s*\[\s*\]\s*|(?:TODO|TASK|AUFGABE|ACTION|AI)\s*[:\-]\s*)(?P<body>.+)$",
    re.IGNORECASE,
)
_TASK_SIGNAL_RE = re.compile(
    r"\b(?:"
    r"todo|aufgabe|action\s+item|übernimmt|uebernimmt|kümmert\s+sich|kuemmert\s+sich|"
    r"bitte\s+.{3,80}?\b(?:bis|erledigen|prüfen|pruefen|schicken|anlegen|bauen|aktualisieren|klären|klaeren)\b|"
    r"ich\s+(?:übernehme|uebernehme|kümmere\s+mich|kuemmere\s+mich|schicke|erstelle|baue|prüfe|pruefe)|"
    r"kannst\s+du\b|könntest\s+du\b|please\s+(?:prepare|send|check|update|fix|create)|"
    r"will\s+handle|takes\s+care\s+of|i'll\s+(?:handle|send|prepare|update)"
    r")",
    re.IGNORECASE,
)
_BLOCKER_RE = re.compile(
    r"\b(?:"
    r"blocker|blockiert|hängt\s+an|haengt\s+an|wartet\s+auf|fehlt\s+noch|"
    r"blocked\s+by|waiting\s+on|waiting\s+for"
    r")\b",
    re.IGNORECASE,
)
_OPEN_QUESTION_RE = re.compile(
    r"\b(?:offen\s*:|unklar|zu\s+klären|zu\s+klaeren|tbd|open\s+question)\b",
    re.IGNORECASE,
)
_MENTION_RE = re.compile(r"@([A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß0-9_.-]{0,40})")
_OWNER_VERB_RE = re.compile(
    r"\b(?P<who>[A-ZÄÖÜ][A-Za-zÄÖÜäöüß0-9_.-]{1,32})\s+"
    r"(?:übernimmt|uebernimmt|kümmert\s+sich|kuemmert\s+sich|erstellt|schickt|prüft|prueft|will\s+handle|takes\s+care\s+of)\b"
)
_FIRST_PERSON_TASK_RE = re.compile(
    r"\b(?:ich\s+(?:übernehme|uebernehme|kümmere\s+mich|kuemmere\s+mich|schicke|erstelle|baue|prüfe|pruefe)|"
    r"i\s+will\s+(?:handle|send|prepare|update)|i'll\s+(?:handle|send|prepare|update))\b",
    re.IGNORECASE,
)
_ISO_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
_DE_DATE_RE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b")


# ---------------------------------------------------------------------------
# 1. Self-Healing Hierarchical Config Loader
# ---------------------------------------------------------------------------

def slugify_identifier(raw: str | None) -> str:
    if not raw:
        return ""
    cleaned = raw.strip().lower()
    cleaned = (
        cleaned.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    cleaned = re.sub(r"[^a-z0-9_-]+", "-", cleaned).strip("-")
    return cleaned


def utc_compact_timestamp(now: datetime | None = None) -> str:
    dt = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def atomic_write_json(path: str | Path, data: Mapping[str, Any]) -> Path:
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


def _backup_corrupt_file(path: Path, ts: str) -> Path:
    backup = path.with_name(f"{path.name}.corrupt.{ts}.bak")
    idx = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.corrupt.{ts}.{idx}.bak")
        idx += 1
    shutil.copy2(str(path), str(backup))
    return backup


def _validate_override_types(
    default_cfg: Mapping[str, Any],
    override_cfg: Mapping[str, Any],
    *,
    label: str,
    warnings: list[str],
) -> tuple[dict[str, Any], bool]:
    cleaned: dict[str, Any] = {}
    had_mismatch = False
    for key, val in override_cfg.items():
        if key in ("_hinweis", "_comment"):
            continue
        def_val = default_cfg.get(key)
        if isinstance(def_val, dict) and not isinstance(val, dict):
            warnings.append(
                f"{label}: section {key!r} must be an object, got {type(val).__name__}; kept default"
            )
            had_mismatch = True
            continue
        if key in ("doc_types", "formats") and not (
            isinstance(val, list) and all(isinstance(x, str) for x in val)
        ):
            warnings.append(
                f"{label}: field {key!r} must be a list of strings; kept previous layer"
            )
            had_mismatch = True
            continue
        cleaned[key] = copy.deepcopy(val)
    return cleaned, had_mismatch


def _resolve_candidate_profile(base_dir: Path, filename: str, *, include_profiles_subdir: bool) -> Path:
    direct = base_dir / filename
    if direct.exists() or not include_profiles_subdir:
        return direct
    in_sub = base_dir / "profiles" / filename
    return in_sub if in_sub.exists() else direct


def load_effective_channel_config(
    *,
    skill_root: str | Path = SKILL_ROOT,
    config_dir: str | Path | None = None,
    channel: str | None = None,
    chat: str | None = None,
    cli_overrides: Mapping[str, Any] | None = None,
    repair_config: bool = False,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Load and self-heal the hierarchical channel/chat configuration cascade.

    Order:
    ``default-config.json -> config.json -> <channel>.json -> <channel>.<chat>.json -> cli_overrides``
    """
    sroot = Path(skill_root)
    def_path = sroot / "default-config.json"
    if not def_path.is_file():
        raise FileNotFoundError(f"Missing default-config.json at {def_path}")
    default_cfg = json.loads(def_path.read_text(encoding="utf-8-sig"))
    if not isinstance(default_cfg, dict):
        raise ValueError("default-config.json root must be a JSON object")

    cdir = Path(config_dir) if config_dir is not None else sroot
    use_sub = cdir.resolve() == sroot.resolve()

    chan_slug = slugify_identifier(channel) if channel and channel != "auto" else ""
    chat_slug = slugify_identifier(chat)

    candidates: list[tuple[str, Path]] = [("config.json", cdir / "config.json")]
    if chan_slug:
        candidates.append((
            f"{chan_slug}.json",
            _resolve_candidate_profile(cdir, f"{chan_slug}.json", include_profiles_subdir=use_sub),
        ))
        if chat_slug:
            candidates.append((
                f"{chan_slug}.{chat_slug}.json",
                _resolve_candidate_profile(
                    cdir, f"{chan_slug}.{chat_slug}.json", include_profiles_subdir=use_sub
                ),
            ))

    ts = timestamp or utc_compact_timestamp()
    effective: dict[str, Any] = copy.deepcopy(default_cfg)
    loaded_layers: list[str] = [str(def_path)]
    skipped_layers: list[str] = []
    warnings: list[str] = []
    healed: list[dict[str, str]] = []

    for idx, (_short_label, cand_path) in enumerate(candidates):
        is_root_cfg = idx == 0
        if not cand_path.exists():
            skipped_layers.append(str(cand_path))
            continue
        if cand_path.is_dir():
            warnings.append(f"{cand_path}: expected JSON file, found directory; skipped")
            skipped_layers.append(str(cand_path))
            continue

        try:
            raw_obj = json.loads(cand_path.read_text(encoding="utf-8-sig"))
            if not isinstance(raw_obj, dict):
                raise ValueError(f"JSON root must be object, got {type(raw_obj).__name__}")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            warnings.append(f"{cand_path}: corrupt config ({exc}); fell back to intact layer")
            if repair_config:
                bak = _backup_corrupt_file(cand_path, ts)
                restored: dict[str, Any] = copy.deepcopy(default_cfg) if is_root_cfg else {}
                atomic_write_json(cand_path, restored)
                healed.append({
                    "path": str(cand_path),
                    "backup_path": str(bak),
                    "reason": str(exc),
                    "action": "restored_default" if is_root_cfg else "reset_empty_profile",
                })
                loaded_layers.append(str(cand_path))
            else:
                skipped_layers.append(str(cand_path))
            continue

        cleaned_obj, had_mismatch = _validate_override_types(
            default_cfg, raw_obj, label=str(cand_path), warnings=warnings
        )
        if repair_config and had_mismatch:
            bak = _backup_corrupt_file(cand_path, ts)
            to_save = deep_merge(default_cfg, cleaned_obj) if is_root_cfg else cleaned_obj
            atomic_write_json(cand_path, to_save)
            healed.append({
                "path": str(cand_path),
                "backup_path": str(bak),
                "reason": "invalid field type sanitized",
                "action": "sanitized_and_saved",
            })

        effective = deep_merge(effective, cleaned_obj)
        loaded_layers.append(str(cand_path))

    if cli_overrides:
        cleaned_cli, _ = _validate_override_types(
            default_cfg, cli_overrides, label="cli_overrides", warnings=warnings
        )
        effective = deep_merge(effective, cleaned_cli)
        loaded_layers.append("cli_overrides")

    return {
        "ok": len(warnings) == 0 or bool(repair_config and len(healed) >= len(warnings)),
        "config": effective,
        "channel": chan_slug or None,
        "chat": chat_slug or None,
        "loaded_layers": loaded_layers,
        "skipped_layers": skipped_layers,
        "warnings": warnings,
        "healed": healed,
    }


# ---------------------------------------------------------------------------
# 2. Multi-Format Chat & Email Thread Parser
# ---------------------------------------------------------------------------

def _clean_email_sender(raw: str) -> str:
    text = raw.strip()
    angle = re.match(r'^"?([^"<]+?)"?\s*<[^>]+>$', text)
    if angle:
        return angle.group(1).strip()
    return text.strip('"') or "Unknown"


def _looks_like_email_thread(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20])
    hits = len(re.findall(r"(?m)^(?:From|Von|To|An|Subject|Betreff|Date|Datum):\s+", head))
    return hits >= 2


def _parse_email_thread(text: str) -> tuple[list[dict[str, Any]], str | None]:
    chunks = _EMAIL_SPLIT_RE.split(text)
    messages: list[dict[str, Any]] = []
    thread_subject: str | None = None

    for chunk in chunks:
        lines = chunk.strip().splitlines()
        if not lines:
            continue
        headers: dict[str, str] = {}
        body_start = 0
        for idx, line in enumerate(lines):
            if not line.strip():
                body_start = idx + 1
                break
            m = _EMAIL_HEADER_KEY_RE.match(line.strip())
            if m:
                headers[m.group("key").lower()] = m.group("val").strip()
                body_start = idx + 1
            else:
                if headers:
                    body_start = idx
                break

        raw_body_lines = lines[body_start:] if headers else lines
        # Strip quoted '>' lines so older replies are not counted twice
        unquoted = [ln for ln in raw_body_lines if not ln.lstrip().startswith(">")]
        body = "\n".join(unquoted).strip()
        if not body:
            continue

        subj = headers.get("subject") or headers.get("betreff")
        if subj and thread_subject is None:
            thread_subject = re.sub(r"^(?:(?:Re|Aw|Fwd|WG):\s*)+", "", subj, flags=re.I).strip() or subj

        sender_raw = headers.get("from") or headers.get("von") or "Mail Sender"
        author = _clean_email_sender(sender_raw)
        ts = headers.get("date") or headers.get("datum") or headers.get("sent") or headers.get("gesendet")
        messages.append({
            "author": author,
            "timestamp": ts,
            "text": body,
            "subject": subj,
        })

    # Top-posted email chains often have newest message at index 0 and older Original Message below;
    # if ISO timestamps clearly descend, sort chronologically.
    iso_timestamps = [m["timestamp"] for m in messages if isinstance(m.get("timestamp"), str)]
    if len(iso_timestamps) >= 2 and all(re.match(r"^\d{4}-\d{2}-\d{2}", x) for x in iso_timestamps):
        if iso_timestamps[0] > iso_timestamps[-1]:
            messages.reverse()

    for idx, msg in enumerate(messages, start=1):
        msg["source_index"] = idx
    return messages, thread_subject


def _person_alias(index: int) -> str:
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if index < 26:
        return f"Person {letters[index]}"
    return f"Person {letters[(index // 26) - 1]}{letters[index % 26]}"


def _apply_anonymization(messages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    mapping: dict[str, str] = {}
    for msg in messages:
        orig = str(msg.get("author") or "Unbekannt").strip()
        if orig not in mapping:
            mapping[orig] = _person_alias(len(mapping))

    # Build token replacement table: full names first, then unambiguous name parts (len >= 3)
    token_to_alias: dict[str, str] = dict(mapping)
    part_owners: dict[str, list[str]] = {}
    for full_name, alias in mapping.items():
        for part in re.findall(r"[A-Za-zÄÖÜäöüß]{3,}", full_name):
            if part.lower() in {"prof", "ing", "frau", "herr", "team"}:
                continue
            part_owners.setdefault(part, []).append(alias)
    for part, aliases in part_owners.items():
        if len(set(aliases)) == 1 and part not in token_to_alias:
            token_to_alias[part] = aliases[0]

    ordered_tokens = sorted(token_to_alias.keys(), key=len, reverse=True)
    anonymized: list[dict[str, Any]] = []
    for msg in messages:
        new_msg = dict(msg)
        orig_author = str(msg.get("author") or "Unbekannt").strip()
        new_msg["author"] = mapping[orig_author]
        txt = str(msg.get("text") or "")
        for real_tok in ordered_tokens:
            alias = token_to_alias[real_tok]
            alias_tag = alias.replace(" ", "_")
            txt = re.sub(rf"@{re.escape(real_tok)}\b", f"@{alias_tag}", txt)
            txt = re.sub(rf"\b{re.escape(real_tok)}\b", alias, txt)
        new_msg["text"] = txt
        anonymized.append(new_msg)
    return anonymized, mapping


def parse_messages(
    raw_text: str,
    *,
    channel_hint: str | None = None,
    anonymize_participants: bool = False,
) -> dict[str, Any]:
    """Parse chat exports, JSON message arrays, email threads, or plain transcripts."""
    cleaned = raw_text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    hint = (channel_hint or "auto").strip().lower()
    detected_channel = hint if hint != "auto" else "generic"
    detected_subject: str | None = None
    messages: list[dict[str, Any]] = []

    stripped = cleaned.strip()
    if stripped.startswith(("[", "{")):
        try:
            parsed_json = json.loads(stripped)
            raw_list = (
                parsed_json
                if isinstance(parsed_json, list)
                else parsed_json.get("messages", []) if isinstance(parsed_json, dict) else None
            )
            if isinstance(raw_list, list):
                if isinstance(parsed_json, dict) and parsed_json.get("channel") and hint == "auto":
                    detected_channel = slugify_identifier(str(parsed_json["channel"])) or "slack"
                elif hint == "auto":
                    detected_channel = "slack"
                for idx, entry in enumerate(raw_list, start=1):
                    if not isinstance(entry, dict):
                        continue
                    txt = str(
                        entry.get("text") or entry.get("content") or entry.get("body") or entry.get("message") or ""
                    ).strip()
                    if not txt:
                        continue
                    author = str(
                        entry.get("author") or entry.get("user") or entry.get("sender") or entry.get("from") or "Unknown"
                    ).strip()
                    ts = entry.get("timestamp") or entry.get("ts") or entry.get("date") or entry.get("time")
                    messages.append({
                        "source_index": idx,
                        "author": author,
                        "timestamp": str(ts).strip() if ts is not None else None,
                        "text": txt,
                    })
                if anonymize_participants:
                    messages, _ = _apply_anonymization(messages)
                return {
                    "channel": detected_channel,
                    "subject": detected_subject,
                    "messages": messages,
                }
        except json.JSONDecodeError:
            pass

    if hint == "email" or (hint == "auto" and _looks_like_email_thread(cleaned)):
        email_msgs, email_subj = _parse_email_thread(cleaned)
        if email_msgs:
            if anonymize_participants:
                email_msgs, _ = _apply_anonymization(email_msgs)
            return {
                "channel": "email",
                "subject": email_subj,
                "messages": email_msgs,
            }

    wa_hits = 0
    slack_hits = 0
    discord_hits = 0
    pending_discord_header: tuple[str, str] | None = None

    for raw_line in cleaned.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            pending_discord_header = None
            continue

        m_wa1 = _WA_BRACKET_RE.match(line)
        m_wa2 = None if m_wa1 else _WA_DASH_RE.match(line)
        if m_wa1 or m_wa2:
            m = m_wa1 or m_wa2
            assert m is not None
            wa_hits += 1
            pending_discord_header = None
            messages.append({
                "source_index": len(messages) + 1,
                "author": m.group("author").strip(),
                "timestamp": m.group("ts").strip(),
                "text": m.group("text").strip(),
            })
            continue

        m_sl = _SLACK_ISO_BRACKET_RE.match(line)
        m_inl = None if m_sl else _AUTHOR_TIME_INLINE_RE.match(line)
        if m_sl or m_inl:
            m = m_sl or m_inl
            assert m is not None
            slack_hits += 1
            pending_discord_header = None
            messages.append({
                "source_index": len(messages) + 1,
                "author": m.group("author").strip(),
                "timestamp": m.group("ts").strip(),
                "text": m.group("text").strip(),
            })
            continue

        m_disc = _DISCORD_HEADER_RE.match(line)
        if m_disc:
            discord_hits += 1
            pending_discord_header = (m_disc.group("author").strip(), m_disc.group("ts").strip())
            continue

        if pending_discord_header is not None:
            author, ts = pending_discord_header
            pending_discord_header = None
            messages.append({
                "source_index": len(messages) + 1,
                "author": author,
                "timestamp": ts,
                "text": line.strip(),
            })
            continue

        # Only treat bare 'Author: Text' as a speaker header in un-timestamped generic transcripts;
        # in timestamped WhatsApp/Slack/Discord exports, lines like 'Fortsetzung: ...' or 'Grund: ...'
        # are multiline continuations of the preceding message!
        m_gen = (
            _GENERIC_COLON_RE.match(line)
            if (wa_hits == 0 and slack_hits == 0 and discord_hits == 0 and hint in {"auto", "generic"})
            else None
        )
        if m_gen and not m_gen.group("author").lower().startswith(("http", "https", "mailto")):
            # Avoid treating "TODO: ..." inside a multiline message as a speaker named "TODO"
            cand_author = m_gen.group("author").strip()
            if cand_author.upper() not in {"TODO", "TASK", "AUFGABE", "ACTION", "BESCHLUSS", "ERGEBNIS", "OFFEN", "HINWEIS"}:
                messages.append({
                    "source_index": len(messages) + 1,
                    "author": cand_author,
                    "timestamp": None,
                    "text": m_gen.group("text").strip(),
                })
                continue

        # Multiline continuation of the previous message (or fallback anonymous note)
        if messages:
            messages[-1]["text"] = f"{messages[-1]['text']}\n{line.strip()}".strip()
        else:
            messages.append({
                "source_index": 1,
                "author": "Notiz",
                "timestamp": None,
                "text": line.strip(),
            })

    if hint == "auto":
        if wa_hits > 0:
            detected_channel = "whatsapp"
        elif discord_hits > 0:
            detected_channel = "discord"
        elif slack_hits > 0:
            detected_channel = "slack"
        else:
            detected_channel = "generic"

    if anonymize_participants:
        messages, _ = _apply_anonymization(messages)

    return {
        "channel": detected_channel,
        "subject": detected_subject,
        "messages": messages,
    }


# ---------------------------------------------------------------------------
# 3. Rule-Based, Source-Anchored Conversation Analyzer
# ---------------------------------------------------------------------------

def _extract_explicit_due_date(text: str) -> str | None:
    iso = _ISO_DATE_RE.search(text)
    if iso:
        return iso.group(1)
    de = _DE_DATE_RE.search(text)
    if de:
        day, month, year_raw = int(de.group(1)), int(de.group(2)), de.group(3)
        year = int(year_raw) + 2000 if len(year_raw) == 2 else int(year_raw)
        if 1 <= month <= 12 and 1 <= day <= 31:
            return f"{year:04d}-{month:02d}-{day:02d}"
    return None


def _resolve_task_owner(line: str, author: str, participants: Sequence[str]) -> str:
    mention = _MENTION_RE.search(line)
    if mention:
        raw_m = mention.group(1).replace("_", " ")
        for p in participants:
            if p.lower() == raw_m.lower() or p.lower().startswith(raw_m.lower()):
                return p
        return mention.group(1)

    if _FIRST_PERSON_TASK_RE.search(line):
        return author

    verb_m = _OWNER_VERB_RE.search(line)
    if verb_m:
        cand = verb_m.group("who")
        for p in participants:
            if p.lower() == cand.lower() or p.split()[0].lower() == cand.lower():
                return p
        if cand.lower() not in {"bitte", "wer", "jemand", "wir"}:
            return cand

    for p in participants:
        first_token = p.split()[0]
        if len(first_token) >= 3 and re.search(rf"\b{re.escape(first_token)}\b", line):
            if p != author or _FIRST_PERSON_TASK_RE.search(line):
                return p
    return "offen"


def _shorten_quote(text: str, limit: int = 140) -> str:
    single = re.sub(r"\s+", " ", text).strip()
    return single if len(single) <= limit else single[: limit - 1].rstrip() + "…"


def analyze_conversation(
    parsed_or_raw: Mapping[str, Any] | str,
    *,
    channel: str | None = None,
    chat: str | None = None,
    anonymize_participants: bool = False,
) -> dict[str, Any]:
    """Extract source-grounded decisions, tasks, open questions, blockers, and summary."""
    if isinstance(parsed_or_raw, str):
        parsed = parse_messages(
            parsed_or_raw,
            channel_hint=channel,
            anonymize_participants=anonymize_participants,
        )
    else:
        parsed = copy.deepcopy(dict(parsed_or_raw))
        if anonymize_participants and parsed.get("messages"):
            parsed["messages"], _ = _apply_anonymization(list(parsed["messages"]))

    messages: list[dict[str, Any]] = list(parsed.get("messages") or [])
    eff_channel = (
        slugify_identifier(channel)
        if channel and channel != "auto"
        else str(parsed.get("channel") or "generic")
    )
    chat_label = (chat or parsed.get("subject") or f"{eff_channel}-verlauf").strip()
    chat_slug = slugify_identifier(chat_label) or "allgemein"

    participants: list[str] = []
    timestamps: list[str] = []
    for msg in messages:
        auth = str(msg.get("author") or "Unbekannt").strip()
        if auth and auth not in participants:
            participants.append(auth)
        ts = msg.get("timestamp")
        if isinstance(ts, str) and ts.strip():
            timestamps.append(ts.strip())

    if timestamps:
        tf_start, tf_end = timestamps[0], timestamps[-1]
        tf_display = tf_start if tf_start == tf_end else f"{tf_start} – {tf_end}"
    else:
        tf_start, tf_end, tf_display = None, None, "keine Zeitangabe"

    decisions: list[dict[str, Any]] = []
    action_items: list[dict[str, Any]] = []
    open_questions: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []

    for msg in messages:
        src_idx = int(msg.get("source_index") or 0)
        author = str(msg.get("author") or "Unbekannt")
        ts = msg.get("timestamp")
        full_text = str(msg.get("text") or "")

        for raw_sentence in full_text.splitlines():
            line = raw_sentence.strip()
            if not line:
                continue

            # 1. Decisions
            if _DECISION_RE.search(line):
                cleaned_dec = re.sub(
                    r"^(?:beschluss|ergebnis|decision|konsens)\s*:\s*",
                    "",
                    line,
                    flags=re.I,
                ).strip()
                decisions.append({
                    "id": f"D-{len(decisions) + 1:02d}",
                    "text": cleaned_dec or line,
                    "author": author,
                    "timestamp": ts,
                    "source_index": src_idx,
                    "quote": _shorten_quote(line),
                })

            # 2. Action items / tasks
            pref_m = _TASK_PREFIX_RE.match(line)
            has_mention_request = bool(
                _MENTION_RE.search(line)
                and not line.endswith("?")
                and len(line.split()) >= 3
            )
            if pref_m or _TASK_SIGNAL_RE.search(line) or has_mention_request:
                # Skip pure questions unless explicitly prefixed as TODO/TASK
                if line.endswith("?") and not pref_m and not re.search(r"\bkannst\s+du\b|\bkönntest\s+du\b", line, re.I):
                    pass
                else:
                    task_body = pref_m.group("body").strip() if pref_m else line
                    owner = _resolve_task_owner(line, author, participants)
                    due = _extract_explicit_due_date(line)
                    action_items.append({
                        "id": f"A-{len(action_items) + 1:02d}",
                        "task": task_body,
                        "owner": owner,
                        "due": due,
                        "status": "open",
                        "author": author,
                        "timestamp": ts,
                        "source_index": src_idx,
                        "quote": _shorten_quote(line),
                    })

            # 3. Blockers & Open Questions
            if _BLOCKER_RE.search(line):
                blockers.append({
                    "id": f"B-{len(blockers) + 1:02d}",
                    "kind": "blocker",
                    "text": line,
                    "author": author,
                    "timestamp": ts,
                    "source_index": src_idx,
                    "quote": _shorten_quote(line),
                })
            elif _OPEN_QUESTION_RE.search(line) or (
                line.endswith("?")
                and not re.search(r"\bkannst\s+du\b|\bkönntest\s+du\b", line, re.I)
            ):
                open_questions.append({
                    "id": f"Q-{len(open_questions) + 1:02d}",
                    "kind": "question",
                    "text": line,
                    "author": author,
                    "timestamp": ts,
                    "source_index": src_idx,
                    "quote": _shorten_quote(line),
                })

    summary_parts = [
        f"Ausgewertet wurden {len(messages)} Nachricht(en) von {len(participants)} Beteiligten im Kanal '{eff_channel}'."
    ]
    if decisions:
        summary_parts.append(
            f"Erfasste Beschlüsse ({len(decisions)}): "
            + "; ".join(d["text"] for d in decisions[:2])
            + ("." if not decisions[0]["text"].endswith(".") else "")
        )
    if action_items:
        owners = sorted({a["owner"] for a in action_items})
        summary_parts.append(
            f"Abgeleitete Aufgaben ({len(action_items)}), Zuständigkeiten: {', '.join(owners)}."
        )
    if blockers or open_questions:
        summary_parts.append(
            f"Offene Punkte: {len(open_questions)} Frage(n), {len(blockers)} Blocker."
        )

    chronology = [
        {
            "source_index": m["source_index"],
            "timestamp": m.get("timestamp"),
            "author": m["author"],
            "text": m["text"],
        }
        for m in messages
    ]

    return {
        "schema": "ocean.chat-mail-protocol.v1",
        "channel": eff_channel,
        "chat": chat_slug,
        "chat_label": chat_label,
        "timeframe": {
            "start": tf_start,
            "end": tf_end,
            "display": tf_display,
        },
        "participants": participants,
        "participant_count": len(participants),
        "message_count": len(messages),
        "summary": " ".join(summary_parts),
        "decisions": decisions,
        "action_items": action_items,
        "open_questions": open_questions,
        "blockers": blockers,
        "chronology": chronology,
    }


# ---------------------------------------------------------------------------
# 4. Pure-Stdlib %PDF-1.4 (WinAnsiEncoding + Umlaute) & Template Renderer
# ---------------------------------------------------------------------------

def _pdf_winansi_literal(text: str) -> str:
    """Encode Unicode text as a 7-bit-clean PDF literal string for /WinAnsiEncoding."""
    normalized = (
        text.replace("—", "-")
        .replace("–", "-")
        .replace("…", "...")
        .replace("•", "*")
        .replace("“", '"')
        .replace("”", '"')
        .replace("„", '"')
        .replace("’", "'")
    )
    raw_bytes = normalized.encode("cp1252", errors="replace")
    out: list[str] = []
    for byte in raw_bytes:
        if byte == 0x5C:  # backslash
            out.append("\\\\")
        elif byte == 0x28:  # (
            out.append("\\(")
        elif byte == 0x29:  # )
            out.append("\\)")
        elif 32 <= byte <= 126:
            out.append(chr(byte))
        else:
            # Octal escape for WinAnsi bytes >= 128 (ä=\344, ö=\366, ü=\374, ß=\337, €=\200)
            out.append(f"\\{byte:03o}")
    return "".join(out)


def render_winansi_pdf(title: str, body_text: str) -> bytes:
    """Render plain/structured UTF-8 text into a valid multi-page %PDF-1.4 with WinAnsiEncoding."""
    wrapped_lines: list[str] = []
    for raw_line in body_text.splitlines():
        if not raw_line.strip():
            wrapped_lines.append("")
            continue
        chunks = textwrap.wrap(
            raw_line,
            width=92,
            replace_whitespace=False,
            drop_whitespace=False,
        )
        wrapped_lines.extend(chunks or [""])

    if not wrapped_lines:
        wrapped_lines = [title]

    lines_per_page = 48
    pages_lines = [
        wrapped_lines[i : i + lines_per_page]
        for i in range(0, len(wrapped_lines), lines_per_page)
    ]

    objects: list[bytes] = []

    def add_object(payload: bytes) -> int:
        objects.append(payload)
        return len(objects)

    font_regular_id = add_object(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    )
    font_bold_id = add_object(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
    )
    pages_tree_id = add_object(b"")
    page_ids: list[int] = []

    total_pages = len(pages_lines)
    for page_idx, page_chunk in enumerate(pages_lines, start=1):
        ops = [
            "BT",
            "/F2 12 Tf",
            "48 796 Td",
            f"({_pdf_winansi_literal(title[:88])}) Tj",
            "/F1 9.5 Tf",
            "0 -18 Td",
            "14 TL",
        ]
        for idx, line in enumerate(page_chunk):
            esc = _pdf_winansi_literal(line)
            if idx == 0:
                ops.append(f"({esc}) Tj")
            else:
                ops.append(f"T* ({esc}) Tj")
        ops.extend([
            "0 -20 Td",
            f"({_pdf_winansi_literal(f'Seite {page_idx} / {total_pages}')}) Tj",
            "ET",
        ])
        stream = "\n".join(ops).encode("ascii")
        content_id = add_object(
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"\nendstream"
        )
        page_id = add_object(
            f"<< /Type /Page /Parent {pages_tree_id} 0 R "
            f"/MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>".encode("ascii")
        )
        page_ids.append(page_id)

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[pages_tree_id - 1] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")
    )
    info_id = add_object(
        f"<< /Title ({_pdf_winansi_literal(title)}) /Producer (chat-mail-protocol stdlib PDF) >>".encode("ascii")
    )
    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_tree_id} 0 R >>".encode("ascii"))

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: list[int] = [0]
    for obj_num, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{obj_num} 0 obj\n".encode("ascii"))
        pdf.extend(body)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R /Info {info_id} 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(pdf)


def list_available_templates(
    config: Mapping[str, Any] | None = None,
    *,
    skill_root: str | Path = SKILL_ROOT,
) -> dict[str, Any]:
    sroot = Path(skill_root)
    tpl_cfg = (config or {}).get("templates") if isinstance(config, dict) else None
    tpl_cfg = tpl_cfg if isinstance(tpl_cfg, dict) else {}

    dirs: list[Path] = []
    custom = tpl_cfg.get("custom_dir")
    if isinstance(custom, str) and custom.strip():
        cp = Path(custom)
        dirs.append(cp if cp.is_absolute() else (sroot / cp))
    rel = str(tpl_cfg.get("dir") or "./templates")
    rp = Path(rel)
    dirs.append(rp if rp.is_absolute() else (sroot / rp))
    if BUNDLED_TEMPLATES_DIR not in dirs:
        dirs.append(BUNDLED_TEMPLATES_DIR)

    found: dict[str, str] = {}
    for folder in dirs:
        if not folder.is_dir():
            continue
        for f in sorted(folder.iterdir()):
            if f.is_file() and f.suffix.lower() in {".html", ".md", ".txt"}:
                if f.name not in found:
                    found[f.name] = str(f)
    return {
        "search_dirs": [str(d) for d in dirs],
        "templates": found,
    }


def _load_template_file(
    template_stem: str,
    ext: str,
    config: Mapping[str, Any] | None,
    skill_root: Path,
) -> str:
    inventory = list_available_templates(config, skill_root=skill_root)["templates"]
    candidates = [f"{template_stem}.{ext}"]
    if ext == "md" and template_stem == "aufgabenliste":
        candidates.append("aufgabenliste.md")
    candidates.append(f"ergebnisprotokoll.{ext}")
    if ext == "txt" and template_stem == "kompakt-chat":
        candidates.insert(0, "kompakt-chat.txt")
    for cand in candidates:
        if cand in inventory:
            return Path(inventory[cand]).read_text(encoding="utf-8")
    raise FileNotFoundError(f"No template found for {template_stem!r} (.{ext})")


def _ordered_tasks(tasks: Sequence[dict[str, Any]], group_by: str) -> list[dict[str, Any]]:
    items = list(tasks)
    if group_by == "owner":
        items.sort(key=lambda t: (0 if t["owner"] != "offen" else 1, t["owner"].lower(), t["source_index"]))
    return items


def render_protocol(
    analysis: Mapping[str, Any],
    *,
    fmt: str = "md",
    template: str | None = None,
    config: Mapping[str, Any] | None = None,
    skill_root: str | Path = SKILL_ROOT,
    generated_at: str | None = None,
) -> bytes | str:
    """Render an analyzed conversation into html, pdf, md, txt, or json."""
    target_fmt = fmt.strip().lower()
    if target_fmt not in VALID_FORMATS:
        raise ValueError(f"Unsupported output format {fmt!r}; choose from {', '.join(VALID_FORMATS)}")

    cfg = dict(config or {})
    pres = cfg.get("presentation") if isinstance(cfg.get("presentation"), dict) else {}
    include_quotes = bool(pres.get("include_quotes", True))
    group_by = str(pres.get("group_tasks_by") or "owner")
    lang = str(pres.get("language") or "de")
    doc_types = cfg.get("doc_types") if isinstance(cfg.get("doc_types"), list) else ["ergebnisprotokoll"]
    include_chronology = "protokoll" in doc_types or template == "protokoll"

    tpl_stem = (template or str(cfg.get("template") or "ergebnisprotokoll")).strip()
    now_iso = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sroot = Path(skill_root)

    if target_fmt == "json":
        payload = {
            **dict(analysis),
            "generated_at": now_iso,
            "template": tpl_stem,
            "doc_types": doc_types,
        }
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    chat_label = str(analysis.get("chat_label") or "Konversationsprotokoll")
    title_prefix = "Aufgabenliste" if tpl_stem == "aufgabenliste" else "Ergebnisprotokoll"
    title = f"{title_prefix}: {chat_label}"
    channel = str(analysis.get("channel") or "generic")
    tf = analysis.get("timeframe") if isinstance(analysis.get("timeframe"), dict) else {}
    tf_display = str(tf.get("display") or "keine Zeitangabe")
    participants = list(analysis.get("participants") or [])
    participants_str = ", ".join(participants) if participants else "—"
    decisions = list(analysis.get("decisions") or [])
    tasks = _ordered_tasks(list(analysis.get("action_items") or []), group_by)
    open_q = list(analysis.get("open_questions") or [])
    blockers = list(analysis.get("blockers") or [])
    all_open = [*blockers, *open_q]
    chronology = list(analysis.get("chronology") or [])
    summary = str(analysis.get("summary") or "")
    footer = f"chat-mail-protocol v0.1.0 · Kanal: {channel} · Entwurf / Dry-Run-sicher"

    if target_fmt == "pdf":
        txt_basis = str(
            render_protocol(
                analysis,
                fmt="txt",
                template="ergebnisprotokoll" if tpl_stem == "kompakt-chat" else tpl_stem,
                config=cfg,
                skill_root=sroot,
                generated_at=now_iso,
            )
        )
        return render_winansi_pdf(title, txt_basis)

    if target_fmt == "html":
        tpl = _load_template_file(tpl_stem, "html", cfg, sroot)
        if decisions:
            dec_blocks = []
            for d in decisions:
                q_html = (
                    f'<div class="quote">Quelle #{d["source_index"]} ({html.escape(d["author"])}): '
                    f'„{html.escape(d["quote"])}“</div>'
                    if include_quotes
                    else ""
                )
                dec_blocks.append(
                    f'<div class="decision-card"><strong>{html.escape(d["id"])}:</strong> '
                    f'{html.escape(d["text"])}{q_html}</div>'
                )
            decisions_html = "\n".join(dec_blocks)
        else:
            decisions_html = "<p><em>Keine expliziten Beschlüsse im Verlauf markiert.</em></p>"

        if tasks:
            rows_html = [
                "<table><thead><tr><th>ID</th><th>Aufgabe</th><th>Verantwortlich</th>"
                "<th>Frist</th><th>Quelle</th></tr></thead><tbody>"
            ]
            for t in tasks:
                due_str = html.escape(str(t["due"])) if t.get("due") else "—"
                src_str = f"#{t['source_index']} ({html.escape(t['author'])})"
                rows_html.append(
                    f"<tr><td>{html.escape(t['id'])}</td><td>{html.escape(t['task'])}</td>"
                    f"<td>{html.escape(t['owner'])}</td><td>{due_str}</td><td>{src_str}</td></tr>"
                )
            rows_html.append("</tbody></table>")
            tasks_html = "\n".join(rows_html)
        else:
            tasks_html = "<p><em>Keine offenen Aufgaben erkannt.</em></p>"

        if all_open:
            op_blocks = []
            for item in all_open:
                badge = "BLOCKER" if item["kind"] == "blocker" else "FRAGE"
                op_blocks.append(
                    f'<div class="open-card"><strong>[{badge} {html.escape(item["id"])}]</strong> '
                    f'{html.escape(item["text"])} '
                    f'<span class="quote">(#{item["source_index"]}, {html.escape(item["author"])})</span></div>'
                )
            open_html = "\n".join(op_blocks)
        else:
            open_html = "<p><em>Keine offenen Fragen oder Blocker.</em></p>"

        if include_chronology and chronology:
            ch_rows = ["<section><h2>4. Chronologischer Verlauf</h2><table><thead><tr><th>#</th><th>Zeit</th><th>Person</th><th>Nachricht</th></tr></thead><tbody>"]
            for c in chronology:
                ch_rows.append(
                    f"<tr><td>{c['source_index']}</td><td>{html.escape(str(c.get('timestamp') or '—'))}</td>"
                    f"<td>{html.escape(c['author'])}</td><td>{html.escape(c['text'])}</td></tr>"
                )
            ch_rows.append("</tbody></table></section>")
            chron_html = "\n".join(ch_rows)
        else:
            chron_html = ""

        return (
            tpl.replace("{{lang}}", html.escape(lang))
            .replace("{{title}}", html.escape(title))
            .replace("{{channel}}", html.escape(channel))
            .replace("{{chat_label}}", html.escape(chat_label))
            .replace("{{timeframe}}", html.escape(tf_display))
            .replace("{{participant_count}}", str(len(participants)))
            .replace("{{participants}}", html.escape(participants_str))
            .replace("{{message_count}}", str(analysis.get("message_count", 0)))
            .replace("{{generated_at}}", html.escape(now_iso))
            .replace("{{summary_html}}", html.escape(summary))
            .replace("{{decision_count}}", str(len(decisions)))
            .replace("{{decisions_html}}", decisions_html)
            .replace("{{task_count}}", str(len(tasks)))
            .replace("{{tasks_html}}", tasks_html)
            .replace("{{open_count}}", str(len(all_open)))
            .replace("{{open_points_html}}", open_html)
            .replace("{{chronology_section_html}}", chron_html)
            .replace("{{footer}}", html.escape(footer))
        )

    if target_fmt == "md":
        tpl = _load_template_file(tpl_stem, "md", cfg, sroot)
        if decisions:
            dec_lines = []
            for d in decisions:
                cite = f' *(Quelle #{d["source_index"]}, {d["author"]}: „{d["quote"]}“)*' if include_quotes else f' *(Quelle #{d["source_index"]})*'
                dec_lines.append(f"- **{d['id']}:** {d['text']}{cite}")
            decisions_md = "\n".join(dec_lines)
        else:
            decisions_md = "_Keine expliziten Beschlüsse markiert._"

        if tasks:
            task_lines = [
                "| ID | Aufgabe | Verantwortlich | Frist | Quelle |",
                "|---|---|---|---|---|",
            ]
            for t in tasks:
                cell_task = str(t["task"]).replace("|", "\\|")
                cell_owner = str(t["owner"]).replace("|", "\\|")
                cell_due = str(t["due"]) if t.get("due") else "—"
                task_lines.append(
                    f"| {t['id']} | {cell_task} | {cell_owner} | {cell_due} | #{t['source_index']} ({t['author']}) |"
                )
            tasks_md = "\n".join(task_lines)
        else:
            tasks_md = "_Keine offenen Aufgaben erkannt._"

        if all_open:
            open_md = "\n".join(
                f"- **[{'BLOCKER' if o['kind'] == 'blocker' else 'FRAGE'} {o['id']}]** {o['text']} *(Quelle #{o['source_index']}, {o['author']})*"
                for o in all_open
            )
        else:
            open_md = "_Keine offenen Fragen oder Blocker._"

        if include_chronology and chronology:
            chron_md = "\n## 4. Chronologischer Verlauf\n\n" + "\n".join(
                f"- **#{c['source_index']}** [{c.get('timestamp') or '—'}] **{c['author']}:** {c['text']}"
                for c in chronology
            ) + "\n"
        else:
            chron_md = ""

        return (
            tpl.replace("{{title}}", title)
            .replace("{{channel}}", channel)
            .replace("{{chat_label}}", chat_label)
            .replace("{{timeframe}}", tf_display)
            .replace("{{participant_count}}", str(len(participants)))
            .replace("{{participants}}", participants_str)
            .replace("{{message_count}}", str(analysis.get("message_count", 0)))
            .replace("{{generated_at}}", now_iso)
            .replace("{{summary_md}}", summary)
            .replace("{{decision_count}}", str(len(decisions)))
            .replace("{{decisions_md}}", decisions_md)
            .replace("{{task_count}}", str(len(tasks)))
            .replace("{{tasks_md}}", tasks_md)
            .replace("{{open_count}}", str(len(all_open)))
            .replace("{{open_points_md}}", open_md)
            .replace("{{chronology_section_md}}", chron_md)
            .replace("{{footer}}", footer)
        )

    # Plaintext (ergebnisprotokoll.txt or kompakt-chat.txt)
    tpl = _load_template_file(tpl_stem, "txt", cfg, sroot)
    dec_txt = (
        "\n".join(f"  * [{d['id']}] {d['text']} (#{d['source_index']}, {d['author']})" for d in decisions)
        if decisions
        else "  (keine Beschluesse markiert)"
    )
    tasks_txt = (
        "\n".join(
            f"  * [{t['id']}] {t['owner']}: {t['task']}"
            + (f" (Frist: {t['due']})" if t.get("due") else "")
            + f" [#{t['source_index']}]"
            for t in tasks
        )
        if tasks
        else "  (keine offenen Aufgaben)"
    )
    open_txt = (
        "\n".join(
            f"  * [{'BLOCKER' if o['kind'] == 'blocker' else 'FRAGE'} {o['id']}] {o['text']} [#{o['source_index']}]"
            for o in all_open
        )
        if all_open
        else "  (keine offenen Punkte)"
    )
    if include_chronology and chronology:
        chron_txt = "\n4. CHRONOLOGISCHER VERLAUF\n--------------------------\n" + "\n".join(
            f"  #{c['source_index']} [{c.get('timestamp') or '-'}] {c['author']}: {c['text']}"
            for c in chronology
        ) + "\n"
    else:
        chron_txt = ""

    return (
        tpl.replace("{{title}}", title)
        .replace("{{channel}}", channel)
        .replace("{{chat_label}}", chat_label)
        .replace("{{timeframe}}", tf_display)
        .replace("{{participant_count}}", str(len(participants)))
        .replace("{{participants}}", participants_str)
        .replace("{{message_count}}", str(analysis.get("message_count", 0)))
        .replace("{{generated_at}}", now_iso)
        .replace("{{summary_txt}}", summary)
        .replace("{{summary_compact}}", summary)
        .replace("{{decision_count}}", str(len(decisions)))
        .replace("{{decisions_txt}}", dec_txt)
        .replace("{{decisions_compact}}", dec_txt)
        .replace("{{task_count}}", str(len(tasks)))
        .replace("{{tasks_txt}}", tasks_txt)
        .replace("{{tasks_compact}}", tasks_txt)
        .replace("{{open_count}}", str(len(all_open)))
        .replace("{{open_points_txt}}", open_txt)
        .replace("{{open_points_compact}}", open_txt)
        .replace("{{chronology_section_txt}}", chron_txt)
        .replace("{{footer}}", footer)
    )


# ---------------------------------------------------------------------------
# 5. Safe Draft / Dry-Run Delivery & reply_in_chat Planner
# ---------------------------------------------------------------------------

def build_delivery_plan(
    analysis: Mapping[str, Any],
    config: Mapping[str, Any],
    *,
    written_files: Mapping[str, str] | None = None,
    skill_root: str | Path = SKILL_ROOT,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Compute a safe, non-sending distribution & reply_in_chat plan."""
    deliv = config.get("delivery") if isinstance(config.get("delivery"), dict) else {}
    enabled = bool(deliv.get("enabled", False))
    dry_run = bool(deliv.get("dry_run", True))
    mode = str(deliv.get("mode") or "draft")
    reply_in_chat = bool(deliv.get("reply_in_chat", False))
    reply_fmt = str(deliv.get("reply_format") or "txt").lower()
    if reply_fmt not in {"txt", "md"}:
        reply_fmt = "txt"
    reply_tpl = str(deliv.get("reply_template") or "kompakt-chat")

    target_channel = deliv.get("target_channel") or analysis.get("channel")
    target_chat = deliv.get("target_chat") or analysis.get("chat")
    handoff_target = deliv.get("handoff_tasks_to")

    reply_payload: str | None = None
    if reply_in_chat:
        rendered_reply = render_protocol(
            analysis,
            fmt=reply_fmt,
            template=reply_tpl,
            config=config,
            skill_root=skill_root,
            generated_at=generated_at,
        )
        reply_payload = rendered_reply.decode("utf-8") if isinstance(rendered_reply, bytes) else rendered_reply

    tasks = list(analysis.get("action_items") or [])
    handoff_payload = (
        {
            "target": str(handoff_target),
            "count": len(tasks),
            "items": [
                {
                    "id": t["id"],
                    "title": t["task"],
                    "owner": t["owner"],
                    "due": t["due"],
                    "source": f"{analysis.get('channel')}:{analysis.get('chat')}#{t['source_index']}",
                }
                for t in tasks
            ],
        }
        if handoff_target
        else None
    )

    return {
        "enabled": enabled,
        "dry_run": dry_run,
        "mode": mode,
        "sent_externally": False,
        "target_channel": target_channel,
        "target_chat": target_chat,
        "reply_in_chat": {
            "enabled": reply_in_chat,
            "format": reply_fmt,
            "template": reply_tpl,
            "payload": reply_payload,
        },
        "exports": dict(written_files or {}),
        "task_handoff": handoff_payload,
    }


def process_conversation(
    raw_text: str,
    *,
    skill_root: str | Path = SKILL_ROOT,
    config_dir: str | Path | None = None,
    channel: str | None = None,
    chat: str | None = None,
    cli_overrides: Mapping[str, Any] | None = None,
    out_dir: str | Path | None = None,
    repair_config: bool = False,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """End-to-end pipeline: parse -> load channel/chat config -> extract -> render -> plan delivery."""
    # Pre-detect channel when 'auto' or None so <channel>.json profile is picked up automatically!
    initial_parse = parse_messages(raw_text, channel_hint=channel, anonymize_participants=False)
    resolved_channel = (
        slugify_identifier(channel)
        if channel and channel != "auto"
        else str(initial_parse["channel"])
    )
    resolved_chat = chat or initial_parse.get("subject")

    cfg_bundle = load_effective_channel_config(
        skill_root=skill_root,
        config_dir=config_dir,
        channel=resolved_channel,
        chat=resolved_chat,
        cli_overrides=cli_overrides,
        repair_config=repair_config,
    )
    eff_cfg = cfg_bundle["config"]
    pres = eff_cfg.get("presentation") if isinstance(eff_cfg.get("presentation"), dict) else {}
    anonymize = bool(pres.get("anonymize_participants", False))

    analysis = analyze_conversation(
        initial_parse,
        channel=resolved_channel,
        chat=resolved_chat,
        anonymize_participants=anonymize,
    )

    formats = eff_cfg.get("formats") if isinstance(eff_cfg.get("formats"), list) else ["md"]
    tpl_name = str(eff_cfg.get("template") or "ergebnisprotokoll")
    now_iso = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    rendered_outputs: dict[str, str] = {}
    written_files: dict[str, str] = {}
    export_base = (
        Path(out_dir)
        if out_dir is not None
        else (Path(eff_cfg["delivery"]["export_dir"]) if eff_cfg.get("delivery", {}).get("export_dir") else None)
    )

    stem = f"{analysis['channel']}_{analysis['chat']}"
    for fmt in formats:
        fmt_clean = str(fmt).strip().lower()
        content = render_protocol(
            analysis,
            fmt=fmt_clean,
            template=tpl_name,
            config=eff_cfg,
            skill_root=skill_root,
            generated_at=now_iso,
        )
        if export_base is not None:
            export_base.mkdir(parents=True, exist_ok=True)
            out_file = export_base / f"{stem}.{fmt_clean}"
            if isinstance(content, bytes):
                out_file.write_bytes(content)
            else:
                out_file.write_text(content, encoding="utf-8", newline="\n")
            written_files[fmt_clean] = str(out_file)
        rendered_outputs[fmt_clean] = (
            f"<binary pdf: {len(content)} bytes>" if isinstance(content, bytes) else content
        )

    delivery_plan = build_delivery_plan(
        analysis,
        eff_cfg,
        written_files=written_files,
        skill_root=skill_root,
        generated_at=now_iso,
    )

    return {
        "ok": True,
        "analysis": analysis,
        "config_resolution": {
            "loaded_layers": cfg_bundle["loaded_layers"],
            "skipped_layers": cfg_bundle["skipped_layers"],
            "warnings": cfg_bundle["warnings"],
            "healed": cfg_bundle["healed"],
            "effective_doc_types": eff_cfg.get("doc_types"),
            "effective_formats": formats,
            "effective_template": tpl_name,
        },
        "outputs": rendered_outputs,
        "written_files": written_files,
        "delivery_plan": delivery_plan,
    }


# ---------------------------------------------------------------------------
# 6. CLI Interface
# ---------------------------------------------------------------------------

def _split_csv(raw: str | None, valid: Sequence[str], flag_name: str) -> list[str] | None:
    if raw is None:
        return None
    items = [part.strip().lower() for part in raw.split(",") if part.strip()]
    if not items:
        raise ValueError(f"{flag_name} must not be empty")
    for item in items:
        if item not in valid:
            raise ValueError(f"Unsupported value {item!r} in {flag_name}; allowed: {', '.join(valid)}")
    return items


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="protocol_core",
        description="Turn chat exports and email threads into structured protocols, summaries, and task lists.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_proc = sub.add_parser("process", help="Parse, analyze, and render a chat or email transcript")
    p_proc.add_argument("--input", required=True, dest="input_path", help="Path to chat/email file ('-' for stdin)")
    p_proc.add_argument("--channel", default="auto", choices=VALID_CHANNELS, help="Source channel (default: auto)")
    p_proc.add_argument("--chat", default=None, help="Chat/thread slug or name (for <channel>.<chat>.json)")
    p_proc.add_argument("--config-dir", default=None, help="Directory holding config.json / channel profiles")
    p_proc.add_argument("--doc-types", default=None, help="Comma-separated: zusammenfassung,protokoll,ergebnisprotokoll,aufgabenliste")
    p_proc.add_argument("--formats", default=None, help="Comma-separated: html,pdf,md,txt,json")
    p_proc.add_argument("--template", default=None, help="Template stem (ergebnisprotokoll, kompakt-chat, aufgabenliste)")
    p_proc.add_argument("--anonymize", action="store_true", help="Anonymize participant names to Person A, Person B, ...")
    p_proc.add_argument("--out-dir", default=None, help="Directory to write rendered files")
    p_proc.add_argument("--repair-config", action="store_true", help="Backup corrupt configs (.corrupt.<ts>.bak) and restore")
    p_proc.add_argument("--json", action="store_true", help="Emit full JSON bundle")

    p_cfg = sub.add_parser("show-config", help="Inspect effective merged config and self-healing diagnostics")
    p_cfg.add_argument("--channel", default=None, help="Channel name (e.g. whatsapp, slack, email)")
    p_cfg.add_argument("--chat", default=None, help="Chat slug (e.g. projekt-alpha)")
    p_cfg.add_argument("--config-dir", default=None, help="Directory holding local config/profile overrides")
    p_cfg.add_argument("--repair-config", action="store_true", help="Self-heal corrupt JSON files with backup")
    p_cfg.add_argument("--json", action="store_true", help="Emit JSON output")

    p_tpl = sub.add_parser("list-templates", help="List available built-in and custom templates")
    p_tpl.add_argument("--config-dir", default=None, help="Optional config directory")
    p_tpl.add_argument("--json", action="store_true", help="Emit JSON output")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        if args.command == "show-config":
            res = load_effective_channel_config(
                config_dir=args.config_dir,
                channel=args.channel,
                chat=args.chat,
                repair_config=args.repair_config,
            )
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(
                    f"OK={res['ok']} LAYERS={len(res['loaded_layers'])} "
                    f"WARNINGS={len(res['warnings'])} HEALED={len(res['healed'])}"
                )
            return 0

        if args.command == "list-templates":
            cfg_res = load_effective_channel_config(config_dir=args.config_dir)
            inv = list_available_templates(cfg_res["config"])
            if args.json:
                print(json.dumps(inv, ensure_ascii=False, indent=2))
            else:
                for name, full_path in inv["templates"].items():
                    print(f"{name}\t{full_path}")
            return 0

        if args.command == "process":
            raw_text = (
                sys.stdin.read()
                if args.input_path == "-"
                else Path(args.input_path).read_text(encoding="utf-8-sig")
            )
            overrides: dict[str, Any] = {}
            doc_types = _split_csv(args.doc_types, VALID_DOC_TYPES, "--doc-types")
            if doc_types is not None:
                overrides["doc_types"] = doc_types
            formats = _split_csv(args.formats, VALID_FORMATS, "--formats")
            if formats is not None:
                overrides["formats"] = formats
            if args.template:
                overrides["template"] = args.template
            if args.anonymize:
                overrides["presentation"] = {"anonymize_participants": True}

            result = process_conversation(
                raw_text,
                config_dir=args.config_dir,
                channel=args.channel,
                chat=args.chat,
                cli_overrides=overrides or None,
                out_dir=args.out_dir,
                repair_config=args.repair_config,
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                first_fmt = result["config_resolution"]["effective_formats"][0]
                print(result["outputs"][first_fmt])
            return 0
    except (ValueError, OSError, FileNotFoundError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
