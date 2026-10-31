import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "sec-scan" / "scripts"))
import seclib  # noqa: E402

CLI = ROOT / "scripts" / "render_report.py"


def finding(rule="py.sql-injection", severity="high", status="candidate", **over):
    snippet = "cur.execute(q + name)"
    f = {"id": seclib.make_id(rule, "app/db.py", snippet), "rule": rule, "title": "SQL built from input",
         "cwe": ["CWE-89"], "severity": severity, "confidence": "high", "status": status,
         "location": {"path": "app/db.py", "startLine": 12, "endLine": 14}, "evidence": snippet}
    f.update(over)
    return f


def doc(*findings):
    return {"documentType": "ellmos.sec.findings", "schemaVersion": 1, "scanId": "s1",
            "target": {"repo": "demo", "ref": "working-tree"},
            "provider": {"name": "claude", "model": "m"}, "findings": list(findings)}


def cov(**over):
    c = {"documentType": "ellmos.sec.coverage", "schemaVersion": 1, "scanId": "s1", "complete": True,
         "scanned": [{"path": "app", "depth": "read", "languages": ["python"]}], "notScanned": []}
    c.update(over)
    return c


def run(tmp_path, d, c, *extra):
    (tmp_path / "f.json").write_text(json.dumps(d), encoding="utf-8")
    (tmp_path / "c.json").write_text(json.dumps(c), encoding="utf-8")
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(CLI), str(tmp_path / "f.json"), str(tmp_path / "c.json"), str(out), *extra],
                       capture_output=True, text=True)
    return r, out


def test_report_and_sarif_written(tmp_path):
    rej = finding("js.path-traversal", "medium", "rejected", rejectedReason="sanitised upstream")
    r, out = run(tmp_path, doc(finding(), rej), cov())
    assert r.returncode == 0, r.stdout
    md = (out / "report.md").read_text(encoding="utf-8")
    assert "### high (1)" in md and "cur.execute(q + name)" in md
    assert "Abgelehnte Funde" in md and "sanitised upstream" in md
    assert md.index("### high") < md.index("Abgelehnte Funde")
    sarif = json.loads((out / "findings.sarif").read_text(encoding="utf-8"))
    assert sarif["version"] == "2.1.0" and len(sarif["runs"][0]["results"]) == 2


def test_partial_scan_is_reported_as_partial(tmp_path):
    c = cov(complete=False, notScanned=[{"path": "vendor", "reason": "too large"}])
    r, out = run(tmp_path, doc(), c)
    md = (out / "report.md").read_text(encoding="utf-8")
    assert r.returncode == 0 and "PARTIELLER SCAN" in md and "KEIN sauberes Ergebnis" in md
    assert "Keine Funde bei vollständiger Abdeckung" not in md


def test_clean_complete_scan_and_english(tmp_path):
    r, out = run(tmp_path, doc(), cov(), "--lang", "en")
    assert r.returncode == 0
    assert "No findings with complete coverage." in (out / "report.md").read_text(encoding="utf-8")


def test_evidence_with_backticks_keeps_fence_intact(tmp_path):
    f = finding(evidence="x = ```\nrun()")
    f["id"] = seclib.make_id(f["rule"], "app/db.py", f["evidence"])
    r, out = run(tmp_path, doc(f), cov())
    assert r.returncode == 0 and "````" in (out / "report.md").read_text(encoding="utf-8")


def test_invalid_input_writes_no_report(tmp_path):
    bad = finding(severity="catastrophic")
    r, out = run(tmp_path, doc(bad), cov())
    assert r.returncode == 1 and "no report written" in r.stdout
    assert not out.exists()


def test_missing_coverage_content_writes_no_report(tmp_path):
    r, out = run(tmp_path, doc(), cov(scanId="other"))
    assert r.returncode == 1 and not out.exists()


def test_usage_error(tmp_path):
    r = subprocess.run([sys.executable, str(CLI)], capture_output=True, text=True)
    assert r.returncode == 2
