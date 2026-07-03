---
name: bilingual-doc-sync
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
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

# Bilingual-Doc-Sync — parallele Sprachfassungen synchron halten

## Zweck

Zweisprachig geführte Dokumente divergieren schleichend: Die aktiv bearbeitete Fassung
wächst, die andere veraltet — bis „Übersetzung" nur noch dem Namen nach stimmt. Dieser
Skill macht die Synchronprüfung zu einem definierten Ablauf mit einer entscheidenden
Vorab-Festlegung: **Welche Fassung führt?** Ohne Leitsprache-Regel wird jede Divergenz
zur Einzelfallentscheidung und der Abgleich unwiederholbar.

## Ablauf

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

### 1.1.0 (2026-07-03)
- Expansions-Audit ergänzt (i18n-Eignung bewerten, technische Vorbereitung, QA für
  nachgezogene Fassungen) — integriert statt als eigener i18n-coverage-audit-Skill
  (Dedup-Entscheid).

### 1.0.0 (2026-07-03)
- Initiale Version. Abstrahiert aus der Codex-Automation
  „research-paper-de-en-synchronisationscheck", verallgemeinert auf beliebige parallel
  geführte Sprachfassungen (Papers, READMEs, Skills, Website-Texte).
