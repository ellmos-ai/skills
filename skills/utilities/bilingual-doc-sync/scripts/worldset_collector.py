"""One guarded offline intake pass, suitable for an existing host scheduler.

Private configuration/runtime and the installed native lock tools are explicit.
This runner never schedules workers, submits models or applies translations.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from worldset import check_writer, exclusive_atomic, safe_path, sha, write_json
from worldset_discovery import archived, bounded_bytes, collect, discover, excluded, read_source, strict_json

MAX_SNAPSHOT_BYTES = 64 * 1024 * 1024


def unlinked(path: Path) -> Path:
    path = path.absolute()
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('linked runtime or configuration path')
    return path.resolve()


def load_tools(directory: Path):
    directory = unlinked(directory)
    for name in ('lock_utils.py', 'lock_scan.py', 'lock_create.py'):
        if not (directory / name).is_file():
            raise ValueError('native lock installation is incomplete')
    spec = importlib.util.spec_from_file_location('worldset_collector_lock_utils', directory / 'lock_utils.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _read_snapshot(path: Path) -> bytes:
    path = unlinked(path)
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SNAPSHOT_BYTES:
        raise ValueError('snapshot is not a bounded regular file')
    if getattr(info, 'st_file_attributes', 0) & 0x1000:
        raise ValueError('offline snapshot placeholder; hydration is not automatic')
    return path.read_bytes()


def _fingerprint(projects: list[dict]) -> list[dict]:
    fields = ('id', 'source_language', 'visibility', 'source_visibility',
              'allow_private', 'stars', 'views', 'eligibility_registry_sha256')
    return [{**{key: project.get(key) for key in fields},
             'root': str(Path(project['root']).resolve())}
            for project in projects]


def _verify_snapshot_sources(report: dict, projects: list[dict]) -> None:
    """Reject a scan whose source or catalogue changed before publication."""
    by_id = {project['id']: project for project in projects}
    observed_catalogues: dict[tuple[str, str], str] = {}
    for reference, record in report['snapshot'].items():
        project_id = next((ident for ident in sorted(by_id, key=len, reverse=True)
                           if reference.startswith(ident + ':')), None)
        if project_id is None:
            raise ValueError('snapshot source is not bound to a discovered project')
        relative = reference[len(project_id) + 1:]
        root = Path(by_id[project_id]['root'])
        if 'source_pointer' in record:
            relative = relative.split('#', 1)[0]
            key = (project_id, relative)
            current = observed_catalogues.get(key)
            if current is None:
                catalogue = safe_path(root, relative)
                current = sha(bounded_bytes(catalogue))
                observed_catalogues[key] = current
            if current != record.get('catalog_sha256'):
                raise ValueError('catalogue changed during collection')
        else:
            source = safe_path(root, relative)
            current = sha(read_source(source).encode())
            if current != record.get('source_sha256'):
                raise ValueError('source changed during collection')
    for reference, record in report.get('catalog_snapshot', {}).items():
        project_id = next((ident for ident in sorted(by_id, key=len, reverse=True)
                           if reference.startswith(ident + ':')), None)
        if project_id is None:
            raise ValueError('catalogue is not bound to a discovered project')
        relative = reference[len(project_id) + 1:].split('#', 1)[0]
        key = (project_id, relative)
        current = observed_catalogues.get(key)
        if current is None:
            catalogue = safe_path(Path(by_id[project_id]['root']), relative)
            current = sha(bounded_bytes(catalogue))
            observed_catalogues[key] = current
        if current != record.get('catalog_sha256'):
            raise ValueError('catalogue changed during collection')


def _source_inventory(projects: list[dict]) -> dict[tuple[str, str, str], tuple]:
    """Capture eligible document paths and configured catalogue file state."""
    patterns = {
        'readme': ['README.md'],
        'skills': ['skills/*/*/SKILL.md'],
        'skills-flat': ['skills/*/SKILL.md'],
    }
    default_catalogs = [
        {'path': 'locales/translations.json'},
        {'path': 'locales/gui_translations.json'},
    ]
    inventory = {}
    for project in projects:
        ident, root = project['id'], Path(project['root'])
        kind = project.get('kind', 'readme')
        if kind not in patterns:
            raise ValueError('unknown document adapter')
        for pattern in patterns[kind]:
            for candidate in sorted(root.glob(pattern)):
                relative = candidate.relative_to(root).as_posix()
                if excluded(Path(relative)):
                    continue
                source = safe_path(root, relative)
                info = source.stat()
                if not stat.S_ISREG(info.st_mode):
                    raise ValueError('document inventory contains a non-regular file')
                inventory[(ident, 'document', relative)] = (info.st_size, info.st_mtime_ns)
        for spec in project.get('catalogs', default_catalogs):
            relative = spec.get('path') if isinstance(spec, dict) else None
            if not isinstance(relative, str) or not relative:
                raise ValueError('catalogue path required')
            if excluded(Path(relative)):
                continue
            catalogue = safe_path(root, relative)
            if not catalogue.exists():
                continue
            info = catalogue.stat()
            if not stat.S_ISREG(info.st_mode):
                inventory[(ident, 'catalogue', relative)] = ('non-regular', info.st_mode)
                continue
            offline = bool(getattr(info, 'st_file_attributes', 0) & 0x1000)
            digest = None
            if not offline:
                try:
                    digest = sha(bounded_bytes(catalogue))
                except (OSError, ValueError):
                    pass
            inventory[(ident, 'catalogue', relative)] = (
                info.st_size, info.st_mtime_ns, offline, digest)
    return inventory


def _load_previous(runtime: Path) -> dict | None:
    receipt_path = unlinked(runtime / 'last-success.json')
    if receipt_path.exists():
        receipt = strict_json(_read_snapshot(receipt_path).decode('utf-8'))
        name = receipt.get('snapshot_file')
        if (receipt.get('status') != 'collected' or not isinstance(name, str)
                or not re.fullmatch(r'discovery-[0-9a-f]{64}\.json', name)):
            raise ValueError('last-success receipt has an invalid snapshot reference')
        raw = _read_snapshot(runtime / name)
        if sha(raw) != receipt.get('snapshot_sha256'):
            raise ValueError('last-success snapshot hash mismatch')
        return strict_json(raw.decode('utf-8'))
    # Read the pre-receipt format once for upgrade continuity.
    legacy = unlinked(runtime / 'discovery.json')
    return strict_json(_read_snapshot(legacy).decode('utf-8')) if legacy.exists() else None


def run(config_path: Path, runtime: Path, lock_tools: Path, *, owner: str = 'worldset-collector') -> dict:
    """Publish only a completed scan under a current native own fence."""
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    config_path, runtime = unlinked(config_path), unlinked(runtime)
    if not runtime.is_dir() or not config_path.is_file():
        raise ValueError('pre-existing private runtime and configuration required')
    config_bytes = bounded_bytes(config_path)
    config = strict_json(config_bytes.decode('utf-8-sig'))
    if not isinstance(config, dict):
        raise ValueError('configuration must be an object')
    required = config.get('required_roots', [])
    if not isinstance(required, list) or any(not isinstance(p, str) or not p for p in required):
        raise ValueError('required_roots must be a list of paths')
    roots = required + [p['root'] for p in config.get('projects', [])
                        if not archived(p) and not excluded(Path(p['root']))]
    roots += [p['root'] for p in config.get('discovery_roots', [])]
    if any(not Path(p).is_dir() for p in roots):
        return {'status': 'skipped_missing_source_root', 'api_calls': 0}
    projects, _ = discover(config)
    roots += [project['root'] for project in projects]
    if any(not Path(root).is_dir() for root in roots):
        return {'status': 'skipped_missing_source_root', 'api_calls': 0}
    if any(runtime.is_relative_to(Path(p['root']).resolve()) for p in projects):
        raise ValueError('runtime must be outside source projects')
    source_inventory = _source_inventory(projects)
    tools = load_tools(lock_tools)
    if tools.active_locks_for_path(runtime):
        return {'status': 'skipped_locked', 'api_calls': 0}
    lock = runtime / 'LOCK.txt'
    # Never replace an unexpired/unknown competing claim, nor an expired foreign file.
    if lock.exists():
        return {'status': 'skipped_existing_claim', 'api_calls': 0}
    claim = subprocess.run([
        sys.executable, str(lock_tools / 'lock_create.py'), str(runtime),
        '--owner', owner, '--expires', '30m',
        '--purpose', 'Offline translation intake snapshot; no source or executor writes',
    ], capture_output=True, text=True, encoding='utf-8', timeout=420)
    if claim.returncode != 0:
        raise ValueError('native collector claim failed')
    match = re.search(r'(?m)^fence:[ \t]*(\d+)[ \t]*$', claim.stdout)
    if not match:
        raise ValueError('native collector claim returned no verifiable fence')
    fence = int(match.group(1))
    checker = lock_tools / 'lock_scan.py'

    def guard():
        if tools.fence_status(lock, fence)[0] != 'held' or not tools.lock_applies_to_target(lock, runtime):
            raise ValueError('collector fence lost')
        check_writer(checker, runtime, lock, str(fence), owner)

    try:
        guard()
        receipt_path = unlinked(runtime / 'last-success.json')
        previous = _load_previous(runtime)
        report = collect(config, previous)
        if config_path.read_bytes() != config_bytes:
            raise ValueError('configuration changed during collection')
        confirmed_projects, _ = discover(config)
        if _fingerprint(projects) != _fingerprint(confirmed_projects):
            raise ValueError('eligible project or registry set changed during collection')
        if any(not Path(root).is_dir() for root in roots):
            raise ValueError('source root disappeared during collection')
        _verify_snapshot_sources(report, confirmed_projects)
        if _source_inventory(confirmed_projects) != source_inventory:
            raise ValueError('source inventory changed during collection')
        guard()
        snapshot_bytes = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        snapshot_digest = sha(snapshot_bytes)
        snapshot_name = f'discovery-{snapshot_digest}.json'
        snapshot_path = unlinked(runtime / snapshot_name)
        if snapshot_path.exists():
            if _read_snapshot(snapshot_path) != snapshot_bytes:
                raise ValueError('content-addressed snapshot collision')
        else:
            exclusive_atomic(snapshot_path, snapshot_bytes)
        if config_path.read_bytes() != config_bytes:
            raise ValueError('configuration changed before receipt publication')
        receipt = {
            'status': 'collected', 'finished_at': datetime.now(timezone.utc).isoformat(),
            'snapshot_file': snapshot_name, 'snapshot_sha256': snapshot_digest,
            'configuration_file_sha256': sha(config_bytes),
            'projects': len(report['packages']), 'sources': len(report['snapshot']),
            'document_jobs': sum(len(p['projection']['jobs']) for p in report['packages']),
            'catalogue_candidates': sum(len(p['catalogue_candidates']) for p in report['packages']),
            'attention': len(report['attention']), 'api_calls': 0,
            'translation_or_source_writes': 0, 'executor_state_owned_here': False,
        }
        guard()
        write_json(receipt_path, receipt)
        return receipt
    finally:
        # Only release our exact, still-held native claim; never clean foreign claims.
        if tools.fence_status(lock, fence)[0] == 'held' and tools.lock_applies_to_target(lock, runtime):
            lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--lock-tools', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.config, args.runtime, args.lock_tools)))


if __name__ == '__main__':
    main()
