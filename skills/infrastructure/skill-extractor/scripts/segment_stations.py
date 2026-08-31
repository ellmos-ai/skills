#!/usr/bin/env python3
"""Segment JSONL transcripts into deterministic, content-free stations.

The first supported format is Claude Code JSONL. The output deliberately keeps
only structural metadata, timestamps, and turn identifiers. Message contents,
tool parameters, and absolute source paths are never copied to the result.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, TextIO

HARD_BOUNDARIES = {"stop_hook_summary", "compact_boundary"}
TURN_TYPES = {"assistant", "user"}
SCHEMA = "ellmos.station-segmentation.v1"


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _session_id(record: dict[str, Any]) -> str | None:
    value = record.get("sessionId") or record.get("session_id")
    return str(value) if value not in (None, "") else None


def _turn_id(record: dict[str, Any]) -> str | None:
    if record.get("type") not in TURN_TYPES:
        return None
    value = record.get("uuid")
    if value in (None, ""):
        message = record.get("message")
        if isinstance(message, dict):
            value = message.get("id")
    return str(value) if value not in (None, "") else None


def _new_station(line: int) -> dict[str, Any]:
    return {
        "start_line": line,
        "end_line": line,
        "start_timestamp": None,
        "end_timestamp": None,
        "session_ids": [],
        "turn_ids": [],
        "event_count": 0,
        "record_types": Counter(),
    }


def _append_event(
    station: dict[str, Any], line: int, record: dict[str, Any]
) -> None:
    if not station["event_count"]:
        station["start_line"] = line
    station["end_line"] = line
    station["event_count"] += 1
    station["record_types"][str(record.get("type") or "unknown")] += 1

    timestamp = record.get("timestamp")
    if isinstance(timestamp, str) and timestamp:
        if station["start_timestamp"] is None:
            station["start_timestamp"] = timestamp
        station["end_timestamp"] = timestamp

    session_id = _session_id(record)
    if session_id and session_id not in station["session_ids"]:
        station["session_ids"].append(session_id)

    turn_id = _turn_id(record)
    if turn_id and turn_id not in station["turn_ids"]:
        station["turn_ids"].append(turn_id)


def _finish_station(
    stations: list[dict[str, Any]],
    station: dict[str, Any],
    boundary_type: str,
    boundary_line: int,
) -> bool:
    if not station["event_count"]:
        return False
    station["station_id"] = f"station-{len(stations) + 1:04d}"
    station["boundary"] = {"type": boundary_type, "line": boundary_line}
    station["record_types"] = dict(sorted(station["record_types"].items()))
    stations.append(station)
    return True


def segment_lines(
    lines: Iterable[str], *, gap_seconds: float | None = None, strict: bool = False
) -> dict[str, Any]:
    """Return deterministic station metadata for an iterable of JSONL lines."""

    if gap_seconds is not None and gap_seconds <= 0:
        raise ValueError("gap_seconds must be greater than zero")

    stations: list[dict[str, Any]] = []
    station = _new_station(1)
    current_session: str | None = None
    previous_timestamp: datetime | None = None
    malformed_lines: list[int] = []
    marker_counts: Counter[str] = Counter()
    last_line = 0

    for line_number, raw_line in enumerate(lines, 1):
        last_line = line_number
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            if strict:
                raise ValueError(f"invalid JSON on line {line_number}: {exc.msg}") from exc
            malformed_lines.append(line_number)
            continue
        if not isinstance(record, dict):
            if strict:
                raise ValueError(f"JSON value on line {line_number} is not an object")
            malformed_lines.append(line_number)
            continue

        session_id = _session_id(record)
        session_changed = bool(
            session_id and current_session and session_id != current_session
        )
        if session_changed:
            if _finish_station(
                stations, station, "session_change", station["end_line"]
            ):
                marker_counts["session_change"] += 1
            station = _new_station(line_number)
            previous_timestamp = None
        if session_id:
            current_session = session_id

        event_timestamp = _timestamp(record.get("timestamp"))
        if (
            not session_changed
            and gap_seconds is not None
            and previous_timestamp is not None
            and event_timestamp is not None
            and (event_timestamp - previous_timestamp).total_seconds() > gap_seconds
        ):
            if _finish_station(stations, station, "time_gap", station["end_line"]):
                marker_counts["time_gap"] += 1
            station = _new_station(line_number)

        _append_event(station, line_number, record)
        if event_timestamp is not None:
            previous_timestamp = event_timestamp

        subtype = record.get("subtype")
        if subtype in HARD_BOUNDARIES:
            marker = str(subtype)
            marker_counts[marker] += 1
            _finish_station(stations, station, marker, line_number)
            station = _new_station(line_number + 1)
            previous_timestamp = None

    if station["event_count"]:
        _finish_station(stations, station, "session_end", last_line)
        marker_counts["session_end"] += 1

    return {
        "schema": SCHEMA,
        "station_count": len(stations),
        "marker_counts": dict(sorted(marker_counts.items())),
        "malformed_line_count": len(malformed_lines),
        "malformed_lines": malformed_lines,
        "stations": stations,
    }


def segment_file(
    path: Path, *, gap_seconds: float | None = None, strict: bool = False
) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        result = segment_lines(handle, gap_seconds=gap_seconds, strict=strict)
    result["source_name"] = path.name
    return result


def _write_json(result: dict[str, Any], output: TextIO) -> None:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Segment a Claude Code JSONL transcript into content-free stations."
    )
    parser.add_argument("input", type=Path, help="Claude Code JSONL transcript")
    parser.add_argument("--output", type=Path, help="write JSON to this file")
    parser.add_argument(
        "--gap-seconds",
        type=float,
        help="also split when consecutive timestamped events exceed this gap",
    )
    parser.add_argument(
        "--strict", action="store_true", help="fail on malformed or non-object JSON lines"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = segment_file(
            args.input, gap_seconds=args.gap_seconds, strict=args.strict
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.output:
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            _write_json(result, handle)
    else:
        _write_json(result, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
