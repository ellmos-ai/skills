# Rechtliche Prüfung — 2026-08-02

> *This document is in German because it examines German and EU statutes; quoting
> them in translation would be less accurate, not more accessible.*

Prüfer: Claude Opus 5 | Skill `rechtsabteilung` v1.1, law-checker config v6
Typ: Inhaltsprüfung (Architekturmuster vor Inbetriebnahme)
Auftrag: Prüfung des Huckepack-Hostingmusters im Zuge seiner Umsetzung in
HungryCall, Ringedingeding und ResearchCall (2026-08-02). Geprüfte Dokumente:
`KONZEPT.md`, `README.md`, die drei `DATA-FLOW.md` und der umgesetzte Code
(Serverart, Speicherschicht, Schlüsseldurchreichung).
Gesetzbücher (aktiv, herangezogen): DSGVO (EUR-Lex 02016R0679, abgerufen
2026-07-19) · TDDDG (gesetze-im-internet.de, abgerufen 2026-08-02) · UWG
(abgerufen 2026-07-11).
Review: keins (kein Fremdmodell-Review durchgeführt).

---

## 1. Gegenstand und Prüfungsrahmen

Das Muster verlagert die dauerhafte Speicherung der Nutzerdaten in den Browser
des Nutzers; der Host führt die Datenbank nur im Arbeitsspeicher einer Sitzung
und schreibt keine Datei. Daraus leitet `README.md` ab, die Nutzerverwaltung
werde **gegenstandslos**. Alle drei Anwendungen rufen dabei **Dritte** an.

Drei Prüffragen:

1. **Trägt die Behauptung**, dass in `huckepack-gift` und `huckepack-only-host`
   keine Nutzerverwaltung nötig ist?
2. **Was bleibt trotzdem Pflicht**, weil Dritte angerufen werden?
3. **Wo verläuft die Haushaltsausnahme** — und wem nützt sie?

Vorab benannter Prüfungsrahmen: Art. 2 Abs. 2 lit. c, Art. 4 Nr. 1, 2, 7,
Art. 6 Abs. 1, Art. 11, Art. 13, Art. 14, Art. 24 Abs. 1, Art. 26 Abs. 1,
Art. 28, Art. 30 Abs. 5, Art. 32 Abs. 1, Art. 33 DSGVO · § 25 TDDDG ·
§ 7 Abs. 2 UWG.

---

## 2. Rechtliche Einschätzung

### 2.1 Der Hoster bleibt Verantwortlicher — auch wenn er nichts speichert

> Art. 4 Nr. 7 DSGVO: „‚Verantwortlicher' die natürliche oder juristische
> Person, Behörde, Einrichtung oder andere Stelle, die allein oder gemeinsam
> mit anderen **über die Zwecke und Mittel der Verarbeitung** von
> personenbezogenen Daten **entscheidet**"
> (Quelle: `DSGVO.txt`, Artikel 4, abgerufen 2026-07-19)

Die Norm knüpft an die **Entscheidung über Zwecke und Mittel** an, nicht an
Speicherung. Der EuGH hat das ausdrücklich bestätigt:

> EuGH, Urteil der Großen Kammer vom 05.12.2023 — C-683/21 (Nacionalinis
> visuomenės sveikatos centras), ECLI:EU:C:2023:949, Tenor: eine Einrichtung
> kann Verantwortlicher sein, „even if that entity has not itself performed any
> processing operations in respect of such data, has not expressly agreed to the
> performance of specific operations for such processing or to that mobile
> application being made available to the public, and has not acquired the
> abovementioned mobile application."
> Fundstelle: eur-lex.europa.eu, CELEX 62021CJ0683 (abgerufen 2026-08-02)

**Verdikt:** Wer eine dieser Anwendungen hostet, entscheidet über Zweck (Anruf
bei einem Betrieb, bei Eingeladenen, bei Studienteilnehmern) und Mittel
(CALL-E, Gesprächsaufbau, Transkript) und ist damit Verantwortlicher — die
Browser-Speicherung ändert daran nichts. Die Aussage „Der Host speichert
nichts" ist zutreffend und wird durch die Tests belegt; die Aussage „damit ist
er nicht mehr beteiligt" wäre falsch. Die Umsetzung formuliert das inzwischen
selbst so (`DATA-FLOW.md`, Abschnitt „Boundaries that remain").

**Verdikt:** Der Wegfall der **Nutzerverwaltung** trägt trotzdem — aber in
engerem Umfang als der Satz vermuten lässt: Er trägt für die **Daten der
Nutzer**, nicht für die Verarbeitung, die der Dienst auslöst.

### 2.2 Was durch die Verlagerung tatsächlich entfällt

| Pflicht | Norm | Wirkung der Verlagerung |
|---|---|---|
| Zugriffsschutz zwischen Nutzern, Kontenführung, Löschfristen für Nutzerbestände | Art. 5 Abs. 1 lit. f, Art. 17, Art. 32 DSGVO | **entfällt weitgehend** — ohne serverseitigen Bestand gibt es keinen fremden Bestand zu trennen oder zu löschen (*Verdikt*) |
| Verzeichnis von Verarbeitungstätigkeiten | Art. 30 Abs. 5 DSGVO: Pflicht entfällt bei < 250 Beschäftigten, „**es sei denn** … die Verarbeitung erfolgt nicht nur gelegentlich" | **entfällt nicht** — ein laufend angebotener Dienst verarbeitet nicht „nur gelegentlich" (*Hypothese*, im Einzelfall zu prüfen) |
| Technische und organisatorische Maßnahmen | Art. 32 Abs. 1 DSGVO | **verkleinert sich, entfällt nicht**: der Transit, der Arbeitsspeicher, die Session-Token und die Weitergabe an CALL-E bleiben zu schützen (*Verdikt*) |
| Meldung von Datenschutzverletzungen | Art. 33 DSGVO | **bleibt** für alles, was der Host verarbeitet; die Angriffsfläche schrumpft, die Pflicht nicht (*Verdikt*) |

### 2.3 Was bleibt, weil Dritte angerufen werden

Der Angerufene hat seine Daten nicht selbst hergegeben. Damit gilt:

> Art. 14 Abs. 1 DSGVO: „Werden personenbezogene Daten nicht bei der betroffenen
> Person erhoben, so teilt der Verantwortliche der betroffenen Person Folgendes
> mit: a) den Namen und die Kontaktdaten des Verantwortlichen … c) die Zwecke,
> für die die personenbezogenen Daten verarbeitet werden sollen, sowie die
> Rechtsgrundlage für die Verarbeitung …"
> (Quelle: `DSGVO.txt`, Artikel 14, abgerufen 2026-07-19)

Dazu die Rechtsgrundlage für den Anruf selbst — regelmäßig Art. 6 Abs. 1
lit. f DSGVO („zur Wahrung der berechtigten Interessen … erforderlich, sofern
nicht die Interessen oder Grundrechte und Grundfreiheiten der betroffenen
Person … überwiegen"), die eine **dokumentierte Abwägung** verlangt, sowie
Art. 24 Abs. 1 DSGVO (Nachweispflicht des Verantwortlichen) und ein
Auftragsverarbeitungsvertrag mit dem Anrufdienst (Art. 28).

**Verdikt:** Genau die Abschnitte einer Datenschutzerklärung, die den
Angerufenen betreffen, werden vom Muster **nicht kürzer** — sie sind die
längsten. Die drei `PRIVACY-TEMPLATE.md` weisen das inzwischen aus.

**Prüfauftrag:** Ob Hoster und Nutzer gemeinsam über Zwecke und Mittel
entscheiden (Art. 26 Abs. 1 DSGVO: „Legen zwei oder mehr Verantwortliche
gemeinsam die Zwecke der und die Mittel zur Verarbeitung fest, so sind sie
gemeinsam Verantwortliche"), hängt von der konkreten Installation ab. In
`huckepack-only-host` — der Nutzer zahlt, der Hoster stellt Oberfläche und
Ausführung — liegt gemeinsame Verantwortlichkeit näher als in `local`. Das ist
vor Inbetriebnahme zu klären, nicht danach.

### 2.4 Betroffenenrechte, wenn niemand mehr etwas nachschlagen kann

Hier gibt es eine Norm, die genau diesen Fall regelt:

> Art. 11 Abs. 1 DSGVO: „Ist für die Zwecke, für die ein Verantwortlicher
> personenbezogene Daten verarbeitet, die Identifizierung der betroffenen Person
> durch den Verantwortlichen nicht oder nicht mehr erforderlich, so ist dieser
> nicht verpflichtet, zur bloßen Einhaltung dieser Verordnung zusätzliche
> Informationen aufzubewahren …"
> Abs. 2: „… so unterrichtet er die betroffene Person hierüber, sofern möglich.
> In diesen Fällen finden die Artikel 15 bis 20 keine Anwendung, es sei denn,
> die betroffene Person stellt … zusätzliche Informationen bereit."
> (Quelle: `DSGVO.txt`, Artikel 11, abgerufen 2026-07-19)

**Verdikt:** Der Host muss nicht anfangen zu speichern, nur um auskunftsfähig
zu werden — Art. 11 Abs. 1 sagt das ausdrücklich. **Prüfauftrag:** Art. 11
befreit nicht von der Unterrichtung nach Abs. 2 und nicht davon, dass ein
Widerspruch des Angerufenen (Art. 21) beim laufenden Betrieb wirksam werden
muss. Für ResearchCall ist das mehr als Formalie: Ein Studienwiderruf, der
niemanden erreicht, ist ein Einwilligungsproblem, kein Dokumentationsproblem.

### 2.5 Speicherung im Browser — § 25 TDDDG

> § 25 Abs. 1 TDDDG: „Die Speicherung von Informationen in der Endeinrichtung
> des Endnutzers oder der Zugriff auf Informationen, die bereits in der
> Endeinrichtung gespeichert sind, sind nur zulässig, wenn der Endnutzer auf der
> Grundlage von klaren und umfassenden Informationen eingewilligt hat."
> Abs. 2 Nr. 2: „Die Einwilligung nach Absatz 1 ist nicht erforderlich, … wenn
> die Speicherung … **unbedingt erforderlich ist, damit der Anbieter eines
> digitalen Dienstes einen vom Nutzer ausdrücklich gewünschten digitalen Dienst
> zur Verfügung stellen kann.**"
> (Quelle: `TDDDG.txt`, § 25, abgerufen 2026-08-02)

Subsumtion je Eintrag:

| Was im Browser liegt | Unbedingt erforderlich für den gewünschten Dienst? | Label |
|---|---|---|
| `huckepack` (IndexedDB): die Datenbank des Nutzers | Ja — sie **ist** der Dienst; ohne sie gibt es keinen Bestand, den der Nutzer führen wollte | Hypothese, gut begründbar |
| `huckepack.session`: Sitzungs-Token | Ja — adressiert die eigene Arbeitskopie; ohne ihn keine Zuordnung | Hypothese |
| `huckepack.calle-key`: eigener API-Schlüssel | Ja im Modus `only-host` — ohne ihn ist kein Anruf möglich | Hypothese |
| Ordner-Handle für Belege | Nein — reiner Komfort; ohne ihn funktioniert der Download weiter | **Prüfauftrag**: hier ist die Ausnahme am schwächsten |
| Sprache, Farbschema | Vorhandene Praxis, unverändert | Prüfauftrag |

**Verdikt:** Für die tragenden Einträge sprechen gute Argumente für die
Ausnahme des Abs. 2 Nr. 2 — es handelt sich um Daten des Nutzers für die
Funktion, die er ausdrücklich angefordert hat, ohne Analyse- oder Werbezweck.
**Das ist ein Argument, kein Befund**; die Vorlagen sagen das so. Einschlägige
Rechtsprechung speziell zu nutzereigener Datenhaltung im Browser: **nicht
ermittelt**.

### 2.6 Die Haushaltsausnahme — sie hilft dem Nutzer, nicht dem Hoster

> Art. 2 Abs. 2 lit. c DSGVO: „Diese Verordnung findet keine Anwendung auf die
> Verarbeitung personenbezogener Daten … **durch natürliche Personen zur
> Ausübung ausschließlich persönlicher oder familiärer Tätigkeiten**"
> (Quelle: `DSGVO.txt`, Artikel 2, abgerufen 2026-07-19)

> EuGH, Urteil vom 11.12.2014 — C-212/13 (Ryneš), ECLI:EU:C:2014:2428:
> Videoüberwachung, die sich auch nur teilweise auf den öffentlichen Raum
> erstreckt und damit auf einen Bereich außerhalb der privaten Sphäre des
> Verarbeitenden richtet, ist keine ausschließlich persönliche oder familiäre
> Tätigkeit. Fundstelle: dejure.org / eurolawyer.at (abgerufen 2026-08-02)

Die Grenze verläuft damit **nicht zwischen den Modi, sondern zwischen den
Personen**:

| Konstellation | Haushaltsausnahme? | Begründung |
|---|---|---|
| Privatperson bestellt mit HungryCall lokal ihr Abendessen | greift voraussichtlich (*Hypothese*) | natürliche Person, persönliche Tätigkeit; der angerufene Betrieb ist geschäftlicher Kontakt, kein fremder Datenbestand |
| Privatperson fragt mit Ringedingeding Freunde nach einem Termin | greift voraussichtlich (*Hypothese*), **Grenze**: fremde Rufnummern werden verarbeitet und die Angerufenen sollten wissen, dass ein Agent anruft | nach Ryneš eng auszulegen, sobald der eigene Kreis verlassen wird |
| Verein/Firma nutzt Ringedingeding für Mitglieder oder Kunden | **greift nicht** (*Verdikt*) | keine ausschließlich persönliche Tätigkeit |
| ResearchCall für eine Studie | **greift nicht** (*Verdikt*) | Forschung ist keine persönliche oder familiäre Tätigkeit |
| **Jemand hostet eine der Apps für andere** (`huckepack-gift`, `only-host`) | **greift nicht** (*Verdikt*) | Ein Dienst für Dritte ist keine ausschließlich persönliche Tätigkeit — auch dann nicht, wenn der Betreiber Privatperson ist und nichts speichert |

**Das ist die eigentliche Antwort auf die dritte Frage:** Die Haushaltsausnahme
rechtfertigt den **lokalen** Betrieb (`local`) durch eine Privatperson. Sie
rechtfertigt gerade **nicht** den Huckepack-Betrieb — der beginnt dort, wo
jemand einen Dienst für andere bereitstellt. Das Muster löst also nicht das
Problem, für das die Haushaltsausnahme da ist; es reduziert das, was beim
Anbieter liegt.

### 2.7 Vergleichsansatz: Welche Pflichten entstehen HIER, die privat nicht bestünden?

Gegenüber der Privatperson, die für sich selbst anruft, entstehen dem Hoster
zusätzlich: Informationspflicht gegenüber Angerufenen (Art. 14), Rechtsgrundlage
mit dokumentierter Abwägung (Art. 6 Abs. 1 lit. f), Nachweispflicht (Art. 24
Abs. 1), Auftragsverarbeitungsvertrag mit dem Anrufdienst (Art. 28), TOM für
Transit und Arbeitsspeicher (Art. 32), Meldewege (Art. 33), Datenschutz-
erklärung, sowie — bei entsprechendem Zuschnitt — eine Vereinbarung nach
Art. 26 Abs. 1.

### 2.8 Am Rande, aber nicht zu übersehen: Werbeanrufe

> § 7 Abs. 2 Nr. 1 UWG: „Eine unzumutbare Belästigung ist stets anzunehmen …
> bei Werbung mit einem Telefonanruf gegenüber einem Verbraucher ohne dessen
> vorherige ausdrückliche Einwilligung oder gegenüber einem sonstigen
> Marktteilnehmer ohne dessen zumindest mutmaßliche Einwilligung"
> (Quelle: `UWG.txt`, § 7, abgerufen 2026-07-11)

**Prüfauftrag:** Eine Bestellung oder Terminfrage ist keine Werbung. Sobald ein
Betreiber die Anwendungen aber für Ansprache im geschäftlichen Interesse
einsetzt — und in der Rechtsprechung wird der Werbebegriff weit verstanden —,
steht § 7 UWG im Raum, unabhängig von jeder Datenschutzfrage. Konkrete
Rechtsprechung zur Einordnung automatisierter Umfrageanrufe: **nicht
ermittelt**.

---

## 3. Risikoeinschätzung

| Risiko | Ampel | Begründung |
|---|---|---|
| Missverständnis „Host speichert nichts ⇒ Host ist nicht verantwortlich" | **Hoch** | C-683/21 ist eindeutig; ein danach gebauter Betrieb ohne Datenschutzerklärung und ohne Art.-14-Konzept wäre angreifbar |
| Fehlende Information der Angerufenen (Art. 13/14) | **Hoch** | betrifft Menschen, die sich nicht selbst gemeldet haben; bei ResearchCall zusätzlich Ethik/Einwilligung |
| Endgeräte-Speicherung ohne Einwilligung (§ 25 TDDDG) | **Mittel** | für die tragenden Einträge gut begründbar, für den Komfort-Eintrag (Ordner-Handle) schwächer |
| Unverschlüsselte Exportdatei mit Klar-Rufnummern | **Mittel** | technisch gewollt (Verlust wäre schlimmer), aber Nutzer müssen es wissen — steht jetzt in allen drei Vorlagen |
| Verlust der Nutzerdaten durch gelöschte Browserdaten | **Mittel** | kein Rechts-, sondern ein Erwartungsrisiko; Export ist umgesetzt und wird angesagt |
| Sitzungs-Token erratbar | **Gering** | serverseitig auf ≥ 22 Zeichen URL-sicheres Alphabet geprüft; Inhalt ist nur die flüchtige Arbeitskopie |
| `pay-membership` als Stub | **Gering** | verweigert den Dienst sichtbar (503) statt so zu tun |

**Fristen:** keine. Es liegt keine Rechtspost und kein laufendes Verfahren vor.

---

## 4. Empfehlung

**Umsetzen, mit drei Auflagen vor dem ersten öffentlichen Betrieb:**

1. **Datenschutzerklärung ausfüllen** — die drei `PRIVACY-TEMPLATE.md` sind
   Muster mit Platzhaltern; sie ersetzen nichts, solange `[REPLACE: …]`
   darin steht.
2. **Art.-14-Konzept für die Angerufenen** — was wird im Gespräch gesagt, wo
   steht die vollständige Information, wie wirkt ein Widerspruch. Das ist der
   Punkt, den das Muster nicht verkleinert.
3. **Rolle klären** (Art. 26 DSGVO) — insbesondere für `only-host`, wo der
   Nutzer zahlt und der Hoster den Anruf komponiert.

**Anwalt einschalten** bei tatsächlicher Inbetriebnahme mit echten Anrufen an
Dritte oder bei ResearchCall mit Studienteilnehmern: Fachgebiet **IT-Recht /
Datenschutzrecht**, für ResearchCall zusätzlich Forschungsethik. Grund: Die
Risiken „Hoch" betreffen Rechte Dritter, nicht nur eigene Compliance.

**Stärkste Gegenposition (Steelman):** Man könnte einwenden, das Muster
verändere die Rechtslage überhaupt nicht und sei damit rechtlich wertlos —
verantwortlich bleibe der Hoster ohnehin. Das trifft für die
**Verantwortlichkeit** zu und ist die wichtigste Korrektur an der
Ausgangsthese. Es übersieht aber, dass Datenschutzrecht risikobasiert ist
(Art. 24 Abs. 1, Art. 32 Abs. 1 stellen ausdrücklich auf Art, Umfang und
Risiko ab): Wer keinen fremden Bestand führt, hat keinen zu verlieren, keinen
zu trennen und keinen zu löschen. Der Gewinn liegt in der **Menge der
Pflichten und der Schadenshöhe**, nicht in ihrer Art.

---

## 5. Grenzen dieser Einschätzung

KI-gestützte Erstorientierung, kein Ersatz für die individuelle Prüfung durch
eine zugelassene Rechtsanwältin oder einen zugelassenen Rechtsanwalt. Ob ein
konkreter Einsatz eine Rechtsdienstleistung darstellt und zulässig ist, hängt
von Einsatzform, Betreiberrolle und Einzelfall ab. Keine Fristüberwachung,
keine Vollständigkeits- oder Aktualitätsgarantie — bei Rechtspost und
laufenden Fristen sofort professionelle Beratung. Bei Risikoeinschätzung „Hoch"
oder „Kritisch" wird die Einschaltung eines Fachanwalts empfohlen.

**Was nicht geprüft wurde:**

- **Herangezogen:** DSGVO, TDDDG, UWG.
- **Aktiv in der Registry, hier nicht herangezogen** (jeweils kein Bezug zum
  Prüfgegenstand): GG, BGB (keine Vertragsfrage geprüft — die Frage, ob eine
  telefonisch vom Agenten aufgegebene Bestellung den Nutzer bindet, ist
  **offen** und eigenständig prüfbedürftig), SGB V, UrhG, RDG, MarkenG,
  StBerG, EHDS-VO, GRCh. **Deaktiviert:** StGB, MStV.
- **Fehlend:** BDSG (nicht in der Registry — Konkretisierungen des nationalen
  Rechts, u. a. zur Datenschutzbeauftragten-Pflicht, blieben ungeprüft).
  Ebenso ungeprüft: Telefonaufzeichnungs-/Transkriptionsrecht (§ 201 StGB wäre
  einschlägig, StGB ist deaktiviert), Verbraucherschutz- und Fernabsatzrecht,
  Recht außerhalb Deutschlands.
- **Rechtsprechung:** zwei Entscheidungen web-verifiziert (siehe 6b). Zu
  § 25 TDDDG und nutzereigener Browser-Datenhaltung sowie zu automatisierten
  Umfrageanrufen unter § 7 UWG wurde **keine** Entscheidung ermittelt — das ist
  ein Befund, keine Entwarnung.
- **Offene Tatsachenfragen:** Rechtsform und Sitz des Anrufdienstes, dessen
  Aufbewahrungsfristen, Unterauftragnehmer und Drittlandbezug. Diese Angaben
  stehen in keinem der Repositorien und müssen vertraglich beschafft werden.

---

## 6. Recherchequellen

**(a) Normtexte (lokal, Modul law-checker):**

- `_data/gesetze/DSGVO.txt` — EUR-Lex, konsolidierte Fassung 02016R0679-20160504,
  abgerufen 2026-07-19
- `_data/gesetze/TDDDG.txt` — gesetze-im-internet.de (Kurzpfad `ttdsg`),
  abgerufen 2026-08-02, im Zuge dieser Prüfung neu in die Registry aufgenommen
  (config v5 → v6)
- `_data/gesetze/UWG.txt` — gesetze-im-internet.de, abgerufen 2026-07-11

**(b) Rechtsprechung (web-verifiziert am 2026-08-02):**

- EuGH, 05.12.2023, C-683/21 (Nacionalinis visuomenės sveikatos centras),
  ECLI:EU:C:2023:949 — Verantwortlicher auch ohne eigene Verarbeitung.
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:62021CJ0683
- EuGH, 11.12.2014, C-212/13 (Ryneš), ECLI:EU:C:2014:2428 — enge Auslegung der
  Haushaltsausnahme. https://dejure.org/dienste/vernetzung/rechtsprechung?Text=ECLI:EU:C:2014:2428

**(c) Amtliche Quellen:** gesetze-im-internet.de (BMJ), EUR-Lex.

**(d) Sekundärquellen:** keine herangezogen.
