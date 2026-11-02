#!/usr/bin/env python3
r"""Taeglicher Janitor fuer ephemere Arbeitsbereiche, die ihre Erzeuger nicht selbst aufraeumen.

Anlass (2026-10-25): Agenten-Reviews legten je PR eine Vollkopie (git clone --bare --no-hardlinks)
unter <local_dev>\reviews ab (~130 Ordner/Tag), %TEMP% hielt 45 GB Altdateien, C: lief auf 0 GB.
Die Windows-Speicheroptimierung war aktiv und hat %TEMP% trotzdem nicht erfasst.

(1) Review-Sandboxen  <local_dev>\<review_dir>\<name>, aelter als --review-hours (Default 24),
    oder sofort bei abgeschlossenem Review (closeout.json) bzw. abgelaufener Ablaufmarke
    (owner.json mit expires_at <= jetzt).
    Behalten werden:
    - echte Lock-Datei (LOCK.txt / LOCK.<scope>.txt wie lock_scan.py; Tiefe <= 2), Reparse-Points,
    - aktive Besitzer-/Ablaufmarke (owner.json mit expires_at in der Zukunft, sofern kein closeout.json),
    - Ordner/Unterordner juenger als die Grenze (sofern weder closeout.json noch abgelaufenes expires_at),
    - Arbeitsklone/Worktrees mit uncommitteten Aenderungen oder Stash,
    - jeder Klon bzw. jedes Bare-Repo, dessen Branch-Tips nicht im kanonischen Klon erreichbar sind
      (Ende der origin-/alternates-/worktree-Kette oder owner.json:canonical_repo ausserhalb der
      Review-Wurzel; endet sie bei einer Remote-URL ohne lokalen Kanon-Beleg, bleibt der Ordner stehen),
    - Ketten-Klon-Elternordner, solange ein abhaengiger Nachbar-Review-Ordner behalten wird.
(2) %TEMP%-Eintraege der ersten Ebene, aelter als --temp-days (Default 7); 'claude' ausgenommen.

DEFAULT = DRY-RUN. --apply loescht endgueltig (long-path-sicher). --selftest prueft die Regeln.
Konfiguration wie clean_build_junk.py ($BUILD_JUNK_CONFIG oder ~/.config/build-junk/config.json):
  "local_dev" (Pflicht fuer Teil 1), optional "review_dirs": ["reviews"].
Log: <local_dev>\_janitor_ephemeral.log (bzw. neben der Konfiguration).
"""
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clean_build_junk import CONFIG, LOCAL_DEV, LOG_DIR  # noqa: E402
from clean_flutter_builds import purge_dir  # noqa: E402

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
PIP_HOURS = 6
CLOSEOUT_KEYS = ("head", "url", "report", "closed_at", "completed_at", "sha256")
# Echte Lock-Dateien, dasselbe Muster wie lock_utils.LOCK_RE (lock_scan.py): LOCK.txt, LOCK.<scope>.txt, ...
# Dokumente wie LOCK-SYSTEM.md sind keine Locks.
LOCK_FILE_RE = re.compile(r"^LOCK(?:\.[A-Za-z0-9_-]+)*\.txt$", re.IGNORECASE)


def is_lock_file(name):
    return LOCK_FILE_RE.match(name) is not None


def git(path, *args):
    r = subprocess.run(["git", "-C", path, *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300, creationflags=NO_WINDOW)
    return r.stdout.split() if r.returncode == 0 else []


def is_reparse(path):
    try:
        return bool(os.lstat(path).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (OSError, AttributeError):
        return False


def is_direct_child(path, root):
    """Fail-closed containment: `path` is an existing directory sitting directly under the existing
    directory `root`.  False for empty arguments, a drive/filesystem root as `root`, reparse points
    (junction/symlink) as `path` or `root`, `root` itself and anything deeper."""
    if not path or not root or not os.path.isdir(path) or not os.path.isdir(root):
        return False
    if is_reparse(path) or is_reparse(root):
        return False
    real_path, real_root = (os.path.normcase(os.path.realpath(p)) for p in (path, root))
    if os.path.dirname(real_root) == real_root:
        return False
    return os.path.dirname(real_path) == real_root


def safe_review_roots(local_dev, review_dirs):
    """Review roots named by the configuration: only plain folder names directly under `local_dev`.
    Empty names, `.`/`..`, separators, drive letters and non-strings are ignored, so a bad
    `review_dirs` entry can never point the janitor at `local_dev` itself or outside of it."""
    if not local_dev:
        return []
    if isinstance(review_dirs, str):
        review_dirs = [review_dirs]
    if not isinstance(review_dirs, list):
        return []
    roots = []
    for name in review_dirs:
        if (isinstance(name, str) and name not in ("", ".", "..") and name == os.path.basename(name)
                and "/" not in name and "\\" not in name and ":" not in name):
            roots.append(os.path.join(local_dev, name))
    return roots


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


def _read_json_dict(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def parse_timestamp(val):
    """Parst Unix-Epoch (int/float/str) oder ISO-8601-Zeitstempel in Epoch-Sekunden."""
    if val is None or isinstance(val, bool):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str):
        return None
    s = val.strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        pass
    if s.endswith("Z") or s.endswith("z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except ValueError:
        return None


def read_owner_meta(full):
    """Liest owner.json einer Review-Sandbox (falls vorhanden)."""
    return _read_json_dict(os.path.join(full, "owner.json"))


def is_closed_out(full):
    """True, wenn eine gueltige closeout.json den Review-Abschluss belegt."""
    data = _read_json_dict(os.path.join(full, "closeout.json"))
    if not data:
        return False
    if data.get("status") in ("closed", "done", "completed"):
        return True
    return any(bool(data.get(k)) for k in CLOSEOUT_KEYS)


def _is_outside_review_root(candidate, review_root):
    if not candidate or not re.match(r"^[A-Za-z]:\\", candidate) or not os.path.isdir(candidate):
        return False
    norm_cand = os.path.normcase(os.path.abspath(candidate))
    norm_root = os.path.normcase(os.path.abspath(review_root))
    return norm_cand != norm_root and not norm_cand.startswith(norm_root + "\\")


def _is_git_repo_dir(path):
    if not path or not os.path.isdir(path):
        return False
    return os.path.exists(os.path.join(path, ".git")) or (
        os.path.isfile(os.path.join(path, "HEAD")) and os.path.isdir(os.path.join(path, "objects"))
    )


def _git_dir_of(repo, bare=False):
    if bare:
        return repo
    dotgit = os.path.join(repo, ".git")
    if os.path.isdir(dotgit):
        return dotgit
    if os.path.isfile(dotgit):
        try:
            with open(dotgit, encoding="utf-8", errors="replace") as fh:
                line = fh.readline().strip()
            if line.lower().startswith("gitdir:"):
                raw = line.split(":", 1)[1].strip().replace("/", "\\")
                return raw if os.path.isabs(raw) else os.path.abspath(os.path.join(repo, raw))
        except OSError:
            pass
    return None


def _is_linked_worktree(repo):
    """True for `git worktree add` checkouts: their git dir is <canon>/.git/worktrees/<id>."""
    gdir = _git_dir_of(repo)
    return bool(gdir) and os.path.basename(os.path.dirname(gdir)).lower() == "worktrees"


def _repo_from_git_or_objects_path(path):
    """Loest <repo>/.git/worktrees/<id>, <repo>/.git/objects oder <bare>/objects zum Repo-Pfad auf."""
    cur = os.path.abspath(path.replace("/", "\\"))
    for _ in range(5):
        base = os.path.basename(cur).lower()
        parent = os.path.dirname(cur)
        if base == ".git" and os.path.isdir(parent):
            return parent
        if _is_git_repo_dir(cur):
            return cur
        if parent == cur:
            break
        cur = parent
    return None


def _linked_local_repos(repo, bare=False):
    """Liefert direkte lokale Referenz-Repos (origin.url, worktree-commondir, alternates)."""
    refs = []
    url = (git(repo, "config", "--get", "remote.origin.url") or [""])[0].replace("/", "\\")
    if re.match(r"^[A-Za-z]:\\", url):
        refs.append(os.path.abspath(url))
    gdir = _git_dir_of(repo, bare)
    if gdir:
        # Worktree: <canon>/.git/worktrees/<name> -> commondir oder Eltern-.git
        common_file = os.path.join(gdir, "commondir")
        if os.path.isfile(common_file):
            try:
                with open(common_file, encoding="utf-8", errors="replace") as fh:
                    rel = fh.readline().strip().replace("/", "\\")
                cdir = rel if os.path.isabs(rel) else os.path.abspath(os.path.join(gdir, rel))
                resolved = _repo_from_git_or_objects_path(cdir)
                if resolved:
                    refs.append(resolved)
            except OSError:
                pass
        else:
            resolved = _repo_from_git_or_objects_path(gdir)
            if resolved and os.path.normcase(resolved) != os.path.normcase(os.path.abspath(repo)):
                refs.append(resolved)
        # Shared / Reference Clone: objects/info/alternates
        alt_file = os.path.join(gdir, "objects", "info", "alternates")
        if os.path.isfile(alt_file):
            try:
                with open(alt_file, encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        s = line.strip()
                        if not s or s.startswith("#"):
                            continue
                        cand = s.replace("/", "\\")
                        if not os.path.isabs(cand):
                            cand = os.path.abspath(os.path.join(gdir, "objects", cand))
                        resolved = _repo_from_git_or_objects_path(cand)
                        if resolved:
                            refs.append(resolved)
            except OSError:
                pass
    return refs


def canon_of(repo, review_root, owner_canon=None):
    visited = set()
    cur = repo
    for _ in range(8):
        norm_cur = os.path.normcase(os.path.abspath(cur))
        if norm_cur in visited:
            break
        visited.add(norm_cur)
        refs = _linked_local_repos(cur, bare=cur.endswith(".git") and not os.path.exists(os.path.join(cur, ".git")))
        next_in_review = None
        for target in refs:
            if not os.path.isdir(target):
                continue
            if _is_outside_review_root(target, review_root) and _is_git_repo_dir(target):
                return target
            if next_in_review is None:
                next_in_review = target
        if next_in_review is None:
            break
        cur = next_in_review
    if owner_canon:
        cand = os.path.abspath(str(owner_canon).replace("/", "\\"))
        if _is_outside_review_root(cand, review_root) and _is_git_repo_dir(cand):
            return cand
    return None


def _sandbox_repos(full):
    repos = []
    for p, names in walk_depth(full):
        if ".git" in names:
            repos.append((p, False))
        elif p.endswith(".git") and "HEAD" in names and "objects" in names:
            repos.append((p, True))
    return repos


def sandbox_dependencies(full, review_root):
    """Namen anderer Sandbox-Ordner unter review_root, auf die `full` direkt verweist."""
    norm_root = os.path.normcase(os.path.abspath(review_root))
    own_name = os.path.normcase(os.path.basename(os.path.abspath(full)))
    deps = set()
    for repo, bare in _sandbox_repos(full):
        for ref in _linked_local_repos(repo, bare):
            norm_ref = os.path.normcase(os.path.abspath(ref))
            if norm_ref.startswith(norm_root + "\\"):
                rel = os.path.abspath(ref)[len(os.path.abspath(review_root)) + 1:]
                top = rel.split("\\", 1)[0]
                if top and os.path.normcase(top) != own_name:
                    deps.add(top)
    return deps


def review_verdict(full, review_root, cutoff, reach, now=None):
    """None = loeschbar, sonst Grund fuers Behalten."""
    if is_reparse(full):
        return "reparse"
    if now is None:
        now = time.time()
    owner_meta = read_owner_meta(full)
    closed_out = is_closed_out(full)
    exp_ts = parse_timestamp(owner_meta.get("expires_at"))
    owner_canon = owner_meta.get("canonical_repo")

    repos = []
    has_young_sub = False
    for i, (p, names) in enumerate(walk_depth(full)):
        if any(is_lock_file(n) and os.path.isfile(os.path.join(p, n)) for n in names):
            return "lock"
        if i == 0 and any(os.path.isdir(os.path.join(p, n)) and os.path.getmtime(os.path.join(p, n)) > cutoff
                          for n in names):
            has_young_sub = True
        if ".git" in names:
            repos.append((p, False))
        elif p.endswith(".git") and "HEAD" in names and "objects" in names:
            repos.append((p, True))

    if not closed_out:
        if exp_ts is not None:
            if exp_ts > now:
                return "aktiv-owner"
        else:
            if os.path.getmtime(full) > cutoff:
                return "jung"
            if has_young_sub:
                return "jung-unterordner"

    for repo, bare in repos:
        if not bare and git(repo, "status", "--porcelain"):
            return f"dirty:{repo}"
        # refs/stash is shared by all worktrees of a repository: in a linked worktree `stash list` shows the
        # stash of the canonical clone, which is never deleted here.  Own stashes (clone, shared clone) keep it.
        if not _is_linked_worktree(repo) and git(repo, "stash", "list"):
            return f"stash:{repo}"
        canon = canon_of(repo, review_root, owner_canon=owner_canon)
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


def remove_review_sandbox(full, review_root):
    """Entfernt eine Review-Sandbox und raeumt etwaige Worktree-Metadaten im Kanon-Repo auf.

    Loescht nur ein direktes Kind von `review_root` (is_direct_child); alles andere bleibt unberuehrt."""
    if not is_direct_child(full, review_root):
        return False
    owner_canon = read_owner_meta(full).get("canonical_repo")
    canons = set()
    for repo, bare in _sandbox_repos(full):
        if not bare and os.path.isfile(os.path.join(repo, ".git")):
            c = canon_of(repo, review_root, owner_canon=owner_canon)
            if c:
                canons.add(c)
    ok = remove(full)
    if ok:
        for c in canons:
            git(c, "worktree", "prune")
    return ok


def prune_reviews(review_root, hours, apply, out):
    now = time.time()
    cutoff, reach, kept = now - hours * 3600, {}, {}
    gone = 0
    entries = []
    verdicts = {}
    deps_of = {}
    case_map = {}

    for name in sorted(os.listdir(review_root)):
        full = os.path.join(review_root, name)
        if not os.path.isdir(full):
            continue
        entries.append(name)
        case_map[os.path.normcase(name)] = name
        verdicts[name] = review_verdict(full, review_root, cutoff, reach, now=now)
        deps_of[name] = sandbox_dependencies(full, review_root)

    # Normalisiere Abhaengigkeiten auf existierende Ordnernamen in review_root
    for name in entries:
        deps_of[name] = {case_map[os.path.normcase(d)] for d in deps_of[name] if os.path.normcase(d) in case_map}

    # Ketten-Klon-Schutz: Wenn ein abhaengiger Kind-Ordner behalten wird, muss auch der Eltern-Ordner bleiben
    changed = True
    while changed:
        changed = False
        for child in entries:
            if verdicts[child] is not None:
                for parent in deps_of[child]:
                    if verdicts.get(parent) is None:
                        verdicts[parent] = f"ketten-abhaengig:{child}"
                        changed = True

    # Loeschbare Sandboxen in Abhaengigkeitsreihenfolge (Kinder vor Eltern) bearbeiten
    deletable = [n for n in entries if verdicts[n] is None]
    ordered = []
    remaining = list(deletable)
    while remaining:
        # Ein Kandidat hat keine noch ungeloeschten Kinder unter `remaining`
        ready = [
            n for n in remaining
            if not any(n in deps_of[other] for other in remaining if other != n)
        ]
        if not ready:
            ready = [remaining[0]]
        for n in ready:
            ordered.append(n)
            remaining.remove(n)

    failed_parents = set()
    for name in ordered:
        full = os.path.join(review_root, name)
        if name in failed_parents:
            verdicts[name] = "ketten-abhaengig"
            continue
        if not apply or remove_review_sandbox(full, review_root):
            gone += 1
            out(f"  [review] {'geloescht' if apply else 'wuerde loeschen'}: {name}")
        else:
            verdicts[name] = "nicht-loeschbar"
            # A retained clone still needs every transitive object-source parent,
            # even when an intermediate parent is skipped later in this loop.
            pending = list(deps_of[name])
            while pending:
                parent = pending.pop()
                if parent in failed_parents:
                    continue
                failed_parents.add(parent)
                pending.extend(deps_of[parent])

    for name in entries:
        why = verdicts[name]
        if why is not None:
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
        configured = CONFIG.get("review_dirs", ["reviews"])
        roots = safe_review_roots(LOCAL_DEV, configured)
        if len(roots) != len(configured if isinstance(configured, list) else [configured]):
            out("[review] review_dirs: nur einfache Ordnernamen direkt unter local_dev sind erlaubt; Rest ignoriert")
        for root in roots:
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
