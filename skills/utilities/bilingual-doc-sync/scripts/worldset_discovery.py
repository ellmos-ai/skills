"""Offline, incremental demand discovery for the existing World Set executor.

This emits native projections and lossless protected chunks, never submits jobs,
changes sources, leases workers, approves translations or maintains another queue.
Host paths and discovery configuration belong in a private runtime directory.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
from pathlib import Path

from worldset import LANGS, SECRET, check_writer, protect, safe_path, sha, write_json
from worldset_segments import fragments

ARCHIVE_PARTS = {'archive', 'archives', 'archived', 'archiv', '_archive', '_archiv',
                 '_archived', '.archive', '.archiv', '.archived', 'archiviert', '_archiviert', '.archiviert'}
SKIP_PARTS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'dist', 'build',
              'private-artifacts', '_templates', '_reference', '.credentials', 'credentials',
              '.pytest_cache', '.ruff_cache', '.mypy_cache', '.tox', '.hypothesis', '.cache',
              '.agents', '.codex', '.claude', '.gemini'}
ARCHIVE_STATUS = {'archived', 'archive', 'archiviert', 'arc'}
PRIVATE_VISIBILITY = {'private', 'private-only', 'private profile', 'private-profile'}


def strict_json(text: str):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON object key')
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=unique)


def configuration_hash(config: dict) -> str:
    return sha(json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def excluded(path: Path) -> bool:
    for part in path.parts:
        name = part.casefold()
        if (name in ARCHIVE_PARTS | SKIP_PARTS or name.startswith('arc_')
                or name in {'_user', '_usr'}
                or name.startswith(('.usr', '.user'))):
            return True
    return False


def archived(project: dict) -> bool:
    return (any(part.casefold().startswith(('arc_', '.usr', '.user')) or part.casefold() in {'_usr', '_user'}
                for key in ('name', 'id') for part in re.split(r'[\\/]', str(project.get(key, ''))))
            or any(str(project.get(key, '')).strip().casefold() in ARCHIVE_STATUS
                for key in ('status', 'lifecycle'))
            or any(str(project.get(key, '')).casefold() in {'usr', 'user', '.usr', '.user'}
                   for key in ('lifecycle', 'project_type', 'business_class')))


def bounded_bytes(path: Path, maximum: int = 1_048_576) -> bytes:
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > maximum:
        raise ValueError('source is not a bounded regular file')
    if getattr(info, 'st_file_attributes', 0) & 0x1000:
        raise ValueError('offline cloud placeholder; hydration is not automatic')
    return path.read_bytes()


def read_source(path: Path, maximum: int = 1_048_576) -> str:
    text = bounded_bytes(path, maximum).decode('utf-8-sig').replace('\r\n', '\n')
    if SECRET.search(text):
        raise ValueError('credential pattern in source')
    return text


def discover(config: dict) -> tuple[list[dict], list[dict]]:
    """Use whitelisted registry fields and bounded, pruned directory discovery."""
    projects = list(config.get('projects', []))
    notes = []
    denied_roots = {str(Path(project['root']).resolve()) for project in projects if archived(project)}
    private_roots = {str(Path(project['root']).resolve()) for project in projects
                     if project.get('visibility') in PRIVATE_VISIBILITY}
    def denied(path):
        resolved = path.resolve()
        return any(resolved.is_relative_to(Path(parent)) for parent in denied_roots)
    def private(path):
        resolved = path.resolve()
        return any(resolved.is_relative_to(Path(parent)) for parent in private_roots)
    for registry in config.get('registries', []):
        path = Path(registry['path'])
        data = strict_json(read_source(path, 8_388_608))
        registry_hash = sha(bounded_bytes(path, 8_388_608))
        for row in data.get('projects', []):
            relative = Path(row['path'])
            root = relative if relative.is_absolute() else path.parent / relative
            if not root.resolve().is_relative_to(path.parent.resolve()):
                notes.append({'project': str(row.get('name', '')), 'reason': 'registry_path_outside_collection'})
                continue
            if row.get('visibility') in PRIVATE_VISIBILITY:
                private_roots.add(str(root.resolve()))
            if archived(row):
                denied_roots.add(str(root.resolve()))
                continue
            projects.append({'id': str(row.get('name', relative.name)), 'root': str(root),
                             'kind': 'readme', 'source_language': registry.get('source_language'),
                             'status': row.get('status'), 'lifecycle': row.get('lifecycle'),
                             'business_class': row.get('business_class'),
                             'visibility': row.get('visibility'),
                             'eligibility_registry': str(path), 'eligibility_registry_sha256': registry_hash})
    for discovery in config.get('discovery_roots', []):
        root = Path(discovery['root'])
        depth = discovery.get('depth', 2)
        minimum = discovery.get('min_project_depth', 1)
        if type(depth) is not int or not 0 <= depth <= 4:
            raise ValueError('discovery depth must be between zero and four')
        if type(minimum) is not int or not 0 <= minimum <= depth:
            raise ValueError('invalid minimum project depth')
        pending = [(root, 0)]
        visited = 0
        while pending:
            directory, level = pending.pop()
            if excluded(directory) or denied(directory) or directory.is_symlink() or getattr(directory, 'is_junction', lambda: False)():
                continue
            visited += 1
            if visited > discovery.get('max_directories', 2000):
                raise ValueError('discovery directory bound exceeded; no incomplete snapshot published')
            try:
                if level >= minimum and (directory / 'README.md').is_file():
                    projects.append({'id': discovery.get('id', 'discovery') + '/' + directory.relative_to(root).as_posix(),
                                     'root': str(directory), 'kind': 'readme',
                                     'source_language': discovery.get('source_language'),
                                     'source_visibility': discovery.get('source_visibility')})
                    continue
                if level < depth:
                    with os.scandir(directory) as entries:
                        children = []
                        for number, item in enumerate(entries):
                            if number >= discovery.get('max_directory_entries', 5000):
                                raise ValueError('discovery directory entry bound exceeded')
                            if not excluded(Path(item.path)) and item.is_dir(follow_symlinks=False):
                                children.append(Path(item.path))
                    pending.extend((child, level + 1) for child in sorted(children, reverse=True))
            except OSError as error:
                raise ValueError('unreadable discovery directory; retain the previous successful snapshot') from error
    unique = {}
    for project in projects:
        root = Path(project['root'])
        if archived(project) or denied(root) or excluded(root) or excluded(root.resolve()):
            continue
        if private(root):
            project = {**project, 'visibility': 'private'}
        if project.get('visibility') in PRIVATE_VISIBILITY and project.get('allow_private') is not True:
            notes.append({'project': project['id'], 'reason': 'private_project_excluded'})
            continue
        # Check before resolve as well: a private path must never be followed out.
        if root.is_symlink() or getattr(root, 'is_junction', lambda: False)():
            notes.append({'project': project['id'], 'reason': 'linked_project_root'})
            continue
        key = str(root.resolve())
        if key in unique:
            existing = unique[key]
            if (existing.get('source_language') and project.get('source_language')
                    and existing['source_language'] != project['source_language']):
                raise ValueError('conflicting source-language configuration for project root')
            # Explicit projects precede registries, which precede filesystem
            # discovery. Preserve their ID, adapters and reviewed overrides.
            if not existing.get('source_language') and project.get('source_language'):
                existing['source_language'] = project['source_language']
            if project.get('eligibility_registry'):
                existing['eligibility_registry'] = project['eligibility_registry']
                existing['eligibility_registry_sha256'] = project['eligibility_registry_sha256']
            continue
        unique[key] = project
    if len(unique) > config.get('max_projects', 2000):
        raise ValueError('project bound exceeded')
    return sorted(unique.values(), key=lambda p: p['id']), notes


def source_language(text: str, configured: str | None) -> str | None:
    if configured is not None and (not isinstance(configured, str) or configured.lower() not in ('en', 'de')):
        raise ValueError('leading source must be explicitly English or German')
    declarations = re.findall(r'<!--\s*source-language:\s*([^>]*?)\s*-->', text, re.I)
    frontmatter = re.match(r'\A---\s*\n(.*?)\n---(?:\n|$)', text, re.S)
    if frontmatter:
        declarations.extend(re.findall(r'^language:[ \t]*([^\n]*)$', frontmatter[1], re.M | re.I))
    declarations = [value.split(' #', 1)[0].strip().strip('\"\'').lower() for value in declarations]
    if any(value not in ('en', 'de') for value in declarations):
        raise ValueError('unsupported declared source language')
    if len(set(declarations)) > 1 or (declarations and configured and declarations[0] != configured.lower()):
        raise ValueError('conflicting source-language declaration')
    language = declarations[0] if declarations else configured
    return language.lower() if language else None


def pointer(value: str) -> str:
    return value.replace('~', '~0').replace('/', '~1')


def catalogue_candidates(project: dict, previous: dict) -> tuple[list[dict], dict, list[dict]]:
    """Extract typed locale fields, without pretending Markdown apply can edit JSON.

    Existing per-project field adapters retain restoration/integration authority.
    Source revisions and JSON pointers make each candidate independently reviewable.
    """
    root = Path(project['root'])
    specs = project.get('catalogs', [
        {'path': 'locales/translations.json', 'shape': 'localized-map', 'source_language': 'de'},
        {'path': 'locales/gui_translations.json', 'shape': 'entries-list'},
    ])
    candidates, snapshot, attention = [], {}, []
    for spec in specs:
        relative = spec['path']
        if excluded(Path(relative)):
            continue
        candidate_start = len(candidates)
        snapshot_before_catalogue = dict(snapshot)
        try:
            path = safe_path(root, relative)
            if not path.is_file():
                continue
            raw = bounded_bytes(path)
            text = raw.decode('utf-8-sig')
            if SECRET.search(text):
                raise ValueError('credential pattern in catalogue')
            data = strict_json(text)
            if not isinstance(data, dict):
                raise ValueError('catalogue root must be an object')
            fields = []
            private_fields = set()
            metadata = data.get('_meta', {})
            if not isinstance(metadata, dict):
                raise ValueError('catalogue metadata must be an object')
            catalogue_visibility = (metadata.get('source_visibility') or metadata.get('visibility')
                                    or project.get('source_visibility') or project.get('visibility'))
            catalogue_private = catalogue_visibility != 'public'
            if catalogue_private and project.get('allow_private') is not True:
                reason = ('private_catalogue_excluded' if catalogue_visibility in PRIVATE_VISIBILITY
                          else 'catalogue_visibility_review_required')
                attention.append({'project': project['id'], 'source': relative, 'reason': reason})
                continue
            if spec['shape'] == 'localized-map':
                lang = spec.get('source_language')
                if lang not in ('en', 'de'):
                    raise ValueError('catalogue leading language required')
                for key, translations in data.items():
                    if key == '_meta':
                        continue
                    if not isinstance(translations, dict) or not isinstance(translations.get(lang), str):
                        raise ValueError('unsupported localized-map entry')
                    field_visibility = translations.get('visibility')
                    if field_visibility is not None and field_visibility != 'public':
                        if project.get('allow_private') is not True:
                            attention.append({'project': project['id'], 'source': relative, 'key': key,
                                              'reason': 'private_catalogue_field_excluded'})
                            continue
                        private_fields.add(key)
                    fields.append((str(key), '/' + pointer(key) + '/' + lang,
                                   translations[lang], lang, translations))
            elif spec['shape'] == 'entries-list':
                if not isinstance(data.get('entries'), list):
                    raise ValueError('catalogue entries must be a list')
                keys = [row.get('key') for row in data['entries'] if isinstance(row, dict)]
                if any(not isinstance(key, str) for key in keys) or len(keys) != len(set(keys)):
                    raise ValueError('duplicate or invalid typed catalogue field key')
                for index, row in enumerate(data['entries']):
                    if not isinstance(row, dict) or not isinstance(row.get('translations'), dict):
                        raise ValueError('typed catalogue entry must contain a translations object')
                    if row.get('visibility') is not None and row.get('visibility') != 'public':
                        if project.get('allow_private') is not True:
                            attention.append({'project': project['id'], 'source': relative, 'key': row.get('key'),
                                              'reason': 'private_catalogue_field_excluded'})
                            continue
                        private_fields.add(row['key'])
                    value, translations = row['canonical_source_value'], row['translations']
                    matches = [code for code in ('en', 'de') if translations.get(code) == value]
                    lang = row.get('source_locale') or (matches[0] if len(matches) == 1 else
                                                       spec.get('source_language') if spec.get('source_language') in matches else None)
                    if lang not in ('en', 'de'):
                        attention.append({'project': project['id'], 'source': relative, 'key': row['key'],
                                          'reason': 'catalogue_canonical_source_language_unresolved',
                                          'source_sha256': sha(str(value).encode()),
                                          'source_text': value})
                        continue
                    fields.append((row['key'], '/entries/' + str(index) + '/canonical_source_value',
                                   value, lang, translations))
            elif spec['shape'] == 'namespace-map':
                lang = spec.get('source_language')
                if lang not in ('en', 'de'):
                    raise ValueError('catalogue leading language required')
                if not isinstance(data.get('entries'), dict):
                    raise ValueError('namespace catalogue entries must be an object')
                for namespace, values in data['entries'].items():
                    if not isinstance(values, dict):
                        raise ValueError('namespace catalogue values must be an object')
                    for key, value in values.items():
                        fields.append((namespace + ':' + key, '/entries/' + pointer(namespace) + '/' + pointer(key),
                                       value, lang, {}))
            else:
                raise ValueError('unsupported catalogue adapter')
            if len(fields) > spec.get('max_fields', 10000):
                raise ValueError('catalogue field bound exceeded')
            if len({field[0] for field in fields}) != len(fields):
                raise ValueError('duplicate catalogue field key')
            for key, source_pointer, value, lang, translations in fields:
                if not isinstance(value, str):
                    raise ValueError('non-string catalogue source')
                digest = sha(value.encode())
                reference = project['id'] + ':' + relative + '#' + key
                hashes = {code: sha(translated.encode()) for code, translated in translations.items()
                          if isinstance(translated, str) and code in LANGS}
                snapshot[reference] = {'source_sha256': digest, 'catalog_sha256': sha(raw),
                                       'source_pointer': source_pointer, 'source_language': lang,
                                       'target_hashes': hashes}
                before = previous.get(reference)
                changed_secondary = [code for code in ('en', 'de') if code != lang and before
                                     and hashes.get(code) != before.get('target_hashes', {}).get(code)]
                if changed_secondary:
                    snapshot[reference] = before
                    attention.append({'project': project['id'], 'source': relative, 'key': key,
                                      'languages': changed_secondary, 'reason': 'secondary_catalogue_source_changed'})
                    continue
                reason = 'source_changed' if before and before['source_sha256'] != digest else 'missing_or_unverified_target'
                protected = protect(value)
                for target in LANGS:
                    if target == lang:
                        continue
                    existing = translations.get(target)
                    candidates.append({'id': sha((reference + '\0' + target + '\0' + digest).encode())[:40],
                                       'project': project['id'], 'source_file': relative,
                                       'source_pointer': source_pointer, 'source_key': key,
                                       'source_language': lang, 'source_sha256': digest,
                                       'source_text': value, 'catalog_sha256': sha(raw),
                                       'language': target, 'existing_value_sha256': sha(existing.encode()) if isinstance(existing, str) else None,
                                       'reason': reason, 'protected_chunks': fragments(protected[0]),
                                       'adapter_required': 'project_field_transport',
                                       'visibility': 'private' if catalogue_private or key in private_fields else 'public',
                                       'publication_allowed': False,
                                       'activation_allowed': False})
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            del candidates[candidate_start:]
            snapshot = snapshot_before_catalogue
            attention.append({'project': project['id'], 'source': relative, 'reason': str(error)})
    return candidates, snapshot, attention


def collect(config: dict, previous: dict | None = None) -> dict:
    previous = previous or {}
    old = previous.get('snapshot', {})
    # A missing or temporarily unreadable source is not permission to discard
    # its EN/DE baseline. Historical hashes stay until explicit reconciliation.
    snapshot = dict(old)
    catalog_snapshot = dict(previous.get('catalog_snapshot', {}))
    packages, attention, observed, observed_catalogues = [], [], set(), set()
    projects, notes = discover(config)
    attention.extend(notes)
    seen_ids = set()
    for project in projects:
        ident = project['id']
        if ident in seen_ids:
            raise ValueError('duplicate project ID')
        seen_ids.add(ident)
        root = Path(project['root'])
        kind = project.get('kind', 'readme')
        patterns = {'readme': ['README.md'], 'skills': ['skills/*/*/SKILL.md'],
                    'skills-flat': ['skills/*/SKILL.md']}
        if kind not in patterns:
            raise ValueError('unknown document adapter')
        sources = [p for pattern in patterns[kind] for p in sorted(root.glob(pattern))
                   if not excluded(p.relative_to(root))]
        jobs = []
        for source in sources:
            relative = source.relative_to(root).as_posix()
            key = ident + ':' + relative
            try:
                source = safe_path(root, relative)
                text = read_source(source)
                frontmatter = re.match(r'\A---\s*\n(.*?)\n---(?:\n|$)', text, re.S)
                if frontmatter and re.search(r'^status:\s*[\"\']?(?:archived|archiviert|archive|arc)[\"\']?\s*(?:#.*)?$', frontmatter[1], re.M | re.I):
                    continue
                declared_visibility = re.search(r'^visibility:[ \t]*([^\n]*)$', frontmatter[1], re.M | re.I) if frontmatter else None
                visibility = (declared_visibility[1].split(' #', 1)[0].strip().strip('\"\'').casefold()
                              if declared_visibility else project.get('source_visibility') or project.get('visibility'))
                unresolved_visibility = visibility != 'public'
                private_source = (visibility in PRIVATE_VISIBILITY or visibility == 'public potential'
                                  or unresolved_visibility or project.get('visibility') in PRIVATE_VISIBILITY)
                if private_source and project.get('allow_private') is not True:
                    attention.append({'project': ident, 'source': relative,
                                      'reason': 'source_visibility_review_required' if unresolved_visibility and visibility not in PRIVATE_VISIBILITY else 'private_source_excluded'})
                    continue
                language = source_language(text, project.get('source_language'))
                source_hash = sha(text.encode())
                targets = {}
                for target_language in LANGS:
                    target = (source if target_language == language else
                              source.with_name('SKILL.' + target_language + '.md') if kind.startswith('skills') else
                              source.with_name('README_' + target_language + '.md'))
                    if target == source:
                        continue
                    target_relative = target.relative_to(root).as_posix()
                    target = safe_path(root, target_relative)
                    # Preserve existing nested skill language conventions.
                    if kind.startswith('skills') and not target.exists():
                        nested = [source.parent / target_language / 'SKILL.md',
                                  source.parent / target_language.upper() / 'SKILL.md']
                        target = next((p for p in nested if p.is_file()), target)
                        target_relative = target.relative_to(root).as_posix()
                        target = safe_path(root, target_relative)
                    targets[target_language] = {
                        'path': target_relative,
                        'sha256': sha(bounded_bytes(target)) if target.is_file() else None,
                    }
                snapshot[key] = {'source_sha256': source_hash, 'source_language': language,
                                 'targets': targets}
                prior = old.get(key)
                protected = protect(text)
                chunks = fragments(protected[0], config.get('chunk_characters', 6000))
                secondary_changed = [lang for lang in ('en', 'de') if lang != language
                                     and prior and lang in prior['targets']
                                     and targets.get(lang, {}).get('sha256') != prior['targets'][lang]['sha256']]
                if not language or secondary_changed:
                    # Keep the last stable baseline until an exact-hash review
                    # resolves this conflict; another scan is not an approval.
                    reviewed = any(
                        review.get('project') == ident and review.get('source') == relative
                        and review.get('source_sha256') == source_hash
                        and review.get('target_hashes') == {lang: targets[lang]['sha256'] for lang in secondary_changed}
                        and bool(review.get('evidence'))
                        for review in config.get('source_reviews', []))
                    if language and secondary_changed and reviewed:
                        secondary_changed = []
                    else:
                        if prior:
                            snapshot[key] = prior
                        attention.append({'project': ident, 'source': relative,
                                          'reason': 'source_language_required' if not language else 'secondary_source_changed',
                                          'languages': secondary_changed,
                                          'source_sha256': source_hash, 'protected_chunks': chunks,
                                          'source_changed': bool(prior and source_hash != prior['source_sha256'])})
                        continue
                for lang, target in targets.items():
                    existing = safe_path(root, target['path'])
                    target_text = read_source(existing) if target['sha256'] else ''
                    provenance = re.search(r'[\"\']?translated_from_sha256[\"\']?\s*[:=]\s*[\"\']?([a-f0-9]{64})', target_text)
                    if provenance and provenance[1] == source_hash:
                        continue
                    jid = sha((relative + '\0' + lang + '\0' + source_hash).encode())[:40]
                    jobs.append({'id': jid, 'source': relative, 'target': target['path'], 'language': lang,
                                 'source_language': language, 'source_sha256': source_hash,
                                 'visibility': 'private' if private_source else 'public',
                                 'publication_allowed': False,
                                 'target_sha256': target['sha256'], 'source_text': text,
                                 'reason': 'missing' if target['sha256'] is None else 'stale' if provenance else 'provenance_review_required',
                                 'protected_chunks': [{'index': n, 'text': value, 'sha256': sha(value.encode())}
                                                      for n, value in enumerate(chunks)],
                                 'oversized_chunk': any(len(value) > config.get('chunk_characters', 6000) for value in chunks)})
            except (OSError, UnicodeError, ValueError) as error:
                if key in old:
                    snapshot[key] = old[key]
                else:
                    snapshot.pop(key, None)
                attention.append({'project': ident, 'source': relative, 'reason': str(error)})
            else:
                observed.add(key)
        catalogues, catalog_state, catalog_notes = catalogue_candidates(project, previous.get('catalog_snapshot', {}))
        catalog_snapshot.update(catalog_state)
        observed_catalogues.update(catalog_state)
        attention.extend(catalog_notes)
        packages.append({'project': ident, 'root': str(root), 'stars': project.get('stars'),
                         'eligibility_registry': project.get('eligibility_registry'),
                         'eligibility_registry_sha256': project.get('eligibility_registry_sha256'),
                         'catalogue_candidates': catalogues,
                         'views': project.get('views'), 'projection': {'schema': 'worldset-projection-v1',
                         'kind': kind, 'jobs': jobs, 'retained': [], 'current': []}})
    for key in sorted(set(old) - observed):
        attention.append({'source_reference': key, 'reason': 'source_removed_excluded_or_unavailable',
                          'baseline_preserved': True,
                          'cancel_executor_jobs_automatically': False})
    for key in sorted(set(previous.get('catalog_snapshot', {})) - observed_catalogues):
        attention.append({'source_reference': key, 'reason': 'catalogue_source_removed_excluded_or_unavailable',
                          'baseline_preserved': True, 'cancel_executor_jobs_automatically': False})
    def priority(package):
        stars, views = package['stars'], package['views']
        if any(value is not None and (type(value) is not int or value < 0) for value in (stars, views)):
            raise ValueError('priority metrics must be nonnegative integers or null')
        return (stars is None, -(stars or 0), views is None, -(views or 0), package['project'])
    packages.sort(key=priority)
    return {'schema': 'worldset-discovery-v1', 'configuration_sha256': configuration_hash(config),
            'snapshot': snapshot, 'catalog_snapshot': catalog_snapshot, 'packages': packages,
            'attention': attention, 'executor_state_owned_here': False, 'api_calls': 0,
            'translation_or_source_writes': 0, 'semantic_acceptance': False}


def select_documents(report: dict, project_id: str, limit: int, languages: list[str], config: dict | None = None) -> dict:
    """Export a bounded native projection, revalidating both sides before use."""
    if type(limit) is not int or limit < 1 or any(lang not in LANGS for lang in languages):
        raise ValueError('invalid selection limit or language')
    if config is None or configuration_hash(config) != report.get('configuration_sha256'):
        raise ValueError('current policy configuration is missing or changed; rescan')
    selected = [package for package in report['packages'] if package['project'] == project_id]
    if len(selected) != 1:
        raise ValueError('project is missing or ambiguous')
    package = selected[0]
    root = Path(package['root'])
    if root.is_symlink() or getattr(root, 'is_junction', lambda: False)():
        raise ValueError('linked project root after discovery')
    if package.get('eligibility_registry'):
        registry = Path(package['eligibility_registry'])
        if sha(bounded_bytes(registry, 8_388_608)) != package['eligibility_registry_sha256']:
            raise ValueError('eligibility registry changed after discovery; rescan')
    current_projects = [project for project in discover(config)[0] if project['id'] == project_id]
    if len(current_projects) != 1 or root.resolve() != Path(current_projects[0]['root']).resolve():
        raise ValueError('project eligibility or root changed after discovery')
    if excluded(root) or excluded(root.resolve()):
        raise ValueError('project is now excluded')
    jobs = [job for job in package['projection']['jobs'] if not languages or job['language'] in languages][:limit]
    for job in jobs:
        if job['language'] not in LANGS or job['id'] != sha((job['source'] + '\0' + job['language'] + '\0' + job['source_sha256']).encode())[:40]:
            raise ValueError('native document identity changed')
        if excluded(Path(job['source'])) or excluded(Path(job['target'])):
            raise ValueError('excluded source or target')
        current = read_source(safe_path(root, job['source']))
        if sha(current.encode()) != job['source_sha256'] or current != job['source_text']:
            raise ValueError('source changed after discovery; rescan')
        target = safe_path(root, job['target'])
        target_hash = sha(bounded_bytes(target)) if target.exists() else None
        if target_hash != job['target_sha256']:
            raise ValueError('target changed after discovery; rescan and review')
    return {**package['projection'], 'jobs': jobs}


def main():
    # Native checker subprocesses must not create bytecode in foreign tool trees.
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--input', type=Path, help='Existing discovery report for bounded native export')
    parser.add_argument('--policy-config', type=Path, help='Current configuration required for --input export')
    parser.add_argument('--project', help='Project ID to export from --input')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--languages', default='')
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--checker', type=Path)
    parser.add_argument('--fence-file', type=Path)
    parser.add_argument('--fence')
    parser.add_argument('--owner')
    args = parser.parse_args()
    if bool(args.config) == bool(args.input):
        parser.error('choose exactly one of --config or --input')
    if args.input:
        if not args.policy_config:
            parser.error('--input requires --policy-config for current eligibility/privacy revalidation')
        report = strict_json(args.input.read_text(encoding='utf-8'))
        current_policy = strict_json(args.policy_config.read_text(encoding='utf-8'))
        result = select_documents(report, args.project, args.limit,
                                  [lang for lang in args.languages.split(',') if lang], current_policy)
        projects = discover(current_policy)[0]
    else:
        config = strict_json(args.config.read_text(encoding='utf-8'))
        previous = strict_json(args.previous.read_text(encoding='utf-8')) if args.previous else None
        result = collect(config, previous)
        projects = discover(config)[0]
    if args.out:
        if not all((args.checker, args.fence_file, args.fence, args.owner)):
            parser.error('output requires the existing native writer checker and own fence')
        for project in projects:
            if args.out.resolve().is_relative_to(Path(project['root']).resolve()):
                parser.error('discovery output must not be inside a source project')
        check_writer(args.checker, args.out.parent, args.fence_file, args.fence, args.owner,
                     target=args.out)
        write_json(args.out, result)
    if args.input:
        print(json.dumps({'exported_jobs': len(result['jobs']), 'api_calls': 0}))
        return
    print(json.dumps({'projects': len(result['packages']), 'sources': len(result['snapshot']),
                      'target_demands': sum(len(p['projection']['jobs']) for p in result['packages']),
                      'catalogue_candidates': sum(len(p['catalogue_candidates']) for p in result['packages']),
                      'attention': len(result['attention']), 'api_calls': 0}))


if __name__ == '__main__':
    main()
