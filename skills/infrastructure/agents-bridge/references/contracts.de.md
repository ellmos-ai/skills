# Dateiverträge von agents-bridge 3

## Autorität und Pointergraph

Ein Profil benennt genau eine `primary_surface`. Dieselbe Kombination aus Pfad
und Anbieter kommt genau einmal als `provider_surfaces[].strategy = primary`
vor. `truth_sources` sind geordnet; `pointer_graph` verweist ausschließlich auf
deklarierte Surface- und Truth-IDs. Ein Dateiname begründet keine Autorität.

`discover` ist nur dann entscheidungsfähig, wenn genau eine vorhandene Fläche
den Marker `agents-bridge-primary: true` enthält. Mehrere Marker führen zu
`status: blocked` samt Kandidaten und Handlungsbedarf. Kein Marker führt zu
`needs-user-selection`.

## Datenflussmatrix der reproduzierten Referenzstruktur

Die folgende nutzerneutralisierte Matrix beschreibt die beobachtete Struktur,
nicht einen neuen Default:

| Native Fläche | Datenfluss | Rolle im Profil |
|---|---|---|
| Codex `AGENTS.md` | lädt einen Codex-spezifischen Pointer, danach gemeinsame Regeln | Loader |
| `GPT.md` | verweist auf die gewählte Hauptfläche und weitere geordnete Quellen | Loader |
| Claude `CLAUDE.md` | erreicht Haupt- und gemeinsame Regeln direkt | Hauptfläche oder Loader, explizit gewählt |
| Gemini `GEMINI.md` | erreicht dieselben gemeinsamen Quellen über Loader oder Projektion | Loader/Projektion |
| Gemeinsamer Memory-Index | verweist auf getrennte providerbezogene Silos | Index, keine Zusammenführung |
| Provider-Silo | eigener Owner und eigene Writer; deklarierte Reader | getrennte Wahrheit |
| Messenger | Sender-Outbox → Empfänger-Inbox → ACK/Receipt | append-only Dateiereignisse |

Eine andere Instanz darf `AGENTS.md`, `GPT.md`, `GEMINI.md` oder einen
benutzerdefinierten relativen Pfad als Hauptfläche wählen. Die Matrix wird im
Profil abgebildet, nicht fest im Programm verdrahtet.

## Projektionen

Loader und Redirects werden bevorzugt. Eine Projektion ist nur für Anbieter
zulässig, die Referenzen nicht nativ laden können. Der generierte Kopf enthält:

- `agents-bridge-projection: v3`,
- Profil-ID und `generated_at`,
- SHA-256-Hashes aller geordneten Quellen,
- die Kennzeichnung, dass die Quellen statt der Projektion zu bearbeiten sind.

`verify` meldet eine Abweichung gezielt als `projection-drift`. Regeneration
läuft mit `capture --regenerate-projections` in ein neues Paket und danach über
Vorschau und Restore; sie überschreibt nichts ohne Backup und Receipt.

## Paket und Restore

`capture` liest ausschließlich manifestierte Profilpfade und explizite
Includes. Excludes haben beim Traversieren Vorrang. Es akzeptiert nur reguläre
UTF-8-Textdateien im Instanz-Root. Der Paket-Manifest enthält Profil- und
Inhaltshash, Dateigröße, Paket-/Quellhash, Synthese-/Projektionsstatus,
Verzeichnisumfang sowie Privacy-Ereignisse. Der absolute Quell-Root wird nicht
gespeichert.

`plan` unterscheidet `create`, `update` und `unchanged`. `restore --apply`
sichert jede geänderte vorhandene Datei, prüft den erwarteten Vorhash, schreibt
atomar und liest den Nachhash zurück. Der Receipt bindet Ziel, Backup,
Paket-Hash und jede Aktion. `rollback` verweigert die Ausführung bei späterer
Zieldrift. Ein unveränderter zweiter Restore ist idempotent.

## Messenger, Memory, Presence und Locks

Der Messenger erzeugt unveränderliche Eventdateien, actorbezogene Inbox und
Outbox, Handoffs, ACKs, senderseitige Receipts und ein append-only
`provenance.jsonl`. Actor-IDs müssen im Profil stehen. Inhalte passieren das
Privacy-Gate.

Der Memory-Index ist gemeinsam lesbar. Jedes Silo deklariert Owner, Writer,
Reader, Scope, Refresh-Regel und `merge_rule`. `automatic` ist unzulässig;
Zusammenführung und gegenseitiges Überschreiben bleiben manuelle Entscheidungen.

Presence-Dateien und kooperative Locks sind zeitlich begrenzt. Ein aktiver
fremder Claim stoppt fail closed. Nur der Owner darf einen aktiven Lock
freigeben. Diese Verträge starten keine Providerprozesse und ersetzen weder
Scheduler noch Ticket-System.

## Datenschutz

Der Standardmodus `reject` stoppt bei erkannten Credentials, privaten
Schlüsseln oder persönlichen absoluten Benutzerpfaden. `redact` ist eine
ausdrückliche Alternative und protokolliert die Ersetzung mit neutralen
Platzhaltern. Binärdateien, Nicht-UTF-8-Inhalte, Symlink-Ausbrüche und
unmanifestierte Paketdateien werden abgewiesen.
