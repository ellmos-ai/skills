#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provider-neutral, approval-gated community-outreach state machine.

The core never performs a live post by itself. A caller may inject a publisher,
but local state advances only after a complete, target-bound PublishReceipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]

DEFAULT_PLATFORM_ROTATION = ["Reddit", "YouTube", "GitHub Discussions", "Foren"]
DEFAULT_EXCLUDED_ORGS = {"biotec-line"}
DEFAULT_PRIMARY_ORGS = ("ellmos-ai", "dev-bricks", "file-bricks", "doc-bricks", "open-bricks")
DEFAULT_DISCOURSE_ORGS = {"research-line"}
DEFAULT_EXCLUDED_REPOS: set[str] = set()
CORE_ECOSYSTEM_FLAGSHIPS = {"ellmos-ai/bach", "ellmos-ai/open-ocean", "ellmos-ai/skills"}
TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
}
PROPOSAL_HEADING_RE = re.compile(
    r"^###\s+(?:"
    r"\[(?P<id>OUTBOUND-PROPOSAL-[^\]]+|INBOUND-REPLY-[^\]]+)\]\s+(?P<title>[^\n]+)"
    r"|Post-Entwurf(?:\s+#\d+|\s+--\s+[^\n]+))\s*$"
)
OUTBOX_ENTRY_RE = re.compile(
    r"^###\s+(?:\[[^\]]+\]\s+Veröffentlicht\b.*|Post\s+(?:--\s+.+|#\d+\b.*))$"
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def canonicalize_url(url: str) -> str:
    """Return a comparison key without fuzzy substring matching.

    Tracking parameters are removed. Reddit host/path casing and common
    YouTube URL forms are normalized while meaningful generic query values are
    retained.
    """

    value = str(url or "").strip()
    if not value:
        return ""
    try:
        parsed = urlsplit(value)
        parsed_port = parsed.port
    except ValueError:
        return ""
    if not parsed.scheme or not parsed.netloc:
        return value.rstrip("/").lower()

    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    port = parsed_port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        host = f"{host}:{port}"

    query_items = [(key, val) for key, val in parse_qsl(parsed.query, keep_blank_values=True) if key.lower() not in TRACKING_QUERY_KEYS]
    path = re.sub(r"/{2,}", "/", parsed.path or "/")

    if host in {"youtu.be", "www.youtu.be"}:
        video_id = path.strip("/").split("/", 1)[0]
        return f"https://youtube.com/watch?v={video_id}" if video_id else "https://youtube.com"

    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        host = "youtube.com"
        if path.rstrip("/") == "/watch":
            video_ids = [val for key, val in query_items if key == "v"]
            if video_ids:
                return f"https://youtube.com/watch?v={video_ids[0]}"
        match = re.match(r"^/(?:shorts|embed)/([^/]+)", path)
        if match:
            return f"https://youtube.com/watch?v={match.group(1)}"

    if host in {"reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com"}:
        scheme = "https"
        host = "reddit.com"
        path = path.rstrip("/").lower() or "/"
        query_items = []
    else:
        path = path.rstrip("/") or "/"

    query = urlencode(sorted(query_items), doseq=True)
    return urlunsplit((scheme, host, path, query, ""))


def _is_valid_target_url(url: str) -> bool:
    try:
        parsed = urlsplit(str(url).strip())
        _ = parsed.port
    except ValueError:
        return False
    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)


def _normalize_repo_reference(value: object) -> str:
    reference = str(value or "").strip().strip("`").rstrip("/")
    if "://" in reference:
        parsed = urlsplit(reference)
        reference = parsed.path.strip("/")
    if reference.lower().endswith(".git"):
        reference = reference[:-4]
    return reference.casefold()


def _extract_repo_org(repo_or_ref: object) -> str:
    if isinstance(repo_or_ref, Mapping):
        org = str(repo_or_ref.get("org", "")).strip().casefold()
        if org:
            return org
        ref = _normalize_repo_reference(repo_or_ref.get("id", "") or repo_or_ref.get("url", ""))
        return ref.split("/", 1)[0] if "/" in ref else ""
    ref = _normalize_repo_reference(repo_or_ref)
    return ref.split("/", 1)[0] if "/" in ref else ""


def _same_repo(left: object, right: object) -> bool:
    left_ref = _normalize_repo_reference(left)
    right_ref = _normalize_repo_reference(right)
    if not left_ref or not right_ref:
        return False
    if left_ref == right_ref:
        return True
    if "/" in left_ref and "/" in right_ref:
        return False
    return left_ref.rsplit("/", 1)[-1] == right_ref.rsplit("/", 1)[-1]


def _public_repo_gate(repo: Mapping[str, Any]) -> tuple[bool, bool]:
    """Shared fail-closed gate: github_meta must positively confirm public, non-archived,
    non-fork, set by --sync-githubbot or when bootstrapping the catalog.

    Returns (passes, unverified_visibility). Used by BOTH select_candidate_repository
    (stage 1/2) and the stage-3 new-proposal pool -- a repo must clear this gate no matter
    which stage considers it. Merge-reviewer fix (T-20260926-665406367): stage 3 previously
    only checked `active`/`exclusion_reason` and could surface private, archived, forked or
    never-synced repos for outreach, most dangerously in exactly the case where the reason
    was "visibility-unverified" -- a missing sync must never be routed around this way.
    """
    gh_meta = repo.get("github_meta") or {}
    if gh_meta.get("visibility") != "public":
        return False, True
    if gh_meta.get("archived") is not False:
        return False, False
    if gh_meta.get("fork") is not False:
        return False, False
    return True, False


def _repo_matches_catalog_entry(repo: Mapping[str, Any], published_repo: object) -> bool:
    published_ref = _normalize_repo_reference(published_repo)
    qualified = {
        reference
        for reference in (
            _normalize_repo_reference(repo.get("id", "")),
            _normalize_repo_reference(repo.get("url", "")),
        )
        if "/" in reference
    }
    if "/" in published_ref and qualified:
        return published_ref in qualified
    return _same_repo(repo.get("name", ""), published_ref)


@dataclass(frozen=True)
class PublishReceipt:
    """Evidence returned by a publisher after a verified external write."""

    platform_post_id: str
    published_url: str
    target_url: str
    platform: str
    published_at: str

    @classmethod
    def validate(cls, value: object, proposal: Mapping[str, Any]) -> PublishReceipt | None:
        if isinstance(value, cls):
            candidate: Mapping[str, Any] = {
                "verified": True,
                "platform_post_id": value.platform_post_id,
                "published_url": value.published_url,
                "target_url": value.target_url,
                "platform": value.platform,
                "published_at": value.published_at,
            }
        elif isinstance(value, Mapping):
            candidate = value
        else:
            return None

        required = ("platform_post_id", "published_url", "target_url", "platform", "published_at")
        if candidate.get("verified") is not True or any(not str(candidate.get(key, "")).strip() for key in required):
            return None
        if canonicalize_url(str(candidate["target_url"])) != canonicalize_url(str(proposal.get("target_url", ""))):
            return None
        if str(candidate["platform"]).strip().casefold() != str(proposal.get("platform", "")).strip().casefold():
            return None
        if not _is_valid_target_url(str(candidate["published_url"])):
            return None
        try:
            published_at = datetime.fromisoformat(str(candidate["published_at"]).replace("Z", "+00:00"))
        except ValueError:
            return None
        if published_at.tzinfo is None:
            return None
        return cls(
            platform_post_id=str(candidate["platform_post_id"]).strip(),
            published_url=str(candidate["published_url"]).strip(),
            target_url=str(candidate["target_url"]).strip(),
            platform=str(candidate["platform"]).strip(),
            published_at=str(candidate["published_at"]).strip(),
        )


class FileReceiptPublisher:
    """Provider-neutral publisher: feeds back a receipt an agent already captured.

    T-20260926-665406367 (posting je App): the actual post -- via open-compute, Playwright,
    Claude-in-Chrome, or a platform API, whichever the calling app's own session can use --
    happens BEFORE this is invoked. This class performs no network action and no browser
    automation itself; it only hands the already-captured evidence to the engine's existing,
    unchanged verification (PublishReceipt.validate still enforces platform/target_url/format
    match, so a wrong or incomplete receipt is rejected exactly as before). Bound to exactly
    one proposal id so a receipt can never be misapplied to a different, unrelated post.
    """

    def __init__(self, receipt_path: str | Path, proposal_id: str):
        self.receipt_path = Path(receipt_path)
        self.proposal_id = proposal_id

    def publish(self, proposal: Mapping[str, Any]) -> Mapping[str, Any]:
        if proposal.get("id") != self.proposal_id:
            raise ValueError(
                f"receipt is bound to proposal {self.proposal_id!r}, not {proposal.get('id')!r} "
                "-- refusing to apply it to a different post"
            )
        data = _read_json(self.receipt_path, None)
        if not isinstance(data, Mapping):
            raise ValueError(f"receipt file {self.receipt_path} is missing or not valid JSON")
        if data.get("proposal_id") != self.proposal_id:
            raise ValueError(
                f"receipt file's proposal_id {data.get('proposal_id')!r} does not match "
                f"--receipt-proposal-id {self.proposal_id!r}"
            )
        return data


class HistoryUnreadable(ValueError):
    """posts_history.json exists but cannot be trusted; nothing may be derived from or written over it."""


# Cut-and-Clue variant A: registers are split before they grow past ~200 lines
REGISTRY_MAX_ROWS = 150
PUBLICATION_STATUSES = ("entwurf", "freigegeben", "veroeffentlicht", "unbestaetigt")


def publication_status(record: Mapping[str, Any]) -> str:
    """History records are 'veroeffentlicht' only with a verified receipt, otherwise 'unbestaetigt'."""
    verified = record.get("status") == "published" and record.get("receipt_verified") is True
    if record.get("publication_status") == "unbestaetigt" or not verified:
        return "unbestaetigt"
    return "veroeffentlicht"


def _registry_cell(value: object) -> str:
    text = " ".join(str(value if value is not None else "").split())
    for char in "\\`*_[]|<>":
        text = text.replace(char, "\\" + char)
    return text


def _registry_link(url: object, label: str | None = None) -> str:
    url = str(url or "").strip()
    if not _is_valid_target_url(url) or any(c.isspace() or c in "<>()\"'`|" for c in url):
        return label or _registry_cell(url)
    return f"[{label or _registry_cell(url)}]({url})"


def _fenced_cell(value: object) -> str:
    """Escape text for embedding inside a ```text fence: break any run of
    3+ backticks so foreign content (e.g. a quoted Reddit comment) can't
    close the fence early and inject markdown/HTML into the document."""
    text = str(value if value is not None else "")
    return re.sub(r"`{3,}", lambda m: "​".join(m.group()), text)


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        temporary.write_text(content, encoding="utf-8", newline="")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _atomic_write_json(path: Path, data: object) -> None:
    _atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _extract_url(field_value: str) -> str:
    value = field_value.strip()
    markdown = re.search(r"\[[^\]]*\]\(([^)]+)\)", value)
    if markdown:
        return markdown.group(1).strip()
    angle = re.search(r"<([^>]+)>", value)
    if angle:
        return angle.group(1).strip()
    return value.strip("` ")


def _markdown_h3_headings(content: str) -> list[tuple[int, str]]:
    """Return H3 headings outside fenced code blocks with byte-safe offsets."""

    headings: list[tuple[int, str]] = []
    offset = 0
    fence: str | None = None
    for line in content.splitlines(keepends=True):
        stripped = line.lstrip()
        fence_match = re.match(r"(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            fence = None if fence == marker else (marker if fence is None else fence)
        elif fence is None and line.startswith("### "):
            headings.append((offset, line.rstrip("\r\n")))
        offset += len(line)
    return headings


def _parse_proposals(content: str) -> list[dict[str, Any]]:
    all_headings = _markdown_h3_headings(content)
    starts: list[tuple[int, re.Match[str]]] = []
    for start, line in all_headings:
        match = PROPOSAL_HEADING_RE.fullmatch(line)
        if match:
            starts.append((start, match))
    proposals: list[dict[str, Any]] = []
    heading_offsets = [start for start, _line in all_headings]
    for heading_start, heading in starts:
        segment_end = next((start for start in heading_offsets if start > heading_start), len(content))
        segment = content[heading_start:segment_end]
        approval = re.search(r"-\s*\[([ xX])\]\s*Genehmigt\b", segment)
        platform = re.search(r"-\s*\*\*Plattform:\*\*\s*([^\n]+)", segment)
        target = re.search(r"-\s*\*\*Ziel-URL(?:\s*/\s*Thread)?:\*\*\s*([^\n]+)", segment)
        repo = re.search(r"-\s*\*\*(?:Lösungs-Repo|Repository):\*\*\s*([^\n]+)", segment)
        code_evidence = re.search(r"-\s*\*\*Code-Beleg(?:\s*\([^\)]*\))?:\*\*\s*([^\n]+)", segment)
        context_check = re.search(r"-\s*\*\*Umgebungs-Check(?:\s*\([^\)]*\))?:\*\*\s*([^\n]+)", segment)
        claim_contract = re.search(
            r"####\s+Claim-Beleg-Vertrag(?:\s*\([^\)]*\))?:\s*\n"
            r"```(?:json)?[ \t]*\n(.*?)\n```",
            segment,
            re.DOTALL,
        )
        post_text = re.search(
            r"(?:####\s+Textvorschlag:|\*\*Vorgeschlagener Beitrag:\*\*)\s*\n"
            r"```(?:markdown|text)?[ \t]*\n(.*?)\n```",
            segment,
            re.DOTALL,
        )
        if not all((approval, platform, target, repo, post_text)):
            continue

        semantic_end = max(post_text.end(), claim_contract.end() if claim_contract else 0)
        trailing = re.match(r"[ \t]*(?:\r?\n[ \t]*)*", segment[semantic_end:])
        if trailing:
            semantic_end += trailing.end()
        raw_block = segment[:semantic_end]
        proposal_id = heading.group("id")
        if not proposal_id:
            digest = hashlib.sha256(raw_block.encode("utf-8")).hexdigest()[:12].upper()
            proposal_id = f"OUTBOUND-PROPOSAL-LEGACY-{digest}"

        repo_value = repo.group(1).strip().strip("`")
        repo_link = re.search(r"\[([^\]]+)\]\(([^)]+)\)", repo_value)
        proposals.append(
            {
                "id": proposal_id,
                "title": (heading.group("title") or heading.group(0).removeprefix("###").strip()),
                "platform": platform.group(1).strip(),
                "target_url": _extract_url(target.group(1)),
                "repo": repo_link.group(1).strip() if repo_link else repo_value,
                "repo_url": repo_link.group(2).strip() if repo_link else "",
                "code_evidence": code_evidence.group(1).strip() if code_evidence else "",
                "context_check": context_check.group(1).strip() if context_check else "",
                "claim_contract_raw": claim_contract.group(1).strip() if claim_contract else "",
                "text": post_text.group(1).strip(),
                "approved": approval.group(1).lower() == "x",
                "raw_block": raw_block,
                "span": (heading_start, heading_start + semantic_end),
            }
        )
    return proposals


def _check_natural_human_style(text: str, platform: str = "") -> list[str]:
    """Detect unmistakable LLM/AI-essay formatting tells in community comments.

    Human comments on Reddit, YouTube, and forums are short, conversational paragraphs
    without Markdown section headers (###), bolded bullet-list definitions (- **Label:**),
    inline **bold** buzzword highlighting, em-dashes (—), or 2,500+ char structured essays.
    """
    violations: list[str] = []
    body = str(text or "").strip()
    if not body:
        return ["empty-text"]

    prose = re.sub(r"```.*?```", "", body, flags=re.DOTALL)

    if re.search(r"(?m)^\s*#{1,6}\s+\S", prose):
        violations.append("markdown-headings-forbidden")
    if re.search(r"\*\*[^*\n]+\*\*", prose):
        violations.append("bold-markup-forbidden")
    if "\u2014" in prose:
        violations.append("em-dash-forbidden")
    bullet_lines = re.findall(r"(?m)^\s*(?:[-*]|\d+\.)\s+\S", prose)
    if len(bullet_lines) >= 3:
        violations.append("structured-list-essay-forbidden")
    max_len = 1200 if str(platform or "").strip().casefold() in {"reddit", "youtube"} else 1500
    if len(body) > max_len:
        violations.append(f"excessive-length-{len(body)}-gt-{max_len}")
    if re.search(
        r"\b(?:here are (?:two|three|four) (?:practical |architectural )?(?:patterns|approaches)|"
        r"here is the architectural pattern|spot[- ]on thesis|really insightful breakdown|"
        r"treating [a-z0-9 _-]+ as [a-z0-9 _-]+ gives you)\b",
        prose,
        re.IGNORECASE,
    ):
        violations.append("ai-cliche-phrasing")
    return violations


_SOURCE_CODE_EXT_RE = re.compile(
    r"\.(?:py|ts|tsx|js|jsx|mjs|cjs|rs|go|c|cpp|h|hpp|cs|java|kt|swift|sql|sh|ps1)$",
    re.IGNORECASE,
)
_MENTIONED_CODE_FILE_RE = re.compile(
    r"(?<![/\w.-])([A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*\.(?:py|ts|tsx|js|jsx|rs|go|toml))(?!\.[A-Za-z0-9_]|[\w-])"
)
_ZERO_DEP_CLAIM_RE = re.compile(
    r"\b(?:zero[- ]dependenc(?:y|ies)|zero runtime dependencies|"
    r"no (?:external |runtime )?dependencies|stdlib[- ]only|pure standard library)\b",
    re.IGNORECASE,
)
_AMBIGUOUS_CAPITALIZED_REPO_NAMES = {
    "anonymizer",
    "bundles",
    "clutch",
    "coma",
    "connectors",
    "gardener",
    "profiler",
    "stacks",
}
_QUALIFIED_ONLY_REPO_NAMES = {
    "skills",
    "web",
    "think",
    "decide",
    "condition",
    "headless",
    "migration",
    "slideshow",
    "figma",
    "swarm",
}


def _resolve_repo_clone(repos_root: Path, repo_ref: object) -> tuple[Path | None, Path | None, str]:
    raw_repo_ref = _normalize_repo_reference(repo_ref)
    skill_rel_dir: Path | None = None
    if (
        raw_repo_ref.startswith("skills/")
        or "/tree/master/skills/" in raw_repo_ref
        or "/tree/main/skills/" in raw_repo_ref
    ):
        repo_slug = "skills"
        if "/tree/master/" in raw_repo_ref:
            skill_rel_dir = Path(raw_repo_ref.split("/tree/master/", 1)[1])
        elif "/tree/main/" in raw_repo_ref:
            skill_rel_dir = Path(raw_repo_ref.split("/tree/main/", 1)[1])
        else:
            skill_rel_dir = Path(raw_repo_ref)
    else:
        repo_slug = raw_repo_ref.rsplit("/", 1)[-1]
    repo_dir = (repos_root / repo_slug) if repo_slug else None
    return repo_dir, skill_rel_dir, repo_slug


def _parse_line_range(lines_spec: object, max_span: int = 80) -> tuple[int, int] | None:
    if isinstance(lines_spec, int):
        return (lines_spec, lines_spec) if lines_spec >= 1 else None
    raw = str(lines_spec or "").strip()
    match = re.fullmatch(r"L?(\d+)(?:\s*-\s*L?(\d+))?", raw, re.IGNORECASE)
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else start
    if start < 1 or end < start or (end - start) > max_span:
        return None
    return start, end


def _git_tracked_files(repo_dir: Path, cache: dict[Path, set[str] | None]) -> set[str] | None:
    resolved = repo_dir.resolve()
    if resolved in cache:
        return cache[resolved]
    if not (resolved / ".git").exists():
        cache[resolved] = None
        return None
    try:
        proc = subprocess.run(
            ["git", "-C", str(resolved), "-c", "core.quotepath=false", "ls-files"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except OSError:
        cache[resolved] = None
        return None
    if proc.returncode != 0:
        cache[resolved] = set()
        return cache[resolved]
    tracked = {line.strip().replace("\\", "/") for line in proc.stdout.splitlines() if line.strip()}
    cache[resolved] = tracked
    return tracked


def _split_into_paragraphs_and_sentences(text: str) -> list[list[str]]:
    norm = str(text or "").replace("\r\n", "\n").strip()
    if not norm:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", norm) if p.strip()]
    result: list[list[str]] = []
    for para in paragraphs:
        masked = re.sub(r"https?://\S+", lambda m: "X" * len(m.group(0)), para)
        masked = re.sub(
            r"\b(?:e\.g|i\.e|vs|etc|cf|approx|min|max)\.",
            lambda m: "X" * len(m.group(0)),
            masked,
            flags=re.IGNORECASE,
        )
        sentences: list[str] = []
        last_idx = 0
        for boundary in re.finditer(r"(?<=[.!?])(\s+)(?=[A-Z0-9\"'(\[])", masked):
            chunk = para[last_idx : boundary.start()].strip()
            if chunk:
                sentences.append(chunk)
            last_idx = boundary.end()
        tail = para[last_idx:].strip()
        if tail:
            sentences.append(tail)
        if sentences:
            result.append(sentences)
    return result


def _fallback_project_dependencies(text: str) -> list[str]:
    """Read ``[project].dependencies`` without tomllib (Python 3.10).

    Fail-closed: anything this minimal reader cannot interpret raises
    ``ValueError`` so the caller records the manifest as unparseable.
    """
    section = None
    pos = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        header = re.fullmatch(r"\[\s*([A-Za-z0-9_.\-\s\"']+?)\s*\]\s*(?:#.*)?", stripped)
        if header and not stripped.startswith("[["):
            section = header.group(1).strip()
        elif section is None and re.match(r"\s*project\s*[.=]", line):
            raise ValueError("dotted or inline project table is not supported")
        elif section == "project":
            match = re.match(r"\s*dependencies\s*=\s*", line)
            if match:
                return _scan_toml_string_array(text, pos + match.end())
        pos += len(line)
    return []


def _scan_toml_string_array(text: str, start: int) -> list[str]:
    if start >= len(text) or text[start] != "[":
        raise ValueError("dependencies is not an inline array")
    items: list[str] = []
    idx = start + 1
    expect_value = True
    while idx < len(text):
        char = text[idx]
        if char in " \t\r\n":
            idx += 1
        elif char == "#":
            newline = text.find("\n", idx)
            idx = len(text) if newline < 0 else newline + 1
        elif char == "]":
            return items
        elif char == ",":
            if expect_value:
                raise ValueError("unexpected comma in dependencies")
            expect_value = True
            idx += 1
        elif char in "\"'" and expect_value:
            end = idx + 1
            while end < len(text) and text[end] != char:
                if text[end] == "\n":
                    raise ValueError("unsupported multi-line string in dependencies")
                end += 2 if char == '"' and text[end] == "\\" else 1
            if end >= len(text):
                break
            items.append(text[idx + 1 : end])
            expect_value = False
            idx = end + 1
        else:
            raise ValueError("unsupported dependencies syntax")
    raise ValueError("unterminated dependencies array")


def _extract_runtime_dependencies(repo_dir: Path) -> tuple[bool, list[str]]:
    deps: list[str] = []
    has_manifest = False
    pyproject = repo_dir / "pyproject.toml"
    if pyproject.is_file():
        has_manifest = True
        try:
            text = pyproject.read_text(encoding="utf-8")
            if tomllib is not None:
                parsed = tomllib.loads(text)
                raw_deps = (parsed.get("project") or {}).get("dependencies") or []
            else:
                raw_deps = _fallback_project_dependencies(text)
            if isinstance(raw_deps, list):
                deps.extend(str(item).strip() for item in raw_deps if str(item).strip())
        except Exception:
            deps.append("<unparseable-pyproject.toml>")
    package_json = repo_dir / "package.json"
    if package_json.is_file():
        has_manifest = True
        try:
            parsed_pkg = json.loads(package_json.read_text(encoding="utf-8"))
            raw_pkg_deps = parsed_pkg.get("dependencies") or {}
            if isinstance(raw_pkg_deps, Mapping):
                deps.extend(str(k).strip() for k in raw_pkg_deps.keys() if str(k).strip())
        except Exception:
            deps.append("<unparseable-package.json>")
    return has_manifest, deps


def _sentence_starts_software_claim(
    sentence: str,
    primary_slug: str,
    unambiguous_catalog_names: set[str],
) -> bool:
    if re.search(r"(?<![\w-])github\.com/", sentence, re.IGNORECASE):
        return True
    prose = re.sub(r"https?://\S+", " ", sentence)
    if primary_slug and len(primary_slug) >= 4 and primary_slug not in _QUALIFIED_ONLY_REPO_NAMES:
        if re.search(rf"(?<![/\w-]){re.escape(primary_slug)}(?![\w-])", prose, re.IGNORECASE):
            return True
    if re.search(
        r"\b(?:we|our)\s+(?:built|bundled|solved|handle|handled|use|used|wrote|added|"
        r"ship|shipped|track|route|enforce|extract|split|pair|check|call|map|maintain|"
        r"created|designed|wired|implemented)\b",
        prose,
        re.IGNORECASE,
    ):
        return True
    if re.search(
        r"\b(?:our|its)\s+(?:[A-Za-z0-9_.-]+\s+){0,4}"
        r"(?:package|toolkit|stack|queue|module|modules|system|agent|os|library|skill|router|engine|bridge|layer|core)\b",
        prose,
        re.IGNORECASE,
    ):
        return True
    if re.search(r"\bin\s+our\s+[A-Za-z0-9_.-]+", prose, re.IGNORECASE):
        return True
    if _MENTIONED_CODE_FILE_RE.search(prose):
        return True
    for cname in unambiguous_catalog_names:
        if re.search(rf"(?<![/\w-]){re.escape(cname)}(?![\w-])", prose, re.IGNORECASE):
            return True
    return False


def _verify_claim_contract(
    proposal: Mapping[str, Any],
    *,
    repos_root: Path | None,
    catalog_repos: list[Mapping[str, Any]],
    require_contract: bool,
    git_cache: dict[Path, set[str] | None] | None = None,
) -> dict[str, Any]:
    """Deterministically verify a proposal's Claim-Beleg-Vertrag against real source code."""
    raw_contract = str(proposal.get("claim_contract_raw") or "").strip()
    if not raw_contract:
        violations = ["missing-claim-contract"] if require_contract else []
        return {
            "present": False,
            "valid": not violations,
            "claim_count": 0,
            "verified_claims": 0,
            "software_sentence_count": 0,
            "covered_sentence_count": 0,
            "uncovered_sentences": [],
            "violations": violations,
        }

    violations: list[str] = []
    try:
        items = json.loads(raw_contract)
    except json.JSONDecodeError as exc:
        return {
            "present": True,
            "valid": False,
            "claim_count": 0,
            "verified_claims": 0,
            "software_sentence_count": 0,
            "covered_sentence_count": 0,
            "uncovered_sentences": [],
            "violations": [f"invalid-contract-json:{exc.msg}"],
        }

    if not isinstance(items, list) or not items:
        return {
            "present": True,
            "valid": False,
            "claim_count": 0,
            "verified_claims": 0,
            "software_sentence_count": 0,
            "covered_sentence_count": 0,
            "uncovered_sentences": [],
            "violations": ["empty-claim-contract"],
        }

    if repos_root is None or not repos_root.is_dir():
        return {
            "present": True,
            "valid": False,
            "claim_count": len(items),
            "verified_claims": 0,
            "software_sentence_count": 0,
            "covered_sentence_count": 0,
            "uncovered_sentences": [],
            "violations": ["repos-root-unavailable"],
        }

    tracked_cache = git_cache if git_cache is not None else {}
    norm_text = str(proposal.get("text") or "").replace("\r\n", "\n")
    verified_entries: list[dict[str, Any]] = []

    for idx, entry in enumerate(items):
        if not isinstance(entry, Mapping):
            violations.append(f"invalid-claim-entry:{idx}:not-an-object")
            continue
        anchor = str(entry.get("text_anchor") or "").replace("\r\n", "\n").strip()
        repo_ref = str(entry.get("repo") or "").strip()
        rel_file = str(entry.get("file") or "").strip()
        lines_spec = entry.get("lines")
        verbatim = str(entry.get("verbatim_code") or "").replace("\r\n", "\n").strip("\n")

        if len(anchor) < 8:
            violations.append(f"invalid-claim-entry:{idx}:text-anchor-too-short")
            continue
        if not repo_ref or not rel_file or Path(rel_file).is_absolute() or ".." in Path(rel_file).parts:
            violations.append(f"invalid-claim-entry:{idx}:invalid-repo-or-file")
            continue
        line_range = _parse_line_range(lines_spec)
        if line_range is None:
            violations.append(f"invalid-claim-entry:{idx}:invalid-line-range")
            continue
        if len(re.sub(r"\s+", "", verbatim)) < 10:
            violations.append(f"invalid-claim-entry:{idx}:verbatim-code-too-short")
            continue
        if anchor not in norm_text:
            violations.append(f"anchor-not-in-text:{idx}")
            continue

        repo_dir, skill_rel_dir, repo_slug = _resolve_repo_clone(repos_root, repo_ref)
        if repo_dir is None or not repo_dir.is_dir():
            violations.append(f"missing-claim-repo:{idx}:{repo_ref}")
            continue
        repo_resolved = repo_dir.resolve()
        candidate_path = repo_dir / rel_file
        if not candidate_path.is_file() and skill_rel_dir is not None:
            alt_candidate = repo_dir / skill_rel_dir / rel_file
            if alt_candidate.is_file():
                candidate_path = alt_candidate
        try:
            resolved_file = candidate_path.resolve()
            rel_to_repo = resolved_file.relative_to(repo_resolved).as_posix()
        except (OSError, ValueError):
            violations.append(f"path-traversal:{idx}:{rel_file}")
            continue
        if not resolved_file.is_file():
            violations.append(f"missing-claim-file:{idx}:{rel_file}")
            continue

        tracked = _git_tracked_files(repo_resolved, tracked_cache)
        if tracked is not None and rel_to_repo not in tracked:
            violations.append(f"untracked-claim-file:{idx}:{rel_to_repo}")
            continue

        try:
            source_text = resolved_file.read_text(encoding="utf-8").replace("\r\n", "\n")
        except (OSError, UnicodeDecodeError):
            violations.append(f"unreadable-claim-file:{idx}:{rel_file}")
            continue
        source_lines = source_text.split("\n")
        start_line, end_line = line_range
        if end_line > len(source_lines):
            violations.append(f"line-range-out-of-bounds:{idx}:{start_line}-{end_line}>{len(source_lines)}")
            continue

        window_text = "\n".join(source_lines[start_line - 1 : end_line])
        if verbatim not in window_text:
            violations.append(f"verbatim-code-mismatch:{idx}:{rel_to_repo}:{start_line}-{end_line}")
            continue

        verified_entries.append(
            {
                "index": idx,
                "anchor": anchor,
                "repo_ref": repo_ref,
                "repo_slug": repo_slug,
                "repo_dir": repo_resolved,
                "rel_file": rel_to_repo,
                "file_name": resolved_file.name,
                "verbatim": verbatim,
            }
        )

    primary_repo_norm = _normalize_repo_reference(proposal.get("repo", ""))
    _primary_dir, primary_skill_rel, primary_slug = _resolve_repo_clone(repos_root, primary_repo_norm)
    is_skill_target = primary_skill_rel is not None or primary_slug == "skills"
    if verified_entries and not is_skill_target:
        has_primary_source_code = any(
            (_same_repo(e["repo_ref"], primary_repo_norm) or e["repo_slug"] == primary_slug)
            and bool(_SOURCE_CODE_EXT_RE.search(e["rel_file"]))
            for e in verified_entries
        )
        if not has_primary_source_code:
            violations.append("code-file-required:primary-repo")

    unambiguous_catalog: dict[str, str] = {}
    ambiguous_catalog: dict[str, str] = {}
    for cat in catalog_repos:
        if not isinstance(cat, Mapping) or not cat.get("active", True):
            continue
        cid = _normalize_repo_reference(cat.get("id", "") or cat.get("url", ""))
        cname = str(cat.get("name", "")).strip()
        cname_low = cname.casefold()
        if not cid or len(cname_low) < 4 or cname_low in _QUALIFIED_ONLY_REPO_NAMES:
            continue
        if cname_low in _AMBIGUOUS_CAPITALIZED_REPO_NAMES:
            ambiguous_catalog[cname_low] = cid
        else:
            unambiguous_catalog[cname_low] = cid

    paragraphs = _split_into_paragraphs_and_sentences(norm_text)
    software_sentences: list[str] = []
    comment_active = False
    for para_sentences in paragraphs:
        para_active = comment_active
        for sent in para_sentences:
            if not para_active and _sentence_starts_software_claim(
                sent, primary_slug, set(unambiguous_catalog.keys())
            ):
                para_active = True
                comment_active = True
            if para_active:
                software_sentences.append(sent)

    if not software_sentences and norm_text.strip():
        software_sentences = [s for para in paragraphs for s in para]

    uncovered_sentences: list[str] = []
    covered_count = 0
    verified_file_names = {e["file_name"].casefold() for e in verified_entries}
    for sent in software_sentences:
        covering = [e for e in verified_entries if e["anchor"] in sent or sent in e["anchor"]]
        if covering:
            covered_count += 1
        else:
            preview = sent[:80] + ("..." if len(sent) > 80 else "")
            uncovered_sentences.append(preview)
            violations.append(f"uncovered-software-sentence:{preview}")

        prose_sent = re.sub(r"https?://\S+", " ", sent)
        for m_file in _MENTIONED_CODE_FILE_RE.finditer(prose_sent):
            fname = m_file.group(1)
            if fname.casefold() not in verified_file_names or not any(
                fname in e["anchor"] for e in verified_entries
            ):
                violations.append(f"unverified-mentioned-file:{fname}")

        if _ZERO_DEP_CLAIM_RE.search(prose_sent):
            zero_dep_entries = [e for e in covering if _ZERO_DEP_CLAIM_RE.search(e["anchor"])]
            target_entries = zero_dep_entries or covering or verified_entries
            checked_dirs: dict[Path, str] = {}
            for e in target_entries:
                checked_dirs[e["repo_dir"]] = e["repo_slug"]
            if not checked_dirs and _primary_dir is not None and _primary_dir.is_dir():
                checked_dirs[_primary_dir.resolve()] = primary_slug
            for r_dir, r_slug in checked_dirs.items():
                has_manifest, runtime_deps = _extract_runtime_dependencies(r_dir)
                if runtime_deps:
                    violations.append(f"predicate-contradiction:zero-dependency:{r_slug}")
                elif has_manifest:
                    has_manifest_entry = any(
                        e["repo_dir"] == r_dir and e["file_name"] in {"pyproject.toml", "package.json"}
                        for e in verified_entries
                    )
                    if not has_manifest_entry:
                        violations.append(f"missing-manifest-proof:zero-dependency:{r_slug}")

    known_orgs = set(DEFAULT_PRIMARY_ORGS) | set(DEFAULT_DISCOURSE_ORGS)
    mentioned_sisters: dict[str, str] = {}
    for m_gh in re.finditer(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", norm_text):
        gh_ref = _normalize_repo_reference(m_gh.group(1))
        gh_org = gh_ref.split("/", 1)[0]
        if gh_org in known_orgs and not _same_repo(gh_ref, primary_repo_norm):
            mentioned_sisters[gh_ref] = gh_ref.rsplit("/", 1)[-1]

    prose_all = re.sub(r"https?://\S+", " ", "\n".join(software_sentences))
    for cname_low, cid in unambiguous_catalog.items():
        if _same_repo(cid, primary_repo_norm) or cname_low == primary_slug:
            continue
        if cid.startswith("skills/") and "-" not in cname_low:
            continue
        if re.search(rf"(?<![/\w-]){re.escape(cname_low)}(?![\w-])", prose_all, re.IGNORECASE):
            mentioned_sisters[cid] = cname_low

    for cname_low, cid in ambiguous_catalog.items():
        if _same_repo(cid, primary_repo_norm) or cname_low == primary_slug:
            continue
        cap_name = cname_low[0].upper() + cname_low[1:]
        for match_cap in re.finditer(rf"(?<![/\w-]){re.escape(cap_name)}(?![\w-])", prose_all):
            prefix = prose_all[: match_cap.start()].rstrip(" \t\"'([")
            if prefix and prefix[-1] not in ".!?\n":
                mentioned_sisters[cid] = cname_low
                break

    for sister_id, sister_name in sorted(mentioned_sisters.items()):
        sister_ok = any(
            sister_name in e["anchor"].casefold()
            and (
                _same_repo(e["repo_ref"], sister_id)
                or e["repo_slug"] == sister_id.rsplit("/", 1)[-1]
                or sister_name in e["verbatim"].casefold()
            )
            for e in verified_entries
        )
        if not sister_ok:
            violations.append(f"unverified-sister-repo:{sister_id}")

    return {
        "present": True,
        "valid": len(violations) == 0,
        "claim_count": len(items),
        "verified_claims": len(verified_entries),
        "software_sentence_count": len(software_sentences),
        "covered_sentence_count": covered_count,
        "uncovered_sentences": uncovered_sentences,
        "violations": violations,
    }

def _remove_spans(content: str, spans: list[tuple[int, int]]) -> str:
    updated = content
    for start, end in sorted(spans, reverse=True):
        updated = updated[:start] + updated[end:]
    return updated


def select_candidate_repository(
    repositories: list[Mapping[str, Any]],
    cooldown_days: float = 7.0,
    now: datetime | None = None,
    excluded_orgs: set[str] | None = None,
    excluded_repos: set[str] | None = None,
) -> tuple[Mapping[str, Any] | None, dict[str, Any]]:
    """Selects the next repository to promote using traffic analysis and cooldown rules.

    Fail-closed: only repositories whose github_meta positively confirms public, non-fork and
    non-archived are eligible (set by --sync-githubbot or when bootstrapping the catalog).
    Organizations in excluded_orgs (default: biotec-line) are strictly excluded.
    """
    blocked_orgs = {
        str(o).strip().casefold() for o in (excluded_orgs or DEFAULT_EXCLUDED_ORGS) if str(o).strip()
    } | DEFAULT_EXCLUDED_ORGS
    blocked_repos = {
        str(r).strip().casefold() for r in (excluded_repos or DEFAULT_EXCLUDED_REPOS) if str(r).strip()
    } | DEFAULT_EXCLUDED_REPOS
    eligible = []
    unverified = 0
    for repo in repositories:
        if not isinstance(repo, Mapping):
            continue
        if _extract_repo_org(repo) in blocked_orgs:
            continue
        if str(repo.get("name", "")).strip().casefold() in blocked_repos:
            continue
        if not repo.get("active", True):
            continue
        if repo.get("exclusion_reason"):
            continue
        passes, unverified_hit = _public_repo_gate(repo)
        if unverified_hit:
            unverified += 1
        if not passes:
            continue
        eligible.append(repo)

    if not eligible:
        return None, {"unverified_visibility": unverified}

    current_time = now or datetime.now(timezone.utc).astimezone()

    def parse_promo_time(r: Mapping[str, Any]) -> datetime | None:
        raw = r.get("last_promoted_at") or r.get("last_promoted")
        if not raw:
            return None
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=current_time.tzinfo)
            return dt
        except ValueError:
            return None

    scored_candidates = []
    for repo in eligible:
        promo_dt = parse_promo_time(repo)
        total_promotions = int(repo.get("total_promotions", 0))
        is_unpromoted = (total_promotions == 0 and promo_dt is None)
        if promo_dt:
            days_since = max(0.0, (current_time - promo_dt).total_seconds() / 86400.0)
            is_cooldown = days_since < cooldown_days
            recency_bonus = min(30.0, days_since) * 2.0
        else:
            days_since = 999.0
            is_cooldown = False
            recency_bonus = 60.0

        traffic = repo.get("traffic") or {}
        clones_u = int(traffic.get("clones_unique_14d", 0))
        views_u = int(traffic.get("views_unique_14d", 0))
        traffic_score = int(traffic.get("traffic_score", clones_u * 2 + views_u))

        priority = str(repo.get("priority", "normal")).casefold()
        priority_bonus = 50.0 if priority == "high" else (-50.0 if priority == "low" else 0.0)

        total_score = traffic_score + priority_bonus + recency_bonus
        repo_id_norm = _normalize_repo_reference(repo.get("id", "") or repo.get("url", ""))
        is_core_flagship = repo_id_norm in CORE_ECOSYSTEM_FLAGSHIPS
        selection_tier = int(repo.get("selection_tier", 1 if is_core_flagship else 3))
        selection_tier_label = str(
            repo.get("selection_tier_label", "tier1_core_flagship" if is_core_flagship else "tier3_smaller_modules")
        )
        quality_score = int(repo.get("quality_score", 99 if is_core_flagship else 60))
        effective_quality_score = quality_score - (total_promotions * 3)

        scored_candidates.append({
            "repo": repo,
            "is_cooldown": is_cooldown,
            "is_unpromoted": is_unpromoted,
            "is_core_flagship": is_core_flagship,
            "selection_tier": selection_tier,
            "selection_tier_label": selection_tier_label,
            "quality_score": quality_score,
            "effective_quality_score": effective_quality_score,
            "days_since_promo": days_since,
            "traffic_score": traffic_score,
            "clones_unique_14d": clones_u,
            "views_unique_14d": views_u,
            "priority": repo.get("priority", "normal"),
            "total_score": total_score,
        })

    # The cooldown is binding: without a ready candidate nothing is selected
    pool = [c for c in scored_candidates if not c["is_cooldown"]]
    if not pool:
        return None, {"all_in_cooldown": True}

    use_tiered_selection = any("selection_tier" in c["repo"] for c in pool)
    if use_tiered_selection:
        pool.sort(
            key=lambda c: (
                c["selection_tier"],
                0 if (c["is_unpromoted"] or c["is_core_flagship"]) else 1,
                -c["effective_quality_score"],
                c["views_unique_14d"],
                -c["total_score"],
                c["days_since_promo"] if c["days_since_promo"] < 999 else -1,
                str(c["repo"].get("name", "")),
            )
        )
    else:
        pool.sort(
            key=lambda c: (
                0 if c["is_unpromoted"] else 1,
                -c["total_score"],
                c["days_since_promo"] if c["days_since_promo"] < 999 else -1,
                str(c["repo"].get("name", "")),
            )
        )

    best = pool[0]
    return best["repo"], {
        "selection_tier": best["selection_tier"],
        "selection_tier_label": best["selection_tier_label"],
        "quality_score": best["quality_score"],
        "traffic_score": best["traffic_score"],
        "clones_unique_14d": best["clones_unique_14d"],
        "views_unique_14d": best["views_unique_14d"],
        "priority": best["priority"],
        "days_since_promo": round(best["days_since_promo"], 1) if best["days_since_promo"] < 999 else None,
        "total_score": round(best["total_score"], 1),
        "is_cooldown": best["is_cooldown"],
    }


class CommunityOutreachEngine:

    def __init__(
        self,
        workspace_dir: str | Path,
        dry_run: bool = False,
        publisher: object | None = None,
        org_allow: list[str] | None = None,
        repos_root: str | Path | None = None,
    ):
        self.workspace = Path(workspace_dir).resolve()
        self.dry_run = dry_run
        self.publisher = publisher
        self.repos_root = repos_root
        # Produktzuschnitt je App (T-20260926-665406367): welche Orgs Stufe 1 zuerst
        # versucht, bevor phase3_research_and_stage auf den ganzen Pool ausweicht.
        self.org_allow = list(org_allow) if org_allow else []
        self.usecases_json = self.workspace / "usecases.json"
        self.inbox_md = self.workspace / "POST-EINGANG.md"
        self.outbox_md = self.workspace / "POST-AUSGANG.md"
        self.registry_md = self.workspace / "POSTVERZEICHNIS.md"
        self.history_json = self.workspace / "posts_history.json"
        self.rejected_json = self.workspace / "rejected_proposals.json"
        self.archive_dir = self.workspace / "_archive"
        self.config_json = self.workspace / "config.json"

    def _blacklisted(self) -> tuple[set[str], set[str], set[str]]:
        """Return (blacklisted_canonical_urls, blacklisted_proposal_ids, excluded_platforms)."""
        urls: set[str] = set()
        ids: set[str] = set()
        platforms: set[str] = set()
        data = _read_json(self.rejected_json, {})
        if isinstance(data, Mapping):
            for plat in data.get("platform_exclusions", []) or []:
                if isinstance(plat, Mapping) and plat.get("platform"):
                    platforms.add(str(plat["platform"]).strip().casefold())
                elif isinstance(plat, str) and plat.strip():
                    platforms.add(plat.strip().casefold())
            for entry in data.get("rejected_proposals", []) or []:
                if not isinstance(entry, Mapping):
                    continue
                if entry.get("proposal_id"):
                    ids.add(str(entry["proposal_id"]).strip())
                for key in ("canonical_url", "target_url"):
                    raw_url = str(entry.get(key, "")).strip()
                    if raw_url:
                        urls.add(canonicalize_url(raw_url))
        config = _read_json(self.config_json, {})
        if isinstance(config, Mapping):
            for plat in (config.get("compliance") or {}).get("excluded_platforms", []) or []:
                if str(plat).strip():
                    platforms.add(str(plat).strip().casefold())
        return urls, ids, platforms

    def _excluded_orgs(self) -> set[str]:
        orgs = set(DEFAULT_EXCLUDED_ORGS)
        data = _read_json(self.rejected_json, {})
        if isinstance(data, Mapping):
            for entry in data.get("excluded_orgs", []) or []:
                if isinstance(entry, Mapping) and entry.get("org"):
                    orgs.add(str(entry["org"]).strip().casefold())
                elif isinstance(entry, str) and entry.strip():
                    orgs.add(entry.strip().casefold())
        config = _read_json(self.config_json, {})
        if isinstance(config, Mapping):
            for org in (config.get("compliance") or {}).get("excluded_orgs", []) or []:
                if str(org).strip():
                    orgs.add(str(org).strip().casefold())
        return orgs

    def _primary_orgs(self) -> list[str]:
        config = _read_json(self.config_json, {})
        if not isinstance(config, Mapping):
            return []
        raw = (config.get("compliance") or {}).get("primary_orgs", []) or []
        return [str(o).strip().casefold() for o in raw if str(o).strip()]

    def _discourse_only_orgs(self) -> set[str]:
        orgs = set(DEFAULT_DISCOURSE_ORGS)
        config = _read_json(self.config_json, {})
        if isinstance(config, Mapping):
            for org in (config.get("compliance") or {}).get("discourse_only_orgs", []) or []:
                if str(org).strip():
                    orgs.add(str(org).strip().casefold())
        return orgs

    def _excluded_repos(self) -> set[str]:
        repos = set(DEFAULT_EXCLUDED_REPOS)
        data = _read_json(self.rejected_json, {})
        if isinstance(data, Mapping):
            for entry in data.get("excluded_repos", []) or []:
                if isinstance(entry, Mapping) and entry.get("repo"):
                    repos.add(_normalize_repo_reference(entry["repo"]).rsplit("/", 1)[-1])
                elif isinstance(entry, str) and entry.strip():
                    repos.add(_normalize_repo_reference(entry).rsplit("/", 1)[-1])
        config = _read_json(self.config_json, {})
        if isinstance(config, Mapping):
            for entry in (config.get("compliance") or {}).get("excluded_repos", []) or []:
                if str(entry).strip():
                    repos.add(_normalize_repo_reference(entry).rsplit("/", 1)[-1])
        return repos

    def _is_repo_from_excluded_org(self, repo_ref: object, repo_url: object = "") -> bool:
        blocked = self._excluded_orgs()
        blocked_repos = self._excluded_repos()
        for candidate in (repo_ref, repo_url):
            org = _extract_repo_org(candidate)
            if org and org in blocked:
                return True
            slug = _normalize_repo_reference(candidate).rsplit("/", 1)[-1]
            if slug and slug in blocked_repos:
                return True
        for entry in self._usecases().get("repositories", []) or []:
            if not isinstance(entry, Mapping):
                continue
            if _repo_matches_catalog_entry(entry, repo_ref) or (
                repo_url and _repo_matches_catalog_entry(entry, repo_url)
            ):
                if _extract_repo_org(entry) in blocked:
                    return True
        return False

    def _require_code_evidence(self) -> bool:
        config = _read_json(self.config_json, {})
        if not isinstance(config, Mapping):
            return False
        return bool((config.get("compliance") or {}).get("require_code_evidence", False))

    def _require_claim_contract(self) -> bool:
        config = _read_json(self.config_json, {})
        if not isinstance(config, Mapping):
            return False
        return bool((config.get("compliance") or {}).get("require_claim_contract", False))

    def _resolve_repos_root(self, repos_root: str | Path | None = None) -> Path | None:
        effective = repos_root or self.repos_root
        if effective:
            return Path(effective).expanduser().resolve()
        config = _read_json(self.config_json, {})
        configured_root = (
            (config.get("verification") or {}).get("local_repos_root")
            if isinstance(config, Mapping)
            else None
        )
        if configured_root:
            return Path(str(configured_root)).expanduser().resolve()
        env_root = os.environ.get("OUTREACH_REPOS_ROOT") or os.environ.get("LOCAL_DEV_REPOS")
        if env_root:
            candidate = Path(env_root).expanduser().resolve()
            if candidate.exists():
                return candidate
        return None

    def _require_natural_style(self) -> bool:
        config = _read_json(self.config_json, {})
        if not isinstance(config, Mapping):
            return False
        compliance = config.get("compliance") or {}
        return bool(compliance.get("require_natural_style", False) or compliance.get("require_code_evidence", False))

    def _history(self) -> list[dict[str, Any]]:
        """A missing history is empty; an unreadable one is an error, never an empty list to overwrite."""
        if not self.history_json.exists():
            return []
        try:
            value = json.loads(self.history_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise HistoryUnreadable(f"posts_history.json unreadable: {exc}") from exc
        if not isinstance(value, list):
            raise HistoryUnreadable("posts_history.json is not a list")
        return value

    def _usecases(self) -> dict[str, Any]:
        value = _read_json(self.usecases_json, {"repositories": []})
        return value if isinstance(value, dict) else {"repositories": []}

    def run_full_cycle(self) -> dict[str, Any]:
        inbound = self.phase1_inbound_check()
        outbound = self.phase2_outbound_execution()
        successful = sum(item["status"] in {"published", "recovered"} for item in outbound)
        candidate = None if successful else self.phase3_research_and_stage()
        archived = self.phase4_cut_and_clue_archive()
        needs_action = candidate is not None or any(item["status"] not in {"published", "recovered"} for item in outbound)
        return {
            "timestamp": _now_iso(),
            "status": "needs-action" if needs_action else "completed",
            "inbound_checks": inbound,
            "outbound_results": outbound,
            "outbound_published": successful,
            "published_items": successful,
            "staged_candidate": candidate,
            "archived_items": archived,
        }

    def phase1_inbound_check(self) -> int:
        return sum(1 for entry in self._history() if entry.get("status") == "published")

    def phase2_outbound_execution(self) -> list[dict[str, Any]]:
        if not self.inbox_md.exists():
            return []
        inbox = self.inbox_md.read_text(encoding="utf-8")
        approved = [proposal for proposal in _parse_proposals(inbox) if proposal["approved"]]
        if not approved:
            return []

        history = self._history()
        blacklisted_urls, blacklisted_ids, excluded_platforms = self._blacklisted()
        require_evidence = self._require_code_evidence()
        require_contract = self._require_claim_contract()
        resolved_repos_root = self._resolve_repos_root()
        catalog_repos = [r for r in self._usecases().get("repositories", []) if isinstance(r, Mapping)]
        git_cache: dict[Path, set[str] | None] = {}
        results: list[dict[str, Any]] = []
        finalized: list[tuple[dict[str, Any], dict[str, Any], str]] = []
        publisher_attempts = 0
        max_posts = self._max_posts_per_cycle()

        for proposal in approved:
            if not _is_valid_target_url(proposal["target_url"]):
                results.append({"id": proposal["id"], "status": "invalid-target"})
                continue
            target_key = canonicalize_url(proposal["target_url"])
            if (
                proposal["id"] in blacklisted_ids
                or target_key in blacklisted_urls
                or proposal["platform"].strip().casefold() in excluded_platforms
                or self._is_repo_from_excluded_org(proposal.get("repo", ""), proposal.get("repo_url", ""))
            ):
                results.append({"id": proposal["id"], "status": "blacklisted"})
                continue
            if require_evidence and not proposal.get("code_evidence", "").strip():
                results.append({"id": proposal["id"], "status": "needs-action", "reason": "missing-code-evidence"})
                continue
            if self._require_natural_style():
                style_violations = _check_natural_human_style(proposal["text"], proposal["platform"])
                if style_violations:
                    results.append({
                        "id": proposal["id"],
                        "status": "needs-action",
                        "reason": "ai-style-violation",
                        "violations": style_violations,
                    })
                    continue
            if require_contract or str(proposal.get("claim_contract_raw") or "").strip():
                contract_report = _verify_claim_contract(
                    proposal,
                    repos_root=resolved_repos_root,
                    catalog_repos=catalog_repos,
                    require_contract=require_contract,
                    git_cache=git_cache,
                )
                if not contract_report["valid"]:
                    reason = (
                        "missing-claim-contract"
                        if contract_report["violations"] == ["missing-claim-contract"]
                        else "invalid-claim-contract"
                    )
                    results.append({
                        "id": proposal["id"],
                        "status": "needs-action",
                        "reason": reason,
                        "violations": contract_report["violations"],
                    })
                    continue
            existing_id = next(
                (
                    item
                    for item in history
                    if item.get("post_id") == proposal["id"]
                    and item.get("status") == "published"
                    and item.get("receipt_verified") is True
                ),
                None,
            )
            if existing_id:
                binding_matches = (
                    canonicalize_url(str(existing_id.get("target_url", "")))
                    == canonicalize_url(proposal["target_url"])
                    and str(existing_id.get("platform", "")).casefold() == str(proposal["platform"]).casefold()
                    and _same_repo(existing_id.get("repo", ""), proposal["repo"])
                )
                if not binding_matches:
                    results.append({"id": proposal["id"], "status": "receipt-conflict"})
                    continue
                finalized.append((proposal, existing_id, "recovered"))
                results.append({"id": proposal["id"], "status": "recovered"})
                continue

            duplicate = next(
                (
                    item
                    for item in history
                    if item.get("status") == "published"
                    and canonicalize_url(str(item.get("target_url", ""))) == target_key
                ),
                None,
            )
            if duplicate:
                results.append({"id": proposal["id"], "status": "duplicate", "duplicate_of": duplicate.get("post_id")})
                continue
            if self.dry_run:
                results.append({"id": proposal["id"], "status": "needs-action", "reason": "dry-run"})
                continue
            if self.publisher is None or not callable(getattr(self.publisher, "publish", None)):
                results.append({"id": proposal["id"], "status": "needs-action", "reason": "publisher-unavailable"})
                continue
            # A publisher bound to one specific proposal (e.g. FileReceiptPublisher, T-20260926-
            # 665406367) must be skipped WITHOUT consuming a cycle-limit slot for every OTHER
            # approved proposal -- otherwise a bound receipt that isn't first in the queue gets
            # "deferred: cycle-limit" instead of being applied, and the already-real evidence of
            # that post is lost (merge-reviewer finding). Checked before counting an attempt.
            bound_id = getattr(self.publisher, "proposal_id", None)
            if bound_id is not None and bound_id != proposal["id"]:
                results.append({"id": proposal["id"], "status": "needs-action", "reason": "publisher-unbound"})
                continue
            if publisher_attempts >= max_posts:
                results.append({"id": proposal["id"], "status": "deferred", "reason": "cycle-limit"})
                continue

            publisher_attempts += 1
            try:
                raw_receipt = self.publisher.publish(dict(proposal))
            except Exception as exc:  # Publisher failures are external and must fail closed.
                results.append({"id": proposal["id"], "status": "needs-action", "reason": f"publisher-error: {exc}"})
                continue
            receipt = PublishReceipt.validate(raw_receipt, proposal)
            if receipt is None:
                results.append({"id": proposal["id"], "status": "needs-action", "reason": "receipt-unverified"})
                continue

            record = self._history_record(proposal, receipt)
            history.append(record)
            _atomic_write_json(self.history_json, history)
            finalized.append((proposal, record, "published"))
            results.append({"id": proposal["id"], "status": "published", "receipt": receipt.platform_post_id})

        if finalized:
            self._finalize_local_projections(inbox, history, finalized)
        return results

    def _max_posts_per_cycle(self) -> int:
        config = _read_json(self.config_json, {})
        try:
            configured = int(config.get("compliance", {}).get("max_posts_per_cycle", 1))
        except (AttributeError, TypeError, ValueError):
            configured = 1
        return max(1, configured)

    @staticmethod
    def _history_record(proposal: Mapping[str, Any], receipt: PublishReceipt) -> dict[str, Any]:
        return {
            "post_id": proposal["id"],
            "published_at": receipt.published_at,
            "date": receipt.published_at[:10] or _today(),
            "platform": proposal["platform"],
            "target_url": proposal["target_url"],
            "published_url": receipt.published_url,
            "platform_post_id": receipt.platform_post_id,
            "repo": proposal["repo"],
            "repo_url": proposal.get("repo_url", ""),
            "content": proposal["text"],
            "content_preview": proposal["text"][:150],
            "status": "published",
            "receipt_verified": True,
            "publication_status": "veroeffentlicht",
        }

    def _finalize_local_projections(
        self,
        inbox: str,
        history: list[dict[str, Any]],
        finalized: list[tuple[dict[str, Any], dict[str, Any], str]],
    ) -> None:
        outbox = self.outbox_md.read_text(encoding="utf-8") if self.outbox_md.exists() else "# POST-AUSGANG\n"
        for _proposal, record, _status in finalized:
            outbox = self._append_outbox_record(outbox, record)
        _atomic_write_text(self.outbox_md, outbox)
        remaining_inbox = _remove_spans(inbox, [proposal["span"] for proposal, _record, _status in finalized])
        self._write_registry(history, remaining_inbox)
        self._update_rotation_from_history(history)
        _atomic_write_text(self.inbox_md, remaining_inbox)

    @staticmethod
    def _append_outbox_record(content: str, record: Mapping[str, Any]) -> str:
        # Marker must match the ESCAPED heading actually written below (a raw
        # post_id containing _ * ` < > | never matches its own escaped header
        # again -> duplicate append on every re-finalize/recovery run), and
        # must only match real H3 headings outside fenced code blocks (a
        # quoted "### [ID]" inside the fenced published text -- e.g. someone
        # replying with an excerpt of a previous entry -- would otherwise
        # spoof-suppress a genuinely new entry with the same id).
        marker = f"### [{_registry_cell(record['post_id'])}]"
        if any(line.startswith(marker) for _, line in _markdown_h3_headings(content)):
            return content
        if content and not content.endswith("\n"):
            content += "\n"
        return content + f"""
### [{_registry_cell(record['post_id'])}] Veröffentlicht am {_registry_cell(record.get('date', ''))} ({_registry_cell(record.get('platform', ''))})
- **Ziel-URL:** {_registry_link(record.get('target_url', ''))}
- **Veröffentlichungsbeleg:** {_registry_link(record.get('published_url', ''), _registry_cell(record.get('platform_post_id', '')))}
- **Lösungs-Repo:** `{_registry_cell(record.get('repo', ''))}`
- **Status:** veroeffentlicht (Beleg verifiziert)
- **Veröffentlichter Text:**
```text
{_fenced_cell(record.get('content', ''))}
```

"""

    @staticmethod
    def _registry_row(record: Mapping[str, Any]) -> str:
        target = _registry_link(record.get("target_url"))
        evidence = _registry_link(record.get("published_url"), _registry_cell(record.get("platform_post_id")))
        return (
            f"| {_registry_cell(record.get('date'))} | {_registry_cell(record.get('platform'))} | {target} | "
            f"{_registry_cell(record.get('repo'))} | {_registry_cell(record.get('post_id'))} | {evidence} |"
        )

    def _registry_documents(self, history: list[dict[str, Any]], inbox: str) -> dict[Path, str]:
        """POSTVERZEICHNIS.md plus Cut-and-Clue archives (variant A), rendered deterministically."""
        published = [r for r in history if isinstance(r, dict) and publication_status(r) == "veroeffentlicht"]
        unconfirmed = [r for r in history if isinstance(r, dict) and publication_status(r) == "unbestaetigt"]
        full_chunks = len(published) // REGISTRY_MAX_ROWS
        archive = [self.archive_dir / f"POSTVERZEICHNIS_ARCHIV_v{k}.md" for k in range(1, full_chunks + 1)]
        head = "| Datum | Plattform | Ziel-URL | Repository | Post-ID | Beleg |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        documents: dict[Path, str] = {}
        for index, path in enumerate(archive):
            rows = published[index * REGISTRY_MAX_ROWS : (index + 1) * REGISTRY_MAX_ROWS]
            predecessor = f"Archiv: [{archive[index - 1].name}]({archive[index - 1].name})" if index else "keiner"
            successor = (
                f"Archiv: [{archive[index + 1].name}]({archive[index + 1].name})"
                if index + 1 < len(archive)
                else "Aktive Datei: [POSTVERZEICHNIS.md](../POSTVERZEICHNIS.md)"
            )
            documents[path] = (
                f"# POSTVERZEICHNIS — Archiv v{index + 1} (veröffentlichte Beiträge, älteste zuerst)\n\n"
                f"---\nPointer / Vorläufer:\n{predecessor}\n---\n\n"
                + head + "\n".join(self._registry_row(r) for r in rows) + "\n\n"
                f"---\nPointer / Nachfolger:\n{successor}\n"
            )
        current = published[full_chunks * REGISTRY_MAX_ROWS :]
        queue = _parse_proposals(inbox)
        drafts = sum(1 for p in queue if not p.get("approved"))
        approved = sum(1 for p in queue if p.get("approved"))
        predecessor = f"Archiv: [_archive/{archive[-1].name}](_archive/{archive[-1].name})" if archive else "keiner"
        text = (
            "# POSTVERZEICHNIS: veröffentlichte und unbestätigte Beiträge\n\n"
            f"---\nPointer / Vorläufer:\n{predecessor}\n---\n\n"
            "> Jeder Beitrag hat genau einen Status: **entwurf** und **freigegeben** (Queue in POST-EINGANG.md),\n"
            "> **veroeffentlicht** (nur mit Beleg: Kommentar-Permalink und Plattform-ID) oder **unbestaetigt**\n"
            "> (als veröffentlicht gemeldet, aber ohne Beleg). Das Verzeichnis wird aus posts_history.json erzeugt.\n\n"
            f"**Stand:** veroeffentlicht {len(published)} · unbestaetigt {len(unconfirmed)} · "
            f"freigegeben {approved} · entwurf {drafts}\n\n"
            f"## Veröffentlicht (mit Beleg, neueste zuerst; {len(current)} hier, ältere im Archiv)\n\n"
            + head + "".join(self._registry_row(r) + "\n" for r in reversed(current))
            + "\n## Unbestätigt (kein Beleg; Ziel-URL bleibt für den Duplikatschutz gesperrt)\n\n"
            + head + "".join(self._registry_row(r) + "\n" for r in reversed(unconfirmed))
        )
        documents[self.registry_md] = text
        # archives no longer needed (e.g. a record became unbestaetigt) are neutralised, not deleted
        for stale in sorted(self.archive_dir.glob("POSTVERZEICHNIS_ARCHIV_v*.md")):
            if stale not in documents:
                documents[stale] = (
                    f"# {stale.stem} — veraltet, keine Einträge\n\n"
                    "Dieses Archiv wird nicht mehr benötigt; alle Beiträge stehen in den aktuellen Dateien.\n"
                    "Aktive Datei: [POSTVERZEICHNIS.md](../POSTVERZEICHNIS.md)\n"
                )
        return documents

    def _write_registry(self, history: list[dict[str, Any]], inbox: str) -> list[str]:
        written = []
        for path, text in self._registry_documents(history, inbox).items():
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                _atomic_write_text(path, text)
                written.append(path.name)
        return written

    def rebuild_registry(self) -> dict[str, Any]:
        inbox = self.inbox_md.read_text(encoding="utf-8") if self.inbox_md.exists() else ""
        history = self._history()
        if self.dry_run:
            return {"status": "dry-run", "documents": [p.name for p in self._registry_documents(history, inbox)]}
        return {"status": "completed", "written": self._write_registry(history, inbox)}

    def _update_rotation_from_history(self, history: list[dict[str, Any]]) -> None:
        if not self.usecases_json.exists():
            return
        data = self._usecases()
        repositories = data.get("repositories", [])
        if not isinstance(repositories, list):
            return
        for repo in repositories:
            if not isinstance(repo, dict):
                continue
            matches = [
                item
                for item in history
                if item.get("receipt_verified") is True
                and item.get("status") == "published"
                and _repo_matches_catalog_entry(repo, item.get("repo", ""))
            ]
            if not matches:
                continue
            latest = max(str(item.get("published_at", "")) for item in matches)
            if "last_promoted" in repo:
                repo["last_promoted"] = latest
            if "last_promoted_at" in repo or "last_promoted" not in repo:
                repo["last_promoted_at"] = latest
            repo["total_promotions"] = len(matches)
        published = [item for item in history if item.get("receipt_verified") is True and item.get("status") == "published"]
        if published:
            data["last_platform"] = published[-1].get("platform", data.get("last_platform", ""))
        data["updated_at"] = _now_iso()
        _atomic_write_json(self.usecases_json, data)

    @staticmethod
    def _stage3_new_proposal_pool(
        repositories: list[Mapping[str, Any]],
        org_allow: list[str],
        excluded_orgs: set[str] | None = None,
        discourse_orgs: set[str] | None = None,
        excluded_repos: set[str] | None = None,
    ) -> list[Mapping[str, Any]]:
        """Candidates for a fresh angle (new use-case/channel) when nothing else is left.

        Deliberately ignores cooldown and the "already queued" exclusion: stage 3 only
        runs when stages 1+2 found nothing, so ALL known repos are either exhausted or
        in cooldown. The caller (the drafting LLM) picks a genuinely new use-case or
        channel for one of these, or researches a public repo not yet in usecases.json.

        Still enforces the same fail-closed _public_repo_gate as select_candidate_repository
        (merge-reviewer fix, T-20260926-665406367): a private, archived, forked or
        never-synced repo must never be proposed here either.
        """
        blocked = {
            str(o).strip().casefold() for o in (excluded_orgs or DEFAULT_EXCLUDED_ORGS) if str(o).strip()
        } | DEFAULT_EXCLUDED_ORGS
        blocked_repos = {
            str(r).strip().casefold() for r in (excluded_repos or DEFAULT_EXCLUDED_REPOS) if str(r).strip()
        } | DEFAULT_EXCLUDED_REPOS
        discourse = {
            str(o).strip().casefold() for o in (discourse_orgs or DEFAULT_DISCOURSE_ORGS) if str(o).strip()
        }
        allow_discourse = any(o in discourse for o in org_allow)
        pool = [
            repo for repo in repositories
            if isinstance(repo, Mapping)
            and _extract_repo_org(repo) not in blocked
            and str(repo.get("name", "")).strip().casefold() not in blocked_repos
            and (allow_discourse or _extract_repo_org(repo) not in discourse)
            and repo.get("active", True)
            and not repo.get("exclusion_reason")
            and _public_repo_gate(repo)[0]
        ]
        if org_allow:
            scoped = [repo for repo in pool if _extract_repo_org(repo) in org_allow]
            if scoped:
                pool = scoped
        pool.sort(
            key=lambda repo: (
                -int((repo.get("traffic") or {}).get("traffic_score", 0)),
                -int(repo.get("total_promotions", 0)),
            )
        )
        return pool[:5]

    def phase3_research_and_stage(self, org_allow: list[str] | None = None) -> dict[str, Any] | None:
        """Stufe 1 (eigener Bereich / primary_orgs) -> Stufe 2 (ganzer Pool) -> Stufe 3 (neue Vorschlaege).

        org_allow scopt Stufe 1 auf bestimmte Orgs (Produktzuschnitt je App,
        T-20260926-665406367, bzw. primary_orgs laut Nutzerentscheid 2026-11-09);
        ohne expliziten Wert gilt self.org_allow aus dem Konstruktor bzw. primary_orgs aus config.json.
        Excluded orgs (biotec-line) sind in allen Stufen gesperrt; discourse_only_orgs (research-line)
        laufen nur bei explizitem Aufruf im Diskurs-/Stellungnahme-Modus statt im Standard-Tool-Outreach.
        """
        if org_allow is None:
            org_allow = self.org_allow if self.org_allow else self._primary_orgs()
        blocked_orgs = self._excluded_orgs()
        blocked_repos = self._excluded_repos()
        discourse_orgs = self._discourse_only_orgs()
        org_allow_norm = [
            org.strip().casefold()
            for org in (org_allow or [])
            if org and org.strip() and org.strip().casefold() not in blocked_orgs
        ]
        allow_discourse = any(org in discourse_orgs for org in org_allow_norm)

        data = self._usecases()
        repositories = [
            repo
            for repo in data.get("repositories", [])
            if isinstance(repo, dict)
            and _extract_repo_org(repo) not in blocked_orgs
            and str(repo.get("name", "")).strip().casefold() not in blocked_repos
            and (allow_discourse or _extract_repo_org(repo) not in discourse_orgs)
        ]

        # Exclude repos that already have an active/pending proposal in POST-EINGANG.md
        queued_refs: list[str] = []
        if self.inbox_md.exists():
            for proposal in _parse_proposals(self.inbox_md.read_text(encoding="utf-8")):
                queued_refs += [ref for ref in (proposal.get("repo"), proposal.get("repo_url")) if ref]

        eligible_repos = [
            repo for repo in repositories
            if not any(_repo_matches_catalog_entry(repo, ref) for ref in queued_refs)
        ]

        stage = 1
        fallback_used = False
        score_meta: dict[str, Any] = {}
        candidate: Mapping[str, Any] | None = None

        if org_allow_norm:
            own_repos = [r for r in eligible_repos if _extract_repo_org(r) in org_allow_norm]
            candidate, score_meta = select_candidate_repository(
                own_repos, excluded_orgs=blocked_orgs, excluded_repos=blocked_repos
            )
            if not candidate:
                # Stufe 2: eigener Bereich leer -> ganzer Pool (Dedup/Cooldown bleiben in Kraft)
                stage = 2
                fallback_used = True
                candidate, score_meta = select_candidate_repository(
                    eligible_repos, excluded_orgs=blocked_orgs, excluded_repos=blocked_repos
                )
        else:
            candidate, score_meta = select_candidate_repository(
                eligible_repos, excluded_orgs=blocked_orgs, excluded_repos=blocked_repos
            )

        if not candidate:
            reason = "no-active-repositories"
            if score_meta.get("all_in_cooldown"):
                reason = "all-in-cooldown"
            elif score_meta.get("unverified_visibility"):
                reason = "visibility-unverified: run --sync-githubbot"
            # Stufe 3 gilt nur im per-App-Zuschnitt (org_allow gesetzt) UND nur, wenn kein
            # Sync-Gap vorliegt -- ein fehlender --sync-githubbot-Lauf darf niemals durch einen
            # "neuen Vorschlag" umgangen werden (merge-reviewer-Fund, T-20260926-665406367).
            proposals = (
                self._stage3_new_proposal_pool(
                    repositories,
                    org_allow_norm,
                    excluded_orgs=blocked_orgs,
                    discourse_orgs=discourse_orgs,
                    excluded_repos=blocked_repos,
                )
                if org_allow_norm and not score_meta.get("unverified_visibility")
                else []
            )
            if not proposals:
                return {"status": "needs-action", "action": "configure-repositories", "reason": reason,
                        "stage": 2 if fallback_used else 1, "fallback_used": fallback_used}
            return {
                "status": "needs-action",
                "action": "propose-new-item",
                "stage": 3,
                "fallback_used": True,
                "reason": (
                    "Weder im eigenen Bereich noch im gesamten Pool ein umsetzbarer Kandidat ("
                    f"{reason}). Neuen Vorschlag erzeugen: neue Use-Case/neuer Zielkanal fuer eines "
                    "der folgenden Repos, oder ein noch nicht in usecases.json gefuehrtes "
                    "OEFFENTLICHES Repo recherchieren. Landet als Entwurf in der Queue, gleicher "
                    "Genehmigungsmodus, keine Uebertreibungen/erfundenen Nutzerzahlen/Testimonials."
                ),
                "candidates_for_new_angle": [
                    {
                        "repo_name": repo.get("name", repo.get("id", "")),
                        "repo_url": repo.get("url", ""),
                        "org": repo.get("org", ""),
                        "total_promotions": repo.get("total_promotions", 0),
                    }
                    for repo in proposals
                ],
            }

        rotation = data.get("platform_rotation") or DEFAULT_PLATFORM_ROTATION
        if not isinstance(rotation, list) or not rotation:
            rotation = DEFAULT_PLATFORM_ROTATION
        last_platform = str(data.get("last_platform", ""))
        if not last_platform:
            history = self._history()
            last_platform = str(history[-1].get("platform", "")) if history else ""
        try:
            platform = rotation[(rotation.index(last_platform) + 1) % len(rotation)]
        except ValueError:
            platform = rotation[0]
        is_discourse_candidate = (
            _extract_repo_org(candidate) in discourse_orgs
            or str(candidate.get("outreach_mode", "")).strip().casefold() == "discourse_positioning"
        )
        problems = candidate.get("problems_solved") or candidate.get("solved_problems") or ["Allgemeine Automatisierung"]
        return {
            "status": "needs-action",
            "action": "research-and-persist-valid-draft",
            "outreach_mode": "discourse-positioning" if is_discourse_candidate else "solution-outreach",
            "stage": stage,
            "fallback_used": fallback_used,
            "repo_name": candidate.get("name", candidate.get("id", "")),
            "repo_url": candidate.get("url", ""),
            "platform": platform,
            "target_problem": problems[0],
            "reason": (
                "Aktuelle Fachdiskussionen und Tendenzen zum Forschungsthema suchen, um unsere eigene "
                "wissenschaftliche Stellungnahme sachlich einzubringen (kein Tool-Pitch)."
                if is_discourse_candidate
                else "Eine echte, aktuelle und noch nicht verwendete Ziel-URL sowie ein geprüfter Entwurf fehlen."
            ),
            "selection_tier": score_meta.get("selection_tier", candidate.get("selection_tier", 3)),
            "selection_tier_label": score_meta.get(
                "selection_tier_label", candidate.get("selection_tier_label", "tier3_smaller_modules")
            ),
            "quality_score": score_meta.get("quality_score", candidate.get("quality_score", 60)),
            "traffic_score": score_meta.get("traffic_score", 0),
            "clones_unique_14d": score_meta.get("clones_unique_14d", 0),
            "views_unique_14d": score_meta.get("views_unique_14d", 0),
            "priority": score_meta.get("priority", "normal"),
        }


    def preview_post(self, proposal_id: str) -> dict[str, Any]:
        """Read-only preview of ONE approved proposal: exactly what would be posted, nothing more.

        T-20260926-665406367 (posting je App, pruefbar ohne echten Post): renders what a
        browser-automation step (open-compute/Playwright/Claude-in-Chrome/API) needs to
        compose -- platform, target thread, comment text -- so the calling app can show it
        (screenshot/preview) and stop BEFORE clicking submit. Touches no state whatsoever;
        refuses proposals that are not yet "- [x] Genehmigt", so a preview alone can never be
        mistaken for permission to send.
        """
        if not self.inbox_md.exists():
            return {"status": "error", "message": "POST-EINGANG.md not found"}
        proposals = _parse_proposals(self.inbox_md.read_text(encoding="utf-8"))
        proposal = next((p for p in proposals if p["id"] == proposal_id), None)
        if proposal is None:
            return {"status": "error", "message": f"proposal {proposal_id!r} not found in POST-EINGANG.md"}
        if not proposal["approved"]:
            return {
                "status": "error",
                "message": f"proposal {proposal_id!r} is not approved (- [x] Genehmigt missing) "
                "-- nothing to preview for posting yet",
            }
        if not _is_valid_target_url(proposal["target_url"]):
            return {"status": "error", "message": "invalid target_url"}
        blacklisted_urls, blacklisted_ids, excluded_platforms = self._blacklisted()
        if (
            proposal["id"] in blacklisted_ids
            or canonicalize_url(proposal["target_url"]) in blacklisted_urls
            or proposal["platform"].strip().casefold() in excluded_platforms
            or self._is_repo_from_excluded_org(proposal.get("repo", ""), proposal.get("repo_url", ""))
        ):
            return {"status": "error", "message": f"proposal {proposal_id!r} or its target/platform is blacklisted"}
        if self._require_code_evidence() and not proposal.get("code_evidence", "").strip():
            return {"status": "error", "message": f"proposal {proposal_id!r} is missing mandatory Code-Beleg"}
        if self._require_natural_style():
            style_violations = _check_natural_human_style(proposal["text"], proposal["platform"])
            if style_violations:
                return {
                    "status": "error",
                    "message": f"proposal {proposal_id!r} violates natural human style: {', '.join(style_violations)}",
                    "violations": style_violations,
                }
        require_contract = self._require_claim_contract()
        if require_contract or str(proposal.get("claim_contract_raw") or "").strip():
            catalog_repos = [r for r in self._usecases().get("repositories", []) if isinstance(r, Mapping)]
            contract_report = _verify_claim_contract(
                proposal,
                repos_root=self._resolve_repos_root(),
                catalog_repos=catalog_repos,
                require_contract=require_contract,
            )
            if not contract_report["valid"]:
                return {
                    "status": "error",
                    "message": (
                        f"proposal {proposal_id!r} failed Claim-Beleg-Vertrag: "
                        f"{', '.join(contract_report['violations'])}"
                    ),
                    "contract_violations": contract_report["violations"],
                }
        return {
            "status": "preview",
            "id": proposal["id"],
            "platform": proposal["platform"],
            "target_url": proposal["target_url"],
            "repo": proposal["repo"],
            "code_evidence": proposal.get("code_evidence", ""),
            "text": proposal["text"],
            "instruction": (
                "Compose exactly this text at target_url via the app's own browser tool, capture "
                "a screenshot as evidence, then STOP -- do not click submit/comment. Only proceed "
                "to an actual send after this preview has been shown to the user and the user's Go "
                "for a desktop takeover (if open-compute) has been obtained via team-lead."
            ),
        }

    def verify_proposals(self, repos_root: str | Path | None = None) -> dict[str, Any]:
        """Verify all queued proposals against blacklist, duplicates, real source code files, and Claim-Beleg-Vertrag."""
        if not self.inbox_md.exists():
            return {"status": "error", "message": "POST-EINGANG.md not found"}
        proposals = _parse_proposals(self.inbox_md.read_text(encoding="utf-8"))
        history = self._history()
        blacklisted_urls, blacklisted_ids, excluded_platforms = self._blacklisted()
        resolved_root = self._resolve_repos_root(repos_root)
        require_contract = self._require_claim_contract()
        catalog_repos = [r for r in self._usecases().get("repositories", []) if isinstance(r, Mapping)]
        git_cache: dict[Path, set[str] | None] = {}

        file_ext_re = re.compile(
            r"\.(?:py|ts|tsx|js|jsx|rs|go|html|css|toml|json|yaml|yml|md|sh|ps1|sql|c|cpp|h)$",
            re.IGNORECASE,
        )

        item_results: list[dict[str, Any]] = []
        verified_count = 0
        failed_count = 0

        for proposal in proposals:
            pid = proposal["id"]
            t_url = proposal["target_url"]
            t_key = canonicalize_url(t_url)
            valid_url = _is_valid_target_url(t_url)
            is_excluded_org = self._is_repo_from_excluded_org(proposal.get("repo", ""), proposal.get("repo_url", ""))
            is_blacklisted = (
                pid in blacklisted_ids
                or (bool(t_key) and t_key in blacklisted_urls)
                or proposal["platform"].strip().casefold() in excluded_platforms
                or is_excluded_org
            )
            is_duplicate = any(
                item.get("status") == "published" and canonicalize_url(str(item.get("target_url", ""))) == t_key
                for item in history
            )
            evidence_raw = str(proposal.get("code_evidence", "")).strip()
            has_evidence = bool(evidence_raw)

            if resolved_root is not None:
                repo_dir, skill_rel_dir, _repo_slug = _resolve_repo_clone(resolved_root, proposal["repo"])
            else:
                repo_dir, skill_rel_dir = None, None
            repo_exists = bool(repo_dir and repo_dir.is_dir())
            if repo_exists and skill_rel_dir is not None and repo_dir is not None:
                repo_exists = (repo_dir / skill_rel_dir).is_dir()

            verified_files: list[str] = []
            missing_files: list[str] = []
            if has_evidence and repo_dir is not None:
                tokens = re.findall(r"`([^`]+)`", evidence_raw)
                for token in tokens:
                    cleaned = re.sub(r":(?:L?\d+(?:-L?\d+)?)$", "", token.strip())
                    if not cleaned or " " in cleaned or "(" in cleaned or ")" in cleaned:
                        continue
                    candidate_path = Path(cleaned)
                    if candidate_path.is_absolute():
                        if candidate_path.is_file():
                            verified_files.append(cleaned)
                        elif file_ext_re.search(cleaned):
                            missing_files.append(cleaned)
                        continue
                    if "/" in cleaned or "\\" in cleaned or file_ext_re.search(cleaned):
                        full_path = repo_dir / cleaned
                        alt_path = (repo_dir / skill_rel_dir / cleaned) if skill_rel_dir is not None else None
                        if full_path.exists() or (alt_path is not None and alt_path.exists()):
                            verified_files.append(cleaned)
                        else:
                            missing_files.append(cleaned)

            files_ok = bool(verified_files) and not missing_files if resolved_root is not None else has_evidence
            style_violations = _check_natural_human_style(proposal["text"], proposal["platform"])
            natural_style_ok = not style_violations
            has_context_check = bool(str(proposal.get("context_check", "")).strip())
            contract_report = _verify_claim_contract(
                proposal,
                repos_root=resolved_root,
                catalog_repos=catalog_repos,
                require_contract=require_contract,
                git_cache=git_cache,
            )
            claim_contract_ok = contract_report["valid"]
            proposal_ok = (
                valid_url
                and not is_blacklisted
                and not is_duplicate
                and has_evidence
                and (repo_exists if resolved_root is not None else True)
                and files_ok
                and natural_style_ok
                and claim_contract_ok
            )
            if proposal_ok:
                verified_count += 1
            else:
                failed_count += 1

            item_results.append({
                "id": pid,
                "repo": proposal["repo"],
                "approved": proposal["approved"],
                "status": "verified" if proposal_ok else "failed",
                "valid_target_url": valid_url,
                "blacklisted": is_blacklisted,
                "excluded_org": is_excluded_org,
                "duplicate": is_duplicate,
                "has_code_evidence": has_evidence,
                "has_context_check": has_context_check,
                "natural_style_ok": natural_style_ok,
                "style_violations": style_violations,
                "claim_contract_present": contract_report["present"],
                "claim_contract_ok": claim_contract_ok,
                "claim_count": contract_report["claim_count"],
                "verified_claims": contract_report["verified_claims"],
                "software_sentence_count": contract_report["software_sentence_count"],
                "covered_sentence_count": contract_report["covered_sentence_count"],
                "uncovered_sentences": contract_report["uncovered_sentences"],
                "contract_violations": contract_report["violations"],
                "repo_clone_exists": repo_exists if resolved_root is not None else None,
                "verified_files": verified_files,
                "missing_files": missing_files,
            })

        overall = "verified" if failed_count == 0 else "failed"
        return {
            "status": overall,
            "total": len(proposals),
            "verified_count": verified_count,
            "failed_count": failed_count,
            "repos_root": str(resolved_root) if resolved_root else None,
            "results": item_results,
        }

    def phase4_cut_and_clue_archive(self, max_outbox_entries: int = 20) -> int:
        if not self.outbox_md.exists():
            return 0
        content = self.outbox_md.read_text(encoding="utf-8")
        entry_starts = [start for start, line in _markdown_h3_headings(content) if OUTBOX_ENTRY_RE.fullmatch(line)]
        if len(entry_starts) <= max_outbox_entries:
            return 0
        blocks = [
            content[start:(entry_starts[index + 1] if index + 1 < len(entry_starts) else len(content))]
            for index, start in enumerate(entry_starts)
        ]
        archive_count = len(blocks) - max_outbox_entries
        if self.dry_run:
            return archive_count

        header = content[:entry_starts[0]].rstrip()
        old_blocks = blocks[:archive_count]
        live_blocks = blocks[archive_count:]
        archive_name = f"POST-AUSGANG_{datetime.now().strftime('%Y-%m')}.md"
        archive_file = self.archive_dir / archive_name
        archive = archive_file.read_text(encoding="utf-8") if archive_file.exists() else "# Archivierte Community-Outreach-Beiträge\n\n"
        for block in old_blocks:
            marker = block.splitlines()[0].strip()
            if marker and marker not in archive:
                if not archive.endswith("\n"):
                    archive += "\n"
                archive += block.lstrip("\n")
        pointer = f"> Ältere vollständige Einträge: [`_archive/{archive_name}`](_archive/{archive_name})"
        live = header + "\n\n" + pointer + "\n\n" + "".join(live_blocks).lstrip("\n")
        _atomic_write_text(archive_file, archive)
        _atomic_write_text(self.outbox_md, live)
        return archive_count


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Community Outreach & Solution Recommender Engine")
    parser.add_argument("--workspace", default=".", help="Workspace containing the outreach state files")
    parser.add_argument("--full-run", action="store_true", help="Run the complete local planning cycle")
    parser.add_argument("--process-approvals", action="store_true", help="Process approved posts with an injected publisher")
    parser.add_argument(
        "--receipt-file", default=None,
        help="Path to a JSON PublishReceipt for --receipt-proposal-id, captured by the calling "
        "app's own session (open-compute/Playwright/Claude-in-Chrome/API) BEFORE this call. "
        "This process performs no posting itself. Requires --receipt-proposal-id.",
    )
    parser.add_argument(
        "--receipt-proposal-id", default=None,
        help="The OUTBOUND-PROPOSAL-... id the --receipt-file belongs to (binding, refuses mismatches)",
    )
    parser.add_argument("--discover-candidate", action="store_true", help="Return the next research task")
    parser.add_argument(
        "--preview-post", default=None, metavar="PROPOSAL_ID",
        help="Read-only preview of an approved proposal (what would be posted, nothing more) -- "
        "for a browser-automation step to compose and screenshot BEFORE ever submitting "
        "(T-20260926-665406367, posting je App)",
    )
    parser.add_argument(
        "--verify-proposals", action="store_true",
        help="Verify all proposals in POST-EINGANG.md against blacklist, duplicates, and real source code files",
    )
    parser.add_argument(
        "--repos-root", default=None,
        help="Local repositories root directory for code-evidence verification (default: verification.local_repos_root in config.json or $OUTREACH_REPOS_ROOT)",
    )
    parser.add_argument(
        "--org-allow", default="",
        help="Comma-separated org allowlist for phase 3 stage 1 (product cut per app, T-20260926-665406367)",
    )
    parser.add_argument("--check-inbound", action="store_true", help="Count published threads requiring monitoring")
    parser.add_argument("--archive", action="store_true", help="Archive old complete outbox entries")
    parser.add_argument("--sync-githubbot", action="store_true", help="Sync repository metadata and traffic from GitHubBot")
    parser.add_argument("--rebuild-registry", action="store_true", help="Re-render POSTVERZEICHNIS.md and its archives from history")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; do not call publishers or modify the workspace")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON only")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _build_parser().parse_args(argv)
    org_allow = [org.strip() for org in args.org_allow.split(",") if org.strip()]
    if bool(args.receipt_file) != bool(args.receipt_proposal_id):
        print(json.dumps({"status": "error", "message": "--receipt-file and --receipt-proposal-id must be given together"}))
        return 1
    publisher = FileReceiptPublisher(args.receipt_file, args.receipt_proposal_id) if args.receipt_file else None
    engine = CommunityOutreachEngine(
        args.workspace,
        dry_run=args.dry_run,
        org_allow=org_allow,
        publisher=publisher,
        repos_root=args.repos_root,
    )
    if args.sync_githubbot:
        try:
            if args.dry_run:
                sys.dont_write_bytecode = True  # the bridge lives in the workspace; a dry run leaves no __pycache__
            from githubbot_bridge import sync_githubbot_traffic

            result: Any = sync_githubbot_traffic(engine.usecases_json, dry_run=args.dry_run)
        except Exception as exc:
            result = {"status": "error", "message": str(exc)}
    else:
        try:
            if args.rebuild_registry:
                result = engine.rebuild_registry()
            elif args.verify_proposals:
                result = engine.verify_proposals(repos_root=args.repos_root)
            elif args.process_approvals:
                result = {"status": "needs-action", "outbound_results": engine.phase2_outbound_execution()}
            elif args.discover_candidate:
                result = engine.phase3_research_and_stage()
            elif args.preview_post:
                result = engine.preview_post(args.preview_post)
            elif args.check_inbound:
                result = {"status": "completed", "inbound_checks": engine.phase1_inbound_check()}
            elif args.archive:
                result = {"status": "completed", "archived_items": engine.phase4_cut_and_clue_archive()}
            else:
                result = engine.run_full_cycle()
        except HistoryUnreadable as exc:
            result = {"status": "error", "message": str(exc)}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if isinstance(result, Mapping) and result.get("status") in {"error", "failed"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
