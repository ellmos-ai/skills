#!/usr/bin/env python3
"""Build a provider-neutral automation self-care plan from a capability profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCHEMA = "automation-self-care.plan.v1"

TASKS = {
    "hygiene": {
        "title": "Automation definition hygiene",
        "functions": ["F1", "bindings", "permissions", "runtime"],
        "required": ["inventory", "run-history"],
        "cadence": "P1D",
        "mutation": "report-first",
    },
    "prompt-quality": {
        "title": "Prompt outcome and text quality",
        "functions": ["F2"],
        "required": ["inventory", "run-history", "update", "readback"],
        "cadence": "P1D",
        "mutation": "one-reversible-change",
    },
    "frequency": {
        "title": "Frequency and activation tuning",
        "functions": ["F3"],
        "required": ["inventory", "run-history", "update", "pause", "readback"],
        "cadence": "P1D",
        "mutation": "one-reversible-change",
    },
    "load": {
        "title": "Scheduler load distribution",
        "functions": ["F4"],
        "required": ["inventory", "update", "readback"],
        "cadence": "P1D",
        "mutation": "one-reversible-change",
    },
    "resources": {
        "title": "Capacity and resource protection",
        "functions": ["F5"],
        "required": ["inventory", "usage-metrics", "update", "pause", "readback"],
        "cadence": "PT6H",
        "mutation": "reversible-throttle",
    },
    "cross-system": {
        "title": "Cross-system automation coordination",
        "functions": ["F6"],
        "required": ["inventory", "run-history"],
        "cadence": "P1D",
        "mutation": "report-first",
    },
    "bindings": {
        "title": "Project and workspace binding integrity",
        "functions": ["bindings"],
        "required": ["inventory", "workspace-bindings", "update", "readback"],
        "cadence": "P1D",
        "mutation": "one-reversible-change",
    },
    "permissions": {
        "title": "Automation permission review",
        "functions": ["permissions"],
        "required": ["inventory", "run-history", "permissions", "update", "readback"],
        "cadence": "P1D",
        "mutation": "one-reversible-change",
    },
    "runtime": {
        "title": "Automation runtime maintenance",
        "functions": ["runtime"],
        "required": ["inventory", "run-history"],
        "cadence": "P1D",
        "mutation": "report-first",
    },
}


def load_profile(path: Path) -> dict:
    """Load and minimally validate a provider capability profile."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "automation-self-care.provider.v1":
        raise ValueError("profile schema must be automation-self-care.provider.v1")
    for field in ("actor_id", "provider", "app_class", "capabilities", "native_surface"):
        if field not in data:
            raise ValueError(f"profile field missing: {field}")
    if not isinstance(data["capabilities"], list):
        raise ValueError("capabilities must be a list")
    return data


def selected_tasks(topology: str) -> list[tuple[str, dict]]:
    """Return task definitions for the requested topology."""
    if topology == "full":
        return list(TASKS.items())
    compact = []
    for key in ("hygiene", "prompt-quality", "resources", "cross-system"):
        compact.append((key, dict(TASKS[key])))
    scheduler = {
        "title": "Frequency, activation and load tuning",
        "functions": ["F3", "F4"],
        "required": sorted(
            set(TASKS["frequency"]["required"] + TASKS["load"]["required"])
        ),
        "cadence": "P1D",
        "mutation": "one-reversible-change",
    }
    compact.insert(2, ("scheduler-tuning", scheduler))
    return compact


def build_plan(profile: dict, topology: str) -> dict:
    """Build task contracts and mark missing capabilities without installing."""
    capabilities = set(profile["capabilities"])
    tasks = []
    for key, definition in selected_tasks(topology):
        missing = sorted(set(definition["required"]) - capabilities)
        tasks.append(
            {
                "task_id": f"automation-care.{key}",
                "title": definition["title"],
                "functions": definition["functions"],
                "cadence": definition["cadence"],
                "mutation_policy": definition["mutation"],
                "required_capabilities": definition["required"],
                "missing_capabilities": missing,
                "readiness": "blocked" if missing else "ready",
                "initial_mode": "read-only",
            }
        )
    return {
        "schema": SCHEMA,
        "actor_id": profile["actor_id"],
        "provider": profile["provider"],
        "app_class": profile["app_class"],
        "topology": topology,
        "native_surface": profile["native_surface"],
        "safeguards": [
            "self-protection",
            "deletion-log",
            "effect-check-and-rollback",
            "one-change-per-run",
            "native-readback",
        ],
        "tasks": tasks,
        "installation_state": "plan-only",
    }


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--topology", choices=("compact", "full"), default="compact")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    plan = build_plan(load_profile(args.profile), args.topology)
    args.out.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    ready = sum(task["readiness"] == "ready" for task in plan["tasks"])
    print(f"wrote {args.out}: {ready}/{len(plan['tasks'])} tasks ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
