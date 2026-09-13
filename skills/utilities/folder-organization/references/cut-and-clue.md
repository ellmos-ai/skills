# Cut-and-Clue

Cut-and-Clue trennt gültige Substanz von überholtem Kontext, ohne die Herkunft unsichtbar zu machen.

## Wann anwenden

- Eine Datei enthält zugleich weiterhin gültige und klar überholte Abschnitte.
- Mehrere historische Dateien bilden eine erkennbare Vorgänger-/Nachfolgerreihe.
- Eine fehlerhafte Altfassung muss aus Nachvollziehbarkeits- oder Beweisgründen erhalten bleiben.
- Ein Indexer oder späteres Modell soll einen alten Fund nicht irrtümlich als aktuelle Wahrheit lesen.

Nicht anwenden, wenn die Gültigkeit fachlich ungeklärt ist. Dann Review statt Umschreiben. Ebenso
nicht auf geheimnisverdächtige Dateien anwenden: keine Werte in neue kanonische Dokumente, Clues,
Sidecars oder Manifeste kopieren. Zuerst die
[`Geheimnis-Policy`](secrets-policy.md) abschließen.

## Verfahren

1. Original hashen und als byteidentische Beweiskopie in einem geschützten Archiv-Unterordner
   sichern; alle eingehenden Verweise erfassen. Diese Beweiskopie wird nie kommentiert oder
   anderweitig verändert.
2. Gültige Aussagen abschnittsweise markieren. Unique Inhalte dürfen nicht verschwinden.
3. Neue kanonische Datei(en) nach bestehender Taxonomie schreiben. Inhalt so nah wie möglich
   übernehmen; keine stillen Claim-Upgrades oder Bedeutungsänderungen.
4. Vollständigkeit prüfen: jeder gültige markierte Abschnitt hat ein Ziel oder eine begründete
   Verwerfung. Links, Quellen und Anhänge bleiben verbunden.
5. Clues in die noch aktive Arbeitskopie oder in eine getrennt benannte, annotierte Archivkopie
   einfügen. Die byteidentische Beweiskopie aus Schritt 1 bleibt unverändert. Für beweisrelevante,
   freigegebene oder signierte Dateien grundsätzlich eine Sidecar-Datei verwenden. Manifest und
   Bericht unterscheiden Originalhash und Hash der annotierten Ableitung.
6. Verweise auf die kanonische Fassung umstellen. Historische Verweise dürfen weiterhin auf das
   Archiv zeigen, müssen aber den Status erkennen lassen.

## Dokument-Clue

Für Formate mit Kommentaren:

```markdown
<!-- CLUE
status: superseded
replaced-by: ../active/current-document.md
reason: Valid content was consolidated; remaining statements are historical.
reviewed: 2026-08-24
-->
```

Wenn der Hinweis sichtbar sein muss oder Kommentare vom Reader entfernt werden:

```markdown
> [!WARNING]
> SUPERSEDED: Diese Datei ist historisch. Gültiger Nachfolger: `../active/current-document.md`.
```

Relative Pfade bevorzugen. Datum ist das tatsächliche Prüfdatum. Keine Personennamen oder
hostgebundenen Pfade in einem portablen Dokument hinterlassen.

## Lokaler Clue an einer Problemstelle

```markdown
<!-- OUTDATED: Seit Version 3 nicht mehr gültig. Siehe current-policy.md#regel-x. -->
Der alte Ablauf verwendete ...
```

oder direkt danach:

```markdown
Der alte Ablauf verwendete ...
<!-- SUPERSEDED-BY: current-policy.md#regel-x -->
```

Für Quellcode die native Kommentarsyntax verwenden. Kommentare müssen so nah an der Stelle stehen,
dass ein Chunker oder Indexer Hinweis und problematischen Text gemeinsam erfasst.

## `[sic]` richtig verwenden

`[sic]` bedeutet: „Der Fehler steht bewusst so im zitierten Original.“ Es ist kein allgemeines
Kennzeichen für veraltete Inhalte. Deshalb:

- fehlerhafte historische Schreibweise im Zitat: `Fehler [sic]`;
- fachlich überholte Behauptung: `OUTDATED`/`SUPERSEDED` plus Nachfolger und Grund;
- aktuell ungeklärter Verdacht: `REVIEW-REQUIRED`, nicht `sic`.

## Binärdateien und unveränderbare Artefakte

PDFs, Bilder, signierte Dateien oder Releases nicht für einen Kommentar verändern. Daneben eine
Sidecar-Datei `<dateiname>.clue.md` anlegen und im Archivmanifest darauf verweisen. Ein signiertes
oder freigegebenes Artefakt bleibt byteidentisch.

## Archiv und Papierkorb

- Historisch wertvoll oder als Vorgänger belegt: Archiv.
- Wahrscheinlich entbehrlich, aber nicht sicher: `_trash_review/<run-id>/`.
- Kein gültiger Nachfolger, unvollständige Extraktion oder ungeklärte Referenz: nicht bewegen.

Ein Archiv ist keine Müllhalde. Es braucht Statushinweis, Ursprungsort, Nachfolger und Hash im
Manifest, damit Modelle und Menschen Geschichte von aktueller Wahrheit unterscheiden können.
