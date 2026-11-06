#!/usr/bin/env python3
"""skill_smoke_gate.py — Opt-in-Smoke-Test-Gate fuer mitgelieferte Skill-Skripte.

Zweck
-----
Prueft mitgelieferte Python-Skripte in Skills auf Lauffaehigkeit (Bytecode-Kompilierung,
--help bzw. Importierbarkeit) und fuehrt vorhandene Skill-eigene Tests (tests/test_smoke.py
bzw. tests/test_*.py) aus.

Rollout
-------
Gemaess Ticket T-20260927-691478228 startet dieses Gate standardmaessig im WARN_ONLY-Modus
(Exit 0). Mit dem Schalter `--strict` schaltet es auf blockierendes Verhalten um (Exit 1 bei Fehlern).

Verwendung
----------
    python testing/skill_smoke_gate.py                 # Scannt alle Skills im WARN_ONLY Modus
    python testing/skill_smoke_gate.py --strict        # Blockierender Modus (CI-Gate)
    python testing/skill_smoke_gate.py --skill dev/dev-soft-agent  # Einzelner Skill
    python testing/skill_smoke_gate.py --json          # JSON-Bericht ausgeben
"""

from __future__ import annotations

import argparse
import ast
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO / "skills"

# Skills or packages known to require optional or external runtime dependencies
KNOWN_OPTIONAL_DEPS = {
    "bpy",
    "vosk",
    "openai-whisper",
    "feedparser",
    "defusedxml",
    "chromadb",
    "ollama",
    "youtube_transcript_api",
    "yt_dlp",
    "numpy",
}


def parse_frontmatter(text: str) -> dict:
    """Extrahiert Frontmatter als flaches oder verschachteltes Dict."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    fm: dict = {}
    current_key = None
    subdict: dict = {}

    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if re.match(r"^\w[\w-]*:", line):
            if current_key and subdict:
                fm[current_key] = subdict
                subdict = {}
            k, v = line.split(":", 1)
            current_key = k.strip()
            val = v.strip()
            if val:
                fm[current_key] = val
        elif line.startswith("  ") and current_key:
            parts = line.strip().split(":", 1)
            if len(parts) == 2:
                subdict[parts[0].strip()] = parts[1].strip()

    if current_key and subdict:
        fm[current_key] = subdict
    return fm


def get_skill_python_files(skill_path: Path) -> tuple[list[Path], list[Path]]:
    """Gibt (code_files, test_files) fuer den Skill zurueck."""
    all_py = [
        p for p in skill_path.rglob("*.py")
        if "__pycache__" not in p.parts
    ]
    test_files = [
        p for p in all_py
        if "test" in p.name.lower() or "tests" in p.parts
    ]
    code_files = [p for p in all_py if p not in test_files]
    return sorted(code_files), sorted(test_files)


def check_skill_smoke(skill_path: Path) -> dict:
    """Prueft einen Skill auf Lauffaehigkeit und Tests."""
    skill_md = skill_path / "SKILL.md"
    name = skill_path.name
    category = skill_path.parent.name
    rel_path = f"{category}/{name}"

    if not skill_md.is_file():
        return {
            "skill": rel_path,
            "status": "SKIP",
            "findings": ["Keine SKILL.md vorhanden"],
            "has_tests": False,
            "py_count": 0,
        }

    code_files, test_files = get_skill_python_files(skill_path)
    if not code_files and not test_files:
        return {
            "skill": rel_path,
            "status": "PASS",
            "findings": ["Reiner Dokumentations-Skill (keine Python-Dateien)"],
            "has_tests": False,
            "py_count": 0,
        }

    findings: list[str] = []
    has_errors = False

    # 1. Bytecode-Kompilierung (Syntax-Check)
    for py_file in code_files + test_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            has_errors = True
            findings.append(f"Syntaxfehler in {py_file.name}: {e.msg}")

    # 2. Ausfuehrung vorhandener Tests
    smoke_test = skill_path / "tests" / "test_smoke.py"
    if smoke_test.is_file():
        # Dedizierter Smoke-Test vorhanden
        res = subprocess.run(
            [sys.executable, "-m", "pytest", str(smoke_test), "-q"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            cwd=str(skill_path),
        )
        if res.returncode != 0:
            has_errors = True
            err_line = res.stderr.strip() or res.stdout.strip()
            findings.append(f"test_smoke.py fehlgeschlagen (rc={res.returncode}): {err_line[:120]}")
        else:
            findings.append("test_smoke.py erfolgreich bestanden")
    elif test_files:
        # Bestehende Tests vorhanden (z.B. in tests/)
        test_dir = skill_path / "tests"
        target = str(test_dir) if test_dir.is_dir() else str(test_files[0])
        res = subprocess.run(
            [sys.executable, "-m", "pytest", target, "-q"],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
            cwd=str(skill_path),
        )
        if res.returncode != 0:
            has_errors = True
            findings.append(f"Vorhandene Tests fehlgeschlagen (rc={res.returncode})")
        else:
            findings.append(f"{len(test_files)} vorhandene Testdateien erfolgreich ausgefuehrt")
    else:
        # Keine Tests vorhanden -> Pruefe Skripte via AST & --help (wo anwendbar)
        findings.append("Keine Test-Suite (test_smoke.py oder tests/) vorhanden")

        # Ueberpruefe CLI-Skripte auf --help Lauffaehigkeit
        for py_file in code_files:
            if py_file.name == "__init__.py":
                continue

            content = py_file.read_text(encoding="utf-8", errors="replace")
            # Pruefe ob Skript als CLI aufrufbar gedacht ist
            if 'if __name__ == "__main__":' in content or "argparse" in content:
                # Pruefe ob bekannte optionale Imports vorliegen
                has_opt = False
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name.split(".")[0] in KNOWN_OPTIONAL_DEPS:
                                    has_opt = True
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            if node.module.split(".")[0] in KNOWN_OPTIONAL_DEPS:
                                has_opt = True
                except SyntaxError:
                    has_errors = True
                    findings.append(f"{py_file.name}: SyntaxError bei AST-Analyse")
                    continue

                if has_opt:
                    findings.append(f"{py_file.name}: Optionale Abhaengigkeit deklariert (Help-Check uebersprungen)")
                    continue

                # Help-Check im Subprozess
                try:
                    res_help = subprocess.run(
                        [sys.executable, str(py_file), "--help"],
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=10,
                        check=False,
                        cwd=str(py_file.parent),
                    )
                    # Exit-Codes 0 (Standard help) oder 2 (manche Custom-Parser mit Usage-Meldung) gelten als lebendig
                    if res_help.returncode in (0, 2):
                        findings.append(f"{py_file.name}: --help erfolgreich (rc={res_help.returncode})")
                    else:
                        findings.append(f"{py_file.name}: --help rc={res_help.returncode}")
                except subprocess.TimeoutExpired:
                    has_errors = True
                    findings.append(f"{py_file.name}: Timeout beim --help Aufruf")
                except OSError as e:
                    findings.append(f"{py_file.name}: Subprozessfehler: {e}")

    status = "FAIL" if has_errors else ("PASS" if bool(test_files) else "WARN")
    return {
        "skill": rel_path,
        "status": status,
        "findings": findings,
        "has_tests": bool(test_files),
        "py_count": len(code_files) + len(test_files),
    }


def scan_all_skills(skills_root: Path) -> list[dict]:
    """Scannt alle Skills im Ordner."""
    skill_dirs = sorted([
        p for p in skills_root.glob("*/*")
        if p.is_dir() and (p / "SKILL.md").is_file()
    ])
    results = []
    for s in skill_dirs:
        results.append(check_skill_smoke(s))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke-Test-Gate fuer mitgelieferte Skill-Skripte")
    parser.add_argument("--repo", type=str, default="", help="Pfad zum Repository-Root")
    parser.add_argument("--skill", type=str, default="", help="Nur einen bestimmten Skill pruefen (z.B. dev/community-outreach)")
    parser.add_argument("--strict", action="store_true", help="Blockierender Modus: Exit 1 bei Fehlern (Default ist WARN_ONLY)")
    parser.add_argument("--json", action="store_true", help="Ergebnisse im JSON-Format ausgeben")
    args = parser.parse_args(argv)

    repo_dir = Path(args.repo) if args.repo else REPO
    skills_dir = repo_dir / "skills"

    if args.skill:
        target = skills_dir / args.skill
        if not target.is_dir():
            target = Path(args.skill)
        if not target.is_dir():
            print(f"[FEHLER] Skill-Verzeichnis nicht gefunden: {args.skill}")
            return 1
        results = [check_skill_smoke(target)]
    else:
        results = scan_all_skills(skills_dir)

    total = len(results)
    fails = [r for r in results if r["status"] == "FAIL"]
    warns = [r for r in results if r["status"] == "WARN"]
    passes = [r for r in results if r["status"] == "PASS"]
    with_code = [r for r in results if r["py_count"] > 0]
    with_tests = [r for r in results if r["has_tests"]]

    if args.json:
        print(json.dumps({
            "total_skills": total,
            "skills_with_python": len(with_code),
            "skills_with_tests": len(with_tests),
            "pass_count": len(passes),
            "warn_count": len(warns),
            "fail_count": len(fails),
            "results": results,
        }, indent=2, ensure_ascii=False))
    else:
        print("=== Skill Smoke Test Gate ===")
        print(f"Gesamtanzahl Skills: {total}")
        print(f"Skills mit Python-Code: {len(with_code)}")
        print(f"Skills mit vorhandenen Tests: {len(with_tests)}")
        print(f"Ergebnis: {len(passes)} PASS, {len(warns)} WARN, {len(fails)} FAIL")
        print("-" * 40)

        if fails:
            print("\n[FEHLER] Skills mit fehlgeschlagenen Smoke-Pruefungen:")
            for f in fails:
                print(f"  * {f['skill']}:")
                for item in f["findings"]:
                    print(f"      - {item}")

        if warns:
            print(f"\n[WARNUNG] {len(warns)} Skills mit Python-Code haben noch keine eigene Testsuite:")
            for w in warns[:15]:
                print(f"  * {w['skill']} ({w['py_count']} Python-Dateien)")
            if len(warns) > 15:
                print(f"  ... und {len(warns) - 15} weitere.")

    if args.strict and fails:
        print("\n[STRICT GATE FAILED] Blockierende Fehler vorhanden!")
        return 1

    print("\n[OK] Smoke-Test-Gate erfolgreich abgeschlossen (WARN_ONLY Modus aktiv).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
