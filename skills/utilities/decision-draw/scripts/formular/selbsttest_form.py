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
from html.parser import HTMLParser
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
            post(d, "V1")["bilder"] = [{"pfad": "gross.png", "beschriftung": "zu gross"}]
            with self.assertRaises(bf.FormError) as caught:
                bf.build(d, Path(tmp))
            self.assertTrue(any("V1" in e and "400" in e for e in caught.exception.errors), caught.exception.errors)
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


class Elements(HTMLParser):
    """Liest HTML mit dem Parser statt mit Regex (Gross-/Kleinschreibung und Endtags wie `</script\\t>` erledigt der Parser).

    `starts` = (Tag, {Attribut: Wert}) aller Starttags AUSSERHALB von script/style, `scripts` = Zahl der script-Elemente."""

    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.starts: list[tuple[str, dict[str, str]]] = []
        self.scripts = 0
        self._raw = 0
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.scripts += 1
        if tag in ("script", "style"):
            self._raw += 1
        elif not self._raw:
            self.starts.append((tag, {k: v or "" for k, v in attrs}))

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._raw:
            self._raw -= 1

    def urls(self) -> list[str]:
        return [v for _, attrs in self.starts for k, v in attrs.items() if k in ("href", "src")]


class DatenSicherheit(unittest.TestCase):
    """Befunde F1 bis F7 der mechanischen Pruefung von skills#98 (s1): jede Nutzlast aus dem Befund, ohne FORMULAR_MD."""

    def assert_error(self, data, *needles):
        errs = errors_of(data)
        self.assertTrue(any(all(n in e for n in needles) for e in errs), f"{needles} nicht in {errs}")

    # --- F1: Link-Schemata in details_markdown (Normalisierung + Positivliste) -------------------------------------
    UNSAFE = {
        "LF im Schema": "[x](java\nscript:window.__pwn=14)",
        "CR im Schema": "[x](java\rscript:window.__pwn=14)",
        "0x01 vorn": "[x](\u0001javascript:window.__pwn=15)",
        "0x04 vorn": "[x](\u0004javascript:window.__pwn=15)",
        "0x08 vorn": "[x](\u0008javascript:window.__pwn=15)",
        "0x0e vorn": "[x](\u000ejavascript:window.__pwn=15)",
        "0x1b vorn": "[x](\u001bjavascript:window.__pwn=15)",
        "klar": "[x](javascript:window.__pwn=10)",
        "gross": "[x](JaVaScRiPt:window.__pwn=11)",
        "Leerzeichen": "[x]( javascript:window.__pwn=12)",
        "Tab": "[x](java\tscript:window.__pwn=13)",
        "Referenz": "[x][1]\n\n[1]: javascript:window.__pwn=20",
        "spitze Klammern": "[x](<javascript:window.__pwn=22>)",
        "Entity": "[x](&#106;avascript:window.__pwn=19)",
        "data": "[x](data:text/html;base64,PHNjcmlwdD4=)",
        "vbscript": "[x](vbscript:msgbox(1))",
        "Bild mit javascript": "![x](javascript:window.__pwn=27)",
        "Bild aus dem Netz": "![x](https://tracker.example/p.png)",
        "relativ ohne Schema": "[x](seite.html)",
    }

    def test_f1_unsafe_links_are_refused(self):
        for label, md in self.UNSAFE.items():
            with self.subTest(label):
                d = load()
                post(d, "V4")["details_markdown"] = md
                self.assertTrue(errors_of(d), f"{label}: muss abgelehnt werden")

    def test_f1_other_control_characters_in_the_text_are_refused(self):
        for code in (0x00, 0x01, 0x04, 0x08, 0x0E, 0x1B, 0x7F, 0x85):
            with self.subTest(hex(code)):
                d = load()
                post(d, "V4")["details_markdown"] = f"Text {chr(code)} mehr"
                self.assert_error(d, "V4", "Steuerzeichen")

    def test_f1_safe_links_are_emitted_in_exactly_the_checked_form(self):
        d = load()
        post(d, "V4")["details_markdown"] = "[a](https://example.org/x?y=1&z=2) [b](#anker) [c](mailto:a@example.org) [d](/pfad) [e](./rel)"
        page, _, _ = bf.build(d, HERE)
        more = page.split('<details class="mehr">')[1].split("</details>")[0]
        self.assertEqual(re.findall(r'href="([^"]*)"', more),
                         ["https://example.org/x?y=1&amp;z=2", "#anker", "mailto:a@example.org", "/pfad", "./rel"])

    def test_f1_emitted_href_is_exactly_the_checked_value(self):
        d = load()
        post(d, "V4")["details_markdown"] = "[a](https://exa&#9;mple.org/x)"  # ein Tab per Entity: geprueft UND ausgegeben ohne Tab
        page, _, _ = bf.build(d, HERE)
        more = page.split('<details class="mehr">')[1].split("</details>")[0]
        self.assertEqual(re.findall(r'href="([^"]*)"', more), ["https://example.org/x"])

    def test_f1_every_href_and_src_of_the_page_is_on_the_allow_list(self):
        allowed = re.compile(r"^(?:https?:|mailto:|#|/|\./|data:image/(?:png|jpeg|webp|gif);base64,)")
        values = Elements(PAGE).urls()
        self.assertTrue(values)
        for value in values:
            self.assertRegex(value, allowed)

    def test_f1_the_page_check_reads_any_spelling_of_tags_and_attributes(self):
        # Negativkontrolle des Pruefwerkzeugs: eine Regex nur fuer Kleinschreibung uebersaehe genau diese Formen (CodeQL: Bad HTML filtering regexp).
        probe = Elements('<SCRIPT>x</SCRIPT><ScRiPt >y</script\t><A HREF="javascript:1">a</A><IMG SRC=" data:text/html,z" onerror=q>'
                         '<STYLE>a{}</STYLE><SCRIPT><a href="javascript:inside"></SCRIPT>')
        self.assertEqual(probe.scripts, 3)
        self.assertEqual(probe.urls(), ["javascript:1", " data:text/html,z"], "Inhalt von script/style zaehlt nicht, die Gross-Schreibung schon")
        self.assertIn("onerror", dict(probe.starts)["img"])

    def test_f2_the_form_has_exactly_the_two_expected_script_elements(self):
        d = load()
        post(d, "V1")["titel"] = "<!--<script>"
        post(d, "V1")["frage"] = "</SCRIPT><ScRiPt >window.__x=1</script\t>"
        page, _, _ = bf.build(d, HERE)
        self.assertEqual(Elements(page).scripts, 2, "Daten und Programm; kein weiteres Skript durch Nutzertext")

    # --- F2: '<' in Datenfeldern darf das Skript-Parsing nie kippen ------------------------------------------------
    def test_f2_no_less_than_sign_inside_the_embedded_data(self):
        d = load()
        post(d, "V1")["titel"] = "<!--<script>"
        post(d, "V1")["frage"] = "</script><script>window.__x=1</script>"
        post(d, "V1")["optionen"][0]["label"] = "a < b > c & d \u2028"
        page, _, _ = bf.build(d, HERE)
        data = page.split('id="form-data">', 1)[1].split("</script>", 1)[0]
        for char in "<>&\u2028\u2029":
            self.assertNotIn(char, data, repr(char))
        self.assertEqual(page.count("<script"), page.count("</script>"))
        self.assertEqual(json.loads(data)["items"][0]["theme"], "<!--<script>")

    # --- F3: Bildpfade bleiben im Datenordner, kein Dateizugriff vor der Pruefung ------------------------------------
    def test_f3_image_paths_stay_inside_the_data_folder(self):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "daten"
            (base / "sub").mkdir(parents=True)
            png = bf.decode_data_uri(PNG)[1]
            (Path(tmp) / "aussen.png").write_bytes(png)
            (base / "sub" / "ok.png").write_bytes(png)
            ok = load()
            post(ok, "V1")["bilder"] = [{"pfad": "sub/ok.png", "beschriftung": "ok"}]
            self.assertIn('<img src="data:image/png;base64,', bf.build(ok, base)[0])
            bad = {
                "..": "../aussen.png", "..\\": "..\\aussen.png", "sub/../..": "sub/../../aussen.png",
                "absolut": str(Path(tmp) / "aussen.png"), "UNC": "\\\\attacker.example\\share\\x.png",
                "UNC mit Schraegstrich": "//attacker.example/share/x.png", "Laufwerk": "C:\\Windows\\x.png",
                "erweitert": "\\\\?\\C:\\x.png", "Wurzel": "/etc/x.png",
            }
            for label, path in bad.items():
                with self.subTest(label):
                    d = load()
                    post(d, "V1")["bilder"] = [{"pfad": path, "beschriftung": "b"}]
                    with mock.patch.object(Path, "read_bytes", side_effect=AssertionError("Dateizugriff vor der Pruefung")):
                        self.assert_error(d, "V1", "pfad")
            outside = Path(tmp) / "draussen"
            outside.mkdir()
            (outside / "geheim.png").write_bytes(png)
            link = base / "link"
            try:
                os.symlink(outside, link, target_is_directory=True)
            except (OSError, NotImplementedError):
                import subprocess

                made = os.name == "nt" and subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                                                         capture_output=True).returncode == 0  # Junction braucht keine Rechte
                if not made:
                    self.skipTest("weder Symlink noch Junction anlegbar: nur die Textpruefungen wurden ausgefuehrt")
            d = load()
            post(d, "V1")["bilder"] = [{"pfad": "link/geheim.png", "beschriftung": "b"}]
            with self.assertRaises(bf.FormError) as caught:
                bf.build(d, base)  # der Link fuehrt aus dem Datenordner hinaus: abgelehnt, obwohl die Datei existiert
            self.assertTrue(any("V1" in e and "ausserhalb" in e for e in caught.exception.errors), caught.exception.errors)

    # --- F5: bisher nicht belegte Sicherungen ------------------------------------------------------------------------
    def test_f5_closing_script_tags_in_data_are_neutralised(self):
        d = load()
        post(d, "V3")["kontext"] = "</script><script>window.__x=1</script>"
        page, _, _ = bf.build(d, HERE)
        self.assertEqual(page.count("<script"), page.count("</script>"))
        self.assertIn("&lt;/script&gt;&lt;script&gt;window.__x=1&lt;/script&gt;", page)

    def test_f5_magic_bytes_are_checked(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "fake.png").write_bytes(b"<html><script>alert(1)</script></html>")
            d = load()
            post(d, "V1")["bilder"] = [{"pfad": "fake.png", "beschriftung": "b"}]
            with self.assertRaises(bf.FormError) as caught:
                bf.build(d, Path(tmp))
            self.assertTrue(any("kein image/png" in e for e in caught.exception.errors), caught.exception.errors)

    # --- F6: Nutzertext aus 64 Nullen bleibt Nutzertext -------------------------------------------------------------
    def test_f6_user_text_of_64_zeros_is_not_replaced_by_the_hash(self):
        zeros = "0" * 64
        d = load()
        post(d, "V3")["kontext"] = zeros
        page, digest, _ = bf.build(d, HERE)
        self.assertNotEqual(digest, zeros)
        self.assertIn(f'<p class="kontext">{zeros}</p>', page)
        self.assertEqual(page.count(digest), 2, "der Hash steht nur im Meta-Tag und in den Formulardaten")
        self.assertEqual(bf.blank_hash(page), (digest, digest))

    def test_f9_dead_option_id_branch_is_gone(self):
        self.assertNotIn("oid == RQ", (HERE / "build_form.py").read_text(encoding="utf-8"))


@unittest.skipUnless(hu.HAVE_PLAYWRIGHT and hu.HAVE_EDGE, "Playwright (Python) oder Edge fehlt: Browsertests uebersprungen")
class HeadlessSicherheit(unittest.TestCase):
    """F2, F5 (Restore) und F7 im Browser; nur headless, eigenes Temp-Profil, nie ein sichtbares Fenster."""

    @classmethod
    def setUpClass(cls):
        import tempfile

        cls.dir = Path(tempfile.mkdtemp(prefix="form_sicherheit_"))

    @classmethod
    def tearDownClass(cls):
        import shutil

        shutil.rmtree(cls.dir, ignore_errors=True)

    def page_file(self, data, name):
        page, digest, items = bf.build(data, HERE)
        path = self.dir / f"{name}.html"
        path.write_text(page, encoding="utf-8", newline="\n")
        return path, digest

    def test_f2_forms_with_comment_script_openers_in_every_field_still_run(self):
        d = load()
        evil = "<!--<script>"
        d["titel"] = d["kontext_kurz"] = evil
        post(d, "V1")["titel"] = post(d, "V1")["frage"] = post(d, "V1")["kontext"] = evil
        post(d, "V1")["optionen"][0]["label"] = post(d, "V1")["optionen"][0]["wirkung"] = evil
        path, _ = self.page_file(d, "f2")
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.goto(path.as_uri())
            hu.ready(page)
            self.assertEqual(page.evaluate("window.__FORM__.ITEMS.length"), 3)
            self.assertEqual(page.evaluate("window.__FORM__.ITEMS[0].theme"), evil)

    def test_f2_answered_copy_with_a_comment_script_note_still_opens_in_answered_mode(self):
        path, _ = self.page_file(load(), "f2copy")
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.add_init_script("window.showDirectoryPicker = undefined;")
            page.goto(path.as_uri())
            hu.ready(page)
            page.click('#item-V1 input[value="A"]')
            page.fill("#item-V1 textarea", "x <!--<script> y </script><b>z")
            page.click("#top-panel .js-save")
            page.click("#dlg-buttons button.primary")
            page.wait_for_selector("#save-links a")
            html = page.evaluate("""async () => {
                const a = Array.from(document.querySelectorAll('#save-links a')).find(x => x.download.indexOf('BEANTWORTET') >= 0);
                return a ? await (await fetch(a.href)).text() : null; }""")
            self.assertTrue(html)
            copy = self.dir / "kopie_BEANTWORTET.html"
            copy.write_text(html, encoding="utf-8", newline="\n")
            second = ctx.new_page()
            second.goto(copy.as_uri())
            second.wait_for_selector("body.answered", timeout=15000)
            self.assertTrue(second.evaluate("document.getElementById('ergebnis') !== null"))

    def seeded(self, ctx, path, digest, state):
        page = ctx.new_page()
        page.goto(path.as_uri())
        hu.ready(page)
        key = f"ticket-master.decisions.{load()['dokument_id']}.{digest[:16]}"
        page.evaluate("([k, s]) => localStorage.setItem(k, s)", [key, json.dumps(state)])
        page.reload()
        hu.ready(page)
        return page

    def test_f5_restore_never_adopts_the_overall_sign_off_at_the_template(self):
        path, digest = self.page_file(load(), "restore")
        state = {"choice": {"V1": "A", "V3": "C", "V4": "A"}, "note": {"V1": "alt"}, "via": {"V1": "bulk", "V3": "bulk", "V4": "bulk"},
                 "agpl": {"choice": None, "note": ""}, "bulk": {"bundle-alle": True},
                 "gesamt": {"explicit": True, "at": "2026-11-01T10:00:00.000Z"}, "restored": None, "savedLocal": "2026-11-01T10:00:00.000Z"}
        with hu.headless_context() as ctx:
            page = self.seeded(ctx, path, digest, state)
            r = page.evaluate("""() => ({explicit: window.__FORM__.state.gesamt.explicit, n: Object.keys(window.__FORM__.state.choice).length,
                answers: window.__FORM__.buildAnswers(), text: document.getElementById('gesamt-state').textContent})""")
        self.assertEqual(r["n"], 3, "Einzelwahlen kommen zurueck")
        self.assertFalse(r["explicit"], "die Gesamtabnahme wird aus einem alten Stand NIE uebernommen")
        self.assertEqual(r["answers"]["bulk_actions"], {})
        self.assertEqual(r["text"], "Gesamtabnahme: nicht erklärt")

    def test_f7_restore_ignores_values_that_are_no_option(self):
        path, digest = self.page_file(load(), "restore7")
        state = {"choice": {"V1": "ZZZ", "V3": "A", "V4": ["A"], "X9": "A"}, "note": {"V1": {"a": 1}, "V3": "ok"}, "via": {}, "bulk": {},
                 "gesamt": {"explicit": False, "at": None}, "savedLocal": "2026-11-01T10:00:00.000Z"}
        with hu.headless_context() as ctx:
            page = self.seeded(ctx, path, digest, state)
            r = page.evaluate("() => ({choice: window.__FORM__.state.choice, note: window.__FORM__.state.note})")
        self.assertEqual(r["choice"], {"V3": "A"})
        self.assertEqual(r["note"].get("V3"), "ok")
        self.assertNotIn("V1", r["note"])


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
