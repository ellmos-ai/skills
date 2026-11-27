"""Lokaler Speicherdienst + Oeffner fuer das Entscheidungsformular (Regel 9, Stufe 1: Speichern ohne Dialog).

Eine file://-Seite darf ohne Dialog nichts auf die Platte schreiben. Dieser Dienst liefert das Formular deshalb ueber
http://127.0.0.1:<Port>/<Token>/ aus und schreibt die Antwort per POST selbst (atomar: alle Dateien erst als tmp, dann os.replace).
Nur Python-Standardbibliothek. Aufruf:

    python serve_form.py <formular.html> [--out-dir ZIELORDNER] [--no-open]

Standard-Zielordner ist der Ordner des Formulars. Der Dienst oeffnet das Formular im normalen Browser (Windows: Edge mit dem
Nutzerprofil), laeuft im Vordergrund und beendet sich selbst, wenn keine Anfrage mehr kommt (das Formular meldet sich im
Minutentakt, solange der Tab offen ist) oder nach der Hoechstlaufzeit. Kein Dienst da? Das Formular faellt auf Download-Links,
Text und erst zuletzt auf den Ordnerdialog zurueck.

Sicherheit: nur 127.0.0.1; Zufalls-Token im Pfad (falsches Token = 403); Host- und Origin-Pruefung (DNS-Rebinding, fremde Seiten);
JSON-Pflicht beim POST; Groessenlimit (413); nur Dateinamen aus Buchstaben/Ziffern/._- mit Endung .json oder .html, nie ein Pfad,
nie das Formular selbst; geschrieben wird ausschliesslich in den einen Zielordner; Inhalte werden nie ausgefuehrt."""
import argparse
import http.server
import importlib.util
import json
import os
import re
import secrets
import sys
import threading
import time
from pathlib import Path


def _load_server_cfg():
    cfg_script = Path(__file__).resolve().parents[1] / "draw_config.py"
    spec = importlib.util.spec_from_file_location("draw_config", cfg_script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_draw_config()["config"]["server"]


_SRV_CFG = _load_server_cfg()
SERVER_HOST = str(_SRV_CFG["host"])
MAX_BYTES = int(_SRV_CFG["max_bytes"])  # Formular mit Bildern (8 MB) plus beantwortete Kopie bleiben weit darunter
IDLE_SECONDS = int(_SRV_CFG["idle_seconds"])  # ohne Anfrage (Formular pingt alle 60 s) beendet sich der Dienst
MAX_LIFETIME = int(_SRV_CFG["max_lifetime_seconds"])
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,150}\.(json|html)$")
MAX_FILES = int(_SRV_CFG["max_files"])


class FormServer(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, form_path, out_dir, token=None, max_bytes=MAX_BYTES, idle=IDLE_SECONDS, max_life=MAX_LIFETIME):
        super().__init__((SERVER_HOST, 0), Handler)
        self.form_path = Path(form_path).resolve()
        self.out_dir = Path(out_dir).resolve()
        self.token = token or secrets.token_urlsafe(24)
        self.max_bytes, self.idle, self.max_life = max_bytes, idle, max_life
        self.last_seen = time.monotonic()
        self.started = self.last_seen
        self.saved = 0

    @property
    def port(self):
        return self.server_address[1]

    @property
    def url(self):
        return "http://127.0.0.1:%d/%s/" % (self.port, self.token)

    def watchdog(self):
        while True:
            time.sleep(min(1.0, max(self.idle / 4, 0.05)))
            now = time.monotonic()
            if now - self.last_seen > self.idle or now - self.started > self.max_life:
                self.shutdown()
                return

    def write_files(self, files):
        """Alle Dateien erst als tmp schreiben, dann ersetzen: scheitert ein tmp, bleibt der Zielordner unveraendert."""
        self.out_dir.mkdir(parents=True, exist_ok=True)
        staged = []
        try:
            for name, data in files:
                tmp = self.out_dir / (".%s.%s.tmp" % (name, secrets.token_hex(4)))
                tmp.write_bytes(data)
                staged.append((tmp, self.out_dir / name))
            for tmp, dst in staged:
                os.replace(tmp, dst)
        except BaseException:
            for tmp, _ in staged:
                tmp.unlink(missing_ok=True)
            raise


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "FormServe/1"

    def log_message(self, fmt, *args):  # kein Token in Logs
        pass

    def _send(self, code, body=b"", ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _err(self, code, msg):
        self._send(code, json.dumps({"ok": False, "error": msg}).encode())

    def _route(self):
        """Prueft Host und Token. Gibt den Rest des Pfads zurueck oder None (Antwort ist dann schon gesendet)."""
        s = self.server
        if self.headers.get("Host") not in ("127.0.0.1:%d" % s.port, "localhost:%d" % s.port):
            self._err(403, "host")
            return None
        parts = self.path.split("?", 1)[0].split("/", 2)  # ['', token, rest]
        if len(parts) < 3 or not secrets.compare_digest(parts[1].encode(), s.token.encode()):
            self._err(403, "token")
            return None
        s.last_seen = time.monotonic()
        return parts[2]

    def do_GET(self):
        rest = self._route()
        if rest is None:
            return
        if rest in ("", "index.html"):
            try:
                body = self.server.form_path.read_bytes()
            except OSError:
                return self._err(404, "formular")
            return self._send(200, body, "text/html; charset=utf-8")
        if rest == "ping":
            return self._send(204)
        self._err(404, "unbekannt")

    def do_POST(self):
        rest = self._route()
        if rest is None:
            return
        s = self.server
        if rest != "save":
            return self._err(404, "unbekannt")
        origins = ("http://127.0.0.1:%d" % s.port, "http://localhost:%d" % s.port)
        if self.headers.get("Origin") not in origins:
            return self._err(403, "origin")
        if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
            return self._err(415, "content-type")
        try:
            n = int(self.headers.get("Content-Length", ""))
        except ValueError:
            return self._err(411, "content-length")
        if n < 0 or n > s.max_bytes:
            self.close_connection = True
            self.rfile.read(min(max(n, 0), 1 << 20))  # kleinen Rest abnehmen, sonst setzt der Client die Verbindung zurueck, bevor er das 413 liest
            return self._err(413, "zu gross")
        try:
            req = json.loads(self.rfile.read(n).decode("utf-8"))
            items = req["files"]
            if not isinstance(items, list) or not 1 <= len(items) <= MAX_FILES:
                raise ValueError("files")
            files, seen = [], set()
            for f in items:
                name, text = f["name"], f["text"]
                if not (isinstance(name, str) and isinstance(text, str) and NAME_RE.match(name)) or name in seen:
                    raise ValueError("name")
                if (s.out_dir / name).resolve() == s.form_path:  # nie das Formular selbst ueberschreiben
                    raise ValueError("name")
                seen.add(name)
                files.append((name, text.encode("utf-8")))
        except (ValueError, KeyError, TypeError, UnicodeDecodeError):
            return self._err(400, "ungueltige Anfrage")
        try:
            s.write_files(files)
        except OSError as e:
            return self._err(500, "schreiben: %s" % type(e).__name__)
        s.saved += 1
        self._send(200, json.dumps({"ok": True, "dir": str(s.out_dir), "written": [f[0] for f in files]}).encode())


def open_in_browser(url):
    """Windows: Edge im normalen Nutzerprofil (Protokoll-Handler), sonst Standardbrowser. Nie ein Temp-Profil."""
    if sys.platform == "win32":
        try:
            os.startfile("microsoft-edge:" + url)
            return
        except OSError:
            pass
    import webbrowser
    webbrowser.open(url)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("form", help="gebautes Formular (.html)")
    ap.add_argument("--out-dir", help="Zielordner der Antwort (Standard: Ordner des Formulars)")
    ap.add_argument("--no-open", action="store_true", help="Browser nicht starten, nur die URL ausgeben")
    ap.add_argument("--idle", type=int, default=IDLE_SECONDS, help="Sekunden ohne Anfrage bis zur Selbstbeendigung")
    a = ap.parse_args(argv)
    form = Path(a.form)
    if not form.is_file():
        sys.exit("Formular nicht gefunden: %s" % form)
    srv = FormServer(form, a.out_dir or form.resolve().parent, idle=a.idle)
    threading.Thread(target=srv.watchdog, daemon=True).start()
    print("Formular: %s\nZielordner: %s\nBeendet sich nach %d s ohne Anfrage." % (srv.url, srv.out_dir, srv.idle), flush=True)
    if not a.no_open:
        open_in_browser(srv.url)
    try:
        srv.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    print("Dienst beendet (%d Speicherung(en))." % srv.saved)


if __name__ == "__main__":
    main()
