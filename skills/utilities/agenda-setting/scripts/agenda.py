#!/usr/bin/env python3
"""Shared time-limited agenda and pointers to existing plans. No task execution."""

from __future__ import annotations

import argparse
import calendar
import copy
import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import date, datetime, time, timezone
from pathlib import Path

VALID_OWNERS = ("lukas", "team", "shared")
VALID_SUMMARY_FORMATS = ("markdown", "text", "json")
_TIMEFRAME_ATOM = re.compile(r"^(\d{4})(?:-(?:(0[1-9]|1[0-2])|Q([1-4])|H([12])))?$")
_CATEGORY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,49}$")


def _parse_timeframe_atom(atom: str) -> tuple[date, date]:
    match = _TIMEFRAME_ATOM.fullmatch(atom)
    if not match:
        raise ValueError(f"Invalid timeframe: {atom!r}")
    year = int(match.group(1))
    if not 1900 <= year <= 2999:
        raise ValueError(f"Timeframe year out of range: {atom!r}")
    if match.group(2):
        month = int(match.group(2))
        return date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])
    if match.group(3):
        quarter = int(match.group(3))
        m1 = 3 * (quarter - 1) + 1
        m2 = 3 * quarter
        return date(year, m1, 1), date(year, m2, calendar.monthrange(year, m2)[1])
    if match.group(4):
        half = int(match.group(4))
        m1, m2 = (1, 6) if half == 1 else (7, 12)
        return date(year, m1, 1), date(year, m2, calendar.monthrange(year, m2)[1])
    return date(year, 1, 1), date(year, 12, 31)


def validate_timeframe(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Timeframe must be a string")
    text = value.strip()
    if not text or len(text) > 32:
        raise ValueError("Timeframe must contain 1..32 characters")
    if text == "ongoing":
        return text
    if ".." in text:
        parts = text.split("..")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(f"Invalid timeframe range: {text!r}")
        s1, e1 = _parse_timeframe_atom(parts[0])
        s2, e2 = _parse_timeframe_atom(parts[1])
        if s1 > s2 or e1 > e2:
            raise ValueError(f"Reversed timeframe range: {text!r}")
        return text
    if text.endswith("+"):
        _parse_timeframe_atom(text[:-1])
        return text
    _parse_timeframe_atom(text)
    return text


def validate_owner(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Owner must be a string")
    text = value.strip()
    if text not in VALID_OWNERS:
        raise ValueError(f"Owner must be one of: {', '.join(VALID_OWNERS)}")
    return text


def validate_category(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Category must be a string")
    text = value.strip().lower()
    if not _CATEGORY_RE.fullmatch(text):
        raise ValueError("Category must be 1..50 tag characters ([a-z0-9][a-z0-9_-]*)")
    return text


def _timeframe_bounds(text: str) -> tuple[date | None, date | None, bool, bool]:
    if text == "ongoing":
        return None, None, True, True
    if ".." in text:
        left, right = text.split("..", 1)
        s1, _ = _parse_timeframe_atom(left)
        _, e2 = _parse_timeframe_atom(right)
        return s1, e2, False, False
    if text.endswith("+"):
        s1, e1 = _parse_timeframe_atom(text[:-1])
        return s1, e1, True, False
    s1, e1 = _parse_timeframe_atom(text)
    return s1, e1, False, False


def _timeframe_sort_key(tf: str | None) -> tuple:
    if not tf:
        return (2, date.max, date.max, 0, "")
    if tf == "ongoing":
        return (1, date.max, date.max, 1, "ongoing")
    s1, anchor_end, is_open, _ = _timeframe_bounds(tf)
    return (0, anchor_end, s1, 1 if is_open else 0, tf)


def _timeframe_matches(item_tf: str | None, filter_tf: str) -> bool:
    if not item_tf:
        return False
    if item_tf == filter_tf:
        return True
    if item_tf == "ongoing" or filter_tf == "ongoing":
        return False
    i_start, i_anchor_end, i_open, _ = _timeframe_bounds(item_tf)
    f_start, f_anchor_end, f_open, _ = _timeframe_bounds(filter_tf)
    assert i_start is not None and f_start is not None
    assert i_anchor_end is not None and f_anchor_end is not None
    if f_open:
        return i_start >= f_start
    if i_open:
        return f_start <= i_start and i_anchor_end <= f_anchor_end
    return f_start <= i_start and i_anchor_end <= f_anchor_end


def now() -> datetime:
    return datetime.now(timezone.utc)


def deadline(value: str) -> datetime:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return datetime.combine(date.fromisoformat(value), time.max, timezone.utc)
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Deadline needs a timezone, or YYYY-MM-DD (inclusive UTC day)")
    return result.astimezone(timezone.utc)


def profile(path: Path | None = None) -> dict:
    path = path or Path(os.environ.get("AGENT_AGENDA_PROFILE", Path.home() / ".config/agent-agenda/profile.json"))
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != "agent-agenda-profile.v1":
        raise ValueError("Invalid agenda profile")
    return data


def state_root(override: Path | None = None, settings: dict | None = None) -> Path:
    settings = settings if settings is not None else profile()
    return Path(override or settings.get("state_root") or Path.home() / ".local/state/agent-agenda").expanduser()


def read(root: Path) -> dict:
    path = root / "agenda.json"
    if not path.exists():
        return {
            "schema": "agent-agenda.v1",
            "revision": 0,
            "agenda_id": None,
            "name": "Agenda",
            "enabled": False,
            "deadline": None,
            "items": [],
        }
    if path.stat().st_size > 2_000_000:
        raise ValueError("Agenda exceeds size limit")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(data, dict)
        or data.get("schema") != "agent-agenda.v1"
        or type(data.get("revision")) is not int
        or data["revision"] < 0
        or type(data.get("enabled")) is not bool
        or not isinstance(data.get("items"), list)
        or len(data["items"]) > 100
        or not isinstance(data.get("name"), str)
        or not 1 <= len(data["name"]) <= 200
    ):
        raise ValueError("Invalid agenda state")
    ids = set()
    for item in data["items"]:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("id"), str)
            or not re.fullmatch(r"A[1-9][0-9]{0,2}", item["id"])
            or item["id"] in ids
            or item.get("status") not in {"pending", "done"}
            or not isinstance(item.get("text"), str)
            or not 1 <= len(item["text"]) <= 2000
            or type(item.get("weight")) is not int
            or not 1 <= item["weight"] <= 100
            or not isinstance(item.get("plans"), list)
        ):
            raise ValueError("Invalid agenda item")
        ids.add(item["id"])
        if "timeframe" in item and item["timeframe"] is not None:
            validate_timeframe(item["timeframe"])
        if "owner" in item and item["owner"] is not None:
            validate_owner(item["owner"])
        if "category" in item and item["category"] is not None:
            if not isinstance(item["category"], str) or not _CATEGORY_RE.fullmatch(item["category"]):
                raise ValueError("Invalid agenda item category")
        for link in item["plans"]:
            if (
                not isinstance(link, dict)
                or not isinstance(link.get("path"), str)
                or not isinstance(link.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", link["sha256"])
            ):
                raise ValueError("Invalid plan pointer")
    if data.get("deadline"):
        deadline(data["deadline"])
    return data


def view(data: dict, at: datetime | None = None) -> dict:
    result = copy.deepcopy(data)
    result["expired"] = bool(data.get("deadline") and deadline(data["deadline"]) <= (at or now()))
    result["active"] = bool(data["enabled"] and data.get("deadline") and not result["expired"])
    result["items"] = sorted(result["items"], key=lambda item: -item["weight"])
    return result


def atomic_write(path: Path, data: dict) -> None:
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=".agenda-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if Path(name).exists():
            Path(name).unlink()


def mutate(root: Path, expected: int, change) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    lock = root / "agenda.lock"
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try:
        current = read(root)
        if current["revision"] != expected:
            raise ValueError("Revision conflict: reread the shared agenda")
        updated = copy.deepcopy(current)
        change(updated)
        updated["revision"] = expected + 1
        updated["updated_at"] = now().isoformat()
        history = root / "history"
        history.mkdir(exist_ok=True)
        atomic_write(history / f"{expected:08d}.json", current)
        atomic_write(root / "agenda.json", updated)
        return view(read(root))
    finally:
        lock.unlink()


def select(data: dict, item_id: str) -> dict:
    matches = [item for item in data["items"] if item["id"] == item_id]
    if len(matches) != 1:
        raise ValueError("Unknown or ambiguous item ID")
    return matches[0]


def plans(data: dict, item_id: str = "") -> list[dict]:
    result = []
    items = [select(data, item_id)] if item_id else data["items"]
    for item in items:
        for link in item.get("plans", []):
            record = dict(link, item_id=item["id"])
            path = Path(link["path"]).expanduser()
            record["available"] = path.is_file()
            if path.is_file() and path.stat().st_size <= 10_000_000:
                record["current_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                record["changed"] = record["current_sha256"] != link["sha256"]
            result.append(record)
    return result


def summary(
    data: dict,
    timeframe: str | None = None,
    owner: str | None = None,
    category: str | None = None,
) -> dict:
    current = view(data)
    tf_filter = validate_timeframe(timeframe) if timeframe is not None else None
    owner_filter = validate_owner(owner) if owner is not None else None
    category_filter = validate_category(category) if category is not None else None

    matched = []
    for item in current["items"]:
        if tf_filter is not None and not _timeframe_matches(item.get("timeframe"), tf_filter):
            continue
        if owner_filter is not None and item.get("owner") != owner_filter:
            continue
        if category_filter is not None and item.get("category") != category_filter:
            continue
        matched.append(item)

    grouped: dict[str | None, list[dict]] = {}
    for item in matched:
        key = item.get("timeframe") or None
        grouped.setdefault(key, []).append(item)

    groups = []
    for tf_key in sorted(grouped, key=_timeframe_sort_key):
        items_sorted = sorted(grouped[tf_key], key=lambda item: (-item["weight"], int(item["id"][1:])))
        groups.append({"timeframe": tf_key, "items": items_sorted})

    return {
        "revision": current["revision"],
        "agenda_id": current["agenda_id"],
        "name": current["name"],
        "enabled": current["enabled"],
        "expired": current["expired"],
        "active": current["active"],
        "deadline": current["deadline"],
        "filters": {
            "timeframe": tf_filter,
            "owner": owner_filter,
            "category": category_filter,
        },
        "total_items": len(current["items"]),
        "matched_items": len(matched),
        "pending_items": sum(1 for item in matched if item["status"] == "pending"),
        "done_items": sum(1 for item in matched if item["status"] == "done"),
        "groups": groups,
    }


def render_summary(data: dict, fmt: str = "markdown") -> str:
    if fmt not in VALID_SUMMARY_FORMATS:
        raise ValueError(f"Format must be one of: {', '.join(VALID_SUMMARY_FORMATS)}")
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    status_label = "aktiv" if data["active"] else ("abgelaufen" if data["expired"] else "inaktiv")
    deadline_label = data["deadline"] or "keine"
    meta_line = (
        f"Status: {status_label} | Revision: {data['revision']} | Frist: {deadline_label} | "
        f"Punkte: {data['matched_items']}/{data['total_items']} "
        f"(offen: {data['pending_items']}, erledigt: {data['done_items']})"
    )
    active_filters = [f"{k}={v}" for k, v in data["filters"].items() if v is not None]

    if fmt == "markdown":
        lines = [f"# {data['name']}", "", meta_line]
        if active_filters:
            lines.append(f"Filter: {', '.join(active_filters)}")
        if not data["groups"]:
            lines.extend(["", "_Keine passenden Punkte._"])
        for group in data["groups"]:
            heading = group["timeframe"] or "Ohne Zeitraum"
            lines.extend(["", f"## {heading}"])
            for item in group["items"]:
                mark = "x" if item["status"] == "done" else " "
                meta = [f"w={item['weight']}"]
                if item.get("owner"):
                    meta.append(item["owner"])
                if item.get("category"):
                    meta.append(item["category"])
                if item.get("plans"):
                    meta.append(f"Pläne: {len(item['plans'])}")
                lines.append(f"- [{mark}] **{item['id']}** ({' | '.join(meta)}) {item['text']}")
        return "\n".join(lines)

    lines = [data["name"], meta_line]
    if active_filters:
        lines.append(f"Filter: {', '.join(active_filters)}")
    if not data["groups"]:
        lines.extend(["", "Keine passenden Punkte."])
    for group in data["groups"]:
        heading = group["timeframe"] or "Ohne Zeitraum"
        lines.extend(["", f"[{heading}]"])
        for item in group["items"]:
            mark = "x" if item["status"] == "done" else " "
            meta = [f"w={item['weight']}"]
            if item.get("owner"):
                meta.append(item["owner"])
            if item.get("category"):
                meta.append(item["category"])
            if item.get("plans"):
                meta.append(f"Pläne: {len(item['plans'])}")
            lines.append(f"  [{mark}] {item['id']} ({' | '.join(meta)}) {item['text']}")
    return "\n".join(lines)


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        nargs="?",
        default="show",
        choices=[
            "show",
            "set",
            "add",
            "update",
            "summary",
            "name",
            "on",
            "off",
            "deadline",
            "done",
            "pending",
            "prios",
            "plans",
        ],
    )
    parser.add_argument("text", nargs="?", default="")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--if-revision", type=int)
    parser.add_argument("--note", default="")
    parser.add_argument("--weight", type=int, default=None)
    parser.add_argument("--text", dest="new_text", default=None)
    parser.add_argument("--timeframe", default=None)
    parser.add_argument("--owner", default=None)
    parser.add_argument("--category", default=None)
    parser.add_argument("--format", dest="output_format", default="markdown")
    parser.add_argument("--path", type=Path)
    parser.add_argument("--kind", choices=["plan", "plan-register", "policy-register"], default="plan")
    parser.add_argument("--planner", default="")
    args = parser.parse_args(argv)
    try:
        root = state_root(args.root, profile(args.profile))
        if args.action == "show":
            result = view(read(root))
        elif args.action == "summary":
            if args.text.strip():
                raise ValueError("summary takes filter flags (--timeframe, --owner, --category, --format)")
            summary_data = summary(
                read(root),
                timeframe=args.timeframe,
                owner=args.owner,
                category=args.category,
            )
            print(render_summary(summary_data, fmt=args.output_format))
            return 0
        elif args.action == "plans" and args.path is None:
            current = read(root)
            result = {"revision": current["revision"], "plans": plans(current, args.text)}
        elif args.action in {"done", "pending", "prios"} and not args.text:
            current = view(read(root))
            result = {
                "revision": current["revision"],
                "items": [i for i in current["items"] if args.action == "prios" or i["status"] == args.action],
            }
        else:
            if args.if_revision is None:
                raise ValueError("Read first, then supply --if-revision (0 for a new agenda)")
            # Read plan bytes before taking the state write lock; store pointers only.
            link = None
            if args.action == "plans":
                path = args.path.expanduser().resolve(strict=True)
                if not path.is_file() or path.stat().st_size > 10_000_000:
                    raise ValueError("Select a plan file at most 10 MB")
                link = {
                    "path": str(path),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "kind": args.kind,
                    "planner": args.planner,
                }

            validated_timeframe = validate_timeframe(args.timeframe) if args.timeframe is not None else None
            validated_owner = validate_owner(args.owner) if args.owner is not None else None
            validated_category = validate_category(args.category) if args.category is not None else None
            if args.weight is not None and not 1 <= args.weight <= 100:
                raise ValueError("Weight must be 1..100")

            def change(data):
                if args.action == "set":
                    entries = [s.strip() for s in re.split(r"[;\n]+", args.text) if s.strip()]
                    if not entries or len(entries) > 100 or any(len(s) > 2000 for s in entries):
                        raise ValueError("Supply 1..100 items, at most 2000 characters each")
                    data.update(
                        agenda_id=uuid.uuid4().hex,
                        enabled=False,
                        deadline=None,
                        items=[
                            {"id": f"A{i + 1}", "text": s, "weight": 100 - i, "status": "pending", "plans": []}
                            for i, s in enumerate(entries)
                        ],
                    )
                elif args.action == "add":
                    raw_text = args.text if args.text.strip() else (args.new_text or "")
                    text = raw_text.strip()
                    if not text or len(text) > 2000:
                        raise ValueError("Item text must contain 1..2000 characters")
                    weight = 50 if args.weight is None else args.weight
                    if len(data["items"]) >= 100 or not 1 <= weight <= 100:
                        raise ValueError("At most 100 items; weight must be 1..100")
                    number = max((int(i["id"][1:]) for i in data["items"]), default=0) + 1
                    if number > 999:
                        raise ValueError("No free item ID left")
                    new_item = {"id": f"A{number}", "text": text, "weight": weight, "status": "pending", "plans": []}
                    if validated_timeframe is not None:
                        new_item["timeframe"] = validated_timeframe
                    if validated_owner is not None:
                        new_item["owner"] = validated_owner
                    if validated_category is not None:
                        new_item["category"] = validated_category
                    data["items"].append(new_item)
                elif args.action == "update":
                    item_id = args.text.strip()
                    if not item_id:
                        raise ValueError("Item ID required for update")
                    if (
                        args.new_text is None
                        and validated_timeframe is None
                        and validated_owner is None
                        and validated_category is None
                        and args.weight is None
                    ):
                        raise ValueError(
                            "Supply at least one field to update (--text, --timeframe, --owner, --category, --weight)"
                        )
                    item = select(data, item_id)
                    if args.new_text is not None:
                        updated_text = args.new_text.strip()
                        if not updated_text or len(updated_text) > 2000:
                            raise ValueError("Item text must contain 1..2000 characters")
                        item["text"] = updated_text
                    if args.weight is not None:
                        item["weight"] = args.weight
                    if validated_timeframe is not None:
                        item["timeframe"] = validated_timeframe
                    if validated_owner is not None:
                        item["owner"] = validated_owner
                    if validated_category is not None:
                        item["category"] = validated_category
                elif args.action == "name":
                    if not args.text.strip() or len(args.text) > 200:
                        raise ValueError("Name must contain 1..200 characters")
                    data["name"] = args.text.strip()
                elif args.action == "deadline":
                    data["deadline"] = deadline(args.text).isoformat()
                elif args.action == "on":
                    if not data["items"] or not data.get("deadline") or deadline(data["deadline"]) <= now():
                        raise ValueError("Activation requires items and a future deadline")
                    data["enabled"] = True
                elif args.action == "off":
                    data["enabled"] = False
                elif args.action in {"done", "pending"}:
                    item = select(data, args.text)
                    item.update(
                        status=args.action,
                        status_source="user_report",
                        status_at=now().isoformat(),
                        note=args.note[:4000],
                    )
                elif args.action == "prios":
                    pairs = [s.strip() for s in args.text.split(";") if s.strip()]
                    if not pairs:
                        raise ValueError("Use item weights, for example A1=100; A2=60")
                    for pair in pairs:
                        key, raw = pair.split("=", 1)
                        weight = int(raw)
                        if not 1 <= weight <= 100:
                            raise ValueError("Weight must be 1..100")
                        select(data, key.strip())["weight"] = weight
                elif args.action == "plans":
                    item = select(data, args.text)
                    item["plans"] = [p for p in item["plans"] if p["path"] != link["path"]] + [link]

            result = mutate(root, args.if_revision, change)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
