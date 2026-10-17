---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "Synthétise des décisions ouvertes regroupées en UN seul concept global cohérent, rédigé en prose, à partir de toutes les variantes recommandées. Montre comment les sous-systèmes s'articulent concrètement après la mise en œuvre, au lieu d'obliger l'utilisateur à répondre à des dizaines de questions isolées. L'utilisateur valide l'image dans son ensemble ou formule des corrections ciblées, qui sont automatiquement traduites en décisions individuelles et réinscrites dans le registre via la phase 4 de decision-briefing. Utilise cette compétence pour « à quoi ressemble l'ensemble si nous acceptons tout », « dessine-moi l'image globale », « concept global des décisions », « decision draw », /decision-draw, « comment les systèmes s'articulent-ils ». NE PAS l'utiliser si des alternatives doivent être discutées point par point — cela relève de decision-briefing ; NI pour le graphe de dépendances — cela relève de decision-path ; NI pour des blocs individuels structurés avec options et pour/contre (y compris pour des groupes étroitement liés) — cela relève de decision-shot ; NI pour la dérivation d'une décision unique — cela relève de decide."
visibility: public
language: fr
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — Image globale et validation de décisions regroupées

> Lorsque cinq ou dix décisions sont en attente, on perd facilement de vue le
> système qui se dessine dans le détail des options. decision-draw ne décrit
> pas les alternatives, mais l'ensemble fonctionnel : comment les systèmes
> travaillent-ils ensemble si toutes les recommandations sont acceptées ?
> L'utilisateur valide l'image dans son ensemble ou la corrige de manière ciblée.

---

## Quand l'utiliser

- Plusieurs décisions liées (issues de [decision-briefing](../decision-briefing/SKILL.md) ou d'un modèle de décision) ne doivent pas être traitées comme une liste fastidieuse de questions isolées.
- L'utilisateur souhaite voir, avant la décision, comment les composants interagissent réellement au quotidien après la mise en œuvre.
- Le graphe de dépendances ([decision-path](../decision-path/SKILL.md)) a identifié un ensemble de décisions fortement couplées, pouvant être validé comme une unité fonctionnelle.
- Mots déclencheurs : `/decision-draw`, « à quoi ressemble l'ensemble si nous acceptons tout », « dessine-moi l'image globale », « concept global des décisions », « decision draw », « comment les systèmes s'articulent ensuite », « image pour la validation globale ».
- **Ne pas utiliser** :
  - Si l'utilisateur veut comparer les options de chaque question et choisir par lettre (A/B/C) — cela relève de [decision-briefing](../decision-briefing/SKILL.md).
  - Pour la seule analyse causale et de blocage dans le terminal — cela relève de [decision-path](../decision-path/SKILL.md).
  - Pour la comparaison isolée d'options dans des blocs en 5 parties (contexte, pour/contre par option, recommandation) pour des questions individuelles ou des groupes étroitement liés — cela relève de [decision-shot](../decision-shot/SKILL.md).
  - Pour l'élaboration méthodique d'une seule question de principe ouverte — cela relève de [decide](../decide/SKILL.md).

---

## Délimitation au sein de la famille des décisions

| Compétence | Approche et focus | Position vis-à-vis des options | Forme de validation |
|---|---|---|---|
| `decision-briefing` | **Décompose** en questions individuelles | Présente toutes les options A/B/C/D | Codes lettres (`1A 2C 3B`) |
| `decision-path` | **Structure** les causalités | Évalue les options dans le graphe | Diagnostic dans le terminal (ASCII) |
| `decision-draw` | **Image cible cohérente** (regroupe des décisions reliées) | Décrit **uniquement la variante recommandée** (alternatives liées) | Validation globale ou phrase de correction |
| `decision-shot` | **Blocs individuels structurés** (pour questions isolées ou groupes étroits) | Présente les options avec 2–4 arguments pour/contre | Décision exécutive / validation individuelle |
| `decide` | **Élabore** le cas individuel | Matrice d'évaluation (critères) | Recommandation analytique |

> **Règle centrale :**
> `decision-draw` décrit **exclusivement la variante recommandée**. Les alternatives écartées ne disparaissent pas — elles sont documentées dans [decision-briefing](../decision-briefing/SKILL.md), [decision-shot](../decision-shot/SKILL.md) ou les tickets liés, et sont référencées dans l'en-tête. Un draw sans ce renvoi ôterait à l'utilisateur son choix au lieu de le faciliter.

---

## Règle de style contraignante : textes destinés à l'utilisateur sans sigles ni numéros

> **Consigne utilisateur canonique (retour du 2026-09-13 / ticket T-20260913-883789445) :**
> *« Les decision draws sont trop techniques, cela doit se passer sans numéro, tu les connais en arrière-plan ou tu les utilises pour la rédaction des textes [...]. »*

1. **Aucun sigle technique dans le texte visible par l'utilisateur :**
   Dans le texte visible destiné à l'humain (lot, concept, articulation, mise en œuvre, question), il n'y a **aucun** sigle interne (comme `BH-A`, `MD-A`, `HA-A`, `PRA`), aucun numéro de ticket (`T-2026...`), aucun numéro D (`D-2026...`), aucun chemin relatif, aucun hash Git ni aucune mesure.
2. **2 à 4 phrases en langage courant, à la première personne, par élément :**
   Chaque élément du lot est formulé selon le triptyque :
   - *Situation :* quel est l'état de départ actuel ?
   - *« Je fais… » :* que prévois-je concrètement / quelle est ma recommandation ?
   - *Repli :* que se passe-t-il si cela échoue, ou que décide l'utilisateur ensuite ?
   *(Exemple : « Hermes ne prend en charge les tâches qu'en anglais. Je signale le problème à Hermes sous forme de ticket et nous mettons en place un contournement. Il existe actuellement d'anciennes sessions inexploitables. J'essaie de les rendre à nouveau utilisables. Si cela ne fonctionne pas, je te fournirai un échantillon aléatoire de 10 sessions et en ferai la synthèse — afin que tu puisses décider si un sauvetage vaut la peine. »)*
3. **Titres clairs en langage courant pour l'orientation :**
   Chaque élément porte un titre compréhensible en français (par ex. *« Backend du modèle comme pièce maîtresse »*, *« Clés de déploiement sécurisées sur le Mac »*). L'utilisateur interagit via ce titre ou valide l'ensemble.
4. **Correspondance technique uniquement en annexe :**
   La correspondance entre titre en langage courant, sigle interne, identifiant de ticket et état du registre se fait **exclusivement dans un tableau d'annexe final** du document. C'est là — et seulement là — qu'interviennent les analyseurs automatisés et le réinscripteur du registre.

---

## Structure contraignante (huit parties)

Un `decision-draw` complet suit sans exception cette structure :

### 1. Lot et périmètre (en langage courant)
Vue d'ensemble des éléments regroupés en langage courant (première personne, 2–4 phrases par point, aucun identifiant ni sigle dans le texte).

### 2. Concept
L'état cible visé, sous forme de texte continu en prose :
- Quel paysage système ou quel flux de travail apparaît si toutes les recommandations sont mises en œuvre exactement ainsi ?
- Pas de juxtaposition d'options, pas de conditionnel parallèle (« on pourrait aussi »).
- Indicatif clair et précis : voici comment le système fonctionne à l'état cible.

### 3. Articulation
Le cœur fonctionnel de la compétence :
- Comment les parties décidées s'engrènent-elles concrètement **après** la mise en œuvre ?
- Présentation de préférence sous forme d'un parcours de bout en bout concret plutôt que d'une simple liste de composants.
- Rend tangibles les flux de données, interfaces et responsabilités.

### 4. Mise en œuvre
L'ordre concret de réalisation :
- Que se passe-t-il réellement en pratique ?
- Reprend directement la logique d'arêtes et de dépendances de [decision-path](../decision-path/SKILL.md).
- Les chantiers indépendants sont présentés honnêtement comme parallèles (ne pas inventer de chaînes causales artificielles ; un lot peut comporter plusieurs chantiers parallèles). Un ordre n'est affirmé que là où des dépendances ou échéances avérées existent.
- Nomme les points de contrôle (gates), étapes de migration et contrôles.

### 5. Ce que cette image ne couvre pas
Protection contre une fausse exhaustivité :
- Quelles questions marginales, points ouverts ou confiances 🔴 sont volontairement exclus ?
- Où se situent les limites d'interface avec les systèmes voisins ?
- Une image qui tait ses marges crée une fausse assurance.

### 6. Validation
L'interaction avec l'utilisateur :
- L'utilisateur examine l'image dans son ensemble.
- Réponse possible 1 : **validation globale explicite** (« Ça me va », « Validé », « Mettons-le en œuvre »). Seule cette réponse enregistre tous les éléments du lot comme décidés.
- Réponse possible 2 : **correction par titre en langage courant ou en langue naturelle** (« Pour le déploiement sur Mac, pas de redémarrage automatique », « Reporter VersicherungsManager pour l'instant »). Entraîne la décomposition en décisions individuelles ; tous les éléments non corrigés restent ouverts.

### 7. Rétrotransfert
La traduction systématique des corrections de l'utilisateur en décisions individuelles :
- **Aucun enregistrement automatique :** seule une validation globale explicite enregistre les éléments inchangés. Une correction partielle n'est **pas** une validation globale !
- **Isolement en cas de correction :** une correction est décomposée en décisions individuelles ; tous les autres éléments du lot restent strictement **ouverts** (dans le registre source / le modèle) jusqu'à ce que l'utilisateur accepte l'image épurée dans son ensemble ou confirme individuellement les éléments restants.
- **Tableau obligatoire du rétrotransfert :** chaque retour de correction produit impérativement un tableau d'analyse structuré à quatre colonnes (correction d'origine, sigles concernés, état des dominos, ambiguïtés ouvertes).
- **Voie d'écriture exclusive via la phase 4 :** `decision-draw` ne dispose **d'aucune** voie d'écriture propre vers le registre. L'enregistrement se fait **exclusivement** selon la procédure standardisée de la phase 4 de [decision-briefing](../decision-briefing/SKILL.md).

### 8. Annexe : tableau de référence technique (uniquement pour l'enregistrement et l'audit)
Tableau compact en fin de document avec :
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## Exemple (extrait pilote : ticket maître du 2026-09-13 — BACH et ensemble système)

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## Règles pratiques

1. **Pas de conditionnel dans le concept :** décris le système global comme s'il était déjà réalisé. L'utilisateur veut de la clarté sur le résultat, pas des éventualités théoriques.
2. **Causalité avant chronologie :** l'ordre de la section *Mise en œuvre* suit les niveaux du graphe de dépendances de [decision-path](../decision-path/SKILL.md). Les chantiers indépendants sont présentés honnêtement comme parallèles et ne sont pas pliés en une chaîne causale artificielle.
3. **Contrôle explicite des dominos dans le rétrotransfert :** une correction de l'utilisateur ne doit jamais être inscrite isolément sans vérifier si des nœuds dépendants du graphe sont invalidés ou influencés.
4. **Pas d'enregistrement automatique en cas de correction partielle :** seule une validation globale explicite enregistre les éléments inchangés. À chaque correction partielle, tous les éléments non concernés restent strictement ouverts jusqu'à ce que l'image globale soit à nouveau validée ou que les éléments soient confirmés individuellement.
5. **Voie d'écriture exclusive via la phase 4 :** `decision-draw` ne dispose d'aucune voie d'écriture propre vers le registre. Les enregistrements se font sans exception via la phase 4 de [decision-briefing](../decision-briefing/SKILL.md).
6. **Respecter les contrats du registre :** les enregistrements suivent toujours les règles du registre des décisions (pas de renumérotation des identifiants, codes d'enregistrement uniques, cible canonique `DECIDED-AND-DONE.md`).
7. **Textes utilisateur sans numéros ni sigles techniques :** le texte visible destiné à l'humain ne comporte ni identifiants, ni sigles, ni chemins, ni numéros de ticket. Chaque élément est formulé à la première personne, dans un langage compréhensible ; toutes les références vont dans le tableau d'annexe.

---

## Provenance de la session

Lorsqu'un decision draw est enregistré comme document de concept durable, il se termine par :

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Priorité des sources : indication explicite d'exécution ou de CLI en premier, puis environnement ou hook du fournisseur faisant autorité, sinon `unbekannt`.
- Les sous-agents héritent de l'identifiant de session parent.
- Les simples modèles de chat ne reçoivent aucun tampon.

---

## Journal des modifications

### 1.1.0 (2026-09-18)
- Règle de style pour des textes de décision accessibles à l'utilisateur ancrée (T-20260913-883789445, consigne utilisateur du 2026-09-13) :
  - Aucun sigle technique, numéro de ticket ou D, chemin ou mesure dans le texte visible.
  - 2 à 4 phrases de langage courant à la première personne (situation, « Je fais… », repli) par élément.
  - Titres clairs en langage courant pour l'identification et la validation.
  - Correspondance technique (sigles, identifiant de ticket, état du registre) déplacée strictement dans le tableau d'annexe final (section 8).

### 1.0.1 (2026-09-13)
- Retouches après relecture :
  - Contrat de rétrotransfert renforcé : aucun enregistrement automatique en cas de correction partielle ; les éléments non touchés restent strictement ouverts jusqu'à la validation globale.
  - Tableau obligatoire du rétrotransfert à 4 colonnes (correction d'origine, sigles concernés, état des dominos, ambiguïtés ouvertes) introduit.
  - Correspondances multiples démontrées dans l'exemple (une seule correction de l'utilisateur déplace `MD-A` et `CF-A` simultanément).
  - Voie d'écriture exclusive via la phase 4 de `decision-briefing` ancrée dans le contrat et l'exemple.
  - Erreur de chaîne causale corrigée dans l'exemple : les éléments indépendants sont présentés honnêtement comme quatre chantiers parallèles (option a).
  - Délimitation avec `decision-shot` précisée par le format de sortie (blocs structurés avec pour/contre vs image cible cohérente avec validation globale).

### 1.0.0 (2026-09-13)
- Version initiale sur la base de la demande utilisateur T-20260913-107991667.
- Structure contraignante en sept parties (lot, concept, articulation, mise en œuvre, limites, validation, rétrotransfert).
- Logique de regroupement fondée sur `decision-path` et pont d'écriture vers la phase 4 de `decision-briefing`.
