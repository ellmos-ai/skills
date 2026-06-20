#!/usr/bin/env python3
"""agent-config-sync -- Cross-agent MCP and skill synchronization (v0.2.0).

Reads three data layers:
  registry.json   (control: which tools sync how)   -> fallback registry.example.json
  config.json     (provider standard specs)
  cache.json      (resolved real paths, written on --status if missing)

Commands:
  --status    Resolve paths, check presence, report drift (read-only except cache.json).
  --plan      Print the sync plan that --apply would execute (read-only, no writes).
  --apply     Apply the plan: block-replace MCP/skills per relation (requires --yes).
              JSON format-preserving block-replace; TOML for Codex via regex section-replace.
              Each write is preceded by a timestamped backup. After writing, re-reads and
              diffs. NEVER touches real configs during tests (use --root for fixture dirs).

Claude MCP profile management (claude-code / claude-desktop) delegates to the
ellmos-controlcenter-mcp backend (resolve_profile / switch_profile MCP tools) instead of
implementing its own Claude-profile logic. The plan output signals which ControlCenter
action to call; the agent executes it at runtime via the MCP tool.

SAFETY: --apply writes ONLY inside the resolved cache paths (real agent config files).
        Tests must pass --root pointing at a temp fixture dir. Default real resolution
        is intentionally blocked when AGENT_CONFIG_SYNC_TEST_ROOT env var is set.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ── Directory layout ──────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent

# Test-isolation: if this env var is set, real-path resolution is blocked and
# --root must be supplied.  Tests set this to prevent accidental real writes.
_TEST_ROOT_ENV = "AGENT_CONFIG_SYNC_TEST_ROOT"


# ── Utilities ─────────────────────────────────────────────────────────────────


def _load_json(primary: str, fallback: str, *, skill_dir: Path = SKILL_DIR) -> tuple[dict, str]:
    p = skill_dir / primary
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")), primary
    f = skill_dir / fallback
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8")), fallback
    raise FileNotFoundError(f"Neither {primary} nor {fallback} found in {skill_dir}")


def _resolve_placeholders(path: str | None, test_root: Path | None = None) -> str | None:
    """Expand placeholder tokens to real paths (read-only; never writes)."""
    if not path:
        return path
    if test_root is not None:
        # In test mode: replace <HOME>/<APPDATA>/<APPSUPPORT> with test_root sub-dirs
        return (path
                .replace("<HOME>", str(test_root / "home"))
                .replace("~", str(test_root / "home"))
                .replace("<APPDATA>", str(test_root / "appdata"))
                .replace("<APPSUPPORT>", str(test_root / "appsupport"))
                .replace("<PROJECT>", str(test_root / "project")))
    # Block accidental real resolution in test runs
    if os.environ.get(_TEST_ROOT_ENV):
        raise RuntimeError(
            "Real path resolution blocked: AGENT_CONFIG_SYNC_TEST_ROOT is set "
            "but --root was not passed to sync.py."
        )
    home = str(Path.home())
    appdata = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
    appsupport = str(Path.home() / "Library" / "Application Support")
    return (path
            .replace("<HOME>", home)
            .replace("~", home)
            .replace("<APPDATA>", appdata)
            .replace("<APPSUPPORT>", appsupport))


def _iso_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _make_backup(path: Path) -> Path:
    """Copy file to <path>.bak.<timestamp> and return the backup path."""
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{ts}")
    shutil.copy2(path, bak)
    return bak


# ── JSON block-replace (format-preserving) ───────────────────────────────────


def _json_block_replace(target_text: str, key: str, new_block: dict) -> str:
    """Replace the value of `key` in a JSON file, preserving all other content.

    Loads the JSON, replaces the key, and re-serialises with the original
    indentation guess (2 spaces).  Non-destructive to other keys.
    """
    data = json.loads(target_text)
    data[key] = new_block
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


# ── TOML MCP block-replace (Codex config.toml) ───────────────────────────────


def _toml_mcp_block_replace(target_text: str, mcp_servers: dict) -> str:
    """Replace all [mcp_servers.*] sections in a TOML config.

    Codex uses:
        [mcp_servers.server-name]
        command = "..."
        args = [...]
        env = {...}

    Strategy:
      1. Remove all existing [mcp_servers.*] table sections from the text.
      2. Append the new sections rendered from `mcp_servers`.
      3. Preserve all other TOML content exactly.

    Note: This is a targeted regex approach for the known Codex schema, not a
    full TOML parser -- intentional to keep stdlib-only.
    """
    # Remove all existing mcp_servers sections (from [mcp_servers.X] until next [section])
    cleaned = re.sub(
        r"\[mcp_servers\.[^\]]+\][^\[]*",
        "",
        target_text,
        flags=re.DOTALL,
    )
    # Remove trailing whitespace/blank lines from cleaned text
    cleaned = cleaned.rstrip() + "\n"

    # Render new mcp_servers sections
    toml_sections: list[str] = []
    for server_name, server_cfg in sorted(mcp_servers.items()):
        lines = [f"\n[mcp_servers.{server_name}]"]
        if "command" in server_cfg:
            lines.append(f'command = "{server_cfg["command"]}"')
        if "args" in server_cfg:
            args_toml = "[" + ", ".join(f'"{a}"' for a in server_cfg["args"]) + "]"
            lines.append(f"args = {args_toml}")
        if "env" in server_cfg and server_cfg["env"]:
            env_lines = []
            for k, v in server_cfg["env"].items():
                env_lines.append(f'  {k} = "{v}"')
            lines.append("[mcp_servers." + server_name + ".env]")
            lines.extend(env_lines)
        toml_sections.append("\n".join(lines))

    if toml_sections:
        cleaned += "\n" + "\n".join(toml_sections) + "\n"

    return cleaned


# ── Cache helpers ─────────────────────────────────────────────────────────────


def _build_cache(config: dict, registry: dict, test_root: Path | None) -> dict:
    """Resolve all provider paths from config + registry into a cache dict."""
    host = registry.get("host", "<HOST>")
    tools = registry.get("tools", {})
    providers_spec = config.get("providers", {})

    cache_providers: dict = {}
    for tid, t in tools.items():
        if not t.get("installed"):
            continue
        spec = providers_spec.get(tid, {})
        mcp = spec.get("mcp", {})
        skills_spec = spec.get("skills", {})

        mcp_raw = mcp.get("path")
        skills_raw = skills_spec.get("path")

        mcp_real = _resolve_placeholders(mcp_raw, test_root)
        skills_real = _resolve_placeholders(skills_raw, test_root) if skills_raw else None

        mcp_exists: bool | None = Path(mcp_real).exists() if mcp_real and "<" not in mcp_real else None
        skills_exists: bool | None = (
            Path(skills_real).exists() if skills_real and "<" not in skills_real else None
        )

        cache_providers[tid] = {
            "mcp_path": mcp_real,
            "mcp_exists": mcp_exists,
            "skills_path": skills_real,
            "skills_exists": skills_exists,
            "resolved_via": "config",
            "last_verified": _iso_now()[:10],
        }

    return {
        "host": host,
        "resolved_at": _iso_now(),
        "providers": cache_providers,
    }


# ── --status ──────────────────────────────────────────────────────────────────


def cmd_status(args) -> int:
    test_root = Path(args.root) if getattr(args, "root", None) else None
    skill_dir = SKILL_DIR

    try:
        config, cfg_src = _load_json("config.json", "config.json", skill_dir=skill_dir)
    except FileNotFoundError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    try:
        registry, reg_src = _load_json("registry.json", "registry.example.json", skill_dir=skill_dir)
    except FileNotFoundError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    print(f"[agent-config-sync --status]  config={cfg_src}  registry={reg_src}")
    print(f"  host: {registry.get('host', '?')}")

    cache = _build_cache(config, registry, test_root)

    # Write cache.json (not gitignored for template, gitignored for real)
    cache_path = skill_dir / "cache.json"
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  cache.json aktualisiert: {len(cache['providers'])} Provider")

    providers_spec = config.get("providers", {})
    print()
    print(f"  {'Tool':<22} {'Role':<9} {'MCP format':<6} {'MCP path status'}")
    print("  " + "-" * 72)

    for tid, entry in cache["providers"].items():
        tool_reg = registry.get("tools", {}).get(tid, {})
        spec = providers_spec.get(tid, {})
        mcp_fmt = spec.get("mcp", {}).get("format", "-")
        mcp_exists = entry.get("mcp_exists")
        mcp_path = entry.get("mcp_path") or "-"

        if mcp_exists is True:
            flag = "OK"
        elif mcp_exists is False:
            flag = "MISSING -> learn-mechanism"
        else:
            flag = "?"

        print(f"  {tid:<22} {tool_reg.get('role', '-'):<9} {mcp_fmt:<6} [{flag}]  {mcp_path}")

    # Warn about UNVERIFIED providers
    unverified = [
        tid for tid, p in providers_spec.items()
        if p.get("mcp", {}).get("key") == "UNVERIFIED"
    ]
    if unverified:
        print()
        print(f"  Nicht verifizierte Anbieter (Lernmechanismus ausfuehren): {', '.join(unverified)}")

    # Summary of relations
    relations = registry.get("relations", [])
    print()
    print(f"  {len(relations)} Sync-Relationen definiert:")
    for rel in relations:
        print(f"    - {rel.get('name')}: {rel.get('mode')} {rel.get('scope')} "
              f"({rel.get('source')} -> {rel.get('members')})")

    return 0


# ── --plan ────────────────────────────────────────────────────────────────────


def cmd_plan(args) -> int:
    test_root = Path(args.root) if getattr(args, "root", None) else None
    skill_dir = SKILL_DIR

    try:
        config, _ = _load_json("config.json", "config.json", skill_dir=skill_dir)
        registry, _ = _load_json("registry.json", "registry.example.json", skill_dir=skill_dir)
    except FileNotFoundError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    try:
        cache, _ = _load_json("cache.json", "cache.example.json", skill_dir=skill_dir)
    except FileNotFoundError:
        # Build fresh cache (read-only)
        cache = _build_cache(config, registry, test_root)

    providers_spec = config.get("providers", {})
    relations = registry.get("relations", [])
    tools = registry.get("tools", {})

    print("[agent-config-sync --plan]  (read-only; no writes)")
    print()

    if not relations:
        print("  Keine Relationen in der Registry. Plan leer.")
        return 0

    for rel in relations:
        name = rel.get("name", "?")
        mode = rel.get("mode", "?")
        scope = rel.get("scope", "?")
        source_id = rel.get("source")
        members = rel.get("members", [])
        notes = rel.get("notes", "")

        print(f"  Relation '{name}'  mode={mode}  scope={scope}")
        if notes:
            print(f"    Anmerkung: {notes}")

        source_spec = providers_spec.get(source_id, {})
        source_cache = cache.get("providers", {}).get(source_id, {})

        targets = [m for m in members if m != source_id]

        if scope in ("mcp", "both"):
            source_mcp_path = source_cache.get("mcp_path")
            source_mcp_key = source_spec.get("mcp", {}).get("key", "mcpServers")
            source_installed = tools.get(source_id, {}).get("installed", False)

            print(f"    [MCP] Quelle: {source_id}  ({source_mcp_path or 'Pfad unbekannt'})")

            if source_id in ("claude-code", "claude-desktop"):
                print("    [MCP] Claude-Profile -> Backend: ellmos-controlcenter-mcp")
                print("          MCP-Tool aufrufen: resolve_profile() dann switch_profile()")
                print("          (keine eigene Claude-Profil-Logik in sync.py)")
            elif source_mcp_path and source_cache.get("mcp_exists"):
                print(f"    [MCP] Quelle existiert -> lesen (key: {source_mcp_key})")
            else:
                print(f"    [MCP] WARNUNG: Quelle nicht gefunden ({source_mcp_path})")

            for target_id in targets:
                t_spec = providers_spec.get(target_id, {})
                t_cache = cache.get("providers", {}).get(target_id, {})
                t_fmt = t_spec.get("mcp", {}).get("format", "json")
                t_key = t_spec.get("mcp", {}).get("key", "mcpServers")
                t_merge = t_spec.get("mcp", {}).get("merge", "block-replace")
                t_path = t_cache.get("mcp_path", "?")
                t_exists = t_cache.get("mcp_exists")

                if t_key == "UNVERIFIED":
                    print(f"    [MCP] -> {target_id}: UEBERSPRUNGEN (Provider nicht verifiziert; "
                          f"Lernmechanismus starten)")
                    continue

                if target_id in ("claude-code", "claude-desktop"):
                    print(f"    [MCP] -> {target_id}: via ControlCenter (switch_profile / "
                          f"generate mcp-config)")
                    continue

                action = "ERSTELLEN" if not t_exists else "BLOCK-REPLACE"
                print(f"    [MCP] -> {target_id}  format={t_fmt}  key={t_key}  "
                      f"merge={t_merge}  [{action}]  {t_path}")

        if scope in ("skills", "both"):
            source_skills_path = source_cache.get("skills_path")
            print(f"    [SKILLS] Quelle: {source_id}  ({source_skills_path or 'n/a'})")
            for target_id in targets:
                t_spec = providers_spec.get(target_id, {})
                t_skills_kind = t_spec.get("skills", {}).get("kind", "none")
                if t_skills_kind == "dir":
                    t_skills_path = cache.get("providers", {}).get(target_id, {}).get("skills_path")
                    print(f"    [SKILLS] -> {target_id}  kind=dir  {t_skills_path or '?'}")
                elif t_skills_kind == "redirect":
                    print(f"    [SKILLS] -> {target_id}  kind=redirect  "
                          f"(Bridge-Skill, kein hartes Kopieren)")
                else:
                    print(f"    [SKILLS] -> {target_id}  kind={t_skills_kind}  (nicht unterstuetzt)")

        print()

    print("  Vorgang: backup + block-replace pro Ziel, dann Verifikation (re-read + diff).")
    print("  Ausfuehren mit: --apply --yes")
    return 0


# ── --apply ───────────────────────────────────────────────────────────────────


def _read_source_mcp(source_mcp_path: str, source_mcp_key: str) -> dict | None:
    """Read MCP server block from a JSON source file."""
    p = Path(source_mcp_path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get(source_mcp_key, {})
    except json.JSONDecodeError:
        return None


def _apply_json_mcp(target_path: Path, mcp_key: str, mcp_data: dict) -> tuple[bool, str]:
    """Apply MCP block to a JSON target file. Returns (ok, message)."""
    if not target_path.parent.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        bak = _make_backup(target_path)
        text = target_path.read_text(encoding="utf-8")
    else:
        bak = None
        text = "{}\n"

    try:
        new_text = _json_block_replace(text, mcp_key, mcp_data)
    except (json.JSONDecodeError, ValueError) as exc:
        return False, f"JSON-Fehler: {exc}"

    target_path.write_text(new_text, encoding="utf-8")

    # Verify
    verify = json.loads(target_path.read_text(encoding="utf-8"))
    if verify.get(mcp_key) != mcp_data:
        if bak:
            shutil.copy2(bak, target_path)
        return False, "Verifikation fehlgeschlagen (Soll/Ist-Differenz); Backup wiederhergestellt"

    bak_msg = f" (Backup: {bak.name})" if bak else ""
    return True, f"Geschrieben + verifiziert{bak_msg}"


def _apply_toml_mcp(target_path: Path, mcp_data: dict) -> tuple[bool, str]:
    """Apply MCP block to a TOML target file (Codex). Returns (ok, message)."""
    if not target_path.parent.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        bak = _make_backup(target_path)
        text = target_path.read_text(encoding="utf-8")
    else:
        bak = None
        text = ""

    # Convert mcpServers (JSON) -> mcp_servers (TOML key-name convention)
    new_text = _toml_mcp_block_replace(text, mcp_data)
    target_path.write_text(new_text, encoding="utf-8")

    # Minimal verify: check that each server name appears
    written = target_path.read_text(encoding="utf-8")
    missing = [sname for sname in mcp_data if f"[mcp_servers.{sname}]" not in written]
    if missing:
        if bak:
            shutil.copy2(bak, target_path)
        return False, f"Verifikation fehlgeschlagen: fehlende Server {missing}; Backup wiederhergestellt"

    bak_msg = f" (Backup: {bak.name})" if bak else ""
    return True, f"Geschrieben + verifiziert{bak_msg}"


def cmd_apply(args) -> int:
    if not getattr(args, "yes", False):
        print("ERROR: --apply requires --yes to confirm. No configs were touched.", file=sys.stderr)
        print("       Run --plan first to review what would change.", file=sys.stderr)
        return 2

    test_root = Path(args.root) if getattr(args, "root", None) else None
    skill_dir = SKILL_DIR

    try:
        config, _ = _load_json("config.json", "config.json", skill_dir=skill_dir)
        registry, _ = _load_json("registry.json", "registry.example.json", skill_dir=skill_dir)
    except FileNotFoundError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    # Build/load cache
    try:
        cache_data, _ = _load_json("cache.json", "cache.example.json", skill_dir=skill_dir)
        cache_providers = cache_data.get("providers", {})
    except FileNotFoundError:
        cache_data = _build_cache(config, registry, test_root)
        cache_providers = cache_data.get("providers", {})

    providers_spec = config.get("providers", {})
    relations = registry.get("relations", [])
    tools = registry.get("tools", {})

    print("[agent-config-sync --apply]")
    print()

    errors_total = 0
    writes_total = 0

    for rel in relations:
        name = rel.get("name", "?")
        mode = rel.get("mode", "?")
        scope = rel.get("scope", "?")
        source_id = rel.get("source")
        members = rel.get("members", [])

        print(f"  Relation '{name}'  mode={mode}  scope={scope}")

        targets = [m for m in members if m != source_id]

        if scope in ("mcp", "both"):
            source_spec = providers_spec.get(source_id, {})
            source_cache = cache_providers.get(source_id, {})
            source_mcp_path = source_cache.get("mcp_path")
            source_mcp_key = source_spec.get("mcp", {}).get("key", "mcpServers")

            # Claude providers: reading a static profile JSON file works directly.
            # ControlCenter is only needed for Claude *targets* (writing) or profile selection.
            if source_id in ("claude-code", "claude-desktop"):
                # Try to read the source config directly first (simple profile JSON)
                mcp_data = _read_source_mcp(source_mcp_path, source_mcp_key) if source_mcp_path else None
                if mcp_data is None:
                    # Path not found / not resolvable -> delegate to ControlCenter
                    print(f"    [MCP] Quelle {source_id}: Direkte Datei nicht gefunden.")
                    print("          Fallback -> ellmos-controlcenter-mcp: resolve_profile()")
                    print("          MCP-Tool manuell aufrufen und Daten einpflegen.")
                    errors_total += 1
                    continue
            else:
                mcp_data = _read_source_mcp(source_mcp_path, source_mcp_key) if source_mcp_path else None
            if mcp_data is None:
                print(f"    [MCP] FEHLER: Quelldaten nicht lesbar ({source_mcp_path})")
                errors_total += 1
                continue

            for target_id in targets:
                t_spec = providers_spec.get(target_id, {})
                t_cache = cache_providers.get(target_id, {})
                t_fmt = t_spec.get("mcp", {}).get("format", "json")
                t_key = t_spec.get("mcp", {}).get("key", "mcpServers")
                t_path = t_cache.get("mcp_path")

                if t_key == "UNVERIFIED":
                    print(f"    [MCP] -> {target_id}: UEBERSPRUNGEN (nicht verifiziert)")
                    continue

                if target_id in ("claude-code", "claude-desktop"):
                    print(f"    [MCP] -> {target_id}: via ControlCenter (switch_profile); uebersprungen")
                    continue

                if not t_path:
                    print(f"    [MCP] -> {target_id}: FEHLER: kein Pfad im Cache")
                    errors_total += 1
                    continue

                target_path = Path(_resolve_placeholders(t_path, test_root) if "<" in t_path else t_path)

                if t_fmt == "toml":
                    ok, msg = _apply_toml_mcp(target_path, mcp_data)
                else:
                    ok, msg = _apply_json_mcp(target_path, t_key, mcp_data)

                status = "OK" if ok else "FEHLER"
                print(f"    [MCP] -> {target_id}  [{status}]  {msg}")
                if ok:
                    writes_total += 1
                else:
                    errors_total += 1

        if scope in ("skills", "both"):
            source_cache = cache_providers.get(source_id, {})
            source_skills_path = source_cache.get("skills_path")

            for target_id in targets:
                t_spec = providers_spec.get(target_id, {})
                t_skills_kind = t_spec.get("skills", {}).get("kind", "none")
                t_skills_path = cache_providers.get(target_id, {}).get("skills_path")

                if t_skills_kind == "redirect":
                    print(f"    [SKILLS] -> {target_id}: Bridge-Skill (kein hartes Kopieren)")
                    continue
                if t_skills_kind != "dir" or not t_skills_path or not source_skills_path:
                    print(f"    [SKILLS] -> {target_id}: uebersprungen (kind={t_skills_kind})")
                    continue

                src_dir = Path(_resolve_placeholders(source_skills_path, test_root)
                               if "<" in source_skills_path else source_skills_path)
                dst_dir = Path(_resolve_placeholders(t_skills_path, test_root)
                               if "<" in t_skills_path else t_skills_path)

                if not src_dir.exists():
                    print(f"    [SKILLS] -> {target_id}: FEHLER: Quellordner fehlt ({src_dir})")
                    errors_total += 1
                    continue

                dst_dir.mkdir(parents=True, exist_ok=True)
                copied = 0
                for src_skill_dir in src_dir.iterdir():
                    if src_skill_dir.is_dir():
                        dst_skill_dir = dst_dir / src_skill_dir.name
                        if not dst_skill_dir.exists():
                            shutil.copytree(src_skill_dir, dst_skill_dir)
                            copied += 1

                print(f"    [SKILLS] -> {target_id}: {copied} neue Skills kopiert -> {dst_dir}")
                writes_total += copied

        print()

    print(f"  Abgeschlossen: {writes_total} Schreibvorgaenge, {errors_total} Fehler.")
    if errors_total > 0:
        print(f"  Einige Schritte fehlgeschlagen -- Logs pruefen.", file=sys.stderr)
        return 1
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(
        description="agent-config-sync -- Cross-agent MCP/skill synchronization (v0.2.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", action="store_true",
                   help="Resolve paths, check presence, update cache.json (read-only for agent configs)")
    g.add_argument("--plan", action="store_true",
                   help="Print sync plan (read-only, no writes to agent configs)")
    g.add_argument("--apply", action="store_true",
                   help="Apply sync plan: block-replace MCP/skills per relation (requires --yes)")
    ap.add_argument("--yes", action="store_true",
                    help="Confirm --apply (required to actually write)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Alias for omitting --yes (no-op, forward-compat)")
    ap.add_argument("--root", metavar="DIR",
                    help="Override base dir for path resolution (tests/fixtures only)")
    args = ap.parse_args()

    if args.status:
        return cmd_status(args)
    if args.plan:
        return cmd_plan(args)
    if args.apply:
        return cmd_apply(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
