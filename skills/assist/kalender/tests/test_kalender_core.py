#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Umfassende Stdlib-Unit-Tests für kalender_core.py (v0.2.0)."""

from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import re
import sqlite3
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import kalender_core as kc  # noqa: E402


class KalenderCoreV02Tests(unittest.TestCase):
    """Testet Migration, Multi-Silo-Profile, Sync/Import und alle Berichtsformate."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.store = self.tmp_path / "test_store.db"
        self._old_env = os.environ.get("KALENDER_STORE")
        os.environ.pop("KALENDER_STORE", None)

    def tearDown(self) -> None:
        if self._old_env is not None:
            os.environ["KALENDER_STORE"] = self._old_env
        else:
            os.environ.pop("KALENDER_STORE", None)
        self._tmp.cleanup()

    def _run_cli(self, *args: str) -> tuple[int, str, str]:
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
            rc = kc.main(["--store", str(self.store), *args])
        return rc, out_buf.getvalue(), err_buf.getvalue()

    def test_01_v01_legacy_store_additive_migration(self) -> None:
        """Bestehende v0.1-Stores (nur 11 events-Spalten) migrieren verlustfrei."""
        conn = sqlite3.connect(str(self.store))
        conn.execute(
            """
            CREATE TABLE events (
                id           TEXT PRIMARY KEY,
                title        TEXT NOT NULL,
                date         TEXT NOT NULL,
                time         TEXT,
                duration_min INTEGER,
                location     TEXT,
                description  TEXT,
                recurrence   TEXT,
                ics_uid      TEXT UNIQUE,
                created_at   TEXT NOT NULL,
                updated_at   TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """INSERT INTO events VALUES
               ('leg00001', 'Alttermin Zahnarzt', '2026-12-10', '09:00', 45,
                'Praxis Nord', 'Kontrolle', NULL, 'leg-1@kal', '2026-06-22T10:00:00', '2026-06-22T10:00:00')"""
        )
        conn.commit()
        conn.close()

        events = kc.list_events(self.store)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], "leg00001")
        self.assertEqual(events[0]["calendar_id"], "user")
        self.assertEqual(events[0]["status"], "planned")
        self.assertEqual(events[0]["end_time"], "09:45")

        conn = sqlite3.connect(str(self.store))
        cols = {row[1] for row in conn.execute("PRAGMA table_info(events)").fetchall()}
        conn.close()
        for expected_col in (
            "calendar_id",
            "category",
            "source_calendar_id",
            "source_event_id",
            "link_mode",
            "external_id",
            "end_time",
            "status",
        ):
            self.assertIn(expected_col, cols)

    def test_02_default_silos_seeded_and_profile_crud(self) -> None:
        """Alle 8 Standard-Silos sind vorhanden; eigene Silos anlegbar; 'user' geschützt."""
        cals = kc.list_calendars(self.store)
        ids = {c["id"] for c in cals}
        self.assertEqual(
            ids,
            {
                "user",
                "tickets",
                "finanzen",
                "gesundheit",
                "geburtstage_privat",
                "geburtstage_beruflich",
                "terminpilot",
                "routinen",
            },
        )
        created = kc.add_calendar(
            self.store,
            "verein_2027",
            "Vereinskalender",
            category="community",
            color="#0ea5e9",
            description="Sitzungen",
        )
        self.assertEqual(created["id"], "verein_2027")
        self.assertEqual(len(kc.list_calendars(self.store)), 9)

        with self.assertRaises(ValueError):
            kc.delete_calendar(self.store, "user")

        rc, _out, err = self._run_cli("calendar", "delete", "user")
        self.assertEqual(rc, 1)
        self.assertIn("user", err)

        self.assertTrue(kc.delete_calendar(self.store, "verein_2027"))
        self.assertFalse(kc.delete_calendar(self.store, "verein_2027"))

    def test_03_silo_filtering_merged_single_and_comma_list(self) -> None:
        """Prüft --calendar all, Einzel-Silo, Kommaliste, --category und --search."""
        kc.add_event(self.store, "Privates Abendessen", "2027-02-10", "19:00", 90, calendar_id="user")
        kc.add_event(self.store, "Hautarzt Screening", "2027-02-11", "08:30", 30, calendar_id="gesundheit")
        kc.add_event(self.store, "Umsatzsteuer-Voranmeldung", "2027-02-12", "11:00", 60, calendar_id="finanzen")
        kc.add_event(self.store, "Ticket-Review Block", "2027-02-13", "14:00", 60, calendar_id="tickets")

        all_evs = kc.get_events_by_date_range(self.store, "2027-02-01", "2027-02-28", calendar="all")
        self.assertEqual(len(all_evs), 4)

        health_evs = kc.get_events_by_date_range(self.store, "2027-02-01", "2027-02-28", calendar="gesundheit")
        self.assertEqual([e["title"] for e in health_evs], ["Hautarzt Screening"])

        combo_evs = kc.get_events_by_date_range(self.store, "2027-02-01", "2027-02-28", calendar="user,finanzen")
        self.assertEqual(len(combo_evs), 2)
        self.assertEqual({e["calendar_id"] for e in combo_evs}, {"user", "finanzen"})

        cat_evs = kc.list_events(self.store, category="health")
        self.assertEqual(len(cat_evs), 1)
        self.assertEqual(cat_evs[0]["calendar_id"], "gesundheit")

        search_evs = kc.list_events(self.store, search="umsatzsteuer")
        self.assertEqual(len(search_evs), 1)
        self.assertEqual(search_evs[0]["calendar_id"], "finanzen")

    def test_04_cli_time_queries_day_week_month_year_range_json(self) -> None:
        """Prüft CLI-Abfragen today, day, week, month, year, range und list mit --json."""
        today_str = date.today().isoformat()
        kc.add_event(self.store, "Heute-Check", today_str, "10:00", 30, calendar_id="user")
        kc.add_event(self.store, "Augenarzt 2027", "2027-05-19", "15:00", 45, calendar_id="gesundheit")
        kc.add_event(self.store, "Zahnreinigung 2027", "2027-11-04", "09:00", 60, calendar_id="gesundheit")

        rc, out, _ = self._run_cli("today", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["count"], 1)

        rc, out, _ = self._run_cli("day", "--date", "2027-05-19", "--calendar", "gesundheit", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["events"][0]["title"], "Augenarzt 2027")

        rc, out, _ = self._run_cli("week", "--from", "2027-05-17", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["count"], 1)

        rc, out, _ = self._run_cli("month", "--month", "2027-05", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["count"], 1)

        rc, out, _ = self._run_cli("year", "--year", "2027", "--calendar", "gesundheit", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["count"], 2)

        rc, out, _ = self._run_cli("range", "--from", "2027-05-01", "--to", "2027-12-01", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["count"], 2)

    def test_05_mirror_idempotency_and_sync_mirrors_lifecycle(self) -> None:
        """mirror aktualisiert idempotent; sync-mirrors erkennt updated, unchanged und orphaned."""
        src_id = kc.add_event(
            self.store,
            "Projekt-Workshop",
            "2026-12-14",
            "13:00",
            120,
            location="Raum 2",
            calendar_id="terminpilot",
        )
        m1 = kc.mirror_event(self.store, src_id, "user")
        self.assertEqual(m1["action"], "created")
        mirror_id = m1["id"]

        # Zweiter mirror-Aufruf legt kein Duplikat an
        m2 = kc.mirror_event(self.store, src_id, "user")
        self.assertEqual(m2["action"], "updated")
        self.assertEqual(m2["id"], mirror_id)
        self.assertEqual(len(kc.list_events(self.store, calendar="user")), 1)

        # Unveränderter Sync
        sync1 = kc.sync_mirrors(self.store)
        self.assertEqual((sync1["updated"], sync1["unchanged"], sync1["orphaned"]), (0, 1, 0))

        # Quelltermin ändern -> sync-mirrors übernimmt Änderung
        conn = sqlite3.connect(str(self.store))
        conn.execute("UPDATE events SET title = 'Projekt-Workshop (verschoben)', time = '15:00' WHERE id = ?", (src_id,))
        conn.commit()
        conn.close()

        sync2 = kc.sync_mirrors(self.store)
        self.assertEqual((sync2["updated"], sync2["unchanged"], sync2["orphaned"]), (1, 0, 0))
        mirrored = kc.list_events(self.store, calendar="user")[0]
        self.assertEqual(mirrored["title"], "Projekt-Workshop (verschoben)")
        self.assertEqual(mirrored["time"], "15:00")

        # Quelltermin löschen -> Spiegel wird als orphaned gemeldet
        kc.delete_event(self.store, src_id)
        sync3 = kc.sync_mirrors(self.store)
        self.assertEqual((sync3["updated"], sync3["unchanged"], sync3["orphaned"]), (0, 0, 1))

    def test_06_transfer_and_clone_semantics(self) -> None:
        """transfer verschiebt mit Herkunftsnachweis; clone erstellt unabhängige Kopie."""
        ev_id = kc.add_event(self.store, "Steuerberatung", "2027-01-20", "10:00", 60, calendar_id="user")
        tr = kc.transfer_event(self.store, ev_id, "finanzen")
        self.assertEqual(tr["action"], "transferred")
        self.assertEqual(tr["source_calendar_id"], "user")
        self.assertEqual(len(kc.list_events(self.store, calendar="user")), 0)
        moved = kc.list_events(self.store, calendar="finanzen")[0]
        self.assertEqual(moved["link_mode"], "transfer")
        self.assertEqual(moved["source_calendar_id"], "user")

        cl = kc.clone_event(self.store, ev_id, "routinen")
        self.assertEqual(cl["action"], "cloned")
        self.assertNotEqual(cl["id"], ev_id)
        cloned = kc.list_events(self.store, calendar="routinen")[0]
        self.assertEqual(cloned["link_mode"], "clone")
        self.assertNotEqual(cloned["ics_uid"], moved["ics_uid"])

    def test_07_terminpilot_ics_import_unfolding_and_idempotency(self) -> None:
        """RFC-5545-Import inkl. Line-Unfolding, TZID, DURATION, Ganztagstermin & Idempotenz."""
        ics_file = self.tmp_path / "terminpilot.ics"
        ics_text = (
            "BEGIN:VCALENDAR\r\n"
            "VERSION:2.0\r\n"
            "PRODID:-//TerminPilot//Poll//DE\r\n"
            "BEGIN:VEVENT\r\n"
            "UID:tp-vote-101@terminpilot.example\r\n"
            "SUMMARY:Beirats\r\n"
            " sitzung\\, Quartal 4\r\n"
            "DTSTART;TZID=Europe/Berlin:20261215T160000\r\n"
            "DTEND;TZID=Europe/Berlin:20261215T173000\r\n"
            "LOCATION:Konferenzraum Süd\r\n"
            "DESCRIPTION:Abgestimmter Termin\\nTeilnehmer: 6\r\n"
            "CATEGORIES:coordination\r\n"
            "END:VEVENT\r\n"
            "BEGIN:VEVENT\r\n"
            "UID:tp-holiday-102@terminpilot.example\r\n"
            "SUMMARY:Klausurtag\r\n"
            "DTSTART;VALUE=DATE:20261218\r\n"
            "RRULE:FREQ=YEARLY\r\n"
            "END:VEVENT\r\n"
            "END:VCALENDAR\r\n"
        )
        ics_file.write_text(ics_text, encoding="utf-8")

        res1 = kc.import_ics(self.store, ics_file, calendar_id="terminpilot")
        self.assertEqual((res1["imported"], res1["updated"], res1["unchanged"]), (2, 0, 0))

        tp_events = kc.list_events(self.store, calendar="terminpilot")
        self.assertEqual(len(tp_events), 2)
        first = tp_events[0]
        self.assertEqual(first["title"], "Beiratssitzung, Quartal 4")
        self.assertEqual(first["date"], "2026-12-15")
        self.assertEqual(first["time"], "16:00")
        self.assertEqual(first["end_time"], "17:30")
        self.assertEqual(first["duration_min"], 90)
        self.assertIn("Teilnehmer: 6", first["description"])

        # Zweiter Import derselben Datei ist 100 % idempotent
        res2 = kc.import_ics(self.store, ics_file, calendar_id="terminpilot")
        self.assertEqual((res2["imported"], res2["updated"], res2["unchanged"]), (0, 0, 2))
        self.assertEqual(len(kc.list_events(self.store, calendar="terminpilot")), 2)

        # Aktualisierte Uhrzeit in ICS -> updated=1, unchanged=1
        ics_file.write_text(ics_text.replace("20261215T160000", "20261215T163000"), encoding="utf-8")
        res3 = kc.import_ics(self.store, ics_file, calendar_id="terminpilot")
        self.assertEqual((res3["imported"], res3["updated"], res3["unchanged"]), (0, 1, 1))

        # Import derselben Datei in ein zweites Silo funktioniert kollisionsfrei
        res_other = kc.import_ics(self.store, ics_file, calendar_id="user")
        self.assertEqual(res_other["imported"], 2)

    def test_08_ics_export_filtered_and_roundtrip(self) -> None:
        """ICS-Export schreibt CATEGORIES:<calendar_id> und lässt sich sauber re-importieren."""
        kc.add_event(self.store, "Kardiologie", "2027-04-08", "11:15", 45, calendar_id="gesundheit")
        kc.add_event(self.store, "Steuerfrist", "2027-04-10", "09:00", 30, calendar_id="finanzen")

        ics_out = kc.export_ics(self.store, calendar="gesundheit", from_date="2027-04-01", to_date="2027-04-30")
        self.assertIn("SUMMARY:Kardiologie", ics_out)
        self.assertIn("CATEGORIES:gesundheit,health", ics_out)
        self.assertNotIn("Steuerfrist", ics_out)

        fresh_store = self.tmp_path / "roundtrip.db"
        imp = kc.import_ics(fresh_store, ics_out, calendar_id="gesundheit", raw_text=True)
        self.assertEqual(imp["imported"], 1)

    def test_09_render_html_views_and_xss_escaping(self) -> None:
        """HTML-Kalenderblätter für month/week/day/year/range inkl. @media print & XSS-Schutz."""
        kc.add_event(
            self.store,
            "Zahnarzt <script>alert(1)</script>",
            "2026-12-15",
            "10:00",
            60,
            location="Praxis Mitte",
            calendar_id="gesundheit",
        )
        kc.add_event(
            self.store,
            "Jahresabschluss",
            "2026-12-28",
            "14:00",
            90,
            calendar_id="finanzen",
        )

        html_month = kc.render_report(self.store, view="month", fmt="html", month_str="2026-12")["content"]
        self.assertIn("@media print", html_month)
        self.assertIn('class="cal-grid"', html_month)
        self.assertIn("<th>Mo</th>", html_month)
        self.assertIn("<th>So</th>", html_month)
        self.assertIn("#dc2626", html_month)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html_month)
        self.assertNotIn("<script>alert(1)</script>", html_month)

        for v_name, kwargs in (
            ("week", {"week_from": "2026-12-14"}),
            ("day", {"day_str": "2026-12-15"}),
            ("year", {"year_str": "2026"}),
            ("range", {"range_from": "2026-12-01", "range_to": "2026-12-31"}),
        ):
            rep = kc.render_report(self.store, view=v_name, fmt="html", **kwargs)
            expected_count = 1 if v_name in {"day", "week"} else 2
            self.assertEqual(rep["events_count"], expected_count)
            self.assertIn("<!DOCTYPE html>", rep["content"])

    def test_10_render_markdown_and_text_reports(self) -> None:
        """MD- und TXT-Berichte enthalten Silo-Legende, Monatsgitter und Terminzeilen."""
        kc.add_event(self.store, "Orthopädie", "2026-12-03", "08:30", 45, calendar_id="gesundheit")
        md_rep = kc.render_report(self.store, view="month", fmt="md", month_str="2026-12")["content"]
        self.assertIn("| Mo | Di | Mi | Do | Fr | Sa | So |", md_rep)
        self.assertIn("`gesundheit`", md_rep)
        self.assertIn("Orthopädie", md_rep)

        txt_rep = kc.render_report(self.store, view="month", fmt="txt", month_str="2026-12")["content"]
        self.assertIn("|  Mo  |  Di  |  Mi  |  Do  |  Fr  |  Sa  |  So  |", txt_rep)
        self.assertIn("[gesundheit] Orthopädie", txt_rep)

    def test_11_render_pdf_valid_pdf14_xref_and_umlauts(self) -> None:
        """PDF-Bericht erzeugt valides %PDF-1.4 mit korrekten xref-Offsets und WinAnsi-Umlauten."""
        kc.add_event(
            self.store,
            "Zahnärztliche Vorsorge für März & Größe",
            "2027-03-18",
            "09:15",
            45,
            location="Ärztehaus Südstraße",
            calendar_id="gesundheit",
        )
        pdf_month_path = self.tmp_path / "dez_2026.pdf"
        kc.add_event(self.store, "Weihnachtsplanung", "2026-12-20", "16:00", 60, calendar_id="user")
        rep_m = kc.render_report(
            self.store,
            view="month",
            fmt="pdf",
            month_str="2026-12",
            out_path=pdf_month_path,
        )
        self.assertTrue(pdf_month_path.is_file())
        self.assertGreater(rep_m["bytes"], 600)

        pdf_year_path = self.tmp_path / "arzt_2027.pdf"
        rc, out, _ = self._run_cli(
            "render",
            "--view",
            "year",
            "--year",
            "2027",
            "--calendar",
            "gesundheit",
            "--format",
            "pdf",
            "--title",
            "Arzttermine 2027 — Übersicht",
            "--out",
            str(pdf_year_path),
            "--json",
        )
        self.assertEqual(rc, 0)
        meta = json.loads(out)
        self.assertEqual(meta["events_count"], 1)

        raw_pdf = pdf_year_path.read_bytes()
        self.assertTrue(raw_pdf.startswith(b"%PDF-1.4\n"))
        self.assertTrue(raw_pdf.endswith(b"%%EOF\n"))
        self.assertIn(b"/WinAnsiEncoding", raw_pdf)
        # ä = \344, ü = \374, ß = \337 in WinAnsi octal literal
        self.assertIn(b"\\344", raw_pdf)
        self.assertIn(b"\\337", raw_pdf)

        # Prüfe exakte xref-Byte-Offsets gegen Objekt-Header
        xref_pos = raw_pdf.find(b"\nxref\n")
        self.assertGreater(xref_pos, 0)
        xref_lines = raw_pdf[xref_pos + 1 :].decode("ascii").splitlines()
        checked_objs = 0
        for line in xref_lines[2:]:
            if line.startswith("trailer"):
                break
            if line.strip().endswith(" f"):
                continue
            offset = int(line.split()[0])
            self.assertRegex(raw_pdf[offset : offset + 16].decode("ascii", errors="ignore"), r"^\d+ 0 obj")
            checked_objs += 1
        self.assertGreaterEqual(checked_objs, 6)

        # Ohne --out verweigert die CLI --format pdf sauber mit Exit 1
        rc_err, _o, err_s = self._run_cli("report", "--view", "month", "--format", "pdf")
        self.assertEqual(rc_err, 1)
        self.assertIn("--out", err_s)

    def test_12_pdf_multipage_pagination(self) -> None:
        """Viele Termine im Jahresbericht umbrechen sauber auf mehrere PDF-Seiten."""
        for i in range(1, 66):
            day_num = ((i - 1) % 28) + 1
            month_num = ((i - 1) % 12) + 1
            kc.add_event(
                self.store,
                f"Kontrolltermin Nr. {i}",
                f"2027-{month_num:02d}-{day_num:02d}",
                "10:00",
                30,
                calendar_id="gesundheit",
            )
        out_pdf = self.tmp_path / "many.pdf"
        kc.render_report(self.store, view="year", fmt="pdf", year_str="2027", out_path=out_pdf)
        raw = out_pdf.read_bytes()
        m = re.search(rb"/Type /Pages /Kids \[[^\]]+\] /Count (\d+)", raw)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertGreaterEqual(int(m.group(1)), 2)

    def test_13_render_ics_format_and_env_store_override(self) -> None:
        """report --format ics und Umgebungsvariable KALENDER_STORE funktionieren."""
        env_db = self.tmp_path / "env_cal.db"
        os.environ["KALENDER_STORE"] = str(env_db)
        out_buf = io.StringIO()
        with contextlib.redirect_stdout(out_buf):
            rc = kc.main(["add", "Env-Termin", "--date", "2027-07-07", "--calendar", "routinen", "--json"])
        self.assertEqual(rc, 0)
        self.assertTrue(env_db.is_file())

        rep_ics = kc.render_report(env_db, view="year", fmt="ics", year_str="2027", calendar="routinen")
        self.assertIn("BEGIN:VCALENDAR", rep_ics["content"])
        self.assertIn("SUMMARY:Env-Termin", rep_ics["content"])

    def test_14_cli_profile_and_silo_commands_end_to_end(self) -> None:
        """End-to-End-CLI-Durchlauf für calendar, mirror, sync-mirrors, transfer, clone, delete."""
        rc, out, _ = self._run_cli("calendar", "list", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["count"], 8)

        rc, out, _ = self._run_cli(
            "calendar", "add", "studium", "--name", "Studienkalender", "--category", "education", "--color", "#14b8a6", "--json"
        )
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["id"], "studium")

        rc, out, _ = self._run_cli(
            "add", "Klausur Mathematik", "--date", "2027-02-22", "--time", "09:00", "--duration", "120", "--calendar", "studium", "--json"
        )
        self.assertEqual(rc, 0)
        ev_id = json.loads(out)["id"]

        rc, out, _ = self._run_cli("mirror", ev_id, "--to", "user", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["action"], "created")

        rc, out, _ = self._run_cli("sync-mirrors", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["unchanged"], 1)

        rc, out, _ = self._run_cli("clone", ev_id, "--to", "tickets", "--json")
        self.assertEqual(rc, 0)
        clone_id = json.loads(out)["id"]

        rc, out, _ = self._run_cli("transfer", clone_id, "--to", "routinen", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["to_calendar_id"], "routinen")

        rc, out, _ = self._run_cli("delete", clone_id, "--json")
        self.assertEqual(rc, 0)
        self.assertTrue(json.loads(out)["deleted"])

        rc, out, _ = self._run_cli("check-backend", "--json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["core_version"], "0.2.0")

    def test_15_stdlib_only_and_public_privacy_cleanliness(self) -> None:
        """Stellt sicher, dass keine Fremdpakete oder privaten Host-/Pfaddaten im Skill liegen."""
        allowed_stdlib = {
            "__future__", "ast", "calendar", "contextlib", "datetime", "html",
            "io", "json", "os", "pathlib", "re", "sqlite3", "sys", "tempfile",
            "typing", "unittest", "uuid", "kalender_core",
        }
        for py_path in SKILL_DIR.rglob("*.py"):
            tree = ast.parse(py_path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertIn(alias.name.split(".")[0], allowed_stdlib, py_path.name)
                elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                    self.assertIn(node.module.split(".")[0], allowed_stdlib, py_path.name)

        private_ip_re = re.compile(
            r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
        )
        abs_user_path_re = re.compile(r"(?:[A-Za-z]:[\\/]+Users[\\/]+|/Users/[A-Za-z0-9_-]+/|/home/[A-Za-z0-9_-]+/)")
        for fpath in SKILL_DIR.rglob("*"):
            if fpath.is_file() and fpath.suffix in {".py", ".md"}:
                text = fpath.read_text(encoding="utf-8")
                self.assertIsNone(private_ip_re.search(text), f"Private IP in {fpath.name}")
                self.assertIsNone(abs_user_path_re.search(text), f"User path in {fpath.name}")


if __name__ == "__main__":
    unittest.main()
