#!/usr/bin/env python3
"""Build a provider-neutral automation self-care plan from a capability profile."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SCHEMA = "automation-self-care.plan.v1"
PROFILE_SCHEMA = "automation-self-care.provider.v1"
TITLE_SEPARATOR = " — "
MAX_APP_DISPLAY_NAME_LENGTH = 48

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


def normalize_visible_text(value: str) -> str:
    """Collapse whitespace without changing user-visible letter case."""
    return " ".join(value.split())


def validate_app_display_name(value: object) -> list[str]:
    """Validate a non-sensitive app label used only for visible task titles."""
    errors = []
    if not isinstance(value, str):
        return ["app_display_name must be a string"]
    normalized = normalize_visible_text(value)
    if not normalized:
        errors.append("app_display_name must not be empty")
    if len(normalized) > MAX_APP_DISPLAY_NAME_LENGTH:
        errors.append(
            f"app_display_name must be at most {MAX_APP_DISPLAY_NAME_LENGTH} characters"
        )
    if TITLE_SEPARATOR.strip() in normalized:
        errors.append("app_display_name must not contain the title separator")
    if any(ord(character) < 32 for character in value):
        errors.append("app_display_name must not contain control characters")
    return errors


def resolve_app_display_name(profile: dict) -> tuple[str, list[str]]:
    """Return an explicit display name or a backwards-compatible provider label."""
    explicit = profile.get("app_display_name")
    if explicit is not None:
        errors = validate_app_display_name(explicit)
        if errors:
            raise ValueError("; ".join(errors))
        return normalize_visible_text(explicit), []

    # v1 profiles predate app_display_name. Keep them usable while making the
    # migration visible in the plan; new profiles should always set the field.
    provider = normalize_visible_text(str(profile.get("provider", ""))).upper()
    errors = validate_app_display_name(provider)
    if errors:
        raise ValueError("cannot derive app_display_name: " + "; ".join(errors))
    return provider, [
        "legacy profile: app_display_name derived from provider; add it explicitly"
    ]


def validate_profile(data: dict, *, strict_display_name: bool = False) -> list[str]:
    """Validate the provider-neutral fields needed to build a safe plan."""
    errors = []
    if data.get("schema") != PROFILE_SCHEMA:
        errors.append(f"profile schema must be {PROFILE_SCHEMA}")
    for field in ("actor_id", "provider", "app_class", "capabilities", "native_surface"):
        if field not in data:
            errors.append(f"profile field missing: {field}")
    if "capabilities" in data and not isinstance(data["capabilities"], list):
        errors.append("capabilities must be a list")
    if strict_display_name and "app_display_name" not in data:
        errors.append("profile field missing: app_display_name")
    if "app_display_name" in data:
        errors.extend(validate_app_display_name(data["app_display_name"]))
    recovery_floor = data.get("recovery_floor", {})
    if recovery_floor and not isinstance(recovery_floor, dict):
        errors.append("recovery_floor must be an object")
    elif recovery_floor:
        minimum = recovery_floor.get("minimum_core_runs_per_day")
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 1:
            errors.append("recovery_floor.minimum_core_runs_per_day must be >= 1")
    return errors


def load_profile(path: Path, *, strict_display_name: bool = False) -> dict:
    """Load and validate a provider capability profile."""
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_profile(data, strict_display_name=strict_display_name)
    if errors:
        raise ValueError("; ".join(errors))
    return data


def format_visible_title(app_display_name: str, care_title: str) -> str:
    """Format a visible title without changing the stable task identity."""
    return f"{app_display_name}{TITLE_SEPARATOR}{normalize_visible_text(care_title)}"


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
    profile_errors = validate_profile(profile)
    if profile_errors:
        raise ValueError("; ".join(profile_errors))
    app_display_name, profile_warnings = resolve_app_display_name(profile)
    recovery_floor = profile.get("recovery_floor") or {
        "minimum_core_runs_per_day": 1
    }
    minimum_runs = recovery_floor["minimum_core_runs_per_day"]
    capabilities = set(profile["capabilities"])
    tasks = []
    for key, definition in selected_tasks(topology):
        missing = sorted(set(definition["required"]) - capabilities)
        care_title = definition["title"]
        tasks.append(
            {
                "task_id": f"automation-care.{key}",
                "semantic_role": key,
                "care_title": care_title,
                "title": format_visible_title(app_display_name, care_title),
                "legacy_titles": [care_title],
                "functions": definition["functions"],
                "cadence": definition["cadence"],
                "mutation_policy": definition["mutation"],
                "required_capabilities": definition["required"],
                "missing_capabilities": missing,
                "readiness": "blocked" if missing else "ready",
                "initial_mode": "read-only",
                "self_protection": {
                    "protected_core": True,
                    "minimum_runs_per_day": minimum_runs,
                    "pause_requires": [
                        "explicit-user-decision",
                        "security-gate",
                        "evidenced-emergency",
                    ],
                },
            }
        )
    plan = {
        "schema": SCHEMA,
        "actor_id": profile["actor_id"],
        "provider": profile["provider"],
        "app_class": profile["app_class"],
        "app_display_name": app_display_name,
        "topology": topology,
        "native_surface": profile["native_surface"],
        "title_policy": {
            "format": "<APP_DISPLAY_NAME> — <CARE_TITLE>",
            "prefix": app_display_name,
            "separator": TITLE_SEPARATOR.strip(),
        },
        "identity_and_reconciliation": {
            "stable_machine_id_field": "task_id",
            "title_is_identity": False,
            "match_order": [
                "task_id",
                "provider_native_id",
                "semantic_role",
                "legacy_unprefixed_title",
            ],
            "on_match": "update-title-in-place",
            "on_ambiguous_match": "blocked",
            "on_missing": "propose-create",
            "duplicate_policy": "never-create-when-semantic-match-exists",
        },
        "recovery_floor": recovery_floor,
        "profile_warnings": profile_warnings,
        "safeguards": [
            "self-protection",
            "recovery-floor",
            "app-prefixed-visible-title",
            "stable-machine-identity",
            "semantic-deduplication",
            "deletion-log",
            "effect-check-and-rollback",
            "one-change-per-run",
            "native-readback",
        ],
        "tasks": tasks,
        "installation_state": "plan-only",
    }
    plan_errors = validate_plan(plan)
    if plan_errors:
        raise ValueError("generated plan is invalid: " + "; ".join(plan_errors))
    return plan


def validate_plan(plan: dict) -> list[str]:
    """Lint a generated plan, including title and identity invariants."""
    errors = []
    if plan.get("schema") != SCHEMA:
        errors.append(f"plan schema must be {SCHEMA}")
    app_display_name = plan.get("app_display_name")
    errors.extend(validate_app_display_name(app_display_name))
    if not isinstance(app_display_name, str):
        return errors
    app_display_name = normalize_visible_text(app_display_name)

    title_policy = plan.get("title_policy", {})
    if title_policy.get("format") != "<APP_DISPLAY_NAME> — <CARE_TITLE>":
        errors.append("title_policy.format is invalid")
    if title_policy.get("prefix") != app_display_name:
        errors.append("title_policy.prefix does not match app_display_name")

    identity = plan.get("identity_and_reconciliation", {})
    if identity.get("stable_machine_id_field") != "task_id":
        errors.append("stable machine identity must remain task_id")
    if identity.get("title_is_identity") is not False:
        errors.append("visible title must not be used as machine identity")
    if identity.get("duplicate_policy") != "never-create-when-semantic-match-exists":
        errors.append("semantic duplicate protection is missing")
    if identity.get("match_order") != [
        "task_id",
        "provider_native_id",
        "semantic_role",
        "legacy_unprefixed_title",
    ]:
        errors.append("semantic match order is invalid")
    if identity.get("on_match") != "update-title-in-place":
        errors.append("semantic matches must be updated in place")
    if identity.get("on_ambiguous_match") != "blocked":
        errors.append("ambiguous semantic matches must block")

    recovery_floor = plan.get("recovery_floor", {})
    minimum_runs = recovery_floor.get("minimum_core_runs_per_day")
    if not isinstance(minimum_runs, int) or isinstance(minimum_runs, bool) or minimum_runs < 1:
        errors.append("recovery floor must require at least one core run per day")

    task_ids = set()
    semantic_roles = set()
    titles = set()
    tasks = plan.get("tasks")
    if not isinstance(tasks, list):
        return errors + ["tasks must be a list"]
    for index, task in enumerate(tasks):
        task_label = f"tasks[{index}]"
        task_id = task.get("task_id")
        semantic_role = task.get("semantic_role")
        care_title = task.get("care_title")
        title = task.get("title")
        if not isinstance(task_id, str) or not re.fullmatch(
            r"automation-care\.[a-z0-9-]+", task_id
        ):
            errors.append(f"{task_label}.task_id is invalid")
        elif task_id in task_ids:
            errors.append(f"duplicate task_id: {task_id}")
        task_ids.add(task_id)
        if not semantic_role or semantic_role in semantic_roles:
            errors.append(f"{task_label}.semantic_role is missing or duplicated")
        semantic_roles.add(semantic_role)
        if isinstance(task_id, str) and task_id != f"automation-care.{semantic_role}":
            errors.append(f"{task_label}.task_id does not match semantic_role")
        if not isinstance(care_title, str) or not care_title.strip():
            errors.append(f"{task_label}.care_title is missing")
        else:
            expected_title = format_visible_title(app_display_name, care_title)
            if title != expected_title:
                errors.append(
                    f"{task_label}.title must use <APP_DISPLAY_NAME> — <CARE_TITLE>"
                )
        if title in titles:
            errors.append(f"duplicate visible title: {title}")
        titles.add(title)
        protection = task.get("self_protection", {})
        if protection.get("protected_core") is not True:
            errors.append(f"{task_label} is not protected as core")
        if protection.get("minimum_runs_per_day") != minimum_runs:
            errors.append(f"{task_label} can drift below the recovery floor")
    return errors


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, nargs="?")
    parser.add_argument("--topology", choices=("compact", "full"), default="compact")
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--strict-profile",
        action="store_true",
        help="Require an explicit app_display_name instead of migrating a legacy profile",
    )
    parser.add_argument(
        "--lint-plan",
        type=Path,
        help="Validate an existing plan without generating or installing anything",
    )
    args = parser.parse_args()

    if args.lint_plan:
        if args.profile or args.out:
            parser.error("--lint-plan cannot be combined with profile or --out")
        plan = json.loads(args.lint_plan.read_text(encoding="utf-8"))
        errors = validate_plan(plan)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print(f"valid plan: {args.lint_plan}")
        return 0

    if args.profile is None or args.out is None:
        parser.error("profile and --out are required when generating a plan")
    plan = build_plan(
        load_profile(args.profile, strict_display_name=args.strict_profile),
        args.topology,
    )
    args.out.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    ready = sum(task["readiness"] == "ready" for task in plan["tasks"])
    print(f"wrote {args.out}: {ready}/{len(plan['tasks'])} tasks ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
