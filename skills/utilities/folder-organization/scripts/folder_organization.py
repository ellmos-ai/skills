#!/usr/bin/env python3
"""Read-only inventory and archive-candidate helper for folder-organization.

The script never moves, renames, edits, or deletes input files. It produces a
JSON or Markdown evidence snapshot that an agent or human can review.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SKILL_DIR / "config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "schema": 1,
    "max_files": 5000,
    "max_depth": 12,
    "hash_max_bytes": 64 * 1024 * 1024,
    "log_retention_days": 30,
    "archive_dir": "_archive",
    "trash_review_dir": "_trash_review",
    "ignore_directories": [
        ".git", ".svn", "node_modules", "__pycache__", ".pytest_cache", ".venv", "venv"
    ],
    "control_files": [
        "AGENTS.md", "CLAUDE.md", "README.md", "START.md", "STATE.md", "TODO.md",
        "DONE.md", "CHANGELOG.md", "DECISIONS.md", "MANIFEST.md",
    ],
    "log_extensions": [".log"],
    "log_exact_names": ["stderr", "stdout"],
    "log_name_tokens": ["log", "journal", "history", "trace"],
    "active_log_tokens": ["active", "current", "live", "running"],
    "evidence_log_tokens": ["audit", "evidence", "proof", "record"],
    "text_extensions": [".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".toml", ".csv"],
    "secret_policy": {
        "enabled": True,
        "protected_name_patterns": [
            ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "*.kdbx",
            "id_rsa*", "id_dsa*", "id_ecdsa*", "id_ed25519*",
            "credentials*.json", "credentials", "credentials.*", "service-account*.json",
            "secrets*.json", "secret-pointer-map.json", ".envrc", ".npmrc", ".pypirc", ".netrc",
        ],
        "protected_name_exclusions": [
            ".env.example", ".env.sample", ".env.template", ".env.dist",
            "*.example.*", "*.example", "*.sample.*", "*.sample",
            "*.template.*", "*.template", "*.dist",
        ],
        "never_semantically_open_protected": True,
        "incidental_content_detection": True,
        "max_content_scan_bytes": 131072,
        "content_signal_patterns": [
            {
                "id": "private-key-header",
                "regex": r"-----BEGIN[ A-Z0-9_-]{0,40}PRIVATE KEY-----",
            },
            {
                "id": "secret-assignment",
                "regex": (
                    r"(?im)^\s*(?:api[_-]?key|client[_-]?secret|password|access[_-]?token)"
                    r"\s*[:=]\s*[^\s]{12,}"
                ),
            },
        ],
        "cloud_detection": {
            "configured_roots": [],
            "environment_root_variables": [
                "OneDrive", "OneDriveConsumer", "OneDriveCommercial", "DROPBOX_HOME",
                "GOOGLE_DRIVE_HOME", "ICLOUD_DRIVE_HOME",
            ],
            "path_component_markers": ["onedrive", "dropbox", "google drive", "icloud drive"],
        },
        "cloud_action": "localize-after-approval",
        "local_secret_root": None,
        "pointer_mode": "control-file",
        "pointer_control_file": "SECRETS-POINTERS.md",
        "local_pointer_map": "SECRET-POINTER-MAP.json",
        "include_local_path_in_cloud_pointer": False,
        "require_destination_outside_cloud": True,
        "require_restrictive_permissions": True,
        "opaque_copy_hash_verify": True,
    },
}

VERSION_TOKEN_RE = re.compile(
    r"(?ix)(?:^|[\s._-])(?:"
    r"v(?:er(?:sion)?)?[\s._-]*\d+(?:[._-]\d+){0,3}"
    r"|20\d{2}[._-]?\d{2}(?:[._-]?\d{2})?"
    r"|old|obsolete|deprecated|backup|bak|copy(?:[\s._-]*\d+)?|final(?:[\s._-]*\d+)?"
    r")(?=$|[\s._-])"
)
LANGUAGE_TOKEN_RE = re.compile(r"(?i)(?:[._-](?:de|en|es|fr|ja|ru|zh))$")


def merge_config(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def load_config(path: Path | None) -> dict[str, Any]:
    selected = path if path is not None else (DEFAULT_CONFIG_PATH if DEFAULT_CONFIG_PATH.is_file() else None)
    if selected is None:
        config = copy.deepcopy(DEFAULT_CONFIG)
    else:
        raw = json.loads(selected.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("configuration root must be a JSON object")
        config = merge_config(DEFAULT_CONFIG, raw)
    if int(config["max_files"]) < 1 or int(config["max_depth"]) < 0:
        raise ValueError("max_files must be positive and max_depth must be non-negative")
    policy = config.get("secret_policy")
    if not isinstance(policy, dict):
        raise ValueError("secret_policy must be a JSON object")
    if policy.get("cloud_action") not in {
        "report-only", "plan-localize", "localize-after-approval"
    }:
        raise ValueError("secret_policy.cloud_action is invalid")
    if policy.get("pointer_mode") not in {"placeholder", "control-file", "sidecar"}:
        raise ValueError("secret_policy.pointer_mode is invalid")
    for field in ("local_pointer_map", "pointer_control_file"):
        value = policy.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"secret_policy.{field} must be a non-empty relative path")
        candidate = Path(value)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"secret_policy.{field} must be traversal-free and relative")
    for signal in policy.get("content_signal_patterns", []):
        if not isinstance(signal, dict) or not isinstance(signal.get("id"), str):
            raise ValueError("every content signal needs a string id")
        try:
            re.compile(str(signal.get("regex", "")))
        except re.error as exc:
            raise ValueError(f"invalid secret signal regex for {signal.get('id')}: {exc}") from exc
    return config


def sha256_file(path: Path, max_bytes: int, hash_all: bool = False) -> str | None:
    size = path.stat().st_size
    if not hash_all and size > max_bytes:
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_series_key(path: Path) -> str | None:
    stem = path.stem.lower()
    without_version = VERSION_TOKEN_RE.sub("_", stem)
    without_version = re.sub(r"[\s._-]+", "_", without_version).strip("_")
    if without_version == re.sub(r"[\s._-]+", "_", stem).strip("_"):
        return None
    return f"{path.parent.as_posix().lower()}::{without_version}::{path.suffix.lower()}"


def relationship_key(path: Path) -> str:
    stem = path.stem.lower()
    # A language token can precede a version token (guide_de_v2) or follow it.
    # Remove both repeatedly so either order converges to the same relation key.
    previous = None
    while stem != previous:
        previous = stem
        stem = VERSION_TOKEN_RE.sub("_", stem)
        stem = re.sub(r"[\s._-]+", "_", stem).strip("_")
        stem = LANGUAGE_TOKEN_RE.sub("", stem)
    stem = re.sub(r"[\s._-]+", "_", stem).strip("_")
    return f"{path.parent.as_posix().lower()}::{stem}"


def name_tokens(path: Path) -> set[str]:
    return set(re.findall(r"[^\W_]+", path.stem.lower(), flags=re.UNICODE))


def protected_secret_rule(relative: Path, config: dict[str, Any]) -> str | None:
    policy = config["secret_policy"]
    if not policy.get("enabled", True):
        return None
    name = relative.name.casefold()
    relative_text = relative.as_posix().casefold()
    local_map = Path(str(policy["local_pointer_map"]))
    local_map_text = local_map.as_posix().casefold()
    if relative_text == local_map_text or name == local_map.name.casefold():
        return "local-pointer-map"
    exclusions = [str(item).casefold() for item in policy["protected_name_exclusions"]]
    if any(fnmatchcase(name, pattern) or fnmatchcase(relative_text, pattern) for pattern in exclusions):
        return None
    for raw_pattern in policy["protected_name_patterns"]:
        pattern = str(raw_pattern).casefold()
        if fnmatchcase(name, pattern) or fnmatchcase(relative_text, pattern):
            return str(raw_pattern)
    return None


def path_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def cloud_location_suspected(path: Path, config: dict[str, Any]) -> bool:
    policy = config["secret_policy"]
    if not policy.get("enabled", True):
        return False
    cloud = policy["cloud_detection"]
    resolved = path.resolve(strict=False)
    parts = [part.casefold() for part in resolved.parts]
    markers = [str(item).casefold() for item in cloud.get("path_component_markers", [])]
    if any(marker in part for part in parts for marker in markers):
        return True

    configured_roots = [str(item) for item in cloud.get("configured_roots", [])]
    for variable in cloud.get("environment_root_variables", []):
        value = os.environ.get(str(variable))
        if value:
            configured_roots.append(value)
    for raw_root in configured_roots:
        candidate = Path(os.path.expandvars(raw_root)).expanduser()
        if not candidate.is_absolute():
            continue
        if path_within(resolved, candidate.resolve(strict=False)):
            return True
    return False


def classify_role(relative: Path, config: dict[str, Any]) -> str:
    name_upper = relative.name.upper()
    parts_lower = {part.lower() for part in relative.parts}
    if name_upper in {str(item).upper() for item in config["control_files"]}:
        return "control"
    if str(config["archive_dir"]).lower() in parts_lower:
        return "archive"
    if str(config["trash_review_dir"]).lower() in parts_lower:
        return "trash-review"
    suffix = relative.suffix.lower()
    stem = relative.stem.lower()
    tokens = name_tokens(relative)
    is_log = (
        suffix in {str(item).lower() for item in config["log_extensions"]}
        or stem in {str(item).lower() for item in config["log_exact_names"]}
        or bool(tokens & {str(item).lower() for item in config["log_name_tokens"]})
    )
    if is_log:
        if tokens & {str(item).lower() for item in config["active_log_tokens"]}:
            return "active-log"
        if tokens & {str(item).lower() for item in config["evidence_log_tokens"]}:
            return "evidence-log"
        return "rotatable-log-candidate"
    if normalized_series_key(relative):
        return "possible-version"
    if suffix in {str(item).lower() for item in config["text_extensions"]}:
        return "document"
    return "asset"


def without_markdown_examples(text: str) -> str:
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        fence_match = re.match(r"(?:(?:[-+*]|\d+[.)])\s+)?(`{3,}|~{3,})", stripped)
        if fence is None and fence_match:
            fence = fence_match.group(1)[0]
            continue
        if fence is not None:
            if re.match(rf"{re.escape(fence)}{{3,}}\s*$", stripped):
                fence = None
            continue
        if line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4:
            continue
        # Remove CommonMark inline code spans, including spans whose delimiter
        # uses multiple backticks. Marker examples inside them are not status.
        visible: list[str] = []
        offset = 0
        while offset < len(line):
            if line[offset] != "`":
                visible.append(line[offset])
                offset += 1
                continue
            end_of_run = offset
            while end_of_run < len(line) and line[end_of_run] == "`":
                end_of_run += 1
            delimiter = line[offset:end_of_run]
            closing = line.find(delimiter, end_of_run)
            if closing < 0:
                visible.append(delimiter)
                offset = end_of_run
                continue
            visible.append(" " * (closing + len(delimiter) - offset))
            offset = closing + len(delimiter)
        kept.append("".join(visible))
    return "\n".join(kept)


def normalized_marker(raw: str) -> str:
    return "SUPERSEDED" if raw.upper().startswith("SUPERSEDED") else raw.upper()


def read_text_prefix(path: Path, max_bytes: int) -> str:
    with path.open("rb") as handle:
        return handle.read(max_bytes).decode("utf-8", errors="replace")


def clue_markers_from_text(path: Path, text: str) -> list[str]:
    markers: set[str] = set()
    if path.name.lower().endswith(".clue.md"):
        markers.add("CLUE")
    if path.suffix.lower() in {".md", ".markdown", ".rst"}:
        text = without_markdown_examples(text)
    marker_pattern = r"(CLUE|OUTDATED|SUPERSEDED(?:-BY)?|REVIEW-REQUIRED)\b"
    for comment in re.findall(r"<!--(.*?)-->", text, flags=re.DOTALL):
        match = re.match(rf"\s*{marker_pattern}", comment, flags=re.IGNORECASE)
        if match:
            markers.add(normalized_marker(match.group(1)))
    line_pattern = re.compile(
        rf"(?im)^\s*(?:>\s*(?:\[![A-Z]+\]\s*)?|(?:#|//|/\*|\*)\s*)"
        rf"{marker_pattern}(?=\s|:|$)"
    )
    markers.update(normalized_marker(match.group(1)) for match in line_pattern.finditer(text))
    return sorted(markers)


def secret_signals_from_text(text: str, config: dict[str, Any]) -> list[str]:
    policy = config["secret_policy"]
    if not policy.get("enabled", True) or not policy.get("incidental_content_detection", True):
        return []
    signals = {
        str(signal["id"])
        for signal in policy["content_signal_patterns"]
        if re.search(str(signal["regex"]), text)
    }
    return sorted(signals)


def inspect_text_metadata(path: Path, config: dict[str, Any]) -> tuple[list[str], list[str]]:
    if path.suffix.lower() not in {str(item).lower() for item in config["text_extensions"]}:
        return [], []
    try:
        text = read_text_prefix(path, int(config["secret_policy"]["max_content_scan_bytes"]))
    except OSError:
        return [], []
    return clue_markers_from_text(path, text), secret_signals_from_text(text, config)


def detect_clue_markers(path: Path, config: dict[str, Any]) -> list[str]:
    return inspect_text_metadata(path, config)[0]


def iter_files(root: Path, config: dict[str, Any]) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    skipped: list[str] = []
    ignored = {str(item).lower() for item in config["ignore_directories"]}
    max_depth = int(config["max_depth"])
    max_files = int(config["max_files"])

    for current, dirs, names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        depth = len(current_path.relative_to(root).parts)
        kept_dirs = []
        for name in sorted(dirs):
            candidate = current_path / name
            if name.lower() in ignored:
                continue
            if candidate.is_symlink():
                skipped.append(candidate.relative_to(root).as_posix() + " [symlink-dir]")
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs if depth < max_depth else []
        for name in sorted(names):
            candidate = current_path / name
            relative = candidate.relative_to(root)
            if candidate.is_symlink():
                skipped.append(relative.as_posix() + " [symlink-file]")
                continue
            files.append(candidate)
            if len(files) > max_files:
                raise RuntimeError(f"max_files exceeded ({max_files})")
    return files, skipped


def build_inventory(root: Path, config: dict[str, Any], hash_all: bool = False) -> dict[str, Any]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    paths, skipped = iter_files(root, config)
    now = datetime.now(timezone.utc)
    items: list[dict[str, Any]] = []
    version_groups: dict[str, list[dict[str, Any]]] = {}
    relation_groups: dict[str, list[str]] = {}
    suggestions: list[dict[str, Any]] = []
    secret_candidates = 0
    protected_unopened = 0
    cloud_secret_candidates = 0
    policy = config["secret_policy"]

    for path in paths:
        try:
            stat = path.stat()
            relative = path.relative_to(root)
            protected_rule = protected_secret_rule(relative, config)
            cloud_suspected = cloud_location_suspected(path, config)
            secret_status: dict[str, Any] | None = None
            if protected_rule:
                role = "protected-secret-candidate"
                digest = None
                clue_markers: list[str] = []
                secret_status = {
                    "detection": "protected-name",
                    "rule": protected_rule,
                    "signal_ids": [],
                    "content_opened": False,
                    "cloud_location_suspected": cloud_suspected,
                }
                protected_unopened += 1
            else:
                role = classify_role(relative, config)
                clue_markers, signal_ids = inspect_text_metadata(path, config)
                if signal_ids:
                    role = "secret-candidate"
                    digest = None
                    secret_status = {
                        "detection": "incidental-content-signal",
                        "rule": None,
                        "signal_ids": signal_ids,
                        "content_opened": True,
                        "cloud_location_suspected": cloud_suspected,
                    }
                else:
                    digest = sha256_file(path, int(config["hash_max_bytes"]), hash_all)
            item = {
                "path": relative.as_posix(),
                "size": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "sha256": digest,
                "role": role,
                "clue_markers": clue_markers,
            }
            if secret_status:
                item["secret_status"] = secret_status
        except OSError as exc:
            suggestions.append({
                "action": "review", "path": path.relative_to(root).as_posix(),
                "confidence": "low", "reason": f"unreadable: {exc.__class__.__name__}",
            })
            continue
        items.append(item)
        if secret_status:
            secret_candidates += 1
            if cloud_suspected:
                cloud_secret_candidates += 1
            action = "review-secret-policy"
            if cloud_suspected and policy["cloud_action"] != "report-only":
                action = "plan-localize-secret"
            suggestions.append({
                "action": action,
                "path": item["path"],
                "confidence": "high" if protected_rule else "medium",
                "reason": (
                    "secret candidate; do not expose content. Cloud localization requires an "
                    "explicitly approved destination outside sync, restrictive permissions, "
                    "opaque copy/hash verification, and a non-secret pointer"
                    if cloud_suspected else
                    "secret candidate; apply configured policy without exposing content"
                ),
            })
        else:
            series = normalized_series_key(relative)
            if series:
                version_groups.setdefault(series, []).append(item)
            relation_groups.setdefault(relationship_key(relative), []).append(item["path"])

        if not secret_status and role == "rotatable-log-candidate":
            age_days = (now - datetime.fromtimestamp(stat.st_mtime, timezone.utc)).days
            if age_days >= int(config["log_retention_days"]):
                suggestions.append({
                    "action": "review-archive-log", "path": item["path"], "confidence": "low",
                    "reason": (
                        f"log-like name and age {age_days} days meet configured retention; "
                        "active/open-handle, audit, and evidence status still require review"
                    ),
                })

    candidate_version_groups = {}
    for key, group in sorted(version_groups.items()):
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda entry: entry["path"])
        candidate_version_groups[key] = [entry["path"] for entry in ordered]
        for entry in ordered:
            suggestions.append({
                "action": "review-version-chain-member", "path": entry["path"],
                "confidence": "low",
                "reason": (
                    "filename suggests a version chain; predecessor, successor, content, internal "
                    "version, and references remain unconfirmed"
                ),
            })

    related_sets = {
        key: sorted(value) for key, value in sorted(relation_groups.items()) if len(value) >= 2
    }
    config_payload = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    stable_payload = json.dumps(
        {"root": str(root), "files": items, "suggestions": suggestions},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    )
    return {
        "schema": 1,
        "root": str(root),
        "created_utc": now.isoformat(),
        "config_sha256": hashlib.sha256(config_payload.encode("utf-8")).hexdigest(),
        "snapshot_sha256": hashlib.sha256(stable_payload.encode("utf-8")).hexdigest(),
        "summary": {
            "files": len(items), "skipped": len(skipped),
            "version_groups": len(candidate_version_groups), "related_sets": len(related_sets),
            "suggestions": len(suggestions), "secret_candidates": secret_candidates,
            "protected_secret_files_not_opened": protected_unopened,
            "cloud_secret_candidates": cloud_secret_candidates,
        },
        "secret_policy": {
            "enabled": bool(policy.get("enabled", True)),
            "cloud_action": policy["cloud_action"],
            "pointer_mode": policy["pointer_mode"],
            "local_destination_configured": bool(policy.get("local_secret_root")),
            "local_destination_preflight": "not-performed-by-read-only-inventory",
            "local_path_disclosed_in_cloud_pointer": bool(
                policy.get("include_local_path_in_cloud_pointer", False)
            ),
        },
        "files": sorted(items, key=lambda entry: entry["path"]),
        "version_groups": candidate_version_groups,
        "related_sets": related_sets,
        "suggestions": sorted(suggestions, key=lambda entry: (entry["path"], entry["action"])),
        "skipped": sorted(skipped),
        "mutation_performed": False,
    }


def as_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Folder Organization Inventory", "",
        f"- Root: `{report['root']}`",
        f"- Snapshot: `{report['snapshot_sha256']}`",
        f"- Files: {summary['files']}",
        f"- Secret candidates: {summary['secret_candidates']}",
        f"- Protected secret files not opened: {summary['protected_secret_files_not_opened']}",
        f"- Suggestions: {summary['suggestions']}", "",
        "| Action | Path | Confidence | Reason |", "|---|---|---|---|",
    ]
    for item in report["suggestions"]:
        reason = str(item["reason"]).replace("|", "\\|")
        lines.append(f"| {item['action']} | `{item['path']}` | {item['confidence']} | {reason} |")
    lines.extend(["", "No mutation was performed.", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a read-only folder organization inventory.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument(
        "--out", type=Path,
        help="create a new report outside the scanned root; existing files are never overwritten",
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--hash-all", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = build_inventory(args.root, load_config(args.config), args.hash_all)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"folder-organization: {exc}", file=sys.stderr)
        return 2
    payload = (
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.format == "json" else as_markdown(report)
    )
    if args.out:
        root = args.root.resolve(strict=True)
        output = args.out.resolve(strict=False)
        try:
            output.relative_to(root)
        except ValueError:
            pass
        else:
            print("folder-organization: --out must be outside the scanned root", file=sys.stderr)
            return 2
        try:
            with output.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
        except OSError as exc:
            print(f"folder-organization: cannot create --out: {exc}", file=sys.stderr)
            return 2
        print(f"folder-organization: created inventory file; source tree unchanged: {output}")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
