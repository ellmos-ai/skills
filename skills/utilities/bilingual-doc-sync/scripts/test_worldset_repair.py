"""Local, provider-free acceptance tests for the scratch repair candidate."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
SCRIPTS = Path(os.environ.get("WORLDSET_SCRIPTS", MODULE_DIR))
if not (SCRIPTS / "worldset.py").is_file():
    raise RuntimeError("set WORLDSET_SCRIPTS to the canonical scripts directory")
sys.path[:0] = [str(MODULE_DIR), str(SCRIPTS)]

import worldset_repair as repair
import worldset_review
from worldset import gates, sha

BATCH = "msgbatch_01OriginalFixture"
REPAIR_BATCH = "msgbatch_01RepairFixture"
REVIEW_ID = "a" * 40
REVIEW_JOB_ID = "b" * 40
STAMP = "2030-01-01T00:00:00+00:00"


class FakeAPI:
    def __init__(self, rows=None, fail_post=False):
        self.calls = []
        self.rows = rows
        self.fail_post = fail_post

    def call(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if method == "POST":
            if self.fail_post:
                raise TimeoutError("ambiguous provider timeout")
            return {"id": REPAIR_BATCH, "processing_status": "in_progress"}
        if path.endswith("/results"):
            return self.rows
        return {"processing_status": "ended", "ended_at": STAMP}


class RepairTests(unittest.TestCase):
    def setUp(self):
        self.assertEqual(
            Path(repair.__file__).resolve(),
            (MODULE_DIR / "worldset_repair.py").resolve(),
        )
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.root = self.workspace / "repo"
        self.root.mkdir()
        self.staging = self.workspace / "staging"
        self.staging.mkdir()
        self.source = (
            "---\nname: demo\ndescription: Verwende `--safe`.\nlanguage: de\n---\n"
            "# Ablauf\n- Nutze `--safe` für die Prüfung.\n"
            "Besuche https://example.com/help.\n\n"
            "```bash\necho ready\ntranslated_at: keep-body-value\n```\n"
        )
        source_file = self.root / "skills/demo/SKILL.md"
        source_file.parent.mkdir(parents=True)
        source_file.write_text(self.source, encoding="utf-8")
        source_hash = sha(self.source.encode())
        self.candidate = (
            '---\nname: demo\ndescription: "Use `--safe`."\nlanguage: en\n'
            f"translated_from_sha256: {source_hash}\n"
            'translator: "claude-haiku-5-5"\n'
            'translated_at: "2026-10-15T00:00:00+00:00"\n---\n'
            "# Procedure\n- Use `--safe` for the check.\n"
            "Read https://example.com/help.\n\n"
            "```bash\necho ready\ntranslated_at: keep-body-value\n```\n"
        )
        self.assertEqual(gates(self.source, self.candidate, "en"), [])
        review = {
            "id": REVIEW_ID,
            "source": "skills/demo/SKILL.md",
            "target": "skills/demo/SKILL.en.md",
            "language": "en",
            "source_sha256": source_hash,
            "candidate_sha256": sha(self.candidate.encode()),
            "reviewer_model": "claude-sonnet-5-5",
            "score": 4.7,
            "verdict": "approve",
            "fully_reviewed": True,
            "findings": [
                {
                    "severity": "minor",
                    "blocking": False,
                    "reason": "check wording",
                    "required_correction": "use inspect",
                }
            ],
        }
        original = {
            "id": REVIEW_JOB_ID,
            "translation_id": REVIEW_ID,
            "translation_batch_id": BATCH,
            "source": review["source"],
            "target": review["target"],
            "language": "en",
            "source_sha256": source_hash,
            "candidate_sha256": review["candidate_sha256"],
            "source_text": self.source,
            "candidate_text": self.candidate,
            "author_model": "claude-haiku-5-5",
            "source_group": "public",
        }
        decision = {
            "batch_id": BATCH,
            "id": REVIEW_ID,
            "source_sha256": source_hash,
            "candidate_sha256": review["candidate_sha256"],
            "decision": "hold",
            "operator_notes": "Use inspect instead of check in the prose.",
        }
        self.cases = [{"review": review, "job": original, "batch_id": BATCH}]
        self.decisions = [decision]
        self.projection = repair.prepare(self.cases, self.decisions, self.root)
        self.job = self.projection["jobs"][0]
        self.patch = {
            "patches": [{"old": "for the check", "new": "for the inspection"}]
        }

    def _html_material(self, source=None, body=None, metadata=None):
        source = source or (
            "# Setup Guide\n\n"
            "This guide explains how to inspect the package before installation.\n"
            "Use the `--safe` option to verify the source before installation.\n"
            "Open https://example.com/install for further instructions.\n"
            '<div class="notice">Inspect the package first.</div>\n'
        )
        body = body or (
            "# Einrichtungsanleitung\n\n"
            "Diese Anleitung erklärt, wie das Paket vor dem Einrichten geprüft wird.\n"
            "Nutze die Option `--safe`, um die Quelle vor der Installation zu prüfen.\n"
            "Weitere Hinweise stehen unter https://example.com/install.\n"
            '<div class="notice">Prüfe zuerst das Paket.</div>\n'
        )
        metadata = metadata or {
            "translated_from_sha256": sha(source.encode("utf-8")),
            "translator": "claude-haiku-5-5",
            "translated_at": "2026-10-15T18:09:04.533291+00:00",
        }
        return source, '<!-- worldset: ' + json.dumps(metadata, ensure_ascii=False) + ' -->\n' + body

    def _html_case(self, source, candidate, *, language="de", target="README.de.md"):
        source_file = self.root / "README.md"
        source_file.write_bytes(source.encode("utf-8"))
        review = copy.deepcopy(self.cases[0]["review"])
        review.update(
            source="README.md",
            target=target,
            language=language,
            source_sha256=sha(source.encode("utf-8")),
            candidate_sha256=sha(candidate.encode("utf-8")),
        )
        original = {
            "id": REVIEW_JOB_ID,
            "translation_id": REVIEW_ID,
            "translation_batch_id": BATCH,
            "source": review["source"],
            "target": review["target"],
            "language": review["language"],
            "source_sha256": review["source_sha256"],
            "candidate_sha256": review["candidate_sha256"],
            "source_text": source,
            "candidate_text": candidate,
            "author_model": "claude-haiku-5-5",
            "source_group": "public",
        }
        decision = copy.deepcopy(self.decisions[0])
        decision.update(
            source_sha256=review["source_sha256"],
            candidate_sha256=review["candidate_sha256"],
            batch_id=BATCH,
        )
        case = {"review": review, "job": original, "batch_id": BATCH}
        return [case], [decision]

    def test_prepare_binds_complete_review_feedback_and_source_group(self):
        job = self.job
        self.assertEqual(job["original_translation_id"], REVIEW_ID)
        self.assertEqual(
            job["id"],
            repair.repair_id(
                BATCH,
                REVIEW_ID,
                job["source_sha256"],
                job["base_candidate_sha256"],
                job["review_sha256"],
                job["repair_feedback"],
                job["source_group"],
            ),
        )
        self.assertEqual(job["source_text"], self.source)
        self.assertEqual(job["base_candidate_text"], self.candidate)
        self.assertEqual(job["review"], self.cases[0]["review"])
        self.assertEqual(job["repair_feedback"], self.decisions[0]["operator_notes"])
        self.assertEqual(job["source_group"], "public")
        self.assertEqual(job["protection_contract"], list(repair.protect(self.source)))

    def test_source_group_is_strict_and_frozen_into_repair_id(self):
        fields = [
            BATCH,
            REVIEW_ID,
            self.job["source_sha256"],
            self.job["base_candidate_sha256"],
            self.job["review_sha256"],
            "Feedback with \x00 separator",
            "public",
        ]
        expected = sha(
            json.dumps(fields, ensure_ascii=False, separators=(",", ":")).encode()
        )[:40]
        self.assertEqual(repair.repair_id(*fields), expected)
        for changed in ("private", "vendor"):
            stale = copy.deepcopy(self.job)
            stale["source_group"] = changed
            with (
                self.subTest(changed=changed),
                self.assertRaisesRegex(ValueError, "repair ID"),
            ):
                repair.validate_job(stale, self.root)
        stale = copy.deepcopy(self.job)
        stale["source_group"] = "unknown"
        with self.assertRaisesRegex(ValueError, "invalid source group"):
            repair.validate_job(stale, self.root)
        absent = copy.deepcopy(self.job)
        del absent["source_group"]
        absent["id"] = repair.repair_id(
            BATCH,
            REVIEW_ID,
            absent["source_sha256"],
            absent["base_candidate_sha256"],
            absent["review_sha256"],
            absent["repair_feedback"],
            None,
        )
        repair.validate_job(absent, self.root)
        absent["source_group"] = "public"
        with self.assertRaisesRegex(ValueError, "repair ID"):
            repair.validate_job(absent, self.root)

    def test_description_requires_json_quoted_scalar_before_and_after_patch(self):
        invalid = self.candidate.replace(
            'description: "Use `--safe`."',
            "description: bad: yaml `--safe`",
        )
        self.assertEqual(gates(self.source, invalid, "en"), [])
        patch = {
            "patches": [
                {
                    "old": 'description: "Use `--safe`."',
                    "new": "description: bad: yaml `--safe`",
                }
            ]
        }
        with self.assertRaisesRegex(ValueError, "JSON-quoted string scalar"):
            repair.apply_patches(self.job, patch, STAMP, self.root)
        stale = copy.deepcopy(self.job)
        stale["base_candidate_text"] = invalid
        stale["base_candidate_sha256"] = sha(invalid.encode())
        stale["review"]["candidate_sha256"] = stale["base_candidate_sha256"]
        stale["review_sha256"] = repair.review_hash(stale["review"])
        stale["operator_decision"]["candidate_sha256"] = stale["base_candidate_sha256"]
        stale["id"] = repair.repair_id(
            BATCH,
            REVIEW_ID,
            stale["source_sha256"],
            stale["base_candidate_sha256"],
            stale["review_sha256"],
            stale["repair_feedback"],
            stale["source_group"],
        )
        receipt = self.staging / "invalid-description.json"
        calls = []
        with self.assertRaisesRegex(ValueError, "JSON-quoted string scalar"):
            repair.submit(
                lambda: calls.append("API constructed"),
                {"schema": repair.REPAIR_SCHEMA, "jobs": [stale]},
                receipt,
                "claude-haiku-5-5",
                self.root,
            )
        self.assertEqual(calls, [])
        self.assertFalse(receipt.exists())

    def test_description_absence_and_escaped_json_are_explicit(self):
        source = "---\nname: demo\nlanguage: de\n---\nText.\n"
        without_description = "---\nname: demo\nlanguage: en\n---\nText.\n"
        repair.validate_description(source, without_description)
        with_description = without_description.replace(
            "language: en", 'description: "Added text."\nlanguage: en'
        )
        with self.assertRaisesRegex(ValueError, "description field"):
            repair.validate_description(source, with_description)
        repair.validate_description(
            self.source,
            self.candidate.replace('"Use `--safe`."', '"Use \\"--safe\\"."'),
        )

    def test_prepare_accepts_flat_frozen_input_and_rejects_stale_feedback_id(self):
        original = self.cases[0]["job"]
        direct = [
            {
                "batch_id": BATCH,
                "job": {
                    "id40": REVIEW_ID,
                    "source": original["source"],
                    "target": original["target"],
                    "language": original["language"],
                    "source_sha256": original["source_sha256"],
                    "target_sha256": None,
                    "source_text": original["source_text"],
                    "base_candidate_text": original["candidate_text"],
                    "base_candidate_sha256": original["candidate_sha256"],
                    "source_group": original["source_group"],
                    "author_model": original["author_model"],
                },
                "review": self.cases[0]["review"],
                "repair_feedback": self.decisions[0]["operator_notes"],
            }
        ]
        projection = repair.prepare(direct, None, self.root)
        self.assertEqual(projection["jobs"][0]["id"], self.job["id"])
        self.assertIsNone(projection["jobs"][0]["target_sha256"])
        stale = copy.deepcopy(projection["jobs"][0])
        stale["repair_feedback"] += " changed"
        with self.assertRaisesRegex(ValueError, "repair ID"):
            repair.validate_job(stale, self.root)
        stale = copy.deepcopy(projection["jobs"][0])
        stale["review"]["findings"][0]["reason"] = "changed after prepare"
        with self.assertRaisesRegex(ValueError, "complete semantic review hash"):
            repair.validate_job(stale, self.root)
        stale = copy.deepcopy(projection["jobs"][0])
        del stale["target_sha256"]
        with self.assertRaisesRegex(ValueError, "target_sha256 must be null"):
            repair.validate_job(stale, self.root)
        direct[0]["job"]["base_candidate_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "candidate hash mismatch"):
            repair.prepare(direct, None, self.root)

    def test_prepare_and_apply_real_html_readme_only_refreshes_timestamp(self):
        fixture_dir = MODULE_DIR / "fixtures"
        manifest = json.loads((fixture_dir / "manifest.json").read_text(encoding="ascii"))
        source = (fixture_dir / manifest["source_file"]).read_bytes().decode("utf-8")
        candidate = (fixture_dir / manifest["candidate_file"]).read_bytes().decode("utf-8")
        self.assertEqual(sha(source.encode("utf-8")), manifest["source_sha256"])
        self.assertEqual(sha(candidate.encode("utf-8")), manifest["candidate_sha256"])
        self.assertEqual(manifest["origin_group"], "public")
        self.assertEqual(manifest["language"], "pt")
        self.assertEqual(gates(source, candidate, manifest["language"]), [])
        cases, decisions = self._html_case(
            source,
            candidate,
            language=manifest["language"],
            target=manifest["target_path"],
        )
        projection = repair.prepare(cases, decisions, self.root)
        job = projection["jobs"][0]
        self.assertEqual(job["source"], "README.md")
        self.assertEqual(job["target"], manifest["target_path"])
        self.assertEqual(job["language"], manifest["language"])
        self.assertEqual(job["source_sha256"], sha(source.encode("utf-8")))
        self.assertEqual(job["base_candidate_text"], candidate)
        source_marker = "<!-- lang-only: zh -->\n"
        source_block = source.split(source_marker, 1)[1].split("\n", 1)[0]
        candidate_block = candidate.split(source_marker, 1)[1].split("\n", 1)[0]
        self.assertNotEqual(source_block, candidate_block)
        metadata_match = repair.HTML_PROVENANCE.match(candidate)
        self.assertIsNotNone(metadata_match)
        original_metadata = json.loads(metadata_match.group(1))
        patched = repair.apply_patches(
            job,
            {"patches": [{"old": candidate_block, "new": source_block}]},
            STAMP,
            self.root,
        )
        expected = candidate.replace(candidate_block, source_block, 1)
        expected = expected.replace(
            json.dumps(original_metadata["translated_at"]), json.dumps(STAMP), 1
        )
        self.assertEqual(patched, expected)
        metadata_match = repair.HTML_PROVENANCE.match(patched)
        self.assertIsNotNone(metadata_match)
        metadata = json.loads(metadata_match.group(1))
        self.assertEqual(
            set(metadata),
            {"translated_from_sha256", "translator", "translated_at"},
        )
        self.assertEqual(metadata["translated_from_sha256"], sha(source.encode("utf-8")))
        self.assertEqual(metadata["translator"], "claude-haiku-5-5")
        self.assertEqual(metadata["translated_at"], STAMP)
        repair.validate_description(source, patched)
        self.assertEqual(gates(source, patched, manifest["language"]), [])
        path_markup = '<a href="README.md"><img src="https://img.shields.io/badge/Language-English-2563eb"'
        self.assertEqual(candidate.count(path_markup), 1)
        with self.assertRaises(ValueError):
            repair.apply_patches(
                job,
                {
                    "patches": [
                        {
                            "old": path_markup,
                            "new": '<a href="README_other.md"><img src="https://img.shields.io/badge/Language-English-2563eb"',
                        }
                    ]
                },
                STAMP,
                self.root,
            )

    def test_prepare_rejects_missing_malformed_or_unbound_html_provenance(self):
        source, valid = self._html_material()
        match = repair.HTML_PROVENANCE.match(valid)
        self.assertIsNotNone(match)
        body = valid[match.end():]
        metadata = json.loads(match.group(1))
        wrong_hash = dict(metadata, translated_from_sha256="0" * 64)
        extra = dict(metadata, unexpected="value")
        empty_translator = dict(metadata, translator="  ")
        bad_timestamp = dict(metadata, translated_at="tomorrow")
        duplicate_key = (
            '{"translated_from_sha256": "' + metadata["translated_from_sha256"]
            + '", "translated_from_sha256": "' + metadata["translated_from_sha256"]
            + '", "translator": "' + metadata["translator"]
            + '", "translated_at": "' + metadata["translated_at"] + '"}'
        )
        candidates = {
            "missing": body,
            "malformed-json": "<!-- worldset: {not-json} -->\n" + body,
            "duplicate-json-key": "<!-- worldset: " + duplicate_key + " -->\n" + body,
            "wrong-source-hash": "<!-- worldset: " + json.dumps(wrong_hash) + " -->\n" + body,
            "extra-field": "<!-- worldset: " + json.dumps(extra) + " -->\n" + body,
            "empty-translator": "<!-- worldset: " + json.dumps(empty_translator) + " -->\n" + body,
            "invalid-timestamp": "<!-- worldset: " + json.dumps(bad_timestamp) + " -->\n" + body,
            "duplicate-comment": valid + "\n" + match.group(0) + body,
            "not-leading": " \n" + valid,
            "wrong-comment-shape": "<!-- worldset:" + match.group(1) + " -->\n" + body,
            "non-finite-json": "<!-- worldset: {\"translated_from_sha256\": NaN} -->\n" + body,
        }
        for name, candidate in candidates.items():
            with self.subTest(name=name):
                cases, decisions = self._html_case(source, candidate)
                with self.assertRaises(ValueError):
                    repair.prepare(cases, decisions, self.root)

    def test_html_and_frontmatter_modes_cannot_be_mixed(self):
        source, candidate = self._html_material()
        cases, decisions = self._html_case(self.source, candidate)
        with self.assertRaisesRegex(ValueError, "mixed frontmatter"):
            repair.prepare(cases, decisions, self.root)
        cases, decisions = self._html_case(source, self.candidate)
        with self.assertRaisesRegex(ValueError, "mixed frontmatter"):
            repair.prepare(cases, decisions, self.root)
        html_header = repair.HTML_PROVENANCE.match(candidate).group(0)
        cases, decisions = self._html_case(source, html_header + self.candidate)
        with self.assertRaisesRegex(ValueError, "mixed frontmatter"):
            repair.prepare(cases, decisions, self.root)

    def test_html_patches_cannot_change_provenance_or_protected_content(self):
        source, candidate = self._html_material()
        cases, decisions = self._html_case(source, candidate)
        job = repair.prepare(cases, decisions, self.root)["jobs"][0]
        metadata = json.loads(repair.HTML_PROVENANCE.match(candidate).group(1))
        attempts = [
            ('"translator": "claude-haiku-5-5"', '"translator": "other"'),
            (
                '"translated_from_sha256": "' + metadata["translated_from_sha256"] + '"',
                '"translated_from_sha256": "' + "0" * 64 + '"',
            ),
            (
                '"translated_at": "' + metadata["translated_at"] + '"',
                '"translated_at": "' + STAMP + '"',
            ),
            ("`--safe`", "`--unsafe`"),
            ("https://example.com/install", "https://other.example/install"),
            ('<div class="notice">', '<section class="notice">'),
            ("<!-- worldset:", "<!-- altered:"),
        ]
        for old, new in attempts:
            with self.subTest(old=old), self.assertRaises(ValueError):
                repair.apply_patches(job, {"patches": [{"old": old, "new": new}]}, STAMP, self.root)
        with self.assertRaisesRegex(ValueError, "timestamp"):
            repair.apply_patches(
                job,
                {"patches": [{"old": "vor dem Einrichten", "new": "vor der Installation"}]},
                "not-a-time",
                self.root,
            )

    def test_prepare_rejects_nan_score_unknown_path_and_bad_binding(self):
        cases = copy.deepcopy(self.cases)
        cases[0]["review"]["score"] = float("nan")
        with self.assertRaisesRegex(ValueError, "non-finite"):
            repair.prepare(cases, self.decisions, self.root)
        cases = copy.deepcopy(self.cases)
        cases[0]["review"]["target"] = "../escape.md"
        cases[0]["job"]["target"] = "../escape.md"
        with self.assertRaisesRegex(ValueError, "unsafe"):
            repair.prepare(cases, self.decisions, self.root)
        decisions = copy.deepcopy(self.decisions)
        decisions[0]["candidate_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "operator decision"):
            repair.prepare(self.cases, decisions, self.root)

    def test_submit_preflight_exclusive_receipt_and_native_batch(self):
        receipt = self.staging / "repair-batch.json"
        api = FakeAPI()
        result = repair.submit(
            lambda: api, self.projection, receipt, "claude-haiku-5-5", self.root
        )
        self.assertEqual(result["batch_id"], REPAIR_BATCH)
        self.assertEqual([call[0] for call in api.calls], ["POST"])
        frozen = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(frozen["schema"], "worldset-batch-v1")
        self.assertEqual(frozen["strategy"], repair.STRATEGY)
        with self.assertRaisesRegex(ValueError, "receipt exists"):
            repair.submit(
                lambda: api, self.projection, receipt, "claude-haiku-5-5", self.root
            )
        self.assertEqual(len(api.calls), 1)

    def test_submit_timeout_keeps_receipt_without_retry(self):
        receipt = self.staging / "repair-batch.json"
        api = FakeAPI(fail_post=True)
        with self.assertRaises(TimeoutError):
            repair.submit(
                lambda: api, self.projection, receipt, "claude-haiku-5-5", self.root
            )
        self.assertIsNone(json.loads(receipt.read_text(encoding="utf-8"))["batch_id"])
        with self.assertRaisesRegex(ValueError, "receipt exists"):
            repair.submit(
                lambda: api, self.projection, receipt, "claude-haiku-5-5", self.root
            )
        self.assertEqual(len(api.calls), 1)

    def test_submit_rejects_bad_hash_duplicate_and_traversal_before_api(self):
        for change in ("hash", "duplicate", "duplicate_target", "traversal"):
            with self.subTest(change=change):
                projection = copy.deepcopy(self.projection)
                if change == "hash":
                    projection["jobs"][0]["source_sha256"] = "0" * 64
                elif change == "duplicate":
                    projection["jobs"].append(copy.deepcopy(projection["jobs"][0]))
                elif change == "duplicate_target":
                    second = copy.deepcopy(projection["jobs"][0])
                    second["repair_feedback"] += " Another bounded correction."
                    second["id"] = repair.repair_id(
                        BATCH,
                        REVIEW_ID,
                        second["source_sha256"],
                        second["base_candidate_sha256"],
                        second["review_sha256"],
                        second["repair_feedback"],
                        second["source_group"],
                    )
                    second.pop("operator_decision")
                    projection["jobs"].append(second)
                else:
                    projection["jobs"][0]["id"] = "../../outside"
                receipt = self.staging / (change + ".json")
                calls = []

                def api_factory(calls=calls):
                    calls.append("constructed")
                    raise AssertionError("API must not be constructed")

                with self.assertRaises(ValueError):
                    repair.submit(
                        api_factory, projection, receipt, "claude-haiku-5-5", self.root
                    )
                self.assertEqual(calls, [])
                self.assertFalse(receipt.exists())

    def test_preflight_rejects_source_drift_existing_target_and_symlink(self):
        source_file = self.root / self.job["source"]
        target_file = self.root / self.job["target"]
        source_file.write_text(self.source + "\nchanged\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "repository source"):
            repair.validate_job(self.job, self.root)
        source_file.write_text(self.source, encoding="utf-8")
        target_file.write_text("already adopted", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "target already exists"):
            repair.validate_job(self.job, self.root)
        target_file.unlink()
        linked = self.root / "skills/linked"
        try:
            linked.symlink_to(source_file.parent, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks unavailable")
        stale = copy.deepcopy(self.job)
        stale["source"] = "skills/linked/SKILL.md"
        stale["review"]["source"] = stale["source"]
        with self.assertRaisesRegex(ValueError, "symlink"):
            repair.validate_job(stale, self.root)

    def test_apply_valid_patch_and_preserve_body_timestamp(self):
        text = repair.apply_patches(self.job, self.patch, STAMP, self.root)
        self.assertIn("for the inspection", text)
        self.assertIn("translated_at: keep-body-value", text)
        self.assertIn('translated_at: "' + STAMP + '"', text)
        self.assertEqual(gates(self.source, text, "en"), [])

    def test_apply_rejects_repeated_old_overlap_code_url_metadata_and_hash(self):
        cases = [
            {"patches": [{"old": "for the check", "new": "for inspection"}], "extra": True},
            {"patches": [{"old": "for the check", "new": "for inspection", "extra": True}]},
            {"patches": [{"old": "for the check"}]},
            {"patches": [{"old": "Use", "new": "Employ"}]},
            {
                "patches": [
                    {"old": "for the check", "new": "for inspection"},
                    {"old": "the check", "new": "inspection"},
                ]
            },
            {"patches": [{"old": "echo ready", "new": "echo unsafe"}]},
            {
                "patches": [
                    {
                        "old": "https://example.com/help",
                        "new": "https://other.example/help",
                    }
                ]
            },
            {"patches": [{"old": "language: en", "new": "language: fr"}]},
            {
                "patches": [
                    {
                        "old": 'translator: "claude-haiku-5-5"',
                        "new": 'translator: "other"',
                    }
                ]
            },
        ]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValueError):
                repair.apply_patches(self.job, data, STAMP, self.root)
        stale = copy.deepcopy(self.job)
        stale["base_candidate_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "frozen"):
            repair.apply_patches(stale, self.patch, STAMP, self.root)
        stale = copy.deepcopy(self.job)
        stale["protection_contract"] = []
        with self.assertRaisesRegex(ValueError, "protection"):
            repair.apply_patches(stale, self.patch, STAMP, self.root)

    def _receipt(self):
        receipt = self.staging / "repair-batch.json"
        repair.submit(
            lambda: FakeAPI(), self.projection, receipt, "claude-haiku-5-5", self.root
        )
        return receipt

    def _row(self, *, model="claude-haiku-5-5", stop="end_turn", identifier=None):
        return {
            "custom_id": identifier if identifier is not None else self.job["id"],
            "result": {
                "type": "succeeded",
                "message": {
                    "model": model,
                    "stop_reason": stop,
                    "content": [{"type": "text", "text": json.dumps(self.patch)}],
                    "usage": {},
                },
            },
        }

    def test_collect_writes_review_required_for_existing_full_review_pipeline(self):
        receipt = self._receipt()
        out = self.staging / "results"
        summary = repair.collect(
            lambda: FakeAPI(rows=[self._row()]), receipt, out, self.root
        )
        self.assertEqual(summary["counts"], {"review_required": 1})
        result = json.loads((out / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(result["batch_id"], REPAIR_BATCH)
        self.assertEqual(result["records"][0]["source_group"], "public")
        self.assertTrue((out / "candidates" / (self.job["id"] + ".md")).exists())
        reviews = worldset_review.prepare(receipt, out)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["author_model"], "claude-haiku-5-5")

    def test_collect_holds_wrong_model_and_truncation(self):
        receipt = self._receipt()
        for name, row in (
            ("model", self._row(model="claude-sonnet-5-5")),
            ("stop", self._row(stop="max_tokens")),
        ):
            with self.subTest(name=name):
                out = self.staging / name
                summary = repair.collect(
                    lambda row=row: FakeAPI(rows=[row]), receipt, out, self.root
                )
                self.assertEqual(summary["counts"], {"held": 1})
                self.assertFalse(
                    (out / "candidates" / (self.job["id"] + ".md")).exists()
                )

    def test_collect_accepts_native_thinking_and_redacted_thinking_before_text(self):
        receipt = self._receipt()
        for name, prelude in (
            (
                "thinking",
                {
                    "type": "thinking",
                    "thinking": "private reasoning",
                    "signature": "signed",
                },
            ),
            ("redacted", {"type": "redacted_thinking", "data": "opaque"}),
        ):
            with self.subTest(name=name):
                row = self._row()
                row["result"]["message"]["content"].insert(0, prelude)
                out = self.staging / name
                summary = repair.collect(
                    lambda row=row: FakeAPI(rows=[row]), receipt, out, self.root
                )
                self.assertEqual(summary["counts"], {"review_required": 1})
                self.assertTrue(
                    (out / "candidates" / (self.job["id"] + ".md")).exists()
                )

    def test_collect_holds_unknown_blocks_and_thinking_without_text(self):
        receipt = self._receipt()
        for name, content in (
            (
                "tool_use",
                [
                    {"type": "tool_use", "id": "tool-1"},
                    {"type": "text", "text": json.dumps(self.patch)},
                ],
            ),
            (
                "unknown",
                [
                    {"type": "future_block"},
                    {"type": "text", "text": json.dumps(self.patch)},
                ],
            ),
            (
                "thinking_only",
                [
                    {
                        "type": "thinking",
                        "thinking": "private reasoning",
                        "signature": "signed",
                    }
                ],
            ),
        ):
            with self.subTest(name=name):
                row = self._row()
                row["result"]["message"]["content"] = content
                out = self.staging / name
                summary = repair.collect(
                    lambda row=row: FakeAPI(rows=[row]), receipt, out, self.root
                )
                self.assertEqual(summary["counts"], {"held": 1})
                self.assertFalse(
                    (out / "candidates" / (self.job["id"] + ".md")).exists()
                )

    def test_collect_holds_duplicate_json_keys_and_nonfinite_response(self):
        receipt = self._receipt()
        for name, body in (
            ("duplicate", '{"patches":[],"patches":[]}'),
            ("nonfinite", '{"patches":NaN}'),
        ):
            with self.subTest(name=name):
                row = self._row()
                row["result"]["message"]["content"][0]["text"] = body
                out = self.staging / name
                summary = repair.collect(
                    lambda row=row: FakeAPI(rows=[row]), receipt, out, self.root
                )
                self.assertEqual(summary["counts"], {"held": 1})
                self.assertFalse(
                    (out / "candidates" / (self.job["id"] + ".md")).exists()
                )

    def test_collect_rejects_unknown_missing_duplicate_results_before_write(self):
        receipt = self._receipt()
        for name, rows in (
            ("unknown", [self._row(identifier="c" * 40)]),
            ("missing", []),
            ("duplicate", [self._row(), self._row()]),
        ):
            with self.subTest(name=name):
                out = self.staging / name
                with self.assertRaisesRegex(ValueError, "result IDs"):
                    repair.collect(
                        lambda rows=rows: FakeAPI(rows=rows), receipt, out, self.root
                    )
                self.assertFalse((out / "provider-results.json").exists())

    def test_collect_rejects_corrupt_receipt_before_api(self):
        receipt = self._receipt()
        batch = json.loads(receipt.read_text(encoding="utf-8"))
        batch["jobs"][0]["id"] = "../../outside"
        receipt.write_text(json.dumps(batch), encoding="utf-8")
        calls = []

        def api_factory():
            calls.append("constructed")
            raise AssertionError("API must not be constructed")

        with self.assertRaisesRegex(ValueError, "ID"):
            repair.collect(api_factory, receipt, self.staging / "out", self.root)
        self.assertEqual(calls, [])

    def test_python_optimized_mode_keeps_validation(self):
        code = (
            "import sys,copy,json; sys.path[:0]=json.loads(sys.argv[1]); "
            "import worldset_repair as r; j=json.loads(sys.argv[2]); "
            "j['source_sha256']='0'*64; "
            "\ntry: r.apply_patches(j,{'patches':[{'old':'for the check','new':'for inspection'}]},"
            "'2030-01-01T00:00:00+00:00',__import__('pathlib').Path(sys.argv[3]))"
            "\nexcept ValueError: print('rejected')"
            "\nelse: raise SystemExit('accepted in -O')"
        )
        process = subprocess.run(
            [
                sys.executable,
                "-B",
                "-O",
                "-c",
                code,
                json.dumps([str(MODULE_DIR), str(SCRIPTS)]),
                json.dumps(self.job),
                str(self.root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("rejected", process.stdout)


if __name__ == "__main__":
    unittest.main()
