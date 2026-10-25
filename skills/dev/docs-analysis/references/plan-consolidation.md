# Plankonsolidierung / Dokument-Synopse

Aus mehreren Plan-, Status- und Übergabedokumenten einen aktuellen Plan mit offenen
Punkten erstellen. Belegbar erledigte Inhalte und vollständig abgelöste Quellen
archivieren; gültige Entscheidungen, Bedingungen und Abhängigkeiten bewahren.

## Einstieg und Zusammenarbeit

`folder-organization/SKILL.md` und dessen `references/cut-and-clue.md` über die
Skill-Suche oder den installierten Geschwisterordner laden. In der kategorisierten
Bibliothek liegt er unter `skills/utilities/folder-organization`. Dieser Skill
übernimmt Archivtransaktionen, Originalschutz, Clues, Referenzen und Readback;
`docs-analysis` entscheidet über Inhalt, Status und den konsolidierten Plan.
Fehlt der Skill, kann die Synopse als Entwurf entstehen; Archivierung bleibt offen,
bis die Abhängigkeit verfügbar ist. Keine zweite Archivierungslogik improvisieren.

Den genannten Ordner und ausdrücklich einbezogene Tickets/Register als Quellen
festlegen. Lokale Steuerdateien, Archivkonventionen und Sperren beachten. Steuerdateien,
aktive Laufzeitdateien, Geheimnisdateien und fremde Arbeitsbereiche sind keine pauschalen
Archivkandidaten. Bei einem reinen Analyseauftrag nur Entwurf und Archivplan liefern.
Ein ausdrücklicher Auftrag zum Konsolidieren und Archivieren autorisiert die nötigen
reversiblen Änderungen im genannten Bereich; bereits erteilte Freigaben nicht erneut
abfragen. Zusätzliche Register nur aktualisieren, wenn beauftragt oder lokal vorgesehen.

## Quellen und Status klären

Alle relevanten Dateien vollständig lesen, einschließlich Anlagen und referenzierter
Fortsetzungen, soweit für ihren Status nötig. Unlesbare oder unvollständig erfasste
Quellen als Lücke ausweisen und nicht archivieren. Neue Dateinamen oder Änderungszeiten
allein entscheiden weder über Gültigkeit noch über Erledigung.

Für jeden sachlich eigenen Punkt Quelle/Abschnitt, Status, Beleg und Ziel festhalten:

| Status | Behandlung |
|---|---|
| offen / teilweise erledigt | Restarbeit mit Abnahmekriterium in den aktuellen Plan |
| erledigt | Nur mit nachvollziehbarem Abschlussbeleg ins Erledigt-Archiv |
| abgelöst / verworfen | Entscheidung und Nachfolger nennen; nicht als erledigt zählen |
| unklar / widersprüchlich | Mit Klärungsbedarf und beiden Quellen im aktuellen Plan |

Ein Häkchen oder „fertig“ ohne prüfbare Grundlage ist zunächst ein berichteter Status.
Belege aufgabengerecht prüfen (z. B. Ergebnisdatei, Test, Release, Ticket-Abnahme);
fehlenden Nachweis nicht durch eigene Annahmen ersetzen. Bei Teilfortschritt Erreichtes
und Restarbeit trennen. Duplikate zusammenführen, aber alle Herkunftsstellen behalten.
Eine neuere Aussage verdrängt eine ältere nur bei sachlich belegter Ablösung.

## Aktuellen Plan schreiben

Bestehenden kanonischen Dateinamen und lokale Struktur bevorzugen; sonst etwa
`AKTUELLER-PLAN.md`. Im Kopf Stand, Quellumfang sowie direkte Vorgänger und deren
Archivpfade nennen. Ein bestehender Plan wird vor seiner Ablösung versioniert gesichert.

Der Plan enthält Ziel und weiterhin gültige Entscheidungen sowie alle offenen,
teilweise erledigten und ungeklärten Punkte. Pro Punkt: stabile ID, konkrete Restarbeit,
Priorität, Abhängigkeiten/Blocker, Abnahmekriterium und Quellen; Verantwortliche und
Fristen nur übernehmen, wenn belegt. Abschlusschronik ins Archiv auslagern und verlinken.
Aktive Voraussetzungen dürfen nicht mit abgeschlossenen Aufgaben verschwinden.

Für beauftragte Tickets/Register deren eigenen Workflow verwenden. IDs, Status,
Abhängigkeiten und aktuellen Inhalt vor dem Schreiben lesen. Bestehende Einträge
gezielt ergänzen, auf Plan/Belege verweisen und keine fremden Notizen überschreiben.
„Dokumente konsolidiert“ bedeutet nicht „Projekt/Ticket abgeschlossen“; offene Restarbeit
bleibt offen. Nicht beauftragte Einträge höchstens als Änderungsvorschlag aufnehmen.

## Archivieren und abnehmen

Vor Änderungen einen konkreten Quellen-Ziel-Plan zeigen. Jede Quelle erhält eine
begründete Aktion: behalten, vollständig abgelöst archivieren, gemischte Inhalte per
Cut-and-Clue trennen oder zur Klärung belassen. **Keine 75-Prozent-Regel:** Ein Dokument
mit offenen Punkten darf erst ins Archiv, wenn diese vollständig im aktuellen Plan
vertreten sind. „Alle übrigen Dokumente archivieren“ überstimmt keine Inhaltslücke.

Mit `folder-organization` byteidentische Originale, Hashes, Herkunft und Rückweg sichern.
Clues/Sidecars müssen auf den neuen Plan verweisen, ohne Beweisoriginale zu verändern.
Archivmanifest und gegebenenfalls Erledigt-Chronik unter der lokalen Archivstruktur
ablegen. Links, Anlagen und historische Belege funktionsfähig erhalten. Quellen, die
sich seit der Analyse geändert haben, erneut lesen, bevor sie ersetzt/verschoben werden.

Abnahme: Jeder Quellpunkt ist im aktiven Plan, im Erledigt-Archiv oder mit begründeter
Ablösung im Manifest nachweisbar; kein offener Punkt existiert nur im Archiv. Plan,
Archivdateien und aktualisierte Tickets unabhängig zurücklesen, Links und Originalhashes
prüfen. Beim erneuten Lauf vorhandene IDs und Zuordnungen weiterverwenden, ohne
Duplikate oder neue Archive unveränderter Quellen zu erzeugen.

Im Abschluss Planpfad, Archivpfad, Quellenabdeckung, aktualisierte Ticket-IDs und
ungeklärte/gesperrte Quellen nennen. Fehlgeschlagene Registerupdates ausdrücklich offen
lassen, statt einen vollständigen Abschluss zu behaupten.
