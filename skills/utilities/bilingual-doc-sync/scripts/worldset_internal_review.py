"""Import actual internal Luna reviews without a provider client or API receipt.

The orchestrator must verify the named agent's actual runtime assignment before
calling this importer. This module validates immutable input/evidence bindings;
it does not itself invoke a model or attest that an agent ran.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

MODEL = 'gpt-6-luna'
FIELDS = ('translation_id', 'translation_batch_id', 'source', 'target', 'language',
          'source_sha256', 'candidate_sha256')
HASH = re.compile(r'[0-9a-f]{64}\Z')
HANDLE = re.compile(r'msgbatch_[A-Za-z0-9_-]+\Z')
ID = re.compile(r'[A-Za-z0-9_-]{1,64}\Z')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def unique(items, key):
    result = {}
    for item in items:
        identity = key(item) if callable(key) else item[key]
        if identity in result:
            raise ValueError('duplicate review identity')
        result[identity] = item
    return result


def validate(projection_paths, evidence_path, expected_agent, auxiliary_paths=()):
    evidence_bytes = evidence_path.read_bytes()
    evidence = json.loads(evidence_bytes.decode('utf-8'))
    if (evidence.get('schema') != 'internal-luna-review-v1'
            or evidence.get('reviewer_model') != MODEL
            or evidence.get('reasoning_effort') != 'max'
            or evidence.get('execution_route') != 'internal-subagent'
            or evidence.get('agent_name') not in (expected_agent, expected_agent.rsplit('/', 1)[-1])
            or not expected_agent.startswith('/root/')
            or 'review_batch_id' in evidence):
        raise ValueError('unexpected internal reviewer identity or route')
    declared = evidence.get('inputs')
    if declared is None:
        declared = [{'path': evidence.get('input_path'), 'sha256': evidence.get('input_sha256')}]
    if not isinstance(declared, list) or not declared:
        raise ValueError('missing review input provenance')
    declared_by_path = {}
    for item in declared:
        path = str(Path(item['path']).resolve())
        if path in declared_by_path or not HASH.fullmatch(item['sha256']):
            raise ValueError('duplicate or invalid input declaration')
        declared_by_path[path] = item['sha256']
    all_paths = list(projection_paths) + list(auxiliary_paths)
    actual = {str(p.resolve()): sha(p.read_bytes()) for p in all_paths}
    if len(actual) != len(all_paths) or actual != declared_by_path:
        raise ValueError('reviewed input paths or bytes changed')
    jobs = unique([j for p in projection_paths for j in read(p)['jobs']], 'id')
    unique(evidence['reviews'], 'id')
    reviews = unique(evidence['reviews'], lambda r: (r['translation_batch_id'], r['translation_id']))
    expected_keys = {(j['translation_batch_id'], j['translation_id']) for j in jobs.values()}
    if not jobs or len(expected_keys) != len(jobs) or expected_keys != set(reviews):
        raise ValueError('review input/result set incomplete or foreign')
    grouped = defaultdict(list)
    native_ids = set()
    for identity, job in jobs.items():
        if (not ID.fullmatch(identity) or not ID.fullmatch(job['translation_id'])
                or not HANDLE.fullmatch(job['translation_batch_id'])
                or job['author_model'] == MODEL):
            raise ValueError('invalid translation identity or dependent reviewer')
        key = (job['translation_batch_id'], job['translation_id'])
        if key in native_ids:
            raise ValueError('duplicate native translation identity')
        native_ids.add(key)
        for text, digest in [('source_text', 'source_sha256'), ('candidate_text', 'candidate_sha256')]:
            if not HASH.fullmatch(job[digest]) or sha(job[text].encode('utf-8')) != job[digest]:
                raise ValueError('projection document hash mismatch')
        review = reviews[key]
        if (review.get('id') not in (identity, job['translation_id'])
                or any(review.get(k) != job[k] for k in FIELDS) or 'review_batch_id' in review):
            raise ValueError('review does not bind exact translation')
        score = review.get('score')
        findings = review.get('findings')
        if (type(score) not in (int, float) or not math.isfinite(score) or not 1 <= score <= 5
                or type(review.get('fully_reviewed')) is not bool
                or review.get('verdict') not in ('approve', 'reject')
                or not isinstance(findings, list)):
            raise ValueError('invalid quality assessment')
        for finding in findings:
            if (not isinstance(finding, dict)
                    or finding.get('severity') not in ('critical', 'major', 'minor')
                    or type(finding.get('blocking')) is not bool
                    or not isinstance(finding.get('reason'), str) or not finding['reason'].strip()
                    or not isinstance(finding.get('required_correction'), str)):
                raise ValueError('invalid quality finding')
        verdict = review['verdict']
        if (not review['fully_reviewed'] or score < 4.5
                or any(f['blocking'] or f['severity'] in ('critical', 'major') for f in findings)):
            verdict = 'reject'
        grouped[job['translation_batch_id']].append(dict(
            id=job['translation_id'], **{k: job[k] for k in FIELDS if not k.startswith('translation_')},
            reviewer_model=MODEL, reasoning_effort='max', execution_route='internal-subagent',
            reviewer_agent=expected_agent, review_evidence_sha256=sha(evidence_bytes),
            review_input_id=identity, evidence_review_id=review['id'],
            fully_reviewed=review['fully_reviewed'], score=score,
            verdict=verdict, findings=findings, operator_review_required=bool(findings),
            notes=json.dumps(findings, ensure_ascii=False)))
    return grouped, dict(schema='internal-luna-review-import-v1',
        reviewer_model=MODEL, reasoning_effort='max', execution_route='internal-subagent',
        reviewer_agent=expected_agent, evidence_path=str(evidence_path.resolve()),
        evidence_sha256=sha(evidence_bytes), inputs=actual,
        counts=dict(Counter(r['verdict'] for rows in grouped.values() for r in rows)),
        importer_sha256=sha(Path(__file__).read_bytes()))


def export(projections, evidence, expected_agent, out, auxiliary_paths=()):
    grouped, summary = validate(projections, evidence, expected_agent, auxiliary_paths)
    outputs = {out / ('reviews-' + handle + '.json'): dict(batch_id=handle, reviews=rows)
               for handle, rows in grouped.items()}
    outputs[out / 'summary.json'] = summary
    encoded = {p: (json.dumps(v, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
               for p, v in outputs.items()}
    # Validate the complete existing output set before the first write.
    if out.exists() and {p.name for p in out.iterdir()} - {p.name for p in encoded}:
        raise ValueError('foreign files in review import directory')
    for path, data in encoded.items():
        if path.exists() and path.read_bytes() != data:
            raise ValueError('existing internal review export differs')
    out.mkdir(parents=True, exist_ok=True)
    for path, data in encoded.items():
        if not path.exists():
            with path.open('xb') as stream:
                stream.write(data)
        if path.read_bytes() != data:
            raise ValueError('review import readback failed')
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--projection', action='append', type=Path, required=True)
    p.add_argument('--evidence', type=Path, required=True)
    p.add_argument('--aux-input', action='append', type=Path, default=[])
    p.add_argument('--expected-agent', required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(export(args.projection, args.evidence, args.expected_agent, args.out, args.aux_input)))


if __name__ == '__main__':
    main()
