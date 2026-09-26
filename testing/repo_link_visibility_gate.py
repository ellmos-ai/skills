#!/usr/bin/env python3
"""Generic, repository-agnostic check for private-repo links in public docs
(T-20260926-820252321).

Extracted as its own reusable module -- like `repo_privacy_gate.py` -- so it
can be called both from this repository's `privacy_gate.py` and, as a
documented step, from the portable `github-repo-care` skill playbook (which
is used across many repos, not just this one).

Reference case: PR #38 in this repo (T-20260926-413198651) ported an
"Ecosystem & Sibling Projects" table row linking `ellmos-ai/ellmos-core` into
all 6 README language versions. That repo is PRIVATE -- the row had already
been in README.md/README_de.md before the PR and nobody had ever checked
whether the linked repos were actually public. Neither `check_language_parity.py`
(link PARITY between language versions) nor `privacy_gate.py` (local paths,
hostnames, token patterns) catch this: it needs an actual GitHub API lookup.

## Design decisions

- **Fail-open on uncertainty, fail-closed only on a confirmed hit.** A
  network outage, `gh` rate limit, or a 404 (which GitHub also returns for a
  private repo the current token cannot see -- indistinguishable from "does
  not exist") must never block a commit or PR. Only a lookup that positively
  returns `private: true` is a blocking finding. Team-lead instruction
  (T-20260926-820252321): "ohne Netz nur warnen statt blocken."
- **Cache to respect the rate limit.** `gh api` uses the authenticated
  token's higher rate limit (5000/hour), but repeated CI/local runs over the
  same well-known repos (ecosystem siblings referenced from many READMEs)
  would still add up. Results are cached to a small JSON file outside any
  repo (`~/.cache/ellmos-repo-link-visibility/cache.json`) with a TTL, so a
  repeat run across repos or CI jobs on the same day does not re-query.
- **Injectable prober for tests.** `check_visibility()` takes an optional
  `prober` callable so tests never hit the real network or burn real rate
  limit; the default prober shells out to `gh api repos/<org>/<repo>`.

Usage:
    python repo_link_visibility_gate.py --repo <path>            # scan all tracked text files
    python repo_link_visibility_gate.py --repo <path> --paths README.md README_de.md
    python repo_link_visibility_gate.py --repo <path> --no-cache  # force a fresh lookup

Exit 0: no confirmed-private repo linked (network/rate-limit/404 findings are
        printed as non-blocking warnings).
Exit 1: at least one linked repo is confirmed private.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Callable

try:  # reuse the generic tracked-file walker instead of duplicating it
    from testing.repo_privacy_gate import tracked_text_files
except ImportError:  # direct script/module import with testing/ on sys.path
    from repo_privacy_gate import tracked_text_files  # type: ignore[no-redef]

_GITHUB_LINK = re.compile(
    r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?=[/)\s\"'>]|$)"
)

_CACHE_DIR = Path.home() / ".cache" / "ellmos-repo-link-visibility"
_CACHE_FILE = _CACHE_DIR / "cache.json"
_CACHE_TTL_SECONDS = 24 * 60 * 60  # 24h: repo visibility rarely flips same-day

# Not real orgs/repos -- reserved top-level GitHub path segments that would
# otherwise look like an org/repo pair (e.g. github.com/marketplace/actions/x)
# and burn a lookup for nothing.
_RESERVED_TOP_LEVEL_SEGMENTS = {
    "marketplace", "sponsors", "settings", "notifications", "topics",
    "collections", "trending", "explore", "apps", "orgs", "codespaces",
}


def extract_github_repo_links(text: str) -> set[tuple[str, str]]:
    """Returns the set of (org, repo) pairs linked via https://github.com/<org>/<repo>."""
    found = set()
    for org, repo in _GITHUB_LINK.findall(text):
        if org.lower() in _RESERVED_TOP_LEVEL_SEGMENTS:
            continue
        found.add((org, repo))
    return found


def _load_cache() -> dict:
    if not _CACHE_FILE.is_file():
        return {}
    try:
        return json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict) -> None:
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
    except OSError:
        pass  # caching is an optimization, never a hard requirement


def _default_prober(org: str, repo: str) -> str:
    """Returns "public", "private", or "unknown" (network/rate-limit/404/other)."""
    try:
        completed = subprocess.run(
            ["gh", "api", f"repos/{org}/{repo}", "--jq", ".private"],
            capture_output=True, text=True, timeout=15, encoding="utf-8",
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"
    if completed.returncode != 0:
        # Covers 404 (deleted/renamed/private-and-inaccessible -- ambiguous,
        # never a confirmed positive), rate limiting, and auth issues alike.
        return "unknown"
    stdout = completed.stdout.strip().lower()
    if stdout == "true":
        return "private"
    if stdout == "false":
        return "public"
    return "unknown"


def check_visibility(
    org: str, repo: str, *,
    cache: dict | None = None,
    prober: Callable[[str, str], str] = _default_prober,
    use_cache: bool = True,
) -> str:
    """Returns "public", "private", or "unknown", using and updating `cache` in place."""
    key = f"{org}/{repo}".lower()
    if use_cache and cache is not None:
        entry = cache.get(key)
        if entry and time.time() - entry.get("checked_at", 0) < _CACHE_TTL_SECONDS:
            return entry["visibility"]
    result = prober(org, repo)
    if cache is not None:
        cache[key] = {"visibility": result, "checked_at": time.time()}
    return result


def run_gate(
    repo_root: Path,
    paths: list[Path] | None = None,
    *,
    prober: Callable[[str, str], str] = _default_prober,
    use_cache: bool = True,
) -> tuple[list[str], list[str]]:
    """Scans `paths` (or all tracked text files if omitted) for GitHub repo
    links and checks each once. Returns (blocking_findings, warnings)."""
    scan_paths = paths if paths is not None else tracked_text_files(repo_root)

    links: dict[tuple[str, str], list[Path]] = {}
    for path in scan_paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for org_repo in extract_github_repo_links(text):
            links.setdefault(org_repo, []).append(path)

    cache = _load_cache() if use_cache else {}
    findings: list[str] = []
    warnings: list[str] = []
    for (org, repo), sources in sorted(links.items()):
        visibility = check_visibility(org, repo, cache=cache, prober=prober, use_cache=use_cache)
        names = ", ".join(sorted(p.name for p in sources))
        if visibility == "private":
            findings.append(
                f"{org}/{repo} is a PRIVATE repo, linked from: {names} -- "
                f"remove the link or make the repo public before publishing."
            )
        elif visibility == "unknown":
            warnings.append(
                f"{org}/{repo}: visibility could not be determined (network, "
                f"rate limit, or 404) -- linked from: {names}. Not blocking; "
                f"verify manually if this is a new/renamed repo."
            )
    if use_cache:
        _save_cache(cache)
    return findings, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--paths", nargs="+", type=Path, default=None,
        help="Specific files to scan (default: all git-tracked text files).",
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Force a fresh lookup for every linked repo, ignore and skip writing the cache.",
    )
    args = parser.parse_args(argv)
    repo_root = args.repo.resolve()

    if args.paths is None and not (repo_root / ".git").exists():
        print(f"Repo-link visibility gate skipped: {repo_root} is not a git repository root.")
        return 0

    findings, warnings = run_gate(repo_root, args.paths, use_cache=not args.no_cache)

    for warning in warnings:
        print(f"WARNING (non-blocking): {warning}")

    if findings:
        print("Repo-link visibility gate failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Repo-link visibility gate passed: no confirmed-private repo links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
