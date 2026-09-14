#!/usr/bin/env python3
"""Score station sequences of a transcript by harvest value (S3).

Builds on the deterministic segmentation of ``segment_stations.py``:

1. segment the transcript into stations (hard boundaries, no judgement),
2. collect hard signals per station (tool names, errors, interrupts, human turns),
3. classify the follow-up prompt of every station into the seven prompt types of
   the ``promptarchaeologie`` method (SP/NT/NM/NS/KO/BE/RA) using a deterministic
   word-list prefilter -- anything not clearly matched stays ``unknown``,
4. group stations into sequences and score each sequence.

The follow-up prompt is the label: a station is judged by what the human says
next. Message text is read for classification only -- the result carries labels,
counts, tool names and identifiers, never transcript content.

The prefilter is deliberately conservative. ``classified_ratio`` reports how much
of the sequence was actually classified; a score built on mostly ``unknown``
follow-ups is not trustworthy and says so.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, TextIO

try:  # running as a module inside the package
    from .segment_stations import segment_file
except ImportError:  # running as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from segment_stations import segment_file  # type: ignore[no-redef]

SCHEMA = "ellmos.station-scoring.v1"

# Hard markers that end a station sequence: a new task starts here.
RESTART_BOUNDARIES = {"session_change", "time_gap", "compact_boundary"}

# A calibration knob, not a constant of nature: within one long session the hard
# restart markers are rare, so without a time gap the whole session collapses into
# a handful of sequences of 30+ stations -- too coarse to harvest a single skill
# from. 30 minutes separates "picked the work back up" from "still on it" in the
# measured transcripts; tune with --gap-seconds, disable with --gap-seconds 0.
DEFAULT_GAP_SECONDS = 1800.0

# Prompt types of the promptarchaeologie method. Order matters: the first match
# wins, so the narrow, high-signal classes are tested before the broad ones.
TYPE_MARKERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "RA",
        (
            "vergiss das",
            "vergiss es",
            "anderer ansatz",
            "anderen ansatz",
            "neuer plan",
            "neuer ansatz",
            "lass uns stattdessen",
            "machen wir stattdessen",
            "kehrtwende",
            "brich ab",
            "abbrechen",
            "verwirf",
        ),
    ),
    (
        "KO",
        (
            "nein",
            "nicht so",
            "stattdessen",
            "falsch",
            "stimmt nicht",
            "merk dir",
            "immer",
            "nie",
            "niemals",
            r"korrigier\w*",
            "so nicht",
        ),
    ),
    (
        "NS",
        (
            "warte",
            "stopp",
            "stop",
            "halt",
            "erst mal",
            "erstmal",
            "zuerst",
            "danach",
            "nicht jetzt",
            "spaeter",
            "später",
            "reihenfolge",
            "noch nicht",
        ),
    ),
    (
        "NM",
        (
            "nochmal",
            "noch mal",
            r"pruef\w*",
            r"prüf\w*",
            r"recherchier\w*",
            "teste",
            r"verifizier\w*",
            "belege",
            "nachweis",
        ),
    ),
    (
        "BE",
        (
            "sehr gut",
            "super",
            "perfekt",
            "passt",
            "genau",
            "richtig so",
            "danke",
            "weiter",
            "ok",
            "okay",
            "ja",
        ),
    ),
    (
        "NT",
        (
            "was ist mit",
            "wie steht es",
            "und was",
            "warum",
            "wieso",
            "wie genau",
            "was bedeutet",
            "noch etwas zu",
            "noch was zu",
        ),
    ),
)

INTERRUPT_MARKER = "[Request interrupted by user"

# Envelopes that ride in a human turn without being a human utterance. The
# interrupt marker is deliberately NOT listed: it is a real human act (stopping
# the agent) and classify_prompt maps it to NS.
MACHINE_ENVELOPE = re.compile(
    r"(?:<task-notification>"
    r"|<system-reminder>"
    r"|<command-message>"
    r"|<command-name>"
    r"|<local-command-std"
    r"|<teammate-message"
    r"|<local-command-caveat>"
    r"|<bash-input>"
    r"|<bash-stdout>"
    r"|Another Claude session sent a message:"
    r"|Caveat: The messages below were generated)",
    re.IGNORECASE,
)

# A bare slash command is typed by a human but carries no prompt type: "/compact"
# says nothing about the station it follows. Kept separate from the envelopes
# above because it is a whole-string match -- "/loop arbeite Tickets ab" DOES
# carry intent and must stay a human prompt.
BARE_COMMAND = re.compile(r"^/[a-z0-9][\w-]*$", re.IGNORECASE)

# The commissioning prompt -- anchored at the start, because only there does an
# imperative name a new job instead of qualifying a running one.
#
# S3 concluded "a start prompt is not recognisable by wording". That holds for
# the SESSION start, which is what was measured then -- but not for the
# COMMISSIONING prompt, which announces a ticket or opens with a creating verb.
# Measured against 57 hand-labelled follow-ups: these markers catch 14 of 25 SP
# at 100% precision (no false positive), where a small model caught 15 and got
# 17 other labels wrong. Cheaper AND more accurate, so it belongs in the
# prefilter rather than in the model stage.
SP_MARKERS = re.compile(
    r"^(?:neues ticket|weiteres ticket|ein letztes ticket|ticket)\b"
    r"|^(?:erstelle|baue|bau|starte|richte|lege|schreibe|oeffne|öffne|ziehe|gib mir)\b"
    r"|^idee\s*:",
    re.IGNORECASE,
)

# A conservative question fallback for natural questions that have no question
# word and are not covered by a more specific marker. It deliberately does not
# classify every vague sentence as a question: explicit punctuation or a small
# set of unambiguous question openers counts. Specific markers still win because
# this check runs after ``_COMPILED_MARKERS``.
QUESTION_OPENERS = re.compile(
    r"^(?:kannst du|könntest du|koenntest du|können wir|koennen wir|"
    r"soll ich|sollen wir|würdest du|wuerdest du|gibt es|hast du|"
    r"habt ihr|ist das|sind das|war das|wäre das|waere das)\b",
    re.IGNORECASE,
)


def _text_of(record: dict[str, Any]) -> str:
    """Return the plain text of a message record (classification input only)."""

    message = record.get("message")
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)


def _content_blocks(record: dict[str, Any]) -> list[dict[str, Any]]:
    message = record.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if not isinstance(content, list):
        return []
    return [block for block in content if isinstance(block, dict)]


_COMPILED_MARKERS: tuple[tuple[str, "re.Pattern[str]"], ...] = tuple(
    (
        prompt_type,
        re.compile(r"\b(?:" + "|".join(markers) + r")\b"),
    )
    for prompt_type, markers in TYPE_MARKERS
)


def prompt_kind(text: str) -> str:
    """Tell apart what a "follow-up" actually is: ``empty``, ``machine`` or ``human``.

    Measured on three real transcripts (246 follow-ups): 19% carried no text at
    all and 10% were machine envelopes that merely travel in a human turn --
    task notifications, teammate messages, slash-command wrappers. Counting
    those as failed classification made the prefilter look far worse than it is
    (0.451 against 0.634 once the denominator holds only human utterances), and
    it would have sent a model 71 inputs that have no prompt type to find.
    Neither is a classification problem; both are decidable by looking.
    """

    stripped = text.strip()
    if not stripped:
        return "empty"
    if MACHINE_ENVELOPE.match(stripped) or BARE_COMMAND.match(stripped):
        return "machine"
    return "human"


def classify_prompt(text: str, *, is_first: bool = False) -> str:
    """Classify a human prompt into one of the seven types, else ``unknown``.

    Markers match on word boundaries, never as substrings: otherwise "weitere"
    reads as the confirmation "weiter" and "jahrelang" as the "ja" that ends a
    correction loop. Anything without a clear marker stays ``unknown`` -- an
    honest gap beats a guessed label, because the score is built on these counts.
    """

    normalized = " ".join(text.lower().split())
    if not normalized:
        return "unknown"
    if INTERRUPT_MARKER.lower() in normalized:
        return "NS"
    for prompt_type, pattern in _COMPILED_MARKERS:
        if pattern.search(normalized):
            return prompt_type
    # A clear follow-up question is NT even when it has no traditional question
    # word. Keep the fallback narrow; vague state messages remain ``unknown``.
    if normalized.endswith("?") or QUESTION_OPENERS.match(normalized):
        return "NT"
    # Checked last on purpose: "erstelle X, aber nicht so wie vorher" is a
    # correction that happens to open with an imperative. The specific class
    # wins; SP is the fallback mode of a prompt, not a competing marker.
    if SP_MARKERS.search(normalized):
        return "SP"
    return "SP" if is_first else "unknown"


VALID_TYPES = frozenset({"SP", "NT", "NM", "NS", "KO", "BE", "RA"})


def classify_with_command(
    texts: list[str], command: str, *, timeout: float = 120.0
) -> list[str]:
    """Hand the prompts the prefilter could not decide to an external classifier.

    Deliberately a COMMAND, not a provider adapter: this repository is public and
    user-neutral, so it must not carry anyone's model endpoint, host path or key.
    The caller points ``--classifier-cmd`` at whatever they already use locally
    (a routing CLI, a local model, a batch script); the contract is one JSON
    array of strings on stdin, one JSON array of labels of equal length on
    stdout. Anything the command returns that is not one of the seven types
    stays ``unknown`` -- a wrong label is worse than an honest gap, because the
    score is built on these counts.

    One call for the whole batch, never one per prompt.

    PRIVACY: this is the one step that sends prompt text out of the process. The
    prefilter reads text locally and emits only labels; a classifier command may
    send it anywhere. That is why the stage is opt-in and off by default.
    """

    if not texts:
        return []
    payload = json.dumps(texts, ensure_ascii=False)
    try:
        completed = subprocess.run(
            command,
            shell=True,
            input=payload,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return ["unknown"] * len(texts)
    if completed.returncode != 0:
        return ["unknown"] * len(texts)
    try:
        labels = json.loads(completed.stdout)
    except (json.JSONDecodeError, ValueError):
        return ["unknown"] * len(texts)
    if not isinstance(labels, list) or len(labels) != len(texts):
        # A length mismatch means the labels no longer line up with the prompts.
        # Mapping them anyway would attach real labels to the wrong stations.
        return ["unknown"] * len(texts)
    return [
        label if isinstance(label, str) and label in VALID_TYPES else "unknown"
        for label in labels
    ]


def _blank_signals() -> dict[str, Any]:
    return {
        "human_turns": 0,
        "tool_results": 0,
        "errors": 0,
        "tool_use_errors": 0,
        "api_errors": 0,
        "interrupts": 0,
        "tool_chain": [],
    }


def collect_signals(path: Path, stations: list[dict[str, Any]]) -> list[str]:
    """Fill hard signals into ``stations`` in place; return follow-up texts.

    The returned list holds, per station, the text of the first human turn that
    starts *after* that station -- the follow-up prompt that labels it.
    """

    for station in stations:
        station["signals"] = _blank_signals()

    bounds = [(s["start_line"], s["end_line"]) for s in stations]
    follow_up_texts = [""] * len(stations)
    index = 0

    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict):
                continue

            while index < len(bounds) and line_number > bounds[index][1]:
                index += 1
            if index >= len(stations):
                break
            if line_number < bounds[index][0]:
                continue

            signals = stations[index]["signals"]
            record_type = record.get("type")
            blocks = _content_blocks(record)

            if record.get("isApiError"):
                signals["api_errors"] += 1

            if record_type == "assistant":
                for block in blocks:
                    if block.get("type") == "tool_use":
                        name = block.get("name")
                        if isinstance(name, str) and name:
                            signals["tool_chain"].append(name)
            elif record_type == "user":
                results = [b for b in blocks if b.get("type") == "tool_result"]
                if results or record.get("toolUseResult") is not None:
                    signals["tool_results"] += 1
                    for block in results:
                        if block.get("is_error"):
                            signals["errors"] += 1
                        if block.get("tool_use_error"):
                            signals["tool_use_errors"] += 1
                else:
                    text = _text_of(record)
                    if INTERRUPT_MARKER in text:
                        signals["interrupts"] += 1
                    signals["human_turns"] += 1
                    # The first human turn of a station labels the station before it.
                    if index > 0 and not follow_up_texts[index - 1]:
                        follow_up_texts[index - 1] = text
                    if index == 0 and not follow_up_texts[0] and signals["human_turns"] == 1:
                        # Opening prompt of the transcript: labels nothing, marks the start.
                        stations[0]["opening_prompt"] = True

    return follow_up_texts


def _sequence_score(sequence: dict[str, Any], *, repeated: bool) -> tuple[int, list[str]]:
    """Return the harvest score and the reasons that produced it."""

    reasons: list[str] = []
    score = 0

    ko_count = sequence["type_counts"].get("KO", 0)
    if ko_count:
        gain = min(ko_count, 3) * 2
        score += gain
        reasons.append(f"+{gain} {ko_count} Korrektur(en) -- teuer erworbenes Wissen")

    if sequence["closing_type"] == "BE":
        score += 3
        reasons.append("+3 mit Bestaetigung abgeschlossen")

    chain_length = len(sequence["tool_chain"])
    if chain_length >= 3:
        score += 2
        reasons.append(f"+2 Werkzeugkette mit {chain_length} Schritten")

    if repeated:
        score += 2
        reasons.append("+2 Werkzeugkette wiederholt sich ueber Sessions")

    if sequence["closing_type"] == "RA":
        score -= 4
        reasons.append("-4 endet mit Richtungsaenderung -- Sackgasse, nur als Fallstrick wertvoll")

    if sequence["signals"]["errors"] and ko_count:
        score += 1
        reasons.append("+1 Fehlersignal mit folgender Korrektur -- belegter Fallstrick")

    return max(score, 0), reasons


def _chain_signature(tool_chain: list[str]) -> str | None:
    """Collapse consecutive repeats; signatures below three steps are not distinctive."""

    collapsed: list[str] = []
    for name in tool_chain:
        if not collapsed or collapsed[-1] != name:
            collapsed.append(name)
    if len(collapsed) < 3:
        return None
    return ">".join(collapsed)


def build_sequences(stations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group stations into sequences.

    A sequence ends after a direction change (RA, the only soft criterion) or at a
    hard restart marker -- session change, time gap, compact boundary. A new task
    is never *guessed* from the wording of a follow-up prompt: ``SP`` cannot be
    told apart from a plain instruction by a word list, so the deterministic
    markers carry that job instead.
    """

    sequences: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []

    def flush() -> None:
        if not current:
            return
        signals = _blank_signals()
        type_counts: dict[str, int] = {}
        for station in current:
            station_signals = station["signals"]
            for key in ("human_turns", "tool_results", "errors", "tool_use_errors", "api_errors", "interrupts"):
                signals[key] += station_signals[key]
            signals["tool_chain"].extend(station_signals["tool_chain"])
            follow_up = station["follow_up_type"]
            type_counts[follow_up] = type_counts.get(follow_up, 0) + 1
        # Only human utterances can carry a prompt type, so only they belong in
        # the denominator. Counting empty turns and machine envelopes as failures
        # understated the prefilter by ~18 points on real transcripts.
        non_prompt = type_counts.get("non_prompt", 0) + type_counts.get("empty", 0)
        human_prompts = len(current) - non_prompt
        classified = sum(
            count
            for key, count in type_counts.items()
            if key not in ("unknown", "non_prompt", "empty")
        )
        sequences.append(
            {
                "sequence_id": f"sequence-{len(sequences) + 1:04d}",
                "station_ids": [s["station_id"] for s in current],
                "station_count": len(current),
                "session_ids": sorted({sid for s in current for sid in s["session_ids"]}),
                "start_timestamp": current[0]["start_timestamp"],
                "end_timestamp": current[-1]["end_timestamp"],
                "type_counts": dict(sorted(type_counts.items())),
                "human_prompt_count": human_prompts,
                "non_prompt_count": non_prompt,
                "classified_ratio": (
                    round(classified / human_prompts, 3) if human_prompts else 0.0
                ),
                "closing_type": current[-1]["follow_up_type"],
                "tool_chain": signals["tool_chain"],
                "signals": {k: v for k, v in signals.items() if k != "tool_chain"},
            }
        )
        current.clear()

    for station in stations:
        current.append(station)
        if station["follow_up_type"] == "RA" or station["boundary"]["type"] in RESTART_BOUNDARIES:
            flush()
    flush()
    return sequences


def score_files(
    paths: list[Path],
    *,
    gap_seconds: float | None = DEFAULT_GAP_SECONDS,
    min_score: int = 5,
    classifier_cmd: str | None = None,
) -> dict[str, Any]:
    """Segment, sign, classify and score one or more transcripts."""

    all_sequences: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    model_pending: list[tuple[dict[str, Any], str]] = []
    segmented: list[tuple[Path, dict[str, Any], list[dict[str, Any]]]] = []

    for path in paths:
        segmentation = segment_file(path, gap_seconds=gap_seconds)
        stations = segmentation["stations"]
        follow_up_texts = collect_signals(path, stations)
        for position, station in enumerate(stations):
            # The opening prompt of a transcript labels no station -- it starts one.
            text = follow_up_texts[position]
            kind = prompt_kind(text)
            station["follow_up_kind"] = kind
            if kind != "human":
                # No human utterance, so no prompt type to find. Labelled apart
                # from "unknown" so it never counts as a classification failure.
                station["follow_up_type"] = "non_prompt" if kind == "machine" else "empty"
                station["follow_up_source"] = "structure"
                continue
            station["follow_up_type"] = classify_prompt(text)
            station["follow_up_source"] = (
                "prefilter" if station["follow_up_type"] != "unknown" else "none"
            )
            if classifier_cmd and station["follow_up_type"] == "unknown":
                model_pending.append((station, text))
        segmented.append((path, segmentation, stations))

    # The model stage runs BEFORE any sequence is built: type_counts and
    # classified_ratio are computed at sequence level, so a label arriving later
    # would not reach them. One call for every pending prompt across all files.
    model_labelled = 0
    if classifier_cmd and model_pending:
        labels = classify_with_command([text for _, text in model_pending], classifier_cmd)
        for (station, _), label in zip(model_pending, labels):
            if label != "unknown":
                station["follow_up_type"] = label
                station["follow_up_source"] = "model"
                model_labelled += 1

    for path, segmentation, stations in segmented:
        sequences = build_sequences(stations)
        for sequence in sequences:
            sequence["source_name"] = path.name
        all_sequences.extend(sequences)
        sources.append(
            {
                "source_name": path.name,
                "station_count": segmentation["station_count"],
                "sequence_count": len(sequences),
            }
        )

    signature_sessions: dict[str, set[str]] = {}
    for sequence in all_sequences:
        signature = _chain_signature(sequence["tool_chain"])
        sequence["chain_signature"] = signature
        if signature:
            key = sequence["source_name"] + "|" + ",".join(sequence["session_ids"])
            signature_sessions.setdefault(signature, set()).add(key)

    for sequence in all_sequences:
        signature = sequence["chain_signature"]
        repeated = bool(signature and len(signature_sessions[signature]) >= 2)
        sequence["chain_repeated"] = repeated
        score, reasons = _sequence_score(sequence, repeated=repeated)
        sequence["harvest_score"] = score
        sequence["score_reasons"] = reasons
        sequence["candidate"] = score >= min_score

    ranked = sorted(all_sequences, key=lambda s: (-s["harvest_score"], s["sequence_id"]))
    classified_values = [s["classified_ratio"] for s in all_sequences]
    overall_ratio = (
        round(sum(classified_values) / len(classified_values), 3) if classified_values else 0.0
    )

    warnings: list[str] = []
    if overall_ratio < 0.5:
        warnings.append(
            "Weniger als die Haelfte der menschlichen Anschlussprompts konnte "
            "klassifiziert werden -- die Rangfolge ist nicht belastbar. Anschluesse "
            "vor der Ernte manuell oder mit --classifier-cmd nachklassifizieren."
        )
    if classifier_cmd and model_pending and model_labelled == 0:
        # Silence here would look exactly like "the model had nothing to add".
        warnings.append(
            f"--classifier-cmd lieferte fuer keinen der {len(model_pending)} offenen "
            "Anschluesse ein gueltiges Label. Pruefen, ob das Kommando eine "
            "JSON-Liste gleicher Laenge auf stdout schreibt."
        )

    return {
        "schema": SCHEMA,
        "min_score": min_score,
        "sources": sources,
        "sequence_count": len(all_sequences),
        "candidate_count": sum(1 for s in all_sequences if s["candidate"]),
        "classified_ratio": overall_ratio,
        "classification": {
            # How the labels came about -- a ratio lifted by a model is a
            # different claim than one the deterministic prefilter reached.
            "model_stage": bool(classifier_cmd),
            "model_offered": len(model_pending),
            "model_labelled": model_labelled,
        },
        "warnings": warnings,
        "sequences": ranked,
    }


def _write_json(result: dict[str, Any], output: TextIO) -> None:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score station sequences of Claude Code JSONL transcripts by harvest value."
    )
    parser.add_argument("input", type=Path, nargs="+", help="one or more JSONL transcripts")
    parser.add_argument("--output", type=Path, help="write JSON to this file")
    parser.add_argument(
        "--gap-seconds",
        type=float,
        default=DEFAULT_GAP_SECONDS,
        help=(
            "split stations when consecutive timestamped events exceed this gap "
            f"(default: {DEFAULT_GAP_SECONDS:.0f}; 0 disables the split)"
        ),
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=5,
        help="mark sequences at or above this score as candidates (default: 5)",
    )
    parser.add_argument(
        "--candidates-only",
        action="store_true",
        help="only emit sequences that reach --min-score",
    )
    parser.add_argument(
        "--classifier-cmd",
        help=(
            "optional second stage for follow-ups the prefilter left unknown: a "
            "shell command that reads a JSON array of prompt strings on stdin and "
            "writes a JSON array of labels (SP/NT/NM/NS/KO/BE/RA or unknown) of "
            "equal length on stdout. PRIVACY: this sends prompt text to that "
            "command; off by default"
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    gap_seconds = args.gap_seconds if args.gap_seconds else None
    try:
        result = score_files(
            args.input,
            gap_seconds=gap_seconds,
            min_score=args.min_score,
            classifier_cmd=args.classifier_cmd,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.candidates_only:
        result["sequences"] = [s for s in result["sequences"] if s["candidate"]]

    if args.output:
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            _write_json(result, handle)
    else:
        _write_json(result, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
