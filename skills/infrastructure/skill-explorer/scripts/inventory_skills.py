#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inventory_skills.py — erhebt das lokale Skill-Inventar (Fähigkeiten, Abhängigkeiten, Ressourcen).

Deterministisches Fundament für den Audit-Modus. Scannt einen oder mehrere Skill-Roots,
liest pro Skill das SKILL.md/skill.md-Frontmatter (name, description, tags, dependencies,
version, status, category) und erfasst die gebündelten Ressourcen (scripts/ references/ assets/).
Markiert jeden Skill als editierbar (user) oder read-only (plugin/extern).

Survey != Mutation: dieses Skript LIEST nur und schreibt höchstens die JSON-Ausgabe.

Aufruf (Windows: PYTHONIOENCODING=utf-8 setzen):
    PYTHONIOENCODING=utf-8 python inventory_skills.py [--roots DIR[,DIR...]]
        [--include-plugins] [--out inventory.json] [--pretty]

Ohne --roots wird ~/.claude/skills gescannt. Mit --include-plugins werden zusätzlich
Plugin-Cache-Skills (read-only) erfasst, damit sie im Cluster-Survey auftauchen.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Drittanbieter-Skills, die per Policy NICHT in die <skills library> gehören
# (Spiegel von the skill-sync script EXTERNAL_ONLY_SKILLS). Werden als source="external" markiert.
EXTERNAL_ONLY = {
    "playwright-cli", "defuddle", "json-canvas", "obsidian-bases", "obsidian-cli",
    "obsidian-markdown", "context7-cli", "context7-mcp", "find-docs",
    "excalidraw-diagram", "notebooklm",
}
# BACH-interne Skills (Spiegel von the skill-sync script SKIP_SKILLS) — system-gebunden.
BACH_SKILLS = {"bach", "bach-experts", "bach-services", "bach-workflows"}


def find_skill_file(skill_dir: Path) -> Path | None:
    """SKILL.md case-insensitiv finden (manche Skills nutzen skill.md)."""
    for entry in skill_dir.iterdir():
        if entry.is_file() and entry.name.lower() == "skill.md":
            return entry
    return None


def split_frontmatter(text: str) -> tuple[str, str]:
    """Trennt YAML-Frontmatter (zwischen den ersten beiden ---) vom Body."""
    if text.lstrip().startswith("---"):
        # auf das erste --- normalisieren
        start = text.index("---")
        rest = text[start + 3:]
        end = rest.find("\n---")
        if end != -1:
            return rest[:end], rest[end + 4:]
    return "", text


def parse_frontmatter(fm: str) -> dict:
    """Leichter YAML-Parser für die hier genutzten Felder (stdlib, kein PyYAML).

    Unterstützt: einfache key: value, folded scalars (>, |), inline-Listen [a, b],
    Block-Listen (- item) und einen verschachtelten dependencies-Block.
    """
    data: dict = {}
    lines = fm.splitlines()
    i = 0
    n = len(lines)

    def indent(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if indent(raw) != 0 or ":" not in line:
            i += 1
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()

        # Folded/literal scalar: Wert über folgende eingerückte Zeilen sammeln
        if val in (">", "|", ">-", "|-"):
            buf = []
            i += 1
            while i < n and (not lines[i].strip() or indent(lines[i]) >= 2):
                buf.append(lines[i].strip())
                i += 1
            data[key] = " ".join(x for x in buf if x).strip()
            continue

        # Inline-Liste
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
            i += 1
            continue

        # Verschachtelter Block (z. B. dependencies:) ODER Block-Liste
        if val == "":
            # Sub-Block einsammeln
            block = {}
            block_list = []
            i += 1
            while i < n and (not lines[i].strip() or indent(lines[i]) >= 2):
                sub = lines[i]
                if sub.strip().startswith("- "):
                    block_list.append(sub.strip()[2:].strip().strip("'\""))
                elif ":" in sub and indent(sub) >= 2:
                    sk, _, sv = sub.strip().partition(":")
                    sv = sv.strip()
                    if sv.startswith("[") and sv.endswith("]"):
                        block[sk.strip()] = [x.strip().strip("'\"") for x in sv[1:-1].split(",") if x.strip()]
                    elif sv:
                        block[sk.strip()] = sv.strip("'\"")
                    else:
                        block[sk.strip()] = []
                i += 1
            data[key] = block if block else block_list
            continue

        data[key] = val.strip("'\"")
        i += 1
    return data


def body_headings(body: str) -> list[str]:
    """H2-Überschriften als grobe Fähigkeits-Hinweise."""
    return [m.strip() for m in re.findall(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)][:25]


def list_resources(skill_dir: Path) -> dict:
    res = {"scripts": [], "references": [], "assets": []}
    for sub in res:
        d = skill_dir / sub
        if d.is_dir():
            res[sub] = sorted(
                str(p.relative_to(skill_dir)).replace(os.sep, "/")
                for p in d.rglob("*") if p.is_file()
            )
    return res


def classify_source(skill_name: str, root: Path) -> str:
    rp = str(root).lower().replace("\\", "/")
    if "plugins/cache" in rp or "/plugins/" in rp:
        return "plugin"
    if skill_name in EXTERNAL_ONLY:
        return "external"
    if skill_name in BACH_SKILLS:
        return "bach"
    return "user"


def inventory_root(root: Path) -> list[dict]:
    out = []
    if not root.is_dir():
        return out
    for skill_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        sf = find_skill_file(skill_dir)
        if not sf:
            continue
        try:
            text = sf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm_raw, body = split_frontmatter(text)
        fm = parse_frontmatter(fm_raw)
        name = fm.get("name") or skill_dir.name
        source = classify_source(skill_dir.name, root)
        deps = fm.get("dependencies") or {}
        if isinstance(deps, list):
            deps = {"_list": deps}
        res = list_resources(skill_dir)
        out.append({
            "dir": skill_dir.name,
            "name": name,
            "path": str(sf),
            "source": source,
            "editable": source == "user",  # nur user-eigene Skills dürfen mutiert werden
            "version": fm.get("version"),
            "status": fm.get("status"),
            "category": fm.get("category"),
            "tags": fm.get("tags") or [],
            "description": fm.get("description") or "",
            "dependencies": {
                "tools": deps.get("tools", []),
                "services": deps.get("services", []),
                "protocols": deps.get("protocols", []),
                "python": deps.get("python", []),
            },
            "resources": res,
            "has_scripts": bool(res["scripts"]),
            "has_references": bool(res["references"]),
            "has_assets": bool(res["assets"]),
            "headings": body_headings(body),
            "body_words": len(body.split()),
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Skill-Inventar erheben (read-only).")
    ap.add_argument("--roots", default=None,
                    help="Komma-getrennte Skill-Roots. Default: ~/.claude/skills")
    ap.add_argument("--include-plugins", action="store_true",
                    help="Plugin-Cache-Skills (read-only) zusätzlich erfassen.")
    ap.add_argument("--out", default=None, help="JSON-Ausgabedatei (sonst stdout).")
    ap.add_argument("--pretty", action="store_true", help="Eingerücktes JSON.")
    args = ap.parse_args()

    home = Path.home()
    roots: list[Path] = []
    if args.roots:
        roots = [Path(os.path.expanduser(r.strip())) for r in args.roots.split(",") if r.strip()]
    else:
        roots = [home / ".claude" / "skills"]
        if args.include_plugins:
            cache = home / ".claude" / "plugins" / "cache"
            if cache.is_dir():
                # alle skills/-Unterordner der Plugins einsammeln
                for skills_dir in cache.rglob("skills"):
                    if skills_dir.is_dir():
                        roots.append(skills_dir)

    skills = []
    seen = set()
    for root in roots:
        for entry in inventory_root(root):
            key = (entry["dir"], entry["source"])
            if key in seen:
                continue
            seen.add(key)
            skills.append(entry)

    result = {
        "roots": [str(r) for r in roots],
        "count": len(skills),
        "by_source": {s: sum(1 for x in skills if x["source"] == s)
                      for s in sorted({x["source"] for x in skills})},
        "skills": sorted(skills, key=lambda x: (x["source"], x["dir"])),
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
        print(f"[inventory] {len(skills)} Skills → {args.out}")
    else:
        sys.stdout.write(payload + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
