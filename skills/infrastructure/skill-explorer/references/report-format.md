# Report-Format & globales Nummerierungsschema

## Aufbau des Gesamtberichts

1. **Kopf** — Inventar-Kennzahlen (Anzahl je `source`), Datum, Quell-Roots.
2. **Pro Familie ein Teilbericht** (Template unten).
3. **Eine konsolidierte Entscheidungsliste** über alle Familien, fortlaufend nummeriert.
4. **Register- & Pflege-Block** am Ende (unabhängig von Familien).

## Teilbericht-Template (pro Familie)

```markdown
### Familie: <Name>  (<n> Skills: <m> user, <k> read-only)

**Mitglieder**
| Skill | source | Fähigkeiten (Kurz) | Abhängigkeiten | Ressourcen |
|-------|--------|--------------------|----------------|------------|
| `x`   | user   | …                  | protocols: …   | scripts:1, refs:2 |
| `y`   | plugin | …                  | —              | — (read-only) |

**Analyse**
- Wann welcher Skill? <Vorzugsregeln je Anwendungsfall>
- Gut gekoppelt? <Kombinationen, die sich verstärken — "erst X (vor), dann Y (nach)">
- Duplikate? <überlappende Fähigkeiten; wer hat mehr/weniger Ballast>
- Ungleich gute Workflows? <gleiche Fähigkeit; einer bringt Ressourcen mit, der andere nur
  Abhängigkeiten/Prosa → ressourcenreicherer bevorzugen>

**Empfehlungen** (Nummern laufen global weiter — siehe Schema)
- [N] (a) <Redundanz: Skill X Duplikat von Y, mehr Abhängigkeiten → ablösen>
- [N] (b) <Workflow: aus n, o, p Workflow-Skill `/name` bauen>
- [N] (c) Familien-Maßnahme:
    - [N c1] Umbrella-Skill `<familie>-umbrella` anlegen
    - [N c2] Familie per Header-Router verlinken (nur user-Skills)
    - [N c3] beides
```

## Globales Nummerierungsschema

Die Nummern laufen über **alle** Familien fortlaufend weiter, damit der User mit einer einzigen
Zahlenliste antworten kann (z. B. „2, 5c2, 8, 11c3").

- Jede Empfehlung bekommt eine eindeutige Ganzzahl, beginnend bei 1, **familienübergreifend** hochzählend.
- Bei (c) sind die Unteroptionen als `Nc1 / Nc2 / Nc3` adressierbar (eine c-Empfehlung = eine Nummer
  mit drei Varianten; der User wählt die Variante mit Suffix, Default c1 wenn nur „N" genannt wird —
  aber im Zweifel nachfragen statt raten).
- Beispiel über zwei Familien:
  ```
  Familie Denkwerkzeuge
    [1] (a) structured-thinking ist Teil-Duplikat von think → ablösen
    [2] (c) Familie verlinken/umbrella  → 2c1 | 2c2 | 2c3
  Familie Recherche
    [3] (a) web-reading vs defuddle: defuddle bringt CLI-Ressource → web-reading ablösen
    [4] (b) aus deep-research + find-docs Workflow `/research-cited` bauen
    [5] (c) Familie verlinken/umbrella  → 5c1 | 5c2 | 5c3
  ```
  Antwort des Users dann z. B.: „1, 2c2, 4, 5c3".

## Register- & Pflege-Block (Listenende)

```markdown
### Register & Pflege
- [R] Register: existiert (code-skill-index + the skill index + the family map)
      → bei Bestätigung werden diese um die heutigen Ergebnisse ERWEITERT (kein neues Register).
      (Nur falls KEINS existierte: [R] Register aus Vorlage anlegen.)
- [P1] Care-Mechanismus für die gefundenen Familien anlegen? (Pflege-Subskill, siehe family-care.md)
- [P2] Care-Mechanismus für das Register anlegen? (Pflege-Subskill)
```

`R`, `P1`, `P2` sind separat adressierbar, damit sie nicht mit den durchnummerierten
Familien-Empfehlungen kollidieren.

## Stil

- Knapp und tabellarisch. Keine Skill-Inhalte reproduzieren — nur Fähigkeiten/Abhängigkeiten/Ressourcen
  vergleichen.
- Jede read-only-Empfehlung vermeiden: read-only-Skills tauchen in Analyse auf, aber nie in (a)/(c2)/Löschung.
