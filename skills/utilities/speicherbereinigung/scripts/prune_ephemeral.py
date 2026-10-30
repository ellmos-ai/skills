#!/usr/bin/env python3
r"""Taeglicher Janitor fuer ephemere Arbeitsbereiche, die ihre Erzeuger nicht selbst aufraeumen.

Anlass (2026-10-25): Agenten-Reviews legten je PR eine Vollkopie (git clone --bare --no-hardlinks)
unter <local_dev>\reviews ab (~130 Ordner/Tag), %TEMP% hielt 45 GB Altdateien, C: lief auf 0 GB.
Die Windows-Speicheroptimierung war aktiv und hat %TEMP% trotzdem nicht erfasst.

(1) Review-Sandboxen  <local_dev>\<review_dir>\<name>, aelter als --review-hours (Default 24).
    Behalten werden: LOCK*-Datei (Tiefe <= 2), Unterordner juenger als die Grenze, Reparse-Points,
    Arbeitsklone mit uncommitteten Aenderungen oder Stash und jeder Klon bzw. jedes Bare-Repo,
    dessen Branch-Tips nicht im kanonischen Klon erreichbar sind (Ende der origin-Kette ausserhalb
    der Review-Wurzel; endet sie bei einer Remote-URL, bleibt der Ordner stehen).
(2) %TEMP%-Eintraege der ersten Ebene, aelter als --temp-days (Default 7); 'claude' ausgenommen.

DEFAULT = DRY-RUN. --apply loescht endgueltig (long-path-sicher). --selftest prueft die Regeln.
Konfiguration wie clean_build_junk.py ($BUILD_JUNK_CONFIG oder ~/.config/build-junk/config.json):
  "local_dev" (Pflicht fuer Teil 1), optional "review_dirs": ["reviews"].
Log: <local_dev>\_janitor_ephemeral.log (bzw. neben der Konfiguration).
"""
import os
import re
import shutil
import stat
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clean_build_junk import CONFIG, LOCAL_DEV, LOG_DIR  # noqa: E402
from clean_flutter_builds import purge_dir  # noqa: E402

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
PIP_HOURS = 6


def git(path, *args):
    r = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300, creationflags=NO_WINDOW)
    return r.stdout.split() if r.returncode == 0 else []


def is_reparse(path):
    try:
        return bool(os.lstat(path).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (OSError, AttributeError):
        return False


def walk_depth(root, depth=2):
    """(Pfad, Namen) bis Tiefe `depth` unterhalb von root, ohne in .git abzusteigen."""
    stack = [(root, 0)]
    while stack:
        p, d = stack.pop()
        try:
            names = os.listdir(p)
        except OSError:
            continue
        yield p, names
        if d < depth:
            stack += [(os.path.join(p, n), d + 1) for n in names
                      if n != ".git" and os.path.isdir(os.path.join(p, n)) and not is_reparse(os.path.join(p, n))]


def canon_of(repo, review_root):
    for _ in range(8):
        url = (git(repo, "config", "--get", "remote.origin.url") or [""])[0].replace("/", "\\")
        if not re.match(r"^[A-Za-z]:\\", url) or not os.path.isdir(url):
            return None  # Remote-URL oder verschwunden: kein lokaler Beleg
        if not os.path.normcase(url).startswith(os.path.normcase(review_root) + "\\"):
            return url
        repo = url
    return None


def review_verdict(full, review_root, cutoff, reach):
    """None = loeschbar, sonst Grund fuers Behalten."""
    if is_reparse(full):
        return "reparse"
    if os.path.getmtime(full) > cutoff:
        return "jung"
    repos = []
    for i, (p, names) in enumerate(walk_depth(full)):
        if i == 0 and any(os.path.isdir(os.path.join(p, n)) and os.path.getmtime(os.path.join(p, n)) > cutoff
                          for n in names):
            return "jung-unterordner"
        if any(n.startswith("LOCK") and os.path.isfile(os.path.join(p, n)) for n in names):
            return "lock"
        if ".git" in names:
            repos.append((p, False))
        elif p.endswith(".git") and "HEAD" in names and "objects" in names:
            repos.append((p, True))
    for repo, bare in repos:
        if not bare and git(repo, "status", "--porcelain"):
            return f"dirty:{repo}"
        if git(repo, "stash", "list"):
            return f"stash:{repo}"
        canon = canon_of(repo, review_root)
        if not canon:
            return f"kein-kanon:{repo}"
        if canon not in reach:
            reach[canon] = set(git(canon, "rev-list", "--all"))
        tips = git(repo, "for-each-ref", "--format=%(objectname)", "refs/heads") + git(repo, "rev-parse", "HEAD")
        if any(t not in reach[canon] for t in tips):
            return f"fehlt-im-kanon:{repo}"
    return None


def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)  # schnell; robocopy nur fuer Long-Path-Reste
        if os.path.isdir(path):
            purge_dir(path)
        try:
            os.rmdir(path)
        except OSError:
            pass
    else:
        try:
            os.remove(path)
        except OSError:
            pass
    return not os.path.exists(path)


def prune_reviews(review_root, hours, apply, out):
    cutoff, reach, kept = time.time() - hours * 3600, {}, {}
    gone = 0
    for name in sorted(os.listdir(review_root)):
        full = os.path.join(review_root, name)
        if not os.path.isdir(full):
            continue
        why = review_verdict(full, review_root, cutoff, reach)
        if why is None:
            if not apply or remove(full):
                gone += 1
                out(f"  [review] {'geloescht' if apply else 'wuerde loeschen'}: {name}")
                continue
            why = "nicht-loeschbar"
        kept[why.split(":")[0]] = kept.get(why.split(":")[0], 0) + 1
    out(f"[review] {review_root}: {gone} {'geloescht' if apply else 'loeschbar'}, behalten {kept}")


def prune_temp(temp, days, apply, out):
    # pip-Reste (pip-unpack/-metadata/-build-tracker ...) bleiben nur liegen, wenn pip abgebrochen wurde;
    # kein pip-Lauf dauert 6 h. Anlass: ~88 liegengebliebene claude_agent_sdk-Wheels (je 0,13 GB).
    now, n, rest = time.time(), 0, 0
    for name in os.listdir(temp):
        full = os.path.join(temp, name)
        cutoff = now - (PIP_HOURS * 3600 if name.startswith("pip-") else days * 86400)
        try:
            if name.lower() == "claude" or is_reparse(full) or os.path.getmtime(full) > cutoff:
                continue
        except OSError:
            continue
        n += 1
        if apply and not remove(full):
            rest += 1  # in Benutzung
    out(f"[temp] {temp}: {n} Eintraege aelter als {days} Tage {'entfernt' if apply else 'gefunden'}"
        + (f", {rest} in Benutzung" if apply else ""))


def free_gb(path):
    import shutil
    return shutil.disk_usage(path).free / 1024 ** 3


def selftest():
    import tempfile
    base = tempfile.mkdtemp(prefix="prune_selftest_")
    rv, tp = os.path.join(base, "reviews"), os.path.join(base, "temp")
    old = time.time() - 3 * 86400

    def mk(*parts, file=None):
        p = os.path.join(*parts)
        os.makedirs(p, exist_ok=True)
        if file:
            open(os.path.join(p, file), "w").close()
        return p

    def run(*a, cwd):
        subprocess.run(a, cwd=cwd, capture_output=True, check=True, creationflags=NO_WINDOW)

    canon = mk(base, "canon")
    run("git", "init", "-q", cwd=canon)
    run("git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "c", cwd=canon)
    mk(rv, "evidence", file="ci.json")
    mk(rv, "locked", "sub", file="LOCK.txt")
    mk(rv, "young", file="x")
    run("git", "clone", "-q", canon, os.path.join(rv, "clean", "source"), cwd=base)
    run("git", "clone", "-q", canon, os.path.join(rv, "dirty", "source"), cwd=base)
    open(os.path.join(rv, "dirty", "source", "neu.txt"), "w").close()
    for name in ("alt", "neu", "pip-unpack-8h", "pip-unpack-neu", "mittel-8h"):
        mk(tp, name, file="x")
    for p, _ in walk_depth(rv, 4):
        if not p.endswith("young"):
            os.utime(p, (old, old))
    h8 = time.time() - 8 * 3600
    for name, ts in (("alt", old), ("pip-unpack-8h", h8), ("mittel-8h", h8)):
        os.utime(os.path.join(tp, name), (ts, ts))
    prune_reviews(rv, 24, True, lambda _: None)
    prune_temp(tp, 1, True, lambda _: None)
    left = sorted(os.listdir(rv)), sorted(os.listdir(tp))
    purge_dir(base)
    assert left == (["dirty", "locked", "young"], ["mittel-8h", "neu", "pip-unpack-neu"]), left
    print("selftest ok")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    log_path = os.path.join(LOG_DIR, "_janitor_ephemeral.log")
    if sys.stdout is None:  # pythonw / Scheduled Task
        os.makedirs(LOG_DIR, exist_ok=True)
        sys.stdout = sys.stderr = open(log_path, "a", encoding="utf-8")
    raw = sys.argv[1:]
    apply = "--apply" in raw

    def opt(name, default):
        return int(raw[raw.index(name) + 1]) if name in raw else default

    out = print
    out(f"\n== prune_ephemeral {time.strftime('%Y-%m-%d %H:%M')} {'[APPLY]' if apply else '[DRY-RUN]'}"
        f"  frei {free_gb(os.environ.get('SystemDrive', 'C:') + os.sep):.1f} GB")
    if LOCAL_DEV:
        for rd in CONFIG.get("review_dirs", ["reviews"]):
            root = os.path.join(LOCAL_DEV, rd)
            if os.path.isdir(root):
                prune_reviews(root, opt("--review-hours", 24), apply, out)
    else:
        out("[review] uebersprungen: local_dev fehlt in der Konfiguration")
    temp = os.environ.get("TEMP") or os.environ.get("TMP")
    if temp and os.path.isdir(temp):
        prune_temp(temp, opt("--temp-days", 7), apply, out)
    out(f"== Ende, frei {free_gb(os.environ.get('SystemDrive', 'C:') + os.sep):.1f} GB")


if __name__ == "__main__":
    main()
