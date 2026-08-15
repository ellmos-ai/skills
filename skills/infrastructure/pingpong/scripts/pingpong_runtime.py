#!/usr/bin/env python3
"""Create provider-specific PingPong prompts and perform bounded waits."""

from __future__ import annotations

import argparse
import os
import re
import socket
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

DURATION_RE = re.compile(r"^(?P<value>[1-9][0-9]*)(?P<unit>[smhd])$", re.IGNORECASE)
PROVIDER_ACTORS = {
    "codex": "codex-cli",
    "claude": "claude-code",
}


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
    return parser


def main() -> int:
    args = create_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
