#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community Outreach Workspace Bootstrapper
=========================================
Initializes a clean, provider-agnostic workspace for Community Outreach:
  - Generates USECASES.md & usecases.json from repository definitions
  - Creates POST-EINGANG.md (Human-in-the-Loop approval queue)
  - Creates POST-AUSGANG.md (live tracking)
  - Creates POSTVERZEICHNIS.md (global duplicate prevention)
  - Creates ACCOUNTVERZEICHNIS.md (account and SSO guidelines)
  - Copies or links outreach_runner.py

License: MIT
Author: ellmos-ai / Antigravity Team
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

def bootstrap_workspace(target_dir: Path, repo_list: list[dict] = None):
    target_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = target_dir / "_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    if not repo_list:
        repo_list = [
            {
                "name": "example-tool",
                "org": "example-org",
                "url": "https://github.com/example-org/example-tool",
                "description": "Beispiel-Werkzeug zur Demonstration.",
                "usecases": ["Automatisierung", "Code-Analyse"],
                "solved_problems": ["Manuelle repetitive Aufgaben", "Fehlende Code-Transparenz"],
                "last_promoted": None
            }
        ]

    # 1. usecases.json
    usecases_json_path = target_dir / "usecases.json"
    if not usecases_json_path.exists():
        data = {
            "meta": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "version": "1.0.0",
                "total_repos": len(repo_list)
            },
            "platform_rotation": ["Reddit", "YouTube", "Dev.to / Foren"],
            "last_platform": "",
            "repositories": repo_list
        }
        with open(usecases_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] {usecases_json_path.name} erstellt ({len(repo_list)} Repositories).")

    # 2. USECASES.md
    usecases_md_path = target_dir / "USECASES.md"
    if not usecases_md_path.exists():
        md = "# 📋 Repository Usecase- & Problemlösungs-Katalog\n\n"
        md += "| Repository | Organisation | Beschreibung | Ziel-Usecases | Gelöste Probleme |\n"
        md += "| :--- | :--- | :--- | :--- | :--- |\n"
        for r in repo_list:
            u_str = ", ".join(r.get("usecases", []))
            p_str = ", ".join(r.get("solved_problems", []))
            md += f"| [{r['name']}]({r.get('url', '#')}) | `{r.get('org', '')}` | {r.get('description', '')} | {u_str} | {p_str} |\n"
        usecases_md_path.write_text(md, encoding="utf-8")
        print(f"[OK] {usecases_md_path.name} erstellt.")

    # 3. POST-EINGANG.md
    inbox_path = target_dir / "POST-EINGANG.md"
    if not inbox_path.exists():
        inbox_content = """# 📥 POST-EINGANG -- Genehmigungs-Queue (Human-in-the-Loop)

> ⚠️ **EU AI Act & Transparenz-Garantie:**
> Jeder Beitrag verbleibt im Entwurfsstatus, bis er durch dich manuell autorisiert wurde.
> Setze das Häkchen von `- [ ] Genehmigt` auf `- [x] Genehmigt`, um einen Beitrag freizugeben.

---
"""
        inbox_path.write_text(inbox_content, encoding="utf-8")
        print(f"[OK] {inbox_path.name} erstellt.")

    # 4. POST-AUSGANG.md
    outbox_path = target_dir / "POST-AUSGANG.md"
    if not outbox_path.exists():
        outbox_content = """# 📤 POST-AUSGANG -- Veröffentlichte Beiträge & Feedback-Monitoring

> Dieser Bereich dokumentiert alle veröffentlichten Beiträge zur Überwachung von Reaktionen und Diskussionen.

---
"""
        outbox_path.write_text(outbox_content, encoding="utf-8")
        print(f"[OK] {outbox_path.name} erstellt.")

    # 5. POSTVERZEICHNIS.md
    reg_path = target_dir / "POSTVERZEICHNIS.md"
    if not reg_path.exists():
        reg_content = """# 📑 POSTVERZEICHNIS -- Globaler Duplikatschutz

> Jede bespielte URL / Thread-ID wird hier irreversibel protokolliert.

| Zeitstempel | Plattform | Repository | Ziel-URL |
| :--- | :--- | :--- | :--- |
"""
        reg_path.write_text(reg_content, encoding="utf-8")
        print(f"[OK] {reg_path.name} erstellt.")

    # 6. ACCOUNTVERZEICHNIS.md
    acc_path = target_dir / "ACCOUNTVERZEICHNIS.md"
    if not acc_path.exists():
        acc_content = """# 👤 ACCOUNTVERZEICHNIS & SSO-RICHTLINIEN

Dokumentation autorisierter Plattform-Accounts und Browser-Profile:
- **Reddit:** SSO via Default Browser Profil
- **YouTube / Google:** SSO via Default Browser Profil
- **Foren / Dev.to:** SSO via Default Browser Profil

Regeln:
1. Keine Klartext-Passwörter in Dateien speichern.
2. Ausschließlich autorisierte Konten nutzen.
"""
        acc_path.write_text(acc_content, encoding="utf-8")
        print(f"[OK] {acc_path.name} erstellt.")

    print(f"\n[SUCCESS] Community Outreach Workspace unter '{target_dir}' vollständig initialisiert!")

def main():
    parser = argparse.ArgumentParser(description="Initialize Community Outreach Workspace")
    parser.add_argument("--target-dir", default="./community_outreach", help="Target directory to create")
    parser.add_argument("--repo-list", help="Path to JSON file containing list of repositories")

    args = parser.parse_args()
    target_path = Path(args.target_dir).resolve()

    repos = None
    if args.repo_list and Path(args.repo_list).exists():
        with open(args.repo_list, "r", encoding="utf-8") as f:
            repos = json.load(f)

    bootstrap_workspace(target_path, repo_list=repos)

if __name__ == "__main__":
    main()
