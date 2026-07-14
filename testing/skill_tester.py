#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_tester.py -- Skill-Qualitaetstester fuer die .SKILLS Bibliothek

Dreiperspektivisches Testverfahren:
  S-Tests (Statisch):         Automatisierte Frontmatter/Code-Pruefung
  L-Tests (LLM-Selbsterfahrung): Prompt-generierte LLM-Bewertung
  U-Tests (User-Erfahrung):  Interaktive Nutzerbewertung

Usage:
    python skill_tester.py test <skill-pfad>                   # STANDARD-Profil
    python skill_tester.py test <skill-pfad> --profile QUICK   # Schnelltest
    python skill_tester.py test <skill-pfad> --type static     # Nur S-Tests
    python skill_tester.py test <skill-pfad> --type llm        # Nur L-Tests generieren
    python skill_tester.py test <skill-pfad> --type user       # Nur U-Tests
    python skill_tester.py report <skill-name>                 # Letztes Ergebnis
    python skill_tester.py batch [--profile QUICK]             # Alle lokalen Skills testen
    python skill_tester.py batch --type static --ci [SKILL.md ...]
                                                               # CI/pre-commit Gate

Version: 1.0.0
"""

import sys
import os
import re
import json
import ast
import subprocess
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
SKILLS_ROOT = SCRIPT_DIR.parent / "skills"
RESULTS_DIR = SCRIPT_DIR / "results"
PROFILES_DIR = SCRIPT_DIR / "profiles"


# ---------------------------------------------------------------------------
# Frontmatter Parser
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Extrahiert YAML-Frontmatter aus Markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}

    fm = {}
    current_key = None
    current_indent = 0
    nested = {}

    for line in match.group(1).split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # Top-level key: value
        m = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if m and not line.startswith(' '):
            if current_key and nested:
                fm[current_key] = nested
                nested = {}
            current_key = m.group(1)
            val = m.group(2).strip()
            if val and val != '>':
                # Boolean
                if val.lower() == 'true':
                    fm[current_key] = True
                elif val.lower() == 'false':
                    fm[current_key] = False
                elif val.lower() == 'null':
                    fm[current_key] = None
                elif val.startswith('[') and val.endswith(']'):
                    # Inline list
                    items = [x.strip().strip('"').strip("'")
                             for x in val[1:-1].split(',') if x.strip()]
                    fm[current_key] = items
                else:
                    fm[current_key] = val.strip('"').strip("'")
            elif val == '>':
                fm[current_key] = ''  # Multiline, collected below
            continue

        # Nested key under current block
        m2 = re.match(r'^\s+(\w[\w-]*)\s*:\s*(.*)', line)
        if m2 and current_key:
            nkey = m2.group(1)
            nval = m2.group(2).strip()
            if nval.startswith('[') and nval.endswith(']'):
                nested[nkey] = [x.strip().strip('"').strip("'")
                                for x in nval[1:-1].split(',') if x.strip()]
            elif nval.lower() == 'true':
                nested[nkey] = True
            elif nval.lower() == 'false':
                nested[nkey] = False
            elif nval.lower() == 'null':
                nested[nkey] = None
            elif nval:
                nested[nkey] = nval.strip('"').strip("'")
            continue

        # Multiline description continuation
        if current_key and isinstance(fm.get(current_key), str) and stripped:
            fm[current_key] = (fm[current_key] + ' ' + stripped).strip()

    if current_key and nested:
        fm[current_key] = nested

    return fm


FRONTMATTER_REQUIRED_FIELDS = (
    'name', 'version', 'type', 'author', 'created', 'updated', 'description',
    'standalone',
)


def frontmatter_gate_errors(skill_path):
    """Return blocking frontmatter errors for CI and pre-commit."""
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md nicht gefunden"]

    text = skill_md.read_text(encoding='utf-8', errors='replace')
    fm = parse_frontmatter(text)
    if not fm:
        return ["YAML-Frontmatter fehlt oder ist nicht lesbar"]

    errors = []
    for field in FRONTMATTER_REQUIRED_FIELDS:
        if field not in fm or fm[field] in (None, ''):
            errors.append(f"Pflichtfeld fehlt: {field}")

    name = str(fm.get('name', ''))
    if name and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        errors.append(f"Name ist nicht kebab-case: {name}")

    version = str(fm.get('version', ''))
    if version and not re.fullmatch(r'\d+\.\d+\.\d+', version):
        errors.append(f"Version ist nicht SemVer: {version}")

    if 'standalone' in fm and not isinstance(fm['standalone'], bool):
        errors.append("standalone muss true oder false sein")

    return errors


# ---------------------------------------------------------------------------
# S-Tests (Statisch / Automatisiert)
# ---------------------------------------------------------------------------

def s001_frontmatter(skill_path):
    """S001: Frontmatter-Pflichtfelder und Typen pruefen."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return 0, "SKILL.md nicht gefunden"

    text = skill_md.read_text(encoding='utf-8', errors='replace')
    fm = parse_frontmatter(text)

    required = list(FRONTMATTER_REQUIRED_FIELDS)
    recommended = ['anthropic_compatible', 'category', 'tags',
                   'language', 'status', 'dependencies']

    missing_req = [f for f in required if f not in fm]
    missing_rec = [f for f in recommended if f not in fm]
    has_provenance = isinstance(fm.get('provenance'), dict)

    score = 5.0
    details = []

    if missing_req:
        score -= len(missing_req) * 1.0
        details.append(f"Pflichtfelder fehlen: {missing_req}")

    if missing_rec:
        penalty = len(missing_rec) * 0.2
        score -= min(penalty, 1.5)
        details.append(f"Empfohlene Felder fehlen: {missing_rec}")

    if not has_provenance and fm.get('bach_origin'):
        score -= 0.5
        details.append("bach_origin=true aber kein provenance-Block")

    # Version format check
    version = fm.get('version', '')
    if version and not re.match(r'^\d+\.\d+\.\d+$', str(version)):
        score -= 0.5
        details.append(f"Version '{version}' nicht im SemVer-Format")

    score = max(0, min(5, score))
    return round(score, 1), "; ".join(details) if details else "Alle Felder korrekt"


def s002_completeness(skill_path):
    """S002: Inhaltliche Vollstaendigkeit pruefen."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return 0, "SKILL.md nicht gefunden"

    text = skill_md.read_text(encoding='utf-8', errors='replace')
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.DOTALL)

    checks = {
        'title': bool(re.search(r'^#\s+\S', body, re.MULTILINE)),
        'description_text': len(body.strip()) > 200,
        'changelog': 'changelog' in body.lower(),
        'example': bool(re.search(r'```|Beispiel|Example|Nutzung|Usage', body, re.IGNORECASE)),
        'sections': body.count('\n## ') >= 2,
    }

    # Therapy skills: ethics reference
    fm = parse_frontmatter(text)
    if fm.get('category') == 'therapy':
        checks['ethics_ref'] = 'ETHICS.md' in body

    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    score = (passed / total) * 5

    missing = [k for k, v in checks.items() if not v]
    detail = f"{passed}/{total} Kriterien erfuellt"
    if missing:
        detail += f" (fehlt: {missing})"

    return round(score, 1), detail


def s003_dependencies(skill_path):
    """S003: Abhaengigkeiten analysieren."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return 0, "SKILL.md nicht gefunden"

    fm = parse_frontmatter(skill_md.read_text(encoding='utf-8', errors='replace'))
    deps = fm.get('dependencies', {})

    py_files = list(skill_path.rglob("*.py"))
    has_code = len(py_files) > 0

    score = 5.0
    details = []

    if isinstance(deps, dict):
        pip_deps = deps.get('python', [])
        service_deps = deps.get('services', [])

        if pip_deps:
            score -= len(pip_deps) * 0.3
            details.append(f"pip: {pip_deps}")
        if service_deps:
            score -= len(service_deps) * 0.5
            details.append(f"services: {service_deps}")
        if not pip_deps and not service_deps:
            details.append("Zero Dependencies")
    else:
        if has_code:
            score -= 0.5
            details.append("dependencies-Block fehlt trotz Python-Code")

    # Check if py files import non-stdlib
    external_imports = set()
    stdlib_plus = {
        'os', 'sys', 're', 'json', 'pathlib', 'datetime', 'typing',
        'collections', 'functools', 'itertools', 'math', 'hashlib',
        'uuid', 'copy', 'io', 'abc', 'dataclasses', 'enum', 'textwrap',
        'argparse', 'unittest', 'sqlite3', 'csv', 'xml', 'html',
        'http', 'urllib', 'email', 'logging', 'subprocess', 'shutil',
        'tempfile', 'glob', 'fnmatch', 'stat', 'time', 'calendar',
        'random', 'string', 'struct', 'codecs', 'base64', 'binascii',
        'platform', 'socket', 'contextlib', 'warnings', 'traceback',
        'inspect', 'importlib', 'pkgutil', 'pprint', 'difflib',
        'configparser', 'threading', 'multiprocessing', 'concurrent',
        'asyncio', 'signal', 'getpass', 'secrets',
    }

    for py_file in py_files:
        try:
            tree = ast.parse(py_file.read_text(encoding='utf-8', errors='replace'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split('.')[0]
                        if top not in stdlib_plus:
                            external_imports.add(top)
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.level == 0:
                        top = node.module.split('.')[0]
                        if top not in stdlib_plus:
                            external_imports.add(top)
        except SyntaxError:
            score -= 0.5
            details.append(f"SyntaxError: {py_file.name}")

    # Check declared vs actual
    declared = set(deps.get('python', [])) if isinstance(deps, dict) else set()
    undeclared = external_imports - declared - {'scripts', 'generator', 'services',
                                                 'sources', 'workflows', 'policies',
                                                 'prompt_templates', 'kontext', 'schemas',
                                                 'templates', 'examples'}
    if undeclared:
        score -= len(undeclared) * 0.3
        details.append(f"Nicht deklarierte Imports: {undeclared}")

    score = max(0, min(5, score))
    return round(score, 1), "; ".join(details) if details else "Keine Abhaengigkeiten"


def s004_code_quality(skill_path):
    """S004: Code-Qualitaet der Python-Scripts."""
    py_files = list(skill_path.rglob("*.py"))
    if not py_files:
        return 5.0, "Kein Python-Code (reiner Dokumentations-Skill)"

    score = 5.0
    details = []
    total_lines = 0
    total_docstrings = 0

    for py_file in py_files:
        if py_file.name == '__init__.py':
            continue
        try:
            content = py_file.read_text(encoding='utf-8', errors='replace')
            lines = content.split('\n')
            total_lines += len(lines)

            # Docstring check
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    if (node.body and isinstance(node.body[0], ast.Expr)
                            and isinstance(node.body[0].value, ast.Constant)
                            and isinstance(node.body[0].value.value, str)):
                        total_docstrings += 1

            # Hardcoded paths
            if re.search(r'C:\\Users\\|/home/\w+/', content):
                score -= 0.5
                details.append(f"{py_file.name}: Hardcodierte Pfade")

            # Print statt logging (minor)
            emoji_prints = len(re.findall(r'print\(.*[\U0001F300-\U0001F9FF]', content))
            if emoji_prints > 0:
                details.append(f"{py_file.name}: {emoji_prints}x Emoji in print()")

        except SyntaxError as e:
            score -= 1.0
            details.append(f"{py_file.name}: SyntaxError ({e})")

    if total_lines > 0 and total_lines > 50 and total_docstrings == 0:
        score -= 0.5
        details.append("Keine Docstrings in groesserem Code")

    score = max(0, min(5, score))
    return round(score, 1), "; ".join(details) if details else f"{len(py_files)} Dateien, Code sauber"


def s005_standalone_check(skill_path):
    """S005: Standalone-Faehigkeit pruefen (keine BACH/User-Abhaengigkeiten)."""
    score = 5.0
    details = []
    violations = []

    patterns = {
        'BACH CLI': r'bach\s+(psycho|task|skills|tools)\s',
        'BACH API': r'from\s+bach_api\s+import|import\s+bach_api',
        'BACH internal': r'from\s+(tools|core|hub)\.\w+\s+import',
        'BACH DB': r'bach\.db',
        'User path': r'C:\\Users\\lukas|/c/Users/lukas|/home/lukas',
        'parent_agent': r'^parent_agent:',
        'expert field': r'^expert:\s+\w',
    }

    for filepath in skill_path.rglob("*"):
        if filepath.is_dir() or filepath.suffix not in ['.md', '.py', '.txt', '.json']:
            continue
        try:
            content = filepath.read_text(encoding='utf-8', errors='replace')
            for label, pattern in patterns.items():
                matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                if matches:
                    violations.append(f"{filepath.name}: {label} ({len(matches)}x)")
        except Exception:
            pass

    if violations:
        score -= len(violations) * 0.5
        details = violations
    else:
        details = ["Keine BACH/User-Abhaengigkeiten gefunden"]

    # Check frontmatter standalone flag
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        fm = parse_frontmatter(skill_md.read_text(encoding='utf-8', errors='replace'))
        if fm.get('standalone') is False and not violations:
            details.append("standalone=false aber keine Abhaengigkeiten erkannt")
        elif fm.get('standalone') is True and violations:
            score -= 1.0
            details.append("WARNUNG: standalone=true aber Abhaengigkeiten vorhanden!")

    score = max(0, min(5, score))
    return round(score, 1), "; ".join(details)


S_TESTS = {
    'S001': ('Frontmatter', s001_frontmatter),
    'S002': ('Vollstaendigkeit', s002_completeness),
    'S003': ('Dependencies', s003_dependencies),
    'S004': ('Code-Qualitaet', s004_code_quality),
    'S005': ('Standalone-Check', s005_standalone_check),
}


# ---------------------------------------------------------------------------
# L-Tests (LLM-Selbsterfahrung) -- Prompt-Generator
# ---------------------------------------------------------------------------

def generate_l_test_prompt(skill_path):
    """Generiert den Prompt fuer LLM-Selbsterfahrungstests."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding='utf-8', errors='replace')
    fm = parse_frontmatter(content)
    name = fm.get('name', skill_path.name)

    prompt = f"""# LLM-Selbsterfahrungstest: {name}

Du bist ein LLM-Tester. Du hast gerade den folgenden Skill geladen.
Bewerte ihn aus deiner eigenen Erfahrung als KI-Assistent.

---

## Der Skill

```markdown
{content}
```

---

## Deine Aufgabe

Bewerte den Skill anhand dieser 6 Kriterien (jeweils 0-5 Punkte).
Antworte AUSSCHLIESSLICH im folgenden JSON-Format:

```json
{{
  "L001_readability": {{
    "score": <0-5>,
    "notes": "Verstehe ich sofort, was der Skill tut? Ist die Struktur klar?"
  }},
  "L002_applicability": {{
    "score": <0-5>,
    "notes": "Kann ich den Skill sofort anwenden, ohne Zusatzwissen?"
  }},
  "L003_completeness": {{
    "score": <0-5>,
    "notes": "Fehlt mir etwas Wesentliches, um den Skill zu nutzen?"
  }},
  "L004_standalone": {{
    "score": <0-5>,
    "notes": "Brauche ich externes Wissen oder andere Systeme?"
  }},
  "L005_prompt_quality": {{
    "score": <0-5>,
    "notes": "Sind die Anweisungen klar, praezise und effektiv?"
  }},
  "L006_example_quality": {{
    "score": <0-5>,
    "notes": "Helfen die Beispiele beim Verstaendnis? Sind genug vorhanden?"
  }},
  "summary": {{
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."],
    "one_sentence": "Zusammenfassung in einem Satz"
  }}
}}
```

## Bewertungsskala

- 5 = Exzellent (Vorbildlich, nichts zu verbessern)
- 4 = Gut (Kleine Verbesserungen moeglich)
- 3 = Akzeptabel (Funktioniert, aber deutlicher Verbesserungsbedarf)
- 2 = Mangelhaft (Wesentliche Probleme)
- 1 = Schlecht (Kaum nutzbar)
- 0 = Unbrauchbar

## Wichtig

- Bewerte EHRLICH. Ein Score von 5 ist selten.
- Begruende jeden Score kurz.
- Wenn der Skill Code enthaelt: Pruefe ob du den Code verstehst und anwenden koenntest.
- Wenn der Skill ein Protokoll ist: Pruefe ob du die Schritte ausfuehren koenntest.
"""
    return prompt


# ---------------------------------------------------------------------------
# U-Tests (User-Erfahrung) -- Interaktiv
# ---------------------------------------------------------------------------

def run_u_tests_interactive(skill_path):
    """Fuehrt interaktive User-Erfahrungstests durch."""
    fm_text = (skill_path / "SKILL.md").read_text(encoding='utf-8', errors='replace')
    fm = parse_frontmatter(fm_text)
    name = fm.get('name', skill_path.name)

    print(f"\n{'='*60}")
    print(f"  U-TEST: User-Erfahrung fuer '{name}'")
    print(f"{'='*60}")
    print(f"\nBitte bewerte den Skill nach deiner Nutzungserfahrung.")
    print(f"Skala: 0 (unbrauchbar) bis 5 (exzellent)\n")

    tests = {
        'U001': 'Aufgaben-Erfuellung: Hat der Skill gemacht, was du wolltest?',
        'U002': 'Ergebnis-Qualitaet: War das Ergebnis gut genug?',
        'U003': 'Effizienz: War der Weg zum Ergebnis effizient?',
        'U004': 'Ueberraschungen: Gab es unerwartetes Verhalten? (5=keine, 0=viele)',
        'U005': 'Wiederverwendbarkeit: Wuerdest du den Skill nochmal nutzen?',
    }

    results = {}
    for test_id, question in tests.items():
        while True:
            try:
                raw = input(f"  {test_id} - {question}\n  Score (0-5): ").strip()
                score = float(raw)
                if 0 <= score <= 5:
                    notes = input(f"  Anmerkung (optional, Enter=skip): ").strip()
                    results[test_id] = {
                        'score': score,
                        'notes': notes if notes else ''
                    }
                    print()
                    break
                else:
                    print("  Bitte 0-5 eingeben.")
            except ValueError:
                print("  Bitte eine Zahl eingeben.")
            except EOFError:
                return results

    # Optional: Welche Aufgabe wurde getestet?
    try:
        task = input("  Welche Aufgabe hast du dem Skill gegeben? (optional): ").strip()
        if task:
            results['_task_description'] = task
    except EOFError:
        pass

    return results


# ---------------------------------------------------------------------------
# Profil-Laden
# ---------------------------------------------------------------------------

PROFILES = {
    'QUICK': {
        's_tests': ['S001', 'S005'],
        'l_tests': ['L001', 'L002'],
        'u_tests': [],
    },
    'STANDARD': {
        's_tests': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'l_tests': ['L001', 'L002', 'L003', 'L004', 'L005', 'L006'],
        'u_tests': [],
    },
    'FULL': {
        's_tests': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'l_tests': ['L001', 'L002', 'L003', 'L004', 'L005', 'L006'],
        'u_tests': ['U001', 'U002', 'U003', 'U004', 'U005'],
    },
    'STATIC': {
        's_tests': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'l_tests': [],
        'u_tests': [],
    },
    'LLM_ONLY': {
        's_tests': [],
        'l_tests': ['L001', 'L002', 'L003', 'L004', 'L005', 'L006'],
        'u_tests': [],
    },
    'USER_ONLY': {
        's_tests': [],
        'l_tests': [],
        'u_tests': ['U001', 'U002', 'U003', 'U004', 'U005'],
    },
}


# ---------------------------------------------------------------------------
# Score-Berechnung
# ---------------------------------------------------------------------------

def calculate_dimensions(s_results, l_results, u_results):
    """Berechnet die 5 Fitness-Dimensionen."""
    def avg(*keys_and_dicts):
        vals = []
        for key, d in keys_and_dicts:
            if key in d and isinstance(d[key], dict) and 'score' in d[key]:
                vals.append(d[key]['score'])
        return round(sum(vals) / len(vals), 1) if vals else None

    dims = {}
    dims['d1_clarity'] = avg(('L001', l_results), ('L005', l_results), ('U003', u_results))
    dims['d2_completeness'] = avg(('S002', s_results), ('L003', l_results), ('L006', l_results))
    dims['d3_independence'] = avg(('S003', s_results), ('S005', s_results), ('L004', l_results))
    dims['d4_effectiveness'] = avg(('U001', u_results), ('U002', u_results), ('U005', u_results))
    dims['d5_efficiency'] = avg(('S004', s_results), ('U003', u_results))

    return {k: v for k, v in dims.items() if v is not None}


def calculate_quality_score(s_results, l_results, u_results):
    """Berechnet den gewichteten Gesamtscore."""
    def avg_score(results):
        scores = [v['score'] for v in results.values()
                  if isinstance(v, dict) and 'score' in v]
        return sum(scores) / len(scores) if scores else None

    s_avg = avg_score(s_results)
    l_avg = avg_score(l_results)
    u_avg = avg_score(u_results)

    parts = []
    weights = []

    if s_avg is not None:
        parts.append(s_avg * 0.25)
        weights.append(0.25)
    if l_avg is not None:
        parts.append(l_avg * 0.50)
        weights.append(0.50)
    if u_avg is not None:
        parts.append(u_avg * 0.25)
        weights.append(0.25)

    if not weights:
        return 0.0

    # Normalize weights if not all test types present
    total_weight = sum(weights)
    return round(sum(parts) / total_weight, 2)


# ---------------------------------------------------------------------------
# Skill finden
# ---------------------------------------------------------------------------

def find_skill(identifier):
    """Findet Skill-Pfad anhand Name oder Pfad."""
    # Direkter Pfad (resolve: relative Pfade normalisieren, sonst crasht
    # spaeter skill_path.relative_to(SKILLS_ROOT) mit ValueError)
    p = Path(identifier)
    if p.exists() and (p / "SKILL.md").exists():
        return p.resolve()

    # Relative zum Skills-Root
    rel = SKILLS_ROOT / identifier
    if rel.exists() and (rel / "SKILL.md").exists():
        return rel

    # Suche nach Name
    for skill_dir in SKILLS_ROOT.rglob("SKILL.md"):
        if skill_dir.parent.name == identifier:
            return skill_dir.parent

    # Suche in Kategorien
    for cat_dir in SKILLS_ROOT.iterdir():
        if cat_dir.is_dir() and not cat_dir.name.startswith('_'):
            candidate = cat_dir / identifier
            if candidate.exists() and (candidate / "SKILL.md").exists():
                return candidate

    return None


def find_all_skills():
    """Findet alle Skills in der Bibliothek."""
    skills = []
    for skill_md in SKILLS_ROOT.rglob("SKILL.md"):
        if '_templates' not in str(skill_md) and '_examples' not in str(skill_md):
            skills.append(skill_md.parent)
    return sorted(skills, key=lambda p: p.name)


def find_tracked_skills():
    """Find public skills from Git's index instead of local ignored content."""
    repo_root = SKILLS_ROOT.parent
    completed = subprocess.run(
        ['git', 'ls-files', '--', 'skills/**/SKILL.md'],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
    )
    skills = []
    for relative_file in completed.stdout.splitlines():
        skill_dir = (repo_root / relative_file).resolve().parent
        if (skill_dir / 'SKILL.md').is_file():
            skills.append(skill_dir)
    return sorted(set(skills), key=lambda p: str(p).lower())


def resolve_batch_skills(identifiers=None, tracked_only=False):
    """Resolve pre-commit file arguments or the complete requested inventory."""
    if not identifiers:
        return find_tracked_skills() if tracked_only else find_all_skills()

    skills = []
    for identifier in identifiers:
        candidate = Path(identifier)
        if candidate.is_file() and candidate.name == 'SKILL.md':
            skill_path = candidate.resolve().parent
        else:
            skill_path = find_skill(identifier)
        if not skill_path:
            raise ValueError(f"Skill nicht gefunden: {identifier}")
        skills.append(Path(skill_path).resolve())

    return sorted(set(skills), key=lambda p: str(p).lower())


# ---------------------------------------------------------------------------
# Hauptbefehle
# ---------------------------------------------------------------------------

def cmd_test(skill_identifier, profile_name='STANDARD', test_type=None):
    """Fuehrt Tests fuer einen Skill durch."""
    skill_path = find_skill(skill_identifier)
    if not skill_path:
        print(f"Skill nicht gefunden: {skill_identifier}")
        return None

    fm_text = (skill_path / "SKILL.md").read_text(encoding='utf-8', errors='replace')
    fm = parse_frontmatter(fm_text)
    name = fm.get('name', skill_path.name)

    profile = PROFILES.get(profile_name, PROFILES['STANDARD'])

    # Override profile by test_type
    if test_type == 'static':
        profile = PROFILES['STATIC']
    elif test_type == 'llm':
        profile = PROFILES['LLM_ONLY']
    elif test_type == 'user':
        profile = PROFILES['USER_ONLY']

    print(f"\n{'='*60}")
    print(f"  SKILL-TEST: {name}")
    try:
        rel_path = skill_path.resolve().relative_to(SKILLS_ROOT.resolve())
    except ValueError:
        rel_path = skill_path
    print(f"  Pfad: {rel_path}")
    print(f"  Profil: {profile_name}")
    print(f"  Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    s_results = {}
    l_results = {}
    u_results = {}

    # --- S-Tests ---
    if profile['s_tests']:
        print("--- S-TESTS (Statisch) ---\n")
        for test_id in profile['s_tests']:
            if test_id in S_TESTS:
                label, func = S_TESTS[test_id]
                score, detail = func(skill_path)
                s_results[test_id] = {'score': score, 'details': detail}
                status = "OK" if score >= 3 else "!!"
                print(f"  [{status}] {test_id} {label}: {score}/5  ({detail})")
        print()

    # --- L-Tests ---
    if profile['l_tests']:
        print("--- L-TESTS (LLM-Selbsterfahrung) ---\n")
        prompt = generate_l_test_prompt(skill_path)
        if prompt:
            prompt_file = RESULTS_DIR / f"{name}_l_test_prompt.md"
            prompt_file.write_text(prompt, encoding='utf-8')
            print(f"  L-Test Prompt generiert: {prompt_file.name}")
            print(f"  Fuehre diesen Prompt in einer separaten Claude-Session aus.")
            print(f"  Speichere das JSON-Ergebnis als: results/{name}_l_results.json")
            print()

            # Try to load existing L-results
            l_file = RESULTS_DIR / f"{name}_l_results.json"
            if l_file.exists():
                try:
                    l_data = json.loads(l_file.read_text(encoding='utf-8'))
                    for key, val in l_data.items():
                        if key.startswith('L') and isinstance(val, dict):
                            l_results[key.split('_')[0]] = val
                    print(f"  Vorhandene L-Ergebnisse geladen ({len(l_results)} Tests)")
                except json.JSONDecodeError:
                    print(f"  L-Ergebnisse nicht parsebar")
        print()

    # --- U-Tests ---
    if profile['u_tests']:
        u_results = run_u_tests_interactive(skill_path)

    # --- Scores ---
    dimensions = calculate_dimensions(s_results, l_results, u_results)
    quality = calculate_quality_score(s_results, l_results, u_results)

    print(f"\n{'='*60}")
    print(f"  ERGEBNIS: {name}")
    print(f"{'='*60}")

    if s_results:
        s_avg = sum(v['score'] for v in s_results.values()) / len(s_results)
        print(f"  S-Tests (Statisch):     {s_avg:.1f}/5")
    if l_results:
        l_avg = sum(v['score'] for v in l_results.values() if 'score' in v) / max(1, len([v for v in l_results.values() if 'score' in v]))
        print(f"  L-Tests (LLM):          {l_avg:.1f}/5")
    if u_results:
        u_scores = [v['score'] for v in u_results.values() if isinstance(v, dict) and 'score' in v]
        if u_scores:
            print(f"  U-Tests (User):         {sum(u_scores)/len(u_scores):.1f}/5")

    if dimensions:
        print(f"\n  Dimensionen:")
        dim_labels = {
            'd1_clarity': 'Klarheit',
            'd2_completeness': 'Vollstaendigkeit',
            'd3_independence': 'Unabhaengigkeit',
            'd4_effectiveness': 'Wirksamkeit',
            'd5_efficiency': 'Effizienz',
        }
        for key, val in dimensions.items():
            print(f"    {dim_labels.get(key, key)}: {val}/5")

    rating = "Exzellent" if quality >= 4 else "Gut" if quality >= 3 else "Akzeptabel" if quality >= 2 else "Mangelhaft" if quality >= 1 else "Unbrauchbar"
    print(f"\n  QUALITY SCORE: {quality}/5  ({rating})")
    print(f"{'='*60}\n")

    # --- Ergebnis speichern ---
    result = {
        'meta': {
            'skill': name,
            'skill_path': str(skill_path.relative_to(SKILLS_ROOT)),
            'tester': 'skill_tester.py',
            'date': datetime.now().isoformat(),
            'profile': profile_name,
            'version': fm.get('version', 'unknown'),
        },
        's_tests': s_results,
        'l_tests': l_results,
        'u_tests': {k: v for k, v in u_results.items() if not k.startswith('_')},
        'dimensions': dimensions,
        'quality_score': quality,
        'rating': rating,
    }

    result_dir = RESULTS_DIR / name
    result_dir.mkdir(parents=True, exist_ok=True)
    result_file = result_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    result_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"  Ergebnis gespeichert: {result_file.relative_to(SCRIPT_DIR)}")

    return result


def cmd_batch(profile_name='QUICK', test_type=None, ci_mode=False,
              identifiers=None):
    """Run static tests for all tracked or explicitly supplied skills."""
    if test_type not in (None, 'static'):
        print(f"Batch unterstuetzt nur --type static, nicht: {test_type}")
        return False

    profile = PROFILES['STATIC'] if test_type == 'static' else PROFILES.get(
        profile_name, PROFILES['QUICK'])
    effective_profile = 'STATIC' if test_type == 'static' else profile_name

    try:
        skills = resolve_batch_skills(
            identifiers=identifiers,
            tracked_only=ci_mode and not identifiers,
        )
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"Batch konnte Skills nicht bestimmen: {exc}")
        return False

    print(f"\nBatch-Test: {len(skills)} Skills mit Profil {effective_profile}\n")

    results = []
    for skill_path in skills:
        fm_text = (skill_path / "SKILL.md").read_text(encoding='utf-8', errors='replace')
        fm = parse_frontmatter(fm_text)
        name = fm.get('name', skill_path.name)

        s_results = {}
        for test_id in profile['s_tests']:
            if test_id in S_TESTS:
                label, func = S_TESTS[test_id]
                score, detail = func(skill_path)
                s_results[test_id] = {'score': score, 'details': detail}

        s_avg = sum(v['score'] for v in s_results.values()) / len(s_results)
        quality = s_avg  # Nur S-Tests im Batch
        gate_errors = frontmatter_gate_errors(skill_path)
        failed_tests = [
            test_id for test_id, value in s_results.items()
            if value['score'] < 3
        ]
        passed = not gate_errors and not failed_tests
        rating = "OK" if passed else "!!"

        try:
            rel = str(skill_path.relative_to(SKILLS_ROOT))
        except ValueError:
            rel = str(skill_path)
        print(f"  [{rating}] {name:30s} {quality:.1f}/5  ({rel})")
        for error in gate_errors:
            print(f"       Frontmatter: {error}")
        for test_id in failed_tests:
            print(f"       {test_id}: {s_results[test_id]['details']}")

        results.append({
            'skill': name,
            'path': rel,
            'quality': round(quality, 1),
            'passed': passed,
            'gate_errors': gate_errors,
            's_tests': s_results,
        })

    # Gesamtstatistik
    if results:
        avg = sum(r['quality'] for r in results) / len(results)
        good = sum(1 for r in results if r['passed'])
        print(f"\n  Gesamt: {avg:.1f}/5 Durchschnitt, {good}/{len(results)} bestanden")

    if not ci_mode:
        batch_file = RESULTS_DIR / f"batch_{datetime.now().strftime('%Y-%m-%d')}.json"
        batch_file.write_text(json.dumps({
            'date': datetime.now().isoformat(),
            'profile': effective_profile,
            'total': len(results),
            'average': round(avg, 1) if results else 0,
            'results': results,
        }, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"\n  Batch-Ergebnis: {batch_file.relative_to(SCRIPT_DIR)}")

    return bool(results) and all(result['passed'] for result in results)


def cmd_report(skill_identifier):
    """Zeigt den letzten Testbericht fuer einen Skill."""
    skill_path = find_skill(skill_identifier)
    if not skill_path:
        print(f"Skill nicht gefunden: {skill_identifier}")
        return

    fm_text = (skill_path / "SKILL.md").read_text(encoding='utf-8', errors='replace')
    fm = parse_frontmatter(fm_text)
    name = fm.get('name', skill_path.name)

    result_dir = RESULTS_DIR / name
    if not result_dir.exists():
        print(f"Keine Testergebnisse fuer '{name}'")
        return

    results = sorted(result_dir.glob("*.json"), reverse=True)
    if not results:
        print(f"Keine Testergebnisse fuer '{name}'")
        return

    latest = json.loads(results[0].read_text(encoding='utf-8'))
    print(json.dumps(latest, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0] in ('--help', '-h', 'help'):
        print(__doc__)
        return 0

    cmd = args[0]

    if cmd == 'test' and len(args) >= 2:
        skill = args[1]
        profile = 'STANDARD'
        test_type = None

        for i, a in enumerate(args[2:], 2):
            if a == '--profile' and i + 1 < len(args):
                profile = args[i + 1].upper()
            elif a == '--type' and i + 1 < len(args):
                test_type = args[i + 1].lower()

        cmd_test(skill, profile, test_type)
        return 0

    elif cmd == 'batch':
        profile = 'QUICK'
        test_type = None
        ci_mode = False
        identifiers = []
        index = 1
        while index < len(args):
            argument = args[index]
            if argument in ('--profile', '--type'):
                if index + 1 >= len(args):
                    print(f"Wert fehlt fuer {argument}")
                    return 2
                value = args[index + 1]
                if argument == '--profile':
                    profile = value.upper()
                else:
                    test_type = value.lower()
                index += 2
                continue
            if argument == '--ci':
                ci_mode = True
            elif argument.startswith('-'):
                print(f"Unbekannte Option: {argument}")
                return 2
            else:
                identifiers.append(argument)
            index += 1

        passed = cmd_batch(
            profile_name=profile,
            test_type=test_type,
            ci_mode=ci_mode,
            identifiers=identifiers or None,
        )
        return 0 if passed else 1

    elif cmd == 'report' and len(args) >= 2:
        cmd_report(args[1])
        return 0

    elif cmd == 'prompt' and len(args) >= 2:
        # Nur L-Test Prompt generieren
        skill_path = find_skill(args[1])
        if skill_path:
            prompt = generate_l_test_prompt(skill_path)
            if prompt:
                print(prompt)
        else:
            print(f"Skill nicht gefunden: {args[1]}")
            return 1
        return 0

    else:
        print(f"Unbekannter Befehl: {cmd}")
        print("Verfuegbar: test, batch, report, prompt")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
