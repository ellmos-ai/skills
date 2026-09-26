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
hostnames, token patterns) catch this: it needs an actual GitHub visibility
lookup.

## Design decisions (round 2, merge-reviewer measurement on PR #39)

- **Unauthenticated by default, works either way.** The question this gate
  answers is "can a stranger reading this public doc actually reach the
  linked repo?" `GET https://api.github.com/repos/<org>/<repo>` with NO
  token returns 200 for a public repo and 404 for a private one (measured:
  `ellmos-ai/ellmos-core` -> 404, `ellmos-ai/usmc` -> 200) -- and 404 also
  means "does not exist", but a public-facing link pointing at a
  nonexistent repo is equally wrong, so both cases are a confirmed finding,
  not "unknown". Unauthenticated GitHub API calls are capped at 60/hour per
  IP, which in CI (a shared runner IP) is reached fast enough in practice
  that the gate degraded to "warn only" -- so an optional `GH_TOKEN` or
  `GITHUB_TOKEN` env var, if present, is sent as a bearer header purely to
  raise that ceiling. It does NOT change the verdict on its own: on a 200
  response the JSON body's `private` field decides (`true` -> a confirmed
  finding, `false` -> public) instead of assuming 200 always means public --
  that is what makes a token safe to use here. A token whose owner happens
  to have read access to a linked private repo (e.g. its own org's private
  sibling) still gets `private: true` back and the finding still fires;
  only a repo the token cannot see at all still falls through to 404 ->
  finding, same as unauthenticated. 403/429 (rate limit) or a network error
  stay "unknown" either way (warning only). Without a token: exactly the
  previous behaviour (any 200 is public, since an unauthenticated caller
  can only ever get a 200 for an actually-public repo).
- **The REST API, not a HEAD on the web page.** Considered and rejected: the
  web page (`https://github.com/<org>/<repo>`) gives the same 404-for-private-
  or-missing ambiguity with none of the API's benefits (a plain, unambiguous
  status code, no HTML/redirect chain to reason about, no differing behavior
  for org-SSO-enforced repos) -- there is no additional signal to gain from
  it, only more fragility.
- **Fail-open on uncertainty, fail-closed only on a confirmed hit.** A
  network outage or a 403/429 rate limit must never block a commit or PR.
  Only a confirmed 200 (public) or 404 (private-or-nonexistent) is decisive;
  anything else is "unknown" and only ever a warning.
- **Cache only decisive results.** An "unknown" result (typically a rate
  limit) must NOT be cached -- caching it would make the check silently
  toothless for the rest of the cache TTL. Only "public"/"private" are
  written to the cache file (`~/.cache/ellmos-repo-link-visibility/cache.json`,
  24h TTL), which still absorbs the 60/h ceiling for the well-known,
  repeatedly-referenced ecosystem repos across runs.
- **Injectable prober for tests.** `check_visibility()` takes an optional
  `prober` callable so tests never hit the real network or burn real rate
  limit; the default prober performs the (optionally token-bearing) HTTP GET
  described above.

Usage:
    python repo_link_visibility_gate.py --repo <path>            # scan all tracked text files
    python repo_link_visibility_gate.py --repo <path> --paths README.md README_de.md
    python repo_link_visibility_gate.py --repo <path> --no-cache  # force a fresh lookup

Exit 0: no confirmed-private (or confirmed-nonexistent) repo linked
        (rate-limit/network findings are printed as non-blocking warnings).
Exit 1: at least one linked repo is confirmed private or does not exist.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

try:  # reuse the generic tracked-file walker instead of duplicating it
    from testing.repo_privacy_gate import tracked_text_files
except ImportError:  # direct script/module import with testing/ on sys.path
    from repo_privacy_gate import tracked_text_files  # type: ignore[no-redef]

# Greedy captures bounded only by the character class itself -- no lookahead
# assertion. A prior version required the character right after the repo name
# to be one of a fixed set ("/", ")", whitespace, quote, ">"), which silently
# dropped the ENTIRE match for any other terminator: "#readme", "?tab=x", and
# a trailing "," in prose all failed to match at all (round-2 merge-reviewer
# finding). Stopping wherever the character class stops needs no such list --
# "#", "?", "," (and anything else outside the class) end the match on their
# own. What the class DOES still swallow (".git", a trailing sentence period)
# is stripped afterwards in _clean_repo_name(), not fought in the regex.
_GITHUB_LINK = re.compile(r"https://github\.com/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+)")

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

_TRAILING_PUNCTUATION = ".,;:!?)]}>'\""


def _clean_repo_name(repo: str) -> str:
    """Strips a trailing `.git` and/or trailing sentence punctuation that the
    greedy capture above still includes -- repeatedly, since either can
    follow the other (e.g. "ellmos-core.git.", "ellmos-core.git),")."""
    changed = True
    while changed:
        changed = False
        if repo.lower().endswith(".git"):
            repo = repo[:-4]
            changed = True
        if repo and repo[-1] in _TRAILING_PUNCTUATION:
            repo = repo[:-1]
            changed = True
    return repo


def extract_github_repo_links(text: str) -> set[tuple[str, str]]:
    """Returns the set of (org, repo) pairs linked via https://github.com/<org>/<repo>."""
    found = set()
    for org, raw_repo in _GITHUB_LINK.findall(text):
        if org.lower() in _RESERVED_TOP_LEVEL_SEGMENTS:
            continue
        repo = _clean_repo_name(raw_repo)
        if repo:
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
    """GitHub REST API lookup, authenticated only to raise the rate limit
    (see the module docstring for why an authenticated 200 still cannot
    silently mean "public"). Returns "public" (200 with private:false, or a
    200 without a token at all -- an unauthenticated caller can only ever
    get a 200 for an actually-public repo), "private" (404 -- inaccessible
    or nonexistent, both wrong as a public link -- or 200 with
    private:true), or "unknown" (403/429 rate limit, a network error, or an
    unparsable 200 body)."""
    url = f"https://api.github.com/repos/{org}/{repo}"
    headers = {
        "User-Agent": "ellmos-repo-link-visibility-gate",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                return "unknown"
            if not token:
                return "public"
            try:
                body = json.loads(response.read().decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return "unknown"
            is_private = body.get("private")
            if is_private is True:
                return "private"
            if is_private is False:
                return "public"
            return "unknown"  # body without a "private" field -- unexpected shape
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "private"
        return "unknown"  # 403/429 rate limit, or any other unexpected status
    except (urllib.error.URLError, OSError, TimeoutError):
        return "unknown"


def check_visibility(
    org: str, repo: str, *,
    cache: dict | None = None,
    prober: Callable[[str, str], str] = _default_prober,
    use_cache: bool = True,
) -> str:
    """Returns "public", "private", or "unknown". Only a decisive result
    ("public"/"private") is written to `cache` -- "unknown" is never cached,
    so a transient rate limit does not silence the check for the TTL."""
    key = f"{org}/{repo}".lower()
    if use_cache and cache is not None:
        entry = cache.get(key)
        if entry and time.time() - entry.get("checked_at", 0) < _CACHE_TTL_SECONDS:
            return entry["visibility"]
    result = prober(org, repo)
    if cache is not None and result != "unknown":
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
                f"{org}/{repo} is not a public repo (private, or does not "
                f"exist), linked from: {names} -- remove the link or make "
                f"the repo public before publishing."
            )
        elif visibility == "unknown":
            warnings.append(
                f"{org}/{repo}: visibility could not be determined (rate "
                f"limit or network error) -- linked from: {names}. Not "
                f"blocking; re-run later or verify manually."
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

    print("Repo-link visibility gate passed: no confirmed-private or confirmed-missing repo links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
