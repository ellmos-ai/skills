import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1] / "skills/utilities/decision-draw"
spec = importlib.util.spec_from_file_location("decision_viewer", SKILL / "scripts/decision_viewer.py")
viewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(viewer)


@pytest.fixture
def draft(tmp_path):
    path = tmp_path / "draw-example.json"
    shutil.copyfile(SKILL / "references/example.json", path)
    data, sha, _ = viewer.read(path)
    return path, data, sha


def submit(draft):
    path, data, sha = draft
    choices = viewer.default_choices(data)
    choices["example-results"] = {"accept": False, "comment": "Bitte ändern: äöü\n" * 100}
    return viewer.submit(path, data["revision"], sha, choices)


def test_explicit_submit_and_undo_preserve_choices_and_provenance(draft):
    path, original, sha = draft
    assert path.exists() and viewer.read(path)[0]["state"] == "draft"
    target, result, result_sha = submit(draft)
    assert target.name == "draw-example_decided.json" and target.exists() and not path.exists()
    assert result["submission"]["source_sha256"] == sha
    assert result["submission"]["explicit_full_submission"] is True
    assert result["revision"] == 2
    # Parent rejection never changes the child's independent choice.
    assert result["submission"]["choices"]["example-filters"]["accept"] is True
    prompt = viewer.handoff_prompt(target, result_sha)
    assert str(target.absolute()) in prompt and original["draw_id"] in prompt
    restored_path, restored, _ = viewer.undo(target, result["submission"]["id"], result_sha)
    assert restored_path == path and path.exists() and not target.exists()
    assert restored["revision"] == 3 and restored["state"] == "draft"
    assert restored["history"][-1]["submission_id"] == result["submission"]["id"]
    assert restored["draft_choices"]["example-results"]["comment"].count("äöü") == 100


def test_collision_parallel_windows_and_source_change(draft):
    path, data, sha = draft
    target = path.with_name(path.stem + "_decided.json")
    target.write_text("foreign output", encoding="utf-8")
    with pytest.raises(viewer.DecisionError):
        submit(draft)
    assert target.read_text() == "foreign output" and viewer.read(path)[1] == sha
    target.unlink()
    submit(draft)
    with pytest.raises(OSError):
        submit(draft)  # second stale window cannot find/submit the consumed source


def test_foreign_edit_never_clobbered_by_undo(draft):
    target, result, result_sha = submit(draft)
    raw = target.read_bytes() + b" "
    target.write_bytes(raw)
    with pytest.raises(viewer.DecisionError):
        viewer.undo(target, result["submission"]["id"], result_sha)
    assert target.read_bytes() == raw


def test_recreated_source_blocks_undo_and_consumer(draft):
    original, _, _ = draft
    target, result, result_sha = submit(draft)
    original.write_text("foreign source", encoding="utf-8")
    with pytest.raises(viewer.DecisionError):
        viewer.undo(target, result["submission"]["id"], result_sha)
    with pytest.raises(viewer.DecisionError):
        viewer.mark_processing(target, result_sha, "processing", "test", "example-evidence")
    assert original.read_text() == "foreign source"


def test_processing_claim_blocks_undo_and_other_consumers(draft):
    target, result, result_sha = submit(draft)
    claimed, claimed_sha = viewer.mark_processing(target, result_sha, "processing", "consumer-one", "phase4-plan")
    with pytest.raises(viewer.DecisionError):
        viewer.undo(target, result["submission"]["id"], claimed_sha)
    with pytest.raises(viewer.DecisionError):
        viewer.mark_processing(target, claimed_sha, "processing", "consumer-two", "foreign-plan")
    with pytest.raises(viewer.DecisionError):
        viewer.mark_processing(target, claimed_sha, "processed", "consumer-two", "foreign-result")
    done, _ = viewer.mark_processing(target, claimed_sha, "processed", "consumer-one", "phase4-result")
    assert done["processing"]["state"] == "processed" and done["revision"] == 4
    assert claimed["revision"] == 3


def test_validation_dependencies_and_complete_choices(draft):
    path, data, sha = draft
    choices = viewer.default_choices(data)
    choices.pop("example-filters")
    with pytest.raises(viewer.DecisionError):
        viewer.submit(path, 1, sha, choices)
    assert path.exists()
    bad = copy.deepcopy(data)
    bad["nodes"][0]["depends_on"] = ["missing"]
    with pytest.raises(viewer.DecisionError):
        viewer.validate(bad)
    bad["nodes"][0]["depends_on"] = ["example-filters"]
    with pytest.raises(viewer.DecisionError):
        viewer.validate(bad)


def test_lock_stale_hash_and_repeated_submit_after_undo(draft):
    path, data, sha = draft
    with viewer.locked(path):
        with pytest.raises(viewer.DecisionError):
            submit(draft)
    with pytest.raises(viewer.DecisionError):
        viewer.submit(path, 2, sha, viewer.default_choices(data))
    target, result, result_sha = submit(draft)
    _, restored, restored_sha = viewer.undo(target, result["submission"]["id"], result_sha)
    _, second, _ = viewer.submit(path, restored["revision"], restored_sha, restored["draft_choices"])
    assert second["submission"]["id"] != result["submission"]["id"]
    assert second["revision"] == 4


def test_simultaneous_submit_has_one_winner(draft):
    from concurrent.futures import ThreadPoolExecutor
    def attempt(_):
        try:
            return submit(draft)[0]
        except (viewer.DecisionError, OSError):
            return None
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, range(2)))
    assert sum(item is not None for item in results) == 1
    assert viewer.read(next(item for item in results if item is not None))[0]["state"] == "submitted"


def test_standalone_fresh_skill_copy_and_json_schema(tmp_path):
    copied = tmp_path / "decision-draw"
    shutil.copytree(SKILL, copied)
    result = subprocess.run([sys.executable, str(copied / "scripts/decision_viewer.py"), "validate", str(copied / "references/example.json")], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["draw_id"] == "example-draw"
    import jsonschema
    schema = json.loads((SKILL / "references/draw.schema.json").read_text(encoding="utf-8"))
    example = json.loads((SKILL / "references/example.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(example)


def test_saved_draft_choices_are_validated_before_gui(draft):
    path, data, _ = draft
    valid = viewer.default_choices(data)
    valid["example-results"]["comment"] = "Änderung bitte\n" * 40
    valid["example-results"]["accept"] = False
    data["draft_choices"] = valid
    viewer.validate(data)
    invalid_maps = [None, [], {}, {**valid, "foreign-node": {"accept": True, "comment": ""}}]
    missing = copy.deepcopy(valid)
    missing.pop("example-results")
    invalid_maps.append(missing)
    for field, value in (("accept", 1), ("accept", "yes"), ("comment", None), ("comment", 7)):
        broken = copy.deepcopy(valid)
        broken["example-results"][field] = value
        invalid_maps.append(broken)
    extra_field = copy.deepcopy(valid)
    extra_field["example-results"]["unexpected"] = True
    invalid_maps.append(extra_field)
    for broken in invalid_maps:
        candidate = copy.deepcopy(data)
        candidate["draft_choices"] = broken
        with pytest.raises(viewer.DecisionError):
            viewer.validate(candidate)
    # Even the GUI CLI must reject the minimal repro without importing Tk.
    data["draft_choices"] = {}
    path.write_bytes(viewer.encode(data))
    from unittest.mock import patch
    with patch.dict(sys.modules, {"tkinter": None}), pytest.raises(SystemExit) as error:
        viewer.main(["open", str(path)])
    assert error.value.code == 2


def test_undo_draft_is_schema_and_runtime_valid(draft):
    import jsonschema
    target, submitted, submitted_sha = submit(draft)
    _, restored, _ = viewer.undo(target, submitted["submission"]["id"], submitted_sha)
    schema = json.loads((SKILL / "references/draw.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    validator.validate(restored)
    viewer.validate(restored)
    assert restored["draft_choices"]["example-results"]["accept"] is False
    assert restored["draft_choices"]["example-results"]["comment"].count("äöü") == 100
    broken = copy.deepcopy(restored)
    broken["draft_choices"]["example-results"]["accept"] = 1
    assert not validator.is_valid(broken)
    with pytest.raises(viewer.DecisionError):
        viewer.validate(broken)


def with_preselect(draft, value):
    path, data, _ = draft
    data["preselect"] = value
    path.write_bytes(viewer.encode(data))
    return path, *viewer.read(path)[:2]


def test_default_still_preselects_consent_as_draft(draft):
    _, data, _ = draft
    assert data.get("preselect", "accept") == "accept"
    assert all(item["accept"] is True for item in viewer.initial_choices(data).values())


def test_preselect_none_starts_unanswered_and_blocks_incomplete_submit(draft):
    path, data, sha = with_preselect(draft, "none")
    choices = viewer.initial_choices(data)
    assert set(choices) == {node["id"] for node in viewer.nodes(data)}
    assert all(item["accept"] is None and item["comment"] == "" for item in choices.values())
    decided = path.with_name(path.stem + "_decided.json")
    with pytest.raises(viewer.DecisionError, match="Noch nicht beantwortet"):
        viewer.submit(path, data["revision"], sha, choices)
    choices[next(iter(choices))]["accept"] = True  # one answer is still not a full submission
    with pytest.raises(viewer.DecisionError, match="Noch nicht beantwortet"):
        viewer.submit(path, data["revision"], sha, choices)
    assert path.exists() and not decided.exists() and viewer.read(path)[1] == sha
    for item in choices.values():
        item["accept"] = False  # explicit refusals are answers; nothing is coerced to consent
    _, result, _ = viewer.submit(path, data["revision"], sha, choices)
    assert all(item["accept"] is False for item in result["submission"]["choices"].values())


def test_preselect_value_is_validated_in_runtime_and_schema(draft):
    import jsonschema
    _, data, _ = draft
    schema = json.loads((SKILL / "references/draw.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for value in ("accept", "none"):
        data["preselect"] = value
        viewer.validate(data)
        validator.validate(data)
    for value in ("maybe", True, None, ""):
        data["preselect"] = value
        with pytest.raises(viewer.DecisionError):
            viewer.validate(data)
        assert not validator.is_valid(data)


def test_tk_variable_values_map_to_answers():
    # BooleanVar yields bool; an unset/clicked StringVar yields '', '1' or '0'.
    assert [viewer.as_accept(v) for v in ("", "1", "0", True, False)] == [None, True, False, True, False]


def deep_chain(data, depth):
    """One branch per level, so every level below the first is a collapsed-at-open candidate."""
    chain = None
    for level in range(depth, 0, -1):
        chain = {"id": f"level-{level}", "title": f"Ebene {level}", "text": "t", "source_ref": "s", "recommendation": "r",
                 "alternatives_ref": "a", "addressee": "u", "children": [chain] if chain else []}
    deep = copy.deepcopy(data)
    deep["nodes"] = [chain]
    return deep


def test_deep_branches_are_expanded_at_open_and_must_have_been_shown(draft):
    path, data, _ = draft
    path.write_bytes(viewer.encode(deep_chain(data, 4)))
    deep, sha, _ = viewer.read(path)
    ids = {node["id"] for node in viewer.nodes(deep)}
    assert len(ids) == 4 and viewer.initially_expanded(deep) == ids  # nothing starts collapsed
    choices = viewer.default_choices(deep)
    assert viewer.unseen_ids(deep, {"level-1", "level-2"}) == ["level-3", "level-4"]
    with pytest.raises(viewer.DecisionError, match="Noch nicht angezeigt"):
        viewer.check_ready(deep, choices, {"level-1", "level-2"})
    decided = path.with_name(path.stem + "_decided.json")
    with pytest.raises(viewer.DecisionError, match="Noch nicht angezeigt"):
        viewer.submit(path, deep["revision"], sha, choices, seen={"level-1", "level-2"})
    assert path.exists() and not decided.exists() and viewer.read(path)[1] == sha
    _, result, _ = viewer.submit(path, deep["revision"], sha, choices, seen=ids)
    assert set(result["submission"]["choices"]) == ids


@pytest.mark.skipif(os.environ.get("TM_NATIVE_UI_TEST") != "1", reason="Opt-in native desktop smoke")
def test_native_tree_comment_submit_copy_undo_and_foreign_update(draft):
    import tkinter as tk
    path, _, _ = draft
    root = tk.Tk()
    try:
        window = viewer.DecisionWindow(root, path)
        root.update()
        assert root.winfo_viewable()
        window.rerender(window.expanded, "example-results")
        assert "example-filters" not in window.variables
        window.rerender(window.expanded, "example-results")
        window.rerender(window.comments_open, "example-results")
        window.variables["example-results"].set(False)
        window.comment_widgets["example-results"].insert("1.0", "Änderung bitte\n" * 40)
        window.on_submit()
        root.update()
        assert window.data["state"] == "submitted" and not path.exists()
        window.copy_prompt()
        assert str(window.path) in root.clipboard_get()
        window.on_undo()
        assert window.data["state"] == "draft" and path.exists()
        assert window.choices["example-results"]["comment"].count("Änderung") == 40
        window.on_submit()
        claimed, claimed_sha = viewer.mark_processing(window.path, window.sha, "processing", "test-consumer", "test-only")
        window.watch()
        root.update()
        assert window.data["revision"] == claimed["revision"]
        assert window.undo_button.instate(["disabled"])
        assert viewer.read(window.path)[1] == claimed_sha
    finally:
        root.destroy()
