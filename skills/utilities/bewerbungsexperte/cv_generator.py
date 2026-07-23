#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cv_generator.py -- Standalone CV-Generator (portiert aus BACH, userneutral)
============================================================================

Generiert einen strukturierten ASCII-Lebenslauf aus einer SQLite-Datenbank
und optionalen Ordner-Scans. Die Datenbank kann eine beliebige SQLite-Datei
sein (BACH-kompatibel oder eigen), solange die Tabellen vorhanden sind.

Erwartete Tabellen (alle optional -- fehlende Tabellen fuehren zu leeren Sektionen):
  assistant_user_profile (key TEXT, value TEXT)
  contacts               (name, organization, position, phone, email,
                          is_active, category)

Usage:
  python cv_generator.py --db <pfad/zu/daten.db>
  python cv_generator.py --db <pfad> --output lebenslauf.txt
  python cv_generator.py --db <pfad> --career-path <ordner>
  python cv_generator.py --db <pfad> --education-path <ordner> --certs-path <ordner>
  python cv_generator.py --dry-run

Version: 1.1.0 (standalone, userneutral)
Provenance: portiert aus BACH system/agents/_experts/bewerbungsexperte/cv_generator.py v1.0.0
Änderungen vs. Original:
  - Kein hardcodierter Origin-DB-Pfad mehr; --db <pfad> ist Pflicht (oder --dry-run)
  - --scan-folders entfernt (erforderte user_data_folders-Tabelle in BACH)
  - Dry-Run-Modus hinzugefuegt (generiert Beispiel-CV ohne Datenbankzugriff)
  - Footer-Text neutralisiert
  - PYTHONDONTWRITEBYTECODE-Hinweis: mit PYTHONDONTWRITEBYTECODE=1 starten
"""

__version__ = "1.1.0"
__author__ = "BACH Team / ellmos (standalone port)"

import argparse
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# CV-Generator-Klasse
# ---------------------------------------------------------------------------

class CVGenerator:
    """Generiert ASCII-Lebenslauf aus einer SQLite-Datenbank und Ordnerstruktur."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.sections: Dict = {}

    def _get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ------------------------------------------------------------------
    # Daten sammeln
    # ------------------------------------------------------------------

    def collect_personal_data(self) -> Dict:
        """Persoenliche Daten aus assistant_user_profile."""
        conn = self._get_db()
        try:
            rows = conn.execute(
                "SELECT key, value FROM assistant_user_profile"
            ).fetchall()
            data = {r["key"]: r["value"] for r in rows}
            self.sections["personal"] = data
            return data
        except Exception:
            self.sections["personal"] = {}
            return {}
        finally:
            conn.close()

    def collect_contacts(self, category: str = "beruflich") -> List[Dict]:
        """Berufliche Kontakte als potenzielle Referenzen."""
        conn = self._get_db()
        try:
            rows = conn.execute("""
                SELECT name, organization, position, phone, email
                FROM contacts
                WHERE is_active = 1 AND category = ?
                ORDER BY name
            """, (category,)).fetchall()
            contacts = [dict(r) for r in rows]
            self.sections["references"] = contacts
            return contacts
        except Exception:
            self.sections["references"] = []
            return []
        finally:
            conn.close()

    def scan_career_folders(self, base_path: str) -> List[Dict]:
        """
        Scannt Arbeitgeber-Ordner und extrahiert Karriere-Stationen.

        Erwartet Ordnerstruktur:
          _Arbeitgeber/
            Firma_A/
              Vertrag.pdf
              Zeugnis.pdf
        """
        career = []
        base = Path(base_path)

        if not base.exists():
            self.sections["career"] = []
            return []

        for folder in sorted(base.iterdir()):
            if not folder.is_dir():
                continue
            if folder.name.startswith("."):
                continue

            entry = {
                "name": folder.name,
                "path": str(folder),
                "documents": [],
            }

            for f in folder.rglob("*"):
                if f.is_file() and not f.name.startswith(".") and f.name != "desktop.ini":
                    entry["documents"].append({
                        "name": f.name,
                        "ext": f.suffix.lower(),
                        "size": f.stat().st_size,
                    })

            years = re.findall(r"20\d{2}|19\d{2}", folder.name)
            if years:
                entry["years"] = years

            career.append(entry)

        self.sections["career"] = career
        return career

    def scan_education_folders(self, base_path: str) -> List[Dict]:
        """Scannt Zeugnisse/Abschluesse-Ordner."""
        education = []
        base = Path(base_path)

        if not base.exists():
            self.sections["education"] = []
            return []

        for folder in sorted(base.iterdir()):
            if not folder.is_dir():
                continue
            if folder.name.startswith("."):
                continue

            entry = {
                "name": folder.name,
                "documents": [
                    f.name for f in folder.rglob("*")
                    if f.is_file() and f.suffix.lower() in (".pdf", ".docx", ".jpg")
                    and f.name != "desktop.ini"
                ],
            }
            education.append(entry)

        self.sections["education"] = education
        return education

    def scan_certifications(self, base_path: str) -> List[str]:
        """Scannt Fortbildungen-Ordner."""
        certs = []
        base = Path(base_path)

        if not base.exists():
            self.sections["certifications"] = []
            return []

        for f in sorted(base.rglob("*")):
            if f.is_file() and f.suffix.lower() in (".pdf", ".docx"):
                if f.name != "desktop.ini":
                    name = f.stem.replace("_", " ").replace("-", " ")
                    name = re.sub(r"\d{8}_\d{4}", "", name).strip()
                    certs.append(name)

        self.sections["certifications"] = certs
        return certs

    # ------------------------------------------------------------------
    # CV generieren
    # ------------------------------------------------------------------

    def generate_ascii_cv(self) -> str:
        """Generiert ASCII-formatierten Lebenslauf."""
        lines = []
        width = 60

        lines.append("=" * width)
        lines.append("L E B E N S L A U F".center(width))
        lines.append("=" * width)
        lines.append("")

        # Persoenliche Daten
        personal = self.sections.get("personal", {})
        if personal:
            lines.append("PERSOENLICHE DATEN")
            lines.append("-" * width)
            field_map = {
                "name": "Name",
                "full_name": "Name",
                "email": "E-Mail",
                "phone": "Telefon",
                "address": "Adresse",
                "birthday": "Geburtsdatum",
                "birth_date": "Geburtsdatum",
                "nationality": "Staatsangehoerigkeit",
                "marital_status": "Familienstand",
            }
            for key, label in field_map.items():
                if key in personal and personal[key]:
                    lines.append(f"  {label:<25} {personal[key]}")
            lines.append("")

        # Berufserfahrung
        career = self.sections.get("career", [])
        if career:
            lines.append("BERUFSERFAHRUNG")
            lines.append("-" * width)
            for entry in career:
                name = entry["name"].lstrip("_")
                doc_count = len(entry.get("documents", []))
                years_str = ""
                if entry.get("years"):
                    years_str = f" ({', '.join(entry['years'])})"
                lines.append(f"  {name}{years_str}")
                if doc_count > 0:
                    lines.append(f"    Dokumente: {doc_count}")
                docs = entry.get("documents", [])
                important = [
                    d for d in docs
                    if any(kw in d["name"].lower()
                           for kw in ["zeugnis", "vertrag", "arbeits", "bescheinigung"])
                ]
                for d in important[:3]:
                    lines.append(f"    -> {d['name']}")
                lines.append("")

        # Ausbildung
        education = self.sections.get("education", [])
        if education:
            lines.append("AUSBILDUNG / ABSCHLUESSE")
            lines.append("-" * width)
            for entry in education:
                name = entry["name"].lstrip("0123456789 ")
                lines.append(f"  {name}")
                for doc in entry.get("documents", [])[:5]:
                    doc_clean = doc.replace(".pdf", "").replace(".docx", "")
                    lines.append(f"    - {doc_clean}")
            lines.append("")

        # Fortbildungen
        certs = self.sections.get("certifications", [])
        if certs:
            lines.append("FORTBILDUNGEN / ZERTIFIKATE")
            lines.append("-" * width)
            for cert in certs[:15]:
                lines.append(f"  - {cert}")
            if len(certs) > 15:
                lines.append(f"  ... und {len(certs) - 15} weitere")
            lines.append("")

        # Referenzen
        refs = self.sections.get("references", [])
        if refs:
            lines.append("REFERENZEN")
            lines.append("-" * width)
            for ref in refs[:5]:
                company = f" ({ref.get('organization', '')})" if ref.get("organization") else ""
                pos = f", {ref['position']}" if ref.get("position") else ""
                contact = ref.get("email") or ref.get("phone") or ""
                lines.append(f"  {ref['name']}{pos}{company}")
                if contact:
                    lines.append(f"    {contact}")
            lines.append("")

        lines.append("-" * width)
        lines.append(f"Stand: {datetime.now().strftime('%d.%m.%Y')}")
        lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dry-Run-Daten
# ---------------------------------------------------------------------------

def _dry_run_cv() -> str:
    """Gibt ein Beispiel-CV ohne Datenbankzugriff aus."""
    gen = CVGenerator(":memory:")
    gen.sections = {
        "personal": {
            "name": "Max Mustermann",
            "email": "max@example.com",
            "phone": "+49 123 456789",
            "address": "Musterstrasse 1, 12345 Musterstadt",
        },
        "career": [
            {
                "name": "Musterfirma GmbH (2020-2024)",
                "years": ["2020", "2024"],
                "documents": [
                    {"name": "Arbeitszeugnis.pdf", "ext": ".pdf", "size": 120000},
                ],
            }
        ],
        "education": [
            {"name": "Universitaet Musterstadt", "documents": ["Bachelor_Zeugnis.pdf"]},
        ],
        "certifications": ["Projektmanagement-Zertifikat", "Python Grundlagen"],
        "references": [],
    }
    return gen.generate_ascii_cv()


# ---------------------------------------------------------------------------
# Report-Ausgabe
# ---------------------------------------------------------------------------

def format_cv_report(cv_text: str, sections: Dict) -> str:
    """Gibt CV mit Metadaten-Report aus."""
    lines = [
        "[CV-GENERATOR] Lebenslauf generiert",
        f"  Sektionen:    {len(sections)}",
    ]
    for name, data in sections.items():
        if isinstance(data, list):
            lines.append(f"    {name}: {len(data)} Eintraege")
        elif isinstance(data, dict):
            lines.append(f"    {name}: {len(data)} Felder")
    lines.append("")
    lines.append(cv_text)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="CV Generator -- generiert ASCII-Lebenslauf aus SQLite-DB und Ordnerstruktur"
    )
    parser.add_argument("--db", help="Pfad zur SQLite-Datenbank (z.B. Origin-DB oder eigene DB)")
    parser.add_argument("--output", "-o", help="Ausgabedatei (ansonsten stdout)")
    parser.add_argument("--career-path", help="Pfad zum Arbeitgeber-Ordner")
    parser.add_argument("--education-path", help="Pfad zum Abschluesse-Ordner")
    parser.add_argument("--certs-path", help="Pfad zum Fortbildungen-Ordner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Beispiel-CV generieren ohne Datenbankzugriff")
    args = parser.parse_args()

    if args.dry_run:
        cv_text = _dry_run_cv()
        print("[DRY-RUN] Beispiel-CV:\n")
        print(cv_text)
        sys.exit(0)

    if not args.db:
        parser.error("--db <pfad> ist erforderlich (oder --dry-run fuer Beispiel-Ausgabe)")

    db_path = args.db
    if not Path(db_path).exists():
        print(f"[FEHLER] Datenbank nicht gefunden: {db_path}", file=sys.stderr)
        sys.exit(1)

    gen = CVGenerator(db_path)
    gen.collect_personal_data()
    gen.collect_contacts("beruflich")

    if args.career_path:
        gen.scan_career_folders(args.career_path)

    if args.education_path:
        gen.scan_education_folders(args.education_path)

    if args.certs_path:
        gen.scan_certifications(args.certs_path)

    cv_text = gen.generate_ascii_cv()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cv_text)
        print(f"[OK] Lebenslauf gespeichert: {args.output}")
        print(f"     {len(cv_text)} Zeichen, {cv_text.count(chr(10))} Zeilen")
    else:
        print(format_cv_report(cv_text, gen.sections))
