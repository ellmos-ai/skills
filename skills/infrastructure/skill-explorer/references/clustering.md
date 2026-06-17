# Clustering — Familien bilden

## Grundsatz: aus Bestehendem seeden, nicht neu erfinden

Vor dem Clustern die existierenden Familien-Quellen lesen und als Seed übernehmen (sofern auf dem
System vorhanden):

- die **Familien-/Routing-Map** (eine kuratierte Quervergleichsdoku „welcher Skill statt welchem"),
- der **Skill-Index** (Liste mit Kategorie-Abschnitten),
- ein vorhandener **Skill-Index-Skill** mit Kategorie-Katalogen.

Vorhandene Familien **übernehmen** (gleiche Namen, gleiche Zuordnung). Nur dort einen neuen oder
anderen Cluster bilden, wo der reale Bestand es erzwingt (neue Skills ohne Familie, oder eine Familie
wird zu groß/heterogen). Jede Abweichung von der bestehenden Map im Bericht begründen.

## Typische Seed-Familien

Ein generischer Startpunkt — an den realen Bestand anpassen:

| Familie | Worum es geht |
| --- | --- |
| Utilities / Werkzeuge | kleine Helfer (Datei-Ops, Chunking, Transkription) |
| Design / Visualisierung | UI, Diagramme, Canvas, Notizansichten |
| Coding & Debugging | Bug-Suche, Debug-Protokolle, Entwicklungszyklen |
| Denk- / Entscheidungswerkzeuge | Analyse, Ideenfindung, Entscheidungsframeworks |
| Wissens- / Recherche-Skills | Literatur, Doku-Abruf, Web→Markdown, Quellenprüfung |
| Pipeline / Projekt-Setup | Projekte/Pipelines anlegen, optimieren, onboarden |
| System / Meta / Skill-Management | Onboarding, Sync, Skill-Index, dieser Skill |
| Domänen-Gruppen | thematische Bündel (z. B. Game-Dev, Office, Forschung) |

Konkrete Familien und Mitglieder kommen aus dem **eigenen** Inventar + der Familien-Map — nicht aus
dieser generischen Tabelle.

## Clustering-Achsen (zum Einordnen & Vergleichen)

Skills entlang weniger Achsen einordnen — das macht Duplikate und Kopplungen sichtbar:

| Achse | Pol A | Pol B |
| --- | --- | --- |
| Phase | vor Code / vor Entscheidung | nach Code / nach Entscheidung |
| Breite | ein Element (1 Bug, 1 Datei, 1 Frage) | ganze Codebase / Pipeline |
| Rigidität | rigide Disziplin (genau befolgen) | flexibles Muster (adaptieren) |
| Wirkung | nur Analyse / Report | verändert Code / Dateien |
| Rohstoff | vorhandenes Wissen im Kontext | externe / dokumentierte Fakten |

Zwei Skills, die auf allen Achsen nahe beieinanderliegen, sind Duplikat-Kandidaten. Zwei Skills, die
sich auf der Phase-Achse ergänzen (einer „vor", einer „nach"), sind Kopplungs-Kandidaten.

## Quelle-Markierung (Survey vs. Mutation)

Jeden Skill im Cluster mit seiner `source` aus dem Inventar labeln:

- `user` — editierbar; nur diese dürfen Header bekommen, abgelöst oder in Workflows verbaut werden.
- `plugin` — read-only (Plugin-Cache, wird bei Update überschrieben). Nur clustern/vergleichen.
- `external` — read-only Drittanbieter. Nur clustern/vergleichen.
- weitere system-gebundene Quellen — nur erwähnen.

Im Bericht read-only-Skills klar als solche kennzeichnen, damit keine Empfehlung sie zu verändern
oder zu löschen vorschlägt.
