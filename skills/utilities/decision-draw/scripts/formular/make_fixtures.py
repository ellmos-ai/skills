"""Erzeugt die Testdaten testdata/{teil,voll}_{antwort.json,BEANTWORTET.html} reproduzierbar im HEADLESS-Edge
(Python-Playwright, eigenes Temp-Profil, kein sichtbares Fenster, Regel-9-Sicherungsbereich).

Aufruf: python make_fixtures.py <FORMULAR.html> <zielordner>
Es sind TESTDATEN: keine Nutzerentscheidung (siehe testdata/UNGUELTIG-TESTDATEN.txt).
Funktioniert mit dem Regel-9-Sicherungsbereich: Nach dem Bestätigen im Speicherdialog wird auf die Download-Links
in #save-links a gewartet und deren Inhalte (Antwortdatei und beantwortete HTML-Kopie) werden ausgelesen.
"""
import sys
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
    page.wait_for_selector("#save-links a")


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
        with hu.headless_context() as ctx:
            page = ctx.new_page()
            page.add_init_script("window.showDirectoryPicker = undefined;")  # Download-Fallback erzwingen
            page.goto(url)
            hu.ready(page)
            run(page, steps)
            blobs = page.evaluate("""async () => {
                const links = Array.from(document.querySelectorAll('#save-links a'));
                const res = [];
                for (const a of links) {
                    const resp = await fetch(a.href);
                    const text = await resp.text();
                    res.push({name: a.download, text: text});
                }
                return res;
            }""")
            assert len(blobs) >= 2, (name, blobs)
            ans = next(b for b in blobs if b["name"].endswith(".antwort.json"))
            copy = next(b for b in blobs if b["name"].endswith("_BEANTWORTET.html"))
            (out / f"{name}_antwort.json").write_text(ans["text"], encoding="utf-8")
            (out / f"{name}_BEANTWORTET.html").write_text(copy["text"], encoding="utf-8")
            print("geschrieben:", name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
