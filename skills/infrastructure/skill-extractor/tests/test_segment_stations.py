import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "segment_stations.py"
SPEC = importlib.util.spec_from_file_location("segment_stations", SCRIPT)
assert SPEC and SPEC.loader
segment_stations = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(segment_stations)


def line(**values):
    return json.dumps(values) + "\n"


def test_stop_markers_split_stations_without_copying_content():
    result = segment_stations.segment_lines(
        [
            line(type="user", uuid="u1", sessionId="s1", timestamp="2026-01-01T00:00:00Z", message={"content": "secret"}),
            line(type="assistant", uuid="a1", timestamp="2026-01-01T00:00:01Z", message={"content": "answer"}),
            line(type="system", subtype="stop_hook_summary", uuid="m1", timestamp="2026-01-01T00:00:02Z"),
            line(type="user", uuid="u2", sessionId="s1", timestamp="2026-01-01T00:00:03Z"),
        ]
    )

    assert result["station_count"] == 2
    assert result["marker_counts"] == {"session_end": 1, "stop_hook_summary": 1}
    assert result["stations"][0]["boundary"]["type"] == "stop_hook_summary"
    assert result["stations"][0]["turn_ids"] == ["u1", "a1"]
    assert result["stations"][1]["turn_ids"] == ["u2"]
    assert "secret" not in json.dumps(result)
    assert "answer" not in json.dumps(result)


def test_missing_session_ids_do_not_create_false_boundaries():
    result = segment_stations.segment_lines(
        [
            line(type="user", uuid="u1", sessionId="s1"),
            line(type="attachment"),
            line(type="assistant", uuid="a1", sessionId="s1"),
        ]
    )

    assert result["station_count"] == 1
    assert result["stations"][0]["boundary"]["type"] == "session_end"
    assert result["stations"][0]["session_ids"] == ["s1"]


def test_nonempty_session_change_and_compact_marker_are_boundaries():
    result = segment_stations.segment_lines(
        [
            line(type="user", uuid="u1", sessionId="s1"),
            line(type="user", uuid="u2", sessionId="s2"),
            line(type="system", subtype="compact_boundary", sessionId="s2"),
        ]
    )

    assert [s["boundary"]["type"] for s in result["stations"]] == [
        "session_change",
        "compact_boundary",
    ]
    assert result["marker_counts"] == {"compact_boundary": 1, "session_change": 1}


def test_optional_time_gap_and_lenient_malformed_line_tracking():
    result = segment_stations.segment_lines(
        [
            line(type="user", uuid="u1", timestamp="2026-01-01T00:00:00Z"),
            "not-json\n",
            line(type="assistant", uuid="a1", timestamp="2026-01-01T00:02:00Z"),
        ],
        gap_seconds=60,
    )

    assert [s["boundary"]["type"] for s in result["stations"]] == [
        "time_gap",
        "session_end",
    ]
    assert result["malformed_lines"] == [2]


def test_malformed_prefix_does_not_change_first_event_line():
    result = segment_stations.segment_lines(
        ["not-json\n", line(type="user", uuid="u1")]
    )

    assert result["stations"][0]["start_line"] == 2


def test_gap_after_hard_boundary_does_not_create_an_empty_marker():
    result = segment_stations.segment_lines(
        [
            line(
                type="system",
                subtype="stop_hook_summary",
                timestamp="2026-01-01T00:00:00Z",
            ),
            line(type="user", uuid="u1", timestamp="2026-01-01T01:00:00Z"),
        ],
        gap_seconds=60,
    )

    assert result["marker_counts"] == {
        "session_end": 1,
        "stop_hook_summary": 1,
    }


def test_strict_mode_rejects_malformed_lines():
    with pytest.raises(ValueError, match="invalid JSON on line 2"):
        segment_stations.segment_lines([line(type="user"), "nope\n"], strict=True)
