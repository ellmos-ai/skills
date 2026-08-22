import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
MODULE_PATH = SKILL_ROOT / "scripts" / "bridge.py"
SPEC = importlib.util.spec_from_file_location("agents_bridge", MODULE_PATH)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


def fixture(name):
    root = FIXTURES / name
    return BRIDGE.load_profile(root / "profile.json"), root / "source"


class CompatibilityTests(unittest.TestCase):
    def test_discovery_marks_existing_surface(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / "CLAUDE.md").write_text("# rules", encoding="utf-8")
            surfaces = BRIDGE.candidate_surfaces(home)
        claude = next(item for item in surfaces if item["provider_hint"] == "claude")
        self.assertTrue(claude["exists"])

    def test_render_preserves_explicit_order(self):
        output = BRIDGE.render_loader(["first.md", "second.md"], "p1", "codex")
        self.assertLess(output.index("first.md"), output.index("second.md"))

    def test_render_rejects_empty_truth(self):
        with self.assertRaises(ValueError):
            BRIDGE.render_loader([], "p1", "generic")


class ProfileAndDiscoveryTests(unittest.TestCase):
    def test_profiles_validate_and_reject_absolute_paths(self):
        profile, _ = fixture("claude-primary")
        self.assertEqual(BRIDGE.validate_profile(profile)["schema"], BRIDGE.PROFILE_SCHEMA)
        for absolute in ("X:/private/CLAUDE.md", "/private/CLAUDE.md"):
            invalid = copy.deepcopy(profile)
            invalid["primary_surface"]["path"] = absolute
            with self.subTest(absolute=absolute):
                with self.assertRaisesRegex(BRIDGE.BridgeError, "relative and portable"):
                    BRIDGE.validate_profile(invalid)

    def test_profile_rejects_a_second_primary_strategy(self):
        profile, _ = fixture("claude-primary")
        profile["provider_surfaces"][1]["strategy"] = "primary"
        with self.assertRaisesRegex(BRIDGE.BridgeError, "exactly one primary"):
            BRIDGE.validate_profile(profile)

    def test_discover_selects_explicit_claim_without_provider_default(self):
        _, source = fixture("claude-primary")
        result = BRIDGE.discover_instance(source)
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["decision"]["primary_surface"]["path"], "CLAUDE.md")

    def test_discover_conflicting_claims_fails_closed(self):
        result = BRIDGE.discover_instance(FIXTURES / "conflicting-authority")
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(len(result["decision_briefing"]["candidates"]), 2)
        self.assertIn("No filename", result["decision_briefing"]["selection_policy"])


class CaptureRestoreTests(unittest.TestCase):
    def _roundtrip(self, fixture_name):
        profile, source = fixture(fixture_name)
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            package = temp / "package"
            target = temp / "target"
            receipt = temp / "receipt.json"
            manifest = BRIDGE.capture_instance(profile, source, package)
            self.assertFalse(manifest["source_root_included"])
            self.assertFalse(manifest["privacy"]["secrets_included"])
            plan = BRIDGE.plan_restore(package, target)
            self.assertEqual(plan["status"], "change-required")
            restored = BRIDGE.restore_instance(package, target, backup_root=temp / "backup", receipt_path=receipt)
            self.assertEqual(restored["status"], "restored")
            self.assertEqual(BRIDGE.verify_target(package, target)["status"], "verified")
            self.assertEqual(BRIDGE.plan_restore(package, target)["status"], "idempotent")
            for surface in ("AGENTS.md", "GPT.md", "CLAUDE.md", "GEMINI.md"):
                self.assertTrue((target / surface).is_file())
                self.assertEqual((target / surface).read_bytes(), (package / "files" / surface).read_bytes())
            self.assertEqual(BRIDGE.memory_status(profile, target)["status"], "ready")
            return manifest

    def test_claude_primary_roundtrip(self):
        manifest = self._roundtrip("claude-primary")
        paths = {entry["path"] for entry in manifest["scope"]["files"]}
        self.assertIn("rules/SHARED.md", paths)

    def test_agents_primary_roundtrip(self):
        manifest = self._roundtrip("agents-primary")
        self.assertEqual(manifest["profile"]["primary_surface"]["path"], "AGENTS.md")

    def test_projection_drift_and_rollback_of_created_files(self):
        profile, source = fixture("claude-primary")
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            package = temp / "package"
            target = temp / "target"
            receipt = temp / "receipt.json"
            BRIDGE.capture_instance(profile, source, package)
            BRIDGE.restore_instance(package, target, backup_root=temp / "backup", receipt_path=receipt)
            (target / "GEMINI.md").write_text("projection drift", encoding="utf-8")
            result = BRIDGE.verify_target(package, target)
            self.assertIn("projection-drift", {item["code"] for item in result["findings"]})
            (target / "GEMINI.md").write_bytes((package / "files" / "GEMINI.md").read_bytes())
            self.assertEqual(BRIDGE.rollback_restore(receipt)["status"], "rolled-back")
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_rollback_restores_preexisting_content(self):
        profile, source = fixture("agents-primary")
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            package = temp / "package"
            target = temp / "target"
            target.mkdir()
            original = b"preexisting local authority\n"
            (target / "AGENTS.md").write_bytes(original)
            receipt = temp / "receipt.json"
            BRIDGE.capture_instance(profile, source, package)
            BRIDGE.restore_instance(package, target, backup_root=temp / "backup", receipt_path=receipt)
            BRIDGE.rollback_restore(receipt)
            self.assertEqual((target / "AGENTS.md").read_bytes(), original)

    def test_capture_privacy_reject_and_redact(self):
        profile, source_fixture = fixture("agents-primary")
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "source"
            source.mkdir()
            for path in source_fixture.rglob("*"):
                if path.is_file():
                    target = source / path.relative_to(source_fixture)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(path.read_bytes())
            sensitive = "api" + "_key=" + "synthetic_value_1234567890"
            personal = "C:" + "\\" + "Users" + "\\" + "NamedPerson" + "\\rules"
            (source / "AGENTS.md").write_text(sensitive + "\n" + personal, encoding="utf-8")
            with self.assertRaisesRegex(BRIDGE.BridgeError, "privacy gate rejected"):
                BRIDGE.capture_instance(profile, source, temp / "rejected")
            redacting = copy.deepcopy(profile)
            redacting["privacy"]["mode"] = "redact"
            manifest = BRIDGE.capture_instance(redacting, source, temp / "redacted")
            output = (temp / "redacted" / "files" / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("<redacted-secret>", output)
            self.assertIn("<user-home>", output)
            self.assertTrue(manifest["privacy"]["events"])
            self.assertFalse(BRIDGE._privacy_findings(output))

    def test_capture_include_and_exclude_bound_manifest_scope(self):
        profile, source_fixture = fixture("agents-primary")
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "source"
            shutil.copytree(source_fixture, source)
            (source / "notes").mkdir()
            (source / "notes" / "public.md").write_text("synthetic public note", encoding="utf-8")
            (source / "notes" / "private.md").write_text("synthetic excluded note", encoding="utf-8")
            profile["privacy"]["include"] = ["notes"]
            profile["privacy"]["exclude"].append("notes/private.md")
            manifest = BRIDGE.capture_instance(profile, source, temp / "package")
            paths = {entry["path"] for entry in manifest["scope"]["files"]}
            self.assertIn("notes/public.md", paths)
            self.assertNotIn("notes/private.md", paths)
            self.assertEqual(manifest["scope"]["includes"], ["notes"])

    def test_capture_gates_and_redacts_private_profile_variables(self):
        profile, source = fixture("agents-primary")
        personal = "C:" + "\\" + "Users" + "\\" + "NamedPerson" + "\\bridge"
        profile["platform"]["variables"]["local_root"] = personal
        profile["platform"]["variables"]["api_key"] = "synthetic_value_1234567890"
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            with self.assertRaisesRegex(BRIDGE.BridgeError, "platform variable"):
                BRIDGE.capture_instance(profile, source, temp / "rejected")
            profile["privacy"]["mode"] = "redact"
            manifest = BRIDGE.capture_instance(profile, source, temp / "redacted")
            variables = manifest["profile"]["platform"]["variables"]
            self.assertIn("<user-home>", variables["local_root"])
            self.assertEqual(variables["api_key"], "<redacted-secret>")
            self.assertEqual(manifest["privacy"]["events"][0]["path"], "BRIDGE-PROFILE.json")

    def test_controlled_projection_regeneration_records_hash_provenance(self):
        profile, source = fixture("claude-primary")
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "package"
            manifest = BRIDGE.capture_instance(profile, source, package, regenerate_projections=True)
            projection = (package / "files" / "GEMINI.md").read_text(encoding="utf-8")
            entry = next(item for item in manifest["scope"]["files"] if item["path"] == "GEMINI.md")
            self.assertTrue(entry["synthesized"])
            self.assertTrue(entry["projection"])
            self.assertIn("source_hashes:", projection)
            self.assertIn("generated_at:", projection)
            self.assertIn("source-begin: CLAUDE.md", projection)


class RuntimeContractsTests(unittest.TestCase):
    def test_messenger_roundtrip_ack_and_append_only_provenance(self):
        profile, _ = fixture("claude-primary")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            message = BRIDGE.send_message(
                profile,
                root,
                sender="claude",
                recipient="codex",
                subject="Synthetic handoff",
                body="Please verify the portable fixture.",
                kind="handoff",
            )
            before = BRIDGE.message_status(profile, root, sender="claude", message_id=message["id"])
            self.assertEqual(before["status"], "pending")
            ack = BRIDGE.acknowledge_message(profile, root, actor="codex", message_id=message["id"])
            after = BRIDGE.message_status(profile, root, sender="claude", message_id=message["id"])
            self.assertEqual(after["status"], "acknowledged")
            self.assertEqual(after["receipt"]["id"], ack["id"])
            provenance = (
                (root / profile["messenger"]["root"] / "provenance.jsonl").read_text(encoding="utf-8").splitlines()
            )
            self.assertEqual(
                [json.loads(line)["event"] for line in provenance],
                ["sent", "acknowledged"],
            )

    def test_presence_and_cooperative_locks(self):
        profile, _ = fixture("claude-primary")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            BRIDGE.heartbeat(profile, root, actor="claude", ttl_seconds=60)
            actors = BRIDGE.presence_status(profile, root)["actors"]
            self.assertTrue(next(item for item in actors if item["actor"] == "claude")["active"])
            BRIDGE.claim_lock(profile, root, actor="claude", resource="rules/SHARED.md")
            with self.assertRaisesRegex(BRIDGE.BridgeError, "already claimed"):
                BRIDGE.claim_lock(profile, root, actor="codex", resource="rules/SHARED.md")
            BRIDGE.release_lock(profile, root, actor="claude", resource="rules/SHARED.md")
            self.assertFalse(BRIDGE.lock_status(profile, root)["locks"])

    def test_message_subject_uses_the_privacy_gate(self):
        profile, _ = fixture("claude-primary")
        personal = "C:" + "\\" + "Users" + "\\" + "NamedPerson" + "\\handoff"
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(BRIDGE.BridgeError, "privacy gate"):
                BRIDGE.send_message(
                    profile,
                    Path(temp),
                    sender="claude",
                    recipient="codex",
                    subject=personal,
                    body="Synthetic body",
                )


if __name__ == "__main__":
    unittest.main()
