import json
from pathlib import Path

import pytest
import worldset
import worldset_discovery
from worldset import protect
from worldset_discovery import collect, excluded, select_documents


def project(tmp_path, language='en'):
    root = tmp_path / 'project'
    root.mkdir()
    (root / 'README.md').write_text('# Example\n\nHello world.\n', encoding='utf-8')
    return root, {'projects': [{'id': 'example', 'root': str(root), 'source_language': language,
                                'source_visibility': 'public'}]}


def jobs(result):
    return [job for package in result['packages'] for job in package['projection']['jobs']]


def test_persisted_discovery_checks_the_exact_output_target(tmp_path, monkeypatch):
    _root, config = project(tmp_path)
    config_path = tmp_path / 'config.json'
    config_path.write_text(json.dumps(config), encoding='utf-8')
    runtime = tmp_path / 'runtime'
    runtime.mkdir()
    output = runtime / 'discovery.json'
    checker = tmp_path / 'lock_scan.py'
    fence = runtime / 'LOCK.txt'
    canonical_runtime = tmp_path / 'canonical-runtime'
    canonical_runtime.mkdir()
    checked_output = canonical_runtime / output.name
    checks = []
    writes = []
    monkeypatch.setattr(worldset_discovery, 'write_json',
                        lambda path, value: writes.append((path, value)))
    monkeypatch.setattr(worldset_discovery, 'check_writer',
                        lambda *args, **kwargs: (checks.append((args, kwargs)), checked_output)[1])
    monkeypatch.setattr('sys.argv', [
        'worldset_discovery.py', '--config', str(config_path), '--out', str(output),
        '--checker', str(checker), '--fence-file', str(fence), '--fence', '17', '--owner', 'fixture',
    ])

    worldset_discovery.main()

    assert checks == [((checker, output.parent, fence, '17', 'fixture'), {'target': output})]
    assert len(writes) == 1 and writes[0][0] == checked_output


def test_persisted_discovery_rejects_symlink_output_before_scanning(tmp_path, monkeypatch):
    _root, config = project(tmp_path)
    config_path = tmp_path / 'config.json'
    config_path.write_text(json.dumps(config), encoding='utf-8')
    runtime = tmp_path / 'runtime'
    runtime.mkdir()
    output = runtime / 'alias.json'
    referent = runtime / 'referent.json'
    referent.write_text('untouched', encoding='utf-8')
    try:
        output.symlink_to(referent)
        real_symlink = True
    except OSError:
        real_symlink = False
        monkeypatch.setattr(Path, 'is_symlink', lambda path: path == output)
    checker = tmp_path / 'lock_scan.py'
    fence = runtime / 'LOCK.txt'
    scanner_calls = []
    monkeypatch.setattr(worldset.subprocess, 'run',
                        lambda *args, **kwargs: scanner_calls.append((args, kwargs)))
    monkeypatch.setattr('sys.argv', [
        'worldset_discovery.py', '--config', str(config_path), '--out', str(output),
        '--checker', str(checker), '--fence-file', str(fence), '--fence', '17', '--owner', 'fixture',
    ])

    with pytest.raises(ValueError, match='writer target must not be a symlink'):
        worldset_discovery.main()

    assert not scanner_calls
    if real_symlink:
        assert output.is_symlink()
        assert referent.read_text(encoding='utf-8') == 'untouched'
    else:
        assert not output.exists()


def test_persisted_discovery_rechecks_source_boundary_after_path_normalization(tmp_path, monkeypatch):
    source_root, config = project(tmp_path)
    config_path = tmp_path / 'config.json'
    config_path.write_text(json.dumps(config), encoding='utf-8')
    runtime = tmp_path / 'runtime'
    runtime.mkdir()
    output = runtime / 'discovery.json'
    checked_output = source_root / 'discovery.json'
    writes = []
    monkeypatch.setattr(worldset_discovery, 'check_writer', lambda *args, **kwargs: checked_output)
    monkeypatch.setattr(worldset_discovery, 'write_json',
                        lambda path, value: writes.append((path, value)))
    monkeypatch.setattr('sys.argv', [
        'worldset_discovery.py', '--config', str(config_path), '--out', str(output),
        '--checker', str(tmp_path / 'lock_scan.py'), '--fence-file', str(runtime / 'LOCK.txt'),
        '--fence', '17', '--owner', 'fixture',
    ])

    with pytest.raises(SystemExit):
        worldset_discovery.main()

    assert not writes


def test_stable_ids_and_no_changes_to_source_or_targets(tmp_path):
    root, config = project(tmp_path)
    before = (root / 'README.md').read_bytes()
    one = collect(config)
    two = collect(config, one)
    assert len(jobs(one)) == 10
    assert jobs(one) == jobs(two)
    assert (root / 'README.md').read_bytes() == before
    assert list(root.iterdir()) == [root / 'README.md']
    assert one['api_calls'] == one['translation_or_source_writes'] == 0


def test_changed_source_invalidates_prior_job_hash(tmp_path):
    root, config = project(tmp_path)
    one = collect(config)
    (root / 'README.md').write_text('# Example\n\nChanged instruction.\n', encoding='utf-8')
    two = collect(config, one)
    assert {j['id'] for j in jobs(one)}.isdisjoint(j['id'] for j in jobs(two))


def test_new_skill_discovered_without_resubmitting_old_identity(tmp_path):
    config = {'projects': [{'id': 'skills', 'root': str(tmp_path), 'kind': 'skills'}]}
    source = tmp_path / 'skills' / 'utilities' / 'first' / 'SKILL.md'
    source.parent.mkdir(parents=True)
    source.write_text('---\nlanguage: de\nvisibility: public\n---\n# Erstes Werkzeug\n', encoding='utf-8')
    first = collect(config)
    new = source.parent.parent / 'second' / 'SKILL.md'
    new.parent.mkdir()
    new.write_text('---\nlanguage: en\nvisibility: public\n---\n# Second tool\n', encoding='utf-8')
    second = collect(config, first)
    assert len(jobs(second)) == 20
    assert {j['id'] for j in jobs(first)}.issubset(j['id'] for j in jobs(second))


@pytest.mark.parametrize('segment', ['.USR', '.USER', '.usr-private', '_USER', '_archive', 'ARC_Old', 'archiv', 'archiviert'])
def test_exclusions_apply_before_source_read(tmp_path, segment):
    root = tmp_path / segment / 'project'
    root.mkdir(parents=True)
    (root / 'README.md').write_bytes(b'\xff')
    result = collect({'projects': [{'id': 'excluded', 'root': str(root)}]})
    assert not result['packages'] and not result['snapshot']


def test_user_home_name_is_not_private_project_marker():
    assert not excluded(Path('Users') / 'User' / 'projects' / 'tool')


def test_archived_registry_entry_never_becomes_a_project(tmp_path):
    root, _ = project(tmp_path)
    registry = tmp_path / 'releases.json'
    registry.write_text(json.dumps({'projects': [
        {'name': 'archived', 'path': str(root), 'lifecycle': 'ARC'},
        {'name': 'also-archived', 'path': str(root), 'status': 'archiviert'},
    ]}), encoding='utf-8')
    assert collect({'registries': [{'path': str(registry)}]})['packages'] == []


def test_secondary_english_or_german_edit_stays_on_hold_across_runs(tmp_path):
    root, config = project(tmp_path)
    (root / 'README_de.md').write_text('# Beispiel\n', encoding='utf-8')
    baseline = collect(config)
    (root / 'README_de.md').write_text('# Verbesserte deutsche Fassung\n', encoding='utf-8')
    held = collect(config, baseline)
    held_again = collect(config, held)
    assert held['attention'][0]['reason'] == 'secondary_source_changed'
    assert not jobs(held) and not jobs(held_again)
    assert held_again['attention'] == held['attention']


def test_unknown_leading_language_is_not_guessed(tmp_path):
    _, config = project(tmp_path, None)
    result = collect(config)
    assert not jobs(result)
    assert result['attention'][0]['reason'] == 'source_language_required'


def test_chunks_reassemble_exact_protected_document(tmp_path):
    root, config = project(tmp_path)
    text = '# Guide\n\n' + ('A paragraph to translate.\n\n' * 40) + '```sh\npython --flag\n```\n'
    (root / 'README.md').write_text(text, encoding='utf-8')
    config['chunk_characters'] = 256
    job = jobs(collect(config))[0]
    assert ''.join(c['text'] for c in job['protected_chunks']) == protect(text)[0]
    assert len(job['protected_chunks']) > 1


def test_new_project_discovery_and_directory_limit(tmp_path):
    discovery = {'discovery_roots': [{'root': str(tmp_path), 'depth': 2, 'source_language': 'en',
                                      'source_visibility': 'public'}]}
    assert collect(discovery)['packages'] == []
    root = tmp_path / 'new-project'
    root.mkdir()
    (root / 'README.md').write_text('# New project\n', encoding='utf-8')
    assert len(jobs(collect(discovery))) == 10
    discovery['discovery_roots'][0]['max_directories'] = 1
    with pytest.raises(ValueError, match='bound'):
        collect(discovery)


def test_symlink_source_is_not_followed(tmp_path):
    root, config = project(tmp_path)
    (root / 'README.md').unlink()
    outside = tmp_path / 'outside.md'
    outside.write_text('# Private\n', encoding='utf-8')
    try:
        (root / 'README.md').symlink_to(outside)
    except OSError:
        pytest.skip('symlinks unavailable on this host')
    result = collect(config)
    assert not jobs(result)
    assert result['attention']


def test_runtime_catalogue_change_and_new_field_are_collected(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'button': {'de': 'Öffnen', 'en': 'Open'}}), encoding='utf-8')
    first = collect(config)
    original = first['packages'][0]['catalogue_candidates']
    assert len(original) == 10
    path.write_text(json.dumps({'button': {'de': 'Datei öffnen', 'en': 'Open'},
                                'save': {'de': 'Speichern'}}), encoding='utf-8')
    second = collect(config, first)
    changed = second['packages'][0]['catalogue_candidates']
    assert len(changed) == 20
    assert {r['id'] for r in original}.isdisjoint(r['id'] for r in changed)
    assert all(r['adapter_required'] == 'project_field_transport' and not r['activation_allowed']
               for r in changed)


def test_catalogue_secondary_edit_does_not_become_automatic_overwrite(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'button': {'de': 'Öffnen', 'en': 'Open'}}), encoding='utf-8')
    first = collect(config)
    path.write_text(json.dumps({'button': {'de': 'Öffnen', 'en': 'Open file'}}), encoding='utf-8')
    held = collect(config, first)
    assert not held['packages'][0]['catalogue_candidates']
    assert any(note['reason'] == 'secondary_catalogue_source_changed' for note in held['attention'])
    assert not collect(config, held)['packages'][0]['catalogue_candidates']


def test_typed_catalogue_preserves_mixed_en_de_sources(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'gui_translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'entries': [
        {'key': 'error', 'canonical_source_value': 'Request failed',
         'translations': {'en': 'Request failed', 'de': 'Anfrage fehlgeschlagen'}},
        {'key': 'open', 'canonical_source_value': 'Öffnen',
         'translations': {'en': 'Open', 'de': 'Öffnen'}},
    ]}), encoding='utf-8')
    rows = collect(config)['packages'][0]['catalogue_candidates']
    assert {r['source_language'] for r in rows} == {'en', 'de'}
    assert len(rows) == 20


def test_namespaced_bach_source_catalogue_adapter(tmp_path):
    root, config = project(tmp_path)
    path = root / 'de.json'
    path.write_text(json.dumps({'entries': {'cli': {'help': 'Hilfe anzeigen'}}}), encoding='utf-8')
    config['projects'][0]['catalogs'] = [{'path': 'de.json', 'shape': 'namespace-map', 'source_language': 'de'}]
    rows = collect(config)['packages'][0]['catalogue_candidates']
    assert len(rows) == 10
    assert rows[0]['source_pointer'] == '/entries/cli/help'


def test_collection_readme_does_not_hide_new_projects(tmp_path):
    (tmp_path / 'README.md').write_text('# Collection\n', encoding='utf-8')
    child = tmp_path / 'new-project'
    child.mkdir()
    (child / 'README.md').write_text('# Application\n', encoding='utf-8')
    result = collect({'discovery_roots': [{'root': str(tmp_path), 'depth': 1,
                                         'min_project_depth': 1, 'source_language': 'en'}]})
    assert len(result['packages']) == 1
    assert result['packages'][0]['root'] == str(child)


def test_unreviewed_discovered_readme_is_held_for_visibility(tmp_path):
    root = tmp_path / 'collection'
    project_root = root / 'new-project'
    project_root.mkdir(parents=True)
    (project_root / 'README.md').write_text(
        '<!-- source-language: en -->\n# New project\n', encoding='utf-8')
    result = collect({'discovery_roots': [{'root': str(root), 'depth': 1,
                                           'min_project_depth': 1}]})
    assert not jobs(result)
    assert result['attention'][0]['reason'] == 'source_visibility_review_required'


def test_unreviewed_catalogue_is_held_for_visibility(tmp_path):
    root, config = project(tmp_path)
    config['projects'][0].pop('source_visibility')
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'button': {'de': 'Öffnen', 'en': 'Open'}}), encoding='utf-8')
    result = collect(config)
    assert not result['packages'][0]['catalogue_candidates']
    assert any(item['reason'] == 'catalogue_visibility_review_required'
               for item in result['attention'])


def test_reviewed_public_localized_map_skips_metadata_envelope(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({
        '_meta': {'description': 'UI catalogue', 'format': 1, 'languages': ['en', 'de'],
                  'source': 'registry', 'instructions': 'Stable metadata.'},
        'button': {'de': 'Öffnen', 'en': 'Open'},
    }), encoding='utf-8')
    result = collect(config)
    assert len(result['packages'][0]['catalogue_candidates']) == 10
    assert not any(item['reason'] == 'unsupported localized-map entry'
                   for item in result['attention'])


def test_archived_skill_frontmatter_is_not_translated(tmp_path):
    skill = tmp_path / 'skills' / 'utilities' / 'old' / 'SKILL.md'
    skill.parent.mkdir(parents=True)
    skill.write_text('---\nlanguage: de\nstatus: archived\n---\n# Alt\n', encoding='utf-8')
    assert not jobs(collect({'projects': [{'id': 'skills', 'root': str(tmp_path), 'kind': 'skills'}]}))


def test_unclassified_project_still_has_reviewable_chunks(tmp_path):
    _, config = project(tmp_path, None)
    note = collect(config)['attention'][0]
    assert note['source_sha256'] and note['protected_chunks']


def test_explicit_reviewed_project_overrides_unclassified_discovery(tmp_path):
    root, config = project(tmp_path)
    config['discovery_roots'] = [{'root': str(tmp_path), 'depth': 1}]
    result = collect(config)
    assert len(result['packages']) == 1
    assert result['packages'][0]['project'] == 'example'
    assert len(jobs(result)) == 10


def test_small_export_is_native_and_rejects_changed_source_and_target(tmp_path):
    root, config = project(tmp_path)
    report = collect(config)
    selected = select_documents(report, 'example', 2, ['fr', 'hi'], config)
    assert selected['schema'] == 'worldset-projection-v1'
    assert len(selected['jobs']) == 2
    (root / 'README_fr.md').write_text('Concurrent change', encoding='utf-8')
    with pytest.raises(ValueError, match='target changed'):
        select_documents(report, 'example', 2, ['fr'], config)
    (root / 'README.md').write_text('New source', encoding='utf-8')
    with pytest.raises(ValueError, match='source changed'):
        select_documents(report, 'example', 2, ['hi'], config)


def test_priority_keeps_unknown_separate_from_zero(tmp_path):
    root, config = project(tmp_path)
    config['projects'][0]['stars'] = 0
    other = tmp_path / 'other'
    other.mkdir()
    config['projects'].append({'id': 'a-unknown', 'root': str(other), 'source_language': 'en'})
    report = collect(config)
    assert [p['project'] for p in report['packages']] == ['example', 'a-unknown']


def test_root_collection_readme_is_not_a_project_by_default(tmp_path):
    (tmp_path / 'README.md').write_text('# Collection', encoding='utf-8')
    child = tmp_path / 'application'
    child.mkdir()
    (child / 'README.md').write_text('# Application', encoding='utf-8')
    result = collect({'discovery_roots': [{'root': str(tmp_path), 'source_language': 'en'}]})
    assert len(result['packages']) == 1 and result['packages'][0]['root'] == str(child)


def test_duplicate_typed_catalogue_keys_are_held_without_colliding_ids(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'gui_translations.json'
    path.parent.mkdir()
    row = {'key': 'duplicate', 'canonical_source_value': 'Open', 'translations': {'en': 'Open'}}
    path.write_text(json.dumps({'entries': [row, row]}), encoding='utf-8')
    report = collect(config)
    assert not report['packages'][0]['catalogue_candidates']
    assert any('catalogue field key' in note['reason'] for note in report['attention'])


def test_archive_after_snapshot_invalidates_export(tmp_path):
    root, _ = project(tmp_path)
    registry = tmp_path / 'releases.json'
    row = {'name': 'project', 'path': str(root), 'status': 'released'}
    registry.write_text(json.dumps({'projects': [row]}), encoding='utf-8')
    config = {'registries': [{'path': str(registry), 'source_language': 'en'}]}
    report = collect(config)
    row['status'] = 'archived'
    registry.write_text(json.dumps({'projects': [row]}), encoding='utf-8')
    with pytest.raises(ValueError, match='registry changed'):
        select_documents(report, 'project', 1, ['fr'], config)
    assert not collect(config, report)['packages']


def test_explicit_project_cannot_override_archived_registry(tmp_path):
    root, config = project(tmp_path)
    registry = tmp_path / 'releases.json'
    registry.write_text(json.dumps({'projects': [{'name': 'project', 'path': str(root),
                                                'lifecycle': 'ARC'}]}), encoding='utf-8')
    config['registries'] = [{'path': str(registry)}]
    assert not collect(config)['packages']


def test_registry_path_cannot_escape_its_collection(tmp_path):
    collection = tmp_path / 'collection'
    collection.mkdir()
    outside = tmp_path / 'outside'
    outside.mkdir()
    (outside / 'README.md').write_bytes(b'\xff')
    registry = collection / 'releases.json'
    registry.write_text(json.dumps({'projects': [{'name': 'escape', 'path': '../outside'}]}), encoding='utf-8')
    report = collect({'registries': [{'path': str(registry)}]})
    assert not report['packages']
    assert report['attention'][0]['reason'] == 'registry_path_outside_collection'


def test_secondary_document_deletion_stays_on_hold(tmp_path):
    root, config = project(tmp_path)
    target = root / 'README_de.md'
    target.write_text('# Deutsch', encoding='utf-8')
    before = collect(config)
    target.unlink()
    held = collect(config, before)
    assert not jobs(held)
    assert held['attention'][0]['reason'] == 'secondary_source_changed'
    assert not jobs(collect(config, held))


def test_secondary_catalogue_deletion_stays_on_hold(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'label': {'de': 'Öffnen', 'en': 'Open'}}), encoding='utf-8')
    before = collect(config)
    path.write_text(json.dumps({'label': {'de': 'Öffnen'}}), encoding='utf-8')
    held = collect(config, before)
    assert not held['packages'][0]['catalogue_candidates']
    assert held['attention'][0]['reason'] == 'secondary_catalogue_source_changed'


@pytest.mark.parametrize('filename,data', [
    ('translations.json', []),
    ('gui_translations.json', {'entries': {}}),
    ('gui_translations.json', {'entries': [{'translations': []}]}),
])
def test_schema_drift_is_held_without_crashing_other_documents(tmp_path, filename, data):
    root, config = project(tmp_path)
    path = root / 'locales' / filename
    path.parent.mkdir()
    path.write_text(json.dumps(data), encoding='utf-8')
    result = collect(config)
    assert len(jobs(result)) == 10
    assert not result['packages'][0]['catalogue_candidates']
    assert result['attention']


def test_archived_registry_root_excludes_discovered_descendant(tmp_path):
    archived = tmp_path / 'old-project'
    nested = archived / 'nested'
    nested.mkdir(parents=True)
    (nested / 'README.md').write_bytes(b'\xff')
    registry = tmp_path / 'releases.json'
    registry.write_text(json.dumps({'projects': [{'name': 'old', 'path': str(archived),
                                                'status': 'archived'}]}), encoding='utf-8')
    config = {'registries': [{'path': str(registry)}],
              'discovery_roots': [{'root': str(tmp_path), 'depth': 3}]}
    result = collect(config)
    assert not result['packages']
    assert not result['snapshot']


@pytest.mark.parametrize('visibility', ['private-only', 'private profile', 'private-profile'])
def test_private_skill_metadata_requires_explicit_private_project_scope(tmp_path, visibility):
    source = tmp_path / 'skills' / 'utilities' / 'private-skill' / 'SKILL.md'
    source.parent.mkdir(parents=True)
    source.write_text('---\nlanguage: en\nvisibility: ' + visibility + '\n---\n# Private\n', encoding='utf-8')
    config = {'projects': [{'id': 'skills', 'root': str(tmp_path), 'kind': 'skills'}]}
    withheld = collect(config)
    assert not jobs(withheld)
    assert withheld['attention'][0]['reason'] == 'private_source_excluded'
    config['projects'][0]['allow_private'] = True
    allowed = jobs(collect(config))
    assert len(allowed) == 10
    assert all(job['visibility'] == 'private' and not job['publication_allowed'] for job in allowed)


def test_unsupported_or_conflicting_source_declaration_is_not_ignored(tmp_path):
    root, config = project(tmp_path)
    for declared in ('fr', 'de'):
        (root / 'README.md').write_text('---\nlanguage: ' + declared + '\n---\n# Source\n', encoding='utf-8')
        result = collect(config)
        assert not jobs(result) and result['attention']


def test_ambiguous_typed_source_is_held_until_language_is_explicit(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'gui_translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'entries': [{'key': 'stop', 'canonical_source_value': 'Stop',
                                            'translations': {'en': 'Stop', 'de': 'Stop'}}]}), encoding='utf-8')
    report = collect(config)
    assert not report['packages'][0]['catalogue_candidates']
    assert any(note['reason'] == 'catalogue_canonical_source_language_unresolved' for note in report['attention'])
    config['projects'][0]['catalogs'] = [{'path': 'locales/gui_translations.json', 'shape': 'entries-list',
                                        'source_language': 'en'}]
    rows = collect(config)['packages'][0]['catalogue_candidates']
    assert len(rows) == 10 and all(row['source_language'] == 'en' for row in rows)


def test_source_read_error_keeps_baseline_for_later_secondary_edit(tmp_path, monkeypatch):
    root, config = project(tmp_path)
    mate = root / 'README_de.md'
    mate.write_text('# Deutsch', encoding='utf-8')
    before = collect(config)
    original = worldset_discovery.read_source
    def unavailable(path, *args):
        if path == root / 'README.md':
            raise PermissionError('temporarily unavailable')
        return original(path, *args)
    with monkeypatch.context() as patch:
        patch.setattr(worldset_discovery, 'read_source', unavailable)
        held = collect(config, before)
    assert held['snapshot'] == before['snapshot']
    mate.write_text('# Neue deutsche Änderung', encoding='utf-8')
    assert not jobs(collect(config, held))


def test_unreadable_discovery_fails_without_replacing_successful_snapshot(tmp_path, monkeypatch):
    root, _ = project(tmp_path)
    config = {'discovery_roots': [{'root': str(tmp_path), 'source_language': 'en',
                                   'source_visibility': 'public'}]}
    before = collect(config)
    original = worldset_discovery.os.scandir
    def unavailable(path):
        if Path(path) == tmp_path:
            raise PermissionError('temporarily unavailable')
        return original(path)
    with monkeypatch.context() as patch:
        patch.setattr(worldset_discovery.os, 'scandir', unavailable)
        with pytest.raises(ValueError, match='previous successful snapshot'):
            collect(config, before)
    assert before['snapshot']


def test_catalogue_schema_error_preserves_secondary_baseline(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'label': {'de': 'Öffnen', 'en': 'Open'}}), encoding='utf-8')
    before = collect(config)
    path.write_text('[]', encoding='utf-8')
    broken = collect(config, before)
    assert broken['catalog_snapshot'] == before['catalog_snapshot']
    path.write_text(json.dumps({'label': {'de': 'Öffnen', 'en': 'Open file'}}), encoding='utf-8')
    held = collect(config, broken)
    assert not held['packages'][0]['catalogue_candidates']


def test_arc_skill_status_is_archived(tmp_path):
    source = tmp_path / 'skills' / 'utilities' / 'old' / 'SKILL.md'
    source.parent.mkdir(parents=True)
    source.write_text('---\nlanguage: en\nstatus: ARC\n---\n# Old\n', encoding='utf-8')
    result = collect({'projects': [{'id': 'skills', 'root': str(tmp_path), 'kind': 'skills'}]})
    assert not jobs(result)


def test_archive_name_does_not_need_matching_directory_name(tmp_path):
    root, config = project(tmp_path)
    config['projects'][0]['id'] = 'ARC_retired'
    assert not collect(config)['packages']


def test_export_rechecks_linked_project_root(tmp_path, monkeypatch):
    _, config = project(tmp_path)
    report = collect(config)
    original = Path.is_symlink
    root = Path(config['projects'][0]['root'])
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'is_symlink', lambda path: True if path == root else original(path))
        with pytest.raises(ValueError, match='linked project root'):
            select_documents(report, 'example', 1, ['fr'], config)


@pytest.mark.parametrize('visibility', ['', 'visibility: public potential\n'])
def test_unknown_or_potential_skill_visibility_is_not_public(tmp_path, visibility):
    source = tmp_path / 'skills' / 'utilities' / 'candidate' / 'SKILL.md'
    source.parent.mkdir(parents=True)
    source.write_text('---\nlanguage: en\n' + visibility + '---\n# Candidate\n', encoding='utf-8')
    config = {'projects': [{'id': 'skills', 'root': str(tmp_path), 'kind': 'skills'}]}
    result = collect(config)
    assert not jobs(result)
    assert result['attention'][0]['reason'] == 'source_visibility_review_required'
    config['projects'][0]['allow_private'] = True
    assert all(job['visibility'] == 'private' for job in jobs(collect(config)))


def test_policy_only_privacy_change_invalidates_old_export(tmp_path):
    _, config = project(tmp_path)
    report = collect(config)
    config['projects'][0]['visibility'] = 'private'
    with pytest.raises(ValueError, match='policy configuration'):
        select_documents(report, 'example', 1, ['fr'], config)


def test_removed_catalogue_source_is_visible_without_discarding_baseline(tmp_path):
    root, config = project(tmp_path)
    path = root / 'locales' / 'translations.json'
    path.parent.mkdir()
    path.write_text(json.dumps({'label': {'de': 'Öffnen'}}), encoding='utf-8')
    before = collect(config)
    path.write_text('{}', encoding='utf-8')
    after = collect(config, before)
    assert after['catalog_snapshot'] == before['catalog_snapshot']
    assert any(note['reason'] == 'catalogue_source_removed_excluded_or_unavailable'
               for note in after['attention'])


def test_cache_readme_is_not_a_new_software_project(tmp_path):
    cache = tmp_path / '.pytest_cache'
    cache.mkdir()
    (cache / 'README.md').write_bytes(b'\xff')
    report = collect({'discovery_roots': [{'root': str(tmp_path), 'depth': 1}]})
    assert not report['packages'] and not report['snapshot']
