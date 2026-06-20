#!/usr/bin/env python3
"""versionctl -- .SKILLS Versionierungs- und Registry-Verwaltungs-CLI.

Etappe 5 des UMSETZUNGSPLAN.md.

Befehle:
  status            Drift zwischen skills/ und produktiver Registry zeigen
  validate          Skills gegen Schemas + CONVENTIONS pruefen
  inventory         Inventory-Report (reproduzierbar) neu erzeugen
  registry-generate Produktive registry/ aus Skill-Bestand erzeugen

Keine externen Abhaengigkeiten ausser stdlib.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── Verzeichnisse ───

TOOLS_DIR = Path(__file__).parent
SKILLS_DIR = TOOLS_DIR / "skills"
SCHEMAS_DIR = TOOLS_DIR / "schemas"
REGISTRY_DIR = TOOLS_DIR / "registry"
REPORTS_DIR = TOOLS_DIR / "_reports"

# Windows Encoding Fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# ─── YAML-Frontmatter Parser (aus catalog.py, ohne externe Abhaengigkeit) ───


def parse_frontmatter(filepath: Path) -> dict | None:
    """Liest YAML-Frontmatter aus einer SKILL.md Datei."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    data: dict = {}
    current_key: str | None = None

    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        kv = re.match(r"^(\w[\w.-]*)\s*:\s*(.*)$", line)
        if kv and not line.startswith(" "):
            key, val = kv.group(1), kv.group(2).strip()
            current_key = key

            if val == ">":
                data[key] = ""
            elif val in ("", "null", "~"):
                data[key] = None
            elif val.lower() in ("true", "false"):
                data[key] = val.lower() == "true"
            elif val.startswith("[") and val.endswith("]"):
                items = [i.strip().strip("'\"") for i in val[1:-1].split(",") if i.strip()]
                data[key] = items
            elif val.startswith('"') and val.endswith('"'):
                data[key] = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                data[key] = val[1:-1]
            else:
                data[key] = val
            continue

        nested_kv = re.match(r"^(\s+)(\w[\w.-]*)\s*:\s*(.*)$", line)
        if nested_kv:
            nkey = nested_kv.group(2)
            nval = nested_kv.group(3).strip()

            if nval in ("", "null", "~"):
                nval = None
            elif nval.lower() in ("true", "false"):
                nval = nval.lower() == "true"
            elif nval.startswith("[") and nval.endswith("]"):
                nval = [i.strip().strip("'\"") for i in nval[1:-1].split(",") if i.strip()]
            elif nval.startswith('"') and nval.endswith('"'):
                nval = nval[1:-1]
            elif nval.startswith("'") and nval.endswith("'"):
                nval = nval[1:-1]

            if current_key and isinstance(data.get(current_key), dict):
                data[current_key][nkey] = nval
            elif current_key:
                data[current_key] = {nkey: nval}
            continue

        if current_key and isinstance(data.get(current_key), str) and line.startswith("  "):
            data[current_key] += stripped + " "

    for k, v in data.items():
        if isinstance(v, str):
            data[k] = v.strip()

    return data


# ─── Skill Discovery ───


def _get_git_tracked_skill_paths(root_dir: Path) -> set[str] | None:
    """Gibt die Menge aller von Git getrackten SKILL.md-Relativpfade zurueck.

    Gibt None zurueck wenn git nicht verfuegbar ist oder das Verzeichnis kein Repo ist
    (Fallback: alle Dateien verwenden, aber das ist nur fuer Tests relevant).
    Relative Pfade werden mit Forward-Slashes normalisiert.
    """
    import subprocess

    try:
        result = subprocess.run(
            ["git", "ls-files", "--", "skills/**/SKILL.md", "skills/*/SKILL.md"],
            capture_output=True,
            text=True,
            cwd=str(root_dir),
            timeout=10,
        )
        if result.returncode != 0:
            return None
        tracked = set()
        for line in result.stdout.splitlines():
            line = line.strip()
            if line:
                # Normalisieren auf Forward-Slashes
                tracked.add(line.replace("\\", "/"))
        return tracked if tracked else None
    except Exception:
        return None


def find_all_skills(skills_dir: Path = SKILLS_DIR, tracked_only: bool = True) -> list[tuple[Path, dict]]:
    """Findet alle SKILL.md Dateien und parst deren Frontmatter.

    Mit tracked_only=True (Standard) werden nur von Git getrackte Skills einbezogen.
    So werden .gitignore-ausgeschlossene private Skills nicht in die Registry aufgenommen.
    Falls Git nicht verfuegbar ist, wird auf alle vorhandenen Dateien zurueckgefallen.
    """
    root_dir = skills_dir.parent  # Repo-Wurzel (enthaelt .git)

    # Git-getrackte Pfade ermitteln (relativ zur Repo-Wurzel, Forward-Slashes)
    tracked_paths: set[str] | None = None
    if tracked_only:
        tracked_paths = _get_git_tracked_skill_paths(root_dir)

    results = []
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        rel = skill_md.relative_to(skills_dir)
        parts = rel.parts
        if parts[0].startswith("_"):
            continue

        # Filter: nur Git-getrackte Skills (falls tracked_paths bekannt)
        if tracked_paths is not None:
            # Relativpfad von Repo-Wurzel
            rel_from_root = skill_md.relative_to(root_dir)
            rel_str = str(rel_from_root).replace("\\", "/")
            if rel_str not in tracked_paths:
                continue

        fm = parse_frontmatter(skill_md)
        if fm:
            fm["_path"] = str(skill_md.parent.relative_to(skills_dir))
            results.append((skill_md, fm))
    return results


# ─── Content Hashing ───


def sha256_file(path: Path) -> str:
    """SHA-256 Hash einer Datei als 'sha256:<hex>'."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return f"sha256:{h.hexdigest()}"


# ─── Minimaler JSON-Schema-Validator (stdlib, unterstuetzt allOf + lokale $ref) ───


def _load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _resolve_ref(ref: str, base_dir: Path) -> dict:
    """Loedt ein relatives $ref-Schema."""
    ref_path = base_dir / ref
    return _load_schema(ref_path)


def _collect_required(schema: dict, base_dir: Path) -> set:
    """Sammelt alle required-Felder aus schema + allOf-Branches."""
    required: set = set(schema.get("required", []))
    for branch in schema.get("allOf", []):
        if "$ref" in branch:
            sub = _resolve_ref(branch["$ref"], base_dir)
            required |= _collect_required(sub, base_dir)
        else:
            required |= set(branch.get("required", []))
    return required


def _collect_properties(schema: dict, base_dir: Path) -> dict:
    """Sammelt properties aus schema + allOf-Branches."""
    props: dict = dict(schema.get("properties", {}))
    for branch in schema.get("allOf", []):
        if "$ref" in branch:
            sub = _resolve_ref(branch["$ref"], base_dir)
            props.update(_collect_properties(sub, base_dir))
        else:
            props.update(branch.get("properties", {}))
    return props


def validate_against_schema(data: dict, schema_path: Path) -> list[str]:
    """
    Validiert data gegen ein JSON-Schema.
    Unterstuetzt: type, required, enum, pattern, minLength, allOf, $ref.
    Gibt eine Liste von Fehlermeldungen zurueck (leer = valid).
    """
    schema = _load_schema(schema_path)
    base_dir = schema_path.parent
    errors: list[str] = []

    required = _collect_required(schema, base_dir)
    for field in sorted(required):
        if field not in data:
            errors.append(f"Pflichtfeld fehlt: '{field}'")

    all_props = _collect_properties(schema, base_dir)

    def check_value(field: str, value, prop_schema: dict) -> list[str]:
        errs = []
        types = prop_schema.get("type")
        if types is not None:
            if isinstance(types, list):
                allowed = [t for t in types if t != "null"]
                if value is not None:
                    type_ok = any(_check_type(value, t) for t in allowed)
                    if not type_ok:
                        errs.append(f"'{field}': falscher Typ (erwartet {types}, erhalten {type(value).__name__})")
            elif types == "null":
                pass
            else:
                if not _check_type(value, types):
                    errs.append(f"'{field}': falscher Typ (erwartet {types}, erhalten {type(value).__name__})")

        if "enum" in prop_schema and value not in prop_schema["enum"]:
            errs.append(f"'{field}': ungültiger Wert '{value}' (erlaubt: {prop_schema['enum']})")

        if "pattern" in prop_schema and isinstance(value, str):
            if not re.match(prop_schema["pattern"], value):
                errs.append(f"'{field}': Wert '{value}' stimmt nicht mit Pattern '{prop_schema['pattern']}' überein")

        if "minLength" in prop_schema and isinstance(value, str):
            if len(value) < prop_schema["minLength"]:
                errs.append(f"'{field}': zu kurz (min {prop_schema['minLength']} Zeichen)")

        return errs

    def _check_type(value, t: str) -> bool:
        return {
            "string": isinstance(value, str),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": isinstance(value, bool),
            "array": isinstance(value, list),
            "object": isinstance(value, dict),
        }.get(t, True)

    for field, prop_schema in all_props.items():
        if field in data and data[field] is not None:
            errors.extend(check_value(field, data[field], prop_schema))

    return errors


# ─── Registry-Eintrag erzeugen ───


def _derive_component_id(category: str, name: str, skill_type: str) -> str:
    """Erzeugt eine stabile Registry-ID aus Typ:Kategorie:Name.
    Verwendet nur lowercase alphanumerische Zeichen, Bindestriche und Punkte."""
    t = (skill_type or "skill").lower().replace(" ", "-").replace("_", "-")
    cat = (category or "general").lower().replace("_", "-")
    n = (name or "unknown").lower().replace(" ", "-").replace("_", "-")
    # Nicht-erlaubte Zeichen entfernen (nur [a-z0-9.-] erlaubt)
    t = re.sub(r"[^a-z0-9.-]", "-", t)
    cat = re.sub(r"[^a-z0-9.-]", "-", cat)
    n = re.sub(r"[^a-z0-9.-]", "-", n)
    return f"{t}:{cat}:{n}"


def _build_registry_entry(skill_md: Path, fm: dict, skills_dir: Path) -> dict:
    """Baut einen schema-validen Registry-Eintrag aus Frontmatter + Datei."""
    fpath_normalized = fm["_path"].replace("\\", "/")
    rel_path = "skills/" + fpath_normalized + "/SKILL.md"
    content_hash = sha256_file(skill_md)

    category = fpath_normalized.split("/")[0]
    name = fm.get("name", skill_md.parent.name)
    skill_type = fm.get("type", "skill")

    component_id = _derive_component_id(category, name, skill_type)

    # Provenance aus Frontmatter
    prov_fm = fm.get("provenance", {})
    if not isinstance(prov_fm, dict):
        prov_fm = {}
    provenance = {
        "origin": prov_fm.get("origin") or fm.get("bach_origin_path") or None,
        "origin_path": prov_fm.get("origin_path") or fm.get("provenance_origin_path") or None,
        "origin_version": prov_fm.get("origin_version") or None,
        "origin_commit": prov_fm.get("origin_commit") or None,
        "last_sync_from_origin": prov_fm.get("last_sync_from_origin") or None,
        "last_sync_to_origin": prov_fm.get("last_sync_to_origin") or None,
        "local_changes_since_sync": prov_fm.get("local_changes_since_sync"),
    }
    # Felder aus Flach-Frontmatter (catalog.py-Konvention)
    if provenance["origin"] is None:
        provenance["origin"] = fm.get("provenance_origin") or None

    # Ownership-Heuristik
    is_private = bool(fm.get("private") or fm.get("private_marker"))
    source_kind = "own"
    neutrality = "neutral-candidate"
    proposed_class = "own-neutral"
    if is_private:
        neutrality = "personalized"
        proposed_class = "own-personal-fork"

    # Privacy-Heuristik
    privacy_level = "private" if is_private else "public"
    export_allowed = not is_private

    # Kompatibilitaet
    compat = {
        "anthropic": bool(fm.get("anthropic_compatible") or fm.get("standalone")),
        "bach": bool(fm.get("bach_compatible") or fm.get("bach_origin")),
        "promptboard": None,
        "profiprompt": None,
        "explorerpro": None,
    }

    # Skill-Metadaten
    skill_dir = skill_md.parent
    all_files = [f for f in skill_dir.rglob("*") if f.is_file()]
    has_scripts = any(f.suffix in (".py", ".sh", ".js", ".ts", ".bat", ".ps1") for f in all_files)
    has_references = (skill_dir / "references").is_dir() or any(
        "ref" in f.name.lower() for f in all_files if f.suffix == ".md"
    )
    has_assets = any(f.suffix in (".png", ".jpg", ".svg", ".gif", ".pdf") for f in all_files)
    has_tests = (skill_dir / "tests").is_dir() or any("test" in f.name.lower() for f in all_files)

    warnings = []
    if not fm.get("version"):
        warnings.append("version fehlt im Frontmatter")
    if not fm.get("description") and not fm.get("description_de"):
        warnings.append("description fehlt")

    return {
        "id": component_id,
        "name": name,
        "type": skill_type,
        "path": rel_path,
        "category": category,
        "version": fm.get("version") or "0.0.0",
        "schema_version": "skill-v1",
        "status": fm.get("status") or "active",
        "content_hash": content_hash,
        "git_commit": None,
        "provenance": provenance,
        "ownership": {
            "source_kind": source_kind,
            "neutrality": neutrality,
            "proposed_class": proposed_class,
            "upstream_component": None,
            "personalized_for": None,
            "sanitization_required": is_private,
        },
        "privacy": {
            "level": privacy_level,
            "export_allowed": export_allowed,
            "contains_local_paths": is_private,
            "contains_personal_data": is_private,
        },
        "compatibility": compat,
        "fork": {
            "is_fork": False,
            "fork_of": None,
            "fork_reason": None,
            "merge_policy": None,
        },
        "branch": {
            "name": "main",
            "base": None,
            "purpose": "current source tree baseline",
        },
        "skill": {
            "standalone": fm.get("standalone"),
            "has_scripts": has_scripts,
            "has_references": has_references,
            "has_assets": has_assets,
            "has_tests": has_tests,
            "language": fm.get("language"),
            "file_count": len(all_files),
        },
        "warnings": warnings,
    }


# ─── Befehle ───


def cmd_status(args) -> int:
    """Drift zwischen skills/ und produktiver Registry zeigen."""
    registry_file = REGISTRY_DIR / "components.json"

    if not registry_file.exists():
        print("Registry nicht gefunden. Zuerst 'versionctl registry-generate' ausfuehren.")
        return 1

    registry_data = json.loads(registry_file.read_text(encoding="utf-8"))
    components = registry_data.get("components", [])
    registry_index = {c["path"]: c for c in components}

    skills = find_all_skills(SKILLS_DIR)
    drift_count = 0
    new_count = 0
    ok_count = 0

    print(f"\nversionctl status -- Drift: skills/ vs. registry/components.json")
    print(f"{'Skill':<35} {'Status':<15} {'Details'}")
    print("─" * 80)

    for skill_md, fm in skills:
        rel_path = "skills/" + fm["_path"].replace("\\", "/").rstrip("/") + "/SKILL.md"
        current_hash = sha256_file(skill_md)
        reg_entry = registry_index.get(rel_path)

        if reg_entry is None:
            status = "NEU (nicht in Registry)"
            new_count += 1
            print(f"  {fm.get('name', '?'):<33} {'NEU':<15} {rel_path}")
        elif reg_entry.get("content_hash") != current_hash:
            status = "DRIFT (Hash geaendert)"
            drift_count += 1
            print(f"  {fm.get('name', '?'):<33} {'DRIFT':<15} {rel_path}")
        else:
            ok_count += 1

    # Skills in Registry aber nicht in skills/
    skill_paths = {
        "skills/" + fm["_path"].replace("\\", "/").rstrip("/") + "/SKILL.md"
        for _, fm in skills
    }
    removed = [c for c in components if c["path"] not in skill_paths]
    for c in removed:
        print(f"  {c.get('name', '?'):<33} {'NUR REGISTRY':<15} {c['path']}")

    print()
    print(f"  OK: {ok_count}  |  NEU: {new_count}  |  DRIFT: {drift_count}  |  Nur-Registry: {len(removed)}")
    if drift_count == 0 and new_count == 0 and len(removed) == 0:
        print("  Registry ist aktuell.")
    else:
        print("  'versionctl registry-generate' empfohlen.")
    print()
    return 0


def cmd_validate(args) -> int:
    """Alle Skills gegen Schemas + CONVENTIONS pruefen."""
    schema_file = SCHEMAS_DIR / "skill-v1.schema.json"

    if not schema_file.exists():
        print(f"FEHLER: Schema nicht gefunden: {schema_file}")
        return 1

    skills = find_all_skills(SKILLS_DIR)
    total_errors = 0
    skills_with_errors = 0

    print(f"\nversionctl validate -- {len(skills)} Skills gegen skill-v1.schema.json")
    print("─" * 80)

    for skill_md, fm in skills:
        rel_path = fm["_path"].replace("\\", "/")
        name = fm.get("name", skill_md.parent.name)

        # Registry-Eintrag bauen und validieren
        entry = _build_registry_entry(skill_md, fm, SKILLS_DIR)
        errors = validate_against_schema(entry, schema_file)

        # Frontmatter-Pflichtfelder pruefen (docs/CONVENTIONS.md)
        required_fm = ["name", "version", "type", "author", "created", "updated", "description"]
        for field in required_fm:
            if not fm.get(field):
                errors.append(f"CONVENTIONS: Frontmatter-Pflichtfeld '{field}' fehlt oder leer")

        if errors:
            skills_with_errors += 1
            total_errors += len(errors)
            print(f"\n  FEHLER: skills/{rel_path}/SKILL.md")
            for err in errors:
                print(f"    - {err}")
        elif args.verbose:
            print(f"  OK:     skills/{rel_path}/SKILL.md")

    print()
    if total_errors == 0:
        print(f"  Alle {len(skills)} Skills valide.")
    else:
        print(f"  {skills_with_errors} Skills mit Fehlern, {total_errors} Fehler gesamt.")
    print()
    return 1 if total_errors > 0 else 0


def cmd_inventory(args) -> int:
    """Inventory-Report reproduzierbar neu erzeugen."""
    skills = find_all_skills(SKILLS_DIR)
    today = datetime.now(timezone.utc).date().isoformat()
    out_path = REPORTS_DIR / f"inventory-{today}.json"

    if args.output:
        out_path = Path(args.output)

    categories: dict[str, int] = {}
    types: dict[str, int] = {}
    private_count = 0
    entries = []

    for skill_md, fm in skills:
        fpath_normalized = fm["_path"].replace("\\", "/")
        category = fpath_normalized.split("/")[0]
        skill_type = fm.get("type")
        is_private = bool(fm.get("private") or fm.get("private_marker"))

        categories[category] = categories.get(category, 0) + 1
        types[skill_type] = types.get(skill_type, 0) + 1
        if is_private:
            private_count += 1

        # Relative Pfade -- KEINE absoluten Systempfade
        rel = "skills/" + fpath_normalized + "/SKILL.md"
        skill_dir = skill_md.parent
        all_files = [f for f in skill_dir.rglob("*") if f.is_file()]

        entry = {
            "path": rel,
            "category": category,
            "directory": skill_md.parent.name,
            "sha256": sha256_file(skill_md).replace("sha256:", ""),
            "size_bytes": skill_md.stat().st_size,
            "line_count": len(skill_md.read_text(encoding="utf-8").splitlines()),
            "frontmatter_present": True,
            "frontmatter_line_count": 0,
            "name": fm.get("name"),
            "version": fm.get("version"),
            "type": skill_type,
            "author": fm.get("author"),
            "created": fm.get("created"),
            "updated": fm.get("updated"),
            "status": fm.get("status"),
            "language": fm.get("language"),
            "standalone": fm.get("standalone"),
            "anthropic_compatible": fm.get("anthropic_compatible") or fm.get("standalone"),
            "bach_compatible": fm.get("bach_compatible"),
            "bach_origin": fm.get("bach_origin", False),
            "provenance_origin": (
                fm.get("provenance", {}).get("origin") if isinstance(fm.get("provenance"), dict) else None
            ) or fm.get("provenance_origin"),
            "provenance_origin_path": (
                fm.get("provenance", {}).get("origin_path") if isinstance(fm.get("provenance"), dict) else None
            ) or fm.get("provenance_origin_path"),
            "has_scripts": any(f.suffix in (".py", ".sh", ".js", ".ts") for f in all_files),
            "has_references": (skill_dir / "references").is_dir(),
            "has_assets": any(f.suffix in (".png", ".jpg", ".svg") for f in all_files),
            "has_tests": (skill_dir / "tests").is_dir(),
            "file_count": len(all_files),
            "missing_required_fields": [],
            "private_marker_hits": ["private: true"] if is_private else [],
            "warnings": [],
        }
        # Frontmatter-Zeilen zaehlen
        text = skill_md.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if m:
            entry["frontmatter_line_count"] = len(m.group(1).splitlines())

        # Fehlende CONVENTIONS-Felder
        for field in ["name", "version", "type", "author", "created", "updated", "description"]:
            if not fm.get(field):
                entry["missing_required_fields"].append(field)

        entries.append(entry)

    report = {
        "summary": {
            # Kein 'root' mit absolutem Pfad -- privatsicheres Format
            "generated_by": "versionctl inventory",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "skill_count": len(skills),
            "private_count": private_count,
            "by_category": dict(sorted(categories.items())),
            "by_type": dict(sorted((k or "None", v) for k, v in types.items())),
        },
        "skills": sorted(entries, key=lambda e: e["path"]),
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False), encoding="utf-8")
    print(f"Inventory geschrieben: {out_path.name}  ({len(skills)} Skills)")
    return 0


def cmd_registry_generate(args) -> int:
    """Produktive Registry aus realem Skill-Bestand erzeugen."""
    skills = find_all_skills(SKILLS_DIR)
    generated_at = datetime.now(timezone.utc).isoformat()

    components = []
    for skill_md, fm in skills:
        entry = _build_registry_entry(skill_md, fm, SKILLS_DIR)
        components.append(entry)

    # Stabil sortieren (nach path), damit zwei Laeufe byte-identisch sind
    components.sort(key=lambda c: c["path"])

    registry_output = {
        "summary": {
            "generated_by": "versionctl registry-generate",
            "generated_at": generated_at,
            "schema_version": "skill-v1",
            "component_count": len(components),
        },
        "components": components,
    }

    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    out_file = REGISTRY_DIR / "components.json"

    # Dry-Run
    if getattr(args, "dry_run", False):
        print(f"[dry-run] Wuerde schreiben: {out_file}  ({len(components)} Eintraege)")
        return 0

    out_file.write_text(
        json.dumps(registry_output, ensure_ascii=False, indent=2, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Registry geschrieben: registry/components.json  ({len(components)} Komponenten)")

    # Companion-Dateien (leer/Platzhalter, fuer Schema-Vollstaendigkeit)
    for fname, key in [
        ("forks.json", "forks"),
        ("branches.json", "branches"),
        ("releases.json", "releases"),
        ("deployments.json", "deployments"),
    ]:
        companion_file = REGISTRY_DIR / fname
        if not companion_file.exists():
            companion_data = {
                "summary": {
                    "generated_by": "versionctl registry-generate",
                    "generated_at": generated_at,
                    "note": f"Wird in Etappe 7+ befuellt.",
                },
                key: [],
            }
            companion_file.write_text(
                json.dumps(companion_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"  Angelegt: registry/{fname}")

    return 0


# ─── CLI ───


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="versionctl",
        description=".SKILLS Versionierungs- und Registry-Verwaltungs-CLI (Etappe 5)",
    )
    sub = parser.add_subparsers(dest="command", metavar="BEFEHL")

    # status
    p_status = sub.add_parser("status", help="Drift zwischen skills/ und Registry zeigen")
    p_status.set_defaults(func=cmd_status)

    # validate
    p_validate = sub.add_parser("validate", help="Skills gegen Schemas + CONVENTIONS pruefen")
    p_validate.add_argument("--verbose", "-v", action="store_true", help="Auch OK-Skills ausgeben")
    p_validate.set_defaults(func=cmd_validate)

    # inventory
    p_inventory = sub.add_parser("inventory", help="Inventory-Report neu erzeugen")
    p_inventory.add_argument("--output", "-o", help="Ausgabedatei (Standard: _reports/inventory-DATUM.json)")
    p_inventory.set_defaults(func=cmd_inventory)

    # registry-generate
    p_regen = sub.add_parser("registry-generate", help="Produktive Registry aus Skill-Bestand erzeugen")
    p_regen.add_argument("--dry-run", action="store_true", help="Nur Vorschau, nichts schreiben")
    p_regen.set_defaults(func=cmd_registry_generate)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
