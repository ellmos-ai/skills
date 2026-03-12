# -*- coding: utf-8 -*-
"""
Encoding Standards Policy.

Enforces consistent encoding practices:
- UTF-8 as default encoding
- BOM detection and handling
- Line ending normalization (LF preferred)
- Fallback chain for reading legacy files
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class EncodingIssue:
    """An encoding-related issue."""
    file_path: str
    issue_type: str  # "bom", "encoding", "line_endings"
    message: str
    auto_fixable: bool = True


class EncodingPolicy:
    """Validates and enforces encoding standards.

    Usage:
        policy = EncodingPolicy()
        issues = policy.check_file(Path("script.py"))
    """

    DEFAULT_ENCODING = "utf-8"
    FALLBACK_CHAIN = ("utf-8", "utf-8-sig", "latin-1", "cp1252")
    TEXT_EXTENSIONS = {
        ".py", ".json", ".md", ".txt", ".yaml", ".yml",
        ".ini", ".cfg", ".toml", ".html", ".css", ".js", ".ts",
    }

    def check_file(self, path: Path) -> List[EncodingIssue]:
        """Check a file for encoding issues.

        Args:
            path: Path to the file

        Returns:
            List of encoding issues found
        """
        issues: List[EncodingIssue] = []

        if path.suffix not in self.TEXT_EXTENSIONS:
            return issues

        try:
            raw = path.read_bytes()
        except OSError:
            return issues

        # BOM check
        if raw.startswith(b"\xef\xbb\xbf"):
            issues.append(EncodingIssue(
                file_path=str(path),
                issue_type="bom",
                message="File has UTF-8 BOM (should be plain UTF-8)",
            ))

        # Encoding check
        detected, text = self._detect_encoding(raw)
        if detected and detected != self.DEFAULT_ENCODING:
            issues.append(EncodingIssue(
                file_path=str(path),
                issue_type="encoding",
                message=f"File encoded as {detected} (should be UTF-8)",
            ))

        # Line ending check
        if text and "\r\n" in text:
            issues.append(EncodingIssue(
                file_path=str(path),
                issue_type="line_endings",
                message="File uses CRLF line endings (LF preferred)",
            ))

        return issues

    def read_safe(self, path: Path) -> Tuple[str, str]:
        """Read a file with encoding fallback.

        Args:
            path: Path to the file

        Returns:
            Tuple of (content, detected_encoding)
        """
        raw = path.read_bytes()
        detected, text = self._detect_encoding(raw)
        return text or "", detected or self.DEFAULT_ENCODING

    def _detect_encoding(
        self, raw: bytes
    ) -> Tuple[Optional[str], Optional[str]]:
        """Try to detect encoding using fallback chain."""
        for enc in self.FALLBACK_CHAIN:
            try:
                text = raw.decode(enc)
                return enc, text
            except (UnicodeDecodeError, ValueError):
                continue
        return None, None
