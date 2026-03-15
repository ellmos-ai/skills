#!/usr/bin/env python3
"""Skills Library Catalog -- CLI fuer Verwaltung und Sync-Status."""

import argparse
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"
TEMPLATES_DIR = SKILLS_DIR / "_templates"

# Windows Encoding Fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ─── YAML-Frontmatter Parser (ohne externe Abhaengigkeit) ───


def parse_frontmatter(filepath: Path) -> dict | None:
    """Liest YAML-Frontmatter aus einer SKILL.md Datei.
    Einfacher Parser ohne PyYAML-Abhaengigkeit."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    data = {}
    current_key = None
    current_indent = 0
    nested = {}

    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Einfache key: value Paare
        kv = re.match(r"^(\w[\w.-]*)\s*:\s*(.*)$", line)
        if kv and not line.startswith(" "):
            key, val = kv.group(1), kv.group(2).strip()
            current_key = key
            current_indent = 0
            nested = {}

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

        # Nested key: value (eingerueckt)
        nested_kv = re.match(r"^(\s+)(\w[\w.-]*)\s*:\s*(.*)$", line)
        if nested_kv:
            indent = len(nested_kv.group(1))
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

        # Mehrzeilige Werte (description: >)
        if current_key and isinstance(data.get(current_key), str) and line.startswith("  "):
            data[current_key] += stripped + " "

    # Trailing spaces in descriptions
    for k, v in data.items():
        if isinstance(v, str):
            data[k] = v.strip()

    return data


# ─── Skill Discovery ───


def find_all_skills() -> list[tuple[Path, dict]]:
    """Findet alle SKILL.md Dateien und parst deren Frontmatter."""
    results = []
    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        # Templates und Beispiele ueberspringen
        rel = skill_md.relative_to(SKILLS_DIR)
        parts = rel.parts
        if parts[0].startswith("_"):
            continue

        fm = parse_frontmatter(skill_md)
        if fm:
            fm["_path"] = str(skill_md.parent.relative_to(SKILLS_DIR))
            results.append((skill_md, fm))

    return results


# ─── Befehle ───


def cmd_list(args):
    """Alle Skills auflisten."""
    skills = find_all_skills()
    if not skills:
        print("Keine Skills gefunden.")
        return

    # Filter
    if args.category:
        skills = [(p, fm) for p, fm in skills
                  if fm.get("category", "") == args.category
                  or fm["_path"].startswith(args.category)]
    if args.standalone:
        skills = [(p, fm) for p, fm in skills if fm.get("standalone") is True]
    if args.bach_origin:
        skills = [(p, fm) for p, fm in skills if fm.get("bach_origin") is True]

    print(f"\n{'Name':<30} {'Version':<10} {'Typ':<10} {'SA':<4} {'BACH':<5} {'Kategorie'}")
    print("─" * 85)
    for path, fm in skills:
        name = fm.get("name", "?")
        version = fm.get("version", "?")
        typ = fm.get("type", "?")
        sa = "Y" if fm.get("standalone") else "N"
        bach = "Y" if fm.get("bach_origin") else "N"
        cat = fm.get("category", fm["_path"].split("/")[0] if "/" in fm["_path"] else fm["_path"])
        print(f"  {name:<28} {version:<10} {typ:<10} {sa:<4} {bach:<5} {cat}")

    print(f"\n  {len(skills)} Skill(s) gefunden.")


def cmd_sync_status(args):
    """Sync-Status aller Skills mit Provenance-Info anzeigen."""
    skills = find_all_skills()
    if not skills:
        print("Keine Skills gefunden.")
        return

    print(f"\n{'Name':<25} {'Origin':<10} {'Orig.Ver.':<10} {'Sync von':<12} {'Sync nach':<12} {'Lokal?'}")
    print("─" * 90)

    for path, fm in skills:
        prov = fm.get("provenance", {})
        if not isinstance(prov, dict):
            prov = {}

        name = fm.get("name", "?")
        origin = prov.get("origin", "-")
        orig_ver = prov.get("origin_version", "-") or "-"
        sync_from = prov.get("last_sync_from_origin", "-") or "-"
        sync_to = prov.get("last_sync_to_origin", "-") or "-"
        local = "JA" if prov.get("local_changes_since_sync") else "nein"

        print(f"  {name:<23} {origin:<10} {orig_ver:<10} {sync_from:<12} {sync_to:<12} {local}")

    print()


def cmd_create(args):
    """Neuen Skill aus Template erstellen."""
    name = args.name
    category = args.category or "general"
    skill_type = args.type or "skill"

    skill_dir = SKILLS_DIR / category / name
    if skill_dir.exists():
        print(f"FEHLER: Skill '{name}' existiert bereits in '{category}/'")
        sys.exit(1)

    skill_dir.mkdir(parents=True, exist_ok=True)

    # Template lesen
    template_path = TEMPLATES_DIR / "TEMPLATE_SKILL.md"
    if not template_path.exists():
        print("FEHLER: Template nicht gefunden!")
        sys.exit(1)

    content = template_path.read_text(encoding="utf-8")
    today = date.today().isoformat()

    # Platzhalter ersetzen
    content = content.replace("{{skill-name}}", name)
    content = content.replace("{{Skill-Name}}", name.replace("-", " ").title())
    content = content.replace("{{author}}", "Lukas Geiger")
    content = content.replace("{{YYYY-MM-DD}}", today)
    content = content.replace("{{kategorie}}", category)
    content = re.sub(r"^type: skill$", f"type: {skill_type}", content, count=1, flags=re.MULTILINE)

    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(content, encoding="utf-8")

    print(f"Skill erstellt: {skill_dir.relative_to(SKILLS_DIR.parent)}/SKILL.md")
    print(f"  Name: {name}")
    print(f"  Typ: {skill_type}")
    print(f"  Kategorie: {category}")


def cmd_info(args):
    """Detail-Info zu einem Skill anzeigen."""
    skills = find_all_skills()
    matches = [(p, fm) for p, fm in skills if fm.get("name") == args.name]

    if not matches:
        # Fuzzy-Suche
        matches = [(p, fm) for p, fm in skills if args.name.lower() in fm.get("name", "").lower()]

    if not matches:
        print(f"Skill '{args.name}' nicht gefunden.")
        return

    for path, fm in matches:
        print(f"\n{'='*60}")
        print(f"  Skill: {fm.get('name')}")
        print(f"  Version: {fm.get('version')}")
        print(f"  Typ: {fm.get('type')}")
        print(f"  Autor: {fm.get('author')}")
        print(f"  Erstellt: {fm.get('created')}")
        print(f"  Aktualisiert: {fm.get('updated')}")
        print(f"  Status: {fm.get('status', '-')}")
        print(f"  Pfad: {fm['_path']}")
        print(f"  Standalone: {fm.get('standalone', '-')}")
        print(f"  BACH-kompatibel: {fm.get('bach_compatible', '-')}")
        print(f"  BACH-Ursprung: {fm.get('bach_origin', '-')}")
        print(f"  Anthropic-kompatibel: {fm.get('anthropic_compatible', '-')}")

        prov = fm.get("provenance", {})
        if isinstance(prov, dict) and prov:
            print(f"\n  Provenance:")
            for k, v in prov.items():
                print(f"    {k}: {v}")

        deps = fm.get("dependencies", {})
        if isinstance(deps, dict) and any(deps.values()):
            print(f"\n  Abhaengigkeiten:")
            for k, v in deps.items():
                if v:
                    print(f"    {k}: {v}")

        print(f"{'='*60}")


def cmd_categories(args):
    """Alle Kategorien (Ordner) auflisten."""
    cats = set()
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            cats.add(item.name)

    if not cats:
        print("Keine Kategorien gefunden.")
        return

    print("\nKategorien:")
    for cat in sorted(cats):
        count = len(list((SKILLS_DIR / cat).rglob("SKILL.md")))
        print(f"  {cat:<30} ({count} Skills)")
    print()


def cmd_quality(args):
    """Quality-Scores anzeigen oder S-Tests ausfuehren."""
    import json as json_mod

    results_dir = Path(__file__).parent / "testing" / "results"

    if args.name:
        # Einzelnen Skill
        if args.run:
            os.system(f'PYTHONIOENCODING=utf-8 python testing/skill_tester.py test {args.name} --type static')
            return

        # Letztes Ergebnis anzeigen
        skill_dir = results_dir / args.name
        if skill_dir.exists():
            results = sorted(skill_dir.glob("*.json"), reverse=True)
            if results:
                data = json_mod.loads(results[0].read_text(encoding="utf-8"))
                score = data.get("quality_score", "?")
                rating = data.get("rating", "?")
                date_str = data.get("meta", {}).get("date", "?")[:10]
                print(f"\n  {args.name}: {score}/5 ({rating}) -- {date_str}")

                dims = data.get("dimensions", {})
                if dims:
                    labels = {
                        "d1_clarity": "Klarheit",
                        "d2_completeness": "Vollstaendigkeit",
                        "d3_independence": "Unabhaengigkeit",
                        "d4_effectiveness": "Wirksamkeit",
                        "d5_efficiency": "Effizienz",
                    }
                    for k, v in dims.items():
                        print(f"    {labels.get(k, k)}: {v}/5")
                print()
                return

        print(f"  Keine Testergebnisse fuer '{args.name}'.")
        print(f"  Ausfuehren: python catalog.py quality {args.name} --run")
        return

    # Alle Skills -- letzten Batch laden
    if args.run:
        os.system('PYTHONIOENCODING=utf-8 python testing/skill_tester.py batch')
        return

    batch_files = sorted(results_dir.glob("batch_*.json"), reverse=True)
    if batch_files:
        data = json_mod.loads(batch_files[0].read_text(encoding="utf-8"))
        print(f"\n  Batch vom {data['date'][:10]} ({data['total']} Skills)\n")
        for r in sorted(data["results"], key=lambda x: x["quality"], reverse=True):
            status = "OK" if r["quality"] >= 3 else "!!"
            print(f"  [{status}] {r['skill']:30s} {r['quality']:.1f}/5")
        print(f"\n  Durchschnitt: {data['average']}/5\n")
    else:
        print("  Keine Batch-Ergebnisse vorhanden.")
        print("  Ausfuehren: python catalog.py quality --run")


# ─── Main ───


def main():
    parser = argparse.ArgumentParser(
        description="Skills Library Catalog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Verfuegbare Befehle")

    # list
    p_list = sub.add_parser("list", help="Alle Skills auflisten")
    p_list.add_argument("--category", "-c", help="Nach Kategorie filtern")
    p_list.add_argument("--standalone", "-s", action="store_true", help="Nur standalone Skills")
    p_list.add_argument("--bach-origin", "-b", action="store_true", help="Nur BACH-Ursprungs-Skills")

    # sync-status
    sub.add_parser("sync-status", help="Sync-Status aller Skills anzeigen")

    # create
    p_create = sub.add_parser("create", help="Neuen Skill erstellen")
    p_create.add_argument("name", help="Skill-Name (kebab-case)")
    p_create.add_argument("--category", "-c", default="general", help="Kategorie (Ordner)")
    p_create.add_argument("--type", "-t", default="skill", help="Typ (skill|agent|expert|...)")

    # info
    p_info = sub.add_parser("info", help="Detail-Info zu einem Skill")
    p_info.add_argument("name", help="Skill-Name")

    # categories
    sub.add_parser("categories", help="Alle Kategorien auflisten")

    # quality
    p_quality = sub.add_parser("quality", help="Quality-Score anzeigen")
    p_quality.add_argument("name", nargs="?", help="Skill-Name (ohne = alle)")
    p_quality.add_argument("--run", action="store_true", help="S-Tests ausfuehren")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "sync-status":
        cmd_sync_status(args)
    elif args.command == "create":
        cmd_create(args)
    elif args.command == "info":
        cmd_info(args)
    elif args.command == "categories":
        cmd_categories(args)
    elif args.command == "quality":
        cmd_quality(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
