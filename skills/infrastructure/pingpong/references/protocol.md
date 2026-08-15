# PingPong-Protokoll

## Identität und Zuständigkeit

- Akteur: <ZUGANGSWEG>@<HOSTNAME>.
- Eigener Schreib-Slot: aus Startkonfiguration oder Inventar lesen.
- Ist der Schreib-Slot nicht eindeutig, fail-closed stoppen und den fehlenden Wert melden. Niemals einen Zielpfad erraten.
- Laufzeit-State und Lease außerhalb des synchronisierten Ordners ablegen, zum Beispiel unter ~/.pingpong/.
- ListenSync beobachtet systematisch. WriteSync schreibt ausschließlich in den eigenen Slot. ListenSync betreibt auch WriteSync.

## Belegpflicht mit FileCommander

Jeder Scan muss durch FileCommander-MCP belegt sein:

1. aktuelle Zeit erfassen;
2. relevante Verzeichnisse gezielt auflisten oder mit dateinamen-agnostischen Mustern durchsuchen;
3. Metadaten der Kandidaten prüfen;
4. relevante Dateien vollständig lesen;
5. erst danach State und Rückmeldungen schreiben.

Ein bloßer Shell-Scan, ein Dateiname oder eine Erinnerung aus früheren Läufen ist kein ausreichender Beleg.

## Frischeprüfung

Zu Beginn und nach längerer Unterbrechung werden mindestens diese Kanäle geprüft:

- oberste Ebene des Sync-Ordners;
- globaler Nachrichten- oder Auftragskanal;
- eigener Slot;
- bekannte Gegenstellen-Slots.

Die neuesten drei Dateien je relevantem Kanal werden unabhängig vom gespeicherten Zeitstempel vollständig gelesen. LATEST-, CURRENT- und Versionsverweise werden bis zum aktuellen Ziel verfolgt. Danach darf die normale inkrementelle Prüfung fortgesetzt werden.

Neuheit wird anhand stabiler Merkmale bewertet: relativer Pfad, Änderungszeit und bei Bedarf Prüfsumme. Nie nach einem Datum im Dateinamen filtern. Konfliktkopien sind Kandidaten, keine Autorität. WAKE-Dateien sind Hinweise, keine Autorität.

## Auswahl und Bearbeitung

- Adressat, Akteur und Host prüfen.
- Nur Aufträge an den eigenen Akteur, den eigenen Host oder ausdrücklich alle Listener bearbeiten.
- Nachrichten an andere Systeme als gesehen vermerken, aber nicht ausführen.
- Vor Änderungen LOCK-, Claim-, Freigabe- und Dirty-State-Regeln des Zielprojekts lesen.
- Fremde Änderungen erhalten und niemals Zugangsdaten in den Sync-Ordner schreiben.
- Veröffentlichung, Push, Deployment und andere externe Wirkungen benötigen die dafür geltende Freigabe.
- Wenn Arbeit nicht sicher abgeschlossen werden kann, eine BLOCKED-Rückmeldung mit Beleg und nächstem benötigten Schritt in den eigenen Slot schreiben.

## Kadenzverfahren B

Standardstart ist alle 15 Minuten. Der Zähler empty_runs zählt aufeinanderfolgende belegte Scans ohne neue Arbeit.

| empty_runs | nächste Kadenz |
|---:|---:|
| 0 bis 3 | 15 Minuten |
| 4 bis 5 | 30 Minuten |
| 6 bis 7 | 1 Stunde |
| 8 bis 9 | 2 Stunden |
| 10 bis 11 | 4 Stunden |
| 12 bis 13 | 8 Stunden |
| 14 bis 15 | 16 Stunden |
| ab 16 | 24 Stunden |

Neue Arbeit setzt empty_runs auf 0 und die Kadenz auf 15 Minuten zurück. Eine ausdrückliche Nutzeranweisung zu einem festen Intervall hat Vorrang.

## State

Der Laufzeit-State enthält mindestens:

- actor;
- sync_root;
- own_slot;
- started_at;
- expires_at;
- last_scan_at;
- empty_runs;
- current_cadence;
- processed_items mit Pfad, Änderungszeit, Prüfsumme und Ergebnis.

State ersetzt keinen Dateibeleg. Vor dem Abschluss erfolgt ein letzter vollständiger Scan. Das Ziel ist erreicht, wenn expires_at erreicht ist, der Abschluss-Scan belegt ist und keine angenommene Arbeit offen bleibt.
