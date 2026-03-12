# -*- coding: utf-8 -*-
"""
devSoftAgent Code Analyzer.

Provides static analysis of software projects:
- Directory structure mapping
- File statistics (LOC, file count by type)
- Dependency detection (imports)
- Quality metrics (docstring coverage, TODO count)
- Entry point detection
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class FileInfo:
    """Information about a single source file."""

    path: Path
    language: str
    lines_total: int = 0
    lines_code: int = 0
    lines_comment: int = 0
    lines_blank: int = 0
    has_docstring: bool = False
    imports: List[str] = field(default_factory=list)
    todos: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)


@dataclass
class ProjectAnalysis:
    """Complete analysis result for a project."""

    project_path: Path
    project_name: str
    files: List[FileInfo] = field(default_factory=list)
    entry_points: List[Path] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_loc(self) -> int:
        return sum(f.lines_code for f in self.files)

    @property
    def total_lines(self) -> int:
        return sum(f.lines_total for f in self.files)

    @property
    def languages(self) -> Dict[str, int]:
        """File count per language."""
        counts: Dict[str, int] = {}
        for f in self.files:
            counts[f.language] = counts.get(f.language, 0) + 1
        return counts

    @property
    def all_imports(self) -> Set[str]:
        """All unique imports across files."""
        imports: Set[str] = set()
        for f in self.files:
            imports.update(f.imports)
        return imports

    @property
    def todo_count(self) -> int:
        return sum(len(f.todos) for f in self.files)

    @property
    def docstring_coverage(self) -> float:
        """Percentage of Python files with module docstrings."""
        py_files = [f for f in self.files if f.language == "python"]
        if not py_files:
            return 0.0
        return sum(1 for f in py_files if f.has_docstring) / len(py_files) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to summary dict."""
        return {
            "project": self.project_name,
            "path": str(self.project_path),
            "total_files": self.total_files,
            "total_loc": self.total_loc,
            "total_lines": self.total_lines,
            "languages": self.languages,
            "todo_count": self.todo_count,
            "docstring_coverage_pct": round(self.docstring_coverage, 1),
            "entry_points": [str(p.relative_to(self.project_path)) for p in self.entry_points],
            "external_imports": sorted(self._external_imports()),
        }

    def to_markdown(self) -> str:
        """Format analysis as Markdown report."""
        lines = [
            f"# Analyse: {self.project_name}",
            "",
            f"- **Dateien:** {self.total_files}",
            f"- **LOC:** {self.total_loc}",
            f"- **Zeilen gesamt:** {self.total_lines}",
            f"- **Sprachen:** {', '.join(f'{k} ({v})' for k, v in self.languages.items())}",
            f"- **TODOs:** {self.todo_count}",
            f"- **Docstring-Abdeckung:** {self.docstring_coverage:.0f}%",
            "",
        ]

        if self.entry_points:
            lines.append("## Entry Points")
            for ep in self.entry_points:
                lines.append(f"- `{ep.name}`")
            lines.append("")

        ext_imports = self._external_imports()
        if ext_imports:
            lines.append("## Externe Abhaengigkeiten")
            for imp in sorted(ext_imports):
                lines.append(f"- `{imp}`")
            lines.append("")

        return "\n".join(lines)

    def _external_imports(self) -> Set[str]:
        """Filter to likely external (third-party) imports."""
        external: Set[str] = set()
        for imp in self.all_imports:
            root = imp.split(".")[0]
            if root and root not in _PYTHON_STDLIB and not root.startswith("_"):
                external.add(root)
        return external


class CodeAnalyzer:
    """Analyzes source code in a project directory.

    Provides file-level and project-level metrics without
    executing any code.

    Usage:
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze(Path("my_project/"))
        print(analysis.to_markdown())
    """

    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".h": "c-header",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
    }

    IGNORED_DIRS = {
        "__pycache__", ".git", "node_modules", ".venv", "venv",
        ".mypy_cache", ".tox", ".eggs", "dist", "build", ".pytest_cache",
    }

    ENTRY_POINT_NAMES = {
        "main.py", "cli.py", "app.py", "__main__.py",
        "run.py", "start.py", "server.py", "manage.py",
    }

    def analyze(
        self,
        project_path: Path,
        extensions: Optional[List[str]] = None,
    ) -> ProjectAnalysis:
        """Analyze a project directory.

        Args:
            project_path: Root directory
            extensions: File extensions to analyze (default: all known)

        Returns:
            ProjectAnalysis with file-level details
        """
        allowed_ext = (
            set(extensions) if extensions else set(self.LANGUAGE_MAP.keys())
        )

        analysis = ProjectAnalysis(
            project_path=project_path,
            project_name=project_path.name,
        )

        for filepath in project_path.rglob("*"):
            if not filepath.is_file():
                continue
            if any(part in self.IGNORED_DIRS for part in filepath.parts):
                continue
            if filepath.suffix not in allowed_ext:
                continue

            language = self.LANGUAGE_MAP.get(filepath.suffix, "unknown")
            info = self._analyze_file(filepath, language)
            analysis.files.append(info)

            if filepath.name in self.ENTRY_POINT_NAMES:
                analysis.entry_points.append(filepath)

        return analysis

    def _analyze_file(self, filepath: Path, language: str) -> FileInfo:
        """Analyze a single source file."""
        try:
            text = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return FileInfo(path=filepath, language=language)

        lines = text.splitlines()
        info = FileInfo(
            path=filepath,
            language=language,
            lines_total=len(lines),
        )

        if language == "python":
            self._analyze_python(info, text, lines)
        else:
            self._analyze_generic(info, lines)

        return info

    def _analyze_python(
        self, info: FileInfo, text: str, lines: List[str]
    ) -> None:
        """Python-specific analysis."""
        in_multiline = False
        multiline_delim = ""

        for line in lines:
            stripped = line.strip()

            if not stripped:
                info.lines_blank += 1
                continue

            # Track multi-line strings/docstrings
            if in_multiline:
                info.lines_comment += 1
                if multiline_delim in stripped:
                    in_multiline = False
                continue

            if stripped.startswith('"""') or stripped.startswith("'''"):
                quote = stripped[:3]
                # Single-line docstring: """text""" (has 2+ occurrences of the quote)
                if stripped.count(quote) >= 2:
                    info.lines_comment += 1
                    continue
                # Multi-line starts
                in_multiline = True
                multiline_delim = quote
                info.lines_comment += 1
                continue

            if stripped.startswith("#"):
                info.lines_comment += 1
                if "TODO" in stripped or "FIXME" in stripped:
                    info.todos.append(stripped)
                continue

            info.lines_code += 1

        # Imports
        raw_imports = re.findall(
            r"^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))",
            text,
            re.MULTILINE,
        )
        info.imports = [m[0] or m[1] for m in raw_imports if m[0] or m[1]]

        # Module docstring (skip encoding declarations and comments at top)
        info.has_docstring = bool(
            re.match(r'(?:\s*#[^\n]*\n)*\s*(?:"""|\'\'\')[\s\S]', text)
        )

        # Classes and top-level functions
        info.classes = re.findall(r"^class\s+(\w+)", text, re.MULTILINE)
        info.functions = re.findall(r"^def\s+(\w+)", text, re.MULTILINE)

    def _analyze_generic(self, info: FileInfo, lines: List[str]) -> None:
        """Generic analysis for non-Python files."""
        for line in lines:
            stripped = line.strip()
            if not stripped:
                info.lines_blank += 1
            elif (
                stripped.startswith("//")
                or stripped.startswith("/*")
                or stripped.startswith("*")
            ):
                info.lines_comment += 1
                if "TODO" in stripped or "FIXME" in stripped:
                    info.todos.append(stripped)
            else:
                info.lines_code += 1


# Common Python stdlib module names for import filtering
_PYTHON_STDLIB = {
    "abc", "argparse", "array", "ast", "asyncio", "atexit",
    "base64", "binascii", "bisect", "builtins", "bz2",
    "calendar", "cmath", "cmd", "code", "codecs", "collections",
    "colorsys", "compileall", "concurrent", "configparser",
    "contextlib", "contextvars", "copy", "csv", "ctypes", "curses",
    "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis",
    "distutils", "doctest",
    "email", "encodings", "enum", "errno",
    "faulthandler", "filecmp", "fileinput", "fnmatch", "fractions",
    "ftplib", "functools",
    "gc", "getopt", "getpass", "gettext", "glob", "gzip",
    "hashlib", "heapq", "hmac", "html", "http",
    "imaplib", "importlib", "inspect", "io", "ipaddress", "itertools",
    "json",
    "keyword",
    "linecache", "locale", "logging", "lzma",
    "mailbox", "marshal", "math", "mimetypes", "mmap",
    "multiprocessing",
    "netrc", "numbers",
    "operator", "optparse", "os",
    "pathlib", "pdb", "pickle", "pkgutil", "platform", "plistlib",
    "poplib", "posixpath", "pprint", "profile", "pstats",
    "py_compile", "pyclbr", "pydoc",
    "queue",
    "random", "re", "readline", "reprlib", "runpy",
    "sched", "secrets", "select", "selectors", "shelve", "shlex",
    "shutil", "signal", "site", "smtplib", "socket", "socketserver",
    "sqlite3", "ssl", "stat", "statistics", "string", "struct",
    "subprocess", "sys", "sysconfig",
    "tarfile", "tempfile", "textwrap", "threading", "time", "timeit",
    "tkinter", "token", "tokenize", "tomllib", "trace", "traceback",
    "tracemalloc", "tty", "types", "typing",
    "unicodedata", "unittest", "urllib", "uuid",
    "venv",
    "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound",
    "wsgiref",
    "xml", "xmlrpc",
    "zipfile", "zipimport", "zlib",
    "__future__",
}
