#!/usr/bin/env python3
"""CLI for the ellmos security contract.

  secfind.py validate findings.json coverage.json          exit 0 ok, 1 errors, 2 usage
  secfind.py sarif findings.json coverage.json [-o out]    validates first; exit 1 and no output on errors
  secfind.py id RULE PATH SNIPPET_FILE|-                    print the stable finding id
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seclib  # noqa: E402


def _load(path):
    """Unreadable or malformed input is a normal error line, not a traceback."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8")), None
    except (OSError, ValueError) as exc:
        return None, f"cannot read {path}: {exc}"


def _validated(findings_path, coverage_path):
    """Return (doc, ok); print every problem. A document is only usable if it validates."""
    doc, err1 = _load(findings_path)
    cov, err2 = _load(coverage_path)
    for err in (err1, err2):
        if err:
            print("ERROR", err)
    if err1 or err2:
        return None, False
    errs, warns = seclib.validate_findings(doc, cov)
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    return doc, not errs


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "validate" and len(argv) == 4:
        _, ok = _validated(argv[2], argv[3])
        if ok:
            print("OK")
        return 0 if ok else 1
    if cmd == "sarif" and len(argv) in (4, 6):
        doc, ok = _validated(argv[2], argv[3])
        if not ok:
            return 1
        out = json.dumps(seclib.to_sarif(doc), indent=2)
        if len(argv) == 6 and argv[4] == "-o":
            Path(argv[5]).write_text(out, encoding="utf-8")
        else:
            print(out)
        return 0
    if cmd == "id" and len(argv) == 5:
        snippet = sys.stdin.read() if argv[4] == "-" else Path(argv[4]).read_text(encoding="utf-8")
        print(seclib.make_id(argv[2], argv[3], snippet))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
