import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from worldset import (
    apply_candidates,
    check_writer,
    collect,
    gates,
    params,
    protect,
    restore,
    retry_projection,
    safe_path,
    scan,
    sha,
    submit,
)

SOURCE = '''---
name: example
version: 1.0.0
description: >
  Prüft die Dateien.
language: de
visibility: public
---
# Prüfen

Prüfe die Dateien mit `tool --check`.

| Schritt | Ergebnis |
| --- | --- |
| Prüfen | Gut |

```python
print("Hallo")  # Kommentar
```

[Anleitung](https://example.org/doc)
'''


def english():
    text = protect(SOURCE)[0]
    for old, new in [('Prüft die Dateien.', 'Checks the files.'), ('Prüfen', 'Check'),
                     ('Prüfe die Dateien mit', 'Check the files with'), ('Schritt', 'Step'),
                     ('Ergebnis', 'Result'), ('Gut', 'Good'), ('Anleitung', 'Instructions')]:
        text = text.replace(old, new)
    return text


class TranslationTests(unittest.TestCase):
    def test_readme_source_language_override_retains_original(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'README.md').write_text('# Beschreibung\nDeutscher Text.\n', encoding='utf-8')
            plan = scan(root, 'readme', ['de', 'en'], source_language='de')
            self.assertEqual([j['target'] for j in plan['jobs']], ['README_en.md'])
            plan = scan(root, 'readme', ['de', 'en'], source_languages={'README.md': 'de'})
            self.assertEqual([j['target'] for j in plan['jobs']], ['README_en.md'])

    def test_nested_list_prose_is_not_mistaken_for_indented_code(self):
        source = '1. Pruefung\n   - Erster Schritt\n     * Nutze `tool` zum Testen.\n'
        target = '1. Check\n   - First step\n     * Use `tool` for testing.\n'
        self.assertEqual(gates(source, target, 'en'), [])
        self.assertIn('protected_regions_changed', gates(source, target.replace('`tool`', '`other`'), 'en'))

    def test_description_quoted_code_roundtrip_keeps_actual_value(self):
        source = '---\nname: example\ndescription: Verwende `class="clip"` und `data-*`.\nlanguage: de\n---\n# Titel\n'
        protected = protect(source)[0].replace('Verwende', 'Use').replace(' und ', ' and ').replace('Titel', 'Title')
        target = restore(source, protected, 'en', 'fixture', sha(source.encode()), translated_at='fixed')
        self.assertEqual(gates(source, target, 'en'), [])
        self.assertIn('protected_regions_changed', gates(source, target.replace('clip', 'wrong'), 'en'))

    def test_inline_values_keep_their_blockquote_and_list_containers(self):
        source = '> Warning: use `--force` with care.\n\nPlain explanation.\n'
        target = 'Warning: use `--force` with care.\n\n> Plain explanation.\n'
        self.assertIn('protected_region_context', gates(source, target, 'en'))
        source = '- Use `--force`.\n\n> Explain the risk.\n'
        target = '> Use `--force`.\n\n- Explain the risk.\n'
        self.assertIn('protected_region_context', gates(source, target, 'en'))

    def test_blank_space_line_does_not_change_list_marker_identity(self):
        source = '- First `one`\n  \n- Second `two`\n'
        target = '- First `one`\n\n- Second `two`\n'
        self.assertEqual(gates(source, target, 'en'), [])
        self.assertIn('list_items', gates(source, target.replace('- Second', '+ Second'), 'en'))

    def test_english_flat_vendor_sources_get_german_without_duplicate_legacy(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root/'skills/vendor'
            (p/'FR').mkdir(parents=True)
            (p/'SKILL.md').write_text('# English source\nUse the tool.\n', encoding='utf-8')
            (p/'FR/SKILL.md').write_text('Independent French text', encoding='utf-8')
            plan = scan(root, 'skills-flat', ['de', 'en', 'fr'], source_language='en')
            self.assertEqual([j['target'] for j in plan['jobs']], ['skills/vendor/SKILL.de.md'])
            self.assertEqual(plan['retained'], [str(Path('skills/vendor/FR/SKILL.md'))])
            self.assertEqual((p/'FR/SKILL.md').read_text(encoding='utf-8'), 'Independent French text')
            with self.assertRaisesRegex(ValueError, 'does not match'):
                scan(root, 'skills-flat', ['de', 'en'], source_languages={'skills/vendors/SKILL.md': 'en'})

    def test_output_limit_retry_increases_capacity_once(self):
        batch = dict(batch_id='a', jobs=[dict(id='x', max_output_tokens=24000)])
        result = dict(batch_id='a', records=[dict(id='x', status='gate_failed', stop_reason='max_tokens')])
        retry = retry_projection(batch, result)['jobs'][0]
        self.assertEqual(retry['max_output_tokens'], 64000)
        self.assertEqual(retry_projection(dict(batch_id='a', jobs=[retry]), result)['jobs'], [])
        full = dict(batch_id='a', jobs=[dict(id='x', max_output_tokens=128000)])
        self.assertEqual(retry_projection(full, result)['requires_segmentation'], ['x'])
        for value in (True, 0, 128001):
            with self.assertRaises(ValueError):
                params(dict(source_text='Text', language='en', max_output_tokens=value), 'fixture')

    def test_unmatched_backticks_do_not_hide_later_prose(self):
        source = 'Prüft jeden ```mermaid-Block.\n\n# Prüfen\n\nDie Dateien werden geprüft.\n\nJeder ```mermaid-Block zählt.\n'
        p, chunks, _ = protect(source)
        self.assertIn('Die Dateien werden geprüft.', p)
        self.assertFalse(any('Dateien' in c for c in chunks))
        p, chunks, _ = protect('Use `multi\nline code` here.\n')
        self.assertIn('`multi\nline code`', chunks)

    def test_bare_url_sentence_punctuation_and_balanced_parentheses(self):
        _, chunks, _ = protect('See https://example.org/a_(b). Also (https://example.org/x).\n')
        self.assertEqual(chunks, ['https://example.org/a_(b)', 'https://example.org/x'])

    def test_inline_identifiers_may_reorder_but_executable_blocks_may_not(self):
        src = 'Use `first` with `second`.\n'
        target = 'With `second`, use `first`.\n'
        self.assertEqual(gates(src, target, 'en'), [])
        src = '```sh\nfirst\n```\n\n```sh\nsecond\n```\n'
        target = '```sh\nsecond\n```\n\n```sh\nfirst\n```\n'
        self.assertIn('protected_region_order', gates(src, target, 'en'))

    def test_inline_values_cannot_move_to_a_different_paragraph(self):
        for first, second in [('`--force`', '`--dry-run`'), ('https://a.example', 'https://b.example')]:
            src = f'# Delete\n\nUse {first}.\n\n# Preview\n\nUse {second}.\n'
            target = f'# Delete\n\nUse {second}.\n\n# Preview\n\nUse {first}.\n'
            self.assertIn('protected_region_context', gates(src, target, 'en'))

    def test_escaped_backticks_remain_translatable_prose(self):
        text = r'Use \`Prüfen Sie alle Dateien und öffnen Sie das Protokoll ohne Freigabe\` during review.'
        p, chunks, _ = protect(text)
        self.assertIn('Prüfen Sie alle Dateien', p)
        self.assertFalse(any('Dateien' in c for c in chunks))
        self.assertIn('german_residue', gates(text, text, 'en'))

    def test_urls_end_at_cjk_punctuation_but_keep_empty_query(self):
        _, chunks, _ = protect('https://example.org/x。を参照してください。')
        self.assertEqual(chunks, ['https://example.org/x'])
        src = 'See https://example.org/search?\n'
        self.assertIn('protected_regions_changed', gates(src, src.replace('search?', 'search'), 'en'))

    def test_same_paragraph_link_target_swap_is_rejected(self):
        src = '[Delete](https://example.org/delete) and [Preview](https://example.org/preview).'
        target = '[Delete](https://example.org/preview) and [Preview](https://example.org/delete).'
        self.assertIn('protected_region_context', gates(src, target, 'en'))
        src = '---\nname: x\ndescription: "Delete via https://a.example/delete and preview via https://b.example/preview today."\n---\nBody.\n'
        target = src.replace('https://a.example/delete', 'TEMP').replace('https://b.example/preview', 'https://a.example/delete').replace('TEMP', 'https://b.example/preview')
        self.assertIn('protected_region_context', gates(src, target, 'en'))

    def test_roundtrip_protects_code_links_and_metadata(self):
        translated = restore(SOURCE, english(), 'en', 'fixture', sha(SOURCE.encode()))
        self.assertEqual(gates(SOURCE, translated, 'en'), [])
        self.assertIn('print("Hallo")  # Kommentar', translated)
        self.assertIn('version: 1.0.0', translated)
        self.assertIn('language: en', translated)
        self.assertIn('description: "Checks the files."', translated)

    def test_missing_duplicate_and_invented_markers_fail(self):
        for text in [english().replace('ZXQPROTECT000000QXZ', ''),
                     english() + 'ZXQPROTECT000000QXZ', english() + 'ZXQPROTECT999999QXZ']:
            with self.assertRaises(ValueError):
                restore(SOURCE, text, 'en', 'fixture', sha(SOURCE.encode()))

    def test_changed_code_and_wrong_script_fail(self):
        t = restore(SOURCE, english(), 'en', 'fixture', sha(SOURCE.encode()))
        self.assertIn('protected_regions_changed', gates(SOURCE, t.replace('print(', 'exec('), 'en'))
        self.assertIn('target_script', gates(SOURCE, t, 'ar'))
        self.assertIn('headings', gates(SOURCE, t.replace('# Check', 'Check'), 'en'))

    def test_scan_retains_legacy_and_detects_stale(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / 'skills/dev/example'
            p.mkdir(parents=True)
            (p / 'SKILL.md').write_text(SOURCE, encoding='utf-8')
            (p / 'SKILL.en.md').write_text('Human translation with independent additions', encoding='utf-8')
            (p / 'SKILL.ar.md').write_text('translated_from_sha256: old', encoding='utf-8')
            plan = scan(root, 'skills', ['de', 'en', 'ar', 'hi'], True)
            self.assertEqual([x['language'] for x in plan['jobs']], ['ar', 'hi'])
            self.assertEqual(len(plan['retained']), 1)
            self.assertIsNone(plan['jobs'][1]['target_sha256'])
            with self.assertRaises(ValueError):
                scan(root, 'skills', ['../en'])

    def test_ambiguous_submission_is_never_retried(self):
        class FailedAPI:
            def call(self, *args):
                raise TimeoutError('lost response')
        with tempfile.TemporaryDirectory() as d:
            receipt = Path(d) / 'batch.json'
            projection = {'jobs': [{'id': 'abc', 'language': 'en', 'source_text': SOURCE}]}
            with self.assertRaises(TimeoutError):
                submit(FailedAPI(), projection, receipt, 'fixture', 0)
            self.assertEqual(json.loads(receipt.read_text())['status'], 'submitting')
            with self.assertRaises(ValueError):
                submit(FailedAPI(), projection, receipt, 'fixture', 0)

    def test_truncated_provider_output_is_not_a_candidate(self):
        class FixtureAPI:
            def call(self, method, path, payload=None):
                if not path.endswith('/results'):
                    return {'processing_status': 'ended'}
                return [{'custom_id': 'abc', 'result': {'type': 'succeeded', 'message': {
                    'model': 'fixture', 'stop_reason': 'max_tokens',
                    'content': [{'type': 'text', 'text': english()}]}}}]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            receipt = root / 'receipt.json'
            receipt.write_text(json.dumps({'batch_id': 'msgbatch_fixture', 'jobs': [
                {'id': 'abc', 'target': 'SKILL.en.md', 'source_text': SOURCE, 'language': 'en',
                 'source_sha256': sha(SOURCE.encode())}]}))
            self.assertEqual(collect(FixtureAPI(), receipt, root / 'out')['counts'], {'gate_failed': 1})
            self.assertFalse((root / 'out/candidates/abc.md').exists())

    def test_concurrent_submit_posts_once(self):
        class FixtureAPI:
            calls = 0
            def call(self, *args):
                self.calls += 1
                return {'id': 'msgbatch_fixture', 'processing_status': 'in_progress'}
        with tempfile.TemporaryDirectory() as d:
            api = FixtureAPI()
            receipt = Path(d) / 'batch.json'
            projection = {'jobs': [{'id': 'abc', 'language': 'en', 'source_text': SOURCE}]}
            start = threading.Barrier(2)
            outcomes = []
            def worker():
                start.wait()
                try:
                    submit(api, projection, receipt, 'fixture', 0)
                    outcomes.append('ok')
                except (ValueError, FileExistsError):
                    outcomes.append('refused')
            ts = [threading.Thread(target=worker) for _ in range(2)]
            for t in ts:
                t.start()
            for t in ts:
                t.join()
            self.assertEqual(api.calls, 1)
            self.assertCountEqual(outcomes, ['ok', 'refused'])

    def test_complete_markdown_regions_and_description_code(self):
        fixtures = [
            SOURCE + '\n    print("Hallo")\n',
            SOURCE + '\n        print("Hallo")\n',
            SOURCE + '\n        print("Hallo")\n\nText.\n',
            SOURCE + '\nUse `[link](relative.md)` for examples.\n',
            SOURCE + '\n[Anleitung](relative.md "Text (title")\n',
            SOURCE + '\n```python\nprint("Hallo")\n````\n',
            SOURCE.replace('Prüft die Dateien.', 'Prüft `tool --check` Dateien.'),
            SOURCE + '\n[Anleitung](files/start_(de).md)\n',
            SOURCE.replace('language: de', '# metadata comment to preserve\nlanguage: de'),
        ]
        for source in fixtures:
            protected, _, _ = protect(source)
            translated = restore(source, protected, 'de', 'fixture', sha(source.encode()))
            self.assertEqual(gates(source, translated, 'de'), [])
            for old, new in [('print(', 'exec('), ('tool --check', 'tool --delete'),
                             ('start_(de).md', 'start_(de).html')]:
                if old in translated:
                    self.assertIn('protected_regions_changed', gates(source, translated.replace(old, new), 'de'))
            if '# metadata comment to preserve' in source:
                self.assertIn('# metadata comment to preserve\n', translated)

    def test_nested_list_is_translatable_prose(self):
        source = '- Erster Schritt\n    - Prüfe die Dateien zuerst und anschließend weitere Dateien.\n'
        protected, chunks, _ = protect(source)
        self.assertEqual(chunks, [])
        self.assertIn('Prüfe die Dateien', protected)

    def test_retry_is_bounded_and_batch_bound(self):
        batch = {'batch_id': 'a', 'jobs': [{'id': 'x'}, {'id': 'y', 'retry': True}]}
        results = {'batch_id': 'a', 'records': [{'id': 'x', 'status': 'gate_failed'}, {'id': 'y', 'status': 'gate_failed'}]}
        self.assertEqual([j['id'] for j in retry_projection(batch, results)['jobs']], ['x'])
        with self.assertRaises(ValueError):
            retry_projection(batch, dict(results, batch_id='b'))

    def test_apply_refuses_source_drift_target_race_and_stale_reviews(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'SKILL.md').write_text(SOURCE, encoding='utf-8')
            data = restore(SOURCE, english(), 'en', 'haiku-fixture', sha(SOURCE.encode())).encode()
            (root / 'candidates').mkdir()
            (root / 'candidates/abc.md').write_bytes(data)
            job = dict(id='abc', source='SKILL.md', target='SKILL.en.md', language='en',
                       source_sha256=sha(SOURCE.encode()), target_sha256=None)
            rec = dict(id='abc', status='review_required', candidate_sha256=sha(data), model='haiku-fixture', target='SKILL.en.md')
            review = dict(id='abc', verdict='approve', candidate_sha256=sha(data), source_sha256=job['source_sha256'],
                          reviewer_model='codex-fixture', score=4, source='SKILL.md', target='SKILL.en.md', language='en')
            for name, obj in [('batch.json', dict(batch_id='a', jobs=[job])),
                              ('results.json', dict(batch_id='a', records=[rec])),
                              ('reviews.json', dict(batch_id='a', reviews=[review]))]:
                (root/name).write_text(json.dumps(obj), encoding='utf-8')
            args = (root/'batch.json', root, root/'reviews.json', root, root/'checker.py', root/'LOCK.txt', '1', 'fixture')
            with patch('worldset.check_writer') as check:
                unresolved = dict(review, operator_review_required=True)
                (root/'reviews.json').write_text(json.dumps(dict(batch_id='a', reviews=[unresolved])), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'operator must resolve'):
                    apply_candidates(*args)
                self.assertFalse((root/'SKILL.en.md').exists())
                for score in [float('nan'), float('inf'), -1, 6, True]:
                    bad = dict(review, score=score)
                    (root/'reviews.json').write_text(json.dumps(dict(batch_id='a', reviews=[bad])), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'quality review'):
                        apply_candidates(*args)
                    self.assertFalse((root/'SKILL.en.md').exists())
                (root/'reviews.json').write_text(json.dumps(dict(batch_id='a', reviews=[review])), encoding='utf-8')
                (root/'SKILL.md').write_text(SOURCE+'changed', encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'source changed'):
                    apply_candidates(*args)
                (root/'SKILL.md').write_text(SOURCE, encoding='utf-8')
                (root/'candidates/abc.md').write_bytes(data+b'changed')
                with self.assertRaisesRegex(ValueError, 'review does not bind'):
                    apply_candidates(*args)
                (root/'candidates/abc.md').write_bytes(data)
                (root/'SKILL.en.md').write_text('concurrent author', encoding='utf-8')
                with self.assertRaises(FileExistsError):
                    apply_candidates(*args)
                self.assertEqual((root/'SKILL.en.md').read_text(), 'concurrent author')
                (root/'SKILL.en.md').unlink()
                self.assertEqual(apply_candidates(*args)['written'], ['SKILL.en.md'])
                self.assertEqual((root/'SKILL.en.md').read_bytes(), data)
                self.assertGreaterEqual(check.call_count, 3)

    def test_collect_keeps_utf8_source_bytes_on_windows(self):
        source = SOURCE.replace('Kommentar', 'Änderung')
        class FixtureAPI:
            def call(self, method, path, payload=None):
                if not path.endswith('/results'):
                    return {'processing_status': 'ended'}
                return [{'custom_id': 'abc', 'result': {'type': 'succeeded', 'message': {
                    'model': 'fixture', 'stop_reason': 'end_turn',
                    'content': [{'type': 'text', 'text': english()}]}}}]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            receipt = root/'receipt.json'
            receipt.write_text(json.dumps({'batch_id': 'msgbatch_fixture', 'jobs': [dict(
                id='abc', source_text=source, target='SKILL.en.md', language='en',
                source_sha256=sha(source.encode()))]}, ensure_ascii=False), encoding='utf-8')
            self.assertEqual(collect(FixtureAPI(), receipt, root/'out')['counts'], {'review_required': 1})
            self.assertIn('# Änderung', (root/'out/candidates/abc.md').read_text(encoding='utf-8'))

    def test_lock_scanner_missing_fields_foreign_locks_and_changed_fence_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            fence = root/'LOCK.txt'
            fence.write_text('owner: fixture\nfence: 1\n', encoding='utf-8')
            data = dict(checked=str(root), twin_status='ok', descendants_complete=True,
                        hook_guards=[], locks=[{'path': str(fence)}])
            from types import SimpleNamespace
            with patch('worldset.subprocess.run') as run:
                run.return_value = SimpleNamespace(returncode=1, stdout=json.dumps(data))
                check_writer(root/'checker.py', root, fence, '1', 'fixture')
                for bad in [dict(data, hook_guards=None), dict(data, checked='wrong'),
                            dict(data, locks=[{'path': str(root/'FOREIGN.txt')}]),
                            dict(data, descendants_complete=False)]:
                    run.return_value = SimpleNamespace(returncode=1, stdout=json.dumps(bad))
                    with self.assertRaises(ValueError):
                        check_writer(root/'checker.py', root, fence, '1', 'fixture')
                run.return_value = SimpleNamespace(returncode=1, stdout=json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'fence changed'):
                    check_writer(root/'checker.py', root, fence, '2', 'fixture')

    def test_broken_target_symlink_does_not_redirect_writes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            link = root/'SKILL.en.md'
            try:
                link.symlink_to(root/'unreviewed.md')
            except OSError as e:
                self.skipTest(f'host lacks symlink permission: {e}')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                safe_path(root, 'SKILL.en.md')
            self.assertFalse((root/'unreviewed.md').exists())


if __name__ == '__main__':
    unittest.main()
