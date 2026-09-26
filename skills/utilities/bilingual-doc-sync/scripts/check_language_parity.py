#!/usr/bin/env python3
"""check_language_parity.py -- Schritt 0 von bilingual-doc-sync (T-20260926-967984806).

Findet Markdown-/HTML-Links/URLs, die nur in einer Teilmenge der uebergebenen
Sprachfassungen eines Dokuments vorkommen. Links sind ein robuster,
sprachunabhaengiger Indikator: anders als Fliesstext bleiben sie ueber eine
Uebersetzung hinweg identisch, ein fehlender Link ist also entweder (a) noch
nicht propagierter neuer Inhalt einer Fassung, oder (b) ein verlorener Inhalt
(z.B. durch einen History-Rewrite) -- in beiden Faellen ein Fall fuer einen
Menschen/Agenten, nicht fuer eine stille Loeschung.

Belegfall: ellmos-ai/skills PR #1 fuegte "[Skills宝](https://skilery.com)"
nur in README.md ein; ein spaeterer History-Rewrite verlor die Zeile in allen
Sprachfassungen, weil kein Sync-Schritt geprueft hat, ob Inhalt existiert, der
in keiner anderen Fassung steht.

## lang-only-Markierung

Nicht jeder einsprachige Inhalt ist ein Fehler -- manches gilt bewusst nur fuer
eine Zielgruppe (Nutzerkorrektur T-20260926-967984806: derselbe Skills-宝-Link
ist fuer DE/ES/JA/RU-Leser:innen irrelevant; ihn in alle sechs Fassungen zu
uebersetzen war selbst der Fehler). Ein Block wird mit
`<!-- lang-only: <code>[,<code>...] --> ... <!-- /lang-only -->` markiert
(HTML-Kommentar, in jedem Markdown-Renderer unsichtbar). Links darin werden nur
gegen Dateien geprueft, deren Sprachcode in der Markierung genannt ist -- fehlen
sie in einer Fassung AUSSERHALB der Markierung, ist das kein Konflikt.

Sprachcode einer Datei wird aus dem Dateinamen abgeleitet: `README.md` -> `en`,
`README_de.md`/`README-de.md` -> `de`, usw. (Gross-/Kleinschreibung egal).
Regionscodes werden erhalten und auf Bindestrich normalisiert:
`README_zh-CN.md` und `README_zh_CN.md` liefern beide `zh-cn`.

Ein lang-only-Code, der zu KEINER der uebergebenen Dateien passt (z.B. Tippfehler
`cn` statt `zh`), wird fail-closed als Befund gemeldet -- der Link wird NICHT
still freigestellt, sondern die Markierung selbst gilt als verdaechtig.

## Link-Formate

Sowohl Markdown-Links (`[text](url)`) als auch HTML-Links/Bilder
(`<a href="url">`, `<img src="url">`) werden erfasst -- README-Dateien mischen
beide Formate (z.B. Badges/Bilder als `<img>`, mit `<a>` umschlossen).

## Badge-Rauschen

`shields.io`-Badge-URLs kodieren die Beschriftung oft direkt in der URL (z.B.
".../badge/Public...svg" vs. ".../badge/%C3%96ffentliche...svg" fuer dieselbe
Badge in zwei Sprachen) -- das ist erwartete Uebersetzungsvarianz, kein
Contentverlust, und wird deshalb standardmaessig herausgefiltert
(`--include-badges` schaltet das ab).

Nutzung:
    python check_language_parity.py README.md README_de.md README_zh.md ...
    python check_language_parity.py --include-badges README.md README_de.md

Exit 0: jeder gefundene Link kommt in allen dafuer relevanten Dateien vor.
Exit 1: mindestens ein Link kommt nicht in allen dafuer relevanten Dateien vor.
Exit 2: Aufrufproblem (zu wenige Dateien, Datei nicht lesbar, nicht UTF-8-lesbar).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_LINK_MD = re.compile(r"\]\((https?://[^\s)]+)\)")
_LINK_HTML = re.compile(
    r"""<(?:a\s[^>]*?href|img\s[^>]*?src)\s*=\s*["'](https?://[^"']+)["']""",
    re.IGNORECASE,
)
_LANG_ONLY_BLOCK = re.compile(
    r"<!--\s*lang-only:\s*([a-zA-Z0-9,\s-]+?)\s*-->(.*?)<!--\s*/lang-only\s*-->",
    re.DOTALL,
)
_BADGE_HOSTS = ("img.shields.io", "shields.io")


def file_lang(path: Path) -> str:
    """Leitet den Sprachcode einer Datei aus ihrem Namen ab (README.md -> en).

    Regionscodes bleiben erhalten und werden auf Bindestrich normalisiert:
    README_zh-CN.md und README_zh_CN.md liefern beide "zh-cn".
    """
    stem = path.stem
    if stem.lower() == "readme":
        return "en"
    m = re.match(r"readme[_-](.+)$", stem, re.IGNORECASE)
    if m:
        return m.group(1).replace("_", "-").lower()
    return stem.lower()


def _is_badge_url(link: str) -> bool:
    return any(host in link for host in _BADGE_HOSTS)


def _find_links(text: str) -> set[str]:
    return set(_LINK_MD.findall(text)) | set(_LINK_HTML.findall(text))


def extract_links(path: Path) -> tuple[set[str], list[tuple[set[str], set[str]]]]:
    """Liefert (untagged_links, tagged_blocks); tagged_blocks = Liste aus
    (Sprachcodes, darin gefundene Links).

    Wirft UnicodeDecodeError, wenn die Datei nicht als UTF-8 lesbar ist --
    main() faengt das kontrolliert ab (Exit 2), statt eine Traceback zu zeigen.
    """
    text = path.read_text(encoding="utf-8")
    tagged: list[tuple[set[str], set[str]]] = []
    for m in _LANG_ONLY_BLOCK.finditer(text):
        codes = {c.strip().lower() for c in m.group(1).split(",") if c.strip()}
        block_links = _find_links(m.group(2))
        if block_links:
            tagged.append((codes, block_links))
    untagged_text = _LANG_ONLY_BLOCK.sub("", text)
    untagged = _find_links(untagged_text)
    return untagged, tagged


def check_parity(paths: list[Path], include_badges: bool = False) -> list[str]:
    """Liefert eine Konfliktzeile je Link, der nicht in allen dafuer relevanten
    Dateien vorkommt."""
    per_file_untagged: dict[Path, set[str]] = {}
    per_file_tagged: dict[Path, list[tuple[set[str], set[str]]]] = {}
    per_file_tagged_links: dict[Path, set[str]] = {}
    lang_of: dict[Path, str] = {}

    for p in paths:
        untagged, tagged = extract_links(p)
        if not include_badges:
            untagged = {link for link in untagged if not _is_badge_url(link)}
        per_file_untagged[p] = untagged
        per_file_tagged[p] = tagged
        per_file_tagged_links[p] = {link for _, links in tagged for link in links}
        lang_of[p] = file_lang(p)

    known_langs = set(lang_of.values())
    conflicts: list[str] = []

    # 0) Fail-closed: ein lang-only-Code, der zu keiner uebergebenen Datei
    #    passt (Tippfehler wie "cn" statt "zh"), wird gemeldet statt den
    #    betroffenen Link stillschweigend freizustellen.
    reported_unknown: set[str] = set()
    for p in paths:
        for codes, block_links in per_file_tagged[p]:
            for code in sorted(codes - known_langs):
                if code in reported_unknown:
                    continue
                reported_unknown.add(code)
                conflicts.append(
                    f"lang-only-Code '{code}' in {p.name} passt zu keiner "
                    f"uebergebenen Sprachfassung ({sorted(known_langs)}) -- "
                    f"Tippfehler? Link(s) {sorted(block_links)} wurden NICHT "
                    f"freigestellt."
                )

    # 1) Unmarkierter Inhalt: muss in ALLEN uebergebenen Dateien vorkommen.
    all_untagged: set[str] = set()
    for links in per_file_untagged.values():
        all_untagged |= links
    for link in sorted(all_untagged):
        present = [p.name for p in paths if link in per_file_untagged[p]]
        missing = [p.name for p in paths if p.name not in present]
        if missing:
            conflicts.append(f"{link}: vorhanden in {present}, fehlt in {missing}")

    # 2) lang-only-markierter Inhalt: nur relevant fuer Dateien, deren Sprache
    #    in der Markierung genannt ist.
    seen: set[tuple[frozenset[str], str]] = set()
    for p in paths:
        for codes, block_links in per_file_tagged[p]:
            for link in block_links:
                key = (frozenset(codes), link)
                if key in seen:
                    continue
                seen.add(key)
                relevant = [q for q in paths if lang_of[q] in codes]
                if not relevant:
                    continue
                present = [q.name for q in relevant if link in per_file_tagged_links[q]]
                missing = [q.name for q in relevant if q.name not in present]
                if missing:
                    codes_str = ",".join(sorted(codes))
                    conflicts.append(
                        f"{link} (lang-only: {codes_str}): vorhanden in {present}, "
                        f"fehlt in {missing}"
                    )

    return conflicts


def main(argv: list[str]) -> int:
    args = argv[1:]
    include_badges = "--include-badges" in args
    args = [a for a in args if a != "--include-badges"]

    if len(args) < 2:
        print(
            "Nutzung: check_language_parity.py [--include-badges] "
            "<datei1> <datei2> [<datei3> ...]",
            file=sys.stderr,
        )
        return 2

    paths = [Path(a) for a in args]
    for p in paths:
        if not p.is_file():
            print(f"FEHLER: {p} ist keine lesbare Datei.", file=sys.stderr)
            return 2

    try:
        conflicts = check_parity(paths, include_badges=include_badges)
    except UnicodeDecodeError as exc:
        print(f"FEHLER: Datei nicht als UTF-8 lesbar ({exc}).", file=sys.stderr)
        return 2

    if not conflicts:
        print(f"OK: {len(paths)} Fassungen haben identische Link-Menge (Schritt-0-Rauchtest).")
        return 0

    print(f"KONFLIKT: {len(conflicts)} Link(s) nicht in allen relevanten Fassungen:")
    for c in conflicts:
        print(f"  - {c}")
    print(
        "Nie still loeschen/ignorieren: uebersetzen+in alle Fassungen uebernehmen, "
        "mit <!-- lang-only: <code> --> bewusst auf Sprachen beschraenken, oder als "
        "Konflikt eskalieren (siehe SKILL.md Schritt 0)."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
