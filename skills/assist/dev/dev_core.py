#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
dev_core.py — Headless Projekt-Scan (ATI-Fähigkeit), stdlib-only.

Inspiriert von: BACH ATI/entwickler-Agent (Projekt-Scan / Tool-Integration)
Zweck: Schneller, tokensparender Überblick über ein Code-Projekt, bevor das
LLM die eigentlichen Coding-Werkzeuge (CodeCommander-MCP, ellmos-code-tools)
einsetzt. KEIN Store, kein BACH-Import.

Verwendung:
  python dev_core.py scan <pfad>        # Struktur + Sprachen + Marker
  python dev_core.py scan .             # aktuelles Verzeichnis
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

# Projekt-Marker → erkannter Stack
_MARKERS = {
    "pyproject.toml": "Python (pyproject)",
    "requirements.txt": "Python (requirements)",
    "setup.py": "Python (setup.py)",
    "package.json": "Node.js / npm",
    "tsconfig.json": "TypeScript",
    "Cargo.toml": "Rust",
    "go.mod": "Go",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java/Kotlin (Gradle)",
    "default.project.json": "Roblox (Rojo)",
    "Dockerfile": "Docker",
    "docker-compose.yml": "Docker Compose",
    ".git": "Git-Repo",
}

# Verzeichnisse, die beim Scan übersprungen werden
_SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build",
    ".idea", ".vscode", "egg-info", ".pytest_cache", ".mypy_cache", "target",
}


def scan(root: Path, max_depth: int = 4) -> dict:
    """Scannt ein Projektverzeichnis: Sprachen, Marker, Struktur."""
    root = root.resolve()
    ext_counter: Counter = Counter()
    markers: list[str] = []
    file_count = 0
    dir_count = 0
    top_level: list[str] = []

    for marker, label in _MARKERS.items():
        if (root / marker).exists():
            markers.append(label)

    for entry in sorted(root.iterdir()):
        if entry.name in _SKIP_DIRS:
            continue
        top_level.append(entry.name + ("/" if entry.is_dir() else ""))

    for path in root.rglob("*"):
        # Skip-Verzeichnisse ausschließen (auch tief)
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        depth = len(path.relative_to(root).parts)
        if depth > max_depth:
            continue
        if path.is_dir():
            dir_count += 1
        elif path.is_file():
            file_count += 1
            if path.suffix:
                ext_counter[path.suffix.lower()] += 1

    return {
        "root": str(root),
        "markers": markers or ["(keine bekannten Projekt-Marker)"],
        "file_count": file_count,
        "dir_count": dir_count,
        "top_languages": ext_counter.most_common(8),
        "top_level": top_level[:25],
    }


def scan_text(root: Path) -> str:
    s = scan(root)
    lines = [
        f"=== Projekt-Scan: {s['root']} ===",
        f"Stack/Marker: {', '.join(s['markers'])}",
        f"Dateien: {s['file_count']} | Verzeichnisse: {s['dir_count']}",
        "Top-Dateitypen: " + ", ".join(f"{ext} ({n})" for ext, n in s["top_languages"]),
        "Top-Level:",
    ]
    lines += [f"  {name}" for name in s["top_level"]]
    lines.append("")
    lines.append("Nächste Werkzeuge: CodeCommander-MCP (cc_analyze_code, cc_extract_classes,")
    lines.append("cc_diagnose_imports, cc_runtime_import_diagnose) · ellmos-code-tools (CLI).")
    return "\n".join(lines)


def main(argv: list | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] != "scan":
        print(__doc__)
        return 0
    target = Path(argv[1]) if len(argv) > 1 else Path(".")
    if not target.exists():
        print(f"[dev] Pfad nicht gefunden: {target}")
        return 1
    print(scan_text(target))
    return 0


if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
