# Dateibasiertes Entscheidungsfenster

`python scripts/decision_viewer.py open /absolut/draw.json` öffnet ein eigenständiges natives Tk/ttk-Fenster. Der komplette Skillordner kann in eine frische Installation kopiert werden; Python 3.10+ mit Tk genügt. Kein BACH/Ocean, Browser, Server oder Drittanbieterpaket ist erforderlich. Ein neutrales Beispiel liegt in `example.json`, das Format in `draw.schema.json`.

Ein Draw enthält die sieben Konzeptteile in `parts`; die technische Anhangstabelle wird aus den Astreferenzen dargestellt. Das bewahrt die acht Teile des aktuellen Skills. `nodes/children` beschreiben ausschließlich die sichtbare Baumstruktur. Echte fachliche Voraussetzungen stehen separat in `depends_on`. Der Viewer ändert niemals heimlich die Auswahl abhängiger Äste. Klartext-Titel und Text gehören in den sichtbaren Bereich, IDs/Quellen/Alternativen/Adressaten in die technische Zuordnung. Zu jedem Ast bleiben Quelle und alternative Varianten erreichbar über den Button „Technische Quellen & Alternativen“; dort sind sie vollständig kopierbar.

Zustimmung ist zunächst für jeden Ast **als Entwurf** vorgewählt. Plus/Minus und aufklappbare, scrollbar vollständig bearbeitbare Kommentare ändern nur den lokalen Entwurf. Erst „Absenden / Entscheiden“ bestätigt ausdrücklich die Auswahl samt Kommentaren aller Äste. Diese GUI-Gesamteinreichung ist vom gewöhnlichen Korrektursatz zu unterscheiden: Außerhalb der GUI gilt weiterhin, dass eine Teilkorrektur keine stillschweigende Annahme unberührter Posten bedeutet. Kommentare in einer Gesamteinreichung können trotzdem Mehrdeutigkeiten enthalten; sie werden vor Buchung geklärt.

Absenden prüft Revision und Quellenhash unter einer exklusiven Dateisperre. Der Viewer veröffentlicht `draw_decided.json` kollisionsgeschützt und entfernt danach die unveränderte ursprüngliche Datei. Submission-ID, ursprünglicher Quellenhash, Quellrevision und gewählte Antworten bleiben im Ergebnis. Der kurze Mehrdateischritt ist **keine** atomare Dateisystemtransaktion: Nach einem Prozessabbruch können beide Namen existieren. Dann fail-closed stoppen und anhand IDs/Hashes auflösen. Keine zweite Registry entsteht.

Auf der Bestätigungsseite kann die eigene unveränderte, noch nicht verarbeitete Einreichung rückgängig gemacht werden. Das erzeugt wieder einen Entwurf mit steigender Revision, erhält Kommentare/Auswahl als `draft_choices` und vermerkt die Rücknahme mit Submission-ID im selben Dokument. Eine bereits vorhandene Quelldatei, Fremdänderung am Ergebnis oder begonnener Rücktransfer verhindert Undo. Ein externer Effekt wird niemals durch Dateiumbenennung zurückgedreht.

Gespeicherte `draft_choices` müssen exakt alle Ast-IDs enthalten. Jeder Wert hat
ausschließlich `accept` als echten Boolean und `comment` als Text. Fehlende,
zusätzliche oder falsch typisierte Auswahlfelder werden vor dem Fensteraufbau
abgelehnt. Das allgemeine JSON-Schema prüft Form und Typen; die vom konkreten
Dokument abhängige exakte ID-Abdeckung prüft die Runtime zusätzlich, da Standard-
JSON-Schema keine dynamische Gleichheit mit den IDs einer anderen Stelle beschreibt.

Der Button „Übergabeprompt kopieren“ prüft die Ergebnisdatei frisch. Er kopiert Draw-ID, Submission-ID, Hash und den absoluten Pfad samt Anweisung zum kanonischen Rücktransfer. Es wird kein Shellbefehl aus JSON/Kommentaren ausgeführt und kein Register beschrieben.

## Rücktransfer mit Verarbeitungssperre

```text
python scripts/decision_viewer.py read /absolut/draw_decided.json
python scripts/decision_viewer.py claim /absolut/draw_decided.json --sha256 <frischer-hash> --actor <consumer> --evidence-ref <plan-ref>
python scripts/decision_viewer.py processed /absolut/draw_decided.json --sha256 <hash-aus-claim> --actor <derselbe-consumer> --evidence-ref <phase4-buchungsbeleg>
```

Der Consumer muss **vor jedem externen Effekt** `claim` mit aktuellem Hash erfolgreich ausführen. Damit wird `processing` beansprucht, Revision/Hash steigen und Undo ist gesperrt. Nur derselbe Consumer kann anschließend `processed` buchen; er tut das erst nach bestätigter Phase-4-Buchung. Claim und Ergebnisflags sind Koordination dieser Datei, kein Ersatz für das Entscheidungsregister. Bei Fehler oder Absturz nach Claim wird über den bestehenden Phase-4-Prozess abgeglichen; der Viewer entsperrt nicht automatisch. Normale Nutzerkorrekturen weiterhin über die dort vorgeschriebene Rücktransfer-Tabelle behandeln.

Alle beteiligten Werkzeuge müssen denselben `.decision-lock` am ursprünglichen Dateinamen respektieren. Liegt ein Lockrest vor, erst den schreibenden Prozess und beide Dateien prüfen; nie automatisch stehlen. Die Hashprüfungen erkennen veraltete Preimages, ersetzen aber keine Kooperation beliebiger externer Editoren zwischen Prüfung und Ersetzen. Ein nicht kooperierender Editor darf die Dateien nicht parallel verändern.

Prüfen: `python scripts/decision_viewer.py validate references/example.json` ist headless. Die gezielten Tests in `testing/test_decision_draw_viewer.py` prüfen Submit/Undo, Fremdupdates, parallele Fenster, Kollisionen und Consumer-Fences. Mit `TM_NATIVE_UI_TEST=1` kommt ein tatsächlicher Tk-Smoke für Baum, Kommentare, Submit, Zwischenablage und Undo hinzu. Andere Betriebssysteme brauchen eigene native Abnahme.
