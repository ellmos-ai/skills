#!/usr/bin/env python3
"""agent-config-sync -- Provider-neutral agent configuration sync (v0.3.0).

Reads three data layers:
  registry.json   (control: which tools sync how)   -> fallback registry.example.json
  config.json     (provider standard specs)
  cache.json      (resolved real paths, written on --status if missing)

Commands:
  --discover  Detect known providers, app classes and configuration surfaces.
  --offer     Offer safe sync topologies from the detected local surfaces.
  --status    Resolve paths, check presence, report drift (read-only except cache.json).
  --plan      Print the sync plan that --apply would execute (read-only, no writes).
  --apply     Apply the plan: block-replace MCP/skills per relation (requires --yes).
              JSON format-preserving block-replace; TOML for Codex via regex section-replace.
              Each write is preceded by a timestamped backup. After writing, re-reads and
              diffs. NEVER touches real configs during tests (use --root for fixture dirs).

Provider-specific read/write adapters are declared in config.json. The engine
does not infer a privileged provider or backend from an endpoint name.

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


def _provider_detected(spec: dict, resolved: dict) -> bool:
    """Return True only for locally evidenced provider presence."""
    command_found = any(shutil.which(command) for command in spec.get("commands", []))
    surface_found = any(
        resolved.get(key) is True for key in ("mcp_exists", "skills_exists", "rules_exists")
    )
    if spec.get("detection") == "command":
        return command_found
    if spec.get("detection") == "surface":
        return surface_found
    return command_found or surface_found


def _resolve_provider(spec: dict, test_root: Path | None) -> dict:
    """Resolve all supported resource surfaces for one provider."""
    result: dict = {}
    for resource in ("mcp", "skills", "rules"):
        raw = spec.get(resource, {}).get("path")
        real = _resolve_placeholders(raw, test_root) if raw else None
        result[f"{resource}_path"] = real
        result[f"{resource}_exists"] = bool(
            real and "<" not in real and Path(real).exists()
        )
    return result


def discover(config: dict, test_root: Path | None = None) -> list[dict]:
    """Inventory configured provider/app-class surfaces without writing."""
    found: list[dict] = []
    for provider_id, spec in sorted(config.get("providers", {}).items()):
        resolved = _resolve_provider(spec, test_root)
        found.append(
            {
                "id": provider_id,
                "provider": spec.get("provider", "unknown"),
                "app_class": spec.get("kind", "unknown"),
                "detected": _provider_detected(spec, resolved),
                "commands": [
                    command
                    for command in spec.get("commands", [])
                    if shutil.which(command)
                ],
                **resolved,
            }
        )
    return found


def topology_offers(items: list[dict]) -> list[dict]:
    """Build provider-axis, class-axis and all-axis offers."""
    detected = [item for item in items if item.get("detected")]
    offers: list[dict] = []

    for provider in sorted({item["provider"] for item in detected}):
        members = [item["id"] for item in detected if item["provider"] == provider]
        classes = {
            item["app_class"] for item in detected if item["provider"] == provider
        }
        if len(members) > 1 and len(classes) > 1:
            offers.append(
                {
                    "axis": "provider",
                    "label": f"{provider}: zwischen App-Klassen",
                    "members": members,
                }
            )

    for app_class in sorted({item["app_class"] for item in detected}):
        members = [
            item["id"] for item in detected if item["app_class"] == app_class
        ]
        providers = {
            item["provider"] for item in detected if item["app_class"] == app_class
        }
        if len(members) > 1 and len(providers) > 1:
            offers.append(
                {
                    "axis": "app-class",
                    "label": f"{app_class}: zwischen Anbietern",
                    "members": members,
                }
            )

    if len(detected) > 1:
        offers.append(
            {
                "axis": "all",
                "label": "alle erkannten Anbieter und App-Klassen",
                "members": [item["id"] for item in detected],
            }
        )
    return offers


def _relation_members(rel: dict, providers_spec: dict) -> list[str]:
    """Resolve explicit members or a provider/app-class selector."""
    if rel.get("members"):
        return list(dict.fromkeys(rel["members"]))

    selector = rel.get("selection", {})
    providers = set(selector.get("providers", ["*"]))
    classes = set(selector.get("app_classes", ["*"]))
    explicit = set(selector.get("members", []))
    result = []
    for provider_id, spec in providers_spec.items():
        provider_match = "*" in providers or spec.get("provider") in providers
        class_match = "*" in classes or spec.get("kind") in classes
        explicit_match = not explicit or provider_id in explicit
        if provider_match and class_match and explicit_match:
            result.append(provider_id)
    return result


def cmd_discover(args) -> int:
    test_root = Path(args.root) if getattr(args, "root", None) else None
    try:
        config, cfg_src = _load_json("config.json", "config.json", skill_dir=SKILL_DIR)
    except FileNotFoundError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    items = discover(config, test_root)
    print(f"[agent-config-sync --discover] config={cfg_src}")
    print(f"  {'Endpoint':<22} {'Provider':<12} {'Klasse':<8} {'Status':<12} Oberflächen")
    print("  " + "-" * 90)
    for item in items:
        surfaces = [
            name
            for name in ("mcp", "skills", "rules")
            if item.get(f"{name}_exists")
        ]
        if item.get("commands"):
            surfaces.append("cli")
        status = "ERKANNT" if item["detected"] else "nicht belegt"
        print(
            f"  {item['id']:<22} {item['provider']:<12} "
            f"{item['app_class']:<8} {status:<12} {', '.join(surfaces) or '-'}"
        )
    print()
    print("  Erkennung ist Inventar, keine Sync-Freigabe. Quelle und Ziele wählt der User.")
    return 0


def cmd_offer(args) -> int:
    test_root = Path(args.root) if getattr(args, "root", None) else None
    try:
        config, _ = _load_json("config.json", "config.json", skill_dir=SKILL_DIR)
    except FileNotFoundError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1

    offers = topology_offers(discover(config, test_root))
    print("[agent-config-sync --offer] read-only")
    if not offers:
        print("  Keine belegte Mehrfach-Topologie gefunden.")
        return 0
    for index, offer in enumerate(offers, start=1):
        print(f"  {index}. [{offer['axis']}] {offer['label']}")
        print(f"     Mitglieder: {', '.join(offer['members'])}")
    print()
    print("  Nächste Entscheidung: Ressourcen, Truth-Quelle(n), Richtung und Ziele.")
    return 0


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
        members = _relation_members(rel, providers_spec)
        notes = rel.get("notes", "")

        print(f"  Relation '{name}'  mode={mode}  scope={scope}")
        if notes:
            print(f"    Anmerkung: {notes}")

        truth_sources = rel.get("truth", {}).get("sources", [])
        has_file_truth = scope in ("rules", "all") and bool(truth_sources)
        if not source_id and not has_file_truth:
            print("    BLOCKIERT: keine Truth-Quelle gewählt; keine Mutation geplant.")
            print("    Setze 'source' oder 'truth.sources' erst nach einer User-Entscheidung.")
            print()
            continue

        source_spec = providers_spec.get(source_id, {})
        source_cache = cache.get("providers", {}).get(source_id, {})

        targets = [m for m in members if m != source_id] if source_id else members

        if scope in ("rules", "all"):
            truth = rel.get("truth", {})
            sources = truth.get("sources", [])
            strategy = truth.get("strategy")
            print(f"    [RULES] Quellen: {sources or '[nicht gewählt]'}")
            print(f"    [RULES] Strategie: {strategy or '[nicht gewählt]'}")
            print(f"    [RULES] Ziele: {targets}")
            print("    [RULES] Apply gesperrt, bis ein User einen Adapter gewählt hat.")

        if scope in ("mcp", "both"):
            source_mcp_path = source_cache.get("mcp_path")
            source_mcp_key = source_spec.get("mcp", {}).get("key", "mcpServers")
            source_installed = tools.get(source_id, {}).get("installed", False)

            print(f"    [MCP] Quelle: {source_id}  ({source_mcp_path or 'Pfad unbekannt'})")

            source_adapter = source_spec.get("mcp", {}).get("read_adapter")
            if source_mcp_path and source_cache.get("mcp_exists"):
                print(f"    [MCP] Quelle existiert -> lesen (key: {source_mcp_key})")
            elif source_adapter:
                print(f"    [MCP] Quelle über konfigurierten Adapter lesen: {source_adapter}")
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

                write_adapter = t_spec.get("mcp", {}).get("write_adapter")
                if write_adapter:
                    print(f"    [MCP] -> {target_id}: via Adapter {write_adapter}")
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
        members = _relation_members(rel, providers_spec)

        print(f"  Relation '{name}'  mode={mode}  scope={scope}")

        if scope in ("rules", "all"):
            print("    FEHLER: Regeldatei-Apply braucht einen explizit gewählten Adapter.")
            errors_total += 1
            print()
            continue

        if not source_id:
            print("    FEHLER: keine Truth-Quelle gewählt; Relation bleibt unverändert.")
            errors_total += 1
            print()
            continue

        targets = [m for m in members if m != source_id]

        if scope in ("mcp", "both"):
            source_spec = providers_spec.get(source_id, {})
            source_cache = cache_providers.get(source_id, {})
            source_mcp_path = source_cache.get("mcp_path")
            source_mcp_key = source_spec.get("mcp", {}).get("key", "mcpServers")

            mcp_data = (
                _read_source_mcp(source_mcp_path, source_mcp_key)
                if source_mcp_path
                else None
            )
            if mcp_data is None:
                read_adapter = source_spec.get("mcp", {}).get("read_adapter")
                if read_adapter:
                    print(
                        f"    [MCP] FEHLER: Quelle braucht Adapter {read_adapter}; "
                        "direkter Apply bleibt gesperrt."
                    )
                else:
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

                write_adapter = t_spec.get("mcp", {}).get("write_adapter")
                if write_adapter:
                    print(
                        f"    [MCP] -> {target_id}: Adapter {write_adapter} erforderlich; "
                        "direkter Write uebersprungen"
                    )
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
        description="agent-config-sync -- provider-neutral config synchronization (v0.3.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--discover", action="store_true",
                   help="Detect known providers, app classes and config surfaces")
    g.add_argument("--offer", action="store_true",
                   help="Offer provider/class/all-axis topologies (read-only)")
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

    if args.discover:
        return cmd_discover(args)
    if args.offer:
        return cmd_offer(args)
    if args.status:
        return cmd_status(args)
    if args.plan:
        return cmd_plan(args)
    if args.apply:
        return cmd_apply(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
