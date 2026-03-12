# -*- coding: utf-8 -*-
"""
devSoftAgent Development Loop.

Orchestrates the complete development cycle:
1. Scan projects
2. Select project (weighted random or explicit)
3. Analyze code
4. Load/generate tasks
5. Prioritize and select next task
6. Execute between-task checks
7. Report results

This is the main coordinator -- it delegates to ProjectManager,
TaskEngine, and CodeAnalyzer.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from .config import Config
from .project_manager import ProjectManager, Project
from .task_engine import TaskEngine, Task, TaskStatus, TaskType
from .code_analyzer import CodeAnalyzer, ProjectAnalysis


@dataclass
class SessionResult:
    """Result of a development session."""

    project: str
    project_path: str
    started: str
    completed: str = ""
    tasks_attempted: int = 0
    tasks_completed: int = 0
    tasks_blocked: int = 0
    task_results: List[Dict[str, Any]] = field(default_factory=list)
    analysis_summary: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project": self.project,
            "project_path": self.project_path,
            "started": self.started,
            "completed": self.completed,
            "tasks_attempted": self.tasks_attempted,
            "tasks_completed": self.tasks_completed,
            "tasks_blocked": self.tasks_blocked,
            "task_results": self.task_results,
            "analysis_summary": self.analysis_summary,
        }

    def to_markdown(self) -> str:
        """Format session result as Markdown report."""
        lines = [
            f"# Session Report: {self.project}",
            "",
            f"- **Gestartet:** {self.started}",
            f"- **Abgeschlossen:** {self.completed}",
            f"- **Tasks:** {self.tasks_completed}/{self.tasks_attempted} erledigt",
            f"- **Blockiert:** {self.tasks_blocked}",
            "",
        ]
        for i, tr in enumerate(self.task_results, 1):
            status = tr.get("status", "?")
            desc = tr.get("description", "?")
            task_type = tr.get("type", "?")
            lines.append(f"### Task {i}: [{task_type}] {desc}")
            lines.append(f"Status: {status}")
            if tr.get("changes"):
                for c in tr["changes"]:
                    lines.append(f"  - {c}")
            lines.append("")
        return "\n".join(lines)


class DevLoop:
    """Orchestrates the software development cycle.

    The DevLoop coordinates all components:
    - ProjectManager for project discovery and selection
    - TaskEngine for task parsing and prioritization
    - CodeAnalyzer for code understanding

    Usage:
        loop = DevLoop(config)
        loop.scan_projects()

        # Full session
        result = loop.run_session(max_tasks=10)

        # Step by step
        project = loop.select_project()
        analysis = loop.analyze_project(project)
        tasks = loop.get_tasks(project)
        loop.run_between_checks()
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self.project_manager = ProjectManager(self._config)
        self.task_engine = TaskEngine(self._config)
        self.code_analyzer = CodeAnalyzer()

        self._current_project: Optional[Project] = None

    def scan_projects(
        self, folders: Optional[List[Union[str, Path]]] = None
    ) -> List[Project]:
        """Scan for projects.

        Args:
            folders: Override scan folders

        Returns:
            Discovered projects
        """
        return self.project_manager.scan(folders)

    def select_project(
        self,
        name: Optional[str] = None,
        exclude: Optional[List[str]] = None,
    ) -> Optional[Project]:
        """Select a project (explicit or weighted random).

        Args:
            name: Explicit project name (bypasses random selection)
            exclude: Project names to exclude

        Returns:
            Selected Project or None
        """
        if name:
            project = self.project_manager.get_project(name)
        else:
            project = self.project_manager.select_random(exclude=exclude)

        self._current_project = project
        return project

    def analyze_project(
        self, project: Optional[Project] = None
    ) -> ProjectAnalysis:
        """Analyze project code.

        Args:
            project: Project to analyze (default: current)

        Returns:
            ProjectAnalysis with metrics
        """
        project = project or self._current_project
        if not project:
            raise ValueError("No project selected")
        return self.code_analyzer.analyze(project.path)

    def get_tasks(
        self,
        project: Optional[Project] = None,
        include_scanned: bool = True,
        limit: int = 10,
    ) -> List[Task]:
        """Get prioritized tasks for a project.

        Args:
            project: Target project (default: current)
            include_scanned: Also scan code for TODO/FIXME
            limit: Max tasks to return

        Returns:
            Prioritized task list
        """
        project = project or self._current_project
        if not project:
            raise ValueError("No project selected")

        file_pattern = self._config.get("scan.file_pattern", "AUFGABEN.txt")
        aufgaben_path = project.path / file_pattern
        tasks = self.task_engine.parse_aufgaben(aufgaben_path)

        if include_scanned:
            scanned = self.task_engine.scan_for_tasks(project.path)
            # Deduplicate: skip scanned tasks whose descriptions overlap
            existing = {t.description.lower() for t in tasks}
            for st in scanned:
                if st.description.lower() not in existing:
                    tasks.append(st)

        return self.task_engine.get_open_tasks(tasks, limit=limit)

    def run_between_checks(self) -> List[Dict[str, Any]]:
        """Run between-task checklist.

        Returns:
            List of check items with pending status
        """
        if not self._config.get("between_checks.enabled", True):
            return []

        items = self._config.get("between_checks.items", [])
        return [{"check": item, "status": "pending"} for item in items]

    def check_onboarding(self) -> List[Project]:
        """Find projects needing onboarding.

        Returns:
            Projects without AUFGABEN.txt
        """
        return self.project_manager.needs_onboarding()

    def create_onboarding_tasks(self, project: Project) -> List[Task]:
        """Generate onboarding tasks for a new project.

        Args:
            project: Project to onboard

        Returns:
            Generated onboarding tasks
        """
        onboarding_texts: List[str] = self._config.get("onboarding.tasks", [])
        tasks = []
        for text in onboarding_texts:
            tasks.append(Task(
                description=text,
                task_type=_guess_task_type(text),
                status=TaskStatus.OPEN,
                priority=90,  # high priority for onboarding
                source="onboarding",
            ))
        return tasks

    def run_session(
        self,
        project_name: Optional[str] = None,
        max_tasks: int = 10,
        task_handler: Optional[
            Callable[[Task, ProjectAnalysis], Dict[str, Any]]
        ] = None,
    ) -> SessionResult:
        """Run a complete development session.

        This is the main entry point for automated dev loops.
        If no task_handler is provided, tasks are listed but not executed.

        Args:
            project_name: Explicit project (or random selection)
            max_tasks: Maximum tasks per session
            task_handler: Callback(task, analysis) -> result dict

        Returns:
            SessionResult with details
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Select project
        project = self.select_project(name=project_name)
        if not project:
            return SessionResult(
                project="NONE", project_path="", started=now, completed=now,
            )

        result = SessionResult(
            project=project.name,
            project_path=str(project.path),
            started=now,
        )

        # Analyze
        analysis = self.analyze_project(project)
        result.analysis_summary = analysis.to_dict()

        # Get tasks
        tasks = self.get_tasks(project, limit=max_tasks)
        result.tasks_attempted = len(tasks)

        # Execute tasks (if handler provided)
        if task_handler:
            for task in tasks:
                try:
                    task_result = task_handler(task, analysis)
                    task.status = TaskStatus.DONE
                    result.tasks_completed += 1
                except Exception as exc:
                    task_result = {"error": str(exc)}
                    task.status = TaskStatus.BLOCKED
                    result.tasks_blocked += 1

                task_result["description"] = task.description
                task_result["type"] = task.task_type.value
                task_result["status"] = task.status.value
                result.task_results.append(task_result)

                # Between-task checks
                self.run_between_checks()
        else:
            # No handler: just list task info
            for task in tasks:
                result.task_results.append(task.to_dict())

        result.completed = datetime.now().strftime("%Y-%m-%d %H:%M")
        return result

    def get_status(self) -> Dict[str, Any]:
        """Get DevLoop status."""
        pm_status = self.project_manager.get_status()
        return {
            "agent": "devSoftAgent",
            "version": self._config.get("version", "0.1.0"),
            "current_project": (
                self._current_project.name if self._current_project else None
            ),
            "projects": pm_status,
            "session_config": {
                "max_tasks": self._config.get(
                    "session.max_tasks_per_session", 10
                ),
                "interval_min": self._config.get(
                    "session.interval_minutes", 30
                ),
            },
        }

    def save_session(
        self,
        result: SessionResult,
        output_dir: Optional[Path] = None,
    ) -> Path:
        """Save session result to file.

        Args:
            result: Session result to save
            output_dir: Output directory (default: module/output/)

        Returns:
            Path to saved file
        """
        if output_dir is None:
            output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"session_{ts}_{result.project}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        return filepath


def _guess_task_type(text: str) -> TaskType:
    """Guess task type from description text."""
    text_lower = text.lower()
    if "analyse" in text_lower or "analysis" in text_lower:
        return TaskType.REFACTOR
    if "qualitaet" in text_lower or "quality" in text_lower:
        return TaskType.TEST
    if "aufgaben" in text_lower or "doku" in text_lower:
        return TaskType.DOKU
    return TaskType.FEATURE
