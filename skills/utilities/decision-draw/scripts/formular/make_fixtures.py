"""Erzeugt die Testdaten testdata/{teil,voll}_{antwort.json,BEANTWORTET.html} reproduzierbar im HEADLESS-Edge (Python-Playwright, eigenes Temp-Profil,
kein sichtbares Fenster, Download-Fallback). Aufruf: python make_fixtures.py <FORMULAR.html> <zielordner>
Es sind TESTDATEN: keine Nutzerentscheidung (siehe testdata/UNGUELTIG-TESTDATEN.txt)."""
import sys
import tempfile
from pathlib import Path

import headless_util as hu


def run(page, steps):
    for kind, *a in steps:
        if kind == "click":
            page.click(a[0])
        elif kind == "fill":
            page.fill(a[0], a[1])
    page.click("#top-panel .js-save")
    page.click("#dlg-buttons button.primary")


SCENARIOS = {
    "teil": [("click", '#item-V1 input[value="B"]'), ("click", '#item-V3 input[value="A"]'), ("click", '#item-O1 input[value="A"]'),
             ("click", '#item-T2\\.2 input[value="C"]'), ("fill", "#item-V1 textarea", "lieber nur 3.0, bitte erst prüfen"),
             ("click", 'input[name=agpl][value="bestätigen"]')],
    "voll": [("click", "#top-panel [data-bulk=all]"), ("click", "#dlg-buttons button.primary"), ("click", 'input[name=agpl][value="bestätigen"]'),
             ("fill", "#item-V5 textarea", "ok, aber ich schaue den Text noch einmal an")],
}


def main(html, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    url = Path(html).resolve().as_uri()
    for name, steps in SCENARIOS.items():
        tmp = Path(tempfile.mkdtemp(prefix="formular_dl_"))
        with hu.headless_context() as ctx:
            got = []
            ctx.on("download", lambda d: got.append(d))
            page = ctx.new_page()
            page.add_init_script("window.showDirectoryPicker = undefined;")  # Download-Fallback erzwingen
            page.goto(url)
            hu.ready(page)
            run(page, steps)
            page.wait_for_timeout(2500)
            for d in got:
                d.save_as(str(tmp / d.suggested_filename))
        files = {p.name: p for p in tmp.iterdir()}
        assert len(files) == 2, (name, sorted(files))
        (out / f"{name}_antwort.json").write_bytes(files["ENTSCHEIDUNGEN_2026-11-07.antwort.json"].read_bytes())
        (out / f"{name}_BEANTWORTET.html").write_bytes(files["ENTSCHEIDUNGEN_2026-11-07_BEANTWORTET.html"].read_bytes())
        print("geschrieben:", name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
