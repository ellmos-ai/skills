#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Scheduler Setup & Controller
==================================
Configures and controls the scheduled execution of Community Outreach
across various environments:
  - Antigravity Sidecar / Scheduled Task
  - Windows Task Scheduler (schtasks)
  - Unix Crontab (cron)
  - ellmos-scheduler (daemon loop)
  - Generic CLI execution

License: MIT
Author: ellmos-ai / Antigravity Team
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

TASK_ID = "community-outreach"
WIN_TASK_NAME = "CommunityOutreach-Daily"

def setup_antigravity(gemini_dir: Path, workspace_dir: Path, schedule_cron: str = "0 10 * * *", enabled: bool = True) -> bool:
    """Configures Antigravity sidecar task."""
    sidecar_dir = gemini_dir / "config" / "sidecars" / TASK_ID
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    
    runner_script = workspace_dir / "outreach_runner.py"
    if not runner_script.exists():
        # Fallback to skill script
        runner_script = Path(__file__).parent / "outreach_engine.py"

    sidecar_data = {
        "builtin": "schedule",
        "restartPolicy": "always",
        "displayName": "COMMUNITY OUTREACH",
        "projectId": "25935ede-6ae5-452d-9b29-c70c286a98b4",
        "model": "gemini-2.5-flash",
        "args": [
            schedule_cron,
            "agentapi",
            "new-conversation",
            f"Führe den 4-Phasen-Laufzyklus für Community Outreach aus:\n\npython \"{runner_script}\" --workspace \"{workspace_dir}\" --full-run"
        ]
    }

    sidecar_file = sidecar_dir / "sidecar.json"
    with open(sidecar_file, "w", encoding="utf-8") as f:
        json.dump(sidecar_data, f, indent=2, ensure_ascii=False)

    # Register in config.json
    cfg_file = gemini_dir / "config" / "config.json"
    if cfg_file.exists():
        with open(cfg_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg.setdefault("sidecars", {})
        cfg["sidecars"][TASK_ID] = {
            "enabled": enabled,
            "projectId": "25935ede-6ae5-452d-9b29-c70c286a98b4"
        }
        with open(cfg_file, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)

    print(f"[OK] Antigravity Sidecar '{TASK_ID}' registered (Cron: {schedule_cron}, Enabled: {enabled}).")
    return True

def setup_windows(workspace_dir: Path, time_str: str = "09:00", action: str = "install") -> bool:
    """Configures Windows Task Scheduler."""
    if action == "remove":
        cmd = ["schtasks", "/Delete", "/TN", WIN_TASK_NAME, "/F"]
        rc = subprocess.run(cmd, capture_output=True).returncode
        print(f"[OK] Windows Task '{WIN_TASK_NAME}' removed (RC={rc}).")
        return rc == 0

    python_exe = sys.executable
    script_path = workspace_dir / "outreach_runner.py"
    if not script_path.exists():
        script_path = Path(__file__).parent / "outreach_engine.py"

    tr_cmd = f'"{python_exe}" "{script_path}" --workspace "{workspace_dir}" --full-run'
    cmd = [
        "schtasks", "/Create",
        "/TN", WIN_TASK_NAME,
        "/TR", tr_cmd,
        "/SC", "DAILY",
        "/ST", time_str,
        "/F"
    ]
    rc = subprocess.run(cmd, capture_output=True).returncode
    if rc == 0:
        print(f"[OK] Windows Task '{WIN_TASK_NAME}' registered daily at {time_str}.")
        return True
    else:
        print(f"[FEHLER] Windows Task Scheduler failed with return code {rc}.")
        return False

def setup_unix_cron(workspace_dir: Path, schedule_cron: str = "0 9 * * *") -> bool:
    """Prints or installs Unix crontab entry."""
    python_exe = sys.executable
    script_path = workspace_dir / "outreach_runner.py"
    if not script_path.exists():
        script_path = Path(__file__).parent / "outreach_engine.py"

    cron_line = f"{schedule_cron} {python_exe} {script_path} --workspace {workspace_dir} --full-run > /dev/null 2>&1"
    print("\n=== Unix Crontab Entry ===")
    print(f"Add the following line to your crontab (`crontab -e`):")
    print(f"\n{cron_line}\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Multi-Scheduler Setup for Community Outreach")
    parser.add_argument("--backend", choices=["antigravity", "windows", "unix", "cron"], default="antigravity")
    parser.add_argument("--workspace", default=".", help="Target workspace path")
    parser.add_argument("--schedule", default="0 10 * * *", help="Cron expression or daily time")
    parser.add_argument("--remove", action="store_true", help="Remove scheduled task")

    args = parser.parse_args()
    ws_path = Path(args.workspace).resolve()

    if args.backend == "antigravity":
        gemini_dir = Path.home() / ".gemini"
        setup_antigravity(gemini_dir, ws_path, schedule_cron=args.schedule, enabled=not args.remove)
    elif args.backend == "windows":
        action = "remove" if args.remove else "install"
        time_part = args.schedule if ":" in args.schedule else "09:00"
        setup_windows(ws_path, time_str=time_part, action=action)
    elif args.backend in ["unix", "cron"]:
        setup_unix_cron(ws_path, schedule_cron=args.schedule)

if __name__ == "__main__":
    main()
