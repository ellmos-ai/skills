# -*- coding: utf-8 -*-
"""
devSoftAgent Configuration Management.

Manages settings for the software development agent:
- Project scanning paths and patterns
- Session configuration (intervals, quiet hours)
- Naming convention definitions
- Task priorities and weights

Config can be loaded from JSON or passed as dict.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Sensible defaults -- override via JSON or dict
DEFAULT_CONFIG: Dict[str, Any] = {
    "version": "0.2.0",

    "scan": {
        "folders": [],
        "file_pattern": "AUFGABEN.txt",
        "patterns": ["TODO:", "FIXME:", "- [ ]", "- [x]", "[!]", "blocked"],
        "ignored_dirs": [
            "__pycache__", ".git", "node_modules", ".venv", "venv",
            ".mypy_cache", "dist", "build",
        ],
    },

    "naming": {
        "prefixes": {
            "REL-PUB": {
                "label": "Released Public",
                "weight": 0.0,
                "description": "Public release on GitHub, no active development",
            },
            "REL-PRI": {
                "label": "Released Private",
                "weight": 0.0,
                "description": "Private release on GitHub, no active development",
            },
            "REL": {
                "label": "Released",
                "weight": 0.0,
                "description": "Released/stable, no active development",
            },
            "GO-PUB": {
                "label": "Go Public",
                "weight": 0.2,
                "description": "Approved for public release, preparing git push",
            },
            "GO-PRI": {
                "label": "Go Private",
                "weight": 0.2,
                "description": "Approved for private release, preparing git push",
            },
            "PreGit": {
                "label": "Pre-Git",
                "weight": 0.4,
                "description": "Git preparation phase (Pflichtdateien, Code-Cleanup)",
            },
            "RDY-PRI": {
                "label": "Ready Private",
                "weight": 0.8,
                "description": "Ready, intended for private release",
            },
            "RDY_FAST": {
                "label": "Ready+Fast",
                "weight": 0.5,
                "description": "Ready and in fast-track development",
            },
            "RDY": {
                "label": "Ready",
                "weight": 1.0,
                "description": "Ready for development, highest priority",
            },
            "FAST": {
                "label": "Fast Track",
                "weight": 0.33,
                "description": "Active fast-track development",
            },
            "DEV": {
                "label": "Development",
                "weight": 0.17,
                "description": "Early development stage",
            },
            "ARC": {
                "label": "Archived",
                "weight": 0.0,
                "description": "Archived, no development",
            },
            "USR": {
                "label": "Personal Use",
                "weight": 0.0,
                "description": "Personal tools, not for publication",
            },
        },
        "default_weight": 0.5,
        "separator": "_",
        "theme_folders": [
            "ASSISTENT", "BIO", "CASH", "CODING", "DATA",
            "DOCS", "ENTERTAINMENT", "GAMES", "LLM", "MAIL", "RESEARCH",
        ],
    },

    "session": {
        "interval_minutes": 30,
        "quiet_start": "22:00",
        "quiet_end": "08:00",
        "timeout_minutes": 15,
        "max_tasks_per_session": 10,
    },

    "onboarding": {
        "enabled": True,
        "auto_scan": True,
        "tasks": [
            "Feature-Analyse erstellen",
            "Code-Qualitaetspruefung",
            "AUFGABEN.txt erstellen",
        ],
    },

    "between_checks": {
        "enabled": True,
        "items": [
            "Memory aktualisiert?",
            "Aenderungen dokumentiert?",
            "Tests ausgefuehrt?",
            "Naechster Task klar?",
        ],
    },

    "task_priorities": {
        "BUG": 100,
        "FEATURE": 80,
        "REFACTOR": 60,
        "TEST": 40,
        "DOKU": 20,
    },
}


class Config:
    """Configuration manager for devSoftAgent.

    Loads configuration from a dict or JSON file.  Missing keys
    fall back to DEFAULT_CONFIG values.

    Usage:
        cfg = Config()                                # defaults only
        cfg = Config.from_json("config.json")         # from file
        cfg = Config({"scan": {"folders": ["/p"]}})   # with overrides

        folders = cfg.get("scan.folders")
        cfg.set("session.timeout_minutes", 20)
    """

    def __init__(self, overrides: Optional[Dict[str, Any]] = None):
        self._data = _deep_merge(DEFAULT_CONFIG, overrides or {})

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "Config":
        """Load configuration from a JSON file."""
        path = Path(path)
        if not path.exists():
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data)

    def get(self, dotpath: str, default: Any = None) -> Any:
        """Get a value using dot notation (e.g., 'scan.folders')."""
        keys = dotpath.split(".")
        val: Any = self._data
        for key in keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return default
        return val

    def set(self, dotpath: str, value: Any) -> None:
        """Set a value using dot notation."""
        keys = dotpath.split(".")
        d = self._data
        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """Return full config as dict."""
        return self._data.copy()

    def save(self, path: Union[str, Path]) -> None:
        """Save configuration to JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"Config(keys={list(self._data.keys())})"


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge *override* into a copy of *base*."""
    result = base.copy()
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result
