---
name: work-autonomous
version: 1.4.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-03
description: >
  Abbruchbedingung für autonome Loops: So weit wie möglich selbständig
  weiterarbeiten UND einen Loop erst beenden, wenn belegt ist, dass keine
  autonom ausführbare Aufgabe mehr vorliegt. Der bloße Eindruck "nichts mehr
  zu tun" reicht NICHT — er löst eine vierstufige Prüfkette aus (think/decide,
  _DECISIONS, Gardener/USMC, decision-avatar/BYUM), die zuerst neue Aufgaben
  GEWINNEN muss, bevor der Loop enden darf. Jeder Kettenschritt meldet
  found/empty/unavailable statt eines binären Ergebnisses — "exhausted" gilt
  nur, wenn ALLE Quellen tatsächlich befragbar waren; ist mindestens eine
  Quelle unavailable, meldet der Skill "blind" statt "exhausted" und behauptet
  nichts Ungeprüftes. Nutze diesen Skill bei /work-autonomous, /waafap,
  "arbeite autonom weiter bis nichts mehr zu tun ist", als Goal-Bedingung
  innerhalb eines /loop, oder wenn geprüft werden soll, ob wirklich keine
  autonome Arbeit mehr übrig ist, bevor ein Loop/eine Session beendet wird.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: de
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — Loop erst beenden, wenn belegt keine autonomen Aufgaben mehr vorliegen

## Zweck

Dieser Skill leistet zwei Dinge zugleich:

1. **So weit wie möglich autonom weiterarbeiten** — ganz normale Sitzungsarbeit, keine Besonderheit.
2. **Einen Loop erst beenden, wenn NACHGEWIESEN ist**, dass keine autonom ausführbare Aufgabe mehr
   existiert. Der Verdacht "ich finde gerade nichts mehr zu tun" ist **kein** Abbruchgrund — er ist
   der **Auslöser** einer Prüfkette, die zuerst versucht, neue Aufgaben zu **gewinnen**. Erst wenn
   diese Kette vollständig ergebnislos bleibt, gilt der Abbruch als belegt.

**Bewusst ohne eingebautes `/goal`:** Der Skill ist eigenständig nutzbar (z. B. direkt als
`/work-autonomous`-Aufruf innerhalb einer normalen Session) und ebenso als Bedingung innerhalb
einer übergeordneten Loop-Konstruktion: `/loop` normal vergeben, dann als Goal nur diesen Skill
nennen. Das Goal lautet dann sinngemäß: *"Beende den Loop, wenn keine autonomen Aufgaben mehr
vorliegen — und arbeite bis dahin so weit wie möglich autonom weiter."* Der Skill selbst ruft
kein `/goal`-Konstrukt auf; er liefert nur das eindeutige Abbruchsignal, das ein solches Konstrukt
lesen kann (siehe „Abbruchsignal" unten).

## Betriebsmodell — zwei Ebenen

### Ebene 1 — Normalarbeit (jeder Tick)

#### TICKET-MASTER-Intake-Gate (Vorrang vor allem anderen in dieser Ebene)

**Nur relevant, wenn überhaupt ein Ticketsystem (`_TICKETS/`) Teil des Kontexts ist** — Sitzungen
ohne Ticketsystem überspringen dieses Gate ersatzlos, der Skill bleibt ohne jedes Ticketsystem
eigenständig nutzbar (siehe „Zweck" oben). Gilt es, zuerst prüfen, ob `INBOX/` — einschließlich
formloser, noch nicht ins Ticket-Format gebrachter Einträge — vollständig formalisiert und
triagiert ist. Ist das nicht der Fall, zählt genau das als gefundene autonome Arbeit
(Formalisieren/Triagieren ist Klerikalarbeit ohne Nutzerentscheidung, siehe Abgrenzung unten) —
erledigen, Tick endet, Ebene 2 wird nicht betreten, wie bei jeder anderen Ebene-1-Quelle.

**Solange INBOX offen ist, dürfen `NO_WORK`, ein Erschöpfungssignal (`exhausted`/`blind`), ein
Guard-STOP oder irgendein anderes Abbruchsignal NICHT entstehen.** Erst wenn Intake vollständig
triagiert ist, dürfen `ACTIONABLE`, entblockte `BLOCKED` und fällige `WAITING` (unten) — und danach
ggf. Ebene 2 — überhaupt geprüft werden.

*Belegfall:* Ein Loop begann nach dem Abarbeiten von `ACTIONABLE` die Erschöpfungsprüfung, während
laufend neue `INBOX`-Tickets eintrafen, darunter zwei mit Priorität P1. Ohne dieses Gate hätte der
Loop `exhausted`/`blind` gemeldet, obwohl Eingang offen war — genau das verhindert das Gate.

Danach ganz normal nach weiterer autonom ausführbarer Arbeit suchen (siehe Abgrenzung
unten) und sie erledigen: offene `ACTIONABLE`-Tickets, entblockte `BLOCKED`-Tickets, fällige
`WAITING`-Tickets, offene `TODO.md`/`AUFGABEN.txt`-Punkte in Projekten ohne User-Abhängigkeit,
fällige Routine-/Hygiene-Checks nach lokaler Policy, angefangene, aber nicht abgeschlossene Arbeit
aus der letzten Session (USMC `working`), **fällige `tidy-up`-Läufe des aktiven Projekts**
(Ergänzung 1.3.0, 2026-08-19 — siehe Skill `tidy-up`: Tasksolver+Writer+Maintainer-Durchlauf für
den Projektordner, in dem die Session gerade gearbeitet hat; Fälligkeit prüft `tidy-up` selbst
über sein eigenes, schlankes USMC-Log, siehe dortiger Abschnitt „Verhältnis zu work-autonomous").

→ **Gefunden & erledigt:** Ergebnis kurz melden, Tick endet, Loop läuft normal weiter. Ebene 2 wird
NICHT betreten — keine der vier teuren Prüfschritte ist nötig, solange sichtbare Arbeit vorliegt.

### Ebene 2 — Exhaustion-Check (nur bei Verdacht „nichts mehr zu tun")

Erst wenn Ebene 1 **nichts** Autonomes mehr findet, entsteht der Verdacht. Dieser Verdacht allein
genügt nicht. Jetzt läuft **pflichtgemäß** die folgende Kette, um neue Aufgaben zu **gewinnen**.

#### Selbstkenntnis (vor der Kette, nicht danach)

Bevor irgendetwas befragt wird: Der Skill deklariert, WELCHE Quellen er für sein Urteil braucht.
Vier Bedarfe (`grounding_seed.self_knowledge.Need`, falls `grounding-seed` installiert ist — sonst
gilt dieselbe Liste als reine Deklaration ohne Bibliotheksanbindung):

| Rolle | Kettenschritt | Was dahintersteht |
|---|---|---|
| `decisions.ledger` | 2 | zentrales Entscheidungsregister |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (Schritt 1) ist bewusst KEINE deklarierte Quelle.** Es ist der eigene
Analyseschritt des Modells, kein externes System, das erreichbar oder nicht erreichbar sein könnte
— es ist immer „verfügbar" im Sinne dieser Unterscheidung. Nur Schritte 2–4 können `unavailable`
werden.

Optionales, testbares Werkzeug für die reine Verortungsfrage (found/unavailable, noch OHNE
Inhaltsprüfung): `scripts/exhaustion_check.py` in diesem Skill-Ordner. Es nutzt
`grounding_seed.resolve()` + `status_from_resolution()` für `decisions.ledger`/`user.model` (dort
existiert ein echter `source-resolver`-Provider), prüft `memory.organic`/`memory.curated` dagegen
**immer** direkt über CLI-Erreichbarkeit (`gardener`/`usmc` auf PATH) — für diese zwei Rollen gab
es bis 2026-08-15 noch keinen registrierten `source-resolver`-Provider; sie über den Resolver zu
befragen hätte nur `unavailable` gemeldet, unabhängig davon, ob Gardener/USMC echt installiert
sind. Läuft identisch mit und ohne installiertes `grounding-seed`.

**Update 2026-08-25 (K3=C, `T-20260825-342866657`):** Die Lücke ist geschlossen — `source-resolver`
registriert `memory.organic` (Gardener) und `memory.curated` (USMC) jetzt beide als Stufe-1-Rolle
mit demselben CLI-Präsenzcheck (`shutil.which("gardener")`/`shutil.which("usmc")`), den dieses
Skript bisher selbst hardcodiert. `exhaustion_check.py` ist deshalb NICHT sofort umgebaut worden
(kein Funktionsverlust, der bestehende Check bleibt korrekt) — beim nächsten Skill-Care-Lauf kann
Schritt 3 auf `source_resolver.resolve("memory.organic"/"memory.curated")` umgestellt werden,
analog zu Schritt 2 (`decisions.ledger`), statt den CLI-Check zweifach zu pflegen.

#### Die vier Kettenschritte — jeder meldet found | empty | unavailable

Jeder Schritt läuft zweistufig: erst **Verortung** (kenne ich überhaupt eine erreichbare Stelle?),
dann — nur wenn verortet — **Inhaltsprüfung** (das Modell liest tatsächlich nach, ob dort etwas
Neues liegt, mit seinen eigenen Werkzeugen). Eine Quelle, die nicht verortet werden konnte, wird
NIE inhaltlich geprüft — sie zählt `unavailable`, nicht `empty`.

1. **`/think` + `/decide`** auf die Frage anwenden: „Gibt es wirklich keine autonom ausführbare
   Arbeit mehr, oder übersehe ich etwas?" — strukturierte Analyse statt Bauchgefühl. Kein
   found/empty/unavailable-Status (siehe oben, keine Quelle).
2. **`decisions.ledger`** — Verortung über `source_resolver.resolve("decisions.ledger")` /
   `grounding_seed.resolve(...)`, falls installiert; sonst der bekannte Fallback-Pfad
   (`_control-center/_DECISIONS/`, `TO-DECIDE-USER*.txt`-Kette, host-eigene
   `TO-DECIDE-USER-<HOST>.txt`, `DECIDED-AND-DONE.md`). Verortet → Inhalt lesen: sind kürzlich
   Entscheidungen gefallen, die vorher blockierte oder auf Freigabe wartende Arbeit jetzt
   entsperren? Treffer → `found`. Gelesen, nichts Neues → `empty`. Nicht verortbar (Resolver fehlt
   UND Fallback-Pfad existiert nicht) → `unavailable`.
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — zwei getrennte Quellen, ein
   Kettenschritt. Verortung: CLI auf PATH (`gardener`/`usmc`), siehe Selbstkenntnis oben. Erreichbar
   → Inhalt lesen (`find()`/`recall()` bzw. `usmc facts|lessons|working|context`): offene
   Working-Memory-Punkte, Lessons mit unerledigter Folgeaufgabe, Fakten, die auf übersehene, aber
   ausführbare Arbeit hindeuten (das ist genau der Ort, an dem frühere Sessions unfertige Punkte —
   `RESUME:`-Feld, offene `note`-Einträge — hinterlassen). Treffer → `found`. Gelesen, nichts Neues
   → `empty`. CLI nicht auf PATH → `unavailable`.
4. **`user.model` (decision-avatar/BYUM)** — Verortung wie bei `decisions.ledger` (Resolver oder
   Fallback-Pfad `_control-center/_TOM-lm/`). Verortet → Inhalt prüfen: Gibt es ein belegtes
   Muster, nach dem der Nutzer an dieser Stelle eine bestimmte Handlung autonom erledigt sehen
   wollte? Nur bei ausreichender Konfidenz (🟢/🟡) als `found` zählen — 🔴 zählt als `empty`, nicht
   als gewonnene Aufgabe, sondern als offener Punkt für Schritt „Nur-User-Rest" unten. Nicht
   verortbar → `unavailable`.

**„Exhausted" darf nur gemeldet werden, wenn ALLE VIER Quellen (Schritte 2–4, drei Schritte, vier
Rollen) tatsächlich befragt werden KONNTEN — also `found` oder `empty`, keine einzige
`unavailable`.** Das entspricht `grounding_seed.self_knowledge.GroundingReport.all_answerable()`.
Ist mindestens eine Rolle `unavailable`, gilt NICHT „exhausted", sondern das eigene Signal „blind"
(siehe Abbruchsignal unten) — der Loop endet trotzdem (er kann ja ohnehin nichts befragen), aber er
behauptet nicht mehr, geprüft zu haben, was er nicht prüfen konnte.

Findet irgendein Schritt neue Arbeit → zurück zu Ebene 1, Arbeit erledigen, Guard-Zustand (siehe
unten) auf „found" setzen statt „exhausted"/„blind".

### Sonderfall: nur User-gebundene Reste

Wenn die Kette **keine autonome** Aufgabe mehr findet, aber `USER/*`-Tickets oder unentschiedene
`_DECISIONS`-Punkte offen sind, ist das trotzdem ein **STOP für die Autonomie** — aber nicht
„nichts zu tun", sondern „nichts *autonom* zu tun". Diese Punkte werden nach der Autonomie-Loop-Regel
aus `ticket-master` **gebündelt** vorgelegt (eine Sammelvorlage, keine Einzel-Pings), nicht einzeln
nachgefragt. Das Abbruchsignal unterscheidet diesen Fall ausdrücklich von echtem Leerstand.

## Abgrenzung — was zählt als „autonom ausführbar"?

Referenz: `ticket-master` Kategorien (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`).

| Fall | Autonom? | Begründung |
|---|---|---|
| `INBOX/` inkl. formlose Einträge, unter TICKET-MASTER (vor Triage) | **Ja, mit Vorrang** | Formalisieren/Triage ist Klerikalarbeit ohne Nutzerentscheidung — geht vor `ACTIONABLE`/`BLOCKED`/`WAITING` und blockiert bis dahin jedes Abbruchsignal (siehe Intake-Gate oben). |
| `ACTIONABLE`-Ticket | **Ja** | Kein Blocker, keine User-Abhängigkeit — per Definition. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | Nein, solange Blocker nicht **empirisch** entfallen ist | Periodischer Re-Check ist erlaubt (Autonomie-Loop), „vorhanden" reicht als Nachweis nicht — Beleg nötig. |
| `WAITING/*` (scheduled, review-due, marker) vor Termin/Marker | Nein | Zeitgebunden. |
| `WAITING/*` nach Termin/Marker-Eintritt | **Ja** | Bedingung erfüllt → zieht nach `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **Nie autonom** | Zwingend Nutzerentscheidung/-daten/-freigabe/-hardware/-sitzung. Gebündelt vorlegen, siehe oben. |
| `PARKED/*` (skip, backlog, until-trigger) | Nein, außer explizitem Auftrag/Trigger | Bewusst zurückgestellt, kein Auto-Re-Check. |
| Offene `TODO.md`/`AUFGABEN.txt`-Punkte ohne Freigabe-/Entscheidungsvermerk | **Ja** | Projektregister, normale Arbeit. |
| Fällige Routine-/Hygiene-Checks (Cooldown abgelaufen, kein Lock) | **Ja** | Reguläre Wartungsarbeit nach lokaler Policy. |
| Von `LOCK.user.*` gesperrte Bereiche | **Nie** | User-Lock — nur der Nutzer hebt ihn auf, siehe LOCK-SYSTEM. |
| Irreversible/extern wirksame Schritte ohne Policy-Freigabe (Zenodo-Upload, Push auf gejudgte/geschützte Branches, Server-Spend-Entscheidung jenseits der Laptop-Schwelle, endgültiges Löschen ohne Vorschau) | **Nein** | Braucht Freigabe/Entscheidung, auch wenn technisch ausführbar. |
| Nur per GUI/Login startbare Sitzung (z. B. Claude-Desktop-Aufgabe, interaktiver Login, physische Hardware-Handlung) | **Nie** | „Nur vom User startbare Sitzung" — kann kein Loop übernehmen. |

Faustregel: Autonom ist, was **ohne** Nutzerentscheidung, -freigabe, -daten, -hardware oder
-Sitzung zu Ende gebracht werden kann UND keine irreversible/extern wirksame Handlung ohne
dokumentierte Policy-Freigabe voraussetzt.

## Guard gegen Endlosschleifen (Pflicht)

**Problem:** Ohne Bremse würde die vierstufige Kette bei jeder erneuten Prüfung wieder komplett
laufen, obwohl sich seit dem letzten ergebnislosen Durchlauf nichts geändert hat — teuer und
witzlos, vor allem wenn der Skill wiederholt aufgerufen wird (Loop, Scheduled Task, erneuter
manueller Aufruf kurz nacheinander).

**Zustand wird in USMC persistiert** (Prozess-State gehört auf diesem System dorthin, nicht in
Markdown-Dateien):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**Fingerprint besteht aus ZWEI Bausteinen — der Lage UND der Erreichbarkeit:**

1. **Lage-Baustein** (wie bisher): Anzahl/IDs offener `ACTIONABLE`-Tickets, mtime der
   `_DECISIONS`-Kette (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), Zahl neuer
   USMC-`working`-Einträge seit dem letzten Kettendurchlauf.
2. **Verfügbarkeits-Baustein (neu, Pflicht seit 1.2.0):** das sortierte Tupel der gerade
   `unavailable` gemeldeten Rollen aus der Selbstkenntnis-Prüfung
   (`exhaustion_check.availability_fingerprint_component()`), z. B. `("memory.organic",)` oder `()`.

**Warum der zweite Baustein Pflicht ist — „der Guard erbt sonst die Lücke":** Ohne ihn stützt sich
der Fingerprint (Baustein 1) u. a. auf die mtime der `_DECISIONS`-Kette. Fehlt diese Kette auf einem
System komplett, ist dieser Anteil des Fingerprints für immer konstant — ein einmal fälschlich
gesetztes `exhausted`/`blind` würde dann NIE neu geprüft, selbst wenn später `source-resolver`
installiert oder `_control-center/_DECISIONS/` angelegt wird. Der Verfügbarkeits-Baustein behebt
das gezielt: Ändert sich, WELCHE Rollen unavailable sind (eine Quelle kommt hinzu oder fällt weg),
ändert sich der Fingerprint automatisch — der Guard erkennt es beim nächsten Aufruf und fährt die
Kette neu. Das ist „Verpflanzung" im Sinne der Grounding-Metapher (T-20260815-371628859): ein
Umgebungswechsel löst eine neue Suche aus, ohne dass irgendjemand den Guard manuell zurücksetzen
müsste.

**Ablauf vor jedem Kettendurchlauf:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```

Ein einziger vollständig ausgeführter Kettendurchlauf, bei dem ALLE VIER Quellen befragbar waren und
KEINE davon einen Treffer lieferte, reicht als Beleg für „keine autonomen Aufgaben mehr" (Ticket-
Vorgabe: „erst wenn ALLE Schritte eines Durchlaufs ergebnislos bleiben" — ergebnislos heißt hier
ausdrücklich `empty`, nicht `unavailable`). Der Guard verhindert nicht das Feststellen selbst,
sondern nur das **wiederholte, unveränderte Neu-Feststellen** bei dichten Folgeaufrufen — und zwar
für `exhausted` UND für `blind` getrennt, nie miteinander verwechselt.

`GUARD_INTERVAL` ist konfigurierbar (Default 15 Minuten) — bei sehr träger Umgebung (seltene neue
Tickets/Entscheidungen) darf länger gewählt werden, bei sehr aktiver Umgebung kürzer.

## Abbruchsignal

Jeder Durchlauf endet mit **einer** eindeutigen, grep-baren Zeile, damit ein umgebender `/loop`
oder ein künftiges `/goal`-Konstrukt daraus lesen kann, ob weitergemacht werden soll:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` ist das einzige Signal, bei dem eine übergeordnete Schleife einen weiteren Tick
anstoßen soll. Alle `STOP`-Varianten sind der belegte Abbruch — inklusive Begründung, welcher Fall
vorliegt.

**Der Unterschied zwischen `exhausted` und `blind` ist für den Nutzer wesentlich, nicht kosmetisch:**
`exhausted` heißt „ich habe alles geprüft, was zu prüfen war — die Arbeit ist fertig". `blind` heißt
„mir fehlt Infrastruktur, um überhaupt zu prüfen — das ist kein Arbeitsstand, sondern eine Lücke".
Ein `/loop`/`/goal`-Konstrukt, das beide gleich behandelt (Loop endet so oder so), darf sie dem
Nutzer nicht gleich MELDEN — sonst verschwindet genau die Information, die T-20260815-205101335
eingefordert hat.

## Verhältnis zu anderen Skills

- **`think`/`decide`** — liefern die strukturierte Analyse/Entscheidung in Kettenschritt 1. Werden
  hier als Baustein aufgerufen, nicht neu erfunden.
- **`decision-avatar`** (dieser Skill, nutzerneutral) — liefert Kettenschritt 4. Auf Systemen mit
  einem konkreten, autorisierten Profil entspricht das `user-model` + `build-your-users-mind`.
- **`orchestrator`** — regelt, WIE an Subagenten delegiert und deren Fertigmeldung geprüft wird.
  `work-autonomous` regelt WANN überhaupt aufgehört wird zu suchen; beide sind kombinierbar
  (der Orchestrator kann als Teil der in Ebene 1 erledigten Arbeit auftreten).
- **`bugsweep`** — ein Beispiel für ein anderes, sich selbst begrenzendes Suchprotokoll
  (Verdopplungs-Eskalation statt Vier-Schritt-Kette). `work-autonomous` ist generischer: Es prüft
  nicht nur Code auf Bugs, sondern jede Quelle autonomer Arbeit.
- **Ticket-Kategorien (`ticket-master`)** — liefern das Vokabular für „autonom ausführbar" (siehe
  Abgrenzungstabelle) und die Vorlage für den Autonomie-Loop (BLOCKED-Re-Check, USER-Bündelung,
  WAITING-Termin-Ziehen, PARKED-Stillstand).
- **`tidy-up`** (seit 1.3.0) — liefert eine zusätzliche Ebene-1-Quelle: den einmaligen
  Tasksolver+Writer+Maintainer-Durchlauf für den gerade bearbeiteten Projektordner. Prüft seine
  eigene Fälligkeit selbst (schlankes USMC-Log, kein Vier-Schritt-Guard wie hier) — `work-autonomous`
  ruft ihn nur als eine von mehreren Ebene-1-Quellen auf, ohne dessen Logik zu duplizieren.

## Beispielablauf

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```

## Changelog

### 1.4.0 (2026-09-03)
- Minimal-invasive Ergänzung aus Ticket T-20260902-729068782: neues
  **TICKET-MASTER-Intake-Gate** in Ebene 1 (Vorrang vor `ACTIONABLE`/`BLOCKED`/`WAITING`) — nur
  relevant, wenn ein Ticketsystem Teil des Kontexts ist. Solange `INBOX/` (inklusive formloser
  Einträge) nicht vollständig triagiert ist, darf kein `NO_WORK`/Erschöpfungssignal/Guard-STOP
  entstehen. Belegfall: ein Loop begann die Erschöpfungsprüfung, während `INBOX` noch offene
  Einträge (darunter zwei P1-Tickets) hielt. Bestehende Vier-Schritt-Erschöpfungskette, Guard und
  Nicht-TICKET-MASTER-Nutzbarkeit unverändert erhalten — das Gate wirkt ausschließlich in Ebene 1
  und nur unter TICKET-MASTER.
- Neue, getestete Hilfsfunktion `scripts/exhaustion_check.py::intake_gate_blocks_stop()` +
  Regressionstests in `tests/test_exhaustion_check.py` (verhaltensbezogen: Gate blockiert bei
  offener INBOX, gibt frei bei leerer INBOX).

### 1.3.0 (2026-08-19)
- Minimal-invasive Ergänzung aus Ticket T-20260819-461890468 (neuer Skill `tidy-up`): Ebene 1
  bekommt eine zusätzliche, eigenständige Quelle — „fällige `tidy-up`-Läufe des aktiven Projekts"
  (Tasksolver+Writer+Maintainer-Durchlauf, siehe Skill `tidy-up`). Kein neuer Kettenschritt, keine
  Änderung an Ebene 2/Guard/Abbruchsignal — `tidy-up` prüft seine eigene Fälligkeit selbst über ein
  schlankes USMC-Log und wird hier nur als weitere Ebene-1-Quelle referenziert, analog zu den
  bereits bestehenden Quellen (Tickets, TODO/AUFGABEN, Routine-Checks, USMC `working`). Damit
  zählen `tidy-up`-Punkte als autonom auszuführende Aufgabe im Sinne eines `/goal`-Konstrukts, das
  `/work-autonomous` + `/tidy-up` kombiniert (Kern-Usecase des Tickets). Kein Eingriff in die
  Vier-Schritt-Erschöpfungskette oder den Guard — Ebene 2 bleibt unverändert.

### 1.2.0 (2026-08-15)
- Retrofit aus Ticket T-20260815-205101335 (Prüfauftrag: „prüfe ob die Lösung dort in Verbindung
  mit der Grounding-Metapher trägt", Befund am ausgelieferten Skill: sie trug in drei Punkten, aber
  NICHT in der Unterscheidung „befragt und leer" vs. „konnte gar nicht befragt werden" — Kette
  meldete `STOP (exhausted)` auch auf Systemen ohne Gardener/USMC/`_DECISIONS`, ohne das je geprüft
  zu haben. Erster echter Anwendungsfall von `grounding-seed`, Ticket T-20260815-371628859).
- **Selbstkenntnis ergänzt:** vier deklarierte Bedarfe (`decisions.ledger`, `memory.organic`,
  `memory.curated`, `user.model`) vor der Kette, statt an vier fest benannten Orten blind zu suchen.
- **Jeder Kettenschritt (2–4) meldet found | empty | unavailable** statt eines binären Ergebnisses
  — zweistufig: Verortung zuerst (`grounding-seed`/`source-resolver` für `decisions.ledger`/
  `user.model`, direkter CLI-Check für `memory.organic`/`memory.curated`, die noch keinen
  `source-resolver`-Provider haben), Inhaltsprüfung nur bei erfolgreicher Verortung.
- **`exhausted` gilt nur noch, wenn alle vier Quellen tatsächlich befragbar waren** (alle
  found/empty, keine unavailable). Neues, unterscheidbares Signal `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` für den Fall, dass mindestens eine Quelle nicht erreichbar war — der Loop endet
  trotzdem, behauptet aber kein geprüftes Ergebnis mehr.
- **Guard-Fingerprint um einen Verfügbarkeits-Baustein erweitert** (sortiertes Tupel der gerade
  unavailable-Rollen). Behebt den Folgebefund „der Guard erbt die Lücke": ohne diesen Baustein
  bleibt ein einmal fälschlich gesetztes `exhausted`/`blind` für immer gültig, wenn die
  `_DECISIONS`-Kette komplett fehlt (der bisherige Fingerprint-Anteil ist dann konstant). Mit dem
  Baustein löst eine neu verfügbar gewordene Quelle automatisch einen erneuten Kettendurchlauf aus
  (Verpflanzung im Sinne der Grounding-Metapher).
- Neues, getestetes Hilfsskript `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`,
  11 Tests, beide Betriebsarten geprüft: mit und ohne installiertes `grounding-seed`) — liefert die
  Selbstkenntnis-/Verortungsprüfung deterministisch, damit der Skill sie nicht bei jedem Lauf neu
  erraten muss. Bleibt optional: Der Skill ist weiterhin primär ein Protokoll, das ein Modell mit
  seinen eigenen Werkzeugen befolgt.
- Abhängigkeit: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` seit
  `grounding-seed` 0.2.0 — ältere `grounding-seed`-Stände (0.1.0) hatten einen Kategorienfehler
  (`not_found` wurde fälschlich zu `empty`), der genau die hier behobene Unterscheidung wieder
  verwischt hätte. Ohne installiertes `grounding-seed` läuft der dokumentierte Fallback identisch.

### 1.1.0 (2026-08-15)
- Referenz-Retrofit aus Ticket T-20260815-385400870: Schritt 2 (Entscheidungsregister) löst
  seinen Ort jetzt über die Rolle `decisions.ledger` auf (`source_resolver.resolve(...)`, Modul
  `source-resolver`), statt ihn hart zu verdrahten — mit dokumentiertem Fallback auf den bisherigen
  Pfad, falls der Resolver nicht installiert ist. Funktionsverhalten unverändert.

### 1.0.0 (2026-08-15)
- Erstversion aus Ticket T-20260815-522639345: Zwei-Ebenen-Betriebsmodell, Vier-Schritt-Prüfkette,
  Abgrenzungstabelle nach `ticket-master`-Kategorien, USMC-gestützter Guard gegen Endlosschleifen,
  eindeutiges Abbruchsignal für `/loop`/`/goal`-Konstruktionen.
