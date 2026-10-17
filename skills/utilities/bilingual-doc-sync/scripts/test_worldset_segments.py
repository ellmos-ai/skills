import json
import tempfile
import unittest
from pathlib import Path

from worldset import sha
from worldset_segments import collect, fragments, submit, validate

SOURCE = '---\nname: demo\ndescription: Prüft die Dateien.\nlanguage: de\n---\n# Prüfen\n\n' + (
    'Prüfe die Dateien mit `tool --check`.\n\n' * 20) + '```python\nprint("Hallo")\n```\n'


def job():
    return dict(id='doc', source='SKILL.md', target='SKILL.de.md', language='de',
                source_sha256=sha(SOURCE.encode()), target_sha256=None, source_text=SOURCE)


class Fixture:
    def call(self, method, path, payload=None):
        if method == 'POST':
            self.requests = payload['requests']
            return dict(id='msgbatch_fixture', processing_status='in_progress')
        if not path.endswith('/results'):
            return dict(processing_status='ended')
        return [dict(custom_id=r['custom_id'], result=dict(type='succeeded', message=dict(
            model='fixture', stop_reason='end_turn', content=[dict(type='text', text=r['params']['messages'][0]['content']
            .split('<source_document>\n', 1)[1].rsplit('\n</source_document>', 1)[0])], usage=dict(output_tokens=10))))
            for r in self.requests]


class SegmentTests(unittest.TestCase):
    def test_fragment_projection_preserves_exact_bytes_and_whole_paragraphs(self):
        source = 'A' * 300 + '\n\n' + '| a | b |\n' * 100 + '\n\nEnd.\n'
        parts = fragments(source, 256)
        self.assertEqual(''.join(parts), source)
        self.assertTrue(any('| a | b |\n' * 100 in p for p in parts))
        loose = '1. ' + 'first ' * 60 + '\n\n2. ' + 'second ' * 60 + '\n'
        self.assertEqual(fragments(loose, 256), [loose])

    def test_complete_fragments_reconstruct_one_whole_document_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            api = Fixture()
            result = submit(api, dict(jobs=[job()]), root/'batch.json', 'fixture', size=256)
            self.assertGreater(result['fragments'], 1)
            result = collect(api, root/'batch.json', root/'out')
            self.assertEqual(result['counts'], dict(review_required=1))
            text = (root/'out/candidates/doc.md').read_text(encoding='utf-8')
            before = (root/'out/candidates/doc.md').read_bytes()
            collect(api, root/'batch.json', root/'out')
            self.assertEqual((root/'out/candidates/doc.md').read_bytes(), before)
            self.assertEqual(text.count('`tool --check`'), 20)
            self.assertIn('print("Hallo")', text)
            self.assertFalse((root/'SKILL.de.md').exists())

    def test_missing_truncated_or_marker_damaged_fragment_never_yields_candidate(self):
        class Broken(Fixture):
            mode = ''
            def call(self, method, path, payload=None):
                rows = super().call(method, path, payload)
                if path.endswith('/results'):
                    if self.mode == 'missing':
                        return rows[:-1]
                    if self.mode == 'truncated':
                        rows[-1]['result']['message']['stop_reason'] = 'max_tokens'
                    if self.mode == 'markers':
                        rows[-1]['result']['message']['content'][0]['text'] += 'ZXQPROTECT999999QXZ'
                    if self.mode == 'short':
                        rows[0]['result']['message']['content'][0]['text'] = 'First paragraph.'
                return rows
        for mode in ('missing', 'truncated', 'markers', 'short'):
            with tempfile.TemporaryDirectory() as d:
                root = Path(d)
                api = Broken()
                api.mode = mode
                submit(api, dict(jobs=[job()]), root/'batch.json', 'fixture', size=256)
                if mode == 'missing':
                    with self.assertRaises(ValueError):
                        collect(api, root/'batch.json', root/'out')
                else:
                    self.assertEqual(collect(api, root/'batch.json', root/'out')['counts'], dict(gate_failed=1))
                self.assertFalse((root/'out/candidates/doc.md').exists())

    def test_ambiguous_submission_is_reserved_and_fragment_paths_fail_closed(self):
        class Timeout(Fixture):
            def call(self, *args):
                raise TimeoutError('no response')
        with tempfile.TemporaryDirectory() as d:
            receipt = Path(d)/'batch.json'
            with self.assertRaises(TimeoutError):
                submit(Timeout(), dict(jobs=[job()]), receipt, 'fixture', size=256)
            with self.assertRaises(ValueError):
                submit(Timeout(), dict(jobs=[job()]), receipt, 'fixture', size=256)
            batch = json.loads(receipt.read_text(encoding='utf-8'))
            original = json.loads(receipt.read_text(encoding='utf-8'))
            a, b = batch['segments'][:2]
            a['id'], b['id'] = b['id'], a['id']
            with self.assertRaisesRegex(ValueError, 'does not bind'):
                validate(batch)
            batch = json.loads(json.dumps(original))
            values = batch['jobs'][0]['protection_contract'][1]
            values[0], values[1] = values[1], values[0]
            with self.assertRaisesRegex(ValueError, 'contract differs'):
                validate(batch)
            batch = original
            batch['segments'][0]['id'] = '../../escape'
            with self.assertRaises(ValueError):
                validate(batch)


if __name__ == '__main__':
    unittest.main()
