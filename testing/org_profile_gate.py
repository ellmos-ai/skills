#!/usr/bin/env python3
"""Org-Profilseiten-Gate: findet öffentliche Repos mit Banner, die auf der
Org-Profilseite (`<org>/.github/profile/README.md`) noch fehlen.

Hintergrund (T-20260926-796851315): der User bemerkte, dass ein neu
veröffentlichtes Repo mit Banner (zombie-killer-tray) nicht automatisch auf
der Org-Profilseite (github.com/dev-bricks) auftauchte -- der Einzelfall
ging an zombie-companion, dieser Gate ist der systemische Mechanismus, der
das künftig auffängt.

Prüflogik bewusst einfach gehalten (siehe repo_privacy_gate.py fürs selbe
Prinzip): "hat Banner" = ein getracktes Bild, dessen Pfad "banner" enthält
(assets/banner.png, assets/banner.svg, root banner.png, ...). "Ist auf der
Profilseite" = der rohe Profiltext enthält irgendeine Erwähnung von
`github.com/<org>/<repo>` (Link, Banner-Galerie-Href, Tabellenzeile --
Format der Profilseite bleibt dadurch frei, es gibt keine feste
Tabellenstruktur die geparst werden müsste).

Nutzung (braucht `gh`, bereits authentifiziert):
    python org_profile_gate.py --org dev-bricks
    python org_profile_gate.py --org dev-bricks --org file-bricks --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass

BANNER_PATH_RE = re.compile(r"(?i)(^|/)[a-z0-9_-]*banner[a-z0-9_-]*\.(?:png|svg|jpe?g)$")


@dataclass
class RepoInfo:
    name: str
    tree_paths: list[str]
    default_branch: str


def find_banner_path(tree_paths: list[str]) -> str | None:
    """Returns the first tracked path that looks like a banner image, or None."""
    for path in tree_paths:
        if BANNER_PATH_RE.search(path):
            return path
    return None


def repo_mentioned_in_profile(profile_text: str, org: str, repo: str) -> bool:
    """True if the profile README references this repo in any form (link,
    banner gallery href, table row) -- format-agnostic on purpose.

    A word boundary after the repo name is required, or "RSS-BOOK" would
    also match inside "RSS-BOOKSTORE" (a real pair in file-bricks) -- a
    plain substring check reported that repo as already listed when it
    was not.
    """
    pattern = re.compile(
        r"github\.com/" + re.escape(org) + r"/" + re.escape(repo) + r'(?=[/)#?"\s]|$)',
        re.IGNORECASE,
    )
    return bool(pattern.search(profile_text))


def banner_snippet(org: str, repo: str, banner_path: str, default_branch: str) -> str:
    """Ready-to-paste markdown matching the house style already established
    organically in dev-bricks' own profile README (banner gallery block)."""
    raw_url = f"https://raw.githubusercontent.com/{org}/{repo}/{default_branch}/{banner_path}"
    repo_url = f"https://github.com/{org}/{repo}"
    return (
        f'  <a href="{repo_url}"><img src="{raw_url}" alt="{repo}" width="680" '
        f'style="border-radius:8px;display:block;margin:0 auto 12px"></a>'
    )


def find_missing_entries(
    org: str, repos: list[RepoInfo], profile_text: str
) -> list[dict[str, str]]:
    """Pure, testable core: which repos have a banner but aren't mentioned
    on the org profile page yet."""
    findings = []
    for repo in repos:
        banner_path = find_banner_path(repo.tree_paths)
        if banner_path is None:
            continue
        if repo_mentioned_in_profile(profile_text, org, repo.name):
            continue
        findings.append(
            {
                "org": org,
                "repo": repo.name,
                "banner_path": banner_path,
                "snippet": banner_snippet(org, repo.name, banner_path, repo.default_branch),
            }
        )
    return findings


# ---- Live data gathering (gh CLI) -----------------------------------------


def _gh(*args: str) -> str | None:
    completed = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if completed.returncode != 0:
        print(f"! gh {' '.join(args)} failed: {completed.stderr.strip()}", file=sys.stderr)
        return None
    return completed.stdout


def _public_repos(org: str) -> list[dict]:
    out = _gh(
        "repo", "list", org, "--visibility", "public", "--limit", "300",
        "--json", "name,defaultBranchRef",
    )
    return json.loads(out) if out else []


def _tree_paths(org: str, repo: str) -> list[str]:
    out = _gh("api", f"repos/{org}/{repo}/git/trees/HEAD?recursive=1")
    if not out:
        return []
    data = json.loads(out)
    return [e["path"] for e in data.get("tree", []) if e.get("type") == "blob"]


def _profile_readme(org: str) -> str:
    import base64

    out = _gh("api", f"repos/{org}/.github/contents/profile/README.md")
    if not out:
        return ""
    data = json.loads(out)
    content = data.get("content", "")
    try:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    except (ValueError, TypeError):
        return ""


def scan_org(org: str) -> list[dict[str, str]]:
    profile_text = _profile_readme(org)
    if not profile_text:
        print(f"! {org}: no readable .github/profile/README.md -- skipping", file=sys.stderr)
        return []
    repos = []
    for entry in _public_repos(org):
        name = entry["name"]
        if name == ".github":
            continue  # the profile repo itself, not a product repo
        branch_ref = entry.get("defaultBranchRef") or {}
        default_branch = branch_ref.get("name") or "main"
        repos.append(RepoInfo(name=name, tree_paths=_tree_paths(org, name), default_branch=default_branch))
    return find_missing_entries(org, repos, profile_text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", action="append", required=True, help="Org to scan (repeatable)")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    args = parser.parse_args(argv)

    all_findings = []
    for org in args.org:
        all_findings.extend(scan_org(org))

    if args.json:
        print(json.dumps(all_findings, indent=2, ensure_ascii=False))
    else:
        if not all_findings:
            print("No missing entries found.")
        for f in all_findings:
            print(f"{f['org']}/{f['repo']}: banner at {f['banner_path']}, not on profile page")
            print(f"  Snippet: {f['snippet']}")
    # Exit non-zero on findings so this can gate CI, matching repo_privacy_gate.py's
    # convention (a clean gate exits 0, a finding is a failure to act on).
    return 1 if all_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
