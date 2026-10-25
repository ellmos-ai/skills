#!/usr/bin/env python3
r"""Generischer Build-/Scratch-Muell-Janitor fuer .SOFTWARE (OneDrive) + lokale Arbeitsordner.

Hintergrund: .gitignore stoppt OneDrive NICHT — OneDrive synchronisiert auch ignorierte
Build-Artefakte. Daher muss Build-/Scratch-Muell physisch entfernt werden.

Bereiche:
  (A) OneDrive .SOFTWARE  [--onedrive, Default]
      - Immer entfernt: __pycache__, .pytest_cache, .mypy_cache, .ruff_cache, *.egg-info
      - build/ + dist/ NUR wenn ein Python-Build-Marker im selben Ordner liegt
        (setup.py / pyproject.toml / *.spec / build_exe.bat) -> sicher als Build-Output erkannt
      - Flutter-Caches (build/.dart_tool/android/.gradle) via clean_flutter_builds
  (B) Lokale Arbeitsordner  [--local]  (nur wenn "local_dev" in der Konfiguration steht)
      - Alters-basiertes Pruning ephemerer Ordner (Name-Muster "prune_globs") aelter als --days
        (Default 21); "protect" nennt Ordner, die nie angefasst werden.
      - Konfiguration: $BUILD_JUNK_CONFIG oder ~/.config/build-junk/config.json
        {"local_dev": "...", "prune_globs": [...], "protect": [...], "software_root": "..."}
      - Ohne Konfiguration wird (B) uebersprungen und gemeldet.

DEFAULT = DRY-RUN (zeigt nur). Mit --apply wird wirklich geloescht. Long-path-sicher.

Nutzung:
  python scripts/clean_build_junk.py                 # dry-run, OneDrive .SOFTWARE
  python scripts/clean_build_junk.py --apply         # echt, OneDrive
  python scripts/clean_build_junk.py --local --apply --days 21
  python scripts/clean_build_junk.py --all --apply   # OneDrive + Flutter + Local (fuer Scheduled Task)
"""
import fnmatch
import json
import os
import sys
import time

# Long-path-sichere Loeschung + Flutter-Logik wiederverwenden (gleicher scripts/-Ordner)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clean_flutter_builds import (  # noqa: E402
    CACHE_DIRS as FL_CACHE,
)
from clean_flutter_builds import (
    GRADLE_REL,
    default_software_root,
    find_flutter_roots,
    purge_dir,
)

CONFIG_FILE = os.environ.get("BUILD_JUNK_CONFIG") or os.path.join(
    os.path.expanduser("~"), ".config", "build-junk", "config.json"
)


def _load_config():
    """Optionale Konfiguration ausserhalb des Skills (sie enthaelt private Ordnernamen)."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


CONFIG = _load_config()
SOFTWARE_ROOT = CONFIG.get("software_root") or default_software_root()
LOCAL_DEV = CONFIG.get("local_dev") or ""  # leer = lokales Pruning aus
LOG_DIR = LOCAL_DEV or os.path.dirname(CONFIG_FILE)
LOG_FILE = os.path.join(LOG_DIR, "_janitor_log.txt")

ALWAYS_CACHE = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EGG_GLOB = "*.egg-info"
BUILD_DIRS = {"build", "dist"}
BUILD_MARKERS = ("setup.py", "pyproject.toml", "build_exe.bat")  # + *.spec separat
SKIP_DESCEND = {".git", "node_modules", "build", "dist", ".dart_tool", ".gradle",
                "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}

# --- Lokales Pruning (nur mit "local_dev" in der Konfiguration) ---
LOCAL_PRUNE_GLOBS = list(CONFIG.get("prune_globs", []))
LOCAL_PROTECT = {str(x).lower() for x in CONFIG.get("protect", [])}


def _has_python_build_marker(d):
    if any(os.path.isfile(os.path.join(d, m)) for m in BUILD_MARKERS):
        return True
    try:
        return any(f.endswith(".spec") for f in os.listdir(d))
    except OSError:
        return False


def scan_onedrive(root):
    """Liefert Liste zu entfernender Cache-/Build-Ordner unter root."""
    targets = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Cache-Ordner selbst einsammeln, dann nicht weiter absteigen
        for d in list(dirnames):
            full = os.path.join(dirpath, d)
            if d in ALWAYS_CACHE or fnmatch.fnmatch(d, EGG_GLOB):
                targets.append(full)
            elif d in BUILD_DIRS and _has_python_build_marker(dirpath):
                targets.append(full)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DESCEND and d not in ALWAYS_CACHE]
    return targets


def scan_flutter(root):
    targets = []
    for fr in find_flutter_roots(root):
        for c in FL_CACHE:
            p = os.path.join(fr, c)
            if os.path.isdir(p):
                targets.append(p)
        g = os.path.join(fr, GRADLE_REL)
        if os.path.isdir(g):
            targets.append(g)
    return targets


def scan_local(local_root, days):
    """Ephemere C:\\_Local_DEV-Ordner aelter als `days` (mtime), nach Muster, nicht geschuetzt."""
    cutoff = time.time() - days * 86400
    out = []
    if not os.path.isdir(local_root):
        return out
    for name in os.listdir(local_root):
        full = os.path.join(local_root, name)
        if not os.path.isdir(full):
            continue
        if name.lower() in LOCAL_PROTECT:
            continue
        if not any(fnmatch.fnmatch(name, g) for g in LOCAL_PRUNE_GLOBS):
            continue
        try:
            if os.path.getmtime(full) > cutoff:
                continue  # zu jung
        except OSError:
            continue
        out.append(full)
    return out


def dir_mb(path):
    total = 0
    for dp, _dn, fn in os.walk(path):
        for f in fn:
            try:
                total += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass
    return total / 1024 / 1024


def process(label, targets, apply, rootlabel):
    freed = 0.0
    for t in targets:
        mb = dir_mb(t)
        freed += mb
        rel = t.replace(rootlabel, "").lstrip("\\/")
        print(f"  [{label}] {'[loesche]' if apply else '[wuerde loeschen]'} {rel}  ({mb:.1f} MB+)")
        if apply:
            purge_dir(t)
    return freed


def main():
    # Fensterlos (pythonw / Scheduled Task): kein Console-stdout -> in Task-Log umleiten
    if sys.stdout is None:
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            sys.stdout = sys.stderr = open(os.path.join(LOG_DIR, "_janitor_task.log"), "a", encoding="utf-8")
        except OSError:
            import io
            sys.stdout = sys.stderr = io.StringIO()
    raw = sys.argv[1:]
    apply = "--apply" in raw
    do_local = "--local" in raw or "--all" in raw
    do_onedrive = ("--onedrive" in raw) or ("--all" in raw) or not do_local or ("--apply" in raw and "--local" not in raw)
    # Default-Ziel = OneDrive, wenn nichts explizit gewaehlt
    if not any(x in raw for x in ("--onedrive", "--local", "--all")):
        do_onedrive, do_local = True, False
    days = 21
    for i, a in enumerate(raw):
        if a == "--days" and i + 1 < len(raw):
            try:
                days = int(raw[i + 1])
            except ValueError:
                pass

    print(f"clean_build_junk  {'[APPLY]' if apply else '[DRY-RUN]'}  onedrive={do_onedrive} local={do_local} days={days}")
    freed = 0.0
    n = 0

    if do_onedrive:
        py = scan_onedrive(SOFTWARE_ROOT)
        fl = scan_flutter(SOFTWARE_ROOT)
        # Flutter-build/ ueberschneidet sich nicht mit Python-build (Flutter-build hat keinen .spec-Marker)
        all_od = list(dict.fromkeys(py + fl))
        print(f"\n[OneDrive .SOFTWARE] {len(all_od)} Ordner (Python-Caches/Build + Flutter):")
        freed += process("OD", all_od, apply, SOFTWARE_ROOT)
        n += len(all_od)

    if do_local and not LOCAL_DEV:
        print(f"\n[lokal] uebersprungen: local_dev fehlt in {CONFIG_FILE}")
    elif do_local:
        loc = scan_local(LOCAL_DEV, days)
        print(f"\n[{LOCAL_DEV}] {len(loc)} ephemere Ordner aelter als {days}d:")
        freed += process("LOCAL", loc, apply, LOCAL_DEV)
        n += len(loc)

    verb = "entfernt" if apply else "(dry-run)"
    summary = f"Gesamt: {n} Ordner, mind. {freed:.0f} MB {verb}"
    print(f"\n{summary}")

    if apply:
        try:
            stamp = time.strftime("%Y-%m-%d %H:%M")
            with open(LOG_FILE, "a", encoding="utf-8") as fh:
                fh.write(f"{stamp} | clean_build_junk --all={do_local and do_onedrive} | {summary}\n")
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
