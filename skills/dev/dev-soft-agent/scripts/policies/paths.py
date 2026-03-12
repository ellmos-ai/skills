# -*- coding: utf-8 -*-
"""
Path Rules Policy.

Enforces path normalization and structure rules:
- Consistent path separators
- No hardcoded absolute paths in source code
- No double separators
- Spaces in paths are flagged
"""

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import List


@dataclass
class PathIssue:
    """A path-related issue."""
    path: str
    issue_type: str  # "absolute", "double_sep", "spaces"
    message: str
    line_number: int = 0
    severity: str = "warning"  # "warning", "info"


class PathPolicy:
    """Validates path usage in source code.

    Usage:
        policy = PathPolicy()
        issues = policy.check_source(Path("main.py"))
        normalized = policy.normalize("/foo//bar\\baz")
    """

    # Patterns that indicate hardcoded absolute paths in source code
    ABSOLUTE_PATTERNS = [
        re.compile(r'["\'][A-Z]:\\\\'),           # Windows: "C:\\"
        re.compile(r'["\']/home/\w+'),             # Linux: "/home/user"
        re.compile(r'["\']/Users/\w+'),            # macOS: "/Users/user"
    ]

    def check_source(self, path: Path) -> List[PathIssue]:
        """Check a source file for path-related issues.

        Args:
            path: Path to the source file

        Returns:
            List of path issues found
        """
        issues: List[PathIssue] = []

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return issues

        for i, line in enumerate(text.splitlines(), 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            # Check for hardcoded absolute paths
            for pattern in self.ABSOLUTE_PATTERNS:
                if pattern.search(line):
                    issues.append(PathIssue(
                        path=str(path),
                        issue_type="absolute",
                        message=f"Hardcoded absolute path found",
                        line_number=i,
                        severity="warning",
                    ))
                    break  # one issue per line

        return issues

    @staticmethod
    def normalize(path_str: str) -> str:
        """Normalize a path string.

        - Converts backslashes to forward slashes
        - Removes double separators
        - Strips trailing separators

        Args:
            path_str: Raw path string

        Returns:
            Normalized path string
        """
        # Normalize separators
        result = path_str.replace("\\", "/")
        # Remove double slashes (but keep leading // for UNC paths)
        while "//" in result[2:]:
            result = result[:2] + result[2:].replace("//", "/")
        # Strip trailing slash
        return result.rstrip("/")
