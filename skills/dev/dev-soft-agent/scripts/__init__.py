# -*- coding: utf-8 -*-
"""
devSoftAgent -- Software Development Pipeline.

Standalone software development agent extracted from BACH's ATI system.
Manages project discovery, task prioritization, code analysis,
and orchestrated development loops.

Usage:
    from devSoftAgent import DevLoop, Config

    loop = DevLoop()
    loop.scan_projects()
    project = loop.select_project()
    tasks = loop.get_tasks(project)

Author: Lukas Geiger
License: MIT
"""

from .code_analyzer import CodeAnalyzer, ProjectAnalysis
from .config import Config
from .dev_loop import DevLoop, SessionResult
from .project_manager import Project, ProjectManager
from .task_engine import Task, TaskEngine, TaskStatus, TaskType

__version__ = "0.1.0"
__all__ = [
    "DevLoop",
    "SessionResult",
    "Config",
    "ProjectManager",
    "Project",
    "TaskEngine",
    "Task",
    "TaskStatus",
    "TaskType",
    "CodeAnalyzer",
    "ProjectAnalysis",
]
