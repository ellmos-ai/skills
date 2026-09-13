# Geheimnis-Policy

Diese Policy greift vor Inhaltsanalyse, Hashing und semantischer Sortierung. Ihr Ziel ist nicht,
Geheimnisse vollständig zu finden, sondern zufällige Offenlegung und unsichere Cloud-Ablage
fail-closed zu behandeln.

## Unverhandelbare Invarianten

- Erkannte oder vermutete Geheimniswerte niemals in Prompt, Chat, Bericht, Manifest, Dateiname,
  Pointer, Log oder Fehlermeldung kopieren.
- Standardmäßig geschützte Namen wie `.env`, private Schlüssel und Credential-Dateien nur anhand
  von Pfad und Metadaten klassifizieren; nicht semantisch öffnen und nicht an ein Modell geben.
- `--hash-all` hebt diesen Schutz nicht auf.
- Ein Inhalts-Signal nennt nur seine Regel-ID, nie den Treffer oder Umgebungstext.
- Erkennung ist kein Beweis für ein echtes Geheimnis. Umgekehrt beweist ein unauffälliger Scan
  nicht, dass die Datei geheimnisfrei ist.

„Nicht öffnen“ bedeutet: Inhalt weder anzeigen noch semantisch lesen oder an ein Modell übertragen.
Eine ausdrücklich freigegebene Auslagerung darf die Datei als opaken Bytestrom kopieren und lokal
hashen, sofern Werkzeugausgaben keine Inhalte zeigen.

## Standarderkennung und Konfiguration

[`../config.json`](../config.json) enthält:

- geschützte Namensmuster und Ausschlüsse für Beispiel-/Template-Dateien;
- lokale, nur als Signal-ID ausgegebene Inhaltsregeln;
- konfigurierbare oder heuristisch erkennbare Cloud-Roots;
- `cloud_action`: `report-only`, `plan-localize` oder `localize-after-approval`;
- `local_secret_root` als zwingend lokal zu belegendes Ziel;
- `pointer_mode`: `control-file`, `sidecar` oder `placeholder`.

Ein projekt- oder laufbezogenes `--config` darf diese Werte überschreiben. Verschachtelte Blöcke
werden mit sicheren Defaults zusammengeführt. Nutzerpfade, Konten und Schlüssel gehören nicht in
die öffentliche Skill-Konfiguration.

## Zufallsfund in einer geöffneten Datei

1. Weitere Inhaltsausgabe sofort stoppen.
2. Trefferwert und Umgebung nicht wiederholen; nur Datei, Signal-ID und Status
   `secret-candidate` nennen.
3. Bereits erzeugte Ausgaben auf unbeabsichtigte Offenlegung prüfen. Eine mögliche Offenlegung als
   ungelösten Sicherheitsvorfall kennzeichnen und Rotation empfehlen; niemals behaupten, das
   Geheimnis sei widerrufen oder gelöscht.
4. Datei aus normalen Sortier-, Cut-and-Clue-, Archiv- und Papierkorbregeln herausnehmen, bis die
   Geheimnis-Policy entschieden ist.

## Transaktionale Cloud-Auslagerung

Ein Pfadmarker ist nur ein Cloud-Verdacht. Vor einer Mutation, soweit verfügbar, Providerstatus,
Sync-Root und Locks frisch prüfen. Dann:

1. `local_secret_root` auflösen und belegen, dass das Ziel außerhalb aller Sync-/Cloud-Roots liegt.
   Fehlt das Ziel oder lassen sich lokale Speicherung und restriktive Berechtigungen nicht prüfen,
   blockieren.
2. Dry-Run mit Quelle, opaker Pointer-ID, Pointermodus, betroffenen Referenzen und Rückweg zeigen.
   Auch bei `localize-after-approval` braucht der konkrete Lauf ausdrückliche Freigabe.
3. Datei ohne Inhaltsausgabe unter temporärem lokalen Namen kopieren, restriktive Berechtigungen
   setzen und Quell-/Zielhash intern vergleichen. Danach atomar auf den geplanten lokalen Namen
   umstellen. Nie ein vorhandenes Ziel überschreiben.
4. In einer ausschließlich lokalen, restriktiven `SECRET-POINTER-MAP.json` die opake ID dem lokalen
   Pfad zuordnen. Dieses Mapping nicht in die Cloud spiegeln.
5. Laufzeitreferenzen prüfen. Ein Pointer ersetzt keine funktionierende `.env`; würde eine
   Anwendung brechen, bleibt die Quellmutation blockiert, bis ihre Konfiguration angepasst und
   getestet ist.
6. Erst nach lokalem Readback und Hashgleichheit die Cloud-Quelle mit einer wiederherstellbaren
   Operation entfernen oder ersetzen. Provider-Papierkorb/Versionierung nutzen, wenn verfügbar.
7. Nicht-geheimen Pointer gemäß Modus schreiben und danach Cloud-Ort, lokales Ziel, Mapping,
   Referenzen und Rollback-Receipt erneut prüfen.

## Pointermodi

- `control-file` (Default): Eintrag in der nächstgelegenen geeigneten Steuerdatei, standardmäßig
  `SECRETS-POINTERS.md`. Geringstes Risiko, eine Anwendung durch einen Dummy zu stören.
- `sidecar`: `<dateiname>.secret-pointer` neben dem früheren Ort.
- `placeholder`: Dummy unter dem alten Dateinamen. Nur verwenden, wenn belegt ist, dass kein Prozess
  ihn als echtes Secret lädt.

Ein Cloud-Pointer enthält höchstens opake ID, Status, Prüfdatum und einen nicht sensiblen Hinweis auf
die lokale Policy. Standardmäßig enthält er weder lokalen Absolutpfad noch Geheimniswert,
Kontobezeichner oder Wiederherstellungsdaten.

## Harte Blocker

- unklarer Geltungsbereich oder fehlende Freigabe;
- lokales Ziel fehlt, liegt selbst in einem Sync-Root oder Berechtigungen sind nicht prüfbar;
- aktiver Schreibzugriff, Cloud-Lock, Kollision oder unvollständige Kopie;
- signierte, beweisrelevante oder laufzeitkritische Datei ohne geprüften Ersatzpfad;
- Pointer oder Bericht würde sensible Daten oder einen privaten lokalen Pfad offenlegen.
