import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import seclib  # noqa: E402

CLI = ROOT / "scripts" / "secfind.py"


def finding(**over):
    f = {
        "id": seclib.make_id("py.sql-injection", "app/db.py", "cur.execute(q + name)"),
        "rule": "py.sql-injection", "title": "SQL built from request input",
        "cwe": ["CWE-89"], "severity": "high", "confidence": "high", "status": "candidate",
        "location": {"path": "app/db.py", "startLine": 12, "endLine": 14},
        "evidence": "cur.execute(q + name)",
    }
    f.update(over)
    return f


def doc(*findings):
    return {"documentType": "ellmos.sec.findings", "schemaVersion": 1, "scanId": "s1",
            "target": {"repo": "demo", "ref": "working-tree"},
            "provider": {"name": "claude", "model": "m"}, "findings": list(findings)}


def cov(**over):
    c = {"documentType": "ellmos.sec.coverage", "schemaVersion": 1, "scanId": "s1", "complete": True,
         "scanned": [{"path": "app", "depth": "read"}], "notScanned": []}
    c.update(over)
    return c


def test_valid_pair_passes():
    errs, warns = seclib.validate_findings(doc(finding()), cov())
    assert errs == [] and warns == []


def test_missing_coverage_is_an_error():
    errs, _ = seclib.validate_findings(doc(), None)
    assert any("coverage document missing" in e for e in errs)


def test_empty_findings_with_incomplete_coverage_warns():
    c = cov(complete=False, notScanned=[{"path": "vendor", "reason": "too large"}])
    errs, warns = seclib.validate_findings(doc(), c)
    assert errs == [] and any("not a clean result" in w for w in warns)


def test_complete_flag_must_match_not_scanned():
    errs, _ = seclib.validate_findings(doc(), cov(complete=True, notScanned=[{"path": "x", "reason": "r"}]))
    assert any("exactly when notScanned is empty" in e for e in errs)


@pytest.mark.parametrize("secret", [
    "key = 'AKIA" + "ABCDEFGHIJKLMNOP'",
    "tok = 'ghp_" + "a" * 36 + "'",
    "-----BEGIN RSA PRIVATE KEY-----",
])
def test_secret_in_evidence_is_rejected(secret):
    errs, _ = seclib.validate_findings(doc(finding(evidence=secret)), cov())
    assert any("secret" in e for e in errs)


def test_validated_needs_confirmed_validator():
    errs, _ = seclib.validate_findings(doc(finding(status="validated")), cov())
    assert any("validatedBy" in e for e in errs)


def test_same_provider_validation_warns():
    vb = {"provider": "claude", "model": "m", "verdict": "confirmed"}
    errs, warns = seclib.validate_findings(doc(finding(status="validated", validatedBy=vb)), cov())
    assert errs == [] and any("same provider" in w for w in warns)


def test_same_family_subagent_still_warns():
    # a descriptive provider string must not switch the independence check off
    vb = {"provider": "claude-subagent-independent", "model": "opus", "verdict": "confirmed"}
    errs, warns = seclib.validate_findings(doc(finding(status="validated", validatedBy=vb)), cov())
    assert errs == [] and any("same provider" in w for w in warns)


def test_other_provider_validation_is_silent():
    vb = {"provider": "codex", "model": "m", "verdict": "confirmed"}
    errs, warns = seclib.validate_findings(doc(finding(status="validated", validatedBy=vb)), cov())
    assert errs == [] and warns == []


def test_rejected_needs_reason_fixed_needs_patch_verified_needs_verifier():
    assert seclib.validate_findings(doc(finding(status="rejected")), cov())[0]
    vb = {"provider": "codex", "model": "m", "verdict": "confirmed"}
    assert seclib.validate_findings(doc(finding(status="fixed", validatedBy=vb)), cov())[0]
    fixed = finding(status="verified", validatedBy=vb, fix={"patchFile": "p.diff"})
    assert any("verifiedBy" in e for e in seclib.validate_findings(doc(fixed), cov())[0])


def test_duplicate_ids_and_bad_lines_and_bad_cwe():
    f = finding()
    assert any("duplicate" in e for e in seclib.validate_findings(doc(f, copy.deepcopy(f)), cov())[0])
    bad = finding(location={"path": "a", "startLine": 5, "endLine": 2}, cwe=["89"])
    errs = seclib.validate_findings(doc(bad), cov())[0]
    assert any("endLine" in e for e in errs) and any("bad CWE" in e for e in errs)


def test_priority_format():
    assert seclib.validate_findings(doc(finding(priority="P2")), cov())[0] == []
    assert any("priority" in e for e in seclib.validate_findings(doc(finding(priority="high")), cov())[0])


def test_scan_id_mismatch():
    errs, _ = seclib.validate_findings(doc(finding()), cov(scanId="other"))
    assert any("scanId differs" in e for e in errs)


def test_id_is_stable_across_whitespace_but_not_across_content():
    a = seclib.make_id("r", "p.py", "x  =   f(1)")
    assert a == seclib.make_id("r", "p.py", "x = f(1)")
    assert a != seclib.make_id("r", "p.py", "x = f(2)")
    assert a != seclib.make_id("r", "q.py", "x = f(1)")


def test_sarif_levels_and_suppression():
    rejected = finding(status="rejected", rejectedReason="dead code", severity="low",
                       id=seclib.make_id("py.other", "app/db.py", "z"), rule="py.other")
    sarif = seclib.to_sarif(doc(finding(), rejected))
    assert sarif["version"] == "2.1.0"
    res = sarif["runs"][0]["results"]
    assert [r["level"] for r in res] == ["error", "note"]
    assert "suppressions" not in res[0] and res[1]["suppressions"][0]["justification"] == "dead code"
    assert len(sarif["runs"][0]["tool"]["driver"]["rules"]) == 2


def run_cli(*args):
    return subprocess.run([sys.executable, "-I", str(CLI), *args], capture_output=True, text=True)


def test_cli_exit_codes(tmp_path):
    d, c = tmp_path / "f.json", tmp_path / "c.json"
    d.write_text(json.dumps(doc(finding())), encoding="utf-8")
    c.write_text(json.dumps(cov()), encoding="utf-8")
    assert run_cli("validate", str(d), str(c)).returncode == 0
    c.write_text(json.dumps(cov(scanId="x")), encoding="utf-8")
    assert run_cli("validate", str(d), str(c)).returncode == 1
    assert run_cli("validate").returncode == 2
    c.write_text(json.dumps(cov()), encoding="utf-8")
    out = tmp_path / "o.sarif"
    assert run_cli("sarif", str(d), str(c), "-o", str(out)).returncode == 0
    assert json.loads(out.read_text(encoding="utf-8"))["version"] == "2.1.0"


def test_cli_sarif_refuses_invalid_input_and_bad_files(tmp_path):
    d, c = tmp_path / "f.json", tmp_path / "c.json"
    d.write_text(json.dumps(doc(finding())), encoding="utf-8")
    c.write_text(json.dumps(cov()), encoding="utf-8")
    out = tmp_path / "o.sarif"
    # coverage passed as the findings file must not yield an empty-but-valid SARIF
    assert run_cli("sarif", str(c), str(c), "-o", str(out)).returncode == 1
    assert not out.exists()
    # missing and malformed files are error lines, not tracebacks
    missing = run_cli("validate", str(tmp_path / "nope.json"), str(c))
    assert missing.returncode == 1 and "Traceback" not in missing.stderr
    d.write_text("{not json", encoding="utf-8")
    broken = run_cli("validate", str(d), str(c))
    assert broken.returncode == 1 and "Traceback" not in broken.stderr


def test_wrong_types_are_errors_not_crashes():
    broken = [
        ["not a dict"],
        42,
    ]
    for case in broken:
        assert seclib.validate_findings(case, cov())[0]
    bad_docs = [
        doc("string finding"),
        doc(finding(location="app/db.py")),
        doc(finding(validatedBy="codex")),
        doc(finding(status="fixed", fix="p.diff", validatedBy={"provider": "x", "model": "m", "verdict": "confirmed"})),
        doc(finding(evidence=["a", "b"])),
        doc(finding(cwe="CWE-89")),
        doc(finding(id=["x"])),
    ]
    for d in bad_docs:
        errs, _ = seclib.validate_findings(d, cov())
        assert errs, d
    assert seclib.validate_findings(doc(finding()), "not a dict")[0]
    assert seclib.validate_findings(doc(finding()), cov(scanned=["x"], notScanned=["y"], complete=False))[0]


def test_validated_by_needs_provider_and_model():
    vb = {"verdict": "confirmed"}
    errs, _ = seclib.validate_findings(doc(finding(status="validated", validatedBy=vb)), cov())
    assert any("validatedBy: missing 'provider'" in e for e in errs)
    assert any("validatedBy: missing 'model'" in e for e in errs)


def test_secret_in_any_rendered_field_is_rejected():
    secret = "AKIA" + "ABCDEFGHIJKLMNOP"
    for key in ("title", "description", "impact", "recommendation"):
        errs, _ = seclib.validate_findings(doc(finding(**{key: f"key {secret}"})), cov())
        assert any(key in e and "secret" in e for e in errs), key
    rejected = finding(status="rejected", rejectedReason=f"was {secret}")
    assert any("rejectedReason" in e for e in seclib.validate_findings(doc(rejected), cov())[0])
    errs, _ = seclib.validate_findings(doc(finding()), cov(limits=[f"seen {secret}"]))
    assert any("limits" in e for e in errs)


def test_id_is_independent_of_path_spelling():
    a = seclib.make_id("r", "app/db.py", "x")
    assert a == seclib.make_id("r", "app\\db.py", "x") == seclib.make_id("r", "./app/db.py", "x")


def test_absolute_and_backslash_paths_are_rejected():
    for bad in ("C:\\repo\\app.py", "app\\db.py", "/etc/passwd", "./app/db.py", "D:/x.py"):
        f = finding(location={"path": bad, "startLine": 1})
        assert any("repo-relative" in e for e in seclib.validate_findings(doc(f), cov())[0]), bad


def test_triaged_requires_priority():
    vb = {"provider": "codex", "model": "m", "verdict": "confirmed"}
    errs, _ = seclib.validate_findings(doc(finding(status="triaged", validatedBy=vb)), cov())
    assert any("requires priority" in e for e in errs)
    ok, _ = seclib.validate_findings(doc(finding(status="triaged", validatedBy=vb, priority="P2")), cov())
    assert ok == []
