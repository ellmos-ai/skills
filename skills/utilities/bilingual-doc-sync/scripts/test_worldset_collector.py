"""Recurring intake must retain the last successful snapshot on failed scans."""
import json
from types import SimpleNamespace

import pytest
import worldset_collector as collector


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    runtime = tmp_path / 'runtime'
    runtime.mkdir()
    project = tmp_path / 'project'
    project.mkdir()
    (project / 'README.md').write_text('# Example\n\nEnglish source.\n', encoding='utf-8')
    config = tmp_path / 'config.json'
    config.write_text(json.dumps({'projects': [{'id': 'app', 'root': str(project),
                                               'kind': 'readme', 'source_language': 'en',
                                               'source_visibility': 'public'}]}))
    tools = SimpleNamespace(active_locks_for_path=lambda p: [],
                            fence_status=lambda p, f: ('held', ''),
                            lock_applies_to_target=lambda p, t: True)
    monkeypatch.setattr(collector, 'load_tools', lambda p: tools)
    guards = []
    monkeypatch.setattr(collector, 'check_writer', lambda *args: guards.append(args))

    def claim(args, **kwargs):
        (runtime / 'LOCK.txt').write_text('fence: 17\n')
        return SimpleNamespace(returncode=0, stdout='created\nfence: 17\n')

    monkeypatch.setattr(collector.subprocess, 'run', claim)
    return SimpleNamespace(runtime=runtime, project=project, config=config,
                           tools=tools, guards=guards, lock_tools=tmp_path / 'tools')


def last_snapshot(runtime):
    receipt = json.loads((runtime / 'last-success.json').read_text(encoding='utf-8'))
    path = runtime / receipt['snapshot_file']
    return receipt, path.read_bytes()


def test_repeat_scan_retains_ids_and_releases_own_claim(fixture):
    f = fixture
    first = collector.run(f.config, f.runtime, f.lock_tools)
    first_receipt, snapshot = last_snapshot(f.runtime)
    second = collector.run(f.config, f.runtime, f.lock_tools)
    second_receipt, second_snapshot = last_snapshot(f.runtime)
    assert first['status'] == second['status'] == 'collected'
    assert first['document_jobs'] == 10
    assert snapshot == second_snapshot
    assert first_receipt['snapshot_file'] == second_receipt['snapshot_file']
    assert first['snapshot_sha256'] == second['snapshot_sha256']
    assert not (f.runtime / 'LOCK.txt').exists()
    assert len(f.guards) == 6
    assert json.loads((f.runtime / 'last-success.json').read_text())['api_calls'] == 0


def test_failed_collection_preserves_previous_snapshot_and_receipt(fixture, monkeypatch):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    old = {p.name: p.read_bytes() for p in f.runtime.iterdir()}
    monkeypatch.setattr(collector, 'collect', lambda *a: (_ for _ in ()).throw(ValueError('scan failed')))
    with pytest.raises(ValueError, match='scan failed'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert {p.name: p.read_bytes() for p in f.runtime.iterdir()} == old


def test_foreign_claim_skips_without_writes(fixture):
    f = fixture
    f.tools.active_locks_for_path = lambda p: ['foreign']
    assert collector.run(f.config, f.runtime, f.lock_tools)['status'] == 'skipped_locked'
    assert not list(f.runtime.iterdir())


def test_missing_source_root_preserves_snapshot(fixture):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    _, old = last_snapshot(f.runtime)
    (f.project / 'README.md').unlink()
    f.project.rmdir()
    assert collector.run(f.config, f.runtime, f.lock_tools)['status'] == 'skipped_missing_source_root'
    assert last_snapshot(f.runtime)[1] == old


def test_config_edit_during_scan_preserves_snapshot(fixture, monkeypatch):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    _, old = last_snapshot(f.runtime)
    original = collector.collect

    def changed(*args):
        result = original(*args)
        f.config.write_text('{}')
        return result

    monkeypatch.setattr(collector, 'collect', changed)
    with pytest.raises(ValueError, match='configuration changed'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert last_snapshot(f.runtime)[1] == old


def test_source_edit_during_collection_preserves_last_receipt(fixture, monkeypatch):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    old_receipt = (f.runtime / 'last-success.json').read_bytes()
    old_snapshot = last_snapshot(f.runtime)[1]
    original = collector.collect

    def changed(*args):
        report = original(*args)
        (f.project / 'README.md').write_text('# Example\n\nConcurrent edit.\n', encoding='utf-8')
        return report

    monkeypatch.setattr(collector, 'collect', changed)
    with pytest.raises(ValueError, match='source changed during collection'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert (f.runtime / 'last-success.json').read_bytes() == old_receipt
    assert last_snapshot(f.runtime)[1] == old_snapshot


def test_lost_fence_never_writes_or_removes_new_claim(fixture):
    f = fixture
    f.tools.fence_status = lambda p, fence: ('lost', '')
    with pytest.raises(ValueError, match='fence lost'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert not list(f.runtime.glob('discovery-*.json'))
    assert (f.runtime / 'LOCK.txt').is_file()


def test_runtime_inside_source_rejected(fixture):
    f = fixture
    runtime = f.project / 'runtime'
    runtime.mkdir()
    with pytest.raises(ValueError, match='outside source'):
        collector.run(f.config, runtime, f.lock_tools)


def test_expired_unowned_claim_is_not_cleaned(fixture):
    f = fixture
    lock = f.runtime / 'LOCK.txt'
    lock.write_text('foreign expired claim')
    assert collector.run(f.config, f.runtime, f.lock_tools)['status'] == 'skipped_existing_claim'
    assert lock.read_text() == 'foreign expired claim'


def test_claim_fence_must_match_native_command_receipt(fixture, monkeypatch):
    f = fixture

    def replaced_claim(args, **kwargs):
        (f.runtime / 'LOCK.txt').write_text('fence: 18\n')
        f.tools.fence_status = lambda path, fence: (
            ('held', '') if path.read_text().find(f'fence: {fence}') >= 0 else ('lost', ''))
        return SimpleNamespace(returncode=0, stdout='created\nfence: 17\n')

    monkeypatch.setattr(collector.subprocess, 'run', replaced_claim)
    with pytest.raises(ValueError, match='fence lost'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert not list(f.runtime.glob('discovery-*.json'))
    assert (f.runtime / 'LOCK.txt').read_text() == 'fence: 18\n'


def test_missing_registry_project_root_never_reports_success(fixture):
    f = fixture
    missing = f.runtime.parent / 'not-created'
    registry = f.runtime.parent / 'registry.json'
    registry.write_text(json.dumps({'projects': [{'name': 'missing-app', 'path': missing.name,
                                                   'visibility': 'public', 'lifecycle': 'active'}]}),
                        encoding='utf-8')
    config = json.loads(f.config.read_text(encoding='utf-8'))
    config['projects'] = []
    config['registries'] = [{'path': str(registry), 'source_language': 'en'}]
    f.config.write_text(json.dumps(config), encoding='utf-8')
    result = collector.run(f.config, f.runtime, f.lock_tools)
    assert result['status'] == 'skipped_missing_source_root'
    assert not (f.runtime / 'last-success.json').exists()
    assert not list(f.runtime.glob('discovery-*.json'))


def test_receipt_failure_keeps_previous_receipt_and_snapshot(fixture, monkeypatch):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    old_receipt = (f.runtime / 'last-success.json').read_bytes()
    receipt, old_snapshot = last_snapshot(f.runtime)
    (f.project / 'README.md').write_text('# Example\n\nUpdated source.\n', encoding='utf-8')
    original_write = collector.write_json

    def fail_receipt(path, value):
        if path.name == 'last-success.json':
            raise OSError('injected receipt failure')
        return original_write(path, value)

    monkeypatch.setattr(collector, 'write_json', fail_receipt)
    with pytest.raises(OSError, match='receipt failure'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert (f.runtime / 'last-success.json').read_bytes() == old_receipt
    after_receipt, after_snapshot = last_snapshot(f.runtime)
    assert after_receipt == receipt
    assert after_snapshot == old_snapshot


def test_unknown_visibility_holds_before_claim_or_snapshot(fixture):
    f = fixture
    config = json.loads(f.config.read_text(encoding='utf-8'))
    del config['projects'][0]['source_visibility']
    f.config.write_text(json.dumps(config), encoding='utf-8')
    result = collector.run(f.config, f.runtime, f.lock_tools)
    assert result['status'] == 'collected'
    receipt, snapshot = last_snapshot(f.runtime)
    report = json.loads(snapshot)
    assert not [job for package in report['packages'] for job in package['projection']['jobs']]
    assert report['attention'][0]['reason'] == 'source_visibility_review_required'
    assert not report['packages'][0]['projection']['jobs']


def test_receipt_snapshot_symlink_is_rejected(fixture, tmp_path):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    receipt = json.loads((f.runtime / 'last-success.json').read_text(encoding='utf-8'))
    target = f.runtime / receipt['snapshot_file']
    target.unlink()
    outside = tmp_path / 'outside.json'
    outside.write_text('{}', encoding='utf-8')
    try:
        target.symlink_to(outside)
    except OSError:
        pytest.skip('host cannot create symlinks')
    with pytest.raises(ValueError, match='linked runtime'):
        collector.run(f.config, f.runtime, f.lock_tools)



def test_new_skill_during_collection_preserves_last_receipt(fixture, monkeypatch):
    f = fixture
    config = json.loads(f.config.read_text(encoding='utf-8'))
    config['projects'][0]['kind'] = 'skills'
    f.config.write_text(json.dumps(config), encoding='utf-8')
    first = f.project / 'skills' / 'utilities' / 'existing' / 'SKILL.md'
    first.parent.mkdir(parents=True)
    first.write_text('---\nname: Existing\n---\nEnglish source.\n', encoding='utf-8')
    collector.run(f.config, f.runtime, f.lock_tools)
    old_files = {p.name: p.read_bytes() for p in f.runtime.iterdir()}
    original = collector.collect

    def changed(*args):
        report = original(*args)
        added = f.project / 'skills' / 'utilities' / 'added' / 'SKILL.md'
        added.parent.mkdir(parents=True)
        added.write_text('---\nname: Added\n---\nNew English source.\n', encoding='utf-8')
        return report

    monkeypatch.setattr(collector, 'collect', changed)
    with pytest.raises(ValueError, match='source inventory changed during collection'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert {p.name: p.read_bytes() for p in f.runtime.iterdir()} == old_files


def test_new_catalogue_during_collection_preserves_last_receipt(fixture, monkeypatch):
    f = fixture
    collector.run(f.config, f.runtime, f.lock_tools)
    old_files = {p.name: p.read_bytes() for p in f.runtime.iterdir()}
    original = collector.collect

    def changed(*args):
        report = original(*args)
        catalogue = f.project / 'locales' / 'translations.json'
        catalogue.parent.mkdir(parents=True)
        catalogue.write_text(json.dumps({'button': {'de': '\u00d6ffnen', 'en': 'Open'}}), encoding='utf-8')
        return report

    monkeypatch.setattr(collector, 'collect', changed)
    with pytest.raises(ValueError, match='source inventory changed during collection'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert {p.name: p.read_bytes() for p in f.runtime.iterdir()} == old_files


def test_unaccepted_catalogue_change_during_collection_is_detected(fixture, monkeypatch):
    f = fixture
    catalogue = f.project / 'locales' / 'translations.json'
    catalogue.parent.mkdir(parents=True)
    catalogue.write_text(json.dumps({'_meta': {'format': 1}}), encoding='utf-8')
    collector.run(f.config, f.runtime, f.lock_tools)
    old_files = {p.name: p.read_bytes() for p in f.runtime.iterdir()}
    original = collector.collect

    def changed(*args):
        report = original(*args)
        catalogue.write_text(json.dumps({'_meta': {'format': 2}}), encoding='utf-8')
        return report

    monkeypatch.setattr(collector, 'collect', changed)
    with pytest.raises(ValueError, match='source inventory changed during collection'):
        collector.run(f.config, f.runtime, f.lock_tools)
    assert {p.name: p.read_bytes() for p in f.runtime.iterdir()} == old_files
