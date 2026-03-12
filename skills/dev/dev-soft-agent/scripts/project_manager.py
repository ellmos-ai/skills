# -*- coding: utf-8 -*-
"""
devSoftAgent Project Manager.

Scans directories for software projects, classifies them by naming
convention, and provides weighted random selection for work prioritization.

Naming Convention (Extended Lifecycle v3.0):
    REL-PUB_*  Released public         (weight: 0.0  -- published on GitHub)
    REL-PRI_*  Released private        (weight: 0.0  -- private GitHub repo)
    REL_*      Released               (weight: 0.0  -- released, no suffix)
    GO-PUB_*   Go public              (weight: 0.2  -- approved, preparing push)
    GO-PRI_*   Go private             (weight: 0.2  -- approved, preparing push)
    PreGit_*   Pre-Git preparation    (weight: 0.4  -- Pflichtdateien, cleanup)
    RDY-PRI_*  Ready private          (weight: 0.8  -- ready, private target)
    RDY_FAST_* Ready + fast-track     (weight: 0.5)
    RDY_*      Ready for development  (weight: 1.0  -- highest priority)
    FAST_*     Fast-track active      (weight: 0.33 -- already progressing)
    DEV_*      In development         (weight: 0.17 -- early stage)
    ARC_*      Archived               (weight: 0.0  -- no development)
    USR_*      Personal use           (weight: 0.0  -- not for publication)

Projects can reside in the root OR in theme folders:
    ASSISTENT, BIO, CASH, CODING, DATA, DOCS,
    ENTERTAINMENT, GAMES, LLM, MAIL, RESEARCH
"""

import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .config import Config


@dataclass
class Project:
    """Represents a software project."""

    name: str
    path: Path
    prefix: str
    label: str
    weight: float
    has_aufgaben: bool = False
    has_readme: bool = False
    task_count_open: int = 0
    task_count_done: int = 0
    tags: List[str] = field(default_factory=list)
    theme: str = ""
    store_ready: bool = False

    @property
    def clean_name(self) -> str:
        """Project name without prefix (e.g., 'AboTracker' from 'FAST_AboTracker')."""
        if self.prefix:
            rest = self.name[len(self.prefix):]
            return rest.lstrip("_")
        return self.name

    @property
    def relative_path(self) -> str:
        """Theme-relative path (e.g., 'CODING/REL-PUB_WinStorePackager')."""
        if self.theme:
            return f"{self.theme}/{self.name}"
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict."""
        return {
            "name": self.name,
            "path": str(self.path),
            "prefix": self.prefix,
            "label": self.label,
            "weight": self.weight,
            "clean_name": self.clean_name,
            "theme": self.theme,
            "relative_path": self.relative_path,
            "has_aufgaben": self.has_aufgaben,
            "has_readme": self.has_readme,
            "task_count_open": self.task_count_open,
            "task_count_done": self.task_count_done,
            "tags": self.tags,
            "store_ready": self.store_ready,
        }


class ProjectManager:
    """Manages software project discovery and selection.

    Scans configured directories for projects, classifies them
    by naming convention prefix, and provides weighted random
    selection for prioritized task assignment.

    Usage:
        pm = ProjectManager(config)
        projects = pm.scan()
        chosen = pm.select_random()
        status = pm.get_status()
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._projects: List[Project] = []
        self._prefix_map: Dict[str, Dict[str, Any]] = self._config.get(
            "naming.prefixes", {}
        )

    @property
    def projects(self) -> List[Project]:
        """Currently known projects (after scan)."""
        return list(self._projects)

    def scan(self, folders: Optional[List[Union[str, Path]]] = None) -> List[Project]:
        """Scan directories for projects.

        Scans both root-level projects and projects inside theme folders
        (ASSISTENT, BIO, CASH, CODING, DATA, DOCS, ENTERTAINMENT,
        GAMES, LLM, MAIL, RESEARCH).

        Args:
            folders: Override scan folders (default: from config)

        Returns:
            List of discovered Project objects
        """
        scan_folders = folders or self._config.get("scan.folders", [])
        theme_folders = set(self._config.get("naming.theme_folders", []))
        skip_dirs = {"_LANG", "_STORE", "_TEMPLATES", "_USER", "_archiv",
                      "__pycache__", ".git", "node_modules", ".venv", "releases"}
        self._projects = []

        for folder in scan_folders:
            folder = Path(folder)
            if not folder.exists():
                continue
            for entry in sorted(folder.iterdir()):
                if not entry.is_dir() or entry.name.startswith("."):
                    continue
                if entry.name in skip_dirs:
                    continue

                if entry.name in theme_folders:
                    # Scan inside theme folder
                    for sub in sorted(entry.iterdir()):
                        if sub.is_dir() and not sub.name.startswith((".", "_")):
                            project = self._classify_project(sub, theme=entry.name)
                            if project.prefix:
                                self._projects.append(project)
                else:
                    # Root-level project
                    project = self._classify_project(entry)
                    if project.prefix:  # Only include recognized projects
                        self._projects.append(project)

        return list(self._projects)

    def select_random(
        self, exclude: Optional[List[str]] = None
    ) -> Optional[Project]:
        """Select a random project using weighted selection.

        Projects with weight 0.0 (REL) are excluded automatically.

        Args:
            exclude: Project names to exclude from selection

        Returns:
            Selected Project or None if no candidates available
        """
        exclude_set = set(exclude or [])
        candidates = [
            p for p in self._projects
            if p.weight > 0 and p.name not in exclude_set
        ]

        if not candidates:
            return None

        weights = [p.weight for p in candidates]
        return random.choices(candidates, weights=weights, k=1)[0]

    def get_project(self, name: str) -> Optional[Project]:
        """Get a project by exact name."""
        for p in self._projects:
            if p.name == name:
                return p
        return None

    def get_projects_by_prefix(self, prefix: str) -> List[Project]:
        """Get all projects with a given prefix."""
        return [p for p in self._projects if p.prefix == prefix]

    def get_status(self) -> Dict[str, Any]:
        """Return scan status summary."""
        prefix_counts: Dict[str, int] = {}
        for p in self._projects:
            key = p.prefix or "NONE"
            prefix_counts[key] = prefix_counts.get(key, 0) + 1

        total_open = sum(p.task_count_open for p in self._projects)
        total_done = sum(p.task_count_done for p in self._projects)

        theme_counts: Dict[str, int] = {}
        for p in self._projects:
            key = p.theme or "ROOT"
            theme_counts[key] = theme_counts.get(key, 0) + 1

        return {
            "total_projects": len(self._projects),
            "by_prefix": prefix_counts,
            "by_theme": theme_counts,
            "with_aufgaben": sum(1 for p in self._projects if p.has_aufgaben),
            "with_readme": sum(1 for p in self._projects if p.has_readme),
            "store_ready": sum(1 for p in self._projects if p.store_ready),
            "total_tasks_open": total_open,
            "total_tasks_done": total_done,
            "scan_folders": [str(f) for f in (self._config.get("scan.folders") or [])],
        }

    def needs_onboarding(self) -> List[Project]:
        """Find projects that need onboarding (no AUFGABEN.txt)."""
        if not self._config.get("onboarding.enabled", True):
            return []
        return [p for p in self._projects if not p.has_aufgaben and p.weight > 0]

    # --- Internal ---

    def _classify_project(self, path: Path, theme: str = "") -> Project:
        """Classify a project directory by its naming convention prefix."""
        name = path.name
        prefix, label, weight = self._parse_prefix(name)

        file_pattern = self._config.get("scan.file_pattern", "AUFGABEN.txt")
        aufgaben_file = path / file_pattern
        readme_file = path / "README.md"

        task_open, task_done = 0, 0
        if aufgaben_file.exists():
            task_open, task_done = self._count_tasks(aufgaben_file)

        tags = self._extract_tags(name)
        store_ready = self._check_store_ready(path)

        return Project(
            name=name,
            path=path,
            prefix=prefix,
            label=label,
            weight=weight,
            has_aufgaben=aufgaben_file.exists(),
            has_readme=readme_file.exists(),
            task_count_open=task_open,
            task_count_done=task_done,
            tags=tags,
            theme=theme,
            store_ready=store_ready,
        )

    def _parse_prefix(self, name: str) -> Tuple[str, str, float]:
        """Extract prefix, label, and weight from project name.

        Handles compound prefixes like RDY_FAST_ and hyphenated
        prefixes like REL-PUB_ by checking longest match first.
        """
        sep = self._config.get("naming.separator", "_")
        default_weight = self._config.get("naming.default_weight", 0.5)

        # Sort prefixes by length descending (longest match first)
        sorted_prefixes = sorted(self._prefix_map.keys(), key=len, reverse=True)

        for prefix in sorted_prefixes:
            pattern = prefix + sep
            if name.startswith(pattern):
                info = self._prefix_map[prefix]
                return (
                    prefix,
                    info.get("label", prefix),
                    info.get("weight", default_weight),
                )

        return "", "Unclassified", default_weight

    @staticmethod
    def _check_store_ready(path: Path) -> bool:
        """Check if a project has all files needed for Windows Store submission."""
        required = [
            "store_package.json",
            "STORE_LISTING.md",
            "THIRD_PARTY_LICENSES.txt",
        ]
        icon_ok = any(path.glob("*.ico")) or (path / "store_assets").is_dir()
        screenshot_ok = (path / "README" / "screenshots" / "main.png").exists()
        files_ok = all((path / f).exists() for f in required)
        return files_ok and icon_ok and screenshot_ok

    def _count_tasks(self, aufgaben_path: Path) -> Tuple[int, int]:
        """Count open and done tasks in AUFGABEN.txt."""
        try:
            text = aufgaben_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return 0, 0

        open_count = len(re.findall(r"^- \[ \]", text, re.MULTILINE))
        done_count = len(re.findall(r"^- \[x\]", text, re.MULTILINE))
        return open_count, done_count

    @staticmethod
    def _extract_tags(name: str) -> List[str]:
        """Extract tags from project name (e.g., SOCIAL, CASHCOW, SUITE)."""
        known_tags = ["SOCIAL", "CASHCOW", "SUITE"]
        name_upper = name.upper()
        return [tag for tag in known_tags if f"_{tag}" in name_upper]
