---
name: bilingual-doc-sync
version: 1.2.2
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-09-26
description: >
  Parallel geführte Sprachfassungen eines Dokuments (Paper DE/EN, README + README_de,
  SKILL.md + SKILL.en.md, Website-Texte) synchron halten: fehlende Fassung nachziehen,
  Abschnitts-Parallelität prüfen, Divergenzen beheben — mit klarer Leitsprache-Regel und
  kontrolliertem Rücktransfer, wenn die Nebenfassung etwas besser löst. Nutze diesen Skill
  bei „sind DE und EN synchron?", „zieh die englische/deutsche Version nach",
  „Übersetzung ist veraltet", bei zweisprachigen Papers/READMEs/Skills, oder als
  periodischen Check über einen Dokumentbestand. Enthält auch das Expansions-Audit:
  bewerten, ob ein Projekt/Dokument WEITERE Sprachen verdient (i18n-Eignung nach
  Zielgruppe, technische Vorbereitung, kein blindes Massenübersetzen).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [übersetzung, zweisprachig, synchronisation, paper, readme, i18n, dokumentation]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">
# Bilingual-Doc-Sync — parallele Sprachfassungen synchron halten

## Zweck

Zweisprachig geführte Dokumente divergieren schleichend: Die aktiv bearbeitete Fassung
wächst, die andere veraltet — bis „Übersetzung" nur noch dem Namen nach stimmt. Dieser
Skill macht die Synchronprüfung zu einem definierten Ablauf mit einer entscheidenden
Vorab-Festlegung: **Welche Fassung führt?** Ohne Leitsprache-Regel wird jede Divergenz
zur Einzelfallentscheidung und der Abgleich unwiederholbar.

## Ablauf

### 0. Einsprachigen Inhalt erkennen (VOR jedem Abgleich)

Divergenz ist nicht immer „veraltet" — manchmal ist sie **neuer, echter Inhalt, der bisher
nur in einer Fassung existiert** (externer Beitrag/PR in einer Nicht-Leitsprache, eine
Änderung, die zuerst in der Nebenfassung ankam, oder Content-Verlust durch einen
History-Rewrite o. ä.). Das ursprüngliche Verfahren kannte nur „in EN oder DE eintragen,
dann an alle ausliefern" — keinen Fall, in dem etwas nur in einer Fassung steht. Belegfall:
`ellmos-ai/skills` PR #1 fügte einen chinesischsprachigen Discovery-Link nur in README.md
ein; ein späterer History-Rewrite verlor ihn wieder, weil kein Schritt geprüft hat, ob
Inhalt existiert, der in keiner anderen Fassung steht (T-20260926-967984806).

- **Prüfen, nicht annehmen:** Vor dem eigentlichen Abgleich (Schritt 3) einen Diff gegen
  den letzten bekannten synchronisierten Stand (oder gegen die anderen Fassungen direkt)
  ziehen und gezielt nach Inhalt suchen, der in EINER Fassung neu ist und in KEINER anderen
  ein Gegenstück hat — nicht nur nach fehlenden Abschnitten der Leitsprache.
- **Werkzeug:** `scripts/check_language_parity.py <datei1> <datei2> [...]` extrahiert
  Markdown- UND HTML-Links (`[text](url)`, `<a href="url">`, `<img src="url">`) aus allen
  übergebenen Fassungen (Links bleiben über Übersetzung hinweg unverändert und sind damit
  ein robuster, sprachunabhängiger Indikator) und meldet jeden Link, der nicht in ALLEN
  Fassungen vorkommt, mit Exit 1. Exit 0 heißt: keine Link-Teilmengen-Abweichung gefunden —
  kein Beweis für vollständige Parität, aber ein gezielter Schritt-0-Rauchtest vor dem
  manuellen Abgleich. Links innerhalb eines `<!-- lang-only: <code> -->`-Blocks werden nur
  gegen Dateien geprüft, deren Sprachcode in der Markierung genannt ist (per Dateiname
  erkannt, z. B. `README_zh.md` → `zh`, `README.md` → `en`) — sie zählen dort NICHT als
  „fehlt in den anderen Fassungen". Zusätzlich filtert das Skript standardmäßig
  `shields.io`-Badge-URLs mit codiertem Label-Text heraus (dort steckt oft die übersetzte
  Beschriftung direkt in der URL — kein echter Contentverlust, sondern erwartete
  Übersetzungs-Varianz; `--include-badges` schaltet den Filter ab). Nicht-UTF-8-lesbare
  Dateien und fehlende Argumente enden mit Exit 2 und einer Fehlermeldung, nicht mit einem
  Traceback.
- **Entscheidung bei Fund:** einsprachiger Inhalt wird NIE still verworfen. Drei Auswege,
  keine stille Löschung:
  (a) **übersetzen und in ALLE Fassungen übernehmen** — der Normalfall bei allgemein
  relevantem Inhalt;
  (b) **bewusst auf eine/mehrere Sprache(n) beschränkt** ("lang-only") — wenn der Inhalt nur
  für diese Zielgruppe gilt (Belegfall T-20260926-967984806: ein chinesischsprachiger
  Discovery-Link ist für DE/ES/JA/RU-Leser:innen nicht relevant, eine Übersetzung in alle
  sechs Fassungen wäre selbst falsch gewesen — Nutzerkorrektur nach der ersten Fassung
  dieses Schritts). Markierung: **`<!-- lang-only: <code>[,<code>...] --> … <!-- /lang-only -->`**
  (HTML-Kommentar, in Markdown-Renderern unsichtbar; für mehrere Zielsprachen kommagetrennt,
  z. B. `zh,ja`). Kein etablierter Branchenstandard für diesen engen Fall bekannt (P-009
  geprüft) — HTML-Kommentare sind die portabelste, unsichtbar rendernde Wahl für Markdown.
  Markierter Inhalt wird beim Abgleich **weder übersetzt noch als fehlend gemeldet**;
  (c) **als Konflikt eskalieren**, wenn unklar ist, ob der Inhalt noch gewollt ist (z. B. wirkt
  widersprüchlich zur Leitfassung) — Nutzer/Entscheidungskette fragen.
  In allen drei Fällen gilt: niemals kommentarlos aus der Fassung entfernen, in der der
  Inhalt steht, nur weil die anderen ihn nicht haben.

### 1. Bestand feststellen

- Liegen beide (alle) Sprachfassungen vor? Fehlt eine ganz → **nachziehen** (vollständige
  Übersetzung der führenden Fassung, nicht Neudichtung).
- Namenskonvention prüfen (z. B. `DOKUMENT.md` + `DOKUMENT.en.md` oder `_de`/`_en`-Suffixe)
  und Abweichler angleichen — Auffindbarkeit ist die halbe Synchronität.

### 2. Leitsprache klären (vor jedem Abgleich)

- Die Leitsprache ist die Fassung, in der inhaltlich gearbeitet wird (bei Papers oft EN,
  bei lokaler Doku oft die Muttersprache). Sie gewinnt bei Widerspruch.
- **Rücktransfer-Ausnahme:** Löst die Nebenfassung etwas nachweislich besser (klarere
  Formulierung, korrigierter Fehler), wird es in die Leitfassung ÜBERNOMMEN — erst
  rücktransferieren, dann normal synchronisieren. Fachliche Korrektheit prüfen, bevor
  eine „schönere" Formulierung übernommen wird.

### 3. Parallelität prüfen

Struktur zuerst, dann Inhalt:

1. **Gliederungsvergleich:** Abschnitte/Überschriften beider Fassungen nebeneinander —
   fehlende, zusätzliche, umsortierte Abschnitte sind die groben Divergenzen.
2. **Abschnittsweise Stichprobe** der übereinstimmenden Gliederung: Aussagen, Zahlen,
   Verweise, Beispiele identisch? Besonders divergenzanfällig: Changelogs, Tabellen,
   Zahlenwerte, Literatur-/Linkverzeichnisse, zuletzt bearbeitete Abschnitte.
3. **Nicht übersetzbare Invarianten** prüfen: Code-Blöcke, Identifier, Formeln, Pfade
   müssen in beiden Fassungen IDENTISCH sein (Code wird nie übersetzt).

### 4. Beheben

- Divergenzen in Richtung Leitsprache auflösen (bzw. nach Rücktransfer).
- Sprachtypografie der Zielsprache respektieren (im Deutschen echte Umlaute ä ö ü ß,
  keine ae/oe/ue-Ersatzschreibung; Anführungszeichen-Konventionen).
- Metadaten nachziehen: Versionsnummern, Datumsfelder, Changelog-Einträge in BEIDEN
  Fassungen (der Changelog selbst ist der häufigste Divergenzpunkt).

### 5. Dokumentieren

Ergebnis festhalten (was war divergent, was wurde übernommen, was rücktransferiert).
Als periodischer Lauf über einen Bestand: mit dem Rotations-Gerüst kombinieren
(`rotation-check`) — ein Dokument(-Paar) pro Lauf, Registry als Gedächtnis.

## Erweiterung: Expansions-Audit (sollten MEHR Sprachen existieren?)

Neben dem Synchronhalten bestehender Fassungen gehört zur Sprachpflege die Frage, ob ein
Dokument/Projekt WEITERE Sprachen verdient:

1. **Eignung bewerten** statt blind übersetzen: Zielgruppe, internationale Nutzbarkeit,
   Store-/Web-Präsenz, Mobilität des Inhalts. Nicht jedes interne Dokument braucht Englisch;
   nicht jede App braucht fünf Sprachen.
2. **Technische Vorbereitung prüfen:** Ist das Ziel überhaupt auf Sprachdateien/Parallel-
   Fassungen vorbereitet (i18n-Struktur, Namenskonvention)? Wenn nein, ist DAS die erste
   Aufgabe, nicht die Übersetzung.
3. **Befund dokumentieren, nicht sofort massenübersetzen:** Konkrete Übersetzungsaufgaben
   in die projektlokale TODO-Datei; „keine weitere Sprache sinnvoll" ist ein gültiges,
   festzuhaltendes Ergebnis.
4. **QA bei nachgezogenen Fassungen:** Auto-generierte Übersetzungen stichprobenartig
   gegen die Leitfassung prüfen (Abschnitt 3), bevor sie als „vorhanden" gelten.

## Beispiel

```text
Auftrag: „Prüf, ob das Paper in DE und EN synchron ist."

1. Bestand: paper_en.tex (führend) + paper_de.tex vorhanden.
2. Gliederung: DE fehlt der neue Abschnitt 4.2 (letzte EN-Revision); DE hat einen
   besseren Beweis-Absatz in 3.1.
3. Rücktransfer: 3.1-Formulierung fachlich geprüft → in EN übernommen.
4. Nachziehen: 4.2 nach DE übersetzt; Zahlen in Tabelle 2 abgeglichen (DE hatte
   veraltete Werte); Literaturverzeichnis identisch gemacht.
5. Registry-Eintrag: „paper-X | 2026-07-03 | de-en-sync | 3 Divergenzen behoben,
   1 Rücktransfer | nächster Check nach nächster EN-Revision".
```

## Red Flags

| Gedanke | Realität |
| --- | --- |
| „Ich übersetze die Unterschiede einfach frisch" | Erst Leitsprache + Rücktransfer-Frage klären — sonst wird die bessere Lösung überschrieben. |
| „Die Gliederung passt, also ist es synchron" | Zahlen, Changelogs und Verweise divergieren zuerst — Stichprobe in die Tiefe ist Pflicht. |
| „Code-Kommentare übersetze ich mit" | Code-Blöcke und Identifier bleiben in beiden Fassungen identisch (englisch). |
| „Ich synchronisiere alle Dokumente in einem Rutsch" | Ein Paar pro Lauf (Rotations-Gerüst) hält den Abgleich prüfbar. |

## Verwandte Skills

- `rotation-check` — Gerüst für den periodischen Lauf über einen Dokumentbestand.
- `workflow-extract` — wenn dieser Check als stehende Automation eingerichtet werden soll.

## Changelog

### 1.2.2 (2026-09-26)
- `scripts/check_language_parity.py`: Praefixregel fuer lang-only-Codes —
  ein Basis-Code (z.B. `zh`) deckt jetzt auch seine Regionsvarianten ab
  (`zh-cn`, `zh-tw`); umgekehrt gilt das nicht.
- Die fail-closed-Pruefung eines lang-only-Codes vergleicht jetzt gegen ALLE
  README-Dateien im Verzeichnis, nicht nur die uebergebene Teilmenge — ein
  Aufruf mit nur zwei von sechs Fassungen loest dadurch keinen Fehlalarm
  mehr aus. Ein gueltiger Code ohne Datei in DIESEM Aufruf ergibt jetzt nur
  einen Hinweis (kein Exit 1); ein wirklich unbekannter Code (Tippfehler wie
  `cn` statt `zh`) bleibt Exit 1.

### 1.2.1 (2026-09-26)
- `scripts/check_language_parity.py`: ein lang-only-Code, der zu keiner der
  uebergebenen Sprachfassungen passt (z.B. Tippfehler `cn` statt `zh`), wird
  jetzt fail-closed als Befund gemeldet statt den Link still freizustellen.
- Dateinamen mit Regionscode werden jetzt als Sprache erkannt:
  `README_zh-CN.md` und `README_zh_CN.md` liefern beide `zh-cn`.

### 1.2.0 (2026-09-26)
- Schritt 0 „Einsprachigen Inhalt erkennen" ergänzt (T-20260926-967984806): Divergenz kann
  neuer, noch nicht propagierter Inhalt sein statt Veralterung; drei Auswege (übersetzen+
  überall / lang-only markieren / als Konflikt eskalieren), nie stille Löschung. Neue
  `<!-- lang-only: <code> -->`-Markierung für bewusst zielgruppenbeschränkten Inhalt.
- `scripts/check_language_parity.py` + `scripts/test_check_language_parity.py` ergänzt:
  findet Links, die nur in einer Teilmenge der Sprachfassungen vorkommen (Markdown- und
  HTML-Links), respektiert die lang-only-Markierung, filtert shields.io-Badge-Rauschen,
  fängt Nicht-UTF-8-Dateien mit Exit 2 statt Traceback ab.

### 1.1.0 (2026-07-03)
- Expansions-Audit ergänzt (i18n-Eignung bewerten, technische Vorbereitung, QA für
  nachgezogene Fassungen) — integriert statt als eigener i18n-coverage-audit-Skill
  (Dedup-Entscheid).

### 1.0.0 (2026-07-03)
- Initiale Version. Abstrahiert aus der Codex-Automation
  „research-paper-de-en-synchronisationscheck", verallgemeinert auf beliebige parallel
  geführte Sprachfassungen (Papers, READMEs, Skills, Website-Texte).
