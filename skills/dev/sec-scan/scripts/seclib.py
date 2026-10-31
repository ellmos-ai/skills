"""Contract helpers for the ellmos security skill family (stdlib only).

Validates findings/coverage documents, builds stable finding ids and exports SARIF 2.1.0.
The JSON schemas in ../schemas document the shape; the checks here are the executable
version (no jsonschema dependency, so every provider's sandbox can run them).
"""
from __future__ import annotations

import hashlib
import re

SEVERITIES = ("critical", "high", "medium", "low", "info")
CONFIDENCES = ("high", "medium", "low")
STATUSES = ("candidate", "validated", "triaged", "fixed", "verified", "rejected")
VERDICTS = ("confirmed", "refuted", "uncertain")
DEPTHS = ("read", "skimmed", "pattern-only")
NEEDS_CONFIRMED = ("validated", "triaged", "fixed", "verified")

ID_RE = re.compile(r"^SEC-[0-9a-f]{12}$")
PRIORITY_RE = re.compile(r"^P[0-4]$")
CWE_RE = re.compile(r"^CWE-[0-9]+$")
# Evidence must show the code, never the secret itself.
SECRET_RES = [re.compile(p) for p in (
    r"AKIA[0-9A-Z]{16}",
    r"gh[pousr]_[A-Za-z0-9]{36,}",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"xox[abprs]-[A-Za-z0-9-]{10,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
)]
SARIF_LEVEL = {"critical": "error", "high": "error", "medium": "warning", "low": "note", "info": "note"}


def make_id(rule: str, path: str, snippet: str) -> str:
    """Stable id: independent of line numbers, so it survives unrelated edits."""
    norm = " ".join(snippet.split())
    digest = hashlib.sha256(f"{rule}\0{path}\0{norm}".encode("utf-8")).hexdigest()
    return "SEC-" + digest[:12]


def _family(provider: str) -> str:
    """'claude-subagent-independent' and 'claude' are the same provider family."""
    return provider.lower().split("-")[0]


def _req(obj: dict, keys, where: str, errs: list) -> None:
    for k in keys:
        if k not in obj or obj[k] in (None, ""):
            errs.append(f"{where}: missing '{k}'")


def validate_coverage(cov: dict) -> tuple[list, list]:
    errs, warns = [], []
    if cov.get("documentType") != "ellmos.sec.coverage":
        errs.append("coverage: documentType must be 'ellmos.sec.coverage'")
    if cov.get("schemaVersion") != 1:
        errs.append("coverage: schemaVersion must be 1")
    _req(cov, ("scanId",), "coverage", errs)
    for key in ("scanned", "notScanned"):
        if not isinstance(cov.get(key), list):
            errs.append(f"coverage: '{key}' must be a list")
    if not isinstance(cov.get("complete"), bool):
        errs.append("coverage: 'complete' must be a boolean")
    elif isinstance(cov.get("notScanned"), list) and cov["complete"] != (not cov["notScanned"]):
        errs.append("coverage: 'complete' must be true exactly when notScanned is empty")
    for i, s in enumerate(cov.get("scanned") or []):
        _req(s, ("path", "depth"), f"coverage.scanned[{i}]", errs)
        if s.get("depth") not in DEPTHS:
            errs.append(f"coverage.scanned[{i}]: depth must be one of {DEPTHS}")
    for i, s in enumerate(cov.get("notScanned") or []):
        _req(s, ("path", "reason"), f"coverage.notScanned[{i}]", errs)
    return errs, warns


def _check_finding(f: dict, i: int, provider: str | None, errs: list, warns: list) -> None:
    w = f"findings[{i}]"
    _req(f, ("id", "rule", "title", "severity", "confidence", "status", "location", "evidence"), w, errs)
    if f.get("id") and not ID_RE.match(f["id"]):
        errs.append(f"{w}: id must match SEC-<12 hex>")
    if f.get("severity") and f["severity"] not in SEVERITIES:
        errs.append(f"{w}: severity must be one of {SEVERITIES}")
    if f.get("confidence") and f["confidence"] not in CONFIDENCES:
        errs.append(f"{w}: confidence must be one of {CONFIDENCES}")
    status = f.get("status")
    if status and status not in STATUSES:
        errs.append(f"{w}: status must be one of {STATUSES}")
    if f.get("priority") is not None and not PRIORITY_RE.match(str(f["priority"])):
        errs.append(f"{w}: priority must be P0..P4")
    for c in f.get("cwe") or []:
        if not CWE_RE.match(str(c)):
            errs.append(f"{w}: bad CWE '{c}'")
    loc = f.get("location") or {}
    _req(loc, ("path", "startLine"), f"{w}.location", errs)
    start, end = loc.get("startLine"), loc.get("endLine")
    if start is not None and (not isinstance(start, int) or start < 1):
        errs.append(f"{w}.location: startLine must be an integer >= 1")
    elif end is not None and isinstance(start, int) and (not isinstance(end, int) or end < start):
        errs.append(f"{w}.location: endLine must be an integer >= startLine")
    for rx in SECRET_RES:
        if rx.search(str(f.get("evidence", ""))):
            errs.append(f"{w}: evidence appears to contain a secret value - quote the code without the value")
            break
    vb = f.get("validatedBy")
    if status in NEEDS_CONFIRMED:
        if not vb or vb.get("verdict") != "confirmed":
            errs.append(f"{w}: status '{status}' requires validatedBy.verdict == 'confirmed'")
    if vb:
        if vb.get("verdict") not in VERDICTS:
            errs.append(f"{w}: validatedBy.verdict must be one of {VERDICTS}")
        if vb.get("provider") and provider and _family(vb["provider"]) == _family(provider):
            warns.append(f"{w}: validated by the same provider ('{provider}') that found it")
    if status == "rejected" and not f.get("rejectedReason"):
        errs.append(f"{w}: status 'rejected' requires rejectedReason")
    fix = f.get("fix") or {}
    if status in ("fixed", "verified") and not fix.get("patchFile"):
        errs.append(f"{w}: status '{status}' requires fix.patchFile")
    if status == "verified" and not fix.get("verifiedBy"):
        errs.append(f"{w}: status 'verified' requires fix.verifiedBy")


def validate_findings(doc: dict, cov: dict | None) -> tuple[list, list]:
    """Return (errors, warnings). An empty findings list without coverage is an error:
    'nothing found' is only a statement when we know what was looked at."""
    errs, warns = [], []
    if doc.get("documentType") != "ellmos.sec.findings":
        errs.append("documentType must be 'ellmos.sec.findings'")
    if doc.get("schemaVersion") != 1:
        errs.append("schemaVersion must be 1")
    _req(doc, ("scanId",), "doc", errs)
    _req(doc.get("target") or {}, ("repo", "ref"), "target", errs)
    prov = doc.get("provider") or {}
    _req(prov, ("name", "model"), "provider", errs)
    items = doc.get("findings")
    if not isinstance(items, list):
        errs.append("findings must be a list")
        items = []
    seen = set()
    for i, f in enumerate(items):
        _check_finding(f, i, prov.get("name"), errs, warns)
        if f.get("id") in seen:
            errs.append(f"findings[{i}]: duplicate id {f.get('id')}")
        seen.add(f.get("id"))
    if cov is None:
        errs.append("coverage document missing - a result without coverage is not a result")
    else:
        cerrs, cwarns = validate_coverage(cov)
        errs += cerrs
        warns += cwarns
        if cov.get("scanId") != doc.get("scanId"):
            errs.append("scanId differs between findings and coverage")
        if not items and cov.get("complete") is not True:
            warns.append("no findings, but coverage is incomplete - this is not a clean result")
    return errs, warns


def to_sarif(doc: dict) -> dict:
    """SARIF 2.1.0. Rejected findings stay in the log as suppressed, not deleted."""
    rules, results = {}, []
    for f in doc.get("findings", []):
        rules.setdefault(f["rule"], {"id": f["rule"], "name": f["rule"],
                                     "properties": {"tags": f.get("cwe", [])}})
        loc = f["location"]
        region = {"startLine": loc["startLine"]}
        if loc.get("endLine"):
            region["endLine"] = loc["endLine"]
        res = {
            "ruleId": f["rule"],
            "level": SARIF_LEVEL[f["severity"]],
            "message": {"text": f["title"]},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": loc["path"]}, "region": region}}],
            "partialFingerprints": {"ellmosId": f["id"]},
            "properties": {"severity": f["severity"], "confidence": f["confidence"], "status": f["status"]},
        }
        if f["status"] == "rejected":
            res["suppressions"] = [{"kind": "external", "justification": f.get("rejectedReason", "")}]
        results.append(res)
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{"tool": {"driver": {"name": "ellmos-security", "rules": list(rules.values())}},
                  "results": results}],
    }
