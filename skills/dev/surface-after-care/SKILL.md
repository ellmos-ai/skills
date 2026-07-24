---
name: surface-after-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [repo-after-care, repo-pflege, after-care, repo-nachpflege, repo-wartung]
description: >
  Regelmaessiger Pflegedurchlauf fuer ein bereits veroeffentlichtes GitHub-Repository (Stufe 1,
  guenstig und oft wiederholbar): zuerst alle Distributionsflaechen des Projekts ermitteln
  (npm, PyPI, Registries, Marketplaces, Stores, Website) und Aenderungen spaeter dorthin spiegeln,
  dann Topics setzen, Privacy-Gate, Dokumente auf Veroeffentlichungsabsicht pruefen und interne
  Planungsdateien nachtraeglich ignorieren, Banner ergaenzen, Aussagen im README gegen den echten
  Code-Stand abgleichen, Darstellung verbessern, Sprachfassungen der README vervollstaendigen,
  Sichtbarkeitsmassnahmen umsetzen, Eintrag auf der Organisationsseite pruefen sowie offene
  Issues und Pull Requests abarbeiten.
  Nutze diesen Skill, wenn ein bestehendes Repo gepflegt, aufgeraeumt, aktualisiert, aufgehuebscht
  oder "mal wieder durchgesehen" werden soll, wenn ein Repo veraltet oder unaufgeraeumt wirkt,
  bei Formulierungen wie "Repo-Pflege", "after care", "Nachpflege", "Repo auf Stand bringen",
  "aufraeumen und pushen" oder bei rotierenden Qualitaetsrunden ueber mehrere Repos.
  Fuer die tiefe Runde inkl. Rechtscheck und orga-uebergreifenden Querverweisen stattdessen
  full-after-care nutzen; fuer die Erstveroeffentlichung github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, privacy, i18n, documentation, visibility, issues]
language: de
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
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

# Surface After Care — die regelmaessige Pflegerunde fuer ein veroeffentlichtes Repo

## Wann dieser Skill greift

Nutze ihn fuer ein Repository, das **bereits oeffentlich ist** und turnusmaessig durchgesehen werden soll. Er ist die guenstige Stufe: alles, was sich am Repo selbst entscheiden laesst, ohne fremde Repos zu inventarisieren oder ein Rechtsgutachten anzustossen.

Abgrenzung zu den Nachbarskills:

| Situation | Skill |
|---|---|
| Repo wird zum ersten Mal veroeffentlicht | `github-repo-care` |
| Repo ist public, regelmaessige Pflegerunde | **dieser Skill** |
| Zusaetzlich Rechtscheck + Querverweise ueber alle Orgas + App-i18n | `full-after-care` (Alias `deep-after-care`) |
| Reine Rechts-/Privacy-/Lizenzpruefung vor dem Public-Stellen | `repo-publish-check` |
| Sprachfassungen inhaltlich synchron halten | `bilingual-doc-sync` |
| Verteilung dieser Runde ueber viele Repos, fair rotierend | `rotation-check` |

## Kernidee

Ein veroeffentlichtes Repo driftet in zwei Richtungen auseinander: **Die Doku beschreibt eine aeltere Software als die, die im Repo liegt**, und **es sammeln sich Dateien an, die nie fuer fremde Augen gedacht waren**. Beides ist selten dramatisch, aber beides kostet genau die Nutzer, die man gewinnen will — der eine springt ab, weil die Installationsanleitung nicht mehr passt, der andere, weil er im Wurzelverzeichnis auf `AUFGABEN.txt` und `Plan.txt` stoesst und den Eindruck bekommt, hier arbeite jemand nur fuer sich selbst.

Diese Runde raeumt beides auf. Sie ist bewusst wiederholbar: lieber viermal im Jahr eine halbe Stunde als einmal ein Grossputz.

## Ablauf

Die Reihenfolge ist nicht willkuerlich. Schritt 0 steht am Anfang, weil er den Umfang aller folgenden Schritte bestimmt. Schritt 2 laeuft vor allem, was Aenderungen pusht — sonst schiebt man Verbesserungen ueber einen Stand, der erst noch bereinigt werden muss. Schritt 1 ist rein serverseitig und stoert dabei nicht.

### 0. Distributionsflaechen inventarisieren

**Bevor irgendetwas geaendert wird: klaeren, wo dieses Projekt ueberall liegt.** Das GitHub-Repo ist selten die einzige Flaeche. Eine korrigierte README nuetzt wenig, wenn die npm-Paketseite weiter die alte Fassung mit der falschen Installationsanweisung zeigt — und genau dort landen die meisten Nutzer, denn Paketregister ranken in Suchmaschinen oft besser als das Repo.

```bash
# Manifeste verraten die Kanaele
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veroeffentlichten Stand der Kanaele abfragen (nur was zutrifft)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Typische Flaechen: npm, PyPI, Crates, Docker Hub, MCP-Registry, Plugin-/Skill-Verzeichnisse, VS-Code- oder Browser-Marketplaces, App-Stores, Zenodo/DOI, Projektwebsite, Organisationsprofil, `llms.txt`, Spiegel-Repos auf anderen Hosts.

Notiere die gefundene Liste im Laufprotokoll. Sie ist ab jetzt die **Zielmenge**: Jede Aenderung aus den folgenden Schritten wird am Ende gegen diese Liste gespiegelt (siehe „Paritaet ueber alle Flaechen"). Findest du eine Flaeche, die niemand mehr pflegt und die auf einen toten Stand zeigt, ist das ein eigener Befund — entweder aktualisieren oder bewusst zurueckziehen, aber nicht stehen lassen.

### 1. Topics setzen

Topics sind die wichtigste Suchflaeche innerhalb von GitHub und kosten fast nichts.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

Ziel sind ungefaehr 5–12 Topics aus drei Richtungen: **was es ist** (`cli`, `mcp-server`, `python-library`), **worum es geht** (`file-management`, `tax`, `note-taking`) und **wie es arbeitet** (`local-first`, `offline`, `privacy`). Orientiere dich an Topics, die bei vergleichbaren Projekten tatsaechlich verwendet werden — erfundene Topics finden keine Nutzer. Description und Homepage gleich mitpruefen, sie stehen in derselben Ansicht.

Topics haben auf den anderen Flaechen aus Schritt 0 ein Pendant: `keywords` in `package.json`, `keywords`/`classifiers` in `pyproject.toml`, Kategorien und Tags in Marketplaces und Stores. Halte sie inhaltlich gleich — sie sind dieselbe Entscheidung, nur an mehreren Orten.

### 2a. Privacy-Gate — laeuft immer

Dieser Schritt entfaellt nie, auch nicht bei einer scheinbar harmlosen Runde. Gesucht wird im **getrackten** Set, nicht im sichtbaren Arbeitsbaum, denn genau das ist der Unterschied zwischen "sieht sauber aus" und "ist sauber".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Fuendig geworden? Dann entscheidet die **Art** des Fundes ueber das Vorgehen — siehe Abschnitt „Force-Push-Regel". Ein Secret, das jemals committet wurde, ist verbrannt: Entfernen aus `HEAD` genuegt nicht, es muss rotiert werden.

### 2b. Veroeffentlichungsabsicht der Dokumente pruefen

Der eigentliche Kern dieser Runde. Gehe die getrackten `.md`, `.txt` und `.json` durch und frage bei jeder Datei: **War die je fuer Fremde gedacht?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Nicht anhand des Dateinamens raten — kurz hineinsehen. Ein `PLAN.md` kann eine oeffentliche Roadmap sein, ein harmlos klingendes `notes.md` die interne Preisstrategie. Drei Kategorien:

**Gehoert ins Repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, API-Referenzen, Beispiel-Configs, echte Roadmaps, Manifeste (`package.json`, `pyproject.toml`), Lockfiles, CI-Konfiguration.

**Gehoert nicht ins Repo, ist aber unkritisch** — der Normalfall dieser Runde. Aufgaben- und Planungsdateien (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), Session-Notizen und Uebergaben (`HANDOFF`, `BRIEFING`, `_handoff/`), Statusdateien der eigenen Pipeline, Entwicklungstagebuecher, `_archive/`, Registry- und Index-JSONs mit lokalen Pfaden, Zwischenstaende und generierte Artefakte, Agenten-Arbeitsdateien. Solche Dateien sind nicht gefaehrlich, aber sie erzeugen Unuebersichtlichkeit und den Eindruck einer fremden Baustelle. Behandlung: `.gitignore` ergaenzen, `git rm --cached <datei>` und **ganz normal pushen**.

**Gehoert nicht ins Repo und ist heikel** — Credentials, personenbezogene Daten, Kundendaten, interne Kalkulationen, Preis- und Verhandlungsstrategien, unveroeffentlichte Geschaeftsplaene, Vertragsentwuerfe, alles mit Wettbewerbswert. Hier reicht ein normaler Commit nicht, siehe Force-Push-Regel.

Bei `.json` lohnt ein zweiter Blick: Manifeste und Lockfiles bleiben, aber lokale Configs, Task-/Registry-Dateien, Export-Dumps und alles mit absoluten Pfaden oder Hostnamen sind typische blinde Passagiere.

Wenn du eine Datei entfernst, die jemand suchen koennte (eine Roadmap etwa), erwaehne im Commit oder im README kurz, wo die Information jetzt lebt — sonst wirkt es wie ein Rueckschritt.

### 3. Banner

Ein Banner entscheidet mit darueber, ob jemand ueberhaupt anfaengt zu lesen. Pruefe, ob eines existiert und im README als erstes Element eingebunden ist.

Fehlt es, gibt es drei Wege — in dieser Reihenfolge sinnvoll:

1. **Bildgenerator eines Agenten** (z. B. agy; das Wort „generiere" ist dort der Trigger fuer echte PNG-Erzeugung), wenn ein Bildmotiv besser passt als Typografie.
2. **Codex**, wenn das Banner aus Code entstehen soll und ein Stilvorbild existiert, an dem es sich orientieren kann.
3. **Selbst als SVG**, wenn das Banner primaer Wortmarke plus Formsprache ist — das ist oft die schnellste und am besten kontrollierbare Variante, und SVG bleibt spaeter aenderbar.

Halte die Familie ein, wenn das Projekt zu einer Gruppe gehoert: gleiche Grundfarbe, gleiche Aesthetik, gleiche Wortmarken-Behandlung. Ein Banner, das aus der Reihe faellt, wirkt schlechter als keines. Uebliche Groesse 1200x300; als PNG ins Repo, das SVG als Quelle daneben.

### 4. Aussagen gegen den echten Stand abgleichen

Hier entsteht der meiste Wert. Das README behauptet Dinge — pruefe sie nach, statt sie zu glauben:

- **Version** im README/Badge gegen `pyproject.toml`/`package.json`/`__version__` und gegen den letzten Release-Tag. Bei mehreren Versionstraegern alle pruefen, nicht nur einen.
- **Installationsweg** wirklich durchspielen, zumindest lesend: Existiert das Paket unter dem genannten Namen? Stimmen Kommandos und Flags?
- **Feature-Liste** gegen den Code: Ist alles Genannte da, und fehlt Neues in der Liste?
- **Zahlen** (Anzahl Tools, unterstuetzte Formate, Testabdeckung) an der Quelle nachzaehlen statt fortzuschreiben. Zahlen im README veralten still.
- **Screenshots** gegen die aktuelle Oberflaeche.
- **Requirements** (Python-/Node-Version, Abhaengigkeiten) gegen die Manifeste.
- **Links** auf Nachbarprojekte, Doku und Registries: laufen sie noch?

Anschliessend die **Darstellung** verbessern, wo sie schwach ist: lange Aufzaehlungen von Optionen werden als Tabelle lesbarer; Codebloecke brauchen Sprach-Tags; eine Struktur- oder Ablaufuebersicht ist als Mermaid-Diagramm oder ASCII-Baum schneller erfasst als in Prosa; die erste Bildschirmhoehe sollte Zweck, Installation und ein Nutzungsbeispiel zeigen, nicht Badges und Vorgeschichte. Wenn das README ueber ~400 Zeilen geht, lagere Details nach `docs/` aus und verlinke.

**Sprachregel fuer READMEs:** Standard ist eine **englische `README.md`** plus **deutsche Zweitfassung**. Ausnahme: Der Gegenstandsbereich der Anwendung ist selbst deutsch (deutsches Recht, deutsches Steuer- oder Foerderwesen, deutschsprachige Zielgruppe) oder es existiert bisher ausschliesslich eine deutsche Fassung — dann bleibt Deutsch die Hauptsprache. Fuer jede weitere Sprache, die das Projekt bereits spricht, gehoert eine eigene README-Fassung dazu. Halte dich an die im Repo schon verwendete Namenskonvention (`README_de.md`, `README.de.md`, `docs/README.de.md`) und erfinde keine zweite daneben. Verlinke die Fassungen gegenseitig in der Kopfzeile.

### 6. Fehlende Standardsprachen anlegen

Ergaenze die READMEs, die von den **Standardsprachen** fehlen: Deutsch, Englisch, Spanisch, vereinfachtes Chinesisch, Japanisch, Russisch. Der Zweck ist Reichweite, deshalb gilt das vor allem fuer nutzernahe Projekte — bei einer entwicklernahen Bibliothek mit rein englischem Publikum ist eine russische README kein Gewinn, sondern nur weitere Pflegelast. Entscheide bewusst und halte die Entscheidung im Laufprotokoll fest, damit die naechste Runde sie nicht neu diskutiert.

Neue Fassungen werden **befuellt, nicht angelegt und leer gelassen** — ein Stub mit „TODO: translate" ist schlechter als gar keine Datei, weil er Vollstaendigkeit vortaeuscht. Inhaltliche Parallelitaet und Rueckangleichung regelt `bilingual-doc-sync`; bei mehr als zwei Fassungen lohnt es sich, diesen Skill fuer den Abgleich hinzuzuziehen.

### 7. Sichtbarkeit und Werbung

Ueberlege, welche Massnahmen fuer **dieses** Projekt tatsaechlich Nutzer bringen, und setze sie um:

- **Registries**, in die das Projekt technisch gehoert: Paketregister (npm, PyPI), MCP-Registry, Plugin-/Skill-Verzeichnisse, Marketplaces.
- **Kuratierte Listen** (`awesome-*` und thematische Sammlungen), sofern die Aufnahmekriterien wirklich erfuellt sind. Ein PR an eine Liste, deren Kriterien das Projekt verfehlt, kostet Reputation.
- **Eigene Flaechen**: Organisationsprofil, `llms.txt`, Projektwebsite, README des Oekosystems, Verweise aus verwandten eigenen Repos.
- **Release-Notes** als Anlass: Ein Release ohne erzaehlte Neuerung wird nicht wahrgenommen.

**Freigabe-Gate:** Alles, was nach aussen geht — PRs an fremde Repos, Eintraege in fremde Listen, Posts, Einreichungen — wird **vorgeschlagen und erst nach ausdruecklicher Freigabe ausgefuehrt**, sofern keine Dauerfreigabe fuer diesen Kanal existiert. Aenderungen an eigenen Flaechen brauchen dieses Gate nicht. Der Grund ist schlicht: Ein zurueckgezogener PR an ein fremdes Repo ist oeffentlich sichtbar und faellt auf das Projekt zurueck.

### 8. Eintrag auf den Organisationsseiten

Zuerst die eigene Organisation: Ist das Repo im Profil-README (`ORG/.github` → `profile/README.md`) ueberhaupt aufgefuehrt, in der richtigen Rubrik, mit aktueller Beschreibung?

```bash
gh api user/orgs --jq '.[].login'
```

Dann durch **alle** Organisationen gehen und je Organisation eine einzige Frage beantworten: Wuerde ein Besucher dieser Organisationsseite von diesem Repo profitieren? Meist lautet die Antwort nein — dann ist „nicht verlinken" das richtige Ergebnis und keine Luecke. Wo die Antwort ja lautet (thematische Naehe, gemeinsame Nutzer, ein Werkzeug, das die dortigen Projekte ergaenzt), setze den Verweis mit einer Zeile, die den Nutzen erklaert, nicht nur den Namen nennt.

Das Profil liegt in einem eigenen Repo (`ORG/.github`). Aenderungen dort werden mitgepflegt und gepusht — nach der Dirty-Tree-Regel aus Schritt 11.

### 10. Issues und Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Arbeite sie durch statt sie nur zu zaehlen:

- **Fixbare Bugs** direkt beheben — in dieser Runde ist der Kontext ohnehin geladen. Kleine, klar umrissene Fixes mit Test und Verweis auf die Issue-Nummer.
- **Bereits erledigte Issues** schliessen, mit einem Satz, was sie geloest hat.
- **Unklare Meldungen** brauchen eine gezielte Rueckfrage (Version, Betriebssystem, Reproduktionsschritte).
- **PRs**: Diff wirklich lesen, Tests laufen lassen, dann mergen oder begruendet zurueckmelden. Ein PR, der monatelang unbeantwortet liegt, kostet mehr Wohlwollen als eine hoefliche Ablehnung.
- **Stale-Faelle** aufloesen statt weiterschleppen.

**Freigabe-Gate:** Oeffentliche Kommentare, Schliessungen mit Begruendung und Merges fremder Beitraege sind Kommunikation nach aussen — vor der Ausfuehrung vorlegen, sofern keine Dauerfreigabe besteht. Reine Code-Fixes im eigenen Repo sind davon nicht betroffen.

### 11. Committen, pushen, verifizieren

Die Runde endet nicht mit den Aenderungen, sondern damit, dass sie **draussen sind**. Ein Arbeitsbaum voller ungepushter Verbesserungen ist das schlechteste Ergebnis: Die naechste Session — moeglicherweise ein anderer Agent oder ein anderes Geraet — muss sich erst in einen fremden, halbfertigen Stand einarbeiten, und auf den oeffentlichen Flaechen hat sich nichts verbessert.

Vor dem Push kurz absichern, was ueberpruefbar ist: Tests und Smokes laufen lassen, bei Doku-Aenderungen die Links und die gerenderte Ansicht pruefen. Dann in **thematisch getrennten Commits** buendeln, statt alles in einen Sammel-Commit zu werfen — Aufraeumen, Doku-Aktualisierung und Bugfixes sind drei verschiedene Dinge, und wer spaeter einen davon zurueckdrehen will, ist dankbar dafuer:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

Danach verifizieren statt annehmen: Remote-README in der gerenderten Ansicht, CI-Lauf, Release- und Tag-Stand.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

Zwei Faelle, in denen **nicht** gepusht wird: wenn fuer das Projekt eine Veroeffentlichungs- oder Einreichungssperre gilt (dann lokal auf einem eigenen Branch committen und den Sperrgrund im Laufprotokoll vermerken), oder wenn der Stand erklaertermaassen unfertig ist. Beides sind Ausnahmen, die man begruendet — der Normalfall ist: committen und pushen.

Existieren weitere Klone desselben Repos (zweites Geraet, Deploy-Kopie, Spiegel), ziehe sie unmittelbar nach dem Push nach. Ein Klon, der zehn Commits zurueckliegt, produziert bei der naechsten Fehlersuche Diagnosen an einem Stand, den es nicht mehr gibt.

#### Aenderungen an anderen Repos — Dirty-Tree-Ausnahme

Diese Runde erzeugt regelmaessig Aenderungen **ausserhalb** des gepflegten Repos: eine Zeile im Organisationsprofil (Schritt 8), spaeter in der tiefen Runde ein Rueckverweis in einem verwandten Repo. Solche Aenderungen werden ebenfalls committet und gepusht — ein unveroeffentlichter Rueckverweis ist kein Rueckverweis.

Vor dem Anfassen eines fremden Repos kurz dessen Zustand pruefen:

```bash
git -C <pfad> status --porcelain
```

**Sauberer Arbeitsbaum** → Aenderung vornehmen, in einem **eigenen, thematisch klaren Commit** (`docs: link <projekt>`) committen und pushen. Nicht mit den Commits des gepflegten Repos vermischen: Es ist ein anderes Repo mit eigener Historie und eigenen Lesern.

**Dirty, also uncommittete Fremdaenderungen vorhanden** → nicht anfassen. Man muesste entweder fremde, ungepruefte Arbeit mit-committen oder sie wegstashen; beides ist riskant, und den fremden Stand erst zu verstehen kostet mehr, als dieser eine Verweis wert ist. Stattdessen: Vorhaben im Laufprotokoll als offenen Punkt notieren (welches Repo, welcher Verweis, warum uebersprungen). Der naechste Pflegelauf, der sich **diesem** Repo zuwendet, findet dort einen sauberen Baum vor und erledigt es. Genauso wird verfahren, wenn im Ziel-Repo eine aktive Sperre liegt.

Zum Schluss die Flaechen aus Schritt 0 bedienen — siehe naechster Abschnitt.

## Paritaet ueber alle Distributionsflaechen

Zum Abschluss der Runde gegen die Liste aus Schritt 0 gehen: **Jede Aenderung, die ein Nutzer sehen wuerde, muss auf jeder Flaeche ankommen, auf der er sie sucht.** Ein Repo, dessen npm-Seite eine andere Geschichte erzaehlt, ist schlechter dran als eines mit nur einer Flaeche.

Der entscheidende Mechanismus: **Paketregister zeigen die README des letzten Publish, nicht den aktuellen Repo-Stand.** Eine README-Korrektur wird auf npm oder PyPI erst mit einer neuen Version sichtbar. Wenn die Korrektur inhaltlich relevant ist (falsche Installation, falsche Version, veraltete Feature-Liste), gehoert ein Patch-Release dazu — sonst bleibt der Fix wirkungslos.

| Flaeche | Was dort gepflegt wird | Wie es ankommt |
|---|---|---|
| npm | README, `description`, `keywords`, Repository-Link | Nur per `npm publish` (Patch-Version); Metadaten kommen aus `package.json` |
| PyPI | README (`long_description`), Classifiers, Projekt-URLs | Nur per neuem Upload; Metadaten aus `pyproject.toml` |
| MCP-Registry / Plugin-Verzeichnisse | Beschreibung, Version, Toolliste, Einstiegsdoku | Je nach Registry Manifest-Update oder erneute Einreichung |
| Marketplace / Store | Beschreibung, Screenshots, Kategorien, Sprachfassungen | Ueber die jeweilige Verwaltungsoberflaeche; Screenshots altern dort besonders schnell |
| Docker Hub / Container-Registry | Beschreibung, Tags, Nutzungsbeispiel | Repository-Beschreibung plus neuer Tag |
| Zenodo / DOI | Metadaten, Autoren, Version | In-Place-Edit fuer Metadaten, neue Version fuer Inhalte |
| Website / Org-Profil / `llms.txt` | Kurzbeschreibung, Link, Positionierung | Direkt editierbar — die guenstigsten Flaechen, deshalb nie vergessen |

Wenn eine Version angehoben wird, muessen **alle Versionstraeger** gleichzeitig mitwandern: Manifest, Code-Konstante, README-Badge, Changelog, Release-Tag, `llms.txt`. Ein halb angehobener Versionsstand ist schwerer zu diagnostizieren als ein durchgaengig alter.

Ist eine Aktualisierung auf einer Flaeche gerade nicht moeglich oder nicht sinnvoll (z. B. ein Release nur wegen eines Tippfehlers), halte das im Laufprotokoll fest, damit die naechste Runde die Abweichung nicht fuer ein Versehen haelt.

## Force-Push-Regel

Der Standard ist **kein Force-Push**. Interne Planungsdateien nachtraeglich zu ignorieren rechtfertigt keine Historien-Umschreibung: Der Aufwand ist hoch, jeder Klon und jeder Fork bricht, offene PRs werden unbrauchbar — und der Gewinn ist gering, weil der Inhalt harmlos ist. Normaler Weg:

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergaenzen
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

Die Historie umschreiben (und damit `--force-with-lease` pushen) ist nur bei **echten Leaks** gerechtfertigt: Credentials und Keys, personenbezogene oder Kundendaten, sowie Dokumente mit echtem Wettbewerbswert — interne Kalkulationen, Preisstrategien, unveroeffentlichte Plaene, Vertragsinterna. In diesem Fall:

1. Betroffene Secrets **zuerst rotieren** — die Historie ist zu diesem Zeitpunkt bereits kopiert, geforkt und in Caches. Rotation wirkt, Loeschen nur kosmetisch.
2. Historie bereinigen (`git filter-repo` oder BFG), `--force-with-lease` pushen.
3. Forks und Caches pruefen; bei Bedarf GitHub-Support fuer verwaiste Objekte kontaktieren.
4. Vorgang im Laufprotokoll festhalten: was, wann, welche Rotation.

Im Zweifel zwischen „unkritisch" und „heikel": als heikel behandeln und vorlegen. Die Kosten sind asymmetrisch.

## Laufprotokoll

Halte das Ergebnis in `_after-care/LOG.md` fest (der Ordner gehoert in die `.gitignore` — er ist Pipeline-Material, kein Repo-Inhalt, genau nach der Regel aus Schritt 2b). Pro Lauf eine Zeile mit Datum, Stufe und den bewussten Entscheidungen:

```markdown
## 2026-07-24 — surface
- Flaechen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push noetig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezaehlt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rueckfrage gestellt
- Push: 3 Commits, CI gruen; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

Das Protokoll erspart der naechsten Runde, dieselben Entscheidungen neu zu treffen, und ist die Grundlage fuer rotierende Pflegelaeufe ueber viele Repos (`rotation-check`).

## Haeufige Fehler

| Fehler | Korrektur |
|---|---|
| Nur den Arbeitsbaum betrachtet, nicht `git ls-files` | Immer das getrackte Set pruefen — dort liegt das Problem |
| Interne Datei entfernt und dabei Historie umgeschrieben | Bei unkritischen Dateien reicht `git rm --cached` + normaler Push |
| Secret aus `HEAD` entfernt und Vorgang als erledigt betrachtet | Secret rotieren; alles andere ist Kosmetik |
| Dateien nach Namen klassifiziert | Kurz hineinsehen — Namen tragen die Absicht nicht zuverlaessig |
| Zahlen im README fortgeschrieben statt nachgezaehlt | An der Quelle zaehlen (Tool-Liste, Testlauf, Manifest) |
| Neue Sprachfassung als leerer Stub angelegt | Befuellen oder weglassen — ein Stub taeuscht Vollstaendigkeit vor |
| Zweite README-Namenskonvention neben der bestehenden eingefuehrt | Vorhandene Konvention uebernehmen |
| PR an eine fremde Liste ohne Freigabe gestellt | Aussenkommunikation vorlegen; nur eigene Flaechen sind frei |
| Issues gezaehlt statt bearbeitet | Fixen, schliessen oder gezielt nachfragen — jeder Fall bekommt einen Zustand |
| Banner im Alleingang in fremdem Stil erzeugt | Design-Familie des Oekosystems einhalten |
| README im Repo korrigiert, npm-/PyPI-Seite zeigt weiter die alte | Registry-Seiten stammen vom letzten Publish — Patch-Release nachziehen |
| Version nur im Manifest angehoben | Alle Versionstraeger gleichzeitig: Manifest, Code, Badge, Changelog, Tag, `llms.txt` |
| Aenderungen fertig, aber ungepusht liegen gelassen | Committen und pushen gehoert zur Runde; nur Sperren rechtfertigen eine Ausnahme |
| Alles in einem Sammel-Commit | Aufraeumen, Doku und Fixes trennen — sonst ist nichts einzeln zurueckdrehbar |
| Fremdes Repo mit uncommitteten Aenderungen trotzdem bearbeitet | Dirty-Tree-Regel: ueberspringen und als offenen Punkt notieren |
| Aenderung im Org-Profil-Repo gemacht, aber nicht gepusht | Fremd-Repos bekommen einen eigenen Commit und einen eigenen Push |

## Abschluss-Checkliste

- [ ] Distributionsflaechen ermittelt und im Laufprotokoll notiert.
- [ ] Topics, Description und Homepage gesetzt und ueberprueft.
- [ ] Privacy-Gate ueber das getrackte Set gelaufen, Funde behandelt.
- [ ] `.md`/`.txt`/`.json` auf Veroeffentlichungsabsicht geprueft, interne Dateien ignoriert.
- [ ] Kein Force-Push ohne echten Leak; bei Leak Rotation durchgefuehrt.
- [ ] Banner vorhanden und im README eingebunden.
- [ ] Version, Features, Zahlen, Screenshots, Links gegen den echten Stand geprueft.
- [ ] Darstellung verbessert (Tabellen, Diagramme, erste Bildschirmhoehe).
- [ ] README-Sprachmatrix vollstaendig; Entscheidungen zu weiteren Sprachen dokumentiert.
- [ ] Sichtbarkeitsmassnahmen umgesetzt bzw. zur Freigabe vorgelegt.
- [ ] Eintrag im eigenen Org-Profil geprueft, sinnvolle Fremd-Orga-Verweise gesetzt.
- [ ] Aenderungen an Fremd-Repos committet und gepusht — oder wegen dirty/Sperre notiert.
- [ ] Issues und PRs in einen definierten Zustand gebracht.
- [ ] Getrennte Commits erstellt, gepusht, CI und Remote-Ansicht verifiziert.
- [ ] Alle Distributionsflaechen auf denselben Stand gebracht (ggf. Patch-Release).
- [ ] Laufprotokoll in `_after-care/LOG.md` geschrieben.

## Changelog

### 1.0.0 (2026-07-24)
- Initiale Version. Stufe 1 der Repo-Nachpflege, abgeleitet aus `github-repo-care`.
