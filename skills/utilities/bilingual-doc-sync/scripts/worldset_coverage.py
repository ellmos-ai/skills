"""Measure World-Set README coverage on the default branches of public GitHub repos.

Read-only. Uses the GitHub CLI (`gh`). Counts, per public, non-archived, non-fork repo with a root
README.md, which target languages have a README/guide variant on the default branch:
`README[._-]<lang>.md` anywhere, or `(docs|i18n|translations|locale(s)|lang)/<lang>/(README|index|guide)*.md`.
README.md is the source language, so each repo has (len(langs) - 1) target slots.

Usage:
  python worldset_coverage.py --orgs ellmos-ai,file-bricks --json out.json
  python worldset_coverage.py --orgs-file orgs.json            # list of org names or {"orgs": [...]}
Exit code 0 on success; the summary goes to stdout.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter

WORLD_SET = ["en", "de", "es", "fr", "pt", "ru", "zh", "ja", "ar", "hi", "bn"]
_FILE = re.compile(r"(?:^|/)readme[._-]([a-z]{2})(?:[-_][a-z]{2,4})?\.md$", re.I)
_DIR = re.compile(r"(?:^|/)(?:docs|i18n|translations|locales?|lang)/([a-z]{2})(?:[-_][a-z]{2,4})?/"
                  r"(?:readme|index|guide)[^/]*\.md$", re.I)
_ROOT_README = re.compile(r"^readme\.md$", re.I)


def languages_in(paths: list[str], langs: list[str] = WORLD_SET) -> set[str]:
    """Language variants (base codes) found among repository paths."""
    found = set()
    for p in paths:
        m = _FILE.search(p) or _DIR.search(p)
        if m and m.group(1).lower() in langs:
            found.add(m.group(1).lower())
    return found


def summarize(rows: list[dict], langs: list[str] = WORLD_SET) -> dict:
    with_readme = [r for r in rows if r["readme"]]
    targets = len(langs) - 1
    filled = sum(min(len(r["langs"]), targets) for r in with_readme)
    slots = len(with_readme) * targets
    return {
        "repos": len(rows),
        "repos_with_readme": len(with_readme),
        "slots": slots,
        "filled": filled,
        "open": slots - filled,
        "open_pct": round(100 * (slots - filled) / slots, 1) if slots else 0.0,
        "per_language": {code: sum(code in r["langs"] for r in with_readme) for code in langs},
        "by_variant_count": dict(sorted(Counter(len(r["langs"]) for r in with_readme).items())),
        "complete": [r["repo"] for r in with_readme if len(r["langs"]) >= targets],
    }


def _gh(args: list[str]) -> str | None:
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def scan(orgs: list[str], langs: list[str] = WORLD_SET) -> list[dict]:
    rows = []
    for org in orgs:
        listing = _gh(["repo", "list", org, "--visibility", "public", "--limit", "500", "--json",
                       "name,isArchived,isFork,defaultBranchRef,stargazerCount"])
        for repo in json.loads(listing or "[]"):
            if repo["isArchived"] or repo["isFork"] or not repo.get("defaultBranchRef"):
                continue
            branch = repo["defaultBranchRef"]["name"]
            tree = _gh(["api", f"repos/{org}/{repo['name']}/git/trees/{branch}?recursive=1", "--jq", ".tree[].path"])
            if tree is None:
                continue
            paths = tree.splitlines()
            rows.append({"repo": f"{org}/{repo['name']}", "stars": repo["stargazerCount"],
                         "readme": any(_ROOT_README.match(p) for p in paths),
                         "langs": sorted(languages_in(paths, langs))})
    return rows


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--orgs", default="", help="comma-separated GitHub owners")
    ap.add_argument("--orgs-file", help="JSON list of owners or object with key 'orgs' or 'organizations'")
    ap.add_argument("--json", help="write per-repo rows and the summary to this file")
    a = ap.parse_args(argv)
    orgs = [o for o in a.orgs.split(",") if o]
    if a.orgs_file:
        data = json.load(open(a.orgs_file, encoding="utf-8"))
        if isinstance(data, dict):  # GithubBot config/orgs.json uses "organizations"
            data = data.get("orgs") or data.get("organizations") or []
        orgs += [o if isinstance(o, str) else o.get("name", "") for o in data
                 if isinstance(o, str) or o.get("enabled", True)]
    if not orgs:
        ap.error("no owners given")
    rows = scan(orgs)
    summary = summarize(rows)
    if a.json:
        json.dump({"summary": summary, "rows": rows}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
