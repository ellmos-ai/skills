# Heuristiken und Grounding Seeds

Diese Referenz nur lesen, wenn Regeln fehlen, Dateien mehrdeutig sind oder aus einem manuellen Lauf
eine wiederkehrende Regel abgeleitet werden soll.

## Evidenzreihenfolge

Von stark nach schwach:

1. ausdrückliche lokale Policy, Manifest, Register oder Nutzerentscheidung;
2. dokumentierter Projektzweck und bestehende, tatsächlich verwendete Taxonomie;
3. Inhalt und Metadaten der Datei;
4. Beziehungen zu anderen Dateien und eingehende/ausgehende Verweise;
5. stabile Namens-, Versions- oder Datumsserie;
6. Dateiname und Endung;
7. Änderungszeit allein.

Schwache Evidenz darf Suche und Gruppierung auslösen, aber keine irreversible Entscheidung.

## Rollenschema

| Rolle | Typische Indizien | Default |
|---|---|---|
| control | README, Regeln, Manifeste, Register, Konfiguration | Root bzw. vorgeschriebener Ort |
| source | Rohdaten, editierbare Quelle, Original | Quellenbereich; nicht durch Export ersetzen |
| canonical | aktuell gültige Fassung | aktiver Fachordner |
| derivative | PDF, Build, Export, Vorschaubild | neben Quelle oder Ausgabeordner |
| evidence | Audit, Receipt, Beweislog, freigegebener Stand | unveränderlich erhalten |
| predecessor | belegte frühere Fassung mit Nachfolger | Archivkandidat |
| active-log | wird noch geschrieben oder aktueller Lauf | nicht bewegen |
| rotated-log | abgeschlossener Verlauf außerhalb Retention | Logarchivkandidat |
| duplicate | gleicher Hash, aber Bedeutung/Referenzen noch prüfen | Review, nicht löschen |
| unknown | unlesbar oder widersprüchlich | Entscheidungsliste |

## Konfidenz

Ein mögliches, nicht verpflichtendes Punktmodell:

- +4 explizite Regel oder Manifest;
- +3 eindeutiger interner Titel/Zweck;
- +2 mindestens zwei passende Beziehungssignale;
- +2 eindeutiger Vorgänger plus gültiger Nachfolger;
- +1 stabiles Namensmuster;
- -3 widersprechender Verweis oder zwei mögliche Ziele;
- -3 unlesbarer Inhalt bei semantischer Entscheidung;
- -4 Zielkollision oder Lock.

Ab 6 Punkten kann eine Entscheidung hoch, bei 3–5 mittel sein. Darunter bleibt sie niedrig. Harte
Blocker werden nicht durch Punkte aufgehoben.

## Versionsreihen

Eine Reihe erst annehmen, wenn mindestens zwei Dateien denselben Zweck teilen und ein echtes
Versionssignal besitzen. Prüfe zusätzlich interne Versionsangabe, Inhaltsüberlappung und Verweise.
Wörter wie `final`, `neu`, `copy` oder ein neueres Änderungsdatum beweisen allein keinen Nachfolger.

Der aktuelle Stand kann eine ältere Versionsnummer tragen, wenn ein Branch oder Release gepflegt
wird. Daher die lokale Release-/Kanonikregel vor dem Archivieren lesen.

## Logs

- Prozesse oder offene Handles prüfen, soweit das System dies unterstützt.
- Audit-, Sicherheits- und Veröffentlichungslogs nicht wie Wegwerfdiagnostik behandeln.
- Retention als Konfiguration, nicht als universelle Zahl verwenden.
- Archivmanifest enthält ursprünglichen Pfad, Zeitraum, Hash, Grund und gegebenenfalls die
  zugehörige Ausführung.

## Aus Modulen abgeleitete sprachliche Regeln

Diese Regeln gelten auch ohne die Module:

- **Dry-Run-Fingerprint:** Ein Plan gilt nur für den inventarisierten Zustand und die verwendete
  Konfiguration. Änderungen entwerten seine Freigabe.
- **No-overwrite:** Ziel muss unmittelbar vor der Aktion frei sein.
- **Hashbindung:** Kritische Verschiebungen an den gelesenen Inhalt binden, nicht nur an Dateinamen.
- **Fail-closed:** Unlesbar, gesperrt, widersprüchlich oder außerhalb des Roots bedeutet Review.
- **Inhalt vor Name:** Extraktion/OCR nutzen, wenn die Bedeutung sonst nicht belastbar ist.
- **Datenschutz vor Egress:** Lokale Verarbeitung bevorzugen; externe Weitergabe separat freigeben.
- **Lernen als Vorschlag:** Korrekturen zählen und sichtbar machen, aber Regeln nicht still ändern.
- **Rollback nur für eigene Aktion:** Fremde oder zwischenzeitliche Änderungen nicht zurückrollen.
- **Checkpoint:** Nach einem Batch den neuen Bestand erneut inventarisieren.

## Geheimnisse vor Semantik

Die Geheimnis-Policy steht vor der Evidenzreihenfolge. Ein geschützter Name ist kein Auftrag zum
Öffnen, sondern ein Stoppsignal: nur Pfad/Metadaten erfassen und die Policy anwenden. Ein zufälliges
Inhaltssignal beendet weitere Inhaltsausgabe; der Bericht nennt nur die Signal-ID.

Cloud-Pfadmarker sind Verdachtsheuristik, kein Beweis. Eine Auslagerung braucht zusätzlich ein
konfiguriertes lokales Ziel außerhalb aller Sync-Roots, restriktive Berechtigungen, Freigabe,
opaken Kopier-/Hashnachweis, geprüfte Laufzeitreferenzen und einen nicht geheimen Pointer. Fehlt ein
Glied, bleibt die Aktion blockiert. Siehe [`secrets-policy.md`](secrets-policy.md).

## Optionale Capability-Erkennung

Vorhandene Fähigkeiten können unter beliebigen Namen auftreten. Suche nach:

- `plan + approval + receipt + undo` für sichere Ausführung;
- `extract + OCR + privacy gate` für Dokumente;
- `cloud lock + file operation` für synchronisierte Ordner;
- `scan + category + dry-run + config fingerprint` für wiederkehrende Regeln;
- `index/reindex` für CLUE-Markierungen.

Ellmos-Beispiele sind FolderHome, doc-services, FileCommander,
file-collect-sort-action und Gardener. Sie bleiben optional; die Capability ist entscheidend.

## Regelübergabe an Automation

Nur Kandidaten ausgeben, wenn Quelle, Erkennung, Ziel, Kollisionsmodus, Archiv-/Papierkorbpfad und
Ausnahmen bekannt sind. Mindestens ein erfolgreicher manueller Lauf und eine Nutzerbestätigung sind
erforderlich. Die erste Automation bleibt Dry-Run; jede Konfigurationsänderung entwertet die vorige
Freigabe.
