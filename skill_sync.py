#!/usr/bin/env python3
"""Skill Sync -- Deploy-/Drift-Tool zwischen Repo (Quelle der Wahrheit) und Deployment.

Quelle:     skills/<kategorie>/<skill-name>/   (dieses Repo, kategorisiert)
Deployment: ~/.claude/skills/<skill-name>/     (Claude-Code-Runtime, flach)

Befehle:
    status              Drift-Report (OK / abweichend / nur-Quelle / nur-Ziel)
    deploy [skill ...]  Quelle -> Ziel kopieren (ohne Argumente: alle abweichenden,
                        die im Ziel schon existieren; Erstinstallation nur mit Namen)
    diff <skill>        Unified-Diff eines Skills

Besonderheiten:
- Deregistrierte Skills: Im Deployment kann SKILL.md bewusst zu CONTENT.md
  umbenannt sein (Skill wird von der Runtime nicht geladen, Inhalt bleibt per
  Read-Tool nutzbar). Der Sync erkennt das und erhaelt die Deregistrierung
  beim Deploy (SKILL*.md wird als CONTENT*.md abgelegt).
- Hold-Liste: <deployment>/.sync-hold (eine Skill-Zeile pro Zeile, # = Kommentar)
  markiert Skills, deren Deployment-Version bewusst lokal abweicht. Sie werden
  beim Sammel-Deploy uebersprungen; explizites Deploy braucht --force.
- Branch-Awareness: Skills, deren SKILL.md im Frontmatter `provenance.origin: branch`
  enthaelt (Fremdskill-Fork) ODER deren Body den Marker `<!-- FAMILY-ROUTER:` traegt
  (Head-Router-Branch), werden automatisch wie HOLD behandelt: beim Sammel-Deploy
  uebersprungen, beim namentlichen Deploy nur mit --force ueberschreibbar. Status-
  Ausgabe zeigt [BRANCH:<grund>]-Label; Zusammenfassung zaehlt gebranchte Skills.
- Nur-Ziel-Skills werden NIE geloescht, nur gemeldet.
- Runtime-Dateien (PRESERVE_TARGET_FILES, z.B. config.json) leben per Design nur
  im Ziel und werden beim Deploy erhalten (keep) statt geprunt.
"""

import argparse
import difflib
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

SOURCE_ROOT = Path(__file__).parent / "skills"
TARGET_ROOT = Path.home() / ".claude" / "skills"
HOLD_FILENAME = ".sync-hold"
IGNORE_DIRS = {"__pycache__", ".git"}
# Runtime-Dateien, die das Deployment selbst erzeugt/pflegt und die per Design nur
# im Ziel leben (nicht aus der Quelle stammen). Sie werden beim Deploy NICHT geprunt,
# sonst geht persistierter Laufzeit-Zustand verloren (z.B. skill-explorer/config.json).
PRESERVE_TARGET_FILES = {"config.json"}

# Windows Encoding Fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# ─── Status-Konstanten ───

ST_OK = "OK"
ST_DRIFT = "ABWEICHEND"
ST_SOURCE_ONLY = "NUR-QUELLE"
ST_TARGET_ONLY = "NUR-ZIEL"


@dataclass
class SkillStatus:
    name: str
    category: str | None  # None bei NUR-ZIEL
    status: str
    deregistered: bool = False
    on_hold: bool = False
    branched: bool = False
    branch_reason: str = ""
    changed: list[str] = field(default_factory=list)      # Dateien mit Inhalts-Diff
    source_only: list[str] = field(default_factory=list)  # Dateien nur in Quelle
    target_only: list[str] = field(default_factory=list)  # Dateien nur im Ziel
    note: str = ""


# ─── Mapping Quelle (kategorisiert) -> flacher Skill-Name ───


def build_mapping(source_root: Path) -> dict[str, Path]:
    """Skill-Name -> Quell-Ordner. Kategorien = Unterordner von skills/.

    Wirft ValueError bei Namens-Kollision (gleicher Skill-Name in zwei Kategorien),
    da das Deployment-Ziel flach ist und der Name dort eindeutig sein muss.
    """
    mapping: dict[str, Path] = {}
    if not source_root.is_dir():
        return mapping
    for category in sorted(source_root.iterdir()):
        if not category.is_dir() or category.name.startswith("_"):
            continue
        for skill_dir in sorted(category.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
                continue
            name = skill_dir.name
            if name in mapping:
                raise ValueError(
                    f"Skill-Namens-Kollision: '{name}' existiert in "
                    f"'{mapping[name].parent.name}/' UND '{category.name}/'. "
                    f"Das flache Deployment-Ziel braucht eindeutige Namen."
                )
            mapping[name] = skill_dir
    return mapping


def read_hold_list(target_root: Path) -> set[str]:
    """Liest die Hold-Liste (bewusst lokal abweichende Skills) aus dem Deployment."""
    hold_file = target_root / HOLD_FILENAME
    if not hold_file.is_file():
        return set()
    names = set()
    for line in hold_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            names.add(line)
    return names


# ─── Datei-Ebene: Deregistrierung + Vergleich ───


def is_deregistered(target_dir: Path) -> bool:
    """Deregistriert = Ziel hat CONTENT.md, aber keine SKILL.md."""
    return (target_dir / "CONTENT.md").is_file() and not (target_dir / "SKILL.md").is_file()


def detect_branch(target_dir: Path) -> "str | None":
    """Prueft ob ein lokaler Skill gebrancht ist (Fremd-Fork oder Router-Branch).

    Liest die SKILL.md (bzw. CONTENT.md bei deregistrierten Skills) des Ziel-Verzeichnisses.
    Gitbt einen Grund-String zurueck:
      'fork'        -- Frontmatter enthaelt 'origin: branch' (Fremdskill-Fork)
      'router'      -- Body enthaelt '<!-- FAMILY-ROUTER:' (Head-Router-Branch)
      'fork+router' -- beides
      None          -- nicht gebrancht

    Robust gegen fehlende Dateien und Encoding-Fehler (errors='ignore').
    """
    if not target_dir.is_dir():
        return None

    # Skill-Datei bestimmen (SKILL.md bevorzugt, CONTENT.md als Fallback)
    skill_file = target_dir / "SKILL.md"
    if not skill_file.is_file():
        skill_file = target_dir / "CONTENT.md"
    if not skill_file.is_file():
        return None

    try:
        text = skill_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None

    # ── Fork-Erkennung: origin: branch IM FRONTMATTER ──
    is_fork = False
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        # Frontmatter: alles zwischen dem ersten und zweiten '---'
        in_frontmatter = False
        for line in lines:
            stripped = line.strip()
            if stripped == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break  # Ende Frontmatter
            if in_frontmatter and stripped.startswith("origin:"):
                value = stripped[len("origin:"):].strip().strip('"').strip("'")
                if value == "branch":
                    is_fork = True
                break

    # ── Router-Erkennung: FAMILY-ROUTER-Marker IM GESAMTEN TEXT ──
    is_router = "<!-- FAMILY-ROUTER:" in text

    if is_fork and is_router:
        return "fork+router"
    if is_fork:
        return "fork"
    if is_router:
        return "router"
    return None


def map_filename(rel_path: str, deregistered: bool) -> str:
    """Bildet einen Quell-Dateinamen auf den Ziel-Dateinamen ab.

    Bei deregistrierten Skills: SKILL.md -> CONTENT.md, SKILL.en.md -> CONTENT.en.md
    (nur auf oberster Ebene des Skill-Ordners).
    """
    if not deregistered or "/" in rel_path:
        return rel_path
    if rel_path == "SKILL.md" or (rel_path.startswith("SKILL.") and rel_path.endswith(".md")):
        return "CONTENT" + rel_path[len("SKILL"):]
    return rel_path


def list_files(root: Path) -> list[str]:
    """Alle Dateien unter root als relative POSIX-Pfade (ohne Ignore-Ordner)."""
    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root)
            if any(part in IGNORE_DIRS for part in rel.parts):
                continue
            files.append(rel.as_posix())
    return files


def files_equal(a: Path, b: Path) -> bool:
    try:
        if a.stat().st_size != b.stat().st_size:
            return False
        return a.read_bytes() == b.read_bytes()
    except OSError:
        return False


def compare_skill(name: str, source_dir: Path, target_root: Path) -> SkillStatus:
    """Vergleicht einen Quell-Skill mit seinem Deployment-Ordner."""
    category = source_dir.parent.name
    target_dir = target_root / name
    if not target_dir.is_dir():
        return SkillStatus(name, category, ST_SOURCE_ONLY)

    dereg = is_deregistered(target_dir)
    src_files = list_files(source_dir)
    dst_files = list_files(target_dir)

    expected = {map_filename(f, dereg): f for f in src_files}
    st = SkillStatus(name, category, ST_OK, deregistered=dereg)

    for dst_name, src_name in expected.items():
        dst_path = target_dir / dst_name
        if not dst_path.is_file():
            st.source_only.append(src_name)
        elif not files_equal(source_dir / src_name, dst_path):
            st.changed.append(src_name)

    for f in dst_files:
        if f not in expected:
            st.target_only.append(f)

    if st.changed or st.source_only or st.target_only:
        st.status = ST_DRIFT
    return st


def scan(source_root: Path, target_root: Path) -> list[SkillStatus]:
    """Vollstaendiger Drift-Scan: Quelle und Ziel in beide Richtungen."""
    mapping = build_mapping(source_root)
    hold = read_hold_list(target_root)
    results = []

    for name, src_dir in mapping.items():
        st = compare_skill(name, src_dir, target_root)
        st.on_hold = name in hold
        if st.status != ST_SOURCE_ONLY:
            branch_reason = detect_branch(target_root / name)
            if branch_reason:
                st.branched = True
                st.branch_reason = branch_reason
        results.append(st)

    # Nur-Ziel-Skills (nie loeschen, nur melden)
    if target_root.is_dir():
        for entry in sorted(target_root.iterdir()):
            if entry.name.startswith(".") or entry.name in mapping:
                continue
            if entry.is_dir():
                st = SkillStatus(entry.name, None, ST_TARGET_ONLY)
                branch_reason = detect_branch(entry)
                if branch_reason:
                    st.branched = True
                    st.branch_reason = branch_reason
                results.append(st)
            elif entry.is_symlink() or not entry.exists():
                # Auch Git-Bash-/Cygwin-Symlinks, die Windows-Python nicht als
                # Symlink erkennt (is_symlink() False, exists() False)
                results.append(SkillStatus(
                    entry.name, None, ST_TARGET_ONLY, note="defekter Symlink/Eintrag"))
    return results


# ─── Deploy ───


def deploy_skill(name: str, source_dir: Path, target_root: Path,
                 dry_run: bool = False) -> list[str]:
    """Kopiert einen Skill-Ordner Quelle -> Ziel. Erhaelt Deregistrierung.

    Gibt die Liste der durchgefuehrten (bzw. bei dry_run: geplanten) Aktionen zurueck.
    """
    target_dir = target_root / name
    dereg = target_dir.is_dir() and is_deregistered(target_dir)
    src_files = list_files(source_dir)
    expected = {map_filename(f, dereg): f for f in src_files}
    actions = []

    for dst_name, src_name in expected.items():
        src_path = source_dir / src_name
        dst_path = target_dir / dst_name
        if dst_path.is_file() and files_equal(src_path, dst_path):
            continue
        verb = "update" if dst_path.is_file() else "copy  "
        rename = f"  (aus {src_name}, Deregistrierung erhalten)" if dst_name != src_name else ""
        actions.append(f"{verb} {name}/{dst_name}{rename}")
        if not dry_run:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)

    # Veraltete Dateien im Ziel entfernen (Quelle der Wahrheit = Repo).
    # Ausnahme: Runtime-Dateien (PRESERVE_TARGET_FILES) leben per Design nur im Ziel
    # und werden erhalten statt geprunt (sonst Verlust von persistiertem Zustand).
    if target_dir.is_dir():
        for f in list_files(target_dir):
            if f not in expected:
                if Path(f).name in PRESERVE_TARGET_FILES:
                    actions.append(f"keep   {name}/{f}  (Runtime-Datei, nicht geprunt)")
                    continue
                actions.append(f"prune  {name}/{f}")
                if not dry_run:
                    (target_dir / f).unlink()

    return actions


# ─── Befehle ───


def _label(st: SkillStatus) -> str:
    label = st.status
    if st.on_hold:
        label += " [HOLD]"
    if st.branched:
        label += f" [BRANCH:{st.branch_reason}]"
    if st.deregistered:
        label += " [dereg]"
    return label


def cmd_status(args, source_root: Path = None, target_root: Path = None):
    source_root = source_root or SOURCE_ROOT
    target_root = target_root or TARGET_ROOT
    results = scan(source_root, target_root)

    drift = [r for r in results if r.status == ST_DRIFT]
    print(f"\nQuelle:  {source_root}")
    print(f"Ziel:    {target_root}\n")
    print(f"{'Skill':<32} {'Kategorie':<15} {'Status':<24} Details")
    print("─" * 100)
    for r in results:
        if r.status == ST_OK and not args.all:
            continue
        details = []
        if r.changed:
            details.append(f"{len(r.changed)} geaendert")
        if r.source_only:
            details.append(f"{len(r.source_only)} nur Quelle")
        if r.target_only:
            details.append(f"{len(r.target_only)} nur Ziel")
        if r.note:
            details.append(r.note)
        print(f"  {r.name:<30} {r.category or '-':<15} {_label(r):<24} {', '.join(details)}")

    ok = sum(1 for r in results if r.status == ST_OK)
    src_only = sum(1 for r in results if r.status == ST_SOURCE_ONLY)
    dst_only = sum(1 for r in results if r.status == ST_TARGET_ONLY)
    branched_count = sum(1 for r in results if r.branched)
    print("─" * 100)
    print(f"  {len(results)} Skills: {ok} OK, {len(drift)} abweichend, "
          f"{src_only} nur Quelle, {dst_only} nur Ziel, {branched_count} gebrancht"
          + ("" if args.all else "   (OK-Zeilen ausgeblendet, --all zeigt alle)"))
    print()


def cmd_deploy(args, source_root: Path = None, target_root: Path = None):
    source_root = source_root or SOURCE_ROOT
    target_root = target_root or TARGET_ROOT
    mapping = build_mapping(source_root)
    hold = read_hold_list(target_root)

    if args.skills:
        names = []
        for n in args.skills:
            if n not in mapping:
                print(f"FEHLER: Skill '{n}' nicht in der Quelle gefunden.")
                sys.exit(1)
            # Branch-Check: detect_branch liest das Ziel-Verzeichnis direkt
            branch_reason = detect_branch(target_root / n)
            if branch_reason and not args.force:
                print(f"UEBERSPRUNGEN (BRANCH:{branch_reason}): '{n}' ist lokal gebrancht "
                      f"(nicht ueberschrieben). Deploy erzwingen mit --force.")
                continue
            if n in hold and not args.force:
                print(f"UEBERSPRUNGEN (HOLD): '{n}' ist als bewusst lokal abweichend "
                      f"markiert ({target_root / HOLD_FILENAME}). Deploy mit --force.")
                continue
            names.append(n)
    else:
        # Alle abweichenden Skills, die in BEIDEN Seiten existieren (ohne HOLD/BRANCH).
        # NUR-QUELLE-Skills werden bewusst NICHT automatisch deployt -- das
        # Deployment ist eine kuratierte Auswahl. Erstinstallation nur mit
        # explizitem Namen: python skill_sync.py deploy <skill>
        names = []
        for st in scan(source_root, target_root):
            if st.status != ST_DRIFT or st.category is None:
                continue
            if st.branched:
                print(f"UEBERSPRUNGEN (BRANCH:{st.branch_reason}): {st.name}")
                continue
            if st.on_hold:
                print(f"UEBERSPRUNGEN (HOLD): {st.name}")
                continue
            names.append(st.name)

    if not names:
        print("Nichts zu deployen.")
        return

    prefix = "[DRY-RUN] " if args.dry_run else ""
    total_actions = 0
    for name in names:
        actions = deploy_skill(name, mapping[name], target_root, dry_run=args.dry_run)
        if actions:
            print(f"\n{prefix}{name}:")
            for a in actions:
                print(f"  {a}")
            total_actions += len(actions)
        else:
            print(f"\n{prefix}{name}: bereits aktuell")
    print(f"\n{prefix}{len(names)} Skill(s), {total_actions} Datei-Aktion(en)."
          + (" KEINE Dateien geschrieben." if args.dry_run else ""))


def cmd_diff(args, source_root: Path = None, target_root: Path = None):
    source_root = source_root or SOURCE_ROOT
    target_root = target_root or TARGET_ROOT
    mapping = build_mapping(source_root)
    name = args.skill
    if name not in mapping:
        print(f"FEHLER: Skill '{name}' nicht in der Quelle gefunden.")
        sys.exit(1)

    st = compare_skill(name, mapping[name], target_root)
    if st.status == ST_SOURCE_ONLY:
        print(f"'{name}' existiert nur in der Quelle (noch nie deployt).")
        return
    if st.status == ST_OK:
        print(f"'{name}' ist identisch (OK)." + (" [dereg]" if st.deregistered else ""))
        return

    source_dir = mapping[name]
    target_dir = target_root / name
    for src_name in st.changed:
        dst_name = map_filename(src_name, st.deregistered)
        src_path, dst_path = source_dir / src_name, target_dir / dst_name
        try:
            dst_lines = dst_path.read_text(encoding="utf-8").splitlines(keepends=True)
            src_lines = src_path.read_text(encoding="utf-8").splitlines(keepends=True)
        except UnicodeDecodeError:
            print(f"--- {name}/{dst_name} (binaer, kein Text-Diff)")
            continue
        diff = difflib.unified_diff(
            dst_lines, src_lines,
            fromfile=f"deployment/{name}/{dst_name}",
            tofile=f"quelle/{st.category}/{name}/{src_name}",
        )
        sys.stdout.writelines(diff)
        print()
    for f in st.source_only:
        print(f"+ nur in Quelle:  {name}/{f}")
    for f in st.target_only:
        print(f"- nur im Ziel:    {name}/{f}")


# ─── Main ───


def main():
    parser = argparse.ArgumentParser(
        description="Skill Sync -- Repo (Quelle) -> ~/.claude/skills (Deployment)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Verfuegbare Befehle")

    p_status = sub.add_parser("status", help="Drift-Report anzeigen")
    p_status.add_argument("--all", "-a", action="store_true",
                          help="Auch identische (OK) Skills anzeigen")

    p_deploy = sub.add_parser("deploy", help="Skills Quelle -> Ziel kopieren")
    p_deploy.add_argument("skills", nargs="*",
                          help="Skill-Namen (ohne Argumente: alle abweichenden)")
    p_deploy.add_argument("--dry-run", "-n", action="store_true",
                          help="Nur anzeigen, nichts kopieren")
    p_deploy.add_argument("--force", "-f", action="store_true",
                          help="Auch HOLD-markierte Skills deployen (nur mit explizitem Namen)")

    p_diff = sub.add_parser("diff", help="Unified-Diff eines Skills")
    p_diff.add_argument("skill", help="Skill-Name")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "deploy":
        cmd_deploy(args)
    elif args.command == "diff":
        cmd_diff(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
