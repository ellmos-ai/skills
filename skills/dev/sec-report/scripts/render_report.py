#!/usr/bin/env python3
"""Render report.md and findings.sarif from a validated findings/coverage pair (stdlib only).

  render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]    exit 0 ok, 1 invalid input (nothing written), 2 usage

Validation runs first (ellmos security contract, sec-scan/references/contract.md);
a report is never rendered from broken data.
"""
import json
import re
import sys
from pathlib import Path

# sec-scan sits next to this skill, in the repo (skills/dev/...) and in a flat deployment (~/.claude/skills/...)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "sec-scan" / "scripts"))
import seclib  # noqa: E402

L = {
    "de": {
        "title": "Sicherheitsbericht", "target": "Ziel", "provider": "Scanner", "summary": "Zusammenfassung",
        "partial": "PARTIELLER SCAN: {n} Pfad(e) nicht gescannt. Dieser Bericht gilt nur für die gescannten Pfade.",
        "complete": "Vollständige Abdeckung laut coverage.json.",
        "clean": "Keine Funde bei vollständiger Abdeckung.",
        "notclean": "KEIN sauberes Ergebnis: keine Funde, aber unvollständige Abdeckung.",
        "active": "Aktive Funde", "by_sev": "nach Schweregrad", "by_status": "nach Status", "none": "keine",
        "findings": "Funde", "rejected": "Abgelehnte Funde", "reason": "Grund", "coverage": "Abdeckung",
        "scanned": "Gescannt", "notscanned": "Nicht gescannt", "limits": "Grenzen", "warnings": "Warnungen",
        "location": "Ort", "conf": "Konfidenz", "status": "Status", "validated": "Validiert durch",
        "evidence": "Beleg", "description": "Beschreibung", "impact": "Auswirkung",
        "recommendation": "Empfehlung", "ticket": "Ticket", "path": "Pfad", "depth": "Tiefe",
    },
    "en": {
        "title": "Security report", "target": "Target", "provider": "Scanner", "summary": "Summary",
        "partial": "PARTIAL SCAN: {n} path(s) not scanned. This report only covers the scanned paths.",
        "complete": "Complete coverage according to coverage.json.",
        "clean": "No findings with complete coverage.",
        "notclean": "NOT a clean result: no findings, but coverage is incomplete.",
        "active": "Active findings", "by_sev": "by severity", "by_status": "by status", "none": "none",
        "findings": "Findings", "rejected": "Rejected findings", "reason": "Reason", "coverage": "Coverage",
        "scanned": "Scanned", "notscanned": "Not scanned", "limits": "Limits", "warnings": "Warnings",
        "location": "Location", "conf": "Confidence", "status": "Status", "validated": "Validated by",
        "evidence": "Evidence", "description": "Description", "impact": "Impact",
        "recommendation": "Recommendation", "ticket": "Ticket", "path": "Path", "depth": "Depth",
    },
}


def _fence(text: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def _loc(f: dict) -> str:
    loc = f["location"]
    end = f" - {loc['endLine']}" if loc.get("endLine") else ""
    return f"`{loc['path']}:{loc['startLine']}{end}`"


def _finding(f: dict, t: dict) -> list:
    out = [f"#### {f['id']} - {f['title']}", ""]
    meta = [f"{t['location']}: {_loc(f)}", f"{t['conf']}: {f['confidence']}", f"{t['status']}: {f['status']}",
            f"rule: `{f['rule']}`"]
    if f.get("cwe"):
        meta.append("CWE: " + ", ".join(f["cwe"]))
    vb = f.get("validatedBy")
    if vb:
        meta.append(f"{t['validated']}: {vb['provider']} / {vb['model']} ({vb['verdict']})")
    if f.get("ticket"):
        meta.append(f"{t['ticket']}: {f['ticket']}")
    out += ["- " + m for m in meta] + ["", f"**{t['evidence']}**", ""]
    fence = _fence(f["evidence"])
    out += [fence, f["evidence"].rstrip("\n"), fence, ""]
    for key in ("description", "impact", "recommendation"):
        if f.get(key):
            out += [f"**{t[key]}**: {f[key]}", ""]
    return out


def render(doc: dict, cov: dict, warns: list, lang: str = "de") -> str:
    t = L[lang]
    findings = doc["findings"]
    active = [f for f in findings if f["status"] != "rejected"]
    rejected = [f for f in findings if f["status"] == "rejected"]
    tgt, prov = doc["target"], doc["provider"]
    out = [f"# {t['title']} - {doc['scanId']}", "",
           f"- {t['target']}: `{tgt['repo']}` @ `{tgt['ref']}`",
           f"- {t['provider']}: {prov['name']} / {prov['model']}" + (f" ({prov['engine']})" if prov.get("engine") else ""),
           "", f"## {t['summary']}", ""]
    if not cov["complete"]:
        out += [f"**{t['partial'].format(n=len(cov['notScanned']))}**", ""]
    else:
        out += [t["complete"], ""]
    if not findings:
        out += [f"**{t['clean'] if cov['complete'] else t['notclean']}**", ""]
    else:
        sev = ", ".join(f"{s}: {n}" for s in seclib.SEVERITIES if (n := sum(f["severity"] == s for f in active)))
        sta = ", ".join(f"{s}: {n}" for s in seclib.STATUSES if (n := sum(f["status"] == s for f in findings)))
        out += [f"- {t['active']}: {len(active)}",
                f"- {t['by_sev']}: {sev or t['none']}", f"- {t['by_status']}: {sta}", ""]
    if warns:
        out += [f"## {t['warnings']}", ""] + [f"- {w}" for w in warns] + [""]
    out += [f"## {t['findings']}", ""]
    if not active:
        out += [t["none"], ""]
    for s in seclib.SEVERITIES:
        group = [f for f in active if f["severity"] == s]
        if group:
            out += [f"### {s} ({len(group)})", ""]
            for f in group:
                out += _finding(f, t)
    if rejected:
        out += [f"## {t['rejected']}", "", f"| id | rule | {t['location']} | {t['reason']} |", "|---|---|---|---|"]
        out += [f"| {f['id']} | `{f['rule']}` | {_loc(f)} | {f['rejectedReason'].replace('|', '/')} |" for f in rejected]
        out.append("")
    out += [f"## {t['coverage']}", "", f"### {t['scanned']}", ""]
    if cov["scanned"]:
        out += [f"| {t['path']} | {t['depth']} | languages |", "|---|---|---|"]
        out += [f"| `{s['path']}` | {s['depth']} | {', '.join(s.get('languages') or [])} |" for s in cov["scanned"]]
    else:
        out.append(t["none"])
    out += ["", f"### {t['notscanned']}", ""]
    out += [f"- `{s['path']}`: {s['reason']}" for s in cov["notScanned"]] or [t["none"]]
    if cov.get("limits"):
        out += ["", f"### {t['limits']}", ""] + [f"- {x}" for x in cov["limits"]]
    return "\n".join(out) + "\n"


def main(argv: list) -> int:
    rest = argv[1:]
    lang = "de"
    args = []
    skip = False
    for i, a in enumerate(rest):
        if skip:
            skip = False
        elif a == "--lang":
            lang = rest[i + 1] if i + 1 < len(rest) else ""
            skip = True
        elif a.startswith("--lang="):
            lang = a.split("=", 1)[1]
        else:
            args.append(a)
    if len(args) != 3 or lang not in L:
        print(__doc__)
        return 2
    try:
        doc = json.loads(Path(args[0]).read_text(encoding="utf-8"))
        cov = json.loads(Path(args[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"ERROR cannot read input: {e}")
        return 1
    errs, warns = seclib.validate_findings(doc, cov)
    if errs:
        for e in errs:
            print("ERROR", e)
        print(f"{len(errs)} error(s) - no report written")
        return 1
    out = Path(args[2])
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(render(doc, cov, warns, lang), encoding="utf-8")
    (out / "findings.sarif").write_text(json.dumps(seclib.to_sarif(doc), indent=2), encoding="utf-8")
    for w in warns:
        print("WARN ", w)
    print(f"OK: {out / 'report.md'}, {out / 'findings.sarif'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
