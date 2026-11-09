# Formular-Template für Entscheidungsdokumente

Aus einer kleinen Daten-JSON entsteht **eine** selbstenthaltene HTML-Datei: kein Netz, keine externen Skripte oder Fonts, hell und dunkel, handytauglich. Alle Posten werden direkt angeklickt. Das Formular wird **nicht jedes Mal neu gebaut**: Daten schreiben, `build_form.py` aufrufen. Die vollständige [Bauanleitung](../../references/formular.md) beschreibt die Postenvorlage, das Antwortschema und die Pflichtregeln.

| Datei | Zweck |
|---|---|
| `formular.html` | Template mit Platzhaltern (`{{TITLE}}`, `{{BUNDLES}}`, …) |
| `form.schema.json` | Datenschema (Postenvorlage mit Längengrenzen und Pflichtfeldern) |
| `example_form.json` | Beispiel mit drei Posten, einer Bilderserie, einem Geld-Posten und aufklappbaren Details |
| `build_form.py` | Generator `<daten.json> -> .html` und Antwort-Validator (`validate_answers()`) |
| `formular.js`, `formular.css`, `form_base.css` | Verhalten und Aussehen; der Generator bettet sie ein |
| `savetests.py` | gemeinsame Headless-Tests für Regel 9 (Speichern hängt nie von einem Dialog ab) |
| `selbsttest_form.py` | Selbsttest des Templates (keine Umgebungsvariablen nötig) |
| `headless_util.py`, `make_fixtures.py` | Hilfen für Browsertests; **nur headless**. `make_fixtures.py` erzeugt Test-Fixtures über den Regel-9-Sicherungsbereich |
| `build_from_markdown.py`, `selbsttest_markdown.py` | frühere Fassung: Gesamtdokument (Markdown) vom 2026-11-07 -> Formular. Nur noch Beispielmigration |

## Aufruf

```
pip install markdown                       # nur nötig, wenn ein Posten details_markdown hat
python build_form.py <daten.json> --out <formular.html>
```

Der Generator liest nur die Daten-JSON (und Bilddateien, falls `pfad` genutzt wird) und schreibt nur die HTML-Datei. Er berührt weder Register noch Tickets. Fehler in den Daten (Pflichtfeld fehlt, Text über der Längengrenze, Bild zu groß, unbekanntes Feld) werden **alle auf einmal** mit Posten und Feld gemeldet; nichts wird still gekürzt.

## Selbsttest

```
python -m unittest selbsttest_form -v
```

`Daten` läuft ohne Browser. `HeadlessSaveTemplate` (Regel 9: simulierte Ausfälle beim Speichern) und `HeadlessTemplate` (Rückfrage, Bilderserie, Details) starten einen Browser und laufen nur, wenn Python-Playwright und Edge vorhanden sind. Die Dateien heißen bewusst nicht `test_*.py`, damit die Test-Suite dieses Repos sie nicht einsammelt.

**Browsertests ausschließlich headless** (`headless_util.py`: eigenes Temp-Profil, `headless=True` fest verdrahtet). Nie ein sichtbares Browserfenster und nie die Playwright-MCP-Werkzeuge des Agenten verwenden: Dort öffnet sich ein sichtbarer Browser auf dem Rechner der Nutzerin oder des Nutzers, und ein Agent kann das Formular damit selbst ausfüllen (genau das ist am 2026-11-07 passiert).

Der frühere Dokumentgenerator wird so geprüft (an das Dokument vom 2026-11-07 gebunden):
`FORMULAR_MD=<DOKUMENT.md> [FORMULAR_MESSUNG=<versiegelte Messdatei.md>] python -m unittest selbsttest_markdown -v`. Die Klasse `Answers` braucht Browser-Fixtures in `testdata/` (hier nicht enthalten) und wird sonst übersprungen. `make_fixtures.py` erzeugt solche Fixtures über den Regel-9-Sicherungsbereich (wartet auf `#save-links a` und liest die Blob-Inhalte aus); den Speicherweg prüfen `HeadlessSaveTemplate` und `HeadlessSicherheit` am allgemeinen Formular.

## Bedienung (Verhalten des Formulars)

- Nichts ist vorausgewählt. Je Posten eine Option oder „Rückfrage / mehr Info nötig“ und eine optionale Anmerkung (bei einer Rückfrage ist sie die Frage).
- **Bild-Modi je nach Entscheidungsart:**
  - `serie` (Standard, 1–12 Bilder): Klassische Bilderserie nebeneinander über den Optionen.
  - `polaroid` (2–12 Bilder, genau ein Bild je Option): Große Kennbuchstaben (A, B, C...), Polaroid-Karten synchron zu den Optionen, wählbar per Klick oder Tastendruck (A/B/C).
  - `swipe` (1–60 Bilder): Stapel-Durchsicht Bild für Bild (Ja/Nein/Rückfrage per Button, Wischgeste oder Pfeiltasten). Erst nach Klick auf „Einzelentscheidungen bestätigen“ zählt der Posten als entschieden.
- Avatar-Vorhersage: Das Vorhersage-Badge erscheint erst, **nachdem** die Nutzerin oder der Nutzer eine Wahl getroffen hat (kein vorbereitender Anker).
- Massenaktionen („Alle wie empfohlen“ je Bündel, „Alles wie empfohlen“ oben) fragen im Dokument nach und setzen nur Posten mit Empfehlung. Markierte Posten werden mit genannt und vor dem Speichern noch einmal aufgelistet, Rückfragen ebenso.
- Eine Gesamtabnahme gilt nur nach ausdrücklichem „Ja“ im Dialog, solange alle Posten wie empfohlen stehen und keine Rückfrage offen ist. Ändert die Nutzerin oder der Nutzer danach einen Posten selbst, wird sie zurückgenommen. Bei einer Wiederherstellung aus dem Zwischenstand wird eine frühere Gesamtabnahme **nie** übernommen.
- Speichern hängt nie von einem Dialog ab (Regel 9): Vor dem Ordnerdialog stehen schon die Download-Links (je Datei ein eigener Klick, nichts startet von allein), der Text der Antwort zum Kopieren und der Knopf „Zwischenstand sichern“. „Gespeichert in …“ erscheint erst, wenn alle Dateien im Ordner vollständig geschlossen sind; nach einem Download heißt es „Download angestoßen“ (die Seite kann den Eingang nicht prüfen). Abbruch und Fehler (`AbortError`, `SecurityError`, …) werden mit Namen und nächstem Schritt gemeldet.
- Die Antwortdatei (`ticket-master.decision-answers.v1`) und eine schreibgeschützte Kopie des Dokuments mit den eingebetteten Entscheidungen entstehen beim Speichern. `document_sha256` ist der SHA-256 des unveränderten Formulars, in dem der eingebettete Hash durch 64 Nullen ersetzt ist. Der Browser kann keine Nachricht senden: Die Nutzerin oder der Nutzer sagt dem Konsumenten Bescheid, der die Datei liest und über `decision-briefing` Phase 4 bucht.
