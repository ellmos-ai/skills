#!/usr/bin/env python3
"""
ANTIGRAVITY KONTEXT AND WORKFLOW LOADER AND DIVIDER
===================================================
Orchestrierungs- und Optimierungsskript für Antigravity Scheduled Tasks / Sidecars.

Aufgaben:
1. Pflege & tägliche Aktualisierung der zentralen STICHWORTLISTE (.SYNC/STICHWORTLISTE.json).
2. Inspektion von Automations-Logs und AUTOMATIONS-MEMORY.md zur Fehlerdiagnose.
3. Durchsetzung des 3-Zeilen-Prompt-Standards ([TITEL], ZWECK, AUFGABE) gemäß TASK_PROMPT_STRUCTURE_POLICY.md.
4. Einbettung von Preflight Bootloadern & Letter Hooks (z. B. Ordner-Navigations-Regel, Memory-Check).
5. 4-Stufen-Modellallokation und lokale Synchronisation über .gemini/config/sidecars und .gemini/antigravity/sidecar_data.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
HOOKS_DIR = SKILL_DIR / "hooks"
CONFIG_JSON = SKILL_DIR / "config.json"
HOME_DIR = Path.home()

DEFAULT_PATHS = {
    "sync_dir": HOME_DIR / "OneDrive" / ".SYNC",
    "sidecars_dir": HOME_DIR / ".gemini" / "config" / "sidecars",
    "mirror_sidecars_dir": HOME_DIR / ".gemini" / "antigravity" / "sidecar_data",
    "skills_root": HOME_DIR / "OneDrive" / ".TOPICS" / ".AI" / ".SKILLS" / "skills",
    "automation_policy_path": HOME_DIR / ".gemini" / "AUTOMATION_POLICY.md",
    "automations_memory_path": HOME_DIR / ".gemini" / "AUTOMATIONS-MEMORY.md",
    "antigravity_log_path": HOME_DIR / ".gemini" / "antigravity" / "ANTIGRAVITY-LOG.txt",
    "antigravity_registry_path": HOME_DIR / ".gemini" / "antigravity" / "ANTIGRAVITY-REGISTRY.md",
}

DEFAULT_SKILL_MAPPINGS = {
    "routing": "infrastructure/semantic-persona-routing/SKILL.md",
    "condition": "infrastructure/condition/SKILL.md",
    "orchestrator": "infrastructure/orchestrator/SKILL.md",
    "agents_bridge": "infrastructure/agents-bridge/SKILL.md",
    "think": "utilities/think/SKILL.md",
    "decide": "utilities/decide/SKILL.md",
    "pipeline_optimizer": "dev/pipeline-optimizer/SKILL.md",
}

def _read_user_config() -> dict:
    if not CONFIG_JSON.exists():
        return {}
    try:
        data = json.loads(CONFIG_JSON.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {CONFIG_JSON}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{CONFIG_JSON} must contain a JSON object")
    return data

def _configured_path(config: dict, key: str, default: Path) -> Path:
    value = config.get(key)
    if value is None:
        return default
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Configuration key {key!r} must be a non-empty path string")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = CONFIG_JSON.parent / path
    return path

def _load_runtime_settings():
    config = _read_user_config()
    paths = {
        key: _configured_path(config, key, default)
        for key, default in DEFAULT_PATHS.items()
    }
    host_slot = os.environ.get("LETTER_HOOKER_HOST_SLOT") or config.get("host_slot") or "default"
    if not isinstance(host_slot, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", host_slot):
        raise ValueError("host_slot must be a safe path segment; set LETTER_HOOKER_HOST_SLOT or config.json")

    configured_mappings = config.get("skill_mappings", {})
    if not isinstance(configured_mappings, dict):
        raise ValueError("Configuration key 'skill_mappings' must be a JSON object")
    mapping_values = dict(DEFAULT_SKILL_MAPPINGS)
    for name, value in configured_mappings.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every skill_mappings key must be a non-empty string")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Skill mapping {name!r} must be a non-empty path string")
        mapping_values[name] = value
    return config, paths, host_slot, mapping_values

CONFIG_ERROR = None
try:
    USER_CONFIG, _PATHS, HOST_SLOT, _SKILL_MAPPING_VALUES = _load_runtime_settings()
except (OSError, ValueError, TypeError) as exc:
    USER_CONFIG = {}
    _PATHS = dict(DEFAULT_PATHS)
    HOST_SLOT = "default"
    _SKILL_MAPPING_VALUES = dict(DEFAULT_SKILL_MAPPINGS)
    CONFIG_ERROR = str(exc)

SYNC_DIR = _PATHS["sync_dir"]
SIDECARS_DIR = _PATHS["sidecars_dir"]
MIRROR_SIDECARS_DIR = _PATHS["mirror_sidecars_dir"]
SKILLS_ROOT = _PATHS["skills_root"]
AUTOMATION_POLICY_PATH = _PATHS["automation_policy_path"]
AUTOMATIONS_MEMORY_PATH = _PATHS["automations_memory_path"]
ANTIGRAVITY_LOG_PATH = _PATHS["antigravity_log_path"]
ANTIGRAVITY_REGISTRY_PATH = _PATHS["antigravity_registry_path"]
STICHWORTLISTE_PATH = SYNC_DIR / "STICHWORTLISTE.json"

def _mapping_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else SKILLS_ROOT / path

SKILL_MAPPINGS = {
    name: _mapping_path(value)
    for name, value in _SKILL_MAPPING_VALUES.items()
}

def _file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def build_or_update_stichwortliste(write: bool = True) -> dict:
    """Extrahiert Stichwörter aus allen Sidecar-Prompts und aktualisiert STICHWORTLISTE.json."""
    keywords = set()
    task_catalog = {}

    if not SIDECARS_DIR.exists():
        return {}

    for folder in SIDECARS_DIR.iterdir():
        if not folder.is_dir():
            continue
        sidecar_file = folder / "sidecar.json"
        if not sidecar_file.exists():
            continue
        try:
            data = json.loads(sidecar_file.read_text(encoding="utf-8"))
            display_name = data.get("displayName", folder.name)
            args = data.get("args", [])
            prompt = args[3] if len(args) > 3 and isinstance(args[3], str) else ""

            # Extract uppercase terms & domain keywords
            found_terms = set(re.findall(r"\b[A-Z0-9_\-]{3,}\b", prompt))
            found_words = set(re.findall(r"\b[a-zA-ZaeoeueAeOeUess]{5,}\b", prompt.lower()))

            keywords.update(found_terms)
            task_catalog[folder.name] = {
                "displayName": display_name,
                "keywords": sorted(list(found_terms | found_words)[:20]),
                "last_inspected": datetime.now(timezone.utc).isoformat(),
            }
        except Exception:
            continue

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_tasks": len(task_catalog),
        "global_keywords": sorted(list(keywords)),
        "tasks": task_catalog,
    }

    if write:
        try:
            STICHWORTLISTE_PATH.parent.mkdir(parents=True, exist_ok=True)
            STICHWORTLISTE_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[WARN] STICHWORTLISTE Schreibfehler: {e}", file=sys.stderr)

    return payload


def format_letter_hooks_footer() -> str:
    """Build a portable footer from bundled hooks and configured local files."""
    lines = ["--- GOVERNANCE, WORKFLOW & HOOKS ---"]

    if AUTOMATION_POLICY_PATH.is_file():
        lines.append(f"1. OPTIONAL LOCAL POLICY: {_file_uri(AUTOMATION_POLICY_PATH)}")
    else:
        lines.append(
            f"1. OPTIONAL LOCAL POLICY: Read {AUTOMATION_POLICY_PATH} if present; "
            "the path is configurable in config.json."
        )

    hook_files = [
        ("BOOTLOADER (document traversal)", "bootloader_doc_traversal.md"),
        ("PREFLIGHT (Gardener and memory)", "preflight_gardener_query.md"),
        ("WORKFLOW (locks and Git hygiene)", "workflow_lock_and_git_hygiene.md"),
        ("PATHS (validation and authority)", "path_validation_and_authority.md"),
    ]
    line_number = 2
    for label, filename in hook_files:
        path = HOOKS_DIR / filename
        if path.is_file():
            lines.append(f"{line_number}. {label}: {_file_uri(path)}")
            line_number += 1

    lines.append(
        f"{line_number}. AUTOMATION MEMORY AND LOGGING: Record important actions and "
        f"verification in {AUTOMATIONS_MEMORY_PATH}, {ANTIGRAVITY_LOG_PATH}, and "
        f"{ANTIGRAVITY_REGISTRY_PATH}. Keep run logs out of agent rule files."
    )
    lines.append(
        f"Host slot: {HOST_SLOT}. Current-slot handoffs belong under "
        f"{SYNC_DIR / HOST_SLOT}; do not write to another host's slot."
    )

    relevant_skills = [
        f"{name}: {_file_uri(path)}"
        for name, path in SKILL_MAPPINGS.items()
        if path.is_file()
    ]
    if relevant_skills:
        lines.append("RELEVANT SKILLS: " + "; ".join(relevant_skills))
    return "\n".join(lines)


def format_prompt_standard(task_name: str, prompt: str) -> str:
    """Stellt sicher, dass der Prompt die Letter Hooks und Gate-Vorgaben einhält."""
    footer = format_letter_hooks_footer()

    # Strip any existing governance or added hook footers to avoid duplicate blocks
    if "--- GOVERNANCE, WORKFLOW & HOOKS ---" in prompt:
        base_prompt = prompt[:prompt.index("--- GOVERNANCE, WORKFLOW & HOOKS ---")].rstrip()
    elif "--- --- HINZUGEFUEGTE WORKFLOW GUIDANCE" in prompt:
        base_prompt = prompt[:prompt.index("--- --- HINZUGEFUEGTE WORKFLOW GUIDANCE")].rstrip()
    else:
        base_prompt = prompt.rstrip()

    return f"{base_prompt}\n\n{footer}"


def inspect_and_enhance_sidecars(dry_run: bool = False) -> int:
    """Inspeziert Sidecars und stellt 3-Zeilen-Prompt-Standard & Pfad-Hygiene sicher (nur aktive Sidecars)."""
    if not SIDECARS_DIR.exists():
        return 0

    enhanced_count = 0

    for folder in SIDECARS_DIR.iterdir():
        if not folder.is_dir():
            continue
        # Strikter Reaktivierungs-Gate-Schutz gemäß Reaktivierungs-Policy 2026-08-15: .DISABLED NIEMALS anfassen!
        if folder.name.endswith(".DISABLED"):
            continue

        sidecar_file = folder / "sidecar.json"
        if not sidecar_file.exists():
            continue

        try:
            data = json.loads(sidecar_file.read_text(encoding="utf-8"))
            args = data.get("args", [])
            if len(args) <= 3 or not isinstance(args[3], str):
                continue

            prompt = args[3]
            formatted_prompt = format_prompt_standard(folder.name, prompt)

            if formatted_prompt != prompt:
                if not dry_run:
                    args[3] = formatted_prompt
                    data["args"] = args
                    if "prompt" in data:
                        data["prompt"] = formatted_prompt

                    # 1. Live file
                    sidecar_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

                    # 2. Mirror file
                    mirror_file = MIRROR_SIDECARS_DIR / folder.name / "sidecar.json"
                    if mirror_file.parent.exists():
                        try:
                            mirror_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                        except Exception:
                            pass

                enhanced_count += 1
            else:
                # Mirror sync check
                if not dry_run:
                    mirror_file = MIRROR_SIDECARS_DIR / folder.name / "sidecar.json"
                    if mirror_file.parent.exists():
                        try:
                            mirror_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                        except Exception:
                            pass
                enhanced_count += 1
        except Exception as e:
            print(f"[WARN] Fehler bei Sidecar {folder.name}: {e}", file=sys.stderr)

    return enhanced_count


def main() -> int:
    if CONFIG_ERROR is not None:
        print(f"[ERROR] Invalid letter-hooker config: {CONFIG_ERROR}", file=sys.stderr)
        return 2
    dry_run = "--check" in sys.argv or "--dry-run" in sys.argv
    print(f"[{datetime.now().isoformat()}] Starte ANTIGRAVITY KONTEXT AND WORKFLOW LOADER AND DIVIDER...")

    stichwort_data = build_or_update_stichwortliste(write=not dry_run)
    action = "geprüft" if dry_run else "aktualisiert"
    print(f"[OK] STICHWORTLISTE {action} ({stichwort_data.get('total_tasks', 0)} Tasks).")

    enhanced = inspect_and_enhance_sidecars(dry_run=dry_run)
    print(f"[OK] {enhanced} aktive Sidecar(s) mit Prompt-Standard & Letter Hooks gepflegt.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
