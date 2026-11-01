#!/usr/bin/env python3
r"""Lifecycle-Helper fuer isolierte Review-Sandboxen ohne Vollkopien (--no-hardlinks-Verbot).

Legt eine Review-Sandbox unter <local_dev>\<review_dir>\<name> ausschliesslich per
`git worktree add --detach` oder `git clone --shared` gegen den kanonischen Klon an,
schreibt `owner.json` (mit `owner`, `ticket_id`, `canonical_repo`, `created_at`, `expires_at`)
und gibt die Sandbox bei `closeout` (schreibt `closeout.json` + Sicherheitspruefung via
`prune_ephemeral.review_verdict`) sofort wieder frei.

Ketten-Klonen (Klonen aus einem anderen Review-Ordner) wird fail-closed abgewiesen.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clean_build_junk import CONFIG, LOCAL_DEV  # noqa: E402
from prune_ephemeral import (  # noqa: E402
    NO_WINDOW,
    _is_git_repo_dir,
    _is_outside_review_root,
    remove_review_sandbox,
    review_verdict,
    sandbox_dependencies,
)


def default_review_root():
    if not LOCAL_DEV:
        return ""
    review_dirs = CONFIG.get("review_dirs") or ["reviews"]
    return os.path.join(LOCAL_DEV, review_dirs[0])


def _iso_utc(ts=None):
    dt = datetime.fromtimestamp(time.time() if ts is None else ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def create_sandbox(
    name,
    canonical_repo,
    owner,
    ticket_id=None,
    ttl_hours=4.0,
    mode="worktree",
    ref="HEAD",
    review_root=None,
):
    """Legt eine Review-Sandbox mit owner.json und worktree/shared-Checkout an."""
    review_root = os.path.abspath(review_root or default_review_root())
    if not review_root:
        raise ValueError("Kein review_root konfiguriert (--review-root oder local_dev in config.json).")
    canon = os.path.abspath(canonical_repo)
    if not _is_git_repo_dir(canon):
        raise ValueError(f"Kanonischer Klon ist kein gueltiges Git-Repository: {canon}")
    if not _is_outside_review_root(canon, review_root):
        raise ValueError(
            f"Ketten-Klonen verboten: Quelle {canon} liegt innerhalb der Review-Wurzel {review_root}."
        )
    if mode not in ("worktree", "shared"):
        raise ValueError(f"Ungueltiger Modus '{mode}': erlaubt sind 'worktree' oder 'shared'.")
    if not name or os.path.basename(name) != name or name in (".", ".."):
        raise ValueError(f"Ungueltiger Sandbox-Name: {name}")

    os.makedirs(review_root, exist_ok=True)
    sandbox_dir = os.path.join(review_root, name)
    if os.path.exists(sandbox_dir):
        raise FileExistsError(f"Sandbox existiert bereits: {sandbox_dir}")
    os.makedirs(sandbox_dir, exist_ok=False)

    now = time.time()
    exp = now + float(ttl_hours) * 3600.0
    owner_meta = {
        "schema": "review-sandbox-owner/v1",
        "owner": str(owner),
        "ticket_id": str(ticket_id or ""),
        "canonical_repo": canon,
        "mode": mode,
        "ref": str(ref),
        "created_at": _iso_utc(now),
        "expires_at": _iso_utc(exp),
    }
    owner_path = os.path.join(sandbox_dir, "owner.json")
    with open(owner_path, "w", encoding="utf-8") as fh:
        json.dump(owner_meta, fh, indent=2)

    source_dir = os.path.join(sandbox_dir, "source")
    try:
        if mode == "worktree":
            subprocess.run(
                ["git", "-C", canon, "worktree", "add", "--detach", source_dir, ref],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=NO_WINDOW,
            )
        else:
            subprocess.run(
                ["git", "clone", "-q", "--shared", "--no-checkout", canon, source_dir],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=NO_WINDOW,
            )
            subprocess.run(
                ["git", "-C", source_dir, "checkout", "-q", "--detach", ref],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=NO_WINDOW,
            )
    except Exception:
        remove_review_sandbox(sandbox_dir, review_root)
        raise

    return {
        "sandbox": sandbox_dir,
        "source": source_dir,
        "owner_file": owner_path,
        "owner_meta": owner_meta,
    }


def closeout_sandbox(
    sandbox_path,
    head=None,
    url=None,
    report=None,
    delete_now=True,
    review_root=None,
):
    """Schreibt closeout.json und loescht die Sandbox sofort, sofern alle Sicherheits-Gates gruen sind."""
    sandbox_dir = os.path.abspath(sandbox_path)
    if not os.path.isdir(sandbox_dir):
        raise FileNotFoundError(f"Sandbox nicht gefunden: {sandbox_dir}")
    review_root = os.path.abspath(review_root or os.path.dirname(sandbox_dir))
    closeout_path = os.path.join(sandbox_dir, "closeout.json")
    data = {}
    if os.path.isfile(closeout_path):
        try:
            with open(closeout_path, encoding="utf-8") as fh:
                existing = json.load(fh)
            if isinstance(existing, dict):
                data.update(existing)
        except (OSError, ValueError):
            pass

    data["status"] = "closed"
    data["closed_at"] = _iso_utc()
    if head:
        data["head"] = str(head)
    if url:
        data["url"] = str(url)
    if report:
        data["report"] = str(report)

    with open(closeout_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    now = time.time()
    verdict = review_verdict(sandbox_dir, review_root, cutoff=now - 86400, reach={}, now=now)
    # Pruefe, ob ein anderer Review-Ordner unter review_root noch von dieser Sandbox abhaengt
    if verdict is None and os.path.isdir(review_root):
        own_norm = os.path.normcase(os.path.basename(sandbox_dir))
        for other in os.listdir(review_root):
            other_full = os.path.join(review_root, other)
            if os.path.normcase(other) == own_norm or not os.path.isdir(other_full):
                continue
            other_deps = {os.path.normcase(d) for d in sandbox_dependencies(other_full, review_root)}
            if own_norm in other_deps:
                verdict = f"ketten-abhaengig:{other}"
                break

    deleted = False
    if delete_now and verdict is None:
        deleted = remove_review_sandbox(sandbox_dir, review_root)
        if not deleted:
            verdict = "nicht-loeschbar"

    return {
        "sandbox": sandbox_dir,
        "closeout_file": closeout_path,
        "status": "closed",
        "verdict": verdict,
        "deleted": deleted,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="Neue Review-Sandbox anlegen (worktree oder shared)")
    p_create.add_argument("--name", required=True, help="Ordnername unter review_root")
    p_create.add_argument("--repo", required=True, help="Pfad zum kanonischen lokalen Klon")
    p_create.add_argument("--owner", required=True, help="Besitzer-Kennung (z. B. agent@host)")
    p_create.add_argument("--ticket", default="", help="Ticket- oder PR-Kennung")
    p_create.add_argument("--ttl-hours", type=float, default=4.0, help="Ablaufzeit in Stunden (Default: 4)")
    p_create.add_argument("--mode", choices=("worktree", "shared"), default="worktree")
    p_create.add_argument("--ref", default="HEAD", help="Git-Ref fuer Checkout (Default: HEAD)")
    p_create.add_argument("--review-root", default=None, help="Optionale Review-Wurzel")

    p_close = sub.add_parser("closeout", help="Review-Sandbox abschliessen und bei gruenen Gates sofort loeschen")
    p_close.add_argument("--sandbox", required=True, help="Pfad zur Review-Sandbox")
    p_close.add_argument("--head", default=None, help="Gepruefter Commit-SHA")
    p_close.add_argument("--url", default=None, help="Verlinkter PR-/Kommentar-Beleg")
    p_close.add_argument("--report", default=None, help="Pfad zum abgelegten Review-Bericht")
    p_close.add_argument("--keep", action="store_true", help="Nur closeout.json schreiben, noch nicht loeschen")
    p_close.add_argument("--review-root", default=None, help="Optionale Review-Wurzel")

    args = parser.parse_args(argv)
    if args.cmd == "create":
        res = create_sandbox(
            name=args.name,
            canonical_repo=args.repo,
            owner=args.owner,
            ticket_id=args.ticket,
            ttl_hours=args.ttl_hours,
            mode=args.mode,
            ref=args.ref,
            review_root=args.review_root,
        )
    else:
        res = closeout_sandbox(
            sandbox_path=args.sandbox,
            head=args.head,
            url=args.url,
            report=args.report,
            delete_now=not args.keep,
            review_root=args.review_root,
        )
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
