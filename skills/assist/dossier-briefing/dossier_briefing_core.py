"""dossier_briefing_core.py — Recherche-Briefing-Scaffold-Generator (standalone, stdlib only).

Portiert aus BACH system/agents/persoenlicher-assistent/tools/dossier_generator.py v1.0.0.
Entfernt: DossierGenerator-Klasse mit Origin-DB (create_dossier, update_dossier,
  DOSSIERS_DIR, _get_db, _ensure_table, alle DB-CRUD-Methoden).
Behaelt: _create_markdown-Logik, verallgemeinert Person→Subjekt (Typen: person,
  organization, topic, event, unspecified).

Funktion: Erzeugt ein leeres, strukturiertes Markdown-Briefing-Geruest zu einem
  beliebigen Subjekt. Kein Netzwerkzugriff, kein Store, nur stdout oder Datei.
"""
from __future__ import annotations

import json
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Briefing-Typen und ihre Abschnitte
# ---------------------------------------------------------------------------

VALID_TYPES = ("person", "organization", "topic", "event", "unspecified")

# Typ → geordnete Liste von (Abschnittsname, Platzhalter-Beschreibung)
_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "person": [
        ("Basisdaten", "Geburtsdatum, Geburtsort, Nationalität, Beruf/Titel"),
        ("Vita / Hintergrund", "Ausbildung, Werdegang, wichtige Lebensstationen"),
        ("Werk & Beiträge", "Hauptwerke, Forschungsbeiträge, Veröffentlichungen, Auszeichnungen"),
        ("Verbindungen", "Institutionen, Kooperationen, Netzwerk"),
        ("Quellen", "Verwendete oder empfohlene Quellen"),
        ("Notizen", "Ergänzende Hinweise, offene Fragen"),
    ],
    "organization": [
        ("Profil", "Gründungsjahr, Hauptsitz, Branche, Rechtsform"),
        ("Geschichte", "Gründungsgeschichte, Meilensteine, Wandel"),
        ("Produkte / Dienste", "Hauptangebote, Marktstellung"),
        ("Schlüsselpersonen", "Gründer, Führungspersonen, Schlüsselrollen"),
        ("Verbindungen", "Tochtergesellschaften, Partner, Investoren"),
        ("Quellen", "Verwendete oder empfohlene Quellen"),
        ("Notizen", "Ergänzende Hinweise, offene Fragen"),
    ],
    "topic": [
        ("Überblick", "Kurzdefinition, Einordnung"),
        ("Hintergrund / Kontext", "Geschichte, Entwicklung, Vorläufer"),
        ("Aktuelle Entwicklung", "Stand der Forschung, aktuelle Diskussion"),
        ("Schlüsselquellen", "Wichtige Studien, Paper, Artikel"),
        ("Offene Fragen", "Ungeklärtes, Forschungslücken"),
        ("Notizen", "Ergänzende Hinweise"),
    ],
    "event": [
        ("Eckdaten", "Datum, Ort, Anlass, Veranstalter"),
        ("Beteiligte", "Hauptakteure, Teilnehmer, Organisatoren"),
        ("Verlauf / Hintergrund", "Vorgeschichte, Ablauf, Chronologie"),
        ("Bedeutung", "Auswirkungen, Reaktionen, Einordnung"),
        ("Quellen", "Berichte, Dokumente, Presseaussagen"),
        ("Notizen", "Ergänzende Hinweise, offene Fragen"),
    ],
    "unspecified": [
        ("Überblick", "Kurzbeschreibung des Subjekts"),
        ("Hintergrund", "Kontext, Geschichte, Einordnung"),
        ("Details", "Spezifische Informationen, Fakten, Daten"),
        ("Quellen", "Verwendete oder empfohlene Quellen"),
        ("Notizen", "Ergänzende Hinweise, offene Fragen"),
    ],
}

# Typ-Etiketten für die Kopfzeile
_TYPE_LABELS: dict[str, str] = {
    "person": "Person",
    "organization": "Organisation",
    "topic": "Thema",
    "event": "Ereignis",
    "unspecified": "Allgemein",
}


# ---------------------------------------------------------------------------
# Scaffold-Generierung
# ---------------------------------------------------------------------------

def create_briefing(
    subject: str,
    subject_type: str = "unspecified",
    author: str = "",
    language: str = "de",
) -> str:
    """Markdown-Briefing-Geruest erzeugen.

    Parameters
    ----------
    subject:      Name/Titel des Briefing-Subjekts
    subject_type: 'person', 'organization', 'topic', 'event' oder 'unspecified'
    author:       Optionaler Autorenname (leer = weggelassen)
    language:     'de' (Standard) oder 'en'

    Returns
    -------
    Markdown-String (noch leer, nur Struktur)
    """
    st = subject_type.lower().strip()
    if st not in VALID_TYPES:
        st = "unspecified"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    type_label = _TYPE_LABELS[st]
    sections = _SECTIONS[st]

    lines: list[str] = []

    # Frontmatter-Kommentar
    lines.append(f"<!-- Briefing-Geruest — bitte Abschnitte durch Recherche befuellen -->")
    lines.append("")

    # Titel
    lines.append(f"# Briefing: {subject}")
    lines.append("")

    # Metablock
    lines.append("| Feld | Wert |")
    lines.append("|---|---|")
    lines.append(f"| **Subjekt** | {subject} |")
    lines.append(f"| **Typ** | {type_label} |")
    lines.append(f"| **Erstellt** | {now} |")
    if author:
        lines.append(f"| **Erstellt von** | {author} |")
    lines.append(f"| **Status** | Geruest (leer) |")
    lines.append("")
    lines.append("> **Hinweis:** Dieses Dokument ist ein leeres Geruest.")
    lines.append("> Abschnitte muessen durch Recherche befuellt werden.")
    lines.append("> Nutze `research-agent` oder `web-reading` zum Befuellen.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Abschnitte
    for section_title, placeholder in sections:
        lines.append(f"## {section_title}")
        lines.append("")
        lines.append(f"<!-- {placeholder} -->")
        lines.append("")
        lines.append("_(noch leer)_")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI / main
# ---------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="dossier_briefing_core",
        description=(
            "Generiert ein strukturiertes Recherche-Briefing-Geruest als Markdown. "
            "Kein Netzwerkzugriff, kein Store — reine Scaffold-Erzeugung."
        ),
    )
    parser.add_argument(
        "subject",
        nargs="?",
        help="Name oder Titel des Briefing-Subjekts (z.B. 'Marie Curie')",
    )
    parser.add_argument(
        "--typ",
        default="unspecified",
        choices=list(VALID_TYPES),
        metavar="TYP",
        help=f"Briefing-Typ: {', '.join(VALID_TYPES)} (Standard: unspecified)",
    )
    parser.add_argument(
        "--autor",
        default="",
        metavar="NAME",
        help="Optionaler Autorenname fuer den Metablock",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        metavar="DATEI",
        help="Ausgabedatei (.md); ohne Angabe: stdout",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Metadaten als JSON ausgeben (kein Markdown)",
    )
    parser.add_argument(
        "--liste-typen",
        action="store_true",
        help="Alle verfuegbaren Briefing-Typen mit Abschnitten ausgeben",
    )

    args = parser.parse_args(argv)

    if args.liste_typen:
        for typ, label in _TYPE_LABELS.items():
            secs = [s for s, _ in _SECTIONS[typ]]
            print(f"{typ:15} ({label}): {', '.join(secs)}")
        return 0

    if not args.subject:
        parser.print_help()
        return 1

    if args.as_json:
        meta = {
            "subject": args.subject,
            "type": args.typ,
            "type_label": _TYPE_LABELS.get(args.typ, args.typ),
            "sections": [s for s, _ in _SECTIONS.get(args.typ, _SECTIONS["unspecified"])],
        }
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return 0

    markdown = create_briefing(
        subject=args.subject,
        subject_type=args.typ,
        author=args.autor,
    )

    if args.output:
        out_path = Path(args.output)
        try:
            out_path.write_text(markdown, encoding="utf-8")
            print(f"Briefing geschrieben: {out_path.resolve()}")
        except OSError as exc:
            print(f"Fehler beim Schreiben: {exc}", file=sys.stderr)
            return 1
    else:
        print(markdown)

    return 0


if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
