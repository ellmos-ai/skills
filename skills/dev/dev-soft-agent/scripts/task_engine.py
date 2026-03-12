# -*- coding: utf-8 -*-
"""
devSoftAgent Task Engine.

Parses AUFGABEN.txt files, generates tasks from code scanning,
and manages task prioritization and lifecycle.

Task Format (AUFGABEN.txt):
    ## OFFEN
    - [ ] [BUG] Description
    - [ ] [FEATURE] Description

    ## IN ARBEIT
    - [-] [BUG] Description

    ## ERLEDIGT
    - [x] [BUG] Description -- DONE 2026-02-21
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .config import Config


class TaskStatus(Enum):
    """Task lifecycle status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class TaskType(Enum):
    """Task category (ordered by default priority)."""
    BUG = "BUG"
    FEATURE = "FEATURE"
    REFACTOR = "REFACTOR"
    TEST = "TEST"
    DOKU = "DOKU"
    OTHER = "OTHER"


@dataclass
class Task:
    """Represents a development task."""

    description: str
    task_type: TaskType = TaskType.OTHER
    status: TaskStatus = TaskStatus.OPEN
    priority: int = 50
    source: str = ""  # "aufgaben", "scanner", "onboarding", "generated"
    line_number: int = 0
    completed_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_aufgaben_line(self) -> str:
        """Format as AUFGABEN.txt line."""
        if self.status == TaskStatus.DONE:
            check = "x"
            suffix = f" -- DONE {self.completed_at or datetime.now().strftime('%Y-%m-%d')}"
        elif self.status == TaskStatus.IN_PROGRESS:
            check = "-"
            suffix = ""
        else:
            check = " "
            suffix = ""
        return f"- [{check}] [{self.task_type.value}] {self.description}{suffix}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict."""
        return {
            "description": self.description,
            "type": self.task_type.value,
            "status": self.status.value,
            "priority": self.priority,
            "source": self.source,
        }


class TaskEngine:
    """Parses, generates, and prioritizes development tasks.

    Core responsibilities:
    - Parse AUFGABEN.txt into structured Task objects
    - Generate new tasks from code scanning (TODOs, FIXMEs)
    - Prioritize tasks by type and weight
    - Write updated task lists back to AUFGABEN.txt

    Usage:
        engine = TaskEngine(config)
        tasks = engine.parse_aufgaben(Path("AUFGABEN.txt"))
        scanned = engine.scan_for_tasks(Path("src/"))
        prioritized = engine.prioritize(tasks + scanned)
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._priority_map: Dict[str, int] = self._config.get(
            "task_priorities",
            {"BUG": 100, "FEATURE": 80, "REFACTOR": 60, "TEST": 40, "DOKU": 20},
        )

    def parse_aufgaben(self, path: Path) -> List[Task]:
        """Parse AUFGABEN.txt into Task objects.

        Args:
            path: Path to AUFGABEN.txt file

        Returns:
            List of parsed Task objects
        """
        if not path.exists():
            return []

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return []

        tasks: List[Task] = []
        current_section = ""

        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()

            # Section headers
            if stripped.startswith("## "):
                section = stripped[3:].strip().upper()
                if "OFFEN" in section:
                    current_section = "open"
                elif "ARBEIT" in section:
                    current_section = "in_progress"
                elif "ERLEDIGT" in section:
                    current_section = "done"
                elif "BLOCK" in section:
                    current_section = "blocked"
                continue

            # Task lines
            task = self._parse_task_line(stripped, current_section, i)
            if task:
                tasks.append(task)

        return tasks

    def scan_for_tasks(self, project_path: Path) -> List[Task]:
        """Scan source files for TODO/FIXME markers.

        Args:
            project_path: Root directory of the project

        Returns:
            List of generated Task objects from code comments
        """
        ignored: Set[str] = set(
            self._config.get("scan.ignored_dirs", [])
        )
        tasks: List[Task] = []
        seen: Set[str] = set()

        for ext in ("*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c", "*.h"):
            for filepath in project_path.rglob(ext):
                # Skip ignored directories
                if any(part in ignored for part in filepath.parts):
                    continue

                try:
                    text = filepath.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue

                for i, line in enumerate(text.splitlines(), 1):
                    for marker in ("# TODO:", "# FIXME:", "// TODO:", "// FIXME:"):
                        if marker not in line:
                            continue

                        desc = line.split(marker, 1)[1].strip()
                        if not desc:
                            continue

                        # Deduplicate by description
                        dedup_key = desc.lower()
                        if dedup_key in seen:
                            continue
                        seen.add(dedup_key)

                        task_type = (
                            TaskType.BUG if "FIXME" in marker else TaskType.REFACTOR
                        )
                        tasks.append(Task(
                            description=f"{desc} ({filepath.name}:{i})",
                            task_type=task_type,
                            status=TaskStatus.OPEN,
                            priority=self._priority_map.get(task_type.value, 50),
                            source="scanner",
                            line_number=i,
                        ))
                        break  # one match per line is enough

        return tasks

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (highest first).

        Priority order: BUG > FEATURE > REFACTOR > TEST > DOKU
        Within same priority: original order preserved (stable sort).

        Args:
            tasks: List of tasks to prioritize

        Returns:
            New sorted list (original unchanged)
        """
        for task in tasks:
            if task.priority == 50:  # still default, update from config
                configured = self._priority_map.get(task.task_type.value)
                if configured is not None:
                    task.priority = configured

        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def get_open_tasks(self, tasks: List[Task], limit: int = 10) -> List[Task]:
        """Get prioritized open tasks.

        Args:
            tasks: All tasks
            limit: Maximum number to return

        Returns:
            Prioritized list of open tasks
        """
        open_tasks = [t for t in tasks if t.status == TaskStatus.OPEN]
        prioritized = self.prioritize(open_tasks)
        return prioritized[:limit]

    def write_aufgaben(
        self, path: Path, tasks: List[Task], project_name: str = ""
    ) -> None:
        """Write tasks back to AUFGABEN.txt format.

        Args:
            path: Output path
            tasks: Tasks to write
            project_name: Project name for header
        """
        now = datetime.now().strftime("%Y-%m-%d")

        open_tasks = [t for t in tasks if t.status == TaskStatus.OPEN]
        wip_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        done_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        blocked = [t for t in tasks if t.status == TaskStatus.BLOCKED]

        lines = [
            f"# AUFGABEN - {project_name}",
            f"# Stand: {now}",
            "",
            "## OFFEN",
        ]
        for t in self.prioritize(open_tasks):
            lines.append(t.to_aufgaben_line())

        lines.extend(["", "## IN ARBEIT"])
        for t in wip_tasks:
            lines.append(t.to_aufgaben_line())

        if blocked:
            lines.extend(["", "## BLOCKIERT"])
            for t in blocked:
                lines.append(t.to_aufgaben_line())

        lines.extend(["", "## ERLEDIGT"])
        for t in done_tasks:
            lines.append(t.to_aufgaben_line())

        lines.append("")  # trailing newline
        path.write_text("\n".join(lines), encoding="utf-8")

    # --- Internal ---

    def _parse_task_line(
        self, line: str, section: str, line_number: int
    ) -> Optional[Task]:
        """Parse a single task line from AUFGABEN.txt."""
        # Matches: - [ ] [TYPE] description
        #          - [x] [TYPE] description -- DONE 2026-02-21
        #          - [-] [TYPE] description
        match = re.match(
            r"^- \[([x \-])\]\s*(?:\[(\w+)\]\s*)?(.+?)(?:\s*--\s*(.+))?$",
            line,
        )
        if not match:
            return None

        check, type_tag, description, suffix = match.groups()

        # Determine status
        if section == "done" or check == "x":
            status = TaskStatus.DONE
        elif section == "in_progress" or check == "-":
            status = TaskStatus.IN_PROGRESS
        elif section == "blocked":
            status = TaskStatus.BLOCKED
        else:
            status = TaskStatus.OPEN

        # Determine type
        task_type = TaskType.OTHER
        if type_tag:
            try:
                task_type = TaskType(type_tag.upper())
            except ValueError:
                pass

        priority = self._priority_map.get(task_type.value, 50)

        completed_at = None
        if suffix and "DONE" in suffix:
            # Try to extract date from "DONE 2026-02-21"
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", suffix)
            if date_match:
                completed_at = date_match.group(1)

        return Task(
            description=description.strip(),
            task_type=task_type,
            status=status,
            priority=priority,
            source="aufgaben",
            line_number=line_number,
            completed_at=completed_at,
        )
