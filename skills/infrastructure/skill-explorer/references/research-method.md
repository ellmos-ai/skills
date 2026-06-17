# Recherche-Methodik

## Zweisprachig & mehrquellig

Jede Recherche läuft in **Muttersprache (Deutsch) UND Englisch**, über drei Quelltypen. Englische
Quellen sind meist ergiebiger (Tooling-Ökosystem), deutsche liefern lokale Erfahrungen/Begriffe.

| Quelle | Wonach suchen | Worauf achten |
|--------|---------------|---------------|
| Allgemeines Web (WebSearch) | „best <thema> skills/plugins", „<thema> tool comparison", offizielle Docs | Aktualität, Vergleichsartikel, offizielle vs. Dritt-Quelle |
| GitHub | „awesome <thema>", „<thema> claude skill", „<thema> plugin", Marktplatz-Repos | Stars, letzte Commits, offene Issues, **Lizenz**, Maintainer-Aktivität |
| Reddit | „<thema> recommendations", r/-Subreddits zum Thema | reale Nutzererfahrung, Warnungen, „X statt Y"-Hinweise |

Suchbegriffe in beiden Sprachen variieren (Synonyme, Fachbegriffe). Pro Thema 4–8 gezielte Queries
statt einer generischen.

## Die drei Erfassungskategorien (pro Kandidat)

Für jeden gefundenen Skill/jedes Plugin strukturiert festhalten:

1. **Fähigkeiten / Features** — konkrete Funktionen; welche Aufgaben löst es?
2. **Abhängigkeiten / Kosten** — benötigte Tools/Runtimes (Node, Python, CLI), API-Keys, Preis
   (gratis/Abo), Wartungszustand, Plattform-Einschränkungen.
3. **Ressourcen / Alleinstellungsmerkmale** — mitgelieferte Skripte/Templates/Daten; was kann **nur**
   dieses Tool (USP)?

Diese drei Achsen sind dieselben, an denen den Audit-Modus Duplikate und „ressourcenreich vs.
abhängigkeitslastig" misst — so sind externe Kandidaten direkt mit dem Bestand vergleichbar.

## Quellencheck (Faktentreue)

- Behauptungen (Feature X, gratis, aktiv gewartet) an der **Originalquelle** verifizieren (Repo/Doc),
  nicht aus einem Blog-Ranking übernehmen.
- Keine erfundenen Stars/Versionen/Preise — nur, was belegt ist; sonst „unklar" kennzeichnen.
- Repo-Gesundheit prüfen: letzter Commit, Issue-Backlog, Lizenz vorhanden? Verwaiste Repos abwerten.

## Konsolidierung

Funde in Familien clustern (Taxonomie aus `references/clustering.md`), je Familie eine
Vergleichstabelle (Kandidat × die drei Kategorien). Bei Orchestrierung: je Quelle/Sprache ein
Subagent, Roh-Funde einsammeln, dann zentral deduplizieren und konsolidieren.
