# -*- coding: utf-8 -*-
"""CLI entry point for devSoftAgent.

Usage:
    python -m devSoftAgent scan /path/to/projects
    python -m devSoftAgent select
    python -m devSoftAgent analyze /path/to/project
    python -m devSoftAgent tasks /path/to/project
    python -m devSoftAgent session --project NAME
    python -m devSoftAgent status
"""

import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace"
    )


def main() -> None:
    import argparse
    from pathlib import Path
    from .dev_loop import DevLoop
    from .config import Config

    parser = argparse.ArgumentParser(
        description="devSoftAgent -- Software Development Pipeline"
    )
    parser.add_argument(
        "--config", help="Pfad zur config.json", default=None
    )
    sub = parser.add_subparsers(dest="command")

    # scan
    sp_scan = sub.add_parser("scan", help="Projekte scannen")
    sp_scan.add_argument("folders", nargs="*", help="Verzeichnisse")

    # select
    sp_select = sub.add_parser("select", help="Projekt auswaehlen (gewichtet)")
    sp_select.add_argument("--name", help="Expliziter Projektname")

    # analyze
    sp_analyze = sub.add_parser("analyze", help="Projekt analysieren")
    sp_analyze.add_argument("path", help="Projektpfad")

    # tasks
    sp_tasks = sub.add_parser("tasks", help="Tasks anzeigen")
    sp_tasks.add_argument("project_path", help="Projektpfad")
    sp_tasks.add_argument("-n", "--limit", type=int, default=10)

    # status
    sub.add_parser("status", help="Agent-Status")

    # session
    sp_session = sub.add_parser("session", help="Dev-Session (dry-run)")
    sp_session.add_argument("--project", help="Expliziter Projektname")
    sp_session.add_argument("-n", "--max-tasks", type=int, default=10)
    sp_session.add_argument(
        "--save", action="store_true", help="Ergebnis speichern"
    )

    args = parser.parse_args()

    config = (
        Config.from_json(args.config) if args.config else Config()
    )
    loop = DevLoop(config)

    if args.command == "scan":
        folders = args.folders or config.get("scan.folders", [])
        if not folders:
            print("Keine Verzeichnisse angegeben. Nutze --config oder Argumente.")
            sys.exit(1)
        projects = loop.scan_projects(folders)
        print(f"Gefunden: {len(projects)} Projekte\n")
        for p in projects:
            marker = "+" if p.has_aufgaben else "-"
            print(
                f"  [{marker}] {p.name:40s}  {p.prefix or '-':10s}"
                f"  w={p.weight:.2f}  tasks={p.task_count_open}"
            )

    elif args.command == "select":
        if not args.name:
            loop.scan_projects()
        project = loop.select_project(name=args.name)
        if project:
            print(f"Gewaehlt: {project.name}")
            print(f"Pfad:     {project.path}")
            print(f"Prefix:   {project.prefix} ({project.label})")
            print(f"Gewicht:  {project.weight}")
        else:
            print("Kein Projekt gefunden.")

    elif args.command == "analyze":
        analysis = loop.code_analyzer.analyze(Path(args.path))
        print(analysis.to_markdown())

    elif args.command == "tasks":
        from .project_manager import Project

        project = Project(
            name=Path(args.project_path).name,
            path=Path(args.project_path),
            prefix="",
            label="Manual",
            weight=1.0,
        )
        loop._current_project = project
        tasks = loop.get_tasks(project, limit=args.limit)
        if tasks:
            print(f"Top {len(tasks)} Tasks:\n")
            for i, t in enumerate(tasks, 1):
                print(
                    f"  {i}. [{t.task_type.value:8s}] "
                    f"(P{t.priority:3d}) {t.description}"
                )
        else:
            print("Keine offenen Tasks gefunden.")

    elif args.command == "status":
        status = loop.get_status()
        print(f"devSoftAgent v{status['version']}")
        print(f"Projekte: {status['projects']['total_projects']}")
        print(
            f"Session-Config: max {status['session_config']['max_tasks']} tasks, "
            f"alle {status['session_config']['interval_min']} min"
        )

    elif args.command == "session":
        loop.scan_projects()
        result = loop.run_session(
            project_name=args.project, max_tasks=args.max_tasks
        )
        print(result.to_markdown())
        if args.save:
            path = loop.save_session(result)
            print(f"\nGespeichert: {path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
