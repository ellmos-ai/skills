---
name: full-after-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [deep-after-care, repo-after-care-full, tiefe-repo-pflege, repo-tiefenpflege]
description: >
  Tiefe Pflegerunde fuer ein veroeffentlichtes GitHub-Repository (Stufe 2): enthaelt den
  vollstaendigen surface-after-care-Durchlauf und ergaenzt ihn um drei teure Schritte —
  rechtliche Ersteinschaetzung ueber die Rechtsabteilung mit Wiedervorlage nach einem Jahr
  (Gutachten bleibt gitignored im Repo), Querverweise zu verwandten Repos ueber ALLE
  Organisationen hinweg sowie das Nachziehen aller Sprachen auf App-Ebene, nicht nur in der
  Doku. Nutze diesen Skill bei "full after care", "deep after care", "tiefe Repo-Pflege",
  "grosse Runde", "Repo grundlegend durchgehen", wenn ein Repo laenger nicht geprueft wurde,
  vor groesseren Releases oder wenn rechtliche Relevanz, Querverweise oder Mehrsprachigkeit
  ausdruecklich Thema sind. Fuer die guenstige, oft wiederholte Runde stattdessen
  surface-after-care; fuer die Erstveroeffentlichung github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, legal, i18n, cross-linking, organization, documentation]
language: de
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: [surface-after-care]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Full After Care — die tiefe Runde (Synonym: Deep After Care)

## Wann dieser Skill greift

Nutze ihn, wenn ein veroeffentlichtes Repo **grundlegend** durchgegangen werden soll: laenger nicht geprueft, vor einem groesseren Release, bei rechtlich relevanten Gegenstaenden, oder wenn die Verzahnung mit den uebrigen eigenen Projekten Thema ist.

Der Unterschied zur guenstigen Runde ist der Aufwand, nicht die Sorgfalt: Stufe 2 verlaesst die Grenzen des einzelnen Repos. Sie fragt Fremdquellen an (Rechtslage), inventarisiert **alle** Organisationen und greift in die Anwendung selbst ein (Sprachen). Deshalb laeuft sie seltener — typischerweise einmal pro Repo und Jahr oder anlassbezogen.

## Ablauf

### Stufe 1 zuerst vollstaendig

Fuehre **`surface-after-care` komplett aus** — inklusive Schritt 0 (Distributionsflaechen), Privacy-Gate, Veroeffentlichungsabsicht, Banner, Ist-Soll-Abgleich, README-Sprachen, Sichtbarkeit, Organisationseintrag, Issues und PRs sowie Commit, Push und Flaechen-Paritaet. Nichts davon wird hier wiederholt oder abgekuerzt.

Die drei folgenden Schritte kommen obendrauf. Sie erzeugen ihrerseits Aenderungen an Doku und Code — pushe sie im selben Rhythmus wie in Stufe 1 beschrieben, in thematisch getrennten Commits.

---

### 5. Rechtliche Ersteinschaetzung mit Jahres-Wiedervorlage

#### Zuerst: Ist eine Einschaetzung ueberhaupt faellig?

Sieh in `_after-care/RECHTSCHECK.md` nach (der Ordner ist gitignored, siehe unten). Steht dort ein Pruefdatum, das **weniger als ein Jahr** zurueckliegt, wird dieser Schritt **uebersprungen** — auch in der tiefen Runde. Eine frische Einschaetzung noch einmal einzuholen kostet Zeit und Geld und bringt nichts Neues.

Ist das Datum **aelter als ein Jahr** oder existiert die Datei nicht, wird geprueft. Der Grund fuer die Wiedervorlage ist nicht, dass das Gutachten schlechter wird, sondern dass sich die **Rechtslage** aendert: neue Verordnungen, geaenderte Schwellenwerte, neue Rechtsprechung, veraenderte Plattformregeln. Ein zwei Jahre altes Gutachten kann formal korrekt und praktisch ueberholt sein.

Ausserhalb des Jahresrhythmus ist eine Neubewertung faellig, wenn sich der **Gegenstand** geaendert hat: neue Datenkategorien, neuer Vertriebsweg, neues Geschaeftsmodell, Lizenzwechsel, neue Abhaengigkeit mit Copyleft, Ausweitung auf einen anderen Rechtsraum.

#### Ist das Repo rechtlich relevant?

Nicht jedes Projekt braucht das. Ausloeser sind unter anderem:

- verarbeitet personenbezogene Daten, auch nur lokal
- greift auf fremde Dienste, Webseiten oder Schnittstellen zu (Nutzungsbedingungen, Scraping)
- gibt Auskunft in regulierten Feldern (Recht, Medizin, Steuern, Finanzen)
- traegt fremde Marken, Namen oder Logos im Namen, in der Doku oder im UI
- enthaelt Abhaengigkeiten mit Copyleft oder unklarer Lizenz, oder liefert fremde Inhalte mit
- richtet sich an Minderjaehrige, verarbeitet Zahlungen, oder faellt unter Ausfuhr-/Kryptoregeln
- trifft automatisiert Entscheidungen ueber Menschen oder wird als KI-System eingeordnet

Trifft nichts davon zu, halte im Laufprotokoll **fest, dass geprueft und verneint wurde** — sonst stellt die naechste Runde dieselbe Frage von vorn.

#### Einschaetzung einholen

Nutze die Rechtsabteilung (Skill `rechtsabteilung`, Modul `law-checker`) und lege ihr den konkreten Sachverhalt vor: was die Anwendung tut, welche Daten sie beruehrt, ueber welche Kanaele sie vertrieben wird, welche Lizenzen mitlaufen, an wen sie sich richtet. Je konkreter der Sachverhalt, desto brauchbarer die Fundstellen. Ergebnis ist eine Ersteinschaetzung mit Paragraphen-Belegen — **keine Rechtsberatung**; bei ernsthaftem Risiko ist das Ergebnis die Empfehlung, anwaltlich pruefen zu lassen, nicht das Urteil selbst.

#### Ablage

```
_after-care/
├── LOG.md                    # Laufprotokoll beider Stufen
└── RECHTSCHECK.md            # Datum, Gegenstand, Ergebnis, Auflagen, Wiedervorlage
```

`_after-care/` gehoert in die `.gitignore`. Das ist kein Versteckspiel, sondern dieselbe Regel wie in Schritt 2b der Stufe 1: interne Arbeitsdokumente sind kein Repo-Inhalt. Bei einem Gutachten kommt hinzu, dass eine oeffentlich mitgelieferte Risikoanalyse als Eingestaendnis gelesen werden kann und Angreifern eine Landkarte liefert. Alternativ kann die Ablage ausserhalb des Repos in einem eigenen Ordner erfolgen — wichtig ist nur, dass sie beim naechsten Lauf **auffindbar** ist, sonst greift die Jahresregel nicht.

Kopfzeile der Datei, maschinell lesbar halten:

```markdown
# Rechtscheck — <Projekt>
geprueft: 2026-07-24
gegenstand: lokale Dateiverwaltung, keine Cloud, keine personenbezogenen Daten Dritter
ergebnis: unbedenklich
auflagen: Hinweis auf MIT-Lizenz der eingebetteten Bibliothek X im README
wiedervorlage: 2027-07-24
```

Was aus der Einschaetzung **oeffentlich** wird, sind nur die **Konsequenzen**: eine Lizenzangabe, ein Haftungsausschluss, ein Datenschutzhinweis, eine praezisierte Beschreibung dessen, was die App tut. Diese Aenderungen gehoeren ins Repo — die Begruendung dahinter nicht.

---

### 9. Querverweise ueber alle Organisationen

Stufe 1 fragt nur, ob das Repo auf den Organisationsseiten steht. Stufe 2 geht eine Ebene tiefer: **Welche einzelnen Repos aus allen eigenen Organisationen haengen mit diesem hier zusammen — und wissen beide Seiten davon?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

Der Ertrag entsteht nicht durch das Auflisten, sondern durch das Erkennen von Beziehungen. Relevante Typen:

- **nutzt / wird genutzt von** — echte technische Abhaengigkeit in beide Richtungen
- **gehoert zur selben Familie** — gemeinsame Produktlinie, gemeinsames Praefix, gemeinsame Architektur
- **loest dasselbe Problem anders** — ein Nutzer, der auf dem einen landet, will oft das andere kennen
- **Vorgaenger / Nachfolger** — abgeloeste Projekte brauchen einen Wegweiser, sonst landen Nutzer dauerhaft auf dem toten Stand
- **Baustein / Komposition** — Bibliothek und die Anwendung, die sie einsetzt

Setze die Verweise **bidirektional**. Eine Einbahnstrasse ist der haeufigste Fehler dieses Schritts: Man ergaenzt im gepflegten Repo eine Liste verwandter Projekte, und in den verwandten Projekten steht nichts. Wer dort landet, findet den Weg nie zurueck.

Der Rueckverweis wird im Gegen-Repo also tatsaechlich gesetzt, committet und gepusht — nach der **Dirty-Tree-Regel** aus Schritt 11 der Stufe 1: bei sauberem Arbeitsbaum in einem eigenen Commit erledigen; bei uncommitteten Fremdaenderungen oder aktiver Sperre nicht anfassen, sondern als offenen Punkt ins Laufprotokoll schreiben. Der Pflegelauf, der sich spaeter jenem Repo zuwendet, findet dort einen sauberen Baum vor und traegt es nach. So bleibt die Runde in sich abgeschlossen, ohne fremde Arbeitsstaende zu gefaehrden.

Formuliere Verweise nutzenorientiert, nicht als Namensliste: „**projekt-b** — liest die von diesem Werkzeug erzeugten Exporte und macht daraus Berichte" ist brauchbar, „siehe auch: projekt-b" nicht.

Archivierte und offensichtlich tote Repos werden nicht verlinkt — ausser als expliziter Nachfolger-Hinweis in die andere Richtung.

Diese Inventur ist der teuerste Teil der Runde. Wenn viele Organisationen und Repos zu pruefen sind, lohnt es sich, das Ergebnis der Repo-Inventur im Laufprotokoll abzulegen, damit die naechste tiefe Runde eines anderen Repos darauf aufsetzen kann.

---

### Alle Sprachen auf App-Ebene nachziehen

Stufe 1 sorgt fuer die README-Sprachfassungen. Hier geht es um das **Produkt selbst**: Oberflaechentexte, Meldungen, Hilfen, CLI-Ausgaben, Fehlermeldungen, Store- und Registry-Beschreibungen.

Ermittle zuerst, welche Sprachen die Anwendung technisch bereits kennt und wie sie sie verwaltet:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Dann die Luecken schliessen, entlang von drei Fragen:

1. **Fehlen Sprachen**, die das Projekt haben sollte? Standardsprachen sind Deutsch, Englisch, Spanisch, vereinfachtes Chinesisch, Japanisch, Russisch — bei nutzernahen Anwendungen. Bei entwicklernahen Bibliotheken ist Englisch allein oft die richtige Antwort; eine unnoetige Sprache ist dauerhafte Pflegelast, kein Gewinn.
2. **Sind die vorhandenen Sprachen vollstaendig?** Nach jedem Feature-Zyklus haengen die Nebensprachen hinterher. Neue Schluessel ohne Uebersetzung fallen im Betrieb oft auf die Leitsprache zurueck und damit gar nicht auf — deshalb hier gezielt gegen die Leitsprache diffen, statt sich auf den Augenschein zu verlassen.
3. **Ist die Sprachwahl fuer Nutzer erreichbar?** Eine vollstaendige Uebersetzung, die niemand einschalten kann, wirkt wie keine. Umschalter vorhanden, Auswahl persistent, Systemsprache als Vorgabe erkannt?

Halte dich an den im Projekt etablierten i18n-Mechanismus und fuehre keinen zweiten daneben ein. Pruefe die Ergebnisse in der **echten Oberflaeche**, nicht nur in der Ressourcendatei: zu lange Zeichenketten brechen Layouts, und fehlende Zeichensatz-Unterstuetzung zeigt sich erst im Rendering (fehlende CJK-Glyphen erscheinen als leere Kaesten).

Zum Schluss die Flaechen aus Schritt 0 der Stufe 1 mitnehmen: Store- und Registry-Beschreibungen haben eigene Sprachfelder, die von der App-Uebersetzung nicht automatisch mitwandern.

## Laufprotokoll

Ergaenze `_after-care/LOG.md` um einen Eintrag mit der Stufe `full`:

```markdown
## 2026-07-24 — full
- Stufe 1 vollstaendig gelaufen (siehe Eintrag oben)
- Rechtscheck: faellig (letzter 2025-06-02) -> neu eingeholt, Ergebnis unbedenklich,
  Auflage Lizenzhinweis Bibliothek X umgesetzt, Wiedervorlage 2027-07-24
- Querverweise: 4 Orgas / 38 Repos geprueft, 3 Beziehungen gefunden,
  bidirektional gesetzt; Rueckverweis in repo-y offen (dort aktiver Lock)
- Sprachen App-Ebene: ES ergaenzt (312 Schluessel), JA auf Stand gebracht,
  Umschalter war vorhanden aber nicht persistent -> gefixt
```

## Haeufige Fehler

| Fehler | Korrektur |
|---|---|
| Rechtscheck erneut eingeholt, obwohl der letzte 3 Monate alt war | Datum in `RECHTSCHECK.md` zuerst lesen — unter einem Jahr wird uebersprungen |
| Rechtscheck uebersprungen, weil „hat sich nichts geaendert" | Die Rechtslage aendert sich unabhaengig vom Projekt; ab einem Jahr wird geprueft |
| Gutachten ins Repo committet | `_after-care/` gehoert in die `.gitignore`; oeffentlich werden nur die Konsequenzen |
| Verneinte Rechtsrelevanz nicht dokumentiert | Auch ein „nicht relevant" ist ein Befund und gehoert ins Protokoll |
| Querverweise nur im gepflegten Repo gesetzt | Bidirektional setzen, sonst ist es eine Einbahnstrasse |
| Nur die eigene Orga geprueft | Stufe 2 heisst alle Organisationen — genau das unterscheidet sie von Stufe 1 |
| Verweise als blosse Namensliste | Nutzen in einem Halbsatz erklaeren, sonst klickt niemand |
| Neue Sprache angelegt, aber nicht im UI erreichbar | Umschalter, Persistenz und Systemsprachen-Erkennung mitpruefen |
| Uebersetzung nur in der Ressourcendatei geprueft | In der echten Oberflaeche pruefen — Layoutbrueche und fehlende Glyphen zeigen sich erst dort |
| Store-/Registry-Sprachfelder vergessen | Sie wandern nicht mit der App-Uebersetzung mit |

## Abschluss-Checkliste

- [ ] `surface-after-care` vollstaendig durchlaufen (inkl. Push und Flaechen-Paritaet).
- [ ] Rechtsrelevanz geprueft; Ergebnis dokumentiert — auch wenn verneint.
- [ ] Rechtscheck faellig gewesen? Wenn ja: eingeholt, Auflagen umgesetzt, Wiedervorlage gesetzt.
- [ ] `_after-care/` in der `.gitignore`, Gutachten nicht getrackt.
- [ ] Alle Organisationen inventarisiert, Beziehungen bestimmt.
- [ ] Querverweise bidirektional gesetzt, in den Gegen-Repos committet und gepusht.
- [ ] Wegen dirty tree oder Sperre uebersprungene Gegen-Repos als offene Punkte notiert.
- [ ] App-Sprachen vollstaendig, Umschalter erreichbar, in der Oberflaeche geprueft.
- [ ] Store-/Registry-Sprachfelder mitgezogen.
- [ ] Laufprotokoll-Eintrag mit Stufe `full` geschrieben.

## Changelog

### 1.0.0 (2026-07-24)
- Initiale Version. Stufe 2 der Repo-Nachpflege, aufbauend auf `surface-after-care`.
