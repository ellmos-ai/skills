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
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

DEFAULT_PLATFORM_ROTATION = ["Reddit", "YouTube", "Dev.to / Foren", "GitHub Discussions"]
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
        post_text = re.search(
            r"(?:####\s+Textvorschlag:|\*\*Vorgeschlagener Beitrag:\*\*)\s*\n"
            r"```(?:markdown|text)?[ \t]*\n(.*?)\n```",
            segment,
            re.DOTALL,
        )
        if not all((approval, platform, target, repo, post_text)):
            continue

        semantic_end = post_text.end()
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
                "text": post_text.group(1).strip(),
                "approved": approval.group(1).lower() == "x",
                "raw_block": raw_block,
                "span": (heading_start, heading_start + semantic_end),
            }
        )
    return proposals


def _remove_spans(content: str, spans: list[tuple[int, int]]) -> str:
    updated = content
    for start, end in sorted(spans, reverse=True):
        updated = updated[:start] + updated[end:]
    return updated


class CommunityOutreachEngine:
    def __init__(self, workspace_dir: str | Path, dry_run: bool = False, publisher: object | None = None):
        self.workspace = Path(workspace_dir).resolve()
        self.dry_run = dry_run
        self.publisher = publisher
        self.usecases_json = self.workspace / "usecases.json"
        self.inbox_md = self.workspace / "POST-EINGANG.md"
        self.outbox_md = self.workspace / "POST-AUSGANG.md"
        self.registry_md = self.workspace / "POSTVERZEICHNIS.md"
        self.history_json = self.workspace / "posts_history.json"
        self.archive_dir = self.workspace / "_archive"
        self.config_json = self.workspace / "config.json"

    def _history(self) -> list[dict[str, Any]]:
        value = _read_json(self.history_json, [])
        return value if isinstance(value, list) else []

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
        results: list[dict[str, Any]] = []
        finalized: list[tuple[dict[str, Any], dict[str, Any], str]] = []
        publisher_attempts = 0
        max_posts = self._max_posts_per_cycle()

        for proposal in approved:
            if not _is_valid_target_url(proposal["target_url"]):
                results.append({"id": proposal["id"], "status": "invalid-target"})
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

            target_key = canonicalize_url(proposal["target_url"])
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
        _atomic_write_text(self.registry_md, self._render_registry(history))
        self._update_rotation_from_history(history)
        _atomic_write_text(self.inbox_md, _remove_spans(inbox, [proposal["span"] for proposal, _record, _status in finalized]))

    @staticmethod
    def _append_outbox_record(content: str, record: Mapping[str, Any]) -> str:
        marker = f"### [{record['post_id']}]"
        if marker in content:
            return content
        if content and not content.endswith("\n"):
            content += "\n"
        return content + f"""
### [{record['post_id']}] Veröffentlicht am {record.get('date', '')} ({record.get('platform', '')})
- **Ziel-URL:** [{record.get('target_url', '')}]({record.get('target_url', '')})
- **Veröffentlichungsbeleg:** [{record.get('platform_post_id', '')}]({record.get('published_url', '')})
- **Lösungs-Repo:** `{record.get('repo', '')}`
- **Status:** published (Receipt verifiziert)
- **Veröffentlichter Text:**
```text
{record.get('content', '')}
```

"""

    @staticmethod
    def _render_registry(history: list[dict[str, Any]]) -> str:
        rows = []
        for record in reversed(history):
            if record.get("status") != "published" or record.get("receipt_verified") is not True:
                continue
            target = str(record.get("target_url", ""))
            rows.append(
                f"| {record.get('date', '')} | {record.get('platform', '')} | "
                f"[{target}]({target}) | `{record.get('repo', '')}` | "
                f"`{record.get('post_id', '')}` | {record.get('status', '')} |"
            )
        return """# POSTVERZEICHNIS: Globaler Duplikatschutz-Index

> Eine Ziel-URL wird nur nach einem verifizierten Veröffentlichungsbeleg eingetragen.

| Datum | Plattform | Ziel-URL | Repository | Post-ID | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
""" + "\n".join(rows) + ("\n" if rows else "")

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

    def phase3_research_and_stage(self) -> dict[str, Any] | None:
        data = self._usecases()
        repositories = [repo for repo in data.get("repositories", []) if isinstance(repo, dict) and repo.get("active", True)]
        if not repositories:
            return {
                "status": "needs-action",
                "action": "configure-repositories",
                "reason": "no-active-repositories",
            }

        def last_promoted(repo: Mapping[str, Any]) -> str:
            return str(repo.get("last_promoted_at") or repo.get("last_promoted") or "1970-01-01T00:00:00")

        candidate = min(repositories, key=lambda repo: (last_promoted(repo), str(repo.get("name", ""))))
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
        problems = candidate.get("problems_solved") or candidate.get("solved_problems") or ["Allgemeine Automatisierung"]
        return {
            "status": "needs-action",
            "action": "research-and-persist-valid-draft",
            "repo_name": candidate.get("name", candidate.get("id", "")),
            "repo_url": candidate.get("url", ""),
            "platform": platform,
            "target_problem": problems[0],
            "reason": "Eine echte, aktuelle und noch nicht verwendete Ziel-URL sowie ein geprüfter Entwurf fehlen.",
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
    parser.add_argument("--discover-candidate", action="store_true", help="Return the next research task")
    parser.add_argument("--check-inbound", action="store_true", help="Count published threads requiring monitoring")
    parser.add_argument("--archive", action="store_true", help="Archive old complete outbox entries")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; do not call publishers or modify the workspace")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON only")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _build_parser().parse_args(argv)
    engine = CommunityOutreachEngine(args.workspace, dry_run=args.dry_run)
    if args.process_approvals:
        result: Any = {"status": "needs-action", "outbound_results": engine.phase2_outbound_execution()}
    elif args.discover_candidate:
        result = engine.phase3_research_and_stage()
    elif args.check_inbound:
        result = {"status": "completed", "inbound_checks": engine.phase1_inbound_check()}
    elif args.archive:
        result = {"status": "completed", "archived_items": engine.phase4_cut_and_clue_archive()}
    else:
        result = engine.run_full_cycle()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
