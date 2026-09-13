#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project the canonical Community Outreach runtime into a target directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SOURCE_FILES = {
    "outreach_engine.py": SCRIPT_DIR / "outreach_engine.py",
    "outreach_runner.py": SCRIPT_DIR / "outreach_runner.py",
    "README.md": SKILL_DIR / "references" / "runtime-readme.md",
    "tests/test_outreach.py": SKILL_DIR / "tests" / "test_runtime_projection.py",
}


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        temporary.write_bytes(content)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def projection_state(target: Path) -> tuple[bool, dict[str, str]]:
    hashes: dict[str, str] = {}
    current = True
    for relative, source in SOURCE_FILES.items():
        content = source.read_bytes()
        hashes[relative] = _sha256(content)
        destination = target / Path(relative)
        if not destination.exists() or destination.read_bytes() != content:
            current = False
    return current, hashes


def deploy(target: Path) -> dict[str, object]:
    target.mkdir(parents=True, exist_ok=True)
    previous = {
        relative: ((target / Path(relative)).read_bytes() if (target / Path(relative)).exists() else None)
        for relative in SOURCE_FILES
    }
    try:
        for relative, source in SOURCE_FILES.items():
            _atomic_write(target / Path(relative), source.read_bytes())
    except Exception:
        for relative, content in previous.items():
            destination = target / Path(relative)
            if content is None:
                if destination.exists():
                    destination.unlink()
            else:
                _atomic_write(destination, content)
        raise
    current, hashes = projection_state(target)
    if not current:
        raise RuntimeError("Runtime projection failed its byte-for-byte readback")
    return {"status": "deployed", "target": str(target), "files": hashes}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Deploy the portable Community Outreach runtime")
    parser.add_argument("--target", required=True, help="Runtime workspace directory")
    parser.add_argument("--check", action="store_true", help="Verify projection hashes without writing")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)
    target = Path(args.target).expanduser().resolve()
    if args.check:
        current, hashes = projection_state(target)
        result: dict[str, object] = {
            "status": "current" if current else "stale",
            "target": str(target),
            "files": hashes,
        }
        exit_code = 0 if current else 1
    else:
        result = deploy(target)
        exit_code = 0
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
