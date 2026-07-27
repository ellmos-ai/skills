"""Discover agent boot surfaces and render an explicit ordered rule loader."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def candidate_surfaces(home: Path, project: Path | None = None) -> list[dict[str, object]]:
    """Return known user and project boot surfaces without choosing a truth."""
    candidates: list[tuple[str, str, Path]] = [
        ("codex", "user", home / ".codex" / "AGENTS.md"),
        ("codex", "user", home / "AGENTS.md"),
        ("claude", "user", home / "CLAUDE.md"),
        ("gemini", "user", home / ".gemini" / "GEMINI.md"),
    ]
    if project is not None:
        candidates.extend(
            [
                ("generic", "project", project / "AGENTS.md"),
                ("claude", "project", project / "CLAUDE.md"),
                ("gemini", "project", project / "GEMINI.md"),
                ("copilot", "project", project / ".github" / "copilot-instructions.md"),
                ("cursor", "project", project / ".cursor" / "rules"),
                ("aider", "project", project / "CONVENTIONS.md"),
                ("cline", "project", project / ".clinerules"),
                ("windsurf", "project", project / ".windsurfrules"),
            ]
        )
    return [
        {
            "provider_hint": provider,
            "scope": scope,
            "path": str(path),
            "exists": path.exists(),
            "kind": "directory" if path.is_dir() else "file",
        }
        for provider, scope, path in candidates
    ]


def render_loader(truth_sources: Iterable[str], profile_id: str, target_kind: str) -> str:
    """Render a non-writing ordered loader for explicit truth sources."""
    sources = [source for source in truth_sources if source.strip()]
    if not sources:
        raise ValueError("at least one explicit --truth source is required")
    lines = [
        "# Agent bootstrap",
        "",
        f"> Truth profile: {profile_id}",
        f"> Target kind: {target_kind}",
        "> Generated loader; edit the selected truth sources, not this file.",
        "",
        "Read and follow these files in order before starting work:",
        "",
    ]
    lines.extend(f"{index}. `{source}`" for index, source in enumerate(sources, start=1))
    lines.extend(
        [
            "",
            "If a source is missing or unreadable, report its exact path. Do not",
            "silently replace it or invent a different precedence order.",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover", help="inventory known boot surfaces")
    discover.add_argument("--home", type=Path, default=Path.home())
    discover.add_argument("--project", type=Path)

    render = subparsers.add_parser("render", help="render a loader to stdout")
    render.add_argument("--truth", action="append", required=True)
    render.add_argument("--profile-id", default="user-selected")
    render.add_argument("--target-kind", default="generic")
    return parser


def main() -> int:
    """Run discovery or render a loader preview."""
    args = build_parser().parse_args()
    if args.command == "discover":
        result = {
            "status": "discovery-only",
            "decision": None,
            "boot_surfaces": candidate_surfaces(args.home, args.project),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    print(render_loader(args.truth, args.profile_id, args.target_kind))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
