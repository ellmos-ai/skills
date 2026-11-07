"""Tests fuer build_formular.py (Standardbibliothek + markdown): python -m unittest selbsttest_markdown -v

Pruefen: reproduzierbarer Hash, Posten/Optionen/Empfehlung/Avatar gegen das Quelldokument (und, falls lesbar, gegen die versiegelte
Messdatei, nur lesend), nichts vorausgewaehlt, kein Netz, Text des Dokuments unveraendert, Schema der Antwortdatei und Roundtrip
(Antworten im Browser gesetzt -> Antwortdatei -> eingebettete Entscheidungen in der BEANTWORTET-Kopie).
Die Dateien in testdata/ stammen aus einem echten Browserlauf (Chromium, Download-Fallback) gegen genau diese Formular-Version;
aendert sich das Formular, aendert sich sein Hash, und die Fixtures muessen mit einem neuen Lauf erneuert werden (der Test sagt es).
"""
import hashlib
import json
import os
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import build_from_markdown as bf
import headless_util as hu
from savetests import SaveTestsMixin

HERE = Path(__file__).resolve().parent
# Referenz-Selbsttest: gilt nur fuer das Dokument vom 2026-11-07. Pfade kommen aus Umgebungsvariablen, nichts ist vorbelegt.
MD = Path(os.environ["FORMULAR_MD"])  # Gesamtdokument (Markdown); KeyError = Variable fehlt
OLD_HTML = MD.with_suffix(".html")
SEALED = Path(os.environ.get("FORMULAR_MESSUNG", ""))  # optional: versiegelte Messdatei, nur lesend
EXPECTED_IDS = ["V1", "V3", "V4", "V5", "V6", "O1", "O2", "O3", "O4", "S1", "S2", "S3", "S4", "T1", "T2.1", "T2.2", "T2.3", "T2.4", "T2.5", "T2.6", "T3", "T4", "F1", "I1"]
EXPECTED_MARKED = {"V1", "V3", "V4", "V5", "V6", "O2", "O3", "S3", "S4", "T2.3", "T2.5", "T3", "I1"}
SEAL_SHA = "aed5202ac964b20e3f22989c52c7f158c094bee25440983f688b98bbd670b0e4"  # Siegel der Avatar-Vorhersage (Spalten Avatar-Wahl, Konfidenz)

PAGE, DIGEST, ITEMS = bf.build(MD)


def plain_text(h):
    h = h[h.index("<body>"): h.rindex("</body>")]
    for rx in (r'<section class="bundle-form".*?</section>', r'<section class="panel" id="top-panel">.*?</section>', r'<div class="sticky-bar">.*?</button></div>',
               r"<dialog.*?</dialog>", r'<div id="toast".*?</div>', r"<script.*?</script>", r"<style.*?</style>"):
        h = re.sub(rx, "", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


class Build(unittest.TestCase):
    def test_hash_is_reproducible_and_blankable(self):
        page2, digest2, _ = bf.build(MD)
        self.assertEqual(page2, PAGE)
        embedded, recomputed = bf.blank_hash(PAGE)
        self.assertEqual(embedded, DIGEST)
        self.assertEqual(recomputed, DIGEST, "document_sha256 = SHA-256 der Datei mit Nullen an Stelle des Hashs")
        self.assertEqual(hashlib.sha256(PAGE.replace(DIGEST, "0" * 64).encode("utf-8")).hexdigest(), DIGEST)

    def test_24_items_in_order_with_options(self):
        self.assertEqual([i["id"] for i in ITEMS], EXPECTED_IDS)
        for it in ITEMS:
            self.assertGreaterEqual(len(it["options"]), 2, it["id"])
            self.assertIn(it["rec"], [o["k"] for o in it["options"]], it["id"] + ": Empfehlung ist keine Option")
            self.assertIn(it["av_conf"], ("gelb", "grün", "rot"))
        self.assertEqual({i["id"] for i in ITEMS if i["marked"]}, EXPECTED_MARKED)
        for k in ("V5", "O2"):
            self.assertIsNone(next(i for i in ITEMS if i["id"] == k)["av_pred"], k + ": roter Avatar-Posten ohne Vorhersage")

    @unittest.skipUnless(SEALED.is_file(), "versiegelte Messdatei nicht lesbar")
    def test_matches_sealed_measurement_read_only(self):
        lines = SEALED.read_text(encoding="utf-8").splitlines()
        i = next(k for k, line in enumerate(lines) if line.startswith("## Teil 1"))
        rows = [bf.cells(line) for line in lines[i:] if line.startswith("| ") and bf.cells(line)[0] in EXPECTED_IDS][: len(EXPECTED_IDS)]
        self.assertEqual([r[0] for r in rows], EXPECTED_IDS)
        seal = "\n".join(f"{r[3]}\t{r[4]}" for r in rows)
        self.assertEqual(hashlib.sha256(seal.encode("utf-8")).hexdigest(), SEAL_SHA, "Spalten Avatar-Wahl/Konfidenz der Messdatei passen zum Siegel")
        for r, it in zip(rows, ITEMS):
            opts, _ = bf.parse_options(r[2])
            self.assertEqual(opts, it["options"], it["id"])
            self.assertEqual(r[1], it["question"], it["id"])
            self.assertEqual("offen" if it["av_pred"] is None else it["av_pred"], r[3], it["id"])
            self.assertEqual(r[4], it["av_conf"], it["id"])

    def test_nothing_preselected_and_no_network(self):
        self.assertIsNone(re.search(r"<input[^>]*\schecked", PAGE), "nichts vorausgewaehlt")
        self.assertIsNone(re.search(r"<(option|textarea)[^>]*\sselected", PAGE))
        self.assertIsNone(re.search(r'(?:src|href|action)="https?://', PAGE), "keine externen Verweise")
        self.assertNotIn("<link", PAGE)
        self.assertNotIn("@import", PAGE)
        self.assertNotIn("alert(", PAGE.split('<script>', 1)[1], "kein Browser-alert")
        self.assertEqual(len(re.findall(r'<fieldset class="item" id="item-', PAGE)), 24)
        self.assertEqual(len(re.findall(r'data-bulk="\d"', PAGE)), 6)
        self.assertEqual(len(re.findall(r'data-bulk="all"', PAGE)), 1)
        self.assertIn('name="agpl"', PAGE)

    @unittest.skipUnless(OLD_HTML.is_file(), "altes Lesedokument nicht vorhanden")
    def test_document_text_unchanged_against_old_html(self):
        # T2-Aufzaehlung: das alte Dokument zeigte die Ziffern 1. bis 6. als Text, jetzt rendert der Browser eine nummerierte Liste.
        # Die Ziffern-Marken werden deshalb auf BEIDEN Seiten gleich entfernt (auch bei den Ueberschriften "1. Buendel ...").
        def norm(t):
            return re.sub(r"(?<=[:.]) [1-7]\. (?=[A-ZÄÖÜ])", " ", t)

        self.assertEqual(norm(plain_text(OLD_HTML.read_text(encoding="utf-8"))), norm(plain_text(PAGE)),
                         "Text der Vorlagen und der Avatar-Bewertung ist unveraendert; nur Formularelemente kamen hinzu")


@unittest.skipUnless((HERE / "testdata").is_dir(), "testdata/ fehlt: Browser-Fixtures mit make_fixtures.py erzeugen")
class Answers(unittest.TestCase):
    def load(self, name):
        a = json.loads((HERE / "testdata" / f"{name}_antwort.json").read_text(encoding="utf-8"))
        h = (HERE / "testdata" / f"{name}_BEANTWORTET.html").read_text(encoding="utf-8")
        return a, h

    def test_schema_and_hash_of_browser_output(self):
        for name in ("teil", "voll"):
            a, _ = self.load(name)
            self.assertEqual(bf.validate_answers(a, ITEMS, expected_sha=DIGEST), [], f"{name}: Antwortdatei ungueltig oder Formular seit dem Browserlauf geaendert (Fixtures erneuern)")

    def test_partial_stays_open_and_not_gesamtabnahme(self):
        a, _ = self.load("teil")
        self.assertEqual(a["counts"], {"total": 24, "answered": 4, "open": 20})
        self.assertFalse(a["gesamtabnahme"]["explicit"])
        self.assertEqual(a["answers"]["V1"]["choice"], "B")
        self.assertEqual(a["answers"]["V1"]["note"], "lieber nur 3.0, bitte erst prüfen")
        self.assertEqual(a["answers"]["V4"]["state"], "open")
        self.assertIsNone(a["answers"]["V4"]["choice"])
        self.assertEqual(a["agpl_bleibt"]["choice"], "bestätigen")

    def test_full_bulk_is_explicit_and_marked_items_flagged(self):
        a, _ = self.load("voll")
        self.assertTrue(a["gesamtabnahme"]["explicit"])
        self.assertEqual(a["counts"]["answered"], 24)
        self.assertIn("bundle-alle", a["bulk_actions"])
        self.assertTrue(all(x["choice"] == x["recommended"] for x in a["answers"].values()))
        self.assertEqual({k for k, x in a["answers"].items() if x["marked"]}, EXPECTED_MARKED)
        self.assertTrue(all(x["via"] == "bulk" for x in a["answers"].values()))

    def test_roundtrip_answered_copy_embeds_the_same_decisions(self):
        for name in ("teil", "voll"):
            a, h = self.load(name)
            m = re.search(r'<script type="application/json" id="embedded-answers">(.*?)</script>', h, re.S)
            self.assertIsNotNone(m, name)
            embedded = json.loads(m.group(1).replace("<\\/", "</"))
            self.assertEqual(embedded, a, f"{name}: eingebettete Entscheidungen == Antwortdatei")
            self.assertIn('data-mode="answered"', h)
            self.assertIn('id="ergebnis"', h)
            self.assertEqual(re.search(r'name="document-sha256" content="([0-9a-f]{64})"', h).group(1), DIGEST, "BEANTWORTET stammt aus genau diesem Formular")

    def test_validator_rejects_bad_files(self):
        a, _ = self.load("voll")
        bad = json.loads(json.dumps(a))
        bad["answers"]["V1"]["choice"] = "Z"
        self.assertTrue(bf.validate_answers(bad, ITEMS))
        bad = json.loads(json.dumps(a))
        bad["answers"]["V1"]["choice"], bad["answers"]["V1"]["choice_label"] = "B", ITEMS[0]["options"][1]["l"]  # weicht von der Empfehlung ab, Gesamtabnahme bleibt true
        self.assertTrue(bf.validate_answers(bad, ITEMS), "explizite Gesamtabnahme mit abweichendem Posten ist ungueltig")
        bad = json.loads(json.dumps(a))
        bad["schema"] = "x"
        self.assertTrue(bf.validate_answers(bad, ITEMS))
        self.assertEqual(bf.validate_answers({}, ITEMS)[0][:12], "Pflichtfelde")


@unittest.skipUnless(hu.HAVE_PLAYWRIGHT and hu.HAVE_EDGE, "Playwright (Python) oder Edge fehlt: Browsertests uebersprungen")
class HeadlessRestore(unittest.TestCase):
    """Echter Edge, headless, eigenes Temp-Profil (kein sichtbares Fenster). Prueft die Wiederherstellung aus localStorage."""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="formular_test_"))
        cls.file = cls.dir / "formular.html"
        cls.file.write_text(PAGE, encoding="utf-8", newline="\n")
        cls.key = f"ticket-master.decisions.{bf.DOC_ID}.{DIGEST[:16]}"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def seed(self, explicit):
        st = {"choice": {i["id"]: i["rec"] for i in ITEMS}, "note": {"V1": "alte Anmerkung"}, "via": {i["id"]: "bulk" for i in ITEMS},
              "agpl": {"choice": "bestätigen", "note": ""}, "bulk": {"bundle-alle": True},
              "gesamt": {"explicit": explicit, "at": "2026-11-01T10:00:00.000Z" if explicit else None}, "restored": None, "savedLocal": "2026-11-01T10:00:00.000Z"}
        return json.dumps(st)

    def load_with_state(self, explicit):
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.goto(self.file.as_uri())
            hu.ready(page)
            page.evaluate("([k, s]) => localStorage.setItem(k, s)", [self.key, self.seed(explicit)])
            page.reload()
            hu.ready(page)
            return page.evaluate("""() => ({
                progress: document.querySelector('.js-progress').textContent,
                explicit: window.__FORM__.state.gesamt.explicit,
                gesamtText: document.getElementById('gesamt-state').textContent,
                restoreVisible: !document.getElementById('restore-note').hidden,
                restoreText: document.getElementById('restore-note').innerText,
                toast: document.getElementById('toast').textContent,
                note: document.querySelector('#item-V1 textarea').value,
                v1: (document.querySelector('#item-V1 input:checked') || {}).value || null,
                answers: window.__FORM__.buildAnswers() })""")

    def test_restore_never_adopts_gesamtabnahme(self):
        r = self.load_with_state(explicit=True)
        self.assertEqual(r["progress"], "24 von 24 beantwortet", "Einzelwahlen werden wiederhergestellt")
        self.assertEqual((r["note"], r["v1"]), ("alte Anmerkung", "A"))
        self.assertFalse(r["explicit"], "Gesamtabnahme darf aus einem alten Stand NIE uebernommen werden")
        self.assertEqual(r["gesamtText"], "Gesamtabnahme: nicht erklärt")
        self.assertFalse(r["answers"]["gesamtabnahme"]["explicit"])
        self.assertEqual(r["answers"]["bulk_actions"], {}, "auch keine alte Bestaetigung von Massenaktionen")
        self.assertTrue(r["restoreVisible"])
        self.assertIn("Gesamtabnahme", r["restoreText"], "sichtbarer Hinweis, dass sie erneut ausdruecklich bestaetigt werden muss")
        self.assertIn("Gesamtabnahme", r["toast"])

    def test_restore_without_gesamtabnahme_shows_no_gesamt_hint(self):
        r = self.load_with_state(explicit=False)
        self.assertEqual(r["progress"], "24 von 24 beantwortet")
        self.assertFalse(r["explicit"])
        self.assertTrue(r["restoreVisible"])
        self.assertNotIn("Gesamtabnahme", r["restoreText"])
        self.assertEqual(r["toast"], "")

    def test_fresh_bulk_confirmation_still_works(self):
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.goto(self.file.as_uri())
            hu.ready(page)
            page.click("#top-panel [data-bulk=all]")
            page.click("#dlg-buttons button.primary")
            r = page.evaluate("() => ({explicit: window.__FORM__.state.gesamt.explicit, n: Object.keys(window.__FORM__.state.choice).length})")
        self.assertEqual(r, {"explicit": True, "n": 24})


class SaveArea(unittest.TestCase):
    """Ohne Browser: der Sicherungsbereich ist im gebauten Formular vorhanden (Regel 9)."""

    def test_backup_ids_exist_and_no_start_in(self):
        for ident in ("btn-download", "btn-copy", "btn-draft", "answer-text", "save-links", "save-state"):
            self.assertIn(f'id="{ident}"', PAGE, ident)
        self.assertNotIn("startIn", PAGE, "kein startIn: Edge sperrt Systemordner wie Dokumente")
        self.assertIn(".USR", PAGE, "der gewuenschte Ordner wird im Dokument genannt")

    def test_no_automatic_multi_download(self):
        js = PAGE.split("<script>", 1)[1]
        self.assertNotIn("setTimeout(function () { download(", js, "kein zeitversetzter programmatischer Mehrfach-Download")


@unittest.skipUnless(hu.HAVE_PLAYWRIGHT and hu.HAVE_EDGE, "Playwright (Python) oder Edge fehlt: Browsertests uebersprungen")
class HeadlessSave(SaveTestsMixin, unittest.TestCase):
    """Regel 9 am Formular des Referenzdokuments (Tests siehe savetests.py)."""

    PAGE_TEXT = PAGE
    ITEMS_ = ITEMS
    validate_answers = staticmethod(bf.validate_answers)


if __name__ == "__main__":
    unittest.main(verbosity=2)
