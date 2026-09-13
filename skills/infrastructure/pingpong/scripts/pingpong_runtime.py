#!/usr/bin/env python3
"""Create provider-specific PingPong prompts, perform bounded waits, and run
the STATE/CALL handshake that decides whether this host joins a conversation."""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

DURATION_RE = re.compile(r"^(?P<value>[1-9][0-9]*)(?P<unit>[smhd])$", re.IGNORECASE)
PROVIDER_ACTORS = {
    "codex": "codex-cli",
    "claude": "claude-code",
}

# --- STATE and CALL -------------------------------------------------------
# STATE = "I am at the phone" (per host, persistent), CALL = "who should join".
# Joining requires BOTH; a call alone or a state alone never spreads.
STATE_KEY = "pingpong"
STATE_SUFFIX = ".state.json"
CALL_PREFIX = "call-"
LEGACY_CALL_PREFIX = "pull-"  # read-only transition, stop reading after 2026-12-31
CALL_SUFFIX = ".txt"
BROADCAST = "all"
DEFAULT_CALL_TTL = "6h"
CALL_NAME_RE = re.compile(
    r"^(?:%s|%s)(?P<sender>.+?)-to-(?P<target>.+)%s$"
    % (CALL_PREFIX, LEGACY_CALL_PREFIX, re.escape(CALL_SUFFIX))
)
# Three distinct outcomes: a failed check must never look like an empty one.
VERDICT_EXITS = {"call-for-me": 0, "idle": 1, "check-failed": 3}


def parse_expiry(value: str, now: datetime) -> datetime:
    """Parse a duration such as 24h or an ISO-8601 local timestamp."""
    match = DURATION_RE.fullmatch(value.strip())
    if match:
        amount = int(match.group("value"))
        unit = match.group("unit").lower()
        seconds = amount * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
        return now + timedelta(seconds=seconds)

    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "duration must be like 90m, 24h, 2d, or an ISO-8601 timestamp"
        ) from exc

    if parsed.tzinfo is None and now.tzinfo is not None:
        parsed = parsed.replace(tzinfo=now.tzinfo)
    return parsed


def build_prompt(args: argparse.Namespace) -> str:
    """Build the launch prompt without guessing host-specific paths."""
    now = datetime.now().astimezone()
    expires_at = parse_expiry(args.duration, now)
    if expires_at <= now:
        raise ValueError("expiry must be in the future")

    slot = args.slot or os.environ.get("PINGPONG_SLOT")
    if not slot:
        raise ValueError(
            "own slot is required; pass --slot or set PINGPONG_SLOT"
        )

    sync_root_value = args.sync_root or os.environ.get("PINGPONG_SYNC_ROOT")
    if not sync_root_value:
        raise ValueError(
            "sync root is required; pass --sync-root or set PINGPONG_SYNC_ROOT"
        )

    sync_root = Path(sync_root_value).expanduser()
    actor = f"{PROVIDER_ACTORS[args.provider]}@{args.host}"
    common = (
        f"Use $pingpong as {actor}. Sync root: {sync_root}. "
        f"Write only to own slot: {slot}. "
        f"Expiry: {expires_at.isoformat(timespec='seconds')}. "
        "Start with an immediate FileCommander-MCP freshness scan and fully read "
        "the newest three files in every relevant channel. Then apply cadence "
        "mechanism B, beginning at 15 minutes. Every scan and every completion "
        "claim must be backed by FileCommander evidence. Run a final full scan "
        "at expiry and finish only when no accepted work remains open."
    )

    if args.provider == "codex":
        return (
            common
            + " Create a persisted goal whose objective contains the expiry, "
            "completion criteria, actor, sync root, and own slot. Keep the goal "
            "active so session wake-ups continue until the criteria are met."
        )

    return (
        common
        + " This prompt is intended for a Claude /loop launch. Do not create a "
        "second loop. Replace the loop interval when cadence changes and stop "
        "the loop after the expiry criteria are satisfied."
    )


def wait_until(target: datetime) -> None:
    """Wait until target while keeping individual sleeps below one minute."""
    while True:
        remaining = (target - datetime.now().astimezone()).total_seconds()
        if remaining <= 0:
            return
        time.sleep(min(remaining, 55.0))


def command_prompt(args: argparse.Namespace) -> int:
    try:
        print(build_prompt(args))
    except (ValueError, argparse.ArgumentTypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


def command_wait(args: argparse.Namespace) -> int:
    now = datetime.now().astimezone()
    try:
        target = parse_expiry(args.until, now)
    except argparse.ArgumentTypeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    wait_until(target)
    return 0


def _required(value: str | None, option: str, env: str) -> str:
    """Fail closed instead of guessing a host-specific value."""
    resolved = value or os.environ.get(env)
    if not resolved:
        raise ValueError(f"{option} is required; pass --{option} or set {env}")
    return resolved


def resolve_sync_root(args: argparse.Namespace) -> Path:
    return Path(
        _required(args.sync_root, "sync-root", "PINGPONG_SYNC_ROOT")
    ).expanduser()


def resolve_slot(args: argparse.Namespace) -> str:
    return _required(args.slot, "slot", "PINGPONG_SLOT")


def registry_dir(sync_root: Path) -> Path:
    return sync_root / "agents" / "registry"


def calls_dir(sync_root: Path) -> Path:
    return sync_root / "agents"


def state_path(sync_root: Path, slot: str) -> Path:
    return registry_dir(sync_root) / f"{slot}{STATE_SUFFIX}"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict) -> None:
    """Replace atomically so a concurrent reader never sees a half file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / (path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    tmp.replace(path)


def set_state(sync_root: Path, slot: str, active: bool, actor: str | None) -> Path:
    """Set the pingpong field in the slot state file, keeping every other key.

    The file belongs to mirror_rulefiles.py, which regenerates it and carries
    this field forward; read-modify-write here keeps both writers additive.
    """
    path = state_path(sync_root, slot)
    data = read_json(path) if path.exists() else {"slot": slot}
    entry = {
        "active": bool(active),
        "since": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    if actor:
        entry["actor"] = actor
    data[STATE_KEY] = entry
    write_json(path, data)
    return path


def active_slots(sync_root: Path, exclude: str | None = None) -> dict[str, dict]:
    """Stage 1, the cheap one: which hosts declare themselves active?

    Raises OSError/ValueError on an unreadable or broken registry so the caller
    can report check-failed instead of a fake empty result.
    """
    directory = registry_dir(sync_root)
    if not directory.is_dir():
        raise OSError(f"registry directory not readable: {directory}")
    found: dict[str, dict] = {}
    for path in sorted(directory.glob(f"*{STATE_SUFFIX}")):
        slot = path.name[: -len(STATE_SUFFIX)]
        if slot == exclude:
            continue
        entry = read_json(path).get(STATE_KEY) or {}
        if entry.get("active"):
            found[slot] = entry
    return found


def call_path(sync_root: Path, sender: str, target: str) -> Path:
    return calls_dir(sync_root) / f"{CALL_PREFIX}{sender}-to-{target}{CALL_SUFFIX}"


def parse_call(path: Path, now: datetime) -> dict:
    """Read one call. Sender and target come from the name, so stage 2 can
    match without opening anything; the body only carries expiry and reason."""
    match = CALL_NAME_RE.match(path.name)
    if not match:
        raise ValueError(f"not a call file name: {path.name}")
    call = {
        "path": path,
        "sender": match.group("sender"),
        "target": match.group("target"),
        "legacy": path.name.startswith(LEGACY_CALL_PREFIX),
        "reason": "",
        "expires": None,
    }
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key = key.strip().upper()
        if key == "REASON":
            call["reason"] = value.strip()
        elif key == "EXPIRES":
            try:
                call["expires"] = parse_expiry(value.strip(), now)
            except argparse.ArgumentTypeError:
                call["expires"] = None
    if call["expires"] is None:
        # No expiry field (hand-written or legacy pull file): fall back to the
        # file's own age plus the default ttl, never to "lives forever".
        mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).astimezone()
        call["expires"] = parse_expiry(DEFAULT_CALL_TTL, mtime)
    call["expired"] = call["expires"] <= now
    return call


def scan_calls(sync_root: Path, now: datetime) -> list[dict]:
    directory = calls_dir(sync_root)
    if not directory.is_dir():
        raise OSError(f"call directory not readable: {directory}")
    calls = []
    for path in sorted(directory.iterdir()):
        if not path.is_file() or not CALL_NAME_RE.match(path.name):
            continue
        calls.append(parse_call(path, now))
    return calls


def calls_for_me(calls: list[dict], slot: str, senders: dict[str, dict]) -> list[dict]:
    """A call reaches me when it is live, not mine, addressed to me or to all,
    and its sender is one of the hosts that stage 1 found active."""
    return [
        call
        for call in calls
        if not call["expired"]
        and call["sender"] != slot
        and call["target"] in (slot, BROADCAST)
        and call["sender"] in senders
    ]


def command_state(args: argparse.Namespace) -> int:
    try:
        sync_root = resolve_sync_root(args)
        slot = resolve_slot(args)
        if args.activate or args.deactivate:
            path = set_state(sync_root, slot, bool(args.activate), args.actor)
            print(f"{slot}: pingpong active={bool(args.activate)} -> {path}")
            return 0
        others = active_slots(sync_root, exclude=slot)
        own = (
            read_json(state_path(sync_root, slot)).get(STATE_KEY) or {}
            if state_path(sync_root, slot).exists()
            else {}
        )
        print(f"self ({slot}): active={bool(own.get('active'))} since={own.get('since', '-')}")
        print("active others: " + (", ".join(sorted(others)) if others else "(none)"))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    return 0


def command_call(args: argparse.Namespace) -> int:
    now = datetime.now().astimezone()
    try:
        sync_root = resolve_sync_root(args)
        slot = resolve_slot(args)
        if args.list:
            for call in scan_calls(sync_root, now):
                mark = "expired" if call["expired"] else "live"
                print(
                    f"{call['path'].name}: {mark} until "
                    f"{call['expires'].isoformat(timespec='seconds')} {call['reason']}"
                )
            return 0
        if not args.to:
            raise ValueError("--to is required unless --list is given")
        path = call_path(sync_root, slot, args.to)
        if args.end:
            if path.exists():
                path.unlink()
                print(f"call ended: {path}")
            else:
                print(f"no call to end: {path}")
            return 0
        reason = args.reason
        if not reason and path.exists():
            reason = parse_call(path, now)["reason"]  # refresh keeps the reason
        expires = parse_expiry(args.ttl, now)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "CALL\n"
            f"FROM:     {slot}\n"
            f"TO:       {args.to}\n"
            f"OPENED:   {now.isoformat(timespec='seconds')}\n"
            f"EXPIRES:  {expires.isoformat(timespec='seconds')}\n"
            f"REASON:   {reason or ''}\n",
            encoding="utf-8",
        )
        print(f"call open until {expires.isoformat(timespec='seconds')}: {path}")
    except (OSError, ValueError, argparse.ArgumentTypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    return 0


def command_check(args: argparse.Namespace) -> int:
    """Two stages: ask the cheap question first, open call files only on a hit."""
    now = datetime.now().astimezone()
    report: dict = {"verdict": "check-failed", "checked_at": now.isoformat(timespec="seconds")}
    try:
        sync_root = resolve_sync_root(args)
        slot = resolve_slot(args)
        report["slot"] = slot
        own_state = state_path(sync_root, slot)
        report["self_active"] = bool(
            (read_json(own_state).get(STATE_KEY) or {}).get("active")
            if own_state.exists()
            else False
        )
        others = active_slots(sync_root, exclude=slot)
        report["active_hosts"] = sorted(others)
        if not others:
            report["verdict"] = "idle"
            report["calls"] = []
        else:
            mine = calls_for_me(scan_calls(sync_root, now), slot, others)
            report["calls"] = [
                {
                    "file": call["path"].name,
                    "from": call["sender"],
                    "to": call["target"],
                    "expires": call["expires"].isoformat(timespec="seconds"),
                    "reason": call["reason"],
                    "legacy_name": call["legacy"],
                }
                for call in mine
            ]
            report["verdict"] = "call-for-me" if mine else "idle"
    except (OSError, ValueError, argparse.ArgumentTypeError) as exc:
        report["error"] = str(exc)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(f"verdict: check-failed ({exc})", file=sys.stderr)
        return VERDICT_EXITS["check-failed"]

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"verdict: {report['verdict']}")
        print(f"self_active: {report['self_active']}")
        print("active_hosts: " + (", ".join(report["active_hosts"]) or "(none)"))
        for call in report["calls"]:
            print(f"call: {call['file']} until {call['expires']} {call['reason']}")
    return VERDICT_EXITS[report["verdict"]]


def add_channel_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--slot", help="own slot name, or set PINGPONG_SLOT")
    parser.add_argument("--sync-root", help="shared sync root, or set PINGPONG_SYNC_ROOT")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prompt_parser = subparsers.add_parser(
        "prompt", help="print a provider-specific PingPong launch prompt"
    )
    prompt_parser.add_argument("--provider", choices=sorted(PROVIDER_ACTORS), required=True)
    prompt_parser.add_argument("--duration", default="24h")
    prompt_parser.add_argument("--host", default=socket.gethostname())
    prompt_parser.add_argument("--slot")
    prompt_parser.add_argument("--sync-root")
    prompt_parser.set_defaults(handler=command_prompt)

    wait_parser = subparsers.add_parser(
        "wait", help="wait until a duration or ISO-8601 timestamp has elapsed"
    )
    wait_parser.add_argument("--until", required=True)
    wait_parser.set_defaults(handler=command_wait)

    state_parser = subparsers.add_parser(
        "state", help="show or set the pingpong state of this host"
    )
    add_channel_arguments(state_parser)
    mode = state_parser.add_mutually_exclusive_group()
    mode.add_argument("--activate", action="store_true", help="I am at the phone")
    mode.add_argument("--deactivate", action="store_true", help="hang up")
    state_parser.add_argument("--actor", help="actor label, e.g. claude-code@HOST")
    state_parser.set_defaults(handler=command_state)

    call_parser = subparsers.add_parser(
        "call", help="open, refresh, end or list calls"
    )
    add_channel_arguments(call_parser)
    call_parser.add_argument("--to", help="target slot or 'all'")
    call_parser.add_argument("--reason", help="why; kept when refreshing")
    call_parser.add_argument(
        "--ttl", default=DEFAULT_CALL_TTL,
        help=f"expiry of the call, default {DEFAULT_CALL_TTL}; re-run to refresh",
    )
    call_parser.add_argument("--end", action="store_true", help="delete my call")
    call_parser.add_argument("--list", action="store_true", help="list all calls")
    call_parser.set_defaults(handler=command_call)

    check_parser = subparsers.add_parser(
        "check",
        help="two-stage check; exit 0 call-for-me, 1 idle, 3 check-failed",
    )
    add_channel_arguments(check_parser)
    check_parser.add_argument("--json", action="store_true")
    check_parser.set_defaults(handler=command_check)
    return parser


def main() -> int:
    args = create_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
