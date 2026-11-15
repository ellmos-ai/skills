"""Selbsttest des lokalen Speicherdienstes (serve_form.py). Aufruf: python -m unittest selbsttest_serve -v

Die Dienst-Tests laufen ohne Browser (http.client gegen einen Dienst im Thread). Der Ende-zu-Ende-Test (Formular im echten Edge,
headless, Temp-Profil, nie ein sichtbares Fenster) laeuft nur, wenn Python-Playwright und Edge vorhanden sind."""
import http.client
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path

import build_form
import headless_util as hu
import serve_form

HERE = Path(__file__).resolve().parent


class Svc:
    """Startet einen Dienst in einem Thread mit eigenem Zielordner und stoppt ihn wieder."""

    def __init__(self, **kw):
        self.tmp = tempfile.TemporaryDirectory(prefix="serve_form_")
        self.root = Path(self.tmp.name)
        self.form = self.root / "formular.html"
        self.form.write_text("<!doctype html><title>x</title>FORM", encoding="utf-8")
        self.out = self.root / "ziel"
        self.srv = serve_form.FormServer(self.form, self.out, **kw)
        self.thread = threading.Thread(target=self.srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        self.thread.start()

    def req(self, method, path, body=None, headers=None, host=None):
        c = http.client.HTTPConnection("127.0.0.1", self.srv.port, timeout=5)
        h = {"Host": host or "127.0.0.1:%d" % self.srv.port}
        h.update(headers or {})
        c.request(method, path, body=body, headers=h)
        r = c.getresponse()
        data = r.read()
        c.close()
        return r.status, data

    def save(self, files, token=None, origin="same", ctype="application/json", host=None):
        origin = "http://127.0.0.1:%d" % self.srv.port if origin == "same" else origin
        h = {"Content-Type": ctype}
        if origin:
            h["Origin"] = origin
        body = json.dumps({"files": files}).encode()
        return self.req("POST", "/%s/save" % (token or self.srv.token), body, h, host)

    def empty_target(self):
        return not self.out.exists() or not any(self.out.iterdir())

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()


class Dienst(unittest.TestCase):
    def setUp(self):
        self.s = Svc()
        self.addCleanup(self.s.close)

    def test_post_writes_files_atomically_and_overwrites(self):
        files = [{"name": "d.antwort.json", "text": '{"a": "ä"}'}, {"name": "d_BEANTWORTET.html", "text": "<p>ok</p>"}]
        code, body = self.s.save(files)
        self.assertEqual(code, 200, body)
        self.assertEqual((self.s.out / "d.antwort.json").read_text(encoding="utf-8"), '{"a": "ä"}')
        self.assertEqual(json.loads(body)["written"], ["d.antwort.json", "d_BEANTWORTET.html"])
        self.assertEqual(self.s.save([{"name": "d.antwort.json", "text": "neu"}])[0], 200)
        self.assertEqual((self.s.out / "d.antwort.json").read_text(encoding="utf-8"), "neu", "gleicher Name wird ersetzt")
        self.assertEqual([p.name for p in self.s.out.iterdir() if p.name.endswith(".tmp")], [], "keine tmp-Reste")

    def test_get_serves_the_form_unchanged_and_ping_works(self):
        self.assertEqual(self.s.req("GET", "/%s/" % self.s.srv.token), (200, b"<!doctype html><title>x</title>FORM"))
        self.assertEqual(self.s.req("GET", "/%s/ping" % self.s.srv.token)[0], 204)

    def test_wrong_or_missing_token_is_403(self):
        self.assertEqual(self.s.save([{"name": "a.json", "text": "x"}], token="falsch")[0], 403)
        self.assertEqual(self.s.req("GET", "/")[0], 403)
        self.assertEqual(self.s.req("GET", "/falsch/")[0], 403)
        self.assertTrue(self.s.empty_target())

    def test_foreign_origin_or_missing_origin_is_403(self):
        f = [{"name": "a.json", "text": "x"}]
        self.assertEqual(self.s.save(f, origin="http://evil.example")[0], 403)
        self.assertEqual(self.s.save(f, origin="http://127.0.0.1:1")[0], 403)
        self.assertEqual(self.s.save(f, origin=None)[0], 403)
        self.assertTrue(self.s.empty_target())

    def test_foreign_host_header_is_403(self):
        self.assertEqual(self.s.req("GET", "/%s/" % self.s.srv.token, host="evil.example")[0], 403, "DNS-Rebinding")

    def test_non_json_content_type_is_415(self):
        self.assertEqual(self.s.save([{"name": "a.json", "text": "x"}], ctype="text/plain")[0], 415)

    def test_too_large_is_413(self):
        s = Svc(max_bytes=200)
        self.addCleanup(s.close)
        self.assertEqual(s.save([{"name": "a.json", "text": "x" * 500}])[0], 413)
        self.assertEqual(s.save([{"name": "a.json", "text": "x"}])[0], 200)

    def test_path_traversal_and_bad_names_are_rejected(self):
        bad = ["../x.json", "..\\x.json", "a/b.json", "/abs.json", "C:\\x.json", "x.exe", "x.json.exe", ".hidden.json", "", "a" * 200 + ".json", "x.json\x00"]
        for name in bad:
            self.assertEqual(self.s.save([{"name": name, "text": "x"}])[0], 400, repr(name))
        self.assertEqual(self.s.save([{"name": "a.json", "text": "x"}, {"name": "a.json", "text": "y"}])[0], 400, "doppelter Name")
        self.assertEqual(self.s.save([{"name": "a.json", "text": "x"}, {"name": "../b.json", "text": "y"}])[0], 400, "ein schlechter Name: nichts wird geschrieben")
        self.assertFalse((self.s.root / "x.json").exists() or (self.s.root / "abs.json").exists())
        self.assertTrue(self.s.empty_target(), "nichts geschrieben")

    def test_formular_in_the_target_folder_is_protected(self):
        """Zielordner = Ordner des Formulars (Standard): der Name des Formulars bleibt gesperrt."""
        s = Svc()
        s.srv.out_dir = s.root
        self.addCleanup(s.close)
        self.assertEqual(s.save([{"name": "formular.html", "text": "x"}])[0], 400)
        self.assertEqual(s.form.read_text(encoding="utf-8"), "<!doctype html><title>x</title>FORM")
        self.assertEqual(s.save([{"name": "d.antwort.json", "text": "{}"}])[0], 200)

    def test_malformed_body_is_400(self):
        h = {"Content-Type": "application/json", "Origin": "http://127.0.0.1:%d" % self.s.srv.port}
        for body in (b"{kaputt", b'{"files": "x"}', b'{"files": []}', b'{"files": [{"name": 1, "text": "x"}]}', b'{"files": [{"name": "a.json"}]}'):
            self.assertEqual(self.s.req("POST", "/%s/save" % self.s.srv.token, body, h)[0], 400, body)

    def test_self_terminates_without_requests(self):
        s = Svc(idle=0.4)
        self.addCleanup(s.close)
        threading.Thread(target=s.srv.watchdog, daemon=True).start()
        end = time.monotonic() + 5
        while s.thread.is_alive() and time.monotonic() < end:
            time.sleep(0.05)
        self.assertFalse(s.thread.is_alive(), "Dienst beendet sich nach Leerlauf")

    def test_ping_keeps_the_service_alive(self):
        s = Svc(idle=0.6)
        self.addCleanup(s.close)
        threading.Thread(target=s.srv.watchdog, daemon=True).start()
        for _ in range(6):
            time.sleep(0.3)
            self.assertEqual(s.req("GET", "/%s/ping" % s.srv.token)[0], 204)
        self.assertTrue(s.thread.is_alive())


@unittest.skipUnless(hu.HAVE_PLAYWRIGHT and hu.HAVE_EDGE, "Python-Playwright und Edge noetig")
class HeadlessEndeZuEnde(unittest.TestCase):
    """Formular ueber den Dienst im echten Edge (headless): Speichern ohne Ordnerdialog, beide Dateien liegen im Zielordner."""

    def test_save_without_dialog_writes_both_files(self):
        tmp = tempfile.TemporaryDirectory(prefix="serve_form_e2e_")
        self.addCleanup(tmp.cleanup)
        page_text, _digest, items = build_form.build(json.loads((HERE / "example_form.json").read_text(encoding="utf-8")), HERE)
        form = Path(tmp.name) / "formular.html"
        form.write_text(page_text, encoding="utf-8", newline="\n")
        out = Path(tmp.name) / "ziel"
        srv = serve_form.FormServer(form, out)
        threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        errors = []
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.add_init_script("window.__picker = 0; window.showDirectoryPicker = () => { window.__picker++; return Promise.reject(new DOMException('x', 'AbortError')); };")
            page.goto(srv.url)
            hu.ready(page)
            page.click("#item-%s input >> nth=0" % items[0]["id"])
            page.click("#top-panel .js-save")
            page.click("#dlg-buttons button.primary")
            page.wait_for_function("document.querySelector('#save-state').innerText.indexOf('Gespeichert in') >= 0", timeout=10000)
            self.assertEqual(page.evaluate("window.__picker"), 0, "kein Ordnerdialog")
            self.assertIn("ohne Dialog", page.evaluate("document.querySelector('#save-state').innerText"))
        self.assertEqual(len(list(out.iterdir())), 2)
        ans = json.loads(next(out.glob("*.antwort.json")).read_text(encoding="utf-8"))
        self.assertEqual(build_form.validate_answers(ans, items), [])
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
