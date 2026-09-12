import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "score_stations.py"
SPEC = importlib.util.spec_from_file_location("score_stations", SCRIPT)
assert SPEC and SPEC.loader
score_stations = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score_stations)


def line(**values):
    return json.dumps(values) + "\n"


def human(uuid, text, session="s1", timestamp="2026-01-01T00:00:00Z"):
    return line(
        type="user", uuid=uuid, sessionId=session, timestamp=timestamp,
        message={"content": [{"type": "text", "text": text}]},
    )


def tool_call(uuid, name, session="s1"):
    return line(
        type="assistant", uuid=uuid, sessionId=session,
        message={"content": [{"type": "tool_use", "name": name, "input": {"path": "/secret/path"}}]},
    )


def tool_result(uuid, is_error=False, session="s1"):
    return line(
        type="user", uuid=uuid, sessionId=session,
        message={"content": [{"type": "tool_result", "is_error": is_error, "content": "output"}]},
    )


def stop(uuid):
    return line(type="system", subtype="stop_hook_summary", uuid=uuid)


def write(tmp_path, lines, name="transcript.jsonl"):
    path = tmp_path / name
    path.write_text("".join(lines), encoding="utf-8")
    return path


def test_classify_prompt_covers_the_seven_types():
    assert score_stations.classify_prompt("Nein, das stimmt nicht") == "KO"
    assert score_stations.classify_prompt("Sehr gut, weiter") == "BE"
    assert score_stations.classify_prompt("Vergiss das, neuer Ansatz") == "RA"
    assert score_stations.classify_prompt("Warte noch") == "NS"
    assert score_stations.classify_prompt("Recherchier das nochmal") == "NM"
    assert score_stations.classify_prompt("Und was ist mit den Tests?") == "NT"
    assert score_stations.classify_prompt("Baue mir ein Werkzeug", is_first=True) == "SP"


def test_unclear_prompt_stays_unknown_instead_of_being_guessed():
    assert score_stations.classify_prompt("Der Ordner liegt woanders") == "unknown"
    assert score_stations.classify_prompt("") == "unknown"


def test_short_confirmations_do_not_match_inside_longer_words():
    # "ja" must not fire on "jahrelang", "ok" not on "Oktober".
    assert score_stations.classify_prompt("jahrelang lief das so") == "unknown"
    assert score_stations.classify_prompt("Oktober war der Stichtag") == "unknown"


def test_scored_output_contains_no_transcript_content(tmp_path):
    path = write(
        tmp_path,
        [
            human("u1", "Mach mir ein Werkzeug fuer GEHEIMNIS"),
            tool_call("a1", "Read"),
            tool_result("r1"),
            stop("m1"),
            human("u2", "Nein, so nicht -- VERTRAULICH"),
            tool_call("a2", "Edit"),
            stop("m2"),
            human("u3", "Sehr gut"),
        ],
    )
    result = score_stations.score_files([path])
    dumped = json.dumps(result, ensure_ascii=False)

    assert "GEHEIMNIS" not in dumped
    assert "VERTRAULICH" not in dumped
    assert "/secret/path" not in dumped
    assert "output" not in dumped
    # Tool names are structural and deliberately kept.
    assert "Read" in dumped and "Edit" in dumped


def test_correction_then_confirmation_scores_above_plain_run(tmp_path):
    learned = write(
        tmp_path,
        [
            human("u1", "Baue das Werkzeug"),
            tool_call("a1", "Read"),
            tool_call("a2", "Edit"),
            tool_call("a3", "Bash"),
            stop("m1"),
            human("u2", "Nein, falsch -- merk dir die Reihenfolge"),
            tool_call("a4", "Edit"),
            stop("m2"),
            human("u3", "Sehr gut"),
        ],
        name="learned.jsonl",
    )
    plain = write(
        tmp_path,
        [
            human("p1", "Baue das Werkzeug"),
            tool_call("b1", "Read"),
            stop("n1"),
            human("p2", "Der Ordner liegt woanders"),
        ],
        name="plain.jsonl",
    )

    learned_score = score_stations.score_files([learned])["sequences"][0]["harvest_score"]
    plain_score = score_stations.score_files([plain])["sequences"][0]["harvest_score"]
    assert learned_score > plain_score


def test_direction_change_ends_sequence_and_is_penalised(tmp_path):
    path = write(
        tmp_path,
        [
            human("u1", "Baue das Werkzeug"),
            tool_call("a1", "Read"),
            stop("m1"),
            human("u2", "Vergiss das, neuer Ansatz"),
            tool_call("a2", "Write"),
            stop("m2"),
            human("u3", "Sehr gut"),
        ],
    )
    result = score_stations.score_files([path])

    assert result["sequence_count"] == 2
    # Sequences come back ranked by score, so pick the dead end by its label.
    dead_end = next(s for s in result["sequences"] if s["closing_type"] == "RA")
    assert dead_end["harvest_score"] == 0
    assert not dead_end["candidate"]


def test_repeated_tool_chain_across_sessions_raises_score(tmp_path):
    def run(name, session):
        return write(
            tmp_path,
            [
                human("u1", "Baue das Werkzeug", session=session),
                tool_call("a1", "Read", session=session),
                tool_call("a2", "Edit", session=session),
                tool_call("a3", "Bash", session=session),
                stop("m1"),
                human("u2", "Sehr gut", session=session),
            ],
            name=name,
        )

    single = score_stations.score_files([run("one.jsonl", "s1")])
    both = score_stations.score_files([run("one.jsonl", "s1"), run("two.jsonl", "s2")])

    assert not single["sequences"][0]["chain_repeated"]
    assert both["sequences"][0]["chain_repeated"]
    assert both["sequences"][0]["harvest_score"] > single["sequences"][0]["harvest_score"]


def test_low_classification_ratio_is_reported_as_warning(tmp_path):
    path = write(
        tmp_path,
        [
            human("u1", "Der Ordner liegt woanders"),
            tool_call("a1", "Read"),
            stop("m1"),
            human("u2", "Die Datei heisst anders"),
            tool_call("a2", "Edit"),
            stop("m2"),
            human("u3", "Ein weiterer Hinweis"),
        ],
    )
    result = score_stations.score_files([path])

    assert result["classified_ratio"] < 0.5
    assert result["warnings"]


def test_error_with_following_correction_counts_as_pitfall(tmp_path):
    path = write(
        tmp_path,
        [
            human("u1", "Baue das Werkzeug"),
            tool_call("a1", "Bash"),
            tool_result("r1", is_error=True),
            stop("m1"),
            human("u2", "Nein, so nicht"),
            stop("m2"),
            human("u3", "Sehr gut"),
        ],
    )
    sequence = score_stations.score_files([path])["sequences"][0]

    assert sequence["signals"]["errors"] == 1
    assert any("Fallstrick" in reason for reason in sequence["score_reasons"])


def test_cli_writes_candidates_only(tmp_path):
    path = write(
        tmp_path,
        [
            human("u1", "Baue das Werkzeug"),
            tool_call("a1", "Read"),
            stop("m1"),
            human("u2", "Der Ordner liegt woanders"),
        ],
    )
    out = tmp_path / "scored.json"
    exit_code = score_stations.main([str(path), "--output", str(out), "--candidates-only"])

    assert exit_code == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema"] == "ellmos.station-scoring.v1"
    assert payload["sequences"] == []
