# -*- coding: utf-8 -*-
"""Sprach-Gate: SKILL.md muss deutsch sein, SKILL.en.md englisch.

WARUM ES DIESES GATE GIBT
-------------------------
Die Sprache eines Skills steht an zwei Stellen -- `SKILL.md` (laut
docs/CONVENTIONS.md Deutsch, kein Suffix) und `SKILL.en.md` (Englisch).
Bis zum 2026-08-23 verglich sie nichts. Deshalb konnte der i18n-Lauf
`6a2d333` am 2026-07-30 in 55 Skills die deutsche Primaerfassung durch die
englische ersetzen, ohne dass es auffiel -- entdeckt wurde es erst, als ein
Deploy die Fassungen nebeneinanderlegte. Das ist Muster P10 aus
`.AI/PATTERNS.md`: Zwei Schalter fuer dieselbe Sache brauchen einen
Vergleich, sonst ist Redundanz kein Schutz, sondern eine zweite Stelle, an
der die Wahrheit stehen kann.

BEWUSSTE AUSNAHMEN
------------------
Nicht jeder englische Skill ist ein Fehler. Manche sind bewusst englisch
angelegt (publizierbare, nutzerneutrale Kerne wie `build-your-users-mind`),
andere sind Fremdmaterial. Solche Faelle gehoeren mit Begruendung in
`testing/language_baseline.json` -- eine Ausnahme ohne Grund ist ein Fehler,
kein Zustand (dieselbe Regel wie bei den Policy-Adoptionen in `.SYNC`).

Aufruf:  PYTHONIOENCODING=utf-8 python testing/language_gate.py
Exit 0 = keine unerklaerten Abweichungen.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASELINE = REPO / "testing" / "language_baseline.json"

DE = re.compile(r"\b(und|oder|nicht|werden|wird|einen|eine|der|die|das|für|mit|auch|"
                r"beim|nach|vor|dann|wenn|sind|kann|muss|soll)\b", re.I)
EN = re.compile(r"\b(and|the|with|for|will|shall|requirements|description|purpose|"
                r"overview|before|throughout|collect|when|then|each|must|should)\b", re.I)

# Unterhalb dieser Trefferzahl ist die Messung nicht aussagekraeftig
# (sehr kurze Skills, reine Verweisdateien).
MINDEST_TREFFER = 15

# Sprachunterordner: dort ist SKILL.md die Fassung DIESER Sprache, nicht die
# deutsche Primaerfassung -- `EN/SKILL.md` SOLL englisch sein.
SPRACHORDNER = {"en", "es", "fr", "ja", "ru", "zh", "hi", "ar", "bn", "pt", "de"}

# Archiv wird nicht geprueft: dort liegen bewusst eingefrorene Altstaende,
# die niemand mehr pflegt.
IGNORIERTE_TEILE = {"_archive", "_reference", "third-party"}


def ueberspringen(md: Path) -> bool:
    teile = {t.lower() for t in md.relative_to(REPO).parts}
    if teile & IGNORIERTE_TEILE:
        return True
    return md.parent.name.lower() in SPRACHORDNER


def split_frontmatter(text: str) -> "tuple[str, str]":
    if not text.startswith("---"):
        return "", text
    teile = text.split("---", 2)
    return ("---" + teile[1] + "---", teile[2]) if len(teile) >= 3 else ("", text)


def sprache(text: str) -> "tuple[str, int, int]":
    _, body = split_frontmatter(text)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    de, en = len(DE.findall(body)), len(EN.findall(body))
    if de + en < MINDEST_TREFFER:
        return "zu-kurz", de, en
    if de > en * 1.5:
        return "de", de, en
    if en > de * 1.5:
        return "en", de, en
    return "gemischt", de, en


def main() -> int:
    baseline = {}
    if BASELINE.is_file():
        roh = json.loads(BASELINE.read_text(encoding="utf-8"))
        baseline = {e["skill"]: e for e in roh.get("ausnahmen", [])}

    befunde, geprueft, ausgenommen = [], 0, 0
    for md in sorted((REPO / "skills").rglob("SKILL.md")):
        if ueberspringen(md):
            continue
        name = md.parent.name
        text = md.read_text(encoding="utf-8", errors="replace")
        spr, de, en = sprache(text)
        if spr == "zu-kurz":
            continue
        geprueft += 1

        if spr != "de":
            if name in baseline:
                ausgenommen += 1
                continue
            befunde.append((name, "SKILL.md", spr, de, en,
                            str(md.relative_to(REPO)).replace("\\", "/")))

        en_datei = md.parent / "SKILL.en.md"
        if en_datei.is_file():
            spr_en, de_en, en_en = sprache(en_datei.read_text(encoding="utf-8", errors="replace"))
            # Baseline gilt fuer BEIDE Richtungen -- ein Skill kann in der einen
            # Datei begruendet abweichen und in der anderen nicht.
            if spr_en == "de" and name not in baseline:
                befunde.append((name, "SKILL.en.md", spr_en, de_en, en_en,
                                str(en_datei.relative_to(REPO)).replace("\\", "/")))

    print(f"Sprach-Gate: {geprueft} Skills geprueft, "
          f"{ausgenommen} laut Baseline ausgenommen.")

    if not befunde:
        print("Language gate passed: SKILL.md ist deutsch, SKILL.en.md ist englisch.")
        return 0

    print(f"\nFEHLER: {len(befunde)} unerklaerte Abweichung(en)\n")
    for name, datei, spr, de, en, pfad in befunde:
        soll = "deutsch" if datei == "SKILL.md" else "englisch"
        print(f"  {name:32s} {datei:14s} wirkt {spr:9s} "
              f"(de={de:3d} en={en:3d}), soll {soll} sein")
        print(f"  {'':32s} {pfad}")
    print("\nEntweder die Sprache korrigieren oder -- wenn die Abweichung gewollt ist --")
    print(f"den Skill mit Begruendung in {BASELINE.name} eintragen.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
