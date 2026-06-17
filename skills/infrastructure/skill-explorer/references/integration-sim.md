# Wirkungs-Simulation — wie ein neuer Skill eine Familie verändert

## Wann

Wenn den Explore-Modus mit den Audit-Modus kombiniert wird, danach läuft, oder eine frühere
`skill-explorer/config.json` existiert. Dann ist die bestehende Familienstruktur bekannt und ein
externer Kandidat kann gegen sie simuliert werden — statt ihn nur isoliert zu bewerten.

## Eingaben

- Die Familie aus `config.json` (Mitglieder, Router, Umbrella) bzw. aus einem frischen
  `inventory_skills.py`-Lauf.
- Der Kandidat mit seinen drei Kategorien (Fähigkeiten / Abhängigkeiten / Ressourcen).

## Simulationsfragen (pro Kandidat × Zielfamilie)

1. **Verbessert** er die Familie? Schließt er eine Fähigkeitslücke, die kein Mitglied abdeckt?
2. **Verschlechtert** er sie? Reines Duplikat eines vorhandenen Mitglieds, aber mit mehr
   Abhängigkeiten/Kosten → erhöht Wartungslast ohne Mehrwert.
3. **Macht er sie unabhängiger?** Ersetzt er eine externe Abhängigkeit eines Mitglieds durch eine
   mitgelieferte Ressource (z. B. eigenes Skript statt API-Key) → robuster, offline-fähiger.
4. **Verschiebt er das Routing?** Würde er für bestimmte Fälle zum neuen Vorzug („X statt Y")? Dann
   müssen Familien-Router/Umbrella angepasst werden.
5. **Risiko/Kosten** vs. Nutzen: Lizenz, Wartung, Kosten gegen den Zugewinn abwägen.

## Ausgabe

Pro Kandidat ein kurzes Urteil mit Einordnung in die nummerierte Empfehlungsliste:
- **(a) Ersatz:** „Mitglied X entfernen, Kandidat A installieren" — wenn A X dominiert (gleiche
  Fähigkeit, weniger Ballast / mehr Ressourcen).
- **(b) Ergänzung:** „Kandidat Z bringt einzigartige Fähigkeit — bei Bedarf installieren" — wenn er
  eine Lücke füllt, ohne ein Mitglied zu verdrängen.
- **(—) Verwerfen:** wenn Duplikat ohne Mehrwert oder zu teuer/riskant — mit Begründung.

Nach einer (a)-Entscheidung beachten: Vernetzungs-/Header-Aufräumen für das entfernte Mitglied und
Einbinden des neuen (siehe `install-uninstall.md`). config.json entsprechend aktualisieren.
