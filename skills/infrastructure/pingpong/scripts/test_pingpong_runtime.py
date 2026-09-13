from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().with_name("pingpong_runtime.py")
_spec = importlib.util.spec_from_file_location("pingpong_runtime", MODULE_PATH)
assert _spec and _spec.loader
pingpong = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pingpong)


def run(*argv: str) -> tuple[int, str]:
    args = pingpong.create_parser().parse_args(list(argv))
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        code = args.handler(args)
    return code, buffer.getvalue()


class PingPongStateCallTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "agents" / "registry").mkdir(parents=True)
        self.addCleanup(self._tmp.cleanup)
        for key in ("PINGPONG_SLOT", "PINGPONG_SYNC_ROOT"):
            os.environ.pop(key, None)

    def set_active(self, slot: str, active: bool, extra: dict | None = None) -> None:
        path = self.root / "agents" / "registry" / f"{slot}.state.json"
        data = {"slot": slot, "pingpong": {"active": active}}
        data.update(extra or {})
        path.write_text(json.dumps(data), encoding="utf-8")

    def write_call(self, name: str, expires: datetime | None, reason: str = "work") -> Path:
        path = self.root / "agents" / name
        body = f"CALL\nREASON:   {reason}\n"
        if expires is not None:
            body += f"EXPIRES:  {expires.isoformat(timespec='seconds')}\n"
        path.write_text(body, encoding="utf-8")
        return path

    def check(self) -> int:
        code, _ = run("check", "--slot", "laptop", "--sync-root", str(self.root))
        return code

    # --- the three distinct outcomes ------------------------------------
    def test_no_active_host_is_idle(self) -> None:
        self.set_active("workstation", False)
        self.assertEqual(self.check(), 1)

    def test_active_host_with_call_for_me(self) -> None:
        self.set_active("workstation", True)
        self.write_call(
            "call-workstation-to-laptop.txt",
            datetime.now().astimezone() + timedelta(hours=1),
        )
        self.assertEqual(self.check(), 0)

    def test_broken_registry_is_not_idle(self) -> None:
        self.set_active("workstation", True)
        (self.root / "agents" / "registry" / "workstation.state.json").write_text(
            "{not json", encoding="utf-8"
        )
        self.assertEqual(self.check(), 3)

    def test_missing_registry_is_not_idle(self) -> None:
        code, _ = run("check", "--slot", "laptop", "--sync-root", str(self.root / "nope"))
        self.assertEqual(code, 3)

    # --- stage 2 matching ------------------------------------------------
    def test_broadcast_reaches_me_but_my_own_call_does_not(self) -> None:
        self.set_active("workstation", True)
        self.write_call(
            "call-laptop-to-all.txt", datetime.now().astimezone() + timedelta(hours=1)
        )
        self.assertEqual(self.check(), 1)
        self.write_call(
            "call-workstation-to-all.txt",
            datetime.now().astimezone() + timedelta(hours=1),
        )
        self.assertEqual(self.check(), 0)

    def test_call_from_inactive_host_does_not_spread(self) -> None:
        self.set_active("workstation", True)
        self.set_active("mac-studio", False)
        self.write_call(
            "call-mac-studio-to-laptop.txt",
            datetime.now().astimezone() + timedelta(hours=1),
        )
        self.assertEqual(self.check(), 1)

    def test_expired_call_terminates_the_conversation(self) -> None:
        self.set_active("workstation", True)
        self.write_call(
            "call-workstation-to-laptop.txt",
            datetime.now().astimezone() - timedelta(minutes=1),
        )
        self.assertEqual(self.check(), 1)

    def test_legacy_pull_name_is_still_read(self) -> None:
        self.set_active("workstation", True)
        self.write_call(
            "pull-workstation-to-laptop.txt",
            datetime.now().astimezone() + timedelta(hours=1),
        )
        self.assertEqual(self.check(), 0)

    def test_call_without_expiry_field_still_expires(self) -> None:
        self.set_active("workstation", True)
        path = self.write_call("call-workstation-to-laptop.txt", None)
        self.assertEqual(self.check(), 0)
        stale = (datetime.now().astimezone() - timedelta(hours=7)).timestamp()
        os.utime(path, (stale, stale))
        self.assertEqual(self.check(), 1)

    # --- writing ---------------------------------------------------------
    def test_state_write_keeps_foreign_keys(self) -> None:
        self.set_active("laptop", False, {"schema": "ellmos.rulefiles-state.v1", "files": [1]})
        run("state", "--activate", "--slot", "laptop", "--sync-root", str(self.root))
        data = json.loads(
            (self.root / "agents" / "registry" / "laptop.state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(data["schema"], "ellmos.rulefiles-state.v1")
        self.assertEqual(data["files"], [1])
        self.assertTrue(data["pingpong"]["active"])

    def test_call_open_refresh_and_end(self) -> None:
        target = self.root / "agents" / "call-laptop-to-workstation.txt"
        run("call", "--to", "workstation", "--reason", "merge", "--slot", "laptop",
            "--sync-root", str(self.root))
        self.assertIn("merge", target.read_text(encoding="utf-8"))
        run("call", "--to", "workstation", "--ttl", "12h", "--slot", "laptop",
            "--sync-root", str(self.root))
        self.assertIn("merge", target.read_text(encoding="utf-8"))  # reason survives
        run("call", "--to", "workstation", "--end", "--slot", "laptop",
            "--sync-root", str(self.root))
        self.assertFalse(target.exists())

    def test_missing_slot_fails_closed(self) -> None:
        code, _ = run("check", "--sync-root", str(self.root))
        self.assertEqual(code, 3)


if __name__ == "__main__":
    unittest.main()
