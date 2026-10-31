#!/usr/bin/env python3
"""CLI for the ellmos security contract.

  secfind.py validate findings.json coverage.json   exit 0 ok, 1 errors, 2 usage
  secfind.py sarif findings.json [-o out.sarif]
  secfind.py id RULE PATH SNIPPET_FILE|-             print the stable finding id
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seclib  # noqa: E402


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "validate" and len(argv) == 4:
        errs, warns = seclib.validate_findings(_load(argv[2]), _load(argv[3]))
        for w in warns:
            print("WARN ", w)
        for e in errs:
            print("ERROR", e)
        print("OK" if not errs else f"{len(errs)} error(s)")
        return 1 if errs else 0
    if cmd == "sarif" and len(argv) in (3, 5):
        out = json.dumps(seclib.to_sarif(_load(argv[2])), indent=2)
        if len(argv) == 5 and argv[3] == "-o":
            Path(argv[4]).write_text(out, encoding="utf-8")
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
