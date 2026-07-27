# Wahrheits-Topologien

## Eine Datei

Eine einzelne Datei ist kanonisch. Ziel-Boot-Dateien verweisen auf sie und
enthalten nur minimale, zielspezifische Startanweisungen.

## Geordnete Dateimenge

Mehrere Dateien bilden gemeinsam die Wahrheit. Das Profil hält die Reihenfolge
explizit fest, zum Beispiel:

1. organisationsweite Regeln,
2. Benutzerregeln,
3. Systemregeln,
4. Workspace- oder Projektoverlay.

Spätere Dateien dürfen frühere Regeln nur überschreiben, wenn das Profil diese
Semantik ausdrücklich festlegt.

## Föderierte Wahrheit

Verschiedene Besitzer verantworten getrennte Teilbereiche. Ein Loader verweist
auf alle Quellen, führt sie aber nicht automatisch zusammen. Konflikte werden
mit Besitzer, Bereich und Entscheidungsregel sichtbar gemacht.

## Generierte Projektion

Wenn ein Ziel keine Verweise laden kann, wird eine Projektion erzeugt. Sie
braucht mindestens:

- stabile Profil-ID,
- Quellpfade und Reihenfolge,
- Hashes oder Revisionen der Quellen,
- Generierungszeitpunkt,
- Kennzeichnung „nicht direkt bearbeiten“,
- definierte Driftprüfung.

## Nicht zulässig

- eine Quelle aus Gewohnheit oder Anbieterzugehörigkeit bestimmen,
- leere Profilfelder als Zustimmung interpretieren,
- bidirektionales Schreiben ohne Konflikt- und Ownership-Modell,
- persönliche absolute Pfade in die portable Skill-Fassung einbauen.
