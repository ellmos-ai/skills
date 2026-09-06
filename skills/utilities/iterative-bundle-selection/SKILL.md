---
name: iterative-bundle-selection
version: 1.2.0
type: skill
author: Lukas Geiger
created: 2026-08-25
updated: 2026-08-25
description: Große Kandidatenlisten durch optionale Themen-Pfützen, Filterstufen und wiederholt neu gemischte Bündel schrittweise reduzieren. Nutzen, wenn der User Skills, Aufgaben, Ideen, Dateien oder andere Einträge gruppenweise auswählen, nach Merkmalen filtern oder nur innerhalb gemeinsamer Themenbereiche mischen will, ohne übrige Einträge endgültig zu verwerfen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, auswahl, datenreduktion, buendel, choice-overload, workflow]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'local_changes_since_sync': True}
---

# Iterative Bündelauswahl

Große Auswahlmengen mit wenigen groben Entscheidungen verkleinern, ohne nicht gewählte Kandidaten vorschnell auszusondern.

## Grundprinzip

1. Alle Kandidaten als gemeinsamen Pool erfassen und eindeutig benennen.
2. Optional Themen-Pfützen definieren und jeden Kandidaten genau einer Primärpfütze zuordnen.
3. Gewünschte Filter nacheinander global oder innerhalb einzelner Pfützen anwenden und ihre Treffer separat aufbewahren.
4. Innerhalb jeder aktiven Pfütze mischen und standardmäßig Bündel zu je fünf Kandidaten bilden.
5. Die Bündel der ersten Runde eindeutig nach Pfütze mit `THEMA-A`, `THEMA-B` … beschriften.
6. Den User ganze Bündel auswählen lassen.
7. Ausgewählte Bündel aus dem offenen Pool nehmen und der nächsten Aktion zuführen.
8. Kandidaten aus nicht gewählten Bündeln in ihre jeweilige Pfütze zurückgeben.
9. Pfützen und Filter beibehalten, jede Pfütze separat neu mischen und Strichlabels verwenden.
10. Weitere Runden fortsetzen, bis der User stoppt oder der Pool leer ist.

Ein letztes Bündel darf weniger als fünf Kandidaten enthalten. Nicht gewählte Bündel bedeuten "noch offen", nicht "abgelehnt".

## Workflow

### 1. Pool vorbereiten

- Duplikate anhand stabiler Namen oder IDs entfernen.
- Bereits ausgewählte oder erledigte Kandidaten ausschließen.
- Gesperrte Kandidaten kennzeichnen, aber nicht stillschweigend löschen.
- Anzahl des Ausgangspools nennen.

### 2. Themen-Pfützen bilden

Eine Themen-Pfütze ist ein abgegrenzter Teilpool. Kandidaten aus verschiedenen Pfützen werden nicht miteinander gemischt.

- Die Methode nur verwenden, wenn der User Themen-Pfützen verlangt oder eine thematische Trennung ausdrücklich sinnvoll findet.
- Pfützen mit stabiler ID, Titel, Zuordnungsregel und Kandidatenzahl dokumentieren.
- Pfützen aus User-Vorgaben, vorhandenen Kategorien oder nachvollziehbaren Merkmalen ableiten.
- Automatisch abgeleitete Zuordnungen vor der ersten Folgeaktion transparent zeigen.
- Jeden Kandidaten standardmäßig genau einer Primärpfütze zuordnen; keine stillen Duplikate über mehrere Pfützen erzeugen.
- Mehrdeutige Kandidaten in `UNZU — Unzugeordnet` halten, bis eine Zuordnung feststeht.
- Eine Pfütze mit weniger als fünf Kandidaten als kleines Bündel ausgeben; niemals mit einem anderen Thema auffüllen.
- Filter können global für alle Pfützen oder lokal für eine benannte Pfütze gelten.
- Gefilterte Kandidaten behalten ihre Pfützenzuordnung, damit sie beim Reaktivieren an die richtige Stelle zurückkehren.
- Beim Teilen, Zusammenlegen oder Umbenennen einer Pfütze nur ihre betroffenen Bündel verwerfen und neu bilden.

Beispiel:

```text
DEV  | Entwicklung     | 12 Kandidaten | DEV-A, DEV-B, DEV-C
MED  | Medien          |  7 Kandidaten | MED-A, MED-B
UNZU | Unzugeordnet    |  2 Kandidaten | UNZU-A
```

In späteren Runden die Rundentiefe am Bündelbuchstaben kennzeichnen: `DEV-A′`, `MED-B″`.

### 3. Filterstufen anwenden

- Filter optional und in der vom User genannten Reihenfolge ausführen.
- Jeden Filter mit stabiler ID, Modus, Regel und Trefferzahl protokollieren.
- Textvergleiche standardmäßig ohne Beachtung der Großschreibung durchführen.
- `exclude` entfernt Treffer nur aus dem aktiven Pool und legt sie im Filterpool ab.
- `include` behält nur Treffer im aktiven Pool; Nichttreffer wandern in den Filterpool.
- Fehlt eine Modusangabe und sagt der User, der Pool solle gefiltert oder bereinigt werden, `exclude` verwenden und diese Annahme nennen.
- Nach jeder Stufe Eingangsgröße, Trefferzahl und verbleibende Größe ausgeben.
- Gefilterte Kandidaten nie löschen oder als abgelehnt markieren; der User kann einzelne Filter später deaktivieren.

Beispiel:

```text
F1 | exclude | Name enthält "aws"         | 13 Treffer
F2 | exclude | Name enthält "hyperframes" | 8 Treffer
Aktiver Pool: 44 | Filterpool: 21
```

Ändert sich ein Filter, alle bisherigen Bündel des aktiven Pools verwerfen und erst danach neu mischen.

### 4. Runde bilden

- Kandidaten wirklich neu mischen; die alte Bündelstruktur nicht bloß umbenennen.
- Möglichst fünf Kandidaten je Bündel verwenden.
- Nur Kandidaten derselben Themen-Pfütze miteinander mischen.
- Keine Kandidaten duplizieren oder verlieren.
- Bei fachlich abhängigen Kandidaten die Abhängigkeit markieren, statt sie zu verschweigen.

Ausgabeformat:

```text
Bündel DEV-A: dev-1, dev-2, dev-3, dev-4, dev-5
Bündel MED-A: media-1, media-2, media-3
```

Ohne Themen-Pfützen weiterhin die einfachen Labels `A`, `B`, `C` … verwenden.

### 5. Auswahl verarbeiten

- Antworten wie `A, D und F` akzeptieren.
- Vor einer Folgeaktion die enthaltenen Kandidaten noch einmal vollständig nennen.
- Notwendige Locks, Voraussetzungen oder Dry-Runs pro Kandidat prüfen.
- Erfolgreiche Kandidaten als ausgewählt oder erledigt protokollieren.
- Blockierte oder fehlgeschlagene Kandidaten in den Restpool zurückgeben.

### 6. Restpool neu bündeln

- Nur tatsächlich erfolgreiche Kandidaten dauerhaft entfernen.
- Alle übrigen Kandidaten in ihre bisherigen Pfützen zurückführen und dort separat neu mischen.
- Aktive Filter vor jeder Neumischung erneut auf den Restpool anwenden.
- Die nächste Runde mit Strichlabels kennzeichnen: `DEV-A′`, danach `DEV-A″` usw.
- Gesamtpool, Filterpool, aktive Poolgröße sowie die Größe jeder Pfütze nennen.

## Schutzregeln

- Nichtauswahl niemals als endgültige Ablehnung interpretieren.
- Filtertreffer niemals stillschweigend verwerfen; sie bleiben im Filterpool rückholbar.
- Pfützengrenzen beim Mischen niemals überschreiten.
- Kandidaten beim Neuverteilen weder duplizieren noch zwischen Pfützen verschieben, sofern der User die Einteilung nicht ändert.
- Keine Kandidaten wegen einer ungünstigen Bündelkombination verlieren.
- Gesperrte Kandidaten nicht erzwingen; sie bleiben offen.
- Bei irreversiblen oder risikoreichen Folgeaktionen erst die einzelnen Kandidaten bestätigen lassen.
- Bei Bedarf einen reproduzierbaren Mischschlüssel dokumentieren; ansonsten genügt eine nachvollziehbar neue Verteilung.
- Das Verfahren reduziert Auswahlkomplexität, ersetzt aber keine fachliche Bewertung einzelner Kandidaten.

## Abgrenzung

- `decide` bewertet eine konkrete Entscheidung mit Kriterien und Frameworks.
- `decision-briefing` koordiniert mehrere unterschiedliche Entscheidungsfragen.
- `iterative-bundle-selection` reduziert einen großen gleichartigen Kandidatenpool durch wiederholte Gruppenwahl und Neumischung.

## Abschluss

Das Verfahren endet, wenn der Pool leer ist, der User ausdrücklich stoppt oder nur noch Kandidaten übrig sind, die eine Einzelentscheidung benötigen. Dann eine kurze Bilanz mit ausgewählt, offen und blockiert ausgeben.

## Changelog

### 1.2.0 (2026-08-25)

- Optionale Themen-Pfützen als Poolteiler ergänzt.
- Pfützengebundene Mischung, lokale Filter, eindeutige Bündellabels und `UNZU`-Behandlung festgelegt.

### 1.1.0 (2026-08-25)

- Reversible `include`- und `exclude`-Filterstufen vor der Neumischung ergänzt.
- Filterprotokoll, Filterpool und Neuberechnung bestehender Bündel festgelegt.

### 1.0.0 (2026-08-25)

- Iterative Fünferbündel, Strichrunden, Restpool und Blocker-Rückführung als eigenständiges Datenreduktions- und Entscheidungsverfahren festgehalten.
