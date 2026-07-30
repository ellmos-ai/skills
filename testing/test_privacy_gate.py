"""Regression tests for the repository privacy gate."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("privacy_gate.py")
SPEC = importlib.util.spec_from_file_location("privacy_gate", MODULE_PATH)
privacy_gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(privacy_gate)


class PrivacyGateTests(unittest.TestCase):
    def test_rejects_concrete_windows_user_home(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            r"Load C:\Users\Alice\OneDrive\private.json"
        )
        self.assertEqual([r"C:\Users\Alice"], findings)

    def test_accepts_portable_windows_placeholder(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            r"Load C:\Users\<user>\project\config.json"
        )
        self.assertEqual([], findings)

    def test_rejects_concrete_posix_user_home(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            "Load /home/alice/project/config.json"
        )
        self.assertEqual(["/home/alice"], findings)

    def test_accepts_generic_posix_example(self) -> None:
        findings = privacy_gate.concrete_home_matches(
            "Load /home/user/project/config.json"
        )
        self.assertEqual([], findings)

    def test_rejects_host_scoped_device_names(self) -> None:
        pattern = privacy_gate.CONTENT_PATTERNS["host-scoped device name"]
        self.assertIsNotNone(pattern.search("WORKSTATION-ABC"))
        self.assertIsNotNone(pattern.search("LAPTOP-123"))


if __name__ == "__main__":
    unittest.main()
