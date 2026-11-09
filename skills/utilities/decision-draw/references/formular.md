# Entscheidungsvorlage als Formular: Bauanleitung

Wiederverwendbare Anleitung, wie aus einer Entscheidungsvorlage (Bündel von Entscheidungen, [decision-draw](../SKILL.md) oder [decision-briefing](../../decision-briefing/SKILL.md)) ein **klickbares Formular** wird. Gilt für beide Skills; die Referenzimplementierung liegt in `scripts/formular/` dieses Skills.

> **Standard: Das Formular wird nicht neu gebaut.** Du schreibst eine kleine Daten-JSON ([`form.schema.json`](../scripts/formular/form.schema.json), Beispiel [`example_form.json`](../scripts/formular/example_form.json)) und rufst `python scripts/formular/build_form.py <daten.json> --out <formular.html>` auf. Template, Skript und Stil bleiben gleich.

> **Status:** Weg A (HTML-Formular) ist erprobt und der Standard. Weg B (Tk-Fenster) ist nativ **nicht abgenommen** und wird erst nach ausdrücklicher Zustimmung der Nutzerin oder des Nutzers geöffnet (siehe [viewer.md](viewer.md)). Der Dialog zur Ordnerwahl im echten Edge wurde nicht getestet, nur simulierte Ausfälle (headless).

## 1. Zweck

Wer viele Entscheidungen zu treffen hat, soll sie im Dokument selbst anklicken statt im Chat in Kürzeln zu antworten. Das Formular erlaubt eine Massenabnahme („alles wie empfohlen“), pro Posten eine Anmerkung, die Wahl „Rückfrage / mehr Info nötig“, ein Zwischenspeichern und ein Abschicken. Am Ende liegt eine **Antwortdatei** vor, die die Entscheidungen maschinenlesbar enthält. Gebucht wird weiterhin nur über `decision-briefing` Phase 4; das Formular schreibt in kein Register.

## 2. Zwei Wege

| | Weg A: selbstenthaltenes HTML-Formular | Weg B: Tk-Fenster mit `draw.json` |
|---|---|---|
| Ort | `scripts/formular/` (Template, Generator, Skript, Stil, Selbsttests) | `scripts/decision_viewer.py`, Format `references/draw.schema.json` |
| Eingabe | Daten-JSON nach `form.schema.json` | eine `draw.json` (Äste, Texte, Quellen) |
| Ausgabe | Antwortdatei `ticket-master.decision-answers.v1` plus eine schreibgeschützte beantwortete Kopie | `draw_decided.json` mit Revisions- und Hashprüfung |
| Voraussetzung | Python 3.10+; für `details_markdown` das Paket `markdown`; ein Browser zum Ausfüllen | Python 3.10+ mit Tk |
| Stand | erprobt | nativ nicht abgenommen |

Faustregel: A, solange nichts dagegen spricht. B, wenn ein Konsument die Äste einzeln beansprucht (`claim`, `processed`) und eine Dateisperre braucht.

## 3. Weg A in Schritten

1. **Daten schreiben** nach der Postenvorlage (Abschnitt 4). Ein neues Dokument ist eine neue Daten-Datei, kein neuer Generator.
2. **Bauen:**
   ```
   pip install markdown        # nur nötig, wenn ein Posten details_markdown hat
   python scripts/formular/build_form.py <daten.json> --out <formular.html>
   ```
   Der Generator prüft **alles auf einmal** und bricht mit einer Fehlerliste ab: Pflichtfelder, Längengrenzen (nie stilles Kürzen), Empfehlung und Optionen, Bilder, unbekannte Felder (Tippfehler). Die Ausgabe ist eine einzige HTML-Datei ohne Netzzugriff (keine externen Skripte, Schriften oder Verweise), hell und dunkel, handytauglich. Der `document_sha256` wird ausgegeben; derselbe Eingang ergibt byte-gleiche Ausgabe.
3. **Unabhängig prüfen lassen**, bevor es zugestellt wird (Regel 6 in Abschnitt 6).
4. **Zustellen:** Die Nutzerin oder der Nutzer klickt, speichert und sagt dem Konsumenten Bescheid. Das Speichern klappt auch ohne Ordnerdialog (Regel 9): „Speichern und abschicken“ versucht zuerst den Ordner; Download-Links, Text und Zwischenstand stehen immer bereit.
5. **Antwortdatei lesen und buchen:** Der Konsument prüft die Datei mit `validate_answers()` (Schema, Hash, vollständige Kürzel, Zählung), behandelt Rückfragen als Fragen (nicht als Entscheidungen), zerlegt Teilantworten über den Rücktransfer des Skills und bucht ausschließlich über `decision-briefing` Phase 4.

Das ältere Verfahren (aus einem Markdown-Gesamtdokument bauen) steht nur noch als **Beispielmigration** in `scripts/formular/build_from_markdown.py`; es ist an das Dokument vom 2026-11-07 gebunden. Wer ein vorhandenes Markdown-Dokument überführen will, schreibt die Daten-JSON daraus, statt den alten Generator anzupassen.

## 4. Postenvorlage: kurz und entscheidungsrelevant

Rückmeldung nach dem ersten Einsatz: Es war zu viel Text, und oft fehlte das Entscheidungsrelevante. Ein kurzer Kontext genügt, um an das Projekt zu erinnern. Deshalb hat jeder Posten feste Felder mit Grenzen; Überschreitung ist ein Fehler mit Hinweis.

| Feld | Pflicht | Grenze | Inhalt |
|---|---|---|---|
| `kuerzel`, `titel` | ja | Titel 80 Zeichen | eindeutige Kennung und ein sprechender Titel |
| `kontext` | ja | 250 Zeichen (höchstens zwei Sätze) | worum es geht, woran es erinnert |
| `frage` | ja | 200 Zeichen | die Entscheidung als Frage |
| `optionen[]` mit `id`, `label`, `wirkung` | ja, 2 bis 6 | Label 100, Wirkung 160 Zeichen | je Option ein Satz Wirkung |
| `empfehlung` mit `option`, `grund` | nein | Grund 160 Zeichen (ein Satz) | die Empfehlung mit einem Grund; ohne sie steht „keine Empfehlung“ |
| `kosten_aufwand` | ja | 160 Zeichen | Geld und Aufwand; darf „keine“ lauten, fehlen darf es nicht |
| `risiko_rueckgaengig` | ja | 160 Zeichen | Risiko und ob es rückgängig zu machen ist; darf „keine“ lauten |
| `frist` | ja | 160 Zeichen | bis wann; darf „keine“ lauten, fehlen darf es nicht |
| `folge_bei_nein` | ja | 160 Zeichen | was passiert, wenn nichts oder „Nein“ gewählt wird; darf „keine“ lauten |
| `avatar` mit `wahl`, `konfidenz` | nein | – | Vorhersage und Konfidenz (grün, gelb, rot) für die Messung; Badge erscheint im Formular erst nach getroffener Wahl |
| `sensitiv`, `sensitiv_grund` | nein | Grund 100 Zeichen | rot, Geld, Löschung, Außenwirkung, Lizenz, Rechte Dritter: wird vor dem Speichern noch einmal aufgelistet |
| `details_markdown` | nein | 4000 Zeichen | Längeres **nur aufklappbar**; wird vor der Umwandlung escaped; erlaubt sind nur Links mit `http:`, `https:`, `mailto:`, `#`, `/` und `./`, bei `/` genau ein führender Schrägstrich (`//host` und `/\host`, auch als `%2F`/`%5C`, wären in der lokal geöffneten Seite ein Netzwerkpfad und werden abgelehnt); geprüft wird der **ausgegebene** Wert nach einmaligem Auflösen der Entities und dem Entfernen von Leerraum und Steuerzeichen; Steuerzeichen im Text und Bilder aus dem Netz (`![](…)`) werden abgelehnt, Bilder gehören in `bilder[]` |
| `bilder_modus` | nein | `serie`, `polaroid`, `swipe` | Format und Interaktionsmodus der Bilder: `serie` (Standard), `polaroid` oder `swipe` |
| `bilder[]` | nein | `serie`: max. 12, `polaroid`: 2–12 (exakt Optionenanzahl), `swipe`: max. 60 | siehe unten |

Das Dokument selbst hat `titel` (80), `kontext_kurz` (400 Zeichen, höchstens drei Sätze, erinnert an das Projekt), `dokument_id` (steckt in den Dateinamen der Antwort) und optional `zielordner`. Oben im Formular stehen nur dieser Kontext und „So antwortest du“ in drei Zeilen; lange Fließtexte und „Hinweise vor dem Lesen“ entfallen.

**Checkliste „Entscheidungsrelevantes“** (vor dem Bauen je Posten abhaken): Kosten oder Aufwand genannt? Risiko und Rückgängigmachbarkeit genannt? Frist genannt (oder „keine“)? Folge bei „Nein“ genannt? Ist erwähnt, was schon entschieden ist (im Kontext, nicht als Absatz)? Steht Längeres nur in den aufklappbaren Details?

**Wahl „Rückfrage / mehr Info nötig“:** Jeder Posten hat sie als eigene Wahl neben den Optionen (`choice: "rueckfrage"`, `state: "question"`). Die Anmerkung gilt dann als Frage. Eine Rückfrage ist nie eine Zustimmung: Sie blockiert die Gesamtabnahme und wird vor dem Speichern gelistet (ohne Text in der Anmerkung mit Hinweis). Der Konsument beantwortet sie, statt zu buchen.

**Bilder (optional):** Je Bild `pfad` (Quelle beim Bauen, **nur relativ zum Datenordner**: absolute, UNC- und Laufwerkspfade, `..` und Links, die aus dem Ordner herausführen, werden vor dem ersten Dateizugriff abgelehnt) oder `data_uri`, `beschriftung` (Pflicht, kurz), optional `id` (Standard `bild-N`), `alt`, `seite`, `variante` (z. B. für Screenshots einer Oberfläche). Der Generator bettet jedes Bild als `data:`-URI ein: höchstens 400 KB je Bild und 8 MB je Formular, nur PNG, JPEG, WebP, GIF (kein SVG, Dateiinhalt wird geprüft); bei Überschreitung bricht er mit Klartext ab, ohne zu kürzen. Verkleinere vorher (Breite höchstens 1200 px).

### Bild-Modi und Entscheidungsarten

Das Feld `bilder_modus` steuert, wie Bilder dargestellt werden und wie die Nutzerin oder der Nutzer damit interagiert:

| Entscheidungsart | Geeigneter Bild-Modus | Beschreibung & Interaktion |
|---|---|---|
| **Variantenvergleich** (Design A vs. B vs. C, Layouts, Mockups) | `polaroid` (`bilder_modus: "polaroid"`) | Jede Option erhält eine Polaroid-Karte mit großem Kennbuchstaben (A, B, C), Bild, Beschriftung und Label. Auswahl per Klick oder Tastendruck (A/B/C). Bildanzahl (2–12) muss exakt der Zahl der Optionen entsprechen. |
| **Massenprüfung / Durchsicht** (Belege, Dokumente, Icons einzeln prüfen) | `swipe` (`bilder_modus: "swipe"`) | Jedes Bild (1–60) wird im Stapel einzeln entschieden (Rechts/Pfeil Rechts = Ja, Links/Pfeil Links = Nein, Oben/Pfeil Oben = Rückfrage, Backspace = Undo). Erst nach Klick auf „Einzelentscheidungen bestätigen“ zählt der Posten als entschieden. |
| **Kontext-Bilderserie** (Vorher/Nachher, Arbeitsablauf, Status quo) | `serie` (`bilder_modus: "serie"`, Standard) | 1 bis 12 Bilder nebeneinander als Referenz zur Frage. Die Entscheidung bezieht sich auf die gesamte Serie. |

**Weitere Entscheidungsformate (Erweiterungsausblick):**
- **Checkliste:** Mehrere voneinander unabhängige Kriterien oder Teilentscheidungen mit Checkboxen.
- **Diff:** Visueller Text- und Code-Vergleich mit hervorgehobenen Änderungen.
- **Vorher / Nachher:** Gezielter Gegenüberstellungs- oder Schieberegler-Vergleich zweier Bildzustände.
- **Markieren im Bild:** Klickbare Hotspots oder Markierungen auf einem Bild oder Screenshot.
- **Matrix:** Tabellarischer Kriterien- und Bewertungsvergleich mehrerer Optionen.

## 5. Antwortschema `ticket-master.decision-answers.v1`

Eine JSON-Datei. Pflichtfelder (der Validator `validate_answers()` in `build_form.py` ist maßgeblich):

| Feld | Inhalt |
|---|---|
| `schema` | `ticket-master.decision-answers.v1` |
| `document_id` | Kennung des Dokuments |
| `document_sha256` | SHA-256 des unveränderten Formulars, in dem der eingebettete Hash durch 64 Nullen ersetzt ist (damit die Antwort an genau diese Fassung gebunden ist) |
| `saved_at` | UTC, ISO 8601 |
| `answers` | je Kürzel: `choice` (Optionskennung, `"rueckfrage"` oder `null`), `choice_label`, `state` (`answered`, `question` oder `open`), `note`, `via` (`single` oder `bulk`), `recommended`, `avatar_prediction`, `avatar_confidence`, `marked`; bei `bilder_modus == "swipe"` zusätzlich `swipe_decisions` (Liste der Einzelentscheidungen) und `swipe_confirmed` (`true`/`false`) |
| `bulk_actions` | welche Massenaktionen ausgelöst wurden |
| `gesamtabnahme` | `explicit` (nur `true` nach ausdrücklichem „Ja“ im Dialog, alle Posten wie empfohlen **und** keine Rückfrage), `at` |
| `counts` | `total`, `answered`, `questions`, `open` (müssen zu `answers` passen; ältere Dateien ohne `questions` bleiben gültig) |
| `agpl_bleibt` | Besonderheit des Referenzdokuments vom 2026-11-07, sonst nicht vorhanden |
| `draft` | nur im Zwischenstand (Knopf „Zwischenstand sichern“): `true`; sonst fehlt das Feld |

Offene Posten bleiben `open`; eine Teilantwort ist **keine** Gesamtabnahme.

## 6. Pflichtregeln (aus dem Vorfall vom 2026-11-07 und dem ersten Einsatz)

Jede Regel hat einen Grund; wer ein Formular baut, hält alle ein.

1. **Nichts vorausgewählt** (oder ausdrücklich als vorausgewählt gekennzeichnet). Eine Vorbelegung wirkt sonst wie ein Selbstausfüllen: Die Antwort stammt dann vom Schreiber, nicht von der Nutzerin oder dem Nutzer. Im Tk-Weg dafür `"preselect": "none"`.
2. **Gesamtabnahme nur nach ausdrücklichem „Ja“ im Dokument-Dialog** (kein Browser-`alert`, sondern ein Dialog im Dokument). Sie gilt, solange alle Posten wie empfohlen stehen und keine Rückfrage offen ist, und wird zurückgenommen, sobald danach ein Posten selbst geändert wird.
3. **Bei Wiederherstellung (Zwischenstand aus `localStorage`) nie die Gesamtabnahme übernehmen.** Ein früherer Stand darf eine neue ausdrückliche Bestätigung nicht ersetzen. Das Formular weist darauf hin.
4. **Sensible Posten vor dem Speichern auflisten:** rot (Avatar ohne Vorhersage), Geld, Löschung, Außenwirkung, Lizenz, Rechte Dritter, Veröffentlichung. Massenaktionen nennen sie ausdrücklich, bevor sie angenommen werden. Rückfragen werden ebenfalls vor dem Speichern gelistet.
5. **UI-Tests nur headless und nie über sichtbare Browser oder die Playwright-MCP-Werkzeuge.** Vorfall: Ein sichtbarer Test-Browser auf dem Rechner der Nutzerin oder des Nutzers füllte das Formular selbst aus. Zulässig ist ausschließlich Python-Playwright mit `headless=True`, eigenem Temp-Profil und Download-Fallback (`scripts/formular/headless_util.py`). Fixtures aus solchen Läufen sind **Testdaten, keine Nutzerentscheidung** und werden entsprechend gekennzeichnet.
6. **Zustellung erst nach unabhängiger Prüfung** durch eine andere Instanz (Hash, Posten gegen die Daten, nichts vorausgewählt, Roundtrip der Antwortdatei, Headless-Wiederherstellung, simulierte Speicher-Ausfälle).
7. **Buchung nur über `decision-briefing` Phase 4.** Das Formular, der Generator und der Viewer besitzen keinen eigenen Schreibweg ins Register.
8. **Messung gegen eine versiegelte Avatar-Prognose (optional):** Die Prognose wird vor der Zustellung mit UTC-Zeit und SHA-256 versiegelt, im Formular als Avatar-Wahl und Konfidenz je Posten angezeigt und nach der Antwort ausgewertet. Antwortdatei und Siegel werden nicht vermischt; die Empfehlung des Schreibers ist ein dritter Vergleichsarm.
9. **Speichern hängt nie von einem Dialog ab.** Jeder Weg über einen Browser-Dialog (Ordnerwahl, Dateispeichern) kann abgebrochen werden oder scheitern (`AbortError`, `SecurityError`, `NotAllowedError`, gesperrte Systemordner, blockierte Mehrfach-Downloads). Vorfall: Nach einem Abbruch der Ordnerwahl zeigte das Formular nur „abgebrochen“ und bot nichts mehr an; der Stand war nur durch eine Rettung gesichert. Deshalb:
   - Das **Sicherungsnetz steht, bevor ein Dialog aufgeht**: ein sichtbarer Bereich mit „Als Datei herunterladen“, „Antwort als Text kopieren“ und „Zwischenstand sichern“, dazu je Datei ein eigener Download-Link. Nach jedem Abbruch oder Fehler bleibt er unverändert stehen.
   - **Kein Download startet von allein.** Jeder Download ist eine eigene Nutzergeste (Link oder Knopf); es gibt keine zeitversetzten programmatischen Klicks, die ein Browser als Mehrfach-Download blockieren kann. Die Antwortdatei ist nötig, die beantwortete Kopie optional.
   - **Antwort als Text:** ein Textfeld mit dem vollständigen JSON, markiert, mit Kopierknopf. Fehlt die Zwischenablage oder wird sie verweigert, bleibt das Feld zum manuellen Kopieren stehen und das Formular sagt es.
   - **Zwischenstand jederzeit sichern** (Datei, `draft: true`, ohne Gesamtabnahme, solange sie nicht bestätigt wurde); `localStorage` ist nur eine Bequemlichkeit, keine Sicherung.
   - **Keine falsche Erfolgsmeldung:** „Gespeichert in …“ steht erst, nachdem alle Dateien im Ordner vollständig geschlossen sind. Nach einem Download heißt es „Download angestoßen“ mit dem Hinweis, dass die Seite den Eingang nicht prüfen kann. Jeder Fehler nennt seinen Namen und den nächsten Schritt in Du-Form; auch der Bau der Kopie und der Antwort sind abgefangen, kein Fehler bleibt unsichtbar. Scheitert nur die Kopie, bleibt die Antwortdatei verfügbar.
   - Kein `startIn` beim Ordnerdialog (Browser sperren Systemordner wie „Dokumente“); der gewünschte Ordner (`zielordner`) wird im Dokument genannt, mit dem Hinweis, dass der Browser ihn eventuell nicht zulässt. Der Download ist der normale Weg, wenn der Ordner nicht geht.
   - Ein **Headless-Test simuliert** Ordnerwahl-Abbruch, `SecurityError`, Schreibfehler bei der zweiten Datei, späten `close()`, fehlende Ordner-API, blockierten Download, fehlende und verweigerte Zwischenablage, einen Fehler beim Bau der Kopie und den Zwischenstand und prüft jedes Mal: Knopf sichtbar, Text gültig, keine falsche Erfolgsmeldung.
10. **Kurz und entscheidungsrelevant:** Die Postenvorlage (Abschnitt 4) nicht umgehen. Längeres nur aufklappbar; ein Generator, der Grenzen still kürzt oder Pflichtfelder auffüllt, ist falsch.

## 7. Prüfen

Im Ordner `scripts/formular/`, ohne Umgebungsvariablen:

```
python -m unittest selbsttest_form -v
```

- **`Daten`** (ohne Browser): Beispiel baut byte-stabil (Hash reproduzierbar), Längengrenzen sind Fehler und genau am Limit erlaubt, Pflichtfelder (auch mit „keine“), Empfehlung und Optionen, Bilder (Größe, Typ, Beschriftung, Gesamtgröße, Pfad), `details_markdown` escaped und Linkschemata nach der Positivliste geprüft (Nutzlasten der Prüfung von #98), `<` in eingebetteten Daten nie roh, nichts vorausgewählt, kein Netz, Schema und Generator im Gleichschritt (`form.schema.json`), Sicherungsbereich statisch vorhanden, Validator kennt die Rückfrage.
- **`HeadlessSaveTemplate`** (Regel 9, headless): die gemeinsamen Tests aus `savetests.py` am Template (Abbruch, `SecurityError`, Schreibfehler, später `close()`, Download-Weg, blockierter Download, Zwischenablage, Fehler beim Bau der Kopie, Zwischenstand).
- **`HeadlessTemplate`** (headless): Rückfrage als eigener Zustand (zählt nie als beantwortet, blockiert die Gesamtabnahme, wird im Dialog gelistet), Bilderserie über den Entscheidungsfeldern, Fakten sichtbar, Details zugeklappt.
- Die Browserklassen brauchen Python-Playwright und Edge und laufen sonst nicht. **Nie sichtbar, nie über die Playwright-MCP-Werkzeuge (Regel 5).** Die Dateien heißen nicht `test_*.py`, damit die Suite dieses Repos sie nicht einsammelt.
- **Beispielmigration:** `FORMULAR_MD=<DOKUMENT.md> [FORMULAR_MESSUNG=<Messdatei.md>] python -m unittest selbsttest_markdown -v` prüft den alten Dokumentgenerator gegen das Dokument vom 2026-11-07 (Hash, Posten, Wiederherstellung, Regel 9 über denselben Mixin).
- **Fixtures** (`testdata/`) gehören nur zum alten Dokumentgenerator und sind nicht Teil des Skills. `make_fixtures.py` erzeugt Test-Fixtures über den Regel-9-Sicherungsbereich (wartet auf `#save-links a` und liest die Blob-Inhalte aus); den allgemeinen Speicherweg prüfen `HeadlessSaveTemplate` und `HeadlessSicherheit` am allgemeinen Formular.
- **Weg B:** `python scripts/decision_viewer.py validate <draw.json>` ist headless; gezielte Tests in `testing/test_decision_draw_viewer.py`.

## 8. Weg B: Draw als `draw.json` abbilden

Wer den Tk-Viewer nutzt (erst nach Zustimmung, siehe Status oben), bildet das Dokument so ab:

- jeder Posten und jede Untersache wird ein Ast mit eigener `id` (das Kürzel), Klartexttitel und Text; Quelle, Alternativen und Adressat stehen in `source_ref`, `alternatives_ref`, `addressee`;
- rote, Geld-, Lösch-, Außen-, Lizenz- und Rechte-Dritter-Posten erhalten `"sensitive": true`;
- soll jede Entscheidung selbst getroffen werden (besonders bei den sensiblen Posten), `"preselect": "none"` setzen;
- reale fachliche Voraussetzungen kommen in `depends_on`, nicht in die Baumstruktur;
- danach `validate`, öffnen, Ergebnis mit `read` lesen, vor jedem externen Effekt `claim`, nach der Phase-4-Buchung `processed` (Einzelheiten in [viewer.md](viewer.md)).

Ein Generator für diesen Weg gehört nicht zum Skill; `references/example.json` zeigt das Format.
