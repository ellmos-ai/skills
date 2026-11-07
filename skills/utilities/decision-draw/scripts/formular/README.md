# Formular-Generator für Entscheidungsdokumente (Referenzimplementierung)

Aus einem fertigen Entscheidungsdokument (Markdown, siehe [Bauanleitung](../../references/formular.md)) entsteht **eine** selbstenthaltene HTML-Datei: kein Netz, keine externen Skripte oder Fonts, hell und dunkel, handytauglich. Alle Posten werden direkt angeklickt. Die Texte des Dokuments bleiben unverändert; es kommen nur Formularelemente hinzu.

Dies ist die eingefrorene Referenz aus der Praxis vom 2026-11-07. Sie ist an das damalige Dokument gebunden (Dokumentkennung, ein Vorab-Block im ersten Bündel, zwei Untersachen mit geerbter Markierung). Welche Stellen für ein neues Dokument anzupassen sind, steht in der [Bauanleitung](../../references/formular.md), Abschnitt „Für ein neues Dokument anpassen“.

| Datei | Zweck |
|---|---|
| `build_formular.py` | Generator und Antwort-Validator (`validate_answers()`) |
| `formular.js`, `formular.css` | eingebettetes Verhalten und Aussehen; der Generator liest beide |
| `selbsttest_formular.py` | Referenz-Selbsttest, gebunden an das Dokument vom 2026-11-07 |
| `headless_util.py`, `make_fixtures.py` | Hilfen für die Browser-Fixtures; **nur headless** |

## Aufruf

```
pip install markdown
python build_formular.py --md <DOKUMENT.md> --out <DOKUMENT_FORMULAR.html>
```

Der Generator liest nur das Markdown-Dokument und schreibt nur die HTML-Datei. Er berührt weder Register noch Tickets.

## Selbsttest

```
FORMULAR_MD=<DOKUMENT.md> [FORMULAR_MESSUNG=<versiegelte Messdatei.md>] python -m unittest selbsttest_formular -v
```

`FORMULAR_MD` ist Pflicht (keine Vorbelegung). Die Datei heißt bewusst nicht `test_*.py`, damit die Test-Suite dieses Repos sie nicht einsammelt: Sie braucht die Originaldaten des Dokuments von 2026-11-07. Die Klasse `Answers` braucht den Ordner `testdata/` (Browser-Fixtures, hier nicht enthalten, mit `make_fixtures.py` erzeugbar) und wird sonst übersprungen. Die Klasse `HeadlessRestore` startet einen Browser und läuft nur, wenn Python-Playwright und Edge vorhanden sind.

**Browsertests ausschließlich headless** (`headless_util.py`: eigenes Temp-Profil, `headless=True` fest verdrahtet). Nie ein sichtbares Browserfenster und nie die Playwright-MCP-Werkzeuge des Agenten verwenden: Dort öffnet sich ein sichtbarer Browser auf dem Rechner der Nutzerin oder des Nutzers, und ein Agent kann das Formular damit selbst ausfüllen (genau das ist am 2026-11-07 passiert).

## Bedienung (Verhalten des Formulars)

- Nichts ist vorausgewählt. Je Posten eine Option und eine optionale Anmerkung.
- Massenaktionen („Alle wie empfohlen“ je Bündel, „Alles wie empfohlen“ oben) fragen im Dokument nach und setzen nur Posten mit Empfehlung. Markierte Posten werden mit genannt und vor dem Speichern noch einmal aufgelistet.
- Eine Gesamtabnahme gilt nur nach ausdrücklichem „Ja“ im Dialog und solange alle Posten wie empfohlen stehen. Ändert die Nutzerin oder der Nutzer danach einen Posten selbst, wird sie zurückgenommen. Bei einer Wiederherstellung aus dem Zwischenstand wird eine frühere Gesamtabnahme **nie** übernommen.
- „Speichern und abschicken“ erzeugt die Antwortdatei (`ticket-master.decision-answers.v1`) und eine schreibgeschützte Kopie des Dokuments mit den eingebetteten Entscheidungen. `document_sha256` ist der SHA-256 des unveränderten Formulars, in dem der eingebettete Hash durch 64 Nullen ersetzt ist.
- Speichern: Ordnerwahl per File System Access API (Chromium, Edge), sonst Download. Der Zwischenstand liegt in `localStorage` (mit `try/catch`; die Seite funktioniert auch ohne). Der Browser kann keine Nachricht senden: Die Nutzerin oder der Nutzer sagt dem Konsumenten Bescheid, der die Datei liest und über `decision-briefing` Phase 4 bucht.
