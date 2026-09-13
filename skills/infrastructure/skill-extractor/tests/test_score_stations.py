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


# ─── S5: was ist ueberhaupt ein Prompt (deterministisch, vor jedem Modell) ───


def test_empty_and_machine_turns_are_not_failed_classification():
    """19% der Anschluesse waren leer, 10% Maschinen-Envelopes. Als 'unknown'
    gezaehlt liessen sie den Vorfilter viel schlechter aussehen, als er ist --
    und ein Modell haette daran nichts zu klassifizieren gehabt."""
    assert score_stations.prompt_kind("") == "empty"
    assert score_stations.prompt_kind("   \n ") == "empty"
    assert score_stations.prompt_kind("<task-notification> <task-id>x</task-id>") == "machine"
    assert score_stations.prompt_kind("<system-reminder>merk dir das</system-reminder>") == "machine"
    assert score_stations.prompt_kind("Another Claude session sent a message: hi") == "machine"
    assert score_stations.prompt_kind("<bash-input> npm publish</bash-input>") == "machine"
    assert score_stations.prompt_kind("pruef das nochmal") == "human"


def test_bare_slash_command_is_machine_but_a_command_with_intent_is_not():
    """"/compact" sagt nichts ueber die Station davor. "/loop <Auftrag>" schon --
    deshalb greift die Regel nur auf den nackten Befehl."""
    assert score_stations.prompt_kind("/compact") == "machine"
    assert score_stations.prompt_kind("/sync") == "machine"
    assert score_stations.prompt_kind("/loop arbeite die Tickets ab") == "human"


def test_commissioning_prompt_is_recognisable_even_though_a_session_start_is_not():
    """S3 mass den SESSION-Start und fand ihn sprachlich nicht erkennbar. Der
    AUFTRAGS-Prompt ist es sehr wohl: 14 von 25 SP bei 100% Praezision."""
    assert score_stations.classify_prompt("neues ticket: USMC an hooker anbinden") == "SP"
    assert score_stations.classify_prompt("erstelle daraus einen Artikel") == "SP"
    assert score_stations.classify_prompt("starte die olympiade") == "SP"
    assert score_stations.classify_prompt("Idee: eigener harness chat") == "SP"


def test_specific_class_beats_the_opening_imperative():
    """Ein Auftrag, der zugleich korrigiert, ist eine Korrektur -- sonst wandern
    KO-Punkte (die einzigen, die im Score wirklich zaehlen) nach SP ab."""
    assert score_stations.classify_prompt("erstelle das nochmal, so nicht") == "KO"
    assert score_stations.classify_prompt("baue das, aber warte auf den Test") == "NS"


# ─── S5: die optionale Modellstufe ───


def test_classifier_command_labels_only_what_it_may_label():
    """Ein Kommando darf Labels liefern -- aber nur die sieben Typen. Alles
    andere bleibt 'unknown': ein erfundenes Label ist schlimmer als eine Luecke."""
    good = 'python -c "import json,sys;sys.stdin.read();print(json.dumps([\'KO\',\'BE\']))"'
    assert score_stations.classify_with_command(["a", "b"], good) == ["KO", "BE"]

    junk = 'python -c "import json,sys;sys.stdin.read();print(json.dumps([\'VIELLEICHT\',\'BE\']))"'
    assert score_stations.classify_with_command(["a", "b"], junk) == ["unknown", "BE"]


def test_classifier_command_failures_never_produce_misaligned_labels():
    """Laengendifferenz, kaputtes JSON oder ein Fehlerexit duerfen NICHT dazu
    fuehren, dass echte Labels an den falschen Stationen landen."""
    short = 'python -c "import json,sys;sys.stdin.read();print(json.dumps([\'KO\']))"'
    assert score_stations.classify_with_command(["a", "b"], short) == ["unknown", "unknown"]

    broken = 'python -c "import sys;sys.stdin.read();print(\'kein json\')"'
    assert score_stations.classify_with_command(["a", "b"], broken) == ["unknown", "unknown"]

    failing = 'python -c "import sys;sys.stdin.read();sys.exit(3)"'
    assert score_stations.classify_with_command(["a"], failing) == ["unknown"]

    assert score_stations.classify_with_command([], "does-not-run") == []


def test_ratio_denominator_holds_only_human_prompts(tmp_path):
    """Der Nenner entscheidet, ob die Kennzahl etwas ueber den Vorfilter sagt.
    Eine Station, deren Anschluss eine Maschinennachricht ist, kann nicht
    klassifiziert werden -- sie darf die Quote deshalb weder heben noch senken."""
    path = write(
        tmp_path,
        [
            human("u1", "starte den Lauf"),
            tool_call("a1", "Read"),
            stop("m1"),
            human("u2", "so nicht, das ist falsch"),
            tool_call("a2", "Edit"),
            stop("m2"),
            human("u3", "<task-notification> <task-id>x</task-id> fertig"),
            tool_call("a3", "Write"),
            stop("m3"),
            human("u4", ""),
        ],
    )
    result = score_stations.score_files([path])
    sequence = result["sequences"][0]

    assert sequence["type_counts"].get("non_prompt", 0) >= 1
    assert sequence["human_prompt_count"] + sequence["non_prompt_count"] == (
        sequence["station_count"]
    )
    # Die nicht-Prompts sind aus dem Nenner heraus: die Quote spiegelt nur,
    # was der Vorfilter an echten Aeusserungen geschafft hat.
    assert sequence["classified_ratio"] == 1.0
    assert result["classification"]["model_stage"] is False


def test_model_stage_labels_the_right_station_end_to_end(tmp_path):
    """Der Modellpfad in score_files() wurde von keinem Test betreten: die Unit
    deckt classify_with_command ab, aber nicht das Einsammeln, den Batch und das
    Zurueckschreiben. Genau dort entscheidet sich, ob ein Label an SEINER Station
    landet -- und genau dort faellt ein Fehler erst im Echtlauf auf."""
    path = write(
        tmp_path,
        [
            human("u1", "mach weiter"),          # BE, Vorfilter
            tool_call("a1", "Read"),
            stop("m1"),
            human("u2", "der Ordner liegt woanders"),   # unknown -> Modell
            tool_call("a2", "Edit"),
            stop("m2"),
        ],
    )
    # Stub statt echtem Modell: liefert fuer jede Eingabe RA, damit eindeutig
    # sichtbar ist, WELCHE Station das Modell-Label bekommen hat.
    stub = 'python -c "import json,sys;n=len(json.loads(sys.stdin.read()));print(json.dumps([\'RA\']*n))"'

    without = score_stations.score_files([path])
    with_model = score_stations.score_files([path], classifier_cmd=stub)

    assert without["classification"] == {
        "model_stage": False, "model_offered": 0, "model_labelled": 0}
    assert with_model["classification"]["model_stage"] is True
    assert with_model["classification"]["model_offered"] == 1
    assert with_model["classification"]["model_labelled"] == 1

    # Die vom Vorfilter entschiedene Station bleibt unangetastet; nur die offene
    # bekommt das Modell-Label -- und die Quote steigt entsprechend.
    types_before = [t for s in without["sequences"] for t in s["type_counts"]]
    assert "unknown" in types_before
    types_after = [t for s in with_model["sequences"] for t in s["type_counts"]]
    assert "unknown" not in types_after
    assert with_model["classified_ratio"] > without["classified_ratio"]


def test_model_stage_reports_when_the_command_delivered_nothing(tmp_path):
    """Ein stummes Kommando sieht sonst genauso aus wie ein Modell, das nichts
    hinzuzufuegen hatte."""
    path = write(
        tmp_path,
        [
            human("u1", "der Ordner liegt woanders"),
            tool_call("a1", "Read"),
            stop("m1"),
            human("u2", "und der zweite auch"),
            tool_call("a2", "Edit"),
            stop("m2"),
        ],
    )
    failing = 'python -c "import sys;sys.stdin.read();sys.exit(1)"'
    result = score_stations.score_files([path], classifier_cmd=failing)

    assert result["classification"]["model_labelled"] == 0
    assert any("--classifier-cmd" in w for w in result["warnings"])
