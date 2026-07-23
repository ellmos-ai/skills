#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 BACH Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Press Compiler - LaTeX-basierte Dokumentenerstellung
=====================================================
Kompiliert Pressemitteilungen und Positionspapiere via pdflatex/xelatex.
Portiert aus BACH press-Experte; user-neutral (kein bach.db, kein bach_paths).

Voraussetzungen: MiKTeX (Windows) oder TeX Live (Mac/Linux)
  LaTeX-Pakete: geometry, fancyhdr, graphicx, hyperref, babel, xcolor, parskip
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

PRESS_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = PRESS_DIR / "templates"
CONFIG_FILE = PRESS_DIR / "config.json"


def load_config() -> dict:
    """Laedt Press-Konfiguration aus config.json (Fallback: leere Defaults)."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {
        "author": "",
        "organization": "",
        "contact_email": "",
        "contact_phone": "",
        "logo_path": "",
        "default_language": "ngerman",
        "output_dir": "",
        "latex_compiler": "pdflatex",
        "fallback_compiler": "xelatex",
    }


def compile_document(doc_type: str, title: str, body: str,
                     output_path: str = None, config: dict = None) -> str:
    """Kompiliert ein LaTeX-Dokument zu PDF.

    Args:
        doc_type: 'pressemitteilung' oder 'positionspapier'
        title: Dokumententitel
        body: Haupttext (kann LaTeX-Markup enthalten)
        output_path: Optionaler Ausgabepfad fuer die PDF; wenn leer,
                     wird output_dir aus config.json (relativ zu cwd) genutzt.
        config: Optionale Konfiguration (sonst aus config.json geladen)

    Returns:
        Pfad zur generierten PDF-Datei

    Raises:
        FileNotFoundError: Template nicht gefunden
        RuntimeError: LaTeX-Kompilierung fehlgeschlagen
    """
    if config is None:
        config = load_config()

    template_file = TEMPLATES_DIR / f"{doc_type}.tex"
    if not template_file.exists():
        raise FileNotFoundError(f"Template nicht gefunden: {template_file}")

    template = template_file.read_text(encoding='utf-8')

    # Variablen ersetzen
    today = datetime.now()
    replacements = {
        '{{TITLE}}': title,
        '{{BODY}}': _escape_latex(body),
        '{{AUTHOR}}': config.get('author', ''),
        '{{ORGANIZATION}}': config.get('organization', ''),
        '{{DATE}}': today.strftime('%d. %B %Y'),
        '{{DATE_ISO}}': today.strftime('%Y-%m-%d'),
        '{{CONTACT_EMAIL}}': config.get('contact_email', ''),
        '{{CONTACT_PHONE}}': config.get('contact_phone', ''),
        '{{YEAR}}': str(today.year),
    }

    # Logo-Pfad (optional)
    logo_path = config.get('logo_path', '')
    if logo_path and Path(logo_path).exists():
        replacements['{{LOGO_PATH}}'] = logo_path.replace('\\', '/')
        replacements['{{HAS_LOGO}}'] = 'true'
    else:
        replacements['{{HAS_LOGO}}'] = 'false'
        replacements['{{LOGO_PATH}}'] = ''

    tex_content = template
    for key, value in replacements.items():
        tex_content = tex_content.replace(key, value)

    # Temporaeres Verzeichnis fuer Kompilierung
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = Path(tmpdir) / "document.tex"
        tex_file.write_text(tex_content, encoding='utf-8')

        # Kompilieren (2x fuer Referenzen)
        compiler = config.get('latex_compiler', 'pdflatex')
        fallback = config.get('fallback_compiler', 'xelatex')

        success = _run_latex(compiler, tex_file, tmpdir)
        if not success:
            success = _run_latex(fallback, tex_file, tmpdir)

        if not success:
            raise RuntimeError(
                f"LaTeX-Kompilierung fehlgeschlagen ({compiler}/{fallback}). "
                f"Ist MiKTeX/TeX Live installiert und '{compiler}' im PATH?"
            )

        pdf_file = Path(tmpdir) / "document.pdf"
        if not pdf_file.exists():
            raise RuntimeError("PDF wurde nicht generiert.")

        # Ausgabepfad bestimmen (user-neutral: relativ zu cwd oder konfigurierbar)
        if not output_path:
            output_dir_cfg = config.get('output_dir', '')
            if output_dir_cfg:
                output_dir = Path(output_dir_cfg)
            else:
                output_dir = Path.cwd() / "press_output"
            output_dir.mkdir(parents=True, exist_ok=True)
            safe_title = "".join(
                c if c.isalnum() or c in '-_ ' else '' for c in title
            )[:50]
            output_path = str(
                output_dir / f"{doc_type}_{today.strftime('%Y%m%d')}_{safe_title}.pdf"
            )

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(pdf_file), output_path)

    return output_path


def _run_latex(compiler: str, tex_file: Path, workdir: str) -> bool:
    """Fuehrt LaTeX-Compiler zweimal aus (fuer Querverweise)."""
    if not shutil.which(compiler):
        return False

    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    creation_flags = 0x08000000 if sys.platform == 'win32' else 0

    for _ in range(2):
        try:
            result = subprocess.run(
                [compiler, '-interaction=nonstopmode', '-halt-on-error',
                 str(tex_file)],
                capture_output=True, timeout=60,
                cwd=workdir, env=env,
                creationflags=creation_flags,
            )
            if result.returncode != 0:
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    return True


def _escape_latex(text: str) -> str:
    """Escaped Sonderzeichen fuer LaTeX; erhaelt vorhandenes LaTeX-Markup."""
    if not text:
        return ""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
    }
    for char, escaped in replacements.items():
        text = text.replace(f'\\{char}', f'__ESCAPED_{char}__')
        text = text.replace(char, escaped)
        text = text.replace(f'__ESCAPED_{char}__', f'\\{char}')
    return text


def list_templates() -> list:
    """Gibt verfuegbare Templates zurueck."""
    templates = []
    if TEMPLATES_DIR.exists():
        for f in sorted(TEMPLATES_DIR.glob("*.tex")):
            templates.append({
                "name": f.stem,
                "path": str(f),
                "size": f.stat().st_size,
            })
    return templates


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Press Compiler — LaTeX-PDF aus Template"
    )
    parser.add_argument("--type", default="pressemitteilung",
                        choices=["pressemitteilung", "positionspapier"],
                        help="Dokumenttyp")
    parser.add_argument("--title", default="Testtitel", help="Dokumenttitel")
    parser.add_argument("--body", default="Testinhalt.", help="Haupttext")
    parser.add_argument("--output", default=None, help="Ausgabepfad (.pdf)")
    parser.add_argument("--list-templates", action="store_true",
                        help="Verfuegbare Templates anzeigen")
    args = parser.parse_args()

    if args.list_templates:
        for t in list_templates():
            print(f"  {t['name']}  ({t['size']} Bytes)  {t['path']}")
        sys.exit(0)

    try:
        out = compile_document(args.type, args.title, args.body, args.output)
        print(f"PDF erstellt: {out}")
    except Exception as e:
        print(f"Fehler: {e}", file=sys.stderr)
        sys.exit(1)
