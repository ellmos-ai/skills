import json
import tempfile
import unittest
from pathlib import Path

from worldset import sha
from worldset_review import assess, collect, submit


def job():
    return dict(id='review1', translation_id='original1', translation_batch_id='msgbatch_original',
        source='SKILL.md', target='SKILL.fr.md', language='fr', source_sha256=sha('Quelle'.encode()),
        candidate_sha256=sha('Cible'.encode()), author_model='claude-haiku-fixture',
        source_text='Quelle', candidate_text='Cible')


def message(**changes):
    d = dict(fully_reviewed=True, score=4.5, verdict='approve', findings=[])
    d.update(changes)
    return dict(stop_reason='end_turn', model='claude-sonnet-fixture', content=[dict(type='text', text=json.dumps(d))])


class ReviewTests(unittest.TestCase):
    def test_non_object_json_and_wrong_reviewer_model_are_rejected(self):
        for body in ('[]', 'null', '42'):
            m = message()
            m['content'][0]['text'] = body
            with self.assertRaises(ValueError):
                assess(job(), m, 'msgbatch_review', 'claude-sonnet-fixture')
        m = message()
        m['model'] = 'claude-haiku-other'
        with self.assertRaises(ValueError):
            assess(job(), m, 'msgbatch_review', 'claude-sonnet-fixture')

    def test_unsafe_receipt_id_rejected_before_network_or_file_write(self):
        class NoNetwork:
            def call(self, *args):
                self.fail('must validate before network')
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            j = job()
            j['id'] = '../../escape'
            receipt = root/'receipt.json'
            receipt.write_text(json.dumps(dict(batch_id='msgbatch_review', model='claude-sonnet-fixture', jobs=[j])), encoding='utf-8')
            with self.assertRaises(ValueError):
                collect(NoNetwork(), receipt, root/'out')
            self.assertFalse((root/'out').exists())
            self.assertFalse((root/'escape.json').exists())

    def test_approval_is_bound_to_actual_candidate_source_paths_and_model(self):
        j = job()
        review = assess(j, message(), 'msgbatch_review', 'claude-sonnet-fixture')
        self.assertEqual(review['candidate_sha256'], j['candidate_sha256'])
        self.assertEqual(review['source_sha256'], j['source_sha256'])
        self.assertEqual(review['target'], j['target'])
        self.assertEqual(review['reviewer_model'], 'claude-sonnet-fixture')
        self.assertEqual(review['verdict'], 'approve')

    def test_major_finding_incomplete_read_and_low_score_override_approval(self):
        finding = dict(severity='major', blocking=True, reason='Added free of charge', required_correction='Use voluntarily')
        for change in [dict(findings=[finding]), dict(findings=[dict(finding, severity='minor')]), dict(fully_reviewed=False), dict(score=4.4)]:
            self.assertEqual(assess(job(), message(**change), 'msgbatch_review', 'claude-sonnet-fixture')['verdict'], 'reject')

    def test_invalid_scores_truncated_same_model_and_bad_json_are_held(self):
        for score in [float('nan'), float('inf'), True, 0, 6]:
            with self.assertRaises(ValueError):
                assess(job(), message(score=score), 'msgbatch_review', 'claude-sonnet-fixture')
        for field, value in [('stop_reason', 'max_tokens'), ('model', 'claude-haiku-fixture')]:
            m = message()
            m[field] = value
            with self.assertRaises(ValueError):
                assess(job(), m, 'msgbatch_review', 'claude-sonnet-fixture')
        m = message()
        m['content'][0]['text'] = 'not JSON'
        with self.assertRaises(ValueError):
            assess(job(), m, 'msgbatch_review', 'claude-sonnet-fixture')

    def test_submission_timeout_is_reserved_and_not_retried(self):
        class Failure:
            def call(self, *args):
                raise TimeoutError('lost response')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'receipt.json'
            with self.assertRaises(TimeoutError):
                submit(Failure(), dict(jobs=[job()]), p, 'claude-sonnet-fixture')
            with self.assertRaises(ValueError):
                submit(Failure(), dict(jobs=[job()]), p, 'claude-sonnet-fixture')

    def test_collect_groups_reviews_by_original_batch_and_never_applies(self):
        class Fixture:
            def call(self, method, path, payload=None):
                if not path.endswith('/results'):
                    return dict(processing_status='ended')
                return [dict(custom_id='review1', result=dict(type='succeeded', message=message()))]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            receipt = root/'receipt.json'
            receipt.write_text(json.dumps(dict(batch_id='msgbatch_review', model='claude-sonnet-fixture', jobs=[job()])), encoding='utf-8')
            result = collect(Fixture(), receipt, root/'out')
            self.assertEqual(result['counts'], dict(approve=1))
            r = json.loads((root/'out/reviews-msgbatch_original.json').read_text(encoding='utf-8'))
            self.assertEqual(r['batch_id'], 'msgbatch_original')
            self.assertEqual(r['reviews'][0]['id'], 'original1')
            self.assertFalse((root/'SKILL.fr.md').exists())


if __name__ == '__main__':
    unittest.main()
