#!/usr/bin/env python3
"""Session-local priority weights. Python 3.10+, standard library only."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def state_path(provider: str, session_id: str, root: Path | None = None) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,39}", provider or ""):
        raise ValueError("A trusted provider namespace is required")
    if not session_id or not session_id.strip() or session_id in {"default", "global"}:
        raise ValueError("Trusted session ID missing: use conversation-only priorities")
    root = root or Path(os.environ.get("AGENT_PRIORITIES_ROOT", Path.home() / ".local/state/agent-priorities"))
    key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    return root.expanduser() / provider / (key + ".json")


def read(path: Path) -> dict:
    if not path.exists():
        return {"schema": "session-priorities.v1", "revision": 0, "items": []}
    if path.stat().st_size > 2_000_000:
        raise ValueError("Priorities exceed size limit")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(data, dict)
        or data.get("schema") != "session-priorities.v1"
        or type(data.get("revision")) is not int
        or data["revision"] < 0
        or not isinstance(data.get("items"), list)
        or len(data["items"]) > 100
    ):
        raise ValueError("Invalid priorities state")
    for item in data["items"]:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("text"), str)
            or not 1 <= len(item["text"]) <= 2000
            or type(item.get("weight")) is not int
            or not 1 <= item["weight"] <= 100
        ):
            raise ValueError("Invalid priority item")
    return data


def parse_items(text: str) -> list[dict]:
    parts = [p.strip() for p in re.split(r"[;\n]+", text) if p.strip()]
    if not parts or len(parts) > 100:
        raise ValueError("Supply 1 to 100 priorities separated by semicolons or newlines")
    items = []
    for i, part in enumerate(parts):
        match = re.fullmatch(r"(\d+)\s*::\s*(.+)", part)
        weight, label = (int(match[1]), match[2].strip()) if match else (100 - i, part)
        if not 1 <= weight <= 100 or len(label) > 2000:
            raise ValueError("Weights must be 1..100; labels at most 2000 characters")
        items.append({"text": label, "weight": weight})
    return sorted(items, key=lambda item: -item["weight"])


def update(path: Path, items: list[dict], expected: int) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(".lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    tmp = None
    try:
        current = read(path)
        if current["revision"] != expected:
            raise ValueError("Revision conflict: reread before changing priorities")
        data = {
            "schema": "session-priorities.v1",
            "revision": expected + 1,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "items": items,
        }
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".priorities-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, indent=2)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, path)
        return data
    finally:
        if tmp and Path(tmp).exists():
            Path(tmp).unlink()
        lock.unlink()


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["show", "set", "clear"])
    parser.add_argument("text", nargs="?", default="")
    parser.add_argument("--provider", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--if-revision", type=int)
    args = parser.parse_args(argv)
    try:
        path = state_path(args.provider, args.session_id, args.root)
        if args.action == "show":
            result = read(path)
        else:
            if args.if_revision is None:
                raise ValueError("Read current state, then supply --if-revision (0 for a new session)")
            result = update(path, parse_items(args.text) if args.action == "set" else [], args.if_revision)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
