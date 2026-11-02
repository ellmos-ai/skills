"""One installable skill identity, with explicitly linked documentation locales.

The extension is a repository contract, not an Agent Skills standard or a promise
that a third-party directory consumes it. Only tracked, public flat variants are
eligible; marker stubs and ambiguous locale directories are never advertised.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

LOCALES = ("de", "en", "es", "zh", "ja", "ru", "fr", "hi", "ar", "bn", "pt")
LOCALE_NAMES = set(LOCALES) | {"zn", "cn", "english", "deutsch", "chinese"}


def document_title(text: str) -> str:
    """Read the first real H1, excluding frontmatter, comments and code fences."""
    text = re.sub(r"\A\ufeff?---\s*\n.*?\n---[^\n]*\n", "", text, count=1, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None and line.startswith("# "):
            title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line[2:])
            title = title.strip().rstrip("#").strip().replace("`", "")
            return title
    return ""


def meaningful_title(title: str) -> bool:
    return bool(title.strip()) and title.strip().casefold() not in LOCALE_NAMES


def skill_localizations(
    canonical_path: Path, source_files: set[str], root: Path
) -> tuple[list[dict], list[str]]:
    """Resolve a family from public-source authority; no filesystem glob fallback."""
    from build_public_registry import read_frontmatter

    canonical = read_frontmatter(canonical_path)
    identity = canonical.get("name")
    results, issues = [], []
    primary = canonical.get("language")
    for code in LOCALES:
        path = canonical_path if code == primary else canonical_path.with_name(f"SKILL.{code}.md")
        relative = path.relative_to(root).as_posix()
        if relative not in source_files:
            continue
        if path.is_symlink():
            issues.append(f"{relative}: symlink locale artifacts are not advertised")
            continue
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
        # A legacy duplicate cannot stand in for an absent flat translation.
        metadata = read_frontmatter(path)
        title = document_title(path.read_text(encoding="utf-8"))
        reason = None
        if not isinstance(identity, str) or identity.casefold() in LOCALE_NAMES:
            reason = "canonical skill identity is missing or is only a language label"
        elif metadata.get("name") != identity:
            reason = "translation name must equal the canonical skill identity"
        elif metadata.get("language") != code:
            reason = "language declaration does not match the locale"
        elif not metadata.get("description", "").strip():
            reason = "missing localized description (marker stubs are not translations)"
        elif not meaningful_title(title):
            reason = "missing meaningful localized H1 title"
        if reason:
            issues.append(f"{relative}: {reason}")
            continue
        results.append({
            "language": code,
            "path": relative,
            "title": title,
            "description": metadata["description"],
        })
    return results, issues


def legacy_locale_paths(files: list[str]) -> list[str]:
    return sorted(p for p in files if len(PurePosixPath(p).parts) == 5
                  and PurePosixPath(p).parts[1] != "third-party"
                  and not PurePosixPath(p).parts[1].startswith("_")
                  and PurePosixPath(p).parts[-2].lower() in LOCALES
                  and PurePosixPath(p).name == "SKILL.md")


def retirement_plan(root: Path, files: list[str]) -> list[tuple[Path, Path]]:
    """Keep every legacy byte; retire only known public locale entry points."""
    plan = []
    for relative in legacy_locale_paths(files):
        old = root / relative
        flat = old.parent.parent / f"SKILL.{old.parent.name.lower()}.md"
        new = old.with_name("README.md")
        if flat.relative_to(root).as_posix() not in files or not flat.is_file():
            raise ValueError(f"No canonical flat counterpart: {relative}")
        if new.exists():
            raise ValueError(f"Preservation destination already exists: {new}")
        if old.is_symlink() or new.parent.is_symlink() or flat.is_symlink():
            raise ValueError(f"Refusing symlink in migration: {relative}")
        old.resolve(strict=True).relative_to(root.resolve(strict=True))
        plan.append((old, new))
    return plan


def schema_graph(registry: dict, base_url: str) -> dict:
    """Schema.org relationships for consumers that opt into them (not hreflang)."""
    from urllib.parse import quote

    base = base_url.rstrip("/") + "/"
    graph = []
    for component in registry["components"]:
        family_url = base + quote(component["path"], safe="/")
        variants = component.get("localizations", [])
        for variant in variants:
            url = base + quote(variant["path"], safe="/")
            node = {
                "@id": url, "@type": "CreativeWork", "url": url,
                "identifier": component["id"], "name": variant["title"],
                "inLanguage": variant["language"], "description": variant["description"],
            }
            if url != family_url:
                node["translationOfWork"] = {"@id": family_url}
            else:
                node["workTranslation"] = [
                    {"@id": base + quote(v["path"], safe="/")}
                    for v in variants if v["path"] != component["path"]
                ]
            graph.append(node)
    return {"@context": "https://schema.org", "@graph": graph}


def main() -> int:
    from build_public_registry import build_registry, resolve_source_files

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retire-legacy", action="store_true", help="Rename legacy SKILL.md to README.md, preserving bytes")
    parser.add_argument("--apply", action="store_true", help="Apply the explicit retirement plan (default: dry run)")
    parser.add_argument("--jsonld", action="store_true", help="Write Schema.org graph to stdout")
    parser.add_argument("--base-url", default="https://github.com/ellmos-ai/skills/blob/master/")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    files, _ = resolve_source_files(repository_root=root)
    if args.retire_legacy:
        plan = retirement_plan(root, files)
        for old, new in plan:
            print(f"{old.relative_to(root).as_posix()} -> {new.relative_to(root).as_posix()}")
        if args.apply:
            for old, new in plan:
                old.rename(new)
        print(f"{'Retired' if args.apply else 'Would retire'} {len(plan)} legacy entry points; content retained.")
        return 0
    registry = build_registry(files, repository_root=root)
    if args.jsonld:
        print(json.dumps(schema_graph(registry, args.base_url), ensure_ascii=False, indent=2))
        return 0
    issues = []
    for component in registry["components"]:
        _, findings = skill_localizations(root / component["path"], set(files), root)
        issues.extend(findings)
    baseline_path = root / "testing" / "localization_omissions.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if baseline.get("reason") != "Pre-existing incomplete locale metadata; not advertised as localizations":
        raise ValueError("Missing explicit omission-baseline rationale")
    new_issues = sorted(set(issues) - set(baseline["issues"]))
    stale_baseline = sorted(set(baseline["issues"]) - set(issues))
    print(json.dumps({"families": len(registry["components"]),
                      "legacy_entry_points": legacy_locale_paths(files),
                      "unadvertised_variants": issues,
                      "new_issues": new_issues,
                      "stale_baseline": stale_baseline}, ensure_ascii=False, indent=2))
    return 1 if legacy_locale_paths(files) or new_issues or stale_baseline else 0


if __name__ == "__main__":
    raise SystemExit(main())
