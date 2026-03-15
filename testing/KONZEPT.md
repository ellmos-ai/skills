# Skill-Testverfahren

Dreiperspektivisches Qualitaetssystem fuer Skills.
Adaptiert aus dem B/O/E-Framework (.DEV/.TESTS) und RecludOS Evolution.

---

## Die drei Testperspektiven

```
S-TESTS (Statisch)          Automatisiert, objektiv
  Frontmatter, Code, Deps     "Ist der Skill formal korrekt?"

L-TESTS (LLM-Selbsterfahrung)  Halbautomatisch, introspektiv
  Claude laedt & nutzt Skill     "Kann ich als LLM damit arbeiten?"

U-TESTS (User-Erfahrung)    Manuell, subjektiv
  Nutzer bewertet Ergebnis       "Hat der Skill gemacht was ich wollte?"
```

---

## S-Tests: Statische Analyse (automatisiert)

Pruefen die formale Qualitaet ohne den Skill auszufuehren.

| ID | Test | Prueft | Score |
|----|------|--------|-------|
| S001 | Frontmatter | Pflichtfelder, Typen, Provenance | 0-5 |
| S002 | Vollstaendigkeit | Changelog, Beispiele, Ethik-Ref | 0-5 |
| S003 | Dependencies | pip-Pakete installierbar, zero-dep Bonus | 0-5 |
| S004 | Code-Qualitaet | Syntax, Imports, keine hardcodierten Pfade | 0-5 |
| S005 | Standalone-Check | Keine BACH-Runtime, keine User-Pfade | 0-5 |

**Ausfuehrung:**
```bash
PYTHONIOENCODING=utf-8 python testing/skill_tester.py test <skill-pfad> --type static
```

---

## L-Tests: LLM-Selbsterfahrung (halbautomatisch)

Claude (oder ein anderes LLM) liest den Skill und bewertet aus eigener Erfahrung.
Dies ist der wertvollste Test -- er prueft, ob ein LLM den Skill tatsaechlich
verstehen und anwenden kann.

| ID | Test | Fragestellung | Score |
|----|------|--------------|-------|
| L001 | Lesbarkeit | Verstehe ich sofort, was der Skill tut? | 0-5 |
| L002 | Anwendbarkeit | Kann ich den Skill sofort anwenden? | 0-5 |
| L003 | Vollstaendigkeit | Fehlt mir etwas, um den Skill zu nutzen? | 0-5 |
| L004 | Standalone-Faehigkeit | Brauche ich externes Wissen? | 0-5 |
| L005 | Prompt-Qualitaet | Sind die Anweisungen klar und effektiv? | 0-5 |
| L006 | Beispiel-Qualitaet | Helfen die Beispiele beim Verstaendnis? | 0-5 |

**Ausfuehrung:**
```bash
PYTHONIOENCODING=utf-8 python testing/skill_tester.py test <skill-pfad> --type llm
```

Der Tester generiert einen Prompt, den Claude ausfuehrt und strukturiert beantwortet.

**Parallele Ausfuehrung:** L-Tests koennen parallel zu U-Tests laufen --
das LLM bewertet den Skill unabhaengig vom Nutzer.

---

## U-Tests: User-Erfahrung (manuell)

Der Nutzer gibt dem Skill eine konkrete Aufgabe und bewertet das Ergebnis.

| ID | Test | Fragestellung | Score |
|----|------|--------------|-------|
| U001 | Aufgaben-Erfuellung | Hat der Skill gemacht, was ich wollte? | 0-5 |
| U002 | Ergebnis-Qualitaet | War das Ergebnis gut genug? | 0-5 |
| U003 | Effizienz | War der Weg zum Ergebnis effizient? | 0-5 |
| U004 | Ueberraschungen | Gab es unerwartetes Verhalten? | 0-5 |
| U005 | Wiederverwendbarkeit | Wuerde ich den Skill nochmal nutzen? | 0-5 |

**Ausfuehrung:**
```bash
PYTHONIOENCODING=utf-8 python testing/skill_tester.py test <skill-pfad> --type user
# Interaktive Eingabe der Bewertungen
```

---

## Testprofile

| Profil | S-Tests | L-Tests | U-Tests | Dauer |
|--------|---------|---------|---------|-------|
| QUICK | S001,S005 | L001,L002 | - | ~2 Min |
| STANDARD | Alle | Alle | - | ~5 Min |
| FULL | Alle | Alle | Alle | ~15 Min |
| STATIC | Alle | - | - | ~1 Min |
| LLM_ONLY | - | Alle | - | ~5 Min |
| USER_ONLY | - | - | Alle | ~10 Min |

---

## Gesamtscore (Quality Score)

```
quality_score = (S_avg * 0.25) + (L_avg * 0.50) + (U_avg * 0.25)
```

**Gewichtung:**
- S-Tests 25% -- Formale Korrektheit ist Grundvoraussetzung
- L-Tests 50% -- LLM-Selbsterfahrung ist der wichtigste Indikator
- U-Tests 25% -- Nutzer-Zufriedenheit als Realitaets-Check

**Schwellwerte (inspiriert von RecludOS Evolution):**

| Score | Bewertung | Aktion |
|-------|-----------|--------|
| >= 4.0 | Exzellent | Empfohlen, featured |
| 3.0-3.9 | Gut | Standardmaessig verfuegbar |
| 2.0-2.9 | Akzeptabel | Verbesserungsbedarf markieren |
| 1.0-1.9 | Mangelhaft | Review noetig, ggf. deprecated |
| < 1.0 | Unbrauchbar | Entfernen oder komplett ueberarbeiten |

---

## Fitness-Dimensionen (aus RecludOS adaptiert)

Zusaetzlich zum Gesamtscore werden 5 Dimensionen einzeln bewertet:

| Dimension | Quellen | Beschreibung |
|-----------|---------|-------------|
| D1 Klarheit | L001, L005, U003 | Ist sofort klar, was der Skill tut? |
| D2 Vollstaendigkeit | S002, L003, L006 | Fehlt nichts Wesentliches? |
| D3 Unabhaengigkeit | S003, S005, L004 | Funktioniert standalone ohne Extras? |
| D4 Wirksamkeit | U001, U002, U005 | Liefert der Skill gute Ergebnisse? |
| D5 Effizienz | S004, U003 | Token-sparend, kompakt, kein Bloat? |

---

## Ergebnis-Format (JSON)

```json
{
  "meta": {
    "skill": "skill-name",
    "skill_path": "skills/category/skill-name",
    "tester": "claude-opus-4-6",
    "date": "2026-03-12",
    "profile": "STANDARD",
    "version": "1.0.0"
  },
  "s_tests": {
    "S001": {"score": 5, "details": "Alle Pflichtfelder vorhanden"},
    "S002": {"score": 4, "details": "Changelog fehlt Detaileintraege"}
  },
  "l_tests": {
    "L001": {"score": 5, "notes": "Sofort verstaendlich"},
    "L002": {"score": 4, "notes": "Anwendbar, aber ein Beispiel unklar"}
  },
  "u_tests": {
    "U001": {"score": 4, "task": "GFK-Formulierung erstellen", "notes": "Ergebnis brauchbar"}
  },
  "dimensions": {
    "d1_clarity": 4.5,
    "d2_completeness": 4.0,
    "d3_independence": 5.0,
    "d4_effectiveness": 4.0,
    "d5_efficiency": 3.5
  },
  "quality_score": 4.1,
  "summary": {
    "strengths": ["Klar strukturiert", "Zero Dependencies"],
    "weaknesses": ["Beispiele koennten ausfuehrlicher sein"],
    "recommendation": "Gut -- empfohlen fuer Aufnahme"
  }
}
```

---

## Integration

- `catalog.py quality <skill>` -- Zeigt letzten Quality-Score
- `catalog.py quality --all` -- Uebersicht aller bewerteten Skills
- `testing/results/<skill-name>/` -- Historische Ergebnisse
- CI/CD: S-Tests automatisch bei PR, L-Tests optional
