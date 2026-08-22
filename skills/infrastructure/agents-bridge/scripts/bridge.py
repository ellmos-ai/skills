"""Portable file contracts for small multi-provider agent systems.

The module deliberately owns only file-level bootstrap, recovery, messaging,
memory pointers, presence, and cooperative locks. It is not a scheduler,
policy registry, ticket system, or provider process launcher.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Iterable

PROFILE_SCHEMA = "agents-bridge.profile.v3"
PACKAGE_SCHEMA = "agents-bridge.package.v3"
RESTORE_SCHEMA = "agents-bridge.restore-receipt.v3"
ROLLBACK_SCHEMA = "agents-bridge.rollback-receipt.v3"
MESSAGE_SCHEMA = "agents-bridge.message.v1"
ACK_SCHEMA = "agents-bridge.ack.v1"
PROJECTION_MARKER = "agents-bridge-projection: v3"

KNOWN_SURFACES: tuple[tuple[str, str], ...] = (
    ("generic", "AGENTS.md"),
    ("generic", "GPT.md"),
    ("claude", "CLAUDE.md"),
    ("gemini", "GEMINI.md"),
    ("codex", ".codex/AGENTS.md"),
    ("codex", ".codex/GPT.md"),
    ("gemini", ".gemini/GEMINI.md"),
    ("copilot", ".github/copilot-instructions.md"),
    ("aider", "CONVENTIONS.md"),
    ("cline", ".clinerules"),
    ("windsurf", ".windsurfrules"),
)

PRIMARY_RE = re.compile(r"(?im)^\s*(?:<!--\s*)?agents-bridge-primary\s*:\s*(?:true|yes|1)\s*(?:-->)?\s*$")
POINTER_RE = re.compile(r"(?im)^\s*(?:<!--\s*)?agents-bridge-pointer\s*:\s*([^\r\n]+?)(?:\s*-->)?\s*$")
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private-key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "credential-assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|secret|password)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{16,}"
        ),
    ),
    (
        "github-token",
        re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
)
WINDOWS_HOME_RE = re.compile(r"(?i)(?:file:///)?[A-Z]:[\\/]+Users[\\/]+([^\\/\s\"'`]+)")
POSIX_HOME_RE = re.compile(r"(?i)(?:^|[\s(\"'`])/(?:home|Users)/([^/\s\"'`)]+)")
SAFE_HOME_SEGMENTS = {"<user>", "<username>", "user", "username", "runner", "test"}
ACTOR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._@-]{0,127}$")
SECRET_VARIABLE_RE = re.compile(r"(?i)^(?:api[_-]?key|access[_-]?token|auth[_-]?token|secret|password)$")


class BridgeError(ValueError):
    """An input or state violates the bridge contract."""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_now() -> str:
    return _now().isoformat().replace("+00:00", "Z")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BridgeError(f"cannot read JSON object {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BridgeError(f"expected a JSON object: {path}")
    return value


def _atomic_write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def _atomic_write_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
    _atomic_write_bytes(path, payload + b"\n")


def _exclusive_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise BridgeError(f"append-only event already exists: {path}") from exc
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def _append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(descriptor, "ab") as stream:
        stream.write(_canonical_bytes(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def normalize_relative(value: str) -> str:
    """Return a portable relative path or fail closed."""
    if not isinstance(value, str) or not value.strip():
        raise BridgeError("profile paths must be non-empty strings")
    raw = value.strip().replace("\\", "/")
    windows = PureWindowsPath(value)
    posix = PurePosixPath(raw)
    if windows.drive or windows.root or posix.is_absolute():
        raise BridgeError(f"profile path must be relative and portable: {value}")
    parts = [part for part in posix.parts if part not in {"", "."}]
    if not parts or any(part == ".." for part in parts):
        raise BridgeError(f"profile path escapes the instance root: {value}")
    return "/".join(parts)


def _under(root: Path, relative: str) -> Path:
    normalized = normalize_relative(relative)
    resolved_root = root.resolve()
    candidate = (resolved_root / Path(*PurePosixPath(normalized).parts)).resolve()
    try:
        common = os.path.commonpath([resolved_root, candidate])
    except ValueError as exc:
        raise BridgeError(f"path is outside the instance root: {relative}") from exc
    if Path(common) != resolved_root:
        raise BridgeError(f"path is outside the instance root: {relative}")
    return candidate


def _validate_actor(actor: str) -> str:
    if not isinstance(actor, str) or not ACTOR_RE.fullmatch(actor):
        raise BridgeError(f"invalid actor id: {actor!r}")
    return actor


def _all_profile_paths(profile: dict[str, Any]) -> list[str]:
    result = [profile["primary_surface"]["path"]]
    result.extend(item["path"] for item in profile["provider_surfaces"])
    result.extend(item["path"] for item in profile["truth_sources"])
    result.append(profile["memory"]["index"]["path"])
    result.extend(item["path"] for item in profile["memory"]["silos"])
    result.extend(
        (
            profile["messenger"]["root"],
            profile["presence"]["root"],
            profile["locks"]["root"],
        )
    )
    result.extend(profile.get("recovery_pointers", []))
    result.extend(profile["privacy"].get("include", []))
    return list(dict.fromkeys(normalize_relative(item) for item in result))


def validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """Validate an agents-bridge v3 profile."""
    if profile.get("schema") != PROFILE_SCHEMA:
        raise BridgeError(f"unsupported profile schema: {profile.get('schema')!r}")
    if not isinstance(profile.get("profile_id"), str) or not profile["profile_id"].strip():
        raise BridgeError("profile_id is required")
    platform = profile.get("platform")
    if not isinstance(platform, dict):
        raise BridgeError("platform profile is required")
    if platform.get("path_style") != "portable-relative":
        raise BridgeError("platform.path_style must be portable-relative")
    if str(platform.get("encoding", "")).lower() != "utf-8":
        raise BridgeError("platform.encoding must be utf-8")
    if not isinstance(platform.get("variables"), dict):
        raise BridgeError("platform.variables must be an object")
    if not all(
        isinstance(key, str) and key.strip() and isinstance(value, (str, int, float, bool, type(None)))
        for key, value in platform["variables"].items()
    ):
        raise BridgeError("platform.variables must contain named scalar values")
    primary = profile.get("primary_surface")
    if not isinstance(primary, dict) or not primary.get("path") or not primary.get("provider"):
        raise BridgeError("exactly one primary_surface with provider and path is required")
    normalize_relative(primary["path"])
    surfaces = profile.get("provider_surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise BridgeError("provider_surfaces must be a non-empty list")
    surface_ids: set[str] = set()
    surface_paths: set[str] = set()
    for surface in surfaces:
        if not isinstance(surface, dict):
            raise BridgeError("provider_surfaces entries must be objects")
        for key in ("id", "provider", "path", "strategy"):
            if not isinstance(surface.get(key), str) or not surface[key].strip():
                raise BridgeError(f"provider surface requires {key}")
        if surface["strategy"] not in {"primary", "loader", "redirect", "projection"}:
            raise BridgeError(f"unsupported provider strategy: {surface['strategy']}")
        if surface["id"] in surface_ids:
            raise BridgeError(f"duplicate provider surface id: {surface['id']}")
        normalized_path = normalize_relative(surface["path"])
        if normalized_path in surface_paths:
            raise BridgeError(f"duplicate provider surface path: {normalized_path}")
        surface_ids.add(surface["id"])
        surface_paths.add(normalized_path)
    primary_path = normalize_relative(primary["path"])
    primary_matches = [item for item in surfaces if normalize_relative(item["path"]) == primary_path]
    primary_strategies = [item for item in surfaces if item["strategy"] == "primary"]
    if len(primary_matches) != 1 or primary_matches[0]["strategy"] != "primary" or len(primary_strategies) != 1:
        raise BridgeError("primary_surface must match exactly one primary provider surface")
    if primary_matches[0]["provider"] != primary["provider"]:
        raise BridgeError("primary_surface provider must match its provider surface")
    truths = profile.get("truth_sources")
    if not isinstance(truths, list) or not truths:
        raise BridgeError("truth_sources must be a non-empty ordered list")
    truth_ids: set[str] = set()
    orders: set[int] = set()
    for truth in truths:
        if not isinstance(truth, dict):
            raise BridgeError("truth source entries must be objects")
        if not all(isinstance(truth.get(key), str) and truth[key].strip() for key in ("id", "path", "owner", "scope")):
            raise BridgeError("truth sources require id, path, owner, and scope")
        if not isinstance(truth.get("order"), int):
            raise BridgeError("truth source order must be an integer")
        normalize_relative(truth["path"])
        if truth["id"] in truth_ids or truth["order"] in orders:
            raise BridgeError("truth source ids and order values must be unique")
        truth_ids.add(truth["id"])
        orders.add(truth["order"])
    graph = profile.get("pointer_graph")
    if not isinstance(graph, list):
        raise BridgeError("pointer_graph must be a list")
    known_nodes = surface_ids | truth_ids
    for edge in graph:
        if not isinstance(edge, dict) or not all(edge.get(key) for key in ("from", "to", "kind")):
            raise BridgeError("pointer graph edges require from, to, and kind")
        if edge["from"] not in known_nodes or edge["to"] not in known_nodes:
            raise BridgeError("pointer graph edge references an unknown node")
    memory = profile.get("memory")
    if not isinstance(memory, dict) or not isinstance(memory.get("index"), dict):
        raise BridgeError("memory index is required")
    normalize_relative(memory["index"].get("path", ""))
    if not isinstance(memory.get("silos"), list):
        raise BridgeError("memory silos must be a list")
    silo_ids: set[str] = set()
    silo_paths: set[str] = set()
    for silo in memory["silos"]:
        if not isinstance(silo, dict) or not all(
            silo.get(key) for key in ("id", "path", "owner", "scope", "merge_rule")
        ):
            raise BridgeError("memory silos require id, path, owner, scope, and merge_rule")
        silo_path = normalize_relative(silo["path"])
        if silo["id"] in silo_ids or silo_path in silo_paths:
            raise BridgeError("memory silo ids and paths must be unique")
        silo_ids.add(silo["id"])
        silo_paths.add(silo_path)
        if silo.get("merge_rule") == "automatic":
            raise BridgeError("memory silos may not be merged automatically")
        if not isinstance(silo.get("refresh_rule"), str) or not silo["refresh_rule"].strip():
            raise BridgeError("memory silos require refresh_rule")
        for access_key in ("writers", "readers"):
            if not isinstance(silo.get(access_key), list):
                raise BridgeError(f"memory silo {access_key} must be a list")
    for section in ("messenger", "presence", "locks"):
        value = profile.get(section)
        if not isinstance(value, dict) or not value.get("root"):
            raise BridgeError(f"{section}.root is required")
        normalize_relative(value["root"])
    actors = profile["messenger"].get("actors")
    if not isinstance(actors, list) or not actors:
        raise BridgeError("messenger actors must be a non-empty list")
    for actor in actors:
        _validate_actor(actor)
    if profile["messenger"].get("transport") != "files":
        raise BridgeError("messenger.transport must be files")
    if profile["messenger"].get("provenance") != "append-only":
        raise BridgeError("messenger.provenance must be append-only")
    presence_ttl = profile["presence"].get("ttl_seconds")
    lock_ttl = profile["locks"].get("ttl_seconds")
    if not isinstance(presence_ttl, int) or presence_ttl <= 0:
        raise BridgeError("presence.ttl_seconds must be positive")
    if not isinstance(lock_ttl, int) or lock_ttl <= 0:
        raise BridgeError("locks.ttl_seconds must be positive")
    if profile["locks"].get("conflict_policy") != "fail-closed":
        raise BridgeError("locks.conflict_policy must be fail-closed")
    privacy = profile.get("privacy")
    if not isinstance(privacy, dict) or privacy.get("mode") not in {"reject", "redact"}:
        raise BridgeError("privacy.mode must be reject or redact")
    for key in ("include", "exclude"):
        if not isinstance(privacy.get(key, []), list):
            raise BridgeError(f"privacy.{key} must be a list")
        if not all(isinstance(item, str) and item.strip() for item in privacy.get(key, [])):
            raise BridgeError(f"privacy.{key} entries must be non-empty strings")
    _all_profile_paths(profile)
    return profile


def load_profile(path: Path) -> dict[str, Any]:
    return validate_profile(_read_json(path))


def candidate_surfaces(home: Path, project: Path | None = None) -> list[dict[str, object]]:
    """Backward-compatible inventory of known user and project boot surfaces."""
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


def discover_instance(root: Path, extra_surfaces: Iterable[str] = ()) -> dict[str, Any]:
    """Discover surfaces and explicit authority claims without choosing by name."""
    resolved_root = root.resolve()
    configured = list(KNOWN_SURFACES)
    configured.extend(("custom", normalize_relative(path)) for path in extra_surfaces)
    seen: set[str] = set()
    surfaces: list[dict[str, Any]] = []
    claims: list[dict[str, str]] = []
    for provider, relative in configured:
        normalized = normalize_relative(relative)
        if normalized in seen:
            continue
        seen.add(normalized)
        path = _under(resolved_root, normalized)
        surface: dict[str, Any] = {
            "provider": provider,
            "path": normalized,
            "exists": path.is_file(),
            "sha256": _sha256_file(path) if path.is_file() else None,
            "pointers": [],
            "authority_claim": False,
        }
        if path.is_file() and path.stat().st_size <= 2_000_000:
            text = path.read_text(encoding="utf-8", errors="replace")
            surface["authority_claim"] = bool(PRIMARY_RE.search(text))
            surface["pointers"] = [match.group(1).strip(' `"') for match in POINTER_RE.finditer(text)]
            if surface["authority_claim"]:
                claims.append({"path": normalized, "provider": provider})
        surfaces.append(surface)
    result: dict[str, Any] = {
        "schema": "agents-bridge.discovery.v3",
        "root": str(resolved_root),
        "surfaces": surfaces,
        "authority_claims": claims,
        "decision": None,
    }
    if len(claims) == 1:
        result["status"] = "selected"
        result["decision"] = {
            "primary_surface": claims[0],
            "basis": "explicit-authority-marker",
        }
    elif len(claims) > 1:
        result["status"] = "blocked"
        result["decision_briefing"] = {
            "question": "Multiple provider surfaces claim primary authority.",
            "candidates": claims,
            "required_action": ("Select exactly one primary surface and remove or demote the other claims."),
            "selection_policy": "No filename or provider preference is used.",
        }
    else:
        result["status"] = "needs-user-selection"
        result["decision_briefing"] = {
            "question": "Which existing surface is the primary authority?",
            "candidates": [{"path": item["path"], "provider": item["provider"]} for item in surfaces if item["exists"]],
            "selection_policy": "No implicit default.",
        }
    return result


def render_loader(truth_sources: Iterable[str], profile_id: str, target_kind: str) -> str:
    """Render a non-writing ordered loader for explicit truth sources."""
    sources = [source for source in truth_sources if source.strip()]
    if not sources:
        raise BridgeError("at least one explicit --truth source is required")
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


def render_profile_surface(
    profile: dict[str, Any],
    source_root: Path,
    surface_id: str,
    *,
    generated_at: str | None = None,
) -> str:
    """Render one loader or projection without writing it."""
    validate_profile(profile)
    surface = next(
        (item for item in profile["provider_surfaces"] if item["id"] == surface_id),
        None,
    )
    if surface is None:
        raise BridgeError(f"unknown provider surface id: {surface_id}")
    truths = sorted(profile["truth_sources"], key=lambda item: item["order"])
    if surface["strategy"] in {"primary", "loader", "redirect"}:
        return render_loader(
            [normalize_relative(item["path"]) for item in truths],
            profile["profile_id"],
            surface["provider"],
        )
    generated = generated_at or _iso_now()
    hashes: dict[str, str] = {}
    bodies: list[str] = []
    for truth in truths:
        relative = normalize_relative(truth["path"])
        path = _under(source_root, relative)
        if not path.is_file():
            raise BridgeError(f"projection truth source is missing: {relative}")
        value = path.read_bytes()
        hashes[relative] = _sha256_bytes(value)
        bodies.extend(
            [
                f"<!-- source-begin: {relative} -->",
                value.decode("utf-8"),
                f"<!-- source-end: {relative} -->",
                "",
            ]
        )
    header = [
        f"<!-- {PROJECTION_MARKER} -->",
        f"<!-- profile_id: {profile['profile_id']} -->",
        f"<!-- generated_at: {generated} -->",
        f"<!-- source_hashes: {json.dumps(hashes, sort_keys=True)} -->",
        "<!-- generated projection; edit the truth sources, not this file -->",
        "",
    ]
    return "\n".join(header + bodies).rstrip() + "\n"


def _privacy_findings(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append({"code": label})
    for pattern in (WINDOWS_HOME_RE, POSIX_HOME_RE):
        for match in pattern.finditer(text):
            segment = match.group(1).lower()
            if segment not in SAFE_HOME_SEGMENTS and not segment.startswith(("<", "{", "$", "%")):
                findings.append({"code": "personal-absolute-path"})
                break
    return findings


def _redact_text(text: str) -> tuple[str, list[str]]:
    codes: list[str] = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            text = pattern.sub("<redacted-secret>", text)
            codes.append(label)
    for pattern in (WINDOWS_HOME_RE, POSIX_HOME_RE):
        if pattern.search(text):
            text = pattern.sub("<user-home>", text)
            codes.append("personal-absolute-path")
    return text, sorted(set(codes))


def _package_profile(
    profile: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Privacy-gate free-form platform variables before embedding a profile."""
    result = json.loads(json.dumps(profile, ensure_ascii=False))
    variables = result["platform"]["variables"]
    codes: list[str] = []
    for key, value in variables.items():
        if not isinstance(value, str):
            continue
        findings = _privacy_findings(value)
        if SECRET_VARIABLE_RE.fullmatch(key) and value:
            findings.append({"code": "credential-assignment"})
        if not findings:
            continue
        found_codes = sorted({item["code"] for item in findings})
        if profile["privacy"]["mode"] == "reject":
            raise BridgeError(f"privacy gate rejected platform variable {key}: " + ", ".join(found_codes))
        if SECRET_VARIABLE_RE.fullmatch(key):
            variables[key] = "<redacted-secret>"
        else:
            variables[key], _ = _redact_text(value)
        codes.extend(found_codes)
    events = [{"path": "BRIDGE-PROFILE.json", "redacted": sorted(set(codes))}] if codes else []
    validate_profile(result)
    return result, events


def _is_excluded(relative: str, patterns: Iterable[str]) -> bool:
    posix = relative.replace("\\", "/")
    return any(fnmatch.fnmatch(posix, pattern) or PurePosixPath(posix).match(pattern) for pattern in patterns)


def _capture_candidates(profile: dict[str, Any], source_root: Path) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    directories: set[str] = set()
    excludes = profile["privacy"].get("exclude", [])
    surface_by_path = {normalize_relative(item["path"]): item for item in profile["provider_surfaces"]}
    for relative in _all_profile_paths(profile):
        if _is_excluded(relative, excludes):
            continue
        path = _under(source_root, relative)
        if path.is_file():
            files.add(relative)
        elif path.is_dir():
            directories.add(relative)
            for child in sorted(path.rglob("*")):
                child_relative = child.relative_to(source_root.resolve()).as_posix()
                if _is_excluded(child_relative, excludes):
                    continue
                if child.is_dir():
                    directories.add(child_relative)
                elif child.is_file():
                    files.add(child_relative)
        elif relative in surface_by_path and surface_by_path[relative]["strategy"] != "primary":
            files.add(relative)
        else:
            directories.add(relative)
    return files, directories


def capture_instance(
    profile: dict[str, Any],
    source_root: Path,
    destination: Path,
    *,
    regenerate_projections: bool = False,
) -> dict[str, Any]:
    """Capture a bounded, privacy-gated instance package."""
    validate_profile(profile)
    package_profile, profile_privacy_events = _package_profile(profile)
    source_root = source_root.resolve()
    if not source_root.is_dir():
        raise BridgeError(f"source root is not a directory: {source_root}")
    if destination.exists():
        raise BridgeError(f"capture destination already exists: {destination}")
    files, directories = _capture_candidates(profile, source_root)
    surface_by_path = {normalize_relative(item["path"]): item for item in profile["provider_surfaces"]}
    temp_parent = destination.parent.resolve()
    temp_parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=temp_parent))
    entries: list[dict[str, Any]] = []
    privacy_events: list[dict[str, Any]] = list(profile_privacy_events)
    generated_at = _iso_now()
    try:
        for relative in sorted(files):
            source = _under(source_root, relative)
            synthesized = False
            surface = surface_by_path.get(relative)
            regenerate = bool(regenerate_projections and surface and surface["strategy"] == "projection")
            if source.is_file() and not regenerate:
                value = source.read_bytes()
            else:
                if surface is None:
                    raise BridgeError(f"capture source is missing: {relative}")
                value = render_profile_surface(profile, source_root, surface["id"], generated_at=generated_at).encode(
                    "utf-8"
                )
                synthesized = True
            if b"\x00" in value:
                raise BridgeError(f"binary content is outside the file bridge contract: {relative}")
            try:
                text = value.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise BridgeError(f"non-UTF-8 content is not portable: {relative}") from exc
            original_hash = _sha256_bytes(value)
            findings = _privacy_findings(text)
            redacted: list[str] = []
            if findings:
                if profile["privacy"]["mode"] == "reject":
                    codes = ", ".join(sorted({item["code"] for item in findings}))
                    raise BridgeError(f"privacy gate rejected {relative}: {codes}")
                text, redacted = _redact_text(text)
                value = text.encode("utf-8")
                privacy_events.append({"path": relative, "redacted": redacted})
            target = _under(temp_root / "files", relative)
            _atomic_write_bytes(target, value)
            entries.append(
                {
                    "path": relative,
                    "source_sha256": original_hash,
                    "package_sha256": _sha256_bytes(value),
                    "size": len(value),
                    "redacted": redacted,
                    "synthesized": synthesized,
                    "projection": (surface_by_path.get(relative, {}).get("strategy") == "projection"),
                }
            )
        manifest = {
            "schema": PACKAGE_SCHEMA,
            "profile": package_profile,
            "profile_sha256": _sha256_bytes(_canonical_bytes(package_profile)),
            "generated_at": generated_at,
            "source_root_included": False,
            "scope": {
                "files": entries,
                "directories": sorted(directories),
                "includes": profile["privacy"].get("include", []),
                "excludes": profile["privacy"].get("exclude", []),
            },
            "privacy": {
                "mode": profile["privacy"]["mode"],
                "events": privacy_events,
                "secrets_included": False,
                "personal_absolute_paths_included": False,
            },
        }
        manifest["content_hash"] = _sha256_bytes(_canonical_bytes(manifest))
        _atomic_write_json(temp_root / "BRIDGE-MANIFEST.json", manifest)
        os.replace(temp_root, destination)
        return manifest
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise


def load_package(package: Path) -> dict[str, Any]:
    manifest = _read_json(package / "BRIDGE-MANIFEST.json")
    if manifest.get("schema") != PACKAGE_SCHEMA:
        raise BridgeError("unsupported bridge package schema")
    profile = manifest.get("profile")
    if not isinstance(profile, dict):
        raise BridgeError("bridge package has no profile")
    validate_profile(profile)
    expected_profile_hash = _sha256_bytes(_canonical_bytes(profile))
    if manifest.get("profile_sha256") != expected_profile_hash:
        raise BridgeError("bridge package profile hash mismatch")
    without_hash = {key: value for key, value in manifest.items() if key != "content_hash"}
    if manifest.get("content_hash") != _sha256_bytes(_canonical_bytes(without_hash)):
        raise BridgeError("bridge package manifest hash mismatch")
    entries = manifest.get("scope", {}).get("files")
    if not isinstance(entries, list):
        raise BridgeError("bridge package file scope is invalid")
    expected_paths: set[str] = set()
    for entry in entries:
        relative = normalize_relative(entry.get("path", ""))
        expected_paths.add(relative)
        path = _under(package / "files", relative)
        if not path.is_file() or _sha256_file(path) != entry.get("package_sha256"):
            raise BridgeError(f"bridge package hash mismatch: {relative}")
        if _privacy_findings(path.read_text(encoding="utf-8")):
            raise BridgeError(f"bridge package contains private material: {relative}")
    files_root = package / "files"
    actual_paths = (
        {path.relative_to(files_root.resolve()).as_posix() for path in files_root.rglob("*") if path.is_file()}
        if files_root.is_dir()
        else set()
    )
    if actual_paths != expected_paths:
        raise BridgeError("bridge package contains unmanifested or missing files")
    return manifest


def plan_restore(package: Path, target_root: Path) -> dict[str, Any]:
    manifest = load_package(package)
    actions: list[dict[str, Any]] = []
    for entry in manifest["scope"]["files"]:
        relative = normalize_relative(entry["path"])
        target = _under(target_root, relative)
        if target.is_symlink():
            raise BridgeError(f"restore target is a symlink: {relative}")
        if target.is_file():
            before_hash = _sha256_file(target)
            action = "unchanged" if before_hash == entry["package_sha256"] else "update"
        elif target.exists():
            raise BridgeError(f"restore target is not a regular file: {relative}")
        else:
            before_hash = None
            action = "create"
        actions.append(
            {
                "path": relative,
                "action": action,
                "before_sha256": before_hash,
                "after_sha256": entry["package_sha256"],
                "projection_drift": bool(entry.get("projection") and action == "update"),
            }
        )
    changed = [item for item in actions if item["action"] != "unchanged"]
    return {
        "schema": "agents-bridge.restore-plan.v3",
        "status": "change-required" if changed else "idempotent",
        "package_hash": manifest["content_hash"],
        "actions": actions,
        "summary": {
            "create": sum(item["action"] == "create" for item in actions),
            "update": sum(item["action"] == "update" for item in actions),
            "unchanged": sum(item["action"] == "unchanged" for item in actions),
        },
    }


def restore_instance(
    package: Path,
    target_root: Path,
    *,
    backup_root: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    """Apply one hash-bound restore with backup and readback."""
    manifest = load_package(package)
    plan = plan_restore(package, target_root)
    target_root = target_root.resolve()
    transaction_id = "restore-" + _now().strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:12]
    transaction_backup = backup_root.resolve() / transaction_id
    records: list[dict[str, Any]] = []
    for action in plan["actions"]:
        relative = action["path"]
        if action["action"] == "unchanged":
            continue
        target = _under(target_root, relative)
        current_hash = _sha256_file(target) if target.is_file() else None
        if current_hash != action["before_sha256"]:
            raise BridgeError(f"restore target changed after preview: {relative}")
        backup_relative = None
        if target.is_file():
            backup_relative = relative
            _atomic_write_bytes(_under(transaction_backup, relative), target.read_bytes())
        source = _under(package / "files", relative)
        _atomic_write_bytes(target, source.read_bytes())
        readback = _sha256_file(target)
        if readback != action["after_sha256"]:
            raise BridgeError(f"restore readback failed: {relative}")
        records.append({**action, "backup": backup_relative, "readback_sha256": readback})
    receipt = {
        "schema": RESTORE_SCHEMA,
        "transaction_id": transaction_id,
        "created_at": _iso_now(),
        "target_root": str(target_root),
        "backup_root": str(transaction_backup),
        "package_hash": manifest["content_hash"],
        "status": "unchanged" if not records else "restored",
        "files": records,
    }
    receipt["content_hash"] = _sha256_bytes(_canonical_bytes(receipt))
    _atomic_write_json(receipt_path, receipt)
    return receipt


def verify_target(package: Path, target_root: Path) -> dict[str, Any]:
    manifest = load_package(package)
    findings: list[dict[str, Any]] = []
    for entry in manifest["scope"]["files"]:
        relative = normalize_relative(entry["path"])
        target = _under(target_root, relative)
        actual = _sha256_file(target) if target.is_file() else None
        if actual != entry["package_sha256"]:
            findings.append(
                {
                    "path": relative,
                    "code": ("projection-drift" if entry.get("projection") else "content-drift"),
                    "expected_sha256": entry["package_sha256"],
                    "actual_sha256": actual,
                }
            )
    return {
        "schema": "agents-bridge.verify.v3",
        "status": "verified" if not findings else "drift",
        "package_hash": manifest["content_hash"],
        "findings": findings,
    }


def rollback_restore(receipt_path: Path) -> dict[str, Any]:
    receipt = _read_json(receipt_path)
    if receipt.get("schema") != RESTORE_SCHEMA:
        raise BridgeError("unsupported restore receipt")
    target_root = Path(receipt["target_root"])
    backup_root = Path(receipt["backup_root"])
    restored: list[str] = []
    removed: list[str] = []
    for entry in reversed(receipt.get("files", [])):
        relative = normalize_relative(entry["path"])
        target = _under(target_root, relative)
        current_hash = _sha256_file(target) if target.is_file() else None
        if current_hash != entry["after_sha256"]:
            raise BridgeError(f"rollback target drifted after restore: {relative}")
        if entry["action"] == "create":
            target.unlink()
            removed.append(relative)
        elif entry["action"] == "update":
            backup = _under(backup_root, entry["backup"])
            if not backup.is_file() or _sha256_file(backup) != entry["before_sha256"]:
                raise BridgeError(f"rollback backup is missing or corrupt: {relative}")
            _atomic_write_bytes(target, backup.read_bytes())
            restored.append(relative)
    result = {
        "schema": ROLLBACK_SCHEMA,
        "restore_receipt_hash": receipt.get("content_hash"),
        "rolled_back_at": _iso_now(),
        "status": "rolled-back",
        "restored": restored,
        "removed": removed,
    }
    rollback_path = receipt_path.with_name(receipt_path.stem + ".rollback.json")
    _atomic_write_json(rollback_path, result)
    result["receipt"] = str(rollback_path)
    return result


def _message_root(profile: dict[str, Any], root: Path) -> Path:
    validate_profile(profile)
    return _under(root, profile["messenger"]["root"])


def _event_id(prefix: str) -> str:
    return f"{prefix}-{_now().strftime('%Y%m%dT%H%M%S%f')}-{uuid.uuid4().hex[:12]}"


def send_message(
    profile: dict[str, Any],
    root: Path,
    *,
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    kind: str = "message",
) -> dict[str, Any]:
    sender = _validate_actor(sender)
    recipient = _validate_actor(recipient)
    actors = set(profile["messenger"]["actors"])
    if sender not in actors or recipient not in actors:
        raise BridgeError("message actors must be declared in the profile")
    findings = _privacy_findings(subject + "\n" + body)
    if findings:
        if profile["privacy"]["mode"] == "reject":
            raise BridgeError("message privacy gate rejected the body")
        subject, _ = _redact_text(subject)
        body, _ = _redact_text(body)
    message_id = _event_id("msg")
    message = {
        "schema": MESSAGE_SCHEMA,
        "id": message_id,
        "kind": kind,
        "from": sender,
        "to": recipient,
        "subject": subject,
        "body": body,
        "created_at": _iso_now(),
    }
    message["content_hash"] = _sha256_bytes(_canonical_bytes(message))
    base = _message_root(profile, root)
    _exclusive_write_json(base / "events" / f"{message_id}.json", message)
    _exclusive_write_json(base / "actors" / sender / "outbox" / f"{message_id}.json", message)
    _exclusive_write_json(base / "actors" / recipient / "inbox" / f"{message_id}.json", message)
    _append_jsonl(
        base / "provenance.jsonl",
        {
            "event": "sent",
            "id": message_id,
            "at": message["created_at"],
            "hash": message["content_hash"],
        },
    )
    return message


def acknowledge_message(profile: dict[str, Any], root: Path, *, actor: str, message_id: str) -> dict[str, Any]:
    actor = _validate_actor(actor)
    base = _message_root(profile, root)
    message = _read_json(base / "actors" / actor / "inbox" / f"{message_id}.json")
    if message.get("schema") != MESSAGE_SCHEMA or message.get("to") != actor:
        raise BridgeError("actor cannot acknowledge this message")
    sender = _validate_actor(message["from"])
    ack_id = _event_id("ack")
    ack = {
        "schema": ACK_SCHEMA,
        "id": ack_id,
        "message_id": message_id,
        "from": actor,
        "to": sender,
        "message_hash": message["content_hash"],
        "created_at": _iso_now(),
    }
    ack["content_hash"] = _sha256_bytes(_canonical_bytes(ack))
    _exclusive_write_json(base / "events" / f"{ack_id}.json", ack)
    _exclusive_write_json(base / "actors" / actor / "outbox" / "acks" / f"{ack_id}.json", ack)
    _exclusive_write_json(base / "actors" / sender / "receipts" / f"{message_id}.ack.json", ack)
    _append_jsonl(
        base / "provenance.jsonl",
        {
            "event": "acknowledged",
            "id": ack_id,
            "message_id": message_id,
            "at": ack["created_at"],
            "hash": ack["content_hash"],
        },
    )
    return ack


def message_status(profile: dict[str, Any], root: Path, *, sender: str, message_id: str) -> dict[str, Any]:
    sender = _validate_actor(sender)
    base = _message_root(profile, root)
    message = _read_json(base / "actors" / sender / "outbox" / f"{message_id}.json")
    receipt = base / "actors" / sender / "receipts" / f"{message_id}.ack.json"
    return {
        "schema": "agents-bridge.message-status.v1",
        "message_id": message_id,
        "message_hash": message["content_hash"],
        "status": "acknowledged" if receipt.is_file() else "pending",
        "receipt": _read_json(receipt) if receipt.is_file() else None,
    }


def memory_status(profile: dict[str, Any], root: Path) -> dict[str, Any]:
    validate_profile(profile)
    index = normalize_relative(profile["memory"]["index"]["path"])
    findings: list[dict[str, str]] = []
    if not _under(root, index).is_file():
        findings.append({"code": "missing-memory-index", "path": index})
    silos: list[dict[str, Any]] = []
    for silo in profile["memory"]["silos"]:
        relative = normalize_relative(silo["path"])
        exists = _under(root, relative).exists()
        silos.append(
            {
                "id": silo["id"],
                "path": relative,
                "owner": silo["owner"],
                "writers": silo["writers"],
                "readers": silo["readers"],
                "merge_rule": silo["merge_rule"],
                "exists": exists,
            }
        )
        if not exists:
            findings.append({"code": "missing-memory-silo", "path": relative})
    return {
        "schema": "agents-bridge.memory-status.v1",
        "status": "ready" if not findings else "incomplete",
        "index": index,
        "silos": silos,
        "findings": findings,
    }


def heartbeat(
    profile: dict[str, Any],
    root: Path,
    *,
    actor: str,
    ttl_seconds: int | None = None,
) -> dict[str, Any]:
    actor = _validate_actor(actor)
    if actor not in profile["messenger"]["actors"]:
        raise BridgeError("presence actor must be declared in messenger.actors")
    ttl = ttl_seconds or int(profile["presence"].get("ttl_seconds", 300))
    if ttl <= 0:
        raise BridgeError("presence ttl must be positive")
    now = _now()
    value = {
        "schema": "agents-bridge.presence.v1",
        "actor": actor,
        "heartbeat_at": now.isoformat().replace("+00:00", "Z"),
        "expires_at": (now + timedelta(seconds=ttl)).isoformat().replace("+00:00", "Z"),
    }
    presence_root = _under(root, profile["presence"]["root"])
    _atomic_write_json(presence_root / f"{actor}.json", value)
    return value


def presence_status(profile: dict[str, Any], root: Path) -> dict[str, Any]:
    presence_root = _under(root, profile["presence"]["root"])
    now = _now()
    actors: list[dict[str, Any]] = []
    paths = sorted(presence_root.glob("*.json")) if presence_root.is_dir() else []
    for path in paths:
        value = _read_json(path)
        try:
            expires = datetime.fromisoformat(value["expires_at"].replace("Z", "+00:00"))
            active = expires > now
        except (KeyError, TypeError, ValueError):
            active = False
        actors.append({**value, "active": active})
    return {
        "schema": "agents-bridge.presence-status.v1",
        "status": "ok",
        "actors": actors,
    }


def _lock_path(profile: dict[str, Any], root: Path, resource: str) -> Path:
    if not resource.strip():
        raise BridgeError("lock resource is required")
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", resource).strip("-.")[:48] or "resource"
    digest = hashlib.sha256(resource.encode("utf-8")).hexdigest()[:12]
    return _under(root, profile["locks"]["root"]) / f"{slug}.{digest}.lock.json"


def claim_lock(
    profile: dict[str, Any],
    root: Path,
    *,
    actor: str,
    resource: str,
    ttl_seconds: int | None = None,
) -> dict[str, Any]:
    actor = _validate_actor(actor)
    ttl = ttl_seconds or int(profile["locks"].get("ttl_seconds", 900))
    if ttl <= 0:
        raise BridgeError("lock ttl must be positive")
    path = _lock_path(profile, root, resource)
    now = _now()
    if path.is_file():
        current = _read_json(path)
        try:
            expires = datetime.fromisoformat(current["expires_at"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError):
            expires = now + timedelta(days=365)
        if current.get("owner") != actor and expires > now:
            raise BridgeError(f"resource is already claimed by {current.get('owner')}")
    value = {
        "schema": "agents-bridge.lock.v1",
        "resource": resource,
        "owner": actor,
        "claimed_at": now.isoformat().replace("+00:00", "Z"),
        "expires_at": (now + timedelta(seconds=ttl)).isoformat().replace("+00:00", "Z"),
    }
    _atomic_write_json(path, value)
    value["path"] = str(path)
    return value


def release_lock(profile: dict[str, Any], root: Path, *, actor: str, resource: str) -> dict[str, Any]:
    actor = _validate_actor(actor)
    path = _lock_path(profile, root, resource)
    current = _read_json(path)
    if current.get("owner") != actor:
        raise BridgeError("only the lock owner may release a live claim")
    path.unlink()
    return {
        "schema": "agents-bridge.lock-release.v1",
        "status": "released",
        "resource": resource,
        "owner": actor,
    }


def lock_status(profile: dict[str, Any], root: Path) -> dict[str, Any]:
    lock_root = _under(root, profile["locks"]["root"])
    now = _now()
    locks: list[dict[str, Any]] = []
    paths = sorted(lock_root.glob("*.lock.json")) if lock_root.is_dir() else []
    for path in paths:
        value = _read_json(path)
        try:
            active = datetime.fromisoformat(value["expires_at"].replace("Z", "+00:00")) > now
        except (KeyError, TypeError, ValueError):
            active = False
        locks.append({**value, "active": active, "path": str(path)})
    return {
        "schema": "agents-bridge.lock-status.v1",
        "status": "ok",
        "locks": locks,
    }


def doctor(profile: dict[str, Any], root: Path, package: Path | None = None) -> dict[str, Any]:
    validate_profile(profile)
    findings: list[dict[str, Any]] = []
    discovery = discover_instance(root, [item["path"] for item in profile["provider_surfaces"]])
    if discovery["status"] == "blocked":
        findings.append({"code": "authority-conflict", "detail": discovery["decision_briefing"]})
    for relative in _all_profile_paths(profile):
        path = _under(root, relative)
        if path.is_file() and path.stat().st_size <= 2_000_000:
            text = path.read_text(encoding="utf-8", errors="replace")
            for finding in _privacy_findings(text):
                findings.append({"path": relative, **finding})
    memory = memory_status(profile, root)
    findings.extend(memory["findings"])
    if package is not None:
        try:
            load_package(package)
        except BridgeError as exc:
            findings.append({"code": "invalid-package", "detail": str(exc)})
    return {
        "schema": "agents-bridge.doctor.v3",
        "status": "ready" if not findings else "blocked",
        "findings": findings,
        "authority": discovery,
        "memory": memory,
    }


def _json_print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="agents-bridge 3.0.0")
    sub = parser.add_subparsers(dest="command", required=True)

    discover = sub.add_parser("discover", help="inventory surfaces and explicit authority claims")
    discover.add_argument("--root", "--home", dest="root", type=Path, default=Path.home())
    discover.add_argument("--project", type=Path)
    discover.add_argument("--surface", action="append", default=[])

    render = sub.add_parser("render", help="preview an ordered loader or profile surface")
    render.add_argument("--truth", action="append")
    render.add_argument("--profile-id", default="user-selected")
    render.add_argument("--target-kind", default="generic")
    render.add_argument("--profile", type=Path)
    render.add_argument("--root", type=Path)
    render.add_argument("--surface-id")

    validate = sub.add_parser("profile-validate", help="validate a v3 profile")
    validate.add_argument("--profile", type=Path, required=True)

    capture = sub.add_parser("capture", help="privacy-gated export to a new package")
    capture.add_argument("--profile", type=Path, required=True)
    capture.add_argument("--root", type=Path, required=True)
    capture.add_argument("--output", type=Path, required=True)
    capture.add_argument(
        "--regenerate-projections",
        action="store_true",
        help="regenerate declared projections from current truth sources",
    )

    plan = sub.add_parser("plan", help="preview a restore without mutation")
    plan.add_argument("--package", type=Path, required=True)
    plan.add_argument("--target", type=Path, required=True)

    restore = sub.add_parser("restore", help="preview or apply a hash-bound restore")
    restore.add_argument("--package", type=Path, required=True)
    restore.add_argument("--target", type=Path, required=True)
    restore.add_argument("--backup-dir", type=Path)
    restore.add_argument("--receipt", type=Path)
    restore.add_argument("--apply", action="store_true")
    restore.add_argument("--yes", action="store_true")

    verify = sub.add_parser("verify", help="verify a restored target")
    verify.add_argument("--package", type=Path, required=True)
    verify.add_argument("--target", type=Path, required=True)

    rollback = sub.add_parser("rollback", help="roll back one exact restore receipt")
    rollback.add_argument("--receipt", type=Path, required=True)
    rollback.add_argument("--yes", action="store_true")

    doctor_cmd = sub.add_parser("doctor", help="read-only profile and target diagnostics")
    doctor_cmd.add_argument("--profile", type=Path, required=True)
    doctor_cmd.add_argument("--root", type=Path, required=True)
    doctor_cmd.add_argument("--package", type=Path)

    message = sub.add_parser("message", help="send, acknowledge, and inspect file messages")
    message_sub = message.add_subparsers(dest="message_command", required=True)
    send = message_sub.add_parser("send")
    send.add_argument("--profile", type=Path, required=True)
    send.add_argument("--root", type=Path, required=True)
    send.add_argument("--from", dest="sender", required=True)
    send.add_argument("--to", dest="recipient", required=True)
    send.add_argument("--subject", required=True)
    send.add_argument("--body", required=True)
    send.add_argument("--kind", choices=["message", "handoff"], default="message")
    ack = message_sub.add_parser("ack")
    ack.add_argument("--profile", type=Path, required=True)
    ack.add_argument("--root", type=Path, required=True)
    ack.add_argument("--actor", required=True)
    ack.add_argument("--message-id", required=True)
    message_status_cmd = message_sub.add_parser("status")
    message_status_cmd.add_argument("--profile", type=Path, required=True)
    message_status_cmd.add_argument("--root", type=Path, required=True)
    message_status_cmd.add_argument("--sender", required=True)
    message_status_cmd.add_argument("--message-id", required=True)

    memory = sub.add_parser("memory", help="inspect the shared index and owned silos")
    memory.add_argument("--profile", type=Path, required=True)
    memory.add_argument("--root", type=Path, required=True)

    presence = sub.add_parser("presence", help="heartbeat or inspect actor presence")
    presence_sub = presence.add_subparsers(dest="presence_command", required=True)
    heartbeat_cmd = presence_sub.add_parser("heartbeat")
    heartbeat_cmd.add_argument("--profile", type=Path, required=True)
    heartbeat_cmd.add_argument("--root", type=Path, required=True)
    heartbeat_cmd.add_argument("--actor", required=True)
    heartbeat_cmd.add_argument("--ttl-seconds", type=int)
    presence_status_cmd = presence_sub.add_parser("status")
    presence_status_cmd.add_argument("--profile", type=Path, required=True)
    presence_status_cmd.add_argument("--root", type=Path, required=True)

    lock = sub.add_parser("lock", help="claim, release, or inspect cooperative file locks")
    lock_sub = lock.add_subparsers(dest="lock_command", required=True)
    claim = lock_sub.add_parser("claim")
    claim.add_argument("--profile", type=Path, required=True)
    claim.add_argument("--root", type=Path, required=True)
    claim.add_argument("--actor", required=True)
    claim.add_argument("--resource", required=True)
    claim.add_argument("--ttl-seconds", type=int)
    release = lock_sub.add_parser("release")
    release.add_argument("--profile", type=Path, required=True)
    release.add_argument("--root", type=Path, required=True)
    release.add_argument("--actor", required=True)
    release.add_argument("--resource", required=True)
    release.add_argument("--yes", action="store_true")
    lock_status_cmd = lock_sub.add_parser("status")
    lock_status_cmd.add_argument("--profile", type=Path, required=True)
    lock_status_cmd.add_argument("--root", type=Path, required=True)
    return parser


def run(args: argparse.Namespace) -> dict[str, Any] | str:
    if args.command == "discover":
        if args.project is not None:
            return {
                "status": "discovery-only",
                "decision": None,
                "boot_surfaces": candidate_surfaces(args.root, args.project),
            }
        return discover_instance(args.root, args.surface)
    if args.command == "render":
        if args.profile:
            if not args.root or not args.surface_id:
                raise BridgeError("profile render requires --root and --surface-id")
            return render_profile_surface(load_profile(args.profile), args.root, args.surface_id)
        return render_loader(args.truth or [], args.profile_id, args.target_kind)
    if args.command == "profile-validate":
        profile = load_profile(args.profile)
        return {
            "schema": "agents-bridge.profile-validation.v3",
            "status": "valid",
            "profile_id": profile["profile_id"],
        }
    if args.command == "capture":
        manifest = capture_instance(
            load_profile(args.profile),
            args.root,
            args.output,
            regenerate_projections=args.regenerate_projections,
        )
        return {
            "schema": "agents-bridge.capture-result.v3",
            "status": "captured",
            "package": str(args.output),
            "package_hash": manifest["content_hash"],
        }
    if args.command == "plan":
        return plan_restore(args.package, args.target)
    if args.command == "restore":
        if not args.apply:
            return plan_restore(args.package, args.target)
        if not args.yes or not args.backup_dir or not args.receipt:
            raise BridgeError("restore apply requires --yes, --backup-dir, and --receipt")
        return restore_instance(
            args.package,
            args.target,
            backup_root=args.backup_dir,
            receipt_path=args.receipt,
        )
    if args.command == "verify":
        return verify_target(args.package, args.target)
    if args.command == "rollback":
        if not args.yes:
            raise BridgeError("rollback requires --yes")
        return rollback_restore(args.receipt)
    if args.command == "doctor":
        return doctor(load_profile(args.profile), args.root, args.package)
    if args.command == "message":
        profile = load_profile(args.profile)
        if args.message_command == "send":
            return send_message(
                profile,
                args.root,
                sender=args.sender,
                recipient=args.recipient,
                subject=args.subject,
                body=args.body,
                kind=args.kind,
            )
        if args.message_command == "ack":
            return acknowledge_message(profile, args.root, actor=args.actor, message_id=args.message_id)
        return message_status(profile, args.root, sender=args.sender, message_id=args.message_id)
    if args.command == "memory":
        return memory_status(load_profile(args.profile), args.root)
    if args.command == "presence":
        profile = load_profile(args.profile)
        if args.presence_command == "heartbeat":
            return heartbeat(profile, args.root, actor=args.actor, ttl_seconds=args.ttl_seconds)
        return presence_status(profile, args.root)
    if args.command == "lock":
        profile = load_profile(args.profile)
        if args.lock_command == "claim":
            return claim_lock(
                profile,
                args.root,
                actor=args.actor,
                resource=args.resource,
                ttl_seconds=args.ttl_seconds,
            )
        if args.lock_command == "release":
            if not args.yes:
                raise BridgeError("lock release requires --yes")
            return release_lock(profile, args.root, actor=args.actor, resource=args.resource)
        return lock_status(profile, args.root)
    raise BridgeError(f"unsupported command: {args.command}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except (BridgeError, OSError) as exc:
        _json_print(
            {
                "schema": "agents-bridge.error.v3",
                "status": "blocked",
                "error": str(exc),
            }
        )
        return 2
    if isinstance(result, str):
        print(result, end="" if result.endswith("\n") else "\n")
        return 0
    _json_print(result)
    return 2 if result.get("status") in {"blocked", "drift", "incomplete"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
