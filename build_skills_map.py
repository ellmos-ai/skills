#!/usr/bin/env python3
"""Render SKILLS-MAP.md from the minimal public registry."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = REPOSITORY_ROOT / "registry" / "components.json"
OUTPUT_PATH = REPOSITORY_ROOT / "SKILLS-MAP.md"


def render() -> str:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    components = registry["components"]
    grouped: dict[str, list[dict]] = defaultdict(list)
    for component in components:
        grouped[component["category"]].append(component)

    lines = [
        "# SKILLS-MAP.md — öffentlicher Skill-Katalog",
        "",
        "> Automatisch aus `registry/components.json` erzeugt. Diese Karte enthält",
        "> ausschließlich veröffentlichte, Ellmos-eigene Skills. Persönliche Profile,",
        "> private Workflows, interne Bewertungen und Drittanbieter-Skills stehen nur",
        "> im getrennten No-Push-Repository.",
        "",
        "## Kategorien und Skills",
        "",
        "```text",
        "skills/",
    ]

    categories = sorted(grouped)
    for category_index, category in enumerate(categories):
        category_components = sorted(grouped[category], key=lambda item: item["name"])
        category_last = category_index == len(categories) - 1
        category_branch = "└──" if category_last else "├──"
        lines.append(f"{category_branch} {category}/ ({len(category_components)})")
        child_prefix = "    " if category_last else "│   "
        for item_index, component in enumerate(category_components):
            item_last = item_index == len(category_components) - 1
            item_branch = "└──" if item_last else "├──"
            description = component["description"] or "Details stehen in der SKILL.md."
            lines.append(
                f"{child_prefix}{item_branch} {component['name']} — {description}"
            )

    lines.extend(
        [
            "```",
            "",
            f"**Gesamt: {len(components)} öffentliche Skills in {len(categories)} Kategorien.**",
            "",
            "## Veröffentlichungsgrenze",
            "",
            "- Öffentliche Skills sind nutzerneutral und stammen von Ellmos AI.",
            "- Persönliche Profile und hostgebundene Workflows bleiben privat.",
            "- Übernommene Drittanbieter-Skills werden nicht im öffentlichen Katalog",
            "  geführt; private Vendorbestände behalten Herkunft und Lizenz.",
            "- Die vollständige interne Registry und die private Skill-Karte liegen",
            "  ausschließlich im lokalen No-Push-Repository.",
            "",
            "Neu erzeugen:",
            "",
            "```bash",
            "python build_public_registry.py",
            "python build_skills_map.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()

    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != expected:
            print(f"Skill map is stale: {OUTPUT_PATH}")
            return 1
        print(f"Skill map is current: {OUTPUT_PATH}")
        return 0

    OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
