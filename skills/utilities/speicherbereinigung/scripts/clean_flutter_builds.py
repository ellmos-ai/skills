#!/usr/bin/env python3
"""Entfernt regenerierbare Flutter-/Gradle-Build-Caches aus OneDrive-Projektordnern.

Zielordner (relativ zur Flutter-Projektwurzel = Ordner mit pubspec.yaml):
  build/, .dart_tool/, android/.gradle/

Grund: Diese Caches enthalten extrem tiefe Pfade (z. B. .transforms/<hash>/.../*.globals),
die das Windows/OneDrive-Pfadlaengenlimit sprengen -> "Element kann nicht synchronisiert
werden, weil der Pfad zu lang ist". Sie sind reproduzierbar (Neubau via `flutter build`)
und gehoeren NIE in OneDrive (wie .venv / .git-Objekte).

Loeschung ist long-path-sicher via robocopy-Purge (umgeht MAX_PATH).

DEFAULT = DRY-RUN (zeigt nur). Geloescht wird erst mit ausdruecklichem --apply.
--dry-run wird weiter akzeptiert und ist wirkungslos (alter Aufruf, jetzt ohnehin Standard).

Nutzung:
  PYTHONIOENCODING=utf-8 python scripts/clean_flutter_builds.py [WURZEL] [--apply]

Default-WURZEL: $SOFTWARE_ROOT, sonst <OneDrive>/.TOPICS/.SOFTWARE (nicht der Skriptort).
Exit 0 = ok. Idempotent: wiederholter Lauf findet dann nichts mehr.
"""
import os
import shutil
import subprocess
import sys
import tempfile

CACHE_DIRS = ["build", ".dart_tool"]          # relativ zur Flutter-Projektwurzel
GRADLE_REL = os.path.join("android", ".gradle")
SKIP_DESCEND = {".dart_tool", "build", ".gradle", ".git", "node_modules", "__pycache__"}


def default_software_root():
    """$SOFTWARE_ROOT, sonst <OneDrive>/.TOPICS/.SOFTWARE; nie aus dem Skriptort abgeleitet."""
    env = os.environ.get("SOFTWARE_ROOT")
    if env:
        return env
    onedrive = os.environ.get("OneDrive") or os.path.join(os.path.expanduser("~"), "OneDrive")
    return os.path.join(onedrive, ".TOPICS", ".SOFTWARE")


def find_flutter_roots(root):
    """Alle Ordner mit pubspec.yaml (= Flutter-/Dart-Projektwurzeln) unter root."""
    roots = []
    for dirpath, dirnames, filenames in os.walk(root):
        if "pubspec.yaml" in filenames:
            roots.append(dirpath)
        # nicht in schwere/tiefe Caches absteigen (verhindert Long-Path-Walk)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DESCEND]
    return roots


def dir_size(path):
    total = 0
    for dp, _dn, fn in os.walk(path):
        for f in fn:
            try:
                total += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass  # zu langer Pfad o. Ae. -> ueberspringen (nur Reporting)
    return total


def purge_dir(path):
    """Long-path-sichere Loeschung: robocopy spiegelt ein leeres Verzeichnis -> /PURGE leert,
    danach wird die leere Huelle entfernt."""
    if not os.path.isdir(path):
        return
    empty = tempfile.mkdtemp(prefix="__empty_mirror_")
    try:
        subprocess.run(
            ["robocopy", empty, path, "/E", "/PURGE",
             "/NJH", "/NJS", "/NFL", "/NDL", "/NC", "/NS", "/R:1", "/W:1"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            # unter pythonw (Scheduled Task) oeffnet sonst JEDER Aufruf ein aufblitzendes Konsolenfenster
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    finally:
        shutil.rmtree(empty, ignore_errors=True)
    for _ in range(3):
        try:
            os.rmdir(path)
            break
        except OSError:
            shutil.rmtree(path, ignore_errors=True)
            if not os.path.isdir(path):
                break


def main():
    raw = sys.argv[1:]
    dry = "--apply" not in raw  # --dry-run ist nur noch ein Alias des Standards
    positional = [a for a in raw if not a.startswith("--")]
    root = positional[0] if positional else default_software_root()
    print(f"Wurzel: {root}{'  [DRY-RUN]' if dry else ''}")

    targets = []
    for fr in find_flutter_roots(root):
        for c in CACHE_DIRS:
            p = os.path.join(fr, c)
            if os.path.isdir(p):
                targets.append(p)
        g = os.path.join(fr, GRADLE_REL)
        if os.path.isdir(g):
            targets.append(g)

    total = 0
    for t in targets:
        sz = dir_size(t)
        total += sz
        rel = t.replace(root, "").lstrip("\\/")
        print(f"  {'[wuerde loeschen]' if dry else '[geloescht]'}  {rel}  ({sz / 1024 / 1024:.1f} MB+)")
        if not dry:
            purge_dir(t)

    verb = "(dry-run, nichts geloescht)" if dry else "entfernt"
    print(f"\nGesamt: {len(targets)} Cache-Ordner, mind. {total / 1024 / 1024:.1f} MB {verb}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
