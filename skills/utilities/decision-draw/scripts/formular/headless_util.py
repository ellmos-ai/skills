"""Gemeinsame Hilfen fuer HEADLESS-Browsertests des Formulars (Python-Playwright mit dem Edge-Kanal, eigenes Temp-Profil, kein sichtbares Fenster).
Nie die Playwright-MCP-Tools verwenden: dort oeffnet sich ein sichtbarer Browser auf dem Desktop des Nutzers."""
import contextlib
import shutil
import tempfile
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    HAVE_PLAYWRIGHT = True
except Exception:  # pragma: no cover
    HAVE_PLAYWRIGHT = False

EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
HAVE_EDGE = EDGE.is_file()


@contextlib.contextmanager
def headless_context(download_dir=None):
    """Liefert (context, profildir). headless=True ist hart verdrahtet."""
    prof = tempfile.mkdtemp(prefix="formular_edge_profile_")
    try:
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(prof, channel="msedge", headless=True, accept_downloads=True, viewport={"width": 1100, "height": 900},
                                                       args=["--disable-gpu", "--no-first-run"])
            try:
                yield ctx
            finally:
                ctx.close()
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def ready(page):
    page.wait_for_function("document.body.classList.contains('ready')", timeout=15000)
