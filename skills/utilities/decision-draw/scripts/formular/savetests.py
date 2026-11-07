"""Regel 9 (Speichern haengt nie von einem Dialog ab): gemeinsame Headless-Tests fuer beide Generatoren.

Eine konkrete Testklasse erbt von SaveTestsMixin und unittest.TestCase und setzt PAGE_TEXT (gebautes Formular),
ITEMS_ (Posten) und validate_answers (Validator). Das Formular braucht die Posten V1 und V3 mit der Option A.
Nur Python-Playwright headless mit Temp-Profil; nie ein sichtbares Fenster, nie die Playwright-MCP-Werkzeuge."""
import json
import shutil
import tempfile
from pathlib import Path

import headless_util as hu


class SaveTestsMixin:
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
        cls.file.write_text(cls.PAGE_TEXT, encoding="utf-8", newline="\n")

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
        self.assertEqual(self.validate_answers(json.loads(snap["text"]), self.ITEMS_), [], label + ": Text ist eine gueltige Antwortdatei")

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
        self.assertEqual(self.validate_answers(json.loads(r["extra"]["text"]), self.ITEMS_), [])
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
        self.assertEqual(self.validate_answers(obj, self.ITEMS_), [])
        self.assertFalse(obj["gesamtabnahme"]["explicit"])
        self.assertEqual(obj["counts"]["answered"], 2)
