"""Selbsttest fuer das generische Formular-Template (build_form.py): python -m unittest selbsttest_form -v

Braucht keine Umgebungsvariablen und liest nur example_form.json und form.schema.json. Die Datei heisst bewusst nicht test_*.py
(sie wuerde sonst von der Suite dieses Repos eingesammelt; die Browserklassen brauchen Python-Playwright und Edge).

Daten: Laengengrenzen sind Fehler (nie stilles Kuerzen), Pflichtfelder, Empfehlung/Optionen, Bilder (Groesse, Typ, Beschriftung),
Details nur als Text bzw. escaped Markdown, byte-stabiler Hash, Schema und Generator im Gleichschritt.
Browser (nur headless, eigenes Temp-Profil, nie ein sichtbares Fenster): Regel 9 am Template (savetests.py), Rueckfrage als eigener
Zustand, Bilderserie und aufklappbare Details.
"""
import copy
import json
import re
import unittest
from pathlib import Path
from unittest import mock

import build_form as bf
import headless_util as hu
from savetests import SaveTestsMixin

HERE = Path(__file__).resolve().parent
EXAMPLE = HERE / "example_form.json"
SCHEMA = HERE / "form.schema.json"
PAGE, DIGEST, ITEMS = bf.build(json.loads(EXAMPLE.read_text(encoding="utf-8")), HERE)
PNG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="


def load():
    return copy.deepcopy(json.loads(EXAMPLE.read_text(encoding="utf-8")))


def post(data, kuerzel):
    return next(p for b in data["buendel"] for p in b["posten"] if p["kuerzel"] == kuerzel)


def errors_of(data):
    try:
        bf.build(data, HERE)
    except bf.FormError as exc:
        return exc.errors
    return []


class Daten(unittest.TestCase):
    def assert_error(self, data, *needles):
        errs = errors_of(data)
        self.assertTrue(any(all(n in e for n in needles) for e in errs), f"{needles} nicht in {errs}")

    def test_example_builds_and_is_byte_stable(self):
        page2, digest2, items2 = bf.build(load(), HERE)
        self.assertEqual(page2, PAGE)
        embedded, recomputed = bf.blank_hash(PAGE)
        self.assertEqual((embedded, recomputed), (DIGEST, DIGEST))
        self.assertEqual([i["id"] for i in ITEMS], ["V1", "V3", "V4"])

    def test_limits_are_errors_never_silent_truncation(self):
        for field, limit in (("kontext", 250), ("frage", 200), ("kosten_aufwand", 160), ("risiko_rueckgaengig", 160),
                             ("folge_bei_nein", 160), ("frist", 160), ("titel", 80)):
            ok = load()
            post(ok, "V1")[field] = "x" * limit
            self.assertEqual(errors_of(ok), [], f"{field}: genau {limit} Zeichen sind erlaubt")
            bad = load()
            post(bad, "V1")[field] = "x" * (limit + 1)
            self.assert_error(bad, "V1", field, str(limit))
        d = load()
        post(d, "V1")["optionen"][0]["wirkung"] = "x" * 161
        self.assert_error(d, "V1", "wirkung", "160")
        d = load()
        post(d, "V1")["empfehlung"]["grund"] = "x" * 161
        self.assert_error(d, "V1", "grund", "160")
        d = load()
        d["kontext_kurz"] = "x" * 401
        self.assert_error(d, "kontext_kurz", "400")

    def test_error_message_names_the_fix(self):
        d = load()
        post(d, "V1")["kontext"] = "x" * 300
        self.assertTrue(any("details_markdown" in e for e in errors_of(d)), "Hinweis: Details gehoeren in details_markdown")

    def test_required_fields_may_say_keine_but_not_be_missing(self):
        for field in ("kosten_aufwand", "risiko_rueckgaengig", "folge_bei_nein"):
            d = load()
            post(d, "V3")[field] = "keine"
            self.assertEqual(errors_of(d), [], field)
            for broken in ("missing", ""):
                d = load()
                if broken == "missing":
                    del post(d, "V3")[field]
                else:
                    post(d, "V3")[field] = ""
                self.assert_error(d, "V3", field)

    def test_options_and_recommendation(self):
        d = load()
        post(d, "V1")["empfehlung"]["option"] = "Z"
        self.assert_error(d, "V1", "Empfehlung")
        d = load()
        del post(d, "V1")["empfehlung"]["grund"]
        self.assert_error(d, "V1", "grund")
        d = load()
        post(d, "V1")["optionen"] = post(d, "V1")["optionen"][:1]
        self.assert_error(d, "V1", "Optionen")
        d = load()
        post(d, "V3")["kuerzel"] = "V1"
        self.assert_error(d, "V1", "doppelt")
        d = load()
        del post(d, "V1")["empfehlung"]
        self.assertEqual(errors_of(d), [], "ein Posten ohne Empfehlung ist erlaubt")

    def test_images_are_embedded_and_limited(self):
        self.assertEqual(PAGE.count('<img src="data:image/png;base64,'), 2)
        self.assertIn("Startseite vorher", PAGE)
        d = load()
        post(d, "V1")["bilder"][0]["beschriftung"] = ""
        self.assert_error(d, "V1", "beschriftung")
        d = load()
        post(d, "V1")["bilder"][0]["data_uri"] = "data:text/html;base64,PGI+eDwvYj4="
        self.assert_error(d, "V1", "Bildtyp")
        with mock.patch.object(bf, "IMG_TOTAL_MAX", 100):
            self.assert_error(load(), "Gesamt", "100")
        with mock.patch.object(bf, "IMG_MAX", 50):
            self.assert_error(load(), "V1", "Bild", "50")

    def test_image_from_path_and_oversize_file(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            big = Path(tmp) / "gross.png"
            big.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * (400 * 1024 + 10))
            d = load()
            post(d, "V1")["bilder"] = [{"pfad": str(big), "beschriftung": "zu gross"}]
            self.assert_error(d, "V1", "400")
            small = Path(tmp) / "klein.png"
            small.write_bytes(bf.decode_data_uri(PNG)[1])
            d = load()
            post(d, "V1")["bilder"] = [{"pfad": "klein.png", "beschriftung": "klein"}]
            page, _, _ = bf.build(d, Path(tmp))
            self.assertIn('<img src="data:image/png;base64,', page)
            svg = Path(tmp) / "x.svg"
            svg.write_text("<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8")
            d = load()
            post(d, "V1")["bilder"] = [{"pfad": "x.svg", "beschriftung": "svg"}]
            with self.assertRaises(bf.FormError):
                bf.build(d, Path(tmp))

    def test_details_markdown_is_escaped(self):
        d = load()
        post(d, "V4")["details_markdown"] = "<script>alert(1)</script> **fett**"
        page, _, _ = bf.build(d, HERE)
        self.assertNotIn("<script>alert(1)", page)
        self.assertIn("&lt;script&gt;alert(1)", page)
        d = load()
        post(d, "V4")["details_markdown"] = "[klick](javascript:alert(1))"
        self.assert_error(d, "V4", "Link")

    def test_nothing_preselected_no_network(self):
        self.assertIsNone(re.search(r"<input[^>]*\schecked", PAGE))
        self.assertIsNone(re.search(r'(?:src|href|action)="https?://', PAGE))
        self.assertNotIn("<link", PAGE)
        self.assertNotIn("alert(", PAGE.split("<script>", 1)[1])
        self.assertEqual(len(re.findall(r'<fieldset class="item" id="item-', PAGE)), 3)
        self.assertEqual(len(re.findall(r'value="rueckfrage"', PAGE)), 3, "jeder Posten hat die Wahl Rueckfrage")

    def test_schema_is_in_step_with_the_generator(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        props = schema["$defs"]["posten"]["properties"]
        for field in ("kontext", "frage", "kosten_aufwand", "risiko_rueckgaengig", "folge_bei_nein", "frist", "titel"):
            self.assertEqual(props[field]["maxLength"], bf.LIMITS[field], field)
        self.assertEqual(schema["properties"]["kontext_kurz"]["maxLength"], bf.LIMITS["kontext_kurz"])
        for field in ("kuerzel", "titel", "kontext", "frage", "optionen", "kosten_aufwand", "risiko_rueckgaengig", "folge_bei_nein"):
            self.assertIn(field, schema["$defs"]["posten"]["required"], field)
        self.assertIn("bilder", props)
        try:
            import jsonschema
        except ImportError:  # pragma: no cover
            return
        jsonschema.validate(load(), schema)

    def test_static_save_area_and_no_start_in(self):
        for ident in ("btn-download", "btn-copy", "btn-draft", "answer-text", "save-links", "save-state"):
            self.assertIn(f'id="{ident}"', PAGE, ident)
        self.assertNotIn("startIn", PAGE)
        js = PAGE.split("<script>", 1)[1]
        self.assertNotIn("setTimeout(function () { download(", js)

    def test_answers_validator_knows_rueckfrage(self):
        d = {"schema": bf.SCHEMA, "document_id": "BEISPIEL_2026-01-01", "document_sha256": DIGEST, "saved_at": "2026-01-01T10:00:00.000Z",
             "bulk_actions": {}, "gesamtabnahme": {"explicit": False, "at": None},
             "counts": {"total": 3, "answered": 1, "questions": 1, "open": 1}, "answers": {}}
        for it in ITEMS:
            d["answers"][it["id"]] = {"choice": None, "choice_label": None, "state": "open", "note": "", "via": None, "recommended": it["rec"],
                                      "avatar_prediction": it["av_pred"], "avatar_confidence": it["av_conf"], "marked": it["marked"]}
        d["answers"]["V1"].update(choice="A", choice_label="Ja, umziehen", state="answered", via="single")
        d["answers"]["V3"].update(choice="rueckfrage", choice_label="Rückfrage / mehr Info nötig", state="question", note="Vor- und Nachteile?", via="single")
        self.assertEqual(bf.validate_answers(d, ITEMS), [])
        d["answers"]["V3"]["state"] = "answered"
        self.assertTrue(bf.validate_answers(d, ITEMS))


@unittest.skipUnless(hu.HAVE_PLAYWRIGHT and hu.HAVE_EDGE, "Playwright (Python) oder Edge fehlt: Browsertests uebersprungen")
class HeadlessSaveTemplate(SaveTestsMixin, unittest.TestCase):
    """Regel 9 am Template: dieselben Tests wie am Dokumentgenerator."""

    PAGE_TEXT = PAGE
    ITEMS_ = ITEMS
    validate_answers = staticmethod(bf.validate_answers)


@unittest.skipUnless(hu.HAVE_PLAYWRIGHT and hu.HAVE_EDGE, "Playwright (Python) oder Edge fehlt: Browsertests uebersprungen")
class HeadlessTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile

        cls.dir = Path(tempfile.mkdtemp(prefix="form_template_"))
        cls.file = cls.dir / "form.html"
        cls.file.write_text(PAGE, encoding="utf-8", newline="\n")

    @classmethod
    def tearDownClass(cls):
        import shutil

        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_rueckfrage_is_its_own_state_and_blocks_gesamtabnahme(self):
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.goto(self.file.as_uri())
            hu.ready(page)
            page.click('#item-V1 input[value="rueckfrage"]')
            page.fill("#item-V1 textarea", "Vor- und Nachteile?")
            page.click('#item-V3 input[value="A"]')
            first = page.evaluate("() => ({a: window.__FORM__.buildAnswers(), progress: document.querySelector('.js-progress').textContent})")
            page.click("#top-panel [data-bulk=all]")
            page.click("#dlg-buttons button.primary")
            after_bulk = page.evaluate("() => ({explicit: window.__FORM__.state.gesamt.explicit, v1: window.__FORM__.state.choice.V1})")
            page.click("#top-panel .js-save")
            dialog = page.evaluate("() => document.getElementById('dlg-body').innerText")
        a = first["a"]
        self.assertEqual((a["answers"]["V1"]["state"], a["answers"]["V1"]["choice"], a["answers"]["V1"]["note"]), ("question", "rueckfrage", "Vor- und Nachteile?"))
        self.assertEqual(a["counts"], {"total": 3, "answered": 1, "questions": 1, "open": 1})
        self.assertEqual(bf.validate_answers(a, ITEMS), [])
        self.assertIn("1 von 3 beantwortet", first["progress"])
        self.assertIn("1 Rückfrage", first["progress"])
        self.assertEqual(after_bulk, {"explicit": False, "v1": "rueckfrage"}, "eine Rueckfrage wird nie als Zustimmung gewertet")
        self.assertIn("Rückfrage", dialog)
        self.assertIn("V1", dialog)

    def test_images_details_and_facts_render(self):
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.goto(self.file.as_uri())
            hu.ready(page)
            r = page.evaluate("""() => {
                const c = document.getElementById('item-V1'), d = document.getElementById('item-V4');
                const figs = c.querySelectorAll('.bilder figure');
                return { figs: figs.length, caps: Array.from(figs).map(f => f.querySelector('figcaption').textContent),
                         before: !!(c.querySelector('.bilder').compareDocumentPosition(c.querySelector('.opts')) & Node.DOCUMENT_POSITION_FOLLOWING),
                         kontext: c.querySelector('.kontext').textContent, fakten: c.querySelector('.fakten').innerText,
                         detailsOpen: d.querySelector('details.mehr').open, detailsText: d.querySelector('details.mehr').textContent.includes('Dreijahrespreis') };
            }""")
        self.assertEqual(r["figs"], 2)
        self.assertTrue(r["caps"][0].startswith("Startseite vorher"))
        self.assertTrue(r["before"], "Bilderserie steht ueber den Entscheidungsfeldern")
        self.assertIn("Hosting", r["kontext"] + "Hosting")
        for label in ("Kosten", "Risiko", "Frist", "Folge"):
            self.assertIn(label, r["fakten"])
        self.assertFalse(r["detailsOpen"], "Details nur aufklappbar")
        self.assertTrue(r["detailsText"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
