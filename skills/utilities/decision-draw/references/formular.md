# Entscheidungsvorlage als Formular: Bauanleitung

Wiederverwendbare Anleitung, wie aus einem fertigen Entscheidungsdokument (Bündel von Entscheidungen, [decision-draw](../SKILL.md) oder [decision-briefing](../../decision-briefing/SKILL.md)) ein **klickbares Formular** wird. Gilt für beide Skills; die Referenzimplementierung liegt in `scripts/formular/` dieses Skills.

> **Status:** Weg A (HTML-Formular) ist erprobt und der Standard. Weg B (Tk-Fenster) ist nativ **nicht abgenommen** und wird erst nach ausdrücklicher Zustimmung der Nutzerin oder des Nutzers geöffnet (siehe [viewer.md](viewer.md)).

## 1. Zweck

Wer viele Entscheidungen zu treffen hat, soll sie im Dokument selbst anklicken statt im Chat in Kürzeln zu antworten. Das Formular erlaubt eine Massenabnahme („alles wie empfohlen“), pro Posten eine Anmerkung, ein Zwischenspeichern und ein Abschicken. Am Ende liegt eine **Antwortdatei** vor, die die Entscheidungen maschinenlesbar enthält. Gebucht wird weiterhin nur über `decision-briefing` Phase 4; das Formular schreibt in kein Register.

## 2. Zwei Wege

| | Weg A: selbstenthaltenes HTML-Formular | Weg B: Tk-Fenster mit `draw.json` |
|---|---|---|
| Ort | `scripts/formular/` (Generator, Skript, Stil, Selbsttest) | `scripts/decision_viewer.py`, Format `references/draw.schema.json` |
| Eingabe | das Entscheidungsdokument als Markdown | eine `draw.json` (Äste, Texte, Quellen) |
| Ausgabe | Antwortdatei `ticket-master.decision-answers.v1` plus eine schreibgeschützte beantwortete Kopie | `draw_decided.json` mit Revisions- und Hashprüfung |
| Voraussetzung | Python 3.10+, Paket `markdown`, ein Browser zum Ausfüllen | Python 3.10+ mit Tk |
| Stand | erprobt (Referenz vom 2026-11-07) | nativ nicht abgenommen |

Faustregel: A, wenn das Dokument bereits als Markdown mit den Tabellen unten existiert. B, wenn ein Konsument die Äste einzeln beansprucht (`claim`, `processed`) und eine Dateisperre braucht.

## 3. Weg A in Schritten

1. **Dokument im erwarteten Muster schreiben.** Der Generator liest nur Markdown und erkennt dieses Muster:
   - je Bündel ein Abschnitt `## Bündel N: Titel` mit einer Tabelle, deren Kopf mit `Kürzel` beginnt, eine Spalte mit „Empfehlung“ und (optional) eine Spalte „Geld / Löschung / …“ enthält und deren letzte Spalte die Konfidenz ist;
   - im Anhang ein Abschnitt `#### Teil 1` mit einer Tabelle (`Zeile | Frage | Optionen | Avatar-Wahl | Konfidenz | …`) und ein Abschnitt `#### Teil 2` (`Zeile | Empfehlung …`);
   - Optionen als `A: Text; B: Text; C: Text`. Stammen die Optionen vom Schreiber und nicht aus der Quelle, hängt `(Optionen vom Schreiber)` an; das Formular weist darauf hin.
2. **Formular erzeugen:**
   ```
   pip install markdown
   python scripts/formular/build_formular.py --md <DOKUMENT.md> --out <DOKUMENT_FORMULAR.html>
   ```
   Die Ausgabe ist eine einzige HTML-Datei ohne Netzzugriff (keine externen Skripte, Schriften oder Verweise), hell und dunkel, handytauglich. Der Generator gibt den `document_sha256` aus.
3. **Für ein neues Dokument anpassen** (die Referenz ist an das Dokument vom 2026-11-07 gebunden). Diese Stellen in `build_formular.py` gehören zum Dokument, nicht zum Verfahren:
   - `DOC_ID` (Dokumentkennung, steckt auch in den Dateinamen der Antwort);
   - `SUBITEM_SENS`: Untersachen (z. B. `T2.3`) erben aus der Zeile ihres Oberpostens nichts; ihre Markierungsgründe stehen hier;
   - `SENS_RX`: Stichwörter, die einen Posten als sensibel markieren (Löschung, Geld, Außenwirkung, Lizenz, Rechte Dritter, Veröffentlichung);
   - `bundle_block()`: der Vorab-Block „AGPL bleibt“ im ersten Bündel und das Feld `agpl_bleibt` in Antwortdatei und Validator sind eine Besonderheit des Referenzdokuments und werden gestrichen oder durch eine eigene Vorab-Frage ersetzt;
   - im Selbsttest `EXPECTED_IDS`, `EXPECTED_MARKED`, `SEAL_SHA` (siehe Abschnitt 6).
4. **Unabhängig prüfen lassen**, bevor es zugestellt wird (Abschnitt 5).
5. **Zustellen**, die Nutzerin oder der Nutzer klickt, speichert und sagt dem Konsumenten Bescheid.
6. **Antwortdatei lesen und buchen:** Der Konsument prüft die Datei mit `validate_answers()` (Schema, Hash, vollständige Kürzel, Zählung), zerlegt Teilantworten über den Rücktransfer des Skills und bucht ausschließlich über `decision-briefing` Phase 4.

## 4. Antwortschema `ticket-master.decision-answers.v1`

Eine JSON-Datei. Pflichtfelder (der Validator `validate_answers()` in `build_formular.py` ist maßgeblich):

| Feld | Inhalt |
|---|---|
| `schema` | `ticket-master.decision-answers.v1` |
| `document_id` | Kennung des Dokuments |
| `document_sha256` | SHA-256 des unveränderten Formulars, in dem der eingebettete Hash durch 64 Nullen ersetzt ist (damit die Antwort an genau diese Fassung gebunden ist) |
| `saved_at` | UTC, ISO 8601 |
| `answers` | je Kürzel: `choice` (Buchstabe oder `null`), `choice_label`, `state` (`answered` oder `open`), `note`, `via` (`single` oder `bulk`), `recommended`, `avatar_prediction`, `avatar_confidence`, `marked` |
| `bulk_actions` | welche Massenaktionen ausgelöst wurden |
| `gesamtabnahme` | `explicit` (nur `true` nach ausdrücklichem „Ja“ im Dialog **und** alle Posten wie empfohlen), `at` |
| `counts` | `total`, `answered`, `open` (müssen zu `answers` passen) |
| `agpl_bleibt` | Besonderheit des Referenzdokuments |

Offene Posten bleiben `open`; eine Teilantwort ist **keine** Gesamtabnahme.

## 5. Pflichtregeln (aus dem Vorfall vom 2026-11-07)

Jede Regel hat einen Grund; wer ein Formular baut, hält alle ein.

1. **Nichts vorausgewählt** (oder ausdrücklich als vorausgewählt gekennzeichnet). Eine Vorbelegung wirkt sonst wie ein Selbstausfüllen: Die Antwort stammt dann vom Schreiber, nicht von der Nutzerin oder dem Nutzer. Im Tk-Weg dafür `"preselect": "none"`.
2. **Gesamtabnahme nur nach ausdrücklichem „Ja“ im Dokument-Dialog** (kein Browser-`alert`, sondern ein Dialog im Dokument). Sie gilt, solange alle Posten wie empfohlen stehen, und wird zurückgenommen, sobald danach ein Posten selbst geändert wird.
3. **Bei Wiederherstellung (Zwischenstand aus `localStorage`) nie die Gesamtabnahme übernehmen.** Ein früherer Stand darf eine neue ausdrückliche Bestätigung nicht ersetzen. Das Formular weist darauf hin.
4. **Sensible Posten vor dem Speichern auflisten:** rot (Avatar ohne Vorhersage), Geld, Löschung, Außenwirkung, Lizenz, Rechte Dritter, Veröffentlichung. Massenaktionen nennen sie ausdrücklich, bevor sie angenommen werden.
5. **UI-Tests nur headless und nie über sichtbare Browser oder die Playwright-MCP-Werkzeuge.** Vorfall: Ein sichtbarer Test-Browser auf dem Rechner der Nutzerin oder des Nutzers füllte das Formular selbst aus. Zulässig ist ausschließlich Python-Playwright mit `headless=True`, eigenem Temp-Profil und Download-Fallback (`scripts/formular/headless_util.py`). Fixtures aus solchen Läufen sind **Testdaten, keine Nutzerentscheidung** und werden entsprechend gekennzeichnet.
6. **Zustellung erst nach unabhängiger Prüfung** durch eine andere Instanz (Hash, Posten gegen das Quelldokument, nichts vorausgewählt, Roundtrip der Antwortdatei, Headless-Wiederherstellung).
7. **Buchung nur über `decision-briefing` Phase 4.** Das Formular, der Generator und der Viewer besitzen keinen eigenen Schreibweg ins Register.
8. **Messung gegen eine versiegelte Avatar-Prognose (optional):** Die Prognose wird vor der Zustellung mit UTC-Zeit und SHA-256 versiegelt, im Formular als Avatar-Wahl und Konfidenz je Posten angezeigt und nach der Antwort ausgewertet. Antwortdatei und Siegel werden nicht vermischt; die Empfehlung des Schreibers ist ein dritter Vergleichsarm.

## 6. Prüfen

- **Selbsttest** (Standardbibliothek plus `markdown`):
  `FORMULAR_MD=<DOKUMENT.md> [FORMULAR_MESSUNG=<Messdatei.md>] python -m unittest selbsttest_formular -v` im Ordner `scripts/formular/`. Er prüft: reproduzierbarer Hash, Posten, Optionen, Empfehlung und Avatar-Angaben gegen das Quelldokument (und, falls lesbar, gegen die versiegelte Messdatei, nur lesend), nichts vorausgewählt, kein Netz, Text des Dokuments unverändert, Schema und Roundtrip der Antwortdatei, Wiederherstellung ohne Gesamtabnahme. Die Datei heißt nicht `test_*.py`, damit sie nicht automatisch eingesammelt wird; sie ist an das Referenzdokument gebunden und für ein neues Dokument anzupassen.
- **Fixtures** (`testdata/`) entstehen durch einen echten Headless-Lauf: `python make_fixtures.py <FORMULAR.html> <Zielordner>`. Ändert sich das Formular, ändert sich sein Hash, und die Fixtures müssen neu erzeugt werden. Sie sind nicht Teil des Skills.
- **Weg B:** `python scripts/decision_viewer.py validate <draw.json>` ist headless; gezielte Tests in `testing/test_decision_draw_viewer.py`.

## 7. Weg B: Draw als `draw.json` abbilden

Wer den Tk-Viewer nutzt (erst nach Zustimmung, siehe Status oben), bildet das Dokument so ab:

- jeder Posten und jede Untersache wird ein Ast mit eigener `id` (das Kürzel), Klartexttitel und Text; Quelle, Alternativen und Adressat stehen in `source_ref`, `alternatives_ref`, `addressee`;
- rote, Geld-, Lösch-, Außen-, Lizenz- und Rechte-Dritter-Posten erhalten `"sensitive": true`;
- soll jede Entscheidung selbst getroffen werden (besonders bei den sensiblen Posten), `"preselect": "none"` setzen;
- reale fachliche Voraussetzungen kommen in `depends_on`, nicht in die Baumstruktur;
- danach `validate`, öffnen, Ergebnis mit `read` lesen, vor jedem externen Effekt `claim`, nach der Phase-4-Buchung `processed` (Einzelheiten in [viewer.md](viewer.md)).

Ein Generator für diesen Weg gehört nicht zum Skill; `references/example.json` zeigt das Format.
