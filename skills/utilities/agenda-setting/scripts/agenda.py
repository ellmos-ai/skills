#!/usr/bin/env python3
"""Shared time-limited agenda and pointers to existing plans. No task execution."""

from __future__ import annotations

import argparse
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


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        nargs="?",
        default="show",
        choices=["show", "set", "add", "name", "on", "off", "deadline", "done", "pending", "prios", "plans"],
    )
    parser.add_argument("text", nargs="?", default="")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--if-revision", type=int)
    parser.add_argument("--note", default="")
    parser.add_argument("--weight", type=int, default=50)
    parser.add_argument("--path", type=Path)
    parser.add_argument("--kind", choices=["plan", "plan-register", "policy-register"], default="plan")
    parser.add_argument("--planner", default="")
    args = parser.parse_args(argv)
    try:
        root = state_root(args.root, profile(args.profile))
        if args.action == "show":
            result = view(read(root))
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
                    text = args.text.strip()
                    if not text or len(text) > 2000:
                        raise ValueError("Item text must contain 1..2000 characters")
                    if len(data["items"]) >= 100 or not 1 <= args.weight <= 100:
                        raise ValueError("At most 100 items; weight must be 1..100")
                    number = max((int(i["id"][1:]) for i in data["items"]), default=0) + 1
                    if number > 999:
                        raise ValueError("No free item ID left")
                    data["items"].append(
                        {"id": f"A{number}", "text": text, "weight": args.weight, "status": "pending", "plans": []}
                    )
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
