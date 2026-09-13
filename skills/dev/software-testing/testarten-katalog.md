# Testarten-Katalog — Referenz zum Skill `software-testing`

> Vollständiger Katalog der Teststufen, Testarten und Testentwurfsverfahren mit
> Phasen-Zuordnung. Basis: Online-Recherche 2026-08-22 (ISTQB-Systematik, Testpyramide,
> Agile Testing Quadrants, moderne Praktiken). Quellen am Ende.

---

## 1. Teststufen im Detail

| Stufe | Prüfobjekt | Prüfziel | Wer | Wann |
|---|---|---|---|---|
| **Komponententest / Unit-Test** | Einzelne Funktion, Klasse, Modul — isoliert (Mocks/Stubs) | Logik der kleinsten Einheit korrekt? | Entwickler | Während der Implementierung, bei jedem Commit |
| **Integrationstest** | Zusammenspiel mehrerer Komponenten, Schnittstellen, APIs, DB-Anbindung | Verträge zwischen Modulen eingehalten? Datenfluss korrekt? | Entwickler / Testteam | Nach bestandenen Unit-Tests; bei jedem Merge in CI |
| **Systemtest** | Das komplette, integrierte System End-to-End | Erfüllt das Gesamtsystem die spezifizierten (technischen) Anforderungen? | Testteam (unabhängig) | Wenn ein integrierter Gesamtbuild vorliegt; vor Release |
| **Abnahmetest (Acceptance Test)** | Gesamtsystem aus Sicht des Auftraggebers/Nutzers | Erfüllt das System die Geschäftserwartungen im realen Einsatz? | Kunde, Fachbereich, Endnutzer | Letzte Stufe vor Auslieferung/Go-Live |

**Integrationsstrategien:** Top-Down (von der UI-Schicht nach innen, untere Schichten
gestubbt), Bottom-Up (von DB/Services nach oben, obere Schichten über Treiber), Big Bang
(alles auf einmal — nur bei kleinen Systemen sinnvoll). Inkrementelle Strategien sind
Best Practice, weil Fehler lokalisierbar bleiben.

**Unterformen des Abnahmetests:**
- **User Acceptance Testing (UAT)** — Fachbereich prüft Geschäftsprozesse.
- **Betrieblicher Abnahmetest (OAT)** — Backup/Restore, Deployment, Monitoring, Wartbarkeit.
- **Vertraglicher / regulatorischer Abnahmetest** — Vertragskriterien bzw. Normen/Gesetze.
- **Alpha-Test** — durch interne, aber entwicklungsfremde Nutzer beim Hersteller.
- **Beta-Test** — durch echte Kunden in deren Umgebung (Feldtest) vor dem Release.

**Testpyramide:** Unit-Tests als breite Basis, darüber Integrations-/**API-Tests**
(Service-Ebene), an der Spitze wenige **E2E-/UI-Tests**. Verbreitete Daumenregel:
grob 70/20/10 — als Startpunkt, nicht als Dogma; nach tatsächlicher Fehlerherkunft
justieren. Anti-Pattern: „Ice-Cream-Cone" (viele UI-Tests, wenige Unit-Tests) →
langsame, flaky Suiten.

---

## 2. Testarten — was geprüft wird

### 2.1 Funktionale Tests
Prüfen, **was** das System tut: Verhalten gegen funktionale Anforderungen, User Stories,
Use Cases. Auf allen Teststufen möglich (Unit-Test einer Berechnungsfunktion ebenso wie
funktionaler Systemtest eines Bestellprozesses).

### 2.2 Nicht-funktionale Tests
Prüfen, **wie gut** das System etwas tut:

| Art | Prüft | Typischer Zeitpunkt |
|---|---|---|
| **Performanztest** | Antwortzeiten, Durchsatz, Ressourcenverbrauch | Sobald ein integriertes System in produktionsnaher Umgebung läuft; punktuell auch früher auf Komponentenebene |
| **Lasttest** | Verhalten unter erwarteter Normal-/Spitzenlast | Vor Release; regelmäßig als Nightly/Pre-Release-Gate |
| **Stresstest** | Verhalten **jenseits** der Grenzen: Wo bricht das System, wie erholt es sich? | Vor Release; nach Architekturänderungen |
| **Security-Test** | Schwachstellen, Zugriffskontrolle, Datenschutz (SAST früh im Code, DAST/Pentest am laufenden System) | SAST ab dem ersten Commit; DAST/Pentest auf Systemebene; kontinuierlich |
| **Usability-Test** | Bedienbarkeit, Verständlichkeit, Nutzerzufriedenheit | Ab ersten Prototypen (früh!), vertieft auf Systemebene mit echten Nutzern |
| **Kompatibilitätstest** | Browser, OS, Geräte, Auflösungen, Versionen | Systemtestphase; bei Web/Mobile kontinuierlich in der Pipeline |
| **Accessibility-Test (A11y)** | Barrierefreiheit (WCAG, Screenreader, Kontraste) | Ab UI-Design, automatisierte Checks in CI, manuelle Prüfung vor Release |
| **Zuverlässigkeits-/Wiederherstellungstest** | Ausfallverhalten, Failover, Recovery | Vor Deployment; in reifen Organisationen als Chaos-Experiment auch danach |
| **Installations-/Wartbarkeitstest** | Installation, Update, Deinstallation, Migration | Vor Auslieferung; bei jedem Release-Paket |

Nicht-funktionale Kriterien **bereits in der Anforderungsphase messbar definieren**
(z. B. „95. Perzentil der Antwortzeit < 300 ms bei 1.000 gleichzeitigen Nutzern") —
sonst ist später nicht entscheidbar, ob ein Test bestanden ist.

### 2.3 Strukturbezogene Tests
Prüfen die **Abdeckung der inneren Struktur**: Anweisungen, Zweige, Pfade. Hauptsächlich
auf Komponenten- und Integrationsebene; Coverage-Messung als Ergänzung (nicht Ersatz)
funktionaler Tests.

### 2.4 Änderungsbezogene Tests

| Art | Zweck | Umfang | Wann |
|---|---|---|---|
| **Smoke-Test** | Ist der Build überhaupt stabil genug zum Testen? Kernfunktionen grob prüfen | Sehr klein, breit | Als Erstes auf jedem neuen Build; automatisiert in CI |
| **Sanity-Test** | Funktioniert der geänderte/betroffene Bereich? | Klein, fokussiert auf die Änderung | Auf stabilen Builds nach gezielten Änderungen, vor der vollen Regression |
| **Fehlernachtest (Re-Test/Confirmation)** | Ist der konkrete gemeldete Fehler wirklich behoben? | Exakt die fehlgeschlagenen Testfälle | Direkt nach dem Bugfix — **nicht** mit Regression verwechseln |
| **Regressionstest** | Hat die Änderung an anderer Stelle etwas kaputt gemacht? | Breite Suite über bestehende Funktionalität | Nach Re-Test/Sanity; automatisiert bei jedem Merge/Nightly |

Bewährte Reihenfolge: **Smoke → Sanity/Re-Test → Regression.**

---

## 3. Statisch vs. dynamisch

**Statisches Testen** prüft **ohne Ausführung** des Codes — früheste und günstigste
Fehlerfindung (Verifikation: „Bauen wir das Produkt richtig?"):
- **Reviews / Walkthroughs / Inspektionen** von Anforderungen, Architektur, Design,
  Testkonzepten und Code (Code-Review im Pull Request als üblichste Form).
- **Statische Analyse** mit Werkzeugen: Linter, Typprüfung, SAST (Security), SCA
  (Abhängigkeits-/Lizenzprüfung), Komplexitätsmetriken.

Einsatz **ab der Anforderungsphase**, bevor Code existiert — Anforderungsreviews finden
Mehrdeutigkeiten, die später die teuersten Fehler würden.

**Dynamisches Testen** führt das System aus (Validierung: „Bauen wir das richtige
Produkt?"). Nur dynamisch findet man Laufzeitfehler, Memory-Leaks, Performance-Engpässe
und Umgebungsprobleme.

**V-Modell-Mapping** (Tests je Stufe beim Erstellen der zugehörigen Spezifikation
entwerfen, nicht erst am Ende):

| Entwicklungsphase (Spezifikation) | Korrespondierende Teststufe (Ausführung) |
|---|---|
| Anforderungen / Fachkonzept | Abnahmetest |
| Systemdesign / Funktionale Spezifikation | Systemtest |
| Architektur / technisches Design | Integrationstest |
| Modul-/Detaildesign, Code | Komponententest |

---

## 4. Testentwurfsverfahren im Detail

### 4.1 Black-Box (spezifikationsbasiert)
- **Äquivalenzklassenbildung:** Eingaberaum in Klassen teilen, die das System gleich
  behandeln sollte; ein Repräsentant pro Klasse genügt (gültige UND ungültige Klassen).
- **Grenzwertanalyse:** Werte an und direkt jenseits der Klassengrenzen (bei erlaubtem
  Bereich 5–50: teste 4, 5, 50, 51) — typische Fehler sind um eins verschobene oder
  fehlende Grenzen.
- **Entscheidungstabellentest:** Kombinationen von Bedingungen und Aktionen tabellarisch
  abdecken — ideal bei komplexen Geschäftsregeln.
- **Zustandsübergangstest:** Zustände, Übergänge und verbotene Übergänge eines
  Zustandsautomaten abdecken — ideal bei Workflows, Sessions, Gerätesteuerung.
- **Anwendungsfallbasiertes Testen:** End-to-End-Szenarien inkl. Fehler- und
  Ausnahmepfaden aus Nutzersicht.

Einsatz: alle Teststufen; Schwerpunkt System-/Abnahmetest; Äquivalenzklassen und
Grenzwerte auch im Unit-Test.

### 4.2 White-Box (strukturbasiert)
- **Anweisungsüberdeckung** (jede Anweisung mindestens einmal),
- **Zweig-/Entscheidungsüberdeckung** (jeder Ausgang jeder Verzweigung),
- höherwertig: Bedingungs-, Pfad-, MC/DC-Überdeckung (in sicherheitskritischen Domänen
  wie Luftfahrt vorgeschrieben).

Einsatz: primär Komponenten-/Integrationstest; Coverage als Lückenindikator, nicht als
Qualitätsziel (100 % Coverage beweist keine Korrektheit).

### 4.3 Erfahrungsbasiert
- **Error Guessing:** gezielt dort testen, wo erfahrene Tester Fehler vermuten
  (Null/None, Leerstrings, Sonderzeichen, Zeitzonen, Gleichzeitigkeit/Races).
- **Exploratives Testen:** gleichzeitiges Lernen, Testentwurf und Ausführung ohne
  Skripte — zeitboxt in Sessions mit Charter. Findet, was skriptbasierte Tests übersehen.
- **Checklistenbasiertes Testen:** strukturierte Prüflisten (UI-Standards, OWASP, …).

Einsatz: ergänzend zu systematischen Verfahren; besonders wertvoll auf Systemebene,
bei knapper Zeit und bei neuen Features.

---

## 5. Vorgehensweisen (testgetrieben)

- **TDD (Test-Driven Development):** Test zuerst (rot) → minimal implementieren (grün) →
  refaktorisieren. Unit-Ebene; erzwingt testbares Design.
- **ATDD (Acceptance Test-Driven Development):** Abnahmekriterien vor der
  Implementierung gemeinsam mit dem Fachbereich als ausführbare Tests.
- **BDD (Behavior-Driven Development):** ATDD mit gemeinsamer Sprache
  (Given/When/Then, Gherkin/Cucumber) — lebende Spezifikation zwischen Fachbereich,
  Entwicklung und Test.

Alle drei: Tests existieren, **bevor** der Code entsteht („Testing Early").

---

## 6. Agile Testing Quadrants (Marick / Crispin & Gregory)

| | **Team-unterstützend** | **Produkt-bewertend** |
|---|---|---|
| **Business-orientiert** | **Q2:** Funktionale Tests, Story-Tests, BDD-Szenarien, Prototypen (weitgehend automatisiert) | **Q3:** Exploratives Testen, Usability, UAT, Alpha/Beta (manuell) |
| **Technologie-orientiert** | **Q1:** Unit-/Komponententests, TDD (voll automatisiert) | **Q4:** Performance, Last, Security, Zuverlässigkeit (werkzeuggestützt) |

Q1/Q2 laufen kontinuierlich in jedem Sprint und *verhindern* Fehler; Q3/Q4 *bewerten*
das Produkt, sobald genug Produkt vorhanden ist.

---

## 7. Phasen-Zuordnung komplett

### Klassisch entlang des Lebenszyklus

| SDLC-Phase | Prüfaktivitäten |
|---|---|
| **Anforderungen** | Anforderungsreviews (statisch); Testbarkeit prüfen; Abnahmekriterien + messbare nicht-funktionale Ziele definieren; Abnahmetests skizzieren (ATDD) |
| **Design/Architektur** | Design-/Architekturreviews; Integrations- und Systemteststrategie planen; Skalierungs-/Sicherheitsrisiken bewerten (Threat Modeling) |
| **Implementierung** | Statische Analyse + Code-Reviews; Unit-Tests (idealerweise TDD); frühe Performance-/Security-Checks auf Komponentenebene |
| **Integration** | Integrationstests, API-/Contract-Tests, Schnittstellenprüfung |
| **Test/Stabilisierung** | Systemtest (funktional + nicht-funktional); Regression; Fehlernachtests |
| **Abnahme/Release** | UAT, betriebliche Abnahme, Alpha/Beta; finale Smoke-Tests auf dem Release-Kandidaten; Recovery-Tests |
| **Betrieb/Wartung** | Monitoring/Observability; Regression bei jedem Patch; ggf. Chaos-Experimente; Wartungstests nach Migrationen |

### CI/CD-Gates

| Pipeline-Stufe | Gate |
|---|---|
| Jeder Commit | Unit-Tests, Linter, statische Analyse (Sekunden–Minuten) |
| Pull Request | Code-Review, SAST/SCA, gezielte Komponententests |
| Merge | Integrations- und API-/Contract-Tests, Smoke auf Testumgebung |
| Nightly / vor Release | Volle Regression, E2E-Suite, Performance-/Lasttests, DAST |
| Release-Kandidat | Smoke auf Staging, UAT, Abnahme |
| Produktion | Canary-/Blue-Green, Monitoring, Feature Flags, ggf. Chaos-Engineering (Shift-Right) |

---

## 8. Moderne/ergänzende Verfahren

- **Contract Testing** (z. B. Pact): prüft API-Verträge zwischen Consumer und Provider
  ohne gemeinsames Deployment — schneller und stabiler als Integrationstests über
  geteilte Staging-Umgebungen. Pflicht-Kandidat bei Microservices.
- **Mutation Testing** (z. B. Stryker, PIT, mutmut): baut absichtlich kleine Codefehler
  („Mutanten") ein und misst, ob die Testsuite sie erkennt — bewertet die **Güte der
  Tests selbst**, wo Coverage-Zahlen täuschen.
- **Property-Based Testing** (z. B. Hypothesis, fast-check): Invarianten formulieren
  („Sortieren ist idempotent"), gegen hunderte generierte Eingaben prüfen — findet
  Randfälle, an die niemand gedacht hat.
- **Fuzzing:** massenhaft zufällige/mutierte Eingaben gegen Parser und Schnittstellen —
  Standard in der Security-Prüfung.
- **Chaos Engineering / Testing in Production** (populär durch Netflix' Chaos Monkey):
  kontrollierte Fehlerinjektion in produktionsnahe oder produktive Systeme — sinnvoll
  erst bei reifer Observability und sauberen Rollback-Wegen.

---

## 9. Best Practices (Langfassung)

1. **Shift-Left:** Reviews und statische Analyse ab der Anforderungsphase; Fehler werden
   nach verbreiteter Faustregel (auf Boehm zurückgehend, im Detail umstritten) um
   Größenordnungen teurer, je später sie gefunden werden.
2. **Testpyramide respektieren:** viele schnelle Unit-Tests, gezielte Integrations-/
   API-Tests, wenige stabile E2E-Tests.
3. **Automatisieren, was wiederholt wird:** Smoke, Regression, API- und Unit-Tests in
   die CI/CD-Pipeline mit klaren Gates je Stufe. Manuelle Kapazität für exploratives
   Testen und Usability reservieren.
4. **Testfälle systematisch entwerfen:** Äquivalenzklassen + Grenzwerte als
   Grundausstattung; Entscheidungstabellen bei Regeln; Zustandsübergänge bei Workflows;
   erfahrungsbasierte Verfahren als bewusste Ergänzung.
5. **Nicht-funktionale Anforderungen messbar machen** — ohne Zahlenziel kein
   auswertbarer Performanztest.
6. **Re-Test ≠ Regression:** erst den Fix bestätigen, dann Seiteneffekte prüfen;
   Reihenfolge Smoke → Sanity → Regression.
7. **Flaky Tests aktiv bekämpfen:** quarantänisieren, Ursache fixen oder löschen.
8. **Testdaten und -umgebungen managen:** produktionsnahe, reproduzierbare Umgebungen
   (Container/IaC), anonymisierte bzw. synthetische Testdaten.
9. **Testqualität selbst messen:** Coverage als Lückenindikator, Mutation Testing als
   Wirksamkeitsnachweis; Defect-Herkunft tracken und Testverteilung danach justieren.
10. **Risikobasiert priorisieren:** Testtiefe dort, wo Ausfallwirkung und
    Fehlerwahrscheinlichkeit am höchsten sind.
11. **Qualität ist Teamaufgabe:** Whole-Team-Approach statt QA-Silo; Tester früh in
    Anforderungen und Design einbinden (BDD/ATDD als Vehikel).
12. **Shift-Right:** Monitoring, Canary-Releases, Feature Flags und (bei Reife)
    Chaos-Experimente verlängern die Qualitätssicherung in die Produktion.

---

## Quellen (Recherche 2026-08-22)

**Teststufen / ISTQB-Systematik:**
[Sundream Blog](https://blog.sundreamsoftware.pl/blog/istqb/2025-10-12-test-levels/) ·
[Testsigma](https://testsigma.com/blog/levels-of-testing/) ·
[Autemos ISTQB Guide](https://www.autemos.com/en/blogs/testarten-software-testing) ·
[Art of Testing](https://artoftesting.com/levels-of-software-testing)

**Testentwurfsverfahren:**
[ISTQB Boundary Value Analysis White Paper](https://istqb.org/wp-content/uploads/2025/10/Boundary-Value-Analysis-white-paper.pdf) ·
[ASTQB Black-Box Techniques](https://astqb.org/4-2-black-box-test-techniques/) ·
[Qase Test Case Design](https://www.qase.io/blog/test-case-design-techniques/) ·
[Master Software Testing CTFL Ch.4](https://mastersoftwaretesting.com/certification-guides/istqb/ctfl/ctfl-test-analysis-design)

**Statisch/dynamisch:**
[BrowserStack](https://www.browserstack.com/guide/static-testing-vs-dynamic-testing) ·
[AccelQ](https://www.accelq.com/blog/static-testing-vs-dynamic-testing/) ·
[GeeksforGeeks](https://www.geeksforgeeks.org/software-engineering/difference-between-static-and-dynamic-testing/)

**Nicht-funktionale Tests:**
[TestRail](https://www.testrail.com/blog/non-functional-testing/) ·
[AccelQ](https://www.accelq.com/blog/non-functional-testing/) ·
[Guru99](https://www.guru99.com/non-functional-testing.html) ·
[Frugal Testing](https://www.frugaltesting.com/blog/what-is-non-functional-testing-types-importance-and-best-practices)

**Änderungsbezogene Tests:**
[Katalon](https://katalon.com/resources-center/blog/sanity-testing-vs-smoke-testing) ·
[Guru99](https://www.guru99.com/smoke-sanity-testing.html) ·
[CloudBees](https://www.cloudbees.com/blog/the-smoke-sanity-and-regression-testing-triad) ·
[Qentelli](https://qentelli.com/insights/blogs/explained-smoke-testing-vs-sanity-testing-vs-regression-testing/)

**Agile Quadrants / TDD / BDD:**
[BrowserStack](https://www.browserstack.com/guide/agile-testing-quadrants) ·
[Sogeti Labs](https://labs.sogeti.com/guiding-development-agile-testing-quadrants/) ·
[TestRail](https://www.testrail.com/blog/agile-testing-methodology/) ·
[Functionize](https://www.functionize.com/automated-testing/agile-testing-quadrants)

**Best Practices / Pyramide / Shift-Left / CI/CD:**
[Testomat](https://testomat.io/blog/testing-pyramid-role-in-modern-software-testing-strategies/) ·
[Virtuoso QA](https://www.virtuosoqa.com/post/shift-left-testing-early-with-the-sdlc) ·
[Total Shift Left](https://totalshiftleft.com/blog/shift-left-testing-complete-guide) ·
[Screendesk](https://blog.screendesk.io/software-testing-best-practices/) ·
[dotMock](https://dotmock.com/blog/software-testing-best-practices)

**Moderne Verfahren:**
[Codelit](https://codelit.io/blog/testing-strategies-architecture) ·
[SDETLab](https://www.sdetlab.com/blog/modern-test-pyramid-2026-complete-strategy) ·
[BrowserStack Chaos Testing](https://www.browserstack.com/guide/chaos-testing) ·
[BlazeMeter](https://www.blazemeter.com/blog/chaos-testing-vs-chaos-engineering) ·
[CalmOps](https://calmops.com/software-engineering/testing-strategies-modern-qa-practices/)
