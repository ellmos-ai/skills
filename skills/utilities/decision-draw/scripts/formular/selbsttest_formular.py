"""Tests fuer build_formular.py (Standardbibliothek + markdown): python -m unittest selbsttest_formular -v

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

import build_formular as bf
import headless_util as hu

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
class HeadlessSave(unittest.TestCase):
    """Regel 9: Speichern haengt nie von einem Dialog ab. Echter Edge, headless, eigenes Temp-Profil, nie ein sichtbares Fenster.

    Jeder Fall setzt per Init-Skript eine Fehlerquelle (Ordnerdialog bricht ab, SecurityError, Schreibfehler, blockierter Download,
    fehlende Zwischenablage, Fehler beim Bau der Kopie) und prueft: Knopf sichtbar, Text gueltig, keine falsche Erfolgsmeldung."""

    SNAP = """() => {
        const q = s => document.querySelector(s);
        const vis = e => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
        return { state: q('#save-state') ? q('#save-state').innerText : '', dl: vis(q('#btn-download')), copy: vis(q('#btn-copy')),
                 draft: vis(q('#btn-draft')), text: q('#answer-text') ? q('#answer-text').value : null, textVisible: vis(q('#answer-text')),
                 links: document.querySelectorAll('#save-links a').length, log: window.__log || null };
    }"""
    NO_PICKER = "window.showDirectoryPicker = undefined;"

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="formular_save_"))
        cls.file = cls.dir / "formular.html"
        cls.file.write_text(PAGE, encoding="utf-8", newline="\n")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def drive(self, init_js=None, after=None, save=True, wait=1200):
        """Zwei Posten per Klick beantworten, speichern und bestaetigen, dann den Zustand der Seite zurueckgeben."""
        errors, got = [], []
        with hu.headless_context() as ctx:
            ctx.on("download", lambda d: got.append(d))
            page = ctx.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            if init_js:
                page.add_init_script(init_js)
            page.goto(self.file.as_uri())
            hu.ready(page)
            page.click('#item-V1 input[value="A"]')
            page.click('#item-V3 input[value="A"]')
            if save:
                page.click("#top-panel .js-save")
                page.click("#dlg-buttons button.primary")
                page.wait_for_timeout(wait)
            snap = page.evaluate(self.SNAP)
            extra = after(page, got) if after else None
            snap2 = page.evaluate(self.SNAP) if after else snap
        return {"snap": snap, "after": snap2, "extra": extra, "errors": errors, "downloads": got}

    def assert_safety_net(self, snap, label):
        self.assertTrue(snap["dl"], label + ": Knopf 'Als Datei herunterladen' sichtbar")
        self.assertTrue(snap["copy"], label + ": Knopf 'Antwort als Text kopieren' sichtbar")
        self.assertTrue(snap["textVisible"], label + ": Textfeld sichtbar")
        self.assertEqual(bf.validate_answers(json.loads(snap["text"]), ITEMS), [], label + ": Text ist eine gueltige Antwortdatei")

    def test_picker_abort_keeps_download_and_text(self):
        r = self.drive("window.showDirectoryPicker = () => Promise.reject(new DOMException('abgebrochen', 'AbortError'));")
        self.assertIn("abgebrochen", r["snap"]["state"])
        self.assertNotIn("gespeichert", r["snap"]["state"].lower())
        self.assertGreaterEqual(r["snap"]["links"], 1, "Download-Links stehen nach dem Abbruch bereit")
        self.assert_safety_net(r["snap"], "AbortError")

    def test_security_error_is_named_and_not_reported_as_saved(self):
        r = self.drive("window.showDirectoryPicker = () => Promise.reject(new DOMException('system', 'SecurityError'));")
        self.assertIn("SecurityError", r["snap"]["state"])
        self.assertNotIn("Gespeichert in", r["snap"]["state"])
        self.assertEqual(r["downloads"], [], "kein automatischer Download ohne Klick")
        self.assert_safety_net(r["snap"], "SecurityError")

    def test_write_error_on_second_file_is_no_success(self):
        init = ("window.showDirectoryPicker = async () => ({name: 'Fake', getFileHandle: async (name) => ({createWritable: async () => ({"
                "write: async () => { if (name.indexOf('BEANTWORTET') >= 0) throw new DOMException('platte', 'NotAllowedError'); },"
                "close: async () => {} })})});")
        r = self.drive(init)
        self.assertIn("NotAllowedError", r["snap"]["state"])
        self.assertNotIn("Gespeichert in", r["snap"]["state"])
        self.assert_safety_net(r["snap"], "Schreibfehler")

    def test_saved_is_claimed_only_after_both_files_are_closed(self):
        init = ("window.__log = {writes: 0, closes: 0}; window.showDirectoryPicker = async () => ({name: 'Fake', getFileHandle: async (name) => ({"
                "createWritable: async () => ({write: async () => { window.__log.writes++; },"
                "close: async () => { if (name.indexOf('BEANTWORTET') >= 0) await new Promise(r => setTimeout(r, 900)); window.__log.closes++; } })})});")
        early = self.drive(init, wait=300)
        self.assertNotIn("Gespeichert in", early["snap"]["state"], "300 ms nach dem Klick ist die zweite Datei noch nicht geschlossen")
        late = self.drive(init, wait=2500)
        self.assertIn("Gespeichert in", late["snap"]["state"])
        self.assertEqual(late["snap"]["log"], {"writes": 2, "closes": 2})

    def test_download_path_needs_user_clicks_and_never_claims_saved(self):
        def click_first(page, got):
            with page.expect_download() as info:
                page.click("#save-links a >> nth=0")
            d = info.value
            page.wait_for_timeout(300)
            return {"name": d.suggested_filename, "text": Path(d.path()).read_text(encoding="utf-8")}

        r = self.drive(self.NO_PICKER, after=click_first)
        self.assertEqual(r["snap"]["links"], 2, "Antwortdatei und beantwortete Kopie als zwei einzeln klickbare Links")
        self.assertTrue(r["extra"]["name"].endswith(".antwort.json"), r["extra"]["name"])
        self.assertEqual(bf.validate_answers(json.loads(r["extra"]["text"]), ITEMS), [])
        self.assertEqual(json.loads(r["extra"]["text"]), json.loads(r["snap"]["text"]), "Datei und Text kommen aus demselben Stand")
        self.assertNotIn("Gespeichert in", r["after"]["state"])
        self.assertIn("angestoßen", r["after"]["state"])
        self.assertIn("nicht prüf", r["after"]["state"])
        self.assert_safety_net(r["snap"], "Download-Weg")

    def test_no_download_starts_without_a_click(self):
        r = self.drive(self.NO_PICKER, wait=2000)
        self.assertEqual(r["downloads"], [], "kein programmatischer Mehrfach-Download im Abstand")

    def test_blocked_download_keeps_buttons_and_does_not_claim_success(self):
        def press(page, got):
            page.click("#btn-download")
            page.wait_for_timeout(500)

        init = self.NO_PICKER + " HTMLAnchorElement.prototype.click = function () { throw new Error('blockiert'); };"
        r = self.drive(init, save=False, after=press)
        self.assertIn("nicht", r["after"]["state"])
        self.assertIn("blockiert", r["after"]["state"])
        self.assertNotIn("Download angestoßen", r["after"]["state"])
        self.assert_safety_net(r["after"], "blockierter Download")

    def test_clipboard_missing_or_denied_leaves_the_text_to_copy_by_hand(self):
        def press(page, got):
            page.click("#btn-copy")
            page.wait_for_timeout(500)

        for label, init in (("fehlt", "Object.defineProperty(navigator, 'clipboard', {value: undefined, configurable: true});"),
                            ("verweigert", "Object.defineProperty(navigator, 'clipboard', {value: {writeText: () => Promise.reject(new DOMException('x', 'NotAllowedError'))}, configurable: true});")):
            r = self.drive(init, save=False, after=press)
            self.assertEqual(r["errors"], [], "Zwischenablage " + label + ": kein Seitenfehler")
            self.assertIn("markiere", r["after"]["state"].lower(), "Zwischenablage " + label)
            self.assert_safety_net(r["after"], "Zwischenablage " + label)

    def test_error_while_building_the_copy_is_visible_and_the_answer_survives(self):
        init = (self.NO_PICKER + " const orig = Node.prototype.cloneNode; Node.prototype.cloneNode = function () {"
                " if (this === document.documentElement) throw new Error('clone-boom'); return orig.apply(this, arguments); };")
        r = self.drive(init)
        self.assertIn("clone-boom", r["snap"]["state"])
        self.assertIn("Kopie", r["snap"]["state"])
        self.assertEqual(r["snap"]["links"], 1, "die Antwortdatei bleibt trotz fehlender Kopie herunterladbar")
        self.assert_safety_net(r["snap"], "Fehler beim Bau der Kopie")

    def test_draft_can_be_saved_any_time_without_gesamtabnahme(self):
        def press(page, got):
            with page.expect_download() as info:
                page.click("#btn-draft")
            d = info.value
            return {"name": d.suggested_filename, "obj": json.loads(Path(d.path()).read_text(encoding="utf-8"))}

        r = self.drive(self.NO_PICKER, save=False, after=press)
        obj = r["extra"]["obj"]
        self.assertIn("zwischenstand", r["extra"]["name"].lower())
        self.assertEqual(bf.validate_answers(obj, ITEMS), [])
        self.assertFalse(obj["gesamtabnahme"]["explicit"])
        self.assertEqual(obj["counts"]["answered"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
